"""Offline 2D differential-drive planner. Sensor fusion/SLAM and motor transport are not implemented."""
import heapq,math
import numpy as np
from scipy.ndimage import distance_transform_edt
RES=.1;RADIUS=.27;DT=.1

def wrap(x):return (x+math.pi)%(2*math.pi)-math.pi
class Grid:
 def __init__(self,occ):
  self.occ=np.asarray(occ,bool);self.free=distance_transform_edt(~self.occ)*RES>RADIUS+RES*math.sqrt(2)/2
 def cell(self,p):return (int(p[1]/RES),int(p[0]/RES))
 def valid(self,p):
  y,x=self.cell(p);return 0<=y<self.free.shape[0] and 0<=x<self.free.shape[1] and self.free[y,x]
 def path(self,start,goal):
  a=self.cell(start);b=self.cell(goal)
  if not self.valid(start) or not self.valid(goal):return []
  q=[(0,a)];cost={a:0};prev={};visited=set()
  while q:
   _,u=heapq.heappop(q)
   if u in visited:continue
   visited.add(u)
   if u==b:
    out=[u]
    while out[-1]!=a:out.append(prev[out[-1]])
    return [((x+.5)*RES,(y+.5)*RES) for y,x in out[::-1]]
   for dy,dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
    v=(u[0]+dy,u[1]+dx);y,x=v
    if not (0<=y<self.free.shape[0] and 0<=x<self.free.shape[1] and self.free[y,x]):continue
    if dx and dy and (not self.free[u[0],x] or not self.free[y,u[1]]):continue
    nc=cost[u]+math.hypot(dx,dy)
    if nc<cost.get(v,float('inf')):cost[v]=nc;prev[v]=u;heapq.heappush(q,(nc+math.hypot(y-b[0],x-b[1]),v))
  return []
class Navigator:
 def __init__(self,grid,pose):
  self.grid=grid;self.pose=np.array(pose,float);self.mode='IDLE';self.goal=None;self.target_id=None;self.latched=False;self.follow_wait=False;self.path=[]
 def start_solo(self,goal):self.mode='SOLO';self.goal=tuple(goal);self.path=[]
 def start_follow(self,target_id):
  if not target_id:raise ValueError('explicit target required')
  self.mode='FOLLOW';self.target_id=target_id;self.follow_wait=False;self.path=[]
 def result(self,state,v=0,w=0):return {'state':state,'v_m_s':float(v),'w_rad_s':float(w),'motor_output_enabled':False,'pose':self.pose.tolist()}
 def step(self,s):
  try:return self._step(s)
  except (KeyError,ValueError,TypeError,IndexError,OverflowError):
   self.latched=True;return self.result('INVALID_SENSOR_STOP')
 def _step(self,s):
  required=['sensor_age_s','localization_ok','estop','cliff','bumper','hands_held','arms_stowed','perception_ok','camera_hazard']
  if any(k not in s for k in required):self.latched=True;return self.result('INVALID_SENSOR_STOP')
  if any(not isinstance(s[k],bool) for k in required if k!='sensor_age_s'):self.latched=True;return self.result('INVALID_SENSOR_STOP')
  if not math.isfinite(s['sensor_age_s']) or s['sensor_age_s']<0 or s['sensor_age_s']>.3:self.latched=True
  danger=s['estop'] or s['cliff'] or s['bumper'] or not s['localization_ok'] or not s['perception_ok'] or s['camera_hazard']
  if danger:self.latched=True
  if self.latched:
   if s.get('reset_stop') is True and not danger and 0<=s['sensor_age_s']<=.3 and not s['hands_held'] and s['arms_stowed']:
    self.latched=False;self.mode='IDLE';return self.result('RESET_IDLE')
   return self.result('STOP_LATCHED')
  if s['hands_held'] or not s['arms_stowed']:
   self.mode='IDLE';self.path=[];return self.result('CONTACT_OR_ARM_STOP')
  if self.mode=='IDLE':return self.result('IDLE')
  goal=self.goal
  if self.mode=='FOLLOW':
   t=s.get('target');valid=bool(t and t.get('id')==self.target_id and 0<=t.get('age_s',99)<=.3 and t.get('quality_pass') is True)
   if not valid:self.follow_wait=True;return self.result('TARGET_LOST_WAIT')
   if self.follow_wait:
    if not s.get('resume_follow'):return self.result('TARGET_RECONFIRM_WAIT')
    self.follow_wait=False
   target=np.array(t['xy'],float)
   if target.shape!=(2,) or not np.isfinite(target).all():self.follow_wait=True;return self.result('TARGET_INVALID_WAIT')
   delta=target-self.pose[:2];dist=float(np.linalg.norm(delta))
   if dist>3:self.follow_wait=True;return self.result('TARGET_TOO_FAR_WAIT')
   if dist<=1.2:return self.result('FOLLOW_DISTANCE_HOLD')
   person_path=self.grid.path(self.pose[:2],target)
   if not person_path:return self.result('BLOCKED_STOP')
   remaining=1.1;goal=np.array(person_path[0])
   for a,b in zip(person_path[::-1],person_path[-2::-1]):
    aa=np.array(a);bb=np.array(b);length=float(np.linalg.norm(bb-aa))
    if remaining<=length:goal=aa+(bb-aa)*remaining/length;break
    remaining-=length
  if goal is None:return self.result('NO_GOAL')
  if np.linalg.norm(np.array(goal)-self.pose[:2])<.18:
   if self.mode=='SOLO':self.mode='IDLE';return self.result('ARRIVED')
   return self.result('FOLLOW_DISTANCE_HOLD')
  self.path=self.grid.path(self.pose[:2],goal)
  if not self.path:return self.result('BLOCKED_STOP')
  waypoint=np.array(self.path[0])
  for point in self.path[1:8]:
   candidate=np.array(point);length=np.linalg.norm(candidate-self.pose[:2])
   if length>.45:break
   if all(self.grid.valid(self.pose[:2]*(1-a)+candidate*a) for a in np.linspace(0,1,max(2,int(length/.015)+1))):waypoint=candidate
   else:break
  heading=math.atan2(waypoint[1]-self.pose[1],waypoint[0]-self.pose[0]);err=wrap(heading-self.pose[2]);w=float(np.clip(2*err,-.6,.6));v=0 if abs(err)>.5 else .2*max(0,math.cos(err));nextpose=self.pose.copy();nextpose[0]+=v*math.cos(self.pose[2]+w*DT/2)*DT;nextpose[1]+=v*math.sin(self.pose[2]+w*DT/2)*DT;nextpose[2]=wrap(self.pose[2]+w*DT)
  if not all(self.grid.valid(self.pose[:2]*(1-a)+nextpose[:2]*a) for a in np.linspace(0,1,5)):
   self.pose[2]=wrap(self.pose[2]+w*DT);return self.result('ROTATE_CLEARANCE',0,w)
  self.pose=nextpose;return self.result(self.mode+'_MOVING',v,w)

def sensors():return {'sensor_age_s':.01,'localization_ok':True,'estop':False,'cliff':False,'bumper':False,'hands_held':False,'arms_stowed':True,'perception_ok':True,'camera_hazard':False}


def wheel_rates(v,w,track_m,radius_m):
 """Kinematic conversion only; measured wheel radius and track are mandatory."""
 if radius_m is None or not all(math.isfinite(x) for x in [v,w,track_m,radius_m]) or radius_m<=0 or track_m<=0:raise ValueError('wheel calibration required')
 return {'left_rad_s':(v-w*track_m/2)/radius_m,'right_rad_s':(v+w*track_m/2)/radius_m}
