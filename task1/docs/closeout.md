# Closeout — 11 October 2026

Status: development handoff at the user's request. No new API runs or model-search stages are authorized by this closeout. The existing authorization to commit and push verified work remains in effect.

## Delivered

- Python CLI and policy-grounded workflow with source provenance, closed response templates, shared cost ledger and provider telemetry.
- Development default: Claude Haiku 5.5, adaptive thinking, medium effort (committed config). Best observed on held-out acceptance: Claude Sonnet 5.5 adaptive/medium (44/48), which still misses the zero-critical gate; neither is an acceptance winner. Explicit model/configuration overrides remain available.
- Shared one-repair-per-turn content budget across schema and cross-field validation; technical failures remain separate from policy decisions.
- Independent request-scope review, preserving genuine multiple questions and explicit repeat requests while filtering background references.
- Customer item references separated from trusted billing facts. Unresolved aliases remain pending; switching trusted items revokes old item-specific verification. No string-subsequence alias grants authority.
- Scenario-specific policy boundaries retain unresolved business choices and known mandatory human-review requirements. Internal decision IDs stay in traces rather than customer replies.

## Verified evidence and limits

- Current v11 local suite: **388 passed** at the coordinator checkpoint. This is local verification, not live acceptance.
- Earlier v8 real original conversation passed seven scoped checks (6 turns).
- Completed v8 independent regression: three configurations,28 scenarios each,84/84 executions; each23/28.
- Completed v8 fresh acceptance:16 independent scenarios ×3 repetitions per configuration. Sol-low24/48 successful,21 technical failures; Haiku-medium34/48 successful,7 technical failures. Neither qualified for final selection. The18 conservative critical flags across both configurations are failed-closed missing mandatory responses; manual review did not observe unsafe issuance. Failed answers remain failures.
- v10 real original conversation:6 turns,1 technical failure on turn4;18 calls,estimatedUS$0.0119011,77.203 seconds summed turn latency. Scope action-span validation failed twice; the original failure is retained.
- Stage 5 (after closeout handoff, same v8 code and cohort): Sonnet medium 44/48 (1 critical, escalation 23/24); Sonnet high 29/48, Opus high 25/48, Opus medium 19/48 (connection-error confounded). Details: `docs/model_selection.md`.
- v11 fixes the generic optional-action-span contract and supplies actionable fixed repair feedback. **One v11 live replay of the supplied conversation (Sonnet adaptive/medium) passed all six turns with zero technical failures (17 calls, ≈US$0.174; `examples/workflow-v11-sonnet-medium/`). Fresh V3 acceptance was not performed.** Fresh V3 remains unrun and its expected answers were not used by core authors.
- New scenario policy and boundary implementation exist with local tests. New fixed-Haiku policy comparisons were not started; default source documents were not promoted. The historical v5 comparison completed240pairs/480scenario runs and did not support whole-document promotion.

## Artifacts

The HTML report is the main readout and separates workflow versions and complete/partial measurements. Raw local evidence remains under runs/; curated, redacted evidence is under examples/. Run outputs, credentials, environments and build products are excluded from Git. Packaging includes the standalone HTML.

## Remaining work when resumed

1. Done once with Sonnet adaptive/medium (passed); repeat with the committed default and any final candidate on a frozen v11 snapshot.
2. Run independent repair regressions and untouched fresh V3 with the fixed development model and explicit budget.
3. Run same-model, same-workflow comparisons for original/clarified/scenario policy versions; do not approve business assumptions through scoring.
4. Revisit authoritative invoice-item identifiers/aliases for frictionless name matching. Conservative clarification is retained when identity is unknown.

No general claim of zero hallucinations, universal attack resistance, production readiness or final model optimality is made.
