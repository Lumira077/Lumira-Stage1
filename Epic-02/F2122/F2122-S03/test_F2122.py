import unittest
from core import *

class TestF2122(unittest.TestCase):
    def setUp(self):
        self.s=LocalModelGate();self.m={"runtime":"llama.cpp","model_hash":"a"*64,"ram_required_mb":1000,"hardware":"cpu-lab"}

    def test_admission_not_inference(self):
        self.assertFalse(self.s.validate(self.m,2000,40)["inference_executed"])

    def test_ram(self):
        self.assertRaises(Rejected,self.s.validate,self.m,1000,40)

    def test_thermal(self):
        self.assertRaises(Rejected,self.s.validate,self.m,2000,70)

    def test_bad_hash(self):
        self.m["model_hash"]="not-a-hash";self.assertRaises(Rejected,self.s.validate,self.m,2000,40)

    def test_unsupported_runtime(self):
        self.m["runtime"]="arbitrary_exec";self.assertRaises(Rejected,self.s.validate,self.m,2000,40)

    def test_tool_denied(self):
        self.assertRaises(Rejected,self.s.propose,"open-door")

    def test_tool_proposal(self):
        self.assertFalse(self.s.propose("stop")["executed"])
