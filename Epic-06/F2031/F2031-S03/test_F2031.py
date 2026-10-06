import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2031(unittest.TestCase):
    def setUp(self):
        self.h=BoardHAL()

    def test_lifecycle(self):
        self.h.configure(profile());self.h.activate(["joint"]);self.assertEqual(self.h.state,"active");self.h.deactivate();self.h.cleanup();self.assertEqual(self.h.state,"unconfigured")

    def test_missing(self):
        self.h.configure(profile())
        with self.assertRaises(Rejected):self.h.activate(["camera"])

    def test_real_denied(self):
        p=profile();p["mode"]="hardware"
        with self.assertRaises(Rejected):self.h.configure(p)

    def test_arch(self):
        p=profile();p["arch"]="unknown"
        with self.assertRaises(Rejected):self.h.configure(p)

    def test_state(self):
        with self.assertRaises(Rejected):self.h.activate(["joint"])

    def test_active_cleanup(self):
        self.h.configure(profile());self.h.activate(["joint"])
        with self.assertRaises(Rejected):self.h.cleanup()

    def test_fault(self):
        self.h.configure(profile());self.h.activate(["joint"]);self.h.fault()
        self.assertEqual(self.h.state,"error")

    def test_copy(self):
        p=profile();self.h.configure(p);p["capabilities"].clear()
        self.h.activate(["joint"])
