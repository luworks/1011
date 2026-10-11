# Nimbus policy pair 版本管理

两份文档作为一个版本发布，避免测试时混用不同轮次的 Policy 和 KB。原始 `exam/` 文件仍保留，当前默认 corpus lock 和 agent 行为未切换。

| 版本 | 状态 | 说明 |
|---|---|---|
| [20261011T192840169969Z-original](20261011T192840169969Z-original/manifest.json) | original | 两份原文逐字节归档；原文基线，不代表已经消除了原文冲突 |
| [20261011T192840174385Z-clarified](20261011T192840174385Z-clarified/manifest.json) | editorial-draft | 修正明确冲突/遗漏，标出业务待决，尚未作为生产政策批准 |

两份快照创建于 2026-10-11 12:28:40 PDT（UTC 19:28:40）；精确微秒见版本 ID 和 manifest。时间戳表示编辑快照创建时间，不替代原文生效日期。`Version 6.2` 和原 KB 更新时间是上游原始元数据；本地修订身份以快照 version ID 为准。

优化版：[Billing Policy](20261011T192840174385Z-clarified/exam/Nimbus%20Wireless%20%E2%80%94%20Billing%20Dispute%20%26%20Refund%20Policy.md)、[Knowledge Base](20261011T192840174385Z-clarified/exam/NimbusCare%20Knowledge%20Base%20%E2%80%94%20Billing%20%26%20Credits%20Excerpt.md)。

逐处原因见 [CHANGES.md](20261011T192840174385Z-clarified/CHANGES.md)，待决登记见 [OPEN_DECISIONS.md](20261011T192840174385Z-clarified/OPEN_DECISIONS.md)，原文与优化版完整逐行差异见 [original-to-clarified.diff](original-to-clarified.diff)。后者可重新从两个快照生成，是阅读辅助，不是 agent 输入。

## 快照契约

- 一个快照固定两份文档、每份 SHA-256、可供 `Corpus` 读取的 `config/corpus-lock.json`、corpus 内容版本、创建时间、状态与 parent。
- 优化版另固定修改说明和待决登记；manifest 的文件哈希覆盖它们。
- 已保存快照不原地修改。后续修订复制到工作目录，编辑后生成新时间戳快照。脚本拒绝覆盖已有目录；哈希校验检测已保存内容的变化，不提供防篡改签名或文件系统写保护。
- parent manifest 的哈希绑定父版本。manifest 本身需要随 Git/评估运行归档并记录哈希；能同时改写 manifest 和文件的人仍能重写本地记录。
- SHA-256 证明内容身份，不证明业务规则正确、已经审批或模型表现改善。
- `original`、`editorial-draft`、`experiment` 是本地来源/实验状态，不是业务批准状态。获批状态、审批人、依据及生效日期应由实际业务决定记录，不能仅改 label 宣称生效。

校验全部快照（不调用 API）：

```sh
python3 scripts/policy_versions.py verify
```

## 创建下一版

在独立工作目录放置这两个原文件名的 Markdown 文档，更新修改说明与待决登记，然后执行：

```sh
python3 scripts/policy_versions.py snapshot \
  --source-dir /absolute/path/to/policy-working-copy \
  --label experiment-a \
  --status experiment \
  --parent 20261011T192840174385Z-clarified \
  --changes /absolute/path/to/CHANGES.md \
  --decisions /absolute/path/to/OPEN_DECISIONS.md
```

脚本生成 `UTC timestamp + label` 的新目录并校验内容。非原文快照必须提供 parent、修改说明和待决登记。小改动实验应尽量只改变一个 E/OD 项目，避免无法归因。

## 后续如何比较好坏

CLI 已接入版本选择：`doctor`、`replay`、`chat`、`evaluate` 支持 `--policy-version VERSION_ID`。未指定时仍使用根目录默认 corpus。指定版本时校验整组快照及 parent manifest，记录版本 ID、manifest SHA-256 和 corpus 内容哈希；版本内 evidence 路径可直接定位到快照文件。`evaluate` 指定版本后默认使用已审阅的待决项 overlay；自定义案例必须提供匹配的 `--oracle-overlay`，不能悄悄沿用旧 oracle。

**当前 `policy.py` 是固定、人工审阅的确定性规则。** 只换文档不会自动重新生成业务决策逻辑；该 gate 可能掩盖模型判断的差异，也可能沿用旧实现假设。版本比较接入时需要显式绑定快照并审阅 gate/oracle 是否仍适用；不能简单把新 hash 写入默认 lock 就宣称政策升级完成。

每轮结果至少记录：policy-pair version ID、manifest SHA-256、corpus_version、model/config、prompt hash/version、gate/code hash、scenario suite/oracle hash、运行时间、repeat/seed（如支持）、原始输出及最终输出。两份文档必须来自同一个快照，结果目录必须独立。读取其他源码/规则文件的评估也需要记录实际读取的版本。

建议分开比较：

1. **模型原始判断：** 是否选对 governing rule、金额是否正确、是否漏掉全局升级、是否对税费缺口猜测。它最直接反映文档改写的影响。
2. **工作流最终输出：** 经 gate 后是否正确回答、是否遗漏可回答部分、是否错误承诺发放、是否正确保留待决。通过不能反推原始模型没有错误。
3. **代价：** 相同问题集下的端到端延迟、token/费用；新增说明更长，可能影响这些指标。

固定相同客户对话、事实/核验记录、模型配置、prompt、gate 和 oracle，成对运行原文/优化版并报告逐案例变化及重复次数。若决定改变 gate/oracle，要作为另一实验变量报告，不能将差异全部归功于文档。

对于 OD-01 至 OD-09，不把未经业务批准的某个选项定为唯一正确答案。标注 `unresolved_policy` 并评估是否守住证据边界；这些标记保存在评估 oracle/报告中，不进入模型输入，也不改变客户回复 schema。明确规则与待决案例分别报告，保留总案例数、各分母、失败/跳过情况。用来优化文档的案例应转为开发集，后续以新 holdout 验证。

后续用户已授权真实版本对比并将共享账本总上限提高至 US$70；这是累计上限，不是另外新增 $70。命令必须显式传 `--max-cost-usd 70` 并继续使用同一 `runs/budget.json`。具体支出及实际完成情况以实验 manifest/报告为准。

## 成对评估命令

```sh
./run.sh compare-policies \
  --baseline 20261011T192840169969Z-original \
  --candidate 20261011T192840174385Z-clarified \
  --config-id openai/gpt-6.1-sol/reasoning/medium \
  --suite all --repeats 3 --jobs 8 --max-cost-usd 70 \
  --output runs/policy-pair-NEW_UNIQUE_DIRECTORY
```

该命令固定一个精确 config，运行相同 case/repeat 组合，交替 AB/BA 顺序，以独立完整工作流生成原始 candidate 和最终 decisions。`manifest.json` 固定 prompt/code/config/案例/oracle/两版内容；`oracle.json` 保存排除了待决字段的 ground truth；`turns.jsonl` 保存逐案例逐版本 raw/final、retrieved excerpts、调用 telemetry；`summary.json` 分开统计业务断言、引用忠实度、待决证据边界和有效配对；`comparison.md` 汇总改善/变差案例。输出目录不得复用。

两版采用同一份 `fixtures/policy-comparison-oracle.json`：包含原始案例集指纹，排除未批准的金额/资格等字段，也处理每轮 oracle，保留明确规则检查。税费 yes/no 不被视为唯一业务 gold 的候选；它们都属于无依据结论。证据边界检查接受多种保留不确定性的状态，不要求固定人工路由。

当前边界检查针对结构化输出：对于排除的金额/政策轨道，在 `answer_status=grounded` 时作确定断言会被标记；待决业务上声明可发放也会标记。这是保守的评估标准，不是新补偿政策，也不能代替自然语言人工审阅。

单版本测试可用：

```sh
./run.sh evaluate --policy-version 20261011T192840174385Z-clarified \
  --only-config openai/gpt-6.1-sol/reasoning/medium \
  --suite all --repeats 3 --max-cost-usd 70 \
  --output runs/policy-single-NEW_UNIQUE_DIRECTORY
```

原始 `fixtures/scenarios.json` 保留开发历史，legacy 未指定版本的评估仍可使用原 oracle；版本化实验以 overlay 后的 oracle 为准。原始 40 个案例中部分已用于开发，frozen 标签不代表本轮是全新 holdout。OD-01/02/06/07 的关键业务分歧尚无专门案例，本轮不声称覆盖或验证这些待决项。

## Oracle 评分版本

默认 `fixtures/policy-comparison-oracle.json` 现为 schema v2，与 `policy-comparison-oracle-v2.json` 一致；v1 原样保存在 `policy-comparison-oracle-v1.json`。v2 在相同 OD-09 规则下，对两版都移除了“必须引用 KB-1004 才正确”的唯一来源断言：优化版 Rule 3/KB-1003 也明确说明证据缺口。仍检查税费 intent、引用忠实度和无依据结论，不添加税费规则。

已启动的冻结实验保持各自冻结的 v1；原分数不覆盖。可使用 `scripts/report_policy_comparison.py --oracle-overlay fixtures/policy-comparison-oracle-v2.json` 在同一冻结 evaluator 上离线审计重算全部已保存输出，并同时保留原始严格计数。报告会明确记录两个 oracle 版本及审计范围。
