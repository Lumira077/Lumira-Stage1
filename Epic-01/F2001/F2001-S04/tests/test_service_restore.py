import json,sqlite3,tempfile,unittest
from pathlib import Path
from onboarding_ops import dependency
from onboarding_ops.service import ObservedService
from onboarding_ops.telemetry import Sink
from onboarding_ops.restore import RestoreLab
from onboarding_ops.metrics import aggregate
from onboarding_lab.safety import Broker
from onboarding_lab.adapters import GuardedOutputs
from ker_onboarding.service import Service,POLICY_VERSION
from ker_onboarding.core import STEPS,DEFAULTS,CONSENTS,Error
OWNER='local-demo-owner';GUARDIAN='local-demo-guardian'
def data(actor=OWNER,kind='self'):
    return {'registration':{'registration_type':kind,'subject_id':'demo-child-01' if kind=='guardian' else 'guest' if kind=='guest' else actor},
            'language':{'language':'ko-KR'},'profile':{'nickname':'synthetic-only','preferred_name':'샘플'},'purpose':{'purpose':'companion'},'preferences':dict(DEFAULTS),
            'consent':{**{k:True if kind!='guest' else False for k in CONSENTS},'policy_version':POLICY_VERSION},'review':{'confirmed':True}}
def fill(service,sid,actor=OWNER,kind='self'):
    x=service.get(sid,actor)
    for step in STEPS:x=service.save_step(sid,actor,step,data(actor,kind)[step],x['revision'])
    return service.complete(sid,actor,'complete',x['revision'])
class Instrumentation(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();p=Path(self.tmp.name);self.now=1000
        self.sink=Sink(str(p/'events.db'),b'k'*32,clock=lambda:self.now)
        self.b=Broker(str(p/'outputs.db'));self.s=ObservedService(str(p/'app.db'),sink=self.sink,outputs=GuardedOutputs(self.b,fail_once='tts'))
        self.sid=self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id']
    def tearDown(self):self.s.close();self.b.close();self.sink.close();self.tmp.cleanup()
    def test_persisted_transitions_and_retry_metrics(self):
        r=fill(self.s,self.sid);self.now+=20;self.s.apply(self.sid,OWNER);self.s.apply(self.sid,OWNER);self.s.greeting(self.sid,OWNER);self.s.greeting(self.sid,OWNER)
        m=aggregate(self.sink.read(),0,2000,4000);self.assertEqual(m['ready_sessions'],1);self.assertEqual(m['apply_failure']['value'],.5)
        self.assertNotIn('synthetic-only',json.dumps(self.sink.read()));self.assertNotIn('샘플',json.dumps(self.sink.read()))
    def test_duplicate_create_and_complete_do_not_double_count(self):
        self.s.create(OWNER,'demo-device-01',['demo-device-01']);r=fill(self.s,self.sid);self.s.complete(self.sid,OWNER,'complete',8)
        m=aggregate(self.sink.read(),0,2000,4000);self.assertEqual(m['started_sessions'],1);self.assertEqual(m['registered_sessions'],1)
    def test_resume_instrumentation(self):
        self.s.resume(self.sid,OWNER);m=aggregate(self.sink.read(),0,2000,4000);self.assertEqual(m['resume_success']['value'],1)
    def test_logger_failure_does_not_roll_back_registration(self):
        self.sink.close();r=fill(self.s,self.sid);self.assertIsNotNone(r['profile_id']);self.assertGreater(self.s.dropped_events,0)
        self.sink.db=sqlite3.connect(':memory:')  # teardown-only replacement
    def test_support_unique_and_cancel_separate(self):
        self.s.request_support(self.sid,OWNER);self.s.request_support(self.sid,OWNER);self.s.cancel(self.sid,OWNER)
        m=aggregate(self.sink.read(),0,2000,4000);self.assertEqual(m['support_request']['numerator'],1);self.assertEqual(m['cancelled_sessions'],1)
    def test_unauthorized_requests_produce_no_victim_events(self):
        n=len(self.sink.read())
        with self.assertRaises(Error):self.s.resume(self.sid,GUARDIAN)
        self.assertEqual(len(self.sink.read()),n)
class Restore(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name);(self.p/'.ker-development-sandbox').write_text('development only')
        self.s=Service(str(self.p/'current.sqlite3'));sid=self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id'];self.first=fill(self.s,sid)
        sid2=self.s.create(GUARDIAN,'demo-guardian-01',['demo-guardian-01'])['session_id'];self.second=fill(self.s,sid2,GUARDIAN,'guardian')
        self.draft=self.s.create(OWNER,'demo-guest-01',['demo-guest-01'])['session_id'];self.s.save_step(self.draft,OWNER,'registration',data()['registration'],1)
        self.lab=RestoreLab(self.p);self.lab.backup()
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def ledger(self,records):
        (self.p/'privacy-ledger.json').write_text(json.dumps([{'seq':i,'operation':op,'profile_id':pid,'purpose':purpose} for i,(op,pid,purpose) in enumerate(records,1)]))
    def test_snapshot_preserves_registered_and_in_progress(self):
        self.ledger([]);self.lab.restore();db=sqlite3.connect(self.p/'restored.sqlite3')
        try:self.assertEqual(db.execute('SELECT count(*) FROM profiles').fetchone()[0],2);self.assertIn('registration',json.loads(db.execute('SELECT data FROM sessions WHERE id=?',(self.draft,)).fetchone()[0]))
        finally:db.close()
    def test_newer_deletion_not_resurrected(self):
        self.ledger([('delete_profile',self.first['profile_id'],None)]);self.lab.restore();db=sqlite3.connect(self.p/'restored.sqlite3')
        try:
            self.assertIsNone(db.execute('SELECT 1 FROM profiles WHERE id=?',(self.first['profile_id'],)).fetchone())
            self.assertIsNone(db.execute('SELECT 1 FROM applications WHERE session_id=?',(self.first['session_id'],)).fetchone())
            self.assertEqual(json.loads(db.execute('SELECT data FROM sessions WHERE id=?',(self.first['session_id'],)).fetchone()[0]),{})
        finally:db.close()
    def test_revocation_reapplied_to_all_contexts(self):
        self.ledger([('revoke_consent',self.second['profile_id'],'long_term_memory')]);self.lab.restore();db=sqlite3.connect(self.p/'restored.sqlite3')
        try:
            d=json.loads(db.execute('SELECT data FROM profiles WHERE id=?',(self.second['profile_id'],)).fetchone()[0]);self.assertFalse(d['consent']['long_term_memory'])
            row=db.execute('SELECT state,context FROM applications WHERE session_id=?',(self.second['session_id'],)).fetchone();self.assertEqual(row[0],'pending');self.assertFalse(json.loads(row[1])['permissions']['long_term_memory'])
            self.assertEqual(db.execute('SELECT granted FROM consent_events WHERE profile_id=? AND purpose=?',(self.second['profile_id'],'long_term_memory')).fetchone()[0],0)
        finally:db.close()
    def test_missing_ledger_blocks_restore(self):
        with self.assertRaises(ValueError):self.lab.restore()
    def test_unsupported_schema_blocks_simple_rollback(self):
        self.ledger([]);db=sqlite3.connect(self.p/'snapshot.sqlite3');db.execute('UPDATE schema_metadata SET version=3');db.commit();db.close()
        with self.assertRaises(ValueError):self.lab.restore()
    def test_missing_sandbox_marker_rejected(self):
        (self.p/'.ker-development-sandbox').unlink()
        with self.assertRaises(ValueError):RestoreLab(self.p)
    def test_symlink_destination_rejected(self):
        self.ledger([]);(self.p/'restored.sqlite3').symlink_to(self.p/'current.sqlite3')
        with self.assertRaises(ValueError):self.lab.restore()
    def test_malformed_ledger_sequence_rejected(self):
        (self.p/'privacy-ledger.json').write_text('[{"seq":2,"operation":"delete_profile","profile_id":"x","purpose":null}]')
        with self.assertRaises(ValueError):self.lab.restore()
    def test_restore_is_repeatable_and_never_production_approval(self):
        self.ledger([('revoke_consent',self.first['profile_id'],'cloud_transfer')]);a=self.lab.restore();b=self.lab.restore();self.assertEqual(a,b);self.assertFalse(a['production_restore_verified'])
