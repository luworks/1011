# Claude handoff

请接手 `/Users/yuanlu/code/1011`（GitHub `luworks/1011`）的 Policy-Grounded Agent。先阅读 `docs/closeout.md`、`docs/eval_final_handoff.md`、`docs/model_selection.md`、README 和题目原始材料 `exam/`。代码与标识符用英文，解释用中文。

## 当前状态与边界

这是 Python 3.12+ 后端 CLI 原型：Pydantic、OpenAI Responses/Anthropic Messages 官方 SDK、本地语料/模拟账户、确定性政策关口、模板回复、评测和离线 HTML。没有真实退款或外部人工转交。默认开发配置为 `config/development-default.json` 中 Claude Haiku 5.5 adaptive/medium，只是用户选定开发基线，绝不是验收冠军。用户准备重新审视模型；不要自行扩大模型矩阵。

当前核心为 `workflow-v11`。关键文件：`src/policy_agent/workflow.py`、`providers.py`、`diagnostics.py`、`boundaries.py`、`policy.py`、`cli.py`。

已实现通用修复：
- SDK JSON/schema、理解契约与 scope 契约共享每轮一次内容修复额度，所有调用计费；临时网络重试另行记录，失败不能伪装成政策拒绝。
- 独立 ScopeReview 区分真实请求、多问、明确重问、背景提及和不确定请求；只对有依据的范围作答。
- 客户账单提法与可信账单字段分开；简称不自动变成事实冲突或覆盖可信项目。不同名称未取得权威关联时仍待确认。工具更换项目会撤销旧项目的金额、错误确认和账单日期依据，保留全局欺诈/历史检查。
- v11 修正 optional action_quote 与疑问句的契约不一致：允许 null；非空引文必须来自当前消息；修复反馈包含固定可操作说明，诊断不存任意模型自由文本。
- 保留 scenario-scoped policy boundaries 与强制升级，不将业务未决项硬编码为企业决定。

## 已验证结果：不能混用版本

- 收尾前 v11 本地完整 pytest：388 passed；如新增报告测试等导致数量变化，以最终实际命令记录为准。v11 已用 Sonnet 5.5 adaptive/medium 真实回放原始六轮对话一次：6轮全部通过、0技术失败（17 calls，约$0.174，`examples/workflow-v11-sonnet-medium/`）；fresh V3 验收仍未运行。
- v8 原始六轮会话曾通过七项针对题目要求的检查，金额 `$225 / 30 * 11 = $82.50`，不乘三、不受 $75 goodwill cap 限制；税费调整未知；恢复后30天，申请在第14天；未虚构批准/发放。
- v8 独立回归84/84执行，三个配置均23/28。v8新验收96/96执行（16场景×3重复×2配置）：Sol-low24/48成功、21技术失败；Haiku-medium34/48成功、7技术失败。selector为no_qualifying_model。18个保守critical标记均是安全停止后缺少必须的人工作答，并非观察到实际错误发放；缺失答案仍算失败。
- 第5阶段（同一v8代码与同一验收集，16×3=48/配置）：Sonnet-medium 44/48（1个critical，强制升级23/24），Sonnet-high 29/48，Opus-high 25/48，Opus-medium 19/48（后三者含16路并发造成的API连接错误）。所有critical均为理解契约校验失败后的安全停止，无错误金额/政策。没有配置满足“0 critical + 强制升级全召回”门槛；Sonnet-medium为观测最优，待fresh V3确认。详见 `docs/model_selection.md`。
- v10 原始六轮真实回放第4轮失败：scope_action_support_missing连续两次，一次修复耗尽。18 calls，估算$0.0119011，逐轮耗时合计77.203秒。原始记录 `runs/mvp-live-demo-haiku-medium-v10/` 必须保留，不能用v11本地测试冒称此失败已获真实验收。
- 旧v5 policy A/B完成240对/480场景执行，raw有所改善但final无净提升；未晋升整版优化政策。审计结果在 `docs/policy_comparison/20261011-full-v5-audited/`。
- 新scenario版 `docs/policy_versions/20261011T200142302410Z-scenario/` 与边界修复有本地检查，但没有完成新固定Haiku的付费对照；默认原文未替换。

## 未解决问题

1. v11是否改善真实新问法稳定性尚未验证。
2. ScopeReview只能审查提取出的intent，不能保证补回理解阶段完全漏掉的问题；引文存在也不能证明语义蕴含。
3. 没有权威item_id/alias映射时，简称仍可能需要澄清，不能用子串相等或模型猜测授予执行权限。
4. 新政策与门控在同一最新workflow上的成对效果尚未测量，业务未决项仍须保留。
5. 新增scope审核的额外调用带来延迟/成本；需要测完整回合P50/P95，不要仅测单API耗时或凭单次回放下结论。

## 接手后验收顺序

用户已要求停止新增模型测试。因此先做只读核对与本地工作，**不要自动启动付费调用**；等用户明确恢复测试并确认模型与剩余预算后再执行后续API步骤。

1. `git status --short`，保留其他线程的修改；`uv sync --frozen`、`uv run pytest -q`、`uv run prototype doctor`（不加--check-api）和 `uv run prototype replay --offline --output runs/一个新的目录`。不要读取/打印.env内容。
2. 恢复测试时冻结代码、prompt、corpus、配置、oracle哈希，先用精确v11重跑原始完整对话，逐轮核对问题范围、事实来源、引用、金额、期限、人工作答和动作权限。
3. 再跑独立14例开发回归 `fixtures/workflow_repair_regression_v1.json`，通过后由独立评测者执行未使用的16例V3验收 `fixtures/acceptance_v3.json`，每例3次。实现/调优者不要读取或使用fresh expected；若用于调优就将其降为回归集，另建新holdout。来源审阅副本在本地 `runs/oracle-v3-source-reviewed/`，使用前核对receipt，禁止把oracle旁注送给模型。
4. 仅在同模型、同thinking、同案例、同workflow内比较original/clarified/scenario policy；统一评分并保留原结果，不替业务负责人选择未决答案，不改gold让实现通过。
5. 更新HTML中的新旧版本、完整计划/执行分母、raw/gate、技术失败、效用失败、整轮P50/P95、tokens、估算成本。无合格配置就明确不推荐。当前报告 `report/dist/index.html` 是静态快照，不会自动刷新。
6. 完成相关验证后可以直接commit/push，已有用户授权；不force push、不覆盖并行工作。

## 预算、证据与交付

唯一共享累计账本为 `runs/budget.json`，历史总授权$70，但收尾指示已暂停新增测试，不能把余额当作立即开跑授权。模型线程$40是同账本停止线，不是新预算；不要清账或丢弃unknown reservations。调用前读取实际账本，费用是客户端估算而非供应商账单。

`runs/`、`.env`、虚拟环境、依赖缓存和构建产物不入Git；本机保留原始证据，跨机器需另行获得脱敏运行文件，不能伪造或将离线结果代替真实评测。`report/src/data.json`、审计文档和curated examples保存可审阅结果。`frontend/`及可能的`scripts/web_api.py`来自并行工作，未被本次后端收尾验证；不要把模板当作完成MVP，也不要删除它们。
