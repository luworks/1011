from policy_agent.selection import select_models


def entry(model='a',cost=.1,latency=2,success=1,thinking='default'):
    return {'config_id':model+'-'+thinking,'suite':'frozen','repeats':3,'run_manifest':{'prompt_version':'p','code_sha256':'c','corpus_version':'s'},'report':{'model_id':model,'manifest':{'sha256':'suite'},'selection':{'scope':'full_suite'},'summary':{'completion_status':'complete','completed_runs':3,'planned_runs':3,'conversation_success':{'rate':success},'critical_final_failures':0,'final_unsupported_tax_claims':0,'mandatory_escalation_recall':{'numerator':3,'denominator':3}},'records':[{'case_id':'scenario-one','repeat':repeat+1,'turns':[{'latency_seconds':latency}]} for repeat in range(3)],'usage':{'cost_status':'complete','cost_per_successful_conversation_usd':cost}}}


def test_speed_before_cost_equal_quality():
    r=select_models([entry('cheap',.01,2),entry('fast',.2,1.5)])
    assert r['winner']=='fast-default'


def test_no_quality_floor_accuracy_first():
    r=select_models([entry('accurate',.5,4,.94),entry('fast',.01,1,.9)])
    assert r['winner']=='accurate-default'


def test_incomplete_other_model_prevents_winner():
    b=entry('b');b['report']['summary']['completion_status']='incomplete'
    assert select_models([entry(),b])['status']=='pending'


def test_missing_latency_never_uses_call_latency():
    e=entry();e['report']['records'][0]['turns']=[{}]
    e['report']['usage']['call_latency_p95_seconds']=1
    assert select_models([e])['winner'] is None


def test_unknown_final_audit_blocks_selection():
    e=entry();del e['report']['summary']['final_unsupported_tax_claims']
    assert select_models([e])['status']=='pending'


def test_mismatched_provenance_blocks_selection():
    e=entry('b');e['run_manifest']['code_sha256']='different'
    assert select_models([entry(),e])['status']=='pending'


def test_critical_failure_disqualifies_faster_model():
    e=entry('unsafe',.001,.1);e['report']['summary']['critical_final_failures']=1
    assert select_models([e,entry('safe')])['winner']=='safe-default'


def test_model_thinking_configs_are_separate():
    r=select_models([entry('same',thinking='low'),entry('same',latency=3,thinking='high')])
    assert r['winner']=='same-low'


def test_equal_latency_uses_cost_but_labels_tentative():
    r=select_models([entry('expensive',.2),entry('cheap',.01)])
    assert r['winner']=='cheap-default'
    assert r['status']=='tentative'


def test_missing_saved_records_blocks_selection():
    e=entry();e['report']['records'].pop()
    assert select_models([e])['status']=='pending'


def test_development_screen_cannot_select_final_winner():
    e=entry();e['suite']='dev'
    r=select_models([e])
    assert r['status']=='pending' and r['winner'] is None
    assert any('frozen suite' in x for x in r['models'][0]['pending_reasons'])


def test_final_selection_requires_three_repeats():
    e=entry();e['repeats']=2
    assert select_models([e])['status']=='pending'


def test_missing_case_id_cannot_create_independent_bootstrap_cluster():
    e=entry();del e['report']['records'][0]['case_id']
    r=select_models([e])
    assert r['status']=='pending' and r['winner'] is None
    assert any('case_id' in x for x in r['models'][0]['pending_reasons'])


def test_declared_repeats_require_matching_scenario_records():
    e=entry();e['report']['records'][0]['case_id']='different-scenario'
    assert select_models([e])['status']=='pending'


def test_bootstrap_keeps_all_repeats_and_turns_in_unique_scenario():
    e=entry()
    for record, latency in zip(e['report']['records'], (1, 2, 99)):
        record['turns']=[{'latency_seconds':latency}, {'latency_seconds':latency+1}]
    r=select_models([e]);row=r['models'][0]
    # One scenario always resamples its full six-turn cluster, including the
    # slow repeat; resampling three independent records would vary this bound.
    assert row['turn_p95_bootstrap_interval_seconds']==[100,100]
    assert row['unique_scenario_count']==1
    assert row['conversation_run_count']==3
    assert row['turn_latency_sample_count']==6
    assert row['bootstrap_resample_count']==1000
    assert 'Descriptive' in r['quality_comparison']
