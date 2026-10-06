import unittest
from core import *

class TestF2207(unittest.TestCase):
    def setUp(self):
        self.s=RealtimeGate(1,True,True,True)

    def test_video(self):
        self.assertFalse(self.s.accept("video",1,1)["transmitted"])

    def test_unneeded_video(self):
        self.s.visual=False;self.assertRaises(Rejected,self.s.accept,"video",1,1)

    def test_no_consent(self):
        self.s.cloud=False;self.assertRaises(Rejected,self.s.accept,"audio",1,1)

    def test_stale_epoch(self):
        self.assertRaises(Rejected,self.s.accept,"audio",1,0)

    def test_sequence(self):
        self.s.accept("audio",1,1);self.assertRaises(Rejected,self.s.accept,"audio",1,1)

    def test_closed(self):
        self.s.close();self.assertRaises(Rejected,self.s.accept,"audio",1,1)
