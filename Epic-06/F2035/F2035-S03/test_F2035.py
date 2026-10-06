import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2035(unittest.TestCase):
    def setUp(self):
        self.d=Diagnostics()

    def test_healthy(self):
        self.d.heartbeat("motor",10)
        self.assertTrue(self.d.report(10,["motor"])["healthy"])

    def test_missing(self):
        self.assertEqual(self.d.report(10,["motor"])["stale"],["motor"])

    def test_stale(self):
        self.d.heartbeat("motor",10)
        self.assertFalse(self.d.report(12,["motor"])["healthy"])

    def test_fault_latch(self):
        self.d.fault("motor","E_STOP");self.d.heartbeat("motor",10)
        self.assertFalse(self.d.report(10,["motor"])["healthy"])

    def test_clear(self):
        self.d.fault("motor","E_STOP")
        with self.assertRaises(Rejected):self.d.clear("motor",False,True)
        self.d.clear("motor",True,True);self.assertEqual(self.d.faults,{})

    def test_unknown_code(self):
        with self.assertRaises(Rejected):self.d.fault("motor","RAW_LOG")

    def test_clock(self):
        self.d.heartbeat("motor",10)
        with self.assertRaises(Rejected):self.d.heartbeat("motor",9)

    def test_not_physical(self):
        self.assertFalse(self.d.report(10,[])["hardware_stop_confirmed"])
