import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2133(unittest.TestCase):
    def setUp(self):
        self.h=HeadAligner()

    def test_audio_step(self):
        r=self.h.propose(C,0,.1,10,10,doa=30,clearance=True)
        self.assertEqual(r["target_yaw_deg"],3);self.assertFalse(r["executable"])

    def test_visual_step(self):
        r=self.h.propose(C,0,.1,10,10,face_x=1,clearance=True)
        self.assertEqual(r["target_yaw_deg"],3)

    def test_limit(self):
        r=self.h.propose(C,59,.1,10,10,doa=120,clearance=True)
        self.assertEqual(r["target_yaw_deg"],60)

    def test_deadband(self):
        self.assertEqual(self.h.propose(C,10,.1,10,10,face_x=.01,clearance=True)["target_yaw_deg"],10)

    def test_lost(self):
        self.assertEqual(self.h.propose(C,10,.1,10,10,clearance=True)["reason"],"hold")

    def test_stale(self):
        self.assertEqual(self.h.propose(C,0,.1,10,12,doa=30,clearance=True)["target_yaw_deg"],0)

    def test_stop(self):
        self.assertEqual(self.h.propose(C,0,.1,10,10,doa=30,clearance=True,stop=True)["reason"],"hold")

    def test_clearance(self):
        self.assertEqual(self.h.propose(C,0,.1,10,10,doa=30)["reason"],"hold")

    def test_quality(self):
        self.assertEqual(self.h.propose(C,0,.1,10,10,doa=30,quality=.2,clearance=True)["reason"],"hold")

    def test_dt(self):
        with self.assertRaises(Rejected):self.h.propose(C,0,0,10,10,doa=30,clearance=True)

    def test_range(self):
        with self.assertRaises(Rejected):self.h.propose(C,0,.1,10,10,face_x=2,clearance=True)
