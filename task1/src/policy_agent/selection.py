"""Quality-gated model selection; compare full-turn latency, never API-only latency."""
from __future__ import annotations
import math
import random


def _percentile(values, quantile):
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * quantile) - 1)] if ordered else None


def select_models(entries: list[dict]) -> dict:
    """Entries: {report, run_manifest, repeats, suite}.

    Audited summary counts critical_final_failures and final_unsupported_tax_claims
    are required. Unknown is never silently treated as zero. Repeated runs are
    samples, not independently authored scenarios. P95 uses nearest rank.
    """
    result = {'status': 'pending', 'winner': None, 'models': [], 'reasons': [],
              'heuristic': 'Require zero critical final failures, mandatory escalation misses and final unsupported tax claims. Maximize final conversation success, then minimize full-turn P95, then P50, then cost per successful conversation. No quality floor, weighted score or cheaper-model latency allowance.',
              'latency_scope': 'Full workflow turn including retrieval, model calls, validation, repair and retries; nearest-rank percentiles.',
              'quality_comparison': 'Descriptive observed success on the matched frozen benchmark; no statistical superiority or simultaneous confidence claim across screened configurations.',
              'bootstrap_scope': 'Unique case_id clusters retain all repeated runs and all turns; 1000 deterministic resamples.'}
    if not entries:
        result['reasons'].append('No model reports supplied.')
        return result
    signatures = []
    unresolved = False
    for entry in entries:
        report, manifest = entry['report'], entry.get('run_manifest', {})
        s, usage = report['summary'], report.get('usage', {})
        signature = (entry.get('suite'), entry.get('repeats'), report.get('manifest', {}).get('sha256'),
                     manifest.get('prompt_version'), manifest.get('code_sha256'), manifest.get('corpus_version'))
        signatures.append(signature)
        reasons = []
        pending = []
        if any(x is None for x in signature): pending.append('Missing comparison provenance.')
        if entry.get('suite') != 'frozen': pending.append('Final selection requires the frozen suite; development screens cannot select a winner.')
        repeats = entry.get('repeats')
        if type(repeats) is not int or repeats < 3: pending.append('Final selection requires at least three repeats per scenario.')
        if s.get('completion_status') != 'complete' or s.get('completed_runs') != s.get('planned_runs'):
            pending.append('Evaluation incomplete.')
        if report.get('selection', {}).get('scope') != 'full_suite': pending.append('Full suite coverage not confirmed.')
        turns = [t for r in report.get('records', []) for t in r.get('turns', [])]
        latencies = [t['latency_seconds'] for t in turns if isinstance(t.get('latency_seconds'), (float, int)) and math.isfinite(t['latency_seconds']) and t['latency_seconds'] >= 0]
        if not turns or len(latencies) != len(turns): pending.append('Full-turn latency unavailable for some or all turns.')
        success = s.get('conversation_success', {}).get('rate')
        if success is None: pending.append('Conversation success unavailable.')
        if len(report.get('records', [])) != s.get('completed_runs'):
            pending.append('Saved conversation records do not match the completed denominator.')
        scenario_counts = {}
        for record in report.get('records', []):
            case_id = record.get('case_id')
            if not isinstance(case_id, str) or not case_id.strip():
                pending.append('Unique scenario case_id unavailable for a saved conversation.')
                continue
            scenario_counts[case_id] = scenario_counts.get(case_id, 0) + 1
        if scenario_counts and any(count != repeats for count in scenario_counts.values()):
            pending.append('Saved repeat counts do not match the declared repeats for each scenario.')
        for field in ('critical_final_failures', 'final_unsupported_tax_claims'):
            count = s.get(field)
            if count is None: pending.append(f'Audited {field} unavailable.')
            elif count != 0: reasons.append(f'{field}: {count}.')
        escalation = s.get('mandatory_escalation_recall', {})
        if escalation.get('denominator', 0) <= 0: pending.append('No mandatory escalation evidence.')
        elif escalation.get('numerator') != escalation.get('denominator'):
            reasons.append('Missed mandatory escalation.')
        cost = usage.get('cost_per_successful_conversation_usd')
        if usage.get('cost_status') != 'complete' or cost is None or not math.isfinite(cost):
            pending.append('Complete measured usage cost unavailable.')
        config_id = entry.get('config_id') or report.get('config_id')
        if not config_id: pending.append('Distinct model-plus-thinking config_id unavailable.')
        row = {'config_id': config_id, 'model_id': report['model_id'], 'success_rate': success, 'cost_per_successful_conversation_usd': cost,
               'turn_latency_p50_seconds': _percentile(latencies, .5), 'turn_latency_p95_seconds': _percentile(latencies, .95),
               'turn_latency_sample_count': len(latencies), 'eligible': not reasons and not pending,
               'unique_scenario_count': len(scenario_counts), 'conversation_run_count': len(report.get('records', [])),
               'bootstrap_resample_count': 0,
               'exclusion_reasons': reasons, 'pending_reasons': pending}
        result['models'].append(row)
        unresolved |= bool(pending)
    if len({row['config_id'] for row in result['models']}) != len(entries):
        result['reasons'].append('Duplicate configuration IDs; model-plus-thinking configurations must be distinct.')
        unresolved = True
    if len(set(signatures)) != 1:
        result['reasons'].append('Suite, repeats, prompt, code or corpus versions differ; reports are not comparable.')
        unresolved = True
    if unresolved:
        result['reasons'].append('Resolve missing evidence or incomplete/noncomparable reports before choosing a winner.')
        return result
    eligible = [row for row in result['models'] if row['eligible']]
    if not eligible:
        result.update(status='no_qualifying_model', reasons=['No model meets the quality gates.'])
        return result
    best_quality = max(row['success_rate'] for row in eligible)
    best = [row for row in eligible if row['success_rate'] == best_quality]
    ranked = sorted(best, key=lambda r: (r['turn_latency_p95_seconds'], r['turn_latency_p50_seconds'], r['cost_per_successful_conversation_usd'], r['config_id']))
    winner = ranked[0]
    # Repeated conversations share a scenario. Resample that unique scenario as
    # one cluster, retaining all its repeats and turns rather than treating them
    # as independent scenarios. Bounds are descriptive, not provider guarantees.
    intervals = {}
    for entry, row in zip(entries, result['models']):
        if row not in best:
            continue
        by_case = {}
        for record in entry['report']['records']:
            by_case.setdefault(record['case_id'], []).extend(t['latency_seconds'] for t in record.get('turns', []))
        clusters = [by_case[case_id] for case_id in sorted(by_case)]
        randomizer = random.Random(0)
        bootstrap = []
        for _ in range(1000):
            sample = [v for _ in clusters for v in randomizer.choice(clusters)]
            bootstrap.append(_percentile(sample, .95))
        interval = [_percentile(bootstrap, .025), _percentile(bootstrap, .975)]
        row['turn_p95_bootstrap_interval_seconds'] = interval
        row['bootstrap_resample_count'] = len(bootstrap)
        intervals[row['config_id']] = interval
    tentative = any(max(intervals[winner['config_id']][0], intervals[other['config_id']][0]) <= min(intervals[winner['config_id']][1], intervals[other['config_id']][1]) for other in ranked[1:])
    result.update(status='tentative' if tentative else 'selected', winner=winner['config_id'],
                  ranking=[r['config_id'] for r in ranked],
                  comparison_order=['final_success_desc', 'turn_p95_asc', 'turn_p50_asc', 'cost_per_success_asc'],
                  uncertainty_note='Overlapping unique-scenario-bootstrap 95% P95 intervals; observed ordering is tentative.' if tentative else 'Observed latency order; unique-scenario bootstrap intervals are descriptive and do not cover provider drift or quality-comparison uncertainty.',
                  evidence_limit='Selection applies only to this complete matched benchmark. Repeated scenarios and temporal/provider variation limit inference; raw candidate diagnostics do not replace final accuracy.')
    return result
