# Design mutation report

Generated: 2026-10-11T21:04:01.856Z

Suite: static. Baseline SHA-256: `7679d8f01d6b3b6bc686a43ab854abd1b9d9e91d67c03a540e5b0969ba8f8727`. Shared source unchanged: **true**.

Predefined mutations only; independent engineer experiments excluded.

| Case | Kind | Rule | Result | Evidence |
| --- | --- | --- | --- | --- |
| negative-hex-color | negative | DS-001 | killed | Original checker reported target rule. |
| negative-rgb-color | negative | DS-001 | killed | Original checker reported target rule. |
| negative-unknown-token | negative | DS-001 | killed | Original checker reported target rule. |
| negative-raw-button | negative | DS-002 | killed | Original checker reported target rule. |
| negative-aliased-button | negative | DS-002 | survived | Target rule did not reject the mutation. |
| negative-expired-exception | negative | GOV-001 | killed | Original checker reported target rule. |
| positive-registered-token | positive | DS-001 | passed | Positive control accepted. |
| positive-approved-button | positive | DS-002 | passed | Positive control accepted. |

Negative kill denominator: 5 / 6. Invalid: 0; errors: 0; positive passes: 2; false positives: 0.

Runtime mutations were not executed in this run.

Full patches, command exits and rule-level evidence are in [report.json](report.json) and per-case receipts. A killed case means a target-rule assertion failed; timeouts and type errors do not count. Source hashes cover copied source/configuration, excluding dependencies/build outputs/reports/experiments.
