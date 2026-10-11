# Mutation experiment history

All dates below are UTC. These are predefined mutations, separate from independently authored engineer experiments.

| Run | Outcome | Interpretation |
| --- | --- | --- |
| [Static first round](../../exam/research/validation/mutations-static-2026-10-11T21-03-48-256Z/report.md) | 5 killed, 1 survived, 2 positive passes; no invalid/error; shared hash unchanged | A real aliased intrinsic JSX button escaped DS-002. This evidence is retained. |
| [Static after generic symbol resolution](../../exam/research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.md) | 6 killed, 2 positive passes; no invalid/error; shared hash unchanged | The checker now resolves const bindings using TypeScript lexical symbols. The same alias challenge is rejected by DS-002. |
| [Browser infrastructure attempt](../../exam/research/validation/history/mutations-browser-2026-10-11T21-06-28-718Z/report.md) | All five unchanged rule groups passed; 7 cases classified invalid | Next.js was still flushing cache when cleanup attempted to remove its temporary directory. `ENOTEMPTY` interrupted the run. These are infrastructure outcomes, not design-rule kills. |
| [Aborted setup](../../exam/research/validation/history/mutations-browser-2026-10-11T21-13-40-991Z/aborted.md) | No case results | A wrong-working-directory edit failed and unintentionally started the old runner. Only its verified owned processes were stopped before any mutation result. |
| [Runner revision preflight](../../exam/research/validation/history/mutations-browser-2026-10-11T21-14-14-207Z/report.md) | Unchanged browser baseline passed; 7 cases invalid due to changed source hash | During runner repair, the hash guard prevented mixing runner versions. This is an infrastructure iteration, excluded from the design denominator. |
| [Superseded baseline setup](../../exam/research/validation/history/mutations-all-2026-10-11T21-15-51-863Z/aborted.md) | Stopped during unchanged-baseline preflight at coordinator direction; no mutation outcomes | Verification moved to the enhanced final baseline; not part of the design denominator. |

The final runner was frozen at `2026-10-11T21:15:27.553Z`, SHA-256 `a084545ecb4b1048b0b2b3be3c0c7bf00aa215d8a934b5cf5c31a8aa5984fa0d`. It waits for its private Next.js process to close before cleanup and retries directory removal. Browser checks stop after the first real failure. Only Playwright's exact administrative message announcing that intentional stop is ignored; other global errors, non-200 routes, uncaught browser errors, compilation errors, and runner deadlines cannot count as a rule kill.

Do not add the invalid/aborted iterations to the 12-case design denominator or claim they prove enforcement. Final rule conclusions require inspecting the retained target assertions, route-health evidence, and server logs. `--max-failures=1` means a mutation can be killed by one targeted assertion; it does not prove every route fails identically. The unchanged baseline still runs all selected rule tests.

## Final enhanced baseline handoff

The enhanced run started at `2026-10-11T21:28:22.239Z` using the same frozen runner. The user/coordinator then requested immediate handoff. The runner, its identified private server/test process groups, and the server that had just spawned at the stop boundary were terminated; a process readback confirmed no mutation runner/private mutation server remained. No additional cold starts were scheduled.

[Durable partial summary](runs/enhanced-baseline/creao-design-lab/reports/mutations-all-2026-10-11T21-28-22-239Z/partial-summary.md) and its JSON contain **11 completed receipts: 9 of 12 configured negative cases killed, 2 of 3 positive controls passed**. The remaining **3 negative cases and 1 positive control are pending**. The final whole-run source-hash check was not reached. There is no full-suite pass or 100% claim.

The completed runtime kills (missing h1, unnamed icon control, missing empty-state recovery) were manually checked against the actual target assertion. Each retained health check shows all four exercised routes returning HTTP 200 with no uncaught page error. The assertion failures respectively report zero h1 elements, an empty accessible name, and the absent recovery button. Process timeouts or compilation failures are not counted as kills.
