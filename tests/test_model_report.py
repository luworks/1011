import importlib.util
import json
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('build_model_report',Path(__file__).parents[1]/'scripts/build_model_report.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_missing_is_not_zero_and_history_cannot_select(tmp_path):
    (tmp_path/'summary.json').write_text(json.dumps({'models':[{'model_id':'model','summary':{'completed_runs':2,'planned_runs':3,'conversation_success':{'numerator':1,'denominator':2,'rate':.5}},'usage':{}}]}))
    result=m.snapshot([('historical-dev',tmp_path)])
    row=result['queries']['models']['rows'][0]
    assert row['p95'] is None and row['critical'] is None
    assert result['selection']['winner'] is None
    selection=tmp_path/'selection.json';selection.write_text(json.dumps({'winner':'model','status':'selected'}))
    with pytest.raises(ValueError):m.snapshot([('historical-dev',tmp_path)],selection)

def test_config_matching_preserves_thinking(tmp_path):
    configs=[{'model':'same','config_id':'same/low','reasoning_effort':'low'},{'model':'same','config_id':'same/high','reasoning_effort':'high'}]
    (tmp_path/'manifest.json').write_text(json.dumps({'models':configs}))
    (tmp_path/'summary.json').write_text(json.dumps({'models':[{'model_id':'same','config_id':'same/high','summary':{}}]}))
    rows,_=m.extract(tmp_path,'frozen')
    assert rows[0]['thinking']=='high'

def test_pending_index_preserves_planned_configurations(tmp_path):
    (tmp_path/'index.json').write_text(json.dumps({'models':[{'config_id':'openai/gpt-6-luna/reasoning/low','directory':'low','status':'pending'}]}))
    rows,_=m.extract(tmp_path,'screen')
    assert len(rows)==1 and rows[0]['status']=='pending'
    assert 'p95' not in rows[0]
