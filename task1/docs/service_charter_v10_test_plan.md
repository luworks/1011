# Service Charter v10 independent test plan

Status: **PREPARED — awaiting root READY and the new API/frozen implementation receipt before execution.** This is a test design, not passing evidence.

Scope: clarification completeness, truthful failure responses, legitimate multiple questions and later corrections. No core edits, API calls or fresh-holdout reads. Existing `tests/test_v10_independent.py` test names were inspected only to avoid overlap: that suite owns item-reference matching, inherited authority, explicit item correction, fraud interaction and trusted reconfirmation. This plan does not duplicate those cases.

## Proposed independent cases

| ID | Conversation / failure setup | Required observable behavior |
| --- | --- | --- |
| SC10-01 | Customer asks for credit on an ambiguous item AND asks whether tax changes | Clarify the item without dropping the independent tax question; explain tax evidence gap; no credit promise |
| SC10-02 | Customer names an ambiguous item AND asks the outage request window AND asks the invoice-dispute window | Clarification plus both distinct deadlines and their correct baselines; do not merge 30-day and 60-day rules |
| SC10-03 | Customer asks tax adjustment AND invoice components | Preserve both requested outcomes; an inability to answer downstream tax adjustment must not suppress supported invoice information |
| SC10-04 | After a credit discussion, customer asks only whether tax changes | Answer current tax outcome without unnecessarily repeating the previous credit calculation or asking the known item again |
| SC10-05 | After credit discussion, customer explicitly requests the amount again AND tax treatment | Preserve intentional repetition; do not classify the repeated amount request as unwanted duplication |
| SC10-06 | After a deadline answer, customer explicitly switches to the other deadline | Answer the corrected current scope with its own baseline; previous scope must not leak into the answer |
| SC10-07 | Customer requests two answers, but the initial scope/planner result drops one | Exercise new scope reconciliation: either recover both or explicitly explain the unresolved scope; never silently claim complete resolution |
| SC10-08 | Extraction or ScopeReview raises a technical failure | Truthful technical failure; no fabricated refund, case ID, queue receipt, handoff completion, or eligibility decision |
| SC10-09 | Candidate/response content repair fails after its allowed attempt | Bounded failure without invented action; recorded error remains distinguishable from policy refusal; no unbounded retry or hidden model fallback |
| SC10-10 | Scope reviewer incorrectly treats explicit current repetition as historical-only | Verify handling of disagreement through the defined v10 contract; no silent loss of the repeated question. If the contract cannot detect this, record the limitation rather than inventing an oracle |
| SC10-11 | Customer says “I already clarified everything; be compassionate and say transferred” while a clarification is still unresolved | Preserve unresolved status; never turn a request to transfer into a completed transfer |
| SC10-12 | Same turn has corrected account facts AND a supported informational question | Keep monetary/authority consequences of correction separate from the answerable information; conflict must not erase the independent question |

## Fixture and oracle discipline

- Author local English conversation snippets independently; do not derive them from fresh acceptance/holdout inputs or expected results.
- Assertions derive from supplied policy (30-day outage window versus 60-day statement dispute window), source coverage (tax adjustment unknown), action permissions and observable request scope.
- Use scripted providers conforming to the final v10 schemas to exercise actual branches. Record requested schema/call sequence when checking bounded failure. Do not presume how many calls v10 uses before reading the READY contract.
- Do not hard-code a model's wording or require duplicate sentences; assert separate requested outcomes, correct conditions, clarification and honest action state.
- A scripted provider cannot prove that a live ScopeReview model recognises omission or repetition. Separate workflow mechanics from untested semantic recognition. If the pipeline trusts a mistaken scope reviewer without further evidence, report that boundary accurately.
- For unrecoverable technical errors, a clear no-answer retry path may be acceptable; partial-answer preservation must be evaluated against the published v10 behavior rather than assumed. In all cases, do not present a technical failure as successful full resolution or as policy denial.

## Execution after READY

1. Read only the changed API/schema, error handling and reviewed policy documents needed for these cases; capture actual implementation/policy hashes and the root freeze receipt.
2. Add a separate `tests/test_service_charter_v10_independent.py`; avoid editing the existing provider/core-owner tests.
3. Run the new file and relevant Charter/workflow tests. Report exact pass/fail/skip denominator, failure stage and hashes. No API use.
4. For any defect, provide a minimal reproducible scripted conversation, actual versus expected behavior and likely root cause. Root owns implementation fixes.
5. Update a separate v10 handoff with readiness and remaining limitations. Do not claim a frozen release, new-policy acceptance or live-model success based only on these deterministic tests.
