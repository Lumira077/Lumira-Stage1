import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest,copy
from contract_core import *
class ContractTests(unittest.TestCase):
 def setUp(self):self.v=Validator('sprint1_demo');self.now=1000000000
 def safe(self,**kw):
  p=dict(estop=False,charging=False,sensors_valid=True,armed=True);p.update(kw)
  return envelope('safety_state',p,now=self.now)
 def gesture(self):return envelope('gesture_request',dict(gesture='nod',amplitude=.1),now=self.now)
 def test_nominal(self):self.v.accept(self.safe(),self.now);self.assertFalse(self.v.accept(self.gesture(),self.now)['hardware_execution'])
 def test_unknown_safety(self):
  with self.assertRaisesRegex(Reject,'safety_stale'):self.v.accept(self.gesture(),self.now)
 def test_stale_safety(self):
  self.v.accept(self.safe(),self.now);m=self.gesture();m['sent_monotonic_ns']+=101000000
  with self.assertRaisesRegex(Reject,'safety_stale'):self.v.accept(m,self.now+101000000)
 def test_estop(self):
  self.v.accept(self.safe(estop=True,armed=False),self.now)
  with self.assertRaisesRegex(Reject,'inhibited'):self.v.accept(self.gesture(),self.now)
 def test_charge(self):
  self.v.accept(self.safe(charging=True,armed=False),self.now)
  with self.assertRaisesRegex(Reject,'inhibited'):self.v.accept(self.gesture(),self.now)
 def test_duplicate(self):
  m=self.safe();self.v.accept(m,self.now)
  with self.assertRaisesRegex(Reject,'sequence'):self.v.accept(m,self.now)
 def test_expired(self):
  with self.assertRaisesRegex(Reject,'expired'):self.v.accept(self.safe(),self.now+201000000)
 def test_future(self):
  with self.assertRaisesRegex(Reject,'future'):self.v.accept(self.safe(),self.now-1)
 def test_foreign_session(self):
  m=self.safe();m['session']='foreign'
  with self.assertRaisesRegex(Reject,'scope'):self.v.accept(m,self.now)
 def test_bool_sequence(self):
  m=self.safe();m['seq']=True
  with self.assertRaisesRegex(Reject,'integer'):self.v.accept(m,self.now)
 def test_nan(self):
  self.v.accept(self.safe(),self.now);m=self.gesture();m['payload']['amplitude']=float('nan')
  with self.assertRaisesRegex(Reject,'number'):self.v.accept(m,self.now)
 def test_extra_field(self):
  m=self.safe();m['raw_audio']='forbidden'
  with self.assertRaisesRegex(Reject,'fields'):self.v.accept(m,self.now)
 def test_bad_joint_count(self):
  m=envelope('joint_states',dict(names=['joint_1'],position_rad=[0]),now=self.now)
  with self.assertRaisesRegex(Reject,'joints'):self.v.accept(m,self.now)
 def test_unsafe_arm(self):
  with self.assertRaisesRegex(Reject,'unsafe_arm'):self.v.accept(self.safe(estop=True),self.now)
 def test_disarmed(self):
  self.v.accept(self.safe(armed=False),self.now)
  with self.assertRaisesRegex(Reject,'inhibited'):self.v.accept(self.gesture(),self.now)
 def test_wrong_topic(self):
  m=self.safe();m['topic']='/real/motor'
  with self.assertRaisesRegex(Reject,'topic'):self.v.accept(m,self.now)
if __name__=='__main__':unittest.main()
