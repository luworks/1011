# CREAO Executable Design Guideline: Implementation and Validation Plan

Date: 2026-10-11. Status: local implementation and enhanced gates are complete, and the final experiments and delivery package are being closed out; detailed status follows the actual receipts in validation-results.md. Scope: local research, an independent Next.js prototype, the guideline, checkers, mutation experiments, and CI configuration; the live CREAO product is not modified, and nothing is deployed or pushed.

## Goals and Acceptance

Turn existing evidence into a runnable closed loop: `design.md → CSS / components / pages → static checks + browser checks → compliant and violating change experiments → CI gate`. Markdown is the entry point for humans and coding agents; the rule registry and check code enforce the automatable parts. It must not be claimed that Markdown by itself can constrain arbitrary implementations.

Completion criteria:

1. `design.md` labels each guideline value as official documentation, live observation, or a proposal of this prototype; it indexes the actual CSS, components, rule IDs, and check entry points.
2. The independent Next.js project starts and builds successfully; the minimal Files, Connectors, and Agents flows are operable and can be checked on desktop and narrow screens.
3. The compliant baseline passes lint, types, design rules, build, and browser verification of affected paths.
4. Violating code changes actually act on the implementation in an isolated copy and are identified by the same checker as the baseline; the hit rule is recorded. Checking only an `isViolation` flag or a preset return value is not acceptable.
5. At least two reasonable guideline-following changes pass, and at least six independent violation categories are tested for acceptance. Report killed / survived / invalid / error with accurate denominators; timeouts or compile failures cannot count as successful design-rule blocks.
6. Keep the simulated engineers' tasks, changes, results, and limitations; the fixed mutation set and the independent engineer experiment are reported separately.
7. The CI configuration uses the same commands and can upload failure evidence; it declares that repository branch protection and remote execution are not yet enabled, and local passes are not equated with successful deployment.

## The Two Required Task Deliverables

These two Markdown files are the core of the final delivery. The prototype and engineering attachments provide reproducible evidence for them and cannot replace them.

| Required file | Must contain | Acceptance criteria | Current status |
| --- | --- | --- | --- |
| [design-system-guideline.md](../design-system-guideline.md) | Product-level layout patterns, usage boundaries of the existing design system, rule IDs, execution steps for engineers/agents, concrete check entry points, exceptions, and release gates | A reader can choose a layout, find the CSS/components, run the checks, and understand failures without asking follow-up questions; every automated rule maps to an actual implementation, and manual rules are clearly labeled | Finalized, including enhanced gates and execution scope |
| `compliance-audit.md` | Apply the guideline to the real pages explored; for each finding record page/state/viewport, screenshot and DOM evidence, violated rule, impact, fix, and which pre-release check would catch it | Every finding has evidence and a rule ID; real live observations, prototype reproductions, and not-yet-covered items are distinguished; actual commands, failure results, and experiment receipts are cited; it must not fabricate having run checks on CREAO's private source | Real audit written; final experiment receipts being closed out |

The original task statement is kept in [task.md](../task.md). Research, plans, and experiments are supplementary material and are not mixed into the original task text.

## Engineering Deliverables and Evidence Checklist

All of the following are within the scope of this implementation. Paths are relative to the repository root; "Written" only means the file exists, not that it has passed acceptance.

| Deliverable | Artifact location | What must be verified | Current status |
| --- | --- | --- | --- |
| Executable design entry point | `creao-design-lab/design.md`, `AGENTS.md` | Official/observed/proposed sources kept separate; real CSS, components, rules, and execution commands indexed; agents must not delete checks to pass | Written |
| Three-layer CSS and components | `src/styles/tokens.css`, `components.css`, `layouts.css`, `src/components/{ui,patterns}/` | Color mappings have sources; layout/responsive and components are layered; governed styles add no raw colors or unknown variables | Passed static/type/build and browser checks |
| Next.js prototype | `creao-design-lab/src/app/`, `package.json`, `package-lock.json` | Files/Connectors/Agents actually operable; Guidelines renders Markdown, and the controlled source viewer can open CSS; dev start and production build pass | Implemented and built |
| CSS/JSX design lint | `scripts/check-design.mjs`, `tests/design/` | CSS AST checks raw colors/unknown tokens; TS AST checks bypassed controls; verifies valid and violating examples, and accurately discloses alias/dynamic-pattern boundaries | 13 unit checks passed |
| General lint and types | `eslint.config.*`, `tsconfig.json`, package scripts | `npm run lint`, `npm run typecheck` pass; reported separately from the design lint | In progress |
| Rule and exception governance | `governance/rules.json`, `exceptions.json` | IDs, entry points, and doc links valid; exceptions precisely scoped to file and rule, with reason/owner/deadline; expired ones fail | Implemented |
| Browser checks | `tests/e2e/design.spec.ts`, `playwright.config.ts` | Desktop and narrow-screen headings, names, operable recovery, destinations, field label/value correspondence and geometry; CI runs against the production build | 38 behavior/axe checks passed; visual baseline 3/3 passed |
| Live-site screenshots and observations | `exam/research/screenshots/`, `deep/`, DOM/AX snapshots and capture manifest | Source URL, time, viewport, and state can be located; screenshots manually reviewed to avoid mistaking loading states/AX mappings for real defects | Captured and reviewed |
| Prototype screenshots and visual acceptance | `exam/research/prototype/` (planned location) and browser failure screenshots/traces | Desktop, 390px, key interactions/empty states; additional checks at narrow and intermediate widths; manual screenshot checks kept separate from automated assertions | Done, including 800px before/after-fix evidence |
| Fixed mutation experiment | `scripts/mutation-runner.mjs`, `tests/mutations/`, `reports/` | Actually modifies the isolated implementation; positives prove no over-blocking; negatives hit actual rules; keep killed/survived/invalid/error and the initial miss | Static re-check 6/6; final enhanced "all" run in progress |
| Independent engineer compliance experiment | `experiments/engineer-protocol.md`, isolated copies, patches, and acceptance receipts | Two subagents build the same new feature, one compliant and one taking shortcuts; check assets unchanged; feature and guideline verified separately; preset mutations must not pass as the independent experiment | v1 complete; enhanced v2 implemented and under acceptance |
| CI and candidate artifact contract | `.github/workflows/creao-design.yml` | Lockfile install, lint/types/unit tests/design check, build, browser, mutation; failure evidence uploaded; a source version receipt is produced only if the gate passes | YAML written; not executed remotely |
| Run instructions and results | `creao-design-lab/README.md`, `exam/compliance-audit.md` | Copyable commands, versions, actual pass/fail counts, report index, unverified paths; local success is not written as successful live deployment | To be backfilled at the end |

`reports/` is a run-generated directory, not a source dependency that must exist before the first run. The final audit must keep readable experiment summaries and location info; it must not leave only ignored temporary reports without a persistent conclusion.

## Acceptance Commands and Evidence Loop

Run in the following order inside `creao-design-lab/`; on failure, locate the cause first, and do not delete rules to get a pass:

```bash
npm ci
npm run typecheck
npm run lint
npm run test:design
npm run check:design
npm run build
npx playwright install chromium
PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
npm run test:mutations
```

Additionally run React Doctor and manual browser acceptance; report static hints and real interaction results separately. Linux CI installs browser system dependencies with `npx playwright install --with-deps chromium`. Freeze the guideline, source, and checker digests before the formal mutation run starts; the independent experiment uses copies and does not change the shared baseline.

The full traceability chain is: **live-site screenshots/DOM → audit finding → guideline rule ID → design.md/CSS/components → check assertion → real failure output → fix and re-check → CI gate**. Each audit finding must state which links in the chain have been tested and which are only requirements once connected to the CREAO repository.

Close-out criteria: both required documents finalized, prototype runnable, check results and experiment denominators reconciled, screenshots reviewed, initial miss kept, and external not-yet-connected items made explicit. If any of these is incomplete, the plan as a whole cannot be marked complete.

## Existing Basis and Boundaries

- The marketing site sitemap has 227 entries and the docs site sitemap has 92; no public index of a standalone site-wide `design.md` was found. The product sitemap returns 403, which is not bypassed here.
- Official Widgets Markdown was found: `https://docs.creao.ai/features/widgets.md`, with the local copy at `research/public-design-search/widgets.official.md`. It is a Dashboard component description, not the source of a site-wide design system.
- The live `/widgets` page offers previews and parameters for Card, Stack, Grid, Tabs, etc.; `research/deep/widgets-dom.json` stores the actual CSS variables. Differences between the official documentation and the live rendering must be kept, and component imports/APIs must not be invented.
- The user confirmed there are no other attachments. Missing attachments are no longer treated as a blocking prerequisite. Where there is no feature brief, verification uses a feature request clearly labeled as part of this experiment.
- Existing real issues include the Files page heading semantics, Connectors empty-state copy and actions, misaligned Files list headers at 390px, and icon buttons losing their names.
- Prototype components are local adapted implementations for verification and do not impersonate CREAO's private component library.

## Workspace and File Contract

The independent project lives in `../creao-design-lab/` (relative to this file). `task1`, root-level credentials, and existing projects are not modified. Use npm with an exact lockfile, Node 24; Next.js App Router + React + TypeScript. Baseline port 3100.

```text
creao-design-lab/
  AGENTS.md
  design.md
  README.md
  package.json / package-lock.json
  src/app/{layout.tsx,page.tsx,files/,connectors/,agents/,guidelines/}
  src/components/ui/             # Approved base components within the prototype
  src/components/patterns/       # Shell, PageHeader, EmptyState, etc.
  src/styles/{tokens.css,components.css,layouts.css}
  src/lib/                      # Synthetic data, unified copy
  governance/rules.json          # Rule IDs, severity, source, enforcement layer, and evidence location
  governance/exceptions.json     # Exception records, empty by default
  scripts/                      # Checkers, mutation, and isolated-run entry points
  tests/{design/,e2e/,mutations/}
  experiments/                  # Tasks, patches, and receipts of independent simulated engineers
  reports/                      # Locally generated machine-readable results; no faked pass states
```

The repository-root `.github/workflows/creao-design.yml` is responsible only for this project. The two files required by the formal task live in `exam/` and reference prototype evidence via relative paths. Research screenshots are not uploaded to public services.

## Guideline and Implementation Scope

### Visual and Interaction

Reuse the observed warm-white background, near-black text, thin borders, restrained semantic colors, and simple sidebar. Color values come from recorded variables; newly added spacing, layout thresholds, and component APIs are labeled as prototype decisions. Avoid an unfounded site-wide redesign.

- Files: search, clear search, grid/list toggle, inline creation of simulated folders, dismissible preview. Uses synthetic files; no user data copied.
- Connectors: "All" / "Connectable" / "Connected" state toggle and a recoverable empty state; simulated connection state must be clearly marked as a local demo and must not perform real OAuth.
- Agents: empty state and example detail/status display, clearly marked as local simulation, with no real model runs triggered.
- Guidelines page: can read the guideline and the CSS/rule mapping; do not stuff CI or implementation jargon into product task pages.
- Narrow screens: sidebar collapses, tables become labeled entries, icon buttons keep accessible names; long names, no results, and error states can be checked.

### Initial Rule IDs (must be consistent across all implementations)

| ID | Rule | Automation approach |
| --- | --- | --- |
| DS-001 | Colors in governed CSS use registered tokens; newly added raw colors must fail | CSS AST |
| DS-002 | Pages must not bypass locally approved base components such as Button/Input | TS/JSX AST, explicit scope |
| LAY-001 | The top-level main region has exactly one visible level-1 heading matching the page identity | DOM |
| A11Y-001 | Operable controls have accessible names on both desktop and narrow screens | DOM/accessibility check |
| STATE-001 | Recoverable empty states have an actionable next step, and the actual destination is verified | Interaction test |
| NAV-001 | Guidance labels match their real destinations and reuse unified copy | Browser copy contract + interaction |
| RESP-001 | Narrow-screen lists keep field correspondence, with no overlap/clipping of key content | Geometry check + manual screenshot review |
| GOV-001 | Rules, doc index, and CSS/check entry points exist, and exceptions are valid | Registry/link/exception validation |

Rules cannot be judged by a self-reported `data-compliant=true`. Test locator attributes are allowed, but assertions must check actual structure, names, behavior, or geometry. Source lint may read the real AST; using regex alone to pose as full analysis is forbidden.

## Execution Phases and Parallel Division of Work

1. **Rules and evidence agent**: consolidates sitemap/screenshot research conclusions and drafts `design.md`, `AGENTS.md`, and the task guideline document; does not write the app or scripts.
2. **Prototype agent**: exclusively owns package, Next config, src, and visual implementation; aligns component exports and paths with the check agent; does not change checkers.
3. **Check agent**: exclusively owns governance, design checks, lint config, and browser tests; reports needed dependencies to the main agent, and the prototype owner merges package changes.
4. **Mutation agent**: exclusively owns the mutation runner, fixtures/patches, and experiment design; runs changes in isolated temporary directories without overwriting shared source files; reports exact hits and escapes.
5. **Main agent**: integration, dependency installation/unified commands, CI, browser visual verification, source verification, scheduling of independent simulated engineers, final receipts, and the task compliance audit. File conflicts are coordinated with the owner first; others' changes are not overwritten.

Design docs, checkers, and UI can be drafted in parallel, but full acceptance must run after the baseline is settled. The simulated engineer experiment must wait until the guideline and baseline are frozen; engineers must not modify check code to make results pass.

## Validation and Mutation Experiments

Three kinds of evidence are used:

- **Deterministic negatives**: inject raw colors, bypass base components, remove h1, hide button text without keeping a name, remove empty-state actions, wrong destination copy, mobile layout regression, expired exceptions, etc.
- **Deterministic positives**: switch to a registered color; add a valid file entry/long name; add a secondary action using guideline components. Used to measure false positives, not only to prove violations are blocked.
- **Independent engineer experiment**: at least one guideline-compliant feature change and one deliberately shortcut change, using different subagents, independent copied directories, the same task, and the original checks. Counted separately from the preset mutation set.

Each experiment receipt records: baseline file digest, task/mutation, changed files, check commands, exit codes, rule IDs, duration, report path, and classification reason. Verify the shared baseline digest before and after the run to avoid contamination. Newly found escapes are kept in the results; after fixing the checker, record a second-round result without overwriting the first failure.

## CI/CD and Governance

- CI stages: lockfile install → types/lint → static design rules → production build → browser tests of affected paths → mutation verification → evidence upload.
- Check content and execution config are also governance assets; CODEOWNERS/rule-owner review and an external required check are needed to prevent authors from deleting the gate themselves. AGENTS.md or an editable CI YAML alone cannot prevent bypass.
- Fast PR checks and time-consuming mutation can be layered, but this prototype must run both layers locally.
- Automatic visual snapshot updates do not count as passing; baseline changes need screenshots and a manual rationale. Semantic and geometry assertions can run cross-platform; enable pixel thresholds only after the environment is fixed.
- Record each exception's scope, reason, owner, and deadline; the checker validates format and expiry but cannot prove approver identity, and real approval must come from a protected process.
- At this stage CD only designs the contract "a release candidate may be produced/published only after passing the gate", with no actual deployment. Remote branch protection, environment approvals, and deployment smoke checks are explicitly listed as not connected.

## Technology Selection and Priorities (conclusions of the 2026-10-11 discussion)

This section records the order confirmed by the user: **first complete the existing validation loop → add axe, visual regression, and the page-state inventory → run the compliant and violating engineer experiments → refine the two required documents**. The main thread `creao-design-master` (`01a12cb6-efdc-77b2-965f-646055a400be`) coordinates the swarm, file owners, baseline freezing, and final acceptance; the discussion thread does not start a separate parallel implementation. The priorities below are implementation decisions and do not mean tools are installed or checks have passed.

### Adopted Approaches and Their Roles

| Approach | Current responsibility | What it cannot replace |
| --- | --- | --- |
| Screenshots, DOM/AX, and CSS variable evidence | Support real issues and visual sources | CREAO's private component APIs, internal authoritative token source |
| `design.md`, `AGENTS.md`, rule and exception registries | Reading entry point for humans/agents, rule index, exception expiry | Repository permissions and real approver identity |
| Next.js + React + TypeScript | Runnable routes, components, and interaction experiments | CREAO's existing tech stack; should adapt to the original library in future |
| tokens/components/layouts three-layer CSS | Separate variables, controls, and page geometry | Comprehensive constraints on spacing, typography, and token semantics |
| TypeScript AST + PostCSS AST | Custom design lint: native controls/static aliases, raw colors, unknown tokens | Complete analysis of arbitrary dynamic factories, wrapper component origins, inline/CSS-in-JS |
| Playwright DOM, interaction, and geometry assertions | Verify real page behavior and part of layout | Full accessibility audit, judging visual quality, unregistered states |
| Custom mutation runner | Inject design violations into isolated source copies and measure whether gates hit | Independent engineer experiment, proof of coverage of all unknown violations |
| GitHub Actions YAML | Chain checks, keep evidence, generate candidate source receipts | Proof of enabled required checks, remote CI, or actual deployment |

Historical evidence verified read-only at discussion time: the first static mutation round had 5/6 negatives hit, 1 alias pattern missed, 2/2 positives passed, invalid/error 0; the report is at `creao-design-lab/reports/mutations-static-2026-10-11T21-03-48-256Z/`. Static const alias resolution was later added to the source, but a separate re-check receipt is required before it can be claimed as verified. At that time `reports/e2e.json` recorded 20 browser launch failures caused by a missing matching Chromium, which are not design-violation blocks. When the main thread continues, it must read the latest evidence and must not treat this historical snapshot as the final state.

### Selection Decisions

| Priority | Approach and decision | Rationale and boundaries |
| --- | --- | --- |
| P0: close out first | Complete the existing lint, types, unit tests, design check, production build, browser, and mutation loop | Establish a trustworthy baseline first; keep the initial survivor, store re-checks separately after adding checks; infrastructure failures cannot count as killed |
| P1: required this round | `@axe-core/playwright` | Add automated accessibility scans on registered first screens, dialogs, and empty/error states; keep naming, keyboard, focus-restoration, and business assertions; do not claim full WCAG compliance |
| P1: required this round | Playwright `toHaveScreenshot()` visual regression | Upgrade screenshot evidence to reviewed-baseline comparison; first cover Files desktop/narrow and key empty states, fixing fonts, data, viewport, browser, and run environment; changes must be explained, and auto-updating baselines after failure is forbidden |
| P1: required this round | Page–state–viewport inventory | Enumerate existing routes, states, expectations, check IDs, screenshots, and coverage status; unimplemented/untested items must be recorded explicitly so new pages do not silently escape the gate |
| P1: required this round | Independent engineer A/B experiment | Two agents build the same feature on a frozen baseline copy, one following the guideline and one taking reasonable but violating shortcuts; original gates unchanged; feature and guideline evaluated separately |
| P1: later, targeted at gaps | Typed page patterns and component APIs | Use CollectionPage, IconButton, and state interfaces distinguished by empty/error type to reduce error space; required fields cannot prove callbacks are valid, so runtime tests stay; this round does not block the loop on a large refactor |
| P1: later standardization | ESLint import restrictions, Stylelint plugin, token-purpose constraints | First govern approved component entry points and high-value semantics, then package stable custom rules as IDE/CI-reusable plugins; valid tokens can still be misused, so checking variable existence alone is not enough |
| Required before production integration | Rulesets, required checks, CODEOWNERS, governance file protection | Protect the guideline, component foundation, tokens, tests, exceptions, workflow, and CODEOWNERS itself; constrain bypasses and approval expiry; verify repository plan/permissions; do not treat local YAML as enabled protection |
| P2: near term as needed | Storybook/CSF pattern catalog | Turn states of PageHeader, EmptyState, and file-list compositions into runnable examples linked from the guideline; complete the state inventory first; do not rebuild the whole component library |
| P2: when integrating APIs | MSW | Uniformly simulate slow responses, 500, insufficient permissions, empty results, and recovery; the current local React state prototype does not impose a network mocking layer for now, and server-side requests need separately designed interception |
| P2: targeted at coverage gaps | fast-check | Generate valid names, filter combinations, and operation sequences, saving seeds and minimal counterexamples; prioritize pure functions/checkers, then bounded browser samples |
| P2: once the checker matures | Stryker | Mutate the checker's internal logic to test unit tests; counted separately from custom mutations that inject page design violations; do not immediately run full mutation on the Next app |
| Deferred | DTCG + Style Dictionary, paid visual platforms, centralized organization workflow | Introduce once multi-platform/theme/team-scale needs arise; there is currently no CREAO private token source, so avoid creating a second source of truth or expanding tool scope |

Integration into the existing product uses progressive governance: freeze the inventory of historical violations, new changes add no new violations, and fixed issues do not regress; each exception has an owner, reason, deadline, and fix task. New exceptions and expansions of the historical baseline also need review. Continuously record false positives, misses, and execution time, to keep teams from turning off the gate to reduce noise.

### Swarm Execution Order and Acceptance Handoff

1. **Phase A — Existing loop.** The check agent owns existing browser/static verification, the mutation agent owns frozen copies and re-checks, and the prototype owner fixes real implementation defects; the main thread unifies dependency/lock changes and baseline versions. Exit criteria: the compliant candidate passes the established checks, positives/negatives are classified accurately, initial failures are fully kept, and reports are reproducible.
2. **Phase B — Expanded verification.** The axe owner, visual regression owner, and state inventory owner can draft in parallel, each exclusively owning their test files/inventory; shared package, Playwright config, and rule registry are integrated by the main thread or a designated owner. Suggested artifacts are `tests/e2e/accessibility.spec.ts`, `tests/e2e/visual.spec.ts`, versioned visual baselines, and `governance/page-states.json` (or an equivalent single inventory); final paths are confirmed and indexed by the main thread, and mutually contradictory inventories must not be maintained in duplicate. Exit criteria: new checks pass on the compliant baseline, at least one appropriate negative proves the check can trigger, baseline screenshots have been viewed by an independent reviewer, and new states have explicit coverage results.
3. **Phase C — Engineer experiment.** The enhanced baseline is frozen again. Two independent agents implement the same feature per `experiments/engineer-protocol.md`; they must not modify tests, rules, dependencies, or gates to make results pass. An independent evaluator verifies protected asset digests, runs the same checks, verifies the new feature's actual behavior, and keeps the task, patches, screenshots, commands, exit codes, and item-by-item conclusions. The violating implementation must compile; a compile failure can only be treated as an invalid experiment. Fixes are a second round and cannot overwrite the first.
4. **Phase D — Required documents.** The documentation owner refines `exam/design-system-guideline.md` and `exam/compliance-audit.md` based on the final run receipts; an independent reviewer verifies rule IDs, real page evidence, check entry points, screenshots, experiment denominators, and external not-yet-connected items; the main thread confirms that the README, implementation plan status, and the two formal deliverables are consistent.

Phases may be prepared in parallel, but dependencies must not be skipped, and different agents must not write to the same frozen baseline. If tests, docs, or UI change, a new candidate identity should be generated, and only affected checks plus the required final gates are re-run. Pass claims must correspond to actual reports, not agent self-reports.

### Additional Acceptance Requirements

- **axe:** save the scanned pages/states, rule tags, violation details, and uncovered scope; failures must not be eliminated by whole-page exclusions.
- **Visual:** save expected/actual/diff, environment info, and the baseline review rationale. Results across operating systems must not be mixed; states without a stable baseline are recorded as pending, not as passed.
- **State inventory:** cover at least the actual current states of Files/Connectors/Agents/Guidelines; Files includes populated, search with no results, long names, create validation, and preview; Connectors includes connected-but-empty and recovery; Agents includes empty state and example detail. If loading/error/permission are not yet implemented, mark them as unimplemented rather than faking coverage.
- **Engineer experiment:** the compliant implementation passes the same set of applicable gates; for the violating implementation, record item by item which rules caught it and which missed; feature acceptance and design compliance get separate conclusions, with no promise that all unknown violations will be blocked.
- **Final documents:** the audit traceability chain adds axe/visual evidence; fixed mutation, engineer experiment, and infrastructure failures are counted separately; local prototype proof is clearly separated from CREAO production integration.

### Technical References

- [TypeScript unions and narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html): component state contracts.
- [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing), [visual comparisons](https://playwright.dev/docs/test-snapshots): axe integration, environment consistency, and screenshot baselines.
- [ESLint import restrictions](https://eslint.org/docs/latest/rules/no-restricted-imports), [Stylelint plugins](https://stylelint.io/developer-guide/plugins/): mature lint extension interfaces.
- [Storybook CSF](https://storybook.js.org/docs/api/csf), [network mocking](https://storybook.js.org/docs/writing-stories/mocking-data-and-modules/mocking-network-requests): runnable state catalog and MSW.
- [fast-check](https://fast-check.dev/docs/core-blocks/), [StrykerJS](https://stryker-mutator.io/docs/stryker-js/introduction/): property-based input testing and program mutation; they cannot replace design mutation or the independent engineer experiment.
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets): trusted check and approval boundaries.
- [DTCG format specification](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/), [Style Dictionary](https://styledictionary.com/getting-started/installation/): later token exchange/generation options; a DTCG Community Group specification is not a W3C Recommendation.

## Risks and Reporting Principles

Passing a limited set of tests does not mean no engineer can bypass the gates. Be explicit about supported code patterns, dynamic style/alias/wrapper component limitations, browser and state coverage, and remaining manual rules. Observed page style values are not an officially recommended API. All demo data is kept separate from real product evidence. The final report includes actual results and residual risks, not just a pretty page or a mutation score.


## Delivery Status at Immediate Close-out per User Request

The two required task documents, the Next.js prototype, the AGENTS/design/CSS index, 13 design unit tests, enhanced browser 38/38, reviewed visual 3/3, and 1 real negative control each for axe and visual are all in place. The original A/B experiment and the same-agent enhanced re-check are saved separately; enhanced A 38/38, B 32/38 and blocked. CI configuration is written; the Linux visual baseline and remote protection are not yet connected.

The final fixed mutation run was still running when the user requested an immediate close-out: sealed at 9/12 planned negatives killed and 2/3 positives passed, with another 3 negatives + 1 positive pending. The full run did not complete, so the plan as a whole cannot be marked fully complete; the first-round alias miss, the two infrastructure invalidations, and all fix evidence are kept. See [validation results](../validation/validation-results.md) and the [partial run receipt](../research/validation/phase-b/mutations-all-partial-2026-10-11T21-28-22-239Z/partial-summary.json).
