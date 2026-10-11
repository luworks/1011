# CREAO Design Constraints: Validation and Experiment Results

Date: 2026-10-11. Status: the current delivery is sealed at the user's request; the full mutation run has not completed and is explicitly kept as pending. This file records the run evidence obtained so far and is meant to be read together with the [implementation plan](../process/implementation-plan.md), the [product design guideline](../design-system-guideline.md), and the [compliance audit](../compliance-audit.md).

## Results Summary

| Validation layer | Currently verified result | Evidence / follow-up acceptance |
| --- | --- | --- |
| Types, general lint, production build | All three commands exit 0 | [commands.json](../research/validation/baseline/commands.json) and corresponding logs |
| CSS / JSX / governance checker unit tests | v1 8/8; enhanced phase 13/13, types/lint/static checks all exit 0 | [Unit test log](../research/validation/baseline/test-design.log), [design check log](../research/validation/baseline/check-design.log) |
| Prototype browser baseline | v1 22/22; enhanced phase 38/38 (original 22 + axe 16), 0 skipped, 0 flaky | [Chrome channel production report](../research/validation/e2e-production-chrome.json); the bootstrap missing-browser failure is kept separately |
| Prototype manual screenshot acceptance | Desktop and 390/320px checks passed; 800px initially overflowed, re-check passed after fix | [Manual review receipt](../research/prototype/manual-review.json), with before/after screenshots kept; create, preview, recovery, and detail interactions actually exercised |
| React Doctor | 6 warnings, 0 errors archived, all under the same performance rule | [diagnostics.json](../research/validation/react-doctor/diagnostics.json); warnings kept, not reported as zero issues |
| New axe gate negative control | 1/1 killed; after a valid build, hit aria-valid-attr-value | [New negative-control receipt](../research/accessibility/negative-control/receipt.json), separate denominator |
| Visual baseline / new visual negative control | Frozen baseline 3/3 passed; 1 visual negative control blocked | [Visual review re-check](../research/validation/phase-b/visual/visual-frozen-compare.json), [visual negative control](../research/validation/phase-b/visual-negative/visual-negative-summary.json) |
| Fixed mutation: first static round | 6 negatives: 5 killed, 1 survived; both positives passed; 0 invalid, 0 error, 0 false-positive | [First-round report.md](../research/validation/mutations-static-2026-10-11T21-03-48-256Z/report.md) / [raw JSON](../research/validation/mutations-static-2026-10-11T21-03-48-256Z/report.json) |
| Fixed mutation: second static round | 6/6 killed, 2/2 positives passed, 0 survived/invalid/error/false-positive | [Second-round report.md](../research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.md) / [raw JSON](../research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.json) |
| Fixed mutation: final "all" partial result | 9/12 planned negatives killed, 2/3 positives passed; remaining 3 negatives + 1 positive pending | [Sealed receipt](../research/validation/phase-b/mutations-all-partial-2026-10-11T21-28-22-239Z/partial-summary.json); not a successful complete run; the two historical invalid runs are kept |
| Independent engineer compliance experiment | A: 22/22 browser passed and 0 static violations; B: 7 static violations, 20/22 browser passed, 2 A11Y failures | [Independent experiment review](engineer-experiment-review.md); the new feature works in both; B's focus loss is an additional manual finding |
| GitHub CI / CD | v1 three-job YAML parses; enhanced version adds visual-gate, new run/parse evidence pending archive | [v1 parse receipt](../research/validation/baseline/workflow-parse.json); remote execution and protection settings not verified |
| Dependency audit (independent of design rules) | Full dependencies 5 high, production dependencies 0; all 5 belong to the same braces dev-tool dependency chain | [Full audit](../research/validation/baseline/npm-audit.json), [production audit](../research/validation/baseline/npm-audit-production.json) |

## Baseline Commands and Browser Results

The [environment receipt](../research/validation/baseline/environment.json) records macOS arm64, Node v24.21.0, npm 11.19.0, and exact package versions. The [command receipt](../research/validation/baseline/commands.json) records that `npm run typecheck`, `npm run lint`, `npm run test:design`, `npm run check:design`, and `npm run build` all exit 0. Unit tests pass 8/8, and the build log shows a successful Next.js 16.4.0 production build. The receipt does not include the install command, so it is not used to infer that a fresh `npm ci` completed.

The [production browser report](../research/validation/e2e-production-chrome.json) ran at `2026-10-11T21:05:33.253Z`: 22 expected passes, 0 unexpected, 0 skipped, 0 flaky. The report config uses `channel: chrome`, and the production server was started with `npm run start -- --hostname 127.0.0.1 --port 3100`. The [local browser version receipt](../research/validation/browser-environment.json) shows Google Chrome 154.0.8037.98; the device-emulation user-agent in the browser report is not a receipt of the actual browser version.

The [initial bootstrap failure report](../research/validation/e2e-bootstrap-missing-browser.json) keeps 20 launch failures caused by a missing Playwright Chromium executable. These are infrastructure failures; the tests never reached product behavior assertions, so they cannot be counted as 20 design violations, nor as mutation kills. The subsequent Chrome channel run against the production server is a separate, independent piece of evidence. Linux CI installs and runs Playwright Chromium by default; no result from that remote environment has been obtained yet.

## Manual Screenshots and Real Interaction

The [manual review receipt](../research/prototype/manual-review.json) comes from the production build at `http://127.0.0.1:3105`, using synthetic data and in-page temporary state. Interactions verified by hand: folder name validation/creation, preview close via Escape with focus restoration, connector empty-state recovery and local simulated connection, agent example creation and detail view, and the guideline page's Markdown tables and controlled CSS source links.

The file list checks passed at 390×844 and 320×844. At 800×900 the page width was initially 806px, a real layout issue; after moving the collection layout breakpoint to 900px, the re-check measured a page width of 800px. The [before-fix screenshot](../research/prototype/files-800.png) and [after-fix screenshot](../research/prototype/files-800-fixed.png) are kept. These manual screenshots are reported separately from automated assertions; no real OAuth or model runs were performed, and not all languages or full screen-reader testing were covered.

## First Mutation Round: Record of a Real Miss

Run time: `2026-10-11T21:03:48.272Z` to `2026-10-11T21:04:01.856Z` (UTC). This is the fixed static mutation set; it includes neither browser mutations nor the independent engineer experiment.

The baseline digest before and after the run is identical: `7679d8f01d6b3b6bc686a43ab854abd1b9d9e91d67c03a540e5b0969ba8f8727`. The original report's `baselineUnchanged` is `true`. All 8 change cases passed type checking; the first round did not count compile failures or timeouts as successful blocks.

| Change | Target rule | Actual classification | Meaning |
| --- | --- | --- | --- |
| Hex raw color added to page styles | DS-001 | killed | Original checker returned a target-rule violation |
| RGB raw color added to page styles | DS-001 | killed | Original checker returned a target-rule violation |
| Unregistered CSS token used | DS-001 | killed | Original checker returned a target-rule violation |
| Native button used to bypass components | DS-002 | killed | Original checker returned a target-rule violation |
| Native button assigned to an alias and rendered | DS-002 | **survived** | Type check passed, design check exited 0; a real first-round miss |
| Expired exception used | GOV-001 | killed | Governance check found the expired exception; the raw-color violation was not exempted either |
| Switched to another registered token | DS-001 | passed | Legitimate change accepted |
| Used the approved Button's primary variant | DS-002 | passed | Legitimate change accepted |

The negative denominator is 6, and the first-round block rate is **5/6 (83.3%)**. The positive denominator is 2, with an acceptance rate of **2/2**; the two denominators must not be mixed. This sample only demonstrates capability on the tested patterns; it does not show that arbitrary bypasses are controlled.

## Second Static Round: Re-check After Fixing the Alias Gap

The [second-round raw report](../research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.json) ran on the same 6 negatives and 2 positives. All 6 negatives were killed and both positives passed; survived / invalid / error / false-positive are all 0. The first-round miss on native-control aliases now hits DS-002 in this round; the first-round report is still kept, and the re-check does not overwrite history.

The baseline digest before and after the second round is `cd142735527fc9cfbfbb8702273efc04c2b43e923a001f8fcefe958d2c09649e`, `baselineUnchanged: true`. The new lexical-symbol alias check and the local same-name identifier test are directly covered in the 8 unit tests; this does not imply complete constraints over cross-module aliases, arbitrary dynamic components, or CSS-in-JS.

## Invalid Run History of Browser Mutations

Neither of the two runs produced a valid denominator usable for a design detection rate:

| Historical run | Classification | Raw cause | Evidence |
| --- | --- | --- | --- |
| 21:06:28 UTC | 7 invalid, 0 killed, valid negative denominator 0 | Baseline cleanup of `.next/dev/cache` hit `ENOTEMPTY`; source digests before and after match | [report.json](../research/validation/history/mutations-browser-2026-10-11T21-06-28-718Z/report.json) |
| 21:14:14 UTC | 7 invalid, 0 killed, valid negative denominator 0 | Shared source digest changed during the run; the hash guard marked all cases invalid; `baselineUnchanged: false` | [report.json](../research/validation/history/mutations-browser-2026-10-11T21-14-14-207Z/report.json) |

In each round, 6 negatives and 1 positive were affected by the same run-level problem; this is not the discovery of 7 independent product defects. They do not enter the killed/survived denominator for design rules. Later frozen-baseline re-checks must be stored in separate directories and must not overwrite the invalid history.

## React Doctor Warnings

The [raw rule report](../research/validation/react-doctor/react-doctor--js-set-map-lookups.txt) and [machine-readable diagnostics](../research/validation/react-doctor/diagnostics.json) record 6 `js-set-map-lookups` warnings at lines 12 and 15 of `src/app/connectors/page.tsx`: repeated array lookups inside loops may add overhead as data size grows. The diagnostics contain no errors.

This archive has no complete CLI stdout, exit code, or score, so it is not used to infer a React Doctor total score or the completion state of the whole command. Whether the warnings need optimization, and any follow-up re-check, is left to the final integration report; they are not an observed user-interaction failure.

## Independent Engineer Experiment

The [full A/B review and independent receipts](engineer-experiment-review.md) keep two implementations of the same "Important marking and filtering" feature. Both produce a production build, and manual pointer interaction and state changes work in both. A reuses approved components and tokens, has 0 static violations, and passes the original production browser checks 22/22. B's 5 raw colors and 2 native-control definitions are detected by static rules; the original browser checks find an unnamed star button on desktop and narrow screens, 20/22 passed, 2 A11Y-001 failures.

The [integrity receipt](../research/validation/engineers/source-integrity-review.json) verifies that each candidate changed only 3 feature files and that none of the 17 protected assets were modified. In B, after unmarking causes the current row to disappear, focus lands on `BODY`; this was found by the main agent's manual interaction. Current automation does not cover this new feature's focus lifecycle, so it must not be claimed that an automated gate caught it. This experiment is counted separately and is not added to the mutation negative denominator.

## CI and Dependency Boundaries

The [v1 CI syntax parse receipt](../research/validation/baseline/workflow-parse.json) confirms that the three-stage jobs existed at the time, with candidate depending on both design-gate and mutation-verification. The later enhanced version plans to add visual-gate, with its receipts stored separately from v1; on Linux without a reviewed pixel baseline it must fail closed, and a pending-baseline integration state must not be described as CI having passed. YAML parsing does not mean GitHub has executed it; required checks, branch protection, environment approvals, and deployment are still not connected.

The [raw npm audit result](../research/validation/baseline/npm-audit.json) has 5 high entries, traced to the same `braces` advisory [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) in the ESLint toolchain, not 5 independent root causes. The [production dependency audit](../research/validation/baseline/npm-audit-production.json) is 0. The non-zero full audit result is kept as a dependency risk; it cannot be claimed that all checks across the whole project have zero issues, and it is not mixed into the design mutation block denominator. The fix suggested by the report involves a cross-major-version change to `eslint-config-next`, so no automatic downgrade was applied blindly.

## Enhanced Phase B: Independent Results of Extended Checks

The [enhanced baseline commands](../research/validation/phase-b/final-baseline/commands.json) record that types, lint, 13 design unit tests, and the static design check all exit 0. The [full browser report](../research/validation/phase-b/final-baseline/e2e.json) is **38/38 passed** (original 22 design checks + 16 axe), 0 unexpected, 0 skipped, 0 flaky. The enhanced results do not rewrite the v1 history of 22 tests.

### axe Scans and Real Fixes

The [full accessibility index](../research/accessibility/README.md) keeps three baseline rounds, full scan JSON, screenshots, and manual review of incomplete results:

| Run | Result | Explanation |
| --- | --- | --- |
| [axe first round](../research/accessibility/axe-baseline-20261011T211342Z/report.json) | 13/16 passed | 2 failed before scanning because the locator conflicted with the Next route announcer; 1 was the Guidelines horizontal table not being keyboard-focusable |
| [axe second round](../research/accessibility/axe-baseline-v2-20261011T212200Z/report.json) | 14/16 passed | After fixing locators and the table, newly added code blocks were not keyboard-focusable at two viewports |
| [axe third round](../research/accessibility/axe-baseline-v3-20261011T212800Z/report.json) | 16/16 passed | Re-checked after fixing the real elements; incomplete review records kept |

[Actual keyboard interaction](../research/accessibility/axe-baseline-v3-20261011T212800Z/keyboard-scroll.json) shows that after table/pre receives focus, ArrowRight increases scrollLeft. The contrast "incomplete" results for the Dialog's overlapping backdrop and the clipped content on narrow-screen Guidelines were reviewed via screenshots, computed styles, and sampled scrolling. Automated zero violations must not be described as axe having automatically confirmed all contrast, let alone as full WCAG certification.

The [new axe negative-control receipt](../research/accessibility/negative-control/receipt.json) records changing a real button's `aria-pressed` to the invalid value `sometimes`: type checking passed, and after a production build / HTTP 200, the original test hit `aria-valid-attr-value`, hence **1/1 killed**. The first Turbopack symlink build failure is kept separately as an infrastructure attempt; what counts as killed is the target violation on the subsequently runnable page. This 1 new gate negative control is kept separate from the original fixed mutation denominator.

### Visual Baseline and Environment Boundaries

After the [manual baseline review](../research/validation/phase-b/visual/visual-baseline-review.json) independently confirmed the three screenshots were legible, both the [reviewed baseline comparison](../research/validation/phase-b/visual/visual-reviewed-compare.json) and the [frozen-source re-check](../research/validation/phase-b/visual/visual-frozen-compare.json) **passed 3/3**. The initial `--update-snapshots` only generated candidates and does not count as passing acceptance.

The [environment record](../research/validation/phase-b/visual/visual-candidate-environment.json) stores macOS arm64, Chrome 154.0.8037.98, Playwright 1.64.0, and the actual fonts; candidate PNGs and review metadata are in [snapshots/](../research/validation/phase-b/visual/snapshots/). These images must not pass as a Linux baseline; CI must block when the corresponding reviewed environment baseline is missing. The [visual negative-control summary](../research/validation/phase-b/visual-negative/visual-negative-summary.json) and [original report](../research/validation/phase-b/visual-negative/visual-negative-final.json) verify an incorrect letter-spacing change that uses a valid registered token: static checks and the production build both exit 0, and the visual test exits 1. Files desktop/narrow show 4735/4738 differing pixels respectively, while Connectors still passes; this is therefore **1 visual negative control killed**, not 2 independent mutations. The reviewed baseline PNG hashes are unchanged, and expected/actual/diff/trace are in a separate archive. The old setup failure is kept and not counted as a block. The enhanced A/B uses **the same two agents re-implementing the same feature**; it is a re-check migrated to the enhanced gates, not a new independent sample. A's [38 tests](../research/validation/engineers-v2/a/final/evaluator-e2e.json) all pass; the first [visual result](../research/validation/engineers-v2/a/final/evaluator-visual-first.json) produced two Files differences because of the newly added Important button. The main agent independently reviewed each image and updated only A's two candidate baselines, keeping the first diff and the [review receipt](../research/validation/engineers-v2/a/final/visual-review.json); the subsequent [plain visual re-check](../research/validation/engineers-v2/a/final/evaluator-visual-reviewed.json) passed 3/3. B's [visual result](../research/validation/engineers-v2/b/final/evaluator-visual-first.json) is 1/3 passed with two Files failures, and no update was approved; B's [full enhanced result](../research/validation/engineers-v2/b/final/evaluator-e2e.json) is **32/38 passed, 6 failed**, 0 skipped/flaky. Both the automated failures and the visual changes are kept, and B's candidate is not approved.

## Integration Build and Close-out Boundaries

After the enhanced implementation was merged into canonical, the first build failed because it mistakenly pulled the ignored `experiments/runs` subproject into the TypeScript scope. After only excluding this run directory in the canonical `tsconfig`, the [production build log](../research/validation/phase-b/canonical-integration/final-build-fixed.log) explicitly shows a successful build, and the [first failure](../research/validation/phase-b/canonical-integration/final-build.log) is kept. This is a workspace isolation fix, not a design violation or mutation kill.

- Install and overall acceptance: the [promote install log](../research/validation/phase-b/canonical-integration/promote-install.log), both baseline versions, and the independent experiment receipts are saved; subsequent changes still need re-checking along affected paths.
- The final mutation run was sealed per the user's request for an immediate close-out: [partial-summary](../research/validation/phase-b/mutations-all-partial-2026-10-11T21-28-22-239Z/partial-summary.json). 9 negatives killed and 2 positives passed so far; 3 negatives and 1 positive pending. No claim is made of an overall exit 0, completed final baseline digest verification, or a 100% detection rate.
- The independent engineer experiment's final commands are complete: [A](../research/validation/engineers/engineer-a/evaluator-commands.json) types/lint/design check/build all exit 0; [B](../research/validation/engineers/engineer-b/evaluator-commands.json) types/lint/build exit 0, design check exits 1.
- Final scope of visual and interaction checks: manual acceptance is archived above; if the final implementation keeps changing, re-check along affected paths.
- CI: locally verified commands are recorded separately from the not-yet-connected remote execution, required checks, approvals, and deployment steps.

## Archive Conventions

Raw evidence is stored in [research/validation/](../research/validation/), with file sizes and SHA-256 in [archive-manifest.json](../research/validation/archive-manifest.json). Each new run uses its own timestamped directory; the first-round miss is not overwritten, and earlier results are not rewritten with better later results. The current archive contains only check reports for the local prototype, synthetic implementation snippets, and local paths; no real CREAO user data has been copied. Temporary directories referenced in raw reports may have been removed; reviews should rely on the reports, patch contents, and receipts kept here.
