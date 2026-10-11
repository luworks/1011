from argparse import Namespace
import copy
import json
from pathlib import Path
import shutil

import pytest

from policy_agent import comparison
from policy_agent.corpus import Corpus
from policy_agent.evaluation import load_cases, freeze_manifest, model_input
from policy_agent.versions import verify_snapshot, version_directory

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '20261011T192840169969Z-original'
CANDIDATE = '20261011T192840174385Z-clarified'


def projected_cases():
    return comparison.project_oracles(load_cases(ROOT/'fixtures/scenarios.json'),
        json.loads((ROOT/'fixtures/policy-comparison-oracle.json').read_text()))


def test_version_pair_loads_and_evidence_resolves():
    old, new = [Corpus(version_directory(v, ROOT)) for v in (BASELINE, CANDIDATE)]
    assert old.version == Corpus(ROOT).version != new.version
    assert old.entries.keys() == new.entries.keys()
    evidence = new.get('Rule 4')
    assert Path(evidence.path).is_file()
    assert evidence.excerpt in Path(evidence.path).read_text()


def test_hash_and_parent_tampering_rejected(tmp_path):
    for version in (BASELINE, CANDIDATE):
        shutil.copytree(version_directory(version, ROOT), tmp_path/version)
    source = next((tmp_path/CANDIDATE/'exam').glob('*.md'))
    source.write_text(source.read_text()+'changed')
    with pytest.raises(ValueError, match='hash mismatch'):
        verify_snapshot(tmp_path/CANDIDATE)
    shutil.copyfile(version_directory(CANDIDATE, ROOT)/'exam'/source.name, source)
    parent = tmp_path/BASELINE/'manifest.json'
    parent.write_text(parent.read_text()+'\n')
    with pytest.raises(ValueError, match='Parent manifest changed'):
        verify_snapshot(tmp_path/CANDIDATE)


@pytest.mark.parametrize('value', ['../exam', '.', '..', '/absolute/path'])
def test_version_path_traversal_rejected(value):
    with pytest.raises(ValueError):
        version_directory(value, ROOT)


def test_masks_every_turn_and_never_leaks_oracle():
    case = next(c for c in projected_cases() if c['id']=='over_four_hours')
    for q in case['expected']['questions'] + [q for t in case['expected']['turns'] for q in t['questions']]:
        assert 'amount' not in q
    payload = model_input(case)
    assert 'expected' not in payload
    assert 'OD-05' not in json.dumps(payload)


def test_overlay_rejects_changed_case_oracle():
    cases = load_cases(ROOT/'fixtures/scenarios.json')
    overlay = json.loads((ROOT/'fixtures/policy-comparison-oracle.json').read_text())
    cases[0]['expected']['questions'][0]['amount']='99.00'
    with pytest.raises(ValueError, match='exact source suite'):
        comparison.project_oracles(cases, overlay)


def test_unresolved_amount_has_no_unique_gold_but_definite_gate_claim_is_flagged():
    case = next(c for c in projected_cases() if c['id']=='rounding')
    def score(amount, status, action):
        return comparison.score_projected(case,[{'decisions':[{
            'question':'outage_credit','amount':amount,'policy_ids':['Rule 3'],
            'answer_status':status,'action_status':action}],
            'candidate':{'questions':[]},'error':None,'reply':''}])
    for amount in ('3.33','3.34'):
        result = score(amount,'grounded','eligible_for_simulation')
        assert not any('amount:' in e for check in result['checks'] for e in check['post_errors'])
        assert result['boundary_errors']['final'] and not result['passed']
    result=score(None,'needs_information','pending_verification')
    assert result['passed'] and not result['fully_resolved']


def test_tax_refusal_labels_not_unique_but_yes_no_is_unsupported():
    case = next(c for c in projected_cases() if c['id']=='tax_gap')
    for label in ('partial','unsupported'):
        turn={'candidate':{'questions':[{'intent':'taxes','policy_ids':['KB-1004'],
            'answer_status':label,'tax_adjustment':'unknown','evidence':[{'source_id':'KB-1004','quote':'base'}]}]},
            'retrieved':[{'source_id':'KB-1004','excerpt':'base'}], 'decisions':[], 'error':None}
        result=comparison.score_projected(case,[turn])
        assert result['candidate_passed']
        turn['candidate']['questions'][0]['tax_adjustment']='no'
        assert comparison.score_projected(case,[turn])['boundary_errors']['raw']


def test_matching_never_turns_technical_failure_into_improvement():
    row={'case_id':'x','repeat':1,'technical_errors':['ProviderError']}
    result=comparison.compare_records({'baseline':[row],'candidate':[row]},planned=2)
    assert result['matched_completed_pairs']==0
    assert result['missing_or_technical_pairs']==2


def test_above_high_config_rejected_before_any_provider_or_output(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('Provider must not be initialized')
    monkeypatch.setattr(comparison,'Provider',forbidden)
    args=Namespace(repeats=1,jobs=1,baseline=BASELINE,candidate=CANDIDATE,
        matrix=ROOT/'config/models.json',config_id='openai/gpt-6.1-sol/reasoning/xhigh',
        output=tmp_path/'out')
    with pytest.raises(ValueError, match='ceiling is high'):
        comparison.run_comparison(args)
    assert not (tmp_path/'out').exists()


def test_full_pair_runner_fixes_controls_and_preserves_raw_gate_difference(tmp_path, monkeypatch):
    case={'id':'demo','split':'dev','trusted_context':{},'messages':[],
          'expected':{'questions':[{'intent':'outage_credit','policy':'Rule 3','amount':'82.50'}]}}
    suite=tmp_path/'cases.json';suite.write_text(json.dumps([case]))
    overlay=tmp_path/'oracle.json';overlay.write_text(json.dumps({
        'source_suite_sha256':freeze_manifest([case])['sha256'],'cases':{}}))
    class FakeProvider:
        def __init__(self, config, budget):
            self.config=copy.deepcopy(config);self.calls=[]
    seen=[]
    def run(payload, provider, corpus):
        assert 'expected' not in payload
        seen.append((payload,provider.config,corpus.policy_snapshot['version_id']))
        source=corpus.get('Rule 3').model_dump(mode='json')
        amount='75.00' if corpus.policy_snapshot['status']=='original' else '82.50'
        return [{'error':None,'retrieved':[source],'reply':'supported',
            'decisions':[{'question':'outage_credit','policy_ids':['Rule 3'],'amount':'82.50'}],
            'candidate':{'questions':[{'intent':'outage_credit','policy_ids':['Rule 3'],'amount':amount,
                'evidence':[{'source_id':'Rule 3','quote':'separate policy track'}]}]}}]
    monkeypatch.setattr(comparison,'Provider',FakeProvider)
    monkeypatch.setattr(comparison,'run_scenario',run)
    config_id='anthropic/claude-haiku-5-5/disabled/low'
    args=Namespace(baseline=BASELINE,candidate=CANDIDATE,config_id=config_id,
        matrix=ROOT/'config/models.json',cases=suite,oracle_overlay=overlay,suite='all',
        repeats=2,jobs=2,max_cost_usd=25,ledger=tmp_path/'ledger.json',output=tmp_path/'out')
    assert comparison.run_comparison(args)==0
    result=json.loads((tmp_path/'out/summary.json').read_text())
    assert result['matched']['counts']['raw']['improved']==2
    assert result['matched']['counts']['final']['unchanged_pass']==2
    assert all(s[1]==seen[0][1] and s[0]==seen[0][0] for s in seen)
    manifest=json.loads((tmp_path/'out/manifest.json').read_text())
    assert manifest['snapshots']['baseline']['code_sha256']==manifest['snapshots']['candidate']['code_sha256']
    assert manifest['snapshots']['baseline']['corpus_version']!=manifest['snapshots']['candidate']['corpus_version']
