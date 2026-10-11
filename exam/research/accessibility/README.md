# 自动无障碍验证记录

环境：macOS、本地生产模式 Next.js、系统 Chrome `154.0.8037.98`、Playwright `1.64.0`、`@axe-core/playwright` / axe-core `4.13.0`。这不是远端 CI 运行或完整 WCAG 认证。

## 基线验证与真实修复

1. `axe-baseline-20261011T211342Z/report.json`：16 个测试中 13 通过，2 个因测试 locator 与 Next.js 自带 route announcer 的 `role=alert` 冲突，在扫描前失败；1 个是窄屏 Guidelines 的四个横向滚动表格不能键盘聚焦，axe 规则 `scrollable-region-focusable`。两类失败明确分开。
2. `axe-baseline-v2-20261011T212200Z/report.json`：精准限定表单错误定位到 `main` 后，表单两态通过；原表格加 `tabIndex=0`，Files 的视图切换容器加 `role=group`。14/16 通过；Guidelines 新增长代码块在两个视口下因 `pre` 不能键盘聚焦而失败。继续修复实际源码，不过滤规则。
3. `axe-baseline-v3-20261011T212800Z/report.json`：`pre` 同样可聚焦后 **16/16 通过**，退出 0。`scan-summary.json` 按状态记录自动结果及 incomplete。`keyboard-scroll.json` 额外验证窄屏 table/pre 聚焦后按 ArrowRight，真实 scrollLeft 分别增长到 35/30；这说明键盘恢复实际生效。

每轮报告中的 `axe-*` JSON 附件包含所有 passes、incomplete、inapplicable、violations；首轮 ID 为 A11Y-001，注册新规则后仅将 axe 测试标题统一为 A11Y-002。初始的两个 locator 错误不算产品违规或 mutation kill。

## 新 gate 负例实验：独立分母 1

`negative-control/receipt.json`、`source.patch`、`axe-results.json`、`negative-report.json` 及 artifacts 保存真实证据。

- 仅在独立副本将 Files 列表视图按钮的 `aria-pressed` 改为运行时非法值 `sometimes`，用显式类型断言保留编译能力。未修改测试、规则或扫描器。
- TypeScript 检查退出 0。首次 Turbopack 构建因实验副本的 node_modules symlink 超出根目录而失败，单独记为基础设施尝试失败；随后 `next build --webpack` 退出 0。
- 页面 HTTP 200、标题和 h1 正常，浏览器读回真实 DOM `aria-pressed="sometimes"`。
- 原样初始 Files axe 测试退出 1，实际得到 `aria-valid-attr-value` critical 违规，目标准确指向列表视图按钮。因此本组为 **1/1 killed**，不是编译失败或超时制造的“成功”。不混入原有设计 mutation 的分母。
- 运行后已关闭独立 3121 服务。报告保存的源码 SHA 与测试 SHA 可用于独立复核。

## incomplete 人工复核

- 初轮 `.view-toggle` 在无 role 的 div 上设置 `aria-label` 被 axe 标为 `aria-prohibited-attr` incomplete；人工确认并通过 `role=group` 修复。
- Dialog 的 `color-contrast` incomplete 原因是 axe 无法从 top-layer/overlap 确认背景。`dialog-manual-v2-1280.png`、`dialog-manual-v2-390.png` 已逐张检查，预览正文及说明无遮挡。`dialog-computed-styles-v2.json` 保存了实际可见元素坐标与颜色；正文 #16181a / #f8f6f3 的对比度为 16.50:1，说明 #66635e / #fefdfb 为 5.88:1，均超过普通文字 4.5:1。
- 最终 Guidelines 窄屏仍有 61 个单元格因横向滚动容器裁剪而得到 `color-contrast` incomplete。`axe-baseline-v3-20261011T212800Z/guidelines-incomplete-computed-review.json` 逐个记录实际前景色、祖先背景和计算结果：没有渐变、背景图片或透明度叠加；最低计算对比度 16.50:1。`guidelines-clipped-cell-revealed.png` 已查看，代表性单元格能通过原生滚动呈现。这里是计算样式与抽样画面复核，不宣称已对全部 61 个单元格逐一截图或由 axe 自动确认。
- 名称含 `dialog-manual-` 但没有 `v2` 的两张截图及对应首次 computed-styles 是一次未等待 dialog 显示完成的人工采集尝试：坐标为零、截图仅有列表，**不作为 dialog 通过证据**；保留是为了说明采集修正。
- 自动零违规不代表所有无障碍要求均已验证；屏幕阅读器、完整键盘旅程与未枚举状态仍在覆盖边界之外。

API依据：[Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)、[Deque Playwright integration](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md)。
