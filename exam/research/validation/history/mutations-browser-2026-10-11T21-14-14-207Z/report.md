# Design mutation report

Generated: 2026-10-11T21:15:48.788Z

Suite: browser. Baseline SHA-256: `dbfc14a102d765ab6d068b786d841491cc545c3deba1e4e749aab49c04a4f9f0`. Shared source unchanged: **false**.

Predefined mutations only; independent engineer experiments excluded.

| Case | Kind | Rule | Result | Evidence |
| --- | --- | --- | --- | --- |
| negative-missing-heading | negative | LAY-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| negative-icon-name | negative | A11Y-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| negative-empty-recovery | negative | STATE-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| negative-wrong-destination | negative | NAV-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| negative-fixed-mobile-width | negative | RESP-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| negative-swapped-file-fields | negative | RESP-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |
| positive-long-filename | positive | RESP-001 | invalid | Shared source changed since baseline; this case is invalid, not a rule kill. |

Negative kill denominator: 0 / 0. Invalid: 7; errors: 0; positive passes: 0; false positives: 0.



Full patches, command exits and rule-level evidence are in [report.json](report.json) and per-case receipts. A killed case means a target-rule assertion failed; process/server timeouts and type errors do not count. Browser route health is checked first; classification still requires review of the retained target assertion and server logs. Source hashes cover copied source/configuration, excluding dependencies/build outputs/reports/experiments.
