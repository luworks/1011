# Automated Accessibility Verification Record

Environment: macOS, local production-mode Next.js, system Chrome `154.0.8037.98`, Playwright `1.64.0`, `@axe-core/playwright` / axe-core `4.13.0`. This is not a remote CI run or a full WCAG certification.

## Baseline verification and real fixes

1. `axe-baseline-20261011T211342Z/report.json`: of 16 tests, 13 passed; 2 failed before scanning because the test locator conflicted with the `role=alert` of Next.js's built-in route announcer; 1 was the narrow-screen Guidelines page, where four horizontally scrolling tables could not receive keyboard focus, axe rule `scrollable-region-focusable`. The two kinds of failures are kept clearly separate.
2. `axe-baseline-v2-20261011T212200Z/report.json`: after scoping the form-error locator precisely to `main`, both form states passed; the original tables got `tabIndex=0`, and the Files view-toggle container got `role=group`. 14/16 passed; the new long code block on Guidelines failed at both viewports because `pre` could not receive keyboard focus. Fixes continued in the actual source, without filtering rules.
3. `axe-baseline-v3-20261011T212800Z/report.json`: after `pre` was likewise made focusable, **16/16 passed**, exit 0. `scan-summary.json` records automated results and incomplete items by state. `keyboard-scroll.json` additionally verifies that after focusing the narrow-screen table/pre and pressing ArrowRight, the real scrollLeft grew to 35/30 respectively; this shows keyboard recovery actually works.

The `axe-*` JSON attachments in each report contain all passes, incomplete, inapplicable, and violations; the first-round ID was A11Y-001, and after registering the new rule only the axe test titles were unified to A11Y-002. The two initial locator errors do not count as product violations or mutation kills.

## New gate negative-case experiment: separate denominator of 1

`negative-control/receipt.json`, `source.patch`, `axe-results.json`, `negative-report.json`, and artifacts hold the real evidence.

- Only in an independent copy, the Files list-view button's `aria-pressed` was changed to the runtime-illegal value `sometimes`, with an explicit type assertion to keep it compiling. Tests, rules, and scanner were not modified.
- TypeScript check exited 0. The first Turbopack build failed because the experiment copy's node_modules symlink pointed outside the root; this is recorded separately as an infrastructure attempt failure. Then `next build --webpack` exited 0.
- The page returned HTTP 200 with normal title and h1, and the browser read back the real DOM `aria-pressed="sometimes"`.
- The unmodified initial Files axe test exited 1 with an actual `aria-valid-attr-value` critical violation, targeting exactly the list-view button. So this group is **1/1 killed**, not a "success" manufactured by a compile failure or timeout. It is not mixed into the denominator of the existing design mutations.
- The independent server on 3121 was shut down after the run. The source SHA and test SHA saved in the report can be used for independent re-verification.

## Manual review of incomplete items

- In the first round, `.view-toggle` set `aria-label` on a div without a role, which axe marked as `aria-prohibited-attr` incomplete; manually confirmed and fixed with `role=group`.
- The Dialog `color-contrast` incomplete was because axe could not determine the background from top-layer/overlap. `dialog-manual-v2-1280.png` and `dialog-manual-v2-390.png` were each reviewed; preview body and description are unobscured. `dialog-computed-styles-v2.json` stores actual visible element coordinates and colors; body #16181a / #f8f6f3 has a contrast ratio of 16.50:1, and description #66635e / #fefdfb is 5.88:1, both above the 4.5:1 for normal text.
- The final narrow-screen Guidelines still has 61 cells with `color-contrast` incomplete because the horizontal scroll container clips them. `axe-baseline-v3-20261011T212800Z/guidelines-incomplete-computed-review.json` records each one's actual foreground color, ancestor background, and computed result: no gradients, background images, or opacity layering; lowest computed contrast 16.50:1. `guidelines-clipped-cell-revealed.png` was viewed, and a representative cell can be revealed via native scrolling. This is a computed-style and sampled-visual review; it does not claim every one of the 61 cells was screenshotted individually or confirmed automatically by axe.
- The two screenshots named `dialog-manual-` without `v2`, and the corresponding first computed-styles, were a manual capture attempt that did not wait for the dialog to finish appearing: coordinates are zero and the screenshot shows only the list, **not used as dialog pass evidence**; kept to document the capture correction.
- Zero automated violations does not mean all accessibility requirements are verified; screen readers, full keyboard journeys, and unenumerated states remain outside coverage.

API references: [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing), [Deque Playwright integration](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md).
