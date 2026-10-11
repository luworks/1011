# CREAO Design Lab

A local Next.js experiment that wires product design guidelines into engineering checks. The prototype is built from CREAO's public Widgets documentation, observed product pages and style variables; it uses synthetic data, connects to no real business system, and does not impersonate CREAO private code.

## Reading order

1. [Implementation plan](../exam/process/implementation-plan.md): goals, parallel work split, acceptance and boundaries.
2. [design.md](design.md): page patterns, CSS index, rules and sources.
3. [AGENTS.md](AGENTS.md): working contract for coding agents.
4. [Rule registry](governance/rules.json): check scope, entry points and limitations.
5. [Independent engineer experiment protocol](experiments/engineer-protocol.md): behavioral experiment kept separate from the preset mutations.

## Running

Environment: Node.js 24, npm. Dependencies are pinned by `package-lock.json`. First run:

```bash
npm ci
npm run dev
```

Open `http://localhost:3100` in a browser. The app contains `/files`, `/connectors`, `/agents` and `/guidelines`. Prototype state is for local demonstration only; whether it survives a refresh depends on the implementation notes. The guidelines page is a reading entry point; the actual constraints are implemented by the CSS, components and check code of the same version.

## Verification interface

The scripts in `package.json` are authoritative:

```bash
npm run typecheck
npm run lint
npm run test:design
npm run check:design
npm run build
npx playwright install chromium
PW_SERVER_COMMAND="npm run start -- --hostname 127.0.0.1 --port 3100" npm run test:e2e
npm run test:mutations
```

Static design checks validate governed source and CSS. Browser checks validate the actual DOM, interactions and layout. Mutations change the real implementation in a temporary copy and then run the existing checkers; they never modify the shared baseline. A `killed` result must be a hit on the target rule; compile failures, timeouts and execution-infrastructure errors are counted separately. Positive cases measure false positives. Actual commands, first failures, reruns and denominators are in [Validation results](../exam/validation/validation-results.md). Fixed design mutations, the added axe/visual negative cases and the independent engineer experiment are counted separately.

## CI and release boundary

The [GitHub Actions workflow](../.github/workflows/creao-design.yml) uses the same commands: it runs the baseline gate first, then mutations, and finally prepares the candidate package. It is currently only a local configuration file; creating it did not enable any remote protection or deployment.

A real integration needs a repository administrator to:

- Make the baseline gate and mutation job required checks on protected branches, with an explicit trusted workflow source.
- Assign real CODEOWNERS to the guidelines, tokens, component primitives, rules, tests and workflow; require approvals and restrict self-approval and direct bypass.
- Bind releases to the same commit/build artifact that passed the checks; run a smoke check on affected pages after deployment.
- Protect the evidence and baseline-update process. Visual snapshots must not be bulk-updated by the author without explanation; exceptions need a scope, an owner and an expiry date.

These are repository settings and permission questions that cannot be guaranteed by `AGENTS.md`, a YAML file, or a hash file editable inside the project. This experiment does not configure remote permissions or deployments on the user's behalf.

## How to read the results

An executable design contract supports three kinds of conclusions:

| Conclusion | Required evidence |
| --- | --- |
| This implementation complies with the covered rules | Static and browser checks pass on a fixed candidate; visuals and behavior confirmed by a human |
| The checker detects a class of violation | Valid baseline + a compiling implementation mutation + the corresponding rule fails |
| No engineer can bypass it | Not provable by this experiment; needs permission boundaries, broader coverage and ongoing governance |

Document consistency checks can only confirm IDs, paths and formats; they cannot fully prove that the natural language and the code are semantically equivalent. Static rules also cannot exhaust every possible JavaScript/CSS spelling. Browser verification covers only the recorded pages, states and viewports. Reports must retain survivors, invalid cases, errors, untested items and human judgments.

## Enhanced gates and state catalog

- The [page-state catalog](governance/page-states.json) enumerates routes, states, viewports, checks and measured evidence; loading/error/permission states that do not exist are explicitly marked as not implemented.
- `npm run test:e2e` runs behavior/layout and axe checks by default; `npm run test:a11y` runs axe on its own. Violations and incomplete results (which need manual review) are recorded separately; zero automated violations is not full WCAG compliance.
- `npm run test:visual` compares reviewed screenshots independently and forbids snapshot updates by default. `VISUAL_ENV` must equal the real OS/architecture/kernel/browser-version namespace. The currently reviewed environment is `darwin-arm64-25.6.0-chromium-154.0.8037.98`; real font evidence is in the acceptance attachments.

Local reproduction (with system Chrome installed and an exactly matching environment):

```bash
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
PW_CHANNEL=chrome VISUAL_ENV=darwin-arm64-25.6.0-chromium-154.0.8037.98 PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
PW_CHANNEL=chrome npm run test:mutations
```

Other environments fail when the identity does not match or the corresponding baseline is missing. A Linux visual baseline for CI still has to be generated as a candidate in the chosen environment, reviewed by a human and committed; the existing workflow does not skip the visual gate, so remote CI cannot be claimed to be fully green. When a legitimate new feature changes pixels, first keep the expected/actual/diff, have an independent reviewer explain the change and approve the baseline update, then rerun in normal mode; the command that generates a baseline never counts as a pass.

The [full implementation and tooling plan](../exam/process/implementation-plan.md), the [delivery packaging plan](../exam/process/delivery-packaging-plan.md) and the [design drift auditor role](../exam/agents/design-drift-auditor.md) provide the follow-up integration contract. The auditor agent is currently delivered as a role document only; no daily schedule or external notification is enabled.

## Known engineering limitations

Automated checks cover only the registered syntax, routes and states. The React Doctor baseline scan reports 0 errors / 6 performance suggestions; the 0-file scan score seen in the experiment copy is not valid evidence. The dependency audit reports 0 findings for production dependencies; the development lint dependency chain has 5 high advisories propagated from the same braces advisory. It is not on the current product request path, but upstream fixes still need tracking and it must not be reported as fixed. Details and raw JSON are in the validation results index.
