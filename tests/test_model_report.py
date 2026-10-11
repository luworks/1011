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

def test_compact_consumer_preserves_workflow_and_all_denominators(tmp_path):
    compact={'repeats':3,'models':[{'model_id':'same','config_id':'same/high','configuration':{'reasoning_effort':'high'},'source_run_manifest':{'prompt_version':'workflow-v8','code_sha256':'frozen'},'summary':{'planned_runs':48,'completed_runs':40,'unique_scenarios':16,'success_against_planned':{'numerator':39,'denominator':48,'rate':39/48}},'usage':{'reported_cost_usd':.2,'reserved_or_unknown_cost_usd':.1,'call_count':80}}]}
    (tmp_path/'summary.json').write_text(json.dumps(compact))
    rows,_=m.extract(tmp_path,'acceptance')
    row=rows[0]
    assert (row['prompt'],row['thinking'],row['repeats'])==('workflow-v8','high',3)
    assert (row['planned'],row['completed'],row['success_against_planned_counts'])==(48,40,'39/48')
    assert row['reserved_cost']==.1 and row['call_count']==80

def test_policy_aggregate_keeps_pairs_and_rejects_wrong_sum(tmp_path):
    counts={'improved':2,'regressed':1,'unchanged_pass':6,'unchanged_fail':1}
    x={'code_sha256':'old-v5','controls':{'selected_projected_suite':{'scenario_count':5},'repeats':2},'scoring_audit':{'overlay_sha256':'audit-v2','scope':'offline'},'claim_scope':'existing cases','experiments':[{'config':{'config_id':'sol/medium'},'manifest':{'snapshots':{'baseline':{'prompt_version':'workflow-v5'}}},'matched':{'planned_pairs':12,'matched_completed_pairs':10,'missing_or_technical_pairs':2,'counts':{'raw':dict(counts),'final':dict(counts)}},'summaries':{'baseline':{'completed_runs':10,'planned_runs':12},'candidate':{'completed_runs':10,'planned_runs':12}},'usage':{'baseline':{},'candidate':{}}}]}
    p=tmp_path/'results.json';p.write_text(json.dumps(x));rows=m.policy_snapshot(p)['rows']
    assert rows[0]['raw_baseline_pass']==7 and rows[0]['raw_candidate_pass']==8
    assert rows[0]['planned']==12 and rows[0]['baseline_reported_cost_usd'] is None
    x['experiments'][0]['matched']['counts']['raw']['improved']=3;p.write_text(json.dumps(x))
    with pytest.raises(ValueError):m.policy_snapshot(p)
