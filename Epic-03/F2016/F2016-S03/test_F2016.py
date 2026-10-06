import unittest
from core import *
def score(label="happy"):
 p=dict.fromkeys(LABELS,.025);p[label]=.9;return p
def obs(modality,**kw):
 d=dict(owner="u",epoch=1,modality=modality,timestamp=10,scores=score(),quality=1,model_version="fixture-v1");d.update(kw);return Observation(**d)

class TestF2016(unittest.TestCase):
    def setUp(self):
        self.a=AudioFeatures();self.g=ObservationGate("audio")

    def test_rms(self):
        self.assertAlmostEqual(self.a.measure([.5,-.5])["rms"],.5)

    def test_crossings(self):
        self.assertEqual(self.a.measure([.5,-.5,.5])["zero_crossing_rate"],1)

    def test_silence(self):
        self.assertTrue(self.a.measure([0,0])["silence"])

    def test_clipping(self):
        self.assertTrue(self.a.measure([1,-1])["clipped"])

    def test_no_inference(self):
        self.assertFalse(self.a.measure([.5,-.5])["emotion_inferred"])

    def test_size(self):
        with self.assertRaises(Rejected): self.a.measure([])

    def test_range(self):
        with self.assertRaises(Rejected): self.a.measure([2,0])

    def test_nan(self):
        with self.assertRaises(Rejected): self.a.measure([float("nan"),0])

    def test_boolean(self):
        with self.assertRaises(Rejected): self.a.measure([True,0])

    def test_noise_quality(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("audio"),True,quality=.1))

    def test_overlap(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("audio"),True,sample_count=2))

    def test_accept(self):
        self.assertIsNotNone(self.g.accept("u",1,10,obs("audio"),True))
