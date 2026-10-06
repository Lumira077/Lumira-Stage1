import unittest
from core import *
def score(label="happy"):
 p=dict.fromkeys(LABELS,.025);p[label]=.9;return p
def obs(modality,**kw):
 d=dict(owner="u",epoch=1,modality=modality,timestamp=10,scores=score(),quality=1,model_version="fixture-v1");d.update(kw);return Observation(**d)

class TestF2018(unittest.TestCase):
    def setUp(self):
        self.f=Fusion()

    def test_agreement(self):
        r=self.f.combine("u",1,10,[obs("face"),obs("audio")],True)
        self.assertEqual(r["label"],"happy");self.assertIsNone(r["action"])

    def test_missing(self):
        self.assertEqual(self.f.combine("u",1,10,[obs("face")],True)["label"],"unknown")

    def test_empty(self):
        self.assertEqual(self.f.combine("u",1,10,[],True)["label"],"unknown")

    def test_conflict(self):
        self.assertEqual(self.f.combine("u",1,10,[obs("face"),obs("audio",scores=score("sad"))],True)["reason"],"conflict")

    def test_time_skew(self):
        self.assertEqual(self.f.combine("u",1,10,[obs("face"),obs("audio",timestamp=9.5)],True)["reason"],"time_skew")

    def test_stale(self):
        self.assertEqual(self.f.combine("u",1,13,[obs("face"),obs("audio")],True)["label"],"unknown")

    def test_foreign(self):
        with self.assertRaises(Rejected): self.f.combine("v",1,10,[obs("face"),obs("audio")],True)

    def test_epoch(self):
        with self.assertRaises(Rejected): self.f.combine("u",2,10,[obs("face"),obs("audio")],True)

    def test_duplicate(self):
        with self.assertRaises(Rejected): self.f.combine("u",1,10,[obs("face"),obs("face")],True)

    def test_no_consent(self):
        self.assertEqual(self.f.combine("u",1,10,[obs("face"),obs("audio")],False)["reason"],"no_consent")

    def test_normalised(self):
        self.assertAlmostEqual(sum(self.f.combine("u",1,10,[obs("face"),obs("audio",quality=.5)],True)["scores"].values()),1)

    def test_evidence_no_raw(self):
        r=self.f.combine("u",1,10,[obs("face"),obs("audio")],True)
        self.assertEqual(set(r["evidence"][0]),{"modality","version","quality","origin"})
