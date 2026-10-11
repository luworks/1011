# CREAO Design Lab

一个将产品设计规范接入工程检查的本地 Next.js 实验。原型依据 CREAO 公开 Widgets 文档、已观察的产品页面与样式变量构建；使用合成数据，不连接真实业务系统，不冒充 CREAO 私有代码。

## 阅读顺序

1. [实施计划](../exam/implementation-plan.zh-CN.md)：目标、并行分工、验收与边界。
2. [design.md](design.md)：页面模式、CSS 索引、规则和来源。
3. [AGENTS.md](AGENTS.md)：编程智能体的工作契约。
4. [规则注册表](governance/rules.json)：检查范围、入口与局限。
5. [独立工程师实验协议](experiments/engineer-protocol.md)：与预设 mutation 分开的行为实验。

## 运行

环境：Node.js 24、npm。依赖使用 `package-lock.json` 固定。首次运行：

```bash
npm ci
npm run dev
```

浏览器打开 `http://localhost:3100`。页面包含 `/files`、`/connectors`、`/agents` 与 `/guidelines`。原型状态仅用于本地演示；刷新是否保留以实现说明为准。规范页提供阅读入口，实际约束由同版本的 CSS、组件和检查代码实现。

## 验证接口

以 `package.json` 的实际脚本为准：

```bash
npm run typecheck
npm run lint
npm run check:design
npm run build
npx playwright install chromium
npm run test:e2e
npm run test:mutations
```

静态设计检查验证受治理源码与 CSS。浏览器检查验证实际 DOM、交互和布局。Mutation 在临时副本改动真实实现后调用原有检查器；不会修改共享基线。结果中的 `killed` 必须是目标规则命中，编译失败、超时和执行基础设施错误分开统计。正例用于测量误报。具体命令和报告位置将在完成验证后补齐收据。

## CI 与发布边界

[GitHub Actions workflow](../.github/workflows/creao-design.yml) 使用相同命令，先运行基线门禁，再执行 mutation，最后准备候选资料。它目前只是本地配置文件；没有因为创建此文件就启用远端保护或发生部署。

真实接入需要仓库管理员完成：

- 将基线门禁与 mutation job 设为受保护分支的必需检查，并明确它们的可信工作流来源。
- 为规范、tokens、组件底座、规则、测试和 workflow 指定真实 CODEOWNERS，要求审批，限制自批准和直接绕过。
- 将发布绑定到通过检查的同一提交/构建产物；部署后执行受影响页面的 smoke check。
- 保护证据与基准更新流程。视觉快照不能由作者无解释地整体更新；例外需要范围、责任人和有效期。

这些是仓库设置和权限问题，无法仅靠 `AGENTS.md`、一份 YAML 或项目内可编辑的 hash 文件保证。此实验不替用户配置远端权限或部署。

## 如何理解结果

一个可执行设计契约有三类结论：

| 结论 | 所需证据 |
| --- | --- |
| 本次实现遵守已覆盖规则 | 固定候选的静态及浏览器检查通过，人工确认视觉和行为 |
| 检查器识别某类违规 | 有效基线 + 能编译的实现变异 + 对应规则失败 |
| 任意工程师无法绕过 | 此实验不能证明；需要权限边界、更广的覆盖与持续治理 |

文档一致性检查只能确认 ID、路径和格式，不能完全证明自然语言与代码语义等价。静态规则也不能穷尽任意 JavaScript/CSS 写法。浏览器验证只覆盖记录的页面、状态和视口。报告必须保留 survivors、invalid、error、未测项及人工判断。
