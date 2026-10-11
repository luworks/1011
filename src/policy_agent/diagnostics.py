"""Content-free diagnostics for rejected, structurally decoded understanding."""
from typing import Literal

from pydantic import BaseModel, ConfigDict

ContractCode = Literal['incomplete_field_review', 'field_fact_mismatch',
                       'request_intent_mismatch', 'request_source_support_missing']


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
