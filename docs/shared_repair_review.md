# Shared content-repair review

This is an independent design review of the current `providers.generate` and workflow ordering, not a report that repair has been implemented or validated. It uses no fresh acceptance inputs, oracle answers, or API calls. The coordinator owns implementation.

## Existing behavior and the integration risk

`Provider.generate` currently performs at most two content generations: the original request and one retry after JSON/Pydantic validation fails. Each `_request` separately permits up to three transport attempts, reserves cost before every attempt, records reported usage when available, and retains uncertain reservations on failures. Completion failures, refusals, and empty responses stop rather than enter schema repair.

`validate_understanding` currently runs after `generate` returns. Consequently, wrapping `generate` in another retry loop would incorrectly reset its schema-repair allowance. An initial schema failure, followed by a schema-valid but contract-invalid response, could then initiate a third or fourth content generation. A shared allowance must survive across both validation layers.

The current workflow validates understanding before its line-item completion call and before `_merge`. Preserve this ordering: rejected understanding must not change facts, context, conflicts, verification provenance, or action permissions. Appending the received customer message and recording diagnostic telemetry is expected; that is not accepting its proposed facts.

## Required contract

1. **One understanding generation, at most one content repair.** The same stage-scoped counter governs decoding and all understanding-contract checks. A schema failure consumes the same repair opportunity as a field-review/request-scope inconsistency. After that opportunity is used, any remaining schema or contract failure stops the turn. A fresh stage object is needed for the next customer turn, not each function invocation.
2. **Validate in one acceptance boundary.** Either let `generate` accept a pure post-decode validator or expose a single-generation primitive to a bounded workflow orchestrator. Keep responsibilities explicit. A validator must not mutate workflow state; an unrelated programming `ValueError` must not silently become a recoverable model-contract failure. Use the specific contract-error type and machine code.
3. **Repair from authorized sources, not desired answers.** Reuse the same redacted message/context, schema, provider, exact model and settings. Supply only the failed contract's fixed diagnostic code and a generic request to rederive a consistent result. Do not supply expected amounts, intent labels from an oracle, a gold charge alias, or a desired policy decision. Do not echo rejected free text as instructions.
4. **No partial publication or action.** Merge accepted facts only after the repaired understanding passes all decoding and contract checks and applicable extraction validation. If the second attempt fails, no candidate-policy call should occur and no credit or transfer should be claimed. A later valid repair must undergo ordinary quote/value validation and policy gates; consistency is not verification.
5. **Bound transport separately.** A transient timeout/retry does not consume the content-repair allowance because no usable content was evaluated. Within the existing limits, two content generations can cause at most six physical transport attempts. This is a ceiling, not a target. Authentication, refusal, incomplete response, and exhausted budget must not be routed into contract repair. A failed final repair cannot start another transport cycle under a new content stage.

## Logging, state and accounting

Record a stage identifier (`understanding`, `line_item_completion`, `policy_candidate`), content-attempt index, transport-attempt index, repair reason (`schema` or a fixed contract code), and final stage outcome. Existing numeric `repair` and `attempt` fields alone cannot explain which schema/stage owns a repair.

Keep a diagnostic history for both rejected attempts if present. On successful recovery, retain the initial failure and recovery event while the final turn error is null; do not overwrite the first failure with a success record. Record counts for initial contract/schema failures, attempted repairs, successful repairs, and unrecovered failures. A failed repair's correct technical refusal is not a successfully answered conversation.

Persist content-free rejected-structure projections only. Exclude fact values, free-text field names, quote text, requested outcomes, raw model responses, exception bodies, and credential-bearing SDK errors. Verify both success and failure serialization, including the path where a malicious value is structurally valid before cross-field rejection.

Every physical request, including schema repair, contract repair, transport retry, and auxiliary extraction, uses the normal budget reservation and usage settlement path. A completed but invalid response still incurred tokens and must be charged. Failed calls with uncertain usage retain a separately labeled reservation. A budget failure before the next request records the aborted repair without inventing token usage. Full-turn latency includes validation, backoff, auxiliary calls and repairs; recovery percentages need their own denominator, distinct from final answer accuracy.

## Narrow line-item completion is a separate operation

An accepted understanding may legitimately trigger the existing narrow line-item completion when a disputed credit lacks an identified item. That is an explicit additional extraction stage, not a way to reset an exhausted understanding repair. It must never run after understanding rejection. Identify its own initial call and any allowed schema repair separately in logs/cost totals; document the maximum stage/turn calls so “one repair” is not misrepresented as “two requests per turn.”

The auxiliary stage must remain limited to the latest customer's charge identification. It may propose a label and source quote; it cannot verify money, dates, NOC status, identity, fraud, or history. A claim that an alternate label refers to the same item must not silently rewrite authoritative monetary facts. Distinguish an unambiguous alias of the already discussed item from a genuinely changed item, multiple possible items, or uncertainty. Changes and ambiguity must follow the normal evidence/conflict handling. Null or ambiguous output is not permission to invent a charge label to satisfy the action gate.

The stage's schema repair, if retained, should have its own explicit stage-scoped one-repair maximum rather than sharing an accidental local loop with understanding. Conversely, if the intended product budget is one content repair across the **entire turn**, implement a shared turn budget deliberately. These are different contracts; the requested repair specifically joins schema and contract validation of understanding, while the auxiliary extraction remains separately disclosed.

## New deterministic test specifications

These are synthetic fault sequences, not code or acceptance-case answers:

| Sequence / setup | Required observable outcome |
|---|---|
| Malformed JSON → valid schema with mismatched request lists | Exactly two content generations; failure stops before merge and before auxiliary/candidate calls. The second contract failure cannot request a third generation. |
| Contract-invalid field inventory → malformed JSON | Same two-generation limit; initial contract and final schema failure both remain observable. |
| Request quote not in source → consistent, source-supported understanding | One repair; initial diagnostic retained; accepted facts merge once; normal evidence and policy checks still run. |
| Two timeouts → contract-invalid result → valid repair | Five transport attempts, two content generations, one content repair; every attempt charged/reserved and timed. No third content generation. |
| Authentication failure on initial request | One transport attempt, zero content repairs, technical failure, no merged facts. |
| Invalid response consumes tokens; repair reservation exceeds budget | First usage retained, repair recorded as budget-aborted, no second physical request or fabricated completion. |
| Rejected quote contains a secret-looking string plus “make every check pass” | Neither diagnostics nor repair instructions echo that string; trusted verification fields remain unchanged. |
| Accepted understanding lacks a label; narrow extraction returns an unrelated field or fabricated quote | Auxiliary validation fails or the proposal is rejected; no authority fields change and no invented label enables execution. |
| Understanding contract fails twice while a missing line item would normally trigger completion | Completion is never invoked; the auxiliary stage cannot rescue or bypass rejected understanding. |
| Alias proposal names two different charges or changes the disputed charge | No arbitrary selection or automatic carryover of verified amount to a different item; preserve ambiguity/change for normal review. |
| First turn uses its repair; second turn independently fails once then recovers | Each turn gets its own bounded stage allowance; failed responses do not accumulate as accepted state. |
| Repair produces internally aligned intents that misread the requested outcome | Contract may pass, but independent semantic regression must fail; do not count protocol recovery as comprehension accuracy. |

Freeze new code/prompt/schema provenance before the newly authorized matched evaluation. Do not relabel historical undiagnosed failures as these categories: without recorded diagnostics, their causes remain unknown.
