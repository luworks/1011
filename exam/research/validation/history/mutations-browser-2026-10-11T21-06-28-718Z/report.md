# Design mutation report

Generated: 2026-10-11T21:12:51.838Z

Suite: browser. Baseline SHA-256: `cd142735527fc9cfbfbb8702273efc04c2b43e923a001f8fcefe958d2c09649e`. Shared source unchanged: **true**.

Predefined mutations only; independent engineer experiments excluded.

| Case | Kind | Rule | Result | Evidence |
| --- | --- | --- | --- | --- |
| negative-missing-heading | negative | LAY-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| negative-icon-name | negative | A11Y-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| negative-empty-recovery | negative | STATE-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| negative-wrong-destination | negative | NAV-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| negative-fixed-mobile-width | negative | RESP-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| negative-swapped-file-fields | negative | RESP-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |
| positive-long-filename | positive | RESP-001 | invalid | ENOTEMPTY: directory not empty, rmdir '/var/folders/zr/hp5t3xpd16b9b_vjf10dd4nm0000gn/T/creao-mutation-DRzFjx/creao-design-lab/.next/dev/cache' |

Negative kill denominator: 0 / 0. Invalid: 7; errors: 0; positive passes: 0; false positives: 0.



Full patches, command exits and rule-level evidence are in [report.json](report.json) and per-case receipts. A killed case means a target-rule assertion failed; process/server timeouts and type errors do not count. Browser route health is checked first; classification still requires review of the retained target assertion and server logs. Source hashes cover copied source/configuration, excluding dependencies/build outputs/reports/experiments.
