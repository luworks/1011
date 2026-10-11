# CREAO 交付包与可执行规则组织方案

日期：2026-10-11。状态：交付设计；尚未生成最终压缩包、上传附件或启用巡查调度。主线程 `creao-design-master` 负责在最终候选验收后集成。

## 交付决定

用户确认的最终范围是截图所示 `.github/`、`creao-design-lab/`、`exam/` 三个目录中与本任务有关的完整过程和交付：题面与翻译、产品探索、技术选型与实施计划、规则及实现、检查脚本、CI、实验协议、首轮失败/漏检、修复复验、截图与结果、数字员工职责，以及两份正式文档。打包保留这三个目录的相对结构，并提供按过程阶段和评审阅读顺序组织的入口。过程说明以可追溯的文档、补丁和运行证据为准，不要求读者翻聊天记录才能理解。打包时逐项核对纳入与排除清单；不能只打包最终成功截图，或遗漏已引用的研究和失败记录。

题面明确要求 `design-system-guideline.md` 和 `compliance-audit.md` 两份 Markdown。它们必须独立说明规则、真实发现和上线前的检查机制。可执行附件为其提供可复现证据，不能替代这两份正文，也不能假定提交平台接受任意数量或格式的附件。

建议准备一套可审阅、可复现的补充交付包：规范正文 + 规则实现 + 最小原型 + 测试 + 精选证据 + 巡查 agent 职责。上传形式由平台支持的文件数量、格式和大小决定：若允许附加 ZIP，提交两份必交文档及补充包；若只接受两份 Markdown，正文保留完整关键规则和审计结论，并在平台允许的方式下引用补充包。不可假称补充包已上传。

## scripts 的职责

目前已有 `creao-design-lab/scripts/`，无需另造一份重复实现：

- `check-design.mjs`：CSS、JSX 和治理规则的自定义检查入口。
- `mutation-runner.mjs`：隔离副本变异、原检查执行与结果收据。
- ESLint、TypeScript、Playwright 继续使用各自配置和 `package.json` 命令入口，不必把所有检查代码移入 scripts。
- 自定义规则单测留在 `tests/design/`；浏览器、axe、视觉测试留在 `tests/e2e/`；变异案例留在 `tests/mutations/`；注册表与状态清单留在 `governance/`。
- 研究和截图放 `exam/research/`，巡查职责放 `exam/agents/`，构建/打包输出是生成物，不放入 scripts 作为源码。

按稳定规则族组织少量检查器；每增加一种真实问题，优先新增规则测试、fixture 或受治理状态，不为每张截图或每个审计发现创建一套独立脚本。文档引用真实入口，不在 Markdown 中维护与源码重复的大段实现。

`design-system-guideline.md` 定义“必须遵循什么”；`design.md` 索引执行契约；`compliance-audit.md` 记录“在哪个版本和状态发现什么、由哪个检查捕获、输出如何证明”。审计文档是结果报告，不是第二份检查器源码。

## 建议交付包结构

保留当前 `exam/` 与 `creao-design-lab/` 的相对位置，以维持已有 `../creao-design-lab/`、`../exam/` 链接。以下为目标结构，新增入口/清单需在打包阶段生成，不表示已经存在：

```text
creao-design-submission/
  README.md                         # 评审阅读入口、复现步骤与范围
  manifest.json                     # 候选身份、逐文件大小与 SHA-256
  .github/workflows/creao-design.yml
  exam/
    design-system-guideline.md       # 必交正文
    compliance-audit.md              # 必交正文
    implementation-plan.zh-CN.md
    delivery-packaging-plan.zh-CN.md
    validation-results.zh-CN.md
    engineer-experiment-review.zh-CN.md
    agents/design-drift-auditor.md
    research/                       # 被正文引用的证据及必要上下文
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
    tests/                          # 含已审阅的视觉基线与环境信息
    experiments/                    # 协议、案例与精选持久结果
```

此树不是可直接用于打包的完整 allowlist。实际打包必须依据源码依赖、测试发现和文档链接生成完整文件集，不能遗漏 Next/TypeScript 所需配置、生成声明的再生步骤或被引用的 fixture。若要将两份正文额外置于 ZIP 顶层，应在 staging 中生成并重写链接，然后验证；不要移动工作区中的权威源文件或维护两套手改正文。

## 最终打包验收

1. 主线程冻结最终候选：记录 commit SHA；尚未跟踪的文件另用 content manifest 标识，不能把所在仓库 HEAD 冒充这些文件的版本。记录规则版本、lockfile 摘要、操作系统、Node、浏览器和视觉基线身份。
2. 区分两套清单：candidate manifest 标识最终源码；evidence manifest 标识历史和最终运行证据。修改最终文档后更新 manifest；manifest 的自校验摘要放外部收据，避免递归包含自身。
3. 按显式文件集组装 staging。排除 `.env*`/凭据、浏览器 profile/auth storage、`node_modules/`、`.next/`、缓存、临时副本和无关项目。逐项检查截图与 trace 是否含真实工作区私有内容；只加入与题目相关且适合提交的证据，不自动打包整个本机研究目录。合成原型与原站资料分开标记。
4. 保留首次漏检、复验、正例、负例和工程师实验结果；精简无关重复日志，但保留能复现和解释结论的命令、退出码、patch、完整 JSON、必要截图/trace。临时绝对路径不应是唯一证据入口；脱敏副本标注来源及变换，不覆写原始私有记录。
5. 在独立解压目录做验收：本地 Markdown 链接均可解析；依赖安装和文档列出的真实检查命令可执行；规则、状态与测试入口一致；没有依赖原机器的 `/tmp` 路径、外部 symlink 或未包含文件。
6. 截图基线按 OS/浏览器/字体环境分开，不能用 Mac 基线证明 Linux CI 通过。缺少对应已审阅基线时明确列为未配置/待审，不自动接受新图或静默跳过。正文说明哪些命令在什么环境已跑通。
7. 生成压缩包、包级 SHA-256、文件大小及复现收据，确认两份正式正文的结论与实际证据一致。最终入口清楚区分“源码可运行”“本地验证通过”“远端 CI 未执行”“生产未接入”。

本轮以源代码和可复现证据为主，不需要捆绑平台相关的 `node_modules` 或 `.next`。如另需部署产物，应以独立 artifact 标识其构建环境和摘要，并与经过检查的候选关联；不能把源码收据称作部署证明。GitHub artifact attestations 可作为后续可信来源增强，本轮不以引入签名基础设施阻塞交付。

## Programmatic rules 的确定性边界

固定输入、规则版本与环境后，AST、类型检查和明确的 DOM/行为断言能给出可复验结果；缺失标题、非法颜色、无名称按钮等适合硬门禁。浏览器和像素检查仍需控制时钟、字体、动画、数据、网络和版本。

视觉差异不自动等于错误，新功能也可能产生合理变化。层级是否清楚、布局是否适合任务、例外是否值得批准等保留设计评审。每日巡查 agent 负责选检查范围、解释证据、发现未覆盖风险；不能用一次模型判断覆盖确定性门禁，也不能自行修改基线来消除漂移。

## 主动巡查与交付包的关系

`agents/design-drift-auditor.md` 是可交接的数字员工职责文档，纳入补充交付。每日巡查应读取可信候选/上次成功游标、增量提交、规则与快照差异，调用同一组检查，并输出带版本身份的报告。

提交差异只是触发信号：依赖、部署、外部内容、字体变化可能在没有新 commit 时改变呈现；修改检查器或基线也可能让违规消失在报告中。因此需要周期性代表状态检查和治理变更审查，不能仅检索最近 24 小时的 commit 标题。

本次先交付职责和接入契约，不启动实际每日任务。后续可选择受保护 CI schedule + 手动触发 + agent 审阅；GitHub schedule 在默认分支运行且可能延迟，实际运行时间和遗漏必须进入报告。CI 合并前 gate 与每日巡查互补，不能用每日巡查替代上线前阻断。

## 官方技术依据

- [Playwright 视觉比较](https://playwright.dev/docs/test-snapshots)：基线及环境差异。
- [GitHub 定时工作流](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)：默认分支和调度延迟边界。
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)：构建来源证明；不能替代测试和复现步骤。
