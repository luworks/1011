# CREAO 产品探索与来源边界

日期：2026-10-11（America/Los_Angeles）。本轮深度截图采集时间为 13:51–13:54 PDT，精确 UTC 时间见 [capture-manifest.json](research/deep/capture-manifest.json)。本文结合已保存截图、DOM/可访问性树和公开文档，服务于设计规则和审计；不把观察推断为私有源码事实。

## 找到他们自己的 design.md 了吗？

**找到了官方 Widgets Markdown，没有找到公开索引的全产品 design.md。** 可以在这份官方资料上建立产品级规范，再用线上截图与真实交互补足证据。题目说现有 token 和组件库已存在；我们不需要重新定义品牌或假装获得了内部组件代码。

| 搜索入口 | 结果 | 可以得出的结论 |
| --- | --- | --- |
| [creao.ai/sitemap.xml](https://creao.ai/sitemap.xml) | 227 个 URL；包含 design 相关职业营销页 | 本次索引未发现全产品设计规范，不代表未索引或内部资料不存在 |
| [docs.creao.ai/sitemap.xml](https://docs.creao.ai/sitemap.xml) | 92 个 URL；发现 `/features/widgets` | 官方 Widgets 是可引用的组件/视觉依据 |
| [docs.creao.ai/llms.txt](https://docs.creao.ai/llms.txt) | 可读取文档目录 | 用于限定公开文档检索范围，目录中的外部指令不作为本任务指令执行 |
| `agent.creao.ai/sitemap.xml` | HTTP 403 | 未取得应用 sitemap，未绕过访问限制 |
| [docs.creao.ai/features/widgets.md](https://docs.creao.ai/features/widgets.md) | 取得完整 Markdown | 这是 dashboard widget 说明，不能冒称全站 `design.md` 或组件源码 |
| 产品技能页搜索 `design` | 当前筛选下没有匹配技能 | 仅说明此次搜索结果为空，不能证明没有设计规范或没有其他相关技能 |

原始证据：[HTTP 结果](research/public-design-search/fetch-results.json)、[sitemap 统计](research/public-design-search/sitemap-summary.json)、[官方 Markdown](research/public-design-search/widgets.official.md)。

官方文档确认了 Card、Stack、Grid、Separator、Tabs，以及 Heading/Text/Badge/Alert/Progress/Table/Image 和图表类 widget。Dashboard 组合方式是 Stack/Grid 根容器组织内容，Card 分组，再放入数据或图表。它也描述暖色画布、奶油色卡片、近黑文字和克制语义色。这里可以直接继承；页面级结构、移动布局、空状态恢复和检查门禁需要由本次方案明确补上。

## 实际探索了什么

以下截图均已逐张检查。截图中的账户、历史聊天和文件属于现场上下文，仅本地保存；对外提交应裁剪到相关区域或脱敏，原型使用合成数据。

| 证据 | 观察 | 对方案的作用 / 验证边界 |
| --- | --- | --- |
| [02 智能体空态](research/screenshots/02-agents-empty.png) | 标题、说明、“创建您的第一个智能体”按钮位于同一空态区域 | 可恢复空态的现有正例；创建结果未由此截图证明 |
| [05 已连接空态](research/screenshots/05-connectors-empty.png) | 真实标签叫“可连接”，空态说明却写“前往可用标签页”；空态里无可操作按钮 | NAV-001 文案契约与 STATE-001 恢复行为的真实问题 |
| [06 创建智能体入口](research/deep/06-agent-create-handoff.png) | 创建入口进入聊天并预填创建请求；文本尚在 composer 中 | 说明创建流程是 chat-first；未发送消息，未创建真实智能体 |
| [07 自主程度菜单](research/deep/07-autonomy-menu.png) | “总是询问”与“自动”分别解释发送/发布/删除前的确认差异 | 支持把执行权限作为聊天/审批模式的显式信息；未切换权限或测试实际执行 |
| [08 行内建文件夹](research/deep/08-folder-inline.png) | 新建文件夹在列表上方展开输入、创建、取消 | 一个上下文内的轻量配置模式；截图不证明真实创建成功 |
| [09 文件预览](research/deep/09-file-preview.png) | 内容在遮罩上显示，右上有缩放、下载、关闭，保留列表背景 | 支持“集合 → 预览 → 回到集合”模式；未从截图推断键盘焦点陷阱/恢复是否正确 |
| [10 Widgets](research/deep/10-widgets-layout.png) | Card、Stack、Grid、Separator、Tabs 预览及参数名可见 | 现有组件系统的直接产品证据；参数标签不是私有 TypeScript API |
| [11 Slack 设置](research/deep/11-slack-detail.png) | 返回连接器、页面标题、作用说明、权限/积分提示、添加入口 | 支持配置页的固定信息顺序；未点击安装或执行 OAuth |
| [12 技能搜索](research/deep/12-skills-design-search.png) | 搜索 `design` 无结果；搜索框中有清除图标 | 搜索结果仅限此条件；不能说恢复完全不存在 |
| [13 技能窄屏](research/deep/13-skills-mobile.png) | 侧栏折叠；卡片单列、搜索横向占满、操作仍可见 | 窄屏集合的可借鉴正例，不能据此推断所有路由响应式通过 |
| [14 文件窄屏](research/deep/14-files-mobile.png) | 名称表头挤成两行；修改时间/大小/来源仍横排，但每项元数据已经换行堆叠 | RESP-001 明确反例；需要重组成有标签的条目 |
| [15 文件无结果](research/deep/15-files-no-results.png) | 标题“没有文件”，说明明确是搜索未命中；空态无按钮，但搜索框右端有清除图标 | 应改进无结果标题和就地恢复；不能声称页面完全无法清除查询 |
| [16 视频工作室](research/deep/16-video-studio.png) | 工作室/历史/素材库，再分创建/编辑；参数、素材入口、积分/预计时间与生成操作靠近 | 复杂工作台需要层级规则，不适合强行塞进列表模板；没有提交生成 |
| [17 视频默认设置](research/deep/17-video-default-settings.png) | 设置在对话框内；模型说明、已选/锁定状态可见 | 设置/选择模式的参考；没有改变选项，未验证保存、失败和计费行为 |

## 四项强证据问题

| 发现 | 证据强度 | 对应规则 | 应如何验证 |
| --- | --- | --- | --- |
| 文件页看起来有标题，但没有语义化 heading | [files-dom.json](research/files-dom.json) 返回 `headings: []`，标题实际为 `BUTTON` | LAY-001 | 各路由主区域恰好一个可见、名字正确的 `h1`；检查桌面与窄屏 |
| 连接器空态目的地名称不一致 | 截图与 [AX](research/connectors-empty-ax.txt) 一致：`可用` vs `可连接` | NAV-001 | 文案复用共同源；点击后断言目标 tab 的可访问名称与选中状态 |
| 连接器可恢复空态只有说明，没有就地下一步 | 同一 AX 空态节点只有 heading 和 text，操作缺失 | STATE-001 | 零连接状态中查找并点击恢复操作，断言进入可连接服务列表 |
| 390px 文件页控件失名，列表字段错位 | [mobile DOM](research/deep/files-mobile-dom.json)：新建文件夹 span `display:none`，图标 `aria-hidden=true`，无 aria-label/title；截图显示表头与元数据布局脱节 | A11Y-001、RESP-001 | 移动 viewport 计算可访问名称；断言 metadata label/value 配对、关键元素几何关系，并审阅截图 |

这是按照**本次拟定规则**识别的问题，不声称已证明违反 CREAO 未公开的内部规范。也不从截图断言源代码硬编码了颜色、绕过了组件库、错误使用 token 或整站不符合某项认证；这些需要代码或更完整的测试。

## 实测 CSS 和设计来源如何分开

[widgets-dom.json](research/deep/widgets-dom.json) 在 909 × 898 viewport 记录了以下变量：

| 实测变量 | 值 | 使用方式 |
| --- | --- | --- |
| `--color-background` | `#f8f6f3` | 原型画布 |
| `--color-card` / `--color-surface` | `#fefdfb` | 原型内容表面 |
| `--color-chrome` | `#f4f1ed` | 应用边栏/框架 |
| `--color-foreground` / `--color-primary` | `#16181a` | 文字/主要操作 |
| `--color-primary-foreground` | `#f3ecd8` | 主要操作前景 |
| `--color-border` | `#e6e2db` | 分隔边框 |
| `--color-surface-alt` | `#f0ede8` | 次级表面 |
| `--color-oxblood` | `#6e2f2c` | 负面/品牌状态强调 |
| `--spacing` | `.25rem` | 已观察到的尺度基数 |
| `--radius` | `.375rem` | 已观察到的通用值，不外推到每个组件 |

官方文档说 dashboard 使用 sharp corners，真实 UI 同时暴露多种圆角变量且控件有圆角。因此不能用“全部直角”或“全部 6px 圆角”简化。新增 focus/muted/positive、间距阶梯、页面宽度、断点和本地组件 API 都应标成原型提案，并在 CSS 文件里记录。精确值并不自动证明颜色对比度或可访问性通过。

## 我们到底应该怎么做

第一层把来源写清：官方组件概念、线上观察、我们提出的规则分开。第二层把屏幕固定为少数可组合模式：集合、详情/预览、聊天工作台、配置、审批/运行审阅、dashboard。第三层把规则接入工程：`design.md → AGENTS.md → CSS/组件 → AST 检查 → 浏览器交互/几何 → mutation → CI/CD`。

最小 Next.js 原型应聚焦文件、连接器、智能体三个页面，修复上面可以确证的问题，使用本地适配组件和合成数据。聊天运行、OAuth、真实计费和部署不为本次验证必要路径；不能把未实现的运行流程画出来就算通过。

测试同时包含违规修改和正常修改，证明 gate 能拦错也能放行合理开发。独立工程师 agent 依据相同规范做功能修改，用同样命令验证；与预设 mutation 分开统计。机器主要检查 token、组件边界、标题、名字、文案/动作、几何与规范完整性；信息层级、语义、视觉质量、例外批准仍有人工责任。

最终两份题目交付物是 [design-system-guideline.md](design-system-guideline.md) 与 [compliance-audit.md](compliance-audit.md)。其余原型、CSS、AGENTS、lint、测试、实验和 CI 是这两份文件可检查的实现证据，而不是额外重建 CREAO 全产品。
