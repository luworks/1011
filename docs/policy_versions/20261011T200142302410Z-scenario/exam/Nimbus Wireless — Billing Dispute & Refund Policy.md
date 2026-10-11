# Nimbus Wireless — Billing Dispute & Refund Policy
**Internal reference for NimbusCare Customer Support — Billing Team**
Document ID: BIL-POL-014 · Version 6.2 · Effective: August 3, 2026
Owner: Billing Operations · Applies to: Postpaid mobile and home internet accounts

**Editorial revision status:** Draft for policy review and controlled evaluation; not a newly approved business policy. The original business effective dates and article update dates below are retained for provenance, not used as this revision's publication date. The paired snapshot's `manifest.json` supplies its exact UTC version timestamp, parent, and source hashes.

**Reading convention:** `OPEN DECISION OD-xx` identifies an unresolved business interpretation, not an approved answer. Do not treat a marked gap as evidence for a definite business conclusion. These labels record evidence boundaries; they do not invent tax treatment, credit entitlement, or a completed escalation. Consult OPEN_DECISION descriptions only when their stated scenario is present. A gap in another scenario does not make a fully specified calculation indeterminate. Cross-document authority remains unapproved under OD-01.

> This document governs how NimbusCare agents evaluate and resolve customer-initiated billing disputes and refund/credit requests. Rules are numbered for reference during live calls and chats. Where more than one rule appears to apply, the more specific rule for the situation governs; agents should not blend two rules into a single calculation. Rule 3 replaces Rule 2's general goodwill calculation track and ceiling for qualifying outage requests; it does not remove the independent escalation requirements in Rules 4 and 5. The interaction with Rule 1 is not fully specified; see OD-02.

---

## Rule 1 — Billing Dispute Eligibility Window

A customer may dispute any charge on a Nimbus Wireless invoice within **60 calendar days of the statement date** shown on that invoice. Disputes filed after the 60-day window may only be considered with Tier 2 Billing Specialist sign-off and are not guaranteed resolution. The dispute must identify the specific line item or charge being contested; general dissatisfaction with the total bill amount is not, by itself, a disputable item under this rule.

**SCENARIO REVIEW OD-02 / OD-08:** Trigger OD-02 when a standalone outage request lacks an invoice/line item or the invoice window has expired while the outage window has not. Keep the two clocks separate; the combined procedure needs business confirmation. Trigger OD-08 for a request on the 60th-day cutoff or disputed timezone/day-zero/cutoff facts; state the 60-calendar-day window without declaring that boundary eligible or ineligible.

---

## Rule 2 — General Refund / Goodwill Credit Limit

For billing errors confirmed by the agent (e.g., duplicate charges, incorrect proration, mis-applied promotions, mis-billed add-ons) that do **not** fall under a more specific policy in this document, NimbusCare agents may issue a goodwill refund or account credit of **up to $75.00 per account, per rolling 12-month period**, without further approval. This $75.00 ceiling is cumulative across all general goodwill credits issued to the account in the trailing 12 months, not a per-incident allowance.


Any general goodwill refund or credit that would bring the account's rolling 12-month total **above $75.00** requires Tier 2 Billing Specialist approval under Rule 4 before it is issued.

**SCENARIO REVIEW OD-03:** Trigger only when an outage condition fails and the customer seeks goodwill without a confirmed billing error or an established amount basis. Refer for evaluation; do not promise $75 or invent discretionary eligibility. A verified ordinary billing error with an established requested amount remains subject to the existing cumulative ceiling.

---

## Rule 3 — Service-Outage Credit Policy (Exception to Rule 2)

When Network Operations (NOC) confirms a service outage affecting the customer's service address that lasted **longer than 4 consecutive hours**, the affected lines are entitled to a **prorated Service-Outage Credit**, calculated as:

```
Service-Outage Credit = (current monthly recurring charge ÷ 30) × number of full days the account was without service
```

This credit is issued under a **separate policy track from Rule 2** and is **not counted against, and not capped by, the $75.00 General Refund/Goodwill Credit Limit**. A Service-Outage Credit may validly exceed $75.00 without triggering the Rule 2 ceiling, provided the conditions below are met.

To qualify, **all** of the following must be true:
- A valid NOC outage ticket number exists covering the customer's service address and the dates in question.
- The outage duration recorded on the NOC ticket exceeds 4 consecutive hours.
- The customer requests the credit within **30 calendar days of the outage's resolution date** (not the billing statement date).

If a condition is established as not met (no NOC ticket, outage ≤ 4 hours, or request made more than 30 days after resolution), the request does not qualify under this rule and should instead be evaluated under Rule 2 as a general goodwill request, subject to Rule 2's eligibility requirements, the cumulative $75.00 ceiling, and Rules 4 and 5. Referral does not approve a credit; see OD-03.

**SCENARIO REVIEW — Apply only the relevant item:**
- **OD-04:** An unqueried/incomplete lookup remains unknown. Request verification. Address/date mismatch or an unverifiable ticket combined with another failed condition needs business clarification of the state-to-action mapping; do not silently relabel it as absent. A known unverifiable ticket still triggers Rule 4(b).
- **OD-05:** Trigger for a qualifying outage shorter than a full day, a remaining partial day, disputed calendar-versus-elapsed-day interpretation, or an amount requiring a rounding convention. State the unchanged formula and seek the missing convention; do not declare $0, floor partial days, select HALF_UP, or grant an assumed minimum. A supplied undisputed integral full-day count with an exact-cent result can be calculated without inventing a rounding method.
- **OD-06:** Trigger when only some lines are affected or the applicable shared/bundled charge is not established. Ask for the affected-service charge base; do not allocate by an invented rule. If all affected lines have an established combined recurring charge, use that combined base once; do not multiply it by the number of lines again.
- **OD-07:** Trigger when a rate or plan changed and the applicable outage charge has not been established. Do not choose the request-time or outage-time rate, or repurpose KB-1010 as an outage segmentation rule.
- **OD-08:** Trigger for the 30th-day request cutoff or disputed timezone/day-zero/cutoff facts. State the 30-calendar-day window from restoration without declaring that boundary eligible or ineligible.
- **OD-09:** Trigger when the question asks about downstream tax or surcharge adjustments. The recurring-plan-charge base does not answer that question. Do not assert either adjustment or no adjustment, invent a verification queue, or claim a completed handoff. A request for the recurring credit amount alone does not trigger this gap.

These review labels record missing policy evidence. Preserve any independent, clearly supported Rule 4/5 escalation; no review label authorizes issuance or proves an escalation was executed.

---

## Rule 4 — Escalation & Approval Thresholds

Escalate to a **Tier 2 Billing Specialist** before issuing any credit when any of the following apply:

- a. A **general** goodwill credit under Rule 2 would bring the account's rolling 12-month total above **$75.00**.
- b. A **Service-Outage Credit** calculated under Rule 3 exceeds **$300.00**, or the underlying outage exceeds **30 consecutive days**, or the NOC ticket number cannot be verified at the time of the request.
- c. The customer has filed a second billing dispute on the same account within **90 days** of a prior resolved dispute (repeat dispute), regardless of dollar amount.
- d. Suspected fraud indicators are present (e.g., disputed charges tied to a device or SIM not registered on the account, or a pattern of disputes across unrelated accounts from the same contact method).

**Note on applying (a) and (b) together:** a Service-Outage Credit that exceeds $75.00 does **not**, by itself, trigger escalation under (a) — (a) applies only to general Rule 2 credits. Escalation remains mandatory if any of conditions (b), (c), or (d) applies, and Rule 5 applies regardless of credit type. This statement does not settle the separate Rule 1 interaction marked in OD-02. Agents should confirm which rule (2 or 3) governs the request *before* checking which escalation condition, if any, applies — checking the $75.00 threshold against a Service-Outage Credit is a misapplication of this rule.

---

## Rule 5 — Repeat Dispute & Fraud Review

Regardless of which rule above would otherwise apply, any account with a second billing dispute within 90 days of a prior *resolved* dispute, or any flagged fraud indicator, must have the credit decision made by a Tier 2 Billing Specialist, not the front-line agent, even if the dollar amount is small. Front-line agents may continue to gather information and communicate status but may not issue the credit themselves in these cases.

**SCENARIO REVIEW OD-08:** Trigger for the same-day/90th-day repeat boundary, disputed time conventions, or uncertain third-and-later classification. Do not decide those cases by an unapproved convention. A clearly established second dispute strictly inside the window, or any fraud flag, still requires Tier 2 regardless of amount.

---

