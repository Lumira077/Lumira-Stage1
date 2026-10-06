import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

class ResetTests(unittest.TestCase):
    def execute(self,confirmed,development,symlink=False):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'scripts').mkdir();(root/'data').mkdir()
            script=root/'scripts/reset_dev.py'
            script.write_text((Path(__file__).resolve().parent.parent/'scripts/reset_dev.py').read_text())
            unrelated=root/'data/keep.sqlite3';unrelated.write_text('preserve')
            db=root/'data/prototype.sqlite3'
            if symlink:db.symlink_to(unrelated)
            else:db.write_text('development fixture')
            env=dict(os.environ,KER_ENV='development' if development else 'production')
            args=[sys.executable,str(script)]+(['--confirm-prototype-reset'] if confirmed else [])
            r=subprocess.run(args,env=env,capture_output=True,text=True)
            return r.returncode,db.exists(),unrelated.read_text()
    def test_reset_requires_development(self):
        code,exists,other=self.execute(True,False);self.assertNotEqual(code,0);self.assertTrue(exists)
    def test_reset_requires_confirmation(self):
        code,exists,other=self.execute(False,True);self.assertNotEqual(code,0);self.assertTrue(exists)
    def test_reset_only_known_database(self):
        code,exists,other=self.execute(True,True);self.assertEqual(code,0);self.assertFalse(exists);self.assertEqual(other,'preserve')
    @unittest.skipIf(os.name=='nt','Windows symlink privilege varies')
    def test_reset_refuses_symlink(self):
        code,exists,other=self.execute(True,True,True);self.assertNotEqual(code,0);self.assertEqual(other,'preserve')
