import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('finalize_eval', Path(__file__).resolve().parents[1] / 'scripts/finalize_evaluation.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(root, suite='dev', repeats=1):
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
    config = {'config_id': 'test/high', 'provider': 'test', 'model': 'test', 'reasoning_effort': 'high'}
    manifest = {'planned_models': [config], 'code_sha256': 'code', 'prompt_version': 'prompt', 'corpus_version': 'corpus'}
    metric = {'numerator': repeats, 'denominator': repeats, 'rate': 1.0}
    report = {'config_id': config['config_id'], 'model_id': 'test', 'manifest': {'sha256': 'oracle'}, 'selection': {'scope': 'full_suite'},
        'summary': {'completion_status': 'complete', 'planned_runs': repeats, 'completed_runs': repeats,
            'unique_scenarios': 1, 'unique_completed_scenarios': 1, 'critical_final_failures': 0,
            'final_unsupported_tax_claims': 0, 'mandatory_escalation_recall': metric,
            'conversation_success': metric, 'success_against_planned': metric,
            'pre_gate_assertion_success': metric, 'post_gate_assertion_success': metric},
        'usage': {'cost_status': 'complete', 'cost_per_successful_conversation_usd': .01,
            'reported_cost_usd': .01 * repeats, 'reserved_or_unknown_cost_usd': 0,
            'input_tokens': 100, 'output_tokens': 50, 'turn_latency_p50_seconds': 1, 'turn_latency_p95_seconds': 1},
        'records': [{'case_id': 'one', 'repeat': i+1, 'passed': True, 'turns': [{'latency_seconds': 1}]} for i in range(repeats)]}
    write(root / 'manifest.json', manifest)
    write(root / 'one/manifest.json', manifest)
    write(root / 'index.json', {'models': [{'config_id': config['config_id'], 'directory': 'one', 'status': 'complete'}]})
    write(root / 'summary.json', {'suite': suite, 'repeats': repeats, 'models': [report]})
    return root


def test_development_never_invokes_final_selector(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'select_models', lambda _: pytest.fail('selector called on development'))
    compact, selection, md = module.finalize(fixture(tmp_path))
    assert selection['winner'] is None
    assert selection['status'] == 'not_final_stage'
    assert compact['planned_configurations'] == 1
    assert compact['models'][0]['reasoning_effort'] == 'high'
    assert 'original 16-case collection was exposed' in md
    assert 'fixtures/acceptance_v2.json' in md
    assert compact['stage_cost']['usage_priced_usd'] == .01


def test_frozen_three_repeats_invokes_selector_and_preserves_result(tmp_path):
    compact, selection, md = module.finalize(fixture(tmp_path, 'frozen', 3))
    assert selection['status'] == 'selected'
    assert selection['winner'] == 'test/high'
    assert compact['models'][0]['summary']['unique_scenarios'] == 1
    assert compact['models'][0]['summary']['planned_runs'] == 3
    assert 'test/high' in md


def test_shared_ledger_never_added_to_stage_cost(tmp_path):
    root = fixture(tmp_path / 'run')
    ledger = tmp_path / 'ledger.json'
    ledger.write_text(json.dumps({'a': {'cost_usd': 10, 'status': 'usage_reported'}, 'b': {'cost_usd': 2, 'status': 'reserved_or_unknown'}}))
    compact, _, _ = module.finalize(root, ledger=ledger)
    assert compact['stage_cost']['usage_priced_usd'] == .01
    assert compact['shared_ledger_snapshot']['total_accounted_upper_bound_usd'] == 12
    assert compact['shared_ledger_snapshot']['reserved_or_unknown_upper_bound_usd'] == 2


def test_pending_process_cannot_be_finalized(tmp_path):
    root = fixture(tmp_path)
    path = root / 'index.json'
    data = json.loads(path.read_text()); data['models'][0]['status'] = 'pending'; path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='still pending'):
        module.finalize(root)


def edit_report(root, mutate):
    path=root/'summary.json'
    data=json.loads(path.read_text())
    mutate(data['models'][0])
    path.write_text(json.dumps(data))


def test_candidate_only_fix_contract_failure_preserved_without_final_failure(tmp_path):
    root=fixture(tmp_path)
    def mutate(report):
        report['summary']['metric_version']='closed-oracle-v2-safety-utility-separated'
        report['summary']['fix_contract_success']={'numerator':0,'denominator':1,'rate':0.0}
        report['records'][0].update(candidate_passed=False, critical_final_failure=False,
            fix_contract_assessed=True, fix_contract_passed=False,
            fix_contract_errors=['candidate_checks: disallowed tax adjustment'],
            candidate_contract_errors=['disallowed tax adjustment'],
            checks=[{'intent':'taxes','pre_errors':['wrong candidate'],'post_errors':[]}])
    edit_report(root,mutate)
    compact,_,md=module.finalize(root)
    model=compact['models'][0];failure=model['failure_cases'][0]
    assert failure['final_passed'] is True
    assert failure['candidate_passed'] is False
    assert failure['fix_contract_errors']
    assert failure['assertion_errors'][0]['post_errors']==[]
    assert model['diagnostics']['final_utility_failure_runs']==0
    assert model['diagnostics']['fix_contract_failure_runs']==1
    assert model['metric_version']=='closed-oracle-v2-safety-utility-separated'
    assert 'Fix-contract success' in md and '0/1 (0.0%)' in md


def test_compact_distinguishes_utility_safety_and_technical_failures(tmp_path):
    root=fixture(tmp_path,repeats=3)
    def mutate(report):
        for r in report['records']:r.update(passed=False,candidate_passed=False)
        report['records'][0].update(critical_final_failure=False, turn_errors=['missing useful answer'])
        report['records'][1].update(critical_final_failure=True, critical_assertion_errors=['incorrect non-null amount'])
        report['records'][2].update(critical_final_failure=False, technical_errors=['ProviderError'])
    edit_report(root,mutate)
    compact,_,_=module.finalize(root)
    model=compact['models'][0]
    assert model['diagnostics']['final_utility_failure_runs']==1
    assert model['diagnostics']['final_severity_assessed_runs']==3
    assert model['failure_cases'][1]['critical_assertion_errors']==['incorrect non-null amount']
    assert model['failure_cases'][2]['technical_errors']==['ProviderError']


def test_legacy_absent_contract_or_severity_not_reported_as_passed(tmp_path):
    root=fixture(tmp_path)
    edit_report(root,lambda r:r['records'][0].update(passed=False))
    compact,_,md=module.finalize(root)
    model=compact['models'][0]
    assert model['metric_version'] is None
    assert model['diagnostics']['fix_contract_assessed_runs']==0
    assert model['diagnostics']['candidate_assessed_runs']==0
    assert model['diagnostics']['final_severity_assessed_runs']==0
    assert model['diagnostics']['final_utility_failure_runs']==0
    assert model['failure_cases'][0]['fix_contract_passed'] is None
    assert 'not recorded' in md and 'not assessed' in md
