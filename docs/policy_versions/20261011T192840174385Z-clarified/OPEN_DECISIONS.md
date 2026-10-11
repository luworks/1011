# 待业务负责人决定的事项

全部状态：**OPEN**。以下是待回答的问题与可选方向，不是新的 Nimbus 规则。建议由 Billing Operations 牵头确认（其是原 Policy 的 Owner），涉及其他部门时由其确定实际负责人。尚未作出决定、未实施任何业务审批或外部转交。

| ID | 必须决定的问题 | 当前证据 / 尚不能推断 | 业务负责人需要给出的决定 | 测试影响 |
|---|---|---|---|---|
| OD-01 | Policy 与 KB 的跨文档权威、更新与发布关系 | Policy 自称 governs；KB 日期更新，但没有跨文档覆盖机制 | 是否 Policy 为权威且 KB 仅实施说明；KB 能否独立修改规则；配对审批与生效机制 | 不得把“更新较晚”自动当成覆盖；两篇必须按同一 bundle 运行 |
| OD-02 | standalone outage 请求是否还需 Rule 1 的账单/line item/60 天检查 | Rule 1 处理 invoice dispute，Rule 3 处理 outage 请求，未完整规定交集 | 定义独立请求、关联账单争议的流程，以及仅 60 天超期时是否需 Tier 2 | 当前代码采用组合检查；不是原文唯一明确解释，不能把该 oracle 当业务定论 |
| OD-03 | outage fallback 在没有 confirmed billing error 时是否允许 goodwill，如何定额 | Rule 2 要求 confirmed error；Rule 3 让失败请求转入评估 | 保留该前提，或明确扩展 discretionary eligibility；同时给出 amount basis、审批规则 | 不可自动给 $75，不能把 cap 当 entitlement |
| OD-04 | 不存在、未查询、查询失败、不可核验、覆盖不匹配及组合失败的处理 | 无 ticket 走 fallback；不可核验走 Tier 2；其余状态未完整定义 | 给出明确状态定义、需要的核验证据、等待/重试/审批/fallback 的完整映射及组合优先级 | unknown 不能成为 absent；不可核验 + 超期等组合应标待决 |
| OD-05 | full days、>4 小时但不足一天、partial day、舍入和阈值比较顺序 | 公式按 full days，资格 >4 小时；无最小补偿和舍入定义 | 选定 calendar days 或 elapsed days，是否零金额/最低补偿/小时计算，最终与逐日舍入，以及舍入前后金额阈值 | 当前 24 小时与 ROUND_HALF_UP 只是实现假设；不据此定义业务 gold label |
| OD-06 | 部分线路中断、共享费用和 bundle discount 的计算基数 | affected lines 与 account formula 混用 | 哪些 recurring charges 属于 affected service，分摊与折扣如何处理 | 全部三线 $225 合计的案例不再次乘三；部分线路不能自行按总额或平均值推算 |
| OD-07 | 套餐/费率变化时 current charge 的取值时间 | current 未指定时点，KB-1010 是不同业务的 plan-change proration | 请求时或 outage 时费率；跨费率 outage 是否分段；与已有账单 credit 如何协调 | 未批准前不能直接复用 KB-1010 作为 outage 新公式 |
| OD-08 | 时区、起算、截止日包含、90 天边界及第三次以后争议 | 日历天/90 天数字明确，边界和多次分类未完整规定 | 指定时区、day zero、最后一天/cutoff、重复争议时间与次数判定 | 30/60/90 天临界案例需依据决定；不要用执行主机日期代替明确请求日期 |
| OD-09 | outage 后税费是否调整以及由谁核实 | KB-1004 限定 credit base，KB-1003 描述 bill；未涵盖 adjustment | 提供实际税费/附加费规则、适用条件、系统/人工处理与核实责任；未决定前只标缺口 | 不能确认 yes 或 no；未定义业务转交目的地或完成状态 |

## 测试解释原则

明确规则可建立相同 gold label：outage 不套 $75、累计 goodwill 上限、Rule 5 不被局部金额条件覆盖、未覆盖税费不能作肯定或否定结论。

待决边界案例分别记录 `unresolved_policy` 与实现采用的 assumption；评估 evidence-boundary adherence，不把某个未批准业务选项算成唯一正确答案。此状态是建议的评估标注，尚未加入程序 schema。

业务决定落地时，新建版本，记录决定人/责任方、日期、来源、选项及理由；相应 oracle 也要版本化。评估标签变化时不能直接用旧版/新版总分宣称改进。
