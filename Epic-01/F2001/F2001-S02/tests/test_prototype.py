import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from ker_onboarding.core import Error, STEPS, DEFAULTS, CONSENTS
from ker_onboarding.service import Service, POLICY_VERSION
from ker_onboarding.adapters import SimulatedOutputs
from ker_onboarding.api import Application

OWNER='local-demo-owner'
GUARDIAN='local-demo-guardian'
def data(actor=OWNER,kind='self'):
    return {'registration':{'registration_type':kind,'subject_id':'guest' if kind=='guest' else 'demo-child-01' if kind=='guardian' else actor},
            'language':{'language':'ko-KR'},'profile':{'nickname':'샘플','preferred_name':'박사님'},
            'purpose':{'purpose':'companion'},'preferences':dict(DEFAULTS),
            'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY_VERSION},'review':{'confirmed':True}}
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=str(Path(self.tmp.name)/'prototype.sqlite3');self.now=1000
        self.s=Service(self.path,clock=lambda:self.now)
        self.x=self.s.create(OWNER,'demo-device-01',['demo-device-01']);self.sid=self.x['session_id']
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def fill(self,actor=OWNER,kind='self',sid=None):
        sid=sid or self.sid;x=self.s.get(sid,actor)
        for step in STEPS:x=self.s.save_step(sid,actor,step,data(actor,kind)[step],x['revision'])
        return x
    def complete(self):
        x=self.fill();return self.s.complete(self.sid,OWNER,'m1',x['revision'])
    def fails(self,code,fn):
        with self.assertRaises(Error) as c:fn()
        self.assertEqual(c.exception.code,code)
    def count(self,table):return self.s.db.execute('SELECT count(*) FROM '+table).fetchone()[0]
    def test_register_apply_greeting(self):
        r=self.complete();self.assertEqual(r['apply_status'],'pending')
        self.fails('SETTINGS_NOT_APPLIED',lambda:self.s.greeting(self.sid,OWNER))
        a=self.s.apply(self.sid,OWNER);self.assertEqual(a['apply_status'],'applied');self.assertEqual(len(a['acks']),4)
        self.assertIn('박사님',self.s.greeting(self.sid,OWNER)['text']);self.assertFalse(r['hardware_connected'])
    def test_repeat_complete_three_times(self):
        x=self.fill();r=self.s.complete(self.sid,OWNER,'m1',x['revision'])
        for _ in range(3):self.assertEqual(r,self.s.complete(self.sid,OWNER,'m1',x['revision']))
        self.assertEqual(self.count('profiles'),1);self.assertEqual(self.count('applications'),1)
    def test_repeat_apply_does_not_duplicate_acks(self):
        self.complete();a=self.s.apply(self.sid,OWNER)
        self.assertEqual(a,self.s.apply(self.sid,OWNER));self.assertEqual(self.count('module_acks'),4)
    def test_retry_failed_output(self):
        self.s.outputs=SimulatedOutputs(fail_once='tts');r=self.complete();a=self.s.apply(self.sid,OWNER)
        self.assertEqual(a['apply_status'],'failed');self.assertEqual(len(a['acks']),1)
        self.assertEqual(self.count('profiles'),1);a=self.s.apply(self.sid,OWNER)
        self.assertEqual(a['apply_status'],'applied');self.assertEqual(a['attempts'],2);self.assertEqual(self.count('profiles'),1)
    def test_retry_after_restart(self):
        self.s.outputs=SimulatedOutputs(fail_once='motion');self.complete();self.s.apply(self.sid,OWNER)
        self.s.close();self.s=Service(self.path,clock=lambda:self.now)
        self.assertEqual(self.s.application(self.sid,OWNER)['apply_status'],'failed')
        self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'applied')
    def test_invalid_ack_is_failed(self):
        class Bad(SimulatedOutputs):
            def apply(self,*a):return {'ack':True,'application_id':'wrong','module':'wrong'}
        self.s.outputs=Bad();self.complete();self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'failed')
    def test_partial_setup_survives_restart(self):
        self.s.save_step(self.sid,OWNER,'registration',data()['registration'],1)
        self.s.close();self.s=Service(self.path,clock=lambda:self.now)
        self.assertEqual(self.s.get(self.sid,OWNER)['current_step'],'language')
    def test_repeat_start_resumes(self):self.assertEqual(self.s.create(OWNER,'demo-device-01',['demo-device-01'])['session_id'],self.sid)
    def test_revision_conflict(self):
        self.s.save_step(self.sid,OWNER,'registration',data()['registration'],1)
        self.fails('REVISION_CONFLICT',lambda:self.s.save_step(self.sid,OWNER,'registration',data()['registration'],1))
    def test_order_enforced(self):self.fails('PREVIOUS_STEP_REQUIRED',lambda:self.s.save_step(self.sid,OWNER,'profile',data()['profile'],1))
    def test_prior_edit_invalidates_later(self):
        x=self.fill();x=self.s.save_step(self.sid,OWNER,'profile',data()['profile'],x['revision']);self.assertNotIn('review',x['draft'])
        self.fails('INCOMPLETE_SETUP',lambda:self.s.complete(self.sid,OWNER,'m1',x['revision']))
    def test_wrong_actor_all_operations(self):
        self.complete()
        for fn in [lambda:self.s.get(self.sid,GUARDIAN),lambda:self.s.cancel(self.sid,GUARDIAN),lambda:self.s.apply(self.sid,GUARDIAN),
                   lambda:self.s.greeting(self.sid,GUARDIAN),lambda:self.s.complete(self.sid,GUARDIAN,'m1',8),
                   lambda:self.s.save_step(self.sid,GUARDIAN,'profile',data()['profile'],1)]:self.fails('NOT_FOUND',fn)
    def test_unauthorized_device(self):self.fails('DEVICE_NOT_AUTHORIZED',lambda:self.s.create(GUARDIAN,'demo-device-01',['demo-device-01']))
    def test_disconnect_blocks_start(self):
        self.s.devices.set_connected(OWNER,'demo-device-01',False)
        self.fails('DEVICE_DISCONNECTED',lambda:self.s.create(OWNER,'demo-device-01',['demo-device-01']))
    def test_disconnect_and_reconnect(self):
        self.complete();self.s.devices.set_connected(OWNER,'demo-device-01',False)
        self.fails('DEVICE_DISCONNECTED',lambda:self.s.apply(self.sid,OWNER))
        self.s.devices.set_connected(OWNER,'demo-device-01',True);self.assertEqual(self.s.apply(self.sid,OWNER)['apply_status'],'applied')
    def test_complete_requires_connection(self):
        x=self.fill();self.s.devices.set_connected(OWNER,'demo-device-01',False)
        self.fails('DEVICE_DISCONNECTED',lambda:self.s.complete(self.sid,OWNER,'m1',x['revision']));self.assertEqual(self.count('profiles'),0)
    def test_self_subject_permission(self):
        self.fails('SUBJECT_NOT_AUTHORIZED',lambda:self.s.save_step(self.sid,OWNER,'registration',{'registration_type':'self','subject_id':'other'},1))
    def test_guardian_fixture(self):
        sid=self.s.create(GUARDIAN,'demo-guardian-01',['demo-guardian-01'])['session_id'];x=self.fill(GUARDIAN,'guardian',sid)
        r=self.s.complete(sid,GUARDIAN,'g1',x['revision']);ctx=self.s.context(r['profile_id'],GUARDIAN)
        self.assertEqual(ctx['subject_id'],'demo-child-01');self.assertNotEqual(ctx['actor_id'],ctx['subject_id'])
    def test_guardian_denied_without_fixture(self):
        self.fails('GUARDIAN_NOT_AUTHORIZED',lambda:self.s.save_step(self.sid,OWNER,'registration',data(OWNER,'guardian')['registration'],1))
    def test_guest_no_profile_and_no_memory(self):
        x=self.fill(kind='guest');r=self.s.complete(self.sid,OWNER,'g1',x['revision']);self.s.apply(self.sid,OWNER)
        self.assertIsNone(r['profile_id']);self.assertEqual(self.count('profiles'),0);self.assertEqual(self.count('consent_events'),0)
        ctx=json.loads(self.s.db.execute('SELECT context FROM applications').fetchone()[0]);self.assertTrue(all(v is False for v in ctx['permissions'].values()))
    def test_guest_rejects_consent_grant(self):
        x=self.fill(kind='guest');d=data()['consent'];d['long_term_memory']=True
        self.fails('GUEST_CONSENT_FORBIDDEN',lambda:self.s.save_step(self.sid,OWNER,'consent',d,x['revision']))
    def test_guest_expiry_erases_temporary_context(self):
        x=self.fill(kind='guest');self.s.complete(self.sid,OWNER,'g1',x['revision']);self.s.apply(self.sid,OWNER);self.now+=86401
        self.fails('SESSION_EXPIRED',lambda:self.s.get(self.sid,OWNER));self.fails('SESSION_EXPIRED',lambda:self.s.greeting(self.sid,OWNER))
        self.s.purge_expired();self.assertEqual(self.count('applications'),0);self.assertEqual(self.count('module_acks'),0);self.assertEqual(self.s.get(self.sid,OWNER)['draft'],{})
    def test_false_consents_and_version_recorded(self):
        r=self.complete();ctx=self.s.context(r['profile_id'],OWNER);self.assertTrue(all(v is False for v in ctx['permissions'].values()))
        rows=self.s.db.execute('SELECT granted,policy_version FROM consent_events').fetchall();self.assertEqual(len(rows),4);self.assertTrue(all(x==(0,POLICY_VERSION) for x in rows))
    def test_policy_version_mismatch(self):
        x=self.fill();d=dict(data()['consent'],policy_version='old')
        self.fails('POLICY_VERSION_MISMATCH',lambda:self.s.save_step(self.sid,OWNER,'consent',d,x['revision']))
    def test_profile_context_owner_only(self):
        r=self.complete();self.fails('NOT_FOUND',lambda:self.s.context(r['profile_id'],GUARDIAN))
    def test_transaction_rollback(self):
        x=self.fill();self.s.db.execute("CREATE TRIGGER fail BEFORE INSERT ON applications BEGIN SELECT RAISE(ABORT,'injected'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.s.complete(self.sid,OWNER,'m1',x['revision'])
        for table in ['profiles','consent_events','applications','completions']:self.assertEqual(self.count(table),0)
        self.assertEqual(self.s.get(self.sid,OWNER)['status'],'in_progress')
    def test_cancel_and_expiry(self):
        self.fill();self.assertEqual(self.s.cancel(self.sid,OWNER)['draft'],{})
        self.fails('SESSION_NOT_ACTIVE',lambda:self.s.complete(self.sid,OWNER,'m1',8))
        x=self.s.create(OWNER,'demo-device-01',['demo-device-01']);self.now+=86401;self.s.purge_expired();self.assertEqual(self.s.get(x['session_id'],OWNER)['status'],'expired')
    def test_validation_boundaries(self):
        x=self.fill()
        for value in (True,-1,101,'20'):
            self.fails('INVALID_INPUT',lambda:self.s.save_step(self.sid,OWNER,'preferences',dict(DEFAULTS,volume=value),x['revision']))
        self.fails('INVALID_INPUT',lambda:self.s.save_step(self.sid,OWNER,'review',{'confirmed':1},x['revision']))
    def test_preview_no_physical_action(self):
        r=self.s.preview(self.sid,OWNER,DEFAULTS);self.assertFalse(r['physical_action_performed']);self.assertEqual(r['motion_preview_id'],'sim-no-motion')
    def test_guidance(self):self.assertIn('등록',self.s.guide(self.sid,OWNER,'registration')['text'])
    def test_registered_device_conflict(self):
        self.complete();self.fails('DEVICE_ALREADY_REGISTERED',lambda:self.s.create(OWNER,'demo-device-01',['demo-device-01']))
    def test_http_security_and_routes(self):
        app=Application(self.s,[{'token':'unit-token','actor_id':OWNER,'device_ids':['demo-device-01']}])
        def call(method,path,raw=b'',token='unit-token',**extra):
            status=[];env={'REQUEST_METHOD':method,'PATH_INFO':path,'HTTP_HOST':'127.0.0.1:8081',
                'HTTP_AUTHORIZATION':'Bearer '+token,'CONTENT_LENGTH':str(len(raw)),'wsgi.input':io.BytesIO(raw),**extra}
            payload=b''.join(app(env,lambda s,h:status.append(s)));return int(status[0].split()[0]),payload
        self.assertEqual(call('GET','/v1/bootstrap',token='bad')[0],401)
        self.assertEqual(call('GET','/v1/bootstrap',token='한글')[0],401)
        self.assertEqual(call('POST','/v1/onboarding/sessions',b'[]')[0],400)
        self.assertEqual(call('GET','/v1/bootstrap',HTTP_ORIGIN='http://evil.example')[0],403)
        self.assertEqual(call('GET','/v1/bootstrap',HTTP_HOST='evil.example')[0],403)
        self.assertEqual(call('GET','/')[0],200)
        self.assertEqual(call('GET','/app.js')[0],200)
        self.assertEqual(call('GET','/v1/bootstrap')[0],200)
if __name__=='__main__':unittest.main()
