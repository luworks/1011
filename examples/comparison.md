# Curated model evaluation snapshots

These are the selected runs, not an aggregate across all experiments. Each row retains its own suite, repetition count and denominator. Development results are not held-out validation. Costs are client estimates; unknown/reserved costs are separate from reported usage. Structured assertion metrics do not measure unrestricted natural-language hallucination. Turn timing is end-to-end where available; missing turn timing is not replaced by API-call timing. GPT 5.4-era runs are development history and excluded from final selection, whose candidates include GPT 6.1 Sol and GPT 6 Luna at supported thinking levels plus Opus 5.5, Sonnet 5.5 and Haiku 5.5. Each configuration is scored separately. Accuracy ranks first, followed by end-to-end turn P95/P50, with price last. Development screening is separate from matched finalist frozen comparisons; incomplete coverage cannot establish a global winner.

| Run / suite | Configuration | Completed / planned | Conversation success | Pre-gate assertions | Post-gate assertions | Escalation recall | Turn P50 seconds | Turn P95 seconds | Turn samples | Reported cost USD | Reserved/unknown USD | API-error calls |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

See `summary.json` for complete metrics, per-case checks and failures, aborted runs, call telemetry, and run manifests. `manifest.json` records hashes of the original source files. A provided conversation trace, when included, is a separately identified replay rather than part of the benchmark denominator.

This MVP export contains only a historical conversation replay, so no benchmark rows are present. Final model evaluation is pending. See `README.md` in this directory.
