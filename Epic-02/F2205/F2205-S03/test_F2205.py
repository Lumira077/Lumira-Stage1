import unittest
from core import *

class TestF2205(unittest.TestCase):
    def setUp(self):
        self.x={'sensitivity':'public','safety_command':False,'cloud_consent':True,'visual_needed':False,'network_ok':True,'credits':10,'robot_ready':True};self.s=PolicyEngine()

    def test_cloud(self):
        self.assertEqual(self.s.decide(self.x)["route"],"cloud")

    def test_safety_priority(self):
        self.x.update(safety_command=True,credits=0);self.assertEqual(self.s.decide(self.x)["reason"],"SAFETY_LOCAL")

    def test_sensitive(self):
        self.x["sensitivity"]="sensitive";self.assertEqual(self.s.decide(self.x)["route"],"local")

    def test_no_consent(self):
        self.x["cloud_consent"]=False;self.assertEqual(self.s.decide(self.x)["route"],"local")

    def test_visual(self):
        self.x["visual_needed"]=True;self.assertEqual(self.s.decide(self.x)["route"],"hybrid")

    def test_invalid_bool(self):
        self.x["credits"]=True;self.assertRaises(Rejected,self.s.decide,self.x)

    def test_repeat(self):
        self.assertEqual(self.s.decide(self.x),self.s.decide(dict(self.x)))

    def test_robot_denied(self):
        self.x["robot_ready"]=False;self.assertEqual(self.s.decide(self.x)["route"],"deny")
