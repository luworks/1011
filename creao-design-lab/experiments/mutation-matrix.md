# Predefined mutation matrix

This is an experiment protocol, not a result. Actual outcomes are written by `scripts/mutation-runner.mjs` to timestamped `reports/mutations-*` directories. Independent engineer holdouts remain separate in `engineer-protocol.md`.

| Planned negative case | Target | Execution layer | What counts as a kill |
| --- | --- | --- | --- |
| Replace a governed color with a hex literal | DS-001 | CSS AST | Target-rule violation |
| Spell a literal using `rgb()` | DS-001 | CSS AST | Target-rule violation |
| Reference an unregistered CSS variable | DS-001 | CSS AST | Target-rule violation |
| Replace an approved control with an intrinsic `button` | DS-002 | JSX AST | Target-rule violation |
| Alias the intrinsic button through a capitalized variable | DS-002 | JSX AST challenge | Target-rule violation; a bypass is retained as survived |
| Add an expired exception | GOV-001 | Governance contract | Target-rule violation |
| Change the rendered page header from h1 to h2 | LAY-001 | Browser DOM | Actual heading assertion fails |
| Remove accessible naming from an icon-only control | A11Y-001 | Browser DOM | Actual accessible-name assertion fails |
| Remove the recovery action from an empty state | STATE-001 | Browser interaction | Actual recovery assertion fails |
| Point the recovery action at the wrong destination | NAV-001 | Browser interaction | Navigation assertion fails |
| Reintroduce a fixed-width layout on narrow screens | RESP-001 | Browser geometry | Measured viewport/overflow assertion fails |
| Swap actual modification/size values under unchanged labels | RESP-001 | Browser field contract | Independent expected label/value mapping fails |

Positive controls make a legitimate registered-token change and a legitimate existing-component/data change. A long-name responsive control may be included after actual component interfaces are available. Every case starts from the same unchanged baseline, receives a real implementation patch, passes TypeScript, and invokes the same original checker as CI. Runtime cases start a private server and run the original browser spec with the target-rule grep.

Do not edit this table to make failures appear successful. The machine report separates killed, survived, invalid, error, positive passes, and false positives. Newly discovered limitations can be repaired only in a subsequent run with a new baseline hash; earlier receipts must remain available.
