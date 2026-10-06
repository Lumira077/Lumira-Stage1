import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2027(unittest.TestCase):
    def setUp(self):
        self.g=GestureGate();self.g.activate(C)

    def test_stable(self):
        self.assertIsNone(self.g.observe(C,"wave",.9,10,10,True))
        self.assertIsNone(self.g.observe(C,"wave",.9,10.1,10.1,True))
        r=self.g.observe(C,"wave",.9,10.2,10.2,True);self.assertEqual(r["gesture"],"wave");self.assertFalse(r["executable"])

    def test_dedup(self):
        for t in (10,10.1,10.2):self.g.observe(C,"wave",.9,t,t,True)
        self.assertIsNone(self.g.observe(C,"wave",.9,10.3,10.3,True))

    def test_low_confidence(self):
        for t in (10,10.1,10.2):self.assertIsNone(self.g.observe(C,"wave",.2,t,t,True))

    def test_unsupported(self):
        self.assertIsNone(self.g.observe(C,"execute",1,10,10,True))

    def test_frame_order(self):
        self.g.observe(C,"wave",1,10,10,True)
        with self.assertRaises(Rejected):self.g.observe(C,"wave",1,10,10,True)

    def test_epoch(self):
        with self.assertRaises(Rejected):self.g.observe(Context("u",2),"wave",1,10,10,True)

    def test_gap(self):
        self.g.observe(C,"wave",1,10,10,True);self.g.observe(C,"wave",1,10.1,10.1,True)
        self.assertIsNone(self.g.observe(C,"wave",1,12,12,True))

    def test_revoke(self):
        self.g.revoke(C)
        with self.assertRaises(Rejected):self.g.observe(C,"wave",1,10,10,True)
        with self.assertRaises(Rejected):self.g.activate(C)

    def test_pose_angle(self):
        self.assertAlmostEqual(self.g.angle([1,0],[0,0],[0,1]),90)

    def test_pose_degenerate(self):
        with self.assertRaises(Rejected):self.g.angle([0,0],[0,0],[0,1])
