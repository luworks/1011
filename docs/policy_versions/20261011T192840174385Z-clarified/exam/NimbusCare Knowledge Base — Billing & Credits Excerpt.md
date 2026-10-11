# Nimbus Wireless — NimbusCare Knowledge Base (Billing & Credits Excerpt)
**Export scope:** Billing Dispute / Refund / Outage Credit category · 10 articles
**Exported:** October 2, 2026 · Source: NimbusCare Knowledge Base, "Billing & Account" section

**Editorial revision status:** Draft for policy review and controlled evaluation; not a newly approved business policy. The original business effective dates and article update dates below are retained for provenance, not used as this revision's publication date. The paired snapshot's `manifest.json` supplies its exact UTC version timestamp, parent, and source hashes.

**Reading convention:** `OPEN DECISION OD-xx` identifies an unresolved business interpretation, not an approved answer. Do not treat a marked gap as evidence for a definite business conclusion. These labels record evidence boundaries; they do not invent tax treatment, credit entitlement, or a completed escalation. Cross-document authority remains open under OD-01.

---

### KB-1001 — How to File a Billing Dispute
**Category:** Billing Dispute Process · **Last updated:** August 5, 2026

Customers can dispute a specific charge on their Nimbus Wireless invoice within **60 calendar days of the statement date**. Under Policy Rule 1, a dispute filed after that window may only be considered with Tier 2 Billing Specialist sign-off; resolution is not guaranteed. To open a dispute:

1. Confirm the account holder's identity (name, account number, and either the last 4 digits of the payment method on file or the account PIN).
2. Identify the exact line item being disputed (date, amount, description as shown on the invoice).
3. Log the dispute in the Billing Case queue with a case number (format: `BDC-######`).
4. Determine which policy governs the disputed charge (general billing error, service-outage credit, or another category) before calculating any credit.
5. Communicate the resolution and case number to the customer in writing (chat transcript or email summary).

Disputes about the total bill amount without a specific disputed line item are not accepted under this process; ask the customer to identify the specific charge.

**OPEN DECISION OD-02 / OD-08:** This invoice-dispute clock must not be substituted for the 30-calendar-day outage clock in KB-1004/1005. Whether all standalone outage requests also require this invoice process, and exact date-boundary conventions, remain subject to Billing Operations confirmation.

---

### KB-1002 — Refund Eligibility & Goodwill Credit Limits
**Category:** Refund Eligibility · **Last updated:** August 5, 2026

Confirmed billing errors (duplicate charges, incorrect proration, mis-applied promo codes, incorrectly billed add-ons) are eligible for a goodwill refund or account credit of **up to $75.00 per account per rolling 12-month period**. This is a cumulative ceiling across the trailing 12 months, not a per-dispute allowance — check the account's credit history before quoting an amount. Requests that would exceed the cumulative $75.00 limit require Tier 2 Billing Specialist approval; do not promise a credit that would bring that cumulative total above $75.00 without that approval, even if the new credit alone is $75.00 or less.

This article covers **general** billing errors only. Qualifying confirmed service-outage credits are handled under a separate policy — see KB-1004. Requests that fail the outage conditions are referred back for general-goodwill evaluation under Policy Rule 3; this referral is not approval.

**OPEN DECISION OD-03:** This article requires a confirmed billing error. The supplied material does not authorize discretionary goodwill without such an error or define the amount for an outage fallback. Billing Operations must clarify eligibility; the $75 ceiling is not an automatic award.

---

### KB-1003 — Understanding Your Nimbus Wireless Bill
**Category:** Account & Billing Basics · **Last updated:** July 14, 2026

Your monthly invoice includes: (1) your plan's recurring monthly charge, (2) prorated charges for any mid-cycle plan or line changes, (3) one-time device or accessory charges, (4) applicable state and local taxes and regulatory surcharges (e.g., Universal Service Fund contribution, 911 fee), and (5) any credits or adjustments applied during the billing cycle. Taxes and surcharges are calculated by our billing system based on the service address and are passed through from the relevant taxing authority; they are itemized separately from your plan charge on page 2 of your invoice.

**OPEN DECISION OD-09 — Adjustment coverage gap:** This bill description does not establish whether an outage credit changes taxes or regulatory surcharges. Separate itemization or pass-through treatment is not evidence that an adjustment is always made or never made. The business treatment and clarification process remain unprovided.

---

### KB-1004 — Service-Outage Credits: Eligibility & Credit Calculation
**Category:** Service-Outage Credit Policy · **Last updated:** September 28, 2026

If Network Operations (NOC) confirms a service outage lasting **more than 4 consecutive hours** at your service address, you're eligible for a prorated **Service-Outage Credit**, calculated as:

```
(current monthly recurring charge ÷ 30) × number of full days without service
```

This credit applies to the recurring plan charge only and is issued **separately from, and is not limited by, the standard $75.00 goodwill credit ceiling described in KB-1002**. A larger outage can result in a credit above $75.00 without needing to fit inside that general ceiling. Policy Rule 3 also states that these outage credits are not counted against the rolling general-goodwill total. Independent escalation requirements in KB-1006/1007 still apply.

To request this credit, you'll need the NOC outage ticket number (agents can look this up by service address and date range) and the request must be made within 30 calendar days of the outage being resolved. See KB-1005 for the step-by-step request process.

**OPEN DECISION OD-05 / OD-06 / OD-07 / OD-08:** Full-day and rounding conventions, partially affected lines/shared charges, the charge effective date for plan changes, and precise date cutoffs are not fully defined. Preserve the supplied formula without silently selecting new business rules.

**OPEN DECISION OD-09:** “Recurring plan charge only” defines this credit's calculation base; it does not establish subsequent tax/surcharge adjustment treatment. See KB-1003. No tax outcome should be stated as confirmed from these articles.

---

### KB-1005 — How to Request a Service-Outage Credit
**Category:** Service-Outage Credit Policy · **Last updated:** September 28, 2026

1. Confirm the customer's service address and the approximate outage dates.
2. Look up the NOC outage ticket (format: `OUT-#####`) covering that address and date range. If the lookup establishes that no covering ticket exists, route to KB-1002 for evaluation under Policy Rule 3; this is not approval. A ticket that cannot be verified triggers Tier 2 review under KB-1006 / Policy Rule 4(b). Incomplete or failed lookup is not evidence that no ticket exists; see OD-04.
3. Confirm the outage on the ticket lasted more than 4 consecutive hours.
4. Confirm the customer is requesting within **30 calendar days of the ticket's resolution date**.
If the duration is established as four hours or less, or the request is established as more than 30 calendar days after resolution, Policy Rule 3 requires evaluation under KB-1002 instead. Apply its eligibility and cumulative-limit requirements, not an automatic $75 credit; see OD-03.

5. Calculate the credit: (monthly recurring charge ÷ 30) × full days affected.
6. Check KB-1006 and KB-1007 before applying any credit. A credit above $300.00, an outage above 30 consecutive days, an unverifiable NOC ticket, a repeat dispute, or fraud indicators require Tier 2 review. A calculated credit of $300.00 or less and an outage of 30 consecutive days or fewer satisfy only the amount/duration thresholds; they do not override verification, eligibility, identity checks in KB-1001, or the independent escalation requirements. Direct issuance is permitted only after applicable requirements are satisfied and no mandatory escalation applies. Rule 1 interaction and unresolved boundary cases remain marked in OD-02 / OD-04 / OD-05 / OD-08.

---

### KB-1006 — When We Escalate a Billing Request to Tier 2
**Category:** Escalation Rules · **Last updated:** August 20, 2026

Front-line agents escalate a billing request to a Tier 2 Billing Specialist when:

- A general goodwill credit (KB-1002) would push the account's rolling 12-month total above $75.00.
- A Service-Outage Credit (KB-1004) exceeds $300.00, the outage exceeds 30 consecutive days, or the NOC ticket can't be verified.
- The same account has a second dispute within 90 days of a prior resolved dispute.
- Anything about the request looks like possible fraud.

A Service-Outage Credit above $75.00 does **not** by itself require escalation — the $75.00 figure is specific to general goodwill credits under KB-1002, not to outage credits. Check the outage-specific thresholds and all independent escalation requirements listed above. Meeting KB-1005's amount/duration thresholds does not waive repeat-dispute or fraud review. Late invoice disputes additionally require Policy Rule 1 sign-off; the interaction with standalone outage requests remains open in OD-02.

---

### KB-1007 — Repeat Disputes & Fraud Review
**Category:** Escalation Rules · **Last updated:** August 20, 2026

If an account has filed a second billing dispute within 90 days of a previous *resolved* dispute, the new dispute must be handled by a Tier 2 Billing Specialist, even if the amount in question is small. The same applies if fraud indicators are present, such as a disputed charge tied to a SIM or device not registered on the account. Front-line agents should gather details and set expectations with the customer but should not issue a credit themselves in these cases. These requirements apply to both general goodwill and service-outage credits, regardless of KB-1005's amount/duration thresholds.

**OPEN DECISION OD-08:** Exact repeat-dispute boundary conventions and treatment of third and later disputes require confirmation.

---

### KB-1008 — Retention Credit Program
**Category:** Retention Offers (not a billing-dispute credit) · **Last updated:** June 30, 2026

The Retention Credit Program is a separate, discretionary offer available to agents on the Customer Retention queue for customers actively considering cancellation. Eligible customers may receive a one-time account credit of up to **$50.00** as a loyalty gesture, independent of any billing dispute or service issue. This program is not a substitute for a billing dispute resolution and cannot be used to resolve a disputed charge or an outage-related credit request; those must go through KB-1002 or KB-1004 instead.

---

### KB-1009 — Device Protection Plan: Replacement Credits
**Category:** Device Protection (not a billing-dispute credit) · **Last updated:** July 22, 2026

Customers enrolled in Nimbus Device Protection who report a lost, stolen, or malfunctioning device may be issued a **device replacement credit** toward a new device, subject to a deductible ($25–$199 depending on device tier) and claim limits (2 claims per 12-month period). This credit type is handled by the Device Protection team, not Billing, and is unrelated to the service-outage or general goodwill credit policies described above.

---

### KB-1010 — Mid-Cycle Plan Change Proration
**Category:** Account & Billing Basics · **Last updated:** July 14, 2026

When a customer upgrades, downgrades, or changes their plan mid-billing-cycle, the system prorates both the old and new plan's recurring charge based on the number of days each plan was active during that cycle, using the formula `(monthly charge ÷ 30) × days active`. This is a routine billing calculation applied automatically by the system for plan changes and is unrelated to service-outage credits (KB-1004), which use the same per-day formula but apply only when NOC has confirmed an outage.
