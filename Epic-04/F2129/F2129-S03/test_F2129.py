import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2129(unittest.TestCase):
    def setUp(self):
        self.s=SkinRegistry();self.asset=skin();self.h=self.s.digest(self.asset)

    def test_install(self):
        self.assertEqual(self.s.install(self.asset,self.h)["id"],"lumira")

    def test_hash(self):
        with self.assertRaises(Rejected):self.s.install(self.asset,"0"*64)

    def test_states(self):
        self.asset["states"].pop()
        with self.assertRaises(Rejected):self.s.install(self.asset,self.s.digest(self.asset))

    def test_rights(self):
        self.asset["rights"]=False
        with self.assertRaises(Rejected):self.s.install(self.asset,self.s.digest(self.asset))

    def test_injection(self):
        self.asset["color"]="<script>"
        with self.assertRaises(Rejected):self.s.install(self.asset,self.s.digest(self.asset))

    def test_atomic_failure(self):
        self.s.install(self.asset,self.h);self.asset["id"]="../x"
        with self.assertRaises(Rejected):self.s.install(self.asset,self.s.digest(self.asset))
        self.assertEqual(self.s.active["id"],"lumira")

    def test_copy(self):
        a=self.s.install(self.asset,self.h);a["color"]="#000000"
        self.assertEqual(self.s.active["color"],"#64d9ff")

    def test_unexpected_payload(self):
        self.asset["raw_photo"]="fixture"
        with self.assertRaises(Rejected):self.s.install(self.asset,self.s.digest(self.asset))
