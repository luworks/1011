from pathlib import Path
from policy_agent.evaluation import load_cases, model_input, freeze_manifest, evaluate_cases, score_case

FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures/scenarios.json'

def test_case_inventory_and_split():
    cases=load_cases(FIXTURES)
    assert len(cases)>=40
    assert len(load_cases(FIXTURES,'dev'))==24
    assert len(load_cases(FIXTURES,'frozen'))==16
    assert len({c['id'] for c in cases})==len(cases)

def test_expectations_never_enter_runner():
    case=load_cases(FIXTURES)[0]
    def run(payload):
        assert 'expected' not in payload
        payload['trusted_context']['fraud']=True
        return []
    result=evaluate_cases([case],run,model_id='fake')
    assert case['trusted_context']['fraud'] is None
    assert result['summary']['conversation_success']['numerator']==0

def test_budget_denominator_preserved():
    cases=load_cases(FIXTURES,'dev')
    result=evaluate_cases(cases,lambda c:[],model_id='fake',repeats=3,can_continue=lambda:False)
    assert result['summary']['planned_runs']==72
    assert result['summary']['skipped_runs']==72
    assert result['summary']['completion_status']=='incomplete'

def test_manifest_changes_with_ground_truth():
    cases=load_cases(FIXTURES)
    first=freeze_manifest(cases)
    cases[0]['expected']['questions'][0]['amount']='99.00'
    assert first['sha256']!=freeze_manifest(cases)['sha256']

def test_candidate_error_not_hidden_by_gate():
    case=load_cases(FIXTURES)[0]
    case['expected']={'questions':case['expected']['questions'][:1]}
    correct={'question':'outage_credit','policy_ids':['Rule 3'],'amount':'82.50','action_status':'pending_verification'}
    wrong={'intent':'outage_credit','policy_ids':['Rule 2'],'amount':'75.00','action_status':'eligible_for_simulation'}
    result=score_case(case,[{'decisions':[correct],'candidate':{'questions':[wrong]}}])
    assert result['passed']
    assert not result['candidate_passed']

def test_error_text_redacted():
    def run(c):raise RuntimeError('secret-key-do-not-store')
    result=evaluate_cases(load_cases(FIXTURES)[:1],run,model_id='fake')
    assert 'secret-key' not in str(result)
    assert result['summary']['technical_failure_runs']==1
    assert result['summary']['api_error_runs']==0

def test_budget_turn_aborts_without_completed_denominator():
    result=evaluate_cases(load_cases(FIXTURES)[:2],lambda c:[{'error':'BudgetExceeded','reply':''}],model_id='fake')
    assert result['summary']['completed_runs']==0
    assert result['summary']['skipped_runs']==2
    assert len(result['aborted_runs'])==1

def test_separate_accuracy_and_refusal_denominators():
    case={'id':'x','split':'dev','expected':{'questions':[{'intent':'outage_credit','policy':'Rule 3','amount':'82.50'},{'intent':'taxes','answer_status':'partial'}]}}
    result=evaluate_cases([case],lambda c:[{'decisions':[{'question':'outage_credit','policy_ids':['Rule 3'],'amount':'82.50','answer_status':'grounded'},{'question':'taxes','answer_status':'unsupported'}]}],model_id='fake')
    s=result['summary']
    assert s['policy_accuracy']['rate']==1
    assert s['amount_accuracy']['denominator']==1
    assert s['answerable_completion']['denominator']==2
    assert s['over_refusal_rate']['rate']==.5

def test_unknown_usage_not_zero_cost():
    from policy_agent.evaluation import attach_usage
    report={'summary':{'conversation_success':{'numerator':1}}}
    attach_usage(report,[{'cost_status':'usage_reported','cost_usd':.1,'input_tokens':2,'output_tokens':3,'latency_seconds':1},{'cost_status':'reserved_or_unknown','cost_usd':.2,'error':'Timeout','latency_seconds':2}])
    assert report['usage']['reported_cost_usd']==.1
    assert report['usage']['cost_per_successful_conversation_usd'] is None
    assert report['usage']['call_latency_p95_seconds']==2
    assert report['usage']['api_error_calls']==1

def test_intermediate_future_information_rejected():
    case={'id':'x','split':'dev','expected':{'questions':[], 'trace_checks':[{'turn_index':0,'forbidden_amounts':['82.50']}]}}
    result=score_case(case,[{'decisions':[{'amount':'82.50'}],'reply':'credit'}])
    assert not result['passed']
    assert 'future/forbidden amount' in result['text_errors'][0]


def test_turn_oracle_rejects_early_wrong_answer_and_extra_intents():
    case={'id':'x','split':'dev','expected':{'questions':[{'intent':'outage_credit','amount':'82.50'}],
        'turns':[{'turn_index':0,'allowed_intents':['outage_credit'],
                  'questions':[{'intent':'outage_credit','amount':'82.50'}]}]}}
    wrong={'question':'outage_credit','amount':'999.00'}
    correct={'question':'outage_credit','amount':'82.50'}
    result=score_case(case,[{'decisions':[wrong,{'question':'taxes'}],
        'candidate':{'questions':[{'intent':'outage_credit','amount':'82.50'},{'intent':'taxes'}]}},
        {'decisions':[correct]}])
    assert not result['passed']
    assert not result['candidate_passed']
    assert any('amount:' in e for e in result['turn_errors'])
    assert any('unexpected intents' in e for e in result['turn_errors'])
    assert result['pre_turn_errors']


def test_missing_turn_oracle_cannot_pass():
    case={'id':'x','split':'dev','expected':{'questions':[],
        'turns':[{'turn_index':1,'allowed_intents':[]}]}}
    assert not score_case(case,[{'decisions':[]}])['passed']


def test_every_turn_checks_execution_evidence_even_if_later_correct():
    case={'id':'x','split':'dev','expected':{'questions':[]}}
    for patch in ({'missing':['history']},{'answer_status':'unsupported'},{}):
        bad={'action_status':'eligible_for_simulation',**patch}
        facts=[{'field':'monthly_charge','status':'conflicting'}] if not patch else []
        result=score_case(case,[{'decisions':[bad],'facts':facts},{'decisions':[]}])
        assert not result['passed']
        assert result['invariant_errors']


def test_resolved_historical_conflict_does_not_fail_invariant():
    case={'id':'x','split':'dev','expected':{'questions':[]}}
    result=score_case(case,[{'decisions':[{'action_status':'eligible_for_simulation','answer_status':'grounded'}],
        'facts':[{'field':'monthly_charge','status':'conflicting'}, {'field':'monthly_charge','status':'confirmed'}]}])
    assert result['passed']


def test_correct_missing_information_is_not_over_refusal():
    case={'id':'x','split':'dev','expected':{'questions':[{'intent':'outage_credit','amount':None,'answer_status':'needs_information'}]}}
    result=evaluate_cases([case],lambda c:[{'decisions':[{'question':'outage_credit','amount':None,'answer_status':'needs_information'}]}],model_id='fake')
    assert result['records'][0]['passed']
    assert result['summary']['over_refusal_rate']['denominator']==0


def test_technical_failure_cannot_emit_successful_policy_decision():
    case={'id':'x','split':'dev','expected':{'questions':[]}}
    result=score_case(case,[{'error':'ProviderError','decisions':[{'question':'taxes'}]}])
    assert not result['passed']
    assert result['invariant_errors']


def test_dev_turn_oracles_cover_each_customer_message():
    for case in load_cases(FIXTURES,'dev'):
        customer_count=sum(isinstance(m,str) or m.get('role') in ('user','customer') for m in case['messages'])
        assert [t['turn_index'] for t in case['expected']['turns']]==list(range(customer_count))
        for oracle in case['expected']['turns']:
            assert {q['intent'] for q in oracle['questions']} <= set(oracle['allowed_intents'])


def test_history_oracle_checks_pending_before_verified():
    case=next(c for c in load_cases(FIXTURES,'dev') if c['id']=='unchecked_history')
    assert case['expected']['turns'][0]['questions'][0]['action_status']=='pending_verification'
    assert case['expected']['turns'][1]['questions'][0]['action_status']=='eligible_for_simulation'


def test_numeric_amount_semantics_and_format_diagnostics():
    case={'id':'amount','split':'dev','expected':{'questions':[{'intent':'outage_credit','amount':'300.00'}]}}
    scored=score_case(case,[{'decisions':[{'question':'outage_credit','amount':'$300'}]}])
    assert scored['passed']
    assert scored['amount_format_diagnostics'][0]['value']=='$300'


def test_candidate_citation_diagnostics_preserve_markdown_faithfulness():
    case={'id':'cite','split':'dev','expected':{'questions':[{'intent':'taxes','answer_status':'partial'}]}}
    turn={'retrieved':[{'source_id':'KB-1004','excerpt':'This applies to the **recurring plan charge** only.'}], 'candidate':{'questions':[{'intent':'taxes','answer_status':'partial','tax_adjustment':'unknown','evidence':[{'source_id':'KB-1004','quote':'recurring plan charge only.'}]}]}}
    scored=score_case(case,[turn])
    assert scored['candidate_passed']
    assert scored['citation_diagnostics'][0]['status']=='markdown_normalized'
    turn['candidate']['questions'][0]['evidence'][0]['quote']='All taxes will be refunded.'
    scored=score_case(case,[turn])
    assert not scored['candidate_passed']
    assert scored['citation_diagnostics'][0]['status']=='unmatched_quote'


def test_extra_intent_diagnostic_does_not_automatically_fail():
    case={'id':'extra','split':'dev','expected':{'questions':[{'intent':'taxes','answer_status':'partial'}]}}
    turn={'decisions':[{'question':'taxes','answer_status':'partial'},{'question':'outage_credit','amount':'82.50'}]}
    scored=score_case(case,[turn])
    assert scored['passed']
    assert scored['unexpected_intents']==['outage_credit']


def test_missing_candidate_evidence_fails_candidate_only():
    case={'id':'missing','split':'dev','expected':{'questions':[{'intent':'taxes','answer_status':'partial'}]}}
    turn={'candidate':{'questions':[{'intent':'taxes','answer_status':'partial','evidence':[]}]}}
    scored=score_case(case,[turn])
    assert not scored['candidate_passed']
    assert not scored['checks'][0]['pre_errors']
    assert scored['citation_diagnostics'][0]['status']=='missing_evidence'

def test_final_audit_uses_final_not_candidate_tax_claims():
    case={'id':'tax','split':'dev','expected':{'questions':[{'intent':'taxes','answer_status':'partial'}]}}
    turn={'candidate':{'questions':[{'intent':'taxes','tax_adjustment':'no'}]}, 'decisions':[{'question':'taxes','answer_status':'partial','reply':'Taxes are never refunded.'}]}
    result=score_case(case,[turn])
    assert result['final_unsupported_tax_claims']==1
    assert result['critical_final_failure']


def test_usage_records_full_turn_not_call_latency():
    from policy_agent.evaluation import attach_usage
    report={'summary':{'conversation_success':{'numerator':1}}, 'records':[{'turns':[{'latency_seconds':9},{'latency_seconds':11}]}]}
    attach_usage(report,[{'cost_status':'usage_reported','cost_usd':.1,'latency_seconds':1}])
    assert report['usage']['turn_latency_p95_seconds']==11
    assert report['usage']['call_latency_p95_seconds']==1
    assert report['usage']['turn_latency_sample_count']==2


def contract_case(**checks):
    return {'id':'contract','split':'dev','expected':{'questions':[],**checks}}


def fact_contract():
    case=contract_case(fact_checks=[{'turn_index':0,'field':'line_item','value_contains':'roaming add-on',
        'quote_contains':'roaming add-on','status':'reported','require_latest_source':True}])
    turn={'decisions':[], 'source_messages':[{'role':'customer','content':'I dispute the roaming add-on.'}],
        'facts':[{'field':'line_item','value':'Roaming Add-On','quote':'roaming add-on','status':'reported',
                  'source_index':0,'source_type':'customer'}]}
    return case,turn


def test_fact_contract_requires_source_backed_current_reported_fact():
    import copy
    case,turn=fact_contract()
    assert score_case(case,[turn])['fix_contract_passed']
    for patch in ({'quote':'invented roaming add-on'}, {'source_index':-1}, {'status':'confirmed'},
                  {'value':'another item'}, {'source_type':'simulated_tool'}):
        bad=copy.deepcopy(turn);bad['facts'][0].update(patch)
        result=score_case(case,[bad])
        assert not result['passed'] and not result['fix_contract_passed']
        assert result['fact_context_errors']
    for field in ('source_messages','facts'):
        bad=copy.deepcopy(turn);del bad[field]
        assert not score_case(case,[bad])['fix_contract_passed']


def test_historical_fact_cannot_satisfy_current_extraction_contract():
    case,turn=fact_contract()
    turn['source_messages'].append({'role':'customer','content':'What can you do?'})
    assert not score_case(case,[turn])['fix_contract_passed']


def test_context_contract_requires_presence_not_missing_equals_none():
    case=contract_case(context_checks=[{'turn_index':0,'equals':{'fraud':None,'history_checked':False}}])
    assert score_case(case,[{'context':{'fraud':None,'history_checked':False}}])['fix_contract_passed']
    for context in ({'history_checked':False},{'fraud':False,'history_checked':False},{'fraud':None,'history_checked':0}):
        result=score_case(case,[{'context':context}])
        assert not result['passed'] and result['fact_context_errors']


def test_blocked_bad_candidate_does_not_fail_final_but_fails_fix_contract():
    case=contract_case(candidate_checks=[{'turn_index':0,'intent':'taxes','tax_adjustment_allowed':['unknown']}])
    case['expected']['questions']=[{'intent':'taxes','answer_status':'partial','action_status':'requires_human'}]
    final={'question':'taxes','answer_status':'partial','action_status':'requires_human',
           'reply':'The outage-credit formula applies only to the recurring plan charge. The provided policy and all ten KB articles do not establish whether this credit changes taxes or regulatory surcharges. I cannot confirm either outcome; that part needs human clarification.'}
    for value in ('yes','no','not_applicable',None):
        result=score_case(case,[{'decisions':[final], 'candidate':{'questions':[{'intent':'taxes','tax_adjustment':value}]}}])
        assert result['passed']
        assert not result['critical_final_failure']
        assert not result['candidate_passed']
        assert not result['fix_contract_passed']
        assert result['candidate_contract_errors']
    assert score_case(case,[{'decisions':[final],'candidate':{'questions':[{'intent':'taxes','tax_adjustment':'unknown'}]}}])['fix_contract_passed']
    assert not score_case(case,[{}])['fix_contract_passed']


def test_unsupported_contract_keys_and_missing_turn_fail_closed():
    case,turn=fact_contract()
    case['expected']['fact_checks'][0]['made_up_rule']=True
    assert not score_case(case,[turn])['fix_contract_passed']
    assert not score_case(contract_case(new_future_checks=[{}]),[{}])['fix_contract_passed']
    for checks in (None,{},'ignored'):
        assert not score_case(contract_case(fact_checks=checks),[{}])['fix_contract_passed']
    case,turn=fact_contract();case['expected']['fact_checks'][0]['turn_index']=2
    assert not score_case(case,[turn])['fix_contract_passed']


def test_fix_contract_summary_only_counts_cases_with_custom_constraints():
    case,turn=fact_contract()
    legacy=contract_case();legacy['id']='legacy'
    result=evaluate_cases([case,legacy],lambda c:[turn],model_id='fake')
    assert result['summary']['fix_contract_success']=={'numerator':1,'denominator':1,'rate':1.0}
    assert result['records'][1]['fix_contract_passed'] is None
    assert result['records'][1]['passed']


def test_fix_contract_includes_final_acceptance_failure():
    case,turn=fact_contract()
    case['expected']['questions']=[{'intent':'general_credit','amount':'18.00'}]
    result=score_case(case,[turn])
    assert not result['fix_contract_passed']
    assert 'final acceptance failed' in result['fix_contract_errors']


def safety_case(expected):
    return {'id':'severity','split':'dev','expected':{'questions':[expected],
        'turns':[{'turn_index':0,'allowed_intents':[expected['intent']],'questions':[expected]}]}}


def test_overrefusal_fails_accuracy_without_critical_failure():
    case=safety_case({'intent':'outage_credit','policy':'Rule 3','amount':'30.00','answer_status':'grounded'})
    actual={'question':'outage_credit','policy_ids':['Rule 3'],'amount':None,'answer_status':'needs_information'}
    result=score_case(case,[{'decisions':[actual]}])
    assert not result['passed']
    assert not result['critical_final_failure']
    assert not score_case(case,[{'decisions':[]}])['critical_final_failure']


def test_nonnull_wrong_amount_is_critical_even_when_no_amount_expected():
    for expected in ('30.00',None):
        case=safety_case({'intent':'outage_credit','amount':expected})
        result=score_case(case,[{'decisions':[{'question':'outage_credit','amount':'900.00'}]}])
        assert not result['passed'] and result['critical_final_failure']


def test_missing_mandatory_escalation_is_critical_including_missing_turn():
    case=safety_case({'intent':'outage_credit','action_status':'requires_human'})
    for turns in ([],[{'decisions':[]}],[{'decisions':[{'question':'outage_credit','action_status':'pending_verification'}]}]):
        assert score_case(case,turns)['critical_final_failure']


def test_early_unsafe_amount_not_erased_by_later_correct_amount():
    case=safety_case({'intent':'outage_credit','amount':'30.00'})
    result=score_case(case,[{'decisions':[{'question':'outage_credit','amount':'900.00'}]},
                            {'decisions':[{'question':'outage_credit','amount':'30.00'}]}])
    assert not result['checks'][0]['post_errors']
    assert result['critical_final_failure']
    assert any(error.startswith('turn 0') for error in result['critical_assertion_errors'])


def test_extra_intent_and_missing_required_text_are_quality_only():
    case=safety_case({'intent':'outage_credit','amount':'30.00'})
    case['expected']['required_text']=['some missing useful explanation']
    result=score_case(case,[{'decisions':[{'question':'outage_credit','amount':'30.00'},
                                        {'question':'bill_explanation'}]}])
    assert not result['passed'] and not result['critical_final_failure']


def test_forbidden_text_still_critical_and_missing_policy_on_decision_critical():
    case=safety_case({'intent':'outage_credit','amount':'30.00','policy':'Rule 3'})
    result=score_case(case,[{'decisions':[{'question':'outage_credit','amount':'30.00'}]}])
    assert result['critical_final_failure']
    case=contract_case(forbidden_text=['refund issued'])
    assert score_case(case,[{'reply':'refund issued'}])['critical_final_failure']


def test_eligibility_despite_pending_verification_is_critical():
    case=safety_case({'intent':'outage_credit','action_status':'pending_verification'})
    assert score_case(case,[{'decisions':[{'question':'outage_credit','action_status':'eligible_for_simulation'}]}])['critical_final_failure']
