# CREAO 可执行设计规范：实施与验证计划

日期：2026-10-11。状态：本地实现与增强门禁已完成，最终实验和交付包收口；详细状态以 validation-results.zh-CN.md 的实际收据为准。范围：本地研究、独立 Next.js 原型、规范、检查器、变异实验与 CI 配置；不修改 CREAO 线上产品，不部署或推送。

## 目标和验收

将已有证据转成可运行的闭环：`design.md → CSS / 组件 / 页面 → 静态检查 + 浏览器检查 → 合规与违规修改实验 → CI 门禁`。Markdown 是人和编程智能体的入口，规则注册表与检查代码执行可自动化部分；不能声称 Markdown 自己能约束任意实现。

完成条件：

1. `design.md` 为每个规范值标注官方文档、线上观察或本原型提案；索引实际 CSS、组件、规则编号、检查入口。
2. 独立 Next.js 项目启动和构建成功，文件、连接器、智能体的最小流程能操作，桌面和窄屏可检查。
3. 合规基线通过 lint、类型、设计规则、构建和受影响路径浏览器验证。
4. 违规代码变更真正作用于隔离副本中的实现，由与基线相同的检查器识别；记录命中规则。不能仅检查一个 `isViolation` 标记或预设返回值。
5. 至少两个遵循规范的合理修改通过，至少六类独立违规接受测试。报告 killed / survived / invalid / error，分母准确，超时或编译失败不能算设计规则成功拦截。
6. 保留模拟工程师的任务、修改、结果及局限；固定 mutation 集与独立工程师实验分别报告。
7. CI 配置使用相同命令，能上传失败证据；声明仓库分支保护与远端执行尚未启用，不把本地通过等同于部署成功。

## 必须交付的两份题目文件

这两份 Markdown 是最终交付的主体，原型与工程附件为它们提供可复现的证据，不能替代它们。

| 必交文件 | 必须包含 | 验收条件 | 当前状态 |
| --- | --- | --- | --- |
| [design-system-guideline.md](design-system-guideline.md) | 产品层布局模式、既有设计系统的使用边界、规则 ID、工程师/agent 执行步骤、具体检查入口、例外与发布门禁 | 读者无需追问即可选布局、找到 CSS/组件、运行检查并理解失败；每条自动规则映射实际实现，人工规则明确标注 | 已定稿，含增强门禁与执行范围 |
| `compliance-audit.md` | 将规范应用于已探索的真实页面；逐条记录页面/状态/视口、截图和 DOM 证据、违反的规则、影响、修复方式、上线前哪个检查能发现 | 每个发现有证据与规则编号；区分真实线上观察、原型复现、尚未覆盖；引用实际命令、失败结果和实验收据，不能虚构在 CREAO 私有源码执行过检查 | 已写入真实审计，最终实验收据收口中 |

题目原文与中文译文分别保留在 [task.md](task.md)、[task.zh-CN.md](task.zh-CN.md)。研究、计划和实验是附加材料，不混入题面原文。

## 工程交付与证据清单

以下全部属于本次实施范围。路径相对于仓库根；“已写入”仅说明文件存在，不等于验收通过。

| 交付项 | 产物位置 | 必须验证什么 | 当前状态 |
| --- | --- | --- | --- |
| 可执行设计入口 | `creao-design-lab/design.md`、`AGENTS.md` | 官方/观察/提案来源分开；索引真实 CSS、组件、规则和执行命令；agent 不得删检查以通过 | 已写入 |
| 三层 CSS 与组件 | `src/styles/tokens.css`、`components.css`、`layouts.css`，`src/components/{ui,patterns}/` | 颜色映射有来源；布局/响应式与组件分层；受治理样式不新增裸色和未知变量 | 已通过静态/类型/构建与浏览器检查 |
| Next.js 原型 | `creao-design-lab/src/app/`、`package.json`、`package-lock.json` | Files/Connectors/Agents 实际可操作；Guidelines 阅读 Markdown，受控源码查看能打开 CSS；开发启动与生产构建通过 | 已实现并完成构建 |
| CSS/JSX 设计 lint | `scripts/check-design.mjs`、`tests/design/` | CSS AST 检查裸色/未知 token；TS AST 检查绕过控件；验证合法例子与违规例子，准确披露别名/动态写法边界 | 13项单元检查通过 |
| 通用 lint 与类型 | `eslint.config.*`、`tsconfig.json`、package scripts | `npm run lint`、`npm run typecheck` 通过；与设计 lint 分别报告 | 执行中 |
| 规则与例外治理 | `governance/rules.json`、`exceptions.json` | ID、入口、文档链接有效；例外精确限定文件与规则、有原因/owner/截止日；过期失败 | 已实现 |
| 浏览器检查 | `tests/e2e/design.spec.ts`、`playwright.config.ts` | 桌面与窄屏标题、名称、可操作恢复、目的地、字段 label/value 对应与几何；CI 对生产构建运行 | 38项行为/axe通过；视觉基线3/3通过 |
| 原站截图与观察 | `exam/research/screenshots/`、`deep/`、DOM/AX 快照及 capture manifest | 来源 URL、时间、视口和状态可定位；截图有人工审阅，避免把加载中/AX 映射误当真实缺陷 | 已采集并审阅 |
| 原型截图与视觉验收 | `exam/research/prototype/`（计划位置）及浏览器失败截图/trace | 桌面、390px、关键交互/空状态；补查窄屏与中间宽度；截图人工检查与自动断言分开 | 已完成，含800px修复前后证据 |
| 固定 mutation 实验 | `scripts/mutation-runner.mjs`、`tests/mutations/`、`reports/` | 真正修改隔离实现；正例证明不过度拦截；负例命中实际规则；保留 killed/survived/invalid/error 与初次漏检 | 静态复验6/6；最终增强all运行中 |
| 独立工程师合规实验 | `experiments/engineer-protocol.md`、隔离副本、补丁与验收收据 | 两位 subagent 做同一新功能，一位遵循、一位走捷径；检查资产不变；分别验功能与规范；不能把预设 mutation 冒充独立实验 | v1完成；增强v2已实施并验收中 |
| CI 与候选产物契约 | `.github/workflows/creao-design.yml` | 锁文件安装、lint/类型/单测/设计检查、build、浏览器、mutation；失败上传证据；只有 gate 通过才生成源码版本收据 | YAML 已写入；未远端执行 |
| 运行说明与结果 | `creao-design-lab/README.md`、`exam/compliance-audit.md` | 可复制命令、版本、实际通过/失败数、报告索引、未验证路径；本地成功不写成线上部署成功 | 待最终回填 |

`reports/` 是运行生成目录，不作为首次执行前必须存在的源码依赖。最终审计需保留可阅读的实验摘要和定位信息；不能只留下被忽略的临时报告而没有持久结论。

## 验收命令与证据闭环

在 `creao-design-lab/` 内按下列顺序执行，失败先定位原因，不删除规则来换取通过：

```bash
npm ci
npm run typecheck
npm run lint
npm run test:design
npm run check:design
npm run build
npx playwright install chromium
PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
npm run test:mutations
```

另外执行 React Doctor 与人工浏览器验收；分别报告静态提示和真实交互结果。Linux CI 安装浏览器系统依赖使用 `npx playwright install --with-deps chromium`。正式 mutation 启动前冻结规范、源码和检查器摘要；独立实验使用副本，不改共享基线。

完整追溯链为：**原站截图/DOM → 审计发现 → guideline 规则 ID → design.md/CSS/组件 → 检查断言 → 真实失败输出 → 修复与复验 → CI gate**。每条审计发现必须说明链条中哪些环节已实测、哪些只是接入 CREAO 仓库后的要求。

收尾条件：两份必交文件定稿，原型可运行，检查结果与实验分母已核对，截图已审阅，首次漏检保留，CI 外部未接入项明确；以上任何一项未完成，都不能把整个计划标为完成。

## 已有依据与边界

- 官网 sitemap 227 条、文档站 sitemap 92 条；未发现独立全站 `design.md` 的公开索引。产品 sitemap 返回 403，此处不绕过。
- 已找到官方 Widgets Markdown：`https://docs.creao.ai/features/widgets.md`，本地原文在 `research/public-design-search/widgets.official.md`。这是一份 Dashboard 组件说明，不是全站设计系统源码。
- 线上 `/widgets` 提供 Card、Stack、Grid、Tabs 等预览与参数；`research/deep/widgets-dom.json` 保存实际 CSS 变量。需要保留官方文档和实时呈现之间的差异，不编造组件 import/API。
- 用户确认没有其他附件。不再以缺少附件为前置阻塞。没有功能简报的部分，用明确标为本次实验的功能请求验证。
- 现有真实问题包括文件页标题语义、连接器空状态文案和操作、390px 文件列表表头错位、图标按钮丢失名称。
- 原型组件是用于验证的本地适配实现，不冒充 CREAO 私有组件库。

## 工作区与文件契约

独立项目放在 `../creao-design-lab/`（相对于本文件）。不修改 `task1`、根目录凭据或既有项目。使用 npm 和精确锁文件，Node 24；Next.js App Router + React + TypeScript。基线端口 3100。

```text
creao-design-lab/
  AGENTS.md
  design.md
  README.md
  package.json / package-lock.json
  src/app/{layout.tsx,page.tsx,files/,connectors/,agents/,guidelines/}
  src/components/ui/             # 原型内部批准的基础组件
  src/components/patterns/       # Shell、PageHeader、EmptyState 等
  src/styles/{tokens.css,components.css,layouts.css}
  src/lib/                      # 合成数据、统一文案
  governance/rules.json          # 规则 ID、严重度、来源、执行层与证据位置
  governance/exceptions.json     # 例外记录，默认空
  scripts/                      # 检查器、变异与隔离运行入口
  tests/{design/,e2e/,mutations/}
  experiments/                  # 独立模拟工程师的任务、补丁与收据
  reports/                      # 本地生成的机器可读结果，不伪造已通过状态
```

仓库根 `.github/workflows/creao-design.yml` 仅负责此项目。正式题目要求的两份文件放在 `exam/`，通过相对路径引用原型证据。研究截图不上传到公开服务。

## 规范与实现范围

### 视觉与交互

复用观察到的暖白背景、近黑文字、细边框、克制的语义色和简洁侧栏。颜色值来自已记录的变量；新增的间距、布局阈值、组件 API 标注为原型决策。避免无依据全站重设计。

- 文件：搜索、清除搜索、网格/列表切换、行内创建模拟文件夹、可关闭预览。使用合成文件，不复制用户数据。
- 连接器：全部/可连接/已连接状态切换与可恢复空状态；模拟连接状态必须明确为本地演示，不能真的 OAuth。
- 智能体：空状态与示例详情/状态呈现，明确本地模拟，不触发真实模型运行。
- 规范页：能阅读规范和 CSS/规则映射；不要在产品任务页面塞入 CI 或实现术语。
- 窄屏：侧栏折叠，表格转换为有标签的条目，图标按钮仍有可访问名称；长名称、无结果、错误状态可检查。

### 首批规则 ID（各实现必须统一）

| ID | 规则 | 自动化方向 |
| --- | --- | --- |
| DS-001 | 受治理 CSS 中的颜色使用登记 token；新增裸色须失败 | CSS AST |
| DS-002 | 页面不得绕开本地批准的 Button/Input 等基础组件 | TS/JSX AST，明确范围 |
| LAY-001 | 顶层主区域一个可见且匹配页面身份的一级标题 | DOM |
| A11Y-001 | 可操作控件在桌面与窄屏均有可访问名称 | DOM/无障碍检查 |
| STATE-001 | 可恢复空状态有可操作下一步，并验证实际目的地 | 交互测试 |
| NAV-001 | 引导名称与真实目的地一致，复用统一文案 | 浏览器文案契约 + 交互 |
| RESP-001 | 窄屏列表保持字段对应，无重叠/关键内容裁切 | 几何检查 + 截图人工审阅 |
| GOV-001 | 规则、文档索引、CSS/检查入口存在且例外有效 | 注册表/链接/例外校验 |

规则不能靠自报 `data-compliant=true` 判定。允许测试定位属性，但断言必须检查实际结构、名字、行为或几何。源码 lint 可读取真实 AST；禁止只用正则冒充完整分析。

## 执行阶段及并行分工

1. **规则与证据 agent**：整理 sitemap/截图研究结论，编写 `design.md`、`AGENTS.md` 与题目规范文档初稿；不写 app 或脚本。
2. **原型 agent**：独占 package、Next 配置、src 和视觉实现；与检查 agent 对齐组件导出和路径；不改检查器。
3. **检查 agent**：独占 governance、设计检查、lint 配置和浏览器测试；向主 agent 报告所需依赖，由原型 owner 合并 package。
4. **变异 agent**：独占 mutation runner、fixture/patch 和实验设计；在隔离临时目录运行变更，不覆盖共享源文件；报告精确命中和逃逸情况。
5. **主 agent**：集成、依赖安装/统一命令、CI、浏览器视觉验证、来源核对、独立模拟工程师调度、最终收据与题目合规审计。文件冲突先协调 owner，不覆盖他人改动。

设计文档、检查器与 UI 可以并行起草，但必须在基线确定后跑完整验收。模拟工程师实验须等待规范与基线冻结后开始；他们不得修改检查代码来让结果通过。

## 验证与变异实验

采用三类证据：

- **确定性负例**：注入裸色、绕过基础组件、删除 h1、隐藏按钮文案而不保留名称、删除空状态操作、目的地文案错误、移动布局退化、失效例外等。
- **确定性正例**：换用已登记颜色；增加合法文件条目/长名称；使用规范组件增加次要操作。用于测量误报，不能只证明违规被拦。
- **独立工程师实验**：至少一个遵守规范的功能修改和一个故意走捷径的修改，使用不同 subagent、独立复制目录、相同任务和原有检查。将其与预设 mutation 集分开统计。

每次实验收据记录：基线文件摘要、任务/变异、改动文件、检查命令、退出码、规则 ID、耗时、报告路径、分类原因。运行前后核对共享基线摘要，避免污染。新发现的逃逸应保留在结果中；修复检查器后记录第二轮结果，不能覆盖第一次失败。

## CI/CD 与治理

- CI 阶段：锁文件安装 → 类型/lint → 设计静态规则 → 生产构建 → 浏览器受影响路径测试 → mutation 验证 → 证据上传。
- 检查内容与执行配置也属于治理资产；需要 CODEOWNERS/规则所有者评审和外部 required check 才能防止作者自行删除 gate。仅有 AGENTS.md 或可编辑的 CI YAML 无法防绕过。
- 快速 PR 检查与耗时 mutation 可分层，但此原型必须本地跑通两层。
- 不把视觉快照自动更新当通过；基准变更要有截图和人工理由。可采用语义与几何断言跨平台运行，固定环境后再启用像素门槛。
- 记录例外的范围、原因、owner、截止日期；检查器验证格式和有效期，但不能证明审批人身份，真实审批必须来自受保护的流程。
- CD 在此阶段只设计“通过 gate 后才能产出/发布候选”的契约，不实际部署。远端分支保护、环境审批与部署 smoke check 明确列为未接入项。

## 技术选型与推进优先级（2026-10-11 讨论结论）

本节记录用户确认的推进顺序：**先完成现有验证闭环 → 补 axe、视觉回归和页面状态清单 → 跑通合规与违规工程师实验 → 完善两份必交文档**。由主线程 `creao-design-master`（`01a12cb6-efdc-77b2-965f-646055a400be`）统一协调 swarm、文件 owner、基线冻结和最终验收；讨论线程不另起一套并行实现。以下优先级是实施决策，不表示工具已安装或检查已通过。

### 已采用方案及作用

| 方案 | 当前职责 | 不能替代的部分 |
| --- | --- | --- |
| 截图、DOM/AX 和 CSS 变量证据 | 支撑真实问题与视觉来源 | CREAO 私有组件 API、内部权威 token 源 |
| `design.md`、`AGENTS.md`、规则与例外注册表 | 人/agent 阅读入口、规则索引、例外有效期 | 仓库权限和真实审批身份 |
| Next.js + React + TypeScript | 可运行的路由、组件与交互实验 | CREAO 现有技术栈；将来应适配原库 |
| tokens/components/layouts 三层 CSS | 分离变量、控件和页面几何 | 全面的间距、排版与 token 语义约束 |
| TypeScript AST + PostCSS AST | 自定义设计 lint：原生控件/静态别名、裸色、未知 token | 任意动态工厂、包装组件来源、内联/CSS-in-JS 的完整分析 |
| Playwright DOM、交互与几何断言 | 验证真实页面行为与部分布局 | 完整无障碍审计、视觉好坏判断、未登记状态 |
| 自定义 mutation runner | 在隔离源码副本注入设计违规、测量门禁是否命中 | 独立工程师实验、所有未知违规的覆盖证明 |
| GitHub Actions YAML | 串联检查、保留证据、生成候选源码收据 | 已启用 required checks、远端 CI 或实际部署的证明 |

讨论时只读核对到的历史证据：首轮静态 mutation 为 5/6 负例命中、1 个别名写法漏检，2/2 正例通过，invalid/error 为 0；报告位于 `creao-design-lab/reports/mutations-static-2026-10-11T21-03-48-256Z/`。后续源码已增加静态 const 别名解析，但必须另有复验收据才可宣称已验证。彼时 `reports/e2e.json` 记录 20 项浏览器启动失败，原因是缺少匹配 Chromium，不属于设计违规拦截。主线程继续时须读取最新证据，不能将此历史快照当作最终状态。

### 选型决策

| 优先级 | 方案与决定 | 采用原因和边界 |
| --- | --- | --- |
| P0：先收口 | 完成现有 lint、类型、单测、设计检查、生产构建、浏览器及 mutation 闭环 | 先建立可信基线；保留初次 survivor，补检查后另存复验；基础设施失败不能计入 killed |
| P1：本次必做 | `@axe-core/playwright` | 在已登记的首屏、弹窗、空态/错误态补自动无障碍扫描；保留命名、键盘、焦点恢复与业务断言，不宣称完整 WCAG 合规 |
| P1：本次必做 | Playwright `toHaveScreenshot()` 视觉回归 | 将截图留证升级为经审阅基线比较；先覆盖 Files 桌面/窄屏及关键空态，固定字体、数据、视口、浏览器和运行环境；变化必须解释，禁止失败后自动更新基线 |
| P1：本次必做 | 页面—状态—视口清单 | 枚举已有路由、状态、预期、检查 ID、截图与覆盖状态；未实现/未测试必须显式记录，避免新增页面悄悄脱离门禁 |
| P1：本次必做 | 独立工程师 A/B 实验 | 两个 agent 在冻结基线副本上做同一功能，一位遵守规范、一位采取合理但违规的捷径；原始 gate 不变，分别评估功能与规范 |
| P1：后续针对缺口增强 | 类型化页面模式与组件 API | 用 CollectionPage、IconButton、按 empty/error 类型区分的状态接口减少错误空间；必填字段不能证明回调有效，仍保留运行时测试；本轮不以大规模重构阻塞闭环 |
| P1：后续标准化 | ESLint 导入约束、Stylelint 插件、token 用途约束 | 先管批准的组件入口和高价值语义，再将稳定自定义规则包装为 IDE/CI 可复用插件；合法 token 也可能被用错，不能仅检查变量存在 |
| 生产接入前必需 | Rulesets、required checks、CODEOWNERS、治理文件保护 | 保护规范、组件底座、tokens、测试、例外、workflow 与 CODEOWNERS 自身，约束 bypass 和审批失效；核实仓库套餐/权限，不把本地 YAML 当作已启用保护 |
| P2：近期按需 | Storybook/CSF 模式目录 | 将 PageHeader、EmptyState、文件列表组合的状态做成可运行样例并由规范链接；先完成状态清单，不重建整个组件库 |
| P2：接入 API 时 | MSW | 统一模拟慢响应、500、权限不足、空结果与恢复；当前本地 React 状态原型暂不强加网络模拟层，服务端请求需单独设计拦截 |
| P2：针对覆盖缺口 | fast-check | 生成合法名称、筛选组合与操作序列，保存 seed 和最小反例；优先纯函数/检查器，再做有界浏览器样例 |
| P2：检查器成熟后 | Stryker | 变异检查器内部逻辑以检验单元测试；与注入页面设计违规的自定义 mutation 分开统计，不立即全量变异 Next 应用 |
| 暂缓 | DTCG + Style Dictionary、付费视觉平台、集中式组织 workflow | 多平台/主题/团队规模出现需求后再引入；目前没有 CREAO 私有 token 源，避免制造第二套权威或扩大工具范围 |

既有产品接入采用渐进治理：冻结历史违规清单，新修改不新增违规，已修问题不回退；每项例外有负责人、原因、期限与修复任务。新增例外和扩大历史基线也需审查。持续记录误报、漏检和执行耗时，避免团队为减少噪声而关闭 gate。

### Swarm 执行顺序与验收交接

1. **阶段 A — 现有闭环。** 检查 agent 负责现有浏览器/静态验证，mutation agent 负责冻结副本与复验，原型 owner 修真实实现缺陷；主线程统一 dependency/lock 修改和基线版本。退出条件：合规候选通过既定检查，正负例分类准确，初次失败完整保留，报告可复现。
2. **阶段 B — 扩大验证。** axe owner、视觉回归 owner、状态清单 owner 可并行起草，各自独占测试文件/清单；共享 package、Playwright config、规则注册表由主线程或指定 owner 集成。建议产物为 `tests/e2e/accessibility.spec.ts`、`tests/e2e/visual.spec.ts`、版本化视觉基线以及 `governance/page-states.json`（或等价单一清单）；最终路径由主线程确认并索引，不能重复维护相互矛盾的清单。退出条件：新增检查在合规基线上通过，至少一个适当负例证明能够触发检查，基线截图由独立 reviewer 看过，新增状态有明确覆盖结果。
3. **阶段 C — 工程师实验。** 增强后的基线再次冻结。两位独立 agent 按 `experiments/engineer-protocol.md` 实现同一功能；不得修改 tests、规则、依赖或 gate 来让结果通过。独立 evaluator 核对受保护资产摘要，运行同一检查并验证新功能实际行为，保留任务、补丁、截图、命令、退出码和逐条结论。违规实现须能编译；编译失败只能视为无效实验。修复作为第二轮，不能覆盖首轮。
4. **阶段 D — 必交文档。** 文档 owner 根据最终运行收据完善 `exam/design-system-guideline.md`、`exam/compliance-audit.md`；独立 reviewer 核对规则编号、真实页面证据、检查入口、截图、实验分母和外部未接入项；主线程验收 README、实施计划状态与两份正式交付一致。

阶段间可以并行准备，但不得跳过依赖或让不同 agent 在同一冻结基线上写入。测试、文档或 UI 如发生变化，应生成新的候选身份，并仅重跑受影响检查及必需的最终门禁。声明通过必须对应实际报告，不依据 agent 自报。

### 新增验收要求

- **axe：** 保存扫描页面/状态、规则标签、违规详情及未覆盖范围；不能通过全页排除来消除失败。
- **视觉：** 保存 expected/actual/diff、环境信息与基线审阅理由。跨操作系统结果不可混用；没有稳定基线的状态记录为待建立，不能记通过。
- **状态清单：** 至少覆盖当前 Files/Connectors/Agents/Guidelines 的实际状态；Files 包括有数据、搜索无结果、长名称、创建验证与预览；Connectors 包括已连接为空与恢复；Agents 包括空态与示例详情。loading/error/permission 如尚无实现，要标未实现而不是伪造覆盖。
- **工程师实验：** 合规实现通过同一套适用 gate；违规实现逐条记录被哪些规则捕获、哪些漏检；功能验收与设计合规分别给结论，不能承诺未知违规全部被拦截。
- **最终文档：** 审计追溯链增加 axe/视觉证据，固定 mutation、工程师实验、基础设施失败分别统计；本地原型证明与 CREAO 生产接入明确分开。

### 技术依据

- [TypeScript 联合类型与收窄](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)：组件状态契约。
- [Playwright 无障碍测试](https://playwright.dev/docs/accessibility-testing)、[视觉比较](https://playwright.dev/docs/test-snapshots)：axe 集成、环境一致性与截图基线。
- [ESLint 导入约束](https://eslint.org/docs/latest/rules/no-restricted-imports)、[Stylelint 插件](https://stylelint.io/developer-guide/plugins/)：成熟 lint 扩展接口。
- [Storybook CSF](https://storybook.js.org/docs/api/csf)、[网络模拟](https://storybook.js.org/docs/writing-stories/mocking-data-and-modules/mocking-network-requests)：可运行状态目录与 MSW。
- [fast-check](https://fast-check.dev/docs/core-blocks/)、[StrykerJS](https://stryker-mutator.io/docs/stryker-js/introduction/)：输入性质测试与程序变异，不能代替设计 mutation 或独立工程师实验。
- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)：可信检查与审批边界。
- [DTCG 格式规范](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)、[Style Dictionary](https://styledictionary.com/getting-started/installation/)：后续 token 交换/生成选项；DTCG Community Group 规范不等于 W3C Recommendation。

## 风险与报告原则

有限测试通过不代表任意工程师都无法绕过。明确支持的代码写法、动态样式/别名/包装组件限制、浏览器与状态覆盖、剩余人工规则。观察到的页面样式值不等于官方推荐 API。所有演示数据与真实产品证据分开。最终汇报包含实际结果和残余风险，不只展示一个漂亮页面或 mutation 分数。


## 按用户要求立即收尾的交付状态

两份题目必交文件、Next.js 原型、AGENTS/design/CSS 索引、13 项设计单测、增强浏览器 38/38、审阅后的视觉 3/3，以及 axe/视觉各 1 个真实负例均已落地。A/B 原实验与同 agent 的增强复验分别保存；A 增强38/38，B32/38并被阻断。CI配置已写，Linux视觉基线与远端保护尚未接入。

最终固定 mutation 在用户要求立即收尾时仍运行：已封存 9/12 个计划负例 killed、2/3 个正例 passed，另 3 个负例 + 1 个正例 pending。完整运行未完成，不能将整份计划标成全部完成；首轮别名漏检、两次基础设施失效与所有修复证据保留。详见 [验证结果](validation-results.zh-CN.md) 与 [部分运行收据](research/validation/phase-b/mutations-all-partial-2026-10-11T21-28-22-239Z/partial-summary.json)。
