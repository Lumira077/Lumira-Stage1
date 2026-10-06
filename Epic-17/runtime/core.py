"""Offline UX review functions. No robot/voice/network/storage-delete I/O."""
from dataclasses import dataclass, replace
import math

@dataclass(frozen=True)
class State:
    mode: str = 'idle'
    muted: bool = False
    connected: bool = True
    charging: bool = False
    estop: bool = False
    cliff: bool = False
    volume: int = 50

def reduce(state, event, value=None):
    if event == 'volume':
        if type(value) is not int or not 0 <= value <= 100: raise ValueError('volume')
        state=replace(state, volume=value)
    elif event == 'mute': state=replace(state,muted=not state.muted,mode='idle')
    elif event in ('charging','estop','cliff','connected'):
        if type(value) is not bool: raise ValueError('boolean required')
        # Clearing a stop/interlock never resumes a prior move or conversation.
        state=replace(state,**{event:value},mode='idle')
    elif event == 'start':
        if not (state.muted or state.estop or state.cliff or not state.connected):state=replace(state,mode='listening')
    elif event == 'process' and state.mode=='listening':state=replace(state,mode='processing')
    elif event == 'reply' and state.mode=='processing':state=replace(state,mode='speaking')
    elif event == 'stop':state=replace(state,mode='idle')
    elif event == 'move':
        if not movement_blockers(state): state=replace(state,mode='move_proposal')
    elif event not in ('process','reply'):raise ValueError('unknown event')
    if state.estop or state.cliff or state.muted or not state.connected:state=replace(state,mode='idle')
    return state

def movement_blockers(s):
    return [label for flag,label in [(s.charging,'charging'),(s.estop,'estop'),(s.cliff,'cliff'),(not s.connected,'disconnected')] if flag]

def presentation(s):
    if s.estop:face='stop'
    elif s.cliff:face='stop'
    elif s.muted:face='muted'
    elif not s.connected:face='error'
    elif s.mode in ('listening','processing','speaking'):face=s.mode
    elif s.charging:face='charging'
    else:face='idle'
    return {'face':face,'mode':s.mode,'movement_blockers':movement_blockers(s),'gesture':'small_proposal' if s.mode=='speaking' and not movement_blockers(s) else 'hold','hardware_executable':False}

def study_metrics(rows):
    """Complete-case duration median; consented, not-withdrawn tasks. No success imputation."""
    eligible=[]; seen=set()
    for r in rows:
        if r.get('consent') is not True or r.get('withdrawn') is True:continue
        key=(r.get('participant_id'),r.get('task_id'))
        if not all(isinstance(x,str) and x for x in key):raise ValueError('ids')
        if key in seen:raise ValueError('duplicate participant-task')
        seen.add(key)
        if type(r.get('completed')) is not bool:raise ValueError('completed boolean')
        v=r.get('duration_s')
        if v is not None and (type(v) not in (int,float) or not math.isfinite(v) or v<0):raise ValueError('duration')
        a=r.get('assistance_count')
        if type(a) is not int or a<0:raise ValueError('assistance')
        eligible.append(r)
    times=sorted(r['duration_s'] for r in eligible if r['duration_s'] is not None)
    n=len(times); median=None if not n else (times[n//2] if n%2 else (times[n//2-1]+times[n//2])/2)
    count=len(eligible)
    return {'denominator':count,'success_count':sum(r['completed'] for r in eligible),'success_rate':sum(r['completed'] for r in eligible)/count if count else None,'median_duration_s':median,'duration_denominator':n,'assistance_total':sum(r['assistance_count'] for r in eligible),'scope':'input observations only; fixture is not user evidence'}

def ab_order(index):
    if type(index) is not int or index<0:raise ValueError('index')
    return ['character','real'] if index%2==0 else ['real','character']

def freeze_readiness(assets,issues,required=('cad','bom','cmf','ui','harness','physical_test','usability')):
    reasons=[]; by={}
    for a in assets:
        name=a.get('name')
        if name in by: reasons.append('duplicate:'+str(name))
        by[name]=a
    revs=set()
    for name in required:
        a=by.get(name)
        if not a:reasons.append('missing:'+name);continue
        if a.get('evidence_type') not in ('physical_measurement','user_observation','review_approval'):reasons.append('draft:'+name)
        if a.get('reviewed') is not True or not a.get('evidence_ref') or not a.get('reviewer'):reasons.append('unreviewed:'+name)
        if not a.get('revision'):reasons.append('revision:'+name)
        else:revs.add(a['revision'])
    if len(revs)>1:reasons.append('revision_mismatch')
    reasons += ['open:'+str(i.get('id')) for i in issues if i.get('state')!='closed' and i.get('severity') in ('critical','major')]
    return {'ready_for_human_review':not reasons,'blocking_reasons':reasons,'release_approved':False}

def accessory_overlap(accessory,zones):
    """AABB geometry screen only, not mechanical/safety approval."""
    def box(v):
        if not isinstance(v,(list,tuple)) or len(v)!=6:raise ValueError('box')
        if any(type(x) not in (int,float) or not math.isfinite(x) for x in v):raise ValueError('finite box')
        if any(v[i]>=v[i+3] for i in range(3)):raise ValueError('box extent')
        return v
    if accessory is None or any(z.get('box') is None for z in zones):return {'state':'unknown','conflicts':[],'safe':False}
    a=box(accessory); conflicts=[]
    for z in zones:
        b=box(z['box'])
        if all(a[i]<=b[i+3] and b[i]<=a[i+3] for i in range(3)):conflicts.append(z['id'])
    return {'state':'conflict' if conflicts else 'no_aabb_overlap','conflicts':conflicts,'safe':False}
