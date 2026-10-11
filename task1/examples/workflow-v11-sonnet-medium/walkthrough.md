# Workflow-v11 live replay — Claude Sonnet 5.5 adaptive/medium

Single real-model replay of the supplied six-turn conversation on `workflow-v11` (code SHA256 `2032e473b946…`). 17 calls, ≈US$0.174, 47 s summed turn time, 0 technical failures. This is not fresh V3 acceptance.

| Turn | Decision | Answer / action | Gate corrections |
|---|---|---|---|
| 1 | outage_credit | partial / pending_verification | candidate_mismatch:outage_credit:answer_status, candidate_mismatch:outage_credit:policy_ids |
| 2 | — | identity only | — |
| 3 | outage_credit | needs_information / pending_verification | candidate_mismatch:outage_credit:policy_ids |
| 4 | outage_credit | grounded / pending_verification | candidate_mismatch:outage_credit:policy_ids |
| 5 | taxes | partial / requires_human | candidate_mismatch:taxes:action_status, candidate_mismatch:taxes:policy_ids |
| 6 | outage_deadline | grounded / not_applicable | — |

Required checks: $225 ÷ 30 × 11 = $82.50 (no extra ×3); the $75 Rule 2 cap is not applied; tax adjustment stays unknown and goes to human clarification; the 30-day window counts from restoration (day 14); unknown fraud and dispute-history checks keep the action at pending verification (no automatic approval). Raw candidate policy-ID and status mismatches were corrected by the deterministic gate and remain visible in `turns.jsonl`.
