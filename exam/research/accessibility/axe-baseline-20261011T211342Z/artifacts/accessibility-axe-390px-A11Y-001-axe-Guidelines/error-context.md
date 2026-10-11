# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accessibility.spec.ts >> axe 390px >> [A11Y-001] axe Guidelines
- Location: tests/e2e/accessibility.spec.ts:89:9

# Error details

```
Error: Automated WCAG A/AA violations in guidelines

expect(received).toEqual(expected) // deep equality

- Expected  -   1
+ Received  + 136

- Array []
+ Array [
+   Object {
+     "description": "Ensure elements that have scrollable content are accessible by keyboard in Safari",
+     "help": "Scrollable region must have keyboard access",
+     "helpUrl": "https://dequeuniversity.com/rules/axe/4.13/scrollable-region-focusable?application=playwright",
+     "id": "scrollable-region-focusable",
+     "impact": "serious",
+     "nodes": Array [
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "focusable-content",
+             "impact": "serious",
+             "message": "Element should have focusable content",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "focusable-element",
+             "impact": "serious",
+             "message": "Element should be focusable",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element should have focusable content
+   Element should be focusable",
+         "html": "<table>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "table:nth-child(14)",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "focusable-content",
+             "impact": "serious",
+             "message": "Element should have focusable content",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "focusable-element",
+             "impact": "serious",
+             "message": "Element should be focusable",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element should have focusable content
+   Element should be focusable",
+         "html": "<table>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "table:nth-child(19)",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "focusable-content",
+             "impact": "serious",
+             "message": "Element should have focusable content",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "focusable-element",
+             "impact": "serious",
+             "message": "Element should be focusable",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element should have focusable content
+   Element should be focusable",
+         "html": "<table>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "table:nth-child(28)",
+         ],
+       },
+       Object {
+         "all": Array [],
+         "any": Array [
+           Object {
+             "data": null,
+             "id": "focusable-content",
+             "impact": "serious",
+             "message": "Element should have focusable content",
+             "relatedNodes": Array [],
+           },
+           Object {
+             "data": null,
+             "id": "focusable-element",
+             "impact": "serious",
+             "message": "Element should be focusable",
+             "relatedNodes": Array [],
+           },
+         ],
+         "failureSummary": "Fix any of the following:
+   Element should have focusable content
+   Element should be focusable",
+         "html": "<table>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "table:nth-child(31)",
+         ],
+       },
+     ],
+     "tags": Array [
+       "cat.keyboard",
+       "wcag2a",
+       "wcag211",
+       "wcag213",
+       "TTv5",
+       "TT4.a",
+       "EN-301-549",
+       "EN-9.2.1.1",
+       "EN-9.2.1.3",
+       "RGAAv4",
+       "RGAA-7.3.2",
+     ],
+   },
+ ]
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e2]:
    - link "跳到主要内容" [ref=e3] [cursor=pointer]:
      - /url: "#main-content"
    - generic [ref=e4]:
      - button "切换导航" [ref=e5] [cursor=pointer]
      - generic [ref=e7]: CREAO
    - main [ref=e8]:
      - generic [ref=e10]:
        - heading "设计规范" [level=1] [ref=e11]
        - paragraph [ref=e12]: 本地适配规范与执行入口。规则是否通过，以实际检查报告为准。
      - article [ref=e13]:
        - heading "CREAO product design contract" [level=2] [ref=e14]
        - paragraph [ref=e15]: "Version: 0.1 · 2026-10-11 · Owner: Product Design + Frontend Engineering."
        - paragraph [ref=e16]:
          - text: This is the implementation contract for the
          - strong [ref=e17]: local CREAO Design Lab
          - text: . It is an evidence-informed proposal for CREAO's product layer, not CREAO's private design-system source. Read this file before changing a screen; use
          - link "AGENTS.md" [ref=e18] [cursor=pointer]:
            - /url: /reference?file=AGENTS.md
          - text: for the delivery workflow. The submission-level rationale is in
          - generic [ref=e19]: design-system-guideline.md（工作区附件）
          - text: .
        - heading "1. Source boundaries" [level=3] [ref=e20]
        - table [ref=e21]:
          - rowgroup [ref=e22]:
            - row [ref=e23]:
              - columnheader "Class" [ref=e24]
              - columnheader "Evidence" [ref=e25]
              - columnheader "What it establishes" [ref=e26]
          - rowgroup [ref=e27]:
            - row [ref=e28]:
              - cell "Official" [ref=e29]
              - cell "Widgets documentation, saved Markdown（工作区附件）" [ref=e30]:
                - link "Widgets documentation" [ref=e31] [cursor=pointer]:
                  - /url: https://docs.creao.ai/features/widgets
                - text: ","
                - generic [ref=e32]: saved Markdown（工作区附件）
              - 'cell "Dashboard component categories and composition: a Stack/Grid root, Cards for groups, data/chart/table widgets inside. Warm surfaces, near-black ink and restrained semantic color." [ref=e33]'
            - row [ref=e34]:
              - cell "Observed" [ref=e35]
              - cell "Widgets screenshot（工作区附件）, DOM/CSS snapshot（工作区附件）" [ref=e36]:
                - generic [ref=e37]: Widgets screenshot（工作区附件）
                - text: ","
                - generic [ref=e38]: DOM/CSS snapshot（工作区附件）
              - cell "Actual rendered controls, variable values and parameter labels at one point in time. These do not establish private import paths or supported component APIs." [ref=e39]
            - row [ref=e40]:
              - cell "Observed" [ref=e41]
              - cell "Files mobile（工作区附件）, Files DOM（工作区附件）, connectors empty state（工作区附件）" [ref=e42]:
                - generic [ref=e43]: Files mobile（工作区附件）
                - text: ","
                - generic [ref=e44]: Files DOM（工作区附件）
                - text: ","
                - generic [ref=e45]: connectors empty state（工作区附件）
              - cell "Screen behavior and specific design defects used to define testable rules." [ref=e46]
            - row [ref=e47]:
              - cell "Proposed" [ref=e48]
              - cell "This document, local CSS, local components and checks" [ref=e49]
              - cell "Product-level patterns, responsive decisions, acceptance thresholds and enforcement for this experiment." [ref=e50]
        - paragraph [ref=e51]:
          - text: Public sitemap research found official Widgets documentation, but no indexed full-product
          - code [ref=e52]: design.md
          - text: . The product sitemap returned 403. This is
          - strong [ref=e53]: not evidence that an internal design system does not exist
          - text: . The task states that it does. Replace the local adapter's imports with real approved library imports when integrating in that repository; preserve the contracts below.
        - heading "2. Executable index" [level=3] [ref=e54]
        - paragraph [ref=e55]: These paths are the implementation interface. Do not copy rules into a second divergent checklist.
        - table [ref=e56]:
          - rowgroup [ref=e57]:
            - row [ref=e58]:
              - columnheader "Responsibility" [ref=e59]
              - columnheader "Source of truth" [ref=e60]
          - rowgroup [ref=e61]:
            - row [ref=e62]:
              - cell "Color, typography and dimension variables" [ref=e63]
              - cell [ref=e64]:
                - link "src/styles/tokens.css" [ref=e65] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Ftokens.css
            - row [ref=e66]:
              - cell "Base component appearance" [ref=e67]
              - cell [ref=e68]:
                - link "src/styles/components.css" [ref=e69] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Fcomponents.css
            - row [ref=e70]:
              - cell "Page geometry and responsive rules" [ref=e71]
              - cell [ref=e72]:
                - link "src/styles/layouts.css" [ref=e73] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Flayouts.css
            - row [ref=e74]:
              - cell "Approved local primitives" [ref=e75]
              - cell [ref=e76]:
                - link "src/components/ui/" [ref=e77] [cursor=pointer]:
                  - /url: /reference?group=src%2Fcomponents%2Fui%2F
            - row [ref=e78]:
              - cell "Page composition patterns" [ref=e79]
              - cell [ref=e80]:
                - link "src/components/patterns/" [ref=e81] [cursor=pointer]:
                  - /url: /reference?group=src%2Fcomponents%2Fpatterns%2F
            - row [ref=e82]:
              - cell "Destination labels / synthetic data" [ref=e83]
              - cell [ref=e84]:
                - link "src/lib/copy.ts" [ref=e85] [cursor=pointer]:
                  - /url: /reference?file=src%2Flib%2Fcopy.ts
                - text: ","
                - link "src/lib/data.ts" [ref=e86] [cursor=pointer]:
                  - /url: /reference?file=src%2Flib%2Fdata.ts
            - row [ref=e87]:
              - cell "Rule metadata and supported scope" [ref=e88]
              - cell [ref=e89]:
                - link "governance/rules.json" [ref=e90] [cursor=pointer]:
                  - /url: /reference?file=governance%2Frules.json
            - row [ref=e91]:
              - cell "Time-limited exceptions" [ref=e92]
              - cell [ref=e93]:
                - link "governance/exceptions.json" [ref=e94] [cursor=pointer]:
                  - /url: /reference?file=governance%2Fexceptions.json
            - row [ref=e95]:
              - cell "Static enforcement" [ref=e96]
              - cell [ref=e97]:
                - link "scripts/check-design.mjs" [ref=e98] [cursor=pointer]:
                  - /url: /reference?file=scripts%2Fcheck-design.mjs
            - row [ref=e99]:
              - cell "Runtime, accessibility and layout enforcement" [ref=e100]
              - cell [ref=e101]:
                - link "tests/e2e/design.spec.ts" [ref=e102] [cursor=pointer]:
                  - /url: /reference?file=tests%2Fe2e%2Fdesign.spec.ts
            - row [ref=e103]:
              - cell "Mutation fixtures and results" [ref=e104]
              - cell [ref=e105]:
                - link "tests/mutations/" [ref=e106] [cursor=pointer]:
                  - /url: /reference?group=tests%2Fmutations%2F
                - text: "; generated evidence:"
                - code [ref=e107]: reports/
        - paragraph [ref=e108]: The registry identifies concrete checker entrypoints. The package scripts are the command interface. A broken index, unknown rule, missing entrypoint or invalid exception fails GOV-001. Directory links above are navigation aids, not a claim that every directory has an independent check.
        - paragraph [ref=e109]:
          - text: The local adapter exports
          - code [ref=e110]: Button
          - text: ","
          - code [ref=e111]: Input
          - text: ", and"
          - code [ref=e112]: Icon
          - text: from
          - code [ref=e113]: src/components/ui/index.tsx
          - text: .
          - code [ref=e114]: Button
          - text: accepts native button props and
          - code [ref=e115]: variant="primary" | "secondary" | "ghost"
          - text: ;
          - code [ref=e116]: Input
          - text: accepts native input props. Patterns are
          - code [ref=e117]: "PageHeader({ title, description?, actions? })"
          - text: ","
          - code [ref=e118]: "EmptyState({ title, description, action: { label, onClick }, icon? })"
          - text: ", and"
          - code [ref=e119]: "Shell({ children })"
          - text: . Read their TypeScript definitions before changing usage; these names are local APIs, not claimed CREAO imports.
        - heading "3. Preserve the existing visual language" [level=3] [ref=e120]
        - paragraph [ref=e121]:
          - text: The following values were observed on
          - code [ref=e122]: /widgets
          - text: ; they are evidence, not a new brand palette. Local tokens may use a shorter semantic alias but must record that mapping in
          - code [ref=e123]: tokens.css
          - text: .
        - table [ref=e124]:
          - rowgroup [ref=e125]:
            - row [ref=e126]:
              - columnheader "Observed CSS variable" [ref=e127]
              - columnheader "Observed value" [ref=e128]
              - columnheader "Intended use in this prototype" [ref=e129]
          - rowgroup [ref=e130]:
            - row [ref=e131]:
              - cell [ref=e132]:
                - code [ref=e133]: "--color-background"
              - cell [ref=e134]:
                - code [ref=e135]: "#f8f6f3"
              - cell "Page canvas" [ref=e136]
            - row [ref=e137]:
              - cell [ref=e138]:
                - code [ref=e139]: "--color-card"
                - text: /
                - code [ref=e140]: "--color-surface"
              - cell [ref=e141]:
                - code [ref=e142]: "#fefdfb"
              - cell "Elevated content surface" [ref=e143]
            - row [ref=e144]:
              - cell [ref=e145]:
                - code [ref=e146]: "--color-chrome"
              - cell [ref=e147]:
                - code [ref=e148]: "#f4f1ed"
              - cell "App shell" [ref=e149]
            - row [ref=e150]:
              - cell [ref=e151]:
                - code [ref=e152]: "--color-surface-alt"
              - cell [ref=e153]:
                - code [ref=e154]: "#f0ede8"
              - cell "Subtle grouped surface" [ref=e155]
            - row [ref=e156]:
              - cell [ref=e157]:
                - code [ref=e158]: "--color-foreground"
                - text: /
                - code [ref=e159]: "--color-primary"
              - cell [ref=e160]:
                - code [ref=e161]: "#16181a"
              - cell "Ink and primary action" [ref=e162]
            - row [ref=e163]:
              - cell [ref=e164]:
                - code [ref=e165]: "--color-primary-foreground"
              - cell [ref=e166]:
                - code [ref=e167]: "#f3ecd8"
              - cell "Text on primary action" [ref=e168]
            - row [ref=e169]:
              - cell [ref=e170]:
                - code [ref=e171]: "--color-border"
              - cell [ref=e172]:
                - code [ref=e173]: "#e6e2db"
              - cell "Hairline structural separator" [ref=e174]
            - row [ref=e175]:
              - cell [ref=e176]:
                - code [ref=e177]: "--color-control-border"
              - cell [ref=e178]:
                - code [ref=e179]: "#ebe7e2"
              - cell "Observed control-border token; does not by itself prove sufficient contrast" [ref=e180]
            - row [ref=e181]:
              - cell [ref=e182]:
                - code [ref=e183]: "--color-oxblood"
              - cell [ref=e184]:
                - code [ref=e185]: "#6e2f2c"
              - cell "Negative / signature accent; never the sole error signal" [ref=e186]
            - row [ref=e187]:
              - cell [ref=e188]:
                - code [ref=e189]: "--spacing"
              - cell [ref=e190]:
                - code [ref=e191]: .25rem
              - cell "Observed scale base" [ref=e192]
            - row [ref=e193]:
              - cell [ref=e194]:
                - code [ref=e195]: "--radius"
              - cell [ref=e196]:
                - code [ref=e197]: .375rem
              - cell "Observed generic radius; do not infer all widgets must have this radius" [ref=e198]
        - paragraph [ref=e199]:
          - text: Observed font stacks start with Instrument Sans for UI, DM Mono for data, JetBrains Mono for code, and EB Garamond for serif. The prototype can use available system fallbacks; do not silently download or claim the same licensed font rendering. Any extra tokens, including positive-state color, focus ring, spacing steps, width limits and mobile breakpoints, are
          - strong [ref=e200]: local proposals
          - text: documented in CSS. Verify contrast on actual text/control pairs; the screenshot alone is insufficient.
        - paragraph [ref=e201]: Official docs describe sharp corners; the observed UI also exposes several radius variables and uses rounded controls. Preserve that difference. Do not derive a universal zero-radius rule from a dashboard paragraph or copy a generic radius to every product surface.
        - heading "4. Choose a page pattern before writing JSX" [level=3] [ref=e202]
        - paragraph [ref=e203]: All top-level routes use an app shell with persistent desktop navigation, a named main region, and a compact navigation control on narrow screens. Put the page identity and highest-priority page action together; put filters beneath; put content and its states in one stable region. Route titles use PageHeader. Inline previews and configuration panels are subordinate to the page identity.
        - table [ref=e204]:
          - rowgroup [ref=e205]:
            - row [ref=e206]:
              - columnheader "Pattern" [ref=e207]
              - columnheader "Use when" [ref=e208]
              - columnheader "Required order / composition" [ref=e209]
              - columnheader "Canonical or experimental" [ref=e210]
          - rowgroup [ref=e211]:
            - row [ref=e212]:
              - cell "Collection" [ref=e213]
              - cell "Files, connectors, agents, skills" [ref=e214]
              - cell "PageHeader → search/filter/view controls → result summary where meaningful → collection OR empty/error/loading state" [ref=e215]
              - cell [ref=e216]:
                - text: Canonical; demonstrated in
                - code [ref=e217]: /files
                - text: ","
                - code [ref=e218]: /connectors
                - text: ","
                - code [ref=e219]: /agents
            - row [ref=e220]:
              - cell "Detail / preview" [ref=e221]
              - cell "Inspect a selected file or agent without losing list context" [ref=e222]
              - cell "Identity → metadata/status → content → contextual actions; provide close/back and restore focus" [ref=e223]
              - cell "Canonical; file preview demonstrated" [ref=e224]
            - row [ref=e225]:
              - cell "Chat workbench" [ref=e226]
              - cell "User gives intent and monitors work" [ref=e227]
              - cell "Conversation identity → ordered messages/results → explicit run/approval state → composer with visible authority and attachment controls" [ref=e228]
              - cell "Canonical proposal; not implemented as a full runtime in this lab" [ref=e229]
            - row [ref=e230]:
              - cell "Configuration" [ref=e231]
              - cell "Connection setup, agent defaults, schedule" [ref=e232]
              - cell "Identity/back → explanation/scope → labeled fields in logical sections → validation → one save/confirm action" [ref=e233]
              - cell "Canonical proposal; real Slack screen informs it; OAuth not executed in lab" [ref=e234]
            - row [ref=e235]:
              - cell "Approval / run review" [ref=e236]
              - cell "Agent needs a decision before an external effect" [ref=e237]
              - cell "Actor and operation → target/scope/consequence → approve and cancel → pending/result evidence" [ref=e238]
              - cell "Canonical proposal; test before production adoption; not proven by this lab" [ref=e239]
            - row [ref=e240]:
              - cell "Dashboard" [ref=e241]
              - cell "Agent-generated structured result" [ref=e242]
              - cell "Stack/Grid root → Cards/group headings → data/charts/tables; keep responsive reading order" [ref=e243]
              - cell "Official widget composition; local adapter does not implement the entire widget catalog" [ref=e244]
        - paragraph [ref=e245]: Do not choose a new page shell for a single feature. A new pattern requires a screenshot with representative content and states, a reason existing patterns fail, Product Design approval, and an implementation/test mapping. One-off promotional or immersive views can be scoped exceptions rather than silently becoming canon.
        - heading "Collection and detail decisions" [level=4] [ref=e246]
        - list [ref=e247]:
          - listitem [ref=e248]: Use a list when users compare repeated fields; use cards when previews or richer descriptions dominate. A view switch must expose selected state and keep search/filter state.
          - listitem [ref=e249]: A page can have multiple actions, but only one filled, visually dominant page-level primary action. Destructive actions belong near the affected object, with explicit consequences before an irreversible effect.
          - listitem [ref=e250]: A preview must not look like a new top-level page unless the URL and navigation context also change. Closing it returns focus to the trigger. Escape and a named close control must work.
          - listitem [ref=e251]: In a collection, loading, initial empty, filtered empty, permission failure and load error are different states. Never reuse “No files” for a failed request.
        - heading "Responsive decisions" [level=4] [ref=e252]
        - paragraph [ref=e253]:
          - text: The lab's navigation compact breakpoint is 760 CSS px; file collections switch to labeled entries at 900 CSS px in
          - code [ref=e254]: layouts.css
          - text: after an 800px overflow was found during visual review; navigation width is
          - code [ref=e255]: "--sidebar-width: 248px"
          - text: and desktop page padding is
          - code [ref=e256]: "--page-padding: 32px"
          - text: in
          - code [ref=e257]: tokens.css
          - text: . These are proposed implementation values, not observed official policy. Automated layout checks use 320, 390, 800 and 1280 CSS px widths (900px height). The live-product audit captured 390 × 844; also inspect this viewport and 320 CSS px manually before production integration.
        - paragraph [ref=e258]:
          - text: "At compact widths, convert file rows to labeled entries: file name first, then each metadata label/value pair. Remove the desktop header when its columns no longer align. Keep names discoverable through the preview or accessible name. Do not leave a narrow desktop header above a stacked list. Controls may hide visible text only if their accessible names remain. Do not use global"
          - code [ref=e259]: "overflow-x: hidden"
          - text: to conceal an overflow bug. A genuinely two-dimensional chart/table can have a labeled local scroll region; the whole page must not require horizontal navigation to reach core actions.
        - heading "5. Rules and failure contracts" [level=3] [ref=e260]
        - paragraph [ref=e261]:
          - text: All eight rules are mandatory within their declared scopes.
          - code [ref=e262]: block
          - text: means the change cannot become a release candidate without a valid scoped exception. Human judgments are explicitly distinguished from automated checks.
        - table [ref=e263]:
          - rowgroup [ref=e264]:
            - row [ref=e265]:
              - columnheader "Rule" [ref=e266]
              - columnheader "Pass contract" [ref=e267]
              - columnheader "Fails when" [ref=e268]
              - columnheader "Enforcement / boundary" [ref=e269]
          - rowgroup [ref=e270]:
            - row [ref=e271]:
              - cell [ref=e272]:
                - strong [ref=e273]: DS-001
                - text: Token use
              - cell [ref=e274]:
                - text: Governed styles use registered semantic color variables. Literal palette values occur only in
                - code [ref=e275]: tokens.css
                - text: .
              - cell "A page/component stylesheet adds an unregistered literal color or references an unknown governed token." [ref=e276]
              - 'cell "CSS AST/static checker. A token can still be used with the wrong meaning: reviewer checks semantics and contrast." [ref=e277]'
            - row [ref=e278]:
              - cell [ref=e279]:
                - strong [ref=e280]: DS-002
                - text: Primitive reuse
              - cell "Feature JSX composes approved local UI primitives; actual native control implementations stay inside the UI boundary." [ref=e281]
              - cell [ref=e282]:
                - text: Governed feature/pattern JSX directly creates
                - code [ref=e283]: button
                - text: ","
                - code [ref=e284]: input
                - text: ","
                - code [ref=e285]: select
                - text: or
                - code [ref=e286]: textarea
                - text: ", including lexically resolved const aliases of those string tags."
              - cell "TS/JSX AST/static checker. It resolves static const string aliases with TypeScript symbols, but does not resolve import provenance, custom wrappers, dynamic aliases or factories; approved library provenance still requires review." [ref=e287]
            - row [ref=e288]:
              - cell [ref=e289]:
                - strong [ref=e290]: LAY-001
                - text: Page identity
              - cell [ref=e291]:
                - text: Each governed route has one visible top-level
                - code [ref=e292]: h1
                - text: within its main region, matching that route's identity. Nested preview/section headings are subordinate.
              - cell "Missing, duplicate, hidden or incorrect main title. A large button/span styled as a heading does not qualify." [ref=e293]
              - cell "DOM test on every governed route at desktop and compact sizes. Correct overall information architecture remains a design review item." [ref=e294]
            - row [ref=e295]:
              - cell [ref=e296]:
                - strong [ref=e297]: A11Y-001
                - text: Named controls
              - cell "Each operable visible button/input/select/link has a non-empty accessible name in the tested states and viewports. Icon controls retain names when text hides." [ref=e298]
              - cell "Name disappears, label is missing, or a control has no usable identifier." [ref=e299]
              - cell "Runtime accessible-name assertions. A non-empty but misleading name can pass; reviewer must assess meaning, focus order and keyboard operation." [ref=e300]
            - row [ref=e301]:
              - cell [ref=e302]:
                - strong [ref=e303]: STATE-001
                - text: Recovery
              - cell "Recoverable empty states explain why and offer an in-state action that actually recovers. Initial empty → create/connect; filtered empty → clear relevant filters; error → retry/appropriate help." [ref=e304]
              - cell "Recovery is absent, inert or leads to the wrong state. A separate distant tab alone is insufficient." [ref=e305]
              - cell "Browser interaction fixtures for known empty states and post-action results. Production network/error states need adapter tests beyond the local fixture." [ref=e306]
            - row [ref=e307]:
              - cell [ref=e308]:
                - strong [ref=e309]: NAV-001
                - text: Destination language
              - cell "Guidance and controls derive destination names from the same label source; actions reveal that destination." [ref=e310]
              - cell "“Available” is referenced when the actual tab is “Connectable”, or the action activates another tab." [ref=e311]
              - cell "Browser assertions against the canonical Chinese destination name, guidance and actual tab/region. Shared-source reuse is a source-review requirement, not import analysis. Localization requires the same check for each supported locale." [ref=e312]
            - row [ref=e313]:
              - cell [ref=e314]:
                - strong [ref=e315]: RESP-001
                - text: Field integrity
              - cell "At tested compact widths, every metadata value stays associated with its visible label, controls stay reachable and key rectangles do not overlap/clip." [ref=e316]
              - cell "Desktop headers no longer correspond to stacked values, or essential content overlaps/offscreen." [ref=e317]
              - cell "Browser geometry and label/structure assertions plus screenshot review. No claim of full visual correctness or every-device coverage." [ref=e318]
            - row [ref=e319]:
              - cell [ref=e320]:
                - strong [ref=e321]: GOV-001
                - text: Contract integrity
              - cell "Registry, document/index links, checker paths and exception records are valid and current. Rule/check changes have owner review." [ref=e322]
              - cell "Referenced files are missing, rule IDs drift, or exception records are malformed/expired/outside their declared scope." [ref=e323]
              - cell "Static validation can check records, not the identity of an approver. External required checks and ownership enforce review." [ref=e324]
        - paragraph [ref=e325]:
          - text: Automated route coverage is
          - code [ref=e326]: /files
          - text: ","
          - code [ref=e327]: /connectors
          - text: ","
          - code [ref=e328]: /agents
          - text: and
          - code [ref=e329]: /guidelines
          - text: ", as recorded in the registry. Future routes and unrepresented dynamic states still require review or new fixtures. DS-001 covers source CSS only; inline styles, CSS-in-JS, dynamically generated styles, external CSS and HTML color attributes are outside its current checker scope. Semantic CSS keywords such as"
          - code [ref=e330]: transparent
          - text: ","
          - code [ref=e331]: currentColor
          - text: and
          - code [ref=e332]: inherit
          - text: are allowed; they do not define new palette values. Adding a privileged UI implementation or changing token authority requires owner review even if the static check passes.
        - heading "State recipes" [level=4] [ref=e333]
        - table [ref=e334]:
          - rowgroup [ref=e335]:
            - row [ref=e336]:
              - columnheader "Situation" [ref=e337]
              - columnheader "Required message" [ref=e338]
              - columnheader "Next action" [ref=e339]
              - columnheader "Result to assert" [ref=e340]
          - rowgroup [ref=e341]:
            - row [ref=e342]:
              - cell "No connected services" [ref=e343]
              - cell "“No connected services” + why connecting helps" [ref=e344]
              - cell "“Browse connectable services”" [ref=e345]
              - cell "Connectable tab is selected and eligible services appear" [ref=e346]
            - row [ref=e347]:
              - cell "File search finds nothing" [ref=e348]
              - cell "State that current query/filters matched nothing" [ref=e349]
              - cell "“Clear search” or “Clear filters”" [ref=e350]
              - cell "Query/filter resets and seeded files reappear" [ref=e351]
            - row [ref=e352]:
              - cell "No agents yet" [ref=e353]
              - cell "Explain repeatable work and how creation starts" [ref=e354]
              - cell "“Create agent” / local example action" [ref=e355]
              - cell "Documented create flow opens; lab must identify it as a simulation" [ref=e356]
            - row [ref=e357]:
              - cell "Load error" [ref=e358]
              - cell "Distinguish failed loading from no data" [ref=e359]
              - cell "Retry, or permission-specific guidance" [ref=e360]
              - cell "Retry is attempted / permission destination is correct" [ref=e361]
            - row [ref=e362]:
              - cell "Agent running / awaiting approval" [ref=e363]
              - cell "Text status, next expected event and available controls" [ref=e364]
              - cell "View progress / make an explicit decision" [ref=e365]
              - cell "Status transitions from actual response, never inferred from animation alone" [ref=e366]
        - heading "6. Before a change ships" [level=3] [ref=e367]
        - list [ref=e368]:
          - listitem [ref=e369]: Declare the pattern, affected route/state/viewports and applicable rule IDs in the change description.
          - listitem [ref=e370]: Read component implementation and CSS; reuse existing variants before adding styles. Register genuinely new tokens with purpose and provenance.
          - listitem [ref=e371]: Implement the behavior and fixtures. Run the package's type, lint, static design, production build and browser checks. Run mutation checks when changing rules, checkers, shared components or layout contracts.
          - listitem [ref=e372]: Inspect desktop and compact screenshots and perform keyboard/focus checks for changed interactions. A green machine check does not waive human design judgment.
          - listitem [ref=e373]: Attach command results, screenshots and any exception ID. Record failures/skips as such; do not silently regenerate snapshots or edit tests just to accept changed behavior.
          - listitem [ref=e374]: Owner review covers pattern choice, semantics, hierarchy, contrast and changes to governance assets. CI must execute against the candidate commit; CD accepts only an artifact from that successful candidate, followed by deployment smoke checks.
        - paragraph [ref=e375]: "From this directory, the concrete gate commands are:"
        - code [ref=e377]: npm ci npm run typecheck npm run lint npm run check:design npm run build npm run test:e2e npm run test:mutations
        - paragraph [ref=e378]:
          - text: Use
          - code [ref=e379]: npm run dev -- --port 3100
          - text: for interactive local inspection. Read the test runner configuration for server startup/port ownership; do not launch competing servers on the same port. The listed commands describe the required gate, not a claim that a run has succeeded. Actual receipts live under
          - code [ref=e380]: reports/
          - text: and are summarized in the compliance audit.
        - paragraph [ref=e381]:
          - text: The prototype demonstrates a local gate. GitHub required checks, CODEOWNERS enforcement, protected environments and deployment receipts must be configured separately.
          - code [ref=e382]: AGENTS.md
          - text: instructs cooperative agents; it is not an access-control boundary. A contributor able to edit every checker and CI policy can bypass local restrictions.
        - heading "7. Exceptions and evolution" [level=3] [ref=e383]
        - paragraph [ref=e384]:
          - code [ref=e385]: exceptions.json
          - text: has the root shape
          - code [ref=e386]: "{ \"exceptions\": [] }"
          - text: . Each record requires exactly
          - code [ref=e387]: id
          - text: ","
          - code [ref=e388]: ruleId
          - text: ","
          - code [ref=e389]: path
          - text: ","
          - code [ref=e390]: reason
          - text: ","
          - code [ref=e391]: owner
          - text: ","
          - code [ref=e392]: approvedBy
          - text: ", and"
          - code [ref=e393]: expires
          - text: (YYYY-MM-DD; current implementation expires at the end of that UTC date). Use an exact existing relative file path and document affected route/state, tracking reference and compensating verification in the reason/review record. An expired exception fails closed. Never use a wildcard exception for an entire app. Only DS-001 and DS-002 support scoped waivers in this prototype. GOV-001 and browser-rule exceptions fail closed and require a separately reviewed contract change.
          - code [ref=e394]: approvedBy
          - text: is a declared identity and must be verified through the protected review system.
        - paragraph [ref=e395]: Repeated exceptions indicate a missing pattern or an incorrect rule. Review them with Product Design + Engineering, then revise the contract and add positive/negative examples. Separate a real product violation from a checker false positive. Keep the original mutation results when improving coverage; report survivors and invalid experiments honestly.
        - heading "8. What this contract does not prove" [level=3] [ref=e396]
        - paragraph [ref=e397]: "This lab does not recover CREAO's internal component library, change its production site, execute real integrations, validate live agent runs or prove universal WCAG compliance. Static checks cover documented syntax and files; runtime checks cover explicit route/state fixtures. Screenshots are retained locally and may contain account context: use cropped/redacted copies before public submission. The experiment's evidence is useful because those limits are explicit."
  - alert [ref=e398]
```

# Test source

```ts
  1  | import AxeBuilder from '@axe-core/playwright';
  2  | import { test, expect, type Page, type TestInfo } from '@playwright/test';
  3  | 
  4  | // An automated WCAG scan complements the existing explicit name, focus,
  5  | // interaction and geometry contracts; zero violations is not a full WCAG audit.
  6  | async function scan(page: Page, testInfo: TestInfo, state: string) {
  7  |   await page.evaluate(() => document.fonts.ready);
  8  |   const results = await new AxeBuilder({ page })
  9  |     .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
  10 |     .analyze();
  11 |   // Retain passes, inapplicable and incomplete as well as violations. Incomplete
  12 |   // findings require manual review; never silently turn them into passing rules.
  13 |   await testInfo.attach(`axe-${state}`, {
  14 |     body: JSON.stringify(results, null, 2),
  15 |     contentType: 'application/json',
  16 |   });
  17 |   testInfo.annotations.push({
  18 |     type: 'axe-incomplete',
  19 |     description: JSON.stringify(results.incomplete.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }))),
  20 |   });
> 21 |   expect(results.violations, `Automated WCAG A/AA violations in ${state}`).toEqual([]);
     |                                                                            ^ Error: Automated WCAG A/AA violations in guidelines
  22 | }
  23 | 
  24 | for (const viewport of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
  25 |   test.describe(`axe ${viewport.width}px`, () => {
  26 |     test.use({ viewport });
  27 | 
  28 |     test.beforeEach(async ({ browser }, testInfo) => {
  29 |       testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  30 |       testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  31 |     });
  32 | 
  33 |     test('[A11Y-001] axe Files initial', async ({ page }, testInfo) => {
  34 |       await page.goto('/files');
  35 |       await expect(page.getByTestId('file-item').first()).toBeVisible();
  36 |       await scan(page, testInfo, 'files-initial');
  37 |     });
  38 | 
  39 |     test('[A11Y-001] axe Files empty search', async ({ page }, testInfo) => {
  40 |       await page.goto('/files');
  41 |       await page.getByRole('searchbox', { name: '搜索文件和文件夹' }).fill('no-match-accessibility-4827');
  42 |       await expect(page.getByRole('heading', { name: '没有找到文件', exact: true })).toBeVisible();
  43 |       await expect(page.getByTestId('file-item')).toHaveCount(0);
  44 |       await scan(page, testInfo, 'files-empty-search');
  45 |     });
  46 | 
  47 |     test('[A11Y-001] axe Files folder validation error', async ({ page }, testInfo) => {
  48 |       await page.goto('/files');
  49 |       await page.getByRole('button', { name: '新建文件夹', exact: true }).click();
  50 |       await page.getByRole('button', { name: '创建文件夹', exact: true }).click();
  51 |       await expect(page.getByRole('alert')).toHaveText('请输入文件夹名称。');
  52 |       await expect(page.getByRole('textbox', { name: '文件夹名称', exact: true })).toHaveAttribute('aria-invalid', 'true');
  53 |       await scan(page, testInfo, 'files-folder-error');
  54 |     });
  55 | 
  56 |     test('[A11Y-001] axe Files preview dialog', async ({ page }, testInfo) => {
  57 |       await page.goto('/files');
  58 |       const trigger = page.getByRole('button', { name: '季度研究摘要.md', exact: true });
  59 |       await trigger.click();
  60 |       const dialog = page.getByRole('dialog', { name: '季度研究摘要.md', exact: true });
  61 |       await expect(dialog).toBeVisible();
  62 |       await scan(page, testInfo, 'files-preview');
  63 |       await dialog.getByRole('button', { name: '关闭预览', exact: true }).click();
  64 |       await expect(dialog).not.toBeVisible();
  65 |       await expect(trigger).toBeFocused();
  66 |     });
  67 | 
  68 |     test('[A11Y-001] axe Connectors connected empty', async ({ page }, testInfo) => {
  69 |       await page.goto('/connectors');
  70 |       await page.getByRole('tab', { name: '已连接 (0)', exact: true }).click();
  71 |       await expect(page.getByRole('heading', { name: '暂无已连接的连接器', exact: true })).toBeVisible();
  72 |       await scan(page, testInfo, 'connectors-connected-empty');
  73 |     });
  74 | 
  75 |     test('[A11Y-001] axe Agents empty', async ({ page }, testInfo) => {
  76 |       await page.goto('/agents');
  77 |       await expect(page.getByRole('button', { name: '创建示例智能体', exact: true })).toBeVisible();
  78 |       await scan(page, testInfo, 'agents-empty');
  79 |     });
  80 | 
  81 |     test('[A11Y-001] axe Agents detail', async ({ page }, testInfo) => {
  82 |       await page.goto('/agents');
  83 |       await page.getByRole('button', { name: '创建示例智能体', exact: true }).click();
  84 |       await page.getByRole('button', { name: '查看详情', exact: true }).click();
  85 |       await expect(page.getByRole('heading', { level: 1, name: '研究助手', exact: true })).toBeVisible();
  86 |       await scan(page, testInfo, 'agents-detail');
  87 |     });
  88 | 
  89 |     test('[A11Y-001] axe Guidelines', async ({ page }, testInfo) => {
  90 |       await page.goto('/guidelines');
  91 |       await expect(page.getByRole('heading', { level: 1, name: '设计规范', exact: true })).toBeVisible();
  92 |       await scan(page, testInfo, 'guidelines');
  93 |     });
  94 |   });
  95 | }
  96 | 
```