"""Content-free diagnostics for rejected, structurally decoded understanding."""
from typing import Literal

from pydantic import BaseModel, ConfigDict

ContractCode = Literal['incomplete_field_review', 'field_fact_mismatch',
                       'request_intent_mismatch', 'request_source_support_missing',
                       'scope_intent_mismatch', 'scope_source_support_missing', 'scope_action_support_missing']


class UnderstandingContractError(ValueError):
    """Machine code only; never include rejected text in an exception."""
    def __init__(self, code: ContractCode):
        self.code = code
        super().__init__(code)


class UnderstandingDiagnostic(BaseModel):
    model_config = ConfigDict(extra='forbid')
    stage: Literal['understanding_contract'] = 'understanding_contract'
    code: ContractCode
    rejected_structure: dict


def contract_diagnostic(value, message, current_source_index, fields, code):
    """Project validated enums/booleans/real indices, excluding all free text.

    Unknown field names and invalid indices are discarded, not hashed: either
    can itself contain sensitive data. No raw quote/value/outcome is persisted.
    """
    return UnderstandingDiagnostic(code=code, rejected_structure={
        'intents': list(value.intents),
        'field_review': [r.model_dump() for r in value.field_review],
        'facts': [{
            'field': f.field if f.field in fields else '__unrecognized__',
            'source_index': f.source_index if 0 <= f.source_index <= current_source_index else None,
            'source_index_is_current': f.source_index == current_source_index,
            'quote_in_current_message': bool(f.quote.strip()) and f.quote in message,
            'correction': f.correction,
        } for f in value.facts],
        'requested_answers': [{
            'intent': r.intent,
            'quote_in_current_message': bool(r.quote.strip()) and r.quote in message,
            'outcome_present': bool(r.requested_outcome.strip()),
        } for r in value.requested_answers],
    }).model_dump()


REPAIR_INSTRUCTIONS = {
    'incomplete_field_review': 'Return exactly one field_review entry for every allowed fact field, with no duplicate or omitted fields.',
    'field_fact_mismatch': 'Make each field_review presence agree with facts: stated requires a fact for that field; not_stated requires no fact. Use only facts actually stated in the same input.',
    'request_intent_mismatch': 'Return one requested_answers entry for each listed intent, with matching intents and no extra entries.',
    'request_source_support_missing': 'Use a nonempty literal quote from the current message for each requested answer, and a nonempty requested_outcome. Do not quote previous messages or paraphrase a quote.',
    'scope_intent_mismatch': 'Return exactly one scope question for each distinct proposed_intent, with no extra or duplicate intents.',
    'scope_source_support_missing': 'Set each clause_quote to a nonempty, verbatim relevant clause from current_message. Do not paraphrase or quote previous messages.',
    'scope_action_support_missing': 'action_quote is optional, including for explicit questions: use null when no literal action fragment is needed. Otherwise copy a nonempty verbatim fragment from current_message, never a paraphrase; it need not be inside clause_quote.',
}


def repair_feedback(code: ContractCode) -> dict:
    """Only reviewed constant instructions; no model output or exception text."""
    return {'code': code, 'instruction': REPAIR_INSTRUCTIONS[code]}


def scope_diagnostic(value, message, code):
    return {'stage': 'scope_contract', 'code': code, 'rejected_structure': {
        'questions': [{
            'intent': q.intent,
            'classification': q.classification,
            'clause_present': bool(q.clause_quote.strip()),
            'clause_in_current_message': bool(q.clause_quote.strip()) and q.clause_quote in message,
            'action_is_null': q.action_quote is None,
            'action_in_current_message': q.action_quote is not None and bool(q.action_quote.strip()) and q.action_quote in message,
        } for q in value.questions],
    }}
