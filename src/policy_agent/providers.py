"""Native provider adapters with conservative, persistent budget accounting."""
from __future__ import annotations

import json
import math
import os
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from threading import RLock
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)


class ProviderError(RuntimeError):
    """Sanitized provider failure; never contains a server response or credential."""


class BudgetExceeded(ProviderError):
    pass


class Budget:
    """Reserve before calling; unknown billable failures retain their reservation.

    A ledger path can be shared across processes on macOS/Linux. ``spent`` includes
    pending and unknown charges, so it is an upper-bound estimate, not a bill.
    """
    def __init__(self, limit: float = 5, path: str | Path | None = None):
        if not math.isfinite(limit) or limit <= 0:
            raise ValueError('Budget limit must be positive and finite')
        self.limit = float(limit)
        self.path = Path(path) if path else None
        self._entries: dict = {}
        self._mutex = RLock()

    @contextmanager
    def _locked(self):
        with self._mutex:
            if self.path is None:
                yield self._entries
                return
            import fcntl
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.with_suffix(self.path.suffix + '.lock').open('a+') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                try:
                    entries = json.loads(self.path.read_text()) if self.path.exists() else {}
                    yield entries
                    temporary = self.path.with_name(self.path.name + '.' + uuid.uuid4().hex + '.tmp')
                    temporary.write_text(json.dumps(entries, indent=2))
                    temporary.replace(self.path)
                finally:
                    fcntl.flock(lock, fcntl.LOCK_UN)

    @property
    def spent(self) -> float:
        with self._locked() as entries:
            return sum(item['cost_usd'] for item in entries.values())

    def reserve(self, amount: float) -> str:
        if not math.isfinite(amount) or amount < 0:
            raise ValueError('Invalid reservation')
        with self._locked() as entries:
            if sum(item['cost_usd'] for item in entries.values()) + amount > self.limit:
                raise BudgetExceeded('Budget exhausted before API request')
            key = uuid.uuid4().hex
            entries[key] = {'cost_usd': amount, 'status': 'reserved_or_unknown'}
            return key

    def settle(self, key: str, actual: float):
        with self._locked() as entries:
            entries[key] = {'cost_usd': actual, 'status': 'usage_reported'}


def strict_schema(schema: dict) -> dict:
    """Make object requirements explicit for both providers' JSON Schema subset."""
    schema = json.loads(json.dumps(schema))
    def visit(node):
        if isinstance(node, dict):
            node.pop('default', None)
            if node.get('type') == 'object':
                node['additionalProperties'] = False
                node['required'] = list(node.get('properties', {}))
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)
    visit(schema)
    return schema


class Provider:
    def __init__(self, config: dict, budget: Budget, client=None):
        self.config = dict(config)
        self.budget = budget
        self.calls: list[dict] = []
        self.name = config['provider']
        if self.name not in ('openai', 'anthropic'):
            raise ValueError('Unknown provider')
        for field in ('input_per_million', 'output_per_million', 'cached_input_per_million'):
            value = config.get(field)
            if value is None or not math.isfinite(float(value)) or float(value) < 0:
                raise ValueError('Known, finite pricing is required before API calls')
        for field in ('cache_write_per_million',):
            if field in config and (not math.isfinite(float(config[field])) or float(config[field]) < 0):
                raise ValueError('Invalid cache-write pricing')
        self.client = client

    def _client(self):
        if self.client is None:
            # Explicit official defaults prevent ambient SDK endpoint variables from
            # forwarding keys to a proxy unintentionally.
            if self.name == 'openai':
                from openai import OpenAI
                self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'),
                    base_url=self.config.get('base_url', 'https://api.openai.com/v1'),
                    max_retries=0, timeout=90)
            else:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'),
                    base_url=self.config.get('base_url', 'https://api.anthropic.com'),
                    max_retries=0, timeout=90)
        return self.client

    def _usage(self, response) -> dict:
        u = response.usage
        cached = int(getattr(u, 'cache_read_input_tokens', 0) or 0)
        writes = int(getattr(u, 'cache_creation_input_tokens', 0) or 0)
        incoming = int(u.input_tokens)
        if self.name == 'openai':
            cached = int(getattr(getattr(u, 'input_tokens_details', None), 'cached_tokens', 0) or 0)
            writes = int(getattr(getattr(u, 'input_tokens_details', None), 'cache_write_tokens', 0) or 0)
            incoming -= cached + writes
        output = int(u.output_tokens)
        # OpenAI totals include reads/writes; Anthropic reports these separately.
        # No explicit Anthropic cache TTL is enabled; retain the conservative
        # one-hour multiplier if the service nevertheless reports writes.
        write_rate = self.config.get('cache_write_per_million',
                                     self.config['input_per_million'] * (2 if self.name == 'anthropic' else 1.25))
        if min(incoming, cached, writes, output) < 0:
            raise ProviderError('Inconsistent provider token usage')
        cost = (incoming * self.config['input_per_million'] +
                cached * self.config['cached_input_per_million'] +
                writes * write_rate +
                output * self.config['output_per_million']) / 1_000_000
        return {'input_tokens': incoming + cached + writes, 'uncached_input_tokens': incoming,
                'cached_input_tokens': cached, 'cache_write_tokens': writes,
                'output_tokens': output, 'cost_usd': cost}

    def generate(self, schema: type[T], system: str, payload: dict) -> T:
        shape = strict_schema(schema.model_json_schema())
        original = json.dumps(payload, ensure_ascii=False)
        for repair in range(2):
            text = original + ('\nReturn valid JSON conforming exactly to the supplied schema. Previous output failed validation.' if repair else '')
            response = self._request(system, text, shape, repair)
            if self.name == 'openai':
                if getattr(response, 'status', 'completed') != 'completed':
                    self.calls[-1]['error'] = 'IncompleteResponse'
                    raise ProviderError('Provider response incomplete')
                raw = response.output_text
            else:
                if response.stop_reason != 'end_turn':
                    self.calls[-1]['error'] = 'IncompleteOrRefusedResponse'
                    raise ProviderError('Provider response incomplete or refused')
                raw = ''.join(block.text for block in response.content if block.type == 'text')
            if not raw:
                self.calls[-1]['error'] = 'EmptyStructuredResponse'
                raise ProviderError('Provider returned no structured text')
            try:
                return schema.model_validate_json(raw)
            except (ValidationError, ValueError):
                self.calls[-1]['validation_error'] = True
                if repair:
                    raise ProviderError('Structured output failed validation after one repair') from None
        raise AssertionError('Unreachable')

    def _request(self, system, text, shape, repair):
        client = self._client()
        # UTF-8 bytes (not chars/4) overestimates token count for our text-only
        # requests, with explicit room for provider framing and schema overhead.
        upper_input = len((system + text + json.dumps(shape)).encode()) + 4096
        if upper_input > self.config.get('max_input_token_bound', 90000):
            raise ProviderError('Input exceeds configured pricing/context bound')
        max_output = self.config.get('max_output_tokens', 2048)
        write_rate = self.config.get('cache_write_per_million',
                                     self.config['input_per_million'] * (2 if self.name == 'anthropic' else 1.25))
        reservation = (upper_input * max(self.config['input_per_million'], write_rate, self.config['cached_input_per_million']) + max_output * self.config['output_per_million']) / 1_000_000
        for attempt in range(3):
            key = self.budget.reserve(reservation)
            start = time.monotonic()
            record = {'provider': self.name, 'model': self.config['model'],
                      'config_id': self.config.get('config_id', self.name + '/' + self.config['model']), 'attempt': attempt,
                      'repair': repair, 'cost_usd': reservation, 'cost_status': 'reserved_or_unknown'}
            try:
                if self.name == 'openai':
                    options = {'model': self.config['model'], 'instructions': system, 'input': text,
                        'max_output_tokens': max_output, 'store': False, 'service_tier': 'default',
                        'text': {'format': {'type': 'json_schema', 'name': 'decision', 'strict': True, 'schema': shape}}}
                    if 'reasoning_effort' in self.config:
                        options['reasoning'] = {'effort': self.config['reasoning_effort']}
                    response = client.responses.create(**options)
                else:
                    options = {'model': self.config['model'], 'system': system,
                        'messages': [{'role': 'user', 'content': text}], 'max_tokens': max_output, 'service_tier': 'standard_only',
                        'output_config': {'format': {'type': 'json_schema', 'schema': shape}}}
                    if 'effort' in self.config:
                        options['output_config']['effort'] = self.config['effort']
                    if 'thinking' in self.config:
                        options['thinking'] = self.config['thinking']
                    response = client.messages.create(**options)
                usage = self._usage(response)
                self.budget.settle(key, usage['cost_usd'])
                record.update(usage, cost_status='usage_reported', response_model=getattr(response, 'model', self.config['model']))
                for field, attr in [('response_id', 'id'), ('request_id', '_request_id')]:
                    value = getattr(response, attr, None)
                    if isinstance(value, str):
                        record[field] = value
                return response
            except Exception as exc:
                code = getattr(exc, 'status_code', None)
                kind = type(exc).__name__
                record.update(error=kind, status_code=code)
                transient = code in (408, 409, 429) or (isinstance(code, int) and code >= 500) or kind in ('APITimeoutError', 'APIConnectionError')
                if not transient or attempt == 2:
                    raise ProviderError(f'{self.name} request failed: {kind}' + (f' ({code})' if code else '')) from None
                time.sleep(min(2 ** attempt, 4))
            finally:
                record['latency_seconds'] = time.monotonic() - start
                self.calls.append(record)
