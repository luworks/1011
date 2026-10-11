# CREAO Design Standard Experiment: Claude Handoff Notes

Updated: 2026-10-11, America/Los_Angeles. This file records the facts at handoff and the remaining work; final run results are governed by the archived receipts, and a pass must not be inferred from an in-progress run.

## Delivery identity and handoff boundaries

- Workspace: `/Users/yuanlu/code/1011`; prototype: `/Users/yuanlu/code/1011/creao-design-lab`; brief, research, and evidence: `/Users/yuanlu/code/1011/exam`.
- Existing checkpoint: `edd2ea0c416f664339b59e56d2bcabe35f287f4a` (`chore: checkpoint CREAO design lab and audit evidence`); it is not the final packaging commit for this round.
- **Final commit SHA: governed by `sourceCommit` in the `.receipt.json` outside the ZIP and by `candidate-manifest.json` inside the package; read back in the workspace with `git rev-parse HEAD` (avoids recursively writing the document's own commit SHA into the commit)**.
- **Full-process ZIP path: `exam/delivery/creao-design-<first 12 chars of sourceCommit>.zip`; select the final version by the final reply and the receipt of the same name**.
- **ZIP SHA-256 / manifest location: the `.receipt.json` with the same name as the ZIP stores the package-level SHA-256; `candidate-manifest.json` / `evidence-manifest.json` inside the package store per-file digests. The package-level digest is kept outside the package to avoid recursive hashing**.
- The user asked to keep the entire process, commit, and hand off. "Commit" here means a local Git commit; there is no authorization or record of remote push, remote deployment, or production changes. Do not describe the checkpoint, ZIP, or local green checks as shipped.
- **Take over only after the main agent confirms all existing owners have finished, write and test processes are accounted for, and the final SHA/package manifest is frozen.** Do not modify shared baselines concurrently with still-running mutation or engineer experiments. Without that confirmation, first verify status read-only.
- Keep `task1/` and all unrelated work. Do not reset, clean failure evidence, or delete temporary experiment directories unless the owning owner has finished and the evidence is fully archived.

## Goal and reading order

The main body of the brief must be two Markdown files; the prototype is a validation attachment:

1. [task.md](../task.md): the original brief.
2. [design-system-guideline.md](../design-system-guideline.md): product-level layout patterns, rules, checks, approval, and exceptions.
3. [compliance-audit.md](../compliance-audit.md): real product observation → rule → how it is caught before release → local evidence.
4. [validation-results.md](../validation/validation-results.md): verified results and failure history; [implementation-plan.md](implementation-plan.md): scope and delivery matrix.
5. [design.md](../../creao-design-lab/design.md), [AGENTS.md](../../creao-design-lab/AGENTS.md), [README.md](../../creao-design-lab/README.md), [package.json](../../creao-design-lab/package.json): implementation entry points, versions, commands, and boundaries.
6. [delivery-packaging-plan.md](delivery-packaging-plan.md), [design drift patrol responsibilities](../agents/design-drift-auditor.md): full-process package and follow-up patrol contract.

The user confirmed there are no other attachments. Public sitemap, official Widgets docs, screenshot, and DOM research are complete; do not restart the search for design.md from scratch, and do not stop on the grounds that the private library is missing. Observed visual values, official Widget concepts, and local proposals are labeled separately; local adapter components must not pose as CREAO's private library. No create, connect, upload, or agent-run actions were performed on CREAO live data.

## Existing trusted evidence

The following are facts from different rounds and are not all bound to the final commit; check the corresponding manifest/hash first, then decide which affected items need re-running.

| Evidence | Verified content | Location |
| --- | --- | --- |
| v1 baseline | Type/lint/static check/build exit 0; checker unit tests 8/8; production Chrome browser 22/22 | `research/validation/baseline/`, `e2e-production-chrome.json` |
| Enhanced baseline | Checker unit tests 13/13; type/lint/static check exit 0; browser 38/38, including 16 axe items | `research/validation/phase-b/final-baseline/` |
| Static mutation history | First round 5/6 killed, aliased button survived; after fix 6/6 killed; positive cases 2/2 in both rounds | `research/validation/mutations-static-2026-10-11T21-03-48-256Z/` and `...21-06-12-461Z/` |
| Real manual acceptance | File create/validate, preview Escape and focus, simulated connection, agent detail, source view; 800px overflow documented before and after the fix | `research/prototype/manual-review.json` and screenshots |
| axe | Three scan rounds kept; final 16/16; scroll-region keyboard operation verified; illegal aria-pressed negative case hit effectively | `research/accessibility/README.md`, `negative-control/receipt.json` |
| Visual | Ordinary comparison 3/3 in the same reviewed macOS environment; wrong letter-spacing with a legal token detected by pixel comparison | `research/validation/phase-b/visual/`, `phase-b/visual-negative/` |
| Independent engineer v1 | A original gate 22/22; B 20/22, raw color/native control and unnamed button detected; feature and compliance accepted separately | [engineer-experiment-review.md](../validation/engineer-experiment-review.md), `research/validation/engineers/` |

In v1 B, focus landing on BODY after unchecking a filter was found manually; do not say the original automated gate caught it. React Doctor has 6 warnings for the same performance rule, and the archive has no full CLI score; npm audit across all dependencies has 5 high entries attributed to the same ESLint toolchain advisory, with 0 for production dependencies; do not write that all checks have zero issues.

The initial missing Chromium, mutation cleanup failure, and source changes during a run are all archived and cannot be counted as design kills. Keep `research/validation/history/` and the first-round survivor; later fixes never overwrite earlier results.

## Unfinished at handoff or needing final verification

- **Enhanced A/B v2 has finished this round's evaluation.** A: 38/38 browser and axe; after independent review of the feature's new screenshots, ordinary visual comparison 3/3. B: 32/38, 6 failures (4 axe, 2 button names), 7 static violations, visual 1/3; B not fixed. Both are the same v1 engineers reusing the feature and do not count as new independent samples. Evidence in `research/validation/engineers-v2/` and the final review.
- **The final frozen mutation run was aborted at the user's request to wrap up immediately and is partially complete.** As of wrap-up, 9/12 preset negative cases are known killed and 2/3 positive cases passed; the remaining 3 negative + 1 positive are pending, governed by the final archived partial receipt; do not report the whole round as passed or 100%. Claude's first task is to verify the remaining items against the frozen source, in a separate run that keeps this round's partial evidence, not stitched into one successful run.
- The final commit includes the documents, evidence, and the isolation fix excluding `experiments/runs/**` from the canonical tsconfig; build exits 0 after the canonical fix. The independently extracted package corresponds to `5a91054`: 238 Markdown links intact; install/type/lint/13 unit tests/static/build, 38 browser and axe, and 3 visual all pass. If the final ZIP contains later changes, distinguish the tested source from the final file identity.
- Verify the final commit, full-process ZIP, archived manifest/hashes, and file integrity. The package should include the main documents, source/lockfile/config, research, experiment tasks/patches/receipts, screenshots/traces, failure history, and these handoff notes; dependency directories and the Next build cache are not needed.
- Linux CI **has no reviewed visual baseline and should currently fail closed**. Do not borrow Mac PNGs, disable the visual gate, or auto-accept baselines to make CI green. The correct follow-up is to generate candidates in a fixed Linux environment, have them independently reviewed by a human, commit approval evidence, and then compare normally.
- There is no evidence of completed remote CI execution, required checks, actual CODEOWNERS protection, release, or production smoke. The patrol has only a responsibility file, **no daily schedule and no external notifications**; do not create tasks/schedules or send messages on your own.

## Environment and exact re-verification commands

Archived environment: Node.js `24.21.0`, npm `11.19.0`; the project requires Node 24; Next `16.4.0`, React `19.3.0`, Playwright `1.64.0`, axe Playwright `4.13.0`. Verify with the lockfile and environment receipt. macOS arm64, system Chrome `154.0.8037.98`; the reviewed visual namespace is `darwin-arm64-25.6.0-chromium-154.0.8037.98`; the device-emulation UA is not proof of browser version.

After confirming no other owner is using port 3100/the shared build directory, run from the project directory; save each round's logs to a separate timestamped directory. If dependencies are already available, there is no need to mechanically reinstall as proof; use `npm ci` in a clean handoff environment.

```sh
cd /Users/yuanlu/code/1011/creao-design-lab
npm ci
npm run typecheck
npm run lint
npm run test:design
npm run check:design
npm run build
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
PW_CHANNEL=chrome VISUAL_ENV=darwin-arm64-25.6.0-chromium-154.0.8037.98 PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
PW_CHANNEL=chrome npm run test:mutations
```

The visual namespace above may be used only when the **real environment matches exactly**; do not fake a match with environment variables. Other environments need their own reviewed baseline. The Linux browser install command is `npx playwright install --with-deps chromium`, but installing a browser does not fix a missing visual baseline. The default `test:e2e` does not include visual, which runs separately; production mode must specify `PW_SERVER_COMMAND` explicitly. An independent copy may use its own port and build directory, and must not reuse a shared `.next` that is being written.

**Never auto-run `--update-snapshots` after a failure.** Generating candidate screenshots is not a pass; legitimate feature changes must also save expected/actual/diff, explain the change, be independently reviewed before updating, and then be re-verified in normal mode. Do not modify an agent's original check assets to make its implementation pass, and do not mix the denominators of fixed mutations, independent engineers, axe negative cases, and visual negative cases.

## Startup prompt ready to copy to Claude

> Take over the CREAO product design standard and enforcement experiment at `/Users/yuanlu/code/1011`. First read `exam/process/handoff.md`, the two required Markdown files, `exam/validation/validation-results.md`, and `exam/process/implementation-plan.md`, then the prototype's AGENTS/design/README. Before any write, confirm all original owners have finished and that the final commit matches the ZIP/manifest identity. Do not repeat public research, do not reset historical failures, and do not auto-update visual snapshots. First verify whether the final frozen mutation run and enhanced A/B v2 have complete receipts; list anything unfinished truthfully; check their identity against the final source, and complete the necessary affected-path re-verification and document consistency wrap-up. The Mac Chrome 154 visual baseline cannot stand in for Linux; Linux without a reviewed baseline should stay fail closed. The two main documents are the final answer to the brief; the prototype and all experiment processes are supporting attachments. Keep unrelated files and all first-round misses/failure records. This round has no remote push, deployment, daily schedule, or external notification actions. Explanations in Chinese, code/identifiers in English; report what was actually completed, what is not yet verified, exact files/commands/exit codes, and the delivery SHA; do not predict a pass from an in-progress run.


Wrap-up process status: the main agent checked this task's working directory and then shut down preview servers on 3105, 3120, 3110, and 3111; the mutation owner stopped this round's runner and cleaned up its own servers. No owner is still writing source. If Claude needs a preview, it should run `npm run dev` from the project directory, or build and then `npm run start`, after first verifying the port is free.
