import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2033(unittest.TestCase):
    def setUp(self):
        self.s=SensorSynchronizer()

    def test_pair(self):
        self.s.update("camera",1,10,10,0);self.s.update("audio",1,10.01,10.01,0)
        self.assertAlmostEqual(self.s.pair("camera","audio",10.02)["skew"],.01)

    def test_one_use(self):
        self.s.update("camera",1,10,10,0);self.s.update("audio",1,10,10,0);self.s.pair("camera","audio",10)
        self.assertIsNone(self.s.pair("camera","audio",10))

    def test_skew(self):
        self.s.update("camera",1,10,10,0);self.s.update("audio",1,10.1,10.1,0)
        self.assertIsNone(self.s.pair("camera","audio",10.1))

    def test_stale(self):
        with self.assertRaises(Rejected):self.s.update("imu",1,9,10,0)

    def test_duplicate(self):
        self.s.update("touch",1,10,10,0)
        with self.assertRaises(Rejected):self.s.update("touch",1,10,10,0)

    def test_reset(self):
        self.s.update("camera",1,10,10,0);self.s.reset()
        with self.assertRaises(Rejected):self.s.update("camera",2,10.1,10.1,0)
        self.assertEqual(self.s.samples,{})

    def test_reverse(self):
        self.s.update("audio",1,10,10,0)
        with self.assertRaises(Rejected):self.s.update("audio",2,9.9,10,0)

    def test_unknown(self):
        with self.assertRaises(Rejected):self.s.update("unknown",1,10,10,0)
