#!/usr/bin/env python3
"""Export selected completed/partial experiments without copying arbitrary run files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from package import ROOT, check, credentials


def compact(value):
    """Preserve scored assertions/errors and metadata; remove repeated full turns."""
    if isinstance(value, dict):
        return {k: compact(v) for k, v in value.items() if k != 'turns'}
    if isinstance(value, list):
        return [compact(v) for v in value]
    return value


def metric(value):
    if not isinstance(value, dict):
        return 'n/a'
    return f"{value.get('numerator', '?')}/{value.get('denominator', '?')}"


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def comparison(runs):
    rows = [
        '# Curated model evaluation snapshots', '',
        'These are the selected runs, not an aggregate across all experiments. Each row retains its own suite, repetition count and denominator. Development results are not held-out validation. Costs are client estimates; unknown/reserved costs are separate from reported usage. Structured assertion metrics do not measure unrestricted natural-language hallucination. Turn timing is end-to-end where available; missing turn timing is not replaced by API-call timing. GPT 5.4-era runs are development history and excluded from final selection, whose candidates include GPT 6.1 Sol and GPT 6 Luna at supported thinking levels plus Opus 5.5, Sonnet 5.5 and Haiku 5.5. Each configuration is scored separately. Accuracy ranks first, followed by end-to-end turn P95/P50, with price last. Development screening is separate from matched finalist frozen comparisons; incomplete coverage cannot establish a global winner.', '',
        '| Run / suite | Configuration | Completed / planned | Conversation success | Pre-gate assertions | Post-gate assertions | Escalation recall | Turn P50 seconds | Turn P95 seconds | Turn samples | Reported cost USD | Reserved/unknown USD | API-error calls |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|',
    ]
    for run in runs:
        result = run['summary']
        for model in result.get('models', []):
            summary = model.get('summary', {})
            usage = model.get('usage', {})
            columns = [
                f"{run['source_run']} / {result.get('suite', 'unknown')} (×{result.get('repeats', 1)})",
                model.get('config_id', model.get('model_id', 'unknown')),
                f"{summary.get('completed_runs', '?')}/{summary.get('planned_runs', '?')}",
                metric(summary.get('conversation_success')),
                metric(summary.get('pre_gate_assertion_success')),
                metric(summary.get('post_gate_assertion_success')),
                metric(summary.get('mandatory_escalation_recall')),
                usage.get('turn_latency_p50_seconds', summary.get('turn_latency_p50_seconds', model.get('turn_latency_p50_seconds', 'not measured'))),
                usage.get('turn_latency_p95_seconds', summary.get('turn_latency_p95_seconds', model.get('turn_latency_p95_seconds', 'not measured'))),
                usage.get('turn_latency_sample_count', summary.get('turn_latency_sample_count', model.get('turn_latency_sample_count', 'not measured'))),
                usage.get('reported_cost_usd', 'unknown'),
                usage.get('reserved_or_unknown_cost_usd', 'unknown'),
                usage.get('api_error_calls', 'unknown'),
            ]
            rows.append('| ' + ' | '.join(cell(c) for c in columns) + ' |')
    rows += ['', 'See `summary.json` for complete metrics, per-case checks and failures, aborted runs, call telemetry, and run manifests. `manifest.json` records hashes of the original source files. A provided conversation trace, when included, is a separately identified replay rather than part of the benchmark denominator.', '']
    return '\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_dirs', nargs='+', type=Path)
    parser.add_argument('--replay', type=Path, help='Replay directory containing turns.jsonl and manifest.json')
    args = parser.parse_args()
    sources = []
    secrets = credentials()

    def read(path):
        data = path.read_bytes()
        check(data, path.name, secrets)
        try:
            display = str(path.resolve().relative_to(ROOT))
        except ValueError:
            display = str(path.resolve())
        sources.append({'path': display, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        return data

    runs = []
    for directory in args.run_dirs:
        summary = json.loads(read(directory / 'summary.json'))
        manifest = json.loads(read(directory / 'manifest.json'))
        suite_path = directory / 'suite_manifest.json'
        suite = json.loads(read(suite_path)) if suite_path.exists() else None
        runs.append({'source_run': str(directory), 'summary': compact(summary),
                     'manifest': manifest, 'suite_manifest': suite})
    outputs = {
        'summary.json': (json.dumps({'schema_version': 1, 'runs': runs}, indent=2, ensure_ascii=False) + '\n').encode(),
        'comparison.md': comparison(runs).encode(),
    }
    if args.replay:
        trace = read(args.replay / 'turns.jsonl')
        # Validate records without modifying their evidence or manufacturing outcomes.
        for line in trace.decode().splitlines():
            if line.strip():
                json.loads(line)
        outputs['original-conversation.jsonl'] = trace
        outputs['replay-manifest.json'] = read(args.replay / 'manifest.json')
    manifest = {
        'schema_version': 1,
        'source_run_dirs': [str(p) for p in args.run_dirs],
        'replay_source': str(args.replay) if args.replay else None,
        'scope': 'Explicit selected experiment snapshots; full scored turns removed from summaries. Original replay retained only when requested. No claim that all experiments or all intended cases completed.',
        'source_files': sources,
        'outputs': {name: hashlib.sha256(data).hexdigest() for name, data in outputs.items()},
    }
    outputs['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    for name, data in outputs.items():
        check(data, name, secrets)
    target = ROOT / 'examples'
    target.mkdir(exist_ok=True)
    # Avoid silently retaining a trace from a different export selection.
    if not args.replay and (target / 'original-conversation.jsonl').exists():
        raise SystemExit('Existing replay export requires explicit --replay to keep provenance consistent')
    for name, data in outputs.items():
        (target / name).write_bytes(data)
    print(f'Exported {len(runs)} run snapshot(s) to examples; no submission archive created.')


if __name__ == '__main__':
    main()
