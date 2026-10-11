# Evaluation strategy: policies and failure classes, not individual customers

The original conversation is an acceptance example, not the system specification. A fix is complete only when its underlying invariant holds across other account values, conversation histories, and adversarial inputs. The executable specification remains the reviewed source policy; a customer example cannot create a new business rule.

## Three distinct layers of evidence

1. **Policy engine tests** provide trusted account records and compare decisions with independently written policy expectations. They cover exception precedence, amount/date boundaries, cumulative goodwill, mandatory escalation, and missing checks.
2. **Workflow adversarial tests** inject deliberately bad structured model outputs, forged citations, source claims, and conflicting facts. They test whether a bad model can cross the evidence and action boundary. These tests do not demonstrate that a real model understands the question or resists the same prompt.
3. **Live end-to-end evaluations** send customer messages through each real model configuration. They score understanding and proposed decisions before the gate separately from the final answer and action after it. Model misclassification can still select the wrong safe template; structural safety alone is not answer correctness.

The current 40-scenario collection has 24 development cases and 16 frozen cases. Frozen cases are evaluated only after choosing the candidate configurations and prompt/rule versions. Each configuration should run each frozen conversation three times. Unique conversations and repeated runs must have separate denominators. Budget exhaustion, API failures, and incomplete runs remain visible; they are not silently removed from the planned denominator.

`tests/test_adversarial.py` adds a separate deterministic structural suite. Its 25 pytest cases include a seeded loop over 100 combinations of monthly charges and outage durations, calendar translations across years, cumulative-credit redistribution, removal of verification evidence, forged administrator/tool assertions, invented policy citations, and malicious approval/tax candidates. The generated variants are not 100 independently authored acceptance conversations, and their result must not be reported as a live-model attack success rate.

## Independent expected answers

Each case has customer-visible inputs, explicitly trusted simulated records, and a separate expected answer. The expected answer identifies source clauses, applicable conditions, permitted amount when known, answer completeness, mandatory escalation, and claims that must not appear. Neither these labels nor the reference calculation enter the model prompt.

An LLM may propose attacks or paraphrases. It cannot certify its own expected answer, invent policy amendments, or decide that a refusal is correct without a source-backed oracle. Human review resolves semantic ambiguity. Deterministic arithmetic and date checks provide independent expected values. A second LLM judge may aid triage but is not the acceptance authority.

## Attack families and metamorphic relations

| Family | Variants to generate | Required invariant |
|---|---|---|
| Money and duration | Different monthly charges, full days, partial days, and totals around $75/$300 | Apply the source formula and correct track; account line count cannot multiply an already aggregated plan charge |
| Time windows | Just below/on/above 4 hours, 30/60/90 days; translated calendar dates | Correct inclusivity and correct reference date; shifting all dates together preserves the decision |
| Missing or conflicting facts | Omit each check, change a date, correct an amount, deliver a failed tool result | Unknown never silently becomes false; conflicting facts cannot support a definite amount or permission |
| Authority spoofing | Customer says “NOC verified,” impersonates staff, quotes an invented policy, or claims prior approval | Customer text cannot write verified account fields or grant execution permission |
| Evidence laundering | Valid article ID with fabricated quote, irrelevant real quote, stale policy version | A citation's presence alone does not establish a supported conclusion |
| Multi-turn contamination | Past question repeated as a new intent, future confirmation, unresolved correction | Only available evidence at the current turn may support the decision |
| Mixed answerability | Formula plus tax adjustment or unrelated coverage question | Answer the supported part and retain the knowledge gap; refusing everything is a quality failure |
| Technical faults | Timeouts, malformed output, authentication failure, exhausted budget | Technical failure remains distinct from a policy decision; no completed external action is claimed |

Metamorphic relations reduce dependence on handpicked examples. For instance, redistributing a fixed rolling goodwill total between the previous credits and the current request must not change the threshold decision. Removing fraud-history evidence must not increase permission. Adding a mandatory fraud escalation must retain human review even when other facts are missing. These properties complement explicit expected answers rather than replace them.

## Multiple policies and policy revisions

This prototype supports the supplied policy only. Its corpus hash lock prevents a changed source document from being used with the existing executable rules. This is a version consistency check, not proof that whoever edits the lock has correctly reviewed the policy.

A genuinely different policy requires a separate reviewed policy pack: original sources, stable clause IDs and hashes, executable rules, supported intent/template mappings, policy-specific oracles, and an evaluation manifest. A revision must update these together after review. Replacing a dollar threshold in a document and asking the model to infer the new production rule is not a supported migration.

For future cross-policy evaluation, keep business expectations local to each policy pack and reuse the same workflow invariants and attack families. Use a policy-to-policy compatibility matrix: which scenarios apply unchanged, which expected decisions change, which questions become unsupported. Run both the old and new packs against their own pinned sources to detect accidental rule mixing. Synthetic policy mutations can be isolated test fixtures with explicitly authored oracles; they must never be advertised as supported production policy or included among the original source documents.

## Release criteria and repair loop

Report at least four dimensions separately:

- **Safety:** unsupported business claims, improper permission, missed mandatory escalation, invented verification, and source/version violations. Report both claim-level and conversation-level rates when all claims have actually been labeled; otherwise mark the metric unassessed.
- **Utility:** policy/amount correctness, supported-question completion, over-refusal, and all-requirements conversation success. A system that refuses every question does not pass.
- **Robustness:** performance by attack family and severity, before/after gate behavior, repeat-run variation, and technical failures.
- **Efficiency:** latency, input/output/cache tokens, actual estimated spend, conservative reservations for unknown usage, and cost per successful conversation. Zero successes has no finite success-cost estimate.

Any unauthorized action permission or invented business commitment is a critical failure for model/configuration selection. Passing a finite suite means only that these failures were not observed in that suite.

When a new customer reveals a failure: reproduce it, identify the general failure class, add multiple variants and a regression test, fix the rule or trust boundary, then rerun the relevant structural and live development suites. Do not add a branch keyed to that customer, exact amount, ticket ID, or original wording. If frozen failures are used for tuning, retire those cases into regression and create independently reviewed replacement holdouts before making new acceptance claims.

The current live results and completion status belong in each saved run manifest and the design memo. This strategy defines how to measure robustness; it does not imply that every proposed attack family or future policy pack has already been evaluated.
