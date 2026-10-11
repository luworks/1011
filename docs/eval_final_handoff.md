# Evaluation closeout

Status: STOPPED at user request, 2026-10-11T13:09:43.259798-07:00. No automatic resumption, new API calls, model search, or optimization. Process inspection found no active benchmark/evaluate/replay/compare-policies process; all eval subagents have completed. Existing completed results and failures are retained.

## Stable result artifacts

- `runs/v8-regression-report/summary.json`, `selection.json`, `report.md`: all 84/84 development executions, 28 unique scenarios across three configurations. All three scored 23/28 after a documented annotation-only offline correction. Original traces and scores are retained.
- `runs/v8-acceptance-report/summary.json`, `selection.json`, `report.md`: all 96/96 acceptance executions, 16 unique scenarios repeated three times for two configurations. Final selector: `no_qualifying_model`.
- `runs/v8-acceptance-comparison/`: combined original completed acceptance traces, manifests and telemetry.
- `docs/v8_acceptance_manual_review.md`: 96 conversations / 114 customer turns reviewed. Missing mandatory escalation conclusions remain failures; no actual issuance was observed.
- `runs/oracle-metadata-correction-v1/correction_receipt.json`: provenance of annotation relocation; executable expectations and model inputs were unchanged for V8 re-scoring.

| Configuration | V8 acceptance success | Technical failures | Estimated acceptance cost |
|---|---:|---:|---:|
| GPT-6.1 Sol low | 24/48 | 21 | $0.7039954 |
| Claude Haiku 5.5 adaptive/medium | 34/48 | 7 | $0.1139922 |

Haiku adaptive/medium is a development default only, not a final acceptance winner. The user will independently review models; no further model selection is scheduled.

## Explicit unfinished boundaries

- V10 original live replay failed on turn 4. No V10 batch evaluation was launched by this eval owner.
- V11 is a subsequent local repair only, according to the coordinator's closeout receipt; it has not received live acceptance. V8 results must not be relabeled as validation of V10/V11.
- The source-reviewed 14-case development set and 16-case V3 frozen acceptance set remain unrun. Preserved copies: `runs/oracle-v3-source-reviewed/`; provenance and revision receipts: `docs/oracles/`. No new calls will start without a new request.
- Pending policy comparison versions remain unvalidated and are not promoted as the default policy.
- No packaging, HTML, README or design-memo edits were made by this eval owner during closeout. The coordinator owns final delivery integration.

## Cost snapshot

The completed final V8 regression and acceptance stages account for $2.154124 estimated usage, with zero unknown reservations in those stages. The sole shared ledger `runs/budget.json` currently accounts for $23.14739293, including $1.84331730 reserved/unknown upper bounds across all threads and historical work. The shared total is not attributable solely to this eval task and is not a supplier invoice. No ledger reset or reservation release was performed.
