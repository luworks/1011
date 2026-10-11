# Evaluation owner status

Status (12:44 PDT): V6 frozen; independent 16-case understanding regression is RUNNING on Haiku 5.5 adaptive/medium and GPT-6.1 Sol low/high (48 planned conversations). Shared global authorization is US$70; model-evaluation process retains cumulative US$25 cap. Earlier sections below are chronological history, not the current state.

- Test checkpoint: 141 passed (2026-10-11).
- Ledger before screen: US$3.83157, including historical calls; total authorized cap US$25, single ledger `runs/budget.json`.
- Current run: `runs/frontier-screen`, 32 model/thinking configurations, same three dev cases (`tax_gap`, `above_three_hundred`, `deadline`), jobs=4. This is screening, not final acceptance.
- Official families: GPT-6 Luna, GPT-6.1 Sol, Claude Opus/Sonnet/Haiku 5.5.
- Next: strongest observed configuration per family on complete 24-case development suite; matched repeat acceptance for leading configurations within remaining budget.
- Objective: final accuracy first, full-turn latency second, price third. No historical GPT-5.4 result is eligible.
- `examples/frozen_baseline.zip` and the existing preliminary dist archive preserve an older implementation/matrix; they are not the official new selection.
- No final winner exists yet. HTML/report owner should consume the current phase manifests only as progress until final summary/selection paths appear here.

## User scope update

User explicitly capped evaluation thinking at **high**. No xhigh/max/ultra calls are allowed going forward. The old32 sweep was terminated and marked `runs/frontier-screen/interrupted.json`. Official replacement matrix: `config/eval-models-high.json` (22 configs); new matched screen: `runs/frontier-screen-high`. Previously incurred costs and unknown reservations remain in the shared US$25 ledger. Do not combine the interrupted32 sweep with the new cohort for ranking.

## Official screen complete; full development running

- `runs/frontier-screen-high/summary.json`: all22 allowed configurations completed the same3-case screen; no technical failures.
- `runs/frontier-shortlist-high/shortlist.json`: provisional ranking and cost estimates. Ten configs promoted using fastest highest-accuracy eligible config plus independently eligible high setting per model family; deduplicated.
- `runs/frontier-dev-high`: currently running all24 development cases on those10 configurations, jobs4.
- Ledger at start of development: about US$6.05 including historical usage and retained unknown reservations. Screen-based projection for all10 configs over24dev+48acceptance is aboutUS$11.08 additional; not a guarantee.
- Selector audit fixed before development: final selection requires frozen suite and at least3 repeats; bootstrap clusters unique scenario IDs together with all repeats;15 selector tests pass. Core workflow/policy/provider not modified.
- Automatic scores are closed-oracle measures. `docs/eval_methodology_audit.md` records thin deadline/adjunct coverage; finalists will receive supplemental review. No final winner yet.

Screen consumer artifacts are ready: `runs/frontier-screen-report/summary.json`, `selection.json`, and `report.md`. These explicitly say provisional/no final winner. Main HTML may ingest `--run screen=runs/frontier-screen-high` now. New reusable finalizer: `scripts/finalize_evaluation.py` emits compact summary/selector JSON and English conclusions for a completed stage. Final acceptance artifacts will be announced here once ready.

Safety against accidental scope regression: `scripts/benchmark.py` now defaults to `config/eval-models-high.json` and rejects any selected xhigh/max/ultra configuration before requests.13 benchmark tests pass. Main README/CLI evaluation examples should explicitly use this high-ceiling matrix; `config/models.json` remains the expanded capability inventory, not authorization to run higher effort.

## Core update coordination

Received main task's user-authorized generic fixes (line-item extraction, previous-topic bleed, unsupported tax candidate). Existing `runs/frontier-dev-high` process keeps its already-loaded old-cohort code; its results are historical diagnostics, not new-prompt acceptance. **No new paid process or frozen evaluation will start until `docs/mvp_fix_status.md` says READY.** Regression owner is creating `fixtures/understanding_regression.json`; a separate oracle author is creating fresh `fixtures/acceptance_v2.json` because the prior16 holdout has been exposed. Neither author inspects current live results to tune expected answers. Existing `fixtures/scenarios.json` remains unchanged for reproducible older runs. Shared total budget remains US$25.

## New independent suites ready

- `fixtures/understanding_regression.json`:16 dev regressions for generic line-item extraction, old-topic references, genuinely mixed questions and unsupported tax/authority claims. Separate oracle doc: `docs/understanding_regression_oracle.md`. Evaluator support for explicit fact/context/candidate fix contracts is being added and tested before new-cohort calls.
- `fixtures/acceptance_v2.json`:16 fresh frozen scenarios,19 customer turns; fileSHA256 `8ce8f6933fdd541ccac32cb21158f41c6ab55250d4767d74e27cd567a70cbad8`. Independently authored from original policy without current model-output inspection or policy-engine execution. `docs/acceptance_v2_provenance.md` records coverage and source logic. No core author should tune on this file. Supplemental `manual_condition_checks` remain manual annotations, not automatically scored.
- No new paid process has started since the core-change notification. Old-cohort dev remains in flight; waiting on `docs/mvp_fix_status.md` READY.

V5 scoring disclosure added: schema-constrained tax outcomes must not be credited as autonomous raw-model reasoning. Finalizer methods now state this explicitly. New understanding fact/context/candidate checks are supported (204 full-suite passed at evaluator checkpoint); pending coreREADY remains respected. A separate generic metric audit is separating conservative safety violations from ordinary omissions/over-refusals before new-cohort scoring, with old saved results unchanged.

## V6 immutable receipt

Snapshot complete: `runs/snapshots/workflow-v6-high-regression`, all code/config/corpus/charter/docs/fixtures/tests hashed in `snapshot_receipt.json`; no secrets copied. Workflow SHA256 9ecfe70f88f645cd6067761eb3cdbb2385201d19dd7c8bb5771bf5ea8d493696. Core owners may continue changes outside this snapshot. Fixed stale finalizer prose assertion. Full suite latest checkpoint 248 passed / 1 expected failure. New metric `closed-oracle-v2-safety-utility-separated` and independent fact/context/candidate contracts are ready. Global authorized ceiling is US$70; this model-eval process retains cumulative US$25 ceiling against the shared absolute ledger. Next run: 16 independent understanding regressions, Haiku adaptive/medium plus GPT-6.1 Sol low/high. No above-high configs. Old dev cohort is historical, not v6 acceptance.

Core-owner follow-up: benchmark.py enforces the user high ceiling and defaults to eval-models-high.json (tests pass), but current prototype evaluate / compare-policies CLI still defaults to models.json and has no visible effort-ceiling guard. Please apply the same fail-before-call rule in your owned CLI before final delivery. Current isolated regression explicitly selects only medium/low/high, so it is within scope.

## V7 authority bug notice

Main identified explicit-null context fields inheriting verified status after customer fills them. V6 independent regression remains diagnostic only; no V6 fresh acceptance or promotion will occur. Oracle reviewer assigned independent explicit-null/revoked-tool-evidence adversarial cases and False/0 controls in a separate new dev fixture. Existing acceptance_v2 stays untouched. Await v7 READY then freeze a separate snapshot and run matched regressions. Current budget cap25 remains; additional allocation request will state concrete projected use if needed.

Independent null-authority suite ready: `fixtures/null_authority_regression.json` (8 dev scenarios /10 customer turns), SHA256 `54146862faa3e8d1ad07212a5dffde917b16e936c5c95e754720b7d1756e0247`; source rationale `docs/null_authority_regression_provenance.md`. Tool-clear faithfully represented by role:tool/context protocol; includes False/0 positive controls. No API or holdout modification. Finalizer now retains candidate-only and fix-contract failures separately from final safety/utility, metric versions explicit;7 tests pass.

## V7 freeze receipt (12:47 PDT)

`runs/snapshots/workflow-v7-high-regression` frozen with full per-file receipt; workflow SHA256 f3df353e02affd6da19f21bebcf3114eee1b645959965ff11237f7216dee8a85. Combined independent regression is24 cases (16understanding +8null-authority), no expected answers changed. Launching same3 configurations medium/low/high on this snapshot,72 planned conversation executions, shared absolute ledger/cap25. V6 continues diagnostic only; fresh holdout remains unrun pending this gate. Main can continue packaging outside snapshot.

V6 diagnostic checkpoint: Haiku medium16/16 executed, final13/16, fix-contract12/15, post-gate21/21 assertions,0critical; Sol-low16/16 executed, final12/16, fix-contract11/15, post-gate20/21,1technical ValueError on fake-manager case (also scorer flags missing mandatory decision critical; no unsafe reply observed from missing output). Both share3 exact line-item qualifier failures (duplicate/incorrect/missing); reviewer is distinguishing oracle representation strictness from actual missing charge labels, without altering scores. Sol-high pending; no final winner. V7 independent24x3 running separately.

V8 hold notice received12:49: V7 already launched before notice, retains diagnostic status; no fresh acceptance onV7. Main fixing whitespace-only line_item authority/bool check. Independent separate whitespace fixture requested. To avoid burning repeated regression budget, next paid cohort awaits explicit final-core freeze; no further new process untilV8READY. Existing V6/V7 costs retained.

Budget allocation request (2026-10-11T12:47:45.821985): shared ledger nowUS$19.39 including other-thread calls/reservations, model cap25 may stop midstage as policy experiments spend concurrently. Request coordinator allocation up to US$6 ADDITIONAL model-eval actual estimated usage for finalV8 three-config regression plus48 freshacceptance runs per eligible config, with cumulative shared ceiling coordinated below70. Need coordinator set a concrete process cumulative cap (suggest40 while otherowner coordinates), because current ledger is shared and25 is not a model-only allocation. No cap changed yet. Snapshot status timestamps above marked12:49 were approximate; actual V8 coordination occurred before12:48.

V8 snapshot captured 2026-10-11T12:48:01.831910: `runs/snapshots/workflow-v8-high-regression`;28 combined independent cases (16understanding +8null +4whitespace), no oraclechanges. Workflow SHA256 2a561f1aa2bcc42d5ef245c473983417dcd90472d53304601f6da9d2ec30b753; schema SHA256 72ab22c918d14dd291fb3b18d13eddcafe3d1d158a60009eb54ca3da6426eea3. PaidV8 held until full live READY receipt. Separate source-authoring rationale for whitespace cases in docs/blank_item_regression_provenance.md. All files hashed, no secrets copied; core may be committed outside snapshot.

Historical pre-fix full development complete:10configs x24cases =240/240 executions. Consumer exports: `runs/frontier-dev-report/summary.json`, `selection.json`, `report.md`; selectionnot_final_stage. This old imported workflow and older metric cohort is historical only; do not merge its scores withV6/V7/V8 or promote it.

Manual review checkpoint available: `docs/v6_regression_manual_review.md` (40/48 planned conversations,49/57turns). Shared three label failures are oracle qualifier-in-value sensitivity; exact scores unchanged. Sol-low missingmandatorydecision criticalcounter is failed-closed ValueError, not observed unsafe issuance. Root cause cannot be proven because the rejected structured extraction and specific validation branch were not persisted. Taxclaims reviewed19, none categorical; no claimofdeadline/null/blankcoverage.

V8 paid stage started 2026-10-11T12:49:28.946993: finalcoreREADY source hashes matched receipt;28cases x3configs =84 planned. Run`runs/v8-independent-regression`, sameHaiku medium/Sol low/high. Coordinator allocated <=US$6 additional actual model-eval estimate inside global70 and processcap40 shared cumulative; cap40 applied, soleledger unchanged. Will monitor this stage plus subsequent acceptance calls separately against6. No source edits after corecommit40abfd86; isolatedsnapshot source remains primary receipt. Final acceptance only after regression review.

V6 now completed48/48 executions; consumer exports`runs/v6-regression-report/{summary.json,selection.json,report.md}` ready. Sourceversion remains diagnostic only. Sol-low andhigh both have technicalfailures; statusfailed does not mean missingdenominator. No V6selection.

Reporting limitation for final memo: V6 Sol low/high both fail closed on the fake-manager injection with ValueError with a persisted error TurnResult (understanding=null, decisions=[]); the rejected structured extraction was not saved. Shared call telemetry exists but rejected structured understanding is not persisted, so exact semantic/protocol cause cannot be reconstructed from outputs. Do not state these as observed real unsafeaction; metrics conservatively count missingrequireddecision, while manualaudit labels technicalfailure. Suggest future diagnostic retention without changing this frozen cohort.

V8 partial checkpoint 2026-10-11T12:52:12.679175: `runs/v8-regression-checkpoint.json` preserves28/config planned denominators, observedaccuracy and fullturnmedian; livecostpending fullcalltelemetry. Remaining: finish28regression/config, manualauthorityaudit, then fresh16x3 onlyeligibleconfigs on samefrozenV8. No freshheldoutcalls yet.

V8 Haiku extra failure manually located: understanding_tax_pressure_yes repeats a tax-only request as outage_credit+taxes. Extra$30 formula calculation is sourced but unrequested; taxoutcome remains unknown. This is scope/utility error, not unsupportedtaxpromise. Preserveexactintent failure andcritical0. Reviewer:docs/v8_regression_manual_review.md (inprogress). Correction to earliertechnicalnote: errorTurnResult WAS saved; what is missing is rejectedparsedunderstanding andexactvalidatorbranch.

SCORING INTEGRATION DEFECT 2026-10-11T12:53:59.974702: independently authored null/blank/fresh fixtures contain expected.manual_basis/manual_condition_checks provenance annotations; pinned strict scorer rejects these unknown keys, artificially failing otherwise correctcases. No source/expectations will be tuned. Reviewer prepares versioned correctedCOPIES underruns/oracle-metadata-correction-v1 deleting ONLYthoseannotationkeys into a separate non-model sidecar, with rawhash+semanticassertion equality receipt. Existing traces/scores remain; completed traces will be re-scoredoffline explicitly, not called paidrerun. Fresh16 stillunrun; correctedcopy used beforefirstcall. Actualzero controls preserve0/False; utilityfailure is shorter extracted line_item vs trusted qualifier causing falseconflict, not zero-truthiness.

Stable corrected partial HTML input ready: `runs/oracle-metadata-correction-v1/checkpoint_compact_1255.json` (27/28Sol-low,25/28Haiku,10/28high at12:54:59, all0critical;84planned). Includes originalsourcecheckpoint/correctionreceipt, explicitno-winner. Correctedassertion/modelinput hashes equal originals excluding metadata only. Low justcompleted28/28; reviewing promotion separately without waitinghigh, per coordinator.

Sol-low completed corrected23/28,0critical/0technical, allrequiredescalationscorrect; P50/P95 fullturn9.99/13.25s, costUS$0.455889. Per-configpromotion receipt`runs/v8-acceptance-sol-low/promotion_receipt.json`; samefrozenV8 fresh16x3=48started 2026-10-11T12:55:29.672309. No finalwinner; otherconfigregressionspending. Correctedcost/success is0.455889/23, not originalmetadata-failed denominator.

HTML stablepartial path: `runs/v8-regression-checkpoint-report/summary.json` and`selection.json` (no-winner,correctedmetadata provenance,84planned). CompletedHaiku23/28,0critical/0technical,9/9requiredescalations, fullturnP50/P9511.57/15.65s, costUS$0.0709768. Haiku fresh16x3 started`runs/v8-acceptance-haiku-medium` sameV8 and correctedpre-calloracle. Sol-lowfresh running; highregpending. Do not carry rawmetadata denominator into corrected cost/success.

FRESH ACCEPTANCE ALERT 2026-10-11T12:56:53.020608: earlyread-onlyreview finds substantial failed-closedValueError rate on newwording: Sol-low5technical in first8/48 traces (cases01/02/03/06/08), Haiku1technical in first2/48 plus01falseconflict. ExistingV8 protocol brittleness, not observedunsafeissuance. MissingTier2specificresponse stillcountsacceptancefailure. Rawfreshtraces retained; no prompt/oracletuning. Both remainrunning to preserve16x3denominator; likelynoqualifyingfinalmodel ifcriticalmissingmandatorypersists. Manualreview`docs/v8_acceptance_manual_review.md` forthcoming. Subsequentdiagnosticpatch isnotthiscohort andcannotborrowthisacceptance.

EarlyfreshHTMLcheckpoint `runs/v8-acceptance-checkpoint-report/summary.json` and`selection.json`, timestamp 2026-10-11T12:58:02.353910;48planned/config,96for2startedconfigs;highseparatelypendingregression. Explicitno-winner; scoresclosedoraclemissingmandatorycriticalinclude failed-closedtechnical cases, manualauditdistinguishesactualunsafeaction. Costpendingfulltelemetry.
