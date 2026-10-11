"""Independent authority-boundary regressions; no APIs or holdout fixtures."""
from decimal import Decimal

import pytest
from policy_agent.corpus import Corpus
from policy_agent.workflow import Workflow


def account(**overrides):
    return dict(general_amount='20', goodwill_total='0', statement_date='2026-10-01',
                request_date='2026-10-05', billing_error_confirmed=True,
                identity_verified=True, fraud=False, history_checked=True,
                line_item='duplicate charge', **overrides)


def turn(flow, text='Please refund the duplicate charge', facts=None):
    return flow.turn(text, {'intents':['general_credit'], 'facts':facts or [], 'search_query':'general refund'})


def fact(field, value, quote, source_index=0):
    return dict(field=field, value=value, quote=quote, source_index=source_index, correction=True)


def test_false_fraud_and_zero_prior_credit_are_known_not_missing():
    flow=Workflow(Corpus(),context=account())
    result=turn(flow)
    assert result['decisions'][0]['action_status']=='eligible_for_simulation'
    assert {'fraud','goodwill_total'} <= flow.verified_fields
    assert flow.context.fraud is False and flow.context.goodwill_total==Decimal('0')


@pytest.mark.parametrize('key,value', [('identity_verified',False),('billing_error_confirmed',False),('history_checked',False)])
def test_false_required_checks_do_not_grant_authority(key,value):
    context=account();context[key]=value
    result=turn(Workflow(Corpus(),context=context))
    assert result['decisions'][0]['action_status']!='eligible_for_simulation'


def test_reported_amount_cannot_replace_zero_trusted_amount():
    context=account();context['general_amount']='0'
    flow=Workflow(Corpus(),context=context)
    result=turn(flow,'Refund 20 for the duplicate charge',[fact('general_amount','20','Refund 20')])
    assert flow.context.general_amount==0
    assert 'general_amount' in flow.conflicts
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_null_tool_amount_then_reported_amount_never_inherits_verification():
    flow=Workflow(Corpus(),context=account())
    flow.observe('tool','Amount lookup unavailable',{'general_amount':None})
    result=turn(flow,'Refund 20 for the duplicate charge',[fact('general_amount','20','Refund 20',1)])
    assert 'general_amount' not in flow.verified_fields
    assert result['decisions'][0]['action_status']=='pending_verification'
    assert 'verified_general_amount' in result['decisions'][0]['missing']


def test_reported_quote_from_older_role_is_rejected():
    context=account();context['general_amount']=None
    flow=Workflow(Corpus(),context=context)
    flow.observe('historical_agent','20 dollars')
    result=turn(flow,'Refund please',[fact('general_amount','20','20 dollars',0)])
    assert flow.context.general_amount is None
    assert 'invalid_fact_source_or_field' in result['gate_errors']


def test_fraud_escalation_survives_conflicting_reported_amount():
    context=account();context['fraud']=True
    flow=Workflow(Corpus(),context=context)
    result=turn(flow,'Refund 30 please',[fact('general_amount','30','Refund 30')])
    assert result['decisions'][0]['action_status']=='requires_human'


def test_unverified_dates_cannot_enable_outage_credit():
    context=account();context.update(monthly_charge='225',ticket_status='verified',
        ticket_number='OUT-12345',address_matches=True,outage_start=None,outage_end=None)
    flow=Workflow(Corpus(),context=context)
    text='Service stopped September 10 at 6 AM and returned September 21 at 6 AM.'
    result=flow.turn(text,{'intents':['outage_credit'],'search_query':'outage',
        'facts':[fact('outage_start','2026-09-10T06:00:00',text),fact('outage_end','2026-09-21T06:00:00',text)]})
    assert not {'outage_start','outage_end'} & flow.verified_fields
    assert result['decisions'][0]['action_status']=='pending_verification'
    assert result['decisions'][0]['amount'] is None


def test_whitespace_line_item_cannot_satisfy_specific_charge_requirement():
    context=account();context['line_item']=None
    flow=Workflow(Corpus(),context=context)
    result=turn(flow,'Please refund my bill',[fact('line_item',' ','Please refund my bill')])
    assert result['decisions'][0]['action_status']!='eligible_for_simulation'


@pytest.mark.parametrize('via_tool',[False,True])
def test_whitespace_trusted_line_item_is_missing(via_tool):
    context=account()
    if not via_tool:context['line_item']=' \t '
    flow=Workflow(Corpus(),context=context)
    if via_tool:flow.observe('tool','Line item unavailable',{'line_item':' \t '})
    result=turn(flow)
    assert flow.context.line_item is None
    assert 'line_item' not in flow.verified_fields
    assert result['decisions'][0]['action_status']!='eligible_for_simulation'
    assert [f for f in flow.facts if f['field']=='line_item'][-1]['status']=='unknown'
