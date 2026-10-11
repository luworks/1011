"""CLI acceptance smoke tests: no network requests and no real credentials."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def invoke(*args):
    env = dict(os.environ)
    # Override dotenv without reading or exposing a real credential. Every command
    # here exits before provider initialization, or explicitly runs offline.
    env.update(OPENAI_API_KEY='cli-test-openai-sentinel',
               ANTHROPIC_API_KEY='cli-test-anthropic-sentinel')
    return subprocess.run([sys.executable, '-m', 'policy_agent.cli', *map(str, args)],
                          cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)


def test_doctor_reports_presence_not_secret():
    result = invoke('doctor')
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data['corpus_entries'] == 15
    assert data['api_access'] == 'not checked'
    assert data['keys'] == {'OPENAI_API_KEY': True, 'ANTHROPIC_API_KEY': True}
    assert 'sentinel' not in result.stdout + result.stderr


def test_offline_replay_records_evidence_and_source_provenance(tmp_path):
    out, ledger = tmp_path/'replay', tmp_path/'budget.json'
    result = invoke('replay', '--offline', '--output', out, '--ledger', ledger)
    assert result.returncode == 0, result.stderr
    summary = json.loads((out/'summary.json').read_text())
    manifest = json.loads((out/'manifest.json').read_text())
    turns = [json.loads(line) for line in (out/'turns.jsonl').read_text().splitlines()]
    assert len(turns) == summary['turns'] == 6
    assert summary['technical_failures'] == 0
    assert summary['mode'] == manifest['mode'] == 'offline_fixture'
    assert manifest['calls'] == manifest['models'] == []
    assert manifest['ledger_total_usd'] == 0
    assert all(t['mode'] == 'offline_fixture' and t['error'] is None for t in turns)
    assert any(d['amount'] == '82.50' for t in turns for d in t['decisions'])
    taxes = [d for t in turns for d in t['decisions'] if d['question'] == 'taxes']
    assert taxes and taxes[0]['answer_status'] == 'partial'
    assert taxes[0]['action_status'] == 'requires_human'
    for turn in turns:
        for decision in turn['decisions']:
            assert decision['evidence']
            for evidence in decision['evidence']:
                assert evidence['source_id'].startswith(('Rule ', 'KB-'))
                assert evidence['start_line'] >= 1
                lines = (ROOT/evidence['path']).read_text().splitlines()
                assert evidence['excerpt'] == '\n'.join(lines[evidence['start_line']-1:evidence['end_line']]).strip()
                assert len(evidence['version']) == 64
    facts = turns[-1]['facts']
    assert any(f['source_type'] == 'provided_transcript_confirmation' for f in facts)
    persisted = '\n'.join(p.read_text() for p in out.iterdir())
    assert 'sentinel' not in persisted
    # Original transcript identifiers and payment digits are never logged.
    assert 'NMB-7745213' not in persisted
    assert '4471' not in persisted
    assert 'sentinel' not in result.stdout + result.stderr


def test_unknown_model_is_rejected_before_request(tmp_path):
    ledger = tmp_path/'budget.json'
    result = invoke('replay', '--model', 'not-in-priced-matrix', '--output', tmp_path/'run', '--ledger', ledger)
    assert result.returncode == 2
    assert 'not in the priced model matrix' in result.stderr
    assert not ledger.exists()
    assert 'sentinel' not in result.stdout + result.stderr


def test_report_round_trip_and_missing_directory(tmp_path):
    (tmp_path/'summary.json').write_text(json.dumps({'example': 'recorded'}))
    result = invoke('report', '--run-dir', tmp_path)
    assert result.returncode == 0
    assert json.loads(result.stdout) == {'example': 'recorded'}
    missing = invoke('report', '--run-dir', tmp_path/'missing')
    assert missing.returncode == 2
    assert 'FileNotFoundError' in missing.stderr


def packaging_module():
    spec = importlib.util.spec_from_file_location('package_under_test', ROOT/'scripts/package.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_package_selection_excludes_credentials_caches_and_runs():
    package = packaging_module()
    paths = [p.relative_to(ROOT) for p in package.selected_files()]
    assert Path('.env.example') in paths
    assert Path('README.md') in paths
    assert Path('src/policy_agent/cli.py') in paths
    for path in paths:
        assert not set(path.parts) & {'.venv', '.git', '__pycache__', '.pytest_cache', 'runs'}
        assert 'dist' not in path.parts or path == Path('report/dist/index.html')
        assert path.name == '.env.example' or not path.name.startswith('.env')
        assert path.suffix not in ('.pyc', '.pyo')
        assert (path.parts[0] in package.TREES or path.as_posix() in package.FILES
                or path in {Path('report/dist/index.html'), Path('model-evaluation-report.html')})


def test_package_secret_check_refuses_without_echoing_value():
    package = packaging_module()
    secret = b'unique-credential-sentinel-value'
    with pytest.raises(SystemExit) as exc:
        package.check(b'example '+secret, 'example.json', [secret])
    assert 'example.json' in str(exc.value)
    assert secret.decode() not in str(exc.value)


def test_evaluation_subset_preserves_parent_and_start_snapshot(tmp_path, monkeypatch):
    from policy_agent import cli
    import hashlib

    cases=[{'id':f'case-{i}', 'split':'frozen', 'messages':['Question'],
            'expected':{'questions':[]}} for i in range(3)]
    case_path=tmp_path/'cases.json'
    case_path.write_text(json.dumps(cases))
    out=tmp_path/'evaluation'
    snapshots=[]
    original_snapshot=cli.start_snapshot
    def record_snapshot(*args):
        value=original_snapshot(*args)
        snapshots.append(value.copy())
        return value
    monkeypatch.setattr(cli,'start_snapshot',record_snapshot)
    class FakeProvider:
        def __init__(self,config,budget):
            self.config=config
            self.calls=[]
    monkeypatch.setattr(cli,'Provider',FakeProvider)
    def run(case,provider,corpus):
        assert snapshots, 'Code snapshot must exist before execution'
        assert (out/'manifest.json').exists()
        return [{'decisions':[], 'candidate':{'questions':[]}, 'reply':'', 'error':None}]
    monkeypatch.setattr(cli,'run_scenario',run)
    monkeypatch.setattr(sys,'argv',['prototype','evaluate','--cases',str(case_path),
        '--suite','frozen','--limit','1','--only-model','gpt-5.4-mini','--matrix','config/development-models.json',
        '--output',str(out),'--ledger',str(tmp_path/'ledger.json')])
    assert cli.main()==0
    summary=json.loads((out/'summary.json').read_text())
    manifest=json.loads((out/'manifest.json').read_text())
    selection=summary['selection']
    assert summary['repeats']==3
    assert selection['scope']=='subset'
    assert selection['parent_suite']['scenario_count']==3
    assert selection['selected_suite']['scenario_count']==1
    assert summary['models'][0]['parent_suite_planned_runs']==9
    assert summary['models'][0]['summary']['planned_runs']==3
    assert len(snapshots)==1
    assert manifest['planned_models'][0]['model']=='gpt-5.4-mini'
    assert manifest['code_sha256']==snapshots[0]['code_sha256']
    assert manifest['started_at']==snapshots[0]['started_at']
    assert manifest['evaluation_selection']==selection
    assert selection['cases_file_sha256']==hashlib.sha256(case_path.read_bytes()).hexdigest()


@pytest.mark.parametrize('bad_cases,extra,error', [
    ([{'id':'same','split':'dev'},{'id':'same','split':'frozen'}], [], 'Duplicate scenario IDs'),
    ([{'id':'one','split':'typo'}], [], 'split must be dev or frozen'),
    ([{'id':'one','split':'dev'}], ['--limit','0'], 'Limit must be positive'),
    ([{'id':'one','split':'dev'}], ['--limit','-2'], 'Limit must be positive'),
    ([{'id':'one','split':'dev'}], ['--repeats','0'], 'Repeats must be positive'),
])
def test_invalid_evaluation_fails_before_provider(tmp_path,monkeypatch,capsys,bad_cases,extra,error):
    from policy_agent import cli
    path=tmp_path/'cases.json'
    path.write_text(json.dumps(bad_cases))
    def forbidden(*args,**kwargs):
        raise AssertionError('No API provider should be initialized')
    monkeypatch.setattr(cli,'Provider',forbidden)
    monkeypatch.setattr(sys,'argv',['prototype','evaluate','--cases',str(path),
        '--output',str(tmp_path/'out'),'--ledger',str(tmp_path/'ledger.json'),*extra])
    assert cli.main()==2
    assert error in capsys.readouterr().err
