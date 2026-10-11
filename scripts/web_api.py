"""Local JSON bridge for the Next.js demo frontend (stdlib only, local use).

Reuses the CLI workflow unchanged: no policy logic lives here or in the frontend.
Run from the project root:  uv run --frozen python scripts/web_api.py
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import uuid
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'src'))

from dotenv import load_dotenv  # noqa: E402

from policy_agent.cli import configurations, dump, manifest, start_snapshot  # noqa: E402
from policy_agent.corpus import Corpus  # noqa: E402
from policy_agent.providers import Budget, Provider  # noqa: E402
from policy_agent.workflow import Workflow, replay  # noqa: E402

load_dotenv(ROOT / '.env', override=False)

PORT = int(os.environ.get('WEB_API_PORT', '8790'))
# Demo-only ledger, separate from the evaluation ledger (runs/budget.json).
MAX_COST_USD = float(os.environ.get('WEB_MAX_COST_USD', '20'))
LEDGER = os.environ.get('WEB_LEDGER', 'runs/web-budget.json')
MATRICES = ['config/development-default.json', 'config/eval-models-high.json']
# Best observed configuration per docs/model_selection.md (Stage 5).
DEFAULT_CONFIG_ID = os.environ.get('WEB_DEFAULT_CONFIG', 'anthropic/claude-sonnet-5-5/adaptive/medium')
TRANSCRIPT = next(Path('exam').glob('*Transcript*.txt'))

CORPUS = Corpus()
SESSIONS: dict[str, dict] = {}
SESSIONS_LOCK = threading.Lock()


def model_configs() -> list[dict]:
    seen, out = set(), []
    for matrix in MATRICES:
        for c in configurations(matrix):
            cid = c.get('config_id', c['model'])
            if cid not in seen:
                seen.add(cid)
                out.append({**c, 'config_id': cid, 'matrix': matrix})
    out.sort(key=lambda c: c['config_id'] != DEFAULT_CONFIG_ID)  # default first
    return out


def find_config(config_id: str | None) -> dict:
    configs = model_configs()
    if not config_id:
        return configs[0]
    for c in configs:
        if c['config_id'] == config_id:
            return c
    raise ValueError('Unknown config_id')


def key_present(provider: str) -> bool:
    return bool(os.environ.get('OPENAI_API_KEY' if provider == 'openai' else 'ANTHROPIC_API_KEY'))


def new_run_dir(prefix: str) -> Path:
    out = Path('runs') / f"{prefix}-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    out.mkdir(parents=True, exist_ok=False)
    return out


def persist(out: Path, snapshot: dict, provider, budget, results: list[dict], mode: str):
    (out / 'turns.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in results))
    dump(out / 'summary.json', {'turns': len(results), 'technical_failures': sum(bool(r['error']) for r in results),
                                'mode': mode, 'source': 'web_demo'})
    dump(out / 'manifest.json', manifest(snapshot, [provider] if provider else [], budget, mode))


def call_summary(provider) -> dict:
    calls = provider.calls if provider else []
    return {'calls': len(calls), 'estimated_cost_usd': round(sum(c.get('cost_usd', 0) for c in calls), 6)}



# ---- handlers -------------------------------------------------------------

def get_status(_body):
    budget = Budget(MAX_COST_USD, LEDGER)
    return {
        'corpus_entries': len(CORPUS.entries), 'corpus_version': CORPUS.version,
        'keys': {'openai': key_present('openai'), 'anthropic': key_present('anthropic')},
        'ledger_spent_usd': round(budget.spent, 4), 'ledger_limit_usd': MAX_COST_USD,
        'models': [{'config_id': c['config_id'], 'provider': c['provider'], 'model': c['model'],
                    'key_present': key_present(c['provider'])} for c in model_configs()],
        'default_config_id': model_configs()[0]['config_id'],
        'today': date.today().isoformat(),
    }


def get_corpus(_body):
    return {'entries': [e.model_dump(mode='json') for e in CORPUS.entries.values()]}


def post_session(body):
    config = find_config(body.get('config_id'))
    if not key_present(config['provider']):
        raise ValueError(f"No API key for provider {config['provider']} in .env")
    context = dict(body.get('context') or {})
    context.setdefault('request_date', body.get('date') or date.today().isoformat())
    budget = Budget(MAX_COST_USD, LEDGER)
    provider = Provider(config, budget)
    flow = Workflow(CORPUS, provider, context)
    sid = uuid.uuid4().hex
    out = new_run_dir('web-chat')
    snapshot = start_snapshot(CORPUS, config["matrix"])
    with SESSIONS_LOCK:
        SESSIONS[sid] = {'flow': flow, 'provider': provider, 'budget': budget, 'out': out,
                         'snapshot': snapshot, 'lock': threading.Lock(), 'config': config}
    return {'session_id': sid, 'config_id': config['config_id'], 'context': flow.context.model_dump(mode='json'),
            'run_dir': str(out)}


def post_turn(body):
    session = SESSIONS.get(body.get('session_id', ''))
    if not session:
        raise LookupError('Unknown session; start a new conversation')
    text = (body.get('text') or '').strip()
    if not text:
        raise ValueError('Empty message')
    with session['lock']:
        started = time.perf_counter()
        result = session['flow'].turn(text)
        persist(session['out'], session['snapshot'], session['provider'], session['budget'],
                session['flow'].results, 'live')
    return {'result': result, 'wall_seconds': round(time.perf_counter() - started, 3),
            'usage': call_summary(session['provider'])}


def post_replay(body):
    live = body.get('mode') == 'live'
    provider, budget, matrix = None, Budget(MAX_COST_USD, LEDGER), MATRICES[0]
    if live:
        config = find_config(body.get('config_id'))
        if not key_present(config['provider']):
            raise ValueError(f"No API key for provider {config['provider']} in .env")
        provider, matrix = Provider(config, budget), config["matrix"]
    snapshot = start_snapshot(CORPUS, matrix)
    results = replay(TRANSCRIPT, provider, CORPUS)
    mode = 'live' if live else 'offline_fixture'
    out = new_run_dir('web-replay')
    persist(out, snapshot, provider, budget, results, mode)
    return {'mode': mode, 'run_dir': str(out), 'turns': results, 'usage': call_summary(provider),
            'transcript': TRANSCRIPT.read_text()}


def get_runs(_body):
    runs = []
    for d in sorted(Path('runs').iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        turns = d / 'turns.jsonl'
        if not d.is_dir() or not turns.exists():
            continue
        with turns.open() as f:
            first = f.readline()
        try:
            if 'turn' not in json.loads(first):
                continue  # evaluation traces use a per-case layout
        except json.JSONDecodeError:
            continue
        info = {'name': d.name, 'modified': d.stat().st_mtime}
        m = d / 'manifest.json'
        if m.exists():
            data = json.loads(m.read_text())
            info.update(mode=data.get('mode'), models=[x.get('config_id', x.get('model')) for x in data.get('models', [])],
                        prompt_version=data.get('prompt_version'))
        runs.append(info)
    return {'runs': runs}


def get_run(name: str):
    d = (Path('runs') / name).resolve()
    if d.parent != (ROOT / 'runs').resolve() or not (d / 'turns.jsonl').exists():
        raise LookupError('Run not found')
    turns = [json.loads(line) for line in (d / 'turns.jsonl').read_text().splitlines() if line.strip()]
    m = d / 'manifest.json'
    meta = json.loads(m.read_text()) if m.exists() else {}
    return {'name': name, 'turns': turns,
            'manifest': {k: meta.get(k) for k in ('mode', 'prompt_version', 'code_sha256', 'created_at', 'ledger_total_usd')},
            'models': [x.get('config_id', x.get('model')) for x in meta.get('models', [])],
            'usage': {'calls': len(meta.get('calls', [])),
                      'estimated_cost_usd': round(sum(c.get('cost_usd', 0) for c in meta.get('calls', [])), 6)}}


ROUTES = {
    ('GET', '/status'): get_status,
    ('GET', '/corpus'): get_corpus,
    ('GET', '/runs'): get_runs,
    ('POST', '/session'): post_session,
    ('POST', '/turn'): post_turn,
    ('POST', '/replay'): post_replay,
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload):
        data = json.dumps(payload, ensure_ascii=False, default=str).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _dispatch(self, method: str):
        path = self.path.split('?', 1)[0].rstrip('/') or '/'
        body = {}
        if method == 'POST':
            length = int(self.headers.get('Content-Length') or 0)
            body = json.loads(self.rfile.read(length) or b'{}')
        try:
            if method == 'GET' and path.startswith('/runs/'):
                return self._send(200, get_run(path[len('/runs/'):]))
            handler = ROUTES.get((method, path))
            if not handler:
                return self._send(404, {'error': 'Not found'})
            self._send(200, handler(body))
        except LookupError as exc:
            self._send(404, {'error': str(exc)})
        except ValueError as exc:
            self._send(400, {'error': str(exc)})
        except Exception as exc:  # never echo SDK messages: they can contain request data
            self._send(500, {'error': type(exc).__name__})

    def do_GET(self):
        self._dispatch('GET')

    def do_POST(self):
        self._dispatch('POST')


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    print(f'Policy agent web API on http://127.0.0.1:{PORT} (ledger cap US${MAX_COST_USD})', flush=True)
    server.serve_forever()
