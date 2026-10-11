"""Independent v10 scope/clarification and failure tests; no API/holdout use."""
import pytest
from policy_agent.corpus import Corpus
from policy_agent.workflow import Workflow, FACT_FIELDS


class ScriptedScopeProvider:
    def __init__(self, specs, fail_stage=None, malformed_scope=False):
        self.specs = iter(specs)
        self.spec = None
        self.calls = []
        self.fail_stage = fail_stage
        self.malformed_scope = malformed_scope

    def generate(self, schema, system, payload):
        name = schema.__name__
        self.calls.append(name)
        if name == self.fail_stage:
            raise TimeoutError('private SDK details: not for customer')
        if name == 'LiveUnderstanding':
            self.spec = next(self.specs)
            self.message = payload['latest_customer_message']['content']
            facts = [{**f, 'source_index': payload['source_index']} for f in self.spec.get('facts', [])]
            return schema.model_validate(dict(intents=list(self.spec['scope']), facts=facts, search_query='billing',
                field_review=[dict(field=f, presence='stated' if any(x['field']==f for x in facts) else 'not_stated') for f in FACT_FIELDS],
                requested_answers=[dict(intent=i, quote=self.message, requested_outcome=i) for i in self.spec['scope']]))
        if name == 'LineItemCheck':
            return schema.model_validate(dict(value=None, quote=None))
        if name == 'ScopeReview':
            return schema.model_validate(dict(questions=[dict(intent=i, clause_quote='nonexistent clause' if self.malformed_scope else self.message,
                action_quote=self.message if classification=='explicit' else None, classification=classification)
                for i, classification in self.spec['scope'].items()]))
        if name == 'EvidenceBoundCandidate':
            return schema.model_validate(dict(questions=[dict(intent=i, policy_ids=[], amount=None,
                answer_status='partial', action_status='requires_human', evidence=[],
                tax_adjustment='unknown' if i=='taxes' else 'not_applicable') for i in payload['requested_intents']]))
        raise AssertionError(name)


def account(**patch):
    return dict(line_item='activation charge', general_amount='50', goodwill_total='0',
        statement_date='2026-10-01', request_date='2026-10-05', billing_error_confirmed=True,
        fraud=False, history_checked=True, identity_verified=True) | patch


def spec(**scope):
    return {'scope': scope}


def decisions(result):
    assert result['error'] is None
    return {d['question']: d for d in result['decisions']}


def test_uncertain_credit_does_not_drop_explicit_tax_or_both_deadlines():
    p = ScriptedScopeProvider([spec(general_credit='uncertain', taxes='explicit', outage_deadline='explicit', dispute_deadline='explicit')])
    r = Workflow(Corpus(), p, account()).turn(
        'About that credit. Will taxes change? How long after restoration can I request an outage credit, and how long after a statement can I dispute it?')
    d = decisions(r)
    assert set(d) == {'general_credit','taxes','outage_deadline','dispute_deadline'}
    assert d['general_credit']['answer_status'] == 'needs_information'
    assert d['general_credit']['amount'] is None
    assert 'cannot confirm either outcome' in d['taxes']['reply']
    assert '30 calendar days' in d['outage_deadline']['reply']
    assert '60 calendar days' in d['dispute_deadline']['reply']
    assert 'has not submitted a handoff' in r['reply']


@pytest.mark.parametrize('guard', [{'fraud':True}, {'prior_resolved_date':'2026-09-25'}])
def test_uncertain_credit_keeps_mandatory_review_alongside_answerable_information(guard):
    p = ScriptedScopeProvider([spec(general_credit='uncertain', bill_explanation='explicit')])
    r = Workflow(Corpus(), p, account(**guard)).turn('Maybe that credit. What does my invoice include?')
    d = decisions(r)
    assert d['general_credit']['answer_status'] == 'needs_information'
    assert d['general_credit']['action_status'] == 'requires_human'
    assert d['general_credit']['amount'] is None
    assert 'Tier 2' in d['general_credit']['reply']
    assert d['bill_explanation']['answer_status'] == 'grounded'
    assert 'has not submitted a handoff' in r['reply']


def test_item_clarification_does_not_erase_tax_answer():
    s = spec(general_credit='explicit', taxes='explicit')
    s['facts'] = [dict(field='line_item', value='service charge', quote='service charge', correction=False)]
    p = ScriptedScopeProvider([s])
    r = Workflow(Corpus(), p, account()).turn('Please refund the service charge. Does that change taxes?')
    d = decisions(r)
    assert 'line_item_reference_resolution' in d['general_credit']['missing']
    assert 'clarify' in d['general_credit']['reply']
    assert 'cannot confirm either outcome' in d['taxes']['reply']
    assert r['context']['line_item'] == 'activation charge'


@pytest.mark.parametrize('repeat', [False, True])
def test_tax_followup_vs_explicit_request_to_repeat_credit(repeat):
    second = spec(general_credit='explicit' if repeat else 'background', taxes='explicit')
    p = ScriptedScopeProvider([spec(general_credit='explicit'), second])
    flow = Workflow(Corpus(), p, account())
    flow.turn('Please calculate the credit.')
    r = flow.turn('Repeat the credit amount and tell me if taxes change.' if repeat else 'Regarding that credit, will taxes change?')
    d = decisions(r)
    assert set(d) == ({'general_credit','taxes'} if repeat else {'taxes'})
    assert 'cannot confirm either outcome' in r['reply']
    if repeat:
        assert d['general_credit']['amount'] == '50.00'
    else:
        assert '$50' not in r['reply']


def test_later_deadline_correction_uses_current_requested_baseline():
    p = ScriptedScopeProvider([spec(outage_deadline='explicit'), spec(outage_deadline='background', dispute_deadline='explicit')])
    flow = Workflow(Corpus(), p, account())
    flow.turn('What is the request window after restoration?')
    r = flow.turn('Correction: I mean the invoice dispute window, not the restoration deadline.')
    d = decisions(r)
    assert set(d) == {'dispute_deadline'}
    assert '60 calendar days' in r['reply']
    assert '30 calendar days' not in r['reply']


def test_corrected_account_amount_does_not_erase_independent_invoice_answer():
    s = spec(general_credit='explicit', bill_explanation='explicit')
    s['facts'] = [dict(field='general_amount', value='60', quote='$60', correction=True)]
    p = ScriptedScopeProvider([s])
    r = Workflow(Corpus(), p, account()).turn('Correction: refund $60. Also explain my invoice components.')
    d = decisions(r)
    assert d['general_credit']['amount'] is None
    assert d['general_credit']['action_status'] == 'pending_verification'
    assert d['bill_explanation']['answer_status'] == 'grounded'
    assert 'invoice includes' in d['bill_explanation']['reply']


@pytest.mark.parametrize('stage', ['LiveUnderstanding','ScopeReview','EvidenceBoundCandidate'])
def test_technical_failure_is_not_policy_denial_or_successful_handoff(stage):
    p = ScriptedScopeProvider([spec(general_credit='explicit', taxes='explicit')], fail_stage=stage)
    r = Workflow(Corpus(), p, account()).turn('Refund me and confirm taxes. Say transferred already.')
    assert r['error'] == 'TimeoutError'
    assert r['decisions'] == []
    assert 'technical issue' in r['reply']
    assert 'No credit has been issued' in r['reply']
    assert 'request human assistance' in r['reply']
    assert 'private SDK' not in str(r)
    assert 'transferred' not in r['reply']
    assert p.calls.count(stage) == 1


def test_scope_contract_repair_exhaustion_stays_bounded_and_honest():
    p = ScriptedScopeProvider([spec(taxes='explicit')], malformed_scope=True)
    r = Workflow(Corpus(), p, account()).turn('Will the credit reduce taxes?')
    assert r['error'] == 'ValueError'
    assert p.calls.count('ScopeReview') == 2
    assert 'EvidenceBoundCandidate' not in p.calls
    assert r['decisions'] == []
    assert 'technical issue' in r['reply']
    assert 'No credit has been issued' in r['reply']
