import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2025(unittest.TestCase):
    def setUp(self):
        self.p=PerformancePlanner()

    def test_plan(self):
        r=self.p.plan("demo-song",10,2,True,False,True)
        self.assertEqual(r["duration"],20);self.assertFalse(r["executable"])

    def test_rights(self):
        with self.assertRaises(Rejected):self.p.plan("demo",10,1,False,False,True)

    def test_repeat(self):
        with self.assertRaises(Rejected):self.p.plan("demo",10,4,True,False,True)

    def test_duration(self):
        with self.assertRaises(Rejected):self.p.plan("demo",60,3,True,False,True)

    def test_quiet(self):
        self.assertFalse(self.p.plan("demo",10,1,True,True,True)["enabled"])

    def test_clearance(self):
        self.assertFalse(self.p.plan("demo",10,1,True,False,False)["enabled"])

    def test_stop(self):
        self.assertFalse(self.p.plan("demo",10,1,True,False,True,stop=True)["enabled"])
