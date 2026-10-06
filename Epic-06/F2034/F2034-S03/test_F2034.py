import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2034(unittest.TestCase):
    def setUp(self):
        self.p=PowerPolicy()

    def test_normal(self):
        self.assertTrue(self.p.assess(.8,30,2,False,10,10,True)["motion_allowed"])

    def test_low(self):
        self.assertEqual(self.p.assess(.15,30,2,False,10,10,True)["mode"],"low_power")

    def test_critical(self):
        self.assertEqual(self.p.assess(.05,30,2,False,10,10,True)["mode"],"shutdown_requested")

    def test_thermal(self):
        r=self.p.assess(.8,70,2,False,10,10,True)
        self.assertFalse(r["motion_allowed"]);self.assertIsNone(r["hardware_action"])

    def test_overcurrent(self):
        self.assertEqual(self.p.assess(.8,30,25,False,10,10,True)["mode"],"fault")

    def test_stale(self):
        self.assertEqual(self.p.assess(.8,30,2,False,10,13,True)["mode"],"unknown")

    def test_charging(self):
        self.assertFalse(self.p.assess(.8,30,2,True,10,10,True)["motion_allowed"])

    def test_soc(self):
        with self.assertRaises(Rejected):self.p.assess(1.5,30,2,False,10,10,True)
