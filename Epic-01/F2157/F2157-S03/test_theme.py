import unittest
from common import Context,Rejected
from theme import Theme,MODULES
class ThemeTests(unittest.TestCase):
    def setUp(self):self.now=10;self.c=Context();self.c.reset('demo');self.t=Theme(self.c,lambda:self.now);self.e=self.c.epoch
    def prep(self,outfit='outfit-blue',seq=1,sku='Home',allowed=True):return self.t.prepare(outfit,seq,self.e,sku,allowed)
    def apply(self):
        p=self.prep();return self.t.commit(p,{m:dict(p) for m in MODULES})
    def test_registered(self):self.assertEqual(self.apply()['theme'],'blue')
    def test_two_outfits(self):
        self.apply();p=self.prep('outfit-sun',2);self.assertEqual(self.t.commit(p,{m:dict(p) for m in MODULES})['theme'],'sun')
    def test_unknown_default(self):self.apply();self.assertRaises(Rejected,self.prep,'url-executable',2);self.assertEqual(self.t.value,'default')
    def test_user_denied(self):self.assertRaises(Rejected,self.prep,'outfit-blue',1,'Home',False)
    def test_model_denied(self):self.assertRaises(Rejected,self.prep,'outfit-blue',1,'Kids')
    def test_partial_ack(self):p=self.prep();self.assertRaises(Rejected,self.t.commit,p,{'face':p});self.assertEqual(self.t.value,'default')
    def test_wrong_receipt(self):p=self.prep();a={m:dict(p) for m in MODULES};a['voice']['theme']='other';self.assertRaises(Rejected,self.t.commit,p,a)
    def test_late_sequence(self):self.apply();self.assertRaises(Rejected,self.prep,'outfit-sun',1)
    def test_remove(self):self.apply();self.assertEqual(self.t.remove(),'default')
    def test_presence_expire(self):self.apply();self.now=13;self.assertEqual(self.t.tick(),'default')
    def test_sensor_failure(self):self.apply();self.assertEqual(self.t.tick(False),'default')
    def test_epoch_change(self):self.apply();self.c.reset('other');self.assertEqual(self.t.tick(),'default')
    def test_stale_commit(self):p=self.prep();self.c.reset('other');self.assertRaises(Rejected,self.t.commit,p,{m:p for m in MODULES})
    def test_nan_ttl(self):self.assertRaises(Rejected,self.t.prepare,'outfit-blue',1,self.e,'Home',True,float('nan'))
    def test_timeout_during_prepare(self):p=self.prep();self.now=13;self.assertRaises(Rejected,self.t.commit,p,{m:p for m in MODULES})
