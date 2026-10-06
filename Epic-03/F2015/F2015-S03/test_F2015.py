import unittest
from core import *
def score(label="happy"):
 p=dict.fromkeys(LABELS,.025);p[label]=.9;return p
def obs(modality,**kw):
 d=dict(owner="u",epoch=1,modality=modality,timestamp=10,scores=score(),quality=1,model_version="fixture-v1");d.update(kw);return Observation(**d)

class TestF2015(unittest.TestCase):
    def setUp(self):
        self.g=ObservationGate("face")

    def test_accept(self):
        self.assertIsNotNone(self.g.accept("u",1,10,obs("face"),True))

    def test_consent(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("face"),False))

    def test_foreign(self):
        with self.assertRaises(Rejected): self.g.accept("v",1,10,obs("face"),True)

    def test_epoch(self):
        with self.assertRaises(Rejected): self.g.accept("u",2,10,obs("face"),True)

    def test_stale(self):
        self.assertIsNone(self.g.accept("u",1,13,obs("face"),True))

    def test_future(self):
        self.assertIsNone(self.g.accept("u",1,9,obs("face"),True))

    def test_multiple_faces(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("face"),True,sample_count=2))

    def test_poor_lighting(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("face"),True,quality=.2))

    def test_low_confidence(self):
        self.assertIsNone(self.g.accept("u",1,10,obs("face",scores=dict.fromkeys(LABELS,.2)),True))

    def test_nan(self):
        with self.assertRaises(Rejected): self.g.accept("u",1,10,obs("face",quality=float("nan")),True)

    def test_probability_sum(self):
        with self.assertRaises(Rejected): self.g.accept("u",1,10,obs("face",scores=dict.fromkeys(LABELS,.9)),True)

    def test_version(self):
        with self.assertRaises(Rejected): self.g.accept("u",1,10,obs("face",model_version=""),True)

    def test_schema(self):
        with self.assertRaises(Rejected): self.g.accept("u",1,10,obs("face",schema="v0"),True)
