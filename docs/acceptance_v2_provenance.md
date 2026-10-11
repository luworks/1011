# Acceptance suite v2 provenance

This is a fresh 16-scenario frozen acceptance collection for the revised workflow. It replaces the previously exposed 16-scenario collection for the next acceptance run; historical results remain historical evidence. It is not a new or hypothetical business policy.

- Source: `exam/Nimbus Wireless — Billing Dispute & Refund Policy.md`, BIL-POL-014 v6.2, Rules 1–5; accompanying ten-article Nimbus KB, particularly KB-1001 through KB-1007.
- Fixture: `fixtures/acceptance_v2.json`.
- File SHA256: `8ce8f6933fdd541ccac32cb21158f41c6ab55250d4767d74e27cd567a70cbad8`.
- Canonical oracle manifest SHA256: `ad81db9c1937f8276accab3cc84e34de55e74ea9004eb6aa1cf4626242356fda`.
- All 16 scenarios are marked `frozen`; 19 customer turns in total. Three complete repetitions mean 48 conversation executions, not 48 independent scenarios.

## Authoring boundary

The author derived new messages, account values, time ranges and expected outcomes from the supplied policy, without consulting current live outputs or model scores. Existing schema, scorer and policy implementation interfaces were inspected for fixture compatibility and status vocabulary; expected amounts and date intervals were calculated manually from source rules. Neither the policy engine nor an LLM was executed against these cases during authoring. No old scenario inputs were changed.

Each scenario uses a distinct fictional customer and a stable explicit simulated account record. The questions state the relevant dispute or outage topic rather than relying on an unexplained phrase such as “process it.” Multi-turn verification changes are carried by explicit simulated backend `context` updates. Customer text cannot itself create trusted NOC, fraud or dispute-history verification.

Standard answers and explanatory derivations appear only under `expected`, which the evaluation runner removes before passing a scenario to the workflow. They are not included in customer messages or trusted account facts. Per-turn required intents, allowed relevant adjunct intents, amounts, policy IDs and answer/action statuses were declared before evaluation. No model outputs were used to adjust these standards.

## Coverage and conventions

The set covers recurring account totals without multiplying by line count, full elapsed-day calculations including sub-day eligible outages, amount and duration escalation independently, absent/unverifiable/unqueried tickets, an address mismatch, cumulative goodwill, global repeat-dispute/fraud requirements, unknown account checks, distinct restoration/invoice deadlines, supported credit plus unsupported tax questions, customer fact conflicts, and subsequent verified corrections without future-information leakage.

Where the source specifies a business rule, the oracle cites that rule. Unknown facts and unresolved customer/backend conflicts block action as prototype trust constraints, not invented Nimbus business policy. Whole days use elapsed 24-hour periods; amounts are hand-calculated in cents. These conventions are the previously declared implementation assumptions, not newly claimed policy wording.

The scorer checks `questions`, per-turn `questions`, `allowed_intents`, amount/status/policy expectations, required text and its general invariants. `manual_basis` documents source reasoning. `manual_condition_checks` records additional condition-level expectations for independent review; the current scorer does **not** automatically score those annotations. Deadline cases additionally assert the explicit 30/60-day policy periods and late-day wording where appropriate. Broader prose semantics still require independent audit.

## Freeze and use

Before paid evaluation, pin the fixture hash together with code, prompt, corpus and model configuration hashes. Use the complete 16-scenario suite with three repetitions per selected configuration. Report incomplete runs against the full planned denominator. Do not feed oracle metadata to the model.

The fresh set has not been run during authoring. If its outcomes are subsequently used to tune the workflow, it becomes regression evidence and a new independent holdout is needed. It covers one supplied policy family; no claim of automatically supporting arbitrary policy documents is established by passing it.

Validation performed: JSON and account-schema validation; 16 unique IDs; complete per-customer-turn oracle coverage; allowed-intent consistency; oracle removal by `model_input`; independent calendar-day arithmetic checks. No API requests and no policy-engine execution.
