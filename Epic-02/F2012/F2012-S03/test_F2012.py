import unittest
from core import *

class TestF2012(unittest.TestCase):
    def setUp(self):
        self.session=ConversationSession(lambda:10);self.e=self.session.open("a");self.s=InterruptController(self.session)

    def test_cancel(self):
        self.assertFalse(self.s.cancel()["actual_cancelled"]);self.assertIsNone(self.session.actor)

    def test_late_output(self):
        self.s.cancel();self.assertRaises(Rejected,self.s.accept_output,self.e)

    def test_missing_ack(self):
        r=self.s.cancel();self.s.ack("tts",r["epoch"]);self.assertRaises(Rejected,self.s.accept_output,r["epoch"])

    def test_wrong_ack(self):
        r=self.s.cancel();self.assertRaises(Rejected,self.s.ack,"tts",r["epoch"]-1)

    def test_all_ack_new_session(self):
        r=self.s.cancel()
        for m in self.s.MODULES:self.s.ack(m,r["epoch"])
        e=self.session.open("b");self.assertTrue(self.s.accept_output(e))

    def test_old_ack_after_new_cancel(self):
        r=self.s.cancel();self.s.cancel();self.assertRaises(Rejected,self.s.ack,"tts",r["epoch"])
