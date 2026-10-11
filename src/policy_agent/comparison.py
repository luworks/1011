"""Matched policy experiments: independent raw/final scoring and open decisions."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import hashlib
import json
from pathlib import Path

from .corpus import Corpus
from .evaluation import load_cases, freeze_manifest, model_input, score_case, summarize, attach_usage
from .providers import Budget, Provider
from .versions import version_directory, sha256
from .workflow import run_scenario, EXTRACT, PLAN


def project_oracles(cases: list[dict], overlay: dict) -> list[dict]:
    """Remove ONLY reviewed ambiguous assertions, from final and every-turn oracles."""
    if overlay['source_suite_sha256'] != freeze_manifest(cases)['sha256']:
        raise ValueError('Oracle overlay does not match the exact source suite')
    ids = {c['id'] for c in cases}
    if set(overlay['cases']) - ids:
        raise ValueError('Overlay contains unknown case IDs')
    projected = copy.deepcopy(cases)
    for case in projected:
        annotation = overlay['cases'].get(case['id'], {})
        case['expected']['unresolved_policy'] = annotation.get('unresolved', [])
        case['expected']['change_ids'] = annotation.get('change_ids', [])
        omitted = annotation.get('omit', {})
        for questions in [case['expected'].get('questions', [])] + [
                t.get('questions', []) for t in case['expected'].get('turns', [])]:
            for question in questions:
                for field in omitted.get(question['intent'], []):
                    if field not in ('amount', 'policy', 'answer_status', 'action_status'):
                        raise ValueError('Unsupported oracle omission field')
                    question.pop(field, None)
        case['expected']['excluded_fields'] = omitted
        case['expected']['boundary_intents'] = annotation.get('boundary_intents', [])
    return projected


def score_projected(case: dict, turns: list[dict]) -> dict:
    result = score_case(case, turns)
    expected = case['expected']
    result['unresolved_policy'] = expected.get('unresolved_policy', [])
    result['excluded_fields'] = expected.get('excluded_fields', {})
    result['change_ids'] = expected.get('change_ids', [])
    result['fully_resolved'] = not result['unresolved_policy']
    boundary = {'raw': [], 'final': []}
    for index, turn in enumerate(turns):
        for stage, rows in [('raw', (turn.get('candidate') or {}).get('questions', [])),
                            ('final', turn.get('decisions', []))]:
            for row in rows:
                intent = row.get('intent', row.get('question'))
                fields = result['excluded_fields'].get(intent, [])
                reasons = []
                if intent in expected.get('boundary_intents', []):
                    if row.get('action_status') == 'eligible_for_simulation':
                        reasons.append('issuance_eligibility_with_open_policy')
                    if row.get('answer_status') == 'grounded':
                        if 'amount' in fields and row.get('amount') is not None:
                            reasons.append('definite_amount_with_open_policy')
                        if 'policy' in fields and row.get('policy_ids'):
                            reasons.append('definite_policy_track_with_open_policy')
                if intent == 'taxes' and stage == 'raw' and row.get('tax_adjustment') in ('yes', 'no'):
                    reasons.append('unsupported_tax_outcome')
                if reasons:
                    boundary[stage].append({'turn_index': index, 'intent': intent, 'reasons': reasons})
    result['boundary_errors'] = boundary
    # Separate business assertions from citation fidelity and evidence boundaries.
    result['raw_supported_passed'] = bool(turns) and not result['technical_errors'] and not result['pre_turn_errors'] and all(not c['pre_errors'] for c in result['checks'])
    result['final_supported_passed'] = result['passed']
    result['candidate_passed'] = result['candidate_passed'] and not boundary['raw']
    result['passed'] = result['passed'] and not boundary['final']
    result['critical_final_failure'] |= bool(boundary['final'])
    return result


def _delta(old: bool, new: bool) -> str:
    return 'improved' if new and not old else 'regressed' if old and not new else 'unchanged_pass' if old else 'unchanged_fail'


def compare_records(records: dict[str, list[dict]], planned: int) -> dict:
    indexed = {side: {(r['case_id'], r['repeat']): r for r in rows}
               for side, rows in records.items()}
    keys = sorted(set(indexed['baseline']) & set(indexed['candidate']))
    pairs = []
    for key in keys:
        old, new = indexed['baseline'][key], indexed['candidate'][key]
        # Failures/budget omissions remain in denominators but not matched quality deltas.
        if old['technical_errors'] or new['technical_errors']:
            continue
        stages = {}
        for stage, name in [('raw', 'candidate_passed'), ('final', 'passed')]:
            stages[stage] = {'status': _delta(old[name], new[name]),
                'supported_assertions': _delta(old[f'{stage}_supported_passed'], new[f'{stage}_supported_passed']),
                'boundary': _delta(not old['boundary_errors'][stage], not new['boundary_errors'][stage])}
        pairs.append({'case_id': key[0], 'repeat': key[1], 'stages': stages,
                      'change_ids': new['change_ids'], 'unresolved_policy': new['unresolved_policy']})
    counts = {stage: {status: sum(p['stages'][stage]['status'] == status for p in pairs)
              for status in ('improved', 'regressed', 'unchanged_pass', 'unchanged_fail')}
              for stage in ('raw', 'final')}
    components = {stage: {component: {status: sum(p['stages'][stage][component] == status for p in pairs)
                  for status in ('improved','regressed','unchanged_pass','unchanged_fail')}
                  for component in ('supported_assertions','boundary')} for stage in ('raw','final')}
    return {'planned_pairs': planned, 'matched_completed_pairs': len(pairs),
            'missing_or_technical_pairs': planned-len(pairs), 'counts': counts, 'pairs': pairs,
            'component_counts':components,
            'attribution_limit': 'Change IDs are scenario associations, not per-edit causal effects; both documents changed together. Use single-edit ablations for attribution.'}


def write_comparison(out: Path, reports: dict, matched: dict) -> None:
    lines = ['# Policy 版本成对对比', '',
        '同一案例、模型配置、prompt、检索算法和固定 gate；原始判断与最终输出分别评分。', '',
        f"计划 {matched['planned_pairs']} 对；有效配对 {matched['matched_completed_pairs']}；缺失/技术失败 {matched['missing_or_technical_pairs']}。", '',
        '| 层级 | 改善 | 变差 | 持续通过 | 持续失败 |', '|---|---:|---:|---:|---:|']
    for stage in ('raw','final'):
        c=matched['counts'][stage]
        lines.append(f"| {stage} | {c['improved']} | {c['regressed']} | {c['unchanged_pass']} | {c['unchanged_fail']} |")
    lines += ['', 'raw 合格包含已支持断言、引用忠实度和证据边界；业务断言、引用问题和待决边界在 summary.json 分别保留。待决字段从唯一答案评分排除；保留适用的明确规则检查。', '',
        '| 案例 | 重复 | raw | final | 关联修改 | 待决 |', '|---|---:|---|---|---|---|']
    for p in matched['pairs']:
        if any(p['stages'][stage]['status'] in ('improved','regressed') for stage in ('raw','final')):
            lines.append(f"| {p['case_id']} | {p['repeat']} | {p['stages']['raw']['status']} | {p['stages']['final']['status']} | {', '.join(p['change_ids'])} | {', '.join(p['unresolved_policy'])} |")
    lines += ['', '关联修改不能证明某一处文字单独造成变化：这是整组文档实验，逐项因果归因需要 ablation。', '',
        '固定 gate 不会自动编译新文档；它可能掩盖模型差异或继续输出未批准的实现假设。这些边界失败独立保留。', '',
        '本批既有案例包含已用于开发/调试的 frozen 标记，不能宣称全新 holdout 或统计显著性。未支持自然语言的语义判断仍需人工审核。', '']
    for side, report in reports.items():
        u=report['usage']
        lines.append(f"{side}: reported cost ${u['reported_cost_usd']:.6f}; full-turn P50={u['turn_latency_p50_seconds']}, P95={u['turn_latency_p95_seconds']}; samples={u['turn_latency_sample_count']}; unknown cost=${u['reserved_or_unknown_cost_usd']:.6f}.")
    (out/'comparison.md').write_text('\n'.join(lines)+'\n')


def run_comparison(args) -> int:
    from .cli import configurations, dump, start_snapshot
    if args.repeats < 1 or not 1 <= args.jobs <= 8:
        raise ValueError('Positive repeats and jobs between 1 and 8 required')
    if args.baseline == args.candidate:
        raise ValueError('Comparison requires different policy versions')
    configs = [c for c in configurations(args.matrix) if c.get('config_id') == args.config_id]
    if len(configs) != 1:
        raise ValueError('Comparison requires one unique exact config-id')
    config = configs[0]
    if any(config.get(key) in ('xhigh','max','ultra') for key in ('reasoning_effort','effort')):
        raise ValueError('Policy comparison effort ceiling is high; above-high calls are not authorized')
    corpora = {side: Corpus(version_directory(value)) for side, value in (
        ('baseline', args.baseline), ('candidate', args.candidate))}
    original = load_cases(args.cases)
    if any(c.get('split') not in ('dev','frozen') for c in original):
        raise ValueError('Every scenario split must be dev or frozen')
    overlay = json.loads(Path(args.oracle_overlay).read_text())
    projected = project_oracles(original, overlay)
    cases = [c for c in projected if args.suite == 'all' or c['split'] == args.suite]
    if not cases:
        raise ValueError('No selected cases')
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    budget = Budget(args.max_cost_usd, args.ledger)
    planned = len(cases) * args.repeats
    initial = budget.spent
    if initial >= budget.limit:
        raise ValueError('Shared experiment budget is already exhausted; no API calls made')
    fixed = {'config': config, 'config_sha256': hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),
        'prompt_sha256': hashlib.sha256((EXTRACT+'\n'+PLAN).encode()).hexdigest(),
        'cases_file_sha256': sha256(Path(args.cases)), 'oracle_overlay_sha256': sha256(Path(args.oracle_overlay)),
        'source_suite': freeze_manifest(original), 'selected_projected_suite': freeze_manifest(cases),
        'repeats':args.repeats, 'jobs':args.jobs, 'planned_pairs':planned,
        'order':'Per-pair AB/BA alternation by scenario index plus repetition; two independent full workflows.',
        'seed':'Provider adapter does not expose a seed; matched repetition is not identical randomness.',
        'retrieval_note':'Same algorithm, different text may change ranked retrieved clauses; full excerpts retained.',
        'gate_note':'Fixed reviewed Python gate, not compiled from revised policy.',
        'boundary_note':'Excluded fields have no unique business gold; evidence-boundary checks assess unqualified structured certainty, not an approved routing rule.',
        'ledger_start_usd':initial, 'budget_limit_usd':budget.limit,
        'snapshots':{side:start_snapshot(corpus,args.matrix) for side,corpus in corpora.items()}}
    dump(out/'manifest.json',fixed)
    dump(out/'oracle.json',{'overlay':overlay,'projected_cases':cases})
    records={'baseline':[],'candidate':[]}
    calls={'baseline':[],'candidate':[]}

    def run_pair(case, repeat, position):
        rows={}
        order=('baseline','candidate') if (position+repeat)%2 == 0 else ('candidate','baseline')
        for side in order:
            provider=Provider(config,budget)
            try:
                turns=run_scenario(model_input(case),provider,corpora[side])
            except Exception as exc:
                turns=[{'error':type(exc).__name__,'decisions':[],'reply':''}]
            row=score_projected(case,turns)
            row.update(repeat=repeat+1,turns=turns,calls=provider.calls,policy_version=fixed['snapshots'][side]['policy_snapshot']['version_id'])
            rows[side]=row
        return rows

    # Limit outstanding work to jobs: budget stop cannot enqueue the entire experiment.
    tasks=[(case,repeat,position) for repeat in range(args.repeats) for position,case in enumerate(cases)]
    completed=0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for offset in range(0,len(tasks),args.jobs):
            if budget.spent >= budget.limit:
                break
            futures=[pool.submit(run_pair,*task) for task in tasks[offset:offset+args.jobs]]
            for future in as_completed(futures):
                rows=future.result()
                with (out/'turns.jsonl').open('a') as stream:
                    for side,row in rows.items():
                        records[side].append(row)
                        calls[side].extend(row['calls'])
                        stream.write(json.dumps({'side':side,**row},ensure_ascii=False)+'\n')
                completed+=1
                print(f'Paired {completed}/{planned}',flush=True)
            reports={}
            for side in records:
                regular=[r for r in records[side] if not any(e in ('BudgetExceeded','BudgetExhausted') for e in r['technical_errors'])]
                reports[side]={'records':regular,'summary':summarize(regular,planned,len(cases))}
                resolved=[r for r in regular if r['fully_resolved']]
                reports[side]['summary']['fully_resolved_runs']=len(resolved)
                reports[side]['summary']['resolved_business_success']={stage:{
                    'numerator':sum(r[f'{stage}_supported_passed'] for r in resolved),
                    'denominator':len(resolved)} for stage in ('raw','final')}
                reports[side]['summary']['unresolved_policy_runs']=sum(not r['fully_resolved'] for r in regular)
                reports[side]['summary']['boundary_failures']={stage:sum(bool(r['boundary_errors'][stage]) for r in regular) for stage in ('raw','final')}
                attach_usage(reports[side],calls[side])
            matched=compare_records(records,planned)
            dump(out/'summary.json',{'reports':reports,'matched':matched})
            write_comparison(out,reports,matched)
            fixed.update(ledger_end_usd=budget.spent,experiment_reported_cost_usd=sum(c.get('cost_usd',0) for rows in calls.values() for c in rows if c.get('cost_status')=='usage_reported'))
            dump(out/'manifest.json',fixed)
    print('Saved:',out)
    return 0 if completed==planned and matched['matched_completed_pairs']==planned else 2
