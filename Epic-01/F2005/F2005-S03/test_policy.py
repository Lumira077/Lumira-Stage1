import unittest,copy
from policy import resolve,PolicySelection,CATALOG
from common import Rejected
class PolicyTests(unittest.TestCase):
    def p(self,sku='Home',mode='companion',quiet=False):return resolve(sku,mode,{'volume':80,'gesture_level':3,'expression_level':2},{'volume':20,'gesture_level':0,'expression_level':1},quiet)
    def test_five_skus(self):
        for sku in CATALOG:
            for mode in CATALOG[sku]['modes']:self.assertEqual(self.p(sku,mode)['sku'],sku)
    def test_unknown_sku(self):self.assertRaises(Rejected,self.p,'Hospital')
    def test_denied_mode(self):self.assertRaises(Rejected,self.p,'Pet','companion')
    def test_limits(self):self.assertEqual(self.p()['limits'],{'volume':20,'gesture_level':0,'expression_level':1})
    def test_quiet(self):self.assertEqual(self.p(quiet=True)['limits']['volume'],0)
    def test_consent_never_added(self):self.assertFalse(self.p()['cloud_allowed'])
    def test_nan_input(self):self.assertRaises(Rejected,resolve,'Home','pet',{'volume':float('nan')},{})
    def test_admin_required(self):self.assertRaises(Rejected,PolicySelection().apply,self.p())
    def test_guardian_required(self):self.assertRaises(Rejected,PolicySelection().apply,self.p('Kids'),True,False,('dialogue','ui','voice','motion'))
    def test_failed_apply_preserves_previous(self):
        s=PolicySelection();p=self.p();s.apply(p,True,False,('dialogue','ui','voice','motion'))
        self.assertRaises(Rejected,s.apply,self.p('Friend'),True,False,('voice',));self.assertEqual(s.value,p);self.assertEqual(s.revision,1)
    def test_caller_mutation_isolated(self):
        s=PolicySelection();p=self.p();s.apply(p,True,False,('dialogue','ui','voice','motion'));p['sku']='unknown';self.assertEqual(s.value['sku'],'Home')
