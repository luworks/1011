# Blank line-item regression provenance

`fixtures/blank_item_regression.json` adds four development scenarios and five customer turns. Existing fixtures, frozen cases and workflow snapshots are untouched.

File SHA256: `cf6f8f86eeb82b9af19c64d2123c4bc21959091f2c4ce033fe2afcaaf03d8b37`.

Nimbus Rule 1 requires the specific charge or line item being contested. Whitespace alone is not an identification. Normalizing leading/trailing whitespace and treating an empty resulting label as unknown is a prototype representation constraint implementing that source requirement, not a new eligibility policy.

Cases cover a whitespace-only initial backend label, a backend update clearing a previously meaningful label, a customer explicitly reporting only quoted whitespace and inability to identify the charge, and a meaningful trusted label surrounded by whitespace. The first three must retain pending verification; the positive control permits simulation given the otherwise confirmed record. The requested amount can still be explained without claiming issuance.

The customer-whitespace case is a natural-language regression, not a deterministic injection of an extracted fact. It cannot guarantee that the model emits a whitespace `FactProposal`; the oracle therefore does not require such a proposal. It checks the decision boundary. Direct proposal-normalization testing belongs in unit tests owned by the implementation task.

Backend clearing is represented honestly as `role: tool` with a `context` patch. Expected turn indices count customer turns only. Oracles are removed by the runner before model input. No API calls or comparisons against model outputs were used to author these cases.
