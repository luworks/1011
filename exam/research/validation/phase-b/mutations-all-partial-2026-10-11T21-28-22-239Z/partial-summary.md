# Mutation handoff — stopped, incomplete

Stopped at user/coordinator request: 2026-10-11T21:33:33.641Z. Owned runner/server/browser-test processes were terminated; no further cold starts are scheduled.

Configured denominator: **12 negative cases and 3 positive controls**. Completed evidence: **9 negative kills, 2 positive passes**. Pending: **3 negative cases, 1 positive controls**. Survived 0; invalid 0; error 0 among completed receipts. This is not a complete suite pass.

Baseline SHA-256: `f7a578e36f2d94115c02cd8afb0b5a4578b2f866a4e5b13d9d95f734104b75bc`. Final run-level unchanged-source check was not reached because execution was stopped.

| Case | Kind | Rule | Status | Receipt |
| --- | --- | --- | --- | --- |
| negative-hex-color | negative | DS-001 | killed | [receipt](negative-hex-color/receipt.json) |
| negative-rgb-color | negative | DS-001 | killed | [receipt](negative-rgb-color/receipt.json) |
| negative-unknown-token | negative | DS-001 | killed | [receipt](negative-unknown-token/receipt.json) |
| negative-raw-button | negative | DS-002 | killed | [receipt](negative-raw-button/receipt.json) |
| negative-aliased-button | negative | DS-002 | killed | [receipt](negative-aliased-button/receipt.json) |
| negative-expired-exception | negative | GOV-001 | killed | [receipt](negative-expired-exception/receipt.json) |
| positive-registered-token | positive | DS-001 | passed | [receipt](positive-registered-token/receipt.json) |
| positive-approved-button | positive | DS-002 | passed | [receipt](positive-approved-button/receipt.json) |
| negative-missing-heading | negative | LAY-001 | killed | [receipt](negative-missing-heading/receipt.json) |
| negative-icon-name | negative | A11Y-001 | killed | [receipt](negative-icon-name/receipt.json) |
| negative-empty-recovery | negative | STATE-001 | killed | [receipt](negative-empty-recovery/receipt.json) |
| negative-wrong-destination | negative | NAV-001 | pending | Not completed |
| negative-fixed-mobile-width | negative | RESP-001 | pending | Not completed |
| negative-swapped-file-fields | negative | RESP-001 | pending | Not completed |
| positive-long-filename | positive | RESP-001 | pending | Not completed |

Run from the enhanced project at `/Users/yuanlu/code/1011/creao-design-lab/experiments/runs/enhanced-baseline/creao-design-lab` (or the promoted project with identical source):

```sh
PW_CHANNEL=chrome node scripts/mutation-runner.mjs --suite browser --ids negative-wrong-destination,negative-fixed-mobile-width,negative-swapped-file-fields,positive-long-filename
```

That command creates a fresh isolated baseline and report for remaining cases; it does not edit the existing receipts. For a single full final receipt, use `PW_CHANNEL=chrome node scripts/mutation-runner.mjs --suite all`. Validate hashes before combining outcomes. Historical infrastructure/aborted attempts and independent engineer holdouts have separate denominators.
