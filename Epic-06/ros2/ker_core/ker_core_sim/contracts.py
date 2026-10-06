"""Development-only control contracts. Mock state changes never drive physical hardware."""
import math,re,copy
class Rejected(ValueError):pass
def num(x,lo,hi):
 if isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or not lo<=x<=hi:raise Rejected('number')
 return float(x)
def token(x):
 if not isinstance(x,str) or not re.fullmatch('[A-Za-z0-9_-]{1,64}',x):raise Rejected('token')
 return x
def fresh(t,now,ttl):return 0<=num(now,0,1e12)-num(t,0,1e12)<=ttl
class CommandGate:
 """Scoped generation/sequence/deadline check; SROS2/auth is not implemented."""
 def __init__(self):self.generation=0;self.seq=-1;self.active=False
 def activate(self):self.generation+=1;self.seq=-1;self.active=True;return self.generation
 def cancel(self):self.active=False;self.generation+=1
 def accept(self,packet,now):
  required={'robot','schema','generation','seq','timestamp','yaw'}
  if not isinstance(packet,dict) or set(packet)!=required:raise Rejected('schema')
  if not self.active or packet['robot']!='lumira_sim' or packet['schema']!='joint-v1' or packet['generation']!=self.generation:raise Rejected('scope')
  for k in ('generation','seq'):
   if isinstance(packet[k],bool) or not isinstance(packet[k],int) or packet[k]<0:raise Rejected('integer')
  if packet['seq']<=self.seq:raise Rejected('sequence')
  if not fresh(packet['timestamp'],now,.5):raise Rejected('deadline')
  yaw=num(packet['yaw'],-.5,.5)
  self.seq=packet['seq'];return {'yaw':yaw,'executable':False,'scope':'mock_only'}
class BoardHAL:
 """Capability registry and lifecycle of fake board; no real device discovery."""
 def __init__(self):self.state='unconfigured';self.profile=None
 def configure(self,profile):
  if self.state not in ('unconfigured','inactive'):raise Rejected('state')
  if not isinstance(profile,dict) or set(profile)!={'id','arch','capabilities','mode'}:raise Rejected('profile')
  token(profile['id'])
  if profile['arch'] not in ('x86_64','aarch64') or profile['mode']!='mock':raise Rejected('unsupported_hardware')
  if not isinstance(profile['capabilities'],list) or not set(profile['capabilities'])<=set(('camera','mic','touch','joint','power')):raise Rejected('capabilities')
  self.profile=copy.deepcopy(profile);self.state='inactive'
 def activate(self,required):
  if self.state!='inactive' or not set(required)<=set(self.profile['capabilities']):raise Rejected('missing_capability')
  self.state='active'
 def deactivate(self):
  if self.state!='active':raise Rejected('state')
  self.state='inactive'
 def fault(self):self.state='error'
 def cleanup(self):
  if self.state=='active':raise Rejected('active_cleanup')
  self.state='unconfigured';self.profile=None
class MockMotor:
 """Bounded position state simulator with software latch/watchdog; not a safe drive."""
 def __init__(self):self.position=0;self.target=0;self.enabled=False;self.latched=False;self.last_command=None;self.last_tick=None
 def enable(self):
  if self.latched:raise Rejected('latched')
  self.enabled=True
 def command(self,target,now):
  now=num(now,0,1e12);target=num(target,-.5,.5)
  if not self.enabled or self.latched:raise Rejected('disabled')
  if self.last_command is not None and now<self.last_command:raise Rejected('clock_reversal')
  self.target=target;self.last_command=now
 def tick(self,now):
  now=num(now,0,1e12)
  if self.last_tick is not None and now<self.last_tick:raise Rejected('clock_reversal')
  dt=0 if self.last_tick is None else min(.1,now-self.last_tick);self.last_tick=now
  if not self.enabled or self.latched:return self.position
  if self.last_command is None or now-self.last_command>.5:
   self.stop();return self.position
  self.position+=max(-dt,min(dt,self.target-self.position));return self.position
 def stop(self):self.enabled=False;self.latched=True;self.target=self.position
 def reset(self,operator_ack,feedback_zero):
  if operator_ack is not True or feedback_zero is not True:raise Rejected('reset_evidence')
  self.latched=False;self.enabled=False;self.target=self.position;self.last_command=None
class SensorSynchronizer:
 """Bounded metadata samples from an already-common clock; no clock calibration."""
 def __init__(self):self.samples={};self.last={};self.epoch=0
 def reset(self):self.samples={};self.last={};self.epoch+=1;return self.epoch
 def update(self,source,seq,timestamp,now,epoch):
  if source not in ('camera','audio','touch','imu'):raise Rejected('source')
  if epoch!=self.epoch or isinstance(epoch,bool):raise Rejected('epoch')
  if not isinstance(seq,int) or isinstance(seq,bool) or seq<=self.last.get(source,-1):raise Rejected('sequence')
  if not fresh(timestamp,now,.5):raise Rejected('stale')
  t=num(timestamp,0,1e12)
  if source in self.samples and t<self.samples[source]['timestamp']:raise Rejected('clock_reversal')
  self.samples[source]={'seq':seq,'timestamp':t};self.last[source]=seq
 def pair(self,a,b,now):
  if a==b:raise Rejected('distinct_sources')
  if a not in self.samples or b not in self.samples:return None
  x,y=self.samples[a],self.samples[b]
  if not fresh(x['timestamp'],now,.5) or not fresh(y['timestamp'],now,.5) or abs(x['timestamp']-y['timestamp'])>.05:return None
  del self.samples[a];del self.samples[b]
  return {'sources':[a,b],'seq':[x['seq'],y['seq']],'skew':abs(x['timestamp']-y['timestamp']),'epoch':self.epoch}
class PowerPolicy:
 """Given BMS metadata -> conservative software proposal; never charging control."""
 def assess(self,soc,temperature,current,charging,timestamp,now,bms_ok):
  soc=num(soc,0,1);temperature=num(temperature,-40,120);current=num(current,-100,100)
  if not isinstance(charging,bool):raise Rejected('charging')
  r={'mode':'normal','motion_allowed':True,'charge_requested':False,'hardware_action':None}
  if bms_ok is not True or not fresh(timestamp,now,2):r.update(mode='unknown',motion_allowed=False);return r
  if temperature>=60 or abs(current)>=20:r.update(mode='fault',motion_allowed=False)
  elif soc<=.1:r.update(mode='shutdown_requested',motion_allowed=False)
  elif soc<=.2:r.update(mode='low_power',motion_allowed=False)
  elif charging:r.update(mode='charging',motion_allowed=False)
  return r
class Diagnostics:
 """Allowlisted fault metadata and heartbeat assessment; no hardware watchdog."""
 CODES={'E_COMM':'communication','E_THERMAL':'thermal','E_POWER':'power','E_STOP':'stop'}
 def __init__(self):self.beats={};self.faults={}
 def heartbeat(self,device,timestamp):
  token(device);t=num(timestamp,0,1e12)
  if t<self.beats.get(device,-1):raise Rejected('clock')
  if device not in self.beats and len(self.beats)>=100:raise Rejected('capacity')
  self.beats[device]=t
 def fault(self,device,code):
  token(device)
  if code not in self.CODES:raise Rejected('fault_code')
  if device not in self.faults and len(self.faults)>=100:raise Rejected('capacity')
  self.faults.setdefault(device,set()).add(code)
 def clear(self,device,operator_ack,healthy):
  if operator_ack is not True or healthy is not True:raise Rejected('clear_evidence')
  self.faults.pop(device,None)
 def report(self,now,required):
  now=num(now,0,1e12)
  if not isinstance(required,list) or len(required)>100:raise Rejected('required')
  for d in required:token(d)
  stale=[d for d in required if d not in self.beats or not fresh(self.beats[d],now,1)]
  return {'stale':stale,'faults':{d:sorted(c) for d,c in self.faults.items()},'healthy':not stale and not self.faults,'hardware_stop_confirmed':False}
class Orchestrator:
 """Placement and stale-result checks; fake adapters only, no GPU/cloud provider."""
 def __init__(self):self.generation=0;self.tasks={}
 def cancel(self):self.generation+=1;self.tasks={}
 def route(self,task,kind,privacy,consent,network,budget,local_ready,edge_ready):
  token(task)
  if task in self.tasks or len(self.tasks)>=100:raise Rejected('task')
  if kind not in ('control','dialogue','perception') or privacy not in ('public','private'):raise Rejected('classification')
  for x in (consent,network,local_ready,edge_ready):
   if not isinstance(x,bool):raise Rejected('policy_type')
  budget=num(budget,0,1e9)
  if kind=='control':place='local' if local_ready else 'blocked'
  elif privacy=='private' or not consent:place='edge' if edge_ready else ('local' if local_ready else 'blocked')
  elif kind=='perception' and edge_ready:place='edge'
  elif network and budget>0:place='cloud'
  else:place='local' if local_ready else ('edge' if edge_ready else 'blocked')
  r={'task':task,'generation':self.generation,'place':place,'actual_calls':0}
  if place!='blocked':self.tasks[task]=r.copy()
  return r
 def complete(self,task,generation,place):
  if generation!=self.generation or task not in self.tasks or place!=self.tasks[task]['place']:raise Rejected('stale_or_foreign_result')
  del self.tasks[task];return {'accepted':True,'hardware_execution':False}
