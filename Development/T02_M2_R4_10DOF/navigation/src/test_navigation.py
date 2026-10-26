import unittest,numpy as np
from navigation import Grid,Navigator,sensors,wheel_rates
class Tests(unittest.TestCase):
 def nav(self):
  a=np.zeros((40,60),bool);a[:2]=a[-2:]=True;a[:,:2]=a[:,-2:]=True;return Navigator(Grid(a),(1,1,0))
 def test_idle(self):self.assertEqual(self.nav().step(sensors())['v_m_s'],0)
 def test_solo_arrives(self):
  n=self.nav();n.start_solo((2,1));states=[n.step(sensors())['state'] for _ in range(150)];self.assertIn('ARRIVED',states)
 def test_lost_target_stops(self):
  n=self.nav();n.start_follow('user1');s=sensors();r=n.step(s);self.assertEqual(r['v_m_s'],0);self.assertEqual(r['state'],'TARGET_LOST_WAIT')
 def test_wrong_user_rejected(self):
  n=self.nav();n.start_follow('user1');s=sensors();s['target']={'id':'other','age_s':0,'quality_pass':True,'xy':[2,1]};self.assertEqual(n.step(s)['state'],'TARGET_LOST_WAIT')
 def test_hand_stops_and_cancels(self):
  n=self.nav();n.start_solo((3,1));s=sensors();s['hands_held']=True;self.assertEqual(n.step(s)['v_m_s'],0);self.assertEqual(n.step(sensors())['state'],'IDLE')
 def test_hazard_latched(self):
  n=self.nav();s=sensors();s['cliff']=True;n.step(s);self.assertEqual(n.step(sensors())['state'],'STOP_LATCHED')
 def test_stale_stops(self):
  n=self.nav();s=sensors();s['sensor_age_s']=1;self.assertEqual(n.step(s)['v_m_s'],0);self.assertTrue(n.latched)
 def test_camera_hazard_stops(self):
  n=self.nav();s=sensors();s['camera_hazard']=True;self.assertEqual(n.step(s)['state'],'STOP_LATCHED')
 def test_dynamic_blocked_goal(self):
  n=self.nav();n.start_solo((3,1));a=n.grid.occ.copy();a[8:13,28:33]=True;n.grid=Grid(a);self.assertEqual(n.step(sensors())['state'],'BLOCKED_STOP')
 def test_bad_input(self):self.assertEqual(self.nav().step({})['state'],'INVALID_SENSOR_STOP')
 def test_wheel_calibration_required(self):
  with self.assertRaises(ValueError):wheel_rates(.1,.1,.334,None)
 def test_extended_arms(self):
  n=self.nav();n.start_solo((3,1));s=sensors();s['arms_stowed']=False;self.assertEqual(n.step(s)['v_m_s'],0)
if __name__=='__main__':unittest.main()
