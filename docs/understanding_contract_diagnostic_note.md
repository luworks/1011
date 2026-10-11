# Understanding contract diagnostics and bounded repair proposal

This note uses newly constructed generic synthetic payloads only. No fresh acceptance text, expected answers, or paid model calls were used. The four examples below were executed locally against the current `LiveUnderstanding` and `validate_understanding`; each decoded successfully and then raised its expected contract code. No core code, prompt, tests, or frozen snapshot was changed.

## What can and cannot be concluded

Historical traces with `error="ValueError"` and `understanding=null` do **not** identify which validation branch failed. The rejected response was not retained, and other code paths can also raise `ValueError`. We cannot reconstruct or retrospectively attribute those historical failures to a particular contract condition, provider, or model misunderstanding. A synthetic reproduction establishes that a failure class is possible, not that it caused an old failure.

The current diagnostic patch distinguishes `stage="understanding_contract"` with a fixed code and a content-free projection. It retains enum fields, presence flags, source-index validity, whether quotes occur in the latest message, and whether outcomes are present. It excludes raw fact values, quotes, search text, and requested outcomes. Future counts may use these codes only when recorded; missing historical diagnostics must remain `unknown cause`. Codes identify the first failing check, not necessarily all defects in the response.

## Taxonomy

| Layer | Failure class | Meaning and boundary |
|---|---|---|
| API transport/access | Timeout, connection failure, rate limit, server error, authentication failure | A usable understanding may never arrive. These are provider/transport events, not evidence of a policy refusal or a contract inconsistency. Current call telemetry records exception type/status and retries transient errors, at most twice; authentication is not retried. |
| Provider response completion | Truncated/incomplete, refused, or empty structured response | No complete parseable output. Current adapter records completion/error telemetry and raises `ProviderError`; do not classify this as an understanding-contract code. |
| JSON/schema decoding | Invalid JSON, missing required fields, invalid enum/type, forbidden extra fields | `LiveUnderstanding` cannot be instantiated. The provider adapter already allows one schema-repair request, then reports a provider/structured-output failure. This is distinct from the following cross-field checks. |
| Cross-field contract | `incomplete_field_review` | The review does not contain exactly one entry for each of the six permitted fact fields. Missing or duplicate field entries can trigger it. |
| Cross-field contract | `field_fact_mismatch` | A field is marked stated without a corresponding fact, or a fact exists while the field is marked not stated. This is internal consistency, not proof the fact is true. |
| Cross-field contract | `request_intent_mismatch` | The requested-answer and intent lists differ in length or intent multiset. |
| Cross-field contract | `request_source_support_missing` | A requested-answer quote is blank/not a literal substring of the latest message, or the requested outcome is blank. |
| Semantic extraction/policy | Wrong intent despite matching lists; a real quote that does not entail a fact; incorrect policy proposal | A structurally valid output can still be wrong. These require provenance validation, policy checks, independent case oracles, and semantic review; contract success does not establish answer correctness. |

## Minimal independent reproducer

Run from the project root with `uv run python`. This example contains no customer identity, account facts, or policy answer:

```python
from policy_agent.workflow import FACT_FIELDS, LiveUnderstanding, validate_understanding
from policy_agent.diagnostics import UnderstandingContractError

message = "Please explain the entries on this statement."

def base():
    return {
        "intents": ["bill_explanation"], "facts": [],
        "search_query": "invoice entries",
        "field_review": [
            {"field": field, "presence": "not_stated"} for field in FACT_FIELDS
        ],
        "requested_answers": [{
            "intent": "bill_explanation",
            "quote": "explain the entries on this statement",
            "requested_outcome": "Explain invoice components",
        }],
    }

validate_understanding(LiveUnderstanding.model_validate(base()), message)
for code in (
    "incomplete_field_review", "field_fact_mismatch",
    "request_intent_mismatch", "request_source_support_missing",
):
    data = base()
    if code == "incomplete_field_review":
        data["field_review"].pop()
    elif code == "field_fact_mismatch":
        data["field_review"][0]["presence"] = "stated"
    elif code == "request_intent_mismatch":
        data["intents"].append("taxes")
    else:
        data["requested_answers"][0]["quote"] = "How much will I receive?"
    decoded = LiveUnderstanding.model_validate(data)
    try:
        validate_understanding(decoded, message)
    except UnderstandingContractError as exc:
        assert exc.code == code
        print(code)
    else:
        raise AssertionError("Expected contract rejection")
```

## Proposed repair-once boundary — not implemented here

A future repair may retry a structurally decoded but inconsistent understanding **before** `_merge`, retrieval, policy proposals, or any action. Send the unchanged redacted current message and authorized context, the same schema, and the fixed diagnostic code. Ask the model to rederive a complete understanding from those sources. Do not supply a gold intent, amount, policy choice, or expected case label. Rejected content is untrusted and need not be echoed into logs or the repair prompt.

Use **one shared content-repair allowance per understanding stage**, covering both schema repair and cross-field contract repair. Do not accidentally allow the adapter's existing schema repair plus a second independent contract repair to multiply output-regeneration attempts. Transport retries remain separately bounded and charged. Repair must preserve the exact provider/model/settings and record all attempts, token/cost usage, and full-turn latency. Authentication failures, exhausted budgets, refusals, and incomplete responses do not automatically become semantic-repair requests.

The replacement must pass schema validation, all four cross-field checks, and the normal subsequent provenance/policy checks. Never fill missing fields with invented facts, delete questions merely to align list lengths, reinterpret a quote as trusted verification, or execute a partial rejected response. If repair fails, preserve content-free diagnostics for both attempts, emit the technical-failure response, and stop policy output for that turn. Report initial contract-failure rate and repair recovery rate separately from final answer correctness and full-conversation success.

Before paid evaluation, test this shared-budget behavior with synthetic providers: valid-once, invalid-then-valid, twice-invalid, schema-then-contract failure, timeout, and no state mutation before acceptance. A newly repaired pipeline needs a new prompt/code/metric provenance record and fresh matched evaluation; historical failure causes remain unresolved.
