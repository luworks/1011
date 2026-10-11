"""Concurrent configuration sweep with one persistent, total-spend ledger.

Run from the repository root with ``uv run python scripts/benchmark.py``.
Each configuration runs its scenarios sequentially; no model fallback is used.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import sys

from dotenv import load_dotenv

from policy_agent.cli import configurations, dump, manifest, start_snapshot
from policy_agent.corpus import Corpus
from policy_agent.evaluation import attach_usage, evaluate_cases, freeze_manifest, load_cases
from policy_agent.providers import Budget, Provider
from policy_agent.workflow import run_scenario


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--matrix', default='config/eval-models-high.json')
    p.add_argument('--cases', default='fixtures/scenarios.json')
    p.add_argument('--suite', choices=('dev', 'frozen'), default='dev')
    p.add_argument('--case-id', action='append')
    p.add_argument('--only-config', action='append')
    p.add_argument('--repeats', type=int)
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--max-cost-usd', type=float, default=25)
    p.add_argument('--ledger', default='runs/budget.json')
    p.add_argument('--output', required=True)
    return p


def config_directory(config_id):
    slug = re.sub(r'[^A-Za-z0-9_-]+', '-', config_id).strip('-')[:80] or 'config'
    return slug + '-' + hashlib.sha256(config_id.encode()).hexdigest()[:12]


def select(args):
    configs = configurations(args.matrix)
    ids = [c.get('config_id') for c in configs]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('Matrix requires unique nonempty config_id values')
    if args.only_config:
        if set(args.only_config) - set(ids):
            raise ValueError('Unknown --only-config value')
        configs = [c for c in configs if c['config_id'] in args.only_config]
    if not configs:
        raise ValueError('No selected configurations')
    if any(c.get('reasoning_effort', c.get('effort')) in {'xhigh', 'max', 'ultra'} for c in configs):
        raise ValueError('Evaluation effort ceiling is high; filter higher-effort configurations before running')
    all_cases = load_cases(args.cases)
    if any(c.get('split') not in ('dev', 'frozen') for c in all_cases):
        raise ValueError('Every scenario split must be dev or frozen')
    cases = [c for c in all_cases if c['split'] == args.suite]
    parent = freeze_manifest(cases)
    if args.case_id:
        if set(args.case_id) - {c['id'] for c in cases}:
            raise ValueError('Unknown --case-id in selected suite')
        cases = [c for c in cases if c['id'] in args.case_id]
    if not cases:
        raise ValueError('No selected scenarios')
    if args.jobs < 1 or (args.repeats is not None and args.repeats < 1):
        raise ValueError('jobs and repeats must be positive')
    repeats = args.repeats if args.repeats is not None else (3 if args.suite == 'frozen' else 1)
    selection = {'parent_suite': parent, 'selected_suite': freeze_manifest(cases),
                 'scope': 'subset' if len(cases) < parent['scenario_count'] else 'full_suite',
                 'requested_case_ids': args.case_id, 'cases_path': str(args.cases),
                 'cases_file_sha256': hashlib.sha256(Path(args.cases).read_bytes()).hexdigest()}
    return configs, cases, repeats, selection


def execute(args, *, provider_factory=Provider, runner=run_scenario, corpus=None):
    """Injection points allow complete orchestration tests without network calls."""
    configs, cases, repeats, selection = select(args)
    corpus = corpus or Corpus()
    snapshot = start_snapshot(corpus, args.matrix)
    snapshot.update(evaluation_selection=selection, planned_models=configs)
    budget = Budget(args.max_cost_usd, args.ledger)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    index = {'suite': args.suite, 'repeats': repeats, 'jobs': args.jobs,
             'selection': selection, 'models': [
                 {'config_id': c['config_id'], 'directory': config_directory(c['config_id']), 'status': 'pending'}
                 for c in configs]}
    dump(out / 'index.json', index)
    dump(out / 'suite_manifest.json', selection)
    dump(out / 'manifest.json', manifest(snapshot, [], budget, 'evaluation'))

    def worker(config):
        directory = out / config_directory(config['config_id'])
        directory.mkdir()
        dump(directory / 'suite_manifest.json', selection)
        local_snapshot = {**snapshot, 'planned_models': [config]}
        dump(directory / 'manifest.json', manifest(local_snapshot, [], budget, 'evaluation'))
        (directory / 'turns.jsonl').touch()
        provider = None
        failure = None
        try:
            provider = provider_factory(config, budget)
        except Exception as exc:
            failure = type(exc).__name__

        completed_calls = 0

        def run(case):
            nonlocal completed_calls
            repeat = completed_calls // len(cases) + 1
            completed_calls += 1
            if failure:
                turns = [{'error': failure, 'decisions': [], 'reply': ''}]
            else:
                try:
                    turns = runner(case, provider, corpus)
                    turns = [t.model_dump(mode='json') if hasattr(t, 'model_dump') else t for t in turns]
                except Exception as exc:
                    turns = [{'error': type(exc).__name__, 'decisions': [], 'reply': ''}]
            with (directory / 'turns.jsonl').open('a') as stream:
                stream.write(json.dumps({'model': config['model'], 'config_id': config['config_id'],
                                         'case_id': case['id'], 'repeat': repeat, 'turns': turns}) + '\n')
            return turns

        report = evaluate_cases(cases, run, model_id=config['model'], repeats=repeats,
                                can_continue=lambda: budget.spent < budget.limit)
        calls = provider.calls if provider is not None else []
        attach_usage(report, calls)
        report.update(config_id=config['config_id'], selection=selection, calls=calls,
                      parent_suite_planned_runs=selection['parent_suite']['scenario_count'] * repeats,
                      estimated_cost_usd=sum(c.get('cost_usd', 0) for c in calls))
        dump(directory / 'summary.json', {'suite': args.suite, 'repeats': repeats,
                                         'selection': selection, 'models': [report]})
        dump(directory / 'manifest.json', manifest(local_snapshot, [provider] if provider is not None else [], budget, 'evaluation'))
        return report

    reports = {}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(worker, c): c for c in configs}
        for future in as_completed(futures):
            config = futures[future]
            row = next(r for r in index['models'] if r['config_id'] == config['config_id'])
            try:
                report = future.result()
                reports[config['config_id']] = report
                row['status'] = ('failed' if report['summary']['technical_failure_runs'] or report['usage']['api_error_calls'] else report['summary']['completion_status'])
            except Exception as exc:
                # Persist safe exception classes, never provider response text.
                row.update(status='failed', error=type(exc).__name__)
                dump(out / row['directory'] / 'error.json', {'error': type(exc).__name__})
            dump(out / 'index.json', index)
            print(f"{config['config_id']}: {row['status']}", flush=True)
    dump(out / 'summary.json', {'suite': args.suite, 'repeats': repeats, 'selection': selection,
                               'models': [reports[c['config_id']] for c in configs if c['config_id'] in reports],
                               'errors': [r for r in index['models'] if r.get('error')]})
    final_manifest = manifest(snapshot, [], budget, 'evaluation')
    final_manifest['models'] = configs
    final_manifest['calls'] = [call for c in configs for call in reports.get(c['config_id'], {}).get('calls', [])]
    dump(out / 'manifest.json', final_manifest)
    return 2 if any(r['status'] != 'complete' for r in index['models']) else 0


def main(argv=None):
    args = parser().parse_args(argv)
    load_dotenv(Path('.env'), override=False)
    try:
        return execute(args)
    except (ValueError, OSError) as exc:
        print(f'Benchmark failed: {type(exc).__name__}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
