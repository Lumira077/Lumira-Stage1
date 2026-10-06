import unittest
from core import *

class TestF2211(unittest.TestCase):
    def setUp(self):
        self.s=PrivacyGuard()

    def test_public(self):
        self.assertTrue(self.s.check("public",True,False,"openai_sample")["allow_cloud"])

    def test_sensitive(self):
        self.assertFalse(self.s.check("sensitive",True,False,"openai_sample")["allow_cloud"])

    def test_unknown(self):
        self.assertFalse(self.s.check("unknown",True,False,"openai_sample")["allow_cloud"])

    def test_no_consent(self):
        self.assertFalse(self.s.check("public",False,False,"openai_sample")["allow_cloud"])

    def test_safety(self):
        self.assertFalse(self.s.check("public",True,True,"openai_sample")["allow_cloud"])

    def test_unapproved(self):
        self.assertFalse(self.s.check("public",True,False,"unknown")["allow_cloud"])
