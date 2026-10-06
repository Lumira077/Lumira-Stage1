import unittest
from core import *
C=Context('u',1)
V=[1,0,0,0,0,0,0,0]
W=[0,1,0,0,0,0,0,0]
def track(id='a',angle=10,epoch=1,timestamp=10,quality=1):return {'id':id,'angle_deg':angle,'epoch':epoch,'timestamp':timestamp,'quality':quality}

class TestF2026(unittest.TestCase):
    def setUp(self):
        self.f=FaceRegistry();self.f.enroll("u",1,V,"fixture_v1",True,True,True)

    def test_candidate(self):
        r=self.f.identify(V,"fixture_v1",10,10,True,True)
        self.assertEqual(r["candidate"],"u");self.assertFalse(r["authenticated"])

    def test_unknown(self):
        self.assertIsNone(self.f.identify(W,"fixture_v1",10,10,True,True)["candidate"])

    def test_ambiguity(self):
        self.f.enroll("v",1,V,"fixture_v1",True,True,True)
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,10,True,True)["candidate"])

    def test_no_consent(self):
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,10,False,True)["candidate"])

    def test_no_live(self):
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,10,True,False)["candidate"])

    def test_multiple(self):
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,10,True,True,2)["candidate"])

    def test_stale(self):
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,12,True,True)["candidate"])

    def test_version(self):
        self.assertIsNone(self.f.identify(V,"fixture_v2",10,10,True,True)["candidate"])

    def test_revoke(self):
        self.f.revoke("u",2)
        self.assertIsNone(self.f.identify(V,"fixture_v1",10,10,True,True)["candidate"])
        with self.assertRaises(Rejected):self.f.enroll("u",1,V,"fixture_v1",True,True,True)
        with self.assertRaises(Rejected):self.f.enroll("u",2,V,"fixture_v1",True,True,True)

    def test_authorized(self):
        with self.assertRaises(Rejected):self.f.enroll("v",1,V,"fixture_v1",True,False,True)

    def test_vector(self):
        with self.assertRaises(Rejected):self.f.enroll("v",1,[0]*8,"fixture_v1",True,True,True)
        with self.assertRaises(Rejected):self.f.enroll("v",1,[float("nan")]*8,"fixture_v1",True,True,True)
