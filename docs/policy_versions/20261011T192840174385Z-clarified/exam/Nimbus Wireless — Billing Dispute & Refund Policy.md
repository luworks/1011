# Nimbus Wireless — Billing Dispute & Refund Policy
**Internal reference for NimbusCare Customer Support — Billing Team**
Document ID: BIL-POL-014 · Version 6.2 · Effective: August 3, 2026
Owner: Billing Operations · Applies to: Postpaid mobile and home internet accounts

**Editorial revision status:** Draft for policy review and controlled evaluation; not a newly approved business policy. The original business effective dates and article update dates below are retained for provenance, not used as this revision's publication date. The paired snapshot's `manifest.json` supplies its exact UTC version timestamp, parent, and source hashes.

**Reading convention:** `OPEN DECISION OD-xx` identifies an unresolved business interpretation, not an approved answer. Do not treat a marked gap as evidence for a definite business conclusion. These labels record evidence boundaries; they do not invent tax treatment, credit entitlement, or a completed escalation. Cross-document authority remains open under OD-01.

> This document governs how NimbusCare agents evaluate and resolve customer-initiated billing disputes and refund/credit requests. Rules are numbered for reference during live calls and chats. Where more than one rule appears to apply, the more specific rule for the situation governs; agents should not blend two rules into a single calculation. Rule 3 replaces Rule 2's general goodwill calculation track and ceiling for qualifying outage requests; it does not remove the independent escalation requirements in Rules 4 and 5. The interaction with Rule 1 is not fully specified; see OD-02.

---

## Rule 1 — Billing Dispute Eligibility Window

A customer may dispute any charge on a Nimbus Wireless invoice within **60 calendar days of the statement date** shown on that invoice. Disputes filed after the 60-day window may only be considered with Tier 2 Billing Specialist sign-off and are not guaranteed resolution. The dispute must identify the specific line item or charge being contested; general dissatisfaction with the total bill amount is not, by itself, a disputable item under this rule.

**OPEN DECISION OD-02 — Relationship to outage requests:** Rule 1 states a 60-calendar-day invoice-dispute window; Rule 3 states a separate 30-calendar-day outage-request window. Neither clock substitutes for the other. The supplied text does not conclusively define whether every standalone outage-credit request must also satisfy Rule 1's invoice and line-item requirements, or how Rule 1 sign-off applies when only its window has expired. Billing Operations must define the combined procedure. See OD-08 for date-boundary conventions.

---

## Rule 2 — General Refund / Goodwill Credit Limit

For billing errors confirmed by the agent (e.g., duplicate charges, incorrect proration, mis-applied promotions, mis-billed add-ons) that do **not** fall under a more specific policy in this document, NimbusCare agents may issue a goodwill refund or account credit of **up to $75.00 per account, per rolling 12-month period**, without further approval. This $75.00 ceiling is cumulative across all general goodwill credits issued to the account in the trailing 12 months, not a per-incident allowance.

**OPEN DECISION OD-03 — Outage fallback eligibility:** Referral from Rule 3 means evaluation, not automatic entitlement. Rule 2 explicitly requires a confirmed billing error. The supplied text does not establish whether an outage request that fails Rule 3 can receive discretionary goodwill without a confirmed billing error, or how such an amount would be determined. Do not interpret the $75 ceiling as a promised $75 payment. Billing Operations must decide whether to expand Rule 2 or retain its confirmed-error requirement.

Any general goodwill refund or credit that would bring the account's rolling 12-month total **above $75.00** requires Tier 2 Billing Specialist approval under Rule 4 before it is issued.

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

**OPEN DECISION OD-04 — NOC verification states:** The source distinguishes no ticket (fallback evaluation) from a ticket that cannot be verified (Rule 4(b) escalation). It does not fully define incomplete lookup, temporary lookup failure, unmatched address/date coverage, or cases with both an unverifiable ticket and another failed condition. Preserve the recorded verification state; missing evidence does not establish either qualification or disqualification. Billing Operations must define the complete state-to-action table.

**OPEN DECISION OD-05 — Full days and rounding:** The formula is retained unchanged. The supplied text does not define full days as calendar days or elapsed 24-hour periods, minimum credits for an outage longer than four hours but shorter than one full day, treatment of partial days, or rounding order/method. Do not present an implementation convention as approved policy.

**OPEN DECISION OD-06 — Affected-line calculation base:** The source refers to affected lines but gives an account-level formula. It does not define allocation for a subset of affected lines, shared charges, or bundle discounts. Do not multiply an account-wide recurring charge by the line count a second time. Billing Operations must define the applicable affected-service charge base.

**OPEN DECISION OD-07 — Charge effective date:** “Current monthly recurring charge” does not specify which point in time governs when the plan or price changes before, during, or after an outage. Billing Operations must define the applicable charge and any segmentation.

**OPEN DECISION OD-09 — Taxes and surcharges:** The formula and KB-1004 establish a recurring-plan-charge calculation base. They do not establish whether taxes or regulatory surcharges are subsequently adjusted, automatically or manually. KB-1003 only describes bill components. Neither a positive nor a negative tax-adjustment conclusion is supported. The actual treatment and clarification owner/process require business confirmation.

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


**OPEN DECISION OD-08 — Date and repeat-dispute boundaries:** The supplied policy uses calendar days for Rules 1 and 3 but does not fully specify governing timezone, day-zero counting, cutoff time, or last-day inclusivity. Rule 5 does not fully specify the same-day/90th-day boundary or how third and later disputes are classified. Billing Operations must publish these conventions before boundary cases have a definitive oracle.
