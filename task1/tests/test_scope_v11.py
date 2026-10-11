"""Scope source grounding, independent of the original conversation wording."""
import json

import pytest

from policy_agent.diagnostics import UnderstandingContractError, repair_feedback, scope_diagnostic, REPAIR_INSTRUCTIONS
from policy_agent.workflow import ScopeReview, validate_scope


def review(clause, action, classification='explicit'):
    return ScopeReview.model_validate({'questions': [dict(intent='dispute_deadline', clause_quote=clause,
                                                          action_quote=action, classification=classification)]})


@pytest.mark.parametrize(('message', 'clause', 'action'), [
    ('What is the deadline for challenging an invoice?', 'What is the deadline for challenging an invoice?', None),
    ('Tell me the dispute deadline.', 'Tell me the dispute deadline.', 'Tell me'),
    ('Please explain. How long do I have to challenge this charge?',
     'How long do I have to challenge this charge?', 'Please explain'),
])
def test_explicit_questions_and_commands_grounded_without_nested_action_requirement(message, clause, action):
    validate_scope(review(clause, action), ['dispute_deadline'], message)


@pytest.mark.parametrize(('clause', 'action', 'code'), [
    ('What is the invoice deadline?', 'calculate the deadline', 'scope_action_support_missing'),
    ('You requested a filing deadline', None, 'scope_source_support_missing'),
    ('What is the invoice deadline?', '', 'scope_action_support_missing'),
    ('What is the invoice deadline?', '   ', 'scope_action_support_missing'),
])
def test_fabricated_or_blank_sources_still_rejected(clause, action, code):
    with pytest.raises(UnderstandingContractError) as caught:
        validate_scope(review(clause, action), ['dispute_deadline'], 'What is the invoice deadline?')
    assert caught.value.code == code


def test_rejected_scope_diagnostic_retains_structure_without_model_free_text():
    secret = 'secret-4532123456789012'
    diagnostic = scope_diagnostic(review(secret, secret), 'What is the invoice deadline?', 'scope_source_support_missing')
    assert secret not in json.dumps(diagnostic)
    assert diagnostic['rejected_structure']['questions'] == [dict(
        intent='dispute_deadline', classification='explicit', clause_present=True,
        clause_in_current_message=False, action_is_null=False, action_in_current_message=False)]


def test_all_contract_codes_have_specific_constant_repair_guidance():
    assert len(REPAIR_INSTRUCTIONS) == 7
    for code in REPAIR_INSTRUCTIONS:
        feedback = repair_feedback(code)
        assert feedback['code'] == code
        assert len(feedback['instruction'].split()) >= 10
    assert 'optional' in repair_feedback('scope_action_support_missing')['instruction']
    assert 'null' in repair_feedback('scope_action_support_missing')['instruction']
