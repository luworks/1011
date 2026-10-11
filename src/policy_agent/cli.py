"""CLI entry points. All persisted output is redacted structured data."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from pydantic import BaseModel

from .corpus import Corpus
from .providers import Budget, Provider
from .workflow import PROMPT_VERSION, replay, Workflow, run_scenario
from .service import charter_metadata
from .versions import version_directory


def dump(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str)+'\n')


def configurations(path):
    return json.loads(Path(path).read_text())['models']


def enforce_evaluation_effort(configs):
    if any(c.get('reasoning_effort', c.get('effort')) in {'xhigh', 'max', 'ultra'} for c in configs):
        raise ValueError('Evaluation effort ceiling is high; explicitly select allowed configurations')


def choose(args):
    matrix = args.matrix or ('config/models.json' if args.provider or args.model or args.config_id else 'config/development-default.json')
    configs = configurations(matrix)
    if getattr(args,'config_id',None):
        choices = [c for c in configs if c.get('config_id')==args.config_id]
    else:
        choices = [c for c in configs if (not args.provider or c['provider'] == args.provider) and (not args.model or c['model']==args.model)]
    if not choices: raise ValueError('Requested model is not in the priced model matrix')
    if not args.model:
        choices.sort(key=lambda c: c['input_per_million']+c['output_per_million'])
    return choices[0]


def output_turn(result):
    print(f"\nTurn {result['turn']} [{result['mode']}] {result['customer_input']}")
    for d in result['decisions']:
        print(f"  {d['question']}: {d['answer_status']} / {d['action_status']}")
        print('  Policy: '+(', '.join(d['policy_ids']) or 'KB / workflow evidence boundary'))
        for e in d['evidence']:
            print(f"  Evidence: {e['source_id']} {e['path']}:{e['start_line']}")
        if d['missing']: print('  Missing: '+', '.join(d['missing']))
        for reason in d['reasons']: print('  Reason: '+reason)
    if result['error']: print('  Technical error: '+result['error'])
    if result['gate_errors']: print('  Gate corrections: '+', '.join(result['gate_errors']))
    print('  Reply: '+result['reply'])


def start_snapshot(corpus, matrix_path):
    code = hashlib.sha256()
    for p in sorted(Path(__file__).parent.glob('*.py')): code.update(p.name.encode()+p.read_bytes())
    return {'schema_version': 2, 'started_at': datetime.now(timezone.utc).isoformat(),
            'code_sha256': code.hexdigest(), 'corpus_version': corpus.version,
            'prompt_version': PROMPT_VERSION, 'policy_snapshot': corpus.policy_snapshot,
            'service_charter': charter_metadata(),
            'model_matrix_sha256': hashlib.sha256(Path(matrix_path).read_bytes()).hexdigest()}


def manifest(snapshot, providers, budget, mode):
    return {**snapshot, 'created_at': datetime.now(timezone.utc).isoformat(),
            'mode': mode, 'models': [p.config for p in providers],
            'calls':[c for p in providers for c in p.calls], 'budget_limit_usd':budget.limit,
            'ledger_total_usd':budget.spent,'cost_note':'Client estimates; unknown failed attempts retain reservations, not a provider invoice.'}


def parser():
    p = argparse.ArgumentParser(description='Evidence-bounded billing agent (no real account actions)')
    sub = p.add_subparsers(dest='command',required=True)
    for name in ('doctor','replay','chat','evaluate'):
        s=sub.add_parser(name)
        s.add_argument('--matrix',default='config/eval-models-high.json' if name=='evaluate' else None)
        s.add_argument('--provider',choices=['openai','anthropic'])
        s.add_argument('--model')
        s.add_argument('--config-id', help='Exact provider/model/thinking/effort configuration')
        s.add_argument('--max-cost-usd',type=float,default=5)
        s.add_argument('--ledger',default='runs/budget.json')
        s.add_argument('--output')
        s.add_argument('--policy-version', help='Exact paired snapshot ID under docs/policy_versions')
        if name=='doctor': s.add_argument('--check-api',action='store_true')
        if name=='replay':
            s.add_argument('--offline',action='store_true')
            s.add_argument('--conversation')
        if name=='chat':
            s.add_argument('--context',help='Explicit local simulated account JSON')
            s.add_argument('--date',default=datetime.now().date().isoformat())
        if name=='evaluate':
            s.add_argument('--suite',choices=['dev','frozen','all'],default='dev')
            s.add_argument('--cases', default='fixtures/scenarios.json')
            s.add_argument('--repeats',type=int)
            s.add_argument('--limit',type=int)
            s.add_argument('--only-model',action='append')
            s.add_argument('--only-config',action='append')
            s.add_argument('--oracle-overlay', help='Reviewed unresolved-policy exclusions (never model input)')
    s=sub.add_parser('compare-policies')
    s.add_argument('--baseline', required=True)
    s.add_argument('--candidate', required=True)
    s.add_argument('--config-id', required=True)
    s.add_argument('--matrix', default='config/eval-models-high.json')
    s.add_argument('--cases', default='fixtures/scenarios.json')
    s.add_argument('--oracle-overlay', default='fixtures/policy-comparison-oracle.json')
    s.add_argument('--suite', choices=['dev','frozen','all'], default='all')
    s.add_argument('--repeats', type=int, default=3)
    s.add_argument('--jobs', type=int, default=4)
    s.add_argument('--max-cost-usd', type=float, default=5)
    s.add_argument('--ledger', default='runs/budget.json')
    s.add_argument('--output', required=True)
    s=sub.add_parser('report');s.add_argument('--run-dir',required=True)
    return p


def main():
    args=parser().parse_args()
    if args.command in ('doctor', 'replay', 'chat') and args.matrix is None:
        args.matrix = ('config/models.json' if args.provider or args.model or args.config_id
                       else 'config/development-default.json')
    load_dotenv(Path('.env'), override=False)
    try:
        if args.command=='report':
            path=Path(args.run_dir)/'summary.json'
            print(path.read_text());return 0
        if args.command=='compare-policies':
            selected = [c for c in configurations(args.matrix) if c.get('config_id') == args.config_id]
            enforce_evaluation_effort(selected)
            from .comparison import run_comparison
            return run_comparison(args)
        corpus=Corpus(version_directory(args.policy_version)) if args.policy_version else Corpus()
        if args.command=='doctor' and not args.check_api:
            print(json.dumps({'corpus_entries':len(corpus.entries),'corpus_version':corpus.version,'policy_snapshot':corpus.policy_snapshot,
                'keys':{k:bool(os.environ.get(k)) for k in ['OPENAI_API_KEY','ANTHROPIC_API_KEY']},
                'api_access':'not checked','model_configs':len(configurations(args.matrix))},indent=2));return 0
        snapshot=start_snapshot(corpus,args.matrix)
        out=Path(args.output or ('runs/'+args.command+'-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]))
        out.mkdir(parents=True,exist_ok=False)
        budget=Budget(args.max_cost_usd,args.ledger)
        providers=[]
        if args.command=='doctor':
            class Probe(BaseModel):
                ok: bool
            provider=Provider(choose(args),budget);providers=[provider]
            try:
                response=provider.generate(Probe,'Return ok=true.',{})
                summary={'api_access':'confirmed','response':response.model_dump()}
            except Exception as exc:
                summary={'api_access':'failed','error':str(exc)}
            dump(out/'summary.json',summary)
            dump(out/'manifest.json',manifest(snapshot,providers,budget,'api_probe'))
            print(json.dumps(summary));print('Saved:',out)
            return 0 if summary['api_access']=='confirmed' else 2
        if args.command in ('replay','chat'):
            offline=getattr(args,'offline',False)
            provider=None if offline else Provider(choose(args),budget)
            if provider: providers=[provider]
            if args.command=='replay':
                path=Path(args.conversation) if args.conversation else next(Path('exam').glob('*.txt'))
                results=replay(path,provider,corpus)
                for result in results:output_turn(result)
            else:
                context=json.loads(Path(args.context).read_text()) if args.context else {}
                context.setdefault('request_date',args.date)
                flow=Workflow(corpus,provider,context)
                print('Local simulation. Enter /quit to exit; no real credits or handoffs.')
                while True:
                    try: text=input('Customer> ')
                    except EOFError: break
                    if text.strip()=='/quit':break
                    output_turn(flow.turn(text))
                results=flow.results
            (out/'turns.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in results))
            summary={'turns':len(results),'technical_failures':sum(bool(r['error']) for r in results),'mode':'offline_fixture' if offline else 'live'}
        else:
            from .evaluation import evaluate_cases, freeze_manifest, attach_usage, load_cases
            all_cases=load_cases(args.cases)
            if args.policy_version and not args.oracle_overlay:
                args.oracle_overlay='fixtures/policy-comparison-oracle.json'
            if args.oracle_overlay:
                from .comparison import project_oracles
                all_cases=project_oracles(all_cases, json.loads(Path(args.oracle_overlay).read_text()))
                snapshot['oracle_overlay_sha256']=hashlib.sha256(Path(args.oracle_overlay).read_bytes()).hexdigest()
            if any(c.get('split') not in ('dev','frozen') for c in all_cases):
                raise ValueError('Every scenario split must be dev or frozen')
            cases=[c for c in all_cases if args.suite=='all' or c['split']==args.suite]
            if not cases: raise ValueError('Selected suite contains no scenarios')
            parent_suite=freeze_manifest(cases)
            if args.limit is not None:
                if args.limit<1: raise ValueError('Limit must be positive')
                cases=cases[:args.limit]
            if args.repeats is None: args.repeats=3 if args.suite in ('frozen','all') else 1
            if args.repeats<1:raise ValueError('Repeats must be positive')
            configs=configurations(args.matrix)
            if args.only_model: configs=[c for c in configs if c['model'] in args.only_model]
            if args.only_config: configs=[c for c in configs if c.get('config_id') in args.only_config]
            if not configs:raise ValueError('No selected model configurations')
            enforce_evaluation_effort(configs)
            frozen=freeze_manifest(cases)
            selection={'parent_suite':parent_suite, 'selected_suite':frozen,
                       'scope':'subset' if len(cases)<parent_suite['scenario_count'] else 'full_suite',
                       'requested_limit':args.limit, 'cases_path':str(args.cases),
                       'cases_file_sha256':hashlib.sha256(Path(args.cases).read_bytes()).hexdigest()}
            snapshot['evaluation_selection']=selection
            snapshot['planned_models']=configs
            dump(out/'suite_manifest.json',selection)
            dump(out/'manifest.json',manifest(snapshot,providers,budget,'evaluation'))
            summary={'suite':args.suite,'repeats':args.repeats,'selection':selection,'models':[]}
            for config in configs:
                config_id=config.get('config_id',config['model'])
                print('Evaluating:',config_id,flush=True)
                provider=Provider(config,budget);providers.append(provider)
                def run_case(case):
                    turns=run_scenario(case,provider,corpus)
                    with (out/'turns.jsonl').open('a') as stream:
                        stream.write(json.dumps({'model':config['model'],'config_id':config_id,'case_id':case['id'],'turns':turns})+'\n')
                    return turns
                report=evaluate_cases(cases,run_case,model_id=config['model'],repeats=args.repeats,
                    can_continue=lambda:budget.spent<budget.limit)
                attach_usage(report,provider.calls)
                report['config_id']=config_id
                report['selection']=selection
                report['parent_suite_planned_runs']=parent_suite['scenario_count']*args.repeats
                report['calls']=provider.calls
                report['estimated_cost_usd']=sum(c['cost_usd'] for c in provider.calls)
                summary['models'].append(report)
                dump(out/'summary.json',summary)
        dump(out/'summary.json',summary)
        dump(out/'manifest.json',manifest(snapshot,providers,budget,'evaluation' if args.command=='evaluate' else summary.get('mode','live')))
        print('Saved:',out)
        if args.command=='evaluate':
            return 2 if any(m['summary']['completion_status']!='complete' or m['summary']['technical_failure_runs'] for m in summary['models']) else 0
        return 2 if summary.get('technical_failures') else 0
    except (ValueError, OSError) as exc:
        print(f'Error: {type(exc).__name__}: {exc}',file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
