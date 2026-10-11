# CMP-002 negative control (round 2)

Date: 2026-10-11 · Lab: `creao-design-lab` · Browser: system Chrome (`PW_CHANNEL=chrome`)

## Mutation

Temporary edit to `src/app/connectors/page.tsx`: the `PageHeader` received
`actions={<><Button variant="primary">NEGATIVE-CONTROL A</Button><Button variant="primary">NEGATIVE-CONTROL B</Button></>}`,
i.e. two filled primary Buttons in the `/connectors` main region. `/connectors` was chosen so the CMP-001 tablist was not touched.

Server mode: the default Playwright `webServer` (`npm run dev -- --hostname 127.0.0.1 --port 3100`), so the mutated source was compiled live. The production `.next` build was not used for this control (it would have served the stale, unmutated build).

Command: `PW_CHANNEL=chrome npx playwright test tests/e2e/design.spec.ts -g 'CMP-002'`

## Result with mutation — detected

- 8 CMP-002 tests run: **2 failed, 6 passed**, exit 1.
- Failed exactly the two mutated cases: `[CMP-002] /connectors at most one filled primary action in main at 1280px` and `... at 390px`, each with `Expected: <= 1, Received: 2`.
- Unmutated routes (/files, /agents, /guidelines) passed at both widths.
- Log: `negative-control-mutated.log`; JSON: `negative-control-mutated.json`.

## Revert and positive control

The file was restored byte-for-byte from a copy taken before the edit (no git used); `grep -c NEGATIVE-CONTROL` returned 0.
Same command after revert: **8 passed, 0 failed**, exit 0. Log: `negative-control-reverted.log`; JSON: `negative-control-reverted.json`.

## Limits

One mutation shape (two literal `variant="primary"` Buttons on one route). It does not test a primary-styled lookalike without the `button-primary` class, a primary inside a dialog outside `main`, or the state-dependent primaries (files create form, agents detail). No CMP-001 negative control was run in this round.
