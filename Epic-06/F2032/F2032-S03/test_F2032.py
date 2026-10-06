import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2032(unittest.TestCase):
    def setUp(self):
        self.m=MockMotor();self.m.enable()

    def test_step_limit(self):
        self.m.command(.5,10);self.m.tick(10);self.assertAlmostEqual(self.m.tick(10.1),.1)

    def test_position_limit(self):
        with self.assertRaises(Rejected):self.m.command(1,10)

    def test_watchdog(self):
        self.m.command(.3,10);self.m.tick(11)
        self.assertTrue(self.m.latched);self.assertFalse(self.m.enabled)

    def test_stop_latch(self):
        self.m.stop()
        with self.assertRaises(Rejected):self.m.enable()
        with self.assertRaises(Rejected):self.m.command(.1,10)

    def test_reset_evidence(self):
        self.m.stop()
        with self.assertRaises(Rejected):self.m.reset(False,True)
        self.m.reset(True,True);self.assertFalse(self.m.enabled)

    def test_clock(self):
        self.m.tick(10)
        with self.assertRaises(Rejected):self.m.tick(9)

    def test_nan(self):
        with self.assertRaises(Rejected):self.m.command(float("nan"),10)

    def test_stopped_hold(self):
        self.m.command(.3,10);self.m.tick(10);self.m.tick(10.1);self.m.stop()
        self.assertAlmostEqual(self.m.tick(11),.1)
