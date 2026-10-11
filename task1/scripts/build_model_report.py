"""Build reviewed report data from explicit benchmark directories; never run APIs."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads(path.read_text())

def extract(directory, stage):
    path = Path(directory)
    summary = path if path.is_file() else path / 'summary.json'
    if not summary.exists():
        index = path / 'index.json'
        if not index.exists():
            return [], []
        rows, files = [], []
        for model in read(index).get('models', []):
            child_rows, child_files = extract(path / model['directory'], stage)
            rows.extend(child_rows or [{'stage':stage, 'config_id':model['config_id'], 'model':model['config_id'].split('/')[1], 'thinking':model['config_id'].split('/')[-1], 'thinking_mode':model['config_id'].split('/')[-2], 'status':model.get('status', 'pending')}])
            files.extend(child_files)
        return rows, files
    data = read(summary)
    if path.is_file():
        path = path.parent
    manifest = read(path / 'manifest.json') if (path / 'manifest.json').exists() else {}
    models = data.get('models', [data])
    rows = []
    for model in models:
        if 'summary' not in model:
            child = path / model.get('directory', '')
            child_rows, _ = extract(child, stage)
            rows.extend(child_rows)
            continue
        s, u = model['summary'], model.get('usage', {})
        model_manifest = model.get('source_run_manifest', manifest)
        configs = manifest.get('models') or manifest.get('planned_models', [])
        config = next((c for c in configs if c.get('config_id') == model.get('config_id')), {}) if model.get('config_id') else next((c for c in configs if c.get('model') == model.get('model_id')), {})
        config = model.get('configuration') or config
        parts = model.get('config_id', '').split('/')
        if not config and len(parts) == 4:
            config = {'model':parts[1], 'thinking_mode':parts[2], 'effort':parts[3]}
        row = {'stage': stage, 'config_id': model.get('config_id', config.get('config_id', model.get('model_id'))), 'model': model.get('model_id', config.get('model')),
               'thinking': config.get('reasoning_effort', config.get('effort', 'not recorded')), 'thinking_mode': config.get('thinking_mode', config.get('thinking', {}).get('type', 'reasoning' if 'reasoning_effort' in config else 'not recorded')),
               'planned': s.get('planned_runs'), 'completed': s.get('completed_runs'), 'unique': s.get('unique_scenarios'), 'repeats': model.get('repeats', data.get('repeats')), 'status': s.get('completion_status'),
               'critical': s.get('critical_final_failures'), 'api_failures': s.get('technical_failure_runs', s.get('api_error_runs')),
               'p50': u.get('turn_latency_p50_seconds'), 'p95': u.get('turn_latency_p95_seconds'),
               'cost': u.get('reported_cost_usd'), 'cost_per_success':u.get('cost_per_successful_conversation_usd'),
               'input_tokens':u.get('input_tokens'), 'output_tokens':u.get('output_tokens'), 'cached_tokens':u.get('cached_input_tokens'), 'cache_write_tokens':u.get('cache_write_tokens'),
               'call_count':u.get('call_count'), 'api_error_calls':u.get('api_error_calls'),
               'reserved_cost':u.get('reserved_or_unknown_cost_usd'), 'cost_status':u.get('cost_status'),
               'metric_version':s.get('metric_version'), 'observed_at':data.get('observed_at', data.get('generated_at_utc')), 'revision':data.get('revision'),
               'source': str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name,
               'code':model_manifest.get('code_sha256'), 'prompt':model_manifest.get('prompt_version'), 'corpus':model_manifest.get('corpus_version')}
        for key in ['candidate_conversation_success','fix_contract_success','success_against_planned','conversation_success','pre_gate_assertion_success','post_gate_assertion_success','amount_accuracy','policy_accuracy','answerable_completion','over_refusal_rate','mandatory_escalation_recall']:
            rate = s.get(key, {})
            row[key] = rate.get('rate')
            row[key + '_counts'] = f"{rate.get('numerator', '—')}/{rate.get('denominator', '—')}"
        rows.append(row)
    return rows, [{'file':str(summary.relative_to(ROOT)) if summary.is_relative_to(ROOT) else summary.name, 'sha256':hashlib.sha256(summary.read_bytes()).hexdigest()}]

def snapshot(inputs, selection=None, existing=None, complete=False):
    rows, files = [], []
    for stage, directory in inputs:
        r, f = extract(Path(directory).resolve(), stage)
        rows.extend(r); files.extend(f)
    selected = read(Path(selection)) if selection else {'status':'pending','winner':None,'reasons':['Final frontier cohort and selection are pending.']}
    if selected.get('winner') and (selected.get('status') not in ('selected', 'tentative') or not any(r['config_id'] == selected['winner'] and not r['stage'].startswith('historical') for r in rows)):
        raise ValueError('Selection must have selected/tentative status and a matching nonhistorical result.')
    old = existing or {}
    return {**old, 'surface':'report','title':'准确率优先，速度决定模型选择','generatedAt':datetime.now(timezone.utc).isoformat(),
            'buildStatus':'complete' if complete else 'updating', 'status':'reviewed' if selected.get('winner') else 'partial',
            'selection':selected, 'filters':[], 'queries':{'models':{'rows':rows,'source':{'label':'Explicit local benchmark artifacts', 'files':[f['file'] for f in files],
                'evidenceFlow':[{'title':f['file'],'detail':'SHA-256 '+f['sha256']} for f in files],
                'metricDefinitions':[{'label':'Conversation success','definition':'All tested requirements pass for a completed conversation; numerator and denominator displayed. Repeats are not independent scenarios.','componentIds':['model-table','report-summary']},
                    {'label':'Whole-turn latency','definition':'Workflow turn including model requests, retrieval, policy checks, retries and repair. Missing historical instrumentation stays null.','componentIds':['model-table']},
                    {'label':'Critical failures','definition':'Closed-template audit of required final decisions; not an unrestricted hallucination audit. Missing is not zero.','componentIds':['model-table']}],
                'caveats':['Historical development and interrupted runs are excluded from final model selection.','API cost is an estimate from recorded token usage, not the supplier invoice.','Only supplied selection JSON can establish a recommendation.']},
                'methods':[{'language':'text','code':'Read explicitly supplied summary.json and manifest.json; retain stage and missing measurements; no pooling across cohorts; no model API requests.'}]}}}

def policy_snapshot(path):
    """Import audited aggregate pairs only; never load source oracle/case records."""
    path = Path(path).resolve()
    data = read(path)
    rows = []
    if data.get('artifact_type') == 'policy_pair_comparison':
        cohort = data['cohort']
        data = {**data, 'code_sha256':cohort['code_sha256'], 'controls':{'selected_projected_suite':{'scenario_count':cohort['scenario_count']}, 'repeats':cohort['repeats']}, 'scoring_audit':data['oracle']['audit_v2'], 'claim_scope':data['promotion']['scope'], 'experiments':[{'config':m['config'], 'manifest':{'snapshots':{'baseline':{'prompt_version':cohort['workflow_version']}}}, 'matched':{'planned_pairs':m['planned_pairs'], 'matched_completed_pairs':m['completed_pairs'], 'missing_or_technical_pairs':m['planned_pairs']-m['completed_pairs'], 'counts':{'raw':m['raw_transitions'],'final':m['final_transitions']}}, 'usage':{side:m[side]['usage'] for side in ('baseline','candidate')}, 'summaries':{side:m[side]['summary'] for side in ('baseline','candidate')}} for m in data['models']]}
    for experiment in data['experiments']:
        matched = experiment['matched']
        manifest = experiment['manifest']
        row = {'config_id': experiment['config']['config_id'],
               'workflow': manifest['snapshots']['baseline']['prompt_version'],
               'code': data['code_sha256'], 'completed': matched['matched_completed_pairs'],
               'planned': matched['planned_pairs'], 'missing_or_technical': matched['missing_or_technical_pairs'],
               'unique': data['controls']['selected_projected_suite']['scenario_count'],
               'repeats': data['controls']['repeats'], 'metric': 'common offline v2 overlay',
               'oracle_hash': data['scoring_audit']['overlay_sha256']}
        for stage in ('raw', 'final'):
            counts = matched['counts'][stage]
            if sum(counts.values()) != row['completed']:
                raise ValueError('Policy transition counts do not match completed pair denominator')
            row[stage+'_baseline_pass'] = counts['unchanged_pass'] + counts['regressed']
            row[stage+'_candidate_pass'] = counts['unchanged_pass'] + counts['improved']
            row[stage+'_improved'] = counts['improved']
            row[stage+'_regressed'] = counts['regressed']
        for side in ('baseline', 'candidate'):
            usage = experiment['usage'][side]
            summary = experiment['summaries'][side]
            for field in ('reported_cost_usd', 'reserved_or_unknown_cost_usd', 'turn_latency_p50_seconds', 'turn_latency_p95_seconds', 'input_tokens', 'output_tokens', 'cached_input_tokens', 'cache_write_tokens', 'call_count', 'api_error_calls'):
                row[side+'_'+field] = usage.get(field)
            row[side+'_completed_runs'] = summary['completed_runs']
            row[side+'_planned_runs'] = summary['planned_runs']
        rows.append(row)
    source_path = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name
    return {'rows': rows, 'source': {'label':'Audited paired policy comparison', 'files':[source_path],
            'evidenceFlow':[{'title':source_path, 'detail':'SHA-256 '+hashlib.sha256(path.read_bytes()).hexdigest()}],
            'caveats':[data['claim_scope'], data['scoring_audit']['scope']],
            'metricDefinitions':[{'label':'Paired pass count', 'definition':'Baseline = unchanged_pass + regressed; candidate = unchanged_pass + improved. Denominator is matched completed pairs, preserving planned pairs separately.', 'componentIds':['policy-comparison']} ]}}

def repair_snapshot(path):
    """Validate bounded reviewed aggregate measurements; missing stays missing."""
    data = read(Path(path))
    if not isinstance(data.get('rows'), list) or not isinstance(data.get('source'), dict):
        raise ValueError('Repair metrics require rows and provenance source')
    for row in data['rows']:
        if not row.get('label') or not row.get('workflow') or not row.get('config_id'):
            raise ValueError('Repair row requires label, workflow and exact configuration')
        for key in ('completed', 'planned', 'technical_failures', 'scope_failures', 'scope_assessed',
                    'citation_conflict_failures', 'citation_conflict_assessed', 'scope_calls',
                    'scope_latency_seconds', 'scope_cost_usd', 'total_calls', 'turn_p50_seconds',
                    'turn_p95_seconds', 'reported_cost_usd'):
            value = row.get(key)
            if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0):
                raise ValueError('Repair measurements must be nonnegative numbers or null')
        for count, denominator in (('completed','planned'), ('scope_failures','scope_assessed'), ('citation_conflict_failures','citation_conflict_assessed')):
            if row.get(count) is not None and row.get(denominator) is not None and row[count] > row[denominator]:
                raise ValueError('Repair measurement exceeds its denominator')
    return data

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',action='append',default=[],metavar='STAGE=DIR')
    p.add_argument('--development-default', help='Explicit user-selected baseline configuration, not a winner')
    p.add_argument('--repair-metrics', help='Owner-reviewed repair aggregates with provenance')
    p.add_argument('--policy-results', help='Audited aggregate Policy A/B results JSON')
    p.add_argument('--coordination', help='Reviewed coordination snapshot JSON; never reads acceptance cases')
    p.add_argument('--run-manifest', action='append', default=[], metavar='STAGE=PATH', help='Frozen metadata for a compact checkpoint without its own manifest')
    p.add_argument('--selection');p.add_argument('--complete',action='store_true');p.add_argument('--build',action='store_true')
    p.add_argument('--project',default=str(ROOT/'report'));p.add_argument('--plugin',default='/Users/yuanlu/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.11')
    p.add_argument('--node',default='node')
    a=p.parse_args(); project=Path(a.project); data=project/'src/data.json'
    result=snapshot([v.split('=',1) for v in a.run],a.selection,read(data) if data.exists() else None,a.complete)
    for item in a.run_manifest:
        stage, manifest_path = item.split('=', 1)
        manifest = read(Path(manifest_path))
        for row in result['queries']['models']['rows']:
            if row['stage'] == stage:
                row.update(prompt=manifest.get('prompt_version'), code=manifest.get('code_sha256'), corpus=manifest.get('corpus_version'))
        result['queries']['models']['source']['evidenceFlow'].append({'title':manifest_path, 'detail':'Frozen source metadata SHA-256 '+hashlib.sha256(Path(manifest_path).read_bytes()).hexdigest()})
    if a.development_default:
        baseline = read(Path(a.development_default))
        if baseline.get('selection_status') != 'development_default_only':
            raise ValueError('Development default must be explicitly marked development_default_only')
        result['development_default'] = {'status': baseline['selection_status'], 'config_ids':[c['config_id'] for c in baseline['models']]}
    if a.repair_metrics:
        result['queries']['repair_metrics'] = repair_snapshot(a.repair_metrics)
    if a.policy_results:
        result['queries']['policy_comparison'] = policy_snapshot(a.policy_results)
    if a.coordination:
        coordination = read(Path(a.coordination))
        result['coordination'] = coordination
        result['queries']['coordination'] = {'rows': coordination['rows'], 'source': {'label': 'Coordinator and owner handoff snapshots', 'files': [f['file'] for f in coordination['sources']], 'evidenceFlow': [{'title': f['file'], 'detail': 'SHA-256 ' + f['sha256']} for f in coordination['sources']], 'caveats': ['Owner progress snapshots are not new live checks; each source retains its own observation time.']}}
    data.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if a.build:
        subprocess.run([a.node,str(Path(a.plugin)/'scripts/data-app.mjs'),'build','--project-dir',str(project)],check=True)
    print(json.dumps({'rows':len(result['queries']['models']['rows']),'selection_status':result['selection']['status'],'output':str(project/'dist/index.html')}))
if __name__=='__main__':main()
