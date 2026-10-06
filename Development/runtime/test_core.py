import unittest,hashlib
from datetime import datetime,timezone,timedelta
from core import *

class Navigation(unittest.TestCase):
 def test_shortest_detour(self):
  g=[[0,1,0],[0,1,0],[0,0,0]];p=grid_path(g,(0,0),(2,0));self.assertEqual(len(p),7);self.assertTrue(all(g[y][x]==0 for x,y in p))
 def test_unknown_blocks(self):self.assertIsNone(grid_path([[0,-1,0]],(0,0),(2,0)))
 def test_invalid(self):
  for g,s,t in [([[0],[0,0]],(0,0),(0,1)),([[0]],(True,0),(0,0)),([[1]],(0,0),(0,0))]:
   with self.assertRaises(ValueError):grid_path(g,s,t)
 def test_same_cell(self):self.assertEqual(grid_path([[0]],(0,0),(0,0)),[(0,0)])
class Manipulation(unittest.TestCase):
 def test_unknown(self):self.assertEqual(grasp_proposal(None,1,'unknown',0,2)['action'],'request_support')
 def test_two_hands(self):self.assertEqual(grasp_proposal(1.5,1,'robust',0,2)['action'],'two_hand_proposal')
 def test_limit(self):self.assertEqual(grasp_proposal(1,1,'fragile',2,2)['action'],'stop_proposal')
 def test_slip(self):self.assertEqual(grasp_proposal(1,1,'fragile',1,2,True)['action'],'regrasp_proposal')
 def test_no_actuation(self):self.assertFalse(grasp_proposal(1,1,'robust',0,2)['executable'])
 def test_nan(self):
  with self.assertRaises(ValueError):grasp_proposal(float('nan'),1,'robust',0,2)
class Care(unittest.TestCase):
 def setUp(self):self.t=datetime(2026,1,1,tzinfo=timezone.utc)
 def test_reminder_dedup(self):
  r=Reminder();self.assertTrue(r.due('a',self.t,self.t,True));self.assertFalse(r.due('a',self.t,self.t,True))
 def test_time_and_consent(self):
  r=Reminder();self.assertFalse(r.due('a',self.t,self.t-timedelta(seconds=1),True));self.assertFalse(r.due('a',self.t,self.t,False))
 def test_timezone(self):
  with self.assertRaises(ValueError):Reminder().due('a',self.t.replace(tzinfo=None),self.t,True)
 def test_low_quality(self):self.assertIsNone(wellness_value(70,.1,.8,True)['value'])
 def test_no_consent(self):self.assertIsNone(wellness_value(70,.9,.8,False)['value'])
 def test_no_medical_claim(self):self.assertFalse(wellness_value(70,.9,.8,True)['medical_validated'])
class Kids(unittest.TestCase):
 def setUp(self):self.a=[{'id':'a','min_age':5,'max_age':8,'approved':True,'licensed':True}]
 def test_approved(self):self.assertEqual(kids_catalog(self.a,6,True,10),['a'])
 def test_age(self):self.assertEqual(kids_catalog(self.a,10,True,10),[])
 def test_parent(self):self.assertEqual(kids_catalog(self.a,6,False,10),[])
 def test_limit(self):self.assertEqual(kids_catalog(self.a,6,True,0),[])
 def test_unlicensed(self):self.a[0]['licensed']=False;self.assertEqual(kids_catalog(self.a,6,True,10),[])
class App(unittest.TestCase):
 def test_conflict(self):
  s=VersionedSettings();s.patch(0,{'quiet':True})
  with self.assertRaises(ValueError):s.patch(0,{'quiet':False})
  self.assertTrue(s.data['quiet'])
 def test_invalid_atomic(self):
  s=VersionedSettings()
  with self.assertRaises(ValueError):s.patch(0,{'quiet':True,'minutes':-1})
  self.assertEqual(s.data,{})
 def test_copy(self):
  s=VersionedSettings();a=['a'];s.patch(0,{'content_ids':a});a.append('b');self.assertEqual(s.data['content_ids'],['a'])
 def test_unknown(self):
  with self.assertRaises(ValueError):VersionedSettings().patch(0,{'password':'raw'})
class Cloud(unittest.TestCase):
 def setUp(self):self.blob=b'fixture';self.m={'version':2,'board':'mock','expires':10,'sha256':hashlib.sha256(self.blob).hexdigest()}
 def test_proposal_only(self):
  r=ota_preflight(self.blob,self.m,1,'mock',1,True,True,True);self.assertTrue(r['eligible_proposal']);self.assertFalse(r['install_performed']);self.assertFalse(r['cryptographic_signature_verified'])
 def test_digest(self):self.assertFalse(ota_preflight(b'bad',self.m,1,'mock',1,True,True,True)['eligible_proposal'])
 def test_downgrade(self):self.assertFalse(ota_preflight(self.blob,self.m,2,'mock',1,True,True,True)['eligible_proposal'])
 def test_expired(self):self.assertFalse(ota_preflight(self.blob,self.m,1,'mock',10,True,True,True)['eligible_proposal'])
 def test_wrong_board(self):self.assertFalse(ota_preflight(self.blob,self.m,1,'other',1,True,True,True)['eligible_proposal'])
 def test_power_and_signature(self):
  self.assertFalse(ota_preflight(self.blob,self.m,1,'mock',1,True,False,True)['eligible_proposal']);self.assertFalse(ota_preflight(self.blob,self.m,1,'mock',1,True,True)['eligible_proposal'])
class Security(unittest.TestCase):
 def setUp(self):self.p={'tenant':'t','owner':'o','epoch':2,'expires':10,'consent':True,'actions':['read']};self.r={'tenant':'t','owner':'o','epoch':2}
 def test_allowed(self):self.assertTrue(scoped_access(self.p,self.r,'read',1))
 def test_tenant(self):self.r['tenant']='x';self.assertFalse(scoped_access(self.p,self.r,'read',1))
 def test_revoke(self):self.r['epoch']=3;self.assertFalse(scoped_access(self.p,self.r,'read',1))
 def test_expiry(self):self.assertFalse(scoped_access(self.p,self.r,'read',10))
 def test_no_consent(self):self.p['consent']=False;self.assertFalse(scoped_access(self.p,self.r,'read',1))
 def test_raw_allowlist(self):self.assertEqual(minimal_event({'code':'secret text','component':'core','result':'accepted','raw':'PII','seq':1}),{'component':'core','result':'accepted','seq':1})
class Billing(unittest.TestCase):
 def test_retry(self):l=UsageLedger(10);l.charge('a',3);self.assertEqual(l.charge('a',3),3)
 def test_conflict(self):
  l=UsageLedger(10);l.charge('a',3)
  with self.assertRaises(ValueError):l.charge('a',4)
 def test_quota_atomic(self):
  l=UsageLedger(2)
  with self.assertRaises(ValueError):l.charge('a',3)
  self.assertEqual(l.used,0)
 def test_refund_replay(self):l=UsageLedger(10);l.charge('a',3);l.refund('a');l.refund('a');self.assertEqual(l.charge('a',3),0)
 def test_invalid_units(self):
  for v in (True,-1,0,1.2):
   with self.assertRaises(ValueError):UsageLedger(10).charge('a',v)
class Home(unittest.TestCase):
 def test_allowlist(self):self.assertTrue(scene_proposal([{'device':'lamp','action':'on'}],{'lamp':['on']})['eligible_proposal'])
 def test_unknown(self):self.assertFalse(scene_proposal([{'device':'lock','action':'unlock'}],{})['eligible_proposal'])
 def test_sensitive(self):self.assertFalse(scene_proposal([{'device':'lock','action':'unlock'}],{'lock':['unlock']})['eligible_proposal'])
 def test_no_execution(self):self.assertFalse(scene_proposal([{'device':'lamp','action':'on'}],{'lamp':['on']})['executable'])
class Hardware(unittest.TestCase):
 def setUp(self):self.p={'id':'a','supply_v':5,'min_v':4,'max_v':6,'kind':'COTS','reviewed':True}
 def test_ratings(self):self.p['supply_v']=24;self.assertIn('voltage:a',bom_review([self.p])['issues'])
 def test_duplicate(self):self.assertIn('duplicate:a',bom_review([self.p,self.p])['issues'])
 def test_gate(self):self.p['reviewed']=False;self.assertIn('review:a',bom_review([self.p])['issues'])
 def test_no_manufacturing(self):self.assertFalse(bom_review([self.p])['manufacturing_approved'])
class IP(unittest.TestCase):
 def setUp(self):self.t=datetime(2026,1,1,tzinfo=timezone.utc)
 def test_unverified(self):self.assertEqual(docket_review([{'id':'x'}],self.t)[0]['state'],'needs_counsel_verification')
 def test_overdue(self):self.assertEqual(docket_review([{'id':'x','counsel_verified':True,'source_ref':'fixture','due':'2025-01-01T00:00:00+00:00'}],self.t)[0]['state'],'overdue')
 def test_no_auto_filing(self):self.assertFalse(docket_review([{'id':'x'}],self.t)[0]['filing_performed'])
class Finance(unittest.TestCase):
 def test_cash(self):self.assertEqual(cashflow('100',[{'receipts':'20','payments':'30'}])['closing_cash'],['90'])
 def test_negative(self):self.assertEqual(cashflow('0',[{'receipts':'0','payments':'10'}])['negative_months'],[1])
 def test_exact(self):self.assertEqual(cashflow('0.1',[{'receipts':'0.2','payments':'0'}])['closing_cash'],['0.3'])
 def test_no_nan(self):
  with self.assertRaises(ValueError):cashflow('NaN',[])
 def test_dilution(self):self.assertEqual(dilution(100,25),'0.2')
class Sales(unittest.TestCase):
 def test_dedup(self):e={'id':'a','stage':'lead','consent':True};self.assertEqual(funnel([e,e])['counts']['lead'],1)
 def test_consent(self):self.assertEqual(funnel([{'id':'a','stage':'lead','consent':False}])['counts']['lead'],0)
 def test_conflict(self):
  with self.assertRaises(ValueError):funnel([{'id':'a','stage':'lead','consent':True},{'id':'a','stage':'order','consent':True}])
if __name__=='__main__':unittest.main()
