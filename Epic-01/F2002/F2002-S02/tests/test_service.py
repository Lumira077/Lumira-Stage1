import tempfile,unittest,json,threading,urllib.request,urllib.error,copy,sys
from pathlib import Path
from profile_service import Service
from profile_contract import Error,DEFAULTS,CONSENTS,POLICY

def sample():return {'language':'ko-KR','nickname':'private','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
class Storage(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.path=str(Path(self.tmp.name)/'profiles.db');self.s=Service(self.path);self.p=self.s.create('owner',sample(),'create');self.pid=self.p['profile_id'];self.s.provision_device('device','owner')
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def test_create_idempotent(self):self.assertEqual(self.s.create('owner',sample(),'create'),self.p);self.assertEqual(len(self.s.list('owner')),1)
    def test_conflicting_create_key(self):d=sample();d['nickname']='other';self.assertRaises(Error,self.s.create,'owner',d,'create')
    def test_foreign_profile_hidden(self):self.assertRaises(Error,self.s.get,self.pid,'intruder');self.assertEqual(self.s.list('intruder'),[])
    def test_guardian_requires_authority(self):self.assertRaises(Error,self.s.create,'owner',sample(),'child',subject='child')
    def test_guardian_trusted_subject(self):p=self.s.create('owner',sample(),'child',subject='child',authorized_subjects=['child']);self.assertEqual(p['subject_id'],'child')
    def test_update_and_idempotency(self):p=self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit');self.assertEqual(p['revision'],2);self.assertEqual(self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit'),p)
    def test_revision_conflict(self):self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit');self.assertRaises(Error,self.s.update,self.pid,'owner',{'purpose':'home'},1,'other');self.assertEqual(self.s.get(self.pid,'owner')['data']['purpose'],'companion')
    def test_old_key_never_returns_old_data(self):self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit');self.assertRaises(Error,self.s.create,'owner',sample(),'create')
    def test_two_connections_conflict(self):other=Service(self.path);p=other.get(self.pid,'owner');self.s.update(self.pid,'owner',{'nickname':'new'},1,'first');self.assertRaises(Error,other.update,self.pid,'owner',{'purpose':'home'},p['revision'],'second');other.close()
    def test_reopen_persists(self):self.s.close();self.s=Service(self.path);self.assertEqual(self.s.get(self.pid,'owner'),self.p)
    def test_reset_keeps_consent(self):d=self.p['data']['consent'];d['long_term_memory']=True;p=self.s.update(self.pid,'owner',{'consent':d,'preferences':{**DEFAULTS,'volume':0}},1,'edit');p=self.s.reset(self.pid,'owner',p['revision'],'reset');self.assertEqual(p['data']['preferences'],DEFAULTS);self.assertTrue(p['data']['consent']['long_term_memory'])
    def test_update_invalidates_activation(self):a=self.s.activate(self.pid,'owner','device',1);self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit');self.assertRaises(Error,self.s.current_context,a['application_id'],'owner')
    def test_switch_invalidates_old_activation(self):a=self.s.activate(self.pid,'owner','device',1);p2=self.s.create('owner',sample(),'second');self.s.activate(p2['profile_id'],'owner','device',1);self.assertRaises(Error,self.s.current_context,a['application_id'],'owner')
    def test_device_other_owner(self):self.s.provision_device('other','intruder');self.assertRaises(Error,self.s.activate,self.pid,'owner','other',1)
    def test_device_disconnected(self):self.s.set_device('device','owner',connected=False);self.assertRaises(Error,self.s.activate,self.pid,'owner','device',1)
    def test_stop_invalidates_pending(self):a=self.s.activate(self.pid,'owner','device',1);self.s.set_device('device','owner',stopped=True);self.assertRaises(Error,self.s.current_context,a['application_id'],'owner')
    def test_delete_clears_data_operations_bindings(self):a=self.s.activate(self.pid,'owner','device',1);self.s.delete(self.pid,'owner',1);self.assertEqual(self.s.list('owner'),[]);self.assertEqual(self.s.db.execute('SELECT count(*) FROM mutations').fetchone()[0],0);self.assertIsNone(self.s.device('device','owner')['active_profile']);self.assertRaises(Error,self.s.application,a['application_id'],'owner')
    def test_delete_conflict_preserves_profile(self):self.assertRaises(Error,self.s.delete,self.pid,'owner',2);self.assertEqual(self.s.get(self.pid,'owner'),self.p)
    def test_logs_no_user_data(self):self.s.update(self.pid,'owner',{'preferred_name':'private-name'},1,'edit');events=self.s.db.execute('SELECT * FROM events').fetchall();self.assertNotIn('private',json.dumps(events));self.assertNotIn(self.pid,json.dumps(events))
    def test_key_reuse_other_profile_rejected(self):p2=self.s.create('owner',sample(),'second');self.s.update(self.pid,'owner',{'nickname':'new'},1,'edit');self.assertRaises(Error,self.s.update,p2['profile_id'],'owner',{'nickname':'new'},1,'edit')
    def test_bool_revision_rejected(self):self.assertRaises(Error,self.s.update,self.pid,'owner',{'nickname':'new'},True,'edit')
class HTTP(unittest.TestCase):
    def test_authenticated_real_http_cycle(self):
        from profile_service.api import server
        # SQLite service constructed in HTTP thread; this exercises actual socket routing.
        tmp=tempfile.TemporaryDirectory();ready=threading.Event();shared={};token='x'*40
        def run():
            s=Service(str(Path(tmp.name)/'api.db'));h=server(s,token,port=0);shared['http']=h;shared['port']=h.server_port;ready.set();h.serve_forever();h.server_close();s.close()
        thread=threading.Thread(target=run);thread.start();ready.wait(5)
        def req(method,path,data=None,auth=True):
            r=urllib.request.Request('http://127.0.0.1:'+str(shared['port'])+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+token} if auth else {})})
            with urllib.request.urlopen(r,timeout=5) as response:return json.load(response)
        try:
            with self.assertRaises(urllib.error.HTTPError) as e:req('GET','/profiles',auth=False)
            self.assertEqual(e.exception.code,401)
            p=req('POST','/profiles',{'data':sample(),'mutation_id':'create'});pid=p['profile_id']
            p=req('PATCH','/profiles/'+pid,{'changes':{'preferred_name':'Hello'},'revision':1,'mutation_id':'edit'});self.assertEqual(p['revision'],2)
            self.assertEqual(req('GET','/profiles/'+pid)['data']['preferred_name'],'Hello');self.assertTrue(req('DELETE','/profiles/'+pid,{'revision':2})['deleted']);self.assertEqual(req('GET','/profiles'),[])
        finally:shared['http'].shutdown();thread.join(5);tmp.cleanup()
