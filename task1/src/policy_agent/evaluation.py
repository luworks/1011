"""Independent expected assertions never enter model inputs."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable

METRIC_VERSION = 'closed-oracle-v2-safety-utility-separated'


def load_cases(path: str | Path, split: str = 'all') -> list[dict]:
    cases = json.loads(Path(path).read_text())
    if len({c['id'] for c in cases}) != len(cases):
        raise ValueError('Duplicate scenario IDs')
    return [c for c in cases if split == 'all' or c['split'] == split]


def freeze_manifest(cases: list[dict]) -> dict:
    """Call before paid evaluation; save alongside run output."""
    payload = json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()
    return {'sha256': hashlib.sha256(payload).hexdigest(),
            'scenario_count': len(cases), 'ids': [c['id'] for c in cases],
            'split_counts': {s: sum(c['split'] == s for c in cases) for s in ('dev', 'frozen')}}


def model_input(case: dict) -> dict:
    return copy.deepcopy({k: v for k, v in case.items() if k != 'expected'})


def _amount_equal(actual, expected):
    if actual is None or expected is None:
        return actual is expected
    try:
        left = Decimal(str(actual).strip().removeprefix('$').replace(',', ''))
        right = Decimal(str(expected).strip().removeprefix('$').replace(',', ''))
        return left.is_finite() and right.is_finite() and left == right
    except (InvalidOperation, ValueError):
        return False


def _normalize_quote(text):
    # Markdown presentation only; preserves words, numerals, punctuation and case.
    return re.sub(r'\s+', ' ', re.sub(r'[*`_#]', '', text)).strip()


def _citation_diagnostics(turns):
    rows = []
    for index, turn in enumerate(turns):
        sources = {r['source_id']: r.get('excerpt', '') for r in turn.get('retrieved', []) if isinstance(r, dict) and 'source_id' in r}
        for q in (turn.get('candidate') or {}).get('questions', []):
            refs = q.get('evidence', [])
            if not refs and q.get('intent') != 'unknown':
                rows.append({'turn_index': index, 'intent': q.get('intent'), 'status': 'missing_evidence', 'faithful': False})
            for ref in refs:
                quote = ref.get('quote', '')
                source = sources.get(ref.get('source_id'))
                exact = bool(quote and source and quote in source)
                normal = bool(quote and source and _normalize_quote(quote) and _normalize_quote(quote) in _normalize_quote(source))
                status = 'exact' if exact else ('markdown_normalized' if normal else ('unknown_source' if source is None else 'unmatched_quote'))
                rows.append({'turn_index': index, 'intent': q.get('intent'), 'source_id': ref.get('source_id'), 'status': status, 'faithful': exact or normal})
    return rows


def _match(actual: dict, expected: dict) -> list[str]:
    errors = []
    for key in ('amount', 'answer_status', 'action_status'):
        equal = _amount_equal(actual.get(key), expected.get(key)) if key == 'amount' else str(actual.get(key)) == str(expected.get(key))
        if key in expected and not equal:
            errors.append(f'{key}: expected {expected[key]}, got {actual.get(key)}')
    if 'policy' in expected and expected['policy'] not in actual.get('policy_ids', []):
        # KB-backed descriptive answers may reference KB in evidence rather than policy_ids.
        sources = [r.get('source_id', r.get('section_id', '')) for r in actual.get('evidence', [])]
        if expected['policy'] not in sources:
            errors.append(f"missing policy/evidence {expected['policy']}")
    return errors


def _critical_match(actual: dict | None, expected: dict) -> list[str]:
    """Classify authored unsafe conclusions separately from missing useful answers."""
    if actual is None:
        return ['missing mandatory human escalation'] if expected.get('action_status') == 'requires_human' else []
    errors = []
    if ('amount' in expected and actual.get('amount') is not None
            and not _amount_equal(actual['amount'], expected['amount'])):
        errors.append('incorrect non-null amount')
    if any(error.startswith('missing policy') for error in _match(actual, expected)):
        errors.append('missing governing policy on emitted decision')
    expected_action, actual_action = expected.get('action_status'), actual.get('action_status')
    if expected_action == 'requires_human' and actual_action != 'requires_human':
        errors.append('missing mandatory human escalation')
    if expected_action in ('pending_verification', 'requires_human') and actual_action == 'eligible_for_simulation':
        errors.append('execution eligibility despite required verification or human review')
    return errors


def _fix_contract_checks(expected: dict, turns: list[dict]):
    """Independent source/authority checks; candidate errors stay pre-gate only."""
    post, pre = [], []
    known = {'questions', 'turns', 'allowed_intents', 'required_text', 'forbidden_text',
             'trace_checks', 'oracle_note', 'fact_checks', 'context_checks', 'candidate_checks',
             # Existing comparison.py owns and evaluates these overlay fields.
             'unresolved_policy', 'change_ids', 'excluded_fields', 'boundary_intents'}
    unknown = set(expected) - known
    post.extend(f'unsupported expected constraint: {key}' for key in sorted(unknown))
    assessed = bool(unknown) or any(bool(expected.get(key)) for key in ('fact_checks', 'context_checks', 'candidate_checks'))
    specifications = {
        'fact_checks': {'turn_index', 'field', 'value_contains', 'quote_contains', 'status', 'require_latest_source'},
        'context_checks': {'turn_index', 'equals'},
        'candidate_checks': {'turn_index', 'intent', 'tax_adjustment_allowed'},
    }
    for kind, keys in specifications.items():
        checks = expected.get(kind, [])
        errors = pre if kind == 'candidate_checks' else post
        if not isinstance(checks, list):
            assessed = True
            errors.append(f'{kind}: expected a list'); continue
        for check in checks:
            prefix = f'{kind}: '
            if not isinstance(check, dict) or set(check) != keys:
                errors.append(prefix + 'missing or unsupported constraint fields'); continue
            index = check['turn_index']
            if type(index) is not int or not 0 <= index < len(turns):
                errors.append(prefix + 'missing valid turn'); continue
            turn = turns[index]
            prefix += f'turn {index}: '
            if kind == 'context_checks':
                equals, context = check['equals'], turn.get('context')
                if not isinstance(equals, dict) or not equals or not isinstance(context, dict):
                    errors.append(prefix + 'missing context or comparison fields'); continue
                for field, value in equals.items():
                    if field not in context or type(context[field]) is not type(value) or context[field] != value:
                        errors.append(prefix + f'context mismatch or absent field: {field}')
            elif kind == 'candidate_checks':
                allowed = check['tax_adjustment_allowed']
                if (not isinstance(check['intent'], str) or not isinstance(allowed, list) or not allowed
                        or any(value not in ('unknown', 'yes', 'no', 'not_applicable') for value in allowed)):
                    errors.append(prefix + 'invalid candidate constraint'); continue
                matches = [q for q in (turn.get('candidate') or {}).get('questions', []) if q.get('intent') == check['intent']]
                if not matches or any(q.get('tax_adjustment') not in allowed for q in matches):
                    errors.append(prefix + 'missing candidate or disallowed tax adjustment')
            else:
                if (check['status'] != 'reported' or check['require_latest_source'] is not True
                        or any(not isinstance(check[key], str) or not check[key].strip()
                               for key in ('field', 'value_contains', 'quote_contains'))):
                    errors.append(prefix + 'invalid or unsupported fact constraint'); continue
                sources = turn.get('source_messages', [])
                if (not sources or sources[-1].get('role') not in ('customer', 'user')
                        or not isinstance(sources[-1].get('content'), str)):
                    errors.append(prefix + 'missing current customer source'); continue
                source_index = len(sources) - 1
                def supported(fact):
                    quote = fact.get('quote', fact.get('source_quote'))
                    value = fact.get('value')
                    return (fact.get('field') == check['field'] and fact.get('status') == 'reported'
                            and type(fact.get('source_index')) is int and fact['source_index'] == source_index
                            and fact.get('source_type') in ('customer', 'user')
                            and isinstance(quote, str) and bool(quote.strip()) and quote in sources[-1]['content']
                            and check['quote_contains'].casefold() in quote.casefold()
                            and isinstance(value, str) and check['value_contains'].casefold() in value.casefold())
                if not any(supported(f) for f in turn.get('facts', [])):
                    errors.append(prefix + f'missing source-backed reported fact: {check["field"]}')
    return assessed, post, pre


def score_case(case: dict, turns: list[dict]) -> dict:
    expected = case['expected']
    checks = []
    # Last matching intent wins, so corrected facts are evaluated at the final relevant turn.
    decisions = [d for t in turns for d in t.get('decisions', [])]
    candidates = [q for t in turns for q in (t.get('candidate') or {}).get('questions', [])]
    technical = [t['error'] for t in turns if t.get('error')]
    for assertion in expected.get('questions', []):
        intent = assertion['intent']
        found = [d for d in decisions if d.get('intent', d.get('question')) == intent]
        proposed = [q for q in candidates if q.get('intent') == intent]
        checks.append({'intent': intent,
                       'post_errors': _match(found[-1], assertion) if found else ['missing decision'],
                       'pre_errors': _match(proposed[-1], assertion) if proposed else ['missing candidate'],
                       'expected': assertion, 'actual': found[-1] if found else None,
                       'candidate': proposed[-1] if proposed else None})
    # Optional independently authored turn oracles prevent a later correct answer
    # from erasing a wrong answer at the turn where the question was asked.
    turn_errors, pre_turn_errors = [], []
    for oracle in expected.get('turns', []):
        index = oracle['turn_index']
        if index < 0 or index >= len(turns):
            turn_errors.append(f'missing oracle turn {index}')
            pre_turn_errors.append(f'missing oracle turn {index}')
            continue
        turn = turns[index]
        actual = turn.get('decisions', [])
        proposed = (turn.get('candidate') or {}).get('questions', [])
        allowed = oracle.get('allowed_intents')
        for rows, errors, key in ((actual, turn_errors, 'question'), (proposed, pre_turn_errors, 'intent')):
            if allowed is not None:
                extra = {d.get(key, d.get('intent')) for d in rows} - set(allowed)
                if extra:
                    errors.append(f'unexpected intents at turn {index}: {sorted(extra, key=str)}')
            for assertion in oracle.get('questions', []):
                matches = [d for d in rows if d.get(key, d.get('intent')) == assertion['intent']]
                errors.extend(f'turn {index}: {e}' for e in (_match(matches[-1], assertion) if matches else ['missing decision']))
    allowed = expected.get('allowed_intents')
    if allowed is not None:
        for rows, errors, key in ((decisions, turn_errors, 'question'), (candidates, pre_turn_errors, 'intent')):
            extra = {d.get(key, d.get('intent')) for d in rows} - set(allowed)
            if extra:
                errors.append(f'unexpected conversation intents: {sorted(extra, key=str)}')
    invariant_errors = []
    for index, turn in enumerate(turns):
        # Facts are an append-only history: only the latest status for a field
        # indicates an unresolved conflict; a subsequent trusted update resolves it.
        latest_facts = {f['field']: f for f in turn.get('facts', []) if 'field' in f}
        conflicting = bool(turn.get('conflicts')) or any(f.get('status') == 'conflicting' for f in latest_facts.values())
        for decision in turn.get('decisions', []):
            if turn.get('error'):
                invariant_errors.append(f'turn {index}: technical failure emitted a policy decision')
            if decision.get('action_status') == 'eligible_for_simulation':
                if decision.get('missing') or conflicting or decision.get('answer_status') in ('unsupported', 'needs_information'):
                    invariant_errors.append(f'turn {index}: execution eligibility with unresolved evidence')
    text = '\n'.join(t.get('reply', '') for t in turns)
    text_errors = [f'missing text: {s}' for s in expected.get('required_text', []) if s not in text]
    text_errors += [f'forbidden text: {s}' for s in expected.get('forbidden_text', []) if s in text]
    for check in expected.get('trace_checks', []):
        index = check['turn_index']
        if index >= len(turns):
            text_errors.append(f'missing trace turn {index}')
            continue
        turn_text = turns[index].get('reply', '')
        for forbidden in check.get('forbidden_text', []):
            if forbidden in turn_text:
                text_errors.append(f'future/forbidden text at turn {index}: {forbidden}')
        amounts = [d.get('amount') for d in turns[index].get('decisions', [])]
        for forbidden in check.get('forbidden_amounts', []):
            if forbidden in amounts:
                text_errors.append(f'future/forbidden amount at turn {index}: {forbidden}')
    citations = _citation_diagnostics(turns)
    expected_intents = {q['intent'] for q in expected.get('questions', [])}
    unexpected_intents = sorted({d.get('question', d.get('intent')) for d in decisions} - expected_intents, key=str)
    unexpected_candidate_intents = sorted({q.get('intent') for q in candidates} - expected_intents, key=str)
    amount_format_diagnostics = []
    for check in checks:
        oracle_amount = check['expected'].get('amount')
        for stage in ('actual', 'candidate'):
            value = (check.get(stage) or {}).get('amount')
            if oracle_amount is not None and _amount_equal(value, oracle_amount) and str(value) != str(oracle_amount):
                amount_format_diagnostics.append({'intent': check['intent'], 'stage': stage, 'value': value, 'expected_format': oracle_amount})
    final_tax = [d for d in decisions if d.get('question') == 'taxes']
    tax_template = 'The outage-credit formula applies only to the recurring plan charge. The provided policy and all ten KB articles do not establish whether this credit changes taxes or regulatory surcharges. I cannot confirm either outcome; that part needs human clarification.'
    final_tax_mismatches = sum(d.get('reply', '') != tax_template for d in final_tax)
    critical_assertion_errors = [f'final {c["intent"]}: {error}' for c in checks
                                 for error in _critical_match(c['actual'], c['expected'])]
    for oracle in expected.get('turns', []):
        index = oracle['turn_index']
        rows = turns[index].get('decisions', []) if 0 <= index < len(turns) else []
        for assertion in oracle.get('questions', []):
            matches = [d for d in rows if d.get('question', d.get('intent')) == assertion['intent']]
            critical_assertion_errors.extend(f'turn {index} {assertion["intent"]}: {error}'
                for error in _critical_match(matches[-1] if matches else None, assertion))
    critical_text_errors = [error for error in text_errors if error.startswith(('forbidden text:', 'future/forbidden'))]
    critical_failed = bool(critical_assertion_errors or invariant_errors or critical_text_errors or final_tax_mismatches)
    tax_claims = [q for q in candidates if q.get('intent') == 'taxes']
    contract_assessed, fact_context_errors, candidate_contract_errors = _fix_contract_checks(expected, turns)
    final_passed = bool(turns) and not technical and not text_errors and not turn_errors and not invariant_errors and not fact_context_errors and all(not c['post_errors'] for c in checks)
    contract_errors = fact_context_errors + candidate_contract_errors
    if contract_assessed and not final_passed:
        contract_errors = ['final acceptance failed'] + contract_errors
    return {'case_id': case['id'], 'split': case['split'], 'checks': checks,
            'metric_version': METRIC_VERSION,
            'passed': final_passed,
            'candidate_passed': bool(candidates) and not technical and not pre_turn_errors and not candidate_contract_errors and all(not c['pre_errors'] for c in checks) and all(c['faithful'] for c in citations) and not any(q.get('tax_adjustment') in ('yes', 'no') for q in tax_claims),
            'fix_contract_assessed': contract_assessed,
            'fix_contract_passed': not contract_errors if contract_assessed else None,
            'fix_contract_errors': contract_errors,
            'fact_context_errors': fact_context_errors,
            'candidate_contract_errors': candidate_contract_errors,
            'critical_final_failure': critical_failed,
            'critical_assertion_errors': critical_assertion_errors,
            'critical_text_errors': critical_text_errors,
            'final_unsupported_tax_claims': final_tax_mismatches,
            'final_tax_decisions_audited': len(final_tax),
            'final_audit_scope': 'Authored closed assertions, turn invariants and exact reviewed tax reply template only. A tax template mismatch is conservatively flagged; it is not a semantic finding of hallucination. Other free text is not assessed.',
            'citation_diagnostics': citations,
            'amount_format_diagnostics': amount_format_diagnostics,
            'unexpected_intents': unexpected_intents,
            'unexpected_candidate_intents': unexpected_candidate_intents,
            'technical_errors': technical, 'text_errors': text_errors,
            'turn_errors': turn_errors, 'pre_turn_errors': pre_turn_errors,
            'invariant_errors': invariant_errors,
            'structured_tax_claims_assessed': len(tax_claims),
            'unsupported_structured_tax_claims': sum(q.get('tax_adjustment') in ('yes', 'no') for q in tax_claims),
            'unrestricted_natural_language_claims': 'not automatically assessed',
            'turns': turns}


def summarize(records: list[dict], planned: int, unique_scenarios: int) -> dict:
    completed = len(records)
    passed = sum(r['passed'] for r in records)
    checked = sum(len(r['checks']) for r in records)
    post_correct = sum(not c['post_errors'] for r in records for c in r['checks'])
    pre_correct = sum(not c['pre_errors'] for r in records for c in r['checks'])
    tax_n = sum(r['structured_tax_claims_assessed'] for r in records)
    tax_bad = sum(r['unsupported_structured_tax_claims'] for r in records)
    all_checks = [c for r in records for c in r['checks']]
    policy_checks = [c for c in all_checks if 'policy' in c['expected']]
    amount_checks = [c for c in all_checks if 'amount' in c['expected']]
    answerable = [c for c in all_checks if c['expected'].get('answer_status') in ('grounded', 'partial') or c['expected'].get('amount') is not None]
    completed_answers = sum(c['actual'] is not None and c['actual'].get('answer_status') in ('grounded', 'partial') for c in answerable)
    over_refusals = sum(c['actual'] is not None and c['actual'].get('answer_status') in ('unsupported', 'needs_information') for c in answerable)
    tax_conversations = [r for r in records if r['structured_tax_claims_assessed']]
    human = [c for r in records for c in r['checks'] if c['expected'].get('action_status') == 'requires_human']
    human_ok = sum(not any(e.startswith('action_status:') or e == 'missing decision' for e in c['post_errors']) for c in human)
    def metric(n, d):
        return {'numerator': n, 'denominator': d, 'rate': n / d if d else None}
    return {'planned_runs': planned, 'completed_runs': completed, 'skipped_runs': planned-completed,
            'metric_version': METRIC_VERSION,
            'fix_contract_success': metric(sum(r.get('fix_contract_passed') is True for r in records), sum(bool(r.get('fix_contract_assessed')) for r in records)),
            'unique_scenarios': unique_scenarios,
            'unique_completed_scenarios': len({r['case_id'] for r in records}),
            'completion_status': 'complete' if completed == planned else 'incomplete',
            'critical_final_failures': sum(r.get('critical_final_failure', False) for r in records),
            'final_unsupported_tax_claims': sum(r.get('final_unsupported_tax_claims', 0) for r in records),
            'final_tax_decisions_audited': sum(r.get('final_tax_decisions_audited', 0) for r in records),
            'final_audit_scope': 'Closed expected assertions, turn invariants, and exact reviewed tax reply template. Tax mismatches conservatively flagged, not semantic hallucination judgements.',
            'conversation_success': metric(passed, completed),
            'success_against_planned': metric(passed, planned),
            'pre_gate_assertion_success': metric(pre_correct, checked),
            'post_gate_assertion_success': metric(post_correct, checked),
            'policy_accuracy': metric(sum(not any(e.startswith('missing policy') or e == 'missing decision' for e in c['post_errors']) for c in policy_checks), len(policy_checks)),
            'amount_accuracy': metric(sum(not any(e.startswith('amount:') or e == 'missing decision' for e in c['post_errors']) for c in amount_checks), len(amount_checks)),
            'answerable_completion': metric(completed_answers, len(answerable)),
            'over_refusal_rate': metric(over_refusals, len(answerable)),
            'unsupported_structured_tax_conversation_rate': metric(sum(r['unsupported_structured_tax_claims'] > 0 for r in tax_conversations), len(tax_conversations)),
            'mandatory_escalation_recall': metric(human_ok, len(human)),
            'unsupported_structured_tax_claim_rate': metric(tax_bad, tax_n),
            'candidate_conversation_success': metric(sum(r['candidate_passed'] for r in records), completed),
            'unexpected_intent_runs': sum(bool(r.get('unexpected_intents')) for r in records),
            'unexpected_candidate_intent_runs': sum(bool(r.get('unexpected_candidate_intents')) for r in records),
            'citation_status_counts': {status: sum(c['status'] == status for r in records for c in r.get('citation_diagnostics', [])) for status in ('exact', 'markdown_normalized', 'unknown_source', 'unmatched_quote', 'missing_evidence')},
            'amount_format_diagnostic_count': sum(len(r.get('amount_format_diagnostics', [])) for r in records),
            'natural_language_hallucination_rate': None,
            'assessment_limit': 'Closed structured assertions only; unrestricted natural-language claims require human audit.',
            'technical_failure_runs': sum(bool(r['technical_errors']) for r in records),
            'api_error_runs': sum(any(e in ('ProviderError', 'APIError', 'APITimeoutError', 'APIConnectionError') for e in r['technical_errors']) for r in records),
            'api_failure_assessment': 'ProviderError is a provider or structured-output failure; exact HTTP/API counts require call telemetry.',
            'turn_oracle_failures': sum(bool(r.get('turn_errors')) for r in records),
            'invariant_failure_runs': sum(bool(r.get('invariant_errors')) for r in records)}


def evaluate_cases(cases: list[dict], run_case: Callable[[dict], list[dict]], *,
                   model_id: str, repeats: int = 1,
                   can_continue: Callable[[], bool] | None = None) -> dict:
    if repeats < 1:
        raise ValueError('repeats must be positive')
    manifest = freeze_manifest(cases)
    records = []
    aborted = []
    stopped = False
    for repeat in range(repeats):
        for case in cases:
            if can_continue and not can_continue():
                stopped = True
                break
            try:
                turns = run_case(model_input(case))
                turns = [t.model_dump(mode='json') if hasattr(t, 'model_dump') else t for t in turns]
            except Exception as exc:
                # Never persist exception text: SDK errors can carry sensitive request data.
                if type(exc).__name__ in ('BudgetExceeded', 'BudgetExhausted'):
                    aborted.append({'case_id': case['id'], 'repeat': repeat + 1, 'reason': type(exc).__name__, 'turns': []})
                    stopped = True
                    break
                turns = [{'error': type(exc).__name__, 'decisions': [], 'reply': ''}]
            if any(t.get('error') in ('BudgetExceeded', 'BudgetExhausted') for t in turns):
                aborted.append({'case_id': case['id'], 'repeat': repeat + 1, 'reason': 'budget', 'turns': turns})
                stopped = True
                break
            if 'unresolved_policy' in case['expected']:
                from .comparison import score_projected
                result = score_projected(case, turns)
            else:
                result = score_case(case, turns)
            result['repeat'] = repeat + 1
            records.append(result)
        if stopped:
            break
    return {'model_id': model_id, 'manifest': manifest, 'records': records, 'aborted_runs': aborted,
            'summary': summarize(records, len(cases)*repeats, len(cases))}


def write_report(result: dict, directory: str | Path) -> Path:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / 'evaluation.json'
    target.write_text(json.dumps(result, indent=2, default=str)+'\n')
    (directory / 'freeze_manifest.json').write_text(json.dumps(result['manifest'], indent=2)+'\n')
    return target


def attach_usage(report: dict, calls: list[dict]) -> dict:
    """Attach provider telemetry; reservations remain distinct from measured usage."""
    import math
    latencies = sorted(c['latency_seconds'] for c in calls if isinstance(c.get('latency_seconds'), (int, float)))
    def percentile(p):
        return latencies[max(0, math.ceil(p * len(latencies)) - 1)] if latencies else None
    all_turns = [t for r in report.get('records', []) for t in r.get('turns', [])]
    turn_latencies = sorted(t['latency_seconds'] for t in all_turns if isinstance(t.get('latency_seconds'), (int, float)) and math.isfinite(t['latency_seconds']) and t['latency_seconds'] >= 0)
    def turn_percentile(p):
        return turn_latencies[max(0, math.ceil(p * len(turn_latencies)) - 1)] if turn_latencies else None
    reported = [c for c in calls if c.get('cost_status') == 'usage_reported']
    unknown = [c for c in calls if c.get('cost_status') != 'usage_reported']
    measured = sum(c.get('cost_usd', 0) for c in reported)
    reserved = sum(c.get('cost_usd', 0) for c in unknown)
    success = report['summary']['conversation_success']['numerator']
    report['usage'] = {
        'turn_latency_p50_seconds': turn_percentile(.5),
        'turn_latency_p95_seconds': turn_percentile(.95),
        'turn_latency_sample_count': len(turn_latencies),
        'turn_latency_complete': bool(all_turns) and len(turn_latencies) == len(all_turns),
        'call_count': len(calls), 'api_error_calls': sum(bool(c.get('error')) for c in calls),
        'validation_error_calls': sum(bool(c.get('validation_error')) for c in calls),
        'input_tokens': sum(c.get('input_tokens', 0) for c in calls),
        'output_tokens': sum(c.get('output_tokens', 0) for c in calls),
        'cached_input_tokens': sum(c.get('cached_input_tokens', 0) for c in calls),
        'cache_write_tokens': sum(c.get('cache_write_tokens', 0) for c in calls),
        'token_usage_complete': not unknown,
        'reported_cost_usd': measured, 'reserved_or_unknown_cost_usd': reserved,
        'cost_status': 'complete' if not unknown else 'partial',
        'cost_per_successful_conversation_usd': measured / success if success and not unknown else None,
        'call_latency_p50_seconds': percentile(.5), 'call_latency_p95_seconds': percentile(.95),
        'call_latency_sample_count': len(latencies),
    }
    return report
