"""Sprint1 mock-only envelope validation. No robot I/O and no hardware safety claim."""
import math,time,json
SCHEMA='sprint1-v0.1'
PREFIX='/ker/sim/sprint1/'
TOPICS={'dialogue_event','expression_state','gesture_request','joint_states','safety_state'}
class Reject(ValueError):pass
def number(v,lo,hi):
 if type(v) not in (int,float) or not math.isfinite(v) or not lo<=v<=hi:raise Reject('number')
def exact(d,keys):
 if type(d)!=dict or set(d)!=set(keys):raise Reject('fields')
class Validator:
 def __init__(self,session):self.session=session;self.seq={};self.safety=None;self.safety_at=None
 def accept(self,m,now=None):
  now=time.monotonic_ns() if now is None else now
  if len(json.dumps(m,allow_nan=True).encode())>4096:raise Reject('size')
  exact(m,['schema','session','seq','sent_monotonic_ns','ttl_ms','topic','payload'])
  if m['schema']!=SCHEMA or m['session']!=self.session:raise Reject('scope')
  t=m['topic']
  if type(t)!=str or not t.startswith(PREFIX) or t[len(PREFIX):] not in TOPICS:raise Reject('topic')
  for k in ['seq','sent_monotonic_ns','ttl_ms']:
   if type(m[k])!=int or m[k]<0:raise Reject('integer')
  if not 1<=m['ttl_ms']<=200:raise Reject('ttl')
  if not 0<=now-m['sent_monotonic_ns']<=m['ttl_ms']*1000000:raise Reject('expired_or_future')
  if m['seq']<=self.seq.get(t,-1):raise Reject('sequence')
  kind=t[len(PREFIX):];p=m['payload']
  if kind=='safety_state':
   exact(p,['estop','charging','sensors_valid','armed'])
   if any(type(x)!=bool for x in p.values()):raise Reject('boolean')
   if p['armed'] and (p['estop'] or p['charging'] or not p['sensors_valid']):raise Reject('unsafe_arm')
  elif kind=='dialogue_event':
   exact(p,['event','request_id'])
   if p['event'] not in ['listening','thinking','speaking','cancel','error']:raise Reject('event')
   if type(p['request_id'])!=str or not 1<=len(p['request_id'])<=64:raise Reject('request_id')
  elif kind=='expression_state':
   exact(p,['state','intensity'])
   if p['state'] not in ['IDLE','LISTENING','THINKING','SPEAKING','ERROR']:raise Reject('state')
   number(p['intensity'],0,1)
  elif kind=='gesture_request':
   exact(p,['gesture','amplitude'])
   if p['gesture'] not in ['nod','greet','neutral']:raise Reject('gesture')
   number(p['amplitude'],0,0.3)
   if self.safety is None or not 0<=now-self.safety_at<=100000000:raise Reject('safety_stale')
   if self.safety['estop'] or self.safety['charging'] or not self.safety['armed'] or not self.safety['sensors_valid']:raise Reject('inhibited')
  else:
   exact(p,['names','position_rad'])
   if p['names']!=['joint_'+str(i) for i in range(1,10)] or type(p['position_rad'])!=list or len(p['position_rad'])!=9:raise Reject('joints')
   for v in p['position_rad']:number(v,-0.5,0.5)
  self.seq[t]=m['seq']
  if kind=='safety_state':self.safety=p.copy();self.safety_at=m['sent_monotonic_ns']
  return {'accepted':True,'hardware_execution':False,'topic':kind}
def envelope(topic,payload,seq=0,session='sprint1_demo',now=None):
 return dict(schema=SCHEMA,session=session,seq=seq,sent_monotonic_ns=time.monotonic_ns() if now is None else now,ttl_ms=200,topic=PREFIX+topic,payload=payload)
def fixtures():
 return [('safety_state',dict(estop=False,charging=False,sensors_valid=True,armed=True)),('dialogue_event',dict(event='speaking',request_id='example_01')),('expression_state',dict(state='SPEAKING',intensity=0.4)),('gesture_request',dict(gesture='nod',amplitude=0.1)),('joint_states',dict(names=['joint_'+str(i) for i in range(1,10)],position_rad=[0.0]*9)),('safety_state',dict(estop=True,charging=False,sensors_valid=True,armed=False)),('gesture_request',dict(gesture='greet',amplitude=0.1))]
