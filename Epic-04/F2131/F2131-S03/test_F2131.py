import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2131(unittest.TestCase):
    def setUp(self):
        self.r=FaceResearchGate()

    def test_insufficient(self):
        r=self.r.assess(0,0,100,2000,.8,False,False)
        self.assertFalse(r["research_candidate"]);self.assertIn("user_samples",r["pending"])

    def test_candidate(self):
        r=self.r.assess(20,30,50,1024,.2,True,True)
        self.assertTrue(r["research_candidate"]);self.assertFalse(r["production_enabled"])

    def test_no_rights(self):
        self.assertIn("asset_rights",self.r.assess(20,30,50,1024,.2,False,True)["pending"])

    def test_privacy(self):
        self.assertIn("privacy_review",self.r.assess(20,30,50,1024,.2,True,False)["pending"])

    def test_gpu_budget(self):
        self.assertIn("gpu_memory",self.r.assess(20,30,50,2048,.2,True,True)["pending"])

    def test_discomfort(self):
        self.assertIn("discomfort",self.r.assess(20,30,50,1024,.5,True,True)["pending"])

    def test_nan(self):
        with self.assertRaises(Rejected):self.r.assess(20,float("nan"),50,1024,.2,True,True)

    def test_default(self):
        self.assertEqual(self.r.assess(0,0,0,0,0,False,False)["default"],"character_2d")
