#!/usr/bin/env python3
"""Plan a provisional next evaluation stage from one benchmark screen; no API calls."""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def cohort(manifest):
    selection = manifest.get('evaluation_selection', {})
    values = {key: manifest.get(key) for key in ('code_sha256', 'corpus_version', 'prompt_version', 'model_matrix_sha256')}
    values.update(selected_suite_sha256=selection.get('selected_suite', {}).get('sha256'),
                  cases_file_sha256=selection.get('cases_file_sha256'))
    if any(not isinstance(value, str) or not value for value in values.values()):
        raise ValueError('Missing cohort provenance; refusing comparison')
    return values


EFFORT_ORDER = ('none', 'low', 'medium', 'high')


def effort_rank(config):
    if config['provider'] == 'anthropic':
        if config.get('thinking', {}).get('type') != 'adaptive':
            return None
        effort = config.get('effort')
    else:
        effort = config.get('reasoning_effort', 'none')
    if effort not in EFFORT_ORDER:
        raise ValueError(f'Unknown effort for {config["config_id"]}: {effort}')
    return EFFORT_ORDER.index(effort)


def build(screen, top_per_family=1, include_high=False):
    if top_per_family < 1:
        raise ValueError('top-per-family must be positive')
    index, root_manifest = read(screen / 'index.json'), read(screen / 'manifest.json')
    stamp = cohort(root_manifest)
    configs = root_manifest['planned_models']
    for config in configs:
        for field in ('reasoning_effort', 'effort'):
            if config.get(field) in ('xhigh', 'max', 'ultra'):
                raise ValueError(f'User effort ceiling is high; rejected {config["config_id"]}')
    by_id = {c['config_id']: c for c in configs}
    if len(by_id) != len(configs) or set(by_id) != {r['config_id'] for r in index['models']}:
        raise ValueError('Planned and indexed configurations differ or duplicate IDs exist')
    selected = index['selection']['selected_suite']
    if selected['sha256'] != stamp['selected_suite_sha256']:
        raise ValueError('Index and root manifest suite mismatch')
    if index['suite'] != 'dev' or selected['scenario_count'] != 3:
        raise ValueError('This planner is for the provisional three-case development screen only')
    expected_runs = selected['scenario_count'] * index['repeats']
    families = defaultdict(list)
    for entry in index['models']:
        config = by_id[entry['config_id']]
        family = config.get('family') or f"{config['provider']}/{config['model']}"
        row = {'config_id': entry['config_id'], 'family': family, 'index_status': entry['status'],
               'directory': entry['directory'], 'eligible': False, 'exclusions': [], 'config': config}
        directory = screen / entry['directory']
        if directory.resolve().parent != screen.resolve():
            raise ValueError('Subrun directory escapes screen root')
        manifest_path, summary_path = directory / 'manifest.json', directory / 'summary.json'
        if manifest_path.exists():
            local_manifest = read(manifest_path)
            if cohort(local_manifest) != stamp:
                raise ValueError(f'Inconsistent cohort: {entry["config_id"]}')
            if local_manifest.get('planned_models') != [config]:
                raise ValueError(f'Configuration changed: {entry["config_id"]}')
        if not manifest_path.exists() or not summary_path.exists():
            row['exclusions'].append('pending_or_missing_report')
            if entry['status'] == 'failed':
                row['exclusions'].append('run_failed_without_report')
            families[family].append(row)
            continue
        wrapper = read(summary_path)
        reports = wrapper.get('models', [])
        if len(reports) != 1 or reports[0].get('config_id') != config['config_id']:
            raise ValueError('Subrun report does not uniquely identify its configuration')
        report = reports[0]
        if report['manifest']['sha256'] != stamp['selected_suite_sha256'] or wrapper['repeats'] != index['repeats']:
            raise ValueError('Subrun oracle/repeat cohort mismatch')
        s, u = report['summary'], report.get('usage', {})
        if s['planned_runs'] != expected_runs or s['unique_scenarios'] != 3:
            raise ValueError('Inconsistent planned denominator')
        row.update(summary=s, usage=u, summary_sha256=sha(summary_path), manifest_sha256=sha(manifest_path))
        reasons = row['exclusions']
        if s.get('completion_status') != 'complete' or s.get('completed_runs') != expected_runs:
            reasons.append('incomplete_screen')
        if s.get('critical_final_failures') is None:
            reasons.append('critical_failure_assessment_missing')
        elif s['critical_final_failures']:
            reasons.append('observed_critical_final_failure')
        if s.get('invariant_failure_runs', 0):
            reasons.append('observed_execution_safety_invariant_failure')
        recall = s.get('mandatory_escalation_recall', {})
        if not recall.get('denominator'):
            reasons.append('mandatory_escalation_not_assessed')
        elif recall.get('numerator') != recall['denominator']:
            reasons.append('missed_mandatory_escalation')
        if s.get('technical_failure_runs', 0) or u.get('api_error_calls', 0):
            reasons.append('observed_technical_or_api_failure')
        if not u.get('turn_latency_complete') or not all(finite(u.get(k)) for k in ('turn_latency_p95_seconds', 'turn_latency_p50_seconds')):
            reasons.append('full_turn_latency_missing')
        if u.get('cost_status') != 'complete' or not finite(u.get('reported_cost_usd')):
            reasons.append('unknown_cost')
        row['eligible'] = not reasons
        completed = s.get('completed_runs', 0)
        known = u.get('reported_cost_usd')
        projectable = completed > 0 and finite(known) and u.get('cost_status') == 'complete'
        unit = known / completed if projectable else None
        row['cost_projection'] = {'screen_completed_runs': completed, 'screen_usage_priced_usd': known,
            'screen_reserved_or_unknown_usd': u.get('reserved_or_unknown_cost_usd'),
            'estimated_usd_per_scenario': unit, 'dev_24_runs_usd': unit * 24 if unit is not None else None,
            'frozen_16_scenarios_times_3_usd': unit * 48 if unit is not None else None,
            'combined_72_runs_usd': unit * 72 if unit is not None else None,
            'assumption': 'Linear extrapolation of three screen scenarios; other scenarios have different lengths, turns, failures and token use. Planning estimate only, not a budget guarantee.'}
        families[family].append(row)
    result_families, promoted = [], []
    for family in sorted(families):
        rows = families[family]
        pending = [r['config_id'] for r in rows if r['index_status'] == 'pending' or ('pending_or_missing_report' in r['exclusions'] and r['index_status'] != 'failed')]
        candidates = [r for r in rows if r['eligible']]
        def order(row):
            s, u = row['summary'], row['usage']
            success = s['success_against_planned']
            return (-Fraction(success['numerator'], success['denominator']), u['turn_latency_p95_seconds'],
                    u['turn_latency_p50_seconds'], u['reported_cost_usd'] / s['completed_runs'], row['config_id'])
        candidates.sort(key=order)
        winners = [] if pending else candidates[:top_per_family]
        promotion_reasons = {r['config_id']: ['accuracy_latency_cost_rank'] for r in winners}
        highest = None
        if include_high and not pending:
            effort_candidates = [(effort_rank(r['config']), r) for r in candidates]
            effort_candidates = [(rank, r) for rank, r in effort_candidates if rank == EFFORT_ORDER.index('high')]
            if effort_candidates:
                highest_rank = max(rank for rank, _ in effort_candidates)
                # candidates already have deterministic accuracy/latency/cost order.
                highest = next(r for rank, r in effort_candidates if rank == highest_rank)
                promotion_reasons.setdefault(highest['config_id'], []).append('eligible_high_effort_quality_probe')
                if highest['config_id'] not in {r['config_id'] for r in winners}:
                    winners.append(highest)
        promoted.extend(r['config'] for r in winners)
        status = 'pending_family_completion' if pending else ('provisional_shortlist' if winners else 'no_safe_complete_configuration_promoted')
        result_families.append({'family': family, 'status': status, 'pending_configs': pending,
            'shortlisted_config_ids': [r['config_id'] for r in winners],
            'promotion_reasons': promotion_reasons,
            'eligible_high_effort_config_id': highest['config_id'] if highest else None,
            'ranked_eligible_config_ids': [r['config_id'] for r in candidates], 'configurations': rows})
    shortlist_ids = {c['config_id'] for c in promoted}
    estimates = [r['cost_projection']['combined_72_runs_usd'] for f in result_families for r in f['configurations'] if r['config_id'] in shortlist_ids]
    return {'stage': 'provisional_three_case_screen', 'final_model_selection': False,
        'source_screen': str(screen), 'cohort': stamp, 'selected_suite': selected,
        'planned_configuration_count': len(configs),
        'include_high': include_high,
        'effort_probe_policy': 'If enabled, additionally promote an eligible high reasoning effort configuration per family; Claude uses adaptive thinking only. Above-high configurations are rejected by user constraint. Deduplicate with rank winners; exclusions still apply.',
        'ranking_order': ['final success against planned runs descending',
            'full-turn p95 ascending', 'full-turn p50 ascending', 'usage-priced cost per completed scenario ascending', 'config_id lexical tie-break'],
        'promotion_policy': 'No promotion after observed critical failure, missed mandatory escalation, technical/API failure, incomplete run or missing telemetry. Wait for every configuration in a family to finish. No unsafe fallback.',
        'families': result_families, 'shortlisted_count': len(promoted),
        'projected_shortlist_24_dev_plus_48_frozen_usd': sum(estimates),
        'limitations': ['Three development scenarios are a screen, not independent final selection evidence.',
            'Full-turn latency includes understanding, reasoning and reply workflow; p95 from three cases is highly uncertain.',
            'No observed critical failures is not evidence of production safety or zero hallucinations.',
            'Cost projection excludes past screen/probe costs and does not reserve or authorize spend.'],
        'shortlist_matrix': {'selection_stage': 'provisional_three_case_screen', 'source_cohort': stamp, 'models': promoted}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--screen', type=Path, default=Path('runs/frontier-screen'))
    parser.add_argument('--output', type=Path, default=Path('runs/frontier-shortlist'))
    parser.add_argument('--top-per-family', type=int, default=1)
    parser.add_argument('--include-high', action='store_true', help='Also promote one eligible high reasoning/adaptive effort configuration per family, deduplicated; reject effort above high')
    args = parser.parse_args()
    try:
        result = build(args.screen, args.top_per_family, args.include_high)
        args.output.mkdir(parents=True, exist_ok=True)
        for name, payload in (('shortlist.json', result), ('matrix.json', result['shortlist_matrix'])):
            target = args.output / name
            temporary = target.with_suffix('.tmp')
            temporary.write_text(json.dumps(payload, indent=2) + '\n')
            temporary.replace(target)
        print(f"Provisional shortlist: {result['shortlisted_count']} configurations; saved {args.output}")
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'No new plan written: {type(exc).__name__}: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
