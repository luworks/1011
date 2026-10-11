# Evaluation branch handoff

The user confirmed that this branch and `main working task` collaborate in the same workspace. Formal model selection belongs to the main task and now covers GPT-6 Luna, GPT-6.1 Sol, Claude Opus/Sonnet/Haiku 5.5 and their supported thinking settings. Priority: accuracy, then full-turn latency, then price. The main task has the user-approved cumulative US$25 budget. This branch will not start additional paid experiments.

## Delivered reusable evaluation work

- `tests/test_adversarial.py`: 25 deterministic tests including 100 generated amount/duration combinations, calendar translation, goodwill redistribution, authority spoofing, malicious candidates and source-version changes. These are gate tests, not live model attack-success evidence.
- `docs/evaluation_strategy.md`: independent oracle, structural versus live tests, multi-policy reviewed packs, fail-closed source revisions, attack families, release criteria and general failure-class repair.
- `evaluation.py`: per-turn oracle and allowed-intent checks, cross-turn action invariants, corrected amount=None over-refusal denominator, separated technical/API failure counts. `fixtures/scenarios.json` has independent per-turn assertions for all 40 cases. Expected answers never enter model requests.
- `cli.py`: case-file selection, validated subsets, parent denominators, frozen default repeats=3, start-time code/config/corpus hashes.
- Workflow trust fixes: reported outage dates/monthly fees cannot complete NOC evidence; a reported general amount or statement date cannot authorize simulation. Conflicts preserve mandatory human review.
- `docs/original_replay_audit.md`: six-turn live original-scenario audit passed core acceptance; extraction and candidate defects remain explicitly recorded.

## Validation and provenance

At this branch checkpoint, 113 tests passed in both the workspace and a freshly extracted project, with locked dependencies and no API keys in the extracted directory. The extracted project is `/tmp/policy-agent-clean.hB5YQE/project`. Concurrent additions after this checkpoint need the main task's final verification.

The historical frozen run code SHA is `dd16cd58fcebb6d56aa7ebc1b10e1ff3441de804bfaab82c79a5a069733a78de`; all four starts used the same hash. `examples/frozen_baseline.zip` preserves that exact runnable snapshot and its original fixture/config. It is historical evidence, not the current official candidate set. The earlier `dist/policy-grounded-agent-prototype.zip` is a preliminary package validation artifact, not final delivery.

## Existing runs and follow-up

`runs/dev-*`, `runs/frozen-gpt`, and `runs/frozen-mini` use the superseded GPT-5.4/initial Claude matrix. GPT-5.4 results must not participate in the new formal selection. The main task has identified and is stopping the old `runs/frozen-haiku` and `runs/frozen-sonnet` processes as candidate-adjustment interruptions; retain their partial traces and do not label them complete.

The 16-case frozen suite has now been exposed in historical evaluations. If failures are used to tune prompts or rules, promote this suite to regression and create a new independently reviewed holdout for acceptance. Comparing new model configurations without tuning on these failures must still disclose the suite's prior exposure.

`scripts/summarize_runs.py` is specifically a historical four-model summarizer, not the new 32-configuration selector; it intentionally refuses unfinished historical runs. Do not relabel its output as the new selection. `selection.py` and the expanded matrices belong to the main task's work.

Final README commands, design memo, curated run artifacts and submission packaging should be finalized by the main task against the new matrix. Preserve failures, version changes and incomplete work rather than publishing a winner prematurely.
