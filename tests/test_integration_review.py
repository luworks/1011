"""Review regressions: retrieved evidence must cover the final decision."""
from policy_agent.corpus import Corpus
from policy_agent.schema import AccountContext
from policy_agent.policy import evaluate
from policy_agent.workflow import Workflow


def test_outage_retrieval_covers_policy_evidence():
    corpus=Corpus()
    retrieved={ref.source_id for ref in corpus.retrieve('', ['outage_credit'])}
    decision=evaluate('outage_credit',AccountContext(),corpus)
    assert {ref.source_id for ref in decision.evidence} <= retrieved


def test_late_outage_deadline_retrieves_fallback_rule():
    corpus=Corpus()
    retrieved={ref.source_id for ref in corpus.retrieve('', ['outage_deadline'])}
    decision=evaluate('outage_deadline',AccountContext(outage_end='2026-09-01T00:00:00',request_date='2026-10-05'),corpus)
    assert {ref.source_id for ref in decision.evidence} <= retrieved


def test_customer_outage_date_does_not_complete_verified_ticket():
    flow=Workflow(Corpus(),context={'ticket_status':'verified','ticket_number':'OUT-12345','address_matches':True,'monthly_charge':'225','request_date':'2026-10-05','history_checked':True,'fraud':False,'identity_verified':True,'statement_date':'2026-10-01','line_item':'Recurring plan charge'})
    quote='My outage started September 10 at 6 AM and ended September 21 at 6 AM.'
    result=flow.turn(quote,{'intents':['outage_credit'],'search_query':'outage','facts':[
        {'field':'outage_start','value':'2026-09-10T06:00:00','quote':quote,'source_index':0,'correction':False},
        {'field':'outage_end','value':'2026-09-21T06:00:00','quote':quote,'source_index':0,'correction':False}]})
    assert result['decisions'][0]['amount'] is None
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_conflicting_amount_preserves_mandatory_fraud_review():
    flow=Workflow(Corpus(),context={'monthly_charge':'225','fraud':True})
    result=flow.turn('My monthly charge is $300.',{'intents':['outage_credit'],'search_query':'outage','facts':[
        {'field':'monthly_charge','value':'300','quote':'monthly charge is $300','source_index':0,'correction':False}]})
    assert result['decisions'][0]['action_status']=='requires_human'
    assert result['decisions'][0]['amount'] is None
