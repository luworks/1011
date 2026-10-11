"""One billable content repair spans parsing and cross-field stages per turn."""
import json
from types import SimpleNamespace as NS

import pytest

from policy_agent.corpus import Corpus
from policy_agent.providers import Provider, Budget
from policy_agent.workflow import FACT_FIELDS, Workflow


MESSAGE = 'Will my taxes change?'


def understanding():
    return dict(intents=['taxes'], facts=[], search_query='taxes',
                field_review=[dict(field=f, presence='not_stated') for f in FACT_FIELDS],
                requested_answers=[dict(intent='taxes', quote=MESSAGE, requested_outcome='tax adjustment')])


def scope():
    return {'questions': [dict(intent='taxes', clause_quote=MESSAGE, action_quote=MESSAGE,
                               classification='explicit')]}


def candidate():
    return {'questions': [dict(intent='taxes', policy_ids=[], amount=None,
                               answer_status='partial', action_status='requires_human',
                               evidence=[], tax_adjustment='unknown')]}


class Client:
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.responses = self
        self.requests = []

    def create(self, **kwargs):
        self.requests.append(kwargs)
        output = next(self.outputs)
        return NS(status='completed', output_text=output if isinstance(output, str) else json.dumps(output),
                  model='fixed-model', usage=NS(input_tokens=10, output_tokens=20))


def provider(outputs):
    client = Client(outputs)
    p = Provider(dict(provider='openai', model='fixed-model', reasoning_effort='medium',
                      input_per_million=1, output_per_million=1, cached_input_per_million=.1,
                      max_output_tokens=300), Budget(), client)
    return p, client


def test_contract_repair_preserves_diagnostics_and_counts_every_request():
    bad = understanding(); bad['field_review'] = []
    p, client = provider([bad, understanding(), scope(), candidate()])
    flow = Workflow(Corpus(), p)
    result = flow.turn(MESSAGE)
    assert result['error'] is None
    assert len(result['understanding_diagnostics']) == 1
    assert result['content_repairs'] == [{'stage': 'understanding_contract',
                                          'code': 'incomplete_field_review', 'repair_index': 1}]
    assert result['decisions'][0]['answer_status'] == 'partial'
    assert len(p.calls) == len(client.requests) == 4
    assert p.budget.spent == pytest.approx(4 * 30 / 1_000_000)
    assert {r['model'] for r in client.requests} == {'fixed-model'}
    assert all(r['reasoning'] == {'effort': 'medium'} for r in client.requests)
    first, repaired = [json.loads(r['input']) for r in client.requests[:2]]
    assert repaired.pop('content_repair')['code'] == 'incomplete_field_review'
    assert repaired == first
    assert flow.results[-1]['content_repairs'] == result['content_repairs']


@pytest.mark.parametrize('next_failure', ['not json', 'scope'])
def test_contract_repair_cannot_be_followed_by_a_second_schema_or_scope_repair(next_failure):
    bad = understanding(); bad['field_review'] = []
    outputs = [bad]
    if next_failure == 'scope':
        outputs += [understanding(), {'questions': []}]
    else:
        outputs += [next_failure]
    p, client = provider(outputs)
    result = Workflow(Corpus(), p).turn(MESSAGE)
    assert result['error'] in ('ValueError', 'ProviderError')
    assert result['decisions'] == []
    assert len(result['content_repairs']) == 1
    assert len(client.requests) == len(outputs)
    assert result['facts'] == []


def test_scope_contract_repair_can_recover_once_without_executing_rejected_scope():
    p, client = provider([understanding(), {'questions': []}, scope(), candidate()])
    result = Workflow(Corpus(), p).turn(MESSAGE)
    assert result['error'] is None
    assert result['content_repairs'][0]['stage'] == 'scope_contract'
    assert result['scope_diagnostics'] == [{'stage': 'scope_contract', 'code': 'scope_intent_mismatch', 'rejected_structure': {'questions': []}}]
    assert result['decisions'][0]['question'] == 'taxes'
    assert len(client.requests) == 4


def test_budget_resets_between_customer_turns():
    bad = understanding(); bad['field_review'] = []
    outputs = [bad, understanding(), scope(), candidate()] * 2
    p, client = provider(outputs)
    flow = Workflow(Corpus(), p)
    results = [flow.turn(MESSAGE), flow.turn(MESSAGE)]
    assert all(r['error'] is None and len(r['content_repairs']) == 1 for r in results)
    assert len(client.requests) == 8


def test_failed_scope_does_not_merge_otherwise_valid_customer_facts():
    value = understanding()
    value['facts'] = [dict(field='monthly_charge', value='15', quote='$15', source_index=0, correction=False)]
    value['field_review'][0]['presence'] = 'stated'
    value['requested_answers'][0]['quote'] = 'Will my taxes change?'
    p, _ = provider([value, {'questions': []}, {'questions': []}])
    result = Workflow(Corpus(), p).turn('My plan costs $15. Will my taxes change?')
    assert result['error'] == 'ValueError'
    assert result['facts'] == []
    assert result['context']['monthly_charge'] is None


def test_item_change_records_revocation_without_erasing_previous_evidence():
    flow = Workflow(Corpus(), context={'line_item': 'device charge', 'general_amount': '20',
                                      'billing_error_confirmed': True, 'statement_date': '2026-10-01',
                                      'fraud': True})
    flow.observe('tool', 'The account tool identified a different charge.', {'line_item': 'insurance premium'})
    for field in ('general_amount', 'billing_error_confirmed', 'statement_date'):
        history = [f for f in flow.facts if f['field'] == field]
        assert history[0]['status'] == 'confirmed'
        assert history[-1]['status'] == 'unknown'
        assert history[-1]['reason'] == 'disputed_item_changed'
        assert history[-1]['value'] is None
        assert field not in flow.verified_fields
    assert flow.context.fraud is True
    assert 'fraud' in flow.verified_fields


def test_uncertain_credit_scope_preserves_known_fraud_escalation_without_amount():
    from policy_agent.workflow import LiveUnderstanding, ScopeReview
    class UncertainProvider:
        def generate(self, schema, system, payload):
            if schema is LiveUnderstanding:
                data = understanding()
                data['intents'] = ['general_credit']
                data['requested_answers'] = [dict(intent='general_credit', quote=MESSAGE,
                                                  requested_outcome='An ambiguous credit request')]
                return schema.model_validate(data)
            assert schema is ScopeReview
            return schema.model_validate({'questions': [dict(intent='general_credit', clause_quote=MESSAGE,
                                                             action_quote=None, classification='uncertain')]})
    result = Workflow(Corpus(), UncertainProvider(), {'fraud': True, 'line_item': 'device charge'}).turn(MESSAGE)
    assert result['error'] is None
    decision = result['decisions'][0]
    assert decision['action_status'] == 'requires_human'
    assert decision['answer_status'] == 'needs_information'
    assert decision['amount'] is None
    assert 'Rule 5' in decision['policy_ids']
    assert 'Tier 2' in decision['reply']
