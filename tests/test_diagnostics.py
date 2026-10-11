"""Rejected protocol diagnostics must explain failure without retaining text."""
import json
from pathlib import Path

import pytest

from policy_agent.corpus import Corpus
from policy_agent.diagnostics import contract_diagnostic
from policy_agent.workflow import (FACT_FIELDS, LiveUnderstanding, FactProposal,
                                   Workflow, EvidenceBoundCandidate, replay)


def understanding():
    return LiveUnderstanding.model_validate(dict(
        intents=['taxes'], facts=[], search_query='tax adjustment',
        field_review=[dict(field=f, presence='not_stated') for f in FACT_FIELDS],
        requested_answers=[dict(intent='taxes', quote='Will taxes change?', requested_outcome='Tax adjustment')]))


class Provider:
    def __init__(self, response):
        self.response, self.calls = response, []

    def generate(self, schema, system, payload):
        self.calls.append(schema)
        if schema is LiveUnderstanding:
            return self.response
        assert schema is EvidenceBoundCandidate
        return schema.model_validate({'questions': [dict(
            intent='taxes', policy_ids=[], amount=None, answer_status='partial',
            action_status='requires_human', evidence=[], tax_adjustment='unknown')]})


@pytest.mark.parametrize('kind', ['incomplete_field_review', 'field_fact_mismatch',
                                  'request_intent_mismatch', 'request_source_support_missing'])
def test_rejected_contract_has_fixed_diagnostic_and_unchanged_fail_closed_behavior(kind):
    value = understanding()
    if kind == 'incomplete_field_review':
        value.field_review.pop()
    elif kind == 'field_fact_mismatch':
        value.field_review[0].presence = 'stated'
    elif kind == 'request_intent_mismatch':
        value.intents = []
    else:
        value.requested_answers[0].quote = 'An unobserved message'
    provider = Provider(value)
    result = Workflow(Corpus(), provider, {'fraud': True}).turn('Will taxes change?')
    assert result['understanding_diagnostic']['stage'] == 'understanding_contract'
    assert result['understanding_diagnostic']['code'] == kind
    assert result['error'] == 'ValueError'
    assert result['understanding'] is None
    assert result['decisions'] == []
    assert result['candidate'] is None
    assert result['context']['fraud'] is True
    assert len(result['facts']) == 1
    assert provider.calls == [LiveUnderstanding]
    assert result['reply'] == ('I could not complete the evidence check due to a technical issue. '
                              'No credit has been issued. Please retry or request human assistance.')


def test_diagnostic_excludes_every_free_text_slot_and_invalid_numeric_indices():
    secret = '4532123456789012'
    value = understanding()
    value.search_query = secret
    value.facts.append(FactProposal(field=secret, value=secret, source_index=int(secret), quote=secret, correction=False))
    value.requested_answers[0].quote = secret
    value.requested_answers[0].requested_outcome = secret
    diagnostic = contract_diagnostic(value, 'Will taxes change?', 0, FACT_FIELDS,
                                     'request_source_support_missing')
    assert secret not in json.dumps(diagnostic)
    assert diagnostic['rejected_structure']['facts'] == [{
        'field': '__unrecognized__', 'source_index': None, 'source_index_is_current': False,
        'quote_in_current_message': False, 'correction': False}]
    provider = Provider(value)
    result = Workflow(Corpus(), provider).turn('Will taxes change?')
    assert secret not in json.dumps(result)


def test_accepted_live_and_offline_decisions_unchanged_without_diagnostics():
    value = understanding()
    live = Workflow(Corpus(), Provider(value)).turn('Will taxes change?')
    fixture = {k: value.model_dump()[k] for k in ('intents', 'facts', 'search_query')}
    offline = Workflow(Corpus()).turn('Will taxes change?', fixture)
    assert live['error'] is None
    assert live['understanding_diagnostic'] is None
    assert offline['understanding_diagnostic'] is None
    assert live['decisions'] == offline['decisions']
    assert live['reply'] == offline['reply']


def test_provided_offline_replay_retains_six_successful_turns_without_diagnostics():
    turns = replay(next(Path('exam').glob('*.txt')))
    assert len(turns) == 6
    assert all(t['error'] is None and t['understanding_diagnostic'] is None for t in turns)
    assert turns[3]['decisions'][0]['amount'] == '82.50'
