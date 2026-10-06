import unittest
from core import *

class TestF2009(unittest.TestCase):
    def setUp(self):
        self.s=TranscriptAssembler(1)

    def test_partial(self):
        self.assertFalse(self.s.update(1,"안녕",False,1)["ready_for_dialogue"])

    def test_final(self):
        self.assertTrue(self.s.update(1,"안녕",True,1)["ready_for_dialogue"])

    def test_late_partial(self):
        self.s.update(1,"안녕",True,1);self.assertRaises(Rejected,self.s.update,2,"안",False,1)

    def test_sequence(self):
        self.s.update(2,"hello",False,1);self.assertRaises(Rejected,self.s.update,1,"he",False,1)

    def test_stale_epoch(self):
        self.assertRaises(Rejected,self.s.update,1,"hi",True,0)

    def test_oversize(self):
        self.assertRaises(Rejected,self.s.update,1,"x"*2001,True,1)
