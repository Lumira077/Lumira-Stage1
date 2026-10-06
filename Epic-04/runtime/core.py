"""Expression planning and offline SVG prototype. No audio, actuator or GPU driver."""
import math,copy,json,hashlib,re
from dataclasses import dataclass
class Rejected(ValueError):pass
def num(x,lo,hi):
 if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not lo<=x<=hi:raise Rejected('number')
 return float(x)
def token(x):
 if not isinstance(x,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',x):raise Rejected('token')
 return x
@dataclass(frozen=True)
class Context:
 owner:str
 epoch:int
 turn:str
 def validate(self):
  token(self.owner);token(self.turn)
  if isinstance(self.epoch,bool) or not isinstance(self.epoch,int) or self.epoch<0:raise Rejected('epoch')
  return self
EXPRESSIONS={'neutral':(0,0),'happy':(.7,.3),'sad':(-.5,-.3),'listening':(0,.2),'thinking':(.1,-.1),'speaking':(.3,.1)}
class FaceEngine:
 def pose(self,name,intensity=1):
  if name not in EXPRESSIONS:raise Rejected('expression')
  intensity=num(intensity,0,1);smile,brow=EXPRESSIONS[name]
  return {'expression':name,'smile':smile*intensity,'brow':brow*intensity,'mouth_open':0,'gaze_x':0,'gaze_y':0}
 def blend(self,a,b,t):
  t=num(t,0,1)
  return {k:num(a[k],-1,1)*(1-t)+num(b[k],-1,1)*t for k in ('smile','brow','mouth_open','gaze_x','gaze_y')}
 def svg(self,pose,color='#64d9ff'):
  if not isinstance(color,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',color):raise Rejected('color')
  vals={k:num(pose[k],-1,1) for k in ('smile','brow','gaze_x','gaze_y')};opening=num(pose['mouth_open'],0,1)
  x=vals['gaze_x']*12;y=vals['gaze_y']*8;curve=110+vals['smile']*25
  mouth=f'<ellipse cx="160" cy="111" rx="22" ry="{3+opening*20}"/>' if opening>.05 else f'<path d="M130 110 Q160 {curve} 190 110" fill="none" stroke="{color}" stroke-width="5"/>'
  return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><rect width="320" height="180" rx="30" fill="#071827"/><g fill="{color}"><ellipse cx="{110+x}" cy="{72+y}" rx="12" ry="18"/><ellipse cx="{210+x}" cy="{72+y}" rx="12" ry="18"/>{mouth}</g></svg>'
class TTSPlanner:
 VOICES={'demo-ko':('ko-KR',frozenset(('neutral','warm'))),'demo-en':('en-US',frozenset(('neutral','warm')))}
 def plan(self,ctx,text,voice,locale,style='neutral',rate=1,volume=.2,cloud=False,cloud_consent=False,quiet=False):
  ctx.validate()
  if not isinstance(text,str) or not 1<=len(text.strip())<=2048:raise Rejected('text')
  if voice not in self.VOICES or self.VOICES[voice][0]!=locale:raise Rejected('voice_locale')
  if cloud is True and cloud_consent is not True:raise Rejected('cloud_consent')
  if not isinstance(cloud,bool) or not isinstance(quiet,bool):raise Rejected('policy_type')
  rate=num(rate,.7,1.3);volume=num(volume,0,.5)
  style=style if style in self.VOICES[voice][1] else 'neutral'
  # No text retained in plan/log; actual TTS adapter must receive text separately.
  return {'context':ctx,'voice':voice,'locale':locale,'style':style,'rate':rate,'volume':0 if quiet else volume,'characters':len(text),
          'audio_generated':False,'alignment_available':False,'provider':'unconnected'}
class GestureLibrary:
 """Provisional joint limits for development validation; not a safety controller."""
 LIMITS={'neck':(-.5,.5,1),'arm':(-.7,.7,1),'waist':(-.3,.3,.5)}
 ASSETS={'nod':[(0,{'neck':0,'arm':0,'waist':0}),(.5,{'neck':.15,'arm':0,'waist':0}),(1,{'neck':0,'arm':0,'waist':0})],
 'wave':[(0,{'neck':0,'arm':0,'waist':0}),(1,{'neck':0,'arm':.3,'waist':0}),(2,{'neck':0,'arm':0,'waist':0})],
 'still':[(0,{'neck':0,'arm':0,'waist':0}),(1,{'neck':0,'arm':0,'waist':0})]}
 def validate(self,points):
  if not isinstance(points,list) or not 2<=len(points)<=1000:raise Rejected('points')
  prev=None
  for t,p in points:
   t=num(t,0,60)
   if set(p)!=set(self.LIMITS):raise Rejected('joints')
   for j,(lo,hi,v) in self.LIMITS.items():num(p[j],lo,hi)
   if prev:
    dt=t-prev[0]
    if dt<=0:raise Rejected('time_order')
    for j,(_,_,v) in self.LIMITS.items():
     if abs(p[j]-prev[1][j])/dt>v:raise Rejected('velocity')
   elif t!=0:raise Rejected('initial_time')
   prev=(t,p)
  return copy.deepcopy(points)
 def plan(self,name,clearance,current):
  if clearance is not True:raise Rejected('clearance')
  if name not in self.ASSETS:raise Rejected('gesture')
  points=self.validate(self.ASSETS[name])
  if not isinstance(current,dict) or set(current)!=set(self.LIMITS):raise Rejected('current_joints')
  # Explicitly demand matching start pose; a real measured-state bridge is pending.
  for j,(lo,hi,_) in self.LIMITS.items():
   if abs(num(current[j],lo,hi)-points[0][1][j])>1e-6:raise Rejected('start_pose')
  return {'points':points,'units':'radians','version':'fixture-v1','hardware_approved':False,'executable':False}
class Timeline:
 """One active context. Cues are proposals driven by given playback clock, not IO."""
 CHANNELS=frozenset(('face','audio','motion'))
 def __init__(self):self.ctx=None;self.queue=[];self.last=0;self.pending=set();self.generation=0
 def start(self,ctx):
  ctx.validate()
  if self.pending:raise Rejected('cancel_ack_pending')
  if self.ctx is not None:raise Rejected('active_turn')
  self.ctx=ctx;self.last=0;self.queue=[];self.generation+=1;return self.generation
 def add(self,ctx,generation,cue_id,channel,offset):
  if ctx!=self.ctx or generation!=self.generation:raise Rejected('stale_context')
  token(cue_id)
  if channel not in self.CHANNELS:raise Rejected('channel')
  offset=num(offset,0,60)
  if offset<self.last:raise Rejected('late_cue')
  if len(self.queue)>=1000 or any(c['id']==cue_id for c in self.queue):raise Rejected('queue')
  self.queue.append({'id':cue_id,'channel':channel,'offset':offset})
 def due(self,ctx,generation,playback):
  if ctx!=self.ctx or generation!=self.generation:raise Rejected('stale_context')
  playback=num(playback,0,60)
  if playback<self.last:raise Rejected('clock_reversal')
  self.last=playback;due=sorted([c for c in self.queue if c['offset']<=playback],key=lambda c:(c['offset'],c['id']))
  self.queue=[c for c in self.queue if c['offset']>playback]
  return due
 def cancel(self):
  if self.ctx is None:return {'generation':self.generation,'pending':sorted(self.pending),'physical_stop_confirmed':False}
  self.ctx=None;self.queue=[];self.generation+=1;self.pending=set(self.CHANNELS)
  return {'generation':self.generation,'pending':sorted(self.pending),'physical_stop_confirmed':False}
 def ack(self,generation,channel):
  if generation!=self.generation or channel not in self.pending:raise Rejected('ack')
  self.pending.remove(channel);return not self.pending
class GestureSelector:
 """Trusted semantic tags to limited proposals; no free-form LLM or motor execution."""
 def choose(self,intent,confidence,emotion='unknown',quiet=False,clearance=False,stop=False):
  if any(not isinstance(x,bool) for x in (quiet,clearance,stop)):raise Rejected('policy_type')
  confidence=num(confidence,0,1)
  if stop:return {'gesture':'still','reason':'stop','executable':False}
  if not clearance or quiet or confidence<.7:return {'gesture':'still','reason':'limited','executable':False}
  gestures={'greeting':'wave','agreement':'nod','comfort':'still'}
  return {'gesture':gestures.get(intent,'still'),'reason':'tag_fixture','executable':False}
class PerformancePlanner:
 def plan(self,asset,duration,repeats,rights,quiet,clearance,stop=False):
  if any(not isinstance(x,bool) for x in (rights,quiet,clearance,stop)):raise Rejected('policy_type')
  token(asset);duration=num(duration,0.1,60)
  if isinstance(repeats,bool) or not isinstance(repeats,int) or not 1<=repeats<=3:raise Rejected('repeat')
  if duration*repeats>120:raise Rejected('duration')
  if rights is not True:raise Rejected('rights_unverified')
  if stop or quiet or not clearance:return {'enabled':False,'reason':'policy','executable':False}
  return {'enabled':True,'asset':asset,'duration':duration*repeats,'rights_evidence':'trusted_fixture_only','executable':False}
class SkinRegistry:
 REQUIRED=frozenset(('neutral','happy','sad','listening','thinking','speaking'))
 def __init__(self):self.active=None
 @staticmethod
 def digest(asset):return hashlib.sha256(json.dumps(asset,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 def install(self,asset,expected_hash):
  # Validate the whole bundle before replacing last valid skin.
  if not isinstance(asset,dict) or set(asset)!={'id','version','color','states','rights'}:raise Rejected('asset_fields')
  token(asset['id']);token(asset['version'])
  if asset['rights'] is not True:raise Rejected('rights')
  if not isinstance(asset['color'],str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}',asset['color']):raise Rejected('color')
  if not isinstance(asset['states'],list) or len(asset['states'])!=len(self.REQUIRED) or set(asset['states'])!=self.REQUIRED:raise Rejected('states')
  if self.digest(asset)!=expected_hash:raise Rejected('hash')
  self.active=copy.deepcopy(asset);return copy.deepcopy(self.active)
class GazeLip:
 """Given viseme timing -> offline mouth/gaze pose. No audio alignment or tracking."""
 VISEMES={'closed':0,'small':.25,'open':.75}
 def pose(self,x,y,cues,playback,cancelled=False):
  if not isinstance(cancelled,bool):raise Rejected('cancelled')
  if cancelled:return {'gaze_x':0,'gaze_y':0,'mouth_open':0,'blink':False}
  x=num(x,-1,1);y=num(y,-1,1);playback=num(playback,0,60)
  if not isinstance(cues,list) or len(cues)>1000:raise Rejected('cues')
  last=-1;mouth=0
  for start,end,viseme in cues:
   start=num(start,0,60);end=num(end,0,60)
   if start<last or end<=start or viseme not in self.VISEMES:raise Rejected('alignment')
   last=end
   if start<=playback<end:mouth=self.VISEMES[viseme]
  return {'gaze_x':x,'gaze_y':y,'mouth_open':mouth,'blink':False}
class FaceResearchGate:
 """User/hardware measurements screening; no GPU renderer or production approval."""
 def assess(self,samples,fps,p95_ms,gpu_mb,discomfort,rights,privacy_review):
  if isinstance(samples,bool) or not isinstance(samples,int) or samples<0:raise Rejected('samples')
  fps=num(fps,0,1000);p95_ms=num(p95_ms,0,10000);gpu_mb=num(gpu_mb,0,100000);discomfort=num(discomfort,0,1)
  if not isinstance(rights,bool) or not isinstance(privacy_review,bool):raise Rejected('review_type')
  pending=[]
  for flag,name in [(samples>=20,'user_samples'),(fps>=30,'fps'),(p95_ms<=50,'latency'),(gpu_mb<=1024,'gpu_memory'),(discomfort<=.2,'discomfort'),(rights,'asset_rights'),(privacy_review,'privacy_review')]:
   if not flag:pending.append(name)
  return {'research_candidate':not pending,'pending':pending,'thresholds':'example_not_approved','production_enabled':False,'default':'character_2d'}
