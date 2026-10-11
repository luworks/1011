"""Shared, versioned public data contracts."""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class EvidenceRef(BaseModel):
    document_id: str
    source_id: str
    path: str
    start_line: int
    end_line: int
    excerpt: str
    version: str

class AccountContext(BaseModel):
    model_config = ConfigDict(extra='forbid')
    monthly_charge: Decimal | None = Field(default=None, ge=0)
    outage_start: datetime | None = None
    outage_end: datetime | None = None
    request_date: date | None = None
    statement_date: date | None = None
    ticket_status: Literal['verified', 'absent', 'unverifiable', 'unknown'] = 'unknown'
    ticket_number: str | None = None
    address_matches: bool | None = None
    prior_resolved_date: date | None = None
    history_checked: bool = False
    fraud: bool | None = None
    identity_verified: bool | None = None
    line_item: str | None = None
    general_amount: Decimal | None = Field(default=None, ge=0)
    goodwill_total: Decimal | None = Field(default=None, ge=0)
    billing_error_confirmed: bool | None = None

    @field_validator('line_item', mode='before')
    @classmethod
    def normalize_line_item(cls, value):
        # An empty label cannot satisfy the policy's specific-item requirement.
        return (value.strip() or None) if isinstance(value, str) else value

class Fact(BaseModel):
    field: str
    value: object = None
    source_turn: int
    source_type: str
    status: Literal['confirmed','reported','unknown','conflicting']
    source_quote: str = ''

class QuestionDecision(BaseModel):
    question: str
    policy_ids: list[str] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(default_factory=list)
    answer_status: Literal['grounded','partial','needs_information','unsupported'] = 'needs_information'
    action_status: Literal['not_applicable','pending_verification','requires_human','eligible_for_simulation'] = 'not_applicable'
    reply: str = ''
    amount: str | None = None
    conditions: dict[str, bool | None] = Field(default_factory=dict)
    missing: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
