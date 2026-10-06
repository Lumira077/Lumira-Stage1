import unittest
from core import *

class TestF2123(unittest.TestCase):
    def setUp(self):
        self.s=HybridRouter();self.x={'sensitivity':'public','safety_command':False,'cloud_consent':True,'visual_needed':False,'network_ok':True,'credits':10,'robot_ready':True}

    def test_cloud(self):
        self.assertEqual(self.s.route(self.x)["route"],"cloud")

    def test_privacy(self):
        self.x["sensitivity"]="sensitive";self.assertEqual(self.s.route(self.x)["route"],"local")

    def test_unapproved(self):
        self.assertEqual(self.s.route(self.x,"unknown")["route"],"local")

    def test_quota(self):
        self.x["credits"]=0;self.assertEqual(self.s.route(self.x)["reason"],"NO_CREDIT")

    def test_network(self):
        self.x["network_ok"]=False;self.assertEqual(self.s.route(self.x)["route"],"local")

    def test_safety(self):
        self.x["safety_command"]=True;self.assertEqual(self.s.route(self.x)["reason"],"SAFETY_LOCAL")

    def test_no_execution(self):
        self.assertFalse(self.s.route(self.x)["executed"])
