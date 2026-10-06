import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2127(unittest.TestCase):
    def setUp(self):
        self.s=SpeakerAssociator()

    def test_associate(self):
        r=self.s.associate(C,10,10,[track()],10,True,False,True)
        self.assertEqual(r["track"],"a");self.assertFalse(r["owner_authenticated"])

    def test_ambiguous(self):
        self.assertEqual(self.s.associate(C,10,10,[track(),track("b",15)],10,True,False,True)["reason"],"ambiguous")

    def test_echo(self):
        self.assertIsNone(self.s.associate(C,10,10,[track()],10,True,True,True)["track"])

    def test_no_vad(self):
        self.assertIsNone(self.s.associate(C,10,10,[track()],10,False,False,True)["track"])

    def test_consent(self):
        self.assertIsNone(self.s.associate(C,10,10,[track()],10,True,False,False)["track"])

    def test_skew(self):
        self.assertIsNone(self.s.associate(C,10,10,[track(timestamp=9.5)],10,True,False,True)["track"])

    def test_stale(self):
        self.assertIsNone(self.s.associate(C,10,10,[track()],12,True,False,True)["track"])

    def test_outside(self):
        self.assertIsNone(self.s.associate(C,60,10,[track()],10,True,False,True)["track"])

    def test_epoch(self):
        with self.assertRaises(Rejected):self.s.associate(C,10,10,[track(epoch=2)],10,True,False,True)

    def test_duplicate(self):
        with self.assertRaises(Rejected):self.s.associate(C,10,10,[track(),track()],10,True,False,True)
