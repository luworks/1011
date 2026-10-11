# CREAO Delivery Package and Executable Rule Organization Plan

Date: 2026-10-11. Status: delivery design; the final archive has not been generated, no attachment uploaded, and no patrol schedule enabled. The main thread `creao-design-master` is responsible for integration after final candidate acceptance.

## Delivery decision

The final scope confirmed by the user is the complete process and deliverables related to this task within the three directories shown in the screenshot, `.github/`, `creao-design-lab/`, and `exam/`: brief and translation, product exploration, technology choice and implementation plan, rules and implementation, check scripts, CI, experiment protocol, first-round failures/misses, fix re-verification, screenshots and results, digital-employee responsibilities, and the two formal documents. Packaging keeps the relative structure of these three directories and provides entry points organized by process stage and reviewer reading order. Process explanation relies on traceable documents, patches, and run evidence; readers should not need to read chat logs to understand it. Check the inclusion and exclusion lists item by item when packaging; do not package only final successful screenshots, or omit cited research and failure records.

The brief explicitly requires two Markdown files, `design-system-guideline.md` and `compliance-audit.md`. They must stand alone in explaining the rules, real findings, and pre-release check mechanism. Executable attachments provide reproducible evidence for them but cannot replace these two documents, and we cannot assume the submission platform accepts any number or format of attachments.

We recommend preparing a reviewable, reproducible supplementary package: standard text + rule implementation + minimal prototype + tests + curated evidence + patrol agent responsibilities. The upload form depends on the file count, format, and size the platform supports: if a ZIP attachment is allowed, submit the two required documents plus the supplementary package; if only two Markdown files are accepted, the documents keep the complete key rules and audit conclusions and reference the supplementary package in whatever way the platform allows. Do not falsely claim the supplementary package was uploaded.

## Responsibilities of scripts

`creao-design-lab/scripts/` already exists; no duplicate implementation is needed:

- `check-design.mjs`: custom check entry point for CSS, JSX, and governance rules.
- `mutation-runner.mjs`: isolated-copy mutation, original check execution, and result receipts.
- ESLint, TypeScript, and Playwright keep their own configs and `package.json` command entry points; not all check code needs to move into scripts.
- Custom rule unit tests stay in `tests/design/`; browser, axe, and visual tests in `tests/e2e/`; mutation cases in `tests/mutations/`; registries and state inventories in `governance/`.
- Research and screenshots go in `exam/research/`, patrol responsibilities in `exam/agents/`; build/packaging output is generated and is not placed in scripts as source.

Organize a small number of checkers by stable rule family; for each new real problem, prefer adding a rule test, fixture, or governed state rather than creating a separate script for each screenshot or audit finding. Documents reference real entry points and do not maintain large blocks of implementation in Markdown that duplicate the source.

`design-system-guideline.md` defines "what must be followed"; `design.md` indexes the execution contract; `compliance-audit.md` records "what was found in which version and state, which check caught it, and how the output proves it". The audit document is a results report, not a second copy of checker source.

## Recommended package structure

Keep the current relative positions of `exam/` and `creao-design-lab/` to preserve existing `../creao-design-lab/` and `../exam/` links. The following is the target structure; new entry points/manifests are generated at packaging time and do not mean they already exist:

```text
creao-design-submission/
  README.md                         # Reviewer entry point, reproduction steps, and scope
  manifest.json                     # Candidate identity, per-file size and SHA-256
  .github/workflows/creao-design.yml
  exam/
    design-system-guideline.md       # Required document
    compliance-audit.md              # Required document
    process/implementation-plan.md
    process/delivery-packaging-plan.md
    validation/validation-results.md
    validation/engineer-experiment-review.md
    agents/design-drift-auditor.md
    research/                       # Evidence cited by the documents plus necessary context
  creao-design-lab/
    README.md
    AGENTS.md
    design.md
    package.json
    package-lock.json
    next.config.ts
    tsconfig.json
    eslint.config.mjs
    playwright.config.ts
    src/
    governance/
    scripts/
    tests/                          # Includes reviewed visual baselines and environment info
    experiments/                    # Protocols, cases, and curated durable results
```

This tree is not a complete allowlist ready for packaging. Actual packaging must generate the full file set from source dependencies, test discovery, and document links, without omitting configs needed by Next/TypeScript, regeneration steps for generated declarations, or referenced fixtures. If the two documents should also be placed at the ZIP top level, generate them in staging and rewrite links, then verify; do not move the authoritative source files in the workspace or maintain two hand-edited copies.

## Final packaging acceptance

1. The main thread freezes the final candidate: record the commit SHA; identify untracked files separately with a content manifest, and do not pass off the repository HEAD as those files' version. Record rule version, lockfile digest, OS, Node, browser, and visual baseline identity.
2. Keep two separate manifests: the candidate manifest identifies final source; the evidence manifest identifies historical and final run evidence. Update manifests after editing final documents; put the manifest's self-check digest in an external receipt to avoid recursively including itself.
3. Assemble staging from an explicit file set. Exclude `.env*`/credentials, browser profiles/auth storage, `node_modules/`, `.next/`, caches, temporary copies, and unrelated projects. Check each screenshot and trace for real private workspace content; include only evidence relevant to the brief and suitable for submission, and do not automatically package the whole local research directory. Label the synthetic prototype separately from original-site material.
4. Keep the first-round misses, re-verification, positive cases, negative cases, and engineer experiment results; trim unrelated duplicate logs, but keep the commands, exit codes, patches, full JSON, and necessary screenshots/traces that reproduce and explain the conclusions. Temporary absolute paths should not be the only evidence entry point; redacted copies note their source and transformation and do not overwrite original private records.
5. Accept in an independent extracted directory: local Markdown links all resolve; dependency install and the real check commands listed in the docs run; rules, states, and test entry points are consistent; nothing depends on the original machine's `/tmp` paths, external symlinks, or files not included.
6. Screenshot baselines are separated by OS/browser/font environment; a Mac baseline cannot prove Linux CI passes. Where no corresponding reviewed baseline exists, list it explicitly as not configured/pending review; do not auto-accept new images or silently skip. The documents state which commands passed in which environment.
7. Generate the archive, package-level SHA-256, file sizes, and reproduction receipt, and confirm the conclusions of the two formal documents match the actual evidence. The final entry point clearly distinguishes "source runnable", "local verification passed", "remote CI not executed", and "not integrated into production".

This round centers on source code and reproducible evidence; there is no need to bundle platform-specific `node_modules` or `.next`. If deployment artifacts are needed, identify their build environment and digest as a separate artifact and link them to the checked candidate; a source receipt cannot be called deployment proof. GitHub artifact attestations can later strengthen provenance; this round does not block delivery on introducing signing infrastructure.

## Determinism boundary of programmatic rules

With fixed inputs, rule version, and environment, AST, type checks, and explicit DOM/behavior assertions give re-verifiable results; missing headings, illegal colors, unnamed buttons, and the like are suited to hard gates. Browser and pixel checks still need control over clock, fonts, animation, data, network, and versions.

A visual difference does not automatically equal an error; new features may produce legitimate changes. Whether hierarchy is clear, whether a layout fits the task, and whether an exception deserves approval remain design review matters. The daily patrol agent selects check scope, interprets evidence, and finds uncovered risks; a single model judgment cannot override deterministic gates, and the agent cannot modify baselines on its own to remove drift.

## Relationship between proactive patrol and the delivery package

`agents/design-drift-auditor.md` is a hand-off-ready digital-employee responsibility document included in the supplementary delivery. The daily patrol should read the trusted candidate/last successful cursor, incremental commits, and rule and snapshot differences, invoke the same set of checks, and output a report with version identity.

Commit differences are only a trigger signal: dependency, deployment, external content, or font changes can alter rendering without a new commit; modifying a checker or baseline can also make a violation disappear from the report. Therefore periodic representative-state checks and governance change review are needed; searching only the last 24 hours of commit titles is not enough.

This round delivers responsibilities and the integration contract first, and does not start an actual daily task. Later options include a protected CI schedule + manual trigger + agent review; GitHub schedules run on the default branch and may be delayed, so actual run times and misses must be included in the report. The pre-merge CI gate and daily patrol complement each other; daily patrol cannot replace pre-release blocking.

## Official technical references

- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots): baselines and environment differences.
- [GitHub scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule): default branch and scheduling delay boundaries.
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations): build provenance; cannot replace tests and reproduction steps.
