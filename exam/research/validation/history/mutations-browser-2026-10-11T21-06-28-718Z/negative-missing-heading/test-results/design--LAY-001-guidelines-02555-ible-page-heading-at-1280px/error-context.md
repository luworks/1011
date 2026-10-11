# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: design.spec.ts >> [LAY-001] /guidelines one visible page heading at 1280px
- Location: tests/e2e/design.spec.ts:18:9

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  getByRole('main').getByRole('heading', { level: 1 })
Expected: 1
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" getByRole('main').getByRole('heading', { level: 1 }) with timeout 5000ms
  - waiting for getByRole('main').getByRole('heading', { level: 1 })
    14 × locator resolved to 0 elements
       - unexpected value "0"

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
        - heading "设计规范" [level=2] [ref=e29]
        - paragraph [ref=e30]: 本地适配规范与执行入口。规则是否通过，以实际检查报告为准。
      - article [ref=e31]:
        - heading "CREAO product design contract" [level=2] [ref=e32]
        - paragraph [ref=e33]: "Version: 0.1 · 2026-10-11 · Owner: Product Design + Frontend Engineering."
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
              - cell "Runtime, accessibility and layout enforcement" [ref=e118]
              - cell [ref=e119]:
                - link "tests/e2e/design.spec.ts" [ref=e120] [cursor=pointer]:
                  - /url: /reference?file=tests%2Fe2e%2Fdesign.spec.ts
            - row [ref=e121]:
              - cell "Mutation fixtures and results" [ref=e122]
              - cell [ref=e123]:
                - link "tests/mutations/" [ref=e124] [cursor=pointer]:
                  - /url: /reference?group=tests%2Fmutations%2F
                - text: "; generated evidence:"
                - code [ref=e125]: reports/
        - paragraph [ref=e126]: The registry identifies concrete checker entrypoints. The package scripts are the command interface. A broken index, unknown rule, missing entrypoint or invalid exception fails GOV-001. Directory links above are navigation aids, not a claim that every directory has an independent check.
        - paragraph [ref=e127]:
          - text: The local adapter exports
          - code [ref=e128]: Button
          - text: ","
          - code [ref=e129]: Input
          - text: ", and"
          - code [ref=e130]: Icon
          - text: from
          - code [ref=e131]: src/components/ui/index.tsx
          - text: .
          - code [ref=e132]: Button
          - text: accepts native button props and
          - code [ref=e133]: variant="primary" | "secondary" | "ghost"
          - text: ;
          - code [ref=e134]: Input
          - text: accepts native input props. Patterns are
          - code [ref=e135]: "PageHeader({ title, description?, actions? })"
          - text: ","
          - code [ref=e136]: "EmptyState({ title, description, action: { label, onClick }, icon? })"
          - text: ", and"
          - code [ref=e137]: "Shell({ children })"
          - text: . Read their TypeScript definitions before changing usage; these names are local APIs, not claimed CREAO imports.
        - heading "3. Preserve the existing visual language" [level=3] [ref=e138]
        - paragraph [ref=e139]:
          - text: The following values were observed on
          - code [ref=e140]: /widgets
          - text: ; they are evidence, not a new brand palette. Local tokens may use a shorter semantic alias but must record that mapping in
          - code [ref=e141]: tokens.css
          - text: .
        - table [ref=e142]:
          - rowgroup [ref=e143]:
            - row [ref=e144]:
              - columnheader "Observed CSS variable" [ref=e145]
              - columnheader "Observed value" [ref=e146]
              - columnheader "Intended use in this prototype" [ref=e147]
          - rowgroup [ref=e148]:
            - row [ref=e149]:
              - cell [ref=e150]:
                - code [ref=e151]: "--color-background"
              - cell [ref=e152]:
                - code [ref=e153]: "#f8f6f3"
              - cell "Page canvas" [ref=e154]
            - row [ref=e155]:
              - cell [ref=e156]:
                - code [ref=e157]: "--color-card"
                - text: /
                - code [ref=e158]: "--color-surface"
              - cell [ref=e159]:
                - code [ref=e160]: "#fefdfb"
              - cell "Elevated content surface" [ref=e161]
            - row [ref=e162]:
              - cell [ref=e163]:
                - code [ref=e164]: "--color-chrome"
              - cell [ref=e165]:
                - code [ref=e166]: "#f4f1ed"
              - cell "App shell" [ref=e167]
            - row [ref=e168]:
              - cell [ref=e169]:
                - code [ref=e170]: "--color-surface-alt"
              - cell [ref=e171]:
                - code [ref=e172]: "#f0ede8"
              - cell "Subtle grouped surface" [ref=e173]
            - row [ref=e174]:
              - cell [ref=e175]:
                - code [ref=e176]: "--color-foreground"
                - text: /
                - code [ref=e177]: "--color-primary"
              - cell [ref=e178]:
                - code [ref=e179]: "#16181a"
              - cell "Ink and primary action" [ref=e180]
            - row [ref=e181]:
              - cell [ref=e182]:
                - code [ref=e183]: "--color-primary-foreground"
              - cell [ref=e184]:
                - code [ref=e185]: "#f3ecd8"
              - cell "Text on primary action" [ref=e186]
            - row [ref=e187]:
              - cell [ref=e188]:
                - code [ref=e189]: "--color-border"
              - cell [ref=e190]:
                - code [ref=e191]: "#e6e2db"
              - cell "Hairline structural separator" [ref=e192]
            - row [ref=e193]:
              - cell [ref=e194]:
                - code [ref=e195]: "--color-control-border"
              - cell [ref=e196]:
                - code [ref=e197]: "#ebe7e2"
              - cell "Observed control-border token; does not by itself prove sufficient contrast" [ref=e198]
            - row [ref=e199]:
              - cell [ref=e200]:
                - code [ref=e201]: "--color-oxblood"
              - cell [ref=e202]:
                - code [ref=e203]: "#6e2f2c"
              - cell "Negative / signature accent; never the sole error signal" [ref=e204]
            - row [ref=e205]:
              - cell [ref=e206]:
                - code [ref=e207]: "--spacing"
              - cell [ref=e208]:
                - code [ref=e209]: .25rem
              - cell "Observed scale base" [ref=e210]
            - row [ref=e211]:
              - cell [ref=e212]:
                - code [ref=e213]: "--radius"
              - cell [ref=e214]:
                - code [ref=e215]: .375rem
              - cell "Observed generic radius; do not infer all widgets must have this radius" [ref=e216]
        - paragraph [ref=e217]:
          - text: Observed font stacks start with Instrument Sans for UI, DM Mono for data, JetBrains Mono for code, and EB Garamond for serif. The prototype can use available system fallbacks; do not silently download or claim the same licensed font rendering. Any extra tokens, including positive-state color, focus ring, spacing steps, width limits and mobile breakpoints, are
          - strong [ref=e218]: local proposals
          - text: documented in CSS. Verify contrast on actual text/control pairs; the screenshot alone is insufficient.
        - paragraph [ref=e219]: Official docs describe sharp corners; the observed UI also exposes several radius variables and uses rounded controls. Preserve that difference. Do not derive a universal zero-radius rule from a dashboard paragraph or copy a generic radius to every product surface.
        - heading "4. Choose a page pattern before writing JSX" [level=3] [ref=e220]
        - paragraph [ref=e221]: All top-level routes use an app shell with persistent desktop navigation, a named main region, and a compact navigation control on narrow screens. Put the page identity and highest-priority page action together; put filters beneath; put content and its states in one stable region. Route titles use PageHeader. Inline previews and configuration panels are subordinate to the page identity.
        - table [ref=e222]:
          - rowgroup [ref=e223]:
            - row [ref=e224]:
              - columnheader "Pattern" [ref=e225]
              - columnheader "Use when" [ref=e226]
              - columnheader "Required order / composition" [ref=e227]
              - columnheader "Canonical or experimental" [ref=e228]
          - rowgroup [ref=e229]:
            - row [ref=e230]:
              - cell "Collection" [ref=e231]
              - cell "Files, connectors, agents, skills" [ref=e232]
              - cell "PageHeader → search/filter/view controls → result summary where meaningful → collection OR empty/error/loading state" [ref=e233]
              - cell [ref=e234]:
                - text: Canonical; demonstrated in
                - code [ref=e235]: /files
                - text: ","
                - code [ref=e236]: /connectors
                - text: ","
                - code [ref=e237]: /agents
            - row [ref=e238]:
              - cell "Detail / preview" [ref=e239]
              - cell "Inspect a selected file or agent without losing list context" [ref=e240]
              - cell "Identity → metadata/status → content → contextual actions; provide close/back and restore focus" [ref=e241]
              - cell "Canonical; file preview demonstrated" [ref=e242]
            - row [ref=e243]:
              - cell "Chat workbench" [ref=e244]
              - cell "User gives intent and monitors work" [ref=e245]
              - cell "Conversation identity → ordered messages/results → explicit run/approval state → composer with visible authority and attachment controls" [ref=e246]
              - cell "Canonical proposal; not implemented as a full runtime in this lab" [ref=e247]
            - row [ref=e248]:
              - cell "Configuration" [ref=e249]
              - cell "Connection setup, agent defaults, schedule" [ref=e250]
              - cell "Identity/back → explanation/scope → labeled fields in logical sections → validation → one save/confirm action" [ref=e251]
              - cell "Canonical proposal; real Slack screen informs it; OAuth not executed in lab" [ref=e252]
            - row [ref=e253]:
              - cell "Approval / run review" [ref=e254]
              - cell "Agent needs a decision before an external effect" [ref=e255]
              - cell "Actor and operation → target/scope/consequence → approve and cancel → pending/result evidence" [ref=e256]
              - cell "Canonical proposal; test before production adoption; not proven by this lab" [ref=e257]
            - row [ref=e258]:
              - cell "Dashboard" [ref=e259]
              - cell "Agent-generated structured result" [ref=e260]
              - cell "Stack/Grid root → Cards/group headings → data/charts/tables; keep responsive reading order" [ref=e261]
              - cell "Official widget composition; local adapter does not implement the entire widget catalog" [ref=e262]
        - paragraph [ref=e263]: Do not choose a new page shell for a single feature. A new pattern requires a screenshot with representative content and states, a reason existing patterns fail, Product Design approval, and an implementation/test mapping. One-off promotional or immersive views can be scoped exceptions rather than silently becoming canon.
        - heading "Collection and detail decisions" [level=4] [ref=e264]
        - list [ref=e265]:
          - listitem [ref=e266]: Use a list when users compare repeated fields; use cards when previews or richer descriptions dominate. A view switch must expose selected state and keep search/filter state.
          - listitem [ref=e267]: A page can have multiple actions, but only one filled, visually dominant page-level primary action. Destructive actions belong near the affected object, with explicit consequences before an irreversible effect.
          - listitem [ref=e268]: A preview must not look like a new top-level page unless the URL and navigation context also change. Closing it returns focus to the trigger. Escape and a named close control must work.
          - listitem [ref=e269]: In a collection, loading, initial empty, filtered empty, permission failure and load error are different states. Never reuse “No files” for a failed request.
        - heading "Responsive decisions" [level=4] [ref=e270]
        - paragraph [ref=e271]:
          - text: The lab's navigation compact breakpoint is 760 CSS px; file collections switch to labeled entries at 900 CSS px in
          - code [ref=e272]: layouts.css
          - text: after an 800px overflow was found during visual review; navigation width is
          - code [ref=e273]: "--sidebar-width: 248px"
          - text: and desktop page padding is
          - code [ref=e274]: "--page-padding: 32px"
          - text: in
          - code [ref=e275]: tokens.css
          - text: . These are proposed implementation values, not observed official policy. Automated layout checks use 320, 390, 800 and 1280 CSS px widths (900px height). The live-product audit captured 390 × 844; also inspect this viewport and 320 CSS px manually before production integration.
        - paragraph [ref=e276]:
          - text: "At compact widths, convert file rows to labeled entries: file name first, then each metadata label/value pair. Remove the desktop header when its columns no longer align. Keep names discoverable through the preview or accessible name. Do not leave a narrow desktop header above a stacked list. Controls may hide visible text only if their accessible names remain. Do not use global"
          - code [ref=e277]: "overflow-x: hidden"
          - text: to conceal an overflow bug. A genuinely two-dimensional chart/table can have a labeled local scroll region; the whole page must not require horizontal navigation to reach core actions.
        - heading "5. Rules and failure contracts" [level=3] [ref=e278]
        - paragraph [ref=e279]:
          - text: All eight rules are mandatory within their declared scopes.
          - code [ref=e280]: block
          - text: means the change cannot become a release candidate without a valid scoped exception. Human judgments are explicitly distinguished from automated checks.
        - table [ref=e281]:
          - rowgroup [ref=e282]:
            - row [ref=e283]:
              - columnheader "Rule" [ref=e284]
              - columnheader "Pass contract" [ref=e285]
              - columnheader "Fails when" [ref=e286]
              - columnheader "Enforcement / boundary" [ref=e287]
          - rowgroup [ref=e288]:
            - row [ref=e289]:
              - cell [ref=e290]:
                - strong [ref=e291]: DS-001
                - text: Token use
              - cell [ref=e292]:
                - text: Governed styles use registered semantic color variables. Literal palette values occur only in
                - code [ref=e293]: tokens.css
                - text: .
              - cell "A page/component stylesheet adds an unregistered literal color or references an unknown governed token." [ref=e294]
              - 'cell "CSS AST/static checker. A token can still be used with the wrong meaning: reviewer checks semantics and contrast." [ref=e295]'
            - row [ref=e296]:
              - cell [ref=e297]:
                - strong [ref=e298]: DS-002
                - text: Primitive reuse
              - cell "Feature JSX composes approved local UI primitives; actual native control implementations stay inside the UI boundary." [ref=e299]
              - cell [ref=e300]:
                - text: Governed feature/pattern JSX directly creates
                - code [ref=e301]: button
                - text: ","
                - code [ref=e302]: input
                - text: ","
                - code [ref=e303]: select
                - text: or
                - code [ref=e304]: textarea
                - text: ", including lexically resolved const aliases of those string tags."
              - cell "TS/JSX AST/static checker. It resolves static const string aliases with TypeScript symbols, but does not resolve import provenance, custom wrappers, dynamic aliases or factories; approved library provenance still requires review." [ref=e305]
            - row [ref=e306]:
              - cell [ref=e307]:
                - strong [ref=e308]: LAY-001
                - text: Page identity
              - cell [ref=e309]:
                - text: Each governed route has one visible top-level
                - code [ref=e310]: h1
                - text: within its main region, matching that route's identity. Nested preview/section headings are subordinate.
              - cell "Missing, duplicate, hidden or incorrect main title. A large button/span styled as a heading does not qualify." [ref=e311]
              - cell "DOM test on every governed route at desktop and compact sizes. Correct overall information architecture remains a design review item." [ref=e312]
            - row [ref=e313]:
              - cell [ref=e314]:
                - strong [ref=e315]: A11Y-001
                - text: Named controls
              - cell "Each operable visible button/input/select/link has a non-empty accessible name in the tested states and viewports. Icon controls retain names when text hides." [ref=e316]
              - cell "Name disappears, label is missing, or a control has no usable identifier." [ref=e317]
              - cell "Runtime accessible-name assertions. A non-empty but misleading name can pass; reviewer must assess meaning, focus order and keyboard operation." [ref=e318]
            - row [ref=e319]:
              - cell [ref=e320]:
                - strong [ref=e321]: STATE-001
                - text: Recovery
              - cell "Recoverable empty states explain why and offer an in-state action that actually recovers. Initial empty → create/connect; filtered empty → clear relevant filters; error → retry/appropriate help." [ref=e322]
              - cell "Recovery is absent, inert or leads to the wrong state. A separate distant tab alone is insufficient." [ref=e323]
              - cell "Browser interaction fixtures for known empty states and post-action results. Production network/error states need adapter tests beyond the local fixture." [ref=e324]
            - row [ref=e325]:
              - cell [ref=e326]:
                - strong [ref=e327]: NAV-001
                - text: Destination language
              - cell "Guidance and controls derive destination names from the same label source; actions reveal that destination." [ref=e328]
              - cell "“Available” is referenced when the actual tab is “Connectable”, or the action activates another tab." [ref=e329]
              - cell "Browser assertions against the canonical Chinese destination name, guidance and actual tab/region. Shared-source reuse is a source-review requirement, not import analysis. Localization requires the same check for each supported locale." [ref=e330]
            - row [ref=e331]:
              - cell [ref=e332]:
                - strong [ref=e333]: RESP-001
                - text: Field integrity
              - cell "At tested compact widths, every metadata value stays associated with its visible label, controls stay reachable and key rectangles do not overlap/clip." [ref=e334]
              - cell "Desktop headers no longer correspond to stacked values, or essential content overlaps/offscreen." [ref=e335]
              - cell "Browser geometry and label/structure assertions plus screenshot review. No claim of full visual correctness or every-device coverage." [ref=e336]
            - row [ref=e337]:
              - cell [ref=e338]:
                - strong [ref=e339]: GOV-001
                - text: Contract integrity
              - cell "Registry, document/index links, checker paths and exception records are valid and current. Rule/check changes have owner review." [ref=e340]
              - cell "Referenced files are missing, rule IDs drift, or exception records are malformed/expired/outside their declared scope." [ref=e341]
              - cell "Static validation can check records, not the identity of an approver. External required checks and ownership enforce review." [ref=e342]
        - paragraph [ref=e343]:
          - text: Automated route coverage is
          - code [ref=e344]: /files
          - text: ","
          - code [ref=e345]: /connectors
          - text: ","
          - code [ref=e346]: /agents
          - text: and
          - code [ref=e347]: /guidelines
          - text: ", as recorded in the registry. Future routes and unrepresented dynamic states still require review or new fixtures. DS-001 covers source CSS only; inline styles, CSS-in-JS, dynamically generated styles, external CSS and HTML color attributes are outside its current checker scope. Semantic CSS keywords such as"
          - code [ref=e348]: transparent
          - text: ","
          - code [ref=e349]: currentColor
          - text: and
          - code [ref=e350]: inherit
          - text: are allowed; they do not define new palette values. Adding a privileged UI implementation or changing token authority requires owner review even if the static check passes.
        - heading "State recipes" [level=4] [ref=e351]
        - table [ref=e352]:
          - rowgroup [ref=e353]:
            - row [ref=e354]:
              - columnheader "Situation" [ref=e355]
              - columnheader "Required message" [ref=e356]
              - columnheader "Next action" [ref=e357]
              - columnheader "Result to assert" [ref=e358]
          - rowgroup [ref=e359]:
            - row [ref=e360]:
              - cell "No connected services" [ref=e361]
              - cell "“No connected services” + why connecting helps" [ref=e362]
              - cell "“Browse connectable services”" [ref=e363]
              - cell "Connectable tab is selected and eligible services appear" [ref=e364]
            - row [ref=e365]:
              - cell "File search finds nothing" [ref=e366]
              - cell "State that current query/filters matched nothing" [ref=e367]
              - cell "“Clear search” or “Clear filters”" [ref=e368]
              - cell "Query/filter resets and seeded files reappear" [ref=e369]
            - row [ref=e370]:
              - cell "No agents yet" [ref=e371]
              - cell "Explain repeatable work and how creation starts" [ref=e372]
              - cell "“Create agent” / local example action" [ref=e373]
              - cell "Documented create flow opens; lab must identify it as a simulation" [ref=e374]
            - row [ref=e375]:
              - cell "Load error" [ref=e376]
              - cell "Distinguish failed loading from no data" [ref=e377]
              - cell "Retry, or permission-specific guidance" [ref=e378]
              - cell "Retry is attempted / permission destination is correct" [ref=e379]
            - row [ref=e380]:
              - cell "Agent running / awaiting approval" [ref=e381]
              - cell "Text status, next expected event and available controls" [ref=e382]
              - cell "View progress / make an explicit decision" [ref=e383]
              - cell "Status transitions from actual response, never inferred from animation alone" [ref=e384]
        - heading "6. Before a change ships" [level=3] [ref=e385]
        - list [ref=e386]:
          - listitem [ref=e387]: Declare the pattern, affected route/state/viewports and applicable rule IDs in the change description.
          - listitem [ref=e388]: Read component implementation and CSS; reuse existing variants before adding styles. Register genuinely new tokens with purpose and provenance.
          - listitem [ref=e389]: Implement the behavior and fixtures. Run the package's type, lint, static design, production build and browser checks. Run mutation checks when changing rules, checkers, shared components or layout contracts.
          - listitem [ref=e390]: Inspect desktop and compact screenshots and perform keyboard/focus checks for changed interactions. A green machine check does not waive human design judgment.
          - listitem [ref=e391]: Attach command results, screenshots and any exception ID. Record failures/skips as such; do not silently regenerate snapshots or edit tests just to accept changed behavior.
          - listitem [ref=e392]: Owner review covers pattern choice, semantics, hierarchy, contrast and changes to governance assets. CI must execute against the candidate commit; CD accepts only an artifact from that successful candidate, followed by deployment smoke checks.
        - paragraph [ref=e393]: "From this directory, the concrete gate commands are:"
        - code [ref=e395]: npm ci npm run typecheck npm run lint npm run check:design npm run build npm run test:e2e npm run test:mutations
        - paragraph [ref=e396]:
          - text: Use
          - code [ref=e397]: npm run dev -- --port 3100
          - text: for interactive local inspection. Read the test runner configuration for server startup/port ownership; do not launch competing servers on the same port. The listed commands describe the required gate, not a claim that a run has succeeded. Actual receipts live under
          - code [ref=e398]: reports/
          - text: and are summarized in the compliance audit.
        - paragraph [ref=e399]:
          - text: The prototype demonstrates a local gate. GitHub required checks, CODEOWNERS enforcement, protected environments and deployment receipts must be configured separately.
          - code [ref=e400]: AGENTS.md
          - text: instructs cooperative agents; it is not an access-control boundary. A contributor able to edit every checker and CI policy can bypass local restrictions.
        - heading "7. Exceptions and evolution" [level=3] [ref=e401]
        - paragraph [ref=e402]:
          - code [ref=e403]: exceptions.json
          - text: has the root shape
          - code [ref=e404]: "{ \"exceptions\": [] }"
          - text: . Each record requires exactly
          - code [ref=e405]: id
          - text: ","
          - code [ref=e406]: ruleId
          - text: ","
          - code [ref=e407]: path
          - text: ","
          - code [ref=e408]: reason
          - text: ","
          - code [ref=e409]: owner
          - text: ","
          - code [ref=e410]: approvedBy
          - text: ", and"
          - code [ref=e411]: expires
          - text: (YYYY-MM-DD; current implementation expires at the end of that UTC date). Use an exact existing relative file path and document affected route/state, tracking reference and compensating verification in the reason/review record. An expired exception fails closed. Never use a wildcard exception for an entire app. Only DS-001 and DS-002 support scoped waivers in this prototype. GOV-001 and browser-rule exceptions fail closed and require a separately reviewed contract change.
          - code [ref=e412]: approvedBy
          - text: is a declared identity and must be verified through the protected review system.
        - paragraph [ref=e413]: Repeated exceptions indicate a missing pattern or an incorrect rule. Review them with Product Design + Engineering, then revise the contract and add positive/negative examples. Separate a real product violation from a checker false positive. Keep the original mutation results when improving coverage; report survivors and invalid experiments honestly.
        - heading "8. What this contract does not prove" [level=3] [ref=e414]
        - paragraph [ref=e415]: "This lab does not recover CREAO's internal component library, change its production site, execute real integrations, validate live agent runs or prove universal WCAG compliance. Static checks cover documented syntax and files; runtime checks cover explicit route/state fixtures. Screenshots are retained locally and may contain account context: use cropped/redacted copies before public submission. The experiment's evidence is useful because those limits are explicit."
  - alert [ref=e416]
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | import { knownFileContract } from './fixtures/file-contract';
  3   | 
  4   | test.beforeEach(async ({ browser }, testInfo) => {
  5   |   testInfo.annotations.push({ type: 'browser-version', description: browser.version() });
  6   |   testInfo.annotations.push({ type: 'browser-channel', description: process.env.PW_CHANNEL || 'bundled-chromium' });
  7   | });
  8   | 
  9   | const routes = [
  10  |   { path: '/files', heading: '文件' },
  11  |   { path: '/connectors', heading: '连接器' },
  12  |   { path: '/agents', heading: '智能体' },
  13  |   { path: '/guidelines', heading: '设计规范' },
  14  | ];
  15  | 
  16  | for (const width of [1280, 390]) {
  17  |   for (const route of routes) {
  18  |     test(`[LAY-001] ${route.path} one visible page heading at ${width}px`, async ({ page }) => {
  19  |       await page.setViewportSize({ width, height: 900 });
  20  |       await page.goto(route.path);
  21  |       const main = page.getByRole('main');
  22  |       await expect(main).toHaveCount(1);
  23  |       const headings = main.getByRole('heading', { level: 1 });
> 24  |       await expect(headings).toHaveCount(1);
      |                              ^ Error: expect(locator).toHaveCount(expected) failed
  25  |       await expect(headings).toBeVisible();
  26  |       await expect(headings).toHaveText(route.heading);
  27  |     });
  28  | 
  29  |     test(`[A11Y-001] ${route.path} visible controls retain accessible names at ${width}px`, async ({ page }) => {
  30  |       await page.setViewportSize({ width, height: 900 });
  31  |       await page.goto(route.path);
  32  |       await expect(page.getByRole('main')).toBeVisible();
  33  |       // Compute accessible names using Playwright's ARIA engine rather than reading a self-reported label flag.
  34  |       const controls = page.locator('button, input:not([type=hidden]), select, textarea, a[href], [role=button], [role=tab]');
  35  |       expect(await controls.count()).toBeGreaterThan(0);
  36  |       for (const control of await controls.all()) {
  37  |         if (await control.isVisible()) await expect(control).toHaveAccessibleName(/\S/);
  38  |       }
  39  |     });
  40  |   }
  41  | }
  42  | 
  43  | test('[STATE-001] connector empty state action reaches available services', async ({ page }) => {
  44  |   await page.goto('/connectors');
  45  |   await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  46  |   const recovery = page.getByRole('button', { name: '浏览可连接服务', exact: true });
  47  |   await expect(recovery).toBeVisible();
  48  |   await recovery.click();
  49  |   await expect(page.getByRole('tab', { name: '可连接', exact: true })).toHaveAttribute('aria-selected', 'true');
  50  |   await expect(page.getByRole('button', { name: /连接/ }).first()).toBeVisible();
  51  |   await expect(recovery).toHaveCount(0);
  52  | });
  53  | 
  54  | test('[NAV-001] empty-state destination copy matches actual available tab', async ({ page }) => {
  55  |   await page.goto('/connectors');
  56  |   const destination = page.getByRole('tab', { name: '可连接', exact: true });
  57  |   await expect(destination).toBeVisible();
  58  |   await page.getByRole('tab', { name: /^已连接(?: \(\d+\))?$/ }).click();
  59  |   // The guidance must name the destination itself, not an obsolete synonym.
  60  |   await expect(page.getByRole('main')).toContainText('可连接');
  61  |   const guidance = page.getByTestId('empty-state-description');
  62  |   await expect(guidance).toContainText('可连接');
  63  |   await expect(guidance).not.toContainText('可用');
  64  |   await page.getByRole('button', { name: '浏览可连接服务', exact: true }).click();
  65  |   await expect(destination).toHaveAttribute('aria-selected', 'true');
  66  | });
  67  | 
  68  | test('[STATE-001] file search no-results action restores actual entries', async ({ page }) => {
  69  |   await page.goto('/files');
  70  |   const search = page.getByRole('searchbox', { name: '搜索文件和文件夹' });
  71  |   await search.fill('no-file-matches-928371');
  72  |   await expect(page.getByTestId('file-item')).toHaveCount(0);
  73  |   await page.getByTestId('empty-state-description').locator('..').getByRole('button', { name: '清除搜索', exact: true }).click();
  74  |   await expect(search).toHaveValue('');
  75  |   await expect(page.getByTestId('file-item').first()).toBeVisible();
  76  | });
  77  | 
  78  | test('[RESP-001] file list preserves field labels and fits 390px viewport', async ({ page }, testInfo) => {
  79  |   await page.setViewportSize({ width: 390, height: 900 });
  80  |   await page.goto('/files');
  81  |   await page.getByRole('button', { name: '列表视图', exact: true }).click();
  82  |   await expect(page.getByTestId('desktop-file-header')).toBeHidden();
  83  |   const items = page.getByTestId('file-item');
  84  |   expect(await items.count()).toBeGreaterThan(0);
  85  |   const knownItem=items.filter({ has: page.getByRole('button', { name: knownFileContract.name, exact: true }) });
  86  |   await expect(knownItem).toHaveCount(1);
  87  |   for (const field of knownFileContract.fields) {
  88  |     const label=knownItem.getByTestId('file-meta-label').filter({ hasText: new RegExp(`^${field.label}$`) });
  89  |     await expect(label).toHaveCount(1);
  90  |     await expect(label.locator('..')).toHaveText(`${field.label}${field.value}`);
  91  |   }
  92  |   for (const item of await items.all()) {
  93  |     await expect(item).toBeVisible();
  94  |     const labels=item.getByTestId('file-meta-label');
  95  |     await expect(labels).toHaveText(knownFileContract.fields.map(field => field.label));
  96  |     for(const label of await labels.all()) await expect(label).toBeVisible();
  97  |     const box=await item.boundingBox();
  98  |     expect(box).not.toBeNull();
  99  |     expect(box!.x).toBeGreaterThanOrEqual(0);
  100 |     expect(box!.x+box!.width).toBeLessThanOrEqual(391);
  101 |     const geometry=await item.evaluate(element=>{
  102 |       const fields=[...element.querySelectorAll('[data-testid="file-meta-label"]')].map(label=>label.parentElement!.getBoundingClientRect());
  103 |       return fields.map(field=>({left:field.left,right:field.right,top:field.top,bottom:field.bottom}));
  104 |     });
  105 |     for(let a=0;a<geometry.length;a++)for(let b=a+1;b<geometry.length;b++){
  106 |       const x=Math.min(geometry[a].right,geometry[b].right)-Math.max(geometry[a].left,geometry[b].left);
  107 |       const y=Math.min(geometry[a].bottom,geometry[b].bottom)-Math.max(geometry[a].top,geometry[b].top);
  108 |       expect(x>1&&y>1,'File metadata fields overlap').toBe(false);
  109 |     }
  110 |   }
  111 |   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  112 |   expect(overflow,'Document has horizontal clipping/overflow').toBe(false);
  113 |   await testInfo.attach('files-390px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  114 |   await page.setViewportSize({ width: 1280, height: 900 });
  115 |   await expect(page.getByTestId('desktop-file-header')).toBeVisible();
  116 |   for(const label of await page.getByTestId('file-meta-label').all())await expect(label).toBeHidden();
  117 |   await testInfo.attach('files-1280px', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  118 | });
  119 | 
  120 | for(const width of [320,800]) {
  121 |   test(`[RESP-001] file list has no horizontal overflow at ${width}px`, async ({ page }, testInfo) => {
  122 |     await page.setViewportSize({ width, height: 900 });
  123 |     await page.goto('/files');
  124 |     await expect(page.getByRole('heading', { level: 1, name: '文件', exact: true })).toBeVisible();
```