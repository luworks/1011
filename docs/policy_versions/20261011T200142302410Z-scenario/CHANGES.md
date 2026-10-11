# 第三版修改说明（相对 clarified）

此版仍是 editorial-draft，父版本及全部结果保留。E01–E12 的明确冲突修正、累计上限、outage 独立轨道、Rule 4/5 强制检查、no-ticket 与 unverifiable 区别及税费证据边界继续保留。没有业务负责人批准任何 OD。

| 修改 | 位置 | 原因 |
|---|---|---|
| S01 | Rule 1 / KB-1001 | 仅在 standalone 缺账单信息、两窗口冲突或日期临界时提示 OD-02/08；不让所有普通请求带上组合流程歧义 |
| S02 | Rule 2 / KB-1002 | 仅在 outage fallback 缺 confirmed error/amount basis 时提示 OD-03；不混淆已核实 ordinary billing error |
| S03 | Rule 3 / KB-1004 | 拆分 OD-05/06/07/08：不足整天、余数、舍入、部分线路、变价或临界日期分别触发。上一轮三线确定基数案例 raw completion 退步，需要把可确定的金额与无关缺口分开 |
| S04 | Rule 3 / KB-1003/1004 | OD-09 只影响 downstream tax 问题；不拒绝独立 recurring-charge 计算，不补充税费调整结论 |
| S05 | Rule 3 / KB-1005 | unknown 不等于 absent；覆盖不匹配及组合失败才触发映射待决；已知 unverifiable 仍按原文要求 Tier 2 |
| S06 | Rule 5 / KB-1007 | 只在 repeat 日期/次数边界触发 OD-08；已明确的窗口内第二次争议与 fraud 仍强制 Tier 2 |
| S07 | workflow scenario boundary gate | 固定 gate 不再把 partial-day/舍入/临界日期等未批准假设改成 grounded 金额或模拟授权；保留独立明确 escalation。原始模型输出保持原样；并非将任意模型犹豫照单全收 |

触发描述是对缺失证据的范围限定，不新增补偿资格、分摊算法、时间约定或审批目的地。具体实现保守覆盖已结构化事实，复杂语义仍可能需要补充信息。测试继续沿用 v2 oracle，待决字段无唯一业务 gold。新旧 policy 在同一最新版 workflow 上配对；历史 v5 指标仅作描述，不能将跨 workflow 差异归因于正文修改。
