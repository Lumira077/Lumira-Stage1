import unittest,numpy as np
from navigation import Grid,sensors
from coordinator import Coordinator
from test_interaction import sample
class Tests(unittest.TestCase):
 def test_hand_input_overrides_mission(self):
  a=np.zeros((40,60),bool);a[:2]=a[-2:]=True;a[:,:2]=a[:,-2:]=True;c=Coordinator(Grid(a),(1,1,0))
  c.step(sample(0),sensors(),0,{'mode':'SOLO','goal_xy':[3,1]})
  r=c.step(sample(100,True),sensors(),100)
  self.assertEqual(r['navigation']['v_m_s'],0);self.assertEqual(r['navigation']['state'],'CONTACT_OR_ARM_STOP');self.assertFalse(r['motor_output_enabled'])
 def test_interaction_fault_overrides_mission(self):
  a=np.zeros((40,60),bool);c=Coordinator(Grid(a),(1,1,0));s=sample(0);s['hands']['left']['valid']=False;r=c.step(s,sensors(),0,{'mode':'SOLO','goal_xy':[3,1]});self.assertEqual(r['navigation']['state'],'STOP_LATCHED')
if __name__=='__main__':unittest.main()
