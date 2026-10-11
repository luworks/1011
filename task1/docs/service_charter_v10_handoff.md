# Independent v10 Charter and scope handoff

Status: **READY for bounded regression review; 12 new tests passed. Residual extraction-omission limitation reproduced separately. Not unconditional completeness or live-model acceptance.**

Only added `tests/test_service_charter_v10_independent.py` and this handoff (earlier preparation in `service_charter_v10_test_plan.md`). No core edits, APIs, paid runs, fresh-holdout inputs or expected-result reads. Implementation was still being finalised by root; compare hashes to the final freeze receipt before promoting this evidence.

## Actual validation

- New independent suite: `uv run pytest -q tests/test_service_charter_v10_independent.py`: **12 passed** (0.14s).
- Combined Charter suites: `uv run pytest -q tests/test_service_charter_v10_independent.py tests/test_service_charter.py tests/test_service_charter_adversarial.py tests/test_service_charter_v8_independent.py`: **74 passed** (0.38s), exit 0, no skips/xfails.
- These are focused checks, not a new full-suite result or new-policy live acceptance. Tested `Corpus()` version: `dbb59ca9a429ab22142b76f32c0704dc3477c5e7ff0a33289efc12d700a05a5f`.

## Independent findings

1. An uncertain general-credit outcome can coexist with explicit tax adjustment, outage deadline and invoice dispute deadline. All four appear; only the uncertain part requests clarification. The 30-day/60-day answers retain their respective policies.
2. Uncertain credit under known fraud OR repeat-dispute review retains `requires_human`, Tier 2 text and no executed-handoff claim, while invoice-component information remains answerable. This independently verifies root's late mandatory-review guard.
3. An unresolved item alias asks whether it refers to the existing item without losing the independently requested tax answer or overwriting the trusted item.
4. A tax-only follow-up drops a background credit outcome; an explicit request to repeat the amount preserves both credit and tax. These are scripted correct classifications, not evidence that a real reviewer always classifies them correctly.
5. A correction from outage deadline to statement-dispute deadline yields the current 60-day answer only. Corrected conflicting account amount blocks a monetary conclusion but preserves an independent invoice-components answer.
6. Timeout at extraction, scope review or candidate generation produces a distinct technical error, empty decisions and retry/human-assistance guidance. It neither invents a transfer nor leaks simulated SDK details. No stage is retried by the workflow on these timeout fixtures.
7. Repeated invalid scope source quotes exhaust the shared content-repair allowance after two scope calls (initial plus one repair), never reach planning, and produce a truthful technical-failure response.

## Residual omission limitation — minimal reproduction

Input: `Will taxes change, and how long after restoration can I request credit?`

Scripted extraction omits `outage_deadline` and proposes only `taxes`; scripted ScopeReview correctly confirms its sole proposed intent as explicit. Observed result: `error=None`, decisions `['taxes']`; calls `LiveUnderstanding`, `ScopeReview`, `EvidenceBoundCandidate`. The second question receives no answer or clarification.

Reproduce using the committed independent fixture helpers:

```python
import runpy
from policy_agent.corpus import Corpus
from policy_agent.workflow import Workflow
n = runpy.run_path('tests/test_service_charter_v10_independent.py')
p = n['ScriptedScopeProvider']([n['spec'](taxes='explicit')])
r = Workflow(Corpus(), p, n['account']()).turn(
    'Will taxes change, and how long after restoration can I request credit?')
print(r['error'], [d['question'] for d in r['decisions']])
# None ['taxes']
```

Root cause/contract boundary: `validate_scope` requires the reviewed intent set to equal the proposed extraction set. ScopeReview classifies that set and cannot add an omitted outcome. A future completeness guarantee would need an independently inventoried outcome set with reconciliation, not just per-proposal classification. This is an injected upstream semantic failure, not proof that a real model missed this sentence. It is also not repaired by the new response composer. It remains a limitation if scope is intended only to remove over-included questions; it is a functional gap if the requirement promises to recover extraction omissions. Root should make that acceptance scope explicit.

Likewise, quote checks establish literal support, not the semantic correctness of every background/explicit classification. Do not label 74 deterministic passes as a measured zero-omission rate. The originally planned v10 design cases are not all independent passing cases: semantic reviewer misclassification remains a limitation rather than a fabricated deterministic oracle.

## Version evidence

```text
workflow-v10
 d6970f29d545ef28d50ba9573e35ca716517f28a3743c6b02ce99dc045bd3709  src/policy_agent/workflow.py
 72ab22c918d14dd291fb3b18d13eddcafe3d1d158a60009eb54ca3da6426eea3  src/policy_agent/schema.py
 68dfbfa431df8584ae2e75928d76e7f84a7ebd69b190b4e3b791713c65fcd0b9  src/policy_agent/service.py
 02ec7359038a0d0a309dbf0c50e0354df332c4e829116724451ec474b2b4c219  tests/test_service_charter_v10_independent.py
```

Charter remains team-proposed and not official customer values. Nimbuscare UK's healthcare identity/policies are not imported into the wireless exercise. No extra leader agent was introduced by this pass.
