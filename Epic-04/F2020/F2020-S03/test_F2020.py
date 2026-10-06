import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2020(unittest.TestCase):
    def setUp(self):
        self.f=FaceEngine()

    def test_pose(self):
        self.assertGreater(self.f.pose("happy")["smile"],0)

    def test_blend(self):
        a=self.f.pose("neutral");b=self.f.pose("happy")
        self.assertAlmostEqual(self.f.blend(a,b,.5)["smile"],.35)

    def test_unknown(self):
        with self.assertRaises(Rejected):self.f.pose("diagnosis")

    def test_nan(self):
        with self.assertRaises(Rejected):self.f.pose("happy",float("nan"))

    def test_intensity(self):
        with self.assertRaises(Rejected):self.f.pose("happy",2)

    def test_svg(self):
        s=self.f.svg(self.f.pose("happy"));self.assertIn("<svg",s);self.assertIn("viewBox",s)

    def test_inject(self):
        with self.assertRaises(Rejected):self.f.svg(self.f.pose("happy"),'<script>')

    def test_mouth(self):
        p=self.f.pose("speaking");p["mouth_open"]=.7
        self.assertIn('cy="111"',self.f.svg(p))

    def test_invalid_mouth(self):
        p=self.f.pose("neutral");p["mouth_open"]=-.1
        with self.assertRaises(Rejected):self.f.svg(p)
