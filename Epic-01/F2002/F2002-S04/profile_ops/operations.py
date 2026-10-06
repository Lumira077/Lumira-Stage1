"""Aggregated count-only metrics and conservative development release decision."""
import math,html,json
from profile_contract import require

def metrics(events,start,end):
    require(type(start) in (int,float) and type(end) in (int,float) and math.isfinite(start) and math.isfinite(end) and start<end)
    counts={}
    for stamp,kind,code in events:
        if start<=stamp<end:counts[kind]=counts.get(kind,0)+1
    n=counts.get('apply_attempt',0);failed=counts.get('apply_failed',0)
    return {'period':{'start':start,'end':end},'unit':'persisted operation events; not unique users','counts':counts,
        'apply_failure_rate':None if not n else failed/n,'apply_attempts':n,'apply_failures':failed,'mode':'simulated','baseline_status':'proposed'}
def study(rows):
    # Minimal proof-preserving evaluator: this feature supplies no real study observations.
    fields={'participant_id','task','mode','version','completed','assisted','seconds'}
    seen=set();eligible=[]
    for r in rows:
        require(set(r)==fields);require(isinstance(r['participant_id'],str) and len(r['participant_id'])==32 and all(c in '0123456789abcdef' for c in r['participant_id']))
        require(r['task'] in ('edit','switch','reset','revoke','delete','resume'));require(r['mode'] in ('simulated','observed'))
        require(type(r['completed']) is bool and type(r['assisted']) is bool)
        require(type(r['seconds']) in (int,float) and math.isfinite(r['seconds']) and 0<=r['seconds']<=86400)
        require(isinstance(r['version'],str) and r['version']=='0.1.0','UNSUPPORTED_STUDY_VERSION')
        key=(r['participant_id'],r['task'],r['version']);require(key not in seen,'DUPLICATE_OBSERVATION');seen.add(key)
        if r['mode']=='observed':eligible.append(r)
    people={r['participant_id'] for r in eligible};tasks={r['task'] for r in eligible};success=sum(r['completed'] and not r['assisted'] for r in eligible)
    return {'actual_participants':len(people),'tasks':sorted(tasks),'independent_success_rate':None if not eligible else success/len(eligible),
        'proposed_criterion_met':len(people)>=10 and tasks=={'edit','switch','reset','revoke','delete','resume'} and success/len(eligible)>=.8,
        'review_status':'pending','observed_label_is_not_proof':True}
def release(report,userstudy):
    # No authority system is connected in v0.1; actual approval cannot be set by a caller flag.
    blockers=['REAL_HARDWARE_NOT_VERIFIED','PRODUCTION_DEPLOYMENT_AND_ROLLBACK_PENDING','OPERATIONS_BASELINE_PENDING','AUTHORIZED_Q1_R1_APPROVAL_NOT_CONNECTED']
    if not userstudy['proposed_criterion_met']:blockers.append('REAL_USER_STUDY_PENDING')
    if report['failed'] or report['errors']:blockers.append('SOFTWARE_TEST_FAILURE')
    return {'release_ready':False,'status':'blocked','blockers':blockers,'mode':'simulated'}
def dashboard(metric,gate):
    esc=lambda x:html.escape(json.dumps(x,ensure_ascii=False,indent=2))
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><title>F2002 운영 검토</title><style>body{font-family:system-ui;max-width:900px;margin:40px auto;padding:20px;background:#eef6fc;color:#12334b}pre{background:white;padding:24px;white-space:pre-wrap}</style><h1>F2002 사용자 프로필·선호 설정</h1><p>simulated 개발 증적 · 실사용/실기/운영 배포 미수행</p><h2>기간별 운영 이벤트</h2><pre>'+esc(metric)+'</pre><h2>Release 차단</h2><pre>'+esc(gate)+'</pre></html>'
