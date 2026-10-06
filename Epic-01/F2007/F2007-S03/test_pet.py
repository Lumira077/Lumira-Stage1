import unittest
from common import Context,Rejected
from pet import Pet
from policy import resolve
class PetTests(unittest.TestCase):
    def setUp(self):self.now=10;self.c=Context();self.c.reset('demo');self.p=Pet(self.c,lambda:self.now);self.policy=resolve('Pet','pet',{},{});self.e=self.c.epoch
    def event(self,id='ev',kind='touch',stamp=None,quiet=False):return self.p.event(id,kind,self.now if stamp is None else stamp,self.e,self.policy,quiet)
    def test_touch(self):self.assertEqual(self.event()['state'],'happy')
    def test_call(self):self.assertEqual(self.event(kind='call')['state'],'curious')
    def test_play(self):self.assertEqual(self.event(kind='play')['state'],'play')
    def test_duplicate(self):self.event();self.assertRaises(Rejected,self.event)
    def test_cooldown(self):self.event();self.assertTrue(self.event('ev2')['suppressed'])
    def test_stale(self):self.assertRaises(Rejected,self.event,'e','touch',4)
    def test_future(self):self.assertRaises(Rejected,self.event,'e','touch',11)
    def test_quiet(self):self.assertEqual(self.event(quiet=True)['state'],'rest')
    def test_stop_priority(self):self.event();self.assertTrue(self.event('ev2','stop')['cancel_required']);self.assertRaises(Rejected,self.event,'ev3')
    def test_rest_timer(self):self.event();self.now=40;self.assertEqual(self.p.tick(),'rest')
    def test_switch(self):self.c.reset('other');self.assertRaises(Rejected,self.event)
    def test_unknown(self):self.assertRaises(Rejected,self.event,'ev','unsafe-motion')
