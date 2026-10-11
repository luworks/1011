from datetime import datetime, date, timedelta
from decimal import Decimal
from pathlib import Path
import shutil
import pytest
from policy_agent.corpus import Corpus
from policy_agent.policy import evaluate
from policy_agent.schema import AccountContext

ROOT=Path(__file__).resolve().parents[1]
@pytest.fixture
def corpus(): return Corpus(ROOT)

def context(**updates):
    base=dict(monthly_charge='225',outage_start=datetime(2026,9,10),outage_end=datetime(2026,9,21),request_date=date(2026,10,5),ticket_status='verified',ticket_number='OUT-58823',line_item='Recurring plan charge',statement_date=date(2026,10,1),address_matches=True,history_checked=True,fraud=False,identity_verified=True)
    base.update(updates)
    return AccountContext(**base)

def test_dana(corpus):
    d=evaluate('outage_credit',context(),corpus)
    assert d.amount=='82.50'
    assert d.action_status=='eligible_for_simulation'
    assert d.policy_ids==['Rule 1','Rule 3','Rule 4','Rule 5']
    assert 'not counted against' in d.reply

@pytest.mark.parametrize('charge,action',[('300','eligible_for_simulation'),('300.01','requires_human')])
def test_amount_boundary(corpus,charge,action):
    d=evaluate('outage_credit',context(monthly_charge=charge,outage_start=datetime(2026,8,22),outage_end=datetime(2026,9,21)),corpus)
    assert d.action_status==action

@pytest.mark.parametrize('seconds,qualifies',[(14400,False),(14401,True),(86399,True),(86400,True)])
def test_four_hours_full_days(corpus,seconds,qualifies):
    d=evaluate('outage_credit',context(outage_start=datetime(2026,9,21)-timedelta(seconds=seconds)),corpus)
    assert ('Rule 2' not in d.policy_ids)==qualifies
    if qualifies: assert d.amount==('7.50' if seconds==86400 else '0.00')

@pytest.mark.parametrize('days,qualifies',[(30,True),(31,False)])
def test_outage_window(corpus,days,qualifies):
    d=evaluate('outage_credit',context(request_date=date(2026,9,21)+timedelta(days=days)),corpus)
    assert ('Rule 2' not in d.policy_ids)==qualifies

@pytest.mark.parametrize('days,action',[(30,'eligible_for_simulation'),(31,'requires_human')])
def test_duration_boundary(corpus,days,action):
    d=evaluate('outage_credit',context(monthly_charge='10',outage_start=datetime(2026,9,21)-timedelta(days=days)),corpus)
    assert d.action_status==action

@pytest.mark.parametrize('days,action',[(89,'requires_human'),(90,'requires_human'),(91,'eligible_for_simulation')])
def test_repeat_boundary(corpus,days,action):
    d=evaluate('outage_credit',context(prior_resolved_date=date(2026,10,5)-timedelta(days=days)),corpus)
    assert d.action_status==action

def test_unknown_global_checks_preserve_calculation(corpus):
    d=evaluate('outage_credit',context(history_checked=False,fraud=None),corpus)
    assert d.amount=='82.50'
    assert d.action_status=='pending_verification'
    assert set(d.missing)=={'dispute_history','fraud_check'}

@pytest.mark.parametrize('ticket,status,rule2',[('absent','pending_verification',True),('unknown','pending_verification',False),('unverifiable','requires_human',False)])
def test_ticket_states(corpus,ticket,status,rule2):
    d=evaluate('outage_credit',context(ticket_status=ticket),corpus)
    assert d.action_status==status
    assert ('Rule 2' in d.policy_ids)==rule2

@pytest.mark.parametrize('amount,total,action',[('25','50','eligible_for_simulation'),('25.01','50','requires_human')])
def test_goodwill_cumulative(corpus,amount,total,action):
    d=evaluate('general_credit',context(general_amount=amount,goodwill_total=total,billing_error_confirmed=True,line_item='Duplicate add-on',statement_date=date(2026,10,1)),corpus)
    assert d.action_status==action

@pytest.mark.parametrize('days,action',[(60,'eligible_for_simulation'),(61,'requires_human')])
def test_dispute_window(corpus,days,action):
    d=evaluate('general_credit',context(general_amount='1',goodwill_total='0',billing_error_confirmed=True,line_item='Duplicate add-on',statement_date=date(2026,10,5)-timedelta(days=days)),corpus)
    assert d.action_status==action

def test_fraud_overrides(corpus):
    d=evaluate('outage_credit',context(fraud=True),corpus)
    assert d.action_status=='requires_human'
    assert d.amount=='82.50'

def test_tax_gap(corpus):
    d=evaluate('taxes',context(),corpus)
    assert d.answer_status=='partial' and d.action_status=='requires_human'
    assert 'cannot confirm either outcome' in d.reply
    assert len(corpus.retrieve('taxes',['taxes']))==15

def test_corpus_and_tamper(tmp_path,corpus):
    assert len(corpus.entries)==15
    for folder in ('exam','config'):shutil.copytree(ROOT/folder,tmp_path/folder)
    source=tmp_path/corpus.get('Rule 3').path
    source.write_text(source.read_text()+'\nChanged')
    with pytest.raises(ValueError,match='Policy source changed'): Corpus(tmp_path)

def test_negative_duration_not_eligible(corpus):
    d=evaluate('outage_credit',context(outage_start=datetime(2026,9,22)),corpus)
    assert d.amount is None and d.action_status=='pending_verification'

@pytest.mark.parametrize('ticket',[None,'invented','OUT-1234'])
def test_verified_requires_ticket_identifier(corpus,ticket):
    d=evaluate('outage_credit',context(ticket_number=ticket),corpus)
    assert d.amount is None and d.action_status=='pending_verification'
    assert d.conditions['valid_ticket'] is None

def test_future_request_blocks_outage_eligibility(corpus):
    d=evaluate('outage_credit',context(request_date=date(2026,9,20)),corpus)
    assert d.amount is None
    assert d.conditions['within_outage_window'] is None

def test_future_statement_blocks_issue_not_amount(corpus):
    d=evaluate('outage_credit',context(statement_date=date(2026,10,6)),corpus)
    assert d.amount=='82.50' and d.action_status=='pending_verification'
    assert 'valid_statement_date' in d.missing

def test_old_statement_escalates_independently(corpus):
    d=evaluate('outage_credit',context(statement_date=date(2026,8,1)),corpus)
    assert d.amount=='82.50' and d.action_status=='requires_human'
    assert d.conditions['within_outage_window'] is True
    assert d.conditions['within_dispute_window'] is False

def test_unknown_invoice_details_block_issue_not_formula(corpus):
    d=evaluate('outage_credit',context(statement_date=None,line_item=None),corpus)
    assert d.amount=='82.50' and d.action_status=='pending_verification'
    assert {'statement_date','line_item'} <= set(d.missing)
