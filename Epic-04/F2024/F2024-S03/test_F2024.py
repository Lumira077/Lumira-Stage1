import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2024(unittest.TestCase):
    def setUp(self):
        self.s=GestureSelector()

    def test_greeting(self):
        self.assertEqual(self.s.choose("greeting",.9,clearance=True)["gesture"],"wave")

    def test_agreement(self):
        self.assertEqual(self.s.choose("agreement",.9,clearance=True)["gesture"],"nod")

    def test_low_conf(self):
        self.assertEqual(self.s.choose("greeting",.2,clearance=True)["gesture"],"still")

    def test_quiet(self):
        self.assertEqual(self.s.choose("greeting",.9,clearance=True,quiet=True)["gesture"],"still")

    def test_clearance(self):
        self.assertEqual(self.s.choose("greeting",.9)["gesture"],"still")

    def test_stop(self):
        self.assertEqual(self.s.choose("greeting",.9,clearance=True,stop=True)["reason"],"stop")

    def test_untrusted_intent(self):
        self.assertEqual(self.s.choose("execute shell",.9,clearance=True)["gesture"],"still")

    def test_not_executable(self):
        self.assertFalse(self.s.choose("greeting",.9,clearance=True)["executable"])
