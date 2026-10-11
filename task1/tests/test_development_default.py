from policy_agent.cli import choose, parser


def test_live_entrypoints_use_pinned_development_config():
    for command in ('doctor', 'replay', 'chat'):
        config = choose(parser().parse_args([command]))
        assert config['config_id'] == 'anthropic/claude-haiku-5-5/adaptive/medium'


def test_explicit_configuration_can_override_development_default():
    config = choose(parser().parse_args(['replay', '--config-id', 'openai/gpt-6.1-sol/reasoning/low']))
    assert config['config_id'] == 'openai/gpt-6.1-sol/reasoning/low'


def test_explicit_provider_is_preserved():
    config = choose(parser().parse_args(['chat', '--provider', 'openai']))
    assert config['provider'] == 'openai'
