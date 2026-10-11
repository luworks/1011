# CREAO Design Submission: Reviewer Entry Point

The submission has three parts: (1) two required documents, (2) the enforcement implementation that turns the guideline into executable gates, and (3) the evidence behind every claim.

## 1. Required documents

- [design-system-guideline.md](design-system-guideline.md): product-layer layout patterns, component/style constraints, and how each rule is enforced.
- [compliance-audit.md](compliance-audit.md): audit of real CREAO pages with findings, mapped rules, pre-release checks, and verification evidence.

The original brief is [task.md](task.md).

## 2. Enforcement implementation

| Entry point | Purpose |
| --- | --- |
| [creao-design-lab/scripts/check-design.mjs](../creao-design-lab/scripts/check-design.mjs) | Static design checker for governed CSS, JSX, and governance files |
| [creao-design-lab/scripts/mutation-runner.mjs](../creao-design-lab/scripts/mutation-runner.mjs) | Injects deliberate violations into an isolated copy and re-runs the same checkers |
| [creao-design-lab/tests/e2e/](../creao-design-lab/tests/e2e/) | Playwright behavior/layout, axe accessibility, and visual regression gates |
| [creao-design-lab/governance/rules.json](../creao-design-lab/governance/rules.json) | Machine-readable rule registry that links rule IDs to their checks |
| [creao-design-lab/AGENTS.md](../creao-design-lab/AGENTS.md) | Constraints coding agents must follow when changing the UI |
| [creao-design-lab/design.md](../creao-design-lab/design.md) | Design contract of the lab, derived from the guideline |
| [.github/workflows/creao-design.yml](../.github/workflows/creao-design.yml) | Proposed CI gate: baseline checks, then mutations, then candidate |
| [agents/design-drift-auditor.md](agents/design-drift-auditor.md) | Responsibility spec for a design-drift patrol agent (no schedule enabled) |
| [tools/package-delivery.py](tools/package-delivery.py) | Builds and verifies the delivery ZIP from an explicit commit |

### Watch a rule block a violation (about 15 minutes)

From `../creao-design-lab` (Node.js 24, npm; scripts as declared in `package.json`):

```bash
npm ci
npm run check:design      # static design rules on governed source + CSS
npm run build
npx playwright install chromium
PW_SERVER_COMMAND="npm run start -- --hostname 127.0.0.1 --port 3100" npm run test:e2e   # behavior, layout, axe
npm run test:mutations    # optional: mutates an isolated copy, re-runs the same checkers
```

Negative example (see [validation results](validation/validation-results.md)): changing a real button's `aria-pressed` to the invalid value `sometimes` typechecks and builds, but the e2e axe gate fails on `aria-valid-attr-value` (1/1 killed). The first static mutation round kept an honest survivor (5 killed, 1 survived); the second round killed 6/6 with both positive controls passing.

## 3. Evidence

- [validation/validation-results.md](validation/validation-results.md): receipts, first failures, invalid runs, and denominators.
- [validation/engineer-experiment-review.md](validation/engineer-experiment-review.md): independent engineer experiments.
- [research-findings.md](research-findings.md): product exploration and source boundaries; raw screenshots, DOM, public sources, and run receipts live in [research/](research/) (site evidence is for local research only).
- Process history in [process/](process/): [implementation plan](process/implementation-plan.md), [early approach](process/approach.md) (superseded by the plan), [handoff](process/handoff.md), [packaging plan](process/delivery-packaging-plan.md), and [staging notes](process/staging-notes/).

## Layout

```text
exam/
  README.md                    # this entry point
  task.md                      # original brief
  design-system-guideline.md   # required document
  compliance-audit.md          # required document
  research-findings.md         # research synthesis
  agents/                      # design-drift auditor spec
  process/                     # plan, approach, handoff, packaging plan, staging notes, path map
  validation/                  # validation results, engineer experiment review
  research/                    # raw evidence (screenshots, DOM, receipts)
  tools/                       # package-delivery.py
```

## Scope boundaries

- Local lab with synthetic data; it does not fix or deploy anything to the live CREAO product.
- The CI workflow is a config file only: no remote required checks, branch protection, or deployment were enabled.
- Linux visual baselines are not yet reviewed, so the CI visual gate fails closed by design; remote CI is not claimed green.
- The final full mutation run is sealed as partial (9/12 negatives killed, remainder pending), not a 100% detection claim.
