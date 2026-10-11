# Null-authority regression provenance

`fixtures/null_authority_regression.json` contains eight new development cases and ten customer turns. It is independent of the V6 live outputs and does not modify either acceptance suite or the V6 snapshot.

File SHA256: `54146862faa3e8d1ad07212a5dffde917b16e936c5c95e754720b7d1756e0247`.

Source basis: Nimbus Rule 1 requires identifying the disputed item and respecting the statement-date window. Rule 2 requires a confirmed billing error and a cumulative goodwill limit. Rule 3 supplies the outage formula; Rules 4–5 govern escalation. No source grants a customer statement the authority of a backend verification. Treating null as unknown, revoking authority after a null backend update, and preserving explicit false/zero values are prototype evidence-handling constraints, not newly invented Nimbus business rules.

Coverage:

- Initial explicit null statement date, followed by a customer-supplied date.
- Initial explicit null requested amount, followed by a customer-supplied amount.
- Previously confirmed statement date and amount, each cleared by a backend null and subsequently reported by the customer.
- Initial and tool-supplied false fraud flags and zero amounts retained as verified values.
- Null clearing followed by a new authoritative restoration.
- Verified zero recurring fee used in the outage formula.

The existing scenario protocol can express null clearing faithfully: a `role: tool` message with a nonempty `context` dictionary, such as a field mapped to JSON null, is observed before the following customer turn. Non-customer tool messages do not increment the expected customer-turn index. These fixtures do not pretend that customer text is a tool response.

Expected values are under `expected`, removed by `model_input`. Monetary explanations may still show the requested amount, but customer-reported date/amount evidence must not permit issuance. First-turn eligibility followed by post-clear pending status tests revocation, not only initialization. Explicit backend zero and false are non-null evidence and should not be rejected by a truthiness test.

Validation: account-schema validation of every initial record and chronological tool patch, per-customer-turn oracle count, and oracle removal. No live model calls were made. These are development regression cases and are not held-out acceptance evidence.
