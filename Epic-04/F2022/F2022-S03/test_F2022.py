import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2022(unittest.TestCase):
    def setUp(self):
        self.g=GestureLibrary()

    def test_plan(self):
        p=self.g.plan("wave",True,ZERO)
        self.assertEqual(p["units"],"radians");self.assertFalse(p["executable"])

    def test_clearance(self):
        with self.assertRaises(Rejected):self.g.plan("wave",False,ZERO)

    def test_start_pose(self):
        with self.assertRaises(Rejected):self.g.plan("wave",True,dict(ZERO,neck=.1))

    def test_joint_limit(self):
        with self.assertRaises(Rejected):self.g.validate([(0,ZERO),(1,dict(ZERO,neck=2))])

    def test_velocity(self):
        with self.assertRaises(Rejected):self.g.validate([(0,ZERO),(.01,dict(ZERO,arm=.3))])

    def test_time_order(self):
        with self.assertRaises(Rejected):self.g.validate([(0,ZERO),(0,ZERO)])

    def test_joint_schema(self):
        with self.assertRaises(Rejected):self.g.validate([(0,{"neck":0}),(1,ZERO)])

    def test_unknown(self):
        with self.assertRaises(Rejected):self.g.plan("jump",True,ZERO)

    def test_copy(self):
        p=self.g.plan("nod",True,ZERO);p["points"][0][1]["neck"]=99
        self.assertEqual(self.g.plan("nod",True,ZERO)["points"][0][1]["neck"],0)
