import unittest,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from ledger_sqlite import SQLiteUsageLedger

class DurableLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'usage.db'
        self.ledger=SQLiteUsageLedger(self.path,10)
    def tearDown(self):self.ledger.close();self.tmp.cleanup()
    def test_restart_retains_charge(self):
        self.ledger.charge('a',3)
        other=SQLiteUsageLedger(self.path,10)
        try:self.assertEqual(other.charge('a',3),3)
        finally:other.close()
    def test_refund_tombstone_survives_restart(self):
        self.ledger.charge('a',3);self.ledger.refund('a')
        other=SQLiteUsageLedger(self.path,10)
        try:self.assertEqual(other.charge('a',3),0);self.assertEqual(other.refund('a'),0)
        finally:other.close()
    def test_conflict_rolls_back(self):
        self.ledger.charge('a',3)
        with self.assertRaises(ValueError):self.ledger.charge('a',4)
        self.assertEqual(self.ledger.charge('b',2),5)
    def test_overquota_does_not_consume_id(self):
        self.ledger.charge('a',8)
        with self.assertRaises(ValueError):self.ledger.charge('b',3)
        self.ledger.refund('a');self.assertEqual(self.ledger.charge('b',3),3)
    def test_quota_reopen_mismatch(self):
        with self.assertRaises(ValueError):SQLiteUsageLedger(self.path,11)
        self.assertEqual(self.ledger.charge('a',1),1)
    def test_unknown_refund(self):
        with self.assertRaises(ValueError):self.ledger.refund('missing')
        self.assertEqual(self.ledger.used,0)
    def test_invalid_units(self):
        for units in (True,0,-1,1.5):
            with self.assertRaises(ValueError):self.ledger.charge('a',units)
    def test_concurrent_quota(self):
        def charge(i):
            ledger=SQLiteUsageLedger(self.path,10)
            try:
                try:ledger.charge(str(i),3);return True
                except ValueError:return False
            finally:ledger.close()
        with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(charge,range(8)))
        self.assertEqual(sum(results),3);self.assertEqual(self.ledger.used,9)
