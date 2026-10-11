# Visual Regression Integration Proposal

> Translated from the original staging note `visual-strategy.zh-CN.md`. Historical draft: the integrated version lives in `creao-design-lab/tests/e2e/visual.spec.ts`.

## Minimum runnable scope for this round

`visual.spec.ts` covers the initial synthetic Files list (1280×900, 390×900) and the Connectors connected-empty state (1280×900). Business UI is not masked and compliance-relevant attributes are not mocked. Each test uses an isolated browser context, a fixed timezone/locale/clock, 1x device pixel ratio and light mode; it waits for fonts to load, disables animations and hides the text caret. Full-page screenshots ensure content below the fold on narrow viewports is also compared.

Tests must run against a production build server so the dev indicator and hot-reload UI never enter the baseline. The new `VISUAL-001` is a proposed additional rule; the coordinator must sync the rule catalog and delivery documents before it is integrated.

## Environment isolation and CI boundaries

The local machine is macOS 26.6 and the project fonts use system fallbacks, so macOS images cannot be used directly as an Ubuntu CI baseline. Playwright's default snapshot path already carries a platform suffix; this test additionally uses `VISUAL_ENV` to distinguish OS version, architecture, browser and font combination, e.g. `darwin26.6-arm64-chrome154.0.8037.98` (the real value must be confirmed from a run receipt, not copied from this example). Record browser.version, the locked Playwright version, OS/build, architecture, actual fonts and screenshot hashes. A naming variable is not a substitute for verifying the environment.

Route that can be verified immediately: on the current macOS, with the same installed browser, capture candidate screenshots -> coordinator reviews them manually -> keep candidate originals and hashes -> rerun in normal mode -> confirm a visual-breaking negative control fails. This only proves the visual gate on this machine's environment.

If CI stays on Linux, pin the visual job to the official container matching the locked Playwright version (e.g. the image for 1.64.0), fix viewport/fonts, and create a separate Linux namespace. The first run only produces artifacts for review; while no reviewed Linux baseline exists the gate stays failing and must not be reported as passing. Download the reviewed Linux images and commit them; afterwards the job may only compare, and `--update-snapshots` is forbidden. There is currently no local Docker verification or remote run evidence, so this part can only be marked as pending, never as passed.

A GitHub macOS runner is not necessarily identical to the local OS 26.6/font environment either; changing `runs-on` to macOS does not by itself justify a cross-machine stability claim. If the coordinator chooses that route, the runner also needs its own reviewed namespace, exact browser version and font receipt.

## Review policy and negative controls

The first baseline may be created with `--update-snapshots` in an explicit candidate directory; that command is not compliance evidence. Only after the coordinator reviews the screenshots against the rules does a normal-mode rerun record a baseline pass. CI, mutation runs and engineer experiments must never update snapshots automatically.

Adding an Important button and filter is a legitimate feature and will likely change the initial Files image. The first experiment round must keep the visual diff; a visual failure means "needs design review", not a semantic or component rule violation. If the feature, rules and human review all pass, a new candidate image may be approved separately, keeping the old hash, new hash, rationale, reviewer and first-round result, and then a second round is recorded. This must not be counted as a static design violation being blocked, and updating snapshots must not be used to hide shortcut code.

The visual negative control should misuse a legal layout value of an already registered token (e.g. increase list item height by 16px). The code still compiles and static CSS checks pass, yet the original `toHaveScreenshot` must show a real pixel diff; keep expected/actual/diff. After restoring the application source, a normal-mode run passes again. Network failures, missing browsers, page exceptions and missing baselines are error/setup outcomes and never count as a successful visual negative kill.
