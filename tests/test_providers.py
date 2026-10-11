import json
from types import SimpleNamespace as N

import pytest
from pydantic import BaseModel
from policy_agent.providers import Budget, BudgetExceeded, Provider, ProviderError

class Answer(BaseModel):
    value: int

def config(provider='openai'):
    return dict(provider=provider, model='test-model', input_per_million=2,
                output_per_million=10, cached_input_per_million=.2, max_output_tokens=100)

def response(raw='{"value":1}'):
    return N(output_text=raw, status='completed', model='actual-model',
             usage=N(input_tokens=100, output_tokens=10, input_tokens_details=N(cached_tokens=50)))

class Client:
    def __init__(self, outcomes):
        self.responses = self.messages = self
        self.outcomes = iter(outcomes)
        self.requests=[]
    def create(self, **kwargs):
        self.requests.append(kwargs)
        result = next(self.outcomes)
        if isinstance(result, Exception): raise result
        return result

def test_usage_cached_and_config_preserved():
    client=Client([response()]); budget=Budget()
    p=Provider(config(),budget,client)
    assert p.generate(Answer,'system',{}).value == 1
    assert budget.spent == pytest.approx(.00021)
    assert p.calls[0]['response_model']=='actual-model'
    assert client.requests[0]['store'] is False
    assert client.requests[0]['text']['format']['schema']['additionalProperties'] is False

def test_persistent_budget_prevents_second_process_overspend(tmp_path):
    path=tmp_path/'ledger.json'
    first=Budget(1,path); second=Budget(1,path)
    key=first.reserve(.8)
    with pytest.raises(BudgetExceeded): second.reserve(.3)
    second.settle(key,.1)
    assert first.spent == .1

def test_no_call_when_budget_insufficient():
    client=Client([])
    with pytest.raises(BudgetExceeded): Provider(config(),Budget(.000001),client).generate(Answer,'s',{})
    assert not client.requests

def test_one_schema_repair_both_calls_counted():
    client=Client([response('{"value":"bad"}'),response()])
    p=Provider(config(),Budget(),client)
    assert p.generate(Answer,'s',{}).value==1
    assert len(p.calls)==2 and p.calls[0]['validation_error']
    assert p.budget.spent == pytest.approx(.00042)

def test_auth_error_not_retried_or_leaked():
    error=RuntimeError('SECRET-CREDENTIAL'); error.status_code=401
    p=Provider(config(),Budget(),Client([error]))
    with pytest.raises(ProviderError, match='401') as caught: p.generate(Answer,'s',{})
    assert 'SECRET' not in str(caught.value)
    assert 'SECRET' not in json.dumps(p.calls)
    assert len(p.calls)==1 and p.budget.spent>0

def test_transient_two_retries(monkeypatch):
    monkeypatch.setattr('policy_agent.providers.time.sleep',lambda _:None)
    error=RuntimeError('server'); error.status_code=503
    p=Provider(config(),Budget(),Client([error,error,error]))
    with pytest.raises(ProviderError): p.generate(Answer,'s',{})
    assert len(p.calls)==3

def test_anthropic_native_format_and_cache_usage():
    result=N(content=[N(type='text',text='{"value":2}')],stop_reason='end_turn',model='test',
             usage=N(input_tokens=100,output_tokens=10,cache_read_input_tokens=50,cache_creation_input_tokens=5))
    client=Client([result]); p=Provider(config('anthropic'),Budget(),client)
    assert p.generate(Answer,'s',{}).value==2
    assert 'format' in client.requests[0]['output_config']
    assert p.calls[0]['input_tokens']==155
    assert p.budget.spent==pytest.approx(.00033)

def test_truncated_response_never_repaired():
    result=response(); result.status='incomplete'
    p=Provider(config(),Budget(),Client([result]))
    with pytest.raises(ProviderError,match='incomplete'): p.generate(Answer,'s',{})
    assert len(p.calls)==1
    assert p.calls[0]['error']=='IncompleteResponse'


def test_openai_cache_writes_are_not_double_counted():
    result=response()
    result.id='resp_fake';result._request_id='req_fake'
    result.usage.input_tokens_details.cache_write_tokens=20
    c=config();c.update(cache_write_per_million=2.5,config_id='openai/test-model/reasoning/low')
    client=Client([result]);p=Provider(c,Budget(),client)
    p.generate(Answer,'s',{})
    # 100 total = 30 ordinary + 50 cached reads + 20 writes.
    assert p.calls[0]['input_tokens']==100
    assert p.calls[0]['uncached_input_tokens']==30
    assert p.calls[0]['cache_write_tokens']==20
    assert p.budget.spent==pytest.approx((30*2+50*.2+20*2.5+10*10)/1e6)
    assert p.calls[0]['config_id']==c['config_id']
    assert p.calls[0]['request_id']=='req_fake'
    assert client.requests[0]['service_tier']=='default'


def test_reservation_accounts_for_write_premium_before_request():
    client=Client([]);c=config();c['cache_write_per_million']=100
    p=Provider(c,Budget(.1),client)
    with pytest.raises(BudgetExceeded):p.generate(Answer,'s',{})
    assert not client.requests


def test_anthropic_explicit_standard_service_tier():
    result=N(content=[N(type='text',text='{"value":2}')],stop_reason='end_turn',model='test',
             usage=N(input_tokens=1,output_tokens=1))
    client=Client([result]);p=Provider(config('anthropic'),Budget(),client)
    p.generate(Answer,'s',{})
    assert client.requests[0]['service_tier']=='standard_only'
