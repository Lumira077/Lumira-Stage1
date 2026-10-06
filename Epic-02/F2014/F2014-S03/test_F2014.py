import unittest
from core import *

class TestF2014(unittest.TestCase):
    def setUp(self):
        self.s=SafetyPolicy()

    def test_adult_clear(self):
        self.assertEqual(self.s.review("adult","clear")["action"],"allow")

    def test_unknown_age(self):
        self.assertEqual(self.s.review("unknown","clear")["action"],"local_guidance")

    def test_medical(self):
        self.assertEqual(self.s.review("elder","medical")["action"],"local_guidance")

    def test_crisis_no_false_contact(self):
        self.assertIn("실행하지",self.s.review("adult","crisis")["safe_reply"])

    def test_private(self):
        self.assertEqual(self.s.review("child","private")["action"],"deny")

    def test_harm(self):
        self.assertEqual(self.s.review("child","harm")["action"],"deny")

    def test_invalid_tag(self):
        self.assertRaises(Rejected,self.s.review,"adult","untrusted-new-tag")
