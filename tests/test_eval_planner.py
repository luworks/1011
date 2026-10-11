"""Offline planner tests: effort coverage, safe exclusions and unique cost totals."""
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('eval_planner', Path(__file__).resolve().parents[1] / 'scripts/plan_eval_stage.py')
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


def screen(tmp_path, configs, *, critical=(), latency=None, pending=()):
    def write(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
    selection = {'selected_suite': {'sha256': 'oracle', 'scenario_count': 3}, 'cases_file_sha256': 'cases'}
    manifest = {k: 'fixed' for k in ('code_sha256', 'corpus_version', 'prompt_version', 'model_matrix_sha256')}
    manifest.update(evaluation_selection=selection, planned_models=configs)
    write(tmp_path / 'manifest.json', manifest)
    write(tmp_path / 'index.json', {'suite': 'dev', 'repeats': 1, 'selection': selection,
        'models': [{'config_id': c['config_id'], 'directory': c['config_id'],
                    'status': 'pending' if c['config_id'] in pending else 'complete'} for c in configs]})
    for i, config in enumerate(configs):
        cid = config['config_id']
        write(tmp_path / cid / 'manifest.json', {**manifest, 'planned_models': [config]})
        if cid in pending:
            continue
        summary = {'planned_runs': 3, 'unique_scenarios': 3, 'completion_status': 'complete', 'completed_runs': 3,
            'critical_final_failures': int(cid in critical), 'mandatory_escalation_recall': {'numerator': 1, 'denominator': 1},
            'success_against_planned': {'numerator': 3, 'denominator': 3}}
        seconds = (latency or {}).get(cid, i + 1)
        usage = {'turn_latency_complete': True, 'turn_latency_p95_seconds': seconds, 'turn_latency_p50_seconds': seconds,
            'cost_status': 'complete', 'reported_cost_usd': .03, 'reserved_or_unknown_cost_usd': 0}
        write(tmp_path / cid / 'summary.json', {'repeats': 1, 'models': [{'config_id': cid,
            'manifest': {'sha256': 'oracle'}, 'summary': summary, 'usage': usage}]})
    return tmp_path


def openai(efforts):
    return [{'config_id': e, 'provider': 'openai', 'model': 'test', 'reasoning_effort': e} for e in efforts]


def test_promotes_fastest_and_highest_without_double_budget(tmp_path):
    root = screen(tmp_path, openai(['none', 'medium', 'high']))
    result = planner.build(root, include_high=True)
    assert result['families'][0]['shortlisted_config_ids'] == ['none', 'high']
    assert result['projected_shortlist_24_dev_plus_48_frozen_usd'] == pytest.approx(1.44)
    assert len(result['shortlist_matrix']['models']) == 2


def test_highest_is_deduplicated_when_also_fastest(tmp_path):
    root = screen(tmp_path, openai(['none', 'high']), latency={'none': 10, 'high': 1})
    result = planner.build(root, include_high=True)
    assert result['families'][0]['shortlisted_config_ids'] == ['high']
    assert result['projected_shortlist_24_dev_plus_48_frozen_usd'] == pytest.approx(.72)
    assert len(result['families'][0]['promotion_reasons']['high']) == 2


def test_unsafe_high_is_excluded_without_quality_probe(tmp_path):
    root = screen(tmp_path, openai(['none', 'medium', 'high']), critical=['high'])
    result = planner.build(root, include_high=True)
    assert result['families'][0]['shortlisted_config_ids'] == ['none']
    assert result['families'][0]['eligible_high_effort_config_id'] is None
    unsafe = result['families'][0]['configurations'][-1]
    assert 'observed_critical_final_failure' in unsafe['exclusions']


def test_claude_disabled_can_win_speed_but_adaptive_high_is_quality_probe(tmp_path):
    configs = [{'config_id': name, 'provider': 'anthropic', 'model': 'test',
                'thinking': {'type': mode}, 'effort': effort}
               for name, mode, effort in [('disabled', 'disabled', 'low'), ('medium', 'adaptive', 'medium'), ('high', 'adaptive', 'high')]]
    result = planner.build(screen(tmp_path, configs), include_high=True)
    assert result['families'][0]['shortlisted_config_ids'] == ['disabled', 'high']


def test_pending_family_not_promoted_even_with_complete_high_effort(tmp_path):
    result = planner.build(screen(tmp_path, openai(['none', 'high']), pending=['none']), include_high=True)
    assert result['shortlisted_count'] == 0
    assert result['projected_shortlist_24_dev_plus_48_frozen_usd'] == 0


def test_option_off_retains_one_rank_winner(tmp_path):
    result = planner.build(screen(tmp_path, openai(['none', 'high'])))
    assert result['families'][0]['shortlisted_config_ids'] == ['none']


@pytest.mark.parametrize('effort', ['xhigh', 'max', 'ultra'])
def test_user_ceiling_rejects_above_high_even_historical_completed_config(tmp_path, effort):
    root = screen(tmp_path, openai(['none', effort]))
    with pytest.raises(ValueError, match='ceiling is high'):
        planner.build(root, include_high=True)
