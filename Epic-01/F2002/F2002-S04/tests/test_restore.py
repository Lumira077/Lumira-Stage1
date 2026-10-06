import unittest,tempfile,json,sqlite3
from pathlib import Path
from profile_ops.restore import RestoreLab
from profile_service import Service
from profile_contract import DEFAULTS,CONSENTS,POLICY,Error
class Restore(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'.ker-development-sandbox').write_text('development')
        self.s=Service(str(self.root/'current.sqlite3'));d={'language':'ko-KR','nickname':'synthetic','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),'consent':{**{k:True for k in CONSENTS},'policy_version':POLICY}};self.p=self.s.create('owner',d,'create');self.s.provision_device('d','owner');self.s.activate(self.p['profile_id'],'owner','d',1);self.lab=RestoreLab(self.root);self.lab.backup()
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def ledger(self,op=None): (self.root/'privacy-ledger.json').write_text(json.dumps([] if op is None else [{'seq':1,'profile_id':self.p['profile_id'],'operation':op,'purpose':'long_term_memory' if op=='revoke' else None}]))
    def test_preserve_profiles_clear_activation(self):self.ledger();self.lab.restore();s=Service(str(self.root/'restored.sqlite3'));self.assertEqual(s.get(self.p['profile_id'],'owner')['data'],self.p['data']);self.assertIsNone(s.device('d','owner')['active_profile']);s.close()
    def test_newer_deletion_not_resurrected(self):self.ledger('delete');self.lab.restore();s=Service(str(self.root/'restored.sqlite3'));self.assertEqual(s.list('owner'),[]);s.close()
    def test_newer_revocation_not_resurrected(self):self.ledger('revoke');r=self.lab.restore();s=Service(str(self.root/'restored.sqlite3'));self.assertFalse(s.get(self.p['profile_id'],'owner')['data']['consent']['long_term_memory']);self.assertFalse(r['production_restore_verified']);s.close()
    def test_missing_ledger_blocks(self):self.assertRaises(Error,self.lab.restore)
    def test_schema_mismatch_blocks(self):self.ledger();db=sqlite3.connect(self.root/'snapshot.sqlite3');db.execute('UPDATE schema_metadata SET version=2');db.commit();db.close();self.assertRaises(Error,self.lab.restore)
    def test_symlink_destination_blocks(self):self.ledger();(self.root/'restored.sqlite3').symlink_to(self.root/'current.sqlite3');self.assertRaises(Error,self.lab.restore)
