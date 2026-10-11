# Accessibility gate integration handoff

- Draft: `accessibility.spec.ts`; destination: `creao-design-lab/tests/e2e/accessibility.spec.ts`.
- Single package owner should add exact dev dependency `@axe-core/playwright: 4.13.0` and update lock using npm. Registry version verified 2026-10-11 with `npm view @axe-core/playwright version`.
- Sixteen checks: eight real UI states × desktop 1280×900 / compact 390×844. No `include`, `exclude`, `disableRules`, or mocks; entire active document is scanned with `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`.
- All axe results are JSON attachments including `passes`, `incomplete`, `inapplicable`, and `violations`. `incomplete` rule IDs/targets are also report annotations for manual review. Passing automatic checks is not full WCAG conformance or completion of manual review.
- Run from lab after integration: `npx playwright test tests/e2e/accessibility.spec.ts`. Preserve any failing first run before repairs. Existing semantics, behavior, names, focus and geometry tests remain required.

## Required negative control (not executed yet)

In an isolated copy, change only Files list-toggle application JSX `aria-pressed={view === 'list'}` to `aria-pressed="sometimes"`. React's ARIA prop typing rejects this literal, so use a type-preserving source mutation `aria-pressed={'sometimes' as unknown as boolean}`. This simulates an API/configuration value leaking into an ARIA attribute while preserving compilation. The rendered DOM must contain `aria-pressed="sometimes"`.

Run the unchanged initial Files axe test and require an actual `aria-valid-attr-value` violation targeting the rendered toggle in the attached JSON. Compilation error, test locator error, browser/server timeout or other infrastructure failure is invalid/error, never a successful kill. Preserve the patch, typecheck result, browser version, command/exit code and complete axe result. Positive baseline uses unmodified application JSX. Do not mutate the scanner, rule list or assertion.

Official API references consulted:

- [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)
- [Deque axe-core Playwright package](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md)

Status: historical staging note. The spec has since been integrated as `creao-design-lab/tests/e2e/accessibility.spec.ts`; see the validation results for executed runs.
