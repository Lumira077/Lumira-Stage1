import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2028(unittest.TestCase):
    def setUp(self):
        self.t=TouchFSM();self.t.activate(C)

    def test_tap(self):
        self.t.event(C,1,"head",True,10)
        self.assertEqual(self.t.event(C,2,"head",False,10.3)["kind"],"tap")

    def test_long(self):
        self.t.event(C,1,"body",True,10)
        self.assertEqual(self.t.event(C,2,"body",False,11.2)["kind"],"long_press")

    def test_debounce(self):
        self.t.event(C,1,"head",True,10)
        self.assertIsNone(self.t.event(C,2,"head",False,10.01))

    def test_duplicate_release(self):
        self.assertIsNone(self.t.event(C,1,"head",False,10))

    def test_duplicate_down(self):
        self.t.event(C,1,"head",True,10);self.t.event(C,2,"head",True,10.8)
        self.assertEqual(self.t.event(C,3,"head",False,11.1)["kind"],"long_press")

    def test_seq(self):
        self.t.event(C,1,"head",True,10)
        with self.assertRaises(Rejected):self.t.event(C,1,"head",False,11)

    def test_time_reverse(self):
        self.t.event(C,1,"head",True,10)
        with self.assertRaises(Rejected):self.t.event(C,2,"head",False,9)

    def test_stuck(self):
        self.t.event(C,1,"head",True,10)
        self.assertIsNone(self.t.event(C,2,"head",False,21))

    def test_region(self):
        with self.assertRaises(Rejected):self.t.event(C,1,"motor",True,10)

    def test_revoke(self):
        self.t.event(C,1,"head",True,10);self.t.revoke(C)
        self.assertEqual(self.t.press,{})
        with self.assertRaises(Rejected):self.t.event(C,2,"head",False,11)
