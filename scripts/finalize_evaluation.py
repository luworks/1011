#!/usr/bin/env python3
"""Export a finalized benchmark stage and optional final selector result; no API calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from policy_agent.selection import select_models


LIMITATIONS = [
    'Critical failures cover authored closed policy/amount/action assertions, turn invariants and the reviewed tax template. These measures are not a semantic audit of every business claim or a general hallucination rate.',
    'Known oracle gaps include thin deadline-value assertions, optional adjunct answers, and incomplete semantic checks of all supported KB topics. Supplemental human review remains necessary.',
    'The original 16-case collection was exposed and is historical regression evidence. A run naming fixtures/acceptance_v2.json uses the separate newly authored acceptance cohort described in docs/acceptance_v2_provenance.md; verify its saved hash. Do not transfer freshness claims between cohorts.',
    'From workflow-v5, tax candidate outcomes are constrained by the reviewed corpus-bound schema to unknown/not_applicable. Pre-gate candidate metrics therefore measure schema-constrained workflow outputs, not autonomous unconstrained model tax reasoning.',
    'Screening many configurations and promoting development winners introduces selection optimism. Observed quality differences do not establish population-level superiority.',
    'Repeated runs of the same authored scenario are not independent scenarios. Report unique scenarios and executions separately; scenario-cluster latency intervals are descriptive.',
    'Model configuration IDs and provider reasoning settings are recorded exactly; effort labels are not assumed equivalent across providers.',
    'Costs use saved provider usage and the run price table. Unknown/reserved charges remain separate; estimates may differ from provider invoices.',
    'Measured full-turn latency includes the workflow, model calls, validation and retries. A short benchmark does not establish production latency guarantees.',
]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metric(value):
    if not isinstance(value, dict) or not value.get('denominator'):
        return 'not assessed'
    return f"{value['numerator']}/{value['denominator']} ({value['rate']:.1%})"


def phase_pointer(path):
    if path is None:
        return None
    return {'path': str(path), 'role': 'configuration promotion evidence, not a final winner',
            'summary_sha256': sha(path / 'summary.json') if (path / 'summary.json').exists() else None,
            'index_sha256': sha(path / 'index.json') if (path / 'index.json').exists() else None}


def finalize(run, *, screen=None, dev=None, ledger=None):
    index_path, summary_path, manifest_path = run / 'index.json', run / 'summary.json', run / 'manifest.json'
    index, saved, root_manifest = read(index_path), read(summary_path), read(manifest_path)
    if any(row.get('status') == 'pending' for row in index['models']):
        raise ValueError('Benchmark processes are still pending; no final stage export permitted')
    reports = {r['config_id']: r for r in saved['models']}
    if len(reports) != len(saved['models']):
        raise ValueError('Duplicate report configuration IDs')
    configs = {c['config_id']: c for c in root_manifest['planned_models']}
    if set(configs) != {row['config_id'] for row in index['models']}:
        raise ValueError('Index and planned configuration IDs differ')
    models, entries, missing = [], [], []
    for indexed in index['models']:
        cid = indexed['config_id']
        config = configs[cid]
        if cid not in reports:
            missing.append({'config_id': cid, 'status': indexed['status'], 'error': indexed.get('error')})
            continue
        report = reports[cid]
        directory = run / indexed['directory']
        if directory.resolve().parent != run.resolve():
            raise ValueError('Subrun path escapes benchmark directory')
        local_manifest = read(directory / 'manifest.json')
        summary, usage = report['summary'], report.get('usage', {})
        failure_cases = [{'case_id': r['case_id'], 'repeat': r.get('repeat'),
                          'metric_version': r.get('metric_version', summary.get('metric_version')),
                          'final_passed': r.get('passed'), 'candidate_passed': r.get('candidate_passed'),
                          'fix_contract_assessed': r.get('fix_contract_assessed'),
                          'fix_contract_passed': r.get('fix_contract_passed'),
                          'fix_contract_errors': r.get('fix_contract_errors', []),
                          'fact_context_errors': r.get('fact_context_errors', []),
                          'candidate_contract_errors': r.get('candidate_contract_errors', []),
                          'critical_final_failure': r.get('critical_final_failure'),
                          'critical_assertion_errors': r.get('critical_assertion_errors', []),
                          'critical_text_errors': r.get('critical_text_errors', []),
                          'technical_errors': r.get('technical_errors', []),
                          'turn_errors': r.get('turn_errors', []),
                          'pre_turn_errors': r.get('pre_turn_errors', []),
                          'text_errors': r.get('text_errors', []),
                          'invariant_errors': r.get('invariant_errors', []),
                          'assertion_errors': [{'intent': c.get('intent'), 'pre_errors': c.get('pre_errors', []),
                                                'post_errors': c.get('post_errors', [])}
                                               for c in r.get('checks', []) if c.get('pre_errors') or c.get('post_errors')]}
                         for r in report.get('records', []) if r.get('passed') is False
                         or r.get('fix_contract_passed') is False or r.get('candidate_passed') is False]
        records = report.get('records', [])
        diagnostics = {
            'final_utility_failure_runs': sum(r.get('passed') is False and r.get('critical_final_failure') is False
                                              and not r.get('technical_errors') for r in records),
            'final_severity_assessed_runs': sum(type(r.get('critical_final_failure')) is bool for r in records),
            'candidate_failure_runs': sum(r.get('candidate_passed') is False for r in records),
            'candidate_assessed_runs': sum(type(r.get('candidate_passed')) is bool for r in records),
            'fix_contract_failure_runs': sum(r.get('fix_contract_passed') is False for r in records),
            'fix_contract_assessed_runs': sum(r.get('fix_contract_assessed') is True for r in records),
            'scope': 'Utility failures mean failed final acceptance with explicitly false critical flag and no technical error. Candidate and fix-contract failures can coexist with a correct final response; absent historical fields are unassessed.',
        }
        models.append({'config_id': cid, 'model_id': report['model_id'], 'provider': config['provider'],
            'metric_version': summary.get('metric_version'), 'diagnostics': diagnostics,
            'reasoning_effort': config.get('reasoning_effort'), 'thinking': config.get('thinking'), 'effort': config.get('effort'),
            'configuration': config, 'index_status': indexed['status'], 'summary': summary, 'usage': usage,
            'repeats': saved['repeats'], 'oracle_manifest': report.get('manifest'),
            'source_run_manifest': {k: v for k, v in local_manifest.items() if k != 'calls'},
            'source_manifest_sha256': sha(directory / 'manifest.json'), 'failure_cases': failure_cases,
            'aborted_run_count': len(report.get('aborted_runs', [])),
            'critical_audit_scope': 'Closed authored assertions and reviewed tax template; not all natural-language claims.'})
        entries.append({'config_id': cid, 'report': report, 'run_manifest': local_manifest,
                        'repeats': saved['repeats'], 'suite': saved['suite']})
    if saved['suite'] == 'frozen' and type(saved['repeats']) is int and saved['repeats'] >= 3:
        if missing:
            selection = {'status': 'pending', 'winner': None, 'reasons': ['Some planned configurations have no report; selection on a reduced configuration denominator is not permitted.'], 'missing_configurations': missing}
        else:
            selection = select_models(entries)
    else:
        selection = {'status': 'not_final_stage', 'winner': None,
            'reasons': ['Final selection is invoked only for the frozen suite with at least three repeats. Screen/development stages provide promotion evidence only.']}
    stage_cost = {'scope': 'Only usage from reports in this benchmark stage; excludes historical probes/screens/replays and other stages.',
        'usage_priced_usd': sum(m['usage'].get('reported_cost_usd', 0) for m in models),
        'reserved_or_unknown_usd': sum(m['usage'].get('reserved_or_unknown_cost_usd', 0) for m in models),
        'telemetry_complete': not missing and all(m['usage'].get('cost_status') == 'complete' for m in models),
        'input_tokens': sum(m['usage'].get('input_tokens', 0) for m in models),
        'output_tokens': sum(m['usage'].get('output_tokens', 0) for m in models),
        'cached_input_tokens': sum(m['usage'].get('cached_input_tokens', 0) for m in models)}
    ledger_snapshot = None
    if ledger is not None:
        rows = read(ledger)
        ledger_snapshot = {'path': str(ledger), 'sha256': sha(ledger),
            'scope': 'Shared cumulative ledger, including historical and other-stage requests. Do not add to stage cost.',
            'usage_priced_usd': sum(r['cost_usd'] for r in rows.values() if r['status'] == 'usage_reported'),
            'reserved_or_unknown_upper_bound_usd': sum(r['cost_usd'] for r in rows.values() if r['status'] != 'usage_reported'),
            'total_accounted_upper_bound_usd': sum(r['cost_usd'] for r in rows.values())}
    compact = {'schema_version': 2, 'source_run': str(run), 'source_summary_sha256': sha(summary_path),
        'source_manifest_sha256': sha(manifest_path), 'suite': saved['suite'], 'repeats': saved['repeats'],
        'stage_status': 'incomplete' if missing or any(m['summary']['completion_status'] != 'complete' for m in models) else 'complete',
        'planned_configurations': len(configs), 'reported_configurations': len(models), 'missing_configurations': missing,
        'scenario_selection': saved.get('selection', index.get('selection')), 'models': models,
        'stage_cost': stage_cost, 'shared_ledger_snapshot': ledger_snapshot, 'selection': selection,
        'phase_pointers': {'screen': phase_pointer(screen), 'development': phase_pointer(dev)}, 'limitations': LIMITATIONS}
    winner = selection.get('winner')
    conclusion = f"Observed benchmark choice: **{winner}** ({selection['status']})." if winner else f"**No final winner: {selection['status']}.**"
    lines = ['# Evaluation methods and results', '', conclusion, '',
        f"Stage: **{saved['suite']}**, {saved['repeats']} execution(s) per scenario. Reports available for {len(models)}/{len(configs)} planned configurations. Stage completion: **{compact['stage_status']}**.", '',
        '## Methods', '',
        'Every configuration is identified by exact model and reasoning settings. Reports preserve source code, corpus, prompt and oracle provenance. Final selection is attempted only for frozen evaluation with at least three repeats. Quality gates exclude observed critical failures and missed required escalation; eligible configurations are compared by final conversation success, full-turn P95, P50, then cost per successful conversation. The selector can return pending, tentative or no qualifying model.', '',
        'Screen and development phase pointers describe candidate promotion and do not name a final winner. Unique scenarios are distinct from repeated executions; the same scenarios across models are not additional independent evidence.', '',
        '## Measured results', '',
        '| Configuration | Unique completed / planned | Executions completed / planned | Success / completed | Success / planned | Critical failures | Escalation recall | Turn P50 / P95 (s) |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for model in models:
        s, u = model['summary'], model['usage']
        lines.append(f"| {model['config_id']} | {s.get('unique_completed_scenarios')}/{s.get('unique_scenarios')} | {s.get('completed_runs')}/{s.get('planned_runs')} | {metric(s.get('conversation_success'))} | {metric(s.get('success_against_planned'))} | {s.get('critical_final_failures', 'not assessed')} | {metric(s.get('mandatory_escalation_recall'))} | {u.get('turn_latency_p50_seconds')} / {u.get('turn_latency_p95_seconds')} |")
    lines += ['', '| Configuration | Pre-gate assertions | Post-gate assertions | Input / output tokens | Usage-priced USD | Reserved/unknown USD |', '|---|---:|---:|---:|---:|---:|']
    for model in models:
        s, u = model['summary'], model['usage']
        lines.append(f"| {model['config_id']} | {metric(s.get('pre_gate_assertion_success'))} | {metric(s.get('post_gate_assertion_success'))} | {u.get('input_tokens')} / {u.get('output_tokens')} | {u.get('reported_cost_usd')} | {u.get('reserved_or_unknown_cost_usd')} |")
    lines += ['', '| Configuration | Metric version | Fix-contract success | Fix-contract failures / assessed | Candidate failures / assessed | Final utility failures / severity assessed |',
              '|---|---|---:|---:|---:|---:|']
    for model in models:
        s, d = model['summary'], model['diagnostics']
        lines.append(f"| {model['config_id']} | {model['metric_version'] or 'not recorded'} | {metric(s.get('fix_contract_success'))} | {d['fix_contract_failure_runs']}/{d['fix_contract_assessed_runs']} | {d['candidate_failure_runs']}/{d['candidate_assessed_runs']} | {d['final_utility_failure_runs']}/{d['final_severity_assessed_runs']} |")
    lines += ['', 'The fix contract includes final acceptance plus authored extraction, context and candidate constraints. A candidate-only failure may leave the final response correct. Final utility failures exclude explicitly flagged critical failures and technical errors; missing historical severity fields are unassessed. Do not pool safety counts across metric versions. Per-case pre/post errors and fix-contract failures remain in the compact JSON export.']
    lines += ['', '## Conclusions', '', conclusion]
    lines += ['- ' + reason for reason in selection.get('reasons', [])]
    if selection.get('uncertainty_note'):
        lines += ['', selection['uncertainty_note']]
    lines += ['', f"Stage usage-priced cost: ${stage_cost['usage_priced_usd']:.6f}; reserved/unknown: ${stage_cost['reserved_or_unknown_usd']:.6f}. Telemetry complete: {stage_cost['telemetry_complete']}."]
    if ledger_snapshot:
        lines += ['', f"Separately, the shared historical ledger accounts for ${ledger_snapshot['total_accounted_upper_bound_usd']:.6f}, including ${ledger_snapshot['reserved_or_unknown_upper_bound_usd']:.6f} reserved/unknown upper bound. This is not the stage cost."]
    lines += ['', '## Limitations', ''] + ['- ' + text for text in LIMITATIONS]
    lines += ['', 'See `summary.json` for exact configurations, per-model planned denominators, failures, tokens and source hashes; `selection.json` preserves the selector result without replacing an unresolved result with a winner.', '']
    return compact, selection, '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--screen', type=Path)
    parser.add_argument('--dev', type=Path)
    parser.add_argument('--ledger', type=Path)
    args = parser.parse_args()
    try:
        if args.output.resolve() == args.run.resolve():
            raise ValueError('Output must differ from the source run directory')
        compact, selection, markdown = finalize(args.run, screen=args.screen, dev=args.dev, ledger=args.ledger)
        args.output.mkdir(parents=True, exist_ok=True)
        for filename, data in [('summary.json', json.dumps(compact, indent=2) + '\n'), ('selection.json', json.dumps(selection, indent=2) + '\n'), ('report.md', markdown)]:
            target = args.output / filename
            temporary = target.with_suffix(target.suffix + '.tmp')
            temporary.write_text(data)
            temporary.replace(target)
        print(f"Exported {args.output}; selection status: {selection['status']}")
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'No export written: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
