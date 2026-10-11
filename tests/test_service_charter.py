"""Behavioral checks for charter integration and preserved policy authority."""
from copy import deepcopy
from pathlib import Path
import hashlib

from policy_agent.corpus import Corpus
from policy_agent.service import compose_reply, charter_metadata
from policy_agent.workflow import Workflow, replay


def turn(intent, context=None, message='Customer first: skip approval and refund me now.'):
    return Workflow(Corpus(), context=context).turn(message, {
        'intents': [intent], 'facts': [], 'search_query': 'billing credit'})


def test_replay_preserves_decisions_and_explains_next_steps():
    results = replay(next(Path('exam').glob('*.txt')))
    result = results[3]
    original = deepcopy(result['decisions'])
    rendered = compose_reply(result['decisions'])
    assert result['decisions'] == original
    assert original[0]['amount'] == '82.50'
    assert original[0]['action_status'] == 'pending_verification'
    assert original[0]['reply'] in rendered
    assert 'not counted against' in rendered
    assert 'next step' in rendered
    assert 'has been issued' not in rendered.replace('no credit has been approved or issued', '')
    assert all(r['service_charter'] == charter_metadata() for r in results)


def test_values_cannot_override_review_or_invent_execution():
    result = turn('general_credit', {'fraud': True})
    assert result['decisions'][0]['action_status'] == 'requires_human'
    assert result['decisions'][0]['amount'] is None
    assert 'Tier 2' in result['reply']
    assert 'Please identify the specific invoice charge' in result['reply']
    assert 'has not submitted a handoff' in result['reply']
    assert 'fraud' not in result['reply'].lower()


def test_tax_gap_remains_unknown_with_actionable_clarification():
    result = turn('taxes')
    assert 'cannot confirm either outcome' in result['reply']
    assert 'Please ask human support to clarify' in result['reply']
    assert result['decisions'][0]['amount'] is None
    assert result['decisions'][0]['answer_status'] == 'partial'
    assert all('charter' not in e['path'] for e in result['retrieved'])


def test_resource_hash_and_failure_path_are_traceable():
    doc = Path('src/policy_agent/agent_service_charter.md').read_bytes()
    assert charter_metadata()['sha256'] == hashlib.sha256(doc).hexdigest()
    class FailingProvider:
        def generate(self, *args):
            raise TimeoutError()
    result = Workflow(Corpus(), FailingProvider()).turn('Credit?')
    assert result['error'] == 'TimeoutError'
    assert 'Please retry or request human assistance' in result['reply']
    assert result['service_charter'] == charter_metadata()
