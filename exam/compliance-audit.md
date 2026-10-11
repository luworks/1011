# CREAO Product Design Compliance Audit

Audit date: 11 October 2026 (PDT). Standard: [design-system-guideline.md](design-system-guideline.md) and the executable [design.md](../creao-design-lab/design.md), version 0.2 (with retained v1 experiment history).

**Finding:** the inspected product contains five directly evidenced issues across page identity, empty-state navigation/recovery, and compact file layouts. A sixth, lower-priority improvement applies the proposed stricter in-state recovery rule to file search. The issues can be translated into specific pre-release checks without redesigning CREAO's token or component library.

**Evidence status:** the source-product observations below are complete. Local receipts are summarized separately below; final runtime-mutation and visual-negative-control results are explicitly reserved for the integrating reviewer. No claim is made that these checks already run inside CREAO's production repository, that the live defects were fixed, or that CREAO's unpublished internal rules were violated.

## Method and boundaries

The user confirmed that the linked live product is the complete supplied resource set. This audit therefore uses captured live screens, their accessibility/DOM evidence and public Widgets documentation. Deep captures were taken on 11 October 2026, 13:51–13:54 PDT; see the [capture manifest](research/deep/capture-manifest.json). Earlier desktop captures are retained under `research/screenshots/`. The inspected narrow source screen is 390 × 844; the local automated fixture uses 390 × 900, with desktop checks at 1280 × 900.

Three evidence lanes are kept separate:

1. **Observed product defect:** a screenshot, DOM record or accessibility tree establishes what the live product did in the captured state.
2. **Local enforcement proof:** a synthetic local implementation, the checker source and a valid mutated candidate show whether the proposed gate can detect that defect class. Actual run results belong in the receipt table; test source alone is not a passing run.
3. **Production adoption:** bind fixtures to CREAO's real routes/library, require protected checks and verify the deployed candidate. This is not performed by the lab.

Severity is a proposed triage decision, not a measured incident rate: P1 means a control cannot be reliably identified in the captured accessibility state; P2 means navigation, comprehension or recovery is materially weakened; P3 means a stricter proposed consistency improvement where a usable alternative exists. These findings are blocking under the proposed rule once adopted, except that prioritization and time-limited exceptions are owned by Product Design and Engineering.

## Findings at a glance

| Finding | Screen/state | Rule | Priority | Evidence | Proposed pre-ship detection |
| --- | --- | --- | --- | --- | --- |
| AUD-01 | Files, desktop list | LAY-001 | P2 | Visual title is a button; no headings in captured DOM | Count visible level-one headings within main and compare route identity |
| AUD-02 | Connectors, Connected (0) | NAV-001 | P2 | Guidance says `可用`; actual target tab says `可连接` | Assert canonical destination name in guidance and selected destination after action |
| AUD-03 | Same connector empty state | STATE-001 | P2 | Empty state contains only heading/text; no in-state next action | Trigger zero connections, invoke recovery action, assert connectable services appear |
| AUD-04 | Files, 390px | A11Y-001 | P1 | Folder button's text is hidden; icon is hidden from accessibility; no alternate name | Compute the visible control's accessible name at compact width |
| AUD-05 | Files, 390px list | RESP-001 | P2 | Desktop-style headers remain above a differently stacked metadata layout | Hide stale headers, preserve known label/value pairs, check field geometry and review screenshot |
| AUD-06 | Files, search with no matches | STATE-001 | P3 | Empty region has no action, although the search box does have a clear affordance | Require an in-state clear action and assert query reset plus restored results |

AUD-02 and AUD-03 occur in one state but are different failure conditions: fixing the wording does not add a recovery action, and adding a button does not guarantee it reaches the correctly named destination. AUD-04 and AUD-05 similarly expose different consequences of the same compact breakpoint.

## AUD-01 — Files loses semantic page identity

**Observed state.** On `https://agent.creao.ai/files`, the desktop screen displays “文件” as the page title. The saved [DOM record](research/files-dom.json) reports `headings: []` and identifies the title as `BUTTON` with text “文件”. The [desktop screenshot](research/screenshots/03-files.png) shows the visual title in the expected page-header position.

**Violation.** LAY-001 requires one visible `h1` identifying each governed top-level page within its main region. A large text button does not satisfy that semantic contract. The evidence is stronger than a screenshot-only judgment because the element and empty heading list were inspected.

**User impact.** A person navigating by headings cannot identify the page through the expected heading structure. Future feature implementations also lack a consistent semantic page-header contract. This audit does not claim a measured screen-reader incident or universal failure across all routes.

**Exact correction.** Render the page identity through `PageHeader` / a semantic `h1`. If the existing title also opens navigation or folder selection, retain that interaction in a separate named control rather than making the page identity only a button. Use lower-level headings for previews and sections.

**How it is caught before shipping.** In [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts), `[LAY-001] /files one visible page heading at 1280px` and its compact counterpart assert exactly one main region, one visible level-one heading and the expected name “文件”. A candidate that reproduces the observed structure has zero matching headings and fails the rule assertion. This requires DOM inspection; the CSS token check would not detect it.

**Adoption boundary.** The local test targets `/files` in the prototype. CREAO can use the same assertion on its real route with authenticated fixture data. That production integration has not occurred.

## AUD-02 — Connector guidance names a tab that is not present

**Observed state.** On `https://agent.creao.ai/integrations`, the selected tab is “已连接 (0)”. The empty-state description says “前往可用标签页连接服务。” The actual available destination is labeled “可连接”, alongside “全部”, “内置” and “已连接”. Both the [screenshot](research/screenshots/05-connectors-empty.png) and [accessibility tree](research/connectors-empty-ax.txt) preserve the mismatch.

**Violation.** NAV-001 requires destination guidance to use the real destination's name. “可用” and “可连接” might be semantically related, but asking the user to locate a named tab that does not exist creates avoidable uncertainty.

**User impact.** A first-time user must infer which tab the instruction means. A coding agent can repeat stale copy when adding or renaming navigation unless copy ownership is explicit.

**Exact correction.** Put the canonical destination label in the shared copy module and compose both the tab and recovery guidance from it. Use an action such as “浏览可连接服务”. Its handler activates the connectable tab, and the panel must show eligible services.

**How it is caught before shipping.** `[NAV-001] empty-state destination copy matches actual available tab` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) finds the actual tab named “可连接”, enters the connected-empty state, checks that its description contains “可连接” and does not contain the obsolete “可用”, then invokes recovery and asserts `aria-selected="true"` on the target. Copying the observed wording into the local candidate fails the description assertion. Wrong routing fails the selected-state assertion.

**Automation limit.** The current test deliberately uses a canonical Chinese contract. It does not prove all locales or future destination renames are correct, and it does not statically prove all strings originate in one module. Shared-source reuse is a source-review requirement; a legitimate rename requires a reviewed contract update.

## AUD-03 — Connector empty state does not offer a direct next step

**Observed state.** The same [Connected (0) screenshot](research/screenshots/05-connectors-empty.png) shows an icon, “暂无已连接的连接器”, and a sentence directing users elsewhere. The matching [AX subtree](research/connectors-empty-ax.txt) contains a heading and text without a button/link inside the empty state. Tabs remain available outside it.

**Violation.** STATE-001 requires a recoverable empty state to include an actionable next step within that state. A distant tab is an available workaround, but it does not fulfill the proposed composition contract.

**User impact.** The screen explains absence without completing the recovery path. Users have to reinterpret the explanation as an instruction to navigate manually; the naming mismatch in AUD-02 compounds the problem.

**Exact correction.** Retain the empty-state title and explanatory purpose, add “浏览可连接服务”, and wire it to the actual connectable panel. Do not launch OAuth merely because the user asks to browse services. Use a distinct explicit action to connect an individual service.

**How it is caught before shipping.** `[STATE-001] connector empty state action reaches available services` triggers the fixture with zero connections, requires the recovery button to be visible, clicks it, asserts the connectable tab is selected and an actual service action appears, then verifies the recovery button disappears. A missing or inert button fails. A compliance attribute or snapshot of a button would not be sufficient.

**Important distinction.** We are not claiming users were completely trapped: the top-level tabs were present. The finding is a specific violation of the adopted in-state recovery rule. Initial empty-state recovery already exists elsewhere in the product: the [agents screen](research/screenshots/02-agents-empty.png) supplies a creation CTA.

## AUD-04 — Compact “New folder” button loses its accessible name

**Observed state.** On Files at 390 × 844, the [screenshot](research/deep/14-files-mobile.png) shows a folder-plus icon near Upload. The saved [mobile DOM record](research/deep/files-mobile-dom.json) identifies the button with text “新建文件夹”, but that text is in a `SPAN` with `display: none`. Its SVG has `aria-hidden="true"`; `aria-label`, `aria-labelledby` and `title` are absent. The button rectangle is visible, 41 × 36 CSS px at x=250, y=56.

**Violation.** A11Y-001 requires visible interactive controls to retain an accessible name after responsive changes. Hidden text plus an accessibility-hidden icon supplies no usable name in this recorded structure. This is a specific naming finding; button dimensions alone are not used to make a target-size compliance claim.

**User impact.** A user relying on accessible control names cannot reliably identify the action. Desktop-only checks would miss the responsive change that removes the label.

**Exact correction.** Retain the name through `aria-label="新建文件夹"` or a genuinely visually hidden text treatment that stays in the accessibility tree. Preserve the decorative icon's hidden state. If text remains visible, it must match the action's accessible name.

**How it is caught before shipping.** `[A11Y-001] /files visible controls retain accessible names at 390px` iterates visible interactive controls and calls Playwright's accessible-name assertion, requiring a non-whitespace result. A local mutation that removes the name while hiding the visible text should fail this specific assertion. The desktop counterpart verifies that the name also exists before collapse.

**Automation limit.** A non-empty but misleading name could pass this particular check. Human review must assess meaning, and separate interaction tests must cover keyboard activation/focus. This finding does not establish a complete WCAG audit.

## AUD-05 — Compact file metadata no longer corresponds to the headers

**Observed state.** In [the 390px Files capture](research/deep/14-files-mobile.png), the “名称” header wraps into separate characters, while “修改时间”, “大小” and “来源” remain in a desktop-style header row. File entries below use another layout: the name appears on its own row, modification time and size sit underneath, and source occupies a further line. The spatial header-to-value mapping has broken.

**Violation.** RESP-001 requires field identity to survive responsive transformation. Keeping table-like headers above values that no longer occupy those columns makes the page look structurally tabular while asking users to infer a different reading order.

**User impact.** Values become harder to scan and compare, particularly when fields contain unfamiliar formats. The evidence establishes layout ambiguity; it does not establish an actual stored-data mix-up.

**Exact correction.** At the compact breakpoint, remove the desktop header and render each item as a name followed by visible metadata label/value pairs. Keep each label and value in the same field group. Maintain a full name through wrapping or an accessible detail/preview path. Desktop should retain the aligned column structure.

**How it is caught before shipping.** `[RESP-001] file list preserves field labels and fits 390px viewport` in [design.spec.ts](../creao-design-lab/tests/e2e/design.spec.ts) requires the desktop header to be hidden, metadata labels to be visible, item bounds to remain inside the viewport, and metadata rectangles not to overlap. It also checks a known file against [an independent label/value fixture](../creao-design-lab/tests/e2e/fixtures/file-contract.ts): modification time, size and source must remain correctly paired. It then checks that desktop headers return at 1280px and captures both layouts.

**Why both kinds of checks matter.** Geometry alone can pass a cleanly laid out but incorrectly paired value. The independent fixture catches this semantic mapping error. Neither assertion proves all visual reading-order decisions: a reviewer still inspects the screenshots. The live screen's first failure against this contract would be the visible stale header; reproducing only metadata value swaps should fail the separate fixture comparison.

**Coverage boundary.** The local automatic test is at 390 × 900, not the exact original 390 × 844 height. A production rollout should include that captured viewport, long names, supported locales and intermediate breakpoints; no all-device claim is made here.

## AUD-06 — File-search recovery is outside the empty region

**Observed state.** Searching for a nonmatching term produces “没有文件” with the more precise description “没有与搜索匹配的文件或文件夹。” The [screenshot](research/deep/15-files-no-results.png) shows no action inside the empty region, **and does show a clear affordance at the right end of the search box**. The [AX capture](research/deep/15-files-no-results.txt) records the no-results message.

**Violation and priority.** This is a P3 application of the proposed STATE-001 in-state recovery contract. It is weaker than AUD-03 because the user already has an obvious recovery affordance adjacent to the active query. It must not be described as “there is no way to clear the search”.

**Exact correction.** Prefer an unambiguous “No matching files” title, retain the explanation, and add “清除搜索” inside the empty state. Keep the search-box clear control as well. If multiple filters contribute to zero results, the action must state and clear the intended filters, rather than silently clearing unrelated user context.

**How it is caught before shipping.** `[STATE-001] file search no-results action restores actual entries` enters a deterministic unmatched query, asserts zero result items, invokes the clear action within the empty region, asserts the query becomes empty and a seeded result returns. A nearby clear button outside the region does not satisfy the locator contract. This catches the proposed consistency requirement; it is not proof the original product had no recovery affordance.

## Positive evidence and findings deliberately not made

| Evidence | Useful existing behavior | What is not inferred |
| --- | --- | --- |
| [Agents initial empty](research/screenshots/02-agents-empty.png) and [create handoff](research/deep/06-agent-create-handoff.png) | Explanation and creation action; creation starts in chat with a prefilled request | No real agent was created or run; success/failure states remain untested |
| [Skills compact layout](research/deep/13-skills-mobile.png) | Sidebar collapses and cards form a readable single column with visible actions | No blanket responsive approval for other routes |
| [Slack setup](research/deep/11-slack-detail.png) | Return navigation, explicit page identity, operational scope and a setup action | OAuth, permission changes and connection success were not exercised |
| [Autonomy menu](research/deep/07-autonomy-menu.png) | The two authority levels explain their consequences | No verification that every real external operation honors those settings |
| [Widgets gallery](research/deep/10-widgets-layout.png) and [CSS snapshot](research/deep/widgets-dom.json) | Existing components and design variables are directly evidenced | No private component imports, source reuse policy or token usage can be recovered from appearance alone |
| [File preview](research/deep/09-file-preview.png) and [video settings](research/deep/17-video-default-settings.png) | Overlay/detail and configuration patterns are already present | Screenshot appearance does not prove focus trapping, focus restoration or keyboard behavior |

No finding is made that engineers hard-coded colors or bypassed CREAO's internal components. DS-001 and DS-002 are preventive gates demonstrated on the local adapter; only repository source can establish such a violation in CREAO itself. Similarly, mixed radii do not establish incorrect component usage: the official Dashboard description and general app controls have different scopes. Screenshot-only color estimates are not accepted as a contrast audit.

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

Detailed immutable reports, command logs and history are indexed in [validation-results.zh-CN.md](validation-results.zh-CN.md), [accessibility/README.md](research/accessibility/README.md), and the [independent engineer experiment review](engineer-experiment-review.zh-CN.md). Results from different candidate revisions and gate versions are not merged into a single unqualified success rate.

| Evidence lane | Recorded result / status | Interpretation and remaining scope |
| --- | --- | --- |
| Typecheck, lint, production build and static gate | v1 archived commands exit 0; final enhanced candidate receipts are recorded in validation results | A passing historical revision is not a substitute for final-candidate identity |
| Checker unit tests | Enhanced checker: 13 passing unit cases; original v1 suite had 8 | These are checker tests, not 13 product screens |
| Original browser suite | 22/22 passed on local production build | Chrome 154.0.8037.98 on macOS; includes semantic, recovery and layout assertions |
| Enhanced axe suite | 16/16 passed after real table/pre and group-role fixes | Separate scan rounds retained; incomplete findings have explicit review and limits |
| Enhanced semantic/browser scope | 38 cases = original 22 + axe 16 | Keep phases/candidate identities visible; do not call this 38 independently explored product states |
| State inventory | 31 entries: 22 implemented, 9 not implemented | Inventory coverage, not a passing-test count; missing states remain listed |
| Visual gate | Three screen snapshots; macOS baseline reviewed | Linux has no approved baseline and must fail closed pending controlled bootstrap/review; final negative-control result below |
| Fixed static mutations, first round | 5 killed / 1 survived; 2/2 positive controls accepted | Valid negative denominator 6; real alias escape retained |
| Fixed static mutations, second round | 6/6 killed; 2/2 positive controls accepted; 0 survived/invalid/error/false-positive | Scope limited to those fixed candidates; later check additions require their own receipts |
| Runtime mutations | **FINAL RUNTIME RESULT: integrating reviewer to insert the final immutable receipt and killed/survived/invalid/error counts** | Prior two runs each had 7 invalid cases; valid design denominator 0 for those runs, never counted as kills |
| Axe negative control | **1/1 killed**, independently validated | Invalid runtime `aria-pressed="sometimes"`; typecheck and production build succeeded, HTTP 200 and real DOM confirmed; axe returned `aria-valid-attr-value` critical |
| Visual negative control | **FINAL VISUAL NEGATIVE RESULT: integrating reviewer to insert actual diff result and receipt** | Must demonstrate real source/pixel change with unchanged baseline and visual gate; environment mismatch is not a successful design kill |
| Independent engineer A | Original suite 22/22; static 0 violations; feature works | Historical original gate, not a re-run of the enhanced 38-case suite |
| Independent engineer B | Original suite 20/22; 2 name-test failures; 7 static violations; feature pointer behavior works | 5 literal-color + 2 native-control findings; focus loss additionally found manually |
| Manual product checks | Desktop, 390/320px reviewed; 800px fixed and rechecked; local create/preview/recovery/detail paths exercised | No real OAuth, model run or complete screen-reader journey |
| Remote CI and protected policy | Configuration is an implementation artifact; remote execution and required protection not established | Linux visual bootstrap is intentionally blocking, not an unexplained green check |
| CREAO deployment | Not performed | No claim that the original live defects are remediated |

The axe negative-control denominator of one is separate from six static negatives and the runtime mutation set. Its initial symlink/Turbopack build failure was an infrastructure attempt, not a kill; the subsequent successful webpack production build and rule-attributed scan provide the valid evidence. Likewise, initial missing-browser failures and invalid shared-baseline runs remain visible in history but do not improve the mutation score.

The accepted candidate must carry its source manifest/hash, environment, exact commands, exit statuses and report paths. Operationally, the frontend owner reviews failed gates/new state gaps/exception expiry daily, and Product Design reviews visual diffs and pattern drift; this describes ownership only and does not assert a recurring automation was scheduled. Local success within this explicit scope does not establish CREAO repository integration, protected CI enforcement or deployment.
