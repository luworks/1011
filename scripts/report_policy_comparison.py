#!/usr/bin/env python3
"""Aggregate completed matched experiments without rerunning or tuning models."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seconds(value):
    return f'{value:.2f}' if isinstance(value, (int,float)) else 'unavailable'


def compact(report):
    grouped={}
    for row in report['records']:
        c=grouped.setdefault(row['case_id'], {'runs':0,'raw_pass':0,'final_pass':0,
            'raw_supported_pass':0,'final_supported_pass':0,'raw_citation_fail':0,
            'raw_boundary_fail':0,'final_boundary_fail':0,'technical_fail':0,
            'unresolved_policy':row['unresolved_policy'],'change_ids':row['change_ids'],'diagnostics':[]})
        c['runs']+=1
        for field,name in [('raw_pass','candidate_passed'),('final_pass','passed'),
                           ('raw_supported_pass','raw_supported_passed'),('final_supported_pass','final_supported_passed')]:
            c[field]+=bool(row[name])
        c['raw_citation_fail']+=any(not cite['faithful'] for cite in row['citation_diagnostics'])
        c['raw_boundary_fail']+=bool(row['boundary_errors']['raw'])
        c['final_boundary_fail']+=bool(row['boundary_errors']['final'])
        c['technical_fail']+=bool(row['technical_errors'])
        checks=[]
        for check in row['checks']:
            small={key:check[key] for key in ('intent','expected','pre_errors','post_errors')}
            for stage in ('actual','candidate'):
                value=check.get(stage)
                small[stage]=None if value is None else {key:value.get(key) for key in ('intent','question','policy_ids','amount','answer_status','action_status','tax_adjustment')}
                if value:
                    small[stage]['evidence_sources']=[ref.get('source_id') for ref in value.get('evidence',[])]
            checks.append(small)
        c['diagnostics'].append({'repeat':row['repeat'],'checks':checks,
            'pre_turn_errors':row['pre_turn_errors'],'turn_errors':row['turn_errors'],
            'citation_diagnostics':row['citation_diagnostics'],'boundary_errors':row['boundary_errors'],
            'technical_errors':row['technical_errors']})
    return grouped


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs',nargs='+',type=Path)
    parser.add_argument('--frozen-inputs',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--oracle-overlay',type=Path,help='Common offline scoring audit, retaining original scores')
    args=parser.parse_args()
    frozen=json.loads((args.frozen_inputs/'frozen-inputs.json').read_text())
    for relative,expected in frozen['files'].items():
        if digest(args.frozen_inputs/relative)!=expected:
            raise ValueError('Frozen input changed')
    code=hashlib.sha256()
    for p in sorted((args.frozen_inputs/'src/policy_agent').glob('*.py')):
        code.update(p.name.encode()+p.read_bytes())
    experiments=[]
    projected=None
    if args.oracle_overlay:
        import policy_agent.comparison as scoring_module
        if Path(scoring_module.__file__).resolve() != (args.frozen_inputs/'src/policy_agent/comparison.py').resolve():
            raise ValueError('Offline audit must import the same frozen evaluator via PYTHONPATH')
        from policy_agent.comparison import project_oracles, score_projected, compare_records
        from policy_agent.evaluation import load_cases, summarize, attach_usage
        projected={c['id']:c for c in project_oracles(load_cases(args.frozen_inputs/'fixtures/scenarios.json'), json.loads(args.oracle_overlay.read_text()))}
    controls=None
    for folder in args.runs:
        if (folder/'EXCLUDED.json').exists():
            raise ValueError('Excluded run must not enter formal report')
        manifest=json.loads((folder/'manifest.json').read_text())
        summary=json.loads((folder/'summary.json').read_text())
        original_counts=summary['matched']['counts']
        current={key:manifest[key] for key in ('prompt_sha256','cases_file_sha256','oracle_overlay_sha256','selected_projected_suite','repeats','jobs')}
        current['policy_versions']={side:manifest['snapshots'][side]['policy_snapshot']['manifest_sha256'] for side in ('baseline','candidate')}
        if controls is not None and current!=controls:
            raise ValueError('Experiments do not have matched controls')
        controls=current
        if any(s['code_sha256']!=code.hexdigest() for s in manifest['snapshots'].values()):
            raise ValueError('Experiment code differs from frozen source')
        if projected is not None:
            rows={'baseline':[],'candidate':[]}
            for side,report in summary['reports'].items():
                for row in report['records']:
                    audit=score_projected(projected[row['case_id']],row['turns'])
                    audit.update(repeat=row['repeat'],turns=row['turns'],calls=row['calls'],policy_version=row['policy_version'])
                    rows[side].append(audit)
                audited={'records':rows[side],'summary':summarize(rows[side],manifest['planned_pairs'],len(manifest['selected_projected_suite']['ids']))}
                attach_usage(audited,[call for r in rows[side] for call in r['calls']])
                summary['reports'][side]=audited
            summary['matched']=compare_records(rows,manifest['planned_pairs'])
        rows={side:compact(summary['reports'][side]) for side in ('baseline','candidate')}
        experiments.append({'run_directory':str(folder.resolve()),'config':manifest['config'],
            'manifest':manifest,'matched':summary['matched'],'original_strict_counts':original_counts,
            'summaries':{side:summary['reports'][side]['summary'] for side in rows},
            'usage':{side:summary['reports'][side]['usage'] for side in rows},
            'cases':rows,
            'source_hashes':{name:digest(folder/name) for name in ('manifest.json','summary.json','turns.jsonl','oracle.json')}})
    result={'created_at_utc':datetime.now(timezone.utc).isoformat(),'controls':controls,
        'frozen_inputs_manifest_sha256':digest(args.frozen_inputs/'frozen-inputs.json'),
        'frozen_inputs_directory':str(args.frozen_inputs.resolve()),'code_sha256':code.hexdigest(),
        'experiments':experiments,'claim_scope':'Paired exploratory results on existing cases; no single-edit causal attribution or fresh holdout claim.',
        'scoring_audit':None if args.oracle_overlay is None else {'overlay_path':str(args.oracle_overlay.resolve()),'overlay_sha256':digest(args.oracle_overlay),'scope':'Common offline re-score of saved outputs; original strict counts retained. No API calls.'}}
    args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    lines=['# Nimbus policy 版本实验结果','',f"两份文档按成对版本运行；相同模型内部固定配置、{controls['selected_projected_suite']['scenario_count']} 个案例、{controls['repeats']} 次重复，baseline/candidate 交替运行顺序。所列模型均使用同一冻结 workflow。", '',
        '| 模型/配置 | 有效配对 | raw baseline→candidate | final baseline→candidate | raw 改善/回退 | final 改善/回退 |', '|---|---:|---:|---:|---:|---:|']
    if args.oracle_overlay:
        lines[4:4]=['评分审计：使用共同 v2 overlay 离线重算税费来源检查；Rule 3/KB-1003 的有效依据不因未引用 KB-1004 而被判错。原始严格评分保存在 results.json 的 original_strict_counts 与原 run summary，不改写或删除。未新增税费业务规则，未重跑模型。','']
    for e in experiments:
        old,new=e['summaries']['baseline'],e['summaries']['candidate'];m=e['matched']
        lines.append(f"| {e['config']['config_id']} | {m['matched_completed_pairs']}/{m['planned_pairs']} | {old['candidate_conversation_success']['numerator']}→{new['candidate_conversation_success']['numerator']} / {old['completed_runs']} | {old['conversation_success']['numerator']}→{new['conversation_success']['numerator']} / {old['completed_runs']} | {m['counts']['raw']['improved']}/{m['counts']['raw']['regressed']} | {m['counts']['final']['improved']}/{m['counts']['final']['regressed']} |")
    lines+=['','raw 合格同时要求支持的结构化断言、引用忠实度和待决证据边界；final 合格包含固定 gate 输出的边界检查。表中的失败不都代表业务答案错误。待决字段不设唯一业务答案。', '',
        '| 模型 | supported raw baseline→candidate | raw 引用失败 baseline→candidate | raw 待决边界失败 baseline→candidate | final 待决边界失败 baseline→candidate |', '|---|---:|---:|---:|---:|']
    for e in experiments:
        counts={side:{field:sum(c[field] for c in cases.values()) for field in ('raw_supported_pass','raw_citation_fail','raw_boundary_fail','final_boundary_fail')} for side,cases in e['cases'].items()}
        values=[f"{counts['baseline'][field]}→{counts['candidate'][field]}" for field in ('raw_supported_pass','raw_citation_fail','raw_boundary_fail','final_boundary_fail')]
        lines.append('| '+e['config']['model']+' | '+' | '.join(values)+' |')
    lines+=['','## 逐案例变化','','只列 raw/final 合格次数改变的案例；完整重复结果、结构化检查、引用问题和待决边界见 results.json。关联 E 编号仅是案例与修改范围的对应，不能证明某一处编辑单独造成变化。', '',
        '| 模型 | 案例 | raw baseline→candidate / 3 | final baseline→candidate / 3 | 关联修改 | 待决 |', '|---|---|---:|---:|---|---|']
    for e in experiments:
        for cid,old in e['cases']['baseline'].items():
            new=e['cases']['candidate'].get(cid)
            if new and (old['raw_pass']!=new['raw_pass'] or old['final_pass']!=new['final_pass']):
                lines.append(f"| {e['config']['model']} | {cid} | {old['raw_pass']}→{new['raw_pass']} | {old['final_pass']}→{new['final_pass']} | {', '.join(new['change_ids'])} | {', '.join(new['unresolved_policy'])} |")
    lines+=['','## 代价与限制','','| 模型 | baseline费用估计 | candidate费用估计 | baseline full-turn P50/P95 秒 | candidate full-turn P50/P95 秒 |', '|---|---:|---:|---|---|']
    for e in experiments:
        old,new=e['usage']['baseline'],e['usage']['candidate']
        lines.append(f"| {e['config']['model']} | ${old['reported_cost_usd']:.4f} | ${new['reported_cost_usd']:.4f} | {seconds(old['turn_latency_p50_seconds'])}/{seconds(old['turn_latency_p95_seconds'])} | {seconds(new['turn_latency_p50_seconds'])}/{seconds(new['turn_latency_p95_seconds'])} |")
    lines+=['',
        '- 固定 gate 不会根据 policy 文本重新编译规则；最终输出可继续暴露旧实现假设。',
        '- 两版各自执行完整的理解阶段；该阶段不读取 policy，差异可来自模型随机性，不能自动归因于文档改写。provider 未固定 seed。',
        '- PLAN prompt 已明确 outage exception、全局限制和税费边界。本轮衡量此 workflow 内文档变化，不是无提示的独立阅读能力。',
        '- 本批冻结 workflow 使用 EvidenceBoundCandidate 限制 tax_adjustment 为 unknown/not_applicable。税费 yes/no 未出现不能计为文档改善了自由推理或消除了幻觉；它是已有 schema 边界。',
        '- 当前 Corpus 只提取 Rule/KB 正文，文档头部/总则改写 E01、E02 中的总则、E12 的文章计数不进入检索证据；不能声称测试了这些改动。',
        '- OD-01/02/06/07 的关键业务分歧没有专门案例；待决字段的保守结构化边界检查不等于业务批准规则或完整自然语言语义审计。',
        '- 既有案例包含开发历史；frozen 标签不代表全新 holdout。三次重复仅用于观察稳定性，不能证明统计显著或泛化。',
        '- 实际模型、jobs 与并发控制以各 manifest 为准；延迟反映此并发/服务状态，费用来自矩阵和 provider token usage 的客户端估计。',
        '- 早期工作区源码漂移而中止的实验明确排除，记录仍保留；共享账本包含其已报告成本和未结算预留。', '',
        '冻结输入：'+str(args.frozen_inputs.resolve()),'','版本标识：']
    for e in experiments:
        lines.append('- '+e['manifest']['snapshots']['baseline']['policy_snapshot']['version_id']+' → '+e['manifest']['snapshots']['candidate']['policy_snapshot']['version_id']+'; '+e['manifest']['snapshots']['baseline']['prompt_version'])
    lines+=['','原始结果目录：']
    for e in experiments:
        lines.append('- '+e['run_directory'])
    (args.output/'report.md').write_text('\n'.join(lines)+'\n')
    print(args.output/'report.md')


if __name__=='__main__':
    main()
