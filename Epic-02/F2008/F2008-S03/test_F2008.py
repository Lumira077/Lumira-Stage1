import unittest
from core import *

class TestF2008(unittest.TestCase):
    def setUp(self):
        self.now=10;self.s=WakeGate(lambda:self.now)

    def test_accepted(self):
        self.assertTrue(self.s.trigger("e",.9,10)["start_session"])

    def test_low_score(self):
        self.assertFalse(self.s.trigger("e",.5,10)["start_session"])

    def test_mute(self):
        self.assertFalse(self.s.trigger("e",.9,10,True)["start_session"])

    def test_echo(self):
        self.assertFalse(self.s.trigger("e",.9,10,False,True)["start_session"])

    def test_cooldown(self):
        self.s.trigger("e",.9,10);self.assertFalse(self.s.trigger("e2",.9,10)["start_session"])

    def test_duplicate(self):
        self.s.trigger("e",.9,10);self.assertRaises(Rejected,self.s.trigger,"e",.9,10)

    def test_stale(self):
        self.assertRaises(Rejected,self.s.trigger,"e",.9,7)
