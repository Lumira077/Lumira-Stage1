import unittest
from core import *

class TestF2121(unittest.TestCase):
    def setUp(self):
        self.s=LocalCommands()

    def test_korean_stop(self):
        self.assertEqual(self.s.parse("정지")["intent"],"stop")

    def test_english_stop(self):
        self.assertEqual(self.s.parse(" STOP ")["intent"],"stop")

    def test_proposal_not_executed(self):
        self.assertFalse(self.s.parse("개인정보 삭제")["executed"])

    def test_no_substring_command(self):
        self.assertEqual(self.s.parse("정지하지 마세요")["intent"],"unsupported")

    def test_local(self):
        self.assertFalse(self.s.parse("status")["cloud_required"])

    def test_unsupported(self):
        self.assertEqual(self.s.parse("open the door")["intent"],"unsupported")
