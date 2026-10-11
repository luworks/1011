# Original conversation: final live replay audit

Audited `runs/final-live-replay/turns.jsonl` against the original `exam` transcript and the hash-verified policy/KB corpus. This is one live conversation, not a broad robustness result.

The run manifest records Anthropic `claude-haiku-5-5`, prompt `workflow-v3`, maximum output 4,096 tokens, and no explicit reasoning override (provider default). It started at `2026-10-11T19:20:15.523808+00:00`; its 11 API calls reported an estimated total cost of **$0.007897**, with no technical errors. Recorded code SHA-256: `d0a6b3ff36fedb7a9755ed814485a03e1f448f534fe343d33096ed7740294968`; corpus version: `dbb59ca9a429ab22142b76f32c0704dc3477c5e7ff0a33289efc12d700a05a5f`.

## Final customer-visible behavior

| Turn / source time | Question or information | Observed final result |
|---|---|---|
| 1 / 14:02 | Outage-related bill dispute | Explains separate outage track; no amount or approval before verification. |
| 2 / 14:04 | Identity details only | Acknowledges pending verification; no unrelated policy answer. Sensitive account/payment fields are redacted. |
| 3 / 14:06 | Outage dates and disputed charge | Keeps customer dates as reported; does not calculate before the subsequent NOC confirmation. |
| 4 / 14:09 | Is $75 the limit? | Correctly calculates **$225 ÷ 30 × 11 = $82.50**, with no second multiplication by three and no $75 cap. Action remains `pending_verification`; explicitly says no credit was approved or issued. |
| 5 / 14:11 | Taxes and regulatory surcharges | Answers the recurring-plan-charge calculation basis while explicitly leaving tax adjustment unknown; requests human clarification without claiming an external transfer occurred. |
| 6 / 14:13 | Deadline after restoration | Correctly states **30 calendar days from outage resolution** and that this request is **14 days later**, within that window. No credit execution is implied. |

Every stored source-message list exactly matches the redacted chronological prefix of the original transcript. Identity confirmation first appears after 14:05; NOC confirmation first appears after 14:08. No future transcript messages appear in an earlier turn. All stored retrieved excerpts and final-decision evidence references match the current locked source text, including locations and hashes. The tax turn retrieves all 15 clauses/articles (five rules plus ten KB articles). The identity-only turn appropriately has no policy retrieval.

## Model errors and limitations retained in the trace

The final responses meet the original conversation's central amount, exception, tax-gap, deadline, and no-issuance requirements. The underlying model output is not error-free:

- Turn 3 omits the explicitly stated disputed `line_item`. Consequently, turn 4 lists this field as missing even though the customer supplied it. History and fraud checks are independently still missing, so blocking issuance remains correct, but the extraction omission is a usefulness defect.
- Turn 3 proposes `$82.50` before NOC confirmation and treats not-yet-queried verification as mandatory human escalation. The gate replaces this with a pending-verification response without an amount.
- Turn 4 supplies one non-verbatim Rule 3 quotation. The trace flags `invalid_candidate_citation`; the published conclusion uses actual source evidence instead.
- Candidate policy-ID lists are mismatched in each substantive turn: they omit governing rules and/or mix article, document, and clause identifiers. Candidate action statuses also disagree on the tax and deadline turns. These remain diagnostic errors rather than being presented as passed model judgments.

This audit verifies the saved run, without additional API calls or source changes. It does not establish performance on other customers, policy packs, attack prompts, or future model versions.
