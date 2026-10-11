# Policy evaluation handoff

**Status: READY — formal frozen-v5 policy pair batch complete; no policy promotion or additional paid confirmation.**

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

## 12:47 PDT milestone

- 正式冻结 cohort 的实际 prompt 是 workflow-v5（不是目录名中的 v4），两模型各完成 80/120 有效 pairs；已覆盖共同 40 例的前两次重复。暂无技术失败。
- 原始严格 v1 分数：Sol raw improved10/regressed9，final improved0/regressed1；Luna raw improved19/regressed14，final improved0/regressed2。**这些不是最终文档收益结论**，第三次仍进行中，且存在税费唯一引用位置评分伪回退。
- 评分审计 v2 已生成并测试：两版一致删除 OD-09 “必须引用KB-1004”约束，因为修订版 Rule3/KB-1003 也直接支持缺口说明。v1 保存在 fixtures/policy-comparison-oracle-v1.json；default与explicit-v2一致。冻结运行仍保持 v1 输入；后续只对保存结果用同一冻结 evaluator 离线重算，原始分数保留，不重跑API、不新增税费规则。
- 已观察到的方向：OD-05/08 明示有助于减少未批准金额/资格的确定断言；Luna 部分已知计算案例出现 amount=None 或金额带说明文本（格式/完整性问题，不应直接称算术错误）。固定 gate 仍覆盖 pending，造成原文与优化版都存在相同边界失败。
- V5原生tax输出由 EvidenceBoundCandidate 约束为unknown/not_applicable；不能把零yes/no计为文档提升自由推理。理解阶段不读policy；final随机差异不能自动归因于文档。
- 主workflow已升级v7：下一棒只在model owner的v7回归结论后做少量固定v7 matched确认，不运行v6，也不重复全矩阵。当前先完成并正确解释v5文档cohort。
- Policy比较入口新增fail-before-call above-high guard，13项相关测试通过；本批固定medium符合上限，冻结旧输入未改变。仍未改默认policy。

## Final READY receipt

- Reviewed compact machine summary: `docs/policy_comparison/20261011-full-v5-audited/summary.json`. This is the HTML consumer entry; artifact_type=policy_pair_comparison, status=complete.
- Readable judgement: `docs/policy_comparison/20261011-full-v5-audited/assessment.md`; tables: `report.md`; compact per-case/repeat diagnostics: `results.json`.
- Completed denominators: 2 models × 40 cases × 3 repeats × 2 policy sides = 480/480 scenario runs, 240/240 matched pairs; zero technical failures. Both processes completed without budget abort.
- Cohort actual workflow-v5/code `a1e13e3b83d1be6de090d9eeb11829d85f5f65b8fe9b9cdb6f274d9098dcd099`; source frozen and checksum verified. Folder `v4` is historical naming only; do not present as v4 or current v8.
- v2 audit raw composite: Sol85→100/120 (improved19/regressed4); Luna63→75/120 (improved29/regressed17). Final: Sol105→104/120 (improved0/regressed1), Luna95→94/120 (improved1/regressed2).
- Supported closed-field raw: Sol102→105; Luna93→85. This includes amount formats/status conventions, not unrestricted business-semantic correctness.
- Raw open-policy boundary failures: Sol15→3, Luna6→0. Final boundary failures12→12 per model; four unresolved cases ×3 repeats.
- Formal API client-estimated cost $5.23917547, formal unknown reservations0. Global ledger also contains other owner usage and interrupted calls; see live ledger for its cumulative bound.
- V1 original scoring, raw data and hashes retained. V2 common offline audit removes uniqueKB1004 citation gold for OD09. No model reruns, no invented tax rule, no oracle change to make fixedgate assumptions pass. All12 final pending-boundary failures remain.
- Machine summary includes exact configs/prompt/code/corpus/version manifests, v1/v2 overlay provenance, side summaries/usage, paired transitions, source hashes and recommendation not to promote whole revision.
- Core owner accepted **no promotion** and explicitly deferred additional v8 paid confirmation. No further policy API process will be started. Default policy remains original.
- Local compatibility recheck:280 tests passed; owned comparison tests13 passed. Formal frozen source checkpoint208 passed. These are distinct checkpoints, not live semantic measurements.

## ACTIVE USER-AUTHORIZED NEXT ROUND — scenario policy / v9 gate (2026-10-11 20:05 UTC)

Direct human authorization in this chat: new immutable policy, scenario-triggered open decisions, fix gate overriding justified caution, rerun same cases/models/configs within cumulative $70.

READY for integration: boundaries.py plus workflow.py import `apply_boundaries`, prompt-version `workflow-v9-scenario-boundaries`, one call immediately BEFORE candidate mismatch comparison. No EXTRACT or PLAN text changed by this owner. Workflow hook complete; this owner will stop editing workflow.py so root can complete new authorized extraction/repair/scope changes. Preserve hook and diagnostic additions. Full local suite 330 passed at this checkpoint. Core workflow not yet frozen for paid testing; awaiting latest root acceptance via docs/mvp_fix_status.md. This owner retains boundaries.py/policy/comparison/tests ownership. New snapshot `20261011T200142302410Z-scenario`, parent clarified, all OD still OPEN. Original and clarified snapshots/results untouched.

Planned exact configs unchanged: Sol/Luna medium, 40 cases ×3 repeats. Both original→scenario and clarified→scenario matched comparisons on SAME latest frozen workflow, separate denominators. Same v2 oracle; no business assumption approved by scoring. Shared ledger currently ~$22.90, hard cap70; estimate additional <=$12 actual, monitor all-thread usage. Freeze only AFTER core final-ready. No benchmark published as latest before that.

### Latest human steering (2026-10-11 20:06 UTC)
User explicitly fixed policy hill climbing to `anthropic/claude-haiku-5-5/adaptive/medium`. This supersedes planned Sol/Luna main runs. Future matched batches use ONLY selected Haiku config, same40×3, all same latest frozen workflow. Planned original→scenario AND clarified→scenario, then one isolated clause iteration iff case diagnostics support it. Retain raw/final and old models' historical results. No unapproved business choices. Shared70ledger unchanged.

Workflow ownership handoff COMPLETE: this policy owner has stopped workflow edits after exactly import/hook/PROMPT_VERSION changes; root v10 may rename version, preserve hook immediately before candidate mismatch checks. Await root latest core READY before freezing. Boundary module targeted14 tests pass; last all330pass before root's further work. No paid new batch has started.

Boundary owner READY (20:09 UTC): targeted32pass (19boundary+13comparison). Added offline gate-only diagnostic `runs/policy-gate-v9-recorded-trace-audit/summary.json`: original saved v5 traces re-scored on unchanged v2 oracle, each of four120-run side/model cohorts improves EXACTLY12 final runs, final boundary12→0, zero formerly passing regressions. This is not a new provider/latest core acceptance. Known integral three-lines computation remains110; repeat90 preserves independently known amount while leaves action pending. Root already integrated hook and versionv10; owner continues not editing workflow. Await latest core READY for paid Haiku-only fixed-model comparisons/hill climb. No paid new batch yet.

## Immutable latest core captured — awaiting live READY
Frozen input directory `runs/policy-inputs-v10-haiku-20261011T2016`: main and frozen full suites BOTH372 passed. All source/config/case/oracle/version hashes saved, no credentials copied. Workflow bytes match root receipt d6970f29d545ef28d50ba9573e35ca716517f28a3743c6b02ce99dc045bd3709; same v10 gate for every policy. Pairing matrix explicitly config/development-default.json, exact Haiku adaptive/medium. Policy paid comparison will start after v10 live READY; no paid batch yet. Planned original→scenario and clarified→scenario each120pairs=240scenario runs, total480. Additional hill-climb round only based on diagnoses, same frozen code; new snapshot may be separately hash-verified rather than changing original frozen receipt.

HOLD accepted (20:17 UTC): v10 original live protocol failure after one repair. Captured immutable inputs preserved as DIAGNOSTIC ONLY, separate receipt `runs/policy-inputs-v10-haiku-20261011T2016-status.json`; no snapshot bytes changed, ZERO paid policy cohort started. Await latest core READY, then capture another immutable version and run fixed Haiku comparisons. User informed honestly that372localtests≠liveacceptance. Policy draft/gate tests ready, not promoted.
