import unittest
from core import *

class TestF2013(unittest.TestCase):
    def setUp(self):
        self.s=LanguageResolver();self.langs=["ko-KR","en-US"]

    def test_korean(self):
        self.assertEqual(self.s.choose("ko-KR",self.langs,self.langs,self.langs),"ko-KR")

    def test_english(self):
        self.assertEqual(self.s.choose("en-US",self.langs,self.langs,self.langs),"en-US")

    def test_unsupported(self):
        self.assertRaises(Rejected,self.s.choose,"zz-ZZ",self.langs,self.langs,self.langs)

    def test_tts_missing(self):
        self.assertRaises(Rejected,self.s.choose,"ko-KR",self.langs,self.langs,["en-US"])

    def test_stt_missing(self):
        self.assertRaises(Rejected,self.s.choose,"ko-KR",[],self.langs,self.langs)

    def test_llm_missing(self):
        self.assertRaises(Rejected,self.s.choose,"en-US",self.langs,[],self.langs)
