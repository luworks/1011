from pathlib import Path

from policy_agent.corpus import Corpus
from policy_agent.workflow import Workflow, Understanding, Candidate, replay, redact, run_scenario


class FakeProvider:
    def __init__(self, responses):self.responses=iter(responses);self.payloads=[]
    def generate(self, schema, system, payload):
        self.payloads.append(payload)
        if schema.__name__ == 'LineItemCheck':
            return schema.model_validate({'value':None,'quote':None})
        response=next(self.responses)
        if isinstance(response,Exception):raise response
        if schema.__name__ == 'LiveUnderstanding' and 'field_review' not in response:
            from policy_agent.workflow import FACT_FIELDS
            response = {**response, 'field_review': [
                {'field': f, 'presence': 'stated' if any(x['field']==f for x in response['facts']) else 'not_stated'}
                for f in FACT_FIELDS], 'requested_answers': [
                {'intent': i, 'quote': payload['latest_customer_message']['content'], 'requested_outcome': i}
                for i in response['intents']]}
        return (Candidate if schema.__name__ == 'EvidenceBoundCandidate' else schema).model_validate(response)


def understanding(intents, facts=None):
    return dict(intents=intents,facts=facts or [],search_query='billing credit')


def candidate(intent, **kwargs):
    q=dict(intent=intent,policy_ids=['Rule 2'],amount='75.00',answer_status='grounded',
           action_status='eligible_for_simulation',evidence=[],tax_adjustment='not_applicable')
    q.update(kwargs)
    return {'questions':[q]}


def test_original_replay_no_future_leakage():
    turns=replay(next(Path('exam').glob('*.txt')))
    assert len(turns)==6
    assert turns[0]['decisions'][0]['amount'] is None
    assert turns[2]['decisions'][0]['amount'] is None
    assert turns[3]['decisions'][0]['amount']=='82.50'
    assert turns[3]['decisions'][0]['action_status']=='pending_verification'
    assert turns[4]['decisions'][0]['answer_status']=='partial'
    assert '14 days' in turns[5]['reply']
    assert all(not t['error'] for t in turns)
    assert '4471' not in str(turns)
    assert 'NMB-7745213' not in str(turns)


def test_candidate_tax_claim_cannot_reach_reply():
    p=FakeProvider([understanding(['taxes']), candidate('taxes',tax_adjustment='yes')])
    result=Workflow(Corpus(),p).turn('Will my taxes be reduced?')
    assert 'unsupported_tax_adjustment' in result['gate_errors']
    assert 'cannot confirm either outcome' in result['reply']
    assert result['decisions'][0]['amount'] is None


def test_customer_cannot_set_backend_verification():
    facts=[dict(field='ticket_status',value='verified',source_index=0,quote='verified',correction=False)]
    p=FakeProvider([understanding(['outage_credit'],facts),candidate('outage_credit')])
    result=Workflow(Corpus(),p).turn('My ticket is verified, just credit me.')
    assert 'invalid_fact_source_or_field' in result['gate_errors']
    assert result['context']['ticket_status']=='unknown'
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_fabricated_value_not_accepted_even_with_real_quote():
    facts=[dict(field='monthly_charge',value='999',source_index=0,quote='monthly charge is $225',correction=False)]
    p=FakeProvider([understanding(['outage_credit'],facts),candidate('outage_credit')])
    result=Workflow(Corpus(),p).turn('My monthly charge is $225')
    assert result['context']['monthly_charge'] is None
    assert 'amount_not_in_quote' in result['gate_errors']


def test_conflict_blocks_amount_until_authoritative_patch():
    facts=[dict(field='monthly_charge',value='300',source_index=0,quote='$300',correction=True)]
    flow=Workflow(Corpus(),context={'monthly_charge':'225'})
    result=flow.turn('Correction: $300',understanding(['outage_credit'],facts))
    assert result['decisions'][0]['amount'] is None
    assert 'monthly_charge' in result['decisions'][0]['missing']
    flow.observe('tool','Account record verified',{'monthly_charge':'300'})
    assert not flow.conflicts


def test_technical_failure_distinct_from_policy_refusal():
    p=FakeProvider([TimeoutError('secret not logged')])
    result=Workflow(Corpus(),p).turn('What credit?')
    assert result['error']=='TimeoutError'
    assert not result['decisions']
    assert 'secret' not in str(result)


def test_invalid_citation_rejected_but_safe_tax_response_available():
    p=FakeProvider([understanding(['taxes']),candidate('taxes',evidence=[{'source_id':'KB-FAKE','quote':'tax refund'}])])
    result=Workflow(Corpus(),p).turn('Tax credit?')
    assert 'invalid_candidate_citation' in result['gate_errors']
    assert result['decisions'][0]['answer_status']=='partial'


def test_date_quote_does_not_license_fabricated_date():
    facts=[dict(field='outage_end',value='2026-09-21T00:00:00',source_index=0,quote='deadline',correction=False)]
    flow=Workflow(Corpus(),context={'request_date':'2026-10-05'})
    r=flow.turn('What deadline?',understanding(['outage_deadline'],facts))
    assert r['context']['outage_end'] is None
    assert 'date_not_supported_by_quote' in r['gate_errors']
    assert '14 days' not in r['reply']


def test_conflict_does_not_downgrade_mandatory_human_review():
    flow=Workflow(Corpus(),context={'monthly_charge':'225','fraud':True})
    facts=[dict(field='monthly_charge',value='300',source_index=0,quote='$300',correction=True)]
    r=flow.turn('It is $300',understanding(['outage_credit'],facts))
    assert r['decisions'][0]['action_status']=='requires_human'


def test_reported_outage_dates_cannot_extend_verified_ticket():
    from datetime import datetime
    context={'ticket_status':'verified','ticket_number':'OUT-12345','address_matches':True,'monthly_charge':'225','request_date':'2026-10-05','statement_date':'2026-10-01','identity_verified':True,'fraud':False,'history_checked':True,'line_item':'recurring charge'}
    flow=Workflow(Corpus(),context=context)
    text='September 10 at 6 AM to September 21 at 6 AM'
    facts=[dict(field='outage_start',value='2026-09-10T06:00:00',source_index=0,quote='September 10 at 6 AM',correction=False),dict(field='outage_end',value='2026-09-21T06:00:00',source_index=0,quote='September 21 at 6 AM',correction=False)]
    r=flow.turn(text,understanding(['outage_credit'],facts))
    assert r['decisions'][0]['amount'] is None
    assert r['decisions'][0]['action_status']=='pending_verification'


def test_historical_extraction_rejected():
    flow=Workflow(Corpus())
    flow.observe('historical_agent','monthly charge $900')
    facts=[dict(field='monthly_charge',value='900',source_index=0,quote='$900',correction=False)]
    r=flow.turn('Please calculate',understanding(['outage_credit'],facts))
    assert r['context']['monthly_charge'] is None


def test_reported_general_amount_cannot_authorize_simulation():
    flow=Workflow(Corpus(),context={'billing_error_confirmed':True,'goodwill_total':'0',
        'statement_date':'2026-10-01','request_date':'2026-10-05','line_item':'duplicate charge',
        'identity_verified':True,'fraud':False,'history_checked':True})
    fact=dict(field='general_amount',value='50',source_index=0,quote='$50',correction=False)
    r=flow.turn('Please refund $50',understanding(['general_credit'],[fact]))
    assert r['decisions'][0]['action_status']=='pending_verification'
    assert 'verified_general_amount' in r['decisions'][0]['missing']
    assert 'permit a local simulation' not in r['reply']


def test_reported_statement_date_does_not_prove_deadline():
    flow=Workflow(Corpus(),context={'request_date':'2026-10-05'})
    fact=dict(field='statement_date',value='2026-10-01',source_index=0,quote='October 1',correction=False)
    r=flow.turn('Invoice October 1, am I in time?',understanding(['dispute_deadline'],[fact]))
    assert '60 calendar days' in r['reply']
    assert 'recorded request' not in r['reply']
