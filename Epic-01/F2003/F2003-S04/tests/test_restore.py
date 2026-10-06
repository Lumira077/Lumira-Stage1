import tempfile,unittest,json,sqlite3
from pathlib import Path
from memory_ops.restore import RestoreLab
from memory_service.fixtures import setup,candidate
from memory_service import Service
from memory_contract import Error
class Restore(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.now=1000;(self.root/'.ker-development-sandbox').write_text('synthetic only')
        self.p,self.s,self.pid=setup(self.root,clock=lambda:self.now);r=self.s.create('demo-owner',self.pid,'demo-device',candidate(),'create');self.r=self.s.confirm('demo-owner',self.pid,'demo-device',r['memory_id'],1,'confirm');self.s.prepare('demo-owner',self.pid,'demo-device','산책');self.lab=RestoreLab(self.root,clock=lambda:self.now);self.lab.backup()
    def tearDown(self):self.s.close();self.p.close();self.tmp.cleanup()
    def restored(self):return Service(str(self.root/'restored.sqlite3'),self.s.policy,clock=lambda:self.now)
    def test_preserves_valid_memory_not_ticket(self):self.lab.export_latest_ledger();self.lab.restore();s=self.restored();self.assertTrue(s.search('demo-owner',self.pid,'demo-device','산책'));self.assertEqual(s.db.execute('SELECT count(*) FROM tickets').fetchone()[0],0);s.close()
    def test_newer_deletion_not_resurrected(self):self.s.delete('demo-owner',self.pid,self.r['memory_id'],2);self.lab.export_latest_ledger();self.lab.restore();s=self.restored();self.assertEqual(s.search('demo-owner',self.pid,'demo-device','산책'),[]);s.close()
    def test_newer_revoke_blocks_stale_true_profile(self):self.s.revoke('demo-owner',self.pid);self.lab.export_latest_ledger();self.lab.restore();p=self.p.get(self.pid,'demo-owner');d=p['data']['consent'];d['long_term_memory']=True;self.p.update(self.pid,'demo-owner',{'consent':d},p['revision'],'unnotified-grant');s=self.restored();self.assertRaises(Error,s.search,'demo-owner',self.pid,'demo-device','산책');self.assertEqual(s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0);s.close()
    def test_restore_preserves_retired_request_barrier(self):
        self.s.delete('demo-owner',self.pid,self.r['memory_id'],2);self.lab.export_latest_ledger();self.lab.restore();s=self.restored();self.assertRaises(Error,s.create,'demo-owner',self.pid,'demo-device',candidate(),'create');s.close()
    def test_newer_correction_does_not_revive_old_content(self):
        self.s.correct('demo-owner',self.pid,'demo-device',self.r['memory_id'],'음악',2,'correct');self.lab.export_latest_ledger();self.lab.restore();s=self.restored();self.assertEqual(s.search('demo-owner',self.pid,'demo-device','산책'),[]);self.assertRaises(Error,s.create,'demo-owner',self.pid,'demo-device',candidate(),'create');s.close()
    def test_missing_latest_ledger_blocks(self):self.assertRaises(Error,self.lab.restore)
    def test_invalid_sequence(self):self.lab.export_latest_ledger();r=json.loads((self.root/'privacy-ledger.json').read_text());r.append({'seq':7,'operation':'revoke','profile_id':self.pid,'memory_id':None,'stamp':1000});(self.root/'privacy-ledger.json').write_text(json.dumps(r));self.assertRaises(Error,self.lab.restore)
    def test_symlink_output(self):self.lab.export_latest_ledger();(self.root/'restored.sqlite3').symlink_to(self.root/'current.sqlite3');self.assertRaises(Error,self.lab.restore)
    def test_schema_incompatible(self):self.lab.export_latest_ledger();db=sqlite3.connect(self.root/'snapshot.sqlite3');db.execute('UPDATE schema_metadata SET version=2');db.commit();db.close();self.assertRaises(Error,self.lab.restore)
    def test_expired_memory_not_restored(self):self.now+=2592001;self.lab.export_latest_ledger();self.lab.restore();s=self.restored();self.assertEqual(s.db.execute('SELECT count(*) FROM memories').fetchone()[0],0);s.close()
    def test_ledger_anchor_missing_prefix(self):self.s.delete_all('demo-owner',self.pid);self.lab.backup();(self.root/'privacy-ledger.json').write_text('[]');self.assertRaises(Error,self.lab.restore)
    def test_repeated_restore_is_safe(self):self.s.delete_all('demo-owner',self.pid);self.lab.export_latest_ledger();a=self.lab.restore();b=self.lab.restore();self.assertEqual(a,b);self.assertFalse(a['production_restore_verified'])
