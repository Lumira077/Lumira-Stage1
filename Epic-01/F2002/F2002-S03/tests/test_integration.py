import tempfile,unittest,json
from pathlib import Path
from profile_lab.adapters import SimulatedOutputs
from profile_service import Service
from profile_contract import DEFAULTS,CONSENTS,POLICY,MODULES,Error

def sample():return {'language':'ko-KR','nickname':'private','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
class Integration(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.path=str(Path(self.tmp.name)/'db');self.s=Service(self.path);self.p=self.s.create('owner',sample(),'create');self.pid=self.p['profile_id'];self.s.provision_device('d','owner');self.a=self.s.activate(self.pid,'owner','d',1)['application_id'];self.out=SimulatedOutputs()
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def test_all_five_modules(self):a=self.s.apply(self.a,'owner',self.out);self.assertEqual(a['state'],'applied');self.assertEqual(self.out.calls,list(MODULES))
    def test_repeat_apply_no_duplicate(self):self.s.apply(self.a,'owner',self.out);self.s.apply(self.a,'owner',self.out);self.assertEqual(len(self.out.calls),5);self.assertEqual(self.s.application(self.a,'owner')['attempts'],1)
    def test_failure_partial_retry(self):self.out.fail_once='tts';self.assertEqual(self.s.apply(self.a,'owner',self.out)['state'],'failed');a=self.s.apply(self.a,'owner',self.out);self.assertEqual(a['state'],'applied');self.assertEqual(self.out.calls.count('dialogue'),1);self.assertEqual(self.out.calls.count('tts'),2)
    def test_restart_retry_uses_persisted_acks(self):self.out.fail_once='expression';self.s.apply(self.a,'owner',self.out);self.s.close();self.s=Service(self.path);out=SimulatedOutputs();self.s.apply(self.a,'owner',out);self.assertEqual(out.calls,['expression','control'])
    def test_invalid_ack_not_ready(self):self.out.bad_ack=True;self.assertEqual(self.s.apply(self.a,'owner',self.out)['state'],'failed');self.assertEqual(self.s.db.execute('SELECT count(*) FROM acks').fetchone()[0],0)
    def test_revoke_blocks_old_context(self):d=self.p['data']['consent'];d['long_term_memory']=True;p=self.s.update(self.pid,'owner',{'consent':d},1,'grant');a=self.s.activate(self.pid,'owner','d',2)['application_id'];self.s.apply(a,'owner',self.out);d['long_term_memory']=False;self.s.update(self.pid,'owner',{'consent':d},2,'revoke');self.assertRaises(Error,self.s.apply,a,'owner',self.out);b=self.s.activate(self.pid,'owner','d',3)['application_id'];self.s.apply(b,'owner',self.out);self.assertFalse(self.out.settings['recognition']['permissions']['long_term_memory'])
    def test_boolean_ack_revision_rejected(self):
        class Wrong(SimulatedOutputs):
            def apply(self,*args):
                result=super().apply(*args);result['revision']=True;return result
        self.assertEqual(self.s.apply(self.a,'owner',Wrong())['state'],'failed')
    def test_simulated_caps(self):p=self.s.update(self.pid,'owner',{'preferences':{**DEFAULTS,'volume':100,'gesture_level':3,'expression_level':3}},1,'loud');a=self.s.activate(self.pid,'owner','d',2)['application_id'];self.s.apply(a,'owner',self.out);self.assertEqual(self.out.settings['tts']['volume'],40);self.assertEqual(self.out.settings['control']['gesture_level'],1)
    def test_mute_and_motion_off(self):p=self.s.update(self.pid,'owner',{'preferences':{**DEFAULTS,'volume':0,'gesture_level':0}},1,'quiet');a=self.s.activate(self.pid,'owner','d',2)['application_id'];self.s.apply(a,'owner',self.out);self.assertEqual(self.out.settings['tts']['volume'],0);self.assertEqual(self.out.settings['control']['gesture_level'],0)
    def test_disconnect_no_dispatch(self):self.s.set_device('d','owner',connected=False);self.assertRaises(Error,self.s.apply,self.a,'owner',self.out);self.assertEqual(self.out.calls,[])
    def test_delete_no_dispatch(self):self.s.delete(self.pid,'owner',1);self.assertRaises(Error,self.s.apply,self.a,'owner',self.out);self.assertEqual(self.out.calls,[])
    def test_foreign_actor_no_dispatch(self):self.assertRaises(Error,self.s.apply,self.a,'intruder',self.out);self.assertEqual(self.out.calls,[])
    def test_ack_storage_excludes_payload(self):self.s.apply(self.a,'owner',self.out);raw=json.dumps(self.s.db.execute('SELECT * FROM acks').fetchall());self.assertNotIn('private',raw);self.assertNotIn('친구',raw)
class Bridge(unittest.TestCase):
    def test_real_f2001_service_import(self):
        import sys
        from profile_service.bridge import import_onboarding
        from profile_lab.dependency import ROOT
        source=ROOT.parent.parent/'F2001/F2001-S02'
        if not source.exists():source=ROOT.parent.parent/'ker-f2001-s02'
        import hashlib
        for name,expected in json.loads((ROOT/'f2001-dependency.json').read_text())['sha256'].items():
            self.assertEqual(hashlib.sha256((source/name).read_bytes()).hexdigest(),expected)
        sys.path.insert(0,str(source))
        from ker_onboarding.service import Service as Onboarding
        from ker_onboarding.core import STEPS
        with tempfile.TemporaryDirectory() as tmp:
            on=Onboarding(str(Path(tmp)/'on.db'));s=Service(str(Path(tmp)/'profiles.db'));actor='local-demo-owner'
            try:
                x=on.create(actor,'demo-device-01',['demo-device-01']);d=sample();draft={'registration':{'registration_type':'self','subject_id':actor},'language':{'language':d['language']},'profile':{'nickname':d['nickname'],'preferred_name':d['preferred_name']},'purpose':{'purpose':d['purpose']},'preferences':d['preferences'],'consent':d['consent'],'review':{'confirmed':True}}
                for step in STEPS:x=on.save_step(x['session_id'],actor,step,draft[step],x['revision'])
                on.complete(x['session_id'],actor,'complete',x['revision']);p=import_onboarding(s,on,x['session_id'],actor);self.assertEqual(p['data'],d)
                self.assertEqual(import_onboarding(s,on,x['session_id'],actor),p)
                with self.assertRaises(Exception) as caught:import_onboarding(s,on,x['session_id'],'intruder')
                self.assertEqual(caught.exception.code,'NOT_FOUND')
                s.delete(p['profile_id'],actor,1);self.assertRaises(Error,import_onboarding,s,on,x['session_id'],actor)
            finally:on.close();s.close()
