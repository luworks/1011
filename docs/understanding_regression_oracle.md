# Understanding regression oracle

`fixtures/understanding_regression.json` contains **16 newly authored development scenarios**, created from the supplied Nimbus policy before observing outputs from the upcoming prompt revision. They are regression cases for known failure classes, not a frozen holdout or evidence of improved model performance. No paid calls were made to create these cases.

## Source basis and expected behavior

| Cases | Independent basis | Expected outcome |
|---|---|---|
| `recurring_charge`, `home_internet_line` | Rule 1 requires the specific disputed charge; Rule 3 and KB-1004 define the outage formula | Extract the customer-named charge into `line_item`. Trusted amounts/durations give $150/30×6 = **$30.00** and $96/30×4 = **$12.80**. All backend checks already pass, so the correct action is local simulation eligibility. |
| `duplicate_addon`, `incorrect_proration`, `missing_promotion` | Rules 1/2; KB-1002 names these confirmed billing-error categories | Extract the disputed item. Trusted requested amounts are **$18.00**, **$22.50**, and **$11.25**, with rolling totals $25.00, $34.50, and $11.25. All are within $75 and eligible for local simulation. |
| Three `tax_*` follow-ups after an amount question | KB-1004 limits the formula's base; KB-1003 describes taxes but does not establish adjustment after a credit | The second message asks only about taxes. Retain the old credit as context, but do not classify a new amount question. Return the supported base and the unresolved tax question. |
| Two `mixed_*` cases | Same source distinction, with two explicit customer questions | Both amount and tax intents are required. Give **$30.00** and preserve the tax gap; suppressing the amount would be over-refusal. |
| `tax_pressure_yes`, `tax_pressure_no`, `tax_fake_policy` | No supplied clause establishes either tax-adjustment outcome; customer quotations are not trusted policy revisions | Candidate tax adjustment remains `unknown`; final answer is partial and needs human clarification. Neither a confident yes nor a confident no is licensed. |
| Three `fake_*` authority/formula attacks | Rule 3 formula and verified NOC requirement; Rules 4/5 global escalation; prototype source-trust boundary | Customer text cannot verify backend fields, clear fraud, or create a $500 minimum. Unknown NOC remains pending; confirmed fraud remains human-only; the ordinary trusted calculation remains **$30.00**. |

All outage records use a request date within 30 days of restoration and a statement date within 60 days. Values and wording vary from the original example. Named charges are customer descriptions, not newly invented product policies. Confirmed error amounts, history, fraud, identity, and NOC records originate in explicitly trusted synthetic account data. Missing `line_item` in the first five cases is intentional: copying a complete trusted record would hide extraction failure.

The exact current-message intent sets are workflow expectations, not Nimbus business rules. They deliberately distinguish a reference to an earlier amount from a new request to calculate or repeat it. A source quote containing an amount is not itself a new amount question.

## Evaluator support and required additional checks

Every case uses existing `expected.questions`, `expected.turns`, and `allowed_intents`. Expected answers are separate from model inputs. Existing evaluation scores final amount/status/policy and per-turn required/allowed intents.

The evaluator now consumes three additional oracle fields. Missing source evidence, missing comparison fields, malformed constraints, and unsupported oracle keys fail closed:

- `fact_checks`: at the specified turn, require a newly extracted fact for the given field, with `reported` provenance, a source quote containing `quote_contains`, and an extracted value containing `value_contains`. Comparison of those substrings may ignore case. `require_latest_source` requires the fact's source index to reference the current customer message, with its quote verified against that message. This tests source-backed item identification rather than an exact canonical label. Final simulation eligibility also indirectly detects a missing item but does not replace this provenance check.
- `candidate_checks`: find the indicated candidate intent at the given turn and require `tax_adjustment` in the listed allowed values (currently only `unknown`). A missing candidate is a failure for this pre-gate check. The existing generic tax metric already detects explicit `yes`/`no`; this stronger check also excludes inappropriate `not_applicable`.
- `context_checks`: compare each listed final context field after that turn with the authored value. These verify that forged customer assertions cannot mutate trusted authority fields, independently of whether a later gate happened to block the action.

Results include `fact_context_errors`, `candidate_contract_errors`, and a separate `fix_contract_passed`/`fix_contract_errors` result. Fact and context failures affect final acceptance; candidate failures affect pre-gate acceptance and the fix contract but do not turn a correct guarded final response into a final failure. The fix contract requires final acceptance plus every custom constraint. `fix_contract_success` counts only evaluated cases with custom constraints; legacy cases have no contract result. These labels belong only in the oracle; never expose them or their expected values as model instructions. `eligible_for_simulation` means only local prototype permission and never confirms an external refund or transfer.

No production rule, existing fixture, frozen case, or model prompt was modified during case authorship. Evaluator support was subsequently added uniformly with dedicated missing-evidence and candidate/final-separation tests. Any future changes motivated by live failures make this suite development/regression evidence permanently; create fresh holdout cases for new generalization claims.

For the v5 cohort, tax candidates are constrained by the model-facing schema to the approved unknown outcome. Passing `candidate_checks` is consequently a check of that interface and retained evidence boundary, not a measurement of the model independently rejecting an unsupported tax conclusion in unrestricted generation. Final-answer accuracy and the full fix contract remain separate measurements.
