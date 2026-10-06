import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2130(unittest.TestCase):
    def setUp(self):
        self.l=GazeLip();self.cues=[(0,.5,"open"),(.5,1,"small")]

    def test_viseme(self):
        self.assertEqual(self.l.pose(.2,.1,self.cues,.1)["mouth_open"],.75)

    def test_boundary(self):
        self.assertEqual(self.l.pose(0,0,self.cues,.5)["mouth_open"],.25)

    def test_end(self):
        self.assertEqual(self.l.pose(0,0,self.cues,1)["mouth_open"],0)

    def test_cancel(self):
        self.assertEqual(self.l.pose(.3,.3,self.cues,.1,True)["mouth_open"],0)

    def test_gaze_limit(self):
        with self.assertRaises(Rejected):self.l.pose(2,0,self.cues,.1)

    def test_overlap(self):
        with self.assertRaises(Rejected):self.l.pose(0,0,[(0,1,"open"),(.5,2,"small")],.1)

    def test_negative_time(self):
        with self.assertRaises(Rejected):self.l.pose(0,0,[(-1,1,"open")],.1)

    def test_unknown_viseme(self):
        with self.assertRaises(Rejected):self.l.pose(0,0,[(0,1,"raw")],.1)

    def test_missing_alignment(self):
        self.assertEqual(self.l.pose(0,0,[],.1)["mouth_open"],0)
