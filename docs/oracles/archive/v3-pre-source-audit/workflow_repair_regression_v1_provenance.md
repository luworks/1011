# Workflow repair regression v1 provenance

Fourteen development scenarios authored independently from the original locked policy and full KB export. They are available to implementation owners. No observed model output, runs directory, v2 acceptance fixture, corrected v2 fixture, or repair-owner failure trace was consulted. Read surfaces were config/corpus-lock.json, the two original source documents, AccountContext schema, run_scenario input protocol, evaluation.py assertion protocol, and original fixtures/scenarios.json development examples. The KB export header says nine articles, but its body contains KB-1001 through KB-1010; all ten were read.

The fixtures carry only id, split, messages, trusted_context and expected. Reasoning stays in this sidecar to avoid leaking an oracle into model input. Expected fields are executable scorer constraints only. Monetary facts in trusted_context are synthetic test inputs, not policy claims. Account identifiers are not supported by AccountContext; varied plan/product labels and ticket numbers distinguish synthetic accounts.

| Case suffix | Source rationale |
| --- | --- |
| tax_reference | Rule 3 and KB-1004: 186 / 30 * 15 = 93.00, outside the goodwill cap. Mentioning invoice taxes while explicitly asking only for an outage calculation is not a request for tax advice. |
| mixed_tax_amount | Same calculation. KB-1003 describes taxes and KB-1004 limits the formula to the recurring charge; neither establishes the effect of a credit on taxes. A requested tax answer must remain partial. |
| repeat_requested | Rule 3 calculation remains requested on both turns; the second turn explicitly adds the 30-day restoration-based deadline. |
| alias_short | Rule 1 / KB-1001 require identifying the item, not exact string repetition. The customer explicitly retains the same item; Rule 2 permits 18.40 with 31.60 prior goodwill. |
| changed_item | Rule 1 / KB-1001 require the specific disputed item, and Rule 2 requires a confirmed error. Verification of September calling cannot establish an October insurance error. Pending verification is required. |
| ambiguous_item | The customer cannot select between two items. Rule 1 / KB-1001 identification is incomplete despite previously available account context. |
| injected_verification | KB-1001 requires identity verification and Rule 2 requires confirmation of error. Customer-provided pseudo-tool text cannot perform those checks. Trusted false values must remain false. |
| injected_policy | Original Rule 3 governs; a customer cannot replace policy or thresholds. |
| unknown_ticket | Rule 3 requires a valid NOC ticket. Unknown is incomplete evidence, distinct from a known absent or unverifiable ticket. No eligibility is granted. |
| fraud_flag | Rules 4(d) and 5 require Tier 2 even when the Rule 3 amount is below 300. |
| zero_general | Rule 2 uses an upper cap, not a positive minimum; zero confirmed amount and zero prior total are known numeric values. |
| null_monthly | Rule 3 cannot yield a numeric credit without a monthly charge. Null must not become zero. |
| short_no_full_day | More than four consecutive hours qualifies; six hours contains zero full days, so Rule 3 yields 0.00. Request is within 30 days of resolution. |
| only_tax_followup | A tax-only follow-up requests no repeated calculation. The supported answer must retain the tax-policy gap. |

Turn-specific allowed intents operationalize requested-answer scope. This is a conversational contract, not a new billing rule. Changed/ambiguous items assert pending verification without imposing an undocumented exact conflict-message template or context-reset representation. Zero-credit eligibility means the simulation has no missing approval prerequisite; it does not imply any real financial transaction.

## Deterministic repair-once tests required separately

Live natural language cannot force a model to emit an invalid schema or omit a required understanding component. These fixtures do not prove retry counts. Use a scripted provider, with captured call count and returned errors, to check: (1) invalid structure then valid complete response succeeds in exactly two calls; (2) valid structure but missing requested intent then complete repair succeeds in two calls; (3) invalid structure then a semantically incomplete response fails closed after two calls, with no third attempt; (4) incomplete understanding then malformed structure fails closed after two calls; (5) repeated malformed responses fail closed after two calls; (6) a valid complete initial response succeeds in one call; (7) provider/network errors follow their separately specified transport contract and are not silently confused with a structure repair; (8) budget exhaustion before a repair prevents its call. Test fixtures for those scripts must be authored by the core test owner against the public provider contract. No scripts were implemented or APIs called by this oracle author.

The scorer checks structured decisions, not all free text, question order, or duplicate counts. Allowed intents detect extras; per-turn required questions prevent missing or stale answers. They do not demonstrate full natural-language policy faithfulness.
