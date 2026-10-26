import unittest,copy
from interaction import Interaction

def sample(t=0,hold=False):
 h={'valid':True,'touch':False,'pressure_contact':False,'overload':False}
 s={'ts_ms':t,'estop':False,'edge':False,'collision':False,'distance_m':.6,'hands':{'left':h.copy(),'right':h.copy()}}
 s['hands']['left']['pressure_contact']=hold;return s
class Tests(unittest.TestCase):
 def test_debounce(self):
  p=Interaction();self.assertEqual(p.step(sample(0,True),0)['state'],'CONTACT_CONFIRMING');self.assertEqual(p.step(sample(100,False),100)['state'],'IDLE')
 def test_hold_and_release(self):
  p=Interaction();p.step(sample(0,True),0);r=p.step(sample(250,True),250);self.assertEqual(r['event'],'hold_started');self.assertEqual(r['arm_mode']['left'],'CONTACT_YIELD_REQUEST');self.assertFalse(r['motor_output_enabled'])
  self.assertEqual(p.step(sample(300,True),300)['speech_ko'],'');p.step(sample(400,False),400);self.assertEqual(p.step(sample(750,False),750)['event'],'released_no_retraction')
 def test_stop_priority(self):
  p=Interaction();s=sample(0,True);s['estop']=True;self.assertEqual(p.step(s,0)['state'],'STOP_LATCHED')
 def test_no_automatic_restart(self):
  p=Interaction();s=sample();s['edge']=True;p.step(s,0);self.assertEqual(p.step(sample(10),10)['state'],'STOP_LATCHED');s=sample(20);s['reset_stop']=True;self.assertEqual(p.step(s,20)['state'],'RESET_IDLE')
 def test_stale(self):self.assertEqual(Interaction().step(sample(0),1000)['state'],'STOP_LATCHED')
 def test_camera_clamp(self):
  s=sample();s['camera']={'ts_ms':0,'confidence':.9,'bearing_deg':70};self.assertEqual(Interaction().step(s,0)['neck_target_deg'],30)
 def test_missing_camera_no_motion(self):self.assertIsNone(Interaction().step(sample(),0)['neck_target_deg'])
 def test_overload(self):
  s=sample();s['hands']['right']['overload']=True;self.assertEqual(Interaction().step(s,0)['state'],'STOP_LATCHED')
 def test_invalid_sensor(self):
  s=sample();s['hands']['left']['valid']=False;self.assertEqual(Interaction().step(s,0)['state'],'STOP_LATCHED')
 def test_both_hands(self):
  p=Interaction();s=sample(0,True);s['hands']['right']['pressure_contact']=True;p.step(s,0);s['ts_ms']=250;r=p.step(s,250);self.assertEqual(r['neck_target_deg'],0);self.assertTrue(all(v=='CONTACT_YIELD_REQUEST' for v in r['arm_mode'].values()))
if __name__=='__main__':unittest.main()
