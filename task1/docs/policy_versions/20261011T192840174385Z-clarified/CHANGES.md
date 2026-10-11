# 优化版逐处修改说明

本文件属于同一时间戳的 policy pair 快照。状态为 `editorial-draft`：明确冲突已修正，未确认的业务语义仍标为待决。没有改变 $75/$300 金额、4 小时/30 天/60 天/90 天阈值，也没有新增税费结论。原始业务生效日期和 KB 更新时间保留；本次编辑时间见 manifest。

| ID | 修改位置 | 修改内容 | 原因与依据 | 类型 |
|---|---|---|---|---|
| E01 | 两份文档头部 | 增加草案状态、快照来源和 OPEN DECISION 的阅读约定 | 避免把编辑版本当成已批准政策，或把待决项当成答案；跨文档权威关系见 OD-01 | 编辑标注 |
| E02 | Policy 开头 | 明确 Rule 3 替换 Rule 2 的计算轨道/上限，但不覆盖 Rules 4/5；Rule 1 关系待决 | Rule 3 的独立轨道与 Rule 5 的 regardless 原句已支持此澄清；不能把 specific rule 优先解释成清除所有限制 | 已有规则澄清 |
| E03 | Policy Rule 1；KB-1001 | 标注 30/60 天关系与边界待决；KB 补回超 60 天可经 Tier 2 考虑且不保证解决，并明确 calendar days | KB 遗漏 Policy Rule 1 已有的超期路径；两个时钟有不同起点，但是否同时约束 standalone outage 未明确 | 对齐 + 待决 |
| E04 | Policy Rule 2/3；KB-1002/1005 | 明确 fallback 是重新评估，仍检查 Rule 2 前提，不是自动给 $75；标注无 confirmed error 能否 goodwill | Rule 2 明确 confirmed billing error，Rule 3 要求 fallback；未授权推导新的 discretionary entitlement | 澄清 + OD-03 |
| E05 | Policy Rule 3；KB-1005 第 2 步 | 将“条件不满足”区分为已证实不满足与缺少证据；列出不存在/不可核验/未完成查询差异及未定组合状态 | Rule 3 无 ticket 走 fallback，Rule 4(b) 不可核验走 Tier 2；查不到结论不能等于查明不存在 | 澄清 + OD-04 |
| E06 | Policy Rule 3/5；KB-1001/1004/1005/1007 | 增加 full days、零金额、部分天、舍入、线路分摊、费率时点和日期/重复争议边界待决标注 | 原文未定义；不将当前代码的 24 小时/half-up 约定写成批准规则 | OD-05 至 OD-08 |
| E07 | Policy Rule 3；KB-1003/1004 | 明确月费计算基数不能证明后续税费调整结果；将真实税费规则及核实流程列为待决 | KB-1004 只限定 credit base，KB-1003 只描述账单组成；不能推出会退或不退 | 证据缺口 + OD-09 |
| E08 | Policy Rule 4 Note | 删除 outage “only … condition (b)” 的排他性说明；改为保留 b/c/d 与 Rule 5 | 原句与 Rule 4(c)/(d)、Rule 5 的跨类型强制审批冲突 | 明确冲突修正 |
| E09 | KB-1005 第 6 步；KB-1006/1007 | 将金额/时长达标限定为局部条件，明确还要核验、资格及全局升级；KB-1006 提及 Rule 1 超期 sign-off | 原流程的直接授权容易覆盖不可核验、重复争议或欺诈限制；未替业务选择 Rule 1 的 standalone outage 范围 | 明确授权修正 + 对齐 |
| E10 | KB-1002 上限承诺句 | 从“不承诺单笔 > $75”改为“不承诺会让累计总额 > $75 的 credit” | 同段已定义累计限额；历史 $60 + 本次 $20 也需要批准，不能只看本次金额 | 已有规则澄清 |
| E11 | KB-1004/1005 | 明确 outage 不计入 general goodwill 累计；补齐 ≤4 小时及 >30 天请求的 fallback；30 天明确 calendar days | 都来自 Policy Rule 3，原 KB 流程遗漏部分分支和累计口径 | 跨文档对齐 |
| E12 | KB 导出头部 | 9 articles 改为 10 articles | 正文实际为 KB-1001 至 KB-1010，包含十篇 | 元数据修正 |

未修改 KB-1008/1009/1010 的业务正文，未修改原始 exam 文件或当前 config/corpus-lock.json，也未切换运行中的默认 corpus。没有写入新的税费金额、退款承诺、minimum credit、受影响线路分摊算法或日期包含规则。

## 审核方式

用本版本与 parent 的逐行 diff 检查全部文本变化；E01–E12 覆盖本次所有修改类别。每项待决选择在 OPEN_DECISIONS.md 中列出，全部为 OPEN。只有获得业务决定后，才在新时间戳版本中发布相应规则和依据；不在本快照原地补写。
