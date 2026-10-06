import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2030(unittest.TestCase):
    def setUp(self):
        self.c=CommandGate();self.g=self.c.activate()

    def test_accept(self):
        self.assertFalse(self.c.accept(packet(),10)["executable"])

    def test_duplicate(self):
        self.c.accept(packet(),10)
        with self.assertRaises(Rejected):self.c.accept(packet(),10)

    def test_stale(self):
        with self.assertRaises(Rejected):self.c.accept(packet(t=9),10)

    def test_future(self):
        with self.assertRaises(Rejected):self.c.accept(packet(t=11),10)

    def test_scope(self):
        p=packet();p["robot"]="physical_robot"
        with self.assertRaises(Rejected):self.c.accept(p,10)

    def test_cancel(self):
        self.c.cancel()
        with self.assertRaises(Rejected):self.c.accept(packet(),10)

    def test_nan(self):
        with self.assertRaises(Rejected):self.c.accept(packet(y=float("nan")),10)

    def test_schema(self):
        p=packet();p["shell"]="fixture"
        with self.assertRaises(Rejected):self.c.accept(p,10)
