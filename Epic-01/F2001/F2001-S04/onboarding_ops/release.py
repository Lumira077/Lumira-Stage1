"""Evidence-bound release decision. No fabricated user study or approval."""
import hashlib,hmac,json,math,re
from .telemetry import check

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()

def evaluate_users(rows):
    fields={'participant_id','group','task','phase','mode','completed','assisted','seconds','normal_connection','version'}
    for r in rows:
        check(set(r)==fields,'Invalid observation fields')
        check(bool(re.fullmatch(r'[0-9a-f]{32}',r['participant_id'])),'Use opaque participant ID')
        check(r['group'] in ('general','elderly','guardian'),'Invalid group')
        check(r['task'] in ('basic_registration','guardian','guest','resume','connection_loss','settings_change'),'Invalid task')
        check(r['phase'] in ('baseline','retest'),'Invalid phase');check(r['mode'] in ('simulated','observed'),'Invalid mode')
        check(all(type(r[k]) is bool for k in ['completed','assisted','normal_connection']),'Invalid boolean')
        check(type(r['seconds']) in (int,float) and math.isfinite(r['seconds']) and 0<=r['seconds']<=86400,'Invalid duration')
        check(bool(re.fullmatch(r'\d+\.\d+\.\d+',r['version'])),'Invalid version')
    groups_by_person={}
    for r in rows:
        key=(r['participant_id'],r['version']);groups_by_person.setdefault(key,r['group']);check(groups_by_person[key]==r['group'],'Conflicting participant group')
    # Duplicate participant/task/phase/version is rejected; retry records need a new evaluation round.
    keys=[(r['participant_id'],r['task'],r['phase'],r['version']) for r in rows];check(len(keys)==len(set(keys)),'Duplicate observation')
    actual=[r for r in rows if r['mode']=='observed' and r['phase']=='retest']
    basic=[r for r in actual if r['task']=='basic_registration' and r['normal_connection']]
    independent=sum(r['completed'] and not r['assisted'] and r['seconds']<=300 for r in basic)
    versions={r['version'] for r in actual}
    people={r['participant_id'] for r in actual};groups={r['group'] for r in actual};tasks={r['task'] for r in actual}
    return {'observations':len(rows),'version':next(iter(versions)) if len(versions)==1 else None,'actual_retest_participants':len(people),'normal_basic_trials':len(basic),
            'independent_within_5min':independent,'independent_rate':None if not basic else independent/len(basic),
            'representative_groups':sorted(groups),'covered_tasks':sorted(tasks),
            'eligible':len(versions)==1 and len(people)>=10 and len(basic)>=10 and independent/len(basic)>=.8 and {'elderly','guardian'}<=groups and
                       {'basic_registration','guardian','guest','resume','connection_loss','settings_change'}<=tasks,
            'mode_note':'Simulated records never count as real participants; observed labels require signed reviewer evidence.'}

def sign(role,evidence,key):
    return {'role':role,'evidence_digest':digest(evidence),'decision':'approved',
            'signature':hmac.new(key,canonical({'role':role,'evidence_digest':digest(evidence),'decision':'approved'}),hashlib.sha256).hexdigest()}

def evaluate(evidence,approvals=(),trusted_keys=None):
    trusted_keys=trusted_keys or {};blockers=[]
    check(set(evidence)=={'candidate','s03','users','rollback','operations','blocker_defects'},'Invalid evidence bundle')
    candidate=evidence['candidate'];check(bool(re.fullmatch('[0-9a-f]{40}',candidate.get('commit',''))),'Invalid candidate commit')
    check(bool(re.fullmatch(r'\d+\.\d+\.\d+',candidate.get('version',''))),'Invalid candidate version')
    if candidate.get('mode')!='hardware':blockers.append('CANDIDATE_NOT_HARDWARE')
    s03=evidence['s03']
    if s03.get('hardware_tests',{}).get('status')!='passed' or s03.get('release_ready') is not True:blockers.append('S03_REAL_ROBOT_ACCEPTANCE_PENDING')
    if not evidence['users'].get('eligible'):blockers.append('REAL_USER_VALIDATION_PENDING')
    if evidence['users'].get('version')!=candidate.get('version'):blockers.append('USER_STUDY_VERSION_MISMATCH')
    if evidence['rollback'].get('scope')!='production_approved' or evidence['rollback'].get('status')!='passed':blockers.append('PRODUCTION_ROLLBACK_PENDING')
    if evidence['operations'].get('status')!='approved' or evidence['operations'].get('data_mode')!='observed':blockers.append('OPERATIONS_BASELINE_PENDING')
    if type(evidence['blocker_defects']) is not int or evidence['blocker_defects']!=0:blockers.append('OPEN_OR_UNKNOWN_BLOCKER_DEFECTS')
    for role in ('Q1','R1'):
        signed=[a for a in approvals if a.get('role')==role];key=trusted_keys.get(role)
        valid=False
        if isinstance(key,bytes) and len(key)>=32 and len(signed)==1:
            a=signed[0];expected=sign(role,evidence,key)
            valid=set(a)==set(expected) and all(a[k]==expected[k] for k in ('role','evidence_digest','decision')) and isinstance(a.get('signature'),str) and bool(re.fullmatch('[0-9a-f]{64}',a['signature'])) and hmac.compare_digest(a['signature'],expected['signature'])
        if not valid:blockers.append(role+'_VERIFIED_APPROVAL_PENDING')
    return {'work_item':'KR1-6','candidate_commit':candidate['commit'],'evidence_digest':digest(evidence),
            'release_ready':not blockers,'status':'approved' if not blockers else 'blocked','blockers':blockers,
            'notes':['A key must come from an authorized reviewer channel; a self-generated key is not reviewer authorization.',
                     'No deployment or Jira status transition is performed by this evaluator.']}
