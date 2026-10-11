# Isolated design-rule mutation experiment

`node scripts/mutation-runner.mjs --suite static` runs the fast suite. Use `--suite browser` for DOM/interaction/geometry mutations, or `--suite all` for both. A passing unchanged baseline is mandatory. The runner copies implementation and governance inputs to a unique temporary directory, excludes `node_modules`, `.next`, `.git`, and reports, and links only dependencies. It never edits the shared source tree. Each browser case owns its own Next.js server and port.

Classification is evidence-based:

- `killed`: a negative mutation produces a structured violation or a failing Playwright assertion for its **target rule**.
- `survived`: a negative mutation passes, or only an unrelated rule fails.
- `passed`: a positive control passes every applicable original check.
- `false-positive`: an otherwise executable positive control is rejected.
- `invalid`: the patch no longer applies, the unchanged baseline fails, or the implementation does not compile.
- `error`: process/server timeout, missing dependencies, server/runner error, or malformed check output.

The report retains actual patches, implementation-tree hashes, commands, exits, structured violations/test outcomes, and durations. `killed / (killed + survived)` excludes invalid/error cases; those remain visible rather than disappearing from the report. Positive controls and independent engineer experiments have separate denominators. Reports from earlier runs are preserved in timestamped directories.

The suite only measures known mutations against the declared rules. It does not establish that arbitrary source edits cannot bypass the checks. Runtime mutations require actual browser assertions; source text or a mutation label cannot count as runtime evidence.

Browser cases first load every exercised route in Chromium, require HTTP 200 and no uncaught page error, and retain server logs. An expired `expect(...)` deadline can be a real design assertion failure; a navigation timeout or runner deadline is an error. This classification is not general root-cause proof: inspect the target assertion and server log before interpreting a kill.
