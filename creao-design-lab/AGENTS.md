# Instructions for engineering agents

This directory is an isolated Next.js experiment, not CREAO production. Explain decisions and verification results in Chinese; keep source code and identifiers in English. Preserve concurrent and unrelated work.

## Required reading

1. [design.md](design.md): source boundaries, canonical patterns, rule IDs and change acceptance.
2. [governance/rules.json](governance/rules.json): actual checker scopes and entrypoints.
3. [governance/page-states.json](governance/page-states.json): implemented and planned route/state/viewport coverage; inventory entries do not prove execution.
4. [package.json](package.json), the affected page/component, and its CSS before changing implementation.

## Implementation contract

- Choose an existing pattern before writing a new screen. Feature controls must use the approved local components under `src/components/ui/`; this folder is a local adapter, not a recovered private library.
- Use registered CSS tokens. `src/styles/tokens.css` owns palette literals, `components.css` owns primitive appearance, and `layouts.css` owns page geometry. Do not invent inline palettes or copy control styles into feature pages.
- Apply DS-001, DS-002, LAY-001, A11Y-001, STATE-001, NAV-001, RESP-001, GOV-001, A11Y-002 and VISUAL-001 within the registry scopes. Destination names must come from the shared copy module; empty-state actions must perform the advertised transition.
- Preserve accessible names when visible labels collapse. Test long names, empty results and compact layout. A visual title is not a substitute for a semantic heading.
- Use synthetic data. Clearly label simulated connection/agent actions. Do not send chat messages, call OAuth, trigger real jobs, upload files or modify the user's CREAO data as part of this experiment.

## Verification and evidence

- Use the verification commands declared in `package.json`; run type/lint, design static checks, build, and affected browser checks. Shared primitives/layout/checker changes require the full baseline and mutation suite.
- Update the page-state inventory whenever adding routes/states or changing a test's coverage. Keep planned/notVerified separate from passed and attach exact title, viewport and immutable evidence before claiming execution.
- Run the 16-state-scan axe gate (A11Y-002); any violation fails. Preserve full incomplete results for human review. Do not add exclusions or disable rules to force green.
- Run the separate three-image VISUAL-001 comparison in a verified OS/architecture/release/browser namespace. Missing Linux baselines fail closed; never skip, reuse Mac images, or use update flags in CI. New or legitimately changed images require a separately authorized baseline review and then a normal comparison rerun.
- Capture the candidate's desktop and compact screens. Review hierarchy, field association, focus and recovery behavior; report untested scenarios instead of extrapolating from one happy path.
- An intentional negative experiment changes application code in an isolated copy, runs the same checker, saves the patch and result, then discards only its temporary copy. Never modify shared baseline files during a mutation run.
- Do not edit checks, rule registries, snapshots or exceptions merely to make a feature pass. A governance change must be explicit, justified, and reviewed separately. A label such as `data-compliant` is never evidence of actual compliance.
- Report killed / survived / invalid / error separately. Compilation errors, missing dependencies, infrastructure errors or timeout are not successful design-rule kills. Positive controls must also pass.

## Completion report

State what changed, pattern and rule IDs, commands and results, screenshot/report paths, and remaining limits. A local green run does not mean CI ran remotely or production was deployed. Do not publish, push or deploy unless separately authorized.

If a real exception is necessary, use `governance/exceptions.json` and its schema. Do not silently weaken the rule. Existing task authorization persists; ask only for a genuinely missing decision or irreversible action, while continuing independent authorized work.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
