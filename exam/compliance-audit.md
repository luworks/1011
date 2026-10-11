# CREAO Product Design Compliance Audit

Audit date: 11 October 2026 (PDT). Standard: [design-system-guideline.md](design-system-guideline.md) and the executable [design.md](../creao-design-lab/design.md), version 0.2 (with retained v1 experiment history).

**Finding:** the audit records **ten findings, AUD-01 to AUD-10** (one P1, five P2, four P3). AUD-01 to AUD-05 are directly evidenced issues in page identity, empty-state navigation/recovery and compact file layouts; AUD-06 is a lower-priority application of the stricter in-state recovery rule to file search. AUD-07 to AUD-10 are screenshot-evidenced cross-screen consistency findings: mixed-locale connector copy, two competing selector styles on Connectors, an inconsistent action hierarchy across routes, and upsell surfaces fused to the chat composer. AUD-07 and AUD-10 are judged against review-gated rules; AUD-08 and AUD-09 against rules whose structural core is now automated in the lab. All ten translate into pre-release checks without redesigning CREAO's token or component library.

**Evidence status:** the source-product observations below are complete. Local receipts are summarized separately below; the runtime-mutation run is explicitly partial at the user-requested closeout, while the visual negative control is archived. No claim is made that these checks already run inside CREAO's production repository, that the live defects were fixed, or that CREAO's unpublished internal rules were violated.

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

## Method and boundaries

The user confirmed that the linked live product is the complete supplied resource set. This audit therefore uses captured live screens, their accessibility/DOM evidence and public Widgets documentation. Deep captures were taken on 11 October 2026, 13:51–13:54 PDT; see the [capture manifest](research/deep/capture-manifest.json). Earlier desktop captures are retained under `research/screenshots/`. The inspected narrow source screen is 390 × 844; the local automated fixture uses 390 × 900, with desktop checks at 1280 × 900.

Live captures were taken with CREAO's zh-CN locale; UI strings are quoted by English meaning; the raw captures linked as evidence retain the original text. The local lab's UI copy is English, so lab-expected strings below are its literal labels.

Three evidence lanes are kept separate:

1. **Observed product defect:** a screenshot, DOM record or accessibility tree establishes what the live product did in the captured state.
2. **Local enforcement proof:** a synthetic local implementation, the checker source and a valid mutated candidate show whether the proposed gate can detect that defect class. Actual run results belong in the receipt table; test source alone is not a passing run.
3. **Production adoption:** bind fixtures to CREAO's real routes/library, require protected checks and verify the deployed candidate. This is not performed by the lab.

Severity is a proposed triage decision, not a measured incident rate: P1 means a control cannot be reliably identified in the captured accessibility state; P2 means navigation, comprehension or recovery is materially weakened; P3 means a stricter proposed consistency improvement where a usable alternative exists. These findings are blocking under the proposed rule once adopted, except that prioritization and time-limited exceptions are owned by Product Design and Engineering.

## Findings at a glance

| Finding | Screen/state | Rule | Priority | Evidence | Proposed pre-ship detection |
| --- | --- | --- | --- | --- | --- |
| AUD-01 | Files, desktop list | LAY-001 | P2 | Visual title is a button; no headings in captured DOM | Count visible level-one headings within main and compare route identity |
| AUD-02 | Connectors, Connected (0) | NAV-001 | P2 | Guidance names an "Available" tab; the actual tab is labelled "Connectable" | Assert canonical destination name in guidance and selected destination after action |
| AUD-03 | Same connector empty state | STATE-001 | P2 | Empty state contains only heading/text; no in-state next action | Trigger zero connections, invoke recovery action, assert connectable services appear |
| AUD-04 | Files, 390px | A11Y-001 | P1 | Folder button's text is hidden; icon is hidden from accessibility; no alternate name | Compute the visible control's accessible name at compact width |
| AUD-05 | Files, 390px list | RESP-001 | P2 | Desktop-style headers remain above a differently stacked metadata layout | Hide stale headers, preserve known label/value pairs, check field geometry and review screenshot |
| AUD-06 | Files, search with no matches | STATE-001 | P3 | Empty region has no action, although the search box does have a clear affordance | Require an in-state clear action and assert query reset plus restored results |
| AUD-07 | Connectors, catalog grid | CONTENT-001 | P2 | zh-CN UI; most visible card descriptions are English, while Instagram and Box are in the UI locale | Review-gated; proposed rendered-text locale scan per catalog item |
| AUD-08 | Connectors, catalog controls | CMP-001 | P3 | Status tabs and category chips are adjacent selectors with different styles and unclear scope | Partly automated in the lab: `[CMP-001]` browser tests (tablist/selection structure); chip style and scope still review-gated |
| AUD-09 | Chat home, Files, Agents, Connectors | CMP-002 | P3 | Filled, outlined, ghost, text-arrow and icon-only actions with no consistent primary/secondary mapping | Partly automated in the lab: `[CMP-002]` browser tests (≤1 filled primary per main); variant mapping still review-gated |
| AUD-10 | Chat home | CHAT-001 | P3 | Dismissible team upsell fused to the composer, repeated in sidebar card and header plan control | Review-gated; proposed composer-region composition check plus screenshot review |

AUD-02 and AUD-03 occur in one state but are different failure conditions: fixing the wording does not add a recovery action, and adding a button does not guarantee it reaches the correctly named destination. AUD-04 and AUD-05 similarly expose different consequences of the same compact breakpoint.

AUD-07 to AUD-10 are visual-composition findings taken from desktop screenshots. CONTENT-001 and CHAT-001 (AUD-07, AUD-10) remain newly proposed, review-gated rules whose automation is named below but is not registered in [rules.json](../creao-design-lab/governance/rules.json). CMP-001 and CMP-002 (AUD-08, AUD-09) are now registered there with browser tests that cover their structural core in the lab; the rest of each finding is still review-gated, as stated below. These tests run against the local lab, not the live CREAO product, and the lab's `/connectors` has no filter-chip group.

## AUD-01 — Files loses semantic page identity

**Observed state.** On `https://agent.creao.ai/files`, the desktop screen displays "Files" as the page title. The saved [DOM record](research/files-dom.json) reports `headings: []` and identifies the title as a `BUTTON` with that text. The [desktop screenshot](research/screenshots/03-files.png) shows the visual title in the expected page-header position.

**Violation.** LAY-001 requires one visible `h1` identifying each governed top-level page within its main region. A large text button does not satisfy that semantic contract. The evidence is stronger than a screenshot-only judgment because the element and empty heading list were inspected.

**User impact.** A person navigating by headings cannot identify the page through the expected heading structure. Future feature implementations also lack a consistent semantic page-header contract. This audit does not claim a measured screen-reader incident or universal failure across all routes.

**Exact correction.** Render the page identity through `PageHeader` / a semantic `h1`. If the existing title also opens navigation or folder selection, retain that interaction in a separate named control rather than making the page identity only a button. Use lower-level headings for previews and sections.

**How it is caught before shipping.** In [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts), `[LAY-001] /files one visible page heading at 1280px` and its compact counterpart assert exactly one main region, one visible level-one heading and the expected name "Files". A candidate that reproduces the observed structure has zero matching headings and fails the rule assertion. This requires DOM inspection; the CSS token check would not detect it.

**Adoption boundary.** The local test targets `/files` in the prototype. CREAO can use the same assertion on its real route with authenticated fixture data. That production integration has not occurred.

## AUD-02 — Connector guidance names a tab that is not present

**Observed state.** On `https://agent.creao.ai/integrations`, the selected tab is "Connected (0)". The empty-state description says "Go to the Available tab to connect services." The actual destination is labelled "Connectable", alongside "All", "Built-in" and "Connected". Both the [screenshot](research/screenshots/05-connectors-empty.png) and [accessibility tree](research/connectors-empty-ax.txt) preserve the mismatch.

**Violation.** NAV-001 requires destination guidance to use the real destination's name. "Available" and "Connectable" might be semantically related, but asking the user to locate a named tab that does not exist creates avoidable uncertainty.

**User impact.** A first-time user must infer which tab the instruction means. A coding agent can repeat stale copy when adding or renaming navigation unless copy ownership is explicit.

**Exact correction.** Put the canonical destination label in the shared copy module and compose both the tab and recovery guidance from it. Use an action such as "Browse connectable services". Its handler activates the connectable tab, and the panel must show eligible services.

**How it is caught before shipping.** `[NAV-001] empty-state destination copy matches actual available tab` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) finds the actual tab named "Connectable", enters the connected-empty state, checks that its description contains "Connectable" and does not contain the obsolete "Available", then invokes recovery and asserts `aria-selected="true"` on the target. Copying the observed wording into the local candidate fails the description assertion. Wrong routing fails the selected-state assertion.

**Automation limit.** The current test deliberately uses a canonical English contract (locale fixtures required for other locales). It does not prove all locales or future destination renames are correct, and it does not statically prove all strings originate in one module. Shared-source reuse is a source-review requirement; a legitimate rename requires a reviewed contract update.

## AUD-03 — Connector empty state does not offer a direct next step

**Observed state.** The same [Connected (0) screenshot](research/screenshots/05-connectors-empty.png) shows an icon, "No connected connectors", and a sentence directing users elsewhere. The matching [AX subtree](research/connectors-empty-ax.txt) contains a heading and text without a button/link inside the empty state. Tabs remain available outside it.

**Violation.** STATE-001 requires a recoverable empty state to include an actionable next step within that state. A distant tab is an available workaround, but it does not fulfill the proposed composition contract.

**User impact.** The screen explains absence without completing the recovery path. Users have to reinterpret the explanation as an instruction to navigate manually; the naming mismatch in AUD-02 compounds the problem.

**Exact correction.** Retain the empty-state title and explanatory purpose, add "Browse connectable services", and wire it to the actual connectable panel. Do not launch OAuth merely because the user asks to browse services. Use a distinct explicit action to connect an individual service.

**How it is caught before shipping.** `[STATE-001] connector empty state action reaches available services` triggers the fixture with zero connections, requires the recovery button to be visible, clicks it, asserts the connectable tab is selected and an actual service action appears, then verifies the recovery button disappears. A missing or inert button fails. A compliance attribute or snapshot of a button would not be sufficient.

**Important distinction.** We are not claiming users were completely trapped: the top-level tabs were present. The finding is a specific violation of the adopted in-state recovery rule. Initial empty-state recovery already exists elsewhere in the product: the [agents screen](research/screenshots/02-agents-empty.png) supplies a creation CTA.

## AUD-04 — Compact "New folder" button loses its accessible name

**Observed state.** On Files at 390 × 844, the [screenshot](research/deep/14-files-mobile.png) shows a folder-plus icon near Upload. The saved [mobile DOM record](research/deep/files-mobile-dom.json) identifies the button with text "New folder", but that text is in a `SPAN` with `display: none`. Its SVG has `aria-hidden="true"`; `aria-label`, `aria-labelledby` and `title` are absent. The button rectangle is visible, 41 × 36 CSS px at x=250, y=56.

**Violation.** A11Y-001 requires visible interactive controls to retain an accessible name after responsive changes. Hidden text plus an accessibility-hidden icon supplies no usable name in this recorded structure. This is a specific naming finding; button dimensions alone are not used to make a target-size compliance claim.

**User impact.** A user relying on accessible control names cannot reliably identify the action. Desktop-only checks would miss the responsive change that removes the label.

**Exact correction.** Retain the name through an `aria-label` of "New folder" (in the active locale) or a genuinely visually hidden text treatment that stays in the accessibility tree. Preserve the decorative icon's hidden state. If text remains visible, it must match the action's accessible name.

**How it is caught before shipping.** `[A11Y-001] /files visible controls retain accessible names at 390px` iterates visible interactive controls and calls Playwright's accessible-name assertion, requiring a non-whitespace result. A local mutation that removes the name while hiding the visible text should fail this specific assertion. The desktop counterpart verifies that the name also exists before collapse.

**Automation limit.** A non-empty but misleading name could pass this particular check. Human review must assess meaning, and separate interaction tests must cover keyboard activation/focus. This finding does not establish a complete WCAG audit.

## AUD-05 — Compact file metadata no longer corresponds to the headers

**Observed state.** In [the 390px Files capture](research/deep/14-files-mobile.png), the "Name" header wraps into separate characters, while "Modified", "Size" and "Source" remain in a desktop-style header row. File entries below use another layout: the name appears on its own row, modification time and size sit underneath, and source occupies a further line. The spatial header-to-value mapping has broken.

**Violation.** RESP-001 requires field identity to survive responsive transformation. Keeping table-like headers above values that no longer occupy those columns makes the page look structurally tabular while asking users to infer a different reading order.

**User impact.** Values become harder to scan and compare, particularly when fields contain unfamiliar formats. The evidence establishes layout ambiguity; it does not establish an actual stored-data mix-up.

**Exact correction.** At the compact breakpoint, remove the desktop header and render each item as a name followed by visible metadata label/value pairs. Keep each label and value in the same field group. Maintain a full name through wrapping or an accessible detail/preview path. Desktop should retain the aligned column structure.

**How it is caught before shipping.** `[RESP-001] file list preserves field labels and fits 390px viewport` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) requires the desktop header to be hidden, metadata labels to be visible, item bounds to remain inside the viewport, and metadata rectangles not to overlap. It also checks a known file against [an independent label/value fixture](../creao-design-lab/tests/e2e/fixtures/file-contract.ts): modification time, size and source must remain correctly paired. It then checks that desktop headers return at 1280px and captures both layouts.

**Why both kinds of checks matter.** Geometry alone can pass a cleanly laid out but incorrectly paired value. The independent fixture catches this semantic mapping error. Neither assertion proves all visual reading-order decisions: a reviewer still inspects the screenshots. The live screen's first failure against this contract would be the visible stale header; reproducing only metadata value swaps should fail the separate fixture comparison.

**Coverage boundary.** The local automatic test is at 390 × 900, not the exact original 390 × 844 height. A production rollout should include that captured viewport, long names, supported locales and intermediate breakpoints; no all-device claim is made here.

## AUD-06 — File-search recovery is outside the empty region

**Observed state.** Searching for a nonmatching term produces "No files" with the more precise description "No files or folders match the search." The [screenshot](research/deep/15-files-no-results.png) shows no action inside the empty region, **and does show a clear affordance at the right end of the search box**. The [AX capture](research/deep/15-files-no-results.txt) records the no-results message.

**Violation and priority.** This is a P3 application of the proposed STATE-001 in-state recovery contract. It is weaker than AUD-03 because the user already has an obvious recovery affordance adjacent to the active query. It must not be described as "there is no way to clear the search".

**Exact correction.** Prefer an unambiguous "No matching files" title, retain the explanation, and add "Clear search" inside the empty state. Keep the search-box clear control as well. If multiple filters contribute to zero results, the action must state and clear the intended filters, rather than silently clearing unrelated user context.

**How it is caught before shipping.** `[STATE-001] file search no-results action restores actual entries` enters a deterministic unmatched query, asserts zero result items, invokes the clear action within the empty region, asserts the query becomes empty and a seeded result returns. A nearby clear button outside the region does not satisfy the locator contract. This catches the proposed consistency requirement; it is not proof the original product had no recovery affordance.

## AUD-07 — Connector catalog mixes languages item by item

**Observed state.** The [Connectors screenshot](research/screenshots/04-connectors.png) is in the zh-CN UI locale: navigation, page title "Connectors", search placeholder "Search connectors", status tabs, category chips, "45 results" and the featured carousel copy are all in that locale. In the catalog grid below, descriptions alternate by item: Shopify, Google Ads, Slack, Notion, Gmail, Asana, Canva and Discord are English (for example "Manage products, orders, customers, and your online…"), while Instagram ("Read an Instagram professional account's…") and Box ("Search, read, upload, download and share Box files and folders…") are in the UI locale. The Shopify featured card above is in the UI locale while the Shopify grid card below is English.

**Violation.** CONTENT-001 requires user-facing copy within one view to follow the active UI locale, with a declared fallback rather than per-item mixing. Product names (Shopify, Notion) are legitimately untranslated; the finding concerns the descriptive sentences.

**User impact.** A reader who relies on the UI locale must scan a grid where most descriptions are in another language, and the same service is described in two languages on one screen. Comparison across cards is harder because the reading mode changes item by item. No claim is made about how many users cannot read English.

**Exact correction.** Source connector descriptions from a localized catalog keyed by connector ID and UI locale. When a translation is missing, apply one declared fallback (for example, show the localized category label plus an untranslated-content marker) and log the gap, rather than silently mixing languages. Featured and grid entries for the same connector must resolve from the same localized record.

**How it is caught before shipping.** Today this is review-gated: Product Design checks catalog screenshots in each supported locale. Proposed automation (not yet in rules.json): a rendered-text locale scan that, for each catalog item under `zh-CN`, flags descriptions whose script does not match the UI locale after excluding an allowlist of product names, plus a contract test that featured and grid entries of the same connector resolve to the same description key.

**Automation limit.** Script detection cannot judge translation quality or mixed-language sentences that are intentionally bilingual. Content fixtures must include the real catalog, because a synthetic fixture with complete translations would pass trivially.

## AUD-08 — Two adjacent selector styles with unclear scope on Connectors

**Observed state.** In the same [Connectors screenshot](research/screenshots/04-connectors.png), the row containing the search box also holds plain text tabs "All / Connectable / Built-in / Connected (0)", with "All" marked by an underline. Directly below, a second row holds category chips "All categories / Business / E-commerce / Marketing / Social media / Productivity", with "All categories" marked by a filled pill. Both rows filter the same grid; "45 results" sits at the right of the chip row.

**Violation.** CMP-001 requires tabs to switch between peer views and filter chips to narrow a collection, with a clear visual hierarchy when both appear. Here two selectors of similar size and weight sit in adjacent rows, with different selected-state treatments, and nothing on screen states whether the status tab and category chip combine or reset each other.

**User impact.** Users must infer which control is the primary view switch and whether a category persists when switching status. The connected-empty state in AUD-02/AUD-03 is reached through these tabs, so their role matters for recovery. No combination defect was exercised; the finding is about ambiguous composition.

**Exact correction.** Promote status to a clearly primary tab list (placed above the search, with `role="tablist"` and selected-state semantics), keep categories as a filter-chip group scoped to the active tab, and keep the result count next to the filter that changes it. Document whether category selection persists across status tabs and preserve that behavior.

**How it is caught before shipping.** Automated part (registered as CMP-001 in rules.json, browser layer): `[CMP-001] <route> tabs are single-select with exactly one selected tab at <1280 or 390>px` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) runs on /files, /connectors, /agents and /guidelines. It requires exactly one `tablist` in main on /connectors (at most one elsewhere), `aria-selected` on every tab, and exactly one `aria-selected="true"` tab before and after switching tabs. Receipt: 38/38 passed in [e2e-design.log](research/validation/round2-cmp/e2e-design.log) (system Chrome, production server), including 8/8 CMP-001. No CMP-001 negative control has been run yet. Still review-gated: the filter group with `aria-pressed` chips, search → tabs → chips → count DOM order, distinct visual styles and the category/status persistence rule. The lab has no chip group, so the defect AUD-08 actually observed (two adjacent selector styles) is not detected by this test.

**Automation limit.** Roles and order can be asserted; whether the visual hierarchy reads as primary versus secondary still needs screenshot review.

## AUD-09 — Action styles do not map consistently to action importance

**Observed state.** Across top-level screens the same importance level uses different treatments:

- [Chat home](research/screenshots/01-chat.png): two adjacent suggestion cards each carry a filled black button ("Try Visual Studio →", "Try /slide"), so the region has two visually equal primary actions; the promo strip uses a text link "Create team →", and the "Popular agents" section uses another text link "Explore →".
- [Files](research/screenshots/03-files.png): the header pairs a ghost icon+text action ("New folder") with a filled black "+ Upload".
- [Agents empty](research/screenshots/02-agents-empty.png): the header has an outlined icon+text "Import", and the empty state has a filled black "Create your first agent" without an icon.
- [Connectors](research/screenshots/04-connectors.png): every catalog card uses an outlined square icon-only "+" button, while the featured carousel cards show no explicit action.

**Violation.** CMP-002 requires one primary action per region and a stable mapping from importance to variant (primary filled, secondary outlined/ghost, tertiary text link), including consistent icon and arrow use. The screens above use the filled variant for repeated card actions, alternate trailing arrows and leading icons without a rule, and use icon-only buttons for the main per-item action on Connectors.

**User impact.** Visual weight stops predicting importance, so users cannot rely on "filled means the main task". On the chat home, repeated filled buttons compete with the composer. Each new feature is likely to pick another variant because no rule is visible in the product. The accessible names of the connector "+" buttons were not captured, so no A11Y-001 claim is made here.

**Exact correction.** Use the library `Button` variants by role: one filled primary per region (Files "Upload", Agents empty "Create your first agent"); outlined secondary for card-level actions such as suggestion cards and connector "Connect"; text links with trailing arrow only for navigation ("Explore →"). Give connector card actions a visible label or a tooltip plus an accessible name such as "Connect Shopify".

**How it is caught before shipping.** Automated part (registered as CMP-002 in rules.json, browser layer): `[CMP-002] <route> at most one filled primary action in main at <1280 or 390>px` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) counts `.button-primary` (the Button primitive's `variant="primary"`) in the main landmark of /files, /connectors, /agents and /guidelines and fails above one. Receipts: 8/8 CMP-002 passed within the 38/38 run in [e2e-design.log](research/validation/round2-cmp/e2e-design.log). [Negative control](research/validation/round2-cmp/negative-control.md): two primaries injected on /connectors → 2 failed (1280 and 390, received 2), 6 passed; after revert, 8/8 passed. Icon-only names stay covered by A11Y-001. Still review-gated: the secondary/tertiary variant mapping, the variant inventory, primary-styled lookalikes without the class, sub-regions, and non-initial states (files create form, agents detail).

**Automation limit.** A checker can count variants but cannot decide which action is semantically most important; that mapping must be declared per screen and reviewed. This is a finding about visible composition, not a claim about which component or code path renders each button.

## AUD-10 — Chat home places upsell surfaces against the composer

**Observed state.** The [Chat home](research/screenshots/01-chat.png) shows the serif greeting "Y, what can I help you with?" and the composer. A promo strip is attached directly under the composer card, sharing its edge: "Using it with a team? Create a team and get 30 free credits… buy seats for another 100 bonus credits." with "Create team →" and a close "×". The same offer appears again in the sidebar bottom card "Create team · 30 free credits — try…", and the header shows "Free plan | Upgrade". Further down the same viewport, two suggestion cards carry filled buttons (AUD-09).

**Violation.** CHAT-001 requires the composer to be the single primary task on the chat workbench, with commercial or onboarding prompts placed in a separate, non-attached region and not duplicated within one viewport. Here the upsell is visually fused to the composer, and the same offer appears twice in one viewport.

**User impact.** The input area reads as a composer plus advertisement, which adds reading load at the moment the user is formulating a request, and the duplicated offer adds noise without adding information. The strip is dismissible and the composer remains the largest element, so this is P3; no effect on task completion was measured.

**Exact correction.** Detach the strip from the composer card (separate container with its own spacing, or move it to the sidebar card only), show one instance of the same offer per viewport, and remember dismissal. Keep the header plan control as the persistent upgrade entry.

**How it is caught before shipping.** Review-gated with a chat-home screenshot in the visual gate. Proposed automation (not yet in rules.json): assert that the composer region contains only composer controls (no promotional link/button descendants or attached siblings sharing its container), and that a given promotion ID renders at most once per route.

**Automation limit.** A DOM check can detect attachment and duplication but not whether a separate promotion is still too prominent; that remains a Product Design judgment.

## Page header anatomy — considered, not raised as a separate finding

LAY-002 (shared page-header anatomy) was checked across the captured routes. Files, Agents and Connectors show the same visual pattern: a bold sans title at top left, with route actions at top right where present. The chat home uses a serif greeting instead of a title, which is a deliberate workbench treatment rather than evidence of drift. The only evidenced header deviation is Files' semantic structure, already recorded as AUD-01 under LAY-001; no additional LAY-002 finding is made from screenshots alone.

## Positive evidence and findings deliberately not made

| Evidence | Useful existing behavior | What is not inferred |
| --- | --- | --- |
| [Agents initial empty](research/screenshots/02-agents-empty.png) and [create handoff](research/deep/06-agent-create-handoff.png) | Explanation and creation action; creation starts in chat with a prefilled request | No real agent was created or run; success/failure states remain untested |
| [Skills compact layout](research/deep/13-skills-mobile.png) | Sidebar collapses and cards form a readable single column with visible actions | No blanket responsive approval for other routes |
| [Slack setup](research/deep/11-slack-detail.png) | Return navigation, explicit page identity, operational scope and a setup action | OAuth, permission changes and connection success were not exercised |
| [Autonomy menu](research/deep/07-autonomy-menu.png) | The two authority levels explain their consequences | No verification that every real external operation honors those settings |
| [Widgets gallery](research/deep/10-widgets-layout.png) and [CSS snapshot](research/deep/widgets-dom.json) | Existing components and design variables are directly evidenced | No private component imports, source reuse policy or token usage can be recovered from appearance alone |
| [File preview](research/deep/09-file-preview.png) and [video settings](research/deep/17-video-default-settings.png) | Overlay/detail and configuration patterns are already present | Screenshot appearance does not prove focus trapping, focus restoration or keyboard behavior |

No finding is made that engineers hard-coded colors or bypassed CREAO's internal components. DS-001 and DS-002 are preventive gates demonstrated on the local adapter; only repository source can establish such a violation in CREAO itself. Similarly, mixed radii alone do not establish incorrect component usage: the official Dashboard description and general app controls have different scopes. AUD-07 to AUD-10 are therefore stated as findings about visible composition (language, selector roles, action hierarchy and placement on screen), not about hard-coded values or which internal component rendered an element. Screenshot-only color estimates are not accepted as a contrast audit.

## How the worked audit becomes a release gate

The guideline is loaded through [AGENTS.md](../creao-design-lab/AGENTS.md), styles are indexed from [design.md](../creao-design-lab/design.md), objective checks are implemented in [check-design.mjs](../creao-design-lab/scripts/check-design.mjs) and [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts), and scope/limits are recorded in [rules.json](../creao-design-lab/governance/rules.json).

For each candidate, the author declares affected pattern/routes/states, runs type/lint/static checks and a production build, then runs browser fixtures against that candidate. CI must do the same on the candidate commit, retain failure evidence and require owner review for visual/pattern judgments and governance changes. A valid, rule-attributed failure blocks release; exceptions must be explicit, scoped and current. Local instruction files and editable CI configuration alone cannot prevent deliberate bypass.

To validate the gate, mutations must change real source in isolated copies. Negative candidates recreate relevant failure conditions; positive candidates demonstrate allowed changes can pass. Independent engineer agents exercise the same contract on a feature task. Results must be reported separately: a predesigned mutant and an independent engineer's implementation are different experiments.

The denominator must include all valid injected negative candidates. Report `killed`, `survived`, `invalid` and `error` separately. A compile failure, browser-install problem or timeout is not a rule-attributed kill. A survivor is evidence about the checker's boundary and must remain in the record even if a later checker revision detects it. Independent experiments must not modify checkers or tests to make their own changes pass.

## Additional findings in the local prototype — not CREAO production

The following were found while evaluating our implementation. They must not be attributed to the captured live CREAO product or counted as additional source-product audit findings.

| Local finding | Evidence and correction | Rule / acceptance |
| --- | --- | --- |
| File columns overflowed at 800px despite passing the initial narrow/desktop fixtures | Manual review measured 806px document width at an 800px viewport. Moving collection reflow to 900px restored 800px width; shell collapse remains 760px. Added 320/800px regressions. | RESP-001; retain before/after screenshots and geometry receipts |
| Static native-control aliases escaped the first checker | First deterministic run killed 5/6 negatives; a `const` alias survived. Lexical symbol resolution was added; second run killed 6/6 while both positive controls still passed. | DS-002; keep original survivor and second-run evidence separately |
| Guidelines' scrollable tables were not keyboard-focusable | axe reported `scrollable-region-focusable`; tables were made focusable. Subsequent scans also exposed scrollable `pre` blocks, which were corrected rather than suppressing the rule. | A11Y-002; final 16/16 scans pass; ArrowRight increased real table/pre scroll positions by 35/30px |
| View-switch container used an unsupported ARIA attribute/role combination | axe incomplete review identified `aria-label` on a roleless div; adding `role=group` made the intended semantics explicit. | A11Y-002; document manual incomplete review as well as automatic results |
| A new feature's focus lifecycle escaped the existing automatic tests | Engineer B's removal of the currently focused marked item moved focus to BODY. Manual interaction found this even though the feature's pointer action worked. | Existing automatic checks did not cover this new dynamic focus transition; retain as a coverage gap |

The [accessibility evidence record](research/accessibility/README.md) preserves three scan rounds. Initial route-announcer locator conflicts were test errors, not product violations. The final scan still required manual review of dialog contrast and 61 clipped Guidelines cells; computed styles and representative revealed-cell screenshots support that review. It does not claim every cell was individually screenshotted or that axe automatically confirmed all incomplete results. Automated zero violations is not full WCAG certification.

## Local validation results and distinct denominators

Detailed immutable reports, command logs and history are indexed in [validation-results.md](validation/validation-results.md), [accessibility/README.md](research/accessibility/README.md), and the [independent engineer experiment review](validation/engineer-experiment-review.md). Results from different candidate revisions and gate versions are not merged into a single unqualified success rate.

| Evidence lane | Result | Scope / caveat |
| --- | --- | --- |
| Typecheck, lint, build, static gate | v1 commands exit 0; enhanced-candidate receipts in validation results | A historical pass does not stand in for final-candidate identity |
| Checker unit tests | 13 passing (v1 suite: 8) | Checker tests, not product screens |
| Original browser suite | 22/22 on local production build | Chrome 154.0.8037.98, macOS; semantic, recovery and layout assertions |
| Axe suite | 16/16 after real table/pre and group-role fixes | Earlier scan rounds retained; incomplete findings reviewed with stated limits |
| Enhanced browser scope | 38 cases = 22 original + 16 axe | Not 38 independent product states |
| CMP-001 / CMP-002 | 8/8 + 8/8 within a 38/38 run ([log](research/validation/round2-cmp/e2e-design.log)); CMP-002 negative control 2/2 detected | No CMP-001 negative control yet |
| State inventory | 31 entries: 22 implemented, 9 not | Coverage plan, not a test count |
| Visual gate | 3 snapshots; macOS baseline reviewed | Linux has no approved baseline and fails closed until reviewed |
| Static mutations, round 1 | 5/6 killed, 1 survived; 2/2 positives accepted | Alias escape retained as evidence |
| Static mutations, round 2 | 6/6 killed; 2/2 positives accepted; 0 survived/invalid/error | Fixed candidates only; new checks need their own receipts |
| Runtime mutations | Partial: 9/12 negatives killed, 2/3 positives accepted; 3 negatives + 1 positive pending ([frozen receipt](research/validation/phase-b/mutations-all-partial-2026-10-11T21-28-22-239Z/partial-summary.json)) | No full-run pass claimed. Two earlier runs had 7 invalid cases each and count as 0 kills |
| Axe negative control | 1/1 killed (`aria-pressed="sometimes"` → `aria-valid-attr-value`, critical) | Build, HTTP 200 and real DOM confirmed |
| Visual negative control | 1/1 killed: token letter-spacing change altered Files desktop/mobile by 4,735/4,738 px; Connectors unchanged ([details](validation/validation-results.md)) | Static checks and build passed; baselines and gate hashes unchanged |
| Engineer A | 22/22; 0 static violations; feature works | v2: 38/38; visual 3/3 after independent approval of two feature-driven baseline changes |
| Engineer B | 20/22 (2 name failures); 7 static violations (5 color, 2 native control); feature works by pointer | Focus loss found manually. v2: 32/38 (6 name/axe failures); visual 1/3, unapproved |
| Manual product checks | Desktop, 390/320px reviewed; 800px fixed and rechecked; local create/preview/recovery/detail paths exercised | No real OAuth, model run or full screen-reader journey |
| Remote CI and protection | Configuration only | Remote execution and required protection not established |
| CREAO deployment | Not performed | Live defects not claimed remediated |

The axe negative-control denominator of one is separate from six static negatives and the runtime mutation set. Its initial symlink/Turbopack build failure was an infrastructure attempt, not a kill; the subsequent successful webpack production build and rule-attributed scan provide the valid evidence. Likewise, initial missing-browser failures and invalid shared-baseline runs remain visible in history but do not improve the mutation score.

The accepted candidate must carry its source manifest/hash, environment, exact commands, exit statuses and report paths. Operationally, the frontend owner reviews failed gates/new state gaps/exception expiry daily, and Product Design reviews visual diffs and pattern drift; this describes ownership only and does not assert a recurring automation was scheduled. Local success within this explicit scope does not establish CREAO repository integration, protected CI enforcement or deployment.
