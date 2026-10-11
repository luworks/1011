# Offline model evaluation report

`dist/index.html` is a self-contained snapshot: open it offline or serve `dist` over loopback HTTP. It does not query model APIs. Pending measurements are shown as missing, not zero. Historical development results never establish a final recommendation.

Update from explicit benchmark directories and the reviewed selection artifact:

```sh
python3 scripts/build_model_report.py \
  --run frontier-screen=runs/frontier-screen \
  --run frozen=runs/frontier-frozen \
  --selection runs/frontier-frozen/selection.json \
  --complete --build
```

Run the command from the repository root. Omit `--selection` while evaluation is pending. A running benchmark's `index.json` is supported, preserving all planned configurations. `--complete` indicates the report authoring is complete, independently of whether the evidence supports a recommendation.

The build uses the installed Data Analytics plugin runtime; pass `--plugin PATH` and `--node PATH` on another workstation. Reading the delivered HTML requires neither Node nor that plugin. Snapshot fields retain source hashes, measurement denominators and missing values; the importer never invokes paid APIs. Keep `report/src/data.json` and stable report identity when updating. Authored content is under `src/content/report/`; do not modify protected runtime files.

Selection is supplied separately, not recomputed by the presentation. It must have `selected` or `tentative` status and a matching nonhistorical result before displaying a winner. The selection module checks full comparable cohorts and orders quality, whole-turn P95, P50, then cost. A report with pending evidence remains usable and explicitly declines a final recommendation.
