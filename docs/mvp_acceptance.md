# MVP acceptance and ownership

The backend MVP and model-selection experiment are separate deliverables. The MVP is runnable before a winning model is selected. No result from a partial or historical cohort establishes the final recommendation.

## Verified on 2026-10-11

- `uv run pytest -q`: 141 tests passed before report-specific additions.
- A clean extraction of the nested submission archive installed successfully with `uv sync --frozen` and passed the same 141 tests.
- `doctor` succeeded without API keys and explicitly reported that API access was not checked.
- Six-turn offline replay completed and exposed governing rules and evidence per turn. It calculated $82.50 under the outage exception, preserved the tax evidence gap, and applied the 30-day request window. This verifies fixture-driven integration, not model accuracy.
- Live replay artifacts are separately labeled with their original model, prompt and source versions. They must not be presented as fresh validation of a changed version.
- Packaging excludes environment files, virtual environments and arbitrary run directories. It checks credential values before writing the archive.

## Ownership during model selection

The `eval` task owns paid API experiments, the shared `runs/budget.json` ledger, evaluation fixtures/scoring and final selection. The approved cap is US$25 cumulative, including previous experiments. The MVP task owns core workflow, CLI, documentation, report presentation and packaging. Core changes that affect an active experiment require a new clearly identified cohort; they must not silently alter a running comparison.

The HTML report consumes measured results and must show pending or incomplete coverage honestly. Selection prioritizes accuracy, then full-turn response speed, then price. Final experiment progress is recorded by the eval task in `docs/eval_handoff_status.md`.

## Intentional prototype boundaries

Account information is supplied through labeled local records and chronological transcript confirmations. No real credit is issued and no external human handoff is performed. Policy changes require reviewed executable rule updates and an updated corpus lock. The current bounded templates do not implement arbitrary policy documents. Intent and fact extraction remain model-dependent and require empirical evaluation.
