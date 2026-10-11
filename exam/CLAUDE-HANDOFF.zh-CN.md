# CREAO 设计规范实验：Claude 接手说明

更新时间：2026-10-11，America/Los_Angeles。本文件记录交接时的事实与剩余工作；最终运行结果以归档收据为准，不能从运行中推断通过。

## 交付身份与接手边界

- 工作区：`/Users/yuanlu/code/1011`；原型：`/Users/yuanlu/code/1011/creao-design-lab`；题目、研究及证据：`/Users/yuanlu/code/1011/exam`。
- 已有 checkpoint：`edd2ea0c416f664339b59e56d2bcabe35f287f4a`（`chore: checkpoint CREAO design lab and audit evidence`）；它不是本次最终打包提交。
- **最终提交 SHA：以 ZIP 外 `.receipt.json` 的 `sourceCommit` 和包内 `candidate-manifest.json` 为准；工作区执行 `git rev-parse HEAD` 读回（避免把文档自己的提交 SHA 递归写入提交）**。
- **全过程 ZIP 路径：`exam/delivery/creao-design-<sourceCommit前12位>.zip`，以最终回复及同名收据选择最终版本**。
- **ZIP SHA-256 / 清单位置：ZIP 同名 `.receipt.json` 保存包级 SHA-256；包内 `candidate-manifest.json` / `evidence-manifest.json` 保存逐文件摘要。包级摘要保存在包外，避免递归哈希**。
- 用户要求保留全部过程、提交并交接。这里的提交指本地 Git commit；没有 remote push、远端部署或生产修改的授权执行事实。不要将 checkpoint、ZIP 或本地绿色检查写成已上线。
- **必须等主 agent 确认现有 owner 全部结束、写入与测试进程已交代、最终 SHA/包清单已冻结后接手。** 不要与仍在运行的 mutation 或工程师实验并发改共享基线。若没有该确认，先只读核对状态。
- 保留 `task1/` 及所有无关工作。不要重置、清理失败证据或删除临时实验目录，除非确认所属 owner 已结束且证据已完整归档。

## 目标与先读顺序

题目主体必须是两份 Markdown，原型是验证附件：

1. [task.md](task.md)、[task.zh-CN.md](task.zh-CN.md)：原题与翻译。
2. [design-system-guideline.md](design-system-guideline.md)：产品层布局模式、规则、检查、审批与例外。
3. [compliance-audit.md](compliance-audit.md)：真实产品观察 → 规则 → 如何在上线前发现 → 本地证据。
4. [validation-results.zh-CN.md](validation-results.zh-CN.md)：已核实结果与失败历史；[implementation-plan.zh-CN.md](implementation-plan.zh-CN.md)：范围和交付矩阵。
5. [design.md](../creao-design-lab/design.md)、[AGENTS.md](../creao-design-lab/AGENTS.md)、[README.md](../creao-design-lab/README.md)、[package.json](../creao-design-lab/package.json)：实现入口、版本、命令和边界。
6. [delivery-packaging-plan.zh-CN.md](delivery-packaging-plan.zh-CN.md)、[设计漂移巡查职责](agents/design-drift-auditor.md)：全过程包与后续巡查契约。

用户确认没有其他附件。公开 sitemap、官方 Widgets 文档、截图和 DOM 研究已经完成，不要重新从头搜索 design.md，也不要以缺少私有库为理由停住。观察到的视觉值、官方 Widget 概念与本地提案已分开标记；本地适配组件不能冒充 CREAO 私有库。没有对 CREAO 线上数据执行创建、连接、上传或 agent 运行。

## 已有可信证据

以下是不同轮次的事实，不等于全部绑定最终提交；先核对对应 manifest/hash，再决定需重跑哪些受影响项。

| 证据 | 已核实内容 | 定位 |
| --- | --- | --- |
| v1 基线 | 类型/lint/静态检查/build 退出 0；检查器单测 8/8；生产 Chrome 浏览器 22/22 | `research/validation/baseline/`、`e2e-production-chrome.json` |
| 增强基线 | 检查器单测 13/13；类型/lint/静态检查退出 0；浏览器 38/38，含 axe 16 项 | `research/validation/phase-b/final-baseline/` |
| 静态 mutation 历史 | 首轮 5/6 killed，别名按钮 survived；修复后 6/6 killed；两轮正例均 2/2 | `research/validation/mutations-static-2026-10-11T21-03-48-256Z/` 与 `...21-06-12-461Z/` |
| 真实手动验收 | 文件创建/校验、预览 Escape 与焦点、模拟连接、智能体详情、源码查看；800px 溢出修复前后都留档 | `research/prototype/manual-review.json` 及 screenshots |
| axe | 三轮扫描保留；最终 16/16；滚动区键盘操作验证；非法 aria-pressed 负例有效命中 | `research/accessibility/README.md`、`negative-control/receipt.json` |
| 视觉 | 同一受审阅 macOS 环境普通比较 3/3；合法 token 的错误字间距被像素比较检出 | `research/validation/phase-b/visual/`、`phase-b/visual-negative/` |
| 独立工程师 v1 | A 原 gate 22/22；B 20/22，裸色/原生控件与无名称按钮被检出；功能与合规单独验收 | [engineer-experiment-review.zh-CN.md](engineer-experiment-review.zh-CN.md)、`research/validation/engineers/` |

v1 B 在筛选中取消标记后焦点落到 BODY 是人工发现，不能说原自动门禁抓到了它。React Doctor 有同一性能规则的 6 条 warning，归档无完整 CLI 评分；npm audit 全依赖有 5 个 high 条目归于同一 ESLint 工具链公告，生产依赖为 0，不能写成所有检查零问题。

首次缺少 Chromium、mutation 清理失败和运行中源码变化均已归档，不能计为设计 killed。保留 `research/validation/history/` 和首轮 survivor；后续修复永不覆盖先前结果。

## 交接时未完成或需最终核对

- **增强 A/B v2 已完成本轮评估。** A：38/38 浏览器与 axe，通过独立审阅功能新增截图后普通视觉比较 3/3；B：32/38，6 项失败（4 axe、2按钮名称），静态 7 项违规，视觉 1/3；B 未修复。两位是 v1 同一工程师复用功能，不算新的独立样本。证据见 `research/validation/engineers-v2/` 和最终评审。
- **最终冻结 mutation 按用户立即收口要求中止，属于部分完成。** 截至收口已知 9/12 预设负例 killed、2/3 正例 passed；其余 3 个负例 + 1 个正例 pending，以最终归档的 partial receipt 为准，不能报告整轮通过或 100%。Claude 首要任务是基于冻结源码核实剩余项，另开独立 run 保留本轮部分证据，不拼接成一次成功。
- 最终提交同时纳入文档、证据和 canonical tsconfig 排除 `experiments/runs/**` 的隔离修复；canonical 修复后 build 已退出 0。独立解压包对应 `5a91054`：238 个 Markdown 链接无损、安装/类型/lint/13单测/静态/build、38浏览器与axe、3视觉均通过。最终 ZIP 如包含后续变动，必须区分已测源码和最终文件身份。
- 核对最终提交、全过程 ZIP、归档 manifest/哈希和文件完整性。包中应包含主体、源码/锁文件/配置、研究、实验任务/补丁/收据、截图/trace、失败历史及本交接说明；不需要依赖目录或 Next 构建缓存。
- Linux CI **没有受审阅视觉基线，当前应 fail closed**。不要借用 Mac PNG、禁用 visual gate 或自动接受基线来让 CI 变绿。正确后续是固定 Linux 环境生成候选、独立人工审阅、提交审批证据、再正常比较。
- 没有远端 CI 执行、required checks、CODEOWNERS 实际保护、发布或生产 smoke 的完成证据。巡查仅有职责文件，**没有每日调度，也没有外部通知**；不要自行创建任务/调度或发送信息。

## 环境与确切复验命令

已归档环境：Node.js `24.21.0`、npm `11.19.0`；项目约束 Node 24；Next `16.4.0`、React `19.3.0`、Playwright `1.64.0`、axe Playwright `4.13.0`。以锁文件及环境收据核验。macOS arm64，系统 Chrome `154.0.8037.98`，受审阅视觉 namespace 为 `darwin-arm64-25.6.0-chromium-154.0.8037.98`；设备模拟 UA 不是浏览器版本证明。

确认没有其他 owner 使用端口 3100/共享构建目录后，从项目目录执行；每轮将日志另存时间戳目录。依赖已可用时无需为证明动作机械重复安装；干净接手环境使用 `npm ci`。

```sh
cd /Users/yuanlu/code/1011/creao-design-lab
npm ci
npm run typecheck
npm run lint
npm run test:design
npm run check:design
npm run build
PW_CHANNEL=chrome PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:e2e
PW_CHANNEL=chrome VISUAL_ENV=darwin-arm64-25.6.0-chromium-154.0.8037.98 PW_SERVER_COMMAND='npm run start -- --hostname 127.0.0.1 --port 3100' npm run test:visual
PW_CHANNEL=chrome npm run test:mutations
```

上述 visual namespace 只能在**真实环境完全匹配**时使用，不可用环境变量伪造匹配。其他环境需自己的受审阅 baseline。Linux 的浏览器安装命令是 `npx playwright install --with-deps chromium`，但安装浏览器不解决视觉 baseline 缺失。默认 `test:e2e` 不包含 visual，后者单独运行；生产模式必须明确 `PW_SERVER_COMMAND`。独立副本可用自己的端口和构建目录，不能复用正在写入的共享 `.next`。

**禁止失败后自动 `--update-snapshots`。** 候选截图生成不是通过；合法功能变化也须保存 expected/actual/diff、说明变化、独立审阅后更新，之后普通模式重新验证。不要修改 agent 的原检查资产来让其实现通过，不要混合固定 mutation、独立工程师、axe 负例和视觉负例的分母。

## 可直接复制给 Claude 的启动 prompt

> 接手 `/Users/yuanlu/code/1011` 的 CREAO 产品设计规范与执行实验。先读 `exam/CLAUDE-HANDOFF.zh-CN.md`、两份必交 Markdown、`exam/validation-results.zh-CN.md` 和 `exam/implementation-plan.zh-CN.md`，再读原型 AGENTS/design/README。先确认原 owners 全部结束、最终提交与 ZIP/manifest 身份一致，再进行任何写入。不要重复公开资料研究，不要重置历史失败，不要自动更新视觉快照。优先核实最终冻结 mutation 和增强 A/B v2 是否已有完整收据，未完成如实列出；核对它们与最终源码的身份，完成必要的受影响路径复验与文档一致性收口。Mac Chrome 154 的视觉基线不能冒充 Linux；Linux 无受审阅基线应保持 fail closed。两份主体是最终题目答案，原型和全部实验过程是支持附件。保留无关文件和全部首轮漏检/失败记录。本次无 remote push、部署、每日调度或外部通知动作。解释用中文，代码/标识符用英文；汇报真实已完成、尚未验证、精确文件/命令/退出码和交付 SHA，不从运行中预判通过。


收尾进程状态：主代理已核对本任务工作目录后关闭 3105、3120、3110、3111 预览服务；mutation owner 已停止本轮 runner 并清理其自有服务。没有继续写入源码的 owner。Claude 如需预览，应从项目目录自行 `npm run dev` 或构建后 `npm run start`，先核实端口空闲。
