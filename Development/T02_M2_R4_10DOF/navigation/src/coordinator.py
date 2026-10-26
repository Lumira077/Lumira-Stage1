"""Single offline arbitration point for hand interaction and navigation. No device output."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from interaction import Interaction
from navigation import Navigator
class Coordinator:
 def __init__(self,grid,pose):self.interaction=Interaction();self.navigation=Navigator(grid,pose)
 def step(self,interaction_snapshot,navigation_snapshot,now_ms,command=None):
  reply=self.interaction.step(interaction_snapshot,now_ms);s=dict(navigation_snapshot)
  s['hands_held']=bool(self.interaction.held or self.interaction.pressure_active)
  if reply['state']=='STOP_LATCHED':s['estop']=True
  if reply['state']=='RESET_IDLE':s['reset_stop']=True
  if command and reply['state'] not in ['STOP_LATCHED','HAND_HELD','CONTACT_CONFIRMING'] and not s['hands_held']:
   if command.get('mode')=='SOLO':self.navigation.start_solo(command['goal_xy'])
   elif command.get('mode')=='FOLLOW':self.navigation.start_follow(command['target_id'])
   elif command.get('mode')=='STOP':self.navigation.mode='IDLE'
  motion=self.navigation.step(s)
  if motion['state'].endswith('MOVING'):
   reply['arm_mode']={'left':'STOWED_NO_GESTURE','right':'STOWED_NO_GESTURE'}
  return {'interaction':reply,'navigation':motion,'motor_output_enabled':False,'command_source':'local_test_only; authenticated app transport not implemented'}
