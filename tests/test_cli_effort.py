import json
import pytest
from policy_agent import cli


def test_evaluation_commands_default_to_authorized_matrix():
    assert cli.parser().parse_args(['evaluate']).matrix == 'config/eval-models-high.json'
    args=cli.parser().parse_args(['compare-policies','--baseline','a','--candidate','b','--config-id','id','--output','out'])
    assert args.matrix == 'config/eval-models-high.json'


@pytest.mark.parametrize('effort',['xhigh','max','ultra'])
@pytest.mark.parametrize('field',['effort','reasoning_effort'])
def test_evaluation_ceiling_rejects_both_provider_parameters(effort,field):
    with pytest.raises(ValueError,match='ceiling'):
        cli.enforce_evaluation_effort([{field:effort}])


def test_policy_compare_rejects_before_executing_comparison(tmp_path,monkeypatch):
    import sys
    from policy_agent import comparison
    matrix=tmp_path/'matrix.json'
    matrix.write_text(json.dumps({'models':[{'config_id':'bad','effort':'max'}]}))
    monkeypatch.setattr(comparison,'run_comparison',lambda _:pytest.fail('comparison should not start'))
    monkeypatch.setattr(sys,'argv',['prototype','compare-policies','--matrix',str(matrix),
        '--baseline','a','--candidate','b','--config-id','bad','--output',str(tmp_path/'out')])
    assert cli.main()==2
    assert not (tmp_path/'out').exists()
