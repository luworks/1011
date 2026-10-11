# CREAO Product Design Guidelines and Enforcement

Version 0.2 · 11 October 2026 · Proposed owner: Product Design, reporting to the CTO; implementation partner: Frontend Engineering.

## Decision

Keep CREAO's existing token/component system. Add a product-level composition contract and make its objective parts release gates. Engineers and coding agents should choose a canonical screen pattern, compose approved components, exercise required states, and attach evidence before a change becomes a release candidate.

This document defines the screen composition rules, exact failure conditions, adoption decisions and delivery mechanism. An engineer can use it to choose a layout and determine what must pass. The accompanying [design.md](../creao-design-lab/design.md) indexes the executable implementation, and [AGENTS.md](../creao-design-lab/AGENTS.md) loads the workflow for coding agents. The local Next.js lab demonstrates enforceability; it does not replace CREAO's private component library or alter production.

## Evidence and scope

CREAO publicly documents a Dashboard Widgets system with Stack, Grid, Card, Tabs, data display and chart components. Its documentation describes a warm canvas, cream surfaces, near-black text, restrained semantic color and structured widget trees. [Official Widgets documentation](https://docs.creao.ai/features/widgets); [saved source](research/public-design-search/widgets.official.md).

The live `/widgets` gallery and CSS inspection corroborate many colors and component concepts. The inspected product also includes chat, agents, file collections/preview, connectors/setup, skills, and a video workspace. [Research findings and evidence index](research-findings.zh-CN.md).

No full-product `design.md` was found in the inspected public sitemaps (227 marketing URLs and 92 documentation URLs); the application sitemap returned 403. This bounded result does not imply CREAO lacks an internal design system. The brief explicitly says it exists. The lab uses observed values and a clearly identified local component adapter to demonstrate how integration would work.

The user confirmed there are no additional screenshots or feature briefs. Live captures therefore provide the audit material. A small synthetic feature request and intentional code mutations provide validation of the mechanism; they are not presented as an official upcoming feature.

## Canonical screen patterns

| Pattern | Composition and hierarchy | State and behavior requirements | Adoption |
| --- | --- | --- | --- |
| Collection | Shell → page identity + one dominant page action → search/filter/view controls → results/empty/error region | Preserve filters across views; show selected view/tab; distinguish no data from no matches and failures | Canonical for files, agents, connectors and skills; implemented for first three in lab |
| Detail / preview | Object identity → status/metadata → content → contextual actions | Return to the originating context; named close/back; Escape and focus restoration for modal previews | Canonical; file preview demonstrated |
| Chat workbench | Conversation identity → ordered message/result stream → explicit run/approval state → composer | Show current execution authority; distinguish running, awaiting user, failed and completed; keep composer reachable | Canonical proposal; full agent runtime not implemented in lab |
| Configuration | Identity/back → scope explanation → labeled sections → validation → save/confirm | Surface effects before confirmation; show field errors near fields; prevent duplicate submission | Canonical proposal based on observed setup surfaces; real OAuth and persistence not exercised |
| Approval / run review | Actor/operation → target/scope/consequence → approve/cancel → resulting state | No automatic approval from mere screen navigation; retain a reviewable outcome | Canonical proposal; requires runtime fixtures before production acceptance |
| Dashboard | Stack/Grid root → Cards/group headings → data/chart/table widgets | Preserve reading order; meaningful labels; local scroll only for genuinely two-dimensional content | Official documented widget composition; not all widgets recreated |

### How to choose and compose a screen

Start from the user's primary task. If they compare or manage multiple objects, choose Collection. If they inspect one object's contents or result, choose Detail/preview. If they express intent and monitor execution through conversation, choose Chat workbench. If they edit structured settings, choose Configuration. If they authorize an external consequence, choose Approval/run review. A Dashboard belongs inside a chat result or detail view when the user needs structured data; it is not a reason to create a new app shell.

Every top-level route uses one named main region, one visible page identity and the existing shell. Desktop navigation stays consistent across routes; compact navigation collapses without removing its accessible name or current-route indication. Put the page identity and page actions together. Place search, filtering and view selection directly beneath, then a stable content/state region. Keep the reading order the same in the DOM and the responsive layout.

Use the approved library's equivalents of PageHeader, Button/Input, EmptyState, Card, Stack/Grid and Tabs. In the demonstration adapter, these are `PageHeader`, `EmptyState`, `Shell`, `Button`, `Input` and `Icon`; the real CREAO integration must bind to the existing library. Feature code must not copy a button's styling or invent its own native control merely because the required variant is missing: first use an existing variant, then request a reviewed primitive extension if necessary.

Choose a **list** when the task depends on comparing recurring attributes, such as filename, size, modification time and source. Choose **cards** when a preview, richer description or grouped content matters more than cross-row comparison. If both views are useful, provide a view switch with an exposed selected state and preserve the query and filters across the switch. Do not mix unrelated metadata into visually interchangeable cards without labels.

Each page has at most one filled, visually dominant page-level primary action. Secondary actions remain available with lower emphasis; destructive actions belong to the affected object and state their consequences before commitment. An object's action menu and an empty-state CTA do not create a license for several competing page-level primaries. A preview stays subordinate to its originating page: retain its identity, provide named close/back, support Escape where modal, and restore focus to the opener. If the route and navigation context change, treat it as a detail page instead.

### Responsive composition

Use content integrity to choose breakpoints, not device names. In the lab, file collections become labeled entries at **900 CSS px and below**; the navigation shell collapses at **760 CSS px and below**. These are local proposals validated against the demonstrated layouts, not claimed private CREAO breakpoints. They differ because an intermediate-width screen can still fit navigation while no longer fitting file columns.

When a list becomes stacked entries, put the name first and move metadata into explicit label/value groups. Hide the old desktop header; do not leave column labels above values that no longer occupy those columns. Keep long names readable through wrapping or an accessible preview/detail path. Hiding visible action text is allowed only when the accessible name remains. Do not use global horizontal overflow clipping to hide a broken layout. A genuinely two-dimensional table or chart may use a named local scroll region, but essential page controls must stay reachable without horizontal page scrolling.

The automated file-layout contract checks widths 320, 390, 800 and 1280 CSS px. The original defect was captured at 390 × 844; the current local tests use height 900. Review the source viewport, representative long content and supported locales before production adoption. Passing these finite widths does not prove every browser or breakpoint.

### Admitting a new pattern or a one-off

1. Identify the user task, the proposed existing pattern and the exact requirement it cannot satisfy. Aesthetic preference alone is insufficient.
2. Supply representative content, long-content and compact examples plus initial-empty, filtered-empty, loading, failure and permission states where applicable. For execution flows include running, awaiting decision and completion states.
3. Show the composition from approved primitives, the alternative layouts considered and the proposed reusable API. Mark every new token or behavior as a proposal.
4. Product Design approves hierarchy, interaction and whether this is reusable canon or a scoped one-off. Frontend Engineering approves the implementation boundary, accessibility and testability; the CTO resolves unresolved ownership conflicts.
5. Before use, update the pattern contract and registry, add positive/negative examples, and add executable checks for its objective requirements. A one-off instead receives a scoped, expiring exception where the supported exception policy permits it. Do not silently make the deviation the new default.

Canonical proposal means the prescribed pattern for new work; it does not mean the lab has implemented every production state. The adoption column above explicitly separates demonstrated collection/preview patterns from unimplemented chat, configuration and approval runtime flows.

## Product-level rules

The following contracts are mandatory within their declared scopes. Any automated failure blocks the candidate until corrected or covered by a valid supported exception. Product Design review also blocks an unresolved human-assessed violation; a green test does not waive that review. The executable mirror is [rules.json](../creao-design-lab/governance/rules.json).

| ID | Mandatory rule | Acceptance evidence | Gate |
| --- | --- | --- | --- |
| DS-001 | Use registered semantic color tokens in governed styles; palette literals belong in the token source | CSS AST contains no disallowed literals/unknown governed tokens | Static block; manual review for semantic misuse/contrast |
| DS-002 | Feature JSX composes approved primitives rather than duplicating native controls | No governed intrinsic or statically aliased `button`/`input`/`select`/`textarea` JSX outside the UI boundary; approved imports checked in review | TS/JSX AST with lexical const alias resolution; dynamic aliases/wrappers/import provenance outside current automation |
| LAY-001 | Each top-level route has exactly one visible matching `h1` in its main region | Runtime heading count, visibility and expected name at desktop/compact sizes | Browser block |
| A11Y-001 | Visible interactive controls retain accessible names at all tested sizes | Runtime names, including icon controls after responsive text hiding | Browser block; manual review for meaningful wording/focus |
| A11Y-002 | Enumerated states have no actionable axe violations; incomplete findings receive documented review | 16 axe scans across route/state/viewport fixtures, retained raw results and targeted keyboard evidence | Browser block; incomplete is not an automatic pass |
| VISUAL-001 | Three specified screen snapshots match a reviewed environment-specific baseline within configured tolerance | Expected/actual/diff images and baseline approval record | Visual gate; missing/unreviewed platform baseline fails closed |
| STATE-001 | Recoverable empty states offer a working next step in that state | Trigger empty fixture, invoke action and assert the recovered destination/content | Browser block |
| NAV-001 | Guidance names the actual destination using the shared label source | Canonical Chinese destination name, guidance, selected tab/region after interaction | Browser block; shared-source reuse checked in review |
| RESP-001 | Compact layouts preserve field associations and reachable controls | Automated checks at widths 320/390/800/1280, height 900; independent field oracle at 390; source audit at 390 × 844 | Browser block for checked geometry; human review for visual meaning |
| GOV-001 | Rules, linked implementation/checker files and scoped exception records stay valid | Registry/link validation, expiry checks, protected owner review | Static block + external review policy |

### Exact failure conditions and automatic coverage

**DS-001 — Token authority.** In all `src/**/*.css` except `src/styles/tokens.css`, fail on literal hex palette colors, literal color functions, named colors in color-bearing declarations, or any `var()` reference not declared in the token file. This covers component and layout styles as well as additional source stylesheets. `transparent`, `currentColor` and `inherit` remain allowed semantic keywords. The PostCSS/value-AST check does not inspect JavaScript inline styles, CSS-in-JS, generated/external CSS or HTML color attributes. Those require review or an explicit extension of the checker. A valid token used with the wrong meaning, insufficient contrast or an unauthorized edit to the palette also requires owner review: existence alone is insufficient.

**DS-002 — Primitive boundary.** In TS/JSX under `src/app`, `src/pages`, `src/features`, `src/components/patterns` and `src/components/features`, fail on native `button`, `input`, `select` or `textarea` JSX, including lexically resolved `const` aliases to those string tags. The native implementations belong inside the approved UI boundary. TypeScript AST/symbol resolution handles static aliases and lexical scope; it does not establish library provenance or cover dynamic aliases, `React.createElement` and arbitrary custom wrappers. Approved imports and changes to the privileged UI directory require source review. Using a statically aliased native element is still a violation even when its visual styling resembles the approved Button.

**LAY-001 — Page identity.** For `/files`, `/connectors`, `/agents` and `/guidelines`, fail if the initial rendered route has other than one main region, other than one visible level-one heading inside it, or a heading name that does not match the page's canonical identity. The expected Chinese identities are “文件”, “连接器”, “智能体” and “设计规范”. Tests run at 1280 and 390 CSS px. A large span/button or a hidden-only title does not qualify. New routes must add their identity fixture; the checker does not automatically discover every route or dynamic state. Preview/section titles remain subordinate and must not create a second visible page-level heading.

**A11Y-001 — Named controls.** At those same four routes and two widths, inspect visible native buttons/inputs/selects/textareas, links with destinations, and button/tab roles. Fail if any inspected control has an empty or whitespace-only accessible name, including after visible text collapses. Use the browser's accessible-name computation, not a self-reported compliance flag or raw `textContent`. This does not establish that a non-empty name is meaningful, nor does it test every opened dialog or later dynamic control. Human review checks meaning, keyboard operation and focus; affected new states need fixtures before release.

**STATE-001 — Working recovery.** For the connected-empty fixture, fail if the in-state “浏览可连接服务” action is absent/hidden, fails to select “可连接”, does not reveal a service action, or leaves the same empty recovery state in place. For the unmatched-file-search fixture, fail if the clear action is absent from the empty region, does not clear the query, or does not restore an actual seeded result. A nearby unrelated control or an inert button is insufficient. These are the two automatically tested recovery flows. Loading, network failures, permission failures, initial agent creation and real connection outcomes remain normative state requirements, with manual review and integration-specific fixtures required before those flows ship.

**NAV-001 — Exact destination.** In the connected-empty state, fail if the real tab named “可连接” is missing, the empty-state description does not contain “可连接” or contains the obsolete “可用”, or the recovery action does not select the actual destination. This browser assertion intentionally anchors to a canonical Chinese contract. Guidance, labels and actions must reuse the shared copy source, but source reuse is currently checked by review rather than import analysis. Other locales or a legitimate rename require reviewed destination fixtures; editing both UI and expected strings without reviewing the navigation contract is not acceptable evidence.

**RESP-001 — Field integrity and reachability.** At 390px, fail if the desktop file header remains visible, metadata labels are absent/hidden or differ from the expected label set, items leave the viewport, metadata rectangles overlap, or the document horizontally overflows. Independently assert that the known file's modification time, size and source values remain paired with their expected labels; do not derive the expected mapping from the component under test. At 1280px, assert desktop headers return and compact metadata labels hide. At 320px and 800px, additionally assert hidden desktop headers, visible field labels, viewport-contained items and no document overflow. Capture screenshots for review. These checks do not prove every visual reading order, other locales, all content lengths or other engines; review those affected cases explicitly.

**GOV-001 — Contract integrity.** Fail if the registry is not valid version-1 structured data, a required rule is missing/duplicated/unknown, required rule fields or enum values are invalid, a checker path is missing, `design.md` lacks a required rule ID or executable file link, or one of its relative file links is broken. Fail on malformed/duplicate/expired exception records, nonexistent or non-relative scope paths, unsupported rule exemptions or unexpected exception fields. The original contract has eight IDs; the enhanced contract adds A11Y-002 and VISUAL-001. Registry and tests must move together for the accepted candidate; the retained v1 registry is historical evidence, not proof that an enhanced check ran. Required executable links include the three CSS files, both governance JSON files, `scripts/check-design.mjs` and `tests/e2e/design.spec.ts`. This validates declared records and paths; it does not authenticate reviewers, prove prose and code are semantically identical, or stop someone with permission from deleting the gate. Protected review and required CI are mandatory external controls.

### Enhanced accessibility and visual contracts

**A11Y-002 — Automated accessibility with reviewable residuals.** Run axe against the 16 enumerated route/state/viewport fixtures in [accessibility.spec.ts](../creao-design-lab/tests/e2e/accessibility.spec.ts). Any actionable violation fails; retain its rule ID, affected nodes and raw report. Do not suppress a rule merely because it exposes a baseline defect. A missing browser, locator failure or unrendered dialog is a test/infrastructure error, not an accessibility violation or mutation kill. Review every `incomplete` category with computed styles, keyboard evidence and representative screenshots where appropriate; record limitations rather than presenting incomplete results as automatically cleared. The local evidence demonstrates why initial-page accessible-name checks alone were insufficient: scrollable tables and code blocks needed keyboard focusability, and the view-switch group needed a valid semantic role. See [accessibility evidence](research/accessibility/README.md).

**VISUAL-001 — Reviewed visual baselines.** Compare three designated screen snapshots—Files list at 1280×900 and 390×900, and Connectors connected-empty at 1280×900—in a fixed browser/platform, viewport, font and fixture environment using [visual.spec.ts](../creao-design-lab/tests/e2e/visual.spec.ts). The current tolerance is `maxDiffPixels: 0` with per-pixel comparison threshold `0.2`; snapshots disable animations and hide the caret, freeze the clock, and wait for fonts. Fail on a missing baseline or a difference beyond the checked-in tolerance. Capture expected, actual and diff images. A deliberate design change requires Product Design review of those images plus the change reason; authors and coding agents must not automatically regenerate baselines to pass. macOS-reviewed snapshots do not authorize a Linux baseline. Linux CI is deliberately fail-closed until its first baseline is generated in the fixed environment, reviewed and committed through protected review. A reviewed baseline proves intentional appearance for those three screens, not all flows; the semantic/axe gates remain required.

The enhanced semantic/browser suite contains **38 cases: 22 original behavior/layout/name tests plus 16 axe scans**. Visual comparisons form a separate three-screen gate and must not be silently added to that denominator. The [state inventory](../creao-design-lab/governance/page-states.json) contains **31 entries: 22 implemented and 9 not implemented**. This inventory is a coverage plan, not 31 passing tests and not a one-to-one mapping to the 38 cases. Unimplemented loading/error/permission/runtime cases remain explicit adoption gaps; a new feature cannot declare them covered merely because initial routes pass. Current receipts and per-phase boundaries are in [validation results](validation-results.zh-CN.md).

### CSS and component integration

Reuse the existing palette's semantic roles. Observed canvas is `--color-background: #f8f6f3`, card/surface is `#fefdfb`, ink/primary is `#16181a`, structural border is `#e6e2db`, primary foreground is `#f3ecd8`, and oxblood accent is `#6e2f2c`. These values were read from the live Widgets DOM; they are not a reconstruction of every private token. New muted/focus/backdrop tokens, spacing steps, widths and breakpoints are explicitly local proposals. Adding a new value requires purpose, provenance and owner review rather than bypassing token authority.

The observed values are mapped in [tokens.css](../creao-design-lab/src/styles/tokens.css); primitive appearance belongs in [components.css](../creao-design-lab/src/styles/components.css), and page/responsive composition in [layouts.css](../creao-design-lab/src/styles/layouts.css). The adapter's UI boundary owns Button/Input/Icon implementations, pattern components own PageHeader/EmptyState/Shell, and the shared copy module owns destination labels. Extend the narrowest relevant layer; do not place feature-specific geometry inside the base Button or repeat its appearance in page CSS.

Official documentation's “sharp corners” and the live UI's radius variables have different scopes. Do not invent a universal zero-radius or fixed-radius rule. Preserve the approved component variants; inspect actual contrast, focus and state communication. Status must use text in addition to color, and color changes alone must not be presented as proof of successful execution.

### Required state behavior

Collections distinguish initial empty, filtered empty, loading, load error and permission failure. Initial empty offers creation/connection; filtered empty offers clearing relevant filters; load error offers retry; permission failure states the missing access and appropriate next step. A zero count must never stand in for an API error.

For connectors, “No connected services” leads directly to the tab actually named “Connectable”; one source owns both labels. For files, a no-results action clears the query and restores known results. For a file preview, close and Escape return focus to its opener. For compact lists, labels travel with their values; desktop headers disappear when the row is no longer a column grid.

These are testable product decisions above the component layer. A Card or Button being valid does not make a screen composed from them valid.

## Delivery mechanism

| Moment | Engineer / coding agent action | Evidence and owner |
| --- | --- | --- |
| Before implementation | Load AGENTS.md + design.md; select pattern; state affected routes/states | Change description; author owns it |
| During implementation | Reuse primitives/tokens; keep labels centralized; build representative state fixtures | Source review; frontend owner owns adapter and scopes |
| Local gate | Run typecheck, lint, static design check, build and browser tests | Command receipts plus screenshots; author owns remediation |
| Rule/shared-system changes | Run negative mutations and positive controls; preserve original failures | Machine results with exact denominator; design + frontend owners review |
| PR gate | Execute same commands against candidate commit; upload reports even on failure | Required status check; reviewer validates screenshots and exceptions |
| Release gate | Publish only an artifact produced by the accepted candidate; smoke-test deployed routes/states | Protected deployment/environment; release owner records commit/artifact identity |

Use Node 24 and the committed lockfile. From `creao-design-lab/`, with port 3100 free, execute the complete local gate in this order:

```sh
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

The browser gate runs the production build just produced, rather than relying on the development server's behavior. Playwright manages that server and fails if another server owns the port. The mutation runner manages isolated candidate copies and its own servers; do not edit the shared baseline while it runs. On Linux CI, install Chromium and OS dependencies with `npx playwright install --with-deps chromium`. CI uses Playwright's bundled Chromium with no `PW_CHANNEL` override.

For a local machine where an installed Chrome is the recorded browser fallback, use the following instead of the final two test commands after the same build and static checks:

```sh
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
PW_CHANNEL=chrome npm run test:mutations
```

In the enhanced candidate, `npm run test:e2e` includes the 22 original tests and 16 axe scans (38 total), excluding visual tests. `npm run test:a11y` runs the 16-scan subset independently; do not count that rerun as additional unique coverage. `npm run test:visual` is the separate three-screen gate. The reviewed local environment can run:

```sh
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:a11y
PW_CHANNEL=chrome VISUAL_ENV=darwin-arm64-25.6.0-chromium-154.0.8037.98 PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
```

`VISUAL_ENV` must match the actual OS, architecture, kernel and browser version; the test rejects a falsely relabeled platform. Do not copy the macOS namespace into Linux CI. Linux visual bootstrap must stop for baseline review, not accept generated images automatically. The historical v1 command receipt alone is not an enhanced-suite receipt.

Record that local browser/channel and version in the receipt; passing installed Chrome locally is not evidence that the bundled CI browser has run. Browser download/setup failure is an environment error, not a design-rule rejection. Use actual command outputs and the audit's receipt table to report results; this command list does not itself claim success.

Static checks parse CSS and TypeScript/JSX rather than trusting an author's compliance flag. Runtime checks inspect actual names, headings, state transitions and geometry. Screenshots support human assessment of hierarchy and field meaning. The executable scopes and limitations in the registry prevail over a broad marketing claim such as “AI reviews the design.”

CI/CD must include protected required checks and ownership of governance files. A contributor who can remove the checker or rewrite the workflow can bypass an unprotected local rule. `AGENTS.md` is an instruction channel, not a security boundary. This repository contains the lab's checks/configuration; remote branch protection, actual CI runs and deployment are distinct integration work and must not be claimed complete from local success.

## Exceptions and maintenance

An exception includes exactly `id`, `ruleId`, exact `path`, `reason`, `owner`, `approvedBy` and `expires`; add route/state scope, tracking and compensating verification in the reason/review record. No blanket app-wide exceptions. Expiry fails closed (YYYY-MM-DD, end of UTC date in this prototype). A declared approver string does not prove approval: rely on the protected review system. The legacy file-waiver implementation supports exact-file DS-001/DS-002 waivers only; unsupported legacy entries fail closed. Broader human acceptance is governed by [Human exceptions and scoped bypass](../creao-design-lab/governance/human-exceptions-policy.md), rather than expanding the old schema implicitly.

### Human override and CI acceptance

The system recommends compliant implementation but supports an authorized human accepting a documented design tradeoff for an important feature. Standard exceptions require the designated Product Design and Frontend responsibilities (a registered dual-role owner may satisfy both), last at most seven days, and disallow requester self-approval. A CTO or explicitly delegated release owner may approve an emergency exception lasting at most 24 hours, with compensating verification, rollback, a repair owner and independent follow-up; any emergency requester/approver overlap must be visible in the record. Ordinary engineers and agents cannot grant themselves those roles.

Scope each approval to one repository and target SHA, policy/request/evidence digests, observed rule/check/finding IDs, exact files or route/state/viewport, and UTC expiry. This includes specific browser/axe findings and reviewed visual differences, not just static CSS/component rules. Original tests still run and original failures remain in the audit. An accepted candidate is labeled `accepted_with_exceptions`; a valid exception never converts the raw failed check to passed. Additional failures, changed scope/commit, expiration or revocation invalidate acceptance. Missing evidence, infrastructure failures and invalid approval are not design findings that can be waived into a verified result.

Coordinator workflow is `REQUEST_DESIGN_EXCEPTION` → verified human `APPROVE_DESIGN_EXCEPTION` → `EVALUATE_DESIGN_EXCEPTION`, with `REVOKE_DESIGN_EXCEPTION` available. These are protocol instructions until mapped to tested commands/CI inputs. The linked policy supplies exact approval wording so the coordinator can present the real candidate, impact, compensating verification and expiry for a concrete decision. Once valid human authorization is recorded, engineers can continue within that scope without repeated approval requests.

CI must retain raw evidence jobs and use a protected final decision gate to distinguish `passed`, `accepted_with_exceptions`, `rejected` and `blocked`. Required-check configuration must support the scoped decision path rather than requiring every waived raw check to become green. A workflow dispatch input or `approvedBy` string alone does not authenticate a human; use verified platform approval and protected role mapping. Unconfigured approval adapters fail closed, while local test fixtures are explicitly labeled simulation. Remote configuration and actual integration must be reported separately from this policy. Test legitimate acceptance, expiration/revocation, unauthorized roles, candidate/scope mismatch, mixed unapproved failures and evidence preservation before claiming the path works.

Operational ownership also includes a daily design-health review: the frontend owner inspects failed gates, new routes/state gaps and expiring exceptions; the designer inspects visual diffs and recurring pattern deviations. Escalate newly introduced user-facing failures to the feature owner with evidence and a due date. This assigns responsibility only; no recurring automation or external schedule is created by this document.

Review recurring exceptions and checker false positives together. Revise a rule when evidence shows it is wrong or a reusable pattern is missing; add both an allowed example and a violating example. The Product Design owner is accountable for pattern quality and wording; the frontend owner for adapter/checker accuracy; the CTO resolves cross-team ownership or release-policy conflicts.

## Proving the gate

The [compliance audit](compliance-audit.md) maps each observed defect to its rule and pre-ship detection path. The lab then validates those paths with real source changes:

- Negative controls inject failures such as a literal color, raw control, missing heading/name, inert recovery, destination mismatch, compact-layout regression and stale governance record.
- Positive controls make legitimate changes using the existing contract and must pass; a gate that blocks everything is not useful.
- Independent engineer agents receive a bounded feature request, work in isolated copies and face the same checks. Their results are reported separately from deterministic fixtures.

Report **killed**, **survived**, **invalid**, and **error** separately. Count only a rule-attributed rejection of a valid candidate as killed; compile failure or missing dependency is not a design-rule success. Retain surviving mutations and first-round failures. No finite suite proves arbitrary future code cannot evade the rules.

This guideline is ready to load and execute in the local adapter. Integration into CREAO's actual repository consists of binding the approved imports/tokens and fixtures to the real library, then enabling protected CI and release policy without weakening the product contracts.
