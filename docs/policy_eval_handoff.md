# Policy evaluation handoff

Updated UTC: 2026-10-11T19:42:34.727980+00:00

本线程负责 policy pair 版本、比较入口、待决 oracle overlay、冻结与对比报告；不修改主 workflow/CLI/providers 的后续通用修复，也不切换默认 policy。已在 CLI 接入的版本选择保留。

## 活跃付费批次

两模型内部各自保持相同配置：40 例 × 两版本 × 3 repeats；每模型计划 120 pairs / 240 scenario runs，共 240 pairs / 480 runs。jobs=8/模型；共享账本 runs/budget.json，总累计上限 $70。不另建账本、不叠加每线程 $70。

冻结输入：`runs/policy-inputs-validated-v4-20261011`。**目录名含 v4 是历史标签，真实冻结 prompt 为 workflow-v5，以下 manifest/hash 才是版本依据。** 模块从该目录加载，源工作区后续 v6 不进入此批次；已通过冻结副本 208 tests。

主 workflow 的 v6 是否可晋升不由本批结论决定。等待 docs/mvp_fix_status.md 的 READY 后，才考虑固定 v6 输入做小型 matched confirmation；尚未启动任何重复大矩阵或下一轮付费验证。

### sol

- Active run: `runs/policy-pair-sol-medium-frozen-v4-20261011`
- Exact config: `openai/gpt-6.1-sol/reasoning/medium`
- Config SHA256: `6d350e6290ab644f55cf8d624abe5a054b9f99b292bfcd85a3f1e68ad617ac16`
- Code SHA256: `a1e13e3b83d1be6de090d9eeb11829d85f5f65b8fe9b9cdb6f274d9098dcd099`
- Prompt: `workflow-v5` / SHA256 `6856be14db2e251857479788199ccc276f75b96c643e00215589a400ae76d137`
- Cases file SHA256: `1a0e556f27f8539effbebfb07dc0e13f9440b03dd0d744e6a293a5f297ae2fd6`
- Projected suite/oracle SHA256: `b442147ccff8faec8a36bf814cf49d0ba1b48b699a0ca9558e61a14cc237869c` / `5fcd6f4595f1d3226516c4794f173815eaa6e5e85ad9b7d5f32b1acda91e37e7`
- Persisted scenario runs: 62/240; completed paired quality denominator in latest batch summary: 24/120.
- Reported cost from persisted calls: $1.473519; partial, active reservations not included.
- Latest raw transitions: `{'improved': 2, 'regressed': 2, 'unchanged_pass': 15, 'unchanged_fail': 5}`
- Latest final transitions: `{'improved': 0, 'regressed': 1, 'unchanged_pass': 20, 'unchanged_fail': 3}`

- baseline: `20261011T192840169969Z-original`; corpus `dbb59ca9a429ab22142b76f32c0704dc3477c5e7ff0a33289efc12d700a05a5f`; manifest `259df1ca2407d1f6b357ebe492ba269f5863cb115773e644701fa3e492550891`
- candidate: `20261011T192840174385Z-clarified`; corpus `6d6979ebb6bd6aae2fbe25640d4c96c5e2dd11ce39a2e6a1e7dd6cfc01d6a42a`; manifest `4ca4c9000b4b024eb69ff8203920e78662a4b7233286b6e8921ca8451d4a0034`

### luna

- Active run: `runs/policy-pair-luna-medium-frozen-v4-20261011`
- Exact config: `openai/gpt-6-luna/reasoning/medium`
- Config SHA256: `be1be9d98a7eb47307e41a9d9ba66386c289c9e2feaf8390204e3789f328ce65`
- Code SHA256: `a1e13e3b83d1be6de090d9eeb11829d85f5f65b8fe9b9cdb6f274d9098dcd099`
- Prompt: `workflow-v5` / SHA256 `6856be14db2e251857479788199ccc276f75b96c643e00215589a400ae76d137`
- Cases file SHA256: `1a0e556f27f8539effbebfb07dc0e13f9440b03dd0d744e6a293a5f297ae2fd6`
- Projected suite/oracle SHA256: `b442147ccff8faec8a36bf814cf49d0ba1b48b699a0ca9558e61a14cc237869c` / `5fcd6f4595f1d3226516c4794f173815eaa6e5e85ad9b7d5f32b1acda91e37e7`
- Persisted scenario runs: 50/240; completed paired quality denominator in latest batch summary: 24/120.
- Reported cost from persisted calls: $0.073431; partial, active reservations not included.
- Latest raw transitions: `{'improved': 5, 'regressed': 6, 'unchanged_pass': 7, 'unchanged_fail': 6}`
- Latest final transitions: `{'improved': 0, 'regressed': 0, 'unchanged_pass': 19, 'unchanged_fail': 5}`

- baseline: `20261011T192840169969Z-original`; corpus `dbb59ca9a429ab22142b76f32c0704dc3477c5e7ff0a33289efc12d700a05a5f`; manifest `259df1ca2407d1f6b357ebe492ba269f5863cb115773e644701fa3e492550891`
- candidate: `20261011T192840174385Z-clarified`; corpus `6d6979ebb6bd6aae2fbe25640d4c96c5e2dd11ce39a2e6a1e7dd6cfc01d6a42a`; manifest `4ca4c9000b4b024eb69ff8203920e78662a4b7233286b6e8921ca8451d4a0034`

## 预算/最早可交付进度

- Shared ledger upper-bound: $15.108147; includes $2.136960 pending/unknown reservations; remaining to $70: $54.891853.
- This formal batch persisted reported cost: $1.546950. Planning allowance for remaining formal batch: **up to $10** estimated, not a second ledger or API pre-reservation. Existing worst-case per-request reservation still applies. No new large batch authorized by this handoff.
- Expected near-term delivery: 完成两个冻结模型各 120 pairs 后生成 docs/policy_comparison 下的报告；若 13:01 PDT 时未全量完成，明确提供完整/部分分母和 active 状态，不宣称全量结果。
- Main experiment still active; no global-winner or per-edit causal claim yet.

## 已排除/保留的记录

- `runs/policy-pair-sol-medium-20261011` / `runs/policy-pair-luna-medium-20261011`: own processes terminated after source drift was detected; EXCLUDED.json marks them out of formal comparison. Partial traces retained; unresolved charged-call reservations retained in ledger.
- `runs/policy-inputs-frozen-20261011`: first freeze omitted required script inputs; no formal live experiment used it.
- `runs/policy-inputs-frozen-v4-20261011`: source changed during copy and verification failed; no formal live experiment used it.

## 判断边界

- 原文与优化版使用同一 reviewed overlay；待决 amount/policy/action/answer fields 被从最后一轮和逐轮唯一答案断言中排除。税费 yes/no 都缺乏依据。
- 比较 supported assertions、citations、unresolved evidence boundaries、raw candidate 与 fixed-gate final，分母分别保留。现有 gate 的未批准计算假设可能两版都失败，不能改 oracle 让它通过。
- E 编号只作场景关联；整组文档改写不能独立归因单条编辑。案例非新 holdout，provider 未固定 seed，理解阶段未读 policy、也存在随机差异。
- 当前 Corpus 不读取文档头部；E01/E12 和 E02 的总则不被这批直接测试。OD-01/02/06/07 没有专门案例。
