"""Synthetic sensor contracts and local perception prototypes; no camera/model/actuator IO."""
import math,re
from dataclasses import dataclass
class Rejected(ValueError):pass
def number(x,lo,hi):
 if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not lo<=x<=hi:raise Rejected('number')
 return float(x)
def token(x):
 if not isinstance(x,str) or not re.fullmatch('[A-Za-z0-9_-]{1,64}',x):raise Rejected('token')
 return x
@dataclass(frozen=True)
class Context:
 owner:str
 epoch:int
 def validate(self):
  token(self.owner)
  if isinstance(self.epoch,bool) or not isinstance(self.epoch,int) or self.epoch<0:raise Rejected('epoch')
  return self
class EpochScope:
 def __init__(self):self.ctx=None;self.watermark=-1
 def activate(self,ctx):
  ctx.validate()
  if ctx.epoch<=self.watermark:raise Rejected('replayed_epoch')
  self.ctx=ctx;self.watermark=ctx.epoch
 def scope(self,ctx):
  ctx.validate()
  if ctx!=self.ctx:raise Rejected('inactive_scope')
 def revoke(self,ctx):self.scope(ctx);self.ctx=None

def freshness(timestamp,now,ttl=1):
 t=number(timestamp,0,1e12);n=number(now,0,1e12);return 0<=n-t<=ttl
class FaceRegistry:
 """In-memory fixture embeddings only. A candidate is never authentication."""
 def __init__(self):self.templates={};self.epochs={};self.revoked=set()
 def _vector(self,v):
  if not isinstance(v,(tuple,list)) or len(v)!=8:raise Rejected('fixture_dimension')
  v=[number(x,-1,1) for x in v];norm=math.sqrt(sum(x*x for x in v))
  if norm<1e-8:raise Rejected('zero_vector')
  return tuple(x/norm for x in v)
 def enroll(self,owner,epoch,vector,version,consent,authorized,live):
  Context(owner,epoch).validate();token(version)
  if any(x is not True for x in (consent,authorized,live)):raise Rejected('enrollment_policy')
  if epoch<self.epochs.get(owner,-1) or (owner,epoch) in self.revoked:raise Rejected('old_epoch')
  v=self._vector(vector)
  if owner not in self.templates and len(self.templates)>=100:raise Rejected('capacity')
  self.templates[owner]=(epoch,version,v);self.epochs[owner]=epoch
 def revoke(self,owner,epoch):
  Context(owner,epoch).validate()
  if epoch<self.epochs.get(owner,-1):raise Rejected('old_epoch')
  self.templates.pop(owner,None);self.epochs[owner]=epoch;self.revoked.add((owner,epoch))
 def identify(self,vector,version,timestamp,now,consent,live,face_count=1):
  token(version)
  unknown={'candidate':None,'authenticated':False,'reason':'unknown'}
  if consent is not True or live is not True or not isinstance(face_count,int) or face_count!=1 or isinstance(face_count,bool):return unknown
  if not freshness(timestamp,now):return unknown
  v=self._vector(vector);rank=[]
  for owner,(epoch,model,t) in self.templates.items():
   if model==version:rank.append((sum(a*b for a,b in zip(v,t)),owner,epoch))
  rank.sort(reverse=True)
  if not rank or rank[0][0]<.9 or (len(rank)>1 and rank[0][0]-rank[1][0]<.15):return unknown
  return {'candidate':rank[0][1],'epoch':rank[0][2],'score':rank[0][0],'authenticated':False,'reason':'fixture_candidate'}
class GestureGate(EpochScope):
 ALLOWED=frozenset(('wave','point','open_palm','stop'))
 def __init__(self):super().__init__();self.last=-1;self.label=None;self.count=0;self.emitted=False
 def activate(self,ctx):super().activate(ctx);self.last=-1;self.label=None;self.count=0;self.emitted=False
 def observe(self,ctx,label,confidence,timestamp,now,consent):
  self.scope(ctx);t=number(timestamp,0,1e12);confidence=number(confidence,0,1)
  if t<=self.last:raise Rejected('repeated_or_reversed_frame')
  gap=t-self.last;self.last=t
  if consent is not True or not freshness(t,now) or confidence<.8 or label not in self.ALLOWED:
   self.label=None;self.count=0;self.emitted=False;return None
  if label!=self.label or gap>.5:self.label=label;self.count=1;self.emitted=False
  else:self.count+=1
  if self.count<3 or self.emitted:return None
  self.emitted=True
  return {'gesture':label,'scope':ctx,'kind':'interaction_candidate','executable':False,'safety_estop':False}
 @staticmethod
 def angle(a,b,c):
  if any(not isinstance(x,(list,tuple)) or len(x)!=2 for x in (a,b,c)):raise Rejected('points')
  a,b,c=([number(y,-1,1) for y in x] for x in (a,b,c))
  u=[a[i]-b[i] for i in range(2)];v=[c[i]-b[i] for i in range(2)]
  norm=math.hypot(*u)*math.hypot(*v)
  if norm<1e-8:raise Rejected('degenerate_pose')
  return math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(u,v))/norm))))
class TouchFSM(EpochScope):
 REGIONS=frozenset(('head','body','screen'))
 def __init__(self):super().__init__();self.press={};self.last=-1;self.seq=-1
 def activate(self,ctx):super().activate(ctx);self.press={};self.last=-1;self.seq=-1
 def revoke(self,ctx):super().revoke(ctx);self.press={}
 def event(self,ctx,seq,region,pressed,timestamp):
  self.scope(ctx);t=number(timestamp,0,1e12)
  if not isinstance(seq,int) or isinstance(seq,bool) or seq<=self.seq or t<self.last:raise Rejected('ordering')
  if region not in self.REGIONS or not isinstance(pressed,bool):raise Rejected('touch_schema')
  self.seq=seq;self.last=t
  if pressed:
   if region not in self.press:self.press[region]=t
   return None
  start=self.press.pop(region,None)
  if start is None:return None
  elapsed=t-start
  if elapsed<.05 or elapsed>10:return None
  return {'region':region,'kind':'long_press' if elapsed>=1 else 'tap','duration':elapsed,'executable':False}
class PresenceGate(EpochScope):
 def __init__(self):super().__init__();self.last=-1;self.count=0;self.proposed=None;self.state='unknown'
 def activate(self,ctx):super().activate(ctx);self.last=-1;self.count=0;self.proposed=None;self.state='unknown'
 def observe(self,ctx,score,timestamp,now,sensor_ready,consent):
  self.scope(ctx);t=number(timestamp,0,1e12);score=number(score,0,1)
  if t<=self.last:raise Rejected('frame_order')
  gap=t-self.last;self.last=t
  if sensor_ready is not True or consent is not True or not freshness(t,now):
   self.count=0;self.proposed=None;self.state='unknown';return self.state
  proposal='present' if score>=.8 else ('absent' if score<=.2 else None)
  if proposal is None:
   self.count=0;self.proposed=None
   if gap>1:self.state='unknown'
   return self.state
  if proposal!=self.proposed or gap>1:
   self.proposed=proposal;self.count=1
   if gap>1:self.state='unknown'
  else:self.count+=1
  if self.count>=3:self.state=proposal
  return self.state
class SpeakerAssociator:
 """Given audio direction and visual tracks -> tentative association, no voice ID."""
 def associate(self,ctx,doa,audio_time,tracks,now,vad,echo,consent):
  ctx.validate();doa=number(doa,-180,180)
  result={'track':None,'owner_authenticated':False,'reason':'unknown','executable':False}
  if vad is not True or echo is not False or consent is not True or not freshness(audio_time,now):return result
  if not isinstance(tracks,list) or len(tracks)>20:raise Rejected('tracks')
  candidates=[];seen=set()
  for track in tracks:
   if not isinstance(track,dict) or set(track)!={'id','epoch','angle_deg','quality','timestamp'}:raise Rejected('track_schema')
   Context(ctx.owner,track['epoch']).validate()
   tid=token(track['id'])
   if tid in seen:raise Rejected('duplicate_track')
   seen.add(tid)
   if track['epoch']!=ctx.epoch:raise Rejected('foreign_epoch')
   angle=number(track['angle_deg'],-180,180);quality=number(track['quality'],0,1)
   if not freshness(track['timestamp'],now) or abs(track['timestamp']-audio_time)>.2 or quality<.7:continue
   delta=abs((angle-doa+180)%360-180)
   if delta<=20:candidates.append((delta,tid))
  candidates.sort()
  if not candidates:return result
  if len(candidates)>1 and candidates[1][0]-candidates[0][0]<10:result['reason']='ambiguous';return result
  result.update(track=candidates[0][1],reason='direction_candidate');return result
class HeadAligner:
 """Bounded angular proposal from supplied DOA/normalized face offset, never motor IO."""
 def propose(self,ctx,yaw,dt,timestamp,now,doa=None,face_x=None,quality=1,clearance=False,stop=False):
  ctx.validate();yaw=number(yaw,-60,60);dt=number(dt,.01,.5);quality=number(quality,0,1)
  base={'target_yaw_deg':yaw,'executable':False,'reason':'hold','physical_stop_confirmed':False}
  if stop is not False or clearance is not True or quality<.7 or not freshness(timestamp,now):return base
  if face_x is not None:
   face_x=number(face_x,-1,1)
   error=math.degrees(math.atan(face_x*math.tan(math.radians(30))))
   if abs(error)<2:return base
   desired=yaw+.5*error;reason='visual_fixture'
  elif doa is not None:desired=number(doa,-180,180);reason='audio_fixture'
  else:return base
  desired=max(-60,min(60,desired));step=max(-30*dt,min(30*dt,desired-yaw))
  base.update(target_yaw_deg=yaw+step,reason=reason);return base
