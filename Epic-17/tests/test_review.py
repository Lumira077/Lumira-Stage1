import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from core import *

class ReviewTest(unittest.TestCase):
 def test_dialogue(self):
  s=State()
  for e in ['start','process','reply']:s=reduce(s,e)
  self.assertEqual(s.mode,'speaking')
  self.assertEqual(reduce(s,'stop').mode,'idle')
 def test_interlocks(self):
  for k in ['charging','estop','cliff']:
   with self.subTest(k=k):
    s=reduce(State(),k,True);self.assertEqual(reduce(s,'move').mode,'idle')
    self.assertFalse(presentation(s)['hardware_executable'])
 def test_clearing_does_not_restart(self):
  for k in ['charging','estop','cliff']:
   s=reduce(State(mode='move_proposal'),k,True);s=reduce(s,k,False)
   self.assertEqual(s.mode,'idle')
 def test_mute(self):
  s=reduce(State(mode='speaking'),'mute');self.assertEqual(s.mode,'idle')
  self.assertEqual(presentation(s)['face'],'muted')
  self.assertEqual(reduce(s,'start').mode,'idle')
 def test_disconnect(self):
  s=reduce(State(mode='speaking'),'connected',False)
  self.assertEqual(s.mode,'idle');self.assertEqual(reduce(s,'move').mode,'idle')
 def test_charging_conversation_still_possible(self):
  s=reduce(State(charging=True),'start');self.assertEqual(s.mode,'listening')
  self.assertEqual(presentation(s)['gesture'],'hold')
 def test_bad_inputs(self):
  for v in [True,-1,101,1.5]:
   with self.assertRaises(ValueError):reduce(State(),'volume',v)
  with self.assertRaises(ValueError):reduce(State(),'estop',1)
 def test_sequence(self):
  self.assertEqual(reduce(State(),'reply').mode,'idle')
  self.assertEqual(reduce(State(),'process').mode,'idle')
 def row(self,id='a',**extra):
  return dict(participant_id=id,task_id='UC1',consent=True,withdrawn=False,completed=True,assistance_count=0,duration_s=20,**extra)
 def test_metrics_consent(self):
  a=self.row();b=self.row('b');b['consent']=False;c=self.row('c');c['withdrawn']=True
  m=study_metrics([a,b,c]);self.assertEqual(m['denominator'],1)
 def test_metrics_denominator(self):
  a=self.row();b=self.row('b');b.update(completed=False,duration_s=None,assistance_count=2)
  m=study_metrics([a,b]);self.assertEqual(m['success_rate'],.5);self.assertEqual(m['duration_denominator'],1)
 def test_no_observations(self):
  self.assertIsNone(study_metrics([])['success_rate'])
 def test_duplicate(self):
  with self.assertRaises(ValueError):study_metrics([self.row(),self.row()])
 def test_invalid_metrics(self):
  for k,v in [('duration_s',float('nan')),('assistance_count',-1),('completed','true')]:
   r=self.row();r[k]=v
   with self.assertRaises(ValueError):study_metrics([r])
 def test_ab(self):
  orders=[ab_order(i)[0] for i in range(20)]
  self.assertEqual(orders.count('character'),10);self.assertEqual(orders.count('real'),10)
 def test_freeze_blocks_missing(self):
  self.assertFalse(freeze_readiness([],[])['ready_for_human_review'])
 def assets(self):
  return [dict(name=n,revision='R1',evidence_type='review_approval',reviewed=True,evidence_ref='fixture:'+n,reviewer='synthetic-reviewer') for n in ('cad','bom','cmf','ui','harness','physical_test','usability')]
 def test_freeze_never_approves(self):
  r=freeze_readiness(self.assets(),[]);self.assertTrue(r['ready_for_human_review']);self.assertFalse(r['release_approved'])
 def test_freeze_draft(self):
  a=self.assets();a[0]['evidence_type']='draft';self.assertFalse(freeze_readiness(a,[])['ready_for_human_review'])
 def test_freeze_revision(self):
  a=self.assets();a[1]['revision']='R2';self.assertFalse(freeze_readiness(a,[])['ready_for_human_review'])
 def test_freeze_issue(self):
  self.assertFalse(freeze_readiness(self.assets(),[dict(id='bad',severity='major',state='open')])['ready_for_human_review'])
 def test_overlap(self):
  z=[dict(id='vent',box=[0,0,0,10,10,10])]
  self.assertEqual(accessory_overlap([9,9,9,11,11,11],z)['state'],'conflict')
  self.assertEqual(accessory_overlap([10,10,10,11,11,11],z)['state'],'conflict')
  self.assertEqual(accessory_overlap([11,11,11,12,12,12],z)['state'],'no_aabb_overlap')
 def test_unknown_never_safe(self):
  self.assertFalse(accessory_overlap(None,[])['safe'])
  self.assertEqual(accessory_overlap([0,0,0,1,1,1],[dict(id='vent',box=None)])['state'],'unknown')
 def test_bad_box(self):
  with self.assertRaises(ValueError):accessory_overlap([0,0,0,0,1,1],[])

if __name__=='__main__':unittest.main()
