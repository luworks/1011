import React, { useState } from 'react';
import { DataComponent, ReportSection, RichNarrative, useDataApp } from '../../data-app-public.jsx';
const num=(v,d=2)=>v == null ? '—' : Number(v).toFixed(d);
const pct=(r,k)=>r[k] == null ? '—' : `${(r[k]*100).toFixed(1)}% (${r[k+'_counts']})`;
export function ReportContent(){
 const {snapshot,appTitle,visible}=useDataApp();
 const rows=snapshot.queries.models.rows;
 const [stage,setStage]=useState(rows.find(r=>!r.stage.startsWith('historical'))?.stage || 'all');
 const selected=snapshot.selection||{};
 const filtered=rows.filter(r=>stage==='all'||r.stage===stage);
 const stages=[...new Set(rows.map(r=>r.stage))];
 const winner=selected.winner;
 const summary=winner?`## Executive Summary\n\n当前推荐 **${winner}**。选择状态：**${selected.status}**。先排除最终关键错误，再最大化会话成功率；准确率相同才比较整轮 P95、P50，最后比较每次成功会话成本。\n\n${(selected.reasons||[]).join(' ')}`:`## Executive Summary\n\n**尚不能推荐最终模型。** 最新候选配置的完整比较尚未完成。下方保留正式初筛结果；它们不能替代新工作流的独立验收。\n\n选型顺序已固定：准确率最高 → 整轮响应最快 → 价格最低。不会用低价抵消关键政策错误。`;
 return <article className="report-content model-report">
  <header className="report-hero"><h1>{appTitle}</h1><RichNarrative id="report:intro" value="Policy-Grounded Agent · GPT-6 Luna / GPT-6.1 Sol / Claude 5.5 · 不同 thinking 配置" /><p className="report-snapshot" data-reviewed-rows>快照生成时间：{snapshot.generatedAt} · 数据不会自动更新</p></header>
  {visible('report-summary')&&<ReportSection id="report-summary" queryId="models" title="Executive Summary" showHeading={false} sourceRows={rows}><RichNarrative id="report-summary:body" value={summary}/></ReportSection>}
  {snapshot.coordination && <ReportSection id="report-coordination" queryId="coordination" title="协同进度" showHeading={false} sourceRows={snapshot.queries.coordination.rows}><RichNarrative id="report-coordination:body" value={snapshot.coordination.narrative}/></ReportSection>}
  <RichNarrative id="report:scope" value="## 各配置的实际表现\n\n表格保留阶段、场景与重复运行分母。关口前表示模型候选判断；关口后表示程序检查后的最终判断。缺失测量显示 —，不能解释为零错误或零耗时。本表为相同三案例初筛的原始分母，未将其改写为完整验收成绩。"/>
  <div className="model-controls"><label>评测阶段 <select value={stage} onChange={e=>setStage(e.target.value)} aria-label="评测阶段"><option value="all">全部阶段</option>{stages.map(s=><option key={s}>{s}</option>)}</select></label><span>{filtered.length} 个配置结果</span></div>
  {visible('model-table')&&<DataComponent id="model-table" queryId="models" kind="table" title="模型、准确率、整轮速度与成本" sourceRows={filtered} displayRows={filtered}>
   {filtered.length?<div className="model-table-scroll"><table data-reviewed-rows><thead><tr>{['模型 / thinking','阶段','独立场景','完成 / 计划','会话成功','关口前断言','关口后断言','关键错误','强制升级召回','技术失败','P50 秒','P95 秒','总费用 USD','成功会话 USD','政策准确率','金额准确率','可回答完成率','过度拒答率','输入 / 输出 / 缓存 token'].map(h=><th key={h}>{h}</th>)}</tr></thead><tbody>{filtered.map((r,i)=><tr key={r.stage+r.config_id+i}><td><strong>{r.model}</strong><small>{r.thinking_mode} / {r.thinking}</small><small>{r.config_id}</small></td><td>{r.stage}</td><td>{r.unique??'—'}</td><td>{r.completed??'—'} / {r.planned??'—'}<small>{r.status}</small></td><td>{pct(r,'conversation_success')}</td><td>{pct(r,'pre_gate_assertion_success')}</td><td>{pct(r,'post_gate_assertion_success')}</td><td>{r.critical??'—'}</td><td>{pct(r,'mandatory_escalation_recall')}</td><td>{r.api_failures??'—'}</td><td>{num(r.p50)}</td><td>{num(r.p95)}</td><td>{num(r.cost,4)}</td><td>{num(r.cost_per_success,5)}</td><td>{pct(r,'policy_accuracy')}</td><td>{pct(r,'amount_accuracy')}</td><td>{pct(r,'answerable_completion')}</td><td>{pct(r,'over_refusal_rate')}</td><td>{r.input_tokens??'—'} / {r.output_tokens??'—'} / {r.cached_tokens??'—'}</td></tr>)}</tbody></table></div>:<p>此阶段尚无已完成的结果。</p>}
  </DataComponent>}
  <RichNarrative id="report:methods" value="## 如何解读这个选择\n\n- **质量关口：** 必须没有已审计的最终关键失败、强制升级遗漏与无依据税费结论，才进入速度比较。未测量不等于通过。\n- **可比范围：** 仅相同场景、重复次数、提示词、代码和语料版本的完整评测可支持最终选型。小规模筛选帮助缩小候选范围，不能证明全局最优。\n- **速度：** P50 表示典型整轮耗时，P95 表示较慢的尾部响应；不是单次 API 请求耗时。不同 thinking 设置是不同配置。\n- **成本：** 包含额外修复、重试及已记录 token；供应商账单可能不同。没有成功会话时不计算成功成本。\n- **不确定性：** 冻结场景重复三次仍是同一组独立场景；速度置信区间重叠时推荐为暂定。通过有限测试不代表真实环境零幻觉。"/>
  <ReportSection id="report-evidence" title="来源与版本" queryId="models" sourceRows={rows} showHeading={false}><RichNarrative id="report:evidence" value="## 来源与版本\n\n所有数值来自指定运行目录的 summary.json 与 manifest.json。来源面板记录文件哈希和指标定义；下面的版本记录方便复核。未完成或历史结果不会自动生成推荐。"/><details><summary>查看每个结果的证据标识</summary><div className="model-provenance" data-reviewed-rows>{rows.map((r,i)=><div key={i}><strong>{r.stage} · {r.config_id}</strong><p>{r.source}</p><code>prompt: {r.prompt??'unknown'}<br/>code: {r.code??'unknown'}<br/>corpus: {r.corpus??'unknown'}</code></div>)}</div></details></ReportSection>
 </article>
}
