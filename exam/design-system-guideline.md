# CREAO Product Design Guidelines and Enforcement

Version 0.2 · 11 October 2026 · Proposed owner: Product Design, reporting to the CTO; implementation partner: Frontend Engineering.

## Decision

Keep CREAO's existing token/component system. Add a product-level composition contract and make its objective parts release gates. Engineers and coding agents choose a canonical screen pattern, compose approved components, exercise required states, and attach evidence before a change becomes a release candidate.

### At a glance

- **Six screen patterns:** Collection, Detail/preview, Chat workbench (primary), Configuration, Approval/run review, Dashboard. Every new screen starts from one of them.
- **Rule families:** tokens and primitives (DS-001, DS-002); page identity and anatomy (LAY-001, LAY-002); accessibility (A11Y-001, A11Y-002); states and navigation (STATE-001, NAV-001); responsive integrity (RESP-001); visual baselines (VISUAL-001); component consistency (CMP-001, CMP-002, CONTENT-001, CHAT-001); contract integrity (GOV-001).
- **Automated vs reviewed:** DS, LAY-001, A11Y, STATE, NAV, RESP, VISUAL, GOV and the structural core of CMP-001/CMP-002 are executable gates. LAY-002, CONTENT-001, CHAT-001 and the rest of CMP-001/CMP-002 are blocking Product Design review today.
- **How the gate runs:** one local sequence (typecheck → lint → static design check → production build → browser tests), repeated by CI on the candidate commit. Any rule-attributed failure blocks release.
- **Exceptions:** scoped to exact files or route/state, owner-approved and expiring (at most 7 days; 24 hours for emergencies). The raw check stays failed; the candidate is labeled `accepted_with_exceptions`.
- **Delivery:** [AGENTS.md](../creao-design-lab/AGENTS.md) loads the workflow for coding agents, [design.md](../creao-design-lab/design.md) indexes the implementation, and [rules.json](../creao-design-lab/governance/rules.json) is the executable mirror of the rule tables.
- **Scope:** the local Next.js lab proves the rules are enforceable. It does not replace CREAO's private component library or change production.

## Companion package

This document is also read standalone. The full repository ships as `creao-design-submission.zip`; all paths in this section are relative to the ZIP root. Relative links elsewhere in this document resolve inside the ZIP (from `exam/`).

| Path (ZIP root) | Purpose |
| --- | --- |
| `SUBMISSION-README.md` | Package overview and reading order |
| `creao-design-lab/AGENTS.md` | Workflow coding agents load before changing UI |
| `creao-design-lab/design.md` | Executable index: rule IDs mapped to tokens, components and checks |
| `creao-design-lab/governance/rules.json` | Machine-readable rule registry (scopes, gates, limits) |
| `creao-design-lab/scripts/check-design.mjs` | Static gate: CSS token and JSX primitive checks, registry validation |
| `creao-design-lab/scripts/mutation-runner.mjs` | Negative/positive mutation runner on isolated copies |
| `creao-design-lab/tests/e2e/design.spec.ts` | Browser gate: LAY, A11Y-001, STATE, NAV, RESP, CMP checks |
| `creao-design-lab/tests/e2e/accessibility.spec.ts` | Axe scans across route/state/viewport fixtures (A11Y-002) |
| `creao-design-lab/tests/e2e/visual.spec.ts` | Reviewed visual baselines (VISUAL-001) |
| `.github/workflows/creao-design.yml` | CI workflow running the same gate on the candidate commit |
| `exam/agents/design-drift-auditor.md` | Agent definition for auditing screens against these rules |
| `exam/research/` | Live-product captures, DOM/AX records and validation evidence |
| `exam/validation/validation-results.md` | Receipts, denominators and per-phase results |

```sh
unzip creao-design-submission.zip
cd creao-design-lab
npm ci
npm run check:design && npm run build && npx playwright install chromium && npm run test:e2e
```

## Evidence and scope

CREAO publicly documents a Dashboard Widgets system with Stack, Grid, Card, Tabs, data display and chart components, on a warm canvas with cream surfaces, near-black text, restrained semantic color and structured widget trees ([official Widgets documentation](https://docs.creao.ai/features/widgets); [saved source](research/public-design-search/widgets.official.md)). The live `/widgets` gallery and CSS inspection corroborate those colors and components. The product also includes chat, agents, file collections/preview, connectors/setup, skills and a video workspace ([research findings](research-findings.md)).

No full-product `design.md` was found in the public sitemaps (227 marketing and 92 documentation URLs; the application sitemap returned 403). The brief states an internal design system exists, so the lab uses observed values and a clearly labeled local component adapter. No additional screenshots or feature briefs were supplied: live captures are the audit material, and a synthetic feature request plus intentional code mutations validate the mechanism.

## Canonical screen patterns

| Pattern | Composition and hierarchy | State and behavior requirements | Adoption |
| --- | --- | --- | --- |
| Collection | Shell → page identity + one dominant page action → search/filter/view controls → results/empty/error region | Preserve filters across views; show selected view/tab; distinguish no data from no matches and failures | Canonical for files, agents, connectors and skills; implemented for first three in lab |
| Detail / preview | Object identity → status/metadata → content → contextual actions | Return to the originating context; named close/back; Escape and focus restoration for modal previews | Canonical; file preview demonstrated |
| Chat workbench | Conversation identity → ordered message/result stream → explicit run/approval state → composer | Show current execution authority; distinguish running, awaiting user, failed and completed; keep composer reachable | Canonical proposal; full agent runtime not implemented in lab |
| Configuration | Identity/back → scope explanation → labeled sections → validation → save/confirm | Surface effects before confirmation; show field errors near fields; prevent duplicate submission | Canonical proposal based on observed setup surfaces; real OAuth and persistence not exercised |
| Approval / run review | Actor/operation → target/scope/consequence → approve/cancel → resulting state | No automatic approval from mere screen navigation; retain a reviewable outcome | Canonical proposal; requires runtime fixtures before production acceptance |
| Dashboard | Stack/Grid root → Cards/group headings → data/chart/table widgets | Preserve reading order; meaningful labels; local scroll only for genuinely two-dimensional content | Official documented widget composition; not all widgets recreated |

"Canonical proposal" means the prescribed pattern for new work, not that the lab implements every production state.

### Pattern skeletons

Regions are listed top to bottom in DOM and visual order. All numbers are **local proposals** pending owner review, not observed CREAO values: 8px spacing base; page gutter 24px desktop / 16px at ≤760px; region gap 24px; control gap 8–16px.

```text
COLLECTION (files, agents, connectors, skills)           content max-width 1120px (local proposal)
Shell [nav | main]
  PageHeader      h1 + optional description ............ [Button filled: one primary action]
  Controls row    Input(search) → Tabs(view/status) → FilterChips(category) → result count
  Results         list rows | Card grid (auto-fill, min 280px) — one view switch, filters preserved
  State region    EmptyState(initial: create/connect | filtered: clear filters) | error: retry | permission

DETAIL / PREVIEW                                         content max-width 1120px; modal preview max 960px
Shell
  Back/close (named) · object identity (h1 on route; h2 in modal preview)
  Status + metadata   label/value pairs, status as text + color
  Content             Card / Widget tree; 2-D tables/charts scroll locally in a named region
  Contextual actions  Button outline · destructive action on the object, consequence stated

CHAT WORKBENCH                                           message column max 760px, centered
Shell
  Conversation identity (title or home greeting)
  Message stream      user turns · agent turns · Card/Widget results · run status · Approval cards
  Composer (sticky)   Input(multiline) + toolbar [mode · model · attach] ......... [IconButton send]
  Side panel (opt.)   wide artifacts; 480px min, collapses to full detail at ≤900px

CONFIGURATION                                            form column max 720px
Shell
  Back + PageHeader   h1 + scope explanation
  Sections            labeled groups (h2) → Input/select via primitives → field error under field
  Footer actions      [Button outline: Cancel] [Button filled: Save] — disabled while submitting

APPROVAL / RUN REVIEW                                    inline Card in chat, or dialog max 560px
  Actor + operation   "<agent> wants to <operation>"
  Target / scope / consequence   explicit list; external effects named
  Actions             [Button outline: Cancel] [Button filled: Approve]
  Result state        Approved/Cancelled/Failed as text + color, retained in the stream
```

### Chat workbench (the primary screen)

CREAO is chat-first, so this pattern takes precedence over every other screen; deviations require the new-pattern process below. Rules are **CHAT-001** (see Component consistency rules).

- **Home state.** One greeting identity (the only place display/serif type is allowed), the composer as the dominant element, at most one promo/announcement strip that is dismissible and sits above or below the composer without displacing it, and suggestion cards that are visually subordinate to the composer (outline Card, smaller type, no filled buttons).
- **Conversation state.** Messages live in a single centered column (max 760px, local proposal). Agent outputs render as Card/Widget trees inside that column; an agent result must never mount a new app shell, second navigation or second page `h1`.
- **Wide artifacts.** Tables, documents, code or dashboards that cannot fit the column open in a side panel (desktop) or a full Detail/preview (compact). They must not overflow the message column or cause horizontal page scroll; a compact summary Card with an "Open" action stays in the stream.
- **Run state.** Every run shows one of Running / Awaiting approval / Failed / Completed as visible text plus color (and an icon where available); color alone is never the signal. Failed shows the reason and a retry or next step.
- **Approvals.** Approval requests render inline as the Approval/run review pattern: actor, target, consequence, then Cancel (outline) and Approve (filled). Navigation or scrolling never approves; the outcome stays in the stream.
- **Composer.** Always reachable (sticky at the bottom of the conversation; never scrolled away or covered by panels). Mode and model selectors, attachments and send are grouped in the composer toolbar, not scattered into the page header.

### How to choose and compose a screen

Start from the user's primary task. Comparing or managing multiple objects → Collection. Inspecting one object's contents or result → Detail/preview. Expressing intent and monitoring execution through conversation → Chat workbench. Editing structured settings → Configuration. Authorizing an external consequence → Approval/run review. A Dashboard belongs inside a chat result or detail view when the user needs structured data; it is not a reason to create a new app shell.

Every top-level route uses one named main region, one visible page identity and the existing shell. Desktop navigation stays consistent across routes; compact navigation collapses without losing its accessible name or current-route indication. Put page identity and page actions together, then search, filtering and view selection, then a stable content/state region. Keep DOM order and responsive reading order the same.

Use the approved library's equivalents of PageHeader, Button/Input, EmptyState, Card, Stack/Grid and Tabs. The demonstration adapter provides `PageHeader`, `EmptyState`, `Shell`, `Button`, `Input` and `Icon`; the real integration binds to CREAO's library. Feature code must not copy a button's styling or create its own native control because a variant is missing: use an existing variant, or request a reviewed primitive extension.

Choose a **list** when the task depends on comparing recurring attributes (filename, size, modification time, source). Choose **cards** when a preview, richer description or grouped content matters more than cross-row comparison. If both are useful, provide a view switch with an exposed selected state and preserve query and filters across it. Do not mix unrelated metadata into visually interchangeable cards without labels.

Each page has at most one filled, visually dominant page-level primary action. Secondary actions use lower emphasis; destructive actions belong to the affected object and state their consequences before commitment. Object menus and empty-state CTAs do not license several competing page-level primaries. A preview stays subordinate to its originating page: keep its identity, provide named close/back, support Escape where modal, and restore focus to the opener. If the route and navigation context change, it is a detail page instead.

### Responsive composition

Choose breakpoints by content integrity, not device names. In the lab, file collections become labeled entries at **≤900 CSS px** and the navigation shell collapses at **≤760 CSS px** (local proposals, not CREAO values). They differ because an intermediate width can still fit navigation but no longer fit file columns.

When a list becomes stacked entries, put the name first and move metadata into explicit label/value groups. Hide the desktop header; never leave column labels above values that no longer occupy those columns. Keep long names readable through wrapping or an accessible preview/detail path. Visible action text may be hidden only if the accessible name remains. Do not use global horizontal overflow clipping to hide a broken layout. A genuinely two-dimensional table or chart may use a named local scroll region, but essential page controls must stay reachable without horizontal page scrolling.

Automated checks cover 320, 390, 800 and 1280 CSS px. Review other widths, long content and supported locales before production adoption.

### Admitting a new pattern or a one-off

1. Identify the user task, the closest existing pattern and the exact requirement it cannot satisfy. Aesthetic preference alone is insufficient.
2. Supply representative, long-content and compact examples plus initial-empty, filtered-empty, loading, failure and permission states where applicable. Execution flows add running, awaiting-decision and completion states.
3. Show the composition from approved primitives, the alternatives considered and the proposed reusable API. Mark every new token or behavior as a proposal.
4. Product Design approves hierarchy, interaction and whether this is reusable canon or a scoped one-off. Frontend Engineering approves the implementation boundary, accessibility and testability; the CTO resolves ownership conflicts.
5. Before use, update the pattern contract and registry, add positive/negative examples, and add executable checks for its objective requirements. A one-off instead receives a scoped, expiring exception. Never silently make the deviation the new default.

## Product-level rules

These contracts are mandatory within their declared scopes. An automated failure blocks the candidate until corrected or covered by a valid exception. An unresolved human-assessed violation also blocks; a green test does not waive Product Design review. The executable mirror is [rules.json](../creao-design-lab/governance/rules.json).

| ID | Mandatory rule | Acceptance evidence | Gate |
| --- | --- | --- | --- |
| DS-001 | Use registered semantic color tokens in governed styles; palette literals belong in the token source | CSS AST contains no disallowed literals/unknown governed tokens | Static block; manual review for semantic misuse/contrast |
| DS-002 | Feature JSX composes approved primitives rather than duplicating native controls | No governed intrinsic or statically aliased `button`/`input`/`select`/`textarea` JSX outside the UI boundary; approved imports checked in review | TS/JSX AST with lexical const alias resolution; dynamic aliases/wrappers/import provenance reviewed |
| LAY-001 | Each top-level route has exactly one visible matching `h1` in its main region | Runtime heading count, visibility and expected name at desktop/compact sizes | Browser block |
| A11Y-001 | Visible interactive controls retain accessible names at all tested sizes | Runtime names, including icon controls after responsive text hiding | Browser block; manual review for meaningful wording/focus |
| A11Y-002 | Enumerated states have no actionable axe violations; incomplete findings receive documented review | Axe scans across route/state/viewport fixtures, retained raw results and targeted keyboard evidence | Browser block; incomplete is not an automatic pass |
| VISUAL-001 | Three specified screen snapshots match a reviewed environment-specific baseline within configured tolerance | Expected/actual/diff images and baseline approval record | Visual gate; missing/unreviewed platform baseline fails closed |
| STATE-001 | Recoverable empty states offer a working next step in that state | Trigger empty fixture, invoke action and assert the recovered destination/content | Browser block |
| NAV-001 | Guidance names the actual destination using the shared label source | Canonical English destination name, guidance, selected tab/region after interaction | Browser block; shared-source reuse checked in review |
| RESP-001 | Compact layouts preserve field associations and reachable controls | Automated checks at widths 320/390/800/1280; independent field oracle at 390 | Browser block for checked geometry; human review for visual meaning |
| GOV-001 | Rules, linked implementation/checker files and scoped exception records stay valid | Registry/link validation, expiry checks, protected owner review | Static block + external review policy |

### Exact failure conditions

Each rule lists what fails, then what the check does not cover (reviewed by the named owner instead).

**DS-001 — Token authority.** In all `src/**/*.css` except `src/styles/tokens.css`, fail on literal hex palette colors, literal color functions, named colors in color-bearing declarations, or any `var()` reference not declared in the token file. `transparent`, `currentColor` and `inherit` are allowed. Not covered: JavaScript inline styles, CSS-in-JS, generated/external CSS, HTML color attributes, and a valid token used with the wrong meaning, insufficient contrast or an unauthorized palette edit.

**DS-002 — Primitive boundary.** In TS/JSX under `src/app`, `src/pages`, `src/features`, `src/components/patterns` and `src/components/features`, fail on native `button`, `input`, `select` or `textarea` JSX, including lexically resolved `const` aliases to those tags. A statically aliased native element is a violation even if it looks like the approved Button. Not covered: library provenance, dynamic aliases, `React.createElement` and custom wrappers; approved imports and changes to the UI directory need source review.

**LAY-001 — Page identity.** For `/files`, `/connectors`, `/agents` and `/guidelines` at 1280 and 390 CSS px, fail unless the initial route has exactly one main region containing exactly one visible level-one heading whose name matches the canonical identity: "Files", "Connectors", "Agents" and "Design guidelines". A large span/button or a hidden-only title does not qualify. Preview and section titles must not create a second visible page-level heading. New routes must add their identity fixture; the checker does not discover routes or dynamic states.

**A11Y-001 — Named controls.** At the same four routes and two widths, inspect visible native buttons/inputs/selects/textareas, links with destinations, and button/tab roles. Fail if any has an empty or whitespace-only accessible name (browser accessible-name computation, not `textContent` or a self-reported flag), including after visible text collapses. Not covered: whether a name is meaningful, opened dialogs, later dynamic controls, keyboard operation and focus.

**STATE-001 — Working recovery.** For the connected-empty fixture, fail if the in-state "Browse connectable services" action is absent/hidden, does not select "Connectable", does not reveal a service action, or leaves the empty state in place. For the unmatched-file-search fixture, fail if the "Clear search" action is absent from the empty region, does not clear the query, or does not restore a seeded result. A nearby unrelated control or an inert button is insufficient. Loading, network and permission failures, initial agent creation and real connection outcomes remain required states that need integration fixtures and review before they ship.

**NAV-001 — Exact destination.** In the connected-empty state, fail if the real tab named "Connectable" is missing, the empty-state description does not contain "Connectable" or contains the obsolete "Available", or the recovery action does not select the actual destination. The assertion anchors to a canonical English contract (locale fixtures required for other locales). Guidance, labels and actions must reuse the shared copy source; that reuse is checked in review. A legitimate rename requires a reviewed fixture update, not edits to both UI and expected strings.

**RESP-001 — Field integrity and reachability.** At 390px, fail if the desktop file header is visible, metadata labels are absent/hidden or differ from the expected set ("Modified", "Size", "Source"), items leave the viewport, metadata rectangles overlap, or the document overflows horizontally. Independently assert that a known file's modification time, size and source stay paired with their labels, using a fixture not derived from the component under test. At 1280px, desktop headers return and compact labels hide. At 320px and 800px, assert hidden desktop headers, visible field labels, contained items and no document overflow. Capture screenshots for review of reading order, other locales and long content.

**GOV-001 — Contract integrity.** Fail if the registry is not valid version-1 structured data; a required rule is missing, duplicated or unknown; rule fields or enum values are invalid; a checker path is missing; or `design.md` lacks a required rule ID, executable file link (the three CSS files, both governance JSON files, `scripts/check-design.mjs`, `tests/e2e/design.spec.ts`) or has a broken relative link. Fail on malformed, duplicate or expired exception records, nonexistent or non-relative scope paths, unsupported rule exemptions or unexpected fields. Registry and tests move together. Not covered: reviewer authentication, prose/code semantic equivalence, or someone with permission deleting the gate; protected review and required CI are mandatory external controls.

**A11Y-002 — Automated accessibility with reviewable residuals.** Run axe against the enumerated route/state/viewport fixtures in [accessibility.spec.ts](../creao-design-lab/tests/e2e/accessibility.spec.ts). Any actionable violation fails; retain its rule ID, affected nodes and raw report. Never suppress a rule because it exposes a baseline defect. A missing browser, locator failure or unrendered dialog is a test error, not a violation. Review every `incomplete` category with computed styles, keyboard evidence and screenshots; incomplete is never reported as cleared. See [accessibility evidence](research/accessibility/README.md).

**VISUAL-001 — Reviewed visual baselines.** Compare three snapshots (Files list at 1280×900 and 390×900; Connectors connected-empty at 1280×900) in a fixed browser/platform, viewport, font and fixture environment using [visual.spec.ts](../creao-design-lab/tests/e2e/visual.spec.ts). Tolerance is `maxDiffPixels: 0` with per-pixel threshold `0.2`; animations off, caret hidden, clock frozen, fonts loaded. Fail on a missing baseline or a difference beyond tolerance; capture expected, actual and diff images. A deliberate change requires Product Design review of those images plus the reason; authors and agents must not regenerate baselines to pass. Baselines are per environment: an unreviewed platform baseline (currently Linux CI) fails closed until generated in the fixed environment and approved through protected review. The semantic and axe gates remain required.

### CSS and component integration

Reuse the existing palette's semantic roles. Observed from the live Widgets DOM: canvas `--color-background: #f8f6f3`, card/surface `#fefdfb`, ink/primary `#16181a`, structural border `#e6e2db`, primary foreground `#f3ecd8`, oxblood accent `#6e2f2c`. New muted/focus/backdrop tokens, spacing steps, widths and breakpoints are local proposals. A new value needs purpose, provenance and owner review.

Observed values are mapped in [tokens.css](../creao-design-lab/src/styles/tokens.css); primitive appearance belongs in [components.css](../creao-design-lab/src/styles/components.css), page/responsive composition in [layouts.css](../creao-design-lab/src/styles/layouts.css). The UI boundary owns Button/Input/Icon, pattern components own PageHeader/EmptyState/Shell, and the shared copy module owns destination labels. Extend the narrowest layer; never put feature geometry in the base Button or repeat its appearance in page CSS.

The official "sharp corners" guidance and the live UI's radius variables have different scopes: do not invent a universal radius rule; preserve approved variants. Status uses text in addition to color, and a color change alone is never proof of successful execution.

### Required state behavior

Collections distinguish initial empty, filtered empty, loading, load error and permission failure. Initial empty offers creation/connection; filtered empty offers clearing the relevant filters; load error offers retry; permission failure states the missing access and next step. A zero count never stands in for an API error.

For connectors, "No connected connectors" leads directly to the tab actually named "Connectable"; one source owns both labels. For files, "Clear search" in the "No files" state clears the query and restores known results. A file preview's close and Escape return focus to its opener. In compact lists, labels travel with their values and desktop headers disappear when the row is no longer a column grid.

These are product decisions above the component layer: valid Cards and Buttons do not make a screen composed from them valid.

### Interaction and feedback

These rules govern how a screen responds to the user. They are mandatory and review-gated unless an existing check covers them.

- **Loading.** Show a skeleton of the target layout in the same region, not a full-page spinner. If content loads in under 300ms, show no indicator (local proposal). Never show a zero count while data is still loading (STATE-001).
- **Streaming agent output.** Append content in place inside the message column. Keep the run state visible as text. Never move the composer or jump the scroll position while the user is reading earlier messages.
- **Confirmation.** Reversible actions apply immediately and offer Undo. Actions that are irreversible or have an external effect (sending, deleting, connecting, spending credits) use the Approval pattern, which names the target and the consequence. The confirming button repeats the verb, e.g. "Delete folder", never just "OK".
- **Transient feedback.** A toast confirms an action that happened away from the current focus. It must not be the only record of a failure: failures stay visible in the region they affect until the user resolves them.
- **Focus.** Opening a dialog or panel moves focus into it. Closing it returns focus to the control that opened it. Removing the focused item moves focus to the next item, or to the list if no item remains, never to `body`. This last case is a known coverage gap from the engineer experiment, and a fixture is required before release.
- **Disabled vs hidden.** Disable a control when the user can make it available, and say how, e.g. "Connect Slack to enable". Hide a control when the user can never use it in this context.

## Component consistency rules

These rules are **mandatory** for new and changed screens. CHAT-001 is **review-gated**: not yet in [rules.json](../creao-design-lab/governance/rules.json), so Product Design review blocks a violation. LAY-002 and CONTENT-001 are registered and enforced by [consistency.spec.ts](../creao-design-lab/tests/e2e/consistency.spec.ts). CMP-001 and CMP-002 are registered in rules.json and `design.md`, with their structural core enforced by browser tests in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts); the parts the tests do not assert stay review-gated. When a check lands for any other rule, add it to the registry and `design.md` together (GOV-001).

| ID | Mandatory rule | Acceptance check | Gate now → automation proposal |
| --- | --- | --- | --- |
| LAY-002 | Page header anatomy: every top-level route uses the same PageHeader — `h1` + optional description + at most one primary action at the right. Display/serif type is reserved for the chat home greeting only. | Same component import on each route; header screenshots at 1280/390 compared in review | Browser block (automated): `[LAY-002] page header anatomy is consistent across routes at 1280px / 390px` in `creao-design-lab/tests/e2e/consistency.spec.ts`; negative control 2/2 detected ([receipt](research/validation/round4-automation/negative-control.md)) |
| CMP-001 | Tabs vs FilterChips: Tabs switch views/status (single-select, `role="tab"`, `aria-selected`); FilterChips narrow results by category. Never render two visual styles for the same role on one screen. Order: search → tabs → chips → result count. | Collection fixture shows one tablist, one chip group, the required DOM order | **Browser block (automated)**: `[CMP-001] <route> tabs are single-select with exactly one selected tab at <1280 or 390>px` on /files, /connectors, /agents, /guidelines (≤1 `tablist` in main, exactly 1 on /connectors; every tab has `aria-selected`; exactly one `true` before and after a tab switch). Still review: chip group, DOM order, visual-style parity |
| CMP-002 | Action hierarchy: primary = filled Button (one per page or region); secondary = outline Button; tertiary = text link with arrow. Icon-only "+" add actions use IconButton with an accessible name and the same variant across a collection. | Primary count and IconButton variant checked per main region | **Browser block (automated)**: `[CMP-002] <route> at most one filled primary action in main at <1280 or 390>px` on the same four routes (counts `.button-primary` in `main`, fails if >1). IconButton names via A11Y-001. Still review: secondary/tertiary mapping, IconButton variant consistency, non-initial states |
| CONTENT-001 | Locale consistency: all user-visible copy in a collection uses the active locale. Catalog descriptions missing a translation use one explicit fallback (show a localized summary, or label the source language); never silently mix languages item by item. | Collection fixture in each supported locale reviewed | Browser block (automated): `[CONTENT-001] collection copy matches document locale at 1280px / 390px` in `creao-design-lab/tests/e2e/consistency.spec.ts`; negative control 2/2 detected ([receipt](research/validation/round4-automation/negative-control.md)) |
| CHAT-001 | Chat workbench composition as specified in "Chat workbench (the primary screen)": subordinate suggestions, ≤1 dismissible promo, results inside the message column, wide artifacts in panel/detail, text+color run state, inline approvals, reachable composer with grouped toolbar. | Fixtures for home, conversation, each run state and an approval request, at 1280 and 390 | Review → proposed fixtures assert composer in viewport, no second `h1`/shell inside messages, no column overflow, run-state text present |

## Worked example: composing a new feature

Synthetic brief (written for this guideline; **not an official CREAO brief**): "Users can see their scheduled agent runs and open one to see what happened."

1. **Choose patterns.** Run list → Collection. Single run → Detail/preview. A run that needs permission to act → Approval/run review rendered inline in the detail and in the originating chat.
2. **Skeleton.**
   ```text
   Shell
     PageHeader   h1 "Scheduled runs" · description ........ [Button filled: New schedule]
     Controls     Input(search) → Tabs(All | Running | Awaiting approval | Failed | Completed) → FilterChips(agent) → count
     Results      list rows: name · agent · next run · last status (text + color) · IconButton(more, named)
     State        EmptyState(initial: "New schedule") | EmptyState(filtered: "Clear filters") | error: Retry | permission
   Detail route   Back · h1 run name · status + metadata pairs · step log (Card) · Approval card if awaiting
   ```
3. **Required states (fixtures).** Initial empty, filtered empty, loading, load error, permission failure; run states Running, Awaiting approval, Failed (with reason + retry), Completed; long run/agent names; 390px compact.
4. **Rules that must pass.** Automated: DS-001, DS-002, LAY-001 (add both route fixtures), A11Y-001, A11Y-002 (add new state scans), STATE-001 (add initial/filtered recovery fixtures), RESP-001 (add compact geometry checks), GOV-001; VISUAL-001 baseline only after reviewed approval. Automated structure only: CMP-001 (one tablist, exactly one selected tab; add the new route to the CMP-001 loop) and CMP-002 (≤1 filled primary in main; add the route). Review-gated: LAY-002, the rest of CMP-001 (status as Tabs, agent as FilterChips, control order), the rest of CMP-002 (variant mapping), CONTENT-001, CHAT-001 for the inline approval.
5. **PR must attach.** Chosen patterns and affected routes/states; command receipts from the local gate; screenshots at 1280 and 390 for every state above; axe results; updated `page-states.json` entries (implemented vs not); any exception record with scope and expiry.

## Delivery mechanism

| Moment | Engineer / coding agent action | Evidence and owner |
| --- | --- | --- |
| Before implementation | Load AGENTS.md + design.md; select pattern; state affected routes/states | Change description; author owns it |
| During implementation | Reuse primitives/tokens; keep labels centralized; build representative state fixtures | Source review; frontend owner owns adapter and scopes |
| Local gate | Run typecheck, lint, static design check, build and browser tests | Command receipts plus screenshots; author owns remediation |
| Rule/shared-system changes | Run negative mutations and positive controls; preserve original failures | Machine results with exact denominator; design + frontend owners review |
| PR gate | Execute same commands against candidate commit; upload reports even on failure | Required status check; reviewer validates screenshots and exceptions |
| Release gate | Publish only an artifact produced by the accepted candidate; smoke-test deployed routes/states | Protected deployment/environment; release owner records commit/artifact identity |

Use Node 24 and the committed lockfile. From `creao-design-lab/`, with port 3100 free, run the complete local gate in this order:

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

The browser gate runs against the production build just produced; Playwright manages that server and fails if another process owns the port. The mutation runner uses isolated candidate copies and its own servers; do not edit the shared baseline while it runs. On Linux CI, install with `npx playwright install --with-deps chromium` and use the bundled Chromium (no `PW_CHANNEL`).

Where installed Chrome is the recorded local browser, replace the last two commands with:

```sh
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
PW_CHANNEL=chrome npm run test:mutations
```

`npm run test:e2e` excludes visual tests. `npm run test:a11y` reruns the axe subset alone; `npm run test:visual` is the separate visual gate:

```sh
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:a11y
PW_CHANNEL=chrome VISUAL_ENV=<os>-<arch>-<kernel>-<browser>-<version> PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
```

`VISUAL_ENV` must match the actual environment (the test rejects a mislabeled platform); Linux visual bootstrap stops for baseline review. Record browser/channel and version in each receipt. A browser download/setup failure is an environment error, not a design-rule rejection, and this command list does not itself claim success.

Static checks parse CSS and TypeScript/JSX rather than trusting an author's compliance flag; runtime checks inspect actual names, headings, state transitions and geometry; screenshots support human review of hierarchy and field meaning. The registry's declared scopes and limitations prevail over broad claims such as "AI reviews the design."

CI/CD must use protected required checks and ownership of governance files: anyone who can remove the checker or rewrite the workflow can bypass an unprotected rule, and `AGENTS.md` is an instruction channel, not a security boundary. Remote branch protection, CI runs and deployment are separate integration work and are not claimed complete from local success.

## Exceptions and maintenance

An exception record contains exactly `id`, `ruleId`, exact `path`, `reason`, `owner`, `approvedBy` and `expires`; route/state scope, tracking and compensating verification go in the reason/review record. No blanket app-wide exceptions. Expiry fails closed (YYYY-MM-DD, end of UTC date). An `approvedBy` string does not prove approval; rely on protected review. The legacy file-waiver schema supports exact-file DS-001/DS-002 waivers only; anything else fails closed. Broader human acceptance follows [Human exceptions and scoped bypass](../creao-design-lab/governance/human-exceptions-policy.md).

### Human override and CI acceptance

An authorized human may accept a documented design tradeoff for an important feature. Standard exceptions need the designated Product Design and Frontend approvers (a registered dual-role owner may satisfy both), last at most seven days, and forbid self-approval. A CTO or delegated release owner may approve an emergency exception of at most 24 hours with compensating verification, rollback, a repair owner and independent follow-up; any requester/approver overlap must be visible. Engineers and agents cannot grant themselves these roles.

Each approval is scoped to one repository and target SHA, policy/request/evidence digests, the observed rule/check/finding IDs (including browser/axe findings and visual diffs), exact files or route/state/viewport, and a UTC expiry. Original tests still run and their failures stay in the audit; the candidate is labeled `accepted_with_exceptions`, never `passed`. New failures, changed scope/commit, expiry or revocation invalidate acceptance. Missing evidence, infrastructure failures and invalid approvals cannot be waived.

The coordinator workflow is `REQUEST_DESIGN_EXCEPTION` → verified human `APPROVE_DESIGN_EXCEPTION` → `EVALUATE_DESIGN_EXCEPTION`, with `REVOKE_DESIGN_EXCEPTION` available; these are protocol instructions until mapped to tested commands/CI inputs. The linked policy supplies the exact approval wording. Once valid authorization is recorded, engineers continue within that scope without repeated requests.

CI keeps raw evidence jobs and a protected final decision gate that distinguishes `passed`, `accepted_with_exceptions`, `rejected` and `blocked`; required checks must allow the scoped decision path rather than forcing waived raw checks green. A dispatch input or `approvedBy` string does not authenticate a human: use verified platform approval and protected role mapping. Unconfigured approval adapters fail closed; local fixtures are labeled simulation. Before claiming the path works, test legitimate acceptance, expiry/revocation, unauthorized roles, candidate/scope mismatch, mixed unapproved failures and evidence preservation.

Ownership: the frontend owner reviews failed gates, new route/state gaps and expiring exceptions daily; the designer reviews visual diffs and recurring pattern deviations. Escalate new user-facing failures to the feature owner with evidence and a due date. (This assigns responsibility; it schedules no automation.)

Review recurring exceptions and checker false positives together. Revise a rule when evidence shows it is wrong or a reusable pattern is missing, adding both an allowed and a violating example. Product Design owns pattern quality and wording; the frontend owner owns adapter/checker accuracy; the CTO resolves cross-team or release-policy conflicts.

## Proving the gate

The [compliance audit](compliance-audit.md) maps each observed defect to its rule and pre-ship detection path. The lab validates those paths with real source changes:

- Negative controls inject failures such as a literal color, raw control, missing heading/name, inert recovery, destination mismatch, compact-layout regression and stale governance record.
- Positive controls make legitimate changes within the contract and must pass; a gate that blocks everything is useless.
- Independent engineer agents implement a bounded feature in isolated copies against the same checks; their results are reported separately from deterministic fixtures.

Report **killed**, **survived**, **invalid** and **error** separately. Only a rule-attributed rejection of a valid candidate counts as killed; a compile failure or missing dependency does not. Retain survivors and first-round failures. No finite suite proves future code cannot evade the rules.

**Evidence pointers.** Receipts, denominators and per-phase boundaries are authoritative in [validation results](validation/validation-results.md); summarized here: `test:e2e` holds 58 cases (42 design-rule tests: 22 original + 8 CMP-001 + 8 CMP-002 + 2 LAY-002 + 2 CONTENT-001, plus 16 axe scans); latest run 58/58 (research/validation/round4-automation/) and visual 3/3 (research/validation/round3-english/), with the three-screen visual gate counted separately and the `test:a11y` rerun not counted as extra coverage; the [state inventory](../creao-design-lab/governance/page-states.json) lists 31 entries (22 implemented, 9 not), a coverage plan rather than a test count; the original contract had eight rule IDs, A11Y-002 and VISUAL-001 were added later, and the retained v1 registry and receipts are history, not proof that enhanced checks ran; the source defect was captured at 390 × 844 while tests use height 900; the reviewed macOS visual namespace is `darwin-arm64-25.6.0-chromium-154.0.8037.98` and must not be copied into Linux CI. CMP-001/CMP-002 receipts are in [round2-cmp](research/validation/round2-cmp/).

The guideline is ready to load and execute in the local adapter. Adopting it in CREAO's repository means binding the approved imports, tokens and fixtures to the real library, then enabling protected CI and release policy without weakening the product contracts.

## Agent / PR checklist

- MUST name the canonical pattern(s) and affected routes/states before writing code.
- MUST compose Shell, PageHeader, Tabs, FilterChips, Input, Card, EmptyState, Button/IconButton from the approved library (DS-002).
- MUST use registered semantic tokens only; new values are proposals with owner review (DS-001).
- MUST render exactly one visible matching `h1` per top-level route via the shared PageHeader (LAY-001, LAY-002).
- MUST keep at most one filled primary Button per page or region; secondary outline, tertiary text link (CMP-002).
- MUST order collection controls search → Tabs → FilterChips → count; Tabs for views/status, chips for categories (CMP-001).
- MUST give every icon-only control an accessible name (A11Y-001).
- MUST show status as text plus color; never color alone.
- MUST implement initial empty, filtered empty, loading, error and permission states with working next steps (STATE-001).
- MUST reuse shared copy for destination labels and keep one locale per collection with an explicit fallback (NAV-001, CONTENT-001).
- MUST keep chat results inside the message column, approvals inline, composer reachable (CHAT-001).
- MUST NOT add a second app shell, navigation or page `h1` inside a chat result or preview.
- MUST NOT use display/serif type outside the chat home greeting (LAY-002).
- MUST NOT hide overflow globally or introduce horizontal page scroll at 320–1280px (RESP-001).
- MUST NOT regenerate visual baselines or add exceptions to make a gate pass (VISUAL-001, GOV-001).
- MUST NOT claim review-gated rules (LAY-002, CONTENT-001, CHAT-001) or the unautomated parts of CMP-001/CMP-002 (chip grouping, control order, variant mapping) as automatically verified.
- VERIFY BY running the full local gate in order (typecheck, lint, test:design, check:design, build, test:e2e).
- VERIFY BY adding route/state fixtures for every new route and state (LAY-001, A11Y-002, RESP-001).
- VERIFY BY attaching screenshots at 1280 and 390 for each required state.
- VERIFY BY recording command receipts, browser/channel and version in the PR.
- VERIFY BY updating `page-states.json` and keeping `rules.json` and `design.md` in sync when a rule changes (GOV-001).
