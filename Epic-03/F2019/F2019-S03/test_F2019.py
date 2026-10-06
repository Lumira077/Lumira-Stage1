import unittest
from core import *
def score(label="happy"):
 p=dict.fromkeys(LABELS,.025);p[label]=.9;return p
def obs(modality,**kw):
 d=dict(owner="u",epoch=1,modality=modality,timestamp=10,scores=score(),quality=1,model_version="fixture-v1");d.update(kw);return Observation(**d)

class TestF2019(unittest.TestCase):
    def setUp(self):
        self.t=TrendStore(ttl=60,capacity=3);self.t.activate("u",1,True);self.r=Fusion().combine("u",1,10,[obs("face"),obs("audio")],True)

    def test_append(self):
        self.assertTrue(self.t.append("u",1,10,"a",self.r))

    def test_duplicate(self):
        self.t.append("u",1,10,"a",self.r)
        self.assertFalse(self.t.append("u",1,10,"a",self.r))

    def test_minimum(self):
        self.t.append("u",1,10,"a",self.r)
        self.assertFalse(self.t.summary("u",1,10)["sufficient"])

    def test_capacity(self):
        for i in range(5):self.t.append("u",1,10,str(i),self.r)
        self.assertEqual(self.t.summary("u",1,10)["samples"],3)

    def test_ttl(self):
        self.t.append("u",1,10,"a",self.r)
        self.assertEqual(self.t.summary("u",1,71)["samples"],0)

    def test_foreign(self):
        with self.assertRaises(Rejected):self.t.summary("v",1,10)

    def test_foreign_result(self):
        self.t.activate("v",1,True)
        with self.assertRaises(Rejected):self.t.append("v",1,10,"a",self.r)

    def test_revoke(self):
        self.t.append("u",1,10,"a",self.r);self.t.activate("u",2,False)
        with self.assertRaises(Rejected):self.t.summary("u",1,10)

    def test_revoke_replay(self):
        self.t.activate("u",2,False)
        with self.assertRaises(Rejected):self.t.activate("u",1,True)
        with self.assertRaises(Rejected):self.t.activate("u",2,True)

    def test_new_epoch(self):
        self.t.append("u",1,10,"a",self.r);self.t.activate("u",2,True)
        self.assertEqual(self.t.summary("u",2,10)["samples"],0)

    def test_delete(self):
        self.t.delete("u",1)
        with self.assertRaises(Rejected):self.t.summary("u",1,10)

    def test_unknown(self):
        self.r["label"]="unknown";self.r["reason"]="conflict"
        self.assertFalse(self.t.append("u",1,10,"a",self.r))

    def test_no_raw(self):
        self.r["raw_text"]="fixture";self.t.append("u",1,10,"a",self.r)
        self.assertEqual(set(self.t.rows["u"][0]),{"id","timestamp","label"})

    def test_no_clinical_alert(self):
        r=self.t.summary("u",1,10)
        self.assertIsNone(r["clinical_risk"]);self.assertFalse(r["automatic_alert"])

    def test_stale_result(self):
        with self.assertRaises(Rejected):self.t.append("u",1,71,"a",self.r)
