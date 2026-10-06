"""Offline prototypes only. No robot, notification, payment, filing or outreach I/O."""
import math, heapq, hashlib, re
from datetime import datetime, timezone
from decimal import Decimal

def number(x, lo=None, hi=None):
    if type(x) not in (int,float) or not math.isfinite(x): raise ValueError('finite number required')
    if lo is not None and x<lo or hi is not None and x>hi: raise ValueError('range')
    return x

def integer(x,lo=0,hi=10**12):
    if type(x) is not int or not lo<=x<=hi:raise ValueError('integer range')
    return x

def grid_path(grid,start,goal):
    """4-connected BFS/A* on <=4096 point cells; unknown/obstacles blocked. No footprint or cmd_vel."""
    if not isinstance(grid,list) or not grid or not isinstance(grid[0],list) or not grid[0]:raise ValueError('grid')
    w=len(grid[0]);h=len(grid)
    if w*h>4096 or any(not isinstance(r,list) or len(r)!=w or any(type(v)is not int or v not in (-1,0,1) for v in r) for r in grid):raise ValueError('grid')
    def valid(p):return type(p) in (tuple,list) and len(p)==2 and all(type(i)is int for i in p) and 0<=p[0]<w and 0<=p[1]<h and grid[p[1]][p[0]]==0
    if not valid(start) or not valid(goal):raise ValueError('blocked/out-of-map endpoint')
    start,goal=tuple(start),tuple(goal);q=[(0,0,start)];cost={start:0};parent={}
    while q:
        _,g,p=heapq.heappop(q)
        if g!=cost[p]:continue
        if p==goal:
            out=[p]
            while out[-1]!=start:out.append(parent[out[-1]])
            return list(reversed(out))
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            v=(p[0]+dx,p[1]+dy)
            if valid(v) and g+1<cost.get(v,10**9):
                cost[v]=g+1;parent[v]=p;heapq.heappush(q,(g+1+abs(v[0]-goal[0])+abs(v[1]-goal[1]),g+1,v))
    return None

def grasp_proposal(mass,capacity,fragility,force,limit,slip=False):
    """Trusted fixture inputs, no trajectory/dynamics/physical grasp."""
    capacity=number(capacity,0.001);force=number(force,0);limit=number(limit,0.001)
    if type(slip)is not bool:raise ValueError('slip')
    if fragility not in ('robust','fragile','unknown'):raise ValueError('fragility')
    if mass is not None:mass=number(mass,0)
    if force>=limit:action='stop_proposal'
    elif mass is None or fragility=='unknown':action='request_support'
    else:
        mass=number(mass,0)
        if mass>2*capacity:action='stop_proposal'
        elif slip:action='regrasp_proposal'
        elif mass>capacity:action='two_hand_proposal'
        else:action='one_hand_proposal'
    return {'action':action,'executable':False,'hardware_stop_confirmed':False}

class Reminder:
    def __init__(self):self.sent=set()
    def due(self,occurrence_id,due_at,now,consent):
        if not isinstance(occurrence_id,str) or not occurrence_id or len(occurrence_id)>128:raise ValueError('id')
        for t in (due_at,now):
            if not isinstance(t,datetime) or t.utcoffset() is None:raise ValueError('timezone required')
        if type(consent)is not bool:raise ValueError('consent')
        if not consent or now<due_at or occurrence_id in self.sent:return False
        if len(self.sent)>=10000:raise ValueError('capacity')
        self.sent.add(occurrence_id);return True # Local proposal, not a delivery receipt.

def wellness_value(value,quality,minimum,consent):
    number(quality,0,1);number(minimum,0,1)
    if type(consent)is not bool:raise ValueError('consent')
    if not consent or quality<minimum:return {'value':None,'status':'withheld','medical_validated':False}
    number(value,0);return {'value':value,'status':'fixture_only','medical_validated':False}

def kids_catalog(items,age,guardian,remaining_minutes):
    integer(age,0,17);integer(remaining_minutes,0,1440)
    if type(guardian)is not bool:raise ValueError('guardian')
    if not isinstance(items,list) or len(items)>1000:raise ValueError('items')
    if not guardian or remaining_minutes==0:return []
    out=[]
    for x in items:
        lo=integer(x['min_age'],0,17);hi=integer(x['max_age'],lo,17)
        if type(x['approved'])is not bool or type(x['licensed'])is not bool:raise ValueError('approval')
        if lo<=age<=hi and x['approved'] and x['licensed']:out.append(x['id'])
    return out

class VersionedSettings:
    ALLOWED={'quiet','minutes','content_ids'}
    def __init__(self):self.version=0;self.data={}
    def patch(self,base,patch):
        integer(base)
        if base!=self.version:raise ValueError('version conflict')
        if not isinstance(patch,dict) or not patch or not set(patch)<=self.ALLOWED:raise ValueError('field')
        p=dict(patch)
        if 'quiet'in p and type(p['quiet'])is not bool:raise ValueError('quiet')
        if 'minutes'in p:integer(p['minutes'],0,1440)
        if 'content_ids'in p:
            if not isinstance(p['content_ids'],list) or len(p['content_ids'])>100 or any(not isinstance(i,str) or not i or len(i)>128 for i in p['content_ids']):raise ValueError('content')
            p['content_ids']=list(p['content_ids'])
        self.data.update(p);self.version+=1;return self.version

def ota_preflight(blob,manifest,current_version,board,now,stationary,power_ok,signature_verified=False):
    """SHA256 integrity is real; signature_verified is an injected fixture, NOT signature verification."""
    integer(current_version);integer(manifest['version']);number(now,0);number(manifest['expires'],0)
    for b in (stationary,power_ok,signature_verified):
        if type(b)is not bool:raise ValueError('boolean')
    if not isinstance(blob,bytes) or len(blob)>10**7:raise ValueError('blob')
    if not isinstance(board,str) or not board:raise ValueError('board')
    checks={'digest':hashlib.sha256(blob).hexdigest()==manifest['sha256'],'version':manifest['version']>current_version,'board':manifest['board']==board,'expiry':now<manifest['expires'],'stationary':stationary,'power':power_ok,'signature_fixture':signature_verified}
    return {'eligible_proposal':all(checks.values()),'checks':checks,'install_performed':False,'cryptographic_signature_verified':False}

def scoped_access(principal,resource,action,now):
    number(now,0)
    if not isinstance(principal,dict) or not isinstance(resource,dict):return False
    try:
        number(principal['expires'],0);integer(principal['epoch']);integer(resource['epoch'])
        return (principal.get('consent') is True and isinstance(principal.get('tenant'),str) and bool(principal['tenant']) and principal['tenant']==resource.get('tenant') and principal.get('owner')==resource.get('owner') and isinstance(principal.get('owner'),str) and bool(principal['owner']) and principal['epoch']==resource['epoch'] and now<principal['expires'] and isinstance(principal.get('actions'),list) and action in principal['actions'])
    except (KeyError,ValueError):return False

def minimal_event(event):
    if not isinstance(event,dict):raise ValueError('event')
    # Strict enums/numeric fields: raw text cannot hide in an allowlisted string value.
    schema={'code':{'OK','E_COMM','E_POWER','E_STOP','E_AUTH'},'component':{'core','navigation','motor','power','app','billing'},'result':{'accepted','rejected','unknown','pending'}}
    out={}
    for k,allowed in schema.items():
        if isinstance(event.get(k),str) and event[k] in allowed:out[k]=event[k]
    if 'seq'in event:out['seq']=integer(event['seq'])
    if 'stamp'in event:out['stamp']=number(event['stamp'],0)
    return out

class UsageLedger:
    """Integer units, in-memory dedup only; no PG/cloud/credit reservations."""
    def __init__(self,quota):self.quota=integer(quota);self.events={};self.used=0
    def charge(self,event_id,units):
        integer(units,1)
        if not isinstance(event_id,str) or not event_id or len(event_id)>128:raise ValueError('id')
        if event_id in self.events:
            if self.events[event_id]!=units:raise ValueError('id conflict')
            return self.used
        if len(self.events)>=10000 or self.used+units>self.quota:raise ValueError('quota/capacity')
        self.events[event_id]=units;self.used+=units;return self.used
    def refund(self,event_id):
        if event_id not in self.events:raise ValueError('unknown event')
        # Preserve a tombstone in a separate set so replay cannot re-charge refunded events.
        if not hasattr(self,'refunded'):self.refunded=set()
        if event_id not in self.refunded:self.used-=self.events[event_id];self.refunded.add(event_id)
        return self.used

def scene_proposal(steps,allowed,confirmation=False):
    if not isinstance(steps,list) or not 1<=len(steps)<=20 or not isinstance(allowed,dict):raise ValueError('scene')
    if type(confirmation)is not bool:raise ValueError('confirmation')
    if any(not isinstance(k,str) or not k or not isinstance(v,list) or any(not isinstance(a,str) or not a for a in v) for k,v in allowed.items()):raise ValueError('allowlist')
    valid=True
    for s in steps:
        if not isinstance(s,dict) or set(s)!={'device','action'}:raise ValueError('step')
        if any(not isinstance(s[k],str) or not s[k] for k in ('device','action')):raise ValueError('step values')
        if s['action'] not in allowed.get(s['device'],[]):valid=False
        if s['action'] in ('unlock','heat') and not confirmation:valid=False
    return {'eligible_proposal':valid,'steps':[dict(s) for s in steps] if valid else [],'executable':False,'actual_calls':0}

def bom_review(parts):
    if not isinstance(parts,list) or len(parts)>1000:raise ValueError('parts')
    ids=set();issues=[];custom=0
    for p in parts:
        if not isinstance(p.get('id'),str) or not p['id']:raise ValueError('part id')
        if p['id'] in ids:issues.append('duplicate:'+p['id'])
        ids.add(p['id'])
        number(p['supply_v'],0);number(p['min_v'],0);number(p['max_v'],p['min_v'])
        if not p['min_v']<=p['supply_v']<=p['max_v']:issues.append('voltage:'+p['id'])
        if p['kind'] not in ('COTS','Custom'):raise ValueError('kind')
        custom+=p['kind']=='Custom'
        if p.get('reviewed') is not True:issues.append('review:'+p['id'])
    return {'issues':issues,'custom_count':custom,'total':len(parts),'manufacturing_approved':False}

def docket_review(records,today):
    if not isinstance(today,datetime) or today.utcoffset() is None:raise ValueError('aware today')
    if not isinstance(records,list) or len(records)>1000:raise ValueError('records')
    out=[]
    for r in records:
        if not isinstance(r.get('id'),str) or not r['id']:raise ValueError('id')
        # Never derive legal deadlines from priority dates; accepts lawyer-verified timestamps only.
        state='needs_counsel_verification'
        if r.get('counsel_verified') is True and r.get('source_ref'):
            due=datetime.fromisoformat(r['due'])
            if due.utcoffset() is None:raise ValueError('aware due')
            state='overdue' if due<today else 'scheduled'
        out.append({'id':r['id'],'state':state,'filing_performed':False})
    return out

def cashflow(opening,months):
    if not isinstance(months,list) or len(months)>60:raise ValueError('months')
    def dec(x):
        if type(x) not in (str,int,Decimal):raise ValueError('decimal string/integer required')
        d=Decimal(x)
        if not d.is_finite() or d<0:raise ValueError('amount')
        return d
    cash=dec(opening);out=[]
    for m in months:
        cash+=dec(m['receipts'])-dec(m['payments']);out.append(str(cash))
    return {'closing_cash':out,'negative_months':[i+1 for i,x in enumerate(out) if Decimal(x)<0],'scope':'illustrative inputs only; no valuation advice'}

def dilution(existing_shares,new_shares):
    integer(existing_shares,1);integer(new_shares)
    return str(Decimal(new_shares)/Decimal(existing_shares+new_shares))

def funnel(events):
    stages=('lead','trial','quote','order','active');seen={};out={s:0 for s in stages}
    if not isinstance(events,list) or len(events)>10000:raise ValueError('events')
    for e in events:
        if e.get('consent')is not True:continue
        if e['stage'] not in stages:raise ValueError('stage')
        if not isinstance(e['id'],str) or not e['id']:raise ValueError('id')
        if e['id'] in seen:
            if seen[e['id']]!=e['stage']:raise ValueError('event conflict')
            continue
        seen[e['id']]=e['stage'];out[e['stage']]+=1
    return {'counts':out,'scope':'consented fixture event counts; not unique customers or causal attribution'}
