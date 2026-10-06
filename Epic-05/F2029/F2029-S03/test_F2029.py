import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2029(unittest.TestCase):
    def setUp(self):
        self.p=PresenceGate();self.p.activate(C)

    def test_stable(self):
        for t in (10,10.1):self.assertEqual(self.p.observe(C,.9,t,t,True,True),"unknown")
        self.assertEqual(self.p.observe(C,.9,10.2,10.2,True,True),"present")

    def test_hysteresis(self):
        for t in (10,10.1,10.2):self.p.observe(C,.9,t,t,True,True)
        self.assertEqual(self.p.observe(C,.1,10.3,10.3,True,True),"present")

    def test_absent(self):
        for t in (10,10.1,10.2):r=self.p.observe(C,.1,t,t,True,True)
        self.assertEqual(r,"absent")

    def test_sensor_failure(self):
        self.assertEqual(self.p.observe(C,.9,10,10,False,True),"unknown")

    def test_stale(self):
        self.assertEqual(self.p.observe(C,.9,10,12,True,True),"unknown")

    def test_consent(self):
        self.assertEqual(self.p.observe(C,.9,10,10,True,False),"unknown")

    def test_gap(self):
        self.p.observe(C,.9,10,10,True,True);self.p.observe(C,.9,10.1,10.1,True,True)
        self.assertEqual(self.p.observe(C,.9,12,12,True,True),"unknown")

    def test_order(self):
        self.p.observe(C,.9,10,10,True,True)
        with self.assertRaises(Rejected):self.p.observe(C,.9,10,10,True,True)

    def test_nan(self):
        with self.assertRaises(Rejected):self.p.observe(C,float("nan"),10,10,True,True)
