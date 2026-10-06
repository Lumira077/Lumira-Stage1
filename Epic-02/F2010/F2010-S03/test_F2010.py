import unittest
from core import *

class TestF2010(unittest.TestCase):
    def setUp(self):
        self.now=10;self.session=ConversationSession(lambda:self.now);self.e=self.session.open("a");self.gateway=Gateway({"openai_sample":lambda i,n:{"text":"safe fixture","usage_tokens":2}});self.s=Dialogue(self.session,self.gateway);self.x={'sensitivity':'public','safety_command':False,'cloud_consent':True,'visual_needed':False,'network_ok':True,'credits':10,'robot_ready':True}

    def test_normal(self):
        self.assertEqual(self.s.answer("a",self.e,"t",self.x,"adult","clear")["backend"],"openai_sample")

    def test_private_local(self):
        self.x["sensitivity"]="sensitive";self.assertEqual(self.s.answer("a",self.e,"t",self.x,"adult","clear")["backend"],"local_template")

    def test_risk_gate(self):
        self.assertEqual(self.s.answer("a",self.e,"t",self.x,"adult","harm")["backend"],"local_safety_template")

    def test_no_consent(self):
        self.x["cloud_consent"]=False;self.assertEqual(self.s.answer("a",self.e,"t",self.x,"adult","clear")["route"]["route"],"local")

    def test_duplicate(self):
        self.s.answer("a",self.e,"t",self.x);self.assertRaises(Rejected,self.s.answer,"a",self.e,"t",self.x)

    def test_switch_during_generation(self):
        def adapter(i,n):
         self.session.open("b");return {"text":"late","usage_tokens":1}
        self.gateway.adapters["openai_sample"]=adapter
        self.assertRaises(Rejected,self.s.answer,"a",self.e,"t",self.x,"adult","clear");self.assertEqual(self.session.history,[])

    def test_foreign_actor(self):
        self.assertRaises(Rejected,self.s.answer,"b",self.e,"t",self.x)
