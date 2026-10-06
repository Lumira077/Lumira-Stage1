import unittest
from core import *

class TestF2011(unittest.TestCase):
    def setUp(self):
        self.now=10;self.s=ConversationSession(lambda:self.now);self.e=self.s.open("a")

    def test_append(self):
        self.s.append("a",self.e,"t","hello");self.assertEqual(self.s.history,["hello"])

    def test_foreign(self):
        self.assertRaises(Rejected,self.s.check,"b",self.e)

    def test_switch(self):
        self.s.open("b");self.assertRaises(Rejected,self.s.check,"a",self.e);self.assertEqual(self.s.history,[])

    def test_expiry(self):
        self.now=310;self.assertRaises(Rejected,self.s.check,"a",self.e);self.assertIsNone(self.s.actor)

    def test_cancel(self):
        self.s.cancel();self.assertRaises(Rejected,self.s.check,"a",self.e)

    def test_bounded(self):
        for i in range(20):self.s.append("a",self.e,"t"+str(i),"hello")
        self.assertEqual(len(self.s.history),8)
