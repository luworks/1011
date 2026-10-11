# Coordinated improvement window

Started 2026-10-11 12:41 America/Los_Angeles. First consolidated evidence readout due before 13:01. This is a progress deadline, not a promise of exhaustive correctness or completed long-running benchmarks.

## Owners and write boundaries

| Owner | Owns | Handoff |
|---|---|---|
| MVP coordinator (this task) | workflow/CLI/provider integration, source release, live replay, final package/report | `docs/mvp_fix_status.md` |
| eval-model selection | model configuration, evaluation scoring, independent development/regression/acceptance cases, model experiments | `docs/eval_handoff_status.md` |
| policy eval | timestamped policy snapshots, paired comparison runner/oracles, change and open-decision registers | `docs/policy_eval_handoff.md` |
| 评估 NimbusCare 客户对齐文件 | proposed service charter and its adversarial checks | `docs/service_charter_handoff.md` |

Shared core files have one writer. Other owners propose core changes in their handoff instead of editing them concurrently. Existing isolated runs retain their frozen inputs; historical results must not be relabeled as validation of a new release.

## Relay and promotion gates

1. **Tune the workflow.** Diagnose raw traces; change general extraction, request scope or evidence contracts. This window does not launch weight fine-tuning. Retain unsuccessful intermediate runs. Pass deterministic regressions and replay the full original conversation with exact model/thinking configuration.
2. **Freeze and validate models.** Copy/hash code, prompt, charter, corpus, configuration, cases and oracle before live calls. Exclude expected answers from inputs. Evaluate independent paraphrases and mixed requests before fresh held-out acceptance. Candidate claims restricted by a schema are system behavior, not unconstrained model reasoning accuracy.
3. **Compare policy versions.** Hold model, thinking, workflow, cases and repeats constant within each pair. Report raw and final effects separately, with improvements and regressions. Open business decisions have no invented unique answer. Existing A/B runs on older frozen workflows are informative but cannot promote policy on the new workflow by themselves.
4. **Attack the candidate.** Test forged verification, instructions inside customer/source text, correction/conflict histories, missing evidence, knowledge gaps, excessive refusals, genuine multi-question turns and service-principle pressure. Include both positive and negative controls. Failures return to the relevant owner; tuning on holdout retires it as holdout.
5. **Promote only with evidence.** No automatic default-policy switch, real credit issuance or external escalation. A ready MVP can be delivered while model/policy selection remains pending. Record coverage, denominators, costs, uncertainties and unresolved business decisions.

## Budget and evidence controls

All paid work uses the same absolute ledger, `runs/budget.json`. The user raised the cumulative policy experiment authorization to US$70; it is the shared overall ceiling, not US$70 per task. Existing model-selection US$25 cumulative cap remains conservative until the coordinator allocates any further authorized capacity. Include prior spend, retries and conservative unknown reservations. Do not erase or reset the ledger. No new above-high thinking experiments.

Every handoff names the artifact path, start/end state, exact input hashes, completed/planned denominator, paid usage, test result and next owner. Report completion separately for code, local tests, live replay, comparative evaluation and packaging. Manual review of a finite suite cannot establish that the system behaves correctly in every possible situation.

## Current focus

The active general fixes are missing bill-item extraction, old-topic repetition, and unsupported downstream tax claims. The coordinator is validating `workflow-v6`; the eval owner is preparing independent regressions and fresh acceptance. Policy A/B runs continue only inside their existing frozen snapshots. The service-charter owner is testing whether helpfulness can weaken authority or evidence boundaries.
