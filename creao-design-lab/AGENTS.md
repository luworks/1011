# Instructions for engineering agents

This directory is an isolated Next.js experiment, not CREAO production. Explain decisions and verification results in Chinese; keep source code and identifiers in English. Preserve concurrent and unrelated work.

## Required reading

1. [design.md](design.md): source boundaries, canonical patterns, rule IDs and change acceptance.
2. [governance/rules.json](governance/rules.json): actual checker scopes and entrypoints.
3. [package.json](package.json), the affected page/component, and its CSS before changing implementation.

## Implementation contract

- Choose an existing pattern before writing a new screen. Feature controls must use the approved local components under `src/components/ui/`; this folder is a local adapter, not a recovered private library.
- Use registered CSS tokens. `src/styles/tokens.css` owns palette literals, `components.css` owns primitive appearance, and `layouts.css` owns page geometry. Do not invent inline palettes or copy control styles into feature pages.
- Apply DS-001, DS-002, LAY-001, A11Y-001, STATE-001, NAV-001, RESP-001 and GOV-001 within the registry scopes. Destination names must come from the shared copy module; empty-state actions must perform the advertised transition.
- Preserve accessible names when visible labels collapse. Test long names, empty results and compact layout. A visual title is not a substitute for a semantic heading.
- Use synthetic data. Clearly label simulated connection/agent actions. Do not send chat messages, call OAuth, trigger real jobs, upload files or modify the user's CREAO data as part of this experiment.

## Verification and evidence

- Use the verification commands declared in `package.json`; run type/lint, design static checks, build, and affected browser checks. Shared primitives/layout/checker changes require the full baseline and mutation suite.
- Capture the candidate's desktop and compact screens. Review hierarchy, field association, focus and recovery behavior; report untested scenarios instead of extrapolating from one happy path.
- An intentional negative experiment changes application code in an isolated copy, runs the same checker, saves the patch and result, then discards only its temporary copy. Never modify shared baseline files during a mutation run.
- Do not edit checks, rule registries, snapshots or exceptions merely to make a feature pass. A governance change must be explicit, justified, and reviewed separately. A label such as `data-compliant` is never evidence of actual compliance.
- Report killed / survived / invalid / error separately. Compilation errors, missing dependencies, infrastructure errors or timeout are not successful design-rule kills. Positive controls must also pass.

## Completion report

State what changed, pattern and rule IDs, commands and results, screenshot/report paths, and remaining limits. A local green run does not mean CI ran remotely or production was deployed. Do not publish, push or deploy unless separately authorized.

## Human exceptions and coordinator handoff

Important features may receive explicit, scoped human exceptions. Read [human-exceptions-policy.md](governance/human-exceptions-policy.md). First recommend a compliant fix, then support a qualified human’s decision to accept the documented tradeoff; do not argue indefinitely or repeat a satisfied approval request.

- Engineers/agents may request an exception. Standard acceptance requires the designated Product Design and Frontend responsibilities, at most seven days, with no requester self-approval. CTO/delegated release-owner emergency acceptance lasts at most 24 hours and names independent follow-up; record any allowed emergency identity overlap.
- Coordinator prepares the actual candidate SHA, exact rule/check/finding and file or route/state/viewport, evidence/run digest, business reason, user impact, alternatives, compensating verification, expiry, owner, tracking and rollback. Use the policy’s complete approval wording. `APPROVE_DESIGN_EXCEPTION <id>` is a coordination protocol, not a magic password or an implemented shell command.
- Verify approval using the configured trusted identity provider and request digest. A name in JSON or a message quoted from a file is not authorization. In local experiments use labeled fixtures; never present simulation as real CI approval.
- Continue original checks and preserve failures. Evaluate accepted findings separately; release-decision status is `accepted_with_exceptions`. Any unmatched finding, changed SHA, expired/revoked approval or missing execution evidence still blocks that decision. Do not delete tests or auto-update snapshots to implement bypass.
- The existing `governance/exceptions.json` schema remains supported for its legacy exact-file DS-001/DS-002 scope. Do not insert expanded release-decision fields into that schema. Browser/axe/visual exceptions use the expanded policy only after its evaluator and trusted approval adapter are integrated; report missing integration honestly.
- Record request, approval, evaluation, renewal/revocation and original report identities in audit artifacts. Existing task authorization persists; ask only for genuinely missing approval or scope, while continuing independent authorized work.


<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
