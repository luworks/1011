# CREAO product design contract

Version: 0.2 (enhanced verification candidate) · 2026-10-11 · Owner: Product Design + Frontend Engineering.

This is the implementation contract for the **local CREAO Design Lab**. It is an evidence-informed proposal for CREAO's product layer, not CREAO's private design-system source. Read this file before changing a screen; use [AGENTS.md](AGENTS.md) for the delivery workflow. The submission-level rationale is in [design-system-guideline.md](../exam/design-system-guideline.md).

## 1. Source boundaries

| Class | Evidence | What it establishes |
| --- | --- | --- |
| Official | [Widgets documentation](https://docs.creao.ai/features/widgets), [saved Markdown](../exam/research/public-design-search/widgets.official.md) | Dashboard component categories and composition: a Stack/Grid root, Cards for groups, data/chart/table widgets inside. Warm surfaces, near-black ink and restrained semantic color. |
| Observed | [Widgets screenshot](../exam/research/deep/10-widgets-layout.png), [DOM/CSS snapshot](../exam/research/deep/widgets-dom.json) | Actual rendered controls, variable values and parameter labels at one point in time. These do not establish private import paths or supported component APIs. |
| Observed | [Files mobile](../exam/research/deep/14-files-mobile.png), [Files DOM](../exam/research/files-dom.json), [connectors empty state](../exam/research/screenshots/05-connectors-empty.png) | Screen behavior and specific design defects used to define testable rules. |
| Proposed | This document, local CSS, local components and checks | Product-level patterns, responsive decisions, acceptance thresholds and enforcement for this experiment. |

Public sitemap research found official Widgets documentation, but no indexed full-product `design.md`. The product sitemap returned 403. This is **not evidence that an internal design system does not exist**. The task states that it does. Replace the local adapter's imports with real approved library imports when integrating in that repository; preserve the contracts below.

## 2. Executable index

These paths are the implementation interface. Do not copy rules into a second divergent checklist.

| Responsibility | Source of truth |
| --- | --- |
| Color, typography and dimension variables | [src/styles/tokens.css](src/styles/tokens.css) |
| Base component appearance | [src/styles/components.css](src/styles/components.css) |
| Page geometry and responsive rules | [src/styles/layouts.css](src/styles/layouts.css) |
| Approved local primitives | [src/components/ui/](src/components/ui/) |
| Page composition patterns | [src/components/patterns/](src/components/patterns/) |
| Destination labels / synthetic data | [src/lib/copy.ts](src/lib/copy.ts), [src/lib/data.ts](src/lib/data.ts) |
| Rule metadata and supported scope | [governance/rules.json](governance/rules.json) |
| Time-limited exceptions | [governance/exceptions.json](governance/exceptions.json) |
| Static enforcement | [scripts/check-design.mjs](scripts/check-design.mjs) |
| Explicit runtime, accessible-name and layout contracts | [tests/e2e/design.spec.ts](tests/e2e/design.spec.ts) |
| Full-page axe state scans | [tests/e2e/accessibility.spec.ts](tests/e2e/accessibility.spec.ts) |
| Reviewed visual comparisons | [tests/e2e/visual.spec.ts](tests/e2e/visual.spec.ts) |
| Route/state/viewport coverage inventory | [governance/page-states.json](governance/page-states.json) |
| State-inventory schema and evidence validation | [tests/design/page-states.test.mjs](tests/design/page-states.test.mjs) |
| Mutation fixtures and results | [tests/mutations/](tests/mutations/); generated evidence: `reports/` |

The registry identifies concrete checker entrypoints. The package scripts are the command interface. A broken index, unknown rule, missing entrypoint or invalid exception fails GOV-001. Directory links above are navigation aids, not a claim that every directory has an independent check.

The local adapter exports `Button`, `Input`, and `Icon` from `src/components/ui/index.tsx`. `Button` accepts native button props and `variant="primary" | "secondary" | "ghost"`; `Input` accepts native input props. Patterns are `PageHeader({ title, description?, actions? })`, `EmptyState({ title, description, action: { label, onClick }, icon? })`, and `Shell({ children })`. Read their TypeScript definitions before changing usage; these names are local APIs, not claimed CREAO imports.

## 3. Preserve the existing visual language

The following values were observed on `/widgets`; they are evidence, not a new brand palette. Local tokens may use a shorter semantic alias but must record that mapping in `tokens.css`.

| Observed CSS variable | Observed value | Intended use in this prototype |
| --- | --- | --- |
| `--color-background` | `#f8f6f3` | Page canvas |
| `--color-card` / `--color-surface` | `#fefdfb` | Elevated content surface |
| `--color-chrome` | `#f4f1ed` | App shell |
| `--color-surface-alt` | `#f0ede8` | Subtle grouped surface |
| `--color-foreground` / `--color-primary` | `#16181a` | Ink and primary action |
| `--color-primary-foreground` | `#f3ecd8` | Text on primary action |
| `--color-border` | `#e6e2db` | Hairline structural separator |
| `--color-control-border` | `#ebe7e2` | Observed control-border token; does not by itself prove sufficient contrast |
| `--color-oxblood` | `#6e2f2c` | Negative / signature accent; never the sole error signal |
| `--spacing` | `.25rem` | Observed scale base |
| `--radius` | `.375rem` | Observed generic radius; do not infer all widgets must have this radius |

Observed font stacks start with Instrument Sans for UI, DM Mono for data, JetBrains Mono for code, and EB Garamond for serif. The prototype can use available system fallbacks; do not silently download or claim the same licensed font rendering. Any extra tokens, including positive-state color, focus ring, spacing steps, width limits and mobile breakpoints, are **local proposals** documented in CSS. Verify contrast on actual text/control pairs; the screenshot alone is insufficient.

Official docs describe sharp corners; the observed UI also exposes several radius variables and uses rounded controls. Preserve that difference. Do not derive a universal zero-radius rule from a dashboard paragraph or copy a generic radius to every product surface.

## 4. Choose a page pattern before writing JSX

All top-level routes use an app shell with persistent desktop navigation, a named main region, and a compact navigation control on narrow screens. Put the page identity and highest-priority page action together; put filters beneath; put content and its states in one stable region. Route titles use PageHeader. Inline previews and configuration panels are subordinate to the page identity.

| Pattern | Use when | Required order / composition | Canonical or experimental |
| --- | --- | --- | --- |
| Collection | Files, connectors, agents, skills | PageHeader → search/filter/view controls → result summary where meaningful → collection OR empty/error/loading state | Canonical; demonstrated in `/files`, `/connectors`, `/agents` |
| Detail / preview | Inspect a selected file or agent without losing list context | Identity → metadata/status → content → contextual actions; provide close/back and restore focus | Canonical; file preview demonstrated |
| Chat workbench | User gives intent and monitors work | Conversation identity → ordered messages/results → explicit run/approval state → composer with visible authority and attachment controls | Canonical proposal; not implemented as a full runtime in this lab |
| Configuration | Connection setup, agent defaults, schedule | Identity/back → explanation/scope → labeled fields in logical sections → validation → one save/confirm action | Canonical proposal; real Slack screen informs it; OAuth not executed in lab |
| Approval / run review | Agent needs a decision before an external effect | Actor and operation → target/scope/consequence → approve and cancel → pending/result evidence | Canonical proposal; test before production adoption; not proven by this lab |
| Dashboard | Agent-generated structured result | Stack/Grid root → Cards/group headings → data/charts/tables; keep responsive reading order | Official widget composition; local adapter does not implement the entire widget catalog |

Do not choose a new page shell for a single feature. A new pattern requires a screenshot with representative content and states, a reason existing patterns fail, Product Design approval, and an implementation/test mapping. One-off promotional or immersive views can be scoped exceptions rather than silently becoming canon.

### Collection and detail decisions

- Use a list when users compare repeated fields; use cards when previews or richer descriptions dominate. A view switch must expose selected state and keep search/filter state.
- A page can have multiple actions, but only one filled, visually dominant page-level primary action. Destructive actions belong near the affected object, with explicit consequences before an irreversible effect.
- A preview must not look like a new top-level page unless the URL and navigation context also change. Closing it returns focus to the trigger. Escape and a named close control must work.
- In a collection, loading, initial empty, filtered empty, permission failure and load error are different states. Never reuse “No files” for a failed request.

### Responsive decisions

The lab's navigation compact breakpoint is 760 CSS px; file collections switch to labeled entries at 900 CSS px in `layouts.css` after an 800px overflow was found during visual review; navigation width is `--sidebar-width: 248px` and desktop page padding is `--page-padding: 32px` in `tokens.css`. These are proposed implementation values, not observed official policy. Automated layout checks use 320, 390, 800 and 1280 CSS px widths (900px height). The live-product audit captured 390 × 844; also inspect this viewport and 320 CSS px manually before production integration.

At compact widths, convert file rows to labeled entries: file name first, then each metadata label/value pair. Remove the desktop header when its columns no longer align. Keep names discoverable through the preview or accessible name. Do not leave a narrow desktop header above a stacked list. Controls may hide visible text only if their accessible names remain. Do not use global `overflow-x: hidden` to conceal an overflow bug. A genuinely two-dimensional chart/table can have a labeled local scroll region; the whole page must not require horizontal navigation to reach core actions.

## 5. Rules and failure contracts

All twelve rules are mandatory within their declared scopes. The original eight remain unchanged; A11Y-002 and VISUAL-001 add independent checks; CMP-001 and CMP-002 promote two component-consistency rules from review-gated to browser checks. `block` means the change cannot become a release candidate without a valid scoped exception. Human judgments are explicitly distinguished from automated checks.

| Rule | Pass contract | Fails when | Enforcement / boundary |
| --- | --- | --- | --- |
| **DS-001** Token use | Governed styles use registered semantic color variables. Literal palette values occur only in `tokens.css`. | A page/component stylesheet adds an unregistered literal color or references an unknown governed token. | CSS AST/static checker. A token can still be used with the wrong meaning: reviewer checks semantics and contrast. |
| **DS-002** Primitive reuse | Feature JSX composes approved local UI primitives; actual native control implementations stay inside the UI boundary. | Governed feature/pattern JSX directly creates `button`, `input`, `select` or `textarea`, including lexically resolved const aliases of those string tags. | TS/JSX AST/static checker. It resolves static const string aliases with TypeScript symbols, but does not resolve import provenance, custom wrappers, dynamic aliases or factories; approved library provenance still requires review. |
| **LAY-001** Page identity | Each governed route has one visible top-level `h1` within its main region, matching that route's identity. Nested preview/section headings are subordinate. | Missing, duplicate, hidden or incorrect main title. A large button/span styled as a heading does not qualify. | DOM test on every governed route at desktop and compact sizes. Correct overall information architecture remains a design review item. |
| **A11Y-001** Named controls | Each operable visible button/input/select/link has a non-empty accessible name in the tested states and viewports. Icon controls retain names when text hides. | Name disappears, label is missing, or a control has no usable identifier. | Runtime accessible-name assertions. A non-empty but misleading name can pass; reviewer must assess meaning, focus order and keyboard operation. |
| **STATE-001** Recovery | Recoverable empty states explain why and offer an in-state action that actually recovers. Initial empty → create/connect; filtered empty → clear relevant filters; error → retry/appropriate help. | Recovery is absent, inert or leads to the wrong state. A separate distant tab alone is insufficient. | Browser interaction fixtures for known empty states and post-action results. Production network/error states need adapter tests beyond the local fixture. |
| **NAV-001** Destination language | Guidance and controls derive destination names from the same label source; actions reveal that destination. | “Available” is referenced when the actual tab is “Connectable”, or the action activates another tab. | Browser assertions against the canonical Chinese destination name, guidance and actual tab/region. Shared-source reuse is a source-review requirement, not import analysis. Localization requires the same check for each supported locale. |
| **RESP-001** Field integrity | At tested compact widths, every metadata value stays associated with its visible label, controls stay reachable and key rectangles do not overlap/clip. | Desktop headers no longer correspond to stacked values, or essential content overlaps/offscreen. | Browser geometry and label/structure assertions plus screenshot review. No claim of full visual correctness or every-device coverage. |
| **GOV-001** Contract integrity | Registry, document/index links, checker paths and exception records are valid and current. Rule/check changes have owner review. | Referenced files are missing, rule IDs drift, or exception records are malformed/expired/outside their declared scope. | Static validation can check records, not the identity of an approver. External required checks and ownership enforce review. |
| **A11Y-002** Axe state scans | The 16 explicit full-page scans have zero WCAG 2 A/AA and 2.1 A/AA tagged axe violations; incomplete results remain visible for manual review. | Any axe violation, regardless of severity. Setup/navigation/browser errors fail execution but are not reported as design-rule detections. | Eight states at 1280×900 and 390×844. No include/exclude/disabled-rule shortcuts. Does not establish complete accessibility or WCAG conformance. |
| **VISUAL-001** Reviewed screenshots | The three explicit screenshots match a reviewed baseline for the actual OS/architecture/release/browser namespace. | Missing baseline, environment mismatch, or any differing pixel beyond the per-pixel color threshold (0.2), because allowed differing pixels = 0. | Files list at 1280×900 and 390×900; Connectors connected-empty at 1280×900. Legitimate changes can also fail and need review; a green image comparison is not a usability proof. |
| **CMP-001** Tabs vs filter chips | Tabs are a single-select view switch: a collection renders at most one `role="tablist"` in main (`/connectors` exactly one), every tab exposes `aria-selected`, and exactly one tab is selected before and after switching. | A second tablist, a missing `aria-selected`, zero or several selected tabs, or a click that adds rather than moves selection. | Browser assertion in [tests/e2e/design.spec.ts](tests/e2e/design.spec.ts) on the four governed routes at 1280 and 390px. FilterChips grouping, search → tabs → chips → count order and visual parity remain review items. |
| **CMP-002** Action hierarchy | The main region has at most one filled primary Button (`Button variant="primary"`, rendered as `.button-primary`). | Two or more `.button-primary` elements inside `main`. | Browser count in [tests/e2e/design.spec.ts](tests/e2e/design.spec.ts) on the four governed routes' initial state at 1280 and 390px. Class-based: a restyled lookalike, sub-region hierarchy, dialogs outside main and the files create form / agents detail states are not exercised; secondary/tertiary and IconButton consistency stay in review. |

Automated route coverage is `/files`, `/connectors`, `/agents` and `/guidelines`, as recorded in the registry. Future routes and unrepresented dynamic states still require review or new fixtures. DS-001 covers source CSS only; inline styles, CSS-in-JS, dynamically generated styles, external CSS and HTML color attributes are outside its current checker scope. Semantic CSS keywords such as `transparent`, `currentColor` and `inherit` are allowed; they do not define new palette values. Adding a privileged UI implementation or changing token authority requires owner review even if the static check passes.

### State recipes

| Situation | Required message | Next action | Result to assert |
| --- | --- | --- | --- |
| No connected services | “No connected services” + why connecting helps | “Browse connectable services” | Connectable tab is selected and eligible services appear |
| File search finds nothing | State that current query/filters matched nothing | “Clear search” or “Clear filters” | Query/filter resets and seeded files reappear |
| No agents yet | Explain repeatable work and how creation starts | “Create agent” / local example action | Documented create flow opens; lab must identify it as a simulation |
| Load error | Distinguish failed loading from no data | Retry, or permission-specific guidance | Retry is attempted / permission destination is correct |
| Agent running / awaiting approval | Text status, next expected event and available controls | View progress / make an explicit decision | Status transitions from actual response, never inferred from animation alone |

## 6. Before a change ships

1. Declare the pattern, affected route/state/viewports and applicable rule IDs in the change description.
2. Read component implementation and CSS; reuse existing variants before adding styles. Register genuinely new tokens with purpose and provenance.
3. Implement the behavior and fixtures. Run the package's type, lint, static design, production build and browser checks. Run mutation checks when changing rules, checkers, shared components or layout contracts.
4. Inspect desktop and compact screenshots and perform keyboard/focus checks for changed interactions. A green machine check does not waive human design judgment.
5. Attach command results, screenshots and any exception ID. Record failures/skips as such; do not silently regenerate snapshots or edit tests just to accept changed behavior.
6. Owner review covers pattern choice, semantics, hierarchy, contrast and changes to governance assets. CI must execute against the candidate commit; CD accepts only an artifact from that successful candidate, followed by deployment smoke checks.

From this directory, the concrete gate commands are:

```sh
npm ci
npm run typecheck
npm run lint
npm run check:design
npm run test:design
npm run build
npx playwright install chromium
PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
npm run test:mutations
# A separate required visual check needs the exact reviewed environment namespace:
VISUAL_ENV="$REVIEWED_VISUAL_ENV" PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
```

Use `npm run dev -- --port 3100` for interactive local inspection. Read the test runner configuration for server startup/port ownership; do not launch competing servers on the same port. The listed commands describe the required gate, not a claim that a run has succeeded. Actual receipts live under `reports/` and are summarized in the compliance audit.

### State coverage is a declared, testable inventory

`governance/page-states.json` catalogs six source routes and 31 states: 22 implemented states and nine explicitly unimplemented loading/network/permission states. A row is an inventory entry, not proof that every assertion passed. Keep implementation, check implementation, execution, exact test title, executed viewport and evidence separate. An implemented test with no receipt stays `notVerified`; a future check stays `planned`; unsupported states stay `notImplemented` / `notApplicable`. Do not inflate the denominator by counting planned checks as executed.

The catalog validator discovers App Router page files and rejects uncatalogued routes, duplicate states, unknown rules, invalid setup/scope/viewports, missing implemented check paths, and pass claims without evidence. Browser receipt claims must match the exact test title and expected number of runs; axe's repeated title requires both viewport runs. Existing 22-test behavior receipts are retained as historical evidence, not as proof that a later changed candidate was tested. State completeness and whether a test fully asserts its declared semantics still require review.

The 16 axe scans cover eight states only: Files initial list, no search results, empty-folder validation and preview dialog; Connectors connected-empty; Agents initial empty and detail; Guidelines. Their 390×844 viewport is distinct from the behavior suite's 390×900. Full axe output preserves `violations`, `incomplete`, `passes` and `inapplicable`. Zero violations passes the automated gate; unresolved incomplete findings require an explicit human disposition before release.

### Visual baseline review and environment policy

The visual suite is separate (`npm run test:visual`), never silently skipped inside an ordinary gate. `npm run test:e2e` covers 22 existing contracts, 16 CMP-001/CMP-002 contracts and 16 axe scans; this test count is planned configuration, not a claim of successful execution. `npm run test:a11y` can isolate the axe scans during investigation.

Set `VISUAL_ENV` to the verified `${platform}-${architecture}-${OS release}-chromium-${browser version}` namespace, for example the local Mac candidate environment `darwin-arm64-25.6.0-chromium-154.0.8037.98`. The test recomputes and checks that string. System Chrome can be selected locally with `PW_CHANNEL=chrome`; CI defaults to Playwright's matching Chromium. This distinction must appear in the receipt. A Linux run cannot reuse a Mac baseline: absent Linux images must fail, then be generated and reviewed in the pinned Linux environment. Environment names do not prove identical fonts; pin the runner image, fonts, dependencies and browser and retain their versions.

Snapshots use synthetic fixed data, a fixed clock, `zh-CN`, the Los Angeles time zone, DPR 1, light mode, reduced motion, disabled screenshot animations, a hidden caret, CSS scale and full-page capture. `threshold: 0.2` is a per-pixel color tolerance; `maxDiffPixels: 0` means no pixels beyond that tolerance are accepted. Keep expected/actual/diff images and traces with the run.

Missing-baseline runs fail closed. Generating candidates with `npm run test:visual -- --update-snapshots` is a separate authorized review operation, never the PR/CI success path. Product Design plus a frontend owner inspect candidate/previous/diff images and justify intended UI changes. Record that review, commit only the accepted platform-specific images, then rerun normal comparison without update flags. Legitimate new features may require this workflow; do not broaden thresholds or overwrite images automatically to force green. Review ownership must be enforced outside author-editable files.

The prototype demonstrates a local gate. GitHub required checks, CODEOWNERS enforcement, protected environments and deployment receipts must be configured separately. `AGENTS.md` instructs cooperative agents; it is not an access-control boundary. A contributor able to edit every checker and CI policy can bypass local restrictions.

## 7. Exceptions and evolution

`exceptions.json` has the root shape `{ "exceptions": [] }`. Each record requires exactly `id`, `ruleId`, `path`, `reason`, `owner`, `approvedBy`, and `expires` (YYYY-MM-DD; current implementation expires at the end of that UTC date). Use an exact existing relative file path and document affected route/state, tracking reference and compensating verification in the reason/review record. An expired exception fails closed. Never use a wildcard exception for an entire app. Only DS-001 and DS-002 support scoped waivers in this prototype. GOV-001 and browser-rule exceptions fail closed and require a separately reviewed contract change. `approvedBy` is a declared identity and must be verified through the protected review system.

Repeated exceptions indicate a missing pattern or an incorrect rule. Review them with Product Design + Engineering, then revise the contract and add positive/negative examples. Separate a real product violation from a checker false positive. Keep the original mutation results when improving coverage; report survivors and invalid experiments honestly.

## 8. What this contract does not prove

This lab does not recover CREAO's internal component library, change its production site, execute real integrations, validate live agent runs or prove universal WCAG compliance. Static checks cover documented syntax and files; runtime checks cover explicit route/state fixtures. Screenshots are retained locally and may contain account context: use cropped/redacted copies before public submission. The experiment's evidence is useful because those limits are explicit.
