import unittest
from core import *
def packet(g=1,s=1,t=10,y=.2):return {'robot':'lumira_sim','schema':'joint-v1','generation':g,'seq':s,'timestamp':t,'yaw':y}
def profile():return {'id':'mock_board','arch':'aarch64','capabilities':['joint','power'],'mode':'mock'}

class TestF2120(unittest.TestCase):
    def setUp(self):
        self.o=Orchestrator()

    def test_control_local(self):
        self.assertEqual(self.o.route("a","control","public",True,True,10,True,True)["place"],"local")

    def test_control_no_cloud(self):
        self.assertEqual(self.o.route("a","control","public",True,True,10,False,True)["place"],"blocked")

    def test_private_edge(self):
        self.assertEqual(self.o.route("a","dialogue","private",True,True,10,True,True)["place"],"edge")

    def test_no_consent(self):
        self.assertEqual(self.o.route("a","dialogue","public",False,True,10,True,False)["place"],"local")

    def test_cloud(self):
        self.assertEqual(self.o.route("a","dialogue","public",True,True,10,True,False)["place"],"cloud")

    def test_offline(self):
        self.assertEqual(self.o.route("a","dialogue","public",True,False,10,True,False)["place"],"local")

    def test_stale_result(self):
        r=self.o.route("a","dialogue","public",True,True,10,True,False);self.o.cancel()
        with self.assertRaises(Rejected):self.o.complete("a",r["generation"],r["place"])

    def test_complete(self):
        r=self.o.route("a","perception","private",True,True,10,True,True)
        self.assertTrue(self.o.complete("a",r["generation"],r["place"])["accepted"])
        with self.assertRaises(Rejected):self.o.complete("a",r["generation"],r["place"])

    def test_wrong_result(self):
        r=self.o.route("a","dialogue","public",True,True,10,True,False)
        with self.assertRaises(Rejected):self.o.complete("a",r["generation"],"edge")

    def test_budget(self):
        with self.assertRaises(Rejected):self.o.route("a","dialogue","public",True,True,float("nan"),True,False)
