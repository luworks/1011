# Policy-Grounded Agent Prototype

> **Closeout status:** workflow-v11 is locally verified, and one live replay of the supplied conversation on v11 with Claude Sonnet 5.5 adaptive/medium passed all six turns with zero technical failures ([examples/workflow-v11-sonnet-medium](examples/workflow-v11-sonnet-medium/walkthrough.md)). Fresh V3 acceptance is unrun. The v10 live replay failed on turn 4. Haiku adaptive/medium remains the committed development default. Held-out acceptance v2 on pinned v8 code (16 scenarios × 3 = 48 per configuration): Sonnet 5.5 adaptive/medium 44/48 (1 critical, escalation 23/24), Haiku adaptive/medium 34/48 (6), Sonnet high 29/48 (6), Opus high 25/48 (12), Sol low 24/48 (12), Opus medium 19/48 (11). No configuration met the zero-critical / full-escalation gate; Sonnet medium is the best observed configuration, pending fresh V3. See [model selection](docs/model_selection.md). No new model tests are running. See [Claude handoff](docs/CLAUDE_HANDOFF.md) and [closeout](docs/closeout.md).

A runnable CLI for Nimbus Wireless billing questions. It separates language-model understanding from a reviewed, deterministic policy decision gate. It exposes the retrieved source text, governing policies, candidate decisions, final decisions, and missing verification for each customer turn.

## Quick start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). Run from the extracted project directory:

```sh
uv sync --frozen
./run.sh doctor
./run.sh replay --offline
uv run pytest -q
```

`run.sh` changes to the project root and invokes `uv run --frozen prototype`. The offline replay uses explicit fixtures for the supplied transcript; it is not an LLM evaluation or a general offline chatbot.

For real model calls, create a local `.env` using `.env.example`, set `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`, and select a configuration from `config/eval-models-high.json`. The current evaluation matrix contains 22 model/thinking configurations across five model families, capped at high effort; configuration presence is not evidence of access or a completed evaluation. `config/development-models.json` retains the earlier four-model development experiment and must not substitute for the final comparison:

```sh
./run.sh doctor --matrix config/eval-models-high.json --check-api --provider openai --model gpt-6.1-sol
./run.sh replay --matrix config/eval-models-high.json --provider openai --model gpt-6.1-sol
./run.sh chat --matrix config/eval-models-high.json --provider openai --model gpt-6.1-sol
./run.sh evaluate --matrix config/eval-models-high.json --suite dev --max-cost-usd 40
./run.sh report --run-dir runs/REPLACE_WITH_RUN_DIRECTORY
```

The candidate families are **GPT 6.1 Sol** (`gpt-6.1-sol`), **GPT 6 Luna** (`gpt-6-luna`), **Claude Opus 5.5** (`claude-opus-5-5`), **Claude Sonnet 5.5** (`claude-sonnet-5-5`), and **Claude Haiku 5.5** (`claude-haiku-5-5`). Each supported model plus thinking/reasoning setting is a separate configuration with its own `config_id`; the same model at different thinking levels must not be merged into one score. Anthropic candidates use `--provider anthropic`. Earlier GPT 5.4 / GPT 5.4 mini experiments are retained only as development history and excluded from final model selection. Access is account-dependent; a configured model is not evidence that credentials or access work. No provider/model fallback is performed silently. Live commands spend API credits. All live commands share the default `runs/budget.json` ledger. The user authorized a **US$70 overall cumulative budget**; the model-selection branch currently applies the conservative **US$40 process stopping line on the shared ledger**. Both include all prior shared-ledger spend; read the ledger for the current total. The CLI retains its conservative US$5 default; pass `--max-cost-usd 40` to use the model-selection branch cap on the same ledger, including probes and replays. `--ledger` must resolve to the existing shared absolute ledger for this coordinated experiment; `--max-cost-usd` changes its cap. Evaluation reserves estimated costs before requests, includes retries, and stops when its budget cannot fund another request. Estimates are not provider invoices. Do not publish `.env` or unreviewed run logs.

## What a reviewer should see

The supplied conversation is processed chronologically. Previous customer statements and historical agent confirmations are available only after they appear. Historical agent confirmation is labeled as supplied transcript evidence, not a newly performed backend check.

Terminal output displays governing IDs, source paths and line references, missing checks, gate corrections, and the reply. The saved `turns.jsonl` contains full retrieved excerpts and the structured raw/final decisions. Use the JSON trace when inspecting citation content rather than just the terminal summary.

For the outage in the supplied conversation, Rule 3 yields `$225 / 30 × 11 = $82.50`. The monthly amount already covers three lines. The general Rule 2 `$75` ceiling does not apply, but Rules 4 and 5 still govern escalation and authority. Missing fraud/dispute-history checks prevent an automatic credit even when an amount can be calculated. The 30-calendar-day outage-request window is distinct from the 60-day statement-dispute window.

KB-1004 supports the credit calculation base. It does **not** establish whether taxes or regulatory fees are adjusted afterward. The final response states this coverage gap and requests human clarification instead of asserting either a refund or no refund.

## Policy versions and experiment budget

Policy-pair snapshots and matched version experiments are documented in
[docs/policy_versions/README.md](docs/policy_versions/README.md). Use
`--policy-version` for an explicit snapshot or `compare-policies` for an exact
model/configuration comparison. Versioned evaluation excludes reviewed open
business decisions from unique-answer scoring and separately checks evidence
boundaries. The latest user authorization raises the **same cumulative ledger
cap to US$70** for these experiments; pass `--max-cost-usd 70` explicitly.
This is the overall shared ceiling, not a per-task allowance. The model-selection branch uses a US$40 process stopping line against that same shared ledger; this is not a new or per-process budget. All owners use the same absolute `runs/budget.json` ledger and include prior spend/reservations.

## Architecture and boundaries

1. The official OpenAI Responses or Anthropic Messages SDK extracts intents and source-quoted candidate facts.
2. Source checks preserve reported, confirmed, unknown, and conflicting facts. Customer assertions cannot establish backend verification.
3. Local text retrieval adds explicit related-policy dependencies. Unsupported topics search the complete small corpus. All ten articles, KB-1001 through KB-1010, are loaded despite the excerpt's nine-article heading.
4. The model proposes structured decisions with citations. The program independently applies reviewed policy rules and computes Decimal amounts.
5. Bounded, reviewed response templates render approved conclusions. Unrestricted model prose never becomes a policy promise. Model citation/mismatch errors remain visible in the trace.

This is a closed-policy prototype, not a general policy compiler. A corpus hash lock requires review after policy changes. Exact quote validation does not prove that an extracted value means what the model claims; semantic extraction and intent omissions remain residual risks. The gate cannot repair every upstream misunderstanding, so raw model and final workflow quality must both be measured.

Account lookups are local fixtures. No production billing, payment, or human-support integration exists. Eligibility, a need for human review, and an executed action are different states. This prototype does not issue money or claim an external handoff succeeded.

Replay uses the supplied conversation's request date. Interactive `chat --date 2026-10-05` sets an explicit request date; without this flag chat uses the execution host's local date. `chat --context path/to/account.json` loads explicitly simulated account state; it does not inherit transcript verification. Elapsed full days drive the supplied formula; Decimal results are rounded to cents using half-up rounding. These arithmetic conventions are implementation assumptions where the source lacks finer specification. Missing or contradictory facts must be resolved before a definitive eligibility/action decision.

## Results and evaluation

Run directories contain machine-readable turn traces and manifests/report data, including model configuration, source/prompt versions, usage, errors, and costs. Terminal output provides a readable view. These structures are intended to support a later frontend without duplicating policy logic.

The scenario suite contains 24 development and 16 frozen cases with independent expected outcomes. Cases cover amount/time boundaries, unknown verification, policy exceptions, unsupported tax claims, injection attempts, conflicts, and multi-turn ordering. Deterministic tests also exercise technical failures. Expectations are not sent to the model. Offline runs are labeled and excluded from live model comparisons.

Use development cases to change prompts. Run frozen cases only after candidate settings are fixed; repeat frozen evaluation three times per model. For example:

```sh
./run.sh evaluate --matrix config/eval-models-high.json --suite dev --limit 4 --only-model gpt-6.1-sol --output runs/pilot
./run.sh evaluate --matrix config/eval-models-high.json --suite frozen --repeats 3 --max-cost-usd 40 --output runs/frozen
```

`--only-model` may be repeated; it filters model IDs in the matrix (evaluation does not select models through `--provider`). `--limit` explicitly selects a subset, so do not describe that result as the full suite. `--output` must name a new directory. `report --run-dir` prints that directory’s stored summary; it does not rerun models.

 If frozen failures guide changes, treat those cases as regression data and replace the holdout. Report the actual run denominator, technical failures, skipped cases, and remaining cases rather than calling a budget-truncated run complete.

Compare raw candidate correctness with final policy/amount correctness, required escalation recall, supported-question completion, unsupported claims, conversation success, and cost per successful conversation. Speed is an explicit selection objective: measure end-to-end customer-turn P50/P95 (both model stages, retrieval, policy gate, and retries), alongside API-call timing. API-call means alone do not describe customer-visible response time.

Selection follows the user's strict priority: **accuracy first, then response speed, then price**. Compare final task correctness and critical policy-cap, unsupported-tax, missed-escalation, and fictitious-action errors before speed. Among configurations tied on the accuracy evidence, prefer lower end-to-end turn P95, then P50; price is the final tie-breaker. These priorities are applied lexicographically, with no trade of accuracy for lower cost. Token throughput is not a substitute for customer-visible turn latency.

Screen the 22 at-most-high configurations on the same three development cases (`tax_gap`, `above_three_hundred`, and `deadline`). This is a small screening signal, not a full accuracy score or proof of a globally best configuration. Advance the most accurate, then fastest configuration per model family to all 24 development cases. Run matched 16-case frozen tests with three repetitions only for finalists, as the remaining budget permits. The benchmark runner supports exact case/configuration selection and bounded concurrency (`--case-id`, `--only-config`, and `--jobs 4`); these controls must not alter the common case subset between screening candidates. Clearly preserve each configuration's development/frozen stage and test denominator. Missing coverage, failed probes, or budget-limited evaluations cannot establish a global winner; even a completed finalist comparison ranks only the tested finalists. Report exclusions and timing sample counts alongside any scoped recommendation.

The US$70 overall authorization and US$40 model-selection process stopping line are cumulative. Estimate each stage against the shared ledger before starting; further model-branch allocation is coordinated centrally, while exceeding the overall US$70 requires new user authorization. Preserve partial results instead of silently expanding spend. Semantic disagreements require review. Zero failures in a small suite is not a zero-hallucination guarantee. Current measured results and limitations are summarized in the accompanying design memo.

## Curating evaluation artifacts

Export only explicitly selected runs after reviewing their scope. This does not rerun models or reinterpret failures:

```sh
uv run python scripts/export_results.py runs/SELECTED_DEV_RUN runs/SELECTED_FROZEN_RUN --replay runs/SELECTED_REPLAY
```

The exporter writes `examples/summary.json` with metrics, manifests, call telemetry and per-case pre/post errors, removing repeated full turn payloads; `comparison.md` summarizes per-run denominators and costs. Optional `original-conversation.jsonl` preserves the selected replay's full evidence. `examples/manifest.json` records source-file SHA256 hashes and export scope. No benchmark scores are merged across different experiments, and selected runs may be explicitly incomplete. Secret checks run before writing. These files are the only selected result snapshots included in the submission.

The reusable adversarial strategy is documented in [docs/evaluation_strategy.md](docs/evaluation_strategy.md). `--cases path/to/scenarios.json` selects a separately reviewed scenario suite; it does not automatically compile a new business policy. The source hash lock rejects unreviewed policy revisions. Deterministic generated attacks, actual LLM results, and unassessed natural-language claim metrics remain separate.

## Submission packaging

```sh
uv run python scripts/package.py
```

Creates `dist/policy-grounded-agent-prototype.zip` containing `agent_prototype.zip` and the one-page `design_memo.md`. The inner archive has this README at its root. Packaging uses a narrow allowlist, excludes `.env`, virtual environments and arbitrary run directories. Curated artifacts under `examples/` are included with their own manifest; these are reviewed snapshots, not all local runs. Packaging rejects matching local credential values or recognizable API secrets. It does not replace reviewing artifacts before distribution. Package creation is separate from test or live-evaluation success.

When available at packaging time, the standalone `report/dist/index.html` is included at the inner archive root as `model-evaluation-report.html`. Open that file in a browser to inspect the curated model-evaluation report. Its presence and stated coverage must be checked before final delivery; packaging can run while the report is still pending.

The backend CLI MVP and model selection have separate completion states. Curated `examples/workflow-v8/` contains the current scoped live repair, while root-level older live/offline examples retain their historical versions; neither implies a completed final model comparison. Final model evaluation is being advanced in the dedicated evaluation chat, with source/version and cohort alignment required before promoting results.

The submission includes the report as a **prebuilt standalone HTML file**. Its frontend source and build workspace are not included in the inner ZIP. A report-build helper under `scripts/` may require those workspace-only sources; it is not a supported report-rebuild command from the extracted submission. The CLI, tests, offline replay, and static HTML remain usable independently.

## Proposed agent service principles

[Agent Service Charter](src/policy_agent/agent_service_charter.md) is a one-page, team-proposed service standard, not official Nimbus Wireless values or a customer-approved policy. The customer's real-world identity and mission remain unverified. The existing policy gate retains authority; a deterministic response composer adds respectful framing and next steps without additional model calls. The charter is excluded from billing retrieval and cannot authorize credits or invent tax rules. Turn traces and new run manifests record its version and SHA256. Historical evaluation artifacts predate this presentation change and are not evidence of its live-model performance.

## Current workflow-v8 repair evidence

`examples/workflow-v8/` preserves the real Haiku 5.5 adaptive/medium replay, original manifest, walkthrough, and seven scoped acceptance checks: six turns, retained bill item, current tax question only, tax candidate unknown, correct amount, correct deadline, and no issuance. All seven passed; 13 calls cost an estimated US$0.011434, with 63.154 seconds summed end-to-end turn time. This demonstrates the original conversation on that exact workflow snapshot, not a global model winner.

The repair requires quoted fact inventory and current-request scope, uses a narrow source-quoted bill-item extraction fallback when necessary, prevents null unknowns from inheriting trusted verification, and restricts downstream tax claims to reviewed coverage. The native tax schema enforces unknown rather than proving autonomous model reasoning. Candidate amount/action/status/policy-ID mismatches remain visible and gated. Independent paraphrase, adversarial, and matched held-out comparisons remain separate acceptance work. The coordinator reports a subsequent 315+ local-test checkpoint; the final release test count will be recorded after the report freezes. Release-validation records identify the specific package snapshot actually checked.

## Post-freeze evidence status

The v8 live replay and immutable benchmark snapshot retain workflow SHA256 `2a561f1aa2bcc42d5ef245c473983417dcd90472d53304601f6da9d2ec30b753`. Post-freeze diagnostics are now integrated into workspace workflow SHA256 `8ce60a12d3200fc73116d205d5489df6b020c3e58e8424b73c9e5e175e8de88f`. The older live replay is not a real-model rerun of this new hash. Diagnostics improve failure visibility and do not close the two utility failures documented in [remaining semantic limits](docs/remaining_semantic_limits.md): background credit references can be treated as requests, and potentially synonymous item labels can remain conservatively conflicting. Their benchmark penalties are retained.

The complete policy-text experiment in [the audited report](docs/policy_comparison/20261011-full-v5-audited/report.md) is a separate frozen **workflow-v5** cohort: Sol medium and Luna medium each completed 120 paired comparisons. Raw composite results improved (85→100 and 63→75), but final composite results each decreased by one (105→104 and 95→94). The optimized policy is **not promoted**. These results cannot select the best v8 model or validate post-freeze code. A further 27 charter attacks passed locally according to the coordinator; that finite structural result is separate from live-model performance. Final model-selection and report evidence may remain explicitly pending in a stage delivery.

## Model selection status

Held-out acceptance v2 on pinned v8 code (16 scenarios × 3 = 48 per configuration): Sonnet 5.5 adaptive/medium 44/48 (1 critical, escalation 23/24), Haiku adaptive/medium 34/48 (6), Sonnet high 29/48 (6), Opus high 25/48 (12), Sol low 24/48 (12), Opus medium 19/48 (11). No configuration met the zero-critical / full-escalation gate; Sonnet medium is the best observed configuration, pending fresh V3. See [model selection](docs/model_selection.md). Every critical failure in every configuration was a fail-closed understanding-contract rejection, never a wrong amount or policy. Sonnet high and both Opus rows include API connection errors from 16-way concurrent runs and are infrastructure-confounded. To use the best observed configuration:

```sh
./run.sh replay --matrix config/eval-models-high.json --provider anthropic --config-id anthropic/claude-sonnet-5-5/adaptive/medium
```

## Stage-delivery freeze — 2026-10-11

The 12:54:59 PDT checkpoint described here (62/84 screening runs) is historical; the packaged HTML report now includes the completed held-out comparison above. Fresh/high model acceptance remains pending. The backend CLI, scoped v8 live repair, and local release checks can be delivered independently of that unfinished comparison. Final local suite at this freeze: **316 passed**. Report HTML SHA256: `abfc9b99cc0214b56c9fc8f929e673183eb1bee2fb87ec2e503b3779cd32a908`.
