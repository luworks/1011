"""Scenario-scoped evidence gaps; these checks do not approve business conventions.

Applied equally to every policy snapshot. Candidate uncertainty is never a new
business rule, and implementation rounding is never evidence of approval.
"""
from decimal import Decimal
import re

from .schema import AccountContext

CLARIFICATION_TOPICS = {
    'OD-02': 'whether the invoice-dispute requirements also apply to this standalone outage request',
    'OD-04': 'how the recorded ticket coverage or conflicting verification outcomes should be handled',
    'OD-05': 'how full days, partial days, or rounding should be treated in this calculation',
    'OD-06': 'which recurring charges belong to the affected services and how shared charges are allocated',
    'OD-07': 'which recurring rate applies when a plan or price has changed',
    'OD-08': 'how eligibility is determined at the relevant request or repeat-dispute date boundary',
}


def apply_boundaries(intent: str, c: AccountContext, decision: dict, messages: list[dict]) -> dict:
    if intent not in {'outage_credit', 'outage_deadline', 'general_credit', 'dispute_deadline'}:
        return decision
    gaps = []
    duration = None
    if c.outage_start and c.outage_end:
        try:
            duration = (c.outage_end - c.outage_start).total_seconds()
        except TypeError:
            pass
    outage = intent in {'outage_credit', 'outage_deadline'}
    if outage and c.outage_end and c.request_date:
        if (c.request_date - c.outage_end.date()).days == 30:
            gaps.append('OD-08')
            decision['conditions']['within_outage_window'] = None
            decision['conditions'].pop('within_window', None)
    if intent in {'general_credit', 'dispute_deadline'} and c.statement_date and c.request_date:
        if (c.request_date - c.statement_date).days == 60:
            gaps.append('OD-08')
            decision['conditions']['within_dispute_window'] = None
            decision['conditions'].pop('within_window', None)
    if intent in {'outage_credit', 'general_credit'} and c.history_checked and c.prior_resolved_date and c.request_date:
        if (c.request_date - c.prior_resolved_date).days in {0, 90}:
            gaps.append('OD-08')
            decision['conditions']['repeat_dispute'] = None
            if c.fraud is not True:
                decision['reasons'] = [r for r in decision['reasons'] if not r.startswith('Rule 5:')]
    if intent == 'outage_credit':
        # A known failed duration/window does not need a full-day calculation.
        qualifies_for_calculation = (duration is not None and duration > 14400
            and c.ticket_status == 'verified' and c.address_matches is True
            and c.request_date is not None and c.outage_end is not None
            and 0 <= (c.request_date - c.outage_end.date()).days <= 30)
        if qualifies_for_calculation:
            if duration % 86400:
                gaps.append('OD-05')
            elif c.monthly_charge is not None:
                # Exact divisibility, without Decimal's repeating-division precision.
                cents_numerator = c.monthly_charge * Decimal(int(duration // 86400)) * 100
                if cents_numerator % 30:
                    gaps.append('OD-05')
        if c.address_matches is False:
            gaps.append('OD-04')
        if c.ticket_status == 'unverifiable' and any(value is False for key, value in decision['conditions'].items()
                if key in {'address_matches', 'duration_over_four_hours', 'within_outage_window'}):
            gaps.append('OD-04')
        if not c.line_item or c.statement_date is None or (
                c.statement_date and c.request_date and (c.request_date - c.statement_date).days > 60):
            gaps.append('OD-02')
            # Rule 1's application to a standalone outage has not been approved.
            decision['reasons'] = [r for r in decision['reasons'] if not r.startswith('Rule 1:')]
        # Scope only current customer/tool statements. Historical agent prose cannot
        # supply new policy facts; arbitrary words in a citation are not account data.
        text = '\n'.join(m.get('content', '') for m in messages if m.get('role') in {'customer', 'tool'})
        if re.search(r'\b(?:only (?:one|two|some|\d+) (?:of (?:the|my|our) )?(?:lines|services)|partially affected|shared charge|bundle discount)\b', text, re.I):
            gaps.append('OD-06')
        if re.search(r'\b(?:plan|rate|price) (?:changed|changes|change|increased|decreased)\b', text, re.I):
            gaps.append('OD-07')
    if not gaps:
        return decision
    gaps = sorted(set(gaps))
    # Remove only unsupported certainty; explicit fraud, unverifiable-ticket,
    # known >30-day duration and exact supported >$300 still require review.
    if 'OD-05' in gaps or 'OD-06' in gaps or 'OD-07' in gaps:
        decision['reasons'] = [r for r in decision['reasons']
            if not r.startswith('Full elapsed') and not r.startswith('Rule 4(b): calculated')]
        decision['conditions'].pop('within_outage_amount_threshold', None)
    if intent == 'outage_credit' and any(gap in gaps for gap in ('OD-02', 'OD-04', 'OD-05', 'OD-06', 'OD-07')):
        decision['amount'] = None
    if 'OD-04' in gaps:
        decision['policy_ids'] = [sid for sid in decision['policy_ids'] if sid != 'Rule 2']
    mandatory = any(r.startswith(('Rule 4(', 'Rule 5:')) for r in decision['reasons'])
    # Invoice-specific late-dispute approval remains valid outside standalone outage.
    mandatory = mandatory or (not outage and any(r.startswith('Rule 1:') for r in decision['reasons']))
    decision['answer_status'] = 'partial'
    decision['action_status'] = 'requires_human' if mandatory else 'pending_verification'
    decision['missing'] = list(dict.fromkeys(decision['missing'] + ['policy_decision:' + gap for gap in gaps]))
    decision['reasons'].append('Scenario evidence boundary: ' + ', '.join(gaps) + '; no business convention approved.')
    if intent == 'outage_deadline':
        known = 'The outage request window is 30 calendar days from restoration. '
    elif intent == 'dispute_deadline':
        known = 'The invoice dispute window is 60 calendar days from the statement date. '
    elif intent == 'outage_credit':
        known = 'Qualifying outage credits use the recurring charge / 30 × full days, separately from the $75 general goodwill ceiling. '
    else:
        known = 'General goodwill requires a confirmed billing error and uses the cumulative $75 rolling limit. '
    topics = '; '.join(CLARIFICATION_TOPICS[gap] for gap in gaps)
    decision['reply'] = (known + 'The supplied policy needs clarification on ' + topics
        + ' before the affected amount or eligibility can be confirmed. '
        + ('An independent policy requirement still requires Tier 2 to decide. ' if mandatory else '')
        + 'No credit has been approved or issued; no business convention or completed handoff is assumed.')
    if decision.get('amount') is not None:
        decision['reply'] += ' The otherwise supported calculation/requested amount is $' + decision['amount'] + '; this does not resolve the open eligibility or approval boundary.'
    return decision
