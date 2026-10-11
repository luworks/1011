#!/usr/bin/env python3
"""Re-score saved dev traces and summarize frozen reports without model calls.

Run after every dev-* and frozen-* process has written its final summary.
No source, prompt, original trace, or original report is modified.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from policy_agent.evaluation import attach_usage, freeze_manifest, score_case, summarize


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def fraction(metric):
    if not metric or metric.get('denominator') in (None, 0):
        return 'n/a'
    return f"{metric['numerator']}/{metric['denominator']} ({metric['rate']:.1%})"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--allow-incomplete', action='store_true', help='Explicitly publish a provisional report with pending runs named')
    args = parser.parse_args()
    root = args.root.resolve()
    all_cases = read(root / 'fixtures/scenarios.json')
    dev_cases = {c['id']: c for c in all_cases if c['split'] == 'dev'}
    directories = sorted(set((root / 'runs').glob('dev-*')) | set((root / 'runs').glob('frozen-*')))
    pending, output_runs = [], []
    seen = {'dev': set(), 'frozen': set()}
    for directory in directories:
        if not directory.is_dir():
            continue
        summary_path, manifest_path = directory / 'summary.json', directory / 'manifest.json'
        if not summary_path.exists() or not manifest_path.exists():
            pending.append(str(directory.relative_to(root)))
            continue
        saved, manifest = read(summary_path), read(manifest_path)
        suite = saved.get('suite')
        if suite not in seen:
            continue
        expected_models = {m['model'] for m in manifest.get('planned_models', manifest.get('models', []))}
        reported_models = {m['model_id'] for m in saved.get('models', [])}
        pending.extend(f'{directory.name}: missing final report for {model}' for model in sorted(expected_models - reported_models))
        trace_path = directory / 'turns.jsonl'
        traces = [json.loads(line) for line in trace_path.read_text().splitlines() if line.strip()] if trace_path.exists() else []
        for original in saved.get('models', []):
            model = original['model_id']
            seen[suite].add(model)
            calls = original.get('calls', [c for c in manifest.get('calls', []) if c.get('model') == model])
            if suite == 'dev':
                records = []
                counts = Counter()
                aborted = []
                for trace in traces:
                    if trace['model'] != model:
                        continue
                    case_id, turns = trace['case_id'], trace['turns']
                    counts[case_id] += 1
                    if any(t.get('error') in ('BudgetExceeded', 'BudgetExhausted') for t in turns):
                        aborted.append({'case_id': case_id, 'repeat': counts[case_id], 'reason': 'budget'})
                        continue
                    if case_id not in dev_cases:
                        raise ValueError(f'Unknown dev case in {directory.name}: {case_id}')
                    record = score_case(dev_cases[case_id], turns)
                    record['repeat'] = counts[case_id]
                    records.append(record)
                report = {'records': records, 'summary': summarize(records, original['summary']['planned_runs'], original['summary']['unique_scenarios'])}
                attach_usage(report, calls)
                scoring = 'Retrospective re-scoring of original saved traces under the final independent dev oracle and current evaluator; no API rerun.'
                oracle = freeze_manifest([dev_cases[i] for i in original['manifest']['ids']])
            else:
                report = original
                records = original['records']
                aborted = original.get('aborted_runs', [])
                scoring = 'Original frozen report, copied without re-scoring or tuning.'
                oracle = original['manifest']
            failures = []
            for r in records:
                if not r['passed']:
                    failures.append({k: r.get(k) for k in ('case_id', 'repeat', 'technical_errors', 'text_errors', 'turn_errors', 'invariant_errors')})
                    failures[-1]['post_assertion_errors'] = [{'intent': c['intent'], 'errors': c['post_errors']} for c in r['checks'] if c['post_errors']]
            output_runs.append({
                'source_run': str(directory.relative_to(root)), 'suite': suite, 'model_id': model,
                'scoring_method': scoring, 'summary': report['summary'], 'usage': report.get('usage'),
                'oracle_manifest': oracle, 'original_oracle_manifest': original['manifest'],
                'original_run_manifest': {k: v for k, v in manifest.items() if k != 'calls'},
                'source_trace_sha256': digest(trace_path), 'source_summary_sha256': digest(summary_path),
                'original_summary': original['summary'], 'failures': failures, 'aborted_runs': aborted,
                'candidate_conversation_passes': sum(bool(r.get('candidate_passed')) for r in records),
            })
    for suite, models in seen.items():
        if not models:
            pending.append(f'{suite}: no completed model reports')
    if pending and not args.allow_incomplete:
        print('No report written; evaluation processes or reports remain incomplete:')
        print('\n'.join(pending))
        return 2
    ledger_path = root / 'runs/budget.json'
    ledger = read(ledger_path) if ledger_path.exists() else None
    accounting = None if ledger is None else {
        'scope': 'All requests sharing runs/budget.json, including probes, pilots, replay, development and frozen evaluation. Do not add this to per-run costs.',
        'usage_reported_cost_usd': sum(x['cost_usd'] for x in ledger.values() if x['status'] == 'usage_reported'),
        'reserved_or_unknown_cost_usd': sum(x['cost_usd'] for x in ledger.values() if x['status'] != 'usage_reported'),
        'ledger_total_usd': sum(x['cost_usd'] for x in ledger.values()),
        'entry_count': len(ledger), 'ledger_sha256': digest(ledger_path),
    }
    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'status': 'provisional' if pending else 'all_selected_runs_finalized', 'pending_runs': pending,
        'current_evaluator_sha256': digest(root / 'src/policy_agent/evaluation.py'),
        'scenario_file_sha256': digest(root / 'fixtures/scenarios.json'),
        'runs': output_runs, 'shared_budget_accounting': accounting,
        'limitations': [
            'Finalized means the process produced a report; budget-skipped runs remain incomplete in each report.',
            'Repeated executions are not new independent scenarios. Unique scenario counts are shown separately and never summed across models.',
            'Development is retrospective diagnostic evidence, not held-out model selection evidence.',
            'Safety invariants and structured assertion scores do not measure unrestricted natural-language hallucination or establish zero production errors.',
            'Provider-reported token usage is priced using the saved matrix; unknown request costs remain reservations. Estimates may differ from provider invoices.',
            'Latency percentiles describe individual API calls, including recorded retries; they are not end-to-end conversation latency.',
        ],
    }
    lines = ['# Evaluation results', '', f"Report status: **{result['status']}**. Generated {result['generated_at']}.", '',
             'Development traces are retrospectively scored against the final independent per-turn oracle. Frozen rows use their original saved reports. Neither operation makes API calls.', '',
             '| Suite | Model | Unique completed / planned | Executions completed / planned | Successful / completed | Successful / planned | Invariant failures |',
             '|---|---|---:|---:|---:|---:|---:|']
    for run in output_runs:
        s = run['summary']
        lines.append(f"| {run['suite']} | {run['model_id']} | {s['unique_completed_scenarios']}/{s['unique_scenarios']} | {s['completed_runs']}/{s['planned_runs']} | {fraction(s['conversation_success'])} | {fraction(s['success_against_planned'])} | {s.get('invariant_failure_runs', 'not assessed')} |")
    lines += ['', '| Suite | Model | Candidate assertion accuracy | Final assertion accuracy | Escalation recall | Over-refusal | Usage-priced USD | Reserved/unknown USD | Call p50 / p95 seconds |',
              '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for run in output_runs:
        s, u = run['summary'], run.get('usage') or {}
        latency = f"{u.get('call_latency_p50_seconds', 'n/a')} / {u.get('call_latency_p95_seconds', 'n/a')}"
        lines.append(f"| {run['suite']} | {run['model_id']} | {fraction(s['pre_gate_assertion_success'])} | {fraction(s['post_gate_assertion_success'])} | {fraction(s['mandatory_escalation_recall'])} | {fraction(s['over_refusal_rate'])} | {u.get('reported_cost_usd', 'unknown')} | {u.get('reserved_or_unknown_cost_usd', 'unknown')} | {latency} |")
    lines += ['', 'Assertion accuracy covers explicit expected policy/amount/status assertions; conversation success additionally includes per-turn intent checks and execution-safety invariants. A high assertion score alone is insufficient.', '', '## Failures and provenance', '']
    for run in output_runs:
        s = run['summary']
        failed = ', '.join(f"{f['case_id']} (repeat {f['repeat']})" for f in run['failures']) or 'none observed'
        lines += [f"- **{run['suite']} / {run['model_id']}**: {failed}. Skipped {s['skipped_runs']} of {s['planned_runs']} planned executions. Original run: `{run['source_run']}`; original trace SHA256 `{run['source_trace_sha256']}`."]
    if accounting:
        lines += ['', f"Shared budget ledger: usage-priced **${accounting['usage_reported_cost_usd']:.6f}**, reserved/unknown **${accounting['reserved_or_unknown_cost_usd']:.6f}**, total **${accounting['ledger_total_usd']:.6f}**. This includes probes, pilots and replays and must not be added to the per-run costs above."]
    lines += ['', '## Interpretation limits', ''] + ['- ' + item for item in result['limitations']]
    if pending:
        lines += ['', 'Pending: ' + '; '.join(pending)]
    lines += ['', 'Machine-readable metrics, failed assertions, original manifests and source hashes: `examples/evaluation_summary.json`.', '']
    for path, data in ((root / 'examples/evaluation_summary.json', json.dumps(result, indent=2) + '\n'), (root / 'docs/evaluation_results.md', '\n'.join(lines))):
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + '.tmp')
        temporary.write_text(data)
        temporary.replace(path)
    print('Wrote examples/evaluation_summary.json and docs/evaluation_results.md')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
