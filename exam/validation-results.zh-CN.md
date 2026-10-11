# CREAO 设计约束：验证与实验结果

日期：2026-10-11。状态：持续更新，尚未完成最终验收。本文件记录已经拿到的运行证据，配合 [实施计划](implementation-plan.zh-CN.md)、[产品设计规范](design-system-guideline.md) 和 [合规审计](compliance-audit.md) 使用。

## 结果总表

| 验证层 | 当前已核实结果 | 证据 / 后续验收 |
| --- | --- | --- |
| 类型、通用 lint、生产构建 | 三项命令均退出 0 | [commands.json](research/validation/baseline/commands.json) 与对应日志 |
| CSS / JSX / 治理检查器单测 | 8/8 通过；全项目设计检查退出 0、无违规 | [单测日志](research/validation/baseline/test-design.log)、[设计检查日志](research/validation/baseline/check-design.log) |
| 原型浏览器基线 | 生产构建 22/22 通过；0 skipped、0 flaky | [Chrome channel 生产报告](research/validation/e2e-production-chrome.json)；bootstrap 缺浏览器失败单独保留 |
| 原型人工截图验收 | 桌面与 390/320px 检查通过；800px 初次溢出，修复后复验通过 | [人工验收收据](research/prototype/manual-review.json)，保留修复前后截图；创建、预览、恢复与详情实际操作已验 |
| React Doctor | 已归档 6 条 warning、0 条 error，全部属于同一性能规则 | [diagnostics.json](research/validation/react-doctor/diagnostics.json)；保留告警，不写成零问题 |
| 固定 mutation：首轮静态 | 6 个负例：5 killed、1 survived；2 个正例均 passed；0 invalid、0 error、0 false-positive | [首轮 report.md](research/validation/mutations-static-2026-10-11T21-03-48-256Z/report.md) / [原始 JSON](research/validation/mutations-static-2026-10-11T21-03-48-256Z/report.json) |
| 固定 mutation：静态第二轮 | 6/6 killed、2/2 正例通过，0 survived/invalid/error/false-positive | [第二轮 report.md](research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.md) / [原始 JSON](research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.json) |
| 固定 mutation：浏览器 | 前两轮各 7 invalid；没有可用设计拦截分母，最终复验待报告 | 两轮基础设施/基线失效历史已归档，不算 killed |
| 独立工程师合规实验 | A：22/22 浏览器通过且静态 0 违规；B：静态 7 违规、浏览器 20/22 通过、2 条 A11Y 失败 | [独立实验审查](engineer-experiment-review.zh-CN.md)；两者新功能可用，B 的焦点丢失为人工额外发现 |
| GitHub CI / CD | v1 三 job YAML 解析通过；增强版增加 visual-gate，新的运行/解析证据待归档 | [v1 解析收据](research/validation/baseline/workflow-parse.json)；远端执行与保护设置未核实 |
| 依赖审计（独立于设计规则） | 全依赖 5 high，生产依赖 0；5 项属于同一 braces 开发工具依赖链 | [完整 audit](research/validation/baseline/npm-audit.json)、[生产 audit](research/validation/baseline/npm-audit-production.json) |

## 基线命令与浏览器结果

[环境收据](research/validation/baseline/environment.json) 记录 macOS arm64、Node v24.21.0、npm 11.19.0，以及精确包版本。[命令收据](research/validation/baseline/commands.json) 记录 `npm run typecheck`、`npm run lint`、`npm run test:design`、`npm run check:design`、`npm run build` 全部退出 0。单测为 8/8 通过，构建日志显示 Next.js 16.4.0 生产构建成功。该收据未包含安装命令，因此不从它推断一次新的 `npm ci` 已完成。

[生产浏览器报告](research/validation/e2e-production-chrome.json) 的运行时间为 `2026-10-11T21:05:33.253Z`，22 个预期通过、0 unexpected、0 skipped、0 flaky，报告配置使用 `channel: chrome`，并由 `npm run start -- --hostname 127.0.0.1 --port 3100` 启动生产服务器。[本机浏览器版本收据](research/validation/browser-environment.json) 为 Google Chrome 154.0.8037.98；浏览器报告中的设备模拟 user-agent 不是实际浏览器版本收据。

[初次 bootstrap 失败报告](research/validation/e2e-bootstrap-missing-browser.json) 保留了 20 次缺少 Playwright Chromium 可执行文件的启动失败；这些是基础设施失败，测试未进入产品行为断言，不能计为 20 个设计违规，也不能计入 mutation killed。随后生产服务器上的 Chrome channel 运行是另一轮独立证据。Linux CI 默认安装和运行 Playwright Chromium，尚未取得该远端环境的结果。

## 人工截图与真实交互

[人工验收收据](research/prototype/manual-review.json) 来自 `http://127.0.0.1:3105` 的生产构建；使用合成数据和页面内临时状态。已操作验证文件夹名称校验/创建、预览 Escape 关闭与焦点恢复、连接器空状态恢复与本地模拟连接、创建智能体示例与查看详情、规范页 Markdown 表格及受控 CSS 源码链接。

文件列表在 390×844 和 320×844 的检查通过。800×900 初次发现页面宽度 806px，属于真实布局问题；将集合布局断点调整为 900px 后，复验页面宽度为 800px。保留 [修复前截图](research/prototype/files-800.png) 和 [修复后截图](research/prototype/files-800-fixed.png)。这组人工截图与自动断言分开报告；没有执行真实 OAuth、模型运行，也没有覆盖所有语言或完整读屏器测试。

## 首轮 mutation：真实漏检记录

运行时间：`2026-10-11T21:03:48.272Z` 至 `2026-10-11T21:04:01.856Z`（UTC）。这是固定静态 mutation 集，不包含浏览器 mutation，也不包含独立工程师实验。

基线摘要与运行后摘要相同：`7679d8f01d6b3b6bc686a43ab854abd1b9d9e91d67c03a540e5b0969ba8f8727`。原报告的 `baselineUnchanged` 为 `true`。8 个变更案例均通过类型检查；首轮没有把编译失败或超时当成拦截成功。

| 变更 | 目标规则 | 实际分类 | 含义 |
| --- | --- | --- | --- |
| 页面样式加入十六进制裸色 | DS-001 | killed | 原检查器返回目标规则违规 |
| 页面样式加入 RGB 裸色 | DS-001 | killed | 原检查器返回目标规则违规 |
| 使用未登记 CSS token | DS-001 | killed | 原检查器返回目标规则违规 |
| 绕过组件使用原生 button | DS-002 | killed | 原检查器返回目标规则违规 |
| 将原生 button 赋给别名后渲染 | DS-002 | **survived** | 类型检查通过，设计检查退出 0；首轮真实漏检 |
| 使用过期例外 | GOV-001 | killed | 治理检查发现例外过期，裸色违规亦未被豁免 |
| 换成另一个已登记 token | DS-001 | passed | 合理修改被接受 |
| 使用批准 Button 的 primary variant | DS-002 | passed | 合理修改被接受 |

负例分母为 6，首轮拦截率为 **5/6（83.3%）**。正例分母为 2，接受率为 **2/2**；两种分母不能混用。这个样本只能证明已测试写法的能力，不能说明任意绕过方式均已受控。

## 静态第二轮：别名漏洞修复后复验

[第二轮原始报告](research/validation/mutations-static-2026-10-11T21-06-12-461Z/report.json) 在相同 6 个负例和 2 个正例上运行。6 个负例全部 killed，2 个正例全部 passed，survived / invalid / error / false-positive 均为 0。原生控件别名这一首轮漏检本轮已命中 DS-002；首轮报告仍保留，不以复验覆盖历史。

第二轮前后基线摘要同为 `cd142735527fc9cfbfbb8702273efc04c2b43e923a001f8fcefe958d2c09649e`，`baselineUnchanged: true`。新增的词法符号别名检查及局部同名标识符测试在 8 项单测中有直接覆盖；这不能推导出对跨模块别名、任意动态组件或 CSS-in-JS 的完整约束。

## 浏览器 mutation 的失效运行历史

两轮运行均未形成可用于设计检出率的有效分母：

| 历史运行 | 分类 | 原始原因 | 证据 |
| --- | --- | --- | --- |
| 21:06:28 UTC | 7 invalid，0 killed，负例有效分母 0 | 基线清理 `.next/dev/cache` 遇到 `ENOTEMPTY`；前后源摘要一致 | [report.json](research/validation/history/mutations-browser-2026-10-11T21-06-28-718Z/report.json) |
| 21:14:14 UTC | 7 invalid，0 killed，负例有效分母 0 | 运行期间共享源码摘要改变，hash guard 判定所有案例无效；`baselineUnchanged: false` | [report.json](research/validation/history/mutations-browser-2026-10-11T21-14-14-207Z/report.json) |

每轮为 6 个负例与 1 个正例受同一个运行级问题影响，不是发现了 7 个独立产品缺陷。它们不进入设计规则 killed/survived 的分母。之后的冻结基线复验应另存目录，不能覆盖失效历史。

## React Doctor 告警

[原始规则报告](research/validation/react-doctor/react-doctor--js-set-map-lookups.txt) 和 [机器可读诊断](research/validation/react-doctor/diagnostics.json) 记录了 `src/app/connectors/page.tsx` 第 12、15 行的 6 个 `js-set-map-lookups` warning：循环内重复调用数组查找可能在数据规模增大时产生额外开销。诊断中没有 error。

这份归档没有 CLI 完整标准输出、退出码或评分，因此不从它推断 React Doctor 总分或整个命令的完成状态。告警是否需优化及后续复验由最终集成报告说明；它不是已观察到的用户交互失败。

## 独立工程师实验

[完整 A/B 审查与独立收据](engineer-experiment-review.zh-CN.md) 保存同一“重要标记与筛选”功能的两种实现。两者均可生产构建，人工指针交互与状态变更均可完成。A 复用批准组件与 token，静态 0 违规，原有生产浏览器检查 22/22 通过。B 的 5 处裸色与 2 个原生控件定义被静态规则检出，原有浏览器检查在桌面和窄屏发现无名称星标按钮，20/22 通过、2 条 A11Y-001 失败。

[完整性收据](research/validation/engineers/source-integrity-review.json) 核实每个候选只变更 3 个功能文件，17 项保护资产均未修改。B 在取消标记导致当前行消失后焦点落到 `BODY`，由主代理操作发现；现有自动化没有覆盖此新功能焦点生命周期，不能冒称自动门禁已抓到它。这个实验单独统计，不加入 mutation 的负例分母。

## CI 与依赖边界

[v1 CI 语法解析收据](research/validation/baseline/workflow-parse.json) 确认当时三阶段 job 存在，candidate 同时依赖 design-gate 与 mutation-verification。后续增强版已计划加入 visual-gate，其收据与 v1 分开保存；Linux 没有已审阅像素基线时必须 fail closed，不能把待基线接入状态说成 CI 已通过。YAML 能解析不代表 GitHub 已执行；required checks、分支保护、环境审批和部署仍未接入。

[npm audit 原始结果](research/validation/baseline/npm-audit.json) 为 5 个 high 条目，追溯到 ESLint 工具链中的同一个 `braces` 公告 [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm)，并非 5 个独立根因。[生产依赖 audit](research/validation/baseline/npm-audit-production.json) 为 0。完整 audit 的非零结果保留为依赖风险，不能说全项目所有检查零问题，也不将它混入设计 mutation 的拦截分母。报告建议的修复涉及 `eslint-config-next` 跨主版本调整，未盲目执行自动降级。

## 增强阶段 B（独立报告，待验证）

增强副本计划执行 16 项 axe 检查与 3 项视觉检查。这是另一阶段的覆盖扩展，当前没有最终运行收据，不计入 v1 的 22 项浏览器结果或固定 mutation 分母。后续只新增独立结果，不覆盖 v1 首轮与复验历史。

## 最终待补充的收据

- 安装收据与最终整体验收：已归档的五项基线命令及生产浏览器结果见上；后续变更如影响这些路径需对应复验。
- 浏览器 mutation：逐例分类、准确分母、目标规则、不可变报告路径、基线摘要。
- 独立工程师实验最终命令已补齐：[A](research/validation/engineers/engineer-a/evaluator-commands.json) 类型/lint/设计检查/build 全退出 0；[B](research/validation/engineers/engineer-b/evaluator-commands.json) 类型/lint/build 退出 0、设计检查退出 1。
- 视觉与交互的最终范围：上面已归档人工验收；若最终实现继续变化，应按受影响路径复验。
- CI：本地已验证命令与尚未接入的远端执行、required checks、审批和部署步骤分别记录。

## 归档约定

原始证据保存在 [research/validation/](research/validation/)，文件大小与 SHA-256 见 [archive-manifest.json](research/validation/archive-manifest.json)。每次新运行使用独立时间戳目录；不覆盖首轮漏检，不以更好的后续结果改写早期结果。当前归档仅包含本地原型的检查报告、合成实现片段和本机路径，没有复制 CREAO 真实用户数据。原始报告内临时目录可能已经移除，审阅应以这里保留的报告、补丁内容和收据为准。
