"""Reviewed executable policy; no model-generated business commitments."""
from decimal import Decimal, ROUND_HALF_UP
import re
from .schema import AccountContext, QuestionDecision
from .corpus import Corpus


def _decision(intent, corpus, ids, reply='', **kwargs):
    return QuestionDecision(question=intent, policy_ids=[x for x in ids if x.startswith('Rule')], evidence=[corpus.get(x) for x in ids], reply=reply, **kwargs)


def _global(c: AccountContext, d: QuestionDecision):
    """Independent global requirements apply even when local qualification is unknown."""
    repeat = None
    if c.history_checked:
        if c.prior_resolved_date is None:
            repeat = False
        elif c.request_date is not None:
            elapsed = (c.request_date - c.prior_resolved_date).days
            repeat = 0 <= elapsed <= 90 if elapsed >= 0 else None
    d.conditions.update(repeat_dispute=repeat, fraud=c.fraud, identity_verified=c.identity_verified)
    if repeat is True or c.fraud is True:
        d.action_status = 'requires_human'
        d.reasons.append('Rule 5: Tier 2 must make the credit decision for repeat disputes or fraud.')
    for missing, value in [('dispute_history',repeat),('fraud_check',c.fraud),('identity_verification',c.identity_verified)]:
        if value is None or (missing == 'identity_verification' and value is not True):
            d.missing.append(missing)
    if d.missing and d.action_status != 'requires_human':
        d.action_status = 'pending_verification'
    if d.action_status == 'requires_human':
        d.reply += ' A Tier 2 Billing Specialist must decide before any credit is issued.'
    elif d.action_status == 'pending_verification':
        d.reply += ' Account or eligibility checks are incomplete; no credit has been approved or issued.'
    else:
        d.reply += ' These checks permit a local simulation only; no actual credit has been issued.'
    d.missing = list(dict.fromkeys(d.missing))
    return d


def evaluate(intent: str, context: AccountContext, corpus: Corpus) -> QuestionDecision:
    c = context
    if intent == 'taxes':
        return _decision(intent,corpus,['KB-1003','KB-1004'],
            'The outage-credit formula applies only to the recurring plan charge. The provided policy and all ten KB articles do not establish whether this credit changes taxes or regulatory surcharges. I cannot confirm either outcome; that part needs human clarification.',answer_status='partial',action_status='requires_human',missing=['tax_adjustment_policy'],reasons=['Workflow evidence boundary: no supplied rule establishes tax adjustment; no invented routing queue.'])
    if intent == 'bill_explanation':
        return _decision(intent,corpus,['KB-1003'],'Your invoice includes recurring plan charges, mid-cycle prorations, one-time device or accessory charges, applicable taxes and regulatory surcharges, and credits or adjustments. Taxes and surcharges are itemized separately on page 2.',answer_status='grounded')
    if intent in ('outage_deadline','dispute_deadline'):
        outage = intent == 'outage_deadline'
        limit = 30 if outage else 60
        baseline = c.outage_end.date() if outage and c.outage_end else (c.statement_date if not outage else None)
        ids = ['Rule 3','KB-1005'] if outage else ['Rule 1','KB-1001']
        d = _decision(intent,corpus,ids,f'The request window is {limit} calendar days from '+('the outage resolution date.' if outage else 'the statement date; identify the specific disputed line item.'),answer_status='grounded')
        if baseline is not None and c.request_date is not None:
            elapsed = (c.request_date-baseline).days
            if elapsed < 0:
                d.answer_status='partial'; d.missing=['valid_request_date']; d.conditions['within_window']=None
            else:
                d.conditions['within_window']=elapsed <= limit
                d.reply += f' The recorded request is {elapsed} days later and is '+('within' if elapsed <= limit else 'outside')+' that window.'
                if elapsed > limit:
                    if outage:
                        d.reply += ' It must instead be evaluated under the general goodwill policy; this is not approval.'
                        d.policy_ids += ['Rule 2']; d.evidence.append(corpus.get('Rule 2'))
                    else:
                        d.action_status='requires_human'; d.reply += ' Tier 2 sign-off is needed for consideration, with no guarantee of resolution.'
        return d
    if intent == 'general_credit':
        d = _decision(intent,corpus,['Rule 1','Rule 2','Rule 4','Rule 5','KB-1001','KB-1002','KB-1006','KB-1007'],answer_status='needs_information',action_status='pending_verification')
        d.reply = 'General goodwill requires a confirmed billing error and uses a cumulative $75 limit per rolling 12 months, not a per-incident allowance.'
        d.conditions['billing_error_confirmed']=c.billing_error_confirmed
        if c.billing_error_confirmed is not True:
            d.missing.append('confirmed_billing_error')
        for field in ('line_item','general_amount','goodwill_total','statement_date','request_date'):
            if getattr(c,field) is None or getattr(c,field) == '': d.missing.append(field)
        if c.statement_date and c.request_date:
            elapsed=(c.request_date-c.statement_date).days
            d.conditions['within_dispute_window']=0<=elapsed<=60 if elapsed>=0 else None
            if elapsed>60:
                d.action_status='requires_human';d.reasons.append('Rule 1: dispute after 60 days requires Tier 2 sign-off.')
            if elapsed<0: d.missing.append('valid_statement_date')
        if c.general_amount is not None and c.goodwill_total is not None:
            total=c.general_amount+c.goodwill_total
            d.conditions['within_goodwill_ceiling']=total<=Decimal('75')
            if total>Decimal('75'):
                d.action_status='requires_human';d.reasons.append('Rule 4(a): rolling goodwill total exceeds $75; requested amount is not promised.')
            if c.billing_error_confirmed is True:
                d.amount=str(c.general_amount.quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
                d.reply += f' The requested amount is ${d.amount}; the resulting rolling total would be ${total:.2f}. This is not approval.'
                d.answer_status='grounded' if not d.missing else 'partial'
        if not d.missing and d.action_status!='requires_human': d.action_status='eligible_for_simulation'
        return _global(c,d)
    if intent == 'outage_credit':
        ids=['Rule 1','Rule 3','Rule 4','Rule 5','KB-1004','KB-1005','KB-1006','KB-1007','KB-1001']
        d=_decision(intent,corpus,ids,answer_status='needs_information',action_status='pending_verification')
        duration=None
        if c.outage_start and c.outage_end:
            try: duration=(c.outage_end-c.outage_start).total_seconds()
            except TypeError: pass
        elapsed=(c.request_date-c.outage_end.date()).days if c.request_date and c.outage_end else None
        d.conditions={
            'valid_ticket':True if c.ticket_status=='verified' and c.ticket_number and re.fullmatch(r'OUT-\d{5}',c.ticket_number) else (False if c.ticket_status=='absent' else None),
            'address_matches':c.address_matches,
            'duration_over_four_hours':duration>14400 if duration is not None and duration>=0 else None,
            'within_outage_window':elapsed<=30 if elapsed is not None and elapsed>=0 else None,
        }
        if c.ticket_status=='unverifiable':
            d.action_status='requires_human';d.reasons.append('Rule 4(b): NOC ticket cannot currently be verified.')
        if False in d.conditions.values():
            fallback=evaluate('general_credit',c,corpus)
            fallback.question=intent
            fallback.policy_ids=list(dict.fromkeys(['Rule 3']+fallback.policy_ids))
            fallback.evidence=[corpus.get('Rule 3'),corpus.get('KB-1005')]+fallback.evidence
            fallback.conditions.update(d.conditions)
            fallback.reply='The request does not qualify for the separate outage-credit track. '+fallback.reply
            if c.ticket_status=='unverifiable':
                fallback.action_status='requires_human';fallback.reasons+=d.reasons
                fallback.reply+=' The unverified NOC ticket also requires Tier 2 review.'
            return fallback
        d.reply='A qualifying Service-Outage Credit is separate from the $75 general goodwill ceiling and is not counted against it.'
        for key,value in d.conditions.items():
            if value is None:d.missing.append(key)
        if c.monthly_charge is None: d.missing.append('monthly_charge')
        if duration is not None and duration>30*86400:
            d.action_status='requires_human';d.reasons.append('Rule 4(b): outage exceeds 30 consecutive days.')
        if not d.missing:
            days=int(duration//86400)
            amount=(c.monthly_charge/Decimal(30)*Decimal(days)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
            d.amount=str(amount);d.answer_status='grounded'
            d.conditions['within_outage_amount_threshold']=amount<=Decimal('300')
            d.reply+=f' The policy calculation is (${c.monthly_charge} / 30) x {days} full days = ${amount}.'
            d.reasons.append('Full elapsed 24-hour days; final amount rounded to cents using ROUND_HALF_UP (implementation rounding convention).')
            if amount>Decimal('300'):
                d.action_status='requires_human';d.reasons.append('Rule 4(b): calculated outage credit exceeds $300.')
            elif d.action_status!='requires_human':d.action_status='eligible_for_simulation'
        # Rule 1's invoice dispute checks are separate from outage qualification.
        if not c.line_item: d.missing.append('line_item')
        if c.statement_date is None: d.missing.append('statement_date')
        if c.statement_date and c.request_date:
            dispute_days=(c.request_date-c.statement_date).days
            d.conditions['within_dispute_window']=0<=dispute_days<=60 if dispute_days>=0 else None
            if dispute_days>60:
                d.action_status='requires_human';d.reasons.append('Rule 1: dispute after 60 days requires Tier 2 sign-off.')
            if dispute_days<0:d.missing.append('valid_statement_date')
        return _global(c,d)
    decision = _decision(intent,corpus,list(corpus.entries),'I cannot establish a supported answer for this question from the provided material. Human clarification is needed.',answer_status='unsupported',action_status='requires_human',missing=['supported_question'],reasons=['Workflow evidence boundary; no business policy invented.'])

    decision.policy_ids = []  # Searched evidence is not an applicable governing policy.
    return decision
