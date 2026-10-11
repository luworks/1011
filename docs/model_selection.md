# Model selection record

**Gate status:** no configuration met the zero-critical / full-escalation gate. **Best observed (updated after Stage 5):** Claude Sonnet 5.5 (`claude-sonnet-5-5`), adaptive thinking, medium effort — config ID `anthropic/claude-sonnet-5-5/adaptive/medium`. Haiku 5.5 adaptive/medium (the earlier development default) remains the low-cost fallback. Stages 1–4 below record the original Haiku decision; Stage 5 supersedes it.

This is a decision for this prototype on the evidence below, not a claim of population-level superiority. Screening many configurations and promoting stage winners introduces selection optimism.

## Selection rule (fixed before results)

1. **Accuracy first:** zero observed critical final failures and full mandatory-escalation recall act as gates; then final conversation success.
2. **Speed second:** end-to-end customer-turn P95, then P50 (both model stages, retrieval, policy gate, validation and retries — not API-call time alone).
3. **Cost third:** usage-priced cost per successful conversation.

Each model + thinking/effort setting is a separate configuration with its own `config_id`; settings of the same model are never merged into one score. Evaluation thinking was capped at **high** by the user; no xhigh/max calls were used for selection. Expected answers are removed before any scenario reaches the model. Technical failures and skipped runs stay in the denominator. Older GPT-5.4 results are development history only and are excluded.

## Stage 1 — Screen (22 configurations)

- Run: `runs/frontier-screen-high`, report `runs/frontier-screen-report/`.
- Scope: all 22 allowed configurations across GPT-6.1 Sol, GPT-6 Luna, Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5; three development cases (`tax_gap`, `above_three_hundred`, `deadline`).
- Result: every configuration passed 3/3 with zero critical failures and zero technical failures. Accuracy did not discriminate; the screen was used for latency/cost and promotion only.
- Haiku adaptive: low/medium/high P50 8.6 / 8.7 / 11.5 s at equal accuracy; raw (pre-gate) assertions 2/3 for every adaptive level.

## Stage 2 — Development suite (10 configurations × 24 cases, workflow v5)

Run `runs/frontier-dev-high`, report `runs/frontier-dev-report/`. One execution per case.

| Configuration | Final success | Critical | Escalation recall | Raw (pre-gate) assertions | Usage cost, 24 cases |
|---|---:|---:|---:|---:|---:|
| Haiku 5.5 adaptive/high | 23/24 | 1 | 6/7 | 19/26 | $0.051 |
| Haiku 5.5 thinking disabled/high | 23/24 | 1 | 7/7 | 9/26 | $0.025 |
| Sonnet 5.5 adaptive/high | 23/24 | 1 | 6/7 | 25/26 | $0.750 |
| Sonnet 5.5 between_tools/high | 23/24 | 1 | 6/7 | 13/26 | $0.528 |
| Opus 5.5 adaptive/medium | 23/24 | 1 | 6/7 | 25/26 | $1.251 |
| Opus 5.5 adaptive/high | 22/24 | 2 | 6/7 | 25/26 | $1.320 |
| GPT-6.1 Sol low | 22/24 | 2 | 6/7 | 24/26 | $0.356 |
| GPT-6.1 Sol high | 21/24 | 3 | 6/7 | 23/26 | $0.539 |
| GPT-6 Luna low | 21/24 | 3 | 6/7 | 20/26 | $0.020 |
| GPT-6 Luna high | 21/24 | 3 | 6/7 | 20/26 | $0.033 |

Findings:

- The deterministic policy gate equalizes final accuracy across most configurations; the Claude family tied at the top.
- Raw model correctness still matters because the gate cannot repair every upstream misunderstanding. Haiku without thinking reached only 9/26 raw assertions versus 19/26 with adaptive thinking, so thinking-disabled Haiku was rejected as too gate-dependent.
- At tied final accuracy, Haiku costs 10–25× less than Sonnet/Opus.

## Stage 3 — Independent regression (28 new cases, workflow v8)

Workflow v6–v8 repaired understanding-stage defects found in development. A new 28-scenario regression set was then run once per configuration. Run `runs/v8-independent-regression`; metadata-corrected offline re-score `runs/v8-regression-checkpoint-report/` (the correction moved explanatory annotations out of the scored fields; it changed no inputs or executable assertions — see `docs/v8_regression_manual_review.md`).

| Configuration | Final success | Critical | Escalation recall | Amount accuracy | Over-refusal | Cost / conversation | Turn P50 / P95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Haiku 5.5 adaptive/medium** | 23/28 | 0 | 9/9 | 32/33 | 1/32 | ≈ $0.0025 | 11.6 / 15.7 s |
| GPT-6.1 Sol low | 23/28 | 0 | 9/9 | 31/33 | 2/32 | ≈ $0.016 | 10.0 / 13.3 s |
| GPT-6.1 Sol high (incomplete, 13/28) | 10/13 | 0 | 8/8 | 18/18 | 0/18 | — | 23.1 / 32.9 s |

Sol high was dropped: its turn latency was roughly double at no demonstrated accuracy gain.

## Stage 4 — Fresh held-out acceptance (acceptance v2)

16 scenarios authored blind from the policy text (`docs/acceptance_v2_provenance.md`), 3 repeats each = 48 planned executions per configuration. Prompts and workflow were frozen before the run. Runs `runs/v8-acceptance-haiku-medium` and `runs/v8-acceptance-sol-low`, scored offline with the project scorer against the corrected fixture `runs/oracle-metadata-correction-v1/acceptance_v2.json`.

Both runs complete (48/48 executions each, scored 13:06 PDT):

| Configuration | Final success | Technical (fail-closed) | Critical | Critical caused by technical failure | Escalation recall | Unsupported tax claims | Cost / conversation | Turn P50 / P95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Haiku 5.5 adaptive/medium** | 34/48 (71%) | 7/48 (15%) | 6 | 6/6 | 18/24 | 0 | ≈ $0.0024 | 11.2 / 16.6 s |
| GPT-6.1 Sol low | 24/48 (50%) | 21/48 (44%) | 12 | 12/12 | 12/24 | 0 | ≈ $0.0147 | 10.0 / 13.2 s |

Failure analysis for Haiku:

- **All 6 critical failures are technical failures.** The understanding-stage output failed the workflow's own contract checks, so no decision was produced. The customer received the fixed safe reply (“No credit has been issued. Please retry or request human assistance.”). The scorer counts this as a missed mandatory escalation because no structured decision exists; every missed escalation above comes from these runs. No wrong amount, wrong governing policy or unsupported tax claim was emitted.
- The 7 non-technical failures are all non-critical and conservative: an amount withheld as `pending_verification` where the oracle expected a calculable, eligible credit (4: cases 01 and 15), and an extra `unknown` intent (3: case 08).

## Stage 5 — Sonnet and Opus on the same held-out cohort

Requested because Sonnet/Opus had higher raw accuracy in development. Same pinned v8 snapshot (code SHA256 `4862475…`, verified), same corrected fixture (`6fd85011…`), 3 repeats. Runs: `runs/v8-acceptance-sonnet-opus-sharded/` (each configuration split into 4 case shards and run concurrently, 16 processes). The concurrency caused API connection errors, which are infrastructure failures rather than model failures. They are reported separately and excluded below. Sonnet medium's 8 affected conversations were rerun at 2-way concurrency (`rerun-*` directories), so its 48/48 is complete. An earlier unsharded attempt (`runs/v8-acceptance-sonnet-opus/`, 5 conversations) was stopped for speed and is not scored.

| Configuration | Scored executions | Final success | Contract fail-closed | Critical | Escalation recall | Amount accuracy | Unsupported tax claims |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Sonnet 5.5 adaptive/medium** | 48 | **44/48 (92%)** | 4 | **1** | **23/24** | 50/54 | 0 |
| Sonnet 5.5 adaptive/high | 37 (11 infra) | 29/37 (78%); 29/48 full | 8 | 6 | 13/19 | 32/40 | 0 |
| Haiku 5.5 adaptive/medium | 48 | 34/48 (71%) | 7 | 6 | 18/24 | 43/54 | 0 |
| Opus 5.5 adaptive/high | 44 (4 infra) | 25/44 (57%); 25/48 full | 19 | 12 | 11/23 | 31/50 | 0 |
| Opus 5.5 adaptive/medium | 35 (13 infra) | 19/35 (54%); 19/48 full | 16 | 11 | 6/17 | 22/38 | 0 |
| GPT-6.1 Sol low | 48 | 24/48 (50%) | 21 | 12 | 12/24 | 30/54 | 0 |

- Every critical failure in every configuration was an understanding-contract rejection that failed closed. The customer got the safe “no credit issued, request human assistance” reply, never a wrong amount or policy.
- Sonnet medium: 0/51 over-refusals. Its four failures were all fail-closed (cases 05, 08, 12×2).
- Higher effort did not help: Sonnet high and both Opus settings failed the understanding contract more often.
- Cost: usage-priced ≈ $0.030 per conversation in the sharded run, $0.045 in the low-concurrency rerun, roughly 15× Haiku. The ledger rose to ≈ US$63 mainly because reservations for failed connection attempts are conservatively retained as unknown charges.
- Latency: concurrent-run latencies are not comparable. At 2-way concurrency Sonnet medium turn P50 was 10.8 s (max 14.0 s, n=11), comparable to Haiku's 11.2 s. In the uncontended stage-1 screen, Sonnet adaptive/medium P50/P95 was 3.7/7.1 s vs Haiku 8.7/9.5 s.

**Updated decision:** Sonnet medium has one critical failure and 23/24 escalation recall, so it does not pass the gate; it is the best observed configuration, pending fresh V3. It ranks first under the accuracy-first rule, with the fewest critical failures and the best escalation recall. Its speed is comparable or better, and its cost is higher but small in absolute terms.

## Original Haiku decision rationale (Stages 1–4)

- **Accuracy:** Haiku adaptive/medium tied the best final accuracy in development (via adaptive/high) and on the v8 regression, with zero critical failures and 9/9 escalation recall there. On the fresh held-out cohort it reached 34/48 versus 24/48 for Sol low and failed closed far less often (15% vs 44% of executions).
- **Speed:** Haiku is slower than Sol low (about +1.5 s P50, +3 s P95). Under the rule, speed only ranks configurations within the same accuracy tier, so this trade-off is accepted.
- **Cost:** about 6× cheaper than Sol low per conversation, and 10–25× cheaper than Sonnet/Opus at equal final development accuracy.
- **Medium over high:** equal screen accuracy at a faster P50 (8.7 s vs 11.5 s) and lower cost. Medium was then validated directly on the v8 regression and the held-out cohort.
- **Original conversation:** a live six-turn replay on Haiku adaptive/medium (`examples/workflow-v8/`) passed 7/7 scoped checks with zero technical failures: 13 calls, ≈ $0.011.

## Known gaps and residual risk

- Haiku adaptive/medium itself was not in the stage-2 shortlist; adaptive/high stood in for it there.
- Sonnet and Opus had higher raw (pre-gate) accuracy but were not carried into the v8 stages because of cost. Higher raw accuracy might reduce understanding-stage technical failures. That comparison is untested.
- The 15% held-out fail-closed rate is safe but an availability cost. It is the main improvement target: the understanding-contract checks or a single bounded retry.
- Automatic scores are closed-oracle checks of authored assertions, not a general hallucination rate. Deadline and adjunct-answer coverage is thin; semantic disagreements need human adjudication.
- The shipped workspace includes post-freeze diagnostics and redaction changes that were not part of the measured v8 snapshot.

## Reproduce

```sh
./run.sh replay --matrix config/eval-models-high.json --config-id anthropic/claude-haiku-5-5/adaptive/medium
./run.sh evaluate --matrix config/eval-models-high.json --cases fixtures/acceptance_v2.json --suite frozen --repeats 3 --only-config anthropic/claude-haiku-5-5/adaptive/medium --max-cost-usd 25 --output runs/NEW_DIRECTORY
```

All live runs share the `runs/budget.json` ledger (≈ US$23.15 after both acceptance runs).
