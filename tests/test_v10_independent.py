"""Independent v10 authority regressions, synthetic inputs, no paid providers."""
from policy_agent.corpus import Corpus
from policy_agent.workflow import Workflow


def context():
    return dict(general_amount='20',goodwill_total='0',statement_date='2026-10-01',
        request_date='2026-10-05',billing_error_confirmed=True,identity_verified=True,
        fraud=False,history_checked=True,line_item='duplicate device charge')


def turn(flow, item=None, correction=False):
    text='Please refund the charge.' if item is None else f'Please refund the {item}.'
    facts=[] if item is None else [dict(field='line_item',value=item,
        source_index=len(flow.messages),quote=item,correction=correction)]
    return flow.turn(text,dict(intents=['general_credit'],facts=facts,search_query='credit'))


def test_shorter_reference_preserves_record_but_cannot_inherit_authority():
    flow=Workflow(Corpus(),context=context())
    result=turn(flow,'device charge')
    assert flow.context.line_item=='duplicate device charge'
    assert 'line_item' not in flow.conflicts
    assert result['decisions'][0]['action_status']=='pending_verification'
    assert result['decisions'][0]['action_status']!='eligible_for_simulation'


def test_unrelated_reference_does_not_reuse_previous_billing_error_approval():
    flow=Workflow(Corpus(),context=context())
    result=turn(flow,'insurance premium')
    assert flow.context.line_item=='duplicate device charge'
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_unresolved_reference_survives_followup_without_new_item():
    flow=Workflow(Corpus(),context=context())
    turn(flow,'insurance premium')
    result=turn(flow)
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_explicit_correction_remains_conflict_and_preserves_trusted_value():
    flow=Workflow(Corpus(),context=context())
    result=turn(flow,'insurance premium',True)
    assert flow.context.line_item=='duplicate device charge'
    assert 'line_item' in flow.conflicts
    assert result['decisions'][0]['action_status']=='pending_verification'


def test_exact_same_label_still_uses_existing_verified_account():
    flow=Workflow(Corpus(),context=context())
    result=turn(flow,'duplicate device charge')
    assert result['decisions'][0]['action_status']=='eligible_for_simulation'


def test_reference_ambiguity_cannot_suppress_global_fraud_escalation():
    record=context();record['fraud']=True
    flow=Workflow(Corpus(),context=record)
    result=turn(flow,'insurance premium')
    assert result['decisions'][0]['action_status']=='requires_human'


def test_customer_same_label_cannot_clear_pending_reference():
    flow=Workflow(Corpus(),context=context())
    turn(flow,'insurance premium')
    result=turn(flow,'duplicate device charge')
    assert result['decisions'][0]['action_status']=='pending_verification'
    assert 'line_item_reference_resolution' in result['decisions'][0]['missing']


def test_explicit_tool_reconfirmation_resolves_pending_reference():
    flow=Workflow(Corpus(),context=context())
    turn(flow,'device charge')
    flow.observe('tool','Confirmed the current dispute refers to the recorded item',
                 {'line_item':'duplicate device charge'})
    result=turn(flow)
    assert result['decisions'][0]['action_status']=='eligible_for_simulation'
    assert result['unresolved_item_references']==[]


def test_tool_unknown_item_does_not_restore_eligibility():
    flow=Workflow(Corpus(),context=context())
    turn(flow,'device charge')
    flow.observe('tool','Could not resolve the disputed item',{'line_item':None})
    result=turn(flow)
    assert result['decisions'][0]['action_status']=='pending_verification'
    assert 'line_item' not in flow.verified_fields


def test_tool_switching_disputed_item_does_not_reuse_old_item_approval():
    flow=Workflow(Corpus(),context=context())
    flow.observe('tool','Identified a different disputed bill item',{'line_item':'insurance premium'})
    result=turn(flow)
    assert result['decisions'][0]['action_status']!='eligible_for_simulation'


def live_understanding(message, intents):
    from policy_agent.workflow import FACT_FIELDS
    return dict(intents=intents,facts=[],search_query='request',
        field_review=[dict(field=f,presence='not_stated') for f in FACT_FIELDS],
        requested_answers=[dict(intent=i,quote=message,requested_outcome=i) for i in intents])


class ScopeProvider:
    def __init__(self,message,classifications):
        self.message,self.classifications=message,classifications
        self.calls=[]
    def generate(self,schema,system,payload):
        from policy_agent.workflow import LiveUnderstanding,ScopeReview,EvidenceBoundCandidate
        self.calls.append(schema.__name__)
        if schema is LiveUnderstanding:
            return schema.model_validate(live_understanding(self.message,list(self.classifications)))
        if schema is ScopeReview:
            return schema.model_validate({'questions':[dict(intent=i,clause_quote=self.message,
                action_quote=self.message if c=='explicit' else None,classification=c)
                for i,c in self.classifications.items()]})
        assert schema is EvidenceBoundCandidate
        return schema.model_validate({'questions':[dict(intent=i,policy_ids=[],amount=None,
            answer_status='partial',action_status='requires_human',evidence=[],tax_adjustment='unknown')
            for i in payload['requested_intents']]})


def test_background_object_does_not_create_extra_policy_decision():
    message='Only tell me whether that credit changes my taxes.'
    provider=ScopeProvider(message,{'outage_credit':'background','taxes':'explicit'})
    result=Workflow(Corpus(),provider,context()).turn(message)
    assert result['error'] is None
    assert [d['question'] for d in result['decisions']]==['taxes']


def test_genuinely_mixed_requests_remain_separate():
    message='Calculate my outage credit and tell me whether taxes change.'
    provider=ScopeProvider(message,{'outage_credit':'explicit','taxes':'explicit'})
    result=Workflow(Corpus(),provider,context()).turn(message)
    assert result['error'] is None
    assert {d['question'] for d in result['decisions']}=={'taxes','outage_credit'}


def test_uncertain_scope_never_gets_execution_permission():
    message='What about that earlier charge?'
    provider=ScopeProvider(message,{'general_credit':'uncertain'})
    result=Workflow(Corpus(),provider,context()).turn(message)
    assert result['error'] is None
    assert result['decisions'][0]['answer_status']=='needs_information'
    assert result['decisions'][0]['action_status']=='not_applicable'
    assert 'EvidenceBoundCandidate' not in provider.calls


def test_one_schema_repair_exhausts_same_turn_contract_repair():
    import json
    from types import SimpleNamespace as NS
    from policy_agent.providers import Provider,Budget
    message='Will taxes change?'
    malformed=live_understanding(message,['taxes']);malformed['field_review']=[]
    class Client:
        def __init__(self):
            self.responses=self;self.calls=0
        def create(self,**kwargs):
            self.calls+=1
            assert self.calls<=2,'Unexpected second content repair'
            return NS(output_text='not json' if self.calls==1 else json.dumps(malformed),
                      status='completed',model='fake',usage=NS(input_tokens=10,output_tokens=10))
    client=Client()
    provider=Provider(dict(provider='openai',model='fake',input_per_million=1,
        output_per_million=1,cached_input_per_million=.1,max_output_tokens=100),Budget(),client)
    result=Workflow(Corpus(),provider,context()).turn(message)
    assert result['error'] is not None
    assert not result['decisions']
    assert client.calls==2
    assert len(result['content_repairs'])==1
    assert result['content_repairs'][0]['stage']=='structured_output'
