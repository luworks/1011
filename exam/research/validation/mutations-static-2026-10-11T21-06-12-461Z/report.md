# Design mutation report

Generated: 2026-10-11T21:06:25.994Z

Suite: static. Baseline SHA-256: `cd142735527fc9cfbfbb8702273efc04c2b43e923a001f8fcefe958d2c09649e`. Shared source unchanged: **true**.

Predefined mutations only; independent engineer experiments excluded.

| Case | Kind | Rule | Result | Evidence |
| --- | --- | --- | --- | --- |
| negative-hex-color | negative | DS-001 | killed | Original checker reported target rule. |
| negative-rgb-color | negative | DS-001 | killed | Original checker reported target rule. |
| negative-unknown-token | negative | DS-001 | killed | Original checker reported target rule. |
| negative-raw-button | negative | DS-002 | killed | Original checker reported target rule. |
| negative-aliased-button | negative | DS-002 | killed | Original checker reported target rule. |
| negative-expired-exception | negative | GOV-001 | killed | Original checker reported target rule. |
| positive-registered-token | positive | DS-001 | passed | Positive control accepted. |
| positive-approved-button | positive | DS-002 | passed | Positive control accepted. |

Negative kill denominator: 6 / 6. Invalid: 0; errors: 0; positive passes: 2; false positives: 0.

Runtime mutations were not executed in this run.

Full patches, command exits and rule-level evidence are in [report.json](report.json) and per-case receipts. A killed case means a target-rule assertion failed; process/server timeouts and type errors do not count. Browser route health is checked first; classification still requires review of the retained target assertion and server logs. Source hashes cover copied source/configuration, excluding dependencies/build outputs/reports/experiments.
