"""Start-cohort metrics, unique sessions and explicit attempt denominators."""
import math,statistics
from .telemetry import check

def ratio(num,den):return {'numerator':num,'denominator':den,'value':None if den==0 else num/den}
def latency(values):
    values=sorted(values)
    return {'samples':len(values),'p50_seconds':None if not values else statistics.median(values),
            'p95_seconds':None if not values else values[math.ceil(.95*len(values))-1]}

def aggregate(events,start,end,as_of,version=None,route=None,mode=None,dropout_window=1800):
    check(all(type(v) in (int,float) and math.isfinite(v) for v in (start,end,as_of,dropout_window)) and 0<=start<end<=as_of and dropout_window>0,'Invalid window')
    check(route in (None,'self','guardian','guest','unknown'),'Invalid route')
    check(mode in (None,'simulated','observed'),'Invalid mode')
    starts={}
    for e in events:
        if e['kind']=='onboarding_started' and start<=e['timestamp']<end and (version is None or e['version']==version) and (mode is None or e['mode']==mode):
            starts.setdefault(e['session'],e)
    cohort={}
    for sid,beg in starts.items():
        rows=[e for e in events if e['session']==sid and beg['timestamp']<=e['timestamp']<=as_of and e['version']==beg['version'] and e['mode']==beg['mode']]
        known=[e['route'] for e in rows if e['route']!='unknown'];resolved=known[-1] if known else 'unknown'
        if route is None or route==resolved:cohort[sid]=(beg,rows,resolved)
    registered=[];ready=[];cancelled=[];durations=[];resume_attempts=set();resume_success=set();apply_attempts=set();apply_failed=set();supported=set();duplicates=set();stage={}
    for sid,(beg,rows,rte) in cohort.items():
        kinds={r['kind'] for r in rows}
        if 'registration_committed' in kinds and rte in ('self','guardian'):registered.append(sid)
        if 'onboarding_ready' in kinds:
            ready.append(sid);t=min(e['timestamp'] for e in rows if e['kind']=='onboarding_ready');durations.append(t-beg['timestamp'])
        if 'onboarding_cancelled' in kinds:cancelled.append(sid)
        if 'support_requested' in kinds:supported.add(sid)
        if 'duplicate_registration' in kinds:duplicates.add(sid)
        for e in rows:
            attempt=(sid,e.get('attempt_id',e['event_id']))
            if e['kind']=='resume_attempt':resume_attempts.add(attempt)
            if e['kind']=='onboarding_resumed' and e.get('success') is True:resume_success.add(attempt)
            if e['kind']=='apply_attempt':apply_attempts.add(attempt)
            if e['kind']=='context_apply_failed':apply_failed.add(attempt)
        # Last entry per unique session/step; immature observations excluded.
        entries={e['step']:e['timestamp'] for e in rows if e['kind']=='step_entered'}
        for step,t in entries.items():
            if t+dropout_window>as_of or 'onboarding_cancelled' in kinds:continue
            bucket=stage.setdefault(step,{'eligible':0,'abandoned':0,'error_events':0})
            bucket['eligible']+=1
            progressed=any(e['kind']=='step_completed' and e.get('step')==step and e['timestamp']>=t for e in rows) or 'onboarding_ready' in kinds
            if not progressed:bucket['abandoned']+=1
            bucket['error_events']+=sum(e['kind']=='step_failed' and e.get('step')==step for e in rows)
    eligible=sum(rte in ('self','guardian') for _,_,rte in cohort.values())
    return {'scope':{'start':start,'end':end,'as_of':as_of,'version':version,'route':route,'mode':mode,'dropout_window_seconds':dropout_window,
                     'cohort':'sessions started within [start,end); follow-up through as_of; events of the start version/mode only'},
        'started_sessions':len(cohort),'registered_sessions':len(registered),'ready_sessions':len(ready),'cancelled_sessions':len(cancelled),
        'registration_completion':ratio(len(registered),eligible),'ready_completion':ratio(len(ready),len(cohort)),
        'duration':latency(durations),'resume_success':ratio(len(resume_success & resume_attempts),len(resume_attempts)),
        'apply_failure':ratio(len(apply_failed & apply_attempts),len(apply_attempts)),
        'support_request':ratio(len(supported),len(cohort)),'duplicate_sessions':len(duplicates),
        'steps':{k:{'dropout':ratio(v['abandoned'],v['eligible']),'error_events':v['error_events']} for k,v in sorted(stage.items())},
        'notes':['Guest is excluded from registration denominator; included in ready denominator.',
                 'Consent refusal is not an error. Normal cancellation is counted separately and excluded from dropout.',
                 'Attempt rates use distinct attempt IDs; session completion rates use unique sessions.',
                 'Observed mode is a provenance label, not proof of user consent or real deployment.']}

def alerts(metrics,min_attempts=20,apply_failure_threshold=.1):
    result=[];failure=metrics['apply_failure']
    if failure['denominator']>=min_attempts and failure['value']>=apply_failure_threshold:result.append({'code':'APPLY_FAILURE_BASELINE_REVIEW','severity':'warning','count':failure['numerator']})
    if metrics['duplicate_sessions']:result.append({'code':'DUPLICATE_REGISTRATION','severity':'blocker','count':metrics['duplicate_sessions']})
    return {'rules_status':'proposed_not_operationally_approved','alerts':result}
