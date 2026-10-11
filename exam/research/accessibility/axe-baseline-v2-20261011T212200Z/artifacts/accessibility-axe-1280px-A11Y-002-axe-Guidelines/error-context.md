# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accessibility.spec.ts >> axe 1280px >> [A11Y-002] axe Guidelines
- Location: tests/e2e/accessibility.spec.ts:89:9

# Error details

```
Error: Automated WCAG A/AA violations in guidelines

expect(received).toEqual(expected) // deep equality

- Expected  -  1
+ Received  + 52

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
+         "html": "<pre>",
+         "impact": "serious",
+         "none": Array [],
+         "target": Array [
+           "pre",
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
    - complementary [ref=e4]:
      - link "CREAO" [ref=e5] [cursor=pointer]:
        - /url: /files
      - navigation "主要导航" [ref=e6]:
        - link "智能体" [ref=e7] [cursor=pointer]:
          - /url: /agents
        - link "文件" [ref=e11] [cursor=pointer]:
          - /url: /files
        - link "连接器" [ref=e16] [cursor=pointer]:
          - /url: /connectors
        - link "设计规范" [ref=e19] [cursor=pointer]:
          - /url: /guidelines
      - generic [ref=e22]:
        - generic [ref=e23]: C
        - generic [ref=e24]:
          - text: 本地交互原型
          - generic [ref=e25]: CREAO Design Lab
    - main [ref=e26]:
      - generic [ref=e28]:
        - heading "设计规范" [level=1] [ref=e29]
        - paragraph [ref=e30]: 本地适配规范与执行入口。规则是否通过，以实际检查报告为准。
      - article [ref=e31]:
        - heading "CREAO product design contract" [level=2] [ref=e32]
        - paragraph [ref=e33]: "Version: 0.2 (enhanced verification candidate) · 2026-10-11 · Owner: Product Design + Frontend Engineering."
        - paragraph [ref=e34]:
          - text: This is the implementation contract for the
          - strong [ref=e35]: local CREAO Design Lab
          - text: . It is an evidence-informed proposal for CREAO's product layer, not CREAO's private design-system source. Read this file before changing a screen; use
          - link "AGENTS.md" [ref=e36] [cursor=pointer]:
            - /url: /reference?file=AGENTS.md
          - text: for the delivery workflow. The submission-level rationale is in
          - generic [ref=e37]: design-system-guideline.md（工作区附件）
          - text: .
        - heading "1. Source boundaries" [level=3] [ref=e38]
        - table [ref=e39]:
          - rowgroup [ref=e40]:
            - row [ref=e41]:
              - columnheader "Class" [ref=e42]
              - columnheader "Evidence" [ref=e43]
              - columnheader "What it establishes" [ref=e44]
          - rowgroup [ref=e45]:
            - row [ref=e46]:
              - cell "Official" [ref=e47]
              - cell "Widgets documentation, saved Markdown（工作区附件）" [ref=e48]:
                - link "Widgets documentation" [ref=e49] [cursor=pointer]:
                  - /url: https://docs.creao.ai/features/widgets
                - text: ","
                - generic [ref=e50]: saved Markdown（工作区附件）
              - 'cell "Dashboard component categories and composition: a Stack/Grid root, Cards for groups, data/chart/table widgets inside. Warm surfaces, near-black ink and restrained semantic color." [ref=e51]'
            - row [ref=e52]:
              - cell "Observed" [ref=e53]
              - cell "Widgets screenshot（工作区附件）, DOM/CSS snapshot（工作区附件）" [ref=e54]:
                - generic [ref=e55]: Widgets screenshot（工作区附件）
                - text: ","
                - generic [ref=e56]: DOM/CSS snapshot（工作区附件）
              - cell "Actual rendered controls, variable values and parameter labels at one point in time. These do not establish private import paths or supported component APIs." [ref=e57]
            - row [ref=e58]:
              - cell "Observed" [ref=e59]
              - cell "Files mobile（工作区附件）, Files DOM（工作区附件）, connectors empty state（工作区附件）" [ref=e60]:
                - generic [ref=e61]: Files mobile（工作区附件）
                - text: ","
                - generic [ref=e62]: Files DOM（工作区附件）
                - text: ","
                - generic [ref=e63]: connectors empty state（工作区附件）
              - cell "Screen behavior and specific design defects used to define testable rules." [ref=e64]
            - row [ref=e65]:
              - cell "Proposed" [ref=e66]
              - cell "This document, local CSS, local components and checks" [ref=e67]
              - cell "Product-level patterns, responsive decisions, acceptance thresholds and enforcement for this experiment." [ref=e68]
        - paragraph [ref=e69]:
          - text: Public sitemap research found official Widgets documentation, but no indexed full-product
          - code [ref=e70]: design.md
          - text: . The product sitemap returned 403. This is
          - strong [ref=e71]: not evidence that an internal design system does not exist
          - text: . The task states that it does. Replace the local adapter's imports with real approved library imports when integrating in that repository; preserve the contracts below.
        - heading "2. Executable index" [level=3] [ref=e72]
        - paragraph [ref=e73]: These paths are the implementation interface. Do not copy rules into a second divergent checklist.
        - table [ref=e74]:
          - rowgroup [ref=e75]:
            - row [ref=e76]:
              - columnheader "Responsibility" [ref=e77]
              - columnheader "Source of truth" [ref=e78]
          - rowgroup [ref=e79]:
            - row [ref=e80]:
              - cell "Color, typography and dimension variables" [ref=e81]
              - cell [ref=e82]:
                - link "src/styles/tokens.css" [ref=e83] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Ftokens.css
            - row [ref=e84]:
              - cell "Base component appearance" [ref=e85]
              - cell [ref=e86]:
                - link "src/styles/components.css" [ref=e87] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Fcomponents.css
            - row [ref=e88]:
              - cell "Page geometry and responsive rules" [ref=e89]
              - cell [ref=e90]:
                - link "src/styles/layouts.css" [ref=e91] [cursor=pointer]:
                  - /url: /reference?file=src%2Fstyles%2Flayouts.css
            - row [ref=e92]:
              - cell "Approved local primitives" [ref=e93]
              - cell [ref=e94]:
                - link "src/components/ui/" [ref=e95] [cursor=pointer]:
                  - /url: /reference?group=src%2Fcomponents%2Fui%2F
            - row [ref=e96]:
              - cell "Page composition patterns" [ref=e97]
              - cell [ref=e98]:
                - link "src/components/patterns/" [ref=e99] [cursor=pointer]:
                  - /url: /reference?group=src%2Fcomponents%2Fpatterns%2F
            - row [ref=e100]:
              - cell "Destination labels / synthetic data" [ref=e101]
              - cell [ref=e102]:
                - link "src/lib/copy.ts" [ref=e103] [cursor=pointer]:
                  - /url: /reference?file=src%2Flib%2Fcopy.ts
                - text: ","
                - link "src/lib/data.ts" [ref=e104] [cursor=pointer]:
                  - /url: /reference?file=src%2Flib%2Fdata.ts
            - row [ref=e105]:
              - cell "Rule metadata and supported scope" [ref=e106]
              - cell [ref=e107]:
                - link "governance/rules.json" [ref=e108] [cursor=pointer]:
                  - /url: /reference?file=governance%2Frules.json
            - row [ref=e109]:
              - cell "Time-limited exceptions" [ref=e110]
              - cell [ref=e111]:
                - link "governance/exceptions.json" [ref=e112] [cursor=pointer]:
                  - /url: /reference?file=governance%2Fexceptions.json
            - row [ref=e113]:
              - cell "Static enforcement" [ref=e114]
              - cell [ref=e115]:
                - link "scripts/check-design.mjs" [ref=e116] [cursor=pointer]:
                  - /url: /reference?file=scripts%2Fcheck-design.mjs
            - row [ref=e117]:
              - cell "Explicit runtime, accessible-name and layout contracts" [ref=e118]
              - cell [ref=e119]:
                - link "tests/e2e/design.spec.ts" [ref=e120] [cursor=pointer]:
                  - /url: /reference?file=tests%2Fe2e%2Fdesign.spec.ts
            - row [ref=e121]:
              - cell "Full-page axe state scans" [ref=e122]
              - cell "tests/e2e/accessibility.spec.ts（工作区附件）" [ref=e123]
            - row [ref=e125]:
              - cell "Reviewed visual comparisons" [ref=e126]
              - cell "tests/e2e/visual.spec.ts（工作区附件）" [ref=e127]
            - row [ref=e129]:
              - cell "Route/state/viewport coverage inventory" [ref=e130]
              - cell "governance/page-states.json（工作区附件）" [ref=e131]
            - row [ref=e133]:
              - cell "State-inventory schema and evidence validation" [ref=e134]
              - cell "tests/design/page-states.test.mjs（工作区附件）" [ref=e135]
            - row [ref=e137]:
              - cell "Mutation fixtures and results" [ref=e138]
              - cell [ref=e139]:
                - link "tests/mutations/" [ref=e140] [cursor=pointer]:
                  - /url: /reference?group=tests%2Fmutations%2F
                - text: "; generated evidence:"
                - code [ref=e141]: reports/
        - paragraph [ref=e142]: The registry identifies concrete checker entrypoints. The package scripts are the command interface. A broken index, unknown rule, missing entrypoint or invalid exception fails GOV-001. Directory links above are navigation aids, not a claim that every directory has an independent check.
        - paragraph [ref=e143]:
          - text: The local adapter exports
          - code [ref=e144]: Button
          - text: ","
          - code [ref=e145]: Input
          - text: ", and"
          - code [ref=e146]: Icon
          - text: from
          - code [ref=e147]: src/components/ui/index.tsx
          - text: .
          - code [ref=e148]: Button
          - text: accepts native button props and
          - code [ref=e149]: variant="primary" | "secondary" | "ghost"
          - text: ;
          - code [ref=e150]: Input
          - text: accepts native input props. Patterns are
          - code [ref=e151]: "PageHeader({ title, description?, actions? })"
          - text: ","
          - code [ref=e152]: "EmptyState({ title, description, action: { label, onClick }, icon? })"
          - text: ", and"
          - code [ref=e153]: "Shell({ children })"
          - text: . Read their TypeScript definitions before changing usage; these names are local APIs, not claimed CREAO imports.
        - heading "3. Preserve the existing visual language" [level=3] [ref=e154]
        - paragraph [ref=e155]:
          - text: The following values were observed on
          - code [ref=e156]: /widgets
          - text: ; they are evidence, not a new brand palette. Local tokens may use a shorter semantic alias but must record that mapping in
          - code [ref=e157]: tokens.css
          - text: .
        - table [ref=e158]:
          - rowgroup [ref=e159]:
            - row [ref=e160]:
              - columnheader "Observed CSS variable" [ref=e161]
              - columnheader "Observed value" [ref=e162]
              - columnheader "Intended use in this prototype" [ref=e163]
          - rowgroup [ref=e164]:
            - row [ref=e165]:
              - cell [ref=e166]:
                - code [ref=e167]: "--color-background"
              - cell [ref=e168]:
                - code [ref=e169]: "#f8f6f3"
              - cell "Page canvas" [ref=e170]
            - row [ref=e171]:
              - cell [ref=e172]:
                - code [ref=e173]: "--color-card"
                - text: /
                - code [ref=e174]: "--color-surface"
              - cell [ref=e175]:
                - code [ref=e176]: "#fefdfb"
              - cell "Elevated content surface" [ref=e177]
            - row [ref=e178]:
              - cell [ref=e179]:
                - code [ref=e180]: "--color-chrome"
              - cell [ref=e181]:
                - code [ref=e182]: "#f4f1ed"
              - cell "App shell" [ref=e183]
            - row [ref=e184]:
              - cell [ref=e185]:
                - code [ref=e186]: "--color-surface-alt"
              - cell [ref=e187]:
                - code [ref=e188]: "#f0ede8"
              - cell "Subtle grouped surface" [ref=e189]
            - row [ref=e190]:
              - cell [ref=e191]:
                - code [ref=e192]: "--color-foreground"
                - text: /
                - code [ref=e193]: "--color-primary"
              - cell [ref=e194]:
                - code [ref=e195]: "#16181a"
              - cell "Ink and primary action" [ref=e196]
            - row [ref=e197]:
              - cell [ref=e198]:
                - code [ref=e199]: "--color-primary-foreground"
              - cell [ref=e200]:
                - code [ref=e201]: "#f3ecd8"
              - cell "Text on primary action" [ref=e202]
            - row [ref=e203]:
              - cell [ref=e204]:
                - code [ref=e205]: "--color-border"
              - cell [ref=e206]:
                - code [ref=e207]: "#e6e2db"
              - cell "Hairline structural separator" [ref=e208]
            - row [ref=e209]:
              - cell [ref=e210]:
                - code [ref=e211]: "--color-control-border"
              - cell [ref=e212]:
                - code [ref=e213]: "#ebe7e2"
              - cell "Observed control-border token; does not by itself prove sufficient contrast" [ref=e214]
            - row [ref=e215]:
              - cell [ref=e216]:
                - code [ref=e217]: "--color-oxblood"
              - cell [ref=e218]:
                - code [ref=e219]: "#6e2f2c"
              - cell "Negative / signature accent; never the sole error signal" [ref=e220]
            - row [ref=e221]:
              - cell [ref=e222]:
                - code [ref=e223]: "--spacing"
              - cell [ref=e224]:
                - code [ref=e225]: .25rem
              - cell "Observed scale base" [ref=e226]
            - row [ref=e227]:
              - cell [ref=e228]:
                - code [ref=e229]: "--radius"
              - cell [ref=e230]:
                - code [ref=e231]: .375rem
              - cell "Observed generic radius; do not infer all widgets must have this radius" [ref=e232]
        - paragraph [ref=e233]:
          - text: Observed font stacks start with Instrument Sans for UI, DM Mono for data, JetBrains Mono for code, and EB Garamond for serif. The prototype can use available system fallbacks; do not silently download or claim the same licensed font rendering. Any extra tokens, including positive-state color, focus ring, spacing steps, width limits and mobile breakpoints, are
          - strong [ref=e234]: local proposals
          - text: documented in CSS. Verify contrast on actual text/control pairs; the screenshot alone is insufficient.
        - paragraph [ref=e235]: Official docs describe sharp corners; the observed UI also exposes several radius variables and uses rounded controls. Preserve that difference. Do not derive a universal zero-radius rule from a dashboard paragraph or copy a generic radius to every product surface.
        - heading "4. Choose a page pattern before writing JSX" [level=3] [ref=e236]
        - paragraph [ref=e237]: All top-level routes use an app shell with persistent desktop navigation, a named main region, and a compact navigation control on narrow screens. Put the page identity and highest-priority page action together; put filters beneath; put content and its states in one stable region. Route titles use PageHeader. Inline previews and configuration panels are subordinate to the page identity.
        - table [ref=e238]:
          - rowgroup [ref=e239]:
            - row [ref=e240]:
              - columnheader "Pattern" [ref=e241]
              - columnheader "Use when" [ref=e242]
              - columnheader "Required order / composition" [ref=e243]
              - columnheader "Canonical or experimental" [ref=e244]
          - rowgroup [ref=e245]:
            - row [ref=e246]:
              - cell "Collection" [ref=e247]
              - cell "Files, connectors, agents, skills" [ref=e248]
              - cell "PageHeader → search/filter/view controls → result summary where meaningful → collection OR empty/error/loading state" [ref=e249]
              - cell [ref=e250]:
                - text: Canonical; demonstrated in
                - code [ref=e251]: /files
                - text: ","
                - code [ref=e252]: /connectors
                - text: ","
                - code [ref=e253]: /agents
            - row [ref=e254]:
              - cell "Detail / preview" [ref=e255]
              - cell "Inspect a selected file or agent without losing list context" [ref=e256]
              - cell "Identity → metadata/status → content → contextual actions; provide close/back and restore focus" [ref=e257]
              - cell "Canonical; file preview demonstrated" [ref=e258]
            - row [ref=e259]:
              - cell "Chat workbench" [ref=e260]
              - cell "User gives intent and monitors work" [ref=e261]
              - cell "Conversation identity → ordered messages/results → explicit run/approval state → composer with visible authority and attachment controls" [ref=e262]
              - cell "Canonical proposal; not implemented as a full runtime in this lab" [ref=e263]
            - row [ref=e264]:
              - cell "Configuration" [ref=e265]
              - cell "Connection setup, agent defaults, schedule" [ref=e266]
              - cell "Identity/back → explanation/scope → labeled fields in logical sections → validation → one save/confirm action" [ref=e267]
              - cell "Canonical proposal; real Slack screen informs it; OAuth not executed in lab" [ref=e268]
            - row [ref=e269]:
              - cell "Approval / run review" [ref=e270]
              - cell "Agent needs a decision before an external effect" [ref=e271]
              - cell "Actor and operation → target/scope/consequence → approve and cancel → pending/result evidence" [ref=e272]
              - cell "Canonical proposal; test before production adoption; not proven by this lab" [ref=e273]
            - row [ref=e274]:
              - cell "Dashboard" [ref=e275]
              - cell "Agent-generated structured result" [ref=e276]
              - cell "Stack/Grid root → Cards/group headings → data/charts/tables; keep responsive reading order" [ref=e277]
              - cell "Official widget composition; local adapter does not implement the entire widget catalog" [ref=e278]
        - paragraph [ref=e279]: Do not choose a new page shell for a single feature. A new pattern requires a screenshot with representative content and states, a reason existing patterns fail, Product Design approval, and an implementation/test mapping. One-off promotional or immersive views can be scoped exceptions rather than silently becoming canon.
        - heading "Collection and detail decisions" [level=4] [ref=e280]
        - list [ref=e281]:
          - listitem [ref=e282]: Use a list when users compare repeated fields; use cards when previews or richer descriptions dominate. A view switch must expose selected state and keep search/filter state.
          - listitem [ref=e283]: A page can have multiple actions, but only one filled, visually dominant page-level primary action. Destructive actions belong near the affected object, with explicit consequences before an irreversible effect.
          - listitem [ref=e284]: A preview must not look like a new top-level page unless the URL and navigation context also change. Closing it returns focus to the trigger. Escape and a named close control must work.
          - listitem [ref=e285]: In a collection, loading, initial empty, filtered empty, permission failure and load error are different states. Never reuse “No files” for a failed request.
        - heading "Responsive decisions" [level=4] [ref=e286]
        - paragraph [ref=e287]:
          - text: The lab's navigation compact breakpoint is 760 CSS px; file collections switch to labeled entries at 900 CSS px in
          - code [ref=e288]: layouts.css
          - text: after an 800px overflow was found during visual review; navigation width is
          - code [ref=e289]: "--sidebar-width: 248px"
          - text: and desktop page padding is
          - code [ref=e290]: "--page-padding: 32px"
          - text: in
          - code [ref=e291]: tokens.css
          - text: . These are proposed implementation values, not observed official policy. Automated layout checks use 320, 390, 800 and 1280 CSS px widths (900px height). The live-product audit captured 390 × 844; also inspect this viewport and 320 CSS px manually before production integration.
        - paragraph [ref=e292]:
          - text: "At compact widths, convert file rows to labeled entries: file name first, then each metadata label/value pair. Remove the desktop header when its columns no longer align. Keep names discoverable through the preview or accessible name. Do not leave a narrow desktop header above a stacked list. Controls may hide visible text only if their accessible names remain. Do not use global"
          - code [ref=e293]: "overflow-x: hidden"
          - text: to conceal an overflow bug. A genuinely two-dimensional chart/table can have a labeled local scroll region; the whole page must not require horizontal navigation to reach core actions.
        - heading "5. Rules and failure contracts" [level=3] [ref=e294]
        - paragraph [ref=e295]:
          - text: All ten rules are mandatory within their declared scopes. The original eight remain unchanged; A11Y-002 and VISUAL-001 add independent checks.
          - code [ref=e296]: block
          - text: means the change cannot become a release candidate without a valid scoped exception. Human judgments are explicitly distinguished from automated checks.
        - table [ref=e297]:
          - rowgroup [ref=e298]:
            - row [ref=e299]:
              - columnheader "Rule" [ref=e300]
              - columnheader "Pass contract" [ref=e301]
              - columnheader "Fails when" [ref=e302]
              - columnheader "Enforcement / boundary" [ref=e303]
          - rowgroup [ref=e304]:
            - row [ref=e305]:
              - cell [ref=e306]:
                - strong [ref=e307]: DS-001
                - text: Token use
              - cell [ref=e308]:
                - text: Governed styles use registered semantic color variables. Literal palette values occur only in
                - code [ref=e309]: tokens.css
                - text: .
              - cell "A page/component stylesheet adds an unregistered literal color or references an unknown governed token." [ref=e310]
              - 'cell "CSS AST/static checker. A token can still be used with the wrong meaning: reviewer checks semantics and contrast." [ref=e311]'
            - row [ref=e312]:
              - cell [ref=e313]:
                - strong [ref=e314]: DS-002
                - text: Primitive reuse
              - cell "Feature JSX composes approved local UI primitives; actual native control implementations stay inside the UI boundary." [ref=e315]
              - cell [ref=e316]:
                - text: Governed feature/pattern JSX directly creates
                - code [ref=e317]: button
                - text: ","
                - code [ref=e318]: input
                - text: ","
                - code [ref=e319]: select
                - text: or
                - code [ref=e320]: textarea
                - text: ", including lexically resolved const aliases of those string tags."
              - cell "TS/JSX AST/static checker. It resolves static const string aliases with TypeScript symbols, but does not resolve import provenance, custom wrappers, dynamic aliases or factories; approved library provenance still requires review." [ref=e321]
            - row [ref=e322]:
              - cell [ref=e323]:
                - strong [ref=e324]: LAY-001
                - text: Page identity
              - cell [ref=e325]:
                - text: Each governed route has one visible top-level
                - code [ref=e326]: h1
                - text: within its main region, matching that route's identity. Nested preview/section headings are subordinate.
              - cell "Missing, duplicate, hidden or incorrect main title. A large button/span styled as a heading does not qualify." [ref=e327]
              - cell "DOM test on every governed route at desktop and compact sizes. Correct overall information architecture remains a design review item." [ref=e328]
            - row [ref=e329]:
              - cell [ref=e330]:
                - strong [ref=e331]: A11Y-001
                - text: Named controls
              - cell "Each operable visible button/input/select/link has a non-empty accessible name in the tested states and viewports. Icon controls retain names when text hides." [ref=e332]
              - cell "Name disappears, label is missing, or a control has no usable identifier." [ref=e333]
              - cell "Runtime accessible-name assertions. A non-empty but misleading name can pass; reviewer must assess meaning, focus order and keyboard operation." [ref=e334]
            - row [ref=e335]:
              - cell [ref=e336]:
                - strong [ref=e337]: STATE-001
                - text: Recovery
              - cell "Recoverable empty states explain why and offer an in-state action that actually recovers. Initial empty → create/connect; filtered empty → clear relevant filters; error → retry/appropriate help." [ref=e338]
              - cell "Recovery is absent, inert or leads to the wrong state. A separate distant tab alone is insufficient." [ref=e339]
              - cell "Browser interaction fixtures for known empty states and post-action results. Production network/error states need adapter tests beyond the local fixture." [ref=e340]
            - row [ref=e341]:
              - cell [ref=e342]:
                - strong [ref=e343]: NAV-001
                - text: Destination language
              - cell "Guidance and controls derive destination names from the same label source; actions reveal that destination." [ref=e344]
              - cell "“Available” is referenced when the actual tab is “Connectable”, or the action activates another tab." [ref=e345]
              - cell "Browser assertions against the canonical Chinese destination name, guidance and actual tab/region. Shared-source reuse is a source-review requirement, not import analysis. Localization requires the same check for each supported locale." [ref=e346]
            - row [ref=e347]:
              - cell [ref=e348]:
                - strong [ref=e349]: RESP-001
                - text: Field integrity
              - cell "At tested compact widths, every metadata value stays associated with its visible label, controls stay reachable and key rectangles do not overlap/clip." [ref=e350]
              - cell "Desktop headers no longer correspond to stacked values, or essential content overlaps/offscreen." [ref=e351]
              - cell "Browser geometry and label/structure assertions plus screenshot review. No claim of full visual correctness or every-device coverage." [ref=e352]
            - row [ref=e353]:
              - cell [ref=e354]:
                - strong [ref=e355]: GOV-001
                - text: Contract integrity
              - cell "Registry, document/index links, checker paths and exception records are valid and current. Rule/check changes have owner review." [ref=e356]
              - cell "Referenced files are missing, rule IDs drift, or exception records are malformed/expired/outside their declared scope." [ref=e357]
              - cell "Static validation can check records, not the identity of an approver. External required checks and ownership enforce review." [ref=e358]
            - row [ref=e359]:
              - cell [ref=e360]:
                - strong [ref=e361]: A11Y-002
                - text: Axe state scans
              - cell "The 16 explicit full-page scans have zero WCAG 2 A/AA and 2.1 A/AA tagged axe violations; incomplete results remain visible for manual review." [ref=e362]
              - cell "Any axe violation, regardless of severity. Setup/navigation/browser errors fail execution but are not reported as design-rule detections." [ref=e363]
              - cell "Eight states at 1280×900 and 390×844. No include/exclude/disabled-rule shortcuts. Does not establish complete accessibility or WCAG conformance." [ref=e364]
            - row [ref=e365]:
              - cell [ref=e366]:
                - strong [ref=e367]: VISUAL-001
                - text: Reviewed screenshots
              - cell "The three explicit screenshots match a reviewed baseline for the actual OS/architecture/release/browser namespace." [ref=e368]
              - cell "Missing baseline, environment mismatch, or any differing pixel beyond the per-pixel color threshold (0.2), because allowed differing pixels = 0." [ref=e369]
              - cell "Files list at 1280×900 and 390×900; Connectors connected-empty at 1280×900. Legitimate changes can also fail and need review; a green image comparison is not a usability proof." [ref=e370]
        - paragraph [ref=e371]:
          - text: Automated route coverage is
          - code [ref=e372]: /files
          - text: ","
          - code [ref=e373]: /connectors
          - text: ","
          - code [ref=e374]: /agents
          - text: and
          - code [ref=e375]: /guidelines
          - text: ", as recorded in the registry. Future routes and unrepresented dynamic states still require review or new fixtures. DS-001 covers source CSS only; inline styles, CSS-in-JS, dynamically generated styles, external CSS and HTML color attributes are outside its current checker scope. Semantic CSS keywords such as"
          - code [ref=e376]: transparent
          - text: ","
          - code [ref=e377]: currentColor
          - text: and
          - code [ref=e378]: inherit
          - text: are allowed; they do not define new palette values. Adding a privileged UI implementation or changing token authority requires owner review even if the static check passes.
        - heading "State recipes" [level=4] [ref=e379]
        - table [ref=e380]:
          - rowgroup [ref=e381]:
            - row [ref=e382]:
              - columnheader "Situation" [ref=e383]
              - columnheader "Required message" [ref=e384]
              - columnheader "Next action" [ref=e385]
              - columnheader "Result to assert" [ref=e386]
          - rowgroup [ref=e387]:
            - row [ref=e388]:
              - cell "No connected services" [ref=e389]
              - cell "“No connected services” + why connecting helps" [ref=e390]
              - cell "“Browse connectable services”" [ref=e391]
              - cell "Connectable tab is selected and eligible services appear" [ref=e392]
            - row [ref=e393]:
              - cell "File search finds nothing" [ref=e394]
              - cell "State that current query/filters matched nothing" [ref=e395]
              - cell "“Clear search” or “Clear filters”" [ref=e396]
              - cell "Query/filter resets and seeded files reappear" [ref=e397]
            - row [ref=e398]:
              - cell "No agents yet" [ref=e399]
              - cell "Explain repeatable work and how creation starts" [ref=e400]
              - cell "“Create agent” / local example action" [ref=e401]
              - cell "Documented create flow opens; lab must identify it as a simulation" [ref=e402]
            - row [ref=e403]:
              - cell "Load error" [ref=e404]
              - cell "Distinguish failed loading from no data" [ref=e405]
              - cell "Retry, or permission-specific guidance" [ref=e406]
              - cell "Retry is attempted / permission destination is correct" [ref=e407]
            - row [ref=e408]:
              - cell "Agent running / awaiting approval" [ref=e409]
              - cell "Text status, next expected event and available controls" [ref=e410]
              - cell "View progress / make an explicit decision" [ref=e411]
              - cell "Status transitions from actual response, never inferred from animation alone" [ref=e412]
        - heading "6. Before a change ships" [level=3] [ref=e413]
        - list [ref=e414]:
          - listitem [ref=e415]: Declare the pattern, affected route/state/viewports and applicable rule IDs in the change description.
          - listitem [ref=e416]: Read component implementation and CSS; reuse existing variants before adding styles. Register genuinely new tokens with purpose and provenance.
          - listitem [ref=e417]: Implement the behavior and fixtures. Run the package's type, lint, static design, production build and browser checks. Run mutation checks when changing rules, checkers, shared components or layout contracts.
          - listitem [ref=e418]: Inspect desktop and compact screenshots and perform keyboard/focus checks for changed interactions. A green machine check does not waive human design judgment.
          - listitem [ref=e419]: Attach command results, screenshots and any exception ID. Record failures/skips as such; do not silently regenerate snapshots or edit tests just to accept changed behavior.
          - listitem [ref=e420]: Owner review covers pattern choice, semantics, hierarchy, contrast and changes to governance assets. CI must execute against the candidate commit; CD accepts only an artifact from that successful candidate, followed by deployment smoke checks.
        - paragraph [ref=e421]: "From this directory, the concrete gate commands are:"
        - code [ref=e423]: "npm ci npm run typecheck npm run lint npm run check:design npm run test:design npm run build npx playwright install chromium PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e npm run test:mutations # A separate required visual check needs the exact reviewed environment namespace: VISUAL_ENV=\"$REVIEWED_VISUAL_ENV\" PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual"
        - paragraph [ref=e424]:
          - text: Use
          - code [ref=e425]: npm run dev -- --port 3100
          - text: for interactive local inspection. Read the test runner configuration for server startup/port ownership; do not launch competing servers on the same port. The listed commands describe the required gate, not a claim that a run has succeeded. Actual receipts live under
          - code [ref=e426]: reports/
          - text: and are summarized in the compliance audit.
        - heading "State coverage is a declared, testable inventory" [level=4] [ref=e427]
        - paragraph [ref=e428]:
          - code [ref=e429]: governance/page-states.json
          - text: "catalogs six source routes and 31 states: 22 implemented states and nine explicitly unimplemented loading/network/permission states. A row is an inventory entry, not proof that every assertion passed. Keep implementation, check implementation, execution, exact test title, executed viewport and evidence separate. An implemented test with no receipt stays"
          - code [ref=e430]: notVerified
          - text: ; a future check stays
          - code [ref=e431]: planned
          - text: ; unsupported states stay
          - code [ref=e432]: notImplemented
          - text: /
          - code [ref=e433]: notApplicable
          - text: . Do not inflate the denominator by counting planned checks as executed.
        - paragraph [ref=e434]: The catalog validator discovers App Router page files and rejects uncatalogued routes, duplicate states, unknown rules, invalid setup/scope/viewports, missing implemented check paths, and pass claims without evidence. Browser receipt claims must match the exact test title and expected number of runs; axe's repeated title requires both viewport runs. Existing 22-test behavior receipts are retained as historical evidence, not as proof that a later changed candidate was tested. State completeness and whether a test fully asserts its declared semantics still require review.
        - paragraph [ref=e435]:
          - text: "The 16 axe scans cover eight states only: Files initial list, no search results, empty-folder validation and preview dialog; Connectors connected-empty; Agents initial empty and detail; Guidelines. Their 390×844 viewport is distinct from the behavior suite's 390×900. Full axe output preserves"
          - code [ref=e436]: violations
          - text: ","
          - code [ref=e437]: incomplete
          - text: ","
          - code [ref=e438]: passes
          - text: and
          - code [ref=e439]: inapplicable
          - text: . Zero violations passes the automated gate; unresolved incomplete findings require an explicit human disposition before release.
        - heading "Visual baseline review and environment policy" [level=4] [ref=e440]
        - paragraph [ref=e441]:
          - text: The visual suite is separate (
          - code [ref=e442]: npm run test:visual
          - text: ), never silently skipped inside an ordinary gate.
          - code [ref=e443]: npm run test:e2e
          - text: covers 22 existing contracts plus 16 axe scans; this test count is planned configuration, not a claim of successful execution.
          - code [ref=e444]: npm run test:a11y
          - text: can isolate the axe scans during investigation.
        - paragraph [ref=e445]:
          - text: Set
          - code [ref=e446]: VISUAL_ENV
          - text: to the verified
          - code [ref=e447]: "${platform}-${architecture}-${OS release}-chromium-${browser version}"
          - text: namespace, for example the local Mac candidate environment
          - code [ref=e448]: darwin-arm64-25.6.0-chromium-154.0.8037.98
          - text: . The test recomputes and checks that string. System Chrome can be selected locally with
          - code [ref=e449]: PW_CHANNEL=chrome
          - text: "; CI defaults to Playwright's matching Chromium. This distinction must appear in the receipt. A Linux run cannot reuse a Mac baseline: absent Linux images must fail, then be generated and reviewed in the pinned Linux environment. Environment names do not prove identical fonts; pin the runner image, fonts, dependencies and browser and retain their versions."
        - paragraph [ref=e450]:
          - text: Snapshots use synthetic fixed data, a fixed clock,
          - code [ref=e451]: zh-CN
          - text: ", the Los Angeles time zone, DPR 1, light mode, reduced motion, disabled screenshot animations, a hidden caret, CSS scale and full-page capture."
          - code [ref=e452]: "threshold: 0.2"
          - text: is a per-pixel color tolerance;
          - code [ref=e453]: "maxDiffPixels: 0"
          - text: means no pixels beyond that tolerance are accepted. Keep expected/actual/diff images and traces with the run.
        - paragraph [ref=e454]:
          - text: Missing-baseline runs fail closed. Generating candidates with
          - code [ref=e455]: npm run test:visual -- --update-snapshots
          - text: is a separate authorized review operation, never the PR/CI success path. Product Design plus a frontend owner inspect candidate/previous/diff images and justify intended UI changes. Record that review, commit only the accepted platform-specific images, then rerun normal comparison without update flags. Legitimate new features may require this workflow; do not broaden thresholds or overwrite images automatically to force green. Review ownership must be enforced outside author-editable files.
        - paragraph [ref=e456]:
          - text: The prototype demonstrates a local gate. GitHub required checks, CODEOWNERS enforcement, protected environments and deployment receipts must be configured separately.
          - code [ref=e457]: AGENTS.md
          - text: instructs cooperative agents; it is not an access-control boundary. A contributor able to edit every checker and CI policy can bypass local restrictions.
        - heading "7. Exceptions and evolution" [level=3] [ref=e458]
        - paragraph [ref=e459]:
          - code [ref=e460]: exceptions.json
          - text: has the root shape
          - code [ref=e461]: "{ \"exceptions\": [] }"
          - text: . Each record requires exactly
          - code [ref=e462]: id
          - text: ","
          - code [ref=e463]: ruleId
          - text: ","
          - code [ref=e464]: path
          - text: ","
          - code [ref=e465]: reason
          - text: ","
          - code [ref=e466]: owner
          - text: ","
          - code [ref=e467]: approvedBy
          - text: ", and"
          - code [ref=e468]: expires
          - text: (YYYY-MM-DD; current implementation expires at the end of that UTC date). Use an exact existing relative file path and document affected route/state, tracking reference and compensating verification in the reason/review record. An expired exception fails closed. Never use a wildcard exception for an entire app. Only DS-001 and DS-002 support scoped waivers in this prototype. GOV-001 and browser-rule exceptions fail closed and require a separately reviewed contract change.
          - code [ref=e469]: approvedBy
          - text: is a declared identity and must be verified through the protected review system.
        - paragraph [ref=e470]: Repeated exceptions indicate a missing pattern or an incorrect rule. Review them with Product Design + Engineering, then revise the contract and add positive/negative examples. Separate a real product violation from a checker false positive. Keep the original mutation results when improving coverage; report survivors and invalid experiments honestly.
        - heading "8. What this contract does not prove" [level=3] [ref=e471]
        - paragraph [ref=e472]: "This lab does not recover CREAO's internal component library, change its production site, execute real integrations, validate live agent runs or prove universal WCAG compliance. Static checks cover documented syntax and files; runtime checks cover explicit route/state fixtures. Screenshots are retained locally and may contain account context: use cropped/redacted copies before public submission. The experiment's evidence is useful because those limits are explicit."
  - alert [ref=e473]
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
  33 |     test('[A11Y-002] axe Files initial', async ({ page }, testInfo) => {
  34 |       await page.goto('/files');
  35 |       await expect(page.getByTestId('file-item').first()).toBeVisible();
  36 |       await scan(page, testInfo, 'files-initial');
  37 |     });
  38 | 
  39 |     test('[A11Y-002] axe Files empty search', async ({ page }, testInfo) => {
  40 |       await page.goto('/files');
  41 |       await page.getByRole('searchbox', { name: '搜索文件和文件夹' }).fill('no-match-accessibility-4827');
  42 |       await expect(page.getByRole('heading', { name: '没有找到文件', exact: true })).toBeVisible();
  43 |       await expect(page.getByTestId('file-item')).toHaveCount(0);
  44 |       await scan(page, testInfo, 'files-empty-search');
  45 |     });
  46 | 
  47 |     test('[A11Y-002] axe Files folder validation error', async ({ page }, testInfo) => {
  48 |       await page.goto('/files');
  49 |       await page.getByRole('button', { name: '新建文件夹', exact: true }).click();
  50 |       await page.getByRole('button', { name: '创建文件夹', exact: true }).click();
  51 |       await expect(page.getByRole('main').getByRole('alert')).toHaveText('请输入文件夹名称。');
  52 |       await expect(page.getByRole('textbox', { name: '文件夹名称', exact: true })).toHaveAttribute('aria-invalid', 'true');
  53 |       await scan(page, testInfo, 'files-folder-error');
  54 |     });
  55 | 
  56 |     test('[A11Y-002] axe Files preview dialog', async ({ page }, testInfo) => {
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
  68 |     test('[A11Y-002] axe Connectors connected empty', async ({ page }, testInfo) => {
  69 |       await page.goto('/connectors');
  70 |       await page.getByRole('tab', { name: '已连接 (0)', exact: true }).click();
  71 |       await expect(page.getByRole('heading', { name: '暂无已连接的连接器', exact: true })).toBeVisible();
  72 |       await scan(page, testInfo, 'connectors-connected-empty');
  73 |     });
  74 | 
  75 |     test('[A11Y-002] axe Agents empty', async ({ page }, testInfo) => {
  76 |       await page.goto('/agents');
  77 |       await expect(page.getByRole('button', { name: '创建示例智能体', exact: true })).toBeVisible();
  78 |       await scan(page, testInfo, 'agents-empty');
  79 |     });
  80 | 
  81 |     test('[A11Y-002] axe Agents detail', async ({ page }, testInfo) => {
  82 |       await page.goto('/agents');
  83 |       await page.getByRole('button', { name: '创建示例智能体', exact: true }).click();
  84 |       await page.getByRole('button', { name: '查看详情', exact: true }).click();
  85 |       await expect(page.getByRole('heading', { level: 1, name: '研究助手', exact: true })).toBeVisible();
  86 |       await scan(page, testInfo, 'agents-detail');
  87 |     });
  88 | 
  89 |     test('[A11Y-002] axe Guidelines', async ({ page }, testInfo) => {
  90 |       await page.goto('/guidelines');
  91 |       await expect(page.getByRole('heading', { level: 1, name: '设计规范', exact: true })).toBeVisible();
  92 |       await scan(page, testInfo, 'guidelines');
  93 |     });
  94 |   });
  95 | }
  96 | 
```