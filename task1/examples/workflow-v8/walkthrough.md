# Workflow v8 live repair verification

Exact configuration: Haiku 5.5 adaptive/medium. Historical confirmations are provided transcript evidence, not real account checks.

```json
{
  "checks": {
    "six_live_turns": true,
    "line_item_retained": true,
    "tax_only_current_question": true,
    "tax_candidate_unknown": true,
    "amount_correct": true,
    "deadline_correct": true,
    "no_issuance": true
  },
  "all_passed": true,
  "model": {
    "provider": "anthropic",
    "model": "claude-haiku-5-5",
    "input_per_million": 0.1,
    "output_per_million": 0.5,
    "cached_input_per_million": 0.01,
    "max_output_tokens": 8192,
    "max_input_token_bound": 90000,
    "role": "screen",
    "price_source": "https://platform.claude.com/docs/en/models/haiku-5-5/overview",
    "price_checked": "2026-10-11",
    "selection_reason": "User-requested model and supported effort sweep; accuracy first, then speed among equal accuracy, then cost.",
    "config_id": "anthropic/claude-haiku-5-5/adaptive/medium",
    "capability_source": "https://platform.claude.com/docs/en/build-with-claude/effort",
    "effort": "medium",
    "thinking": {
      "type": "adaptive"
    }
  },
  "cost_usd": 0.011434,
  "calls": 13,
  "total_turn_seconds": 63.154353500227444,
  "workflow_file_sha256": "2a561f1aa2bcc42d5ef245c473983417dcd90472d53304601f6da9d2ec30b753",
  "limitations": [
    "Single live replay, not statistical proof.",
    "Tax unknown is schema coverage, not autonomous reasoning.",
    "Candidate amount/action/status/policy-id mismatches remain visible and blocked."
  ]
}
```

## Turn 1

Hi, I need to dispute a charge on my latest bill. My service was out for almost two weeks last month and I still got charged the full $225.00 like nothing happened.

**Final reply (verbatim)**

> I understand you want this billing concern resolved. Here is what the available evidence supports.
> A qualifying Service-Outage Credit is separate from the $75 general goodwill ceiling and is not counted against it. Account or eligibility checks are incomplete; no credit has been approved or issued.
> Please identify the specific invoice charge you are disputing.
> Please have authorized support verify the statement date on the disputed invoice before assessing the dispute deadline.
> The next step is to have authorized support verify the outstanding account and eligibility details before a credit decision.

- outage_credit: needs_information / pending_verification; rules: Rule 1, Rule 3, Rule 4, Rule 5; evidence: Rule 1, Rule 3, Rule 4, Rule 5, KB-1004, KB-1005, KB-1006, KB-1007, KB-1001; missing: valid_ticket, address_matches, duration_over_four_hours, within_outage_window, line_item, statement_date, dispute_history, fraud_check, identity_verification

Diagnostics: candidate_mismatch:outage_credit:policy_ids

## Turn 2

Account is [ACCOUNT], and the card ending is [REDACTED].

**Final reply (verbatim)**

> Thank you. Account verification must be completed through the authorized process before any credit is issued.

Diagnostics: 

## Turn 3

Service went down on September 10th at 6 AM and wasn't back until September 21st at 6 AM — all three lines, totally dead, no calls or data. I'm disputing the full $225.00 recurring charge on the invoice dated October 1st.

**Final reply (verbatim)**

> I understand you want this billing concern resolved. Here is what the available evidence supports.
> A qualifying Service-Outage Credit is separate from the $75 general goodwill ceiling and is not counted against it. Account or eligibility checks are incomplete; no credit has been approved or issued.
> The next step is to have authorized support verify the outstanding account and eligibility details before a credit decision.

- outage_credit: needs_information / pending_verification; rules: Rule 1, Rule 3, Rule 4, Rule 5; evidence: Rule 1, Rule 3, Rule 4, Rule 5, KB-1004, KB-1005, KB-1006, KB-1007, KB-1001; missing: valid_ticket, address_matches, duration_over_four_hours, within_outage_window, dispute_history, fraud_check

Diagnostics: candidate_mismatch:outage_credit:amount, candidate_mismatch:outage_credit:answer_status, candidate_mismatch:outage_credit:policy_ids

## Turn 4

Okay, but isn't your refund limit only $75? I saw something like that in your terms once. So you can only give me $75 back for this, right?

**Final reply (verbatim)**

> I understand you want this billing concern resolved. Here is what the available evidence supports.
> A qualifying Service-Outage Credit is separate from the $75 general goodwill ceiling and is not counted against it. The policy calculation is ($225.00 / 30) x 11 full days = $82.50. Account or eligibility checks are incomplete; no credit has been approved or issued.
> The next step is to have authorized support verify the outstanding account and eligibility details before a credit decision.

- outage_credit: grounded / pending_verification; rules: Rule 1, Rule 3, Rule 4, Rule 5; evidence: Rule 1, Rule 3, Rule 4, Rule 5, KB-1004, KB-1005, KB-1006, KB-1007, KB-1001; missing: dispute_history, fraud_check

Diagnostics: candidate_mismatch:outage_credit:policy_ids

## Turn 5

Sure, no rush. While you're looking into that — does whatever credit I end up getting also reduce the taxes and regulatory surcharges I paid during those eleven days, or is it only applied against the plan charge itself?

**Final reply (verbatim)**

> The outage-credit formula applies only to the recurring plan charge. The provided policy and all ten KB articles do not establish whether this credit changes taxes or regulatory surcharges. I cannot confirm either outcome; that part needs human clarification.
> Please ask human support to clarify whether an applicable policy provides for tax or surcharge adjustments.
> Please request human review of this question and the available findings; this prototype has not submitted a handoff.

- taxes: partial / requires_human; rules: ; evidence: KB-1003, KB-1004; missing: tax_adjustment_policy

Diagnostics: candidate_mismatch:taxes:answer_status, candidate_mismatch:taxes:policy_ids

## Turn 6

Sounds good. One more thing while I have you — how long do I actually have to submit a request like this after an outage gets fixed? Just want to make sure I'm not about to miss some deadline.

**Final reply (verbatim)**

> The request window is 30 calendar days from the outage resolution date. The recorded request is 14 days later and is within that window.

- outage_deadline: grounded / not_applicable; rules: Rule 3; evidence: Rule 3, KB-1005; missing: 

Diagnostics: candidate_mismatch:outage_deadline:action_status
