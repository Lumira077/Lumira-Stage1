import io
import json
import tempfile
import unittest
from pathlib import Path
from ker_onboarding.service import Service, Error, STEPS, DEFAULTS, CONSENTS
from ker_onboarding.api import Application

DATA = {'language':{'language':'ko-KR'}, 'profile':{'nickname':'테스트','preferred_name':'박사님'},
        'purpose':{'purpose':'companion'}, 'preferences':dict(DEFAULTS),
        'consent':{k:False for k in CONSENTS}, 'review':{'confirmed':True}}

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name)/'test.sqlite3')
        self.now = 1000
        self.s = Service(self.path, lambda:self.now)
        self.x = self.s.create('owner','device',['device'])
        self.sid = self.x['session_id']
    def tearDown(self):
        self.s.close(); self.tmp.cleanup()
    def fill(self):
        x=self.s.get(self.sid,'owner')
        for step in STEPS:
            x=self.s.save_step(self.sid,'owner',step,DATA[step],x['revision'])
        return x
    def fails(self,code,fn):
        with self.assertRaises(Error) as caught: fn()
        self.assertEqual(caught.exception.code,code)
    def test_complete_and_false_consents(self):
        x=self.fill(); r=self.s.complete(self.sid,'owner','m1',x['revision'])
        self.assertEqual(r['apply_status'],'pending');self.assertFalse(r['hardware_connected'])
        data=json.loads(self.s.db.execute('SELECT data FROM profiles').fetchone()[0])
        self.assertTrue(all(v is False for v in data['consent'].values()))
    def test_idempotent_complete(self):
        x=self.fill();a=self.s.complete(self.sid,'owner','m1',x['revision'])
        for _ in range(3):self.assertEqual(a,self.s.complete(self.sid,'owner','m1',x['revision']))
        self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],1)
    def test_different_mutation_conflicts(self):
        x=self.fill();self.s.complete(self.sid,'owner','m1',x['revision'])
        self.fails('ALREADY_COMPLETED',lambda:self.s.complete(self.sid,'owner','m2',x['revision']))
    def test_resume_after_reopen(self):
        x=self.s.save_step(self.sid,'owner','language',DATA['language'],1)
        self.s.close();self.s=Service(self.path,lambda:self.now)
        self.assertEqual(self.s.get(self.sid,'owner')['draft'],x['draft'])
    def test_repeat_create_resumes(self):
        self.assertEqual(self.s.create('owner','device',['device'])['session_id'],self.sid)
    def test_wrong_actor_hidden(self):
        self.fails('NOT_FOUND',lambda:self.s.get(self.sid,'other'))
        self.fails('NOT_FOUND',lambda:self.s.cancel(self.sid,'other'))
    def test_device_scope(self):
        self.fails('DEVICE_NOT_AUTHORIZED',lambda:self.s.create('other','device',[]))
    def test_revision_conflict(self):
        self.s.save_step(self.sid,'owner','language',DATA['language'],1)
        self.fails('REVISION_CONFLICT',lambda:self.s.save_step(self.sid,'owner','language',DATA['language'],1))
    def test_order(self):
        self.fails('PREVIOUS_STEP_REQUIRED',lambda:self.s.save_step(self.sid,'owner','profile',DATA['profile'],1))
    def test_edit_invalidates_review(self):
        x=self.fill();x=self.s.save_step(self.sid,'owner','profile',DATA['profile'],x['revision'])
        self.assertNotIn('review',x['draft'])
        self.fails('INCOMPLETE_SETUP',lambda:self.s.complete(self.sid,'owner','m1',x['revision']))
    def test_invalid_preferences(self):
        x=self.fill()
        for value in (True,101,-1,'20'):
            bad=dict(DEFAULTS,volume=value)
            self.fails('INVALID_INPUT',lambda:self.s.save_step(self.sid,'owner','preferences',bad,x['revision']))
    def test_unknown_fields(self):
        self.fails('INVALID_INPUT',lambda:self.s.save_step(self.sid,'owner','language',{'language':'ko-KR','token':'x'},1))
    def test_expiry_and_cleanup(self):
        self.s.save_step(self.sid,'owner','language',DATA['language'],1)
        self.now+=86401
        self.fails('SESSION_EXPIRED',lambda:self.s.get(self.sid,'owner'))
        self.assertEqual(self.s.purge_expired(),1)
        self.assertEqual(self.s.get(self.sid,'owner')['draft'],{})
    def test_cancel_clears_draft(self):
        self.fill();x=self.s.cancel(self.sid,'owner');self.assertEqual(x['draft'],{})
        self.fails('SESSION_NOT_ACTIVE',lambda:self.s.complete(self.sid,'owner','m1',x['revision']))
    def test_registered_device_conflict(self):
        x=self.fill();self.s.complete(self.sid,'owner','m1',x['revision'])
        self.fails('DEVICE_ALREADY_REGISTERED',lambda:self.s.create('owner','device',['device']))
    def test_transaction_rollback(self):
        x=self.fill()
        self.s.db.execute("CREATE TRIGGER fail_insert BEFORE INSERT ON completions BEGIN SELECT RAISE(ABORT,'injected'); END")
        with self.assertRaises(Exception):self.s.complete(self.sid,'owner','m1',x['revision'])
        self.assertEqual(self.s.db.execute('SELECT count(*) FROM profiles').fetchone()[0],0)
        self.assertEqual(self.s.get(self.sid,'owner')['status'],'in_progress')
    def test_http_auth_and_json(self):
        app=Application(self.s,[{'token':'secret-test-token','actor_id':'owner','device_ids':['device']}])
        def call(token,raw):
            response=[]
            env={'REQUEST_METHOD':'POST','PATH_INFO':'/v1/onboarding/sessions',
                 'HTTP_AUTHORIZATION':token,'CONTENT_LENGTH':str(len(raw)),'wsgi.input':io.BytesIO(raw)}
            result=b''.join(app(env,lambda status,headers:response.append(status)))
            return response[0],json.loads(result)
        self.assertTrue(call('',b'{}')[0].startswith('401'))
        self.assertTrue(call('Bearer 한글',b'{}')[0].startswith('401'))
        self.assertEqual(call('Bearer secret-test-token',b'{bad')[1]['error_code'],'INVALID_JSON')
        self.assertTrue(call('Bearer secret-test-token',b'[]')[0].startswith('400'))
    def test_review_requires_boolean(self):
        x=self.fill()
        self.fails('INVALID_INPUT',lambda:self.s.save_step(self.sid,'owner','review',{'confirmed':1},x['revision']))
    def test_unknown_step(self):
        self.fails('UNKNOWN_STEP',lambda:self.s.save_step(self.sid,'owner','bogus',{},1))

if __name__=='__main__':unittest.main()
