"""Sensor-event planner only. No motor/network transport. Thresholds require commissioning."""
import math,json
from pathlib import Path
DEFAULT={'fresh_ms':500,'hold_confirm_ms':250,'release_confirm_ms':350,'near_stop_m':.25,'gaze_confidence':.7,'gaze_limit_deg':30,'gaze_deadband_deg':3}
class Interaction:
 def __init__(self,config=None):
  self.c=DEFAULT|dict(config or {});self.held=set();self.pending={};self.releasing={};self.latched=False;self.last_gaze=0.;self.last_time=-1;self.greeted=False;self.pressure_active=set()
 def output(self,state,face='neutral',speech='',neck=None,event=None):
  return {'state':state,'event':event,'face':face,'speech_ko':speech,'neck_target_deg':neck,'arm_mode':{s:'CONTACT_YIELD_REQUEST' if s in self.held|self.pressure_active else 'NO_NEW_MOTION' for s in ['left','right']},'waist_mode':'NO_NEW_MOTION','wheel_command':'STOP','motor_output_enabled':False,'contact_compliance_requires_hardware_controller':bool(self.held|self.pressure_active)}
 def stop(self,reason):
  self.latched=True;r=self.output('STOP_LATCHED',event=reason);r['arm_mode']={'left':'STOP_REQUEST','right':'STOP_REQUEST'};return r
 def step(self,s,now_ms):
  if not isinstance(now_ms,(int,float)) or not math.isfinite(now_ms) or now_ms<self.last_time:return self.stop('invalid_clock')
  self.last_time=now_ms
  try:
   age=now_ms-s['ts_ms'];distance=s['distance_m'];hands=s['hands']
   assert set(hands)=={'left','right'}
   assert math.isfinite(age) and -50<=age<=self.c['fresh_ms']
   assert isinstance(s['estop'],bool) and isinstance(s['edge'],bool) and isinstance(s['collision'],bool)
   assert isinstance(distance,(int,float)) and not isinstance(distance,bool) and math.isfinite(distance) and distance>=0
   for side in ['left','right']:
    h=hands[side];assert h['valid'] is True
    for k in ['touch','pressure_contact','overload']:assert isinstance(h[k],bool)
  except (KeyError,TypeError,AssertionError,ValueError):return self.stop('invalid_or_stale_sensors')
  if s['estop'] or s['edge'] or s['collision'] or distance<self.c['near_stop_m'] or any(hands[x]['overload'] for x in hands):return self.stop('safety_input')
  if self.latched:
   if s.get('reset_stop') is True and not any(hands[x]['pressure_contact'] for x in ['left','right']):
    self.latched=False;self.pressure_active.clear();self.held.clear();self.pending.clear();self.releasing.clear();return self.output('RESET_IDLE',event='explicit_reset')
   return self.stop('awaiting_explicit_reset')
  self.pressure_active={x for x in ['left','right'] if hands[x]['pressure_contact']}
  new=[];released=[]
  for side in ['left','right']:
   contact=hands[side]['pressure_contact']
   if contact:
    self.releasing.pop(side,None)
    if side not in self.held:
     self.pending.setdefault(side,now_ms)
     if now_ms-self.pending[side]>=self.c['hold_confirm_ms']:self.held.add(side);new.append(side);self.pending.pop(side,None)
   else:
    self.pending.pop(side,None)
    if side in self.held:
     self.releasing.setdefault(side,now_ms)
     if now_ms-self.releasing[side]>=self.c['release_confirm_ms']:self.held.remove(side);released.append(side);self.releasing.pop(side,None)
  if new:return self.output('HAND_HELD','affection','손을 잡아 주셨네요. 반가워요.',neck=0 if len(self.held)==2 else (-15 if 'left'in self.held else 15),event='hold_started')
  if self.held:return self.output('HAND_HELD','affection',event='hold_continues')
  if released:return self.output('RELEASE_WAIT','grateful','고마워요.',event='released_no_retraction')
  if any(hands[x]['pressure_contact'] for x in hands):return self.output('CONTACT_CONFIRMING','listening')
  if any(hands[x]['touch'] for x in hands):return self.output('LIGHT_TOUCH','happy')
  cam=s.get('camera')
  if isinstance(cam,dict):
   try:
    age=now_ms-cam['ts_ms'];conf=cam.get('confidence',0.);bearing=cam['bearing_deg']
    if all(math.isfinite(v) for v in [age,conf,bearing]) and -50<=age<=self.c['fresh_ms'] and (cam.get('quality_pass') is True or conf>=self.c['gaze_confidence']):
     target=max(-self.c['gaze_limit_deg'],min(self.c['gaze_limit_deg'],bearing))
     neck=target if abs(target-self.last_gaze)>=self.c['gaze_deadband_deg'] else None
     if neck is not None:self.last_gaze=target
     speech='' if self.greeted else '안녕하세요. 만나서 반가워요.';self.greeted=True
     return self.output('ATTEND_USER','happy',speech,neck,event='camera_target')
   except (KeyError,TypeError,ValueError):pass
  return self.output('IDLE')
if __name__=='__main__':
 import sys
 config=Path(__file__).resolve().parents[1]/'config/interaction.json'
 p=Interaction(json.loads(config.read_text()) if config.exists() else None)
 for line in sys.stdin:
  x=json.loads(line);print(json.dumps(p.step(x,x['now_ms']),ensure_ascii=False),flush=True)
