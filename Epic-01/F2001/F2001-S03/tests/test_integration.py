import io,json,sqlite3,tempfile,unittest
from pathlib import Path
from onboarding_lab import dependency
from onboarding_lab.safety import Broker,Rejected,confirmed_input
from onboarding_lab.adapters import GuardedOutputs,LabService
from ker_onboarding.core import Error,STEPS,DEFAULTS,CONSENTS
from ker_onboarding.api import Application
from ker_onboarding.service import POLICY_VERSION
OWNER='local-demo-owner';GUARDIAN='local-demo-guardian'
def inputs(actor=OWNER,kind='self'):
    return {'registration':{'registration_type':kind,'subject_id':'guest' if kind=='guest' else 'demo-child-01' if kind=='guardian' else actor},
        'language':{'language':'ko-KR'},'profile':{'nickname':'샘플','preferred_name':'박사님'},'purpose':{'purpose':'companion'},
        'preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY_VERSION},'review':{'confirmed':True}}
class Integration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.now=1000
        self.broker=Broker(str(self.root/'outputs.db'),clock=lambda:self.now)
        self.s=LabService(str(self.root/'service.db'),clock=lambda:self.now,outputs=GuardedOutputs(self.broker))
        self.sid=self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id']
    def tearDown(self):self.s.close();self.broker.close();self.tmp.cleanup()
    def fill(self,sid=None,actor=OWNER,kind='self',values=None):
        sid=sid or self.sid;x=self.s.get(sid,actor);d=values or inputs(actor,kind)
        for step in STEPS:x=self.s.save_step(sid,actor,step,d[step],x['revision'])
        return x
    def complete(self,sid=None,actor=OWNER,kind='self',values=None):
        sid=sid or self.sid;x=self.fill(sid,actor,kind,values);return self.s.complete(sid,actor,'complete-1',x['revision'])
    def fails(self,code,fn,exc=Error):
        with self.assertRaises(exc) as e:fn()
        self.assertIn(code,str(e.exception))
    def test_ONB_01_new_registration(self):
        self.complete();self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'applied');self.assertIn('박사님',self.s.greeting(self.sid,OWNER)['text'])
    def test_ONB_02_guardian(self):
        sid=self.s.create(GUARDIAN,'demo-guardian-01',['demo-guardian-01'])['session_id'];r=self.complete(sid,GUARDIAN,'guardian')
        context=self.s.context(r['profile_id'],GUARDIAN);self.assertEqual(context['actor_id'],GUARDIAN);self.assertEqual(context['subject_id'],'demo-child-01')
    def test_ONB_03_guest(self):
        r=self.complete(kind='guest');self.assertIsNone(r['profile_id']);self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],0)
        self.s.apply(self.sid,OWNER);self.assertIn('박사님',self.s.greeting(self.sid,OWNER)['text'])
    def test_ONB_04_consent_refusal(self):
        r=self.complete();self.assertTrue(all(v is False for v in self.s.context(r['profile_id'],OWNER)['permissions'].values()))
    def test_ONB_05_setting_accuracy(self):
        d=inputs();d['profile']['preferred_name']='친구';d['language']['language']='en-US';d['preferences'].update(voice_id='demo_voice_a',volume=0,speech_rate=1.1)
        r=self.complete(values=d);a=self.s.apply(self.sid,OWNER)
        self.assertEqual(a['apply_status'],'applied')
        for ack in a['acks']:self.assertEqual(ack['applied_settings'],d['preferences'])
        g=self.s.greeting(self.sid,OWNER);self.assertIn('친구',g['text']);self.assertEqual(g['preferences'],d['preferences'])
    def test_ONB_06_saved_step_process_restart(self):
        x=self.s.get(self.sid,OWNER)
        for step in STEPS:
            x=self.s.save_step(self.sid,OWNER,step,inputs()[step],x['revision'])
            self.s.close();self.s=LabService(str(self.root/'service.db'),clock=lambda:self.now,outputs=GuardedOutputs(self.broker))
            restored=self.s.get(self.sid,OWNER);self.assertEqual(restored['draft'],x['draft'])
        # Uncommitted transaction disappears after connection close; NOT a physical power-loss test.
        self.s.db.execute('BEGIN IMMEDIATE');self.s.db.execute("UPDATE sessions SET data='{}' WHERE id=?",(self.sid,));self.s.close()
        self.s=LabService(str(self.root/'service.db'),clock=lambda:self.now,outputs=GuardedOutputs(self.broker));self.assertIn('review',self.s.get(self.sid,OWNER)['draft'])
    def test_ONB_07_network_fixture_reconnect(self):
        x=self.fill();self.s.devices.set_connected(OWNER,'demo-device-01',False)
        self.fails('DEVICE_DISCONNECTED',lambda:self.s.complete(self.sid,OWNER,'c1',x['revision']))
        self.s.devices.set_connected(OWNER,'demo-device-01',True);self.s.complete(self.sid,OWNER,'c1',x['revision'])
        self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],1)
    def test_ONB_08_client_reconnect_authorization(self):
        self.fill();self.fails('NOT_FOUND',lambda:self.s.get(self.sid,GUARDIAN));self.assertIn('review',self.s.get(self.sid,OWNER)['draft'])
    def test_ONB_09_repeated_complete_and_greeting(self):
        x=self.fill();r=self.s.complete(self.sid,OWNER,'c1',x['revision'])
        for _ in range(3):self.assertEqual(r,self.s.complete(self.sid,OWNER,'c1',x['revision']))
        self.s.apply(self.sid,OWNER)
        results=[self.s.greeting(self.sid,OWNER) for _ in range(3)]
        self.assertEqual(sum(r['logical_output_started'] for r in results),1)
        self.assertEqual(len([e for e in self.broker.transport.events if e['kind']=='first_greeting']),1)
    def test_ONB_10_unauthorized_access(self):
        self.complete()
        for fn in [lambda:self.s.get(self.sid,GUARDIAN),lambda:self.s.save_step(self.sid,GUARDIAN,'profile',inputs()['profile'],1),lambda:self.s.complete(self.sid,GUARDIAN,'c1',1)]:self.fails('NOT_FOUND',fn)
    def test_ONB_11_cancel_expiry(self):
        self.s.cancel(self.sid,OWNER);self.fails('SESSION_NOT_ACTIVE',lambda:self.s.complete(self.sid,OWNER,'c1',1))
        sid=self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id'];self.now+=86401
        self.fails('SESSION_EXPIRED',lambda:self.s.get(sid,OWNER));self.s.purge_expired();self.assertEqual(self.s.get(sid,OWNER)['draft'],{})
    def test_ONB_12_database_failure(self):
        x=self.fill();self.s.db.execute("CREATE TRIGGER inject BEFORE INSERT ON applications BEGIN SELECT RAISE(ABORT,'injected'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.s.complete(self.sid,OWNER,'c1',x['revision'])
        for table in ['profiles','consent_events','applications','completions']:self.assertEqual(self.s.db.execute('SELECT count(*) FROM '+table).fetchone()[0],0)
        self.s.db.execute('DROP TRIGGER inject');self.s.complete(self.sid,OWNER,'c1',x['revision'])
    def test_ONB_13_each_output_failure_recovery(self):
        self.complete()
        for module in ('context','tts','expression','motion'):
            # Recreate only application/ACK state inside this dedicated test fixture.
            self.s.db.execute('DELETE FROM module_acks');self.s.db.execute("UPDATE applications SET state='pending'")
            self.s.outputs=GuardedOutputs(self.broker,fail_once=module)
            self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'failed')
            self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'applied')
        self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],1)
    def test_ONB_14_preview_stop_discards_delayed_output(self):
        sid='preview';epoch=self.broker.begin(sid,OWNER);cid=self.broker.submit(sid,OWNER,epoch,'motion',{'gesture':'none','level':1},'p1')
        self.broker.stop(sid,OWNER);self.fails('STALE_EPOCH',lambda:self.broker.dispatch(cid,OWNER),Rejected)
        self.assertEqual(self.broker.transport.events,[])
    def test_ONB_15_restart_no_automatic_output(self):
        self.complete();self.s.apply(self.sid,OWNER);self.s.greeting(self.sid,OWNER)
        self.broker.close();self.broker=Broker(str(self.root/'outputs.db'),clock=lambda:self.now)
        self.s.close();self.s=LabService(str(self.root/'service.db'),clock=lambda:self.now,outputs=GuardedOutputs(self.broker))
        self.fails('OUTPUT_DISABLED',lambda:self.s.greeting(self.sid,OWNER),Rejected)
        self.assertEqual(self.broker.transport.events,[]);self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],1)
    def test_ONB_16_local_offline_text(self):
        self.complete();self.s.apply(self.sid,OWNER);self.assertIn('루미라',self.s.greeting(self.sid,OWNER)['text'])
    def test_unconfirmed_critical_recognition(self):
        self.fails('USER_CONFIRMATION_REQUIRED',lambda:confirmed_input('consent',True,False),Rejected)
        self.assertFalse(confirmed_input('consent',False,True));self.assertEqual(confirmed_input('preferred_name','친구',True),'친구')
    def test_HTTP_guarded_application(self):
        app=Application(self.s,[{'token':'synthetic-token','actor_id':OWNER,'device_ids':['demo-device-01']}])
        self.complete();self.s.apply(self.sid,OWNER)
        env={'REQUEST_METHOD':'POST','PATH_INFO':'/v1/onboarding/sessions/'+self.sid+'/greeting','CONTENT_LENGTH':'2',
             'HTTP_AUTHORIZATION':'Bearer synthetic-token','HTTP_HOST':'127.0.0.1:8081','wsgi.input':io.BytesIO(b'{}')}
        status=[];r=json.loads(b''.join(app(env,lambda s,h:status.append(s))));self.assertTrue(status[0].startswith('200'));self.assertFalse(r['physical_output'])
    def test_cancel_session_invalidates_preview_bundle(self):
        r=self.s.preview(self.sid,OWNER,DEFAULTS);self.s.cancel(self.sid,OWNER)
        self.fails('SESSION_NOT_ACTIVE',lambda:self.s.dispatch_preview(self.sid,OWNER,r['command_ids']))
        for cid in r['command_ids']:self.fails('STALE_EPOCH',lambda:self.broker.dispatch(cid,OWNER),Rejected)
        self.assertEqual(self.broker.transport.events,[])
    def test_preview_bundle_validation_no_partial_queue(self):
        self.fails('VOLUME_LIMIT',lambda:self.s.preview(self.sid,OWNER,dict(DEFAULTS,volume=100)),Rejected)
        self.assertEqual(self.broker.db.execute('SELECT count(*) FROM commands').fetchone()[0],0)
    def test_delayed_preview_after_expiry_rejected(self):
        r=self.s.preview(self.sid,OWNER,DEFAULTS);self.now+=86401
        self.fails('SESSION_EXPIRED',lambda:self.s.dispatch_preview(self.sid,OWNER,r['command_ids']))
        self.assertEqual(self.broker.transport.events,[])
    def test_multiple_guests_use_distinct_application_scope(self):
        r1=self.complete(kind='guest');self.s.apply(self.sid,OWNER)
        sid2=self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id'];r2=self.complete(sid2,kind='guest');self.s.apply(sid2,OWNER)
        g1=self.s.greeting(self.sid,OWNER);g2=self.s.greeting(sid2,OWNER)
        self.assertNotEqual(g1['command_id'],g2['command_id']);self.assertNotEqual(r1['application_id'],r2['application_id'])
