# Visual baseline review: English localization

- Reason: deliberate copy change. The lab UI was converted from zh-CN to English using the canonical label map (Files, Connectors, Agents, Design guidelines, Connectable, Browse connectable services, Clear search, New folder).
- Before: the first visual run against the old baselines failed on the three screens, as expected for a text change (`visual-run1-pre-update.log`, diffs in `run1-diffs/`, old images in `before/`).
- Update: baselines regenerated in the same reviewed environment (darwin-arm64-25.6.0, Chrome 154.0.8037.98) (`visual-update.log`); re-run without update: 3/3 passed (`visual.log`, `visual.json`).
- Full gate on the same tree: typecheck 0, lint 0, test:design 13/13, check:design passed with 0 violations, build 0, test:e2e 54/54 (`e2e.json`).
- Reviewer: Claude agent acting for Product Design; human sign-off is still pending, as VISUAL-001 requires.
