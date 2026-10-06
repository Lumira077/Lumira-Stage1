import unittest
from core import *

class TestF2209(unittest.TestCase):
    def setUp(self):
        self.s=Budget(10)

    def test_reservation(self):
        self.s.reserve("r",7);self.assertEqual(self.s.available,3)

    def test_idempotent(self):
        self.s.reserve("r",7);self.s.reserve("r",7);self.assertEqual(self.s.available,3)

    def test_conflict(self):
        self.s.reserve("r",7);self.assertRaises(Rejected,self.s.reserve,"r",6)

    def test_overspend(self):
        self.s.reserve("r",7);self.assertRaises(Rejected,self.s.reserve,"s",4)

    def test_settle(self):
        self.s.reserve("r",7);self.s.settle("r",4);self.s.settle("r",4);self.assertEqual(self.s.available,6)

    def test_usage_above_reserved(self):
        self.s.reserve("r",7);self.assertRaises(Rejected,self.s.settle,"r",8);self.assertEqual(self.s.available,3)

    def test_cancel_once(self):
        self.s.reserve("r",7);self.s.cancel("r");self.s.cancel("r");self.assertEqual(self.s.available,10)

    def test_concurrent_budget(self):
        import concurrent.futures
        def reserve(k):
         try:self.s.reserve(k,7);return True
         except Rejected:return False
        with concurrent.futures.ThreadPoolExecutor(2) as pool:result=list(pool.map(reserve,["a","b"]))
        self.assertEqual(sum(result),1);self.assertEqual(self.s.available,3)
