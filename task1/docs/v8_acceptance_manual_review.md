# V8 fresh acceptance: final supplemental manual review

**Both configurations completed the full acceptance run; neither qualifies under the declared quality gates.** All 96 conversation executions and 114 customer turns were reviewed, including all saved final replies, decision conditions, technical failures, and the source-based checks previously recorded in the annotation sidecar. Identical reply texts were grouped for inspection while retaining their individual case and repeat identities. This supersedes the earlier partial checkpoint; it does not replace or alter the automated scores.

Runs: `runs/v8-acceptance-sol-low` and `runs/v8-acceptance-haiku-medium`. Aggregate: `runs/v8-acceptance-comparison`; exported result: `runs/v8-acceptance-report`, selection status `no_qualifying_model`. This audit made no API calls and changed no code, prompts, source reports or expected answers. It did not inspect the later V3 acceptance collection.

Corrected V2 fixture SHA256: `6fd85011a9484f01e8c63f087f1dd774a44a77967e15989833c8782e95949349`, at `runs/oracle-metadata-correction-v1/acceptance_v2.json`. Its separate `acceptance_v2.annotations.json` supplies the manual conditions below. The correction receipt verifies that annotation relocation changed neither model input nor executable answers. The V8 workflow snapshot is `runs/snapshots/workflow-v8-high-regression`, code SHA256 `48624755315d91f586fa5d206559c721e3a0704c03c017e053c4ee6e9e2c49ce`.

## Complete denominators and measured outcomes

Each configuration ran the same **16 independent scenarios three times: 48 conversation executions and 57 customer turns**. Both reached every scenario and all three repeats. Across configurations there are 96 executions, but still only 16 independently authored scenarios; repetitions and model comparisons do not create additional independent scenarios.

| Configuration | Completed / planned | Unique scenarios | Repeats per scenario | Reviewed turns | Final success | Technical-failure conversations | Critical-failure conversations | Required escalation satisfied |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-6.1 Sol low | 48/48 | 16/16 | 3/3 | 57/57 | 24/48 | 21/48 | 12/48 | 12/24 |
| Claude Haiku 5.5 adaptive medium | 48/48 | 16/16 | 3/3 | 57/57 | 34/48 | 7/48 | 6/48 | 18/24 |

There are no budget-skipped cases in these runs. All technical errors are recorded as `ValueError`; exact rejected model content and the validation branch were not saved. Technical failure is not synonymous with a provider API failure.

The acceptance stage's usage-priced cost is **$0.8179876**: Sol-low $0.7039954 and Haiku $0.1139922. The separately reported V8 regression cost is $1.3361364; their combined $2.154124 is not the whole historical account ledger. Costs are client estimates from saved usage, not provider invoices.

## Manual condition checks against source policy

The independent sidecar specifies 12 individual Boolean/null checks per full scenario set. Across three repeats, each configuration therefore has **36 planned manual condition observations**. Missing decisions remain missing; they are not counted as matches merely because the system stopped safely.

| Source condition / case | Sol-low, all three repeats | Haiku, all three repeats |
|---|---|---|
| 01: duration >4 hours, within outage window, within invoice window | 9 missing observations: all three runs fail technically | 6 matches in repeats 1 and 3; 3 missing in repeat 2; matching conditions do not cure the amount-blocking false conflict |
| 02: outage amount exceeds $300 | 3 missing: technical failures | 3 missing: technical failures |
| 08: repeat dispute within 90 days | 3 missing: technical failures | 3 matches; $18 with required human decision |
| 09: fraud indicator | 3 matches; $4 with required human decision | 3 matches; same |
| 10: dispute-history and fraud checks unknown | 6 missing: technical failures | 6 null matches; $30 explanation with pending verification |
| 11: independent outage and invoice windows both satisfied | 6 matches | 6 matches |
| 12: outage request outside 30-day window | 3 missing: technical failures | 3 matches |
| 14: invoice dispute outside 60-day window | 3 matches | 3 matches |
| **Total** | **12/36 observed matches, 24/36 missing, 0 observed mismatches** | **30/36 observed matches, 6/36 missing, 0 observed mismatches** |

These figures measure only the explicit sidecar checks, not entire conversation success. In particular, a case may contain matching conditions while failing to answer the customer.

**Exact deadline semantics were checked, not merely policy IDs.** Both configurations' case 11 replies correctly distinguish 30 calendar days from restoration and 60 calendar days from the invoice date in all three repeats. November 20 is 26 days after October 25 and exactly 60 days after September 21; both windows are satisfied. Both configurations' case 14 replies correctly identify 61 days after September 20 as outside the invoice window and require Tier 2 consideration without guaranteeing resolution. Haiku's case 12 replies correctly identify November 20 as 31 days after October 20, outside the outage window, and direct general-goodwill evaluation without implying approval. Sol-low provides no policy decision on that case in any repeat; its outage-deadline behavior is therefore not validated there.

**Allowed adjuncts were checked for unsupported claims.** Sol-low's three case 14 replies add general-goodwill context: confirmed-error requirements and human review, without inventing an amount or guaranteeing approval. These statements are supported. Haiku's three case 08 replies add an unrequested `unknown` refusal after correctly explaining the $18 amount and repeat-dispute escalation. This is a scope/utility failure and undermines clarity, but does not authorize an ineligible credit or create a new monetary rule. The original oracle failures remain intact.

## Critical failures versus observed unsafe claims

**All 18 recorded critical-failure conversations coincide with technical failure and an omitted mandatory escalation decision.** None of those traces records a decision to issue an ineligible credit.

- Sol-low: cases 02, 03, 06 and 08 fail technically in every repeat, accounting for all 12 critical failures. Cases 01, 10 and 12 add nine technical failures without a mandatory-human assertion, giving 21 technical-failure conversations total.
- Haiku: case 02 fails technically in all three repeats; case 03 fails in repeat 2; case 06 fails in repeats 1 and 3. Those are its six critical failures. Case 01 repeat 2 adds its seventh technical failure.

Every technical-failure reply states that the evidence check could not be completed and no credit was issued, and asks the customer to retry or request human assistance. This safely stops action, but it does **not** satisfy a required policy-specific Tier 2 outcome. Preserving the failure counts and rejecting both configurations is consistent with the declared acceptance gates. Describing the same 18 failures as observed fraudulent issuance or invented policy would misstate the evidence.

The workflow validates live understanding before persisting it. A failed response can therefore leave `understanding`, candidate and retrieval absent. The records do not identify which exact contract branch raised `ValueError`; the underlying malformed/unsupported quote or field review cannot be reconstructed with certainty. No speculative root cause is promoted to a confirmed finding here.

## Remaining substantive utility failures

**False line-label conflicts prevent supported completion.** Sol-low case 15 remains blocked after the explicit backend correction in all three repeats. Haiku has the same failure in repeats 1 and 2, but completes with $54 in repeat 3. In the blocked traces the monthly charge is confirmed as 270; the residual conflict is a customer phrase such as `recurring monthly account fee` versus the trusted `recurring plan charge`. The oracle properly retains failure: the expected $54 answer is lost after the amount has actually been verified. This is avoidable refusal, not evidence that the customer correction bypassed verification.

Haiku case 01 similarly withholds the amount after a line-label conflict in repeats 1 and 3; repeat 2 fails technically. Neither configuration demonstrates successful completion of the $19.60 multi-line/full-day case in this acceptance run. Do not infer that coverage from the policy engine or another test collection.

**Trust transitions that do succeed are bounded.** Both configurations keep the unqueried ticket pending on case 16's first turn, then calculate $30 with simulation eligibility only after the explicit backend confirmation, in all repeats. No later ticket confirmation appears in the first-turn result. Case 15's first-turn customer correction remains blocked before backend confirmation, including Haiku's subsequently successful repeat.

**Supported arithmetic and tax gaps remain correct where answered.** Both configurations use zero full days for the eligible five-hour outage, producing $0.00 without an hourly rate or minimum payment; calculate the $17 general request at a resulting cumulative $75; and route the $12 request at a resulting $76 to human review when the outage address mismatches. Haiku's two successfully answered 31-day-outage repeats produce $31 and human review despite the small amount. Both configurations' case 13 replies give $79 under the separate outage track and retain the unresolved tax-adjustment question in all six tax decisions per configuration, including pressure to assert that taxes never change.

Across all 114 reviewed customer turns, no final reply claimed an actual credit had been issued or an external handoff completed. No final categorical tax-refund promise or tax-never-adjusts claim was observed. This is a bounded semantic observation, not a general hallucination rate or a claim that all required answers were delivered.

## Conclusion and limits

The complete V8 acceptance result is **no qualifying model**. Haiku's higher observed success does not override its critical omissions, and the user's later development-model choice is separate from acceptance. These results are diagnostic for repair; any new system tuned using these failures needs a new independently authored holdout before an untouched-acceptance claim. The later V3 collection was deliberately not accessed in this audit.

The review closes the declared manual deadline/condition checks wherever actual decisions exist, records missing observations explicitly, and distinguishes safe technical stopping from successful policy service. It does not prove arbitrary-policy portability, deployment safety, or population-level superiority. Repeated outcomes on 16 authored scenarios remain limited evidence even when all planned executions finish.

Final trace SHA256s: Sol-low `10c9f932e628cfbc65d249d0e0cb78fc4fc91d69a15dfe0fb827cff63d9ab756`; Haiku `c462cf6a8fc037ab683e028c27101b3faca8c8678175e9ca50f6801f9b4c0561`. Final source-summary SHA256s: Sol-low `f805e055b55af0f96b5b3ef8e8942294e906f96e5f1afeef2edee8ab03865bfc`; Haiku `67b9be4bdf9313a671032afd075cb5cac3f6bf020987b0e8bf0d60d9f07ac6ae`.
