import unittest
from common import Context,Rejected
from companion import Companion
from policy import resolve
class CompanionTests(unittest.TestCase):
    def setUp(self):self.c=Context();self.c.reset('demo');self.s=Companion(self.c);self.p=resolve('Friend','companion',{},{});self.e=self.c.epoch
    def plan(self,turn='turn',intent='greeting',quiet=False):return self.s.plan(turn,intent,self.e,self.p,quiet)
    def test_greeting(self):self.assertEqual(self.plan()['backend'],'local_template')
    def test_no_actions(self):self.assertEqual(self.plan()['executable_actions'],[])
    def test_duplicate(self):self.plan();self.assertRaises(Rejected,self.plan)
    def test_late_cloud_duplicate(self):self.plan();self.assertRaises(Rejected,self.s.late_backend,'turn',self.e)
    def test_cancel_stales(self):self.s.cancel();self.assertRaises(Rejected,self.plan)
    def test_switch_stales(self):self.c.reset('other');self.assertRaises(Rejected,self.plan)
    def test_stop(self):self.c.stop();self.assertRaises(Rejected,self.plan)
    def test_quiet(self):self.assertFalse(self.plan(quiet=True)['audible'])
    def test_end(self):self.plan(intent='end');self.assertEqual(self.s.state,'ending')
    def test_unknown_intent(self):self.assertRaises(Rejected,self.plan,'t','diagnose')
    def test_pet_denied(self):self.p=resolve('Pet','pet',{},{});self.assertRaises(Rejected,self.plan)
