"""Benchmark orchestration tests; injected providers never contact a network."""
import importlib.util
import json
from pathlib import Path
from threading import Lock
import time

import pytest

spec = importlib.util.spec_from_file_location('benchmark', Path(__file__).parents[1] / 'scripts/benchmark.py')
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


def args_for(tmp_path, extra=()):
    matrix = tmp_path / 'matrix.json'
    matrix.write_text(json.dumps({'models': [
        {'config_id': 'vendor/model/low', 'provider': 'openai', 'model': 'original-model'},
        {'config_id': 'vendor/model/high', 'provider': 'openai', 'model': 'original-model'}]}))
    cases = tmp_path / 'cases.json'
    cases.write_text(json.dumps([
        {'id': 'a', 'split': 'dev', 'expected': {'questions': []}},
        {'id': 'b', 'split': 'dev', 'expected': {'questions': []}},
        {'id': 'c', 'split': 'frozen', 'expected': {'questions': []}}]))
    return benchmark.parser().parse_args(['--matrix', str(matrix), '--cases', str(cases),
        '--output', str(tmp_path / 'output'), '--ledger', str(tmp_path / 'budget.json'), *extra])


class FakeProvider:
    def __init__(self, config, budget):
        self.config, self.budget, self.calls = config, budget, []


def test_selection_preserves_matrix_order_and_subset(tmp_path):
    args = args_for(tmp_path, ['--case-id', 'b', '--only-config', 'vendor/model/high'])
    configs, cases, repeats, selection = benchmark.select(args)
    assert configs[0]['config_id'] == 'vendor/model/high'
    assert configs[0]['model'] == 'original-model'
    assert [c['id'] for c in cases] == ['b']
    assert repeats == 1
    assert selection['scope'] == 'subset'
    assert selection['parent_suite']['scenario_count'] == 2
    args.suite, args.case_id = 'frozen', None
    assert benchmark.select(args)[2] == 3


@pytest.mark.parametrize('flags', [ ['--case-id', 'unknown'], ['--only-config', 'unknown'], ['--jobs', '0'], ['--repeats', '0'] ])
def test_bad_selection_rejected(tmp_path, flags):
    with pytest.raises(ValueError):
        benchmark.select(args_for(tmp_path, flags))


def test_concurrent_configs_shared_ledger_sequential_cases(tmp_path):
    args = args_for(tmp_path)
    Path(args.ledger).write_text(json.dumps({'earlier': {'cost_usd': 2.7, 'status': 'usage_reported'}}))
    active, maximum, providers, call_order = set(), [0], [], {}
    lock = Lock()
    def factory(config, budget):
        p = FakeProvider(config, budget)
        providers.append(p)
        return p
    def runner(case, provider, corpus):
        assert 'expected' not in case
        cid = provider.config['config_id']
        with lock:
            assert cid not in active
            active.add(cid)
            maximum[0] = max(maximum[0], len(active))
            call_order.setdefault(cid, []).append(case['id'])
        token = provider.budget.reserve(.01)
        time.sleep(.04)
        provider.budget.settle(token, .005)
        provider.calls.append({'cost_usd': .005, 'cost_status': 'usage_reported', 'latency_seconds': .02})
        with lock:
            active.remove(cid)
        return [{'reply': '', 'decisions': [], 'latency_seconds': .04}]
    assert benchmark.execute(args, provider_factory=factory, runner=runner) == 0
    assert maximum[0] == 2
    assert providers[0].budget is providers[1].budget
    assert providers[0].budget.spent == pytest.approx(2.72)
    assert all(v == ['a', 'b'] for v in call_order.values())
    root = Path(args.output)
    index = json.loads((root / 'index.json').read_text())
    assert [r['config_id'] for r in index['models']] == ['vendor/model/low', 'vendor/model/high']
    snapshot = json.loads((root / 'manifest.json').read_text())
    for row in index['models']:
        directory = root / row['directory']
        current = json.loads((directory / 'manifest.json').read_text())
        assert current['started_at'] == snapshot['started_at']
        report = json.loads((directory / 'summary.json').read_text())['models'][0]
        assert report['summary']['completed_runs'] == 2
        assert report['records'][0]['turns'][0]['latency_seconds'] == .04
        assert len((directory / 'turns.jsonl').read_text().splitlines()) == 2


def test_budget_exhaustion_keeps_every_candidate(tmp_path):
    args = args_for(tmp_path)
    Path(args.ledger).write_text(json.dumps({'prior': {'cost_usd': 25, 'status': 'usage_reported'}}))
    def forbidden(*a):
        raise AssertionError('No runner should start')
    assert benchmark.execute(args, provider_factory=FakeProvider, runner=forbidden) == 2
    root = Path(args.output)
    summary = json.loads((root / 'summary.json').read_text())
    assert len(summary['models']) == 2
    assert all(r['summary']['completed_runs'] == 0 for r in summary['models'])
    assert all(r['summary']['planned_runs'] == 2 for r in summary['models'])


def test_provider_error_is_saved_without_sensitive_exception_text(tmp_path):
    args = args_for(tmp_path)
    def factory(*a):
        raise RuntimeError('SECRET sentinel response')
    assert benchmark.execute(args, provider_factory=factory) == 2
    root = Path(args.output)
    report = json.loads((root / 'summary.json').read_text())
    assert len(report['models']) == 2
    assert all(r['summary']['technical_failure_runs'] == 2 for r in report['models'])
    assert 'SECRET' not in ''.join(p.read_text() for p in root.rglob('*.json*'))


def test_directory_names_are_safe_and_collision_resistant():
    a = benchmark.config_directory('../../vendor/a/b')
    b = benchmark.config_directory('../../vendor/a-b')
    assert '/' not in a and '..' not in a and a != b


def test_default_matrix_obeys_user_effort_ceiling():
    assert benchmark.parser().parse_args(['--output','example']).matrix == 'config/eval-models-high.json'


@pytest.mark.parametrize('effort',['xhigh','max','ultra'])
def test_eval_rejects_above_high_before_requests(tmp_path, effort):
    args=args_for(tmp_path, [])
    path=Path(args.matrix)
    matrix=json.loads(path.read_text())
    matrix['models'][0]['reasoning_effort']=effort
    path.write_text(json.dumps(matrix))
    with pytest.raises(ValueError,match='ceiling'):
        benchmark.select(args)
