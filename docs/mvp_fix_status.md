# MVP extraction and evidence repair

Status: READY — workflow-v7. Explicit-null authority fix independently verified; 256 local tests and all seven full live replay checks passed. Freeze current inputs before new acceptance. V6 is diagnostic only.

## Root causes

1. A sparse optional fact list allowed a model to extract a charge amount while omitting its separately named line item. The value validator could reject incorrect extracted facts but could not notice an omitted field.
2. Intent extraction conflated the topic referenced by a question with the outcome actually requested. A question about a credit's effect on another charge could therefore reopen the already answered credit calculation.
3. The candidate stage treated a formula's exclusions as evidence about a subsequent adjustment. A valid topical quotation did not entail the claimed relationship. Its account context also lacked the explicit reported/confirmed provenance already maintained by the workflow.

## General repair (`workflow-v5`)

- Live extraction now requires an inventory of all supported fact fields and a quoted current-message request for each intent. The program checks inventory completeness, inventory/fact consistency, and request quote provenance before making policy statements. A field inventory is a model assertion, not proof of semantic completeness.
- The prompt separates field extraction from requested-outcome classification, distinguishes references from new requests, and explicitly preserves genuinely mixed questions and requests to repeat an earlier answer. No customer name, transcript phrase, amount, date, or case-specific branch was added.
- The candidate stage receives requested-answer scopes and fact provenance/verified fields. Instructions require direct support for the asserted relationship: excluding a fee from a formula does not establish whether that fee is adjusted afterward. Both positive and negative claims need evidence. The independent policy gate remains authoritative.
- Offline fixtures retain their recorded contract and are not presented as evidence of improved live extraction. Invalid live protocols stop the turn as a technical failure instead of producing a business refusal.

## Verification

The full local suite passed 194 tests at the repair checkpoint. Sixteen new regressions cover different charge labels, conflicting charge items, real mixed requests, history scope, both unsupported tax outcomes, authoritative-field injection and malformed live contracts. Scripted providers test boundaries; they do not measure natural-language extraction quality.

The same Haiku 5.5 adaptive/medium configuration is being replayed against the complete original conversation, with the same shared US$25 ledger. Results will be recorded below. The eval owner has been notified to add independent paraphrase regressions and keep old/new prompt cohorts separate. No frozen expected answers were incorporated into the prompt.

## Intermediate live check (v4)

`runs/mvp-live-demo-haiku-medium-v4` completed six live turns: the line item was retained and the tax turn contained only the tax intent, but the model still chose `tax_adjustment=no`. This intermediate failure is retained and is not reported as fixed.

V5 therefore narrows the native candidate claim vocabulary to the reviewed corpus coverage: downstream tax outcomes are unknown, or not applicable for a non-tax question. This is an explicit system constraint, not evidence that the unconstrained model learned the rule. The independent output gate remains tested with malicious candidates that deliberately bypass the native schema. Broader positive/negative tax outcomes require a newly reviewed policy contract, not a prompt edit.

Targeted workflow, regression, adversarial, provider and integration checks: 72 passed. A concurrent full-suite checkpoint reported 202 passed / two failures in independently added `test_policy_comparison.py`; these have been reported to the eval owner and are not silently omitted.

Latest complete-suite recheck: **208 passed**. The two concurrent policy-comparison failures noted above are no longer present.

## READY: workflow-v6

A missing bill item on a credit request now triggers one narrow independent extraction call, accepting only source-quoted labels through the same fact merge checks. No item is guessed when absent; it remains reported, never backend verification.

Live result: `runs/mvp-live-demo-haiku-medium-v6/repair_acceptance.json`; all seven scoped acceptance checks passed. Bill item is retained, the tax turn has only the tax question, candidate tax adjustment is unknown, $82.50 and 30-day/14-day timing are correct, no issuance. Calls: 13; estimated cost US$0.0118601; total turn seconds 65.08.

Residual date-quote and candidate policy-ID/status mismatches remain; no claim of perfect extraction. Earlier v4/v5 failures are preserved. Tax correctness is a schema coverage boundary, not raw reasoning credit. Extra slot-check calls must be included in cost/latency. Freeze source before re-evaluation.

Post-freeze presentation follow-up: applied the service-charter statement-date next-step patch after eval confirmed its immutable v6 snapshot. Current complete suite: 251 passed, no xfail. This changes prose only; isolated model results retain their original service renderer hash.

## Explicit-null authority fix (v7)

Charter cross-review identified that an explicit `None` in trusted account state counted as verified, allowing a later customer value to inherit authority. Initialization now grants verification only to non-null normalized fields; tool updates to null revoke verification. False and numeric zero remain valid known values. Null fact records are explicitly unknown. Five new tests cover statement-date and amount initialization/tool-clear paths plus false/zero controls. No new business rule was added. Full suite checkpoint: 256 passed. V7 live replay is `runs/mvp-live-demo-haiku-medium-v7` (in progress).

V7 final replay: `runs/mvp-live-demo-haiku-medium-v7/repair_acceptance.json`, 13 calls, US$0.0116744, 63.37 total turn seconds. Workflow file SHA256 `f3df353e02affd6da19f21bebcf3114eee1b645959965ff11237f7216dee8a85`. No source changes after this release receipt.
