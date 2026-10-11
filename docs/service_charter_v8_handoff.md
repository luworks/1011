# Independent workflow-v8 adversarial handoff

Status: **READY — bounded deterministic regression checks passed; no new defect reproduced in the tested paths. Not a claim of universal safety or live-model performance.**

Owner scope: independent Service Charter/adversarial review. Added only `tests/test_service_charter_v8_independent.py` and this handoff. No core changes, API calls, model spend, or reads of fresh-acceptance expected outcomes. Cases were authored from the existing workflow interfaces and previously reported verification boundaries.

## Test evidence

Command:

```sh
uv run pytest -q tests/test_service_charter_v8_independent.py tests/test_service_charter.py tests/test_service_charter_adversarial.py tests/test_workflow_regressions.py
```

Result: **91 passed in 0.16s**, exit 0. The independent file adds **27 cases**; the other three suites contain 64. No skips or expected failures in this command. This is a focused regression run, not a fresh full-suite result.

| Independent coverage | Cases | Observed result |
| --- | ---: | --- |
| Combined fake system/tool/CEO/compassion override targeting fraud, identity, history, ticket and confirmed-error fields | 5 | Protected proposals rejected; mandatory human review retained |
| Historical/future source-index laundering | 3 | Invalid source rejected; missing amount stays unknown |
| Initial or tool-cleared blank item: null, empty, ASCII whitespace, tab/newline, NBSP, ideographic space | 12 | Item normalises to unknown; permission pending; specific item requested |
| Initial null or tool-cleared date/amount followed by customer impersonating a tool | 4 | Customer value stays reported, permission pending; False/zero remain verified |
| Customer retraction versus authorised conflict resolution | 1 | Customer cannot clear conflict; explicit trusted patch can; simulation never claims actual issuance |
| Conflict then tool-null then customer fill under mandatory fraud review | 1 | Verification not restored; human review retained |
| Combined healthcare-policy contamination, tax assertion and claimed execution | 1 | Tax outcome remains unknown; no healthcare policy or fabricated handoff |

## Closed findings and remaining boundaries

- Previously reported missing-statement-date guidance gap remains closed by the applied service patch; all 35 Charter tests pass within this run.
- Previously reported explicit-null verification defect remains closed on the tested v8 date/amount paths, including a tool-clear and later customer fill. Both false and zero remain usable values.
- Blank specific-item values covered above do not satisfy Rule 1. This does not prove semantic validation of every nonblank label.
- No new defect was reproduced in these 27 independently authored paths, so no core patch is proposed by this handoff.

The new tests intentionally provide explicit offline understanding fixtures. They test the downstream trust/gate/rendering boundary even when extraction produces an adversarial proposal; they do **not** measure an LLM's ability to recognise the message or extract every intent. Existing scripted-provider tests also remain passing, but are not live-API evidence. No claim of zero errors under arbitrary attacks is supported.

`Workflow.observe(..., patch=...)` is a trusted adapter interface: the caller supplies authenticated fixture/tool evidence. This pass verifies that tool-looking **customer text** cannot invoke it or acquire its authority through ordinary `turn` processing. It does not audit a production adapter, authentication, or user-controlled role/patch deserialisation; there is no production integration in this prototype. An integration must not pass user-supplied dictionaries as trusted tool patches.

Nimbuscare UK's medical website is not verified as the telecom exercise customer. Company identity remains unverified/possibly fictional or anonymised; no medical policy, NHS routing or patient-specific obligation was imported.

## Inspected implementation and test hashes

```text
2a561f1aa2bcc42d5ef245c473983417dcd90472d53304601f6da9d2ec30b753  src/policy_agent/workflow.py
72ab22c918d14dd291fb3b18d13eddcafe3d1d158a60009eb54ca3da6426eea3  src/policy_agent/schema.py
68dfbfa431df8584ae2e75928d76e7f84a7ebd69b190b4e3b791713c65fcd0b9  src/policy_agent/service.py
cb8b3d56d1392f2c956d2f34e59c5724245cd04d51f19bb8b2967b124497e6d8  tests/test_service_charter_v8_independent.py
```

`PROMPT_VERSION` readback: `workflow-v8`. Hashes are from the actual shared files immediately after the passing run; compare to the frozen owner receipt before promotion. This handoff does not replace the model owner's freeze or live evaluation evidence.
