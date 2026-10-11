"""Reviewed service-charter presentation; never modifies policy decisions."""
import hashlib
from importlib.resources import files

CHARTER_VERSION = '1.0'
CHARTER_SHA256 = hashlib.sha256(
    files('policy_agent').joinpath('agent_service_charter.md').read_bytes()
).hexdigest()


def charter_metadata() -> dict:
    return {'version': CHARTER_VERSION, 'sha256': CHARTER_SHA256,
            'status': 'team_proposed_not_customer_approved'}


def compose_reply(decisions: list[dict]) -> str:
    if not decisions:
        return 'Thank you. Account verification must be completed through the authorized process before any credit is issued.'
    parts = []
    if any(d['question'] in {'outage_credit', 'general_credit'} for d in decisions):
        parts.append('I understand you want this billing concern resolved. Here is what the available evidence supports.')
    parts.extend(d['reply'] for d in decisions)
    missing = {key for d in decisions for key in d['missing']}
    steps = []
    if 'line_item' in missing:
        steps.append('Please identify the specific invoice charge you are disputing.')
    if missing & {'statement_date', 'verified_statement_date'}:
        steps.append('Please have authorized support verify the statement date on the disputed invoice before assessing the dispute deadline.')
    if any(d['action_status'] == 'pending_verification' for d in decisions):
        steps.append('The next step is to have authorized support verify the outstanding account and eligibility details before a credit decision.')
    if 'tax_adjustment_policy' in missing:
        steps.append('Please ask human support to clarify whether an applicable policy provides for tax or surcharge adjustments.')
    if any(d['action_status'] == 'requires_human' for d in decisions):
        steps.append('Please request human review of this question and the available findings; this prototype has not submitted a handoff.')
    if missing & {'valid_request_date', 'valid_statement_date'}:
        steps.append('Please have the request and statement dates checked before relying on a deadline assessment.')
    parts.extend(steps)
    return '\n'.join(parts)
