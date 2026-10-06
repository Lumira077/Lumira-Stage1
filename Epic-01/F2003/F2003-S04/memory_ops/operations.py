import html,json,math
from memory_contract import require

def metrics(events,start,end):
    require(type(start) in (int,float) and type(end) in (int,float) and math.isfinite(start) and math.isfinite(end) and 0<=start<end)
    counts={}
    for stamp,version,kind,code in events:
        if start<=stamp<end:counts[kind]=counts.get(kind,0)+1
    return {'period':{'start':start,'end':end},'mode':'synthetic_local','version':'0.1.0','unit':'persisted operation events, not unique participants','counts':counts,'operational_baseline':'pending'}
def study(rows):
    people=set();seen=set();tasks=set();success=0;actual=0
    fields={'participant_id','task','mode','completed','assisted','seconds','version'}
    for r in rows:
        require(set(r)==fields);require(isinstance(r['participant_id'],str) and len(r['participant_id'])==32 and all(c in '0123456789abcdef' for c in r['participant_id']))
        require(r['task'] in ('remember','confirm','recall','correct','delete','revoke','switch','offline'));require(r['mode'] in ('simulated','observed'))
        require(r['version']=='0.1.0');require(type(r['completed']) is bool and type(r['assisted']) is bool)
        require(type(r['seconds']) in (int,float) and math.isfinite(r['seconds']) and 0<=r['seconds']<=86400)
        key=(r['participant_id'],r['task'],r['version']);require(key not in seen,'DUPLICATE_OBSERVATION');seen.add(key)
        if r['mode']=='observed':people.add(r['participant_id']);tasks.add(r['task']);actual+=1;success+=r['completed'] and not r['assisted']
    return {'actual_participants':len(people),'actual_observations':actual,'covered_tasks':sorted(tasks),'independent_rate':None if not actual else success/actual,'study_acceptance':'pending_approved_protocol_and_review'}
def release(report):
    blockers=['REAL_MODEL_QUALITY_PENDING','REAL_ROBOT_ACCEPTANCE_PENDING','REAL_USER_STUDY_PENDING','PRODUCTION_PRIVACY_SYNC_AND_RESTORE_PENDING','OPERATIONS_BASELINE_PENDING','AUTHORIZED_Q1_R1_APPROVAL_NOT_CONNECTED']
    if report['failed'] or report['errors']:blockers.append('SOFTWARE_TEST_FAILURE')
    return {'release_ready':False,'status':'blocked','blockers':blockers,'deployed':False}
def dashboard(m,gate):
    esc=lambda v:html.escape(json.dumps(v,ensure_ascii=False,indent=2))
    return '<!doctype html><html lang="ko"><meta charset="utf-8"><title>F2003 기억 운영 검토</title><style>body{font-family:system-ui;max-width:900px;margin:40px auto;padding:20px;background:#eef6fc;color:#16354b}pre{white-space:pre-wrap;background:white;padding:20px}</style><h1>F2003 개인화 장기 기억</h1><p>합성 개발 데이터 · 외부 LLM/클라우드/실제 로봇 미연결</p><h2>기간별 이벤트</h2><pre>'+esc(m)+'</pre><h2>Release 판정</h2><pre>'+esc(gate)+'</pre></html>'
