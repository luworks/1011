# Next reviewed report input contract

The delivered snapshot and `dist/index.html` remain frozen until the coordinator authorizes the next build. Import summaries only; never load fresh acceptance fixtures or expected answers.

## Groups

1. `historical-v8`: immutable prior repair/regression results, explicitly diagnostic/historical.
2. `v10-repair-regression`: completed generic repair regression; preserve its own case and code hashes.
3. `v10-fresh-v3`: fresh acceptance, with planned/completed/unique/repeats and its frozen oracle hash. Partial means no final winner.
4. `v10-policy-original`, `v10-policy-clarified`, `v10-policy-scenario`: same pinned Haiku adaptive/medium configuration, identical paired cases and repetition count. Distinct document variants are not distinct models. Preserve each corpus/version hash and any incomplete denominator.

Use the existing `--run STAGE=DIR_OR_SUMMARY_JSON` for model and policy-variant summaries. Each model row accepts `configuration`, `source_run_manifest`, `summary`, `usage`, and `repeats`; prior raw benchmark summaries are also supported. `--run-manifest STAGE=PATH` supplies exact frozen metadata when a compact checkpoint lacks it. Never overwrite a source summary with presentation data.

## Development baseline

`--development-default config/development-default.json` reads the explicitly user-selected baseline. The report must say development default only, not benchmark winner. Final winner still requires a separately supplied valid selection artifact.

## Repair-specific measurements

`--repair-metrics PATH` accepts an owner-reviewed JSON object:

```json
{
  "rows": [
    {
      "label": "workflow-v10 repair regression",
      "workflow": "workflow-v10",
      "config_id": "anthropic/claude-haiku-5-5/adaptive/medium",
      "case_set_sha256": "the actual frozen hash",
      "completed": 28,
      "planned": 28,
      "technical_failures": 0,
      "scope_failures": null,
      "scope_assessed": null,
      "citation_conflict_failures": null,
      "citation_conflict_assessed": null,
      "scope_calls": null,
      "scope_latency_seconds": null,
      "scope_cost_usd": null,
      "total_calls": null,
      "turn_p50_seconds": null,
      "turn_p95_seconds": null,
      "reported_cost_usd": null
    }
  ],
  "source": {
    "label": "Reviewed repair measurement summary",
    "files": ["relative/artifact/path.json"],
    "evidenceFlow": [{"title": "Frozen source", "detail": "Exact source hash and extraction method"}],
    "caveats": ["Explicitly state unresolved semantic failures and measurement limitations."]
  }
}
```

The row above documents field types only; it is not data to insert into a real report. `scope_failures` and `citation_conflict_failures` need independently reviewed denominators and definitions; absent fields stay missing. Cite workflow/corpus/oracle/code hashes in source metadata. Add before/after rows only from actual comparable experiments. Do not infer causal improvement from different suites, different workflow/model configurations, or a single live replay.

Scope-specific latency/cost require per-stage telemetry or an explicit, reviewed call mapping. Current historical provider records lacking a schema/stage marker cannot support that attribution from call order alone. In that case present total workflow calls, cost and whole-turn latency, and leave scope-specific fields null. Retries, scope repairs, and shared content-repair budget consumption must remain included in totals.

For three policy variants, use the fixed-model grouped results as supplied by the policy owner. Do not silently reuse the older two-way v5 A/B narrative for the newer experiment. Final narrative and promotion recommendation must come from the reviewed policy handoff.
