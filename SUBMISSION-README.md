# CREAO Product Design Guidelines — Submission

Task: *Design and Enforce CREAO's Product Design Guidelines* (brief: [`exam/task.md`](exam/task.md)).

## What is submitted

| Item | Form | Purpose |
| --- | --- | --- |
| `design-system-guideline.md` | Standalone Markdown (also at `exam/design-system-guideline.md`) | The rules: canonical screen patterns with skeletons, chat-workbench composition, product-level and component-consistency rules with exact failure conditions, the enforcement mechanism, exceptions, a worked feature example and an agent/PR checklist |
| `compliance-audit.md` | Standalone Markdown (also at `exam/compliance-audit.md`) | The proof: ten findings on the live CREAO product (AUD-01..AUD-10), the rule each one breaks, and the exact pre-ship check that would catch it, plus local validation receipts |
| `creao-design-submission.zip` | This repository | The working enforcement implementation, tests, CI, research evidence and full process history |

All paths in this file and in the two documents' "Companion package" sections are relative to the ZIP root.

## Five-minute reading path

1. `exam/design-system-guideline.md` — read "Decision", "At a glance", "Canonical screen patterns" and "Agent / PR checklist".
2. `exam/compliance-audit.md` — read "Findings at a glance", then any one finding end to end.

## Fifteen-minute verification path

Requires Node 24. Port 3100 must be free.

```sh
cd creao-design-lab
npm ci
npm run check:design          # static gate: tokens, primitives, governance registry
npm run test:design           # unit tests for the static checker
npm run build
npx playwright install chromium
npm run test:e2e              # browser gate: layout, names, recovery, consistency, axe
```

To watch a rule block a violation, run `npm run mutation:static`: it copies the lab into isolated candidates, injects real violations (literal colors, raw `<button>`, aliased native controls, expired exceptions) and reports killed / survived / invalid / error separately.

## Repository map

```text
SUBMISSION-README.md            this file
.github/workflows/
  creao-design.yml              CI: static gate, browser gate, fail-closed visual gate
creao-design-lab/               enforcement implementation (Next.js lab with synthetic data)
  AGENTS.md                     instructions a coding agent loads before changing UI
  design.md                     executable index: every rule ID -> checker/test/token file
  governance/
    rules.json                  machine-readable rule registry (validated by GOV-001)
    exceptions.json             scoped, expiring exception records
    page-states.json            route/state coverage inventory, including known gaps
    human-exceptions-policy.md  human override and CI acceptance policy
  scripts/
    check-design.mjs            static checker: CSS value AST (DS-001), TSX AST (DS-002), registry (GOV-001)
    mutation-runner.mjs         isolated mutation testing of the gates
  src/
    styles/                     tokens.css (observed CREAO palette), components.css, layouts.css
    components/                 approved primitives (ui/) and screen patterns (patterns/)
    app/                        Files, Connectors, Agents, Guidelines routes built from the patterns
    lib/copy.ts                 single source for navigation/destination labels (NAV-001)
  tests/
    design/                     checker unit tests
    e2e/design.spec.ts          browser rules: LAY, A11Y-001, STATE, NAV, RESP, CMP
    e2e/accessibility.spec.ts   axe scans across route/state/viewport fixtures (A11Y-002)
    e2e/visual.spec.ts          reviewed visual baselines (VISUAL-001)
    mutations/cases.mjs         negative and positive mutation candidates
  experiments/                  engineer-agent protocol, mutation matrix and raw run records
exam/
  task.md                       original brief
  design-system-guideline.md    required deliverable 1
  compliance-audit.md           required deliverable 2
  README.md                     reviewer index for exam/
  agents/design-drift-auditor.md  role spec for a daily design-drift review agent
  process/                      approach, implementation plan, packaging plan, handoff
  validation/                   validation results, independent engineer experiment review
  research/                     live-product screenshots, DOM/AX captures, public docs, run receipts
  tools/package-delivery.py     builds and verifies the submission archive
```

## How the work was done

1. **Research.** Explored the live product (chat, agents, files, connectors, skills, video studio, widgets) at desktop and 390px, captured screenshots plus DOM/accessibility trees, and read CREAO's public Widgets documentation to recover the existing tokens and components. Live captures were taken with the zh-CN locale; documents quote UI strings by English meaning, and the raw captures keep the original text.
2. **Rules.** Wrote the product-layer guideline on top of the existing system: six canonical screen patterns, layout skeletons, chat-workbench rules, and rule families for tokens, primitives, page identity, accessible names, state recovery, navigation copy, responsive integrity, component consistency and governance.
3. **Enforcement.** Built a local lab that composes the observed tokens through an approved-primitive boundary, then made every objective rule a gate: AST-based static checks, Playwright behaviour/geometry/consistency checks, axe scans and reviewed visual baselines, wired into CI and loaded by coding agents through `AGENTS.md`.
4. **Audit.** Applied the rules to the live screens and mapped each finding to the check that would have blocked it.
5. **Proving the gate.** Ran mutation testing (the first round let an aliased native button survive; the checker was fixed and the survivor kept on record), negative controls for axe, visual and consistency rules, and two independent engineer agents implementing a feature under the same gates. Failures, invalid runs and survivors are retained, not overwritten.

## Scope boundaries

- The lab uses synthetic data and a local component adapter; it does not replace CREAO's private component library.
- Nothing was deployed to CREAO; the live defects are documented, not fixed.
- CI configuration is included but has not run on a protected remote branch. The Linux visual baseline intentionally fails closed until a human reviews it.
- Exact pass/fail counts per run are in `exam/validation/validation-results.md` and `exam/research/validation/`.
