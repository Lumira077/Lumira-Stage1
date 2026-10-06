import unittest
from core import *

class TestF2212(unittest.TestCase):
    def setUp(self):
        self.s=Recovery();self.fail=lambda:(_ for _ in ()).throw(TimeoutError())

    def test_second_provider(self):
        self.assertEqual(self.s.complete("t",[self.fail,lambda:"ok"])["attempts"],2)

    def test_all_fail(self):
        self.assertEqual(self.s.complete("t",[self.fail])["backend"],"local_template")

    def test_single_final(self):
        self.s.complete("t",[lambda:"ok"]);self.assertRaises(Rejected,self.s.complete,"t",[lambda:"late"])

    def test_partial_output(self):
        self.assertRaises(Rejected,self.s.complete,"t",[lambda:"ok"],True)

    def test_too_many(self):
        self.assertRaises(Rejected,self.s.complete,"t",[self.fail]*4)

    def test_invalid_reply(self):
        self.assertEqual(self.s.complete("t",[lambda:""])["backend"],"local_template")
