# Human exceptions and scoped bypass

版本：2026-10-11。本文定义人工特例的目标契约；主线程负责 CI、审批适配器和测试集成。未经实际运行证据，不得把本契约标成已启用的远端放行能力。现有 `exceptions.json` 的 DS-001/DS-002 精确文件豁免仍是旧接口，不要把下述扩展字段直接写入其旧 schema。

## 原则与适用情况

系统默认给出合规修复建议，但允许负责人因重要功能、限时试验、规则误报或真实产品取舍，明确接受已知设计偏离。工程师不必反复说服 agent；有效批准一旦存在，coordinator 应执行范围内的放行，不再次索要同一批准。

人工 bypass 是受限的发布接受决定，不删除失败、不关闭整套 QA、不修改截图基线、不把被豁免的检查改写成通过。最终状态为 `accepted_with_exceptions`，与 `passed` 分开。规则本身不因此成为可选项，也不自动扩展为所有后续提交的许可。

允许范围：布局、组件/token 用法、文案/恢复流程、可访问性规则的明确实例，以及经人工审阅的视觉差异。浏览器/axe/视觉发现不应永远排除在特例流程外。每项需要说明用户影响和替代验证；严重影响核心操作或可访问性的例外走紧急审批等级。

不能用设计特例抹去：审批来源无效、范围或目标不匹配、记录被改写、过期/撤销、构建不可执行、报告缺失、浏览器未启动、目标状态未执行、未知额外失败。它们应报告 `rejected`、`blocked` 或 `not_verified`，而非设计规则通过。若发布负责人仍决定在未验证条件下发布，那是另行明确记录的发布决策，不能冒称本设计门禁完成或由 engineer/agent 自行推定授权。

## 谁申请、谁批准

| 角色 | 权限 |
| --- | --- |
| Engineer / coding agent | 运行检查、准备申请、给出修复建议及取舍；不能自填批准身份完成授权 |
| Coordinator | 汇总证据、生成可复制的批准措辞、校验批准、执行范围内重验并报告；不能代替人接受风险 |
| Product Design owner / 正式委派设计负责人 | 批准页面模式、视觉、组件/token 偏离的产品合理性 |
| Frontend owner / 正式委派技术负责人 | 核实影响范围、替代验证、回退和修复计划；标准特例需要设计与技术两项职责签核，已登记兼任者可以承担两项 |
| CTO / 明确登记的 release owner | 可批准紧急特例，接受重大功能发布的设计残余风险；说明为什么不采用建议修复，并指定后续设计/工程复核 |

标准流程不接受申请人自批准。紧急流程由配置的 release owner 作明确决定；如该负责人同时是申请人，必须记录 `selfApproval=true`、紧急理由和独立事后复核负责人，不能隐瞒身份重合或让普通工程师自动获得同等权限。

角色映射来自受保护的配置和平台身份，不由 PR 中任意字符串赋予。尚未配置真实身份时只能本地 fixture 演练，输出 `approvalMode=simulation`，不能用于远端候选或声称真实批准。

## 范围、时效与失效

- **标准特例：** 默认最长 7 天；批准记录必须给出精确 UTC 时间。**紧急特例：** 最长 24 小时，注明事后复核责任人和期限。更长需求应重新评审成正式模式/规则变更，不能无限续期。
- 绑定一个 repository、一个完整 `targetSha`、原检查 `runId` 和证据摘要、规则/测试版本、请求内容摘要。无 commit 的本地实验绑定 `sourceManifestDigest` 并标 simulation，不虚构 SHA。
- scope 列举具体 `ruleId`、`checkId`、已观察的 finding fingerprint；静态问题附精确文件，运行时附 route/state/viewport；视觉问题附原基线与差异摘要。禁止 `*`、全仓、所有失败、无限期范围。
- 每条发现独立匹配。仅批准 DS-001 不会豁免同一文件中的 DS-002；同路由新出现的无名称按钮不会因为该页面已有视觉特例而放行。
- 新提交、申请正文改动、规则版本/证据变更、批准撤销或到期使原决定失效。重跑可引用原批准，仅限目标与请求相同、证据可重新校验且批准明确允许同一候选的复验；新增失败仍需处理。
- 续期是新的批准事件，保留旧记录，不改写原 expiry；合并/候选生成以及发布前均重新验证有效期。部署后到期由巡查员提示整改，不擅自执行回滚或生产修改。

## Coordinator 操作与人工措辞

下面是**协调协议指令**，不是声称已经存在的 shell/CLI 命令。集成 owner 必须将它们映射到实际工具，并在 README 记录真实调用方式；不得执行不存在的 npm script。

1. `REQUEST_DESIGN_EXCEPTION <request-id>`：读取本次失败，先展示建议修复、影响、替代验证、目标身份和期限；生成待批准申请。
2. `APPROVE_DESIGN_EXCEPTION <request-id>`：只能由已验证的授权人作出，批准内容必须绑定申请摘要和范围。coordinator 收到后核对身份及完整记录，不把文本 token 当作秘密通行口令。
3. `EVALUATE_DESIGN_EXCEPTION <request-id>`：原检查照跑/读取同一候选的完整可信结果，再合并批准记录与实际 findings；给出 `passed`、`accepted_with_exceptions`、`rejected` 或 `blocked`。
4. `REVOKE_DESIGN_EXCEPTION <request-id>`：授权负责人撤销，下一次候选/发布判断立即重新检查；保留历史接受结果及撤销事件。

coordinator 在需要人工判断时给出下面的具体模板，填入已观察到的真实值，不能要求人说一句泛泛“继续”：

> 我以【已验证角色】批准设计特例【request-id】，申请摘要为【request digest】，仅适用于【repository + target SHA】中【rule/check + 文件或 route/state/viewport + finding fingerprint】。我已查看【run ID + evidence digest】及建议修复，因【业务理由】接受【具体用户影响】，以【已完成的替代验证】作为补偿。有效至【UTC timestamp】，由【owner】在【追踪项】处理，必要时采用【回退方案】。这不批准新增失败、其他提交、修改测试或自动更新视觉基线。coordinator 可执行该范围的特例评估，无需重复询问本项批准。

紧急模板另加：

> 本次为 emergency，最长 24 小时，由【CTO/release owner】接受风险；不采用常规修复的原因是【原因】，独立事后复核人为【reviewer】，复核截止为【时间】；申请与审批是否同人为【true/false】。

工程师可以在 CI dispatch/UI 提交申请 ID、目标 SHA 和证据 run；申请本身不等于批准。CI/QA 失败输出应给出上述措辞及申请入口，并告诉协调者缺少哪个字段/批准角色，而不是只显示笼统的红灯。

## 申请与审计记录

新机制建议使用独立 `governance/release-exceptions/` 请求记录与报告收据，保持旧 `exceptions.json` 兼容；最终路径/schema 以实现 owner 经测试的版本为准。以下字段是验收契约，不是旧 schema：

| 记录 | 必需内容 |
| --- | --- |
| Request | id、standard/emergency、reason、requestedBy、riskOwner、repository、targetSha 或 simulation manifest、scope、requestDigest、evidenceRunId/evidenceDigest、policyDigest、requestedExpiry |
| Risk/verification | 用户影响、建议修复、为何暂不采用、替代验证及收据、回退方案、跟踪项；紧急情况的事后 reviewer/deadline |
| Approval | 平台主体 ID、已验证角色、批准时间、最终 expiry、requestDigest、批准来源/事件 ID、selfApproval 标识、撤销状态；不能只存 approvedBy 昵称 |
| Decision | 原始 checks 状态及完整 findings、逐项匹配/未匹配结果、目标/规则/环境身份、审批校验结果、decision、exception IDs、命令退出码、执行者和时间 |

原始 checker/browser 报告只读保留；聚合器生成新的 decision artifact。即使候选允许继续，报告中仍显示失败数、被接受数、未接受数及风险 owner。申请、批准、撤销、续期和修复是独立事件，不覆盖旧记录。

## CI/QA 接入契约

```text
固定候选与受信任规则版本
  → 原检查执行并无条件保存报告
  → 全部通过：passed
  → 有确定性设计发现：给建议修复或申请人工特例
  → 验证平台身份/批准、SHA、scope、证据、期限、撤销
  → 所有失败逐项被有效接受：accepted_with_exceptions
  → 任一未匹配/新增/过期/越权：rejected
  → 缺证据/基础设施失败/不可执行：blocked
```

CI 的最终 required decision gate 可以接受 `passed` 或经验证的 `accepted_with_exceptions`，但 artifact 与 job summary 必须明确区分。原始失败检查保留，不能靠让失败 job 从 required checks 消失实现放行；接入 owner 应协调最终 decision check 与原始 evidence jobs 的仓库保护配置，避免合法例外仍被旧的原始必需检查永久卡住。

收集失败 exit code 以便继续生成证据是允许的，但最终聚合器必须校验每个必需检查确实执行且报告完整。禁止全局 `SKIP_DESIGN`、把整 job 的 `continue-on-error` 当合规、删除断言、自动更新快照或把 infraError 转为 passed。

审批可由受保护 GitHub environment/经验证平台审批事件提供；须证明真实审批主体满足所需角色与独立性。仅声明 environment 名称并不证明配置了 reviewers；某些环境只需名单中的一人批准，也不自动满足两个职责的签核。仓库套餐、分支、权限、re-run actor 与真实批准事件均由适配器核验。外部审批未配置时拒绝真实放行，提供 simulation 演练结果而非伪造安全边界。

远端 job 的可信工作流版本和批准映射不能由待批准 PR 任意更换；候选代码执行环境不带审批写权限或生产密钥。此契约不请求现在更改远端权限、关闭安全保护或自动发布。

## Swarm 验收矩阵

以下均须保留测试输入、原报告、批准 fixture/可信事件及决策，不把只有 schema 单测当端到端已验证：

1. 无例外且合规：passed；无批准且有失败：rejected。
2. 标准批准精确覆盖静态发现：accepted_with_exceptions，原 finding 仍在。
3. 浏览器/axe 具体发现、人工审阅视觉差异分别可按范围接受，不仅支持 DS-001/DS-002。
4. CTO/release owner 紧急批准可接受合理设计偏离；普通 engineer/agent 冒称该角色拒绝。
5. 到期、未来批准时间、超长有效期、撤销、错误角色、自批不符合等级要求，均拒绝。
6. SHA、repository、requestDigest、policyDigest、run/evidence 摘要不匹配，均拒绝。
7. 通配范围、同路径不同规则、同路由不同状态/视口/指纹的新失败，不得继承批准。
8. 一项已批准、一项未批准的混合结果仍拒绝；多个独立有效批准精确覆盖全部可接受项时才放行。
9. 缺报告、构建失败、浏览器未启动、测试被跳过、报告重复或候选变更，不能通过特例伪装已验证。
10. 批准前后原始失败报告摘要不变；续期/撤销保留历史；expiry 到界点时行为明确。
11. 同一候选有效批准再次评估无需重复人工输入；新提交必须重新授权。
12. 真实角色适配器未配置时 fail closed；simulation 输出不能满足远端候选条件。
13. 在原本会失败的实际隔离实现上完成“未批准阻断 → 批准后接受 → 过期/新失败再阻断”的集成演练；证明代码未改、检查未删，只有经验证的接受决定变化。

## 官方参考

- [GitHub environments 与审批](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)：所需 reviewers、防自批以及套餐边界需实际核实。
- [Workflow re-run 身份](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)：重跑使用最初触发者的权限，不应只看触发重跑的人。
