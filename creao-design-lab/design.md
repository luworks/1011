# CREAO product design contract

Version: 0.1 · 2026-10-11 · Owner: Product Design + Frontend Engineering.

This is the implementation contract for the **local CREAO Design Lab**. It is an evidence-informed proposal for CREAO's product layer, not CREAO's private design-system source. Read this file before changing a screen; use [AGENTS.md](AGENTS.md) for the delivery workflow. The submission-level rationale is in [design-system-guideline.md](../exam/design-system-guideline.md).

## 1. Source boundaries

| Class | Evidence | What it establishes |
| --- | --- | --- |
| Official | [Widgets documentation](https://docs.creao.ai/features/widgets), [saved Markdown](../exam/research/public-design-search/widgets.official.md) | Dashboard component categories and composition: a Stack/Grid root, Cards for groups, data/chart/table widgets inside. Warm surfaces, near-black ink and restrained semantic color. |
| Observed | [Widgets screenshot](../exam/research/deep/10-widgets-layout.png), [DOM/CSS snapshot](../exam/research/deep/widgets-dom.json) | Actual rendered controls, variable values and parameter labels at one point in time. These do not establish private import paths or supported component APIs. |
| Observed | [Files mobile](../exam/research/deep/14-files-mobile.png), [Files DOM](../exam/research/files-dom.json), [connectors empty state](../exam/research/screenshots/05-connectors-empty.png) | Screen behavior and specific design defects used to define testable rules. |
| Proposed | This document, local CSS, local components and checks | Product-level patterns, responsive decisions, acceptance thresholds and enforcement for this experiment. |

Public sitemap research found official Widgets documentation, but no indexed full-product `design.md`. The product sitemap returned 403. This is **not evidence that an internal design system does not exist**. The task states that it does. Replace the local adapter's imports with real approved library imports when integrating in that repository; preserve the contracts below.

## 2. Executable index

These paths are the implementation interface. Do not copy rules into a second divergent checklist.

| Responsibility | Source of truth |
| --- | --- |
| Color, typography and dimension variables | [src/styles/tokens.css](src/styles/tokens.css) |
| Base component appearance | [src/styles/components.css](src/styles/components.css) |
| Page geometry and responsive rules | [src/styles/layouts.css](src/styles/layouts.css) |
| Approved local primitives | [src/components/ui/](src/components/ui/) |
| Page composition patterns | [src/components/patterns/](src/components/patterns/) |
| Destination labels / synthetic data | [src/lib/copy.ts](src/lib/copy.ts), [src/lib/data.ts](src/lib/data.ts) |
| Rule metadata and supported scope | [governance/rules.json](governance/rules.json) |
| Time-limited exceptions | [governance/exceptions.json](governance/exceptions.json) |
| Static enforcement | [scripts/check-design.mjs](scripts/check-design.mjs) |
| Runtime, accessibility and layout enforcement | [tests/e2e/design.spec.ts](tests/e2e/design.spec.ts) |
| Mutation fixtures and results | [tests/mutations/](tests/mutations/); generated evidence: `reports/` |

The registry identifies concrete checker entrypoints. The package scripts are the command interface. A broken index, unknown rule, missing entrypoint or invalid exception fails GOV-001. Directory links above are navigation aids, not a claim that every directory has an independent check.

The local adapter exports `Button`, `Input`, and `Icon` from `src/components/ui/index.tsx`. `Button` accepts native button props and `variant="primary" | "secondary" | "ghost"`; `Input` accepts native input props. Patterns are `PageHeader({ title, description?, actions? })`, `EmptyState({ title, description, action: { label, onClick }, icon? })`, and `Shell({ children })`. Read their TypeScript definitions before changing usage; these names are local APIs, not claimed CREAO imports.

## 3. Preserve the existing visual language

The following values were observed on `/widgets`; they are evidence, not a new brand palette. Local tokens may use a shorter semantic alias but must record that mapping in `tokens.css`.

| Observed CSS variable | Observed value | Intended use in this prototype |
| --- | --- | --- |
| `--color-background` | `#f8f6f3` | Page canvas |
| `--color-card` / `--color-surface` | `#fefdfb` | Elevated content surface |
| `--color-chrome` | `#f4f1ed` | App shell |
| `--color-surface-alt` | `#f0ede8` | Subtle grouped surface |
| `--color-foreground` / `--color-primary` | `#16181a` | Ink and primary action |
| `--color-primary-foreground` | `#f3ecd8` | Text on primary action |
| `--color-border` | `#e6e2db` | Hairline structural separator |
| `--color-control-border` | `#ebe7e2` | Observed control-border token; does not by itself prove sufficient contrast |
| `--color-oxblood` | `#6e2f2c` | Negative / signature accent; never the sole error signal |
| `--spacing` | `.25rem` | Observed scale base |
| `--radius` | `.375rem` | Observed generic radius; do not infer all widgets must have this radius |

Observed font stacks start with Instrument Sans for UI, DM Mono for data, JetBrains Mono for code, and EB Garamond for serif. The prototype can use available system fallbacks; do not silently download or claim the same licensed font rendering. Any extra tokens, including positive-state color, focus ring, spacing steps, width limits and mobile breakpoints, are **local proposals** documented in CSS. Verify contrast on actual text/control pairs; the screenshot alone is insufficient.

Official docs describe sharp corners; the observed UI also exposes several radius variables and uses rounded controls. Preserve that difference. Do not derive a universal zero-radius rule from a dashboard paragraph or copy a generic radius to every product surface.

## 4. Choose a page pattern before writing JSX

All top-level routes use an app shell with persistent desktop navigation, a named main region, and a compact navigation control on narrow screens. Put the page identity and highest-priority page action together; put filters beneath; put content and its states in one stable region. Route titles use PageHeader. Inline previews and configuration panels are subordinate to the page identity.

| Pattern | Use when | Required order / composition | Canonical or experimental |
| --- | --- | --- | --- |
| Collection | Files, connectors, agents, skills | PageHeader → search/filter/view controls → result summary where meaningful → collection OR empty/error/loading state | Canonical; demonstrated in `/files`, `/connectors`, `/agents` |
| Detail / preview | Inspect a selected file or agent without losing list context | Identity → metadata/status → content → contextual actions; provide close/back and restore focus | Canonical; file preview demonstrated |
| Chat workbench | User gives intent and monitors work | Conversation identity → ordered messages/results → explicit run/approval state → composer with visible authority and attachment controls | Canonical proposal; not implemented as a full runtime in this lab |
| Configuration | Connection setup, agent defaults, schedule | Identity/back → explanation/scope → labeled fields in logical sections → validation → one save/confirm action | Canonical proposal; real Slack screen informs it; OAuth not executed in lab |
| Approval / run review | Agent needs a decision before an external effect | Actor and operation → target/scope/consequence → approve and cancel → pending/result evidence | Canonical proposal; test before production adoption; not proven by this lab |
| Dashboard | Agent-generated structured result | Stack/Grid root → Cards/group headings → data/charts/tables; keep responsive reading order | Official widget composition; local adapter does not implement the entire widget catalog |

Do not choose a new page shell for a single feature. A new pattern requires a screenshot with representative content and states, a reason existing patterns fail, Product Design approval, and an implementation/test mapping. One-off promotional or immersive views can be scoped exceptions rather than silently becoming canon.

### Collection and detail decisions

- Use a list when users compare repeated fields; use cards when previews or richer descriptions dominate. A view switch must expose selected state and keep search/filter state.
- A page can have multiple actions, but only one filled, visually dominant page-level primary action. Destructive actions belong near the affected object, with explicit consequences before an irreversible effect.
- A preview must not look like a new top-level page unless the URL and navigation context also change. Closing it returns focus to the trigger. Escape and a named close control must work.
- In a collection, loading, initial empty, filtered empty, permission failure and load error are different states. Never reuse “No files” for a failed request.

### Responsive decisions

The lab's navigation compact breakpoint is 760 CSS px; file collections switch to labeled entries at 900 CSS px in `layouts.css` after an 800px overflow was found during visual review; navigation width is `--sidebar-width: 248px` and desktop page padding is `--page-padding: 32px` in `tokens.css`. These are proposed implementation values, not observed official policy. Automated layout checks use 320, 390, 800 and 1280 CSS px widths (900px height). The live-product audit captured 390 × 844; also inspect this viewport and 320 CSS px manually before production integration.

At compact widths, convert file rows to labeled entries: file name first, then each metadata label/value pair. Remove the desktop header when its columns no longer align. Keep names discoverable through the preview or accessible name. Do not leave a narrow desktop header above a stacked list. Controls may hide visible text only if their accessible names remain. Do not use global `overflow-x: hidden` to conceal an overflow bug. A genuinely two-dimensional chart/table can have a labeled local scroll region; the whole page must not require horizontal navigation to reach core actions.

## 5. Rules and failure contracts

All eight rules are mandatory within their declared scopes. `block` means the change cannot become a release candidate without a valid scoped exception. Human judgments are explicitly distinguished from automated checks.

| Rule | Pass contract | Fails when | Enforcement / boundary |
| --- | --- | --- | --- |
| **DS-001** Token use | Governed styles use registered semantic color variables. Literal palette values occur only in `tokens.css`. | A page/component stylesheet adds an unregistered literal color or references an unknown governed token. | CSS AST/static checker. A token can still be used with the wrong meaning: reviewer checks semantics and contrast. |
| **DS-002** Primitive reuse | Feature JSX composes approved local UI primitives; actual native control implementations stay inside the UI boundary. | Governed feature/pattern JSX directly creates `button`, `input`, `select` or `textarea`, including lexically resolved const aliases of those string tags. | TS/JSX AST/static checker. It resolves static const string aliases with TypeScript symbols, but does not resolve import provenance, custom wrappers, dynamic aliases or factories; approved library provenance still requires review. |
| **LAY-001** Page identity | Each governed route has one visible top-level `h1` within its main region, matching that route's identity. Nested preview/section headings are subordinate. | Missing, duplicate, hidden or incorrect main title. A large button/span styled as a heading does not qualify. | DOM test on every governed route at desktop and compact sizes. Correct overall information architecture remains a design review item. |
| **A11Y-001** Named controls | Each operable visible button/input/select/link has a non-empty accessible name in the tested states and viewports. Icon controls retain names when text hides. | Name disappears, label is missing, or a control has no usable identifier. | Runtime accessible-name assertions. A non-empty but misleading name can pass; reviewer must assess meaning, focus order and keyboard operation. |
| **STATE-001** Recovery | Recoverable empty states explain why and offer an in-state action that actually recovers. Initial empty → create/connect; filtered empty → clear relevant filters; error → retry/appropriate help. | Recovery is absent, inert or leads to the wrong state. A separate distant tab alone is insufficient. | Browser interaction fixtures for known empty states and post-action results. Production network/error states need adapter tests beyond the local fixture. |
| **NAV-001** Destination language | Guidance and controls derive destination names from the same label source; actions reveal that destination. | “Available” is referenced when the actual tab is “Connectable”, or the action activates another tab. | Browser assertions against the canonical Chinese destination name, guidance and actual tab/region. Shared-source reuse is a source-review requirement, not import analysis. Localization requires the same check for each supported locale. |
| **RESP-001** Field integrity | At tested compact widths, every metadata value stays associated with its visible label, controls stay reachable and key rectangles do not overlap/clip. | Desktop headers no longer correspond to stacked values, or essential content overlaps/offscreen. | Browser geometry and label/structure assertions plus screenshot review. No claim of full visual correctness or every-device coverage. |
| **GOV-001** Contract integrity | Registry, document/index links, checker paths and exception records are valid and current. Rule/check changes have owner review. | Referenced files are missing, rule IDs drift, or exception records are malformed/expired/outside their declared scope. | Static validation can check records, not the identity of an approver. External required checks and ownership enforce review. |

Automated route coverage is `/files`, `/connectors`, `/agents` and `/guidelines`, as recorded in the registry. Future routes and unrepresented dynamic states still require review or new fixtures. DS-001 covers source CSS only; inline styles, CSS-in-JS, dynamically generated styles, external CSS and HTML color attributes are outside its current checker scope. Semantic CSS keywords such as `transparent`, `currentColor` and `inherit` are allowed; they do not define new palette values. Adding a privileged UI implementation or changing token authority requires owner review even if the static check passes.

### State recipes

| Situation | Required message | Next action | Result to assert |
| --- | --- | --- | --- |
| No connected services | “No connected services” + why connecting helps | “Browse connectable services” | Connectable tab is selected and eligible services appear |
| File search finds nothing | State that current query/filters matched nothing | “Clear search” or “Clear filters” | Query/filter resets and seeded files reappear |
| No agents yet | Explain repeatable work and how creation starts | “Create agent” / local example action | Documented create flow opens; lab must identify it as a simulation |
| Load error | Distinguish failed loading from no data | Retry, or permission-specific guidance | Retry is attempted / permission destination is correct |
| Agent running / awaiting approval | Text status, next expected event and available controls | View progress / make an explicit decision | Status transitions from actual response, never inferred from animation alone |

## 6. Before a change ships

1. Declare the pattern, affected route/state/viewports and applicable rule IDs in the change description.
2. Read component implementation and CSS; reuse existing variants before adding styles. Register genuinely new tokens with purpose and provenance.
3. Implement the behavior and fixtures. Run the package's type, lint, static design, production build and browser checks. Run mutation checks when changing rules, checkers, shared components or layout contracts.
4. Inspect desktop and compact screenshots and perform keyboard/focus checks for changed interactions. A green machine check does not waive human design judgment.
5. Attach command results, screenshots and any exception ID. Record failures/skips as such; do not silently regenerate snapshots or edit tests just to accept changed behavior.
6. Owner review covers pattern choice, semantics, hierarchy, contrast and changes to governance assets. CI must execute against the candidate commit; CD accepts only an artifact from that successful candidate, followed by deployment smoke checks.

From this directory, the concrete gate commands are:

```sh
npm ci
npm run typecheck
npm run lint
npm run check:design
npm run build
npm run test:e2e
npm run test:mutations
```

Use `npm run dev -- --port 3100` for interactive local inspection. Read the test runner configuration for server startup/port ownership; do not launch competing servers on the same port. The listed commands describe the required gate, not a claim that a run has succeeded. Actual receipts live under `reports/` and are summarized in the compliance audit.

The prototype demonstrates a local gate. GitHub required checks, CODEOWNERS enforcement, protected environments and deployment receipts must be configured separately. `AGENTS.md` instructs cooperative agents; it is not an access-control boundary. A contributor able to edit every checker and CI policy can bypass local restrictions.

## 7. Exceptions and evolution

`exceptions.json` has the root shape `{ "exceptions": [] }`. Each record requires exactly `id`, `ruleId`, `path`, `reason`, `owner`, `approvedBy`, and `expires` (YYYY-MM-DD; current implementation expires at the end of that UTC date). Use an exact existing relative file path and document affected route/state, tracking reference and compensating verification in the reason/review record. An expired exception fails closed. Never use a wildcard exception for an entire app. This legacy file-level implementation supports DS-001 and DS-002 only; unsupported entries still fail closed. This implementation limit is not a permanent ban on human exceptions for browser or visual design findings. The expanded release-decision contract is [Human exceptions and scoped bypass](governance/human-exceptions-policy.md). `approvedBy` alone is not authenticated approval.

Human-approved departures are supported for important features, scoped experiments and documented tradeoffs. Standard exceptions require the Product Design and Frontend owner responsibilities to sign off (a registered dual-role owner may satisfy both), last no more than seven days, and prohibit requester self-approval. A CTO or explicitly delegated release owner can approve an emergency design exception for at most 24 hours, with user impact, compensating verification, rollback and independent follow-up; any requester/approver overlap must be recorded. Engineer and coordinator agents can prepare or execute an approved decision, but cannot impersonate an approver.

Bind the decision to one repository/candidate SHA, policy and evidence digests, exact rule/check/finding scope and UTC expiry. Preserve original failed checks and report `accepted_with_exceptions`, never a fabricated clean pass. New failures, changed candidates, expiration or revocation require reevaluation. Missing evidence, execution failures and invalid approval cannot be waived as successful design checks. The policy provides request/approve/evaluate/revoke protocol instructions, exact coordinator approval wording, CI aggregation semantics and acceptance tests. Runtime/CI integration and verified platform approval are separate evidence; until they exist, that expanded path must be labeled pending or simulation. Once valid authorization exists, proceed within scope without repeatedly asking for the same approval.

Repeated exceptions indicate a missing pattern or an incorrect rule. Review them with Product Design + Engineering, then revise the contract and add positive/negative examples. Separate a real product violation from a checker false positive. Keep the original mutation results when improving coverage; report survivors and invalid experiments honestly.

## 8. What this contract does not prove

This lab does not recover CREAO's internal component library, change its production site, execute real integrations, validate live agent runs or prove universal WCAG compliance. Static checks cover documented syntax and files; runtime checks cover explicit route/state fixtures. Screenshots are retained locally and may contain account context: use cropped/redacted copies before public submission. The experiment's evidence is useful because those limits are explicit.
