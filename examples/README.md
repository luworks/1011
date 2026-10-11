# MVP examples — final model selection pending

- `original-conversation.jsonl` is a real six-turn Claude Haiku 5.5 API replay from `runs/final-live-replay`; `replay-manifest.json` records its exact older source and prompt version. Its source hash differs from the current offline replay. It demonstrates that historical run only, not the current source or a comparative model result.
- `offline-conversation.jsonl` is a separately generated current-source fixture replay with its own manifest. It is not an LLM score.
- Both examples show the $82.50 outage amount, an unsupported-tax boundary, and the 30-day request window. Missing fraud/history checks block issuance. No credit or external handoff occurred.
- `summary.json` preserves the historical replay summary and provenance. There is no final comparative score in this MVP export; an empty model-comparison table must not be read as an evaluation result.
- `frozen_baseline.zip` and `historical-baseline-manifest.json` are preserved historical inputs using a superseded development cohort. They are excluded from formal selection. The baseline archive hash was checked against its original manifest before curation.
- `manifest.json` identifies these scopes and hashes. Final evaluation is progressing separately; a runnable MVP is not a completed model selection.
