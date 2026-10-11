# Independent Engineer Experiment A/B: Implementation Difference Review

Review time: 2026-10-11 14:08 PDT. Review method: read-only source inspection, per-file SHA-256 comparison, and diff inspection. This document does not replace the main agent's browser acceptance, and no experiment copy's source was modified.

## 1. Experiment Question and Evidence Scope

Two independent engineers received the same request: add an "Important" marker to files and an "Important only" filter, while preserving search, empty-state recovery, narrow-screen readability, and accessible names for controls. A was explicitly told to follow the guideline; B was asked to deliberately take reasonable, visible implementation shortcuts. Neither could modify checkers, rules, dependencies, or tests, nor create negatives through compile errors. Full conditions are in the [experiment protocol](../creao-design-lab/experiments/engineer-protocol.md).

This is a **mechanism validation with two controlled implementations**. It cannot be used to infer the violation probability of real engineers, nor does it prove that simply providing Markdown naturally yields compliant results. A/B is counted separately from the fixed mutation set.

## 2. Baseline Integrity

Frozen manifest: [baseline-manifest.json](research/validation/engineers/baseline-manifest.json), containing 38 files. Manifest SHA-256:

`1294c012784e2e1ef02640bf81d20fe92e86bec9b2840dddbb7f4469f776b440`

| Check | A | B |
| --- | --- | --- |
| Files changed relative to the frozen manifest | 3 | 3 |
| Changed files | `src/app/files/page.tsx`, `src/lib/copy.ts`, `src/styles/layouts.css` | Same three files |
| Remaining files in the manifest | All 35 keep original hashes | All 35 keep original hashes |
| Protected check/governance/config assets | All 17 checked are unchanged | All 17 checked are unchanged |
| Missing manifest files | 0 | 0 |
| Extra files in `src/`, `scripts/`, `tests/`, `governance/` | 0 | 0 |
| Canonical drift relative to the frozen manifest | 0 | 0 |

The 17 protected assets include `AGENTS.md`, `design.md`, rules and exceptions, check scripts, tests, package/lock, and lint/Playwright/Next/TS configs. Tokens and approved UI components are also in the 38-file manifest and are unchanged. Generated `.next`, compilation caches, and run logs are not part of the implementation change denominator.

Verifiable evidence:

- [Machine-readable integrity result](research/validation/engineers/source-integrity-review.json): before/after hashes for each changed file, patch hashes, and verification time.
- [A's full patch](research/validation/engineers/engineer-a.patch).
- [B's full patch](research/validation/engineers/engineer-b.patch).

This supports the conclusion that "both candidate implementations run against the same gate assets"; it does not mean remote CI has run, nor does it prove the checker cannot be modified by future commits.

## 3. Feature Implementation Review

| Behavior | A source | B source | Still needs browser confirmation |
| --- | --- | --- | --- |
| Per-item Important marker | `Set<string>`, functional update copying a new Set | `string[]`, functional add/remove of IDs | After repeated mark/unmark, `aria-pressed` stays in sync with actual filtering |
| Search combined with Important filter | Name condition AND Important ID condition | Same logic | Matching items shown correctly after combining |
| Shared state across list/grid | Same list and marker state | Same | Switching views does not lose markers/filter |
| Recovery from empty filter result | Clears search and Important filter; keeps marked IDs | Same | After clicking, real data is restored and markers are kept |
| Unmarking while in "Important only" | When the row is about to disappear, focus returns to the filter button; also a live status | No active focus transfer, no new live status | A's actual focus destination; whether B loses focus |
| State persistence | React in-page state | Same | Reset on refresh is within the scope of this synthetic demo; persistence must not be claimed |

Both base filtering algorithms express the request; B's problem cannot be summarized as "the feature was not written". The existing create flow adds new folders to the same collection, so both also allow marking newly created folders as Important. No data overreach or live calls were found; the interaction paths still need to be verified in an actual browser.

A's handling of focus when unmarking causes a row to disappear is extra care for dynamic state. B's lack of focus transfer is a manual-review concern visible in the source; it cannot automatically be counted as detected by the A11Y-001 gate: the existing gate mainly checks accessible names and does not cover the full focus lifecycle.

## 4. Guideline Adherence Differences and Expected Gates

### A: Reuses the composition patterns allowed by current rules

- All new controls use the approved `Button` and `Icon`. No native button was added to the feature page, consistent with the scope of DS-002.
- New CSS only adjusts flex layout and uses `var(--space-2)`; no new color literals were added, consistent with the scope of DS-001.
- The file button visibly reads "Important", and its accessible name includes the full file name; `aria-pressed` represents the selected state. The filter button also has a clear name and selected state.
- New copy goes into `copy.ts`; `PageHeader` and `EmptyState` continue to be reused.
- The toolbar may wrap, the file-name area is flexible, and the Important button does not shrink; this is a reasonable responsive intent, but whether it truly avoids clipping must be checked in 320/390/800/1280px runs.

Source review found no obvious bypass of existing governance boundaries by A. This conclusion does not mean the new feature has passed browser acceptance, nor that pixel-level visual consistency has been proven.

### B: Attributable implementation shortcuts

| Shortcut and location | Rule | How the same mechanism identifies it | Caveat |
| --- | --- | --- | --- |
| `layouts.css` adds five color literals: `#d2a22b`, `#fff7d6`, `#5b4400`, `#facc15`, `#9c7200` | DS-001 | CSS value AST identifies colors outside registered tokens in governed style files | It cannot be claimed from this that these five colors violate an unknown official palette; what is violated is the explicit local token-usage rule |
| `files/page.tsx` adds two native `<button>` definitions, for the filter and the star | DS-002 | JSX AST identifies direct native controls in feature pages | These are two source definitions, not violations accumulated per rendered item |
| The star button has only a star child with `aria-hidden="true"`, and no label/title/other accessible name | A11Y-001 | The browser computes the real accessible name and should find an unnamed button | This row is a deterministic source-based expectation; the actual failure count/exit code is confirmed by the main agent's receipts |
| Self-made yellow pill style and star visuals | Manual visual review | Compare against approved components and existing page hierarchy | AST cannot verify visual semantics; a color-gate hit is not a full visual audit |

B did not delete headings, recovery actions, tests, or check code; so this result cannot be interpreted as "B fails every guideline". Its native buttons still have native browser keyboard operability; the defects are the component boundary and the missing accessible name, not a blanket "completely unusable by keyboard".

## 5. Usage Boundaries of the Experiment Conclusions

If A passes the original gates and the new behavior passes browser acceptance, while B builds but is blocked by the design rules above, this proves that two implementations of the same real feature can produce explainable, different results through a shared guideline and gates, rather than by flagging `isViolation` or manufacturing compile errors.

The following still need to be reported separately: base compile success, original design gate results, real behavior of the new feature, and manual visual review. Existing tests have no predefined business contract for the "Important" feature; passing the full old test suite cannot substitute for actual verification of the new marking and filtering. Width, focus, refresh behavior, and long file names also cannot be inferred as passing from source intent alone.

This review does not use the engineers' self-reported test results as the final basis for acceptance. The main agent will append independent execution receipts below; this source snapshot and the first results are kept, and later fixes do not overwrite the original experiment.

## 6. Independent Verification Receipts

Final verification: the main agent ran the original browser checks against two independent production builds, then actually exercised the new feature. The archivist read the JSON and logs to verify the results, without changing experiment source or checkers.

| Check | A | B | Evidence |
| --- | --- | --- | --- |
| Types / ESLint | Both exit 0 | Both exit 0 | Main agent's independent re-run receipts: [A commands](research/validation/engineers/engineer-a/evaluator-commands.json), [B commands](research/validation/engineers/engineer-b/evaluator-commands.json) |
| Production build | Exit 0, build succeeded | Exit 0, build succeeded | [A evaluator build](research/validation/engineers/engineer-a/evaluator-build.log), [B evaluator build](research/validation/engineers/engineer-b/evaluator-build.log) |
| Static design check | Exit 0, `passed: true`, 0 violations | Exit 1, `passed: false`, 5 DS-001 raw colors + 2 DS-002 native controls | [A evaluator static](research/validation/engineers/engineer-a/evaluator-check-design.log), [B evaluator static](research/validation/engineers/engineer-b/evaluator-check-design.log) |
| Original production browser checks | 22/22 passed, exit 0 | 20/22 passed, 2 failed, exit 1 | [A JSON](research/validation/engineers/engineer-a/evaluator-e2e.json), [B JSON](research/validation/engineers/engineer-b/evaluator-e2e.json); exit codes in the main agent's [interaction and result receipt](research/validation/engineers/manual-feature-acceptance.json) |
| Real interaction with the new feature | Passed | Pointer operations and state changes passed | The same receipt records marking, filtering, combined search, empty-result recovery, and unmarking |
| Focus after dynamic removal | Returns to the "Important only" filter button | Lands on `BODY` | B's is a new manual finding, not counted as a detection by the old automated tests |

Both of B's browser failures are A11Y-001: the star control on `/files` lacks an accessible name at 1280px and 390px. Of the 22 results, skipped/flaky are both 0; it must not be described as the entire suite failing. B's feature runs and its production build succeeds, showing that the block comes from design rules, not a failure faked by a syntax error.

The [A filter screenshot](research/validation/engineers/a-important-filter.png), [A narrow-screen screenshot](research/validation/engineers/a-mobile.png), and [B filter screenshot](research/validation/engineers/b-important-filter.png) keep the manually operated states; B's failure screenshots, trace, and error context are stored in `research/validation/engineers/engineer-b/test-results/`. The frozen manifest also has a [persistent archive](research/validation/engineers/baseline-manifest.json), to avoid relying solely on the ignored experiment run directory.

Final verdict: **A is acceptable; B is blocked by the existing static and browser design gates.** B additionally has a focus-restoration defect not covered by current automation, showing that manual acceptance of new features is still needed. This experiment contains only one synthetic feature and two agents implementing in assigned directions; it is separate from the fixed mutation results and cannot be used to infer an overall compliance rate for real engineers.


## 7. Enhanced Gate Re-check (v2, same two agents)

This round reused the A/B agents to re-implement the same "Important marking and filtering" request on the enhanced baseline; it is a re-check of the original experiment and cannot count as two additional independent engineers. The original v1 results, patches, and failure evidence remain unchanged.

A's [enhanced browser result](research/validation/engineers-v2/a/final/evaluator-e2e.json) is 38/38 passed. The first [visual comparison](research/validation/engineers-v2/a/final/evaluator-visual-first.json) had two Files changes caused by the controls added by the new feature; after the main agent independently viewed the actual desktop and narrow-screen screenshots, it approved the corresponding candidate baseline changes, see the [review receipt](research/validation/engineers-v2/a/final/visual-review.json). The original diff is kept in `research/validation/engineers-v2/a/visual-first/`; only A's copy baseline was updated, canonical was not automatically overwritten; the subsequent [visual re-check](research/validation/engineers-v2/a/final/evaluator-visual-reviewed.json) without the update flag passed 3/3.

B's [first visual result](research/validation/engineers-v2/b/final/evaluator-visual-first.json) is 1/3 passed with 2 Files failures, and its changes were not approved. The main agent actually exercised four steps in both candidates: mark → filter to one item → search with no results → clear to recover; this proves the basic feature runs, but does not substitute for accessibility and visual acceptance. B's [full enhanced report](research/validation/engineers-v2/b/final/evaluator-e2e.json) ends at **32/38 passed, 6 failed**, 0 skipped/flaky, with failure screenshots and traces archived in `research/validation/engineers-v2/b/final/e2e-artifacts/`; B remains blocked by the gates.
