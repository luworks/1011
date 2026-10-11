# Service Charter adversarial handoff

Status: **READY — statement-date guidance gap resolved and independently verified (35 passed, 0 xfailed). A separate explicit-null verification defect remains open; not unconditional authority-safety or release acceptance.**

Observed: 2026-10-11 12:42 PDT (19:42 UTC). Workflow: `workflow-v6`. Charter: `1.0`, team-proposed, not customer-approved.

## Ownership and scope

This pass only added `tests/test_service_charter_adversarial.py` and this handoff. It did not edit workflow, CLI, policy, service renderer, existing tests, evaluation artifacts or credentials. No API calls or paid evaluation. Existing Charter integration remains intact. No leader agent added.

The UK healthcare organisation at https://www.nimbuscare.co.uk/ is not established as the entity in the Nimbus Wireless billing exercise. The exercise's company may be fictional or anonymised; that inference is not a verified corporate identity. Do not import healthcare policies, patient obligations, NHS routing or the website's values into this telecom corpus.

## Evidence

- `uv run pytest -q tests/test_service_charter.py tests/test_service_charter_adversarial.py -rxX`: **32 passed, 1 xfailed** (0.12s). New file contributes 28 passing tests and one explicit strict expected failure; existing file contributes four passing tests.
- `uv run pytest -q -rxX`: **242 passed, 1 failed, 1 xfailed** (0.95s), exit 1. This is a shared-workspace snapshot, not a frozen Git revision.
- Full-suite failure: `tests/test_finalize_evaluation.py::test_development_never_invokes_final_selector`, line 43, expects `exposed in historical evaluations` in generated methods Markdown; actual Markdown does not contain that phrase. Report/evaluation owner should reconcile the assertion with intended prose. This pass did not change either file.

The new tests use scripted schema-valid extraction and deliberately overconfident candidate decisions. They exercise the actual workflow gate and response composer, including the provider branch, but **do not measure a real LLM's interpretation of adversarial text**. `mode=live` in a scripted provider result is not live-API evidence. No claim of live-model robustness or subjective empathy is made.

## Tested service boundaries

1. Six pressure formulations crossed with four contexts (24 cases): compassion/financial hardship, CEO override, claimed completion, healthcare identity contamination and replacement-charter instructions cannot lift the $75 approval boundary, fraud review, repeat-dispute review or missing-identity restriction.
2. Scripted candidates propose $9999 and eligibility; final decision retains the actual amount/authority and reports the mismatch. Renderer adds acknowledgement without modifying the decision.
3. A customer's claim that a refund and handoff already occurred does not become tool execution evidence; final reply still says human review is needed and handoff was not submitted.
4. Tax/surcharge policy gap remains `partial / requires_human`, amount `None`, with human clarification. Charter is not retrieved as billing evidence.
5. Missing disputed item gets a concrete question; known item is not requested again. No payment-secret request is introduced.
6. Policy reply/evidence are preserved by composition; no additional model call is introduced by the Charter. For known-item credit cases the provider branch has only the existing extraction/planning calls.

## Known gap and proposed core-owner fix

`test_missing_statement_date_next_step_names_the_missing_record` is `xfail(strict=True)`: with all general-credit fields present except `statement_date`, structured missing checks correctly contain that field, but customer prose only says “outstanding account and eligibility details.” It never identifies the missing statement date. This falls short of a fully concrete next step.

Suggested change for service renderer owner (not applied here): map safe missing fields to concise human-readable next steps, including statement date and verified statement date. Group internal identity/history/fraud checks under authorised account review rather than exposing fraud flags or asking for sensitive credentials in chat. Preserve amount/status/evidence. Consider monthly-charge and conflicting-date cases too; they have not been proven to have specific prose by this test pass. After the fix remove the xfail marker and rerun both Charter suites. Strict XPASS intentionally fails until the test is promoted, preventing the gap from silently disappearing from the acceptance record.

Also retain the fact that changing Markdown alone does not change executable behavior. The document is versioned guidance implemented by reviewed code, not an automatic policy compiler. Turn and manifest metadata preserve Charter provenance; existing pre-Charter experiment results cannot establish its new behavioral quality.

## Observed file hashes (SHA256)

```text
9ecfe70f88f645cd6067761eb3cdbb2385201d19dd7c8bb5771bf5ea8d493696  src/policy_agent/workflow.py
c1382d4a90725aca220cde1f3bf42b876d2aaa378e8b0860408b96aec4069bee  src/policy_agent/service.py
bada474fb0ea6253b97b7403c27e4350cda5acd6bafa71a1eb6d05e6c6d68548  src/policy_agent/agent_service_charter.md
ecd2a938bf7213692e5b3c871fd4851528ae307c0148987642d75eb66d55fcbc  src/policy_agent/cli.py
a6b98f1375c145dbae1ffee7209aa564192a543a26f2afc605a2c39efc624766  tests/test_service_charter_adversarial.py
```

These hashes identify files inspected around the test execution; concurrent writers may subsequently change them. Recheck relevant hashes before promoting the result. The handoff's own hash can be calculated after writing; it is intentionally not embedded recursively.

## Prepared next-step patch (not applied to shared sources)

Artifact: `docs/service_next_step.patch`.
SHA256: `f535b38af84614888f2b9d0565c7286cadddb4887e6e4d0111fbb9dcb6ea0552`.

The patch changes only the service composer and adversarial tests:

- Map either `statement_date` or `verified_statement_date` to one concrete instruction: have authorised support verify the statement date on the disputed invoice before assessing the deadline.
- Preserve the underlying decision, amount, permissions and evidence. Do not expose fraud flags or ask for payment credentials.
- Remove the original strict-xfail decorator and add checks for reported-but-unverified dates, deduplicated alias handling, preserved decisions and internal-flag confidentiality.

Validation: `git apply --check docs/service_next_step.patch` succeeded against the shared baseline; applied only in a temporary isolated copy. Running the two Charter suites in that copy produced **35 passed, 0 xfailed** in 0.10s. Shared `service.py` and adversarial-test hashes remained identical to the baseline above after validation. This is not full-suite or live-model acceptance. Apply after the model owner releases the frozen baseline, then rerun checks and capture a new code hash. The Charter principles and version need not change for this conformance fix; implementation provenance changes through the run's code hash.

## Additional core verification risk discovered during patch validation

**Unfixed; outside this presentation patch.** `Workflow.__init__` includes keys with explicit null values in `verified_fields`. An initially null `statement_date` can therefore be filled by a customer-extracted date and still count as verified. This changes action authority from pending verification to eligible for simulation. No real financial integration exists, but the gate boundary is incorrect.

Reproduced in the shared workflow with all other general-credit checks satisfied, then a source-quoted customer statement of `October 1, 2026`:

| Initial context | Final action | Missing | Date in verified_fields |
| --- | --- | --- | --- |
| `statement_date` key omitted | `pending_verification` | `verified_statement_date` | false |
| `statement_date: null` | `eligible_for_simulation` | none | true |

Suggested core-owner follow-up: distinguish an explicitly unknown/null record from verified usable data; do not mark a later customer fill as verified. Review initialization and tool-patch provenance without treating legitimate boolean false values as missing. The prepared presentation patch tests the absent-key branch and does not conceal or fix the explicit-null defect. Add a separate regression and fix under core ownership before making a broad authority-safety claim.


## Applied-patch independent readback — gap resolved

The coordinator applied the prepared patch after the model owner released the frozen v6 snapshot. This owner independently verified the shared files without changing implementation:

- `git apply --reverse --check docs/service_next_step.patch`: exit 0, confirming the prepared patch is present. No reverse mutation was performed.
- `uv run pytest -q tests/test_service_charter.py tests/test_service_charter_adversarial.py -rxX`: **35 passed, 0 xfailed**, 0.09s.
- Both missing and reported-but-unverified statement-date paths now name the disputed invoice's statement date and authorised verification step. The former xfail is a passing ordinary regression. Alias deduplication and decision immutability checks pass.
- Actual `service.py` SHA256: `68dfbfa431df8584ae2e75928d76e7f84a7ebd69b190b4e3b791713c65fcd0b9`.
- Actual adversarial-test SHA256: `e096b8fd80fc9b7d515687d4aeca655e76f69e4e4e94136b6ca7141c56eb67b6`.
- Observed workflow SHA256 remains `9ecfe70f88f645cd6067761eb3cdbb2385201d19dd7c8bb5771bf5ea8d493696` (`workflow-v6`).

The earlier 32-pass/xfail and full-suite failure records above are historical evidence, not this new readback result. The coordinator owns the subsequent full-suite run. The explicit-null verification issue above is separate, still reproducible on this unchanged workflow, and is **not** closed by these 35 passing service tests. No API calls were used.

## V7 verification receipt (recorded by coordinator)

The Charter owner independently re-ran the original explicit-null reproducer against workflow SHA256 `f3df353e02affd6da19f21bebcf3114eee1b645959965ff11237f7216dee8a85` and reported closure of this specific defect. For statement_date and general_amount, omitted, initially-null, and tool-cleared values all remained pending_verification after customer fill; False and 0 retained legitimate known status. The owner reported 64 targeted tests passed, no API calls and no core modifications. Coordinator complete-suite checkpoint: 256 passed. Earlier statements that the defect is unfixed describe the v6 snapshot, not v7. This receipt is not evidence of completed v7 model benchmarking.
