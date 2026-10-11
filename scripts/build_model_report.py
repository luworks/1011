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
    summary = path / 'summary.json'
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
        configs = manifest.get('models') or manifest.get('planned_models', [])
        config = next((c for c in configs if c.get('config_id') == model.get('config_id')), {}) if model.get('config_id') else next((c for c in configs if c.get('model') == model.get('model_id')), {})
        row = {'stage': stage, 'config_id': model.get('config_id', config.get('config_id', model.get('model_id'))), 'model': model.get('model_id'),
               'thinking': config.get('reasoning_effort', config.get('effort', 'not recorded')), 'thinking_mode': config.get('thinking_mode', config.get('thinking', {}).get('type', 'reasoning' if 'reasoning_effort' in config else 'not recorded')),
               'planned': s.get('planned_runs'), 'completed': s.get('completed_runs'), 'unique': s.get('unique_scenarios'), 'status': s.get('completion_status'),
               'critical': s.get('critical_final_failures'), 'api_failures': s.get('technical_failure_runs', s.get('api_error_runs')),
               'p50': u.get('turn_latency_p50_seconds'), 'p95': u.get('turn_latency_p95_seconds'),
               'cost': model.get('estimated_cost_usd', u.get('reported_cost_usd')), 'cost_per_success':u.get('cost_per_successful_conversation_usd'),
               'input_tokens':u.get('input_tokens'), 'output_tokens':u.get('output_tokens'), 'cached_tokens':u.get('cached_input_tokens'),
               'source': str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else path.name,
               'code':manifest.get('code_sha256'), 'prompt':manifest.get('prompt_version'), 'corpus':manifest.get('corpus_version')}
        for key in ['conversation_success','pre_gate_assertion_success','post_gate_assertion_success','amount_accuracy','policy_accuracy','answerable_completion','over_refusal_rate','mandatory_escalation_recall']:
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

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',action='append',default=[],metavar='STAGE=DIR')
    p.add_argument('--coordination', help='Reviewed coordination snapshot JSON; never reads acceptance cases')
    p.add_argument('--selection');p.add_argument('--complete',action='store_true');p.add_argument('--build',action='store_true')
    p.add_argument('--project',default=str(ROOT/'report'));p.add_argument('--plugin',default='/Users/yuanlu/.codex/plugins/cache/openai-curated-remote/data-analytics/1.0.11')
    p.add_argument('--node',default='node')
    a=p.parse_args(); project=Path(a.project); data=project/'src/data.json'
    result=snapshot([v.split('=',1) for v in a.run],a.selection,read(data) if data.exists() else None,a.complete)
    if a.coordination:
        coordination = read(Path(a.coordination))
        result['coordination'] = coordination
        result['queries']['coordination'] = {'rows': coordination['rows'], 'source': {'label': 'Coordinator and owner handoff snapshots', 'files': [f['file'] for f in coordination['sources']], 'evidenceFlow': [{'title': f['file'], 'detail': 'SHA-256 ' + f['sha256']} for f in coordination['sources']], 'caveats': ['Owner progress snapshots are not new live checks; each source retains its own observation time.']}}
    data.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if a.build:
        subprocess.run([a.node,str(Path(a.plugin)/'scripts/data-app.mjs'),'build','--project-dir',str(project)],check=True)
    print(json.dumps({'rows':len(result['queries']['models']['rows']),'selection_status':result['selection']['status'],'output':str(project/'dist/index.html')}))
if __name__=='__main__':main()
