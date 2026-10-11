# CREAO Design Submission: Reviewer Entry Point

This package delivers two required English documents: a product-layer [design-system-guideline.md](design-system-guideline.md) and a [compliance-audit.md](compliance-audit.md) of real CREAO pages. It also includes a local Next.js enforcement lab ([creao-design-lab](../creao-design-lab/README.md)) that turns the guideline into executable gates (static design checks, Playwright behavior/layout, axe, visual comparison, mutation testing), a [CI workflow](../.github/workflows/creao-design.yml), and the research and validation evidence behind every claim. Required deliverables are in English; process and evidence docs are in Chinese (`*.zh-CN.md`).

> 中文说明：正式交付两份为英文；过程、研究与证据文档为中文 `*.zh-CN.md`，原题见 [task.md](task.md) / [中文翻译](task.zh-CN.md)。

## 5-minute path

1. [design-system-guideline.md](design-system-guideline.md): layout patterns, component/style constraints, and how each rule is enforced.
2. [compliance-audit.md](compliance-audit.md): observed page findings, mapped rules, pre-release checks, and local verification evidence.

## 15-minute path: watch a rule block a violation

From `../creao-design-lab` (Node.js 24, npm; scripts as declared in `package.json`):

```bash
npm ci
npm run check:design      # static design rules on governed source + CSS
npm run build
npx playwright install chromium
PW_SERVER_COMMAND="npm run start -- --hostname 127.0.0.1 --port 3100" npm run test:e2e   # behavior, layout, axe
npm run test:mutations    # optional: mutates an isolated copy, re-runs the same checkers
```

Negative example (see [validation-results.zh-CN.md](validation-results.zh-CN.md)): changing a real button's `aria-pressed` to the invalid value `sometimes` typechecks and builds, but the e2e axe gate fails on `aria-valid-attr-value` (1/1 killed). The first static mutation round also kept an honest survivor (5 killed, 1 survived), and the second round killed 6/6 with both positive controls passing.

Lab contracts: [design.md](../creao-design-lab/design.md), [AGENTS.md](../creao-design-lab/AGENTS.md).

## Deep dive

- Research: [research-findings.zh-CN.md](research-findings.zh-CN.md); raw public sources, site screenshots/DOM, and experiment receipts live in `research/` (site evidence is for local research only, not published).
- Plan and experiments: [implementation-plan.zh-CN.md](implementation-plan.zh-CN.md); [approach.zh-CN.md](approach.zh-CN.md) is early exploration, superseded by the plan and actual results.
- Validation history (first failures, invalid runs, denominators): [validation-results.zh-CN.md](validation-results.zh-CN.md).
- Independent engineer experiments: [engineer-experiment-review.zh-CN.md](engineer-experiment-review.zh-CN.md).
- Design-drift agent: [agents/design-drift-auditor.md](agents/design-drift-auditor.md) (responsibility doc only; no schedule enabled).
- CI: [../.github/workflows/creao-design.yml](../.github/workflows/creao-design.yml) (baseline gates, then mutations, then candidate).
- Handoff and packaging: [CLAUDE-HANDOFF.zh-CN.md](CLAUDE-HANDOFF.zh-CN.md), [delivery-packaging-plan.zh-CN.md](delivery-packaging-plan.zh-CN.md).

## Scope boundaries

- Local lab with synthetic data; it does not fix or deploy anything to the live CREAO product.
- The CI workflow is a config file only: no remote required checks, branch protection, or deployment were enabled.
- Linux visual baselines are not yet reviewed, so the CI visual gate fails closed by design; remote CI is not claimed green.
- The final full mutation run is sealed as partial (9/12 negatives killed, remainder pending), not a 100% detection claim.
