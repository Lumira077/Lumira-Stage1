import unittest
from core import *
def score(label="happy"):
 p=dict.fromkeys(LABELS,.025);p[label]=.9;return p
def obs(modality,**kw):
 d=dict(owner="u",epoch=1,modality=modality,timestamp=10,scores=score(),quality=1,model_version="fixture-v1");d.update(kw);return Observation(**d)

class TestF2017(unittest.TestCase):
    def setUp(self):
        self.s=SelfReport()

    def test_korean(self):
        self.assertEqual(max(self.s.observe("u",1,10,"나는 슬퍼요",True).scores,key=self.s.observe("u",1,10,"나는 슬퍼요",True).scores.get),"sad")

    def test_english(self):
        self.assertEqual(self.s.observe("u",1,10,"I feel happy",True).origin,"self_report_fixture")

    def test_negation(self):
        self.assertIsNone(self.s.observe("u",1,10,"나는 슬프지 않아요",True))

    def test_quote(self):
        self.assertIsNone(self.s.observe("u",1,10,'"나는 슬퍼요"',True))

    def test_other_person(self):
        self.assertIsNone(self.s.observe("u",1,10,"그 사람은 슬퍼요",True))

    def test_ambiguous(self):
        self.assertIsNone(self.s.observe("u",1,10,"좋네",True))

    def test_crisis_not_classified(self):
        self.assertIsNone(self.s.observe("u",1,10,"위험해요",True))

    def test_no_consent(self):
        self.assertIsNone(self.s.observe("u",1,10,"나는 슬퍼요",False))

    def test_oversize(self):
        with self.assertRaises(Rejected): self.s.observe("u",1,10,"a"*2049,True)

    def test_invalid_epoch(self):
        with self.assertRaises(Rejected): self.s.observe("u",True,10,"나는 슬퍼요",True)

    def test_invalid_time(self):
        with self.assertRaises(Rejected): self.s.observe("u",1,float("inf"),"나는 슬퍼요",True)
