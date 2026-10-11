`workflow-v11-sonnet-medium/` is the single live replay of the supplied conversation on workflow-v11 with Claude Sonnet 5.5 adaptive/medium: six turns, zero technical failures, $82.50, no $75 cap, tax unknown → human clarification, day 14 of 30, pending verification. It is not fresh V3 acceptance.

# Versioned MVP examples — final comparative selection pending

`workflow-v8/` is the latest scoped live repair example: real Haiku 5.5 adaptive/medium, six turns, seven scoped checks passed, 13 API calls, estimated US$0.011434, 63.154 seconds across all turns. Its exported workflow file hash matched the workspace at export (`2a561f1…`). Later diagnostics changed the workspace to `8ce60a1…`; this trace is not a real-model rerun of that new hash. Original run manifest and source hashes are preserved. Raw candidate mismatches remain visible; this is not evidence of perfect reasoning or final model selection. The tax claim vocabulary is schema-constrained to corpus coverage. Older artifacts below remain historical and are not relabeled as v8 validation.

- `original-conversation.jsonl` is a real six-turn Claude Haiku 5.5 API replay from `runs/final-live-replay`; `replay-manifest.json` records its exact older source and prompt version. Its source hash differs from the current offline replay. It demonstrates that historical run only, not the current source or a comparative model result.
- `offline-conversation.jsonl` is a separately generated earlier-source fixture replay with its own manifest. It is not an LLM score.
- Both examples show the $82.50 outage amount, an unsupported-tax boundary, and the 30-day request window. Missing fraud/history checks block issuance. No credit or external handoff occurred.
- `summary.json` preserves the historical replay summary and provenance. There is no final comparative score in this MVP export; an empty model-comparison table must not be read as an evaluation result.
- `frozen_baseline.zip` and `historical-baseline-manifest.json` are preserved historical inputs using a superseded development cohort. They are excluded from formal selection. The baseline archive hash was checked against its original manifest before curation.
- `manifest.json` identifies these scopes and hashes. Final evaluation is progressing separately; a runnable MVP is not a completed model selection.
