# Nimbus policy 版本实验结果

两份文档按成对版本运行；相同模型内部固定配置、40 个案例、3 次重复，原文/优化版交替运行顺序。所列模型均使用同一冻结 workflow。

评分审计：使用共同 v2 overlay 离线重算税费来源检查；Rule 3/KB-1003 的有效依据不因未引用 KB-1004 而被判错。原始严格评分保存在 results.json 的 original_strict_counts 与原 run summary，不改写或删除。未新增税费业务规则，未重跑模型。

| 模型/配置 | 有效配对 | raw 原文→优化 | final 原文→优化 | raw 改善/回退 | final 改善/回退 |
|---|---:|---:|---:|---:|---:|
| openai/gpt-6.1-sol/reasoning/medium | 120/120 | 85→100 / 120 | 105→104 / 120 | 19/4 | 0/1 |
| openai/gpt-6-luna/reasoning/medium | 120/120 | 63→75 / 120 | 95→94 / 120 | 29/17 | 1/2 |

raw 合格同时要求支持的结构化断言、引用忠实度和待决证据边界；final 合格包含固定 gate 输出的边界检查。表中的失败不都代表业务答案错误。待决字段不设唯一业务答案。

| 模型 | supported raw 原文→优化 | raw 引用失败 原文→优化 | raw 待决边界失败 原文→优化 | final 待决边界失败 原文→优化 |
|---|---:|---:|---:|---:|
| gpt-6.1-sol | 102→105 | 2→2 | 15→3 | 12→12 |
| gpt-6-luna | 93→85 | 35→22 | 6→0 | 12→12 |

## 逐案例变化

只列 raw/final 合格次数改变的案例；完整重复结果、结构化检查、引用问题和待决边界见 results.json。关联 E 编号仅是案例与修改范围的对应，不能证明某一处编辑单独造成变化。

| 模型 | 案例 | raw 原文→优化 / 3 | final 原文→优化 / 3 | 关联修改 | 待决 |
|---|---|---:|---:|---|---|
| gpt-6.1-sol | four_hours | 1→3 | 3→3 | E02, E09, E11, E04 | OD-03 |
| gpt-6.1-sol | over_four_hours | 0→3 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6.1-sol | late_request | 3→2 | 3→3 | E02, E09, E11, E04 | OD-03 |
| gpt-6.1-sol | wrong_address | 0→3 | 3→3 | E02, E09, E11, E05 | OD-04 |
| gpt-6.1-sol | thirty_day_outage | 0→1 | 3→3 | E02, E09, E11 |  |
| gpt-6.1-sol | goodwill_above_cap | 3→3 | 3→2 | E10 |  |
| gpt-6.1-sol | whole_days | 0→3 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6.1-sol | under_four | 0→1 | 3→3 | E02, E09, E11, E04 | OD-03 |
| gpt-6.1-sol | rounding | 0→3 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6.1-sol | three_lines | 3→2 | 3→3 | E02, E09, E11 |  |
| gpt-6.1-sol | tax_negative | 1→3 | 3→3 | E07 | OD-09 |
| gpt-6.1-sol | unconfirmed_error | 3→2 | 3→3 | E10 |  |
| gpt-6-luna | deadline | 3→2 | 3→3 | E03 |  |
| gpt-6-luna | over_four_hours | 1→3 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6-luna | four_hours | 1→3 | 3→3 | E02, E09, E11, E04 | OD-03 |
| gpt-6-luna | original_amount | 1→0 | 3→3 | E02, E09, E11, E07, E03 | OD-09 |
| gpt-6-luna | ticket_unknown | 1→3 | 3→3 | E02, E09, E11, E05 | OD-04 |
| gpt-6-luna | above_three_hundred | 3→2 | 3→3 | E02, E09, E11, E08 |  |
| gpt-6-luna | repeat_ninety | 2→3 | 3→3 | E02, E09, E11, E06, E08 | OD-08 |
| gpt-6-luna | long_outage | 2→0 | 3→3 | E02, E09, E11, E08 |  |
| gpt-6-luna | wrong_address | 2→3 | 3→3 | E02, E09, E11, E05 | OD-04 |
| gpt-6-luna | sixty_day_dispute | 3→2 | 3→3 | E03, E06 | OD-08 |
| gpt-6-luna | fraud | 1→3 | 3→3 | E02, E09, E11, E08 |  |
| gpt-6-luna | goodwill_at_cap | 1→0 | 0→0 | E10 |  |
| gpt-6-luna | under_four | 0→3 | 3→3 | E02, E09, E11, E04 | OD-03 |
| gpt-6-luna | rounding | 0→3 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6-luna | whole_days | 1→2 | 0→0 | E02, E09, E11, E06 | OD-05 |
| gpt-6-luna | unknown_fraud | 0→3 | 3→3 | E02, E09, E11 |  |
| gpt-6-luna | three_lines | 3→0 | 3→3 | E02, E09, E11 |  |
| gpt-6-luna | repeat_small | 2→1 | 2→1 | E02, E09, E11, E08 |  |
| gpt-6-luna | tax_negative | 1→3 | 3→3 | E07 | OD-09 |
| gpt-6-luna | unconfirmed_error | 3→1 | 3→3 | E10 |  |
| gpt-6-luna | missing_monthly | 1→3 | 3→3 | E02, E09, E11 |  |
| gpt-6-luna | tax_pressure | 2→3 | 3→3 | E07 | OD-09 |

## 代价与限制

| 模型 | 原文费用估计 | 优化版费用估计 | 原文 full-turn P50/P95 秒 | 优化 full-turn P50/P95 秒 |
|---|---:|---:|---|---|
| gpt-6.1-sol | $2.2892 | $2.6287 | 11.89/16.84 | 12.49/16.81 |
| gpt-6-luna | $0.1503 | $0.1709 | 11.78/16.49 | 12.50/19.27 |

- 固定 gate 不会根据 policy 文本重新编译规则；最终输出可继续暴露旧实现假设。
- 两版各自执行完整的理解阶段；该阶段不读取 policy，差异可来自模型随机性，不能自动归因于文档改写。provider 未固定 seed。
- PLAN prompt 已明确 outage exception、全局限制和税费边界。本轮衡量此 workflow 内文档变化，不是无提示的独立阅读能力。
- 本批冻结的 workflow-v5 使用 EvidenceBoundCandidate 限制 tax_adjustment 为 unknown/not_applicable。税费 yes/no 未出现不能计为文档改善了自由推理或消除了幻觉；它是已有 schema 边界。
- 当前 Corpus 只提取 Rule/KB 正文，文档头部/总则改写 E01、E02 中的总则、E12 的文章计数不进入检索证据；不能声称测试了这些改动。
- OD-01/02/06/07 的关键业务分歧没有专门案例；待决字段的保守结构化边界检查不等于业务批准规则或完整自然语言语义审计。
- 既有案例包含开发历史；frozen 标签不代表全新 holdout。三次重复仅用于观察稳定性，不能证明统计显著或泛化。
- 两个模型实验并行运行，每组 jobs=8；延迟反映此并发/服务状态，费用来自矩阵和 provider token usage 的客户端估计。
- 早期工作区源码漂移而中止的实验明确排除，记录仍保留；共享账本包含其已报告成本和未结算预留。

冻结输入：/Users/yuanlu/code/1011/runs/policy-inputs-validated-v4-20261011

原始结果目录：
- /Users/yuanlu/code/1011/runs/policy-pair-sol-medium-frozen-v4-20261011
- /Users/yuanlu/code/1011/runs/policy-pair-luna-medium-frozen-v4-20261011
