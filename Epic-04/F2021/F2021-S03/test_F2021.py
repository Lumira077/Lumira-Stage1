import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2021(unittest.TestCase):
    def setUp(self):
        self.t=TTSPlanner()

    def test_plan(self):
        r=self.t.plan(C,"안녕하세요","demo-ko","ko-KR")
        self.assertFalse(r["audio_generated"]);self.assertNotIn("text",r)

    def test_locale(self):
        with self.assertRaises(Rejected):self.t.plan(C,"hello","demo-ko","en-US")

    def test_voice(self):
        with self.assertRaises(Rejected):self.t.plan(C,"hello","clone-person","en-US")

    def test_style(self):
        self.assertEqual(self.t.plan(C,"안녕","demo-ko","ko-KR",style="angry")["style"],"neutral")

    def test_quiet(self):
        self.assertEqual(self.t.plan(C,"안녕","demo-ko","ko-KR",quiet=True)["volume"],0)

    def test_cloud(self):
        with self.assertRaises(Rejected):self.t.plan(C,"안녕","demo-ko","ko-KR",cloud=True)

    def test_volume(self):
        with self.assertRaises(Rejected):self.t.plan(C,"안녕","demo-ko","ko-KR",volume=1)

    def test_text_limit(self):
        with self.assertRaises(Rejected):self.t.plan(C,"a"*2049,"demo-ko","ko-KR")

    def test_rate(self):
        with self.assertRaises(Rejected):self.t.plan(C,"안녕","demo-ko","ko-KR",rate=float("inf"))
