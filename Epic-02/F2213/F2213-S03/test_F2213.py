import unittest
from core import *

class TestF2213(unittest.TestCase):
    def setUp(self):
        self.s=QualityTelemetry();self.row={"provider":"openai_sample","status":"ok","latency_ms":10,"usage_tokens":5,"cost_units":2}

    def test_counts(self):
        self.s.record(self.row);self.s.record(self.row);self.assertEqual(self.s.snapshot()["operations"],2)

    def test_no_raw_text(self):
        self.row["text"]="private";self.assertRaises(Rejected,self.s.record,self.row)

    def test_nan(self):
        self.row["latency_ms"]=float("nan");self.assertRaises(Rejected,self.s.record,self.row)

    def test_negative_usage(self):
        self.row["usage_tokens"]=-1;self.assertRaises(Rejected,self.s.record,self.row)

    def test_empty(self):
        self.assertIsNone(self.s.snapshot()["p95_ms"])

    def test_quantile(self):
        self.s.record(self.row);self.row["latency_ms"]=50;self.row["status"]="error";self.s.record(self.row);self.assertEqual(self.s.snapshot()["p95_ms"],50);self.assertEqual(self.s.snapshot()["success_rate"],.5)
