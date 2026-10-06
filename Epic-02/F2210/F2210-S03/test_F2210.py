import unittest
from core import *

class TestF2210(unittest.TestCase):
    def setUp(self):
        self.now=10;self.s=NetworkMonitor(lambda:self.now)

    def test_three_recoveries(self):
        self.s.observe(100,.01,512,8);self.s.observe(100,.01,512,9);self.assertEqual(self.s.observe(100,.01,512,10)["route"],"cloud")

    def test_poor_network(self):
        self.assertEqual(self.s.observe(500,.01,512,10)["route"],"local")

    def test_stale(self):
        self.assertEqual(self.s.observe(100,.01,512,1)["route"],"local")

    def test_future(self):
        self.assertRaises(Rejected,self.s.observe,100,.01,512,11)

    def test_nan(self):
        self.assertRaises(Rejected,self.s.observe,float("nan"),.01,512,10)

    def test_reset_recovery(self):
        self.s.observe(100,.01,512,9);self.s.observe(100,.2,512,10);self.assertEqual(self.s.recovery,0)

    def test_duplicate_sample(self):
        self.s.observe(100,.01,512,10);self.assertRaises(Rejected,self.s.observe,100,.01,512,10)
