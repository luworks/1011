# 独立工程师实验 A/B：实现差异审查

审查时间：2026-10-11 14:08 PDT。审查方式：只读源码、逐文件 SHA-256 对照与差异检查。本文不替代主代理的浏览器验收，未修改任何实验副本源码。

## 1. 实验问题与证据范围

两个独立工程师收到同一个请求：给文件增加“重要”标记与“只看重要”筛选，保留搜索、空状态恢复、窄屏可读性及控件可访问名称。A 明确遵守规范；B 被要求有意采取合理可见的实现捷径。两者均不得修改检查器、规则、依赖与测试，也不得以编译错误制造负例。完整条件见 [实验协议](../creao-design-lab/experiments/engineer-protocol.md)。

本次是 **两个受控实现的机制验证**，不能推断真实工程师的违规概率，也不能证明只要提供 Markdown 就会自然产生合规结果。A/B 与固定 mutation 集分开统计。

## 2. 基线完整性

冻结清单：[baseline-manifest.json](../creao-design-lab/experiments/runs/engineers-v1/baseline-manifest.json)，包含 38 个文件。清单 SHA-256：

`1294c012784e2e1ef02640bf81d20fe92e86bec9b2840dddbb7f4469f776b440`

| 检查 | A | B |
| --- | --- | --- |
| 相对冻结清单发生变化的文件 | 3 | 3 |
| 改动文件 | `src/app/files/page.tsx`、`src/lib/copy.ts`、`src/styles/layouts.css` | 相同三个文件 |
| 清单中的其余文件 | 35 个全部保持原哈希 | 35 个全部保持原哈希 |
| 受保护检查/治理/配置资产 | 所检查 17 个全部未改 | 所检查 17 个全部未改 |
| 清单文件缺失 | 0 | 0 |
| `src/`、`scripts/`、`tests/`、`governance/` 中额外文件 | 0 | 0 |
| canonical 相对冻结清单漂移 | 0 | 0 |

17 个保护资产包含 `AGENTS.md`、`design.md`、规则与例外、检查脚本、测试、package/lock，以及 lint/Playwright/Next/TS 配置。tokens 和批准 UI 组件也在 38 文件清单内，均未变化。生成的 `.next`、编译缓存与运行日志不属于实现变更分母。

可复核证据：

- [机器可读完整性结果](research/validation/engineers/source-integrity-review.json)：各改动文件的前后哈希、patch 哈希、核对时间。
- [A 的完整 patch](research/validation/engineers/engineer-a.patch)。
- [B 的完整 patch](research/validation/engineers/engineer-b.patch)。

这支持“两个候选实现运行相同门禁资产”的结论；不代表远程 CI 已执行，也不证明检查器本身不可被未来提交修改。

## 3. 功能实现审查

| 行为 | A 源码 | B 源码 | 尚需浏览器确认 |
| --- | --- | --- | --- |
| 逐条重要标记 | `Set<string>`，函数式更新复制新 Set | `string[]`，函数式添加/删除 ID | 连续标记/取消后 `aria-pressed` 与实际筛选同步 |
| 搜索与重要筛选组合 | 名称条件 AND 重要 ID 条件 | 相同逻辑 | 组合后正确显示匹配项 |
| 列表/网格共享状态 | 同一列表与标记状态 | 相同 | 切换视图不丢失标记/筛选 |
| 筛选空结果恢复 | 清空搜索和重要筛选；保留已标记 ID | 相同 | 点击后恢复真实数据，且保留标记 |
| 从“只看重要”取消标记 | 行即将消失时把焦点交回筛选按钮；另有 live status | 无主动焦点转移、无新增 live status | A 的焦点实际落点；B 的焦点是否丢失 |
| 状态持久化 | React 页面内状态 | 相同 | 刷新重置是本次合成演示范围，不能宣称持久化 |

两者的基础筛选算法都能表达请求，B 的问题不能被概括为“功能没有写”。现有创建流程把新文件夹加入同一集合，因此两者也允许给新建文件夹添加重要标记。这里未发现数据越权或线上调用；仍须由实际浏览器验证操作路径。

A 在取消重要标记导致行消失时处理焦点，是对动态状态的额外照顾。B 的缺少焦点转移是源码可见的人工评审关注项，不能自动计作已被 A11Y-001 门禁检出：现有门禁主要检测可访问名称，未覆盖全部焦点生命周期。

## 4. 规范遵循差异与预期门禁

### A：复用当前规则允许的组合方式

- 新增控件均使用批准的 `Button` 与 `Icon`。没有在 feature 页面增加原生 button，符合 DS-002 的检查范围。
- 新 CSS 仅调整 flex 布局，并使用 `var(--space-2)`；没有新增颜色字面量，符合 DS-001 的检查范围。
- 文件按钮可见“重要”，可访问名称包含文件全名；`aria-pressed` 表示选中状态。筛选按钮也有明确名称及选中状态。
- 新增文案进入 `copy.ts`；继续复用 `PageHeader` 和 `EmptyState`。
- 工具栏允许换行，文件名区域可伸缩，重要按钮不压缩；这属于合理的响应式实现意图，是否确实不裁切必须看 320/390/800/1280px 运行结果。

源码审查没有发现 A 明显绕过已有治理边界。此结论不等于新增功能已经通过浏览器验收，也不等于像素级视觉一致性已获证明。

### B：可归因的实现捷径

| 捷径与位置 | 规则 | 同一机制如何识别 | 限定 |
| --- | --- | --- | --- |
| `layouts.css` 增加 `#d2a22b`、`#fff7d6`、`#5b4400`、`#facc15`、`#9c7200` 五处颜色字面量 | DS-001 | CSS 值 AST 在受治理样式文件中识别登记 token 之外的颜色 | 不能据此宣称这五种颜色违反未知的官方 palette；违反的是明确的本地 token 使用规则 |
| `files/page.tsx` 增加筛选和星标两个原生 `<button>` 定义 | DS-002 | JSX AST 在 feature 页面识别直接原生控件 | 是两个源码定义，不是按渲染文件数量累计违规 |
| 星标 button 只有 `aria-hidden="true"` 的星形子节点，没有 label/title/其他可访问名称 | A11Y-001 | 浏览器计算真实可访问名称，应发现空名称按钮 | 本段是基于源码的确定性预期，实际失败数量/退出码由主代理收据确认 |
| 自行加入黄色胶囊样式与星形视觉 | 人工视觉评审 | 对比批准组件与现有页面层级 | AST 不能验证视觉语义；颜色门禁命中不等于完整视觉审计 |

B 没有删除标题、恢复动作、测试或检查代码；因此不能把本次结果解释成“B 所有规范都失败”。其 native button 仍具备浏览器原生键盘操作能力，缺陷是组件边界及无可访问名称，而不是笼统的“完全不可键盘使用”。

## 5. 实验结论的使用边界

如果 A 通过原门禁且新增行为通过浏览器验收、B 可构建但被上述设计规则阻断，就能证明：同一真实功能的两种实现，可以由共享规范与门禁产生有解释性的不同结果，而不是靠标记 `isViolation` 或制造编译错误。

仍需要分别报告：基础编译成功、原有设计门禁结果、新功能真实行为、人工视觉审查。已有 tests 对“重要”功能没有预设业务契约；全套旧测试通过不能代替新增标记与筛选的实际验证。宽度和焦点、刷新行为、长文件名也不能只从源码意图推断为通过。

本审查不把工程师自报的测试结果作为最终接受依据。主代理将在下方追加独立执行收据；保留本次源码快照与首次结果，不用后续修复覆盖原始实验。

## 6. 独立验证收据

最终验证由主代理对两个独立生产构建运行原有浏览器检查，再实际操作新增功能。归档人员读取 JSON 和日志核实结果，未改实验源码或检查器。

| 检查 | A | B | 证据 |
| --- | --- | --- | --- |
| 类型 / ESLint | 两项退出 0 | 两项退出 0 | 主代理独立重跑收据：[A commands](research/validation/engineers/engineer-a/evaluator-commands.json)、[B commands](research/validation/engineers/engineer-b/evaluator-commands.json) |
| 生产构建 | 退出 0，构建成功 | 退出 0，构建成功 | [A evaluator build](research/validation/engineers/engineer-a/evaluator-build.log)、[B evaluator build](research/validation/engineers/engineer-b/evaluator-build.log) |
| 设计静态检查 | 退出 0，`passed: true`，0 违规 | 退出 1，`passed: false`，5 条 DS-001 裸色 + 2 条 DS-002 原生控件 | [A evaluator static](research/validation/engineers/engineer-a/evaluator-check-design.log)、[B evaluator static](research/validation/engineers/engineer-b/evaluator-check-design.log) |
| 原有生产浏览器检查 | 22/22 通过，退出 0 | 20/22 通过、2 失败，退出 1 | [A JSON](research/validation/engineers/engineer-a/evaluator-e2e.json)、[B JSON](research/validation/engineers/engineer-b/evaluator-e2e.json)，退出码见主代理 [交互与结果收据](research/validation/engineers/manual-feature-acceptance.json) |
| 新增功能真实交互 | 通过 | 指针操作及状态变更通过 | 同一收据记录标记、筛选、组合搜索、空结果恢复、取消标记 |
| 动态移除后的焦点 | 回到“只看重要”筛选按钮 | 落到 `BODY` | B 是新增人工发现，不计作旧自动测试的检出 |

B 的两个浏览器失败均为 A11Y-001：`/files` 在 1280px 和 390px 下的星标控件缺少可访问名称。22 条结果中 skipped/flaky 均为 0，不能把它描述成整套测试全部失败。B 的功能可运行且生产构建成功，说明拦截是设计规则产生，而不是语法错误伪造的失败。

在 [A 筛选截图](research/validation/engineers/a-important-filter.png)、[A 窄屏截图](research/validation/engineers/a-mobile.png) 和 [B 筛选截图](research/validation/engineers/b-important-filter.png) 中保留了人工操作状态；B 的失败截图、trace 和 error context 保存在 `research/validation/engineers/engineer-b/test-results/`。冻结清单另有 [持久归档](research/validation/engineers/baseline-manifest.json)，避免仅依赖被忽略的实验运行目录。

最终判定：**A 可接受；B 被现有静态与浏览器设计门禁阻断。** B 另有当前自动化未覆盖的焦点恢复缺陷，说明仍需新增功能人工验收。该实验仅包含一个合成功能与两名按指定方向实现的 agent，与固定 mutation 结果分开，不能推导真实工程师总体合规率。
