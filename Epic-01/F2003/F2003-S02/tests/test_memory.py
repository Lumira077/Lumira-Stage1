import tempfile,unittest,json,sqlite3,threading,urllib.request,urllib.error
from pathlib import Path
from memory_service.fixtures import setup,candidate
from memory_service import Service
from memory_contract import Error
class Memory(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.now=1000;self.p,self.s,self.pid=setup(self.root,clock=lambda:self.now)
    def tearDown(self):self.s.close();self.p.close();self.tmp.cleanup()
    def create(self,content='산책',key='create'):return self.s.create('demo-owner',self.pid,'demo-device',candidate(content),key)
    def confirmed(self):r=self.create();return self.s.confirm('demo-owner',self.pid,'demo-device',r['memory_id'],r['revision'],'confirm')
    def test_candidate_not_searchable(self):self.create();self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책'),[])
    def test_confirm_and_search(self):r=self.confirmed();self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책')[0]['memory_id'],r['memory_id'])
    def test_create_idempotency(self):r=self.create();self.assertEqual(self.create(),r);self.assertEqual(len(self.s.list('demo-owner',self.pid,'demo-device')),1)
    def test_conflicting_key(self):self.create();self.assertRaises(Error,self.create,'음악','create')
    def test_semantic_exact_duplicate(self):a=self.create('Jazz');b=self.create(' jazz ','different');self.assertEqual(a['memory_id'],b['memory_id'])
    def test_revision_conflict(self):r=self.confirmed();self.assertRaises(Error,self.s.correct,'demo-owner',self.pid,'demo-device',r['memory_id'],'음악',1,'correct');self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책')[0]['content'],'산책')
    def test_correction_replaces_index(self):r=self.confirmed();n=self.s.correct('demo-owner',self.pid,'demo-device',r['memory_id'],'음악',r['revision'],'correct');self.assertEqual(n['revision'],3);self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책'),[]);self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','음악')[0]['content'],'음악')
    def test_confirmation_idempotent(self):r=self.create();a=self.s.confirm('demo-owner',self.pid,'demo-device',r['memory_id'],1,'confirm');self.assertEqual(self.s.confirm('demo-owner',self.pid,'demo-device',r['memory_id'],1,'confirm'),a)
    def test_old_create_key_not_old_content(self):self.confirmed();self.assertRaises(Error,self.create)
    def test_conflicting_slot_superseded(self):self.confirmed();r=self.create('음악','new');self.s.confirm('demo-owner',self.pid,'demo-device',r['memory_id'],1,'confirm-new');self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책'),[]);self.assertEqual(self.s.db.execute("SELECT content FROM memories WHERE state='superseded'").fetchone()[0],'')
    def test_foreign_owner_cannot_read_or_purge(self):self.confirmed();self.assertRaises(Error,self.s.search,'intruder',self.pid,'demo-device','산책');self.assertEqual(self.s.db.execute('SELECT count(*) FROM memories').fetchone()[0],1)
    def test_profile_switch_blocks(self):self.confirmed();d=self.p.get(self.pid,'demo-owner')['data'];q=self.p.create('demo-owner',d,'second');self.p.activate(q['profile_id'],'demo-owner','demo-device',1);self.assertRaises(Error,self.s.search,'demo-owner',self.pid,'demo-device','산책');self.assertEqual(self.s.search('demo-owner',q['profile_id'],'demo-device','산책'),[])
    def test_consent_revoke_purges(self):self.confirmed();self.s.revoke('demo-owner',self.pid);self.assertEqual(self.s.db.execute('SELECT count(*) FROM search_index').fetchone()[0],0);self.assertRaises(Error,self.create)
    def test_external_revoke_detected(self):self.confirmed();p=self.p.get(self.pid,'demo-owner');d=p['data']['consent'];d['long_term_memory']=False;self.p.update(self.pid,'demo-owner',{'consent':d},p['revision'],'revoke');self.assertRaises(Error,self.s.synchronize,'demo-owner',self.pid);self.assertEqual(self.s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0)
    def test_regrant_never_restores_old_memories(self):self.confirmed();self.s.revoke('demo-owner',self.pid);self.s.grant('demo-owner',self.pid);self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책'),[])
    def test_revoke_profile_update_failure_stays_blocked(self):self.confirmed();original=self.p.update;self.p.update=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('fixture failure'));self.assertRaises(RuntimeError,self.s.revoke,'demo-owner',self.pid);self.p.update=original;self.assertRaises(Error,self.create)
    def test_profile_deleted_purges_known_owner(self):self.confirmed();self.p.delete(self.pid,'demo-owner',1);self.assertRaises(Error,self.s.search,'demo-owner',self.pid,'demo-device','산책');self.assertEqual(self.s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0)
    def test_delete_after_revoke_allowed(self):r=self.confirmed();p=self.p.get(self.pid,'demo-owner');d=p['data']['consent'];d['long_term_memory']=False;self.p.update(self.pid,'demo-owner',{'consent':d},1,'revoke');self.s.delete('demo-owner',self.pid,r['memory_id'],2);self.assertEqual(self.s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0)
    def test_delete_cleans_index_and_requests(self):r=self.confirmed();self.s.delete('demo-owner',self.pid,r['memory_id'],2);self.assertEqual(self.s.db.execute('SELECT count(*) FROM search_index').fetchone()[0],0);self.assertEqual(self.s.db.execute('SELECT count(*) FROM mutations').fetchone()[0],0)
    def test_deleted_request_replay_cannot_recreate_memory(self):
        r=self.confirmed();self.s.delete('demo-owner',self.pid,r['memory_id'],2);self.assertRaises(Error,self.create);self.assertEqual(self.s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0)
    def test_regrant_old_request_replay_blocked(self):
        self.confirmed();self.s.revoke('demo-owner',self.pid);self.s.grant('demo-owner',self.pid);self.assertRaises(Error,self.create);self.create('음악','fresh-request')
    def test_expiry(self):self.confirmed();self.now+=2592001;self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책'),[]);self.assertEqual(self.s.db.execute('SELECT count(*) FROM search_index').fetchone()[0],0)
    def test_candidate_shorter_retention(self):r=self.create();self.assertEqual(r['expires_at'],self.now+604800)
    def test_restart_persists(self):r=self.confirmed();self.s.close();self.s=Service(str(self.root/'current.sqlite3'),self.s.policy,clock=lambda:self.now);self.assertEqual(self.s.search('demo-owner',self.pid,'demo-device','산책')[0]['memory_id'],r['memory_id'])
    def test_logs_no_content_identity(self):r=self.confirmed();self.s.search('demo-owner',self.pid,'demo-device','산책');raw=json.dumps(self.s.db.execute('SELECT * FROM events').fetchall(),ensure_ascii=False);self.assertNotIn('산책',raw);self.assertNotIn(self.pid,raw);self.assertNotIn('demo-owner',raw)
    def test_sync_consent_and_disconnected_adapter(self):self.assertRaises(Error,self.s.sync_status,'demo-owner',self.pid);p=self.p.get(self.pid,'demo-owner');d=p['data']['consent'];d['cloud_transfer']=True;self.p.update(self.pid,'demo-owner',{'consent':d},1,'cloud');r=self.s.sync_status('demo-owner',self.pid);self.assertFalse(r['payload_exported'])
    def test_offline_local_read(self):self.confirmed();self.p.set_device('demo-device','demo-owner',connected=False);self.assertTrue(self.s.search('demo-owner',self.pid,'demo-device','산책'))
    def test_search_limit_bounds(self):self.assertRaises(Error,self.s.search,'demo-owner',self.pid,'demo-device','산책',True)
    def test_guest_or_unknown_profile_rejected(self):self.assertRaises(Error,self.s.search,'demo-owner','a'*32,'demo-device','산책')
    def test_index_failure_rolls_back_confirmation(self):r=self.create();self.s.db.execute("CREATE TRIGGER fail_index BEFORE INSERT ON search_index BEGIN SELECT RAISE(ABORT,'fixture'); END;");self.assertRaises(sqlite3.DatabaseError,self.s.confirm,'demo-owner',self.pid,'demo-device',r['memory_id'],1,'confirm');self.assertEqual(self.s.get('demo-owner',self.pid,'demo-device',r['memory_id'])['state'],'candidate')
class HTTP(unittest.TestCase):
    def test_real_http_authenticated_cycle(self):
        from memory_service.api import server
        tmp=tempfile.TemporaryDirectory();ready=threading.Event();shared={};token='x'*40
        def run():
            p,s,pid=setup(tmp.name);h=server(s,token,'demo-owner',pid,'demo-device');shared['http']=h;shared['port']=h.server_port;ready.set();h.serve_forever();h.server_close();s.close();p.close()
        thread=threading.Thread(target=run);thread.start();ready.wait(5)
        def req(method,path,data=None,auth=True):
            r=urllib.request.Request('http://127.0.0.1:'+str(shared['port'])+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Content-Type':'application/json',**({'Authorization':'Bearer '+token} if auth else {})})
            with urllib.request.urlopen(r,timeout=5) as response:return json.load(response)
        try:
            with self.assertRaises(urllib.error.HTTPError) as e:req('GET','/memories',auth=False)
            self.assertEqual(e.exception.code,401)
            r=req('POST','/memories',{'data':candidate(),'mutation_id':'create'});mid=r['memory_id'];self.assertEqual(req('POST','/search',{'query':'산책'}),[])
            self.assertEqual(req('GET','/memories/'+mid)['state'],'candidate')
            r=req('POST','/memories/'+mid+'/confirm',{'revision':1,'mutation_id':'confirm'});self.assertTrue(req('POST','/search',{'query':'산책'}))
            r=req('PATCH','/memories/'+mid,{'content':'음악','revision':2,'mutation_id':'correct'});self.assertEqual(r['revision'],3)
            req('DELETE','/memories/'+mid,{'revision':3});self.assertEqual(req('GET','/memories'),[])
        finally:shared['http'].shutdown();thread.join(5);tmp.cleanup()
