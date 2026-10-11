from copy import deepcopy
from datetime import datetime, date
from decimal import Decimal

import pytest
from policy_agent.boundaries import apply_boundaries
from policy_agent.corpus import Corpus
from policy_agent.policy import evaluate
from policy_agent.schema import AccountContext


def context(**updates):
    values=dict(monthly_charge=Decimal('300'),outage_start=datetime(2026,9,1),outage_end=datetime(2026,9,12),
        request_date=date(2026,9,15), statement_date=date(2026,9,1), ticket_status='verified',
        ticket_number='OUT-12345',address_matches=True,history_checked=True,fraud=False,
        identity_verified=True,line_item='recurring plan charge')
    return AccountContext(**(values|updates))


def decision(c, intent='outage_credit', text=''):
    d=evaluate(intent,c,Corpus()).model_dump(mode='json')
    return apply_boundaries(intent,c,d,[{'role':'customer','content':text}])


def test_known_three_lines_still_calculates_exact_amount():
    d=decision(context(),text='All three lines together cost $300 monthly, and all were affected.')
    assert (d['amount'],d['answer_status'],d['action_status'])==('110.00','grounded','eligible_for_simulation')
    assert not any(x.startswith('policy_decision:') for x in d['missing'])


@pytest.mark.parametrize('end,charge',[(datetime(2026,9,1,5), '300'),(datetime(2026,9,12,1),'300'),(datetime(2026,9,12),'225.01')])
def test_unapproved_days_or_rounding_never_promoted(end,charge):
    d=decision(context(outage_end=end,monthly_charge=Decimal(charge)))
    assert d['amount'] is None
    assert d['answer_status']=='partial'
    assert d['action_status']=='pending_verification'
    assert 'policy_decision:OD-05' in d['missing']
    assert not any('ROUND_HALF_UP' in r for r in d['reasons'])
    assert 'policy calculation is' not in d['reply']


def test_fraud_remains_mandatory_with_partial_day():
    d=decision(context(outage_end=datetime(2026,9,12,1),fraud=True))
    assert d['amount'] is None and d['action_status']=='requires_human'
    assert any(r.startswith('Rule 5:') for r in d['reasons'])


def test_boundary_does_not_approve_thirtieth_day():
    d=decision(context(request_date=date(2026,10,12)))
    assert d['conditions']['within_outage_window'] is None
    assert d['amount']=='110.00' and d['action_status']=='pending_verification'


def test_ninetieth_day_not_automatic_escalation_but_fraud_is():
    for fraud, action in [(False,'pending_verification'),(True,'requires_human')]:
        d=decision(context(prior_resolved_date=date(2026,6,17),fraud=fraud))
        assert d['action_status']==action
        assert d['conditions']['repeat_dispute'] is None


@pytest.mark.parametrize('text,gap',[('Only one of my lines was affected.','OD-06'),('My rate changed during the outage.','OD-07')])
def test_unsupported_base_triggers_only_corresponding_gap(text,gap):
    d=decision(context(),text=text)
    assert d['amount'] is None and 'policy_decision:'+gap in d['missing']


def test_historical_agent_does_not_create_base_gap():
    c=context(); d=evaluate('outage_credit',c,Corpus()).model_dump(mode='json')
    final=apply_boundaries('outage_credit',c,deepcopy(d),[{'role':'historical_agent','content':'Your rate changed.'}])
    assert final==d


def test_noncovering_ticket_not_automatic_general_entitlement():
    d=decision(context(address_matches=False))
    assert d['amount'] is None and 'Rule 2' not in d['policy_ids']
    assert 'policy_decision:OD-04' in d['missing']


def test_standalone_missing_invoice_does_not_invent_combined_rule():
    d=decision(context(line_item=None,statement_date=None))
    assert d['amount'] is None and d['answer_status']=='partial'
    assert 'policy_decision:OD-02' in d['missing']


def test_explicit_unverifiable_ticket_still_escalates():
    d=decision(context(ticket_status='unverifiable',address_matches=False))
    assert d['action_status']=='requires_human'
    assert any('cannot currently be verified' in r for r in d['reasons'])


def test_latest_workflow_preserves_candidate_and_boundary():
    from policy_agent.workflow import Workflow, Candidate
    class Scripted:
        def generate(self,schema,prompt,payload):
            if schema.__name__=='LiveUnderstanding':
                from policy_agent.workflow import FACT_FIELDS
                return schema(intents=['outage_credit'],facts=[],search_query='outage credit',
                    field_review=[dict(field=f,presence='not_stated') for f in FACT_FIELDS],
                    requested_answers=[dict(intent='outage_credit',quote='What is my outage credit?',requested_outcome='credit amount')])
            if schema.__name__=='ScopeReview':
                return schema(questions=[dict(intent=i,classification='explicit',
                    clause_quote=payload['current_message'],action_quote=payload['current_message'])
                    for i in payload['proposed_intents']])
            assert schema.__name__=='EvidenceBoundCandidate'
            return Candidate(questions=[dict(intent='outage_credit',policy_ids=['Rule 3'],amount=None,
                answer_status='partial',action_status='pending_verification',evidence=[],tax_adjustment='not_applicable')])
    flow=Workflow(Corpus(),Scripted(),context(outage_end=datetime(2026,9,1,5)).model_dump())
    result=flow.turn('What is my outage credit?',dict(intents=['outage_credit'],facts=[],search_query='outage credit'))
    assert result['error'] is None
    assert result['candidate']['questions'][0]['amount'] is None
    assert result['decisions'][0]['amount'] is None
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_unknown_ticket_does_not_become_absent_or_approved():
    d=decision(context(ticket_status='unknown'))
    assert d['amount'] is None
    assert d['action_status']=='pending_verification'
    assert 'Rule 2' not in d['policy_ids']


def test_known_repeat_inside_window_and_exact_large_amount_still_escalate():
    for c in (context(prior_resolved_date=date(2026,9,14)), context(monthly_charge=Decimal('900'))):
        d=decision(c)
        assert d['action_status']=='requires_human' and d['amount'] is not None


def test_ordinary_general_credit_not_blocked_by_outage_gap():
    c=context(general_amount=Decimal('15'),goodwill_total=Decimal('10'),billing_error_confirmed=True,
              outage_end=datetime(2026,9,1,5))
    d=decision(c,'general_credit', 'Refund my confirmed duplicate charge.')
    assert (d['amount'],d['action_status'])==('15.00','eligible_for_simulation')
    assert not any(x.startswith('policy_decision:') for x in d['missing'])


def test_known_sub_four_hour_failure_keeps_evaluation_not_entitlement():
    d=decision(context(outage_end=datetime(2026,9,1,4)))
    assert d['amount'] is None and d['action_status']=='pending_verification'
    assert 'Rule 2' in d['policy_ids']
    assert 'policy_decision:OD-05' not in d['missing']


def test_deadline_only_not_reclassified_as_credit_calculation():
    d=decision(context(outage_end=datetime(2026,9,1,5)), 'outage_deadline')
    assert d['question']=='outage_deadline' and d['answer_status']=='grounded'
    assert '30 calendar days' in d['reply']


@pytest.mark.parametrize('updates,text',[
    ({'line_item':None},''),
    ({'address_matches':False},''),
    ({'outage_end':datetime(2026,9,1,5)},''),
    ({},'Only one of my lines was affected.'),
    ({},'My rate changed during the outage.'),
    ({'request_date':date(2026,10,12)},''),
])
def test_customer_reply_uses_specific_topics_not_internal_codes(updates,text):
    from policy_agent.service import compose_reply
    d=decision(context(**updates),text=text)
    assert any(m.startswith('policy_decision:OD-') for m in d['missing'])
    assert 'OD-' not in d['reply']
    assert 'OD-' not in compose_reply([d])
    assert 'The supplied policy needs clarification on' in d['reply']
