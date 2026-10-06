import unittest
from core import *

class TestF2206(unittest.TestCase):
    def setUp(self):
        self.s=Gateway({"openai_sample":lambda i,n:{"text":"fixture one","usage_tokens":2},"gemini_sample":lambda i,n:{"text":"fixture two","usage_tokens":3}})

    def test_two_adapters(self):
        self.assertNotEqual(self.s.complete("openai_sample","r")["text"],self.s.complete("gemini_sample","r")["text"])

    def test_unapproved(self):
        self.assertRaises(Rejected,self.s.complete,"arbitrary_url","r")

    def test_invalid_usage(self):
        self.s.adapters["openai_sample"]=lambda i,n:{"text":"x","usage_tokens":-1};self.assertRaises(Rejected,self.s.complete,"openai_sample","r")

    def test_extra_secret_field(self):
        self.s.adapters["openai_sample"]=lambda i,n:{"text":"x","usage_tokens":1,"secret":"private"};self.assertRaises(Rejected,self.s.complete,"openai_sample","r")

    def test_oversize(self):
        self.s.adapters["openai_sample"]=lambda i,n:{"text":"x"*2001,"usage_tokens":1};self.assertRaises(Rejected,self.s.complete,"openai_sample","r")

    def test_sanitized_error(self):
        self.s.adapters["openai_sample"]=lambda i,n:(_ for _ in ()).throw(ValueError("secret"))
        with self.assertRaises(Rejected) as e:self.s.complete("openai_sample","r")
        self.assertNotIn("secret",str(e.exception))
