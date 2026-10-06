"""Reproducible synthetic operations evidence, never a real release approval."""
import argparse,json,os,secrets,sqlite3,tempfile,unittest
from pathlib import Path
from .dependency import ROOT,verify
from .telemetry import Sink
from .service import ObservedService
from .metrics import aggregate,alerts
from .release import evaluate_users,evaluate
from .restore import RestoreLab
from .dashboard import build
from onboarding_lab.adapters import GuardedOutputs
from onboarding_lab.safety import Broker
from ker_onboarding.service import POLICY_VERSION
from ker_onboarding.core import STEPS,DEFAULTS,CONSENTS

VERSION='0.4.0'
def values(actor,kind):
    return {'registration':{'registration_type':kind,'subject_id':'demo-child-01' if kind=='guardian' else 'guest' if kind=='guest' else actor},
        'language':{'language':'ko-KR'},'profile':{'nickname':'synthetic-only','preferred_name':'샘플'},'purpose':{'purpose':'companion'},
        'preferences':dict(DEFAULTS),'consent':{**{k:kind!='guest' for k in CONSENTS},'policy_version':POLICY_VERSION},'review':{'confirmed':True}}
def fill(service,x,actor,kind):
    for step in STEPS:x=service.save_step(x['session_id'],actor,step,values(actor,kind)[step],x['revision'])
    return service.complete(x['session_id'],actor,'demo-complete',x['revision'])
def demo(root):
    (root/'.ker-development-sandbox').write_text('Synthetic development fixtures only\n')
    now=[1000.0];sink=Sink(str(root/'events.sqlite3'),secrets.token_bytes(32),VERSION,clock=lambda:now[0],mode='simulated')
    broker=Broker(str(root/'outputs.sqlite3'));service=ObservedService(str(root/'current.sqlite3'),sink=sink,outputs=GuardedOutputs(broker,fail_once='tts'))
    try:
        completed=[]
        service.devices.devices.update({name:{'owner':'local-demo-owner','connected':True} for name in ('demo-draft','demo-cancel')})
        for i,kind in enumerate(('self','guardian','guest')):
            actor='local-demo-guardian' if kind=='guardian' else 'local-demo-owner';device=('demo-device-01','demo-guardian-01','demo-guest-01')[i]
            x=service.create(actor,device,[device]);service.resume(x['session_id'],actor);r=fill(service,x,actor,kind)
            now[0]+=40;service.apply(x['session_id'],actor);service.apply(x['session_id'],actor);service.greeting(x['session_id'],actor)
            completed.append(r)
        x=service.create('local-demo-owner','demo-draft',['demo-draft']);service.save_step(x['session_id'],'local-demo-owner','registration',values('local-demo-owner','self')['registration'],x['revision'])
        draft_sid=x['session_id'];service.request_support(draft_sid,'local-demo-owner')
        x=service.create('local-demo-owner','demo-cancel',['demo-cancel']);service.cancel(x['session_id'],'local-demo-owner')
        lab=RestoreLab(root);lab.backup()
        ledger=[{'seq':1,'operation':'delete_profile','profile_id':completed[0]['profile_id'],'purpose':None},
                {'seq':2,'operation':'revoke_consent','profile_id':completed[1]['profile_id'],'purpose':'long_term_memory'}]
        (root/'privacy-ledger.json').write_text(json.dumps(ledger));restored=lab.restore()
        db=sqlite3.connect(root/'restored.sqlite3')
        try:
            deleted=db.execute('SELECT 1 FROM profiles WHERE id=?',(completed[0]['profile_id'],)).fetchone() is None
            data=json.loads(db.execute('SELECT data FROM profiles WHERE id=?',(completed[1]['profile_id'],)).fetchone()[0])
            preserved='registration' in json.loads(db.execute('SELECT data FROM sessions WHERE id=?',(draft_sid,)).fetchone()[0])
            restored['checks']={'deletion_not_resurrected':deleted,'revocation_reapplied':data['consent']['long_term_memory'] is False,'in_progress_preserved':preserved}
            if not all(restored['checks'].values()):raise RuntimeError('Sandbox restoration assertion failed')
        finally:db.close()
        events=sink.read();metrics=aggregate(events,0,2000,4000,version=VERSION,mode='simulated')
        return events,metrics,restored,service.dropped_events
    finally:service.close();broker.close();sink.close()
def write(out,name,value): (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='results');parser.add_argument('--require-release',action='store_true');args=parser.parse_args()
    manifest=verify();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    with (out/'tests.txt').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    if not result.wasSuccessful():print('Software tests failed; see tests.txt');return 1
    with tempfile.TemporaryDirectory() as tmp:events,metrics,restore,dropped=demo(Path(tmp))
    rows=[]
    for i in range(10):
        for task in ('basic_registration','guardian','guest','resume','connection_loss','settings_change'):
            rows.append({'participant_id':f'{i+1:032x}','group':'elderly' if i==0 else 'guardian' if i==1 else 'general',
                'task':task,'phase':'retest','mode':'simulated','completed':True,'assisted':False,'seconds':180,'normal_connection':True,'version':VERSION})
    users=evaluate_users(rows)
    candidate_commit=os.environ.get('GITHUB_SHA','0'*40)
    evidence={'candidate':{'version':VERSION,'commit':candidate_commit,'mode':'simulated'},
        's03':{'hardware_tests':{'status':'not_run'},'release_ready':False},'users':users,'rollback':restore,
        'operations':{'status':'pending','data_mode':'simulated'},'blocker_defects':None}
    gate=evaluate(evidence)
    write(out,'metrics.json',metrics);write(out,'study-simulated.json',rows);write(out,'study-evaluation.json',users)
    write(out,'sandbox-restore.json',restore);write(out,'release-evidence.json',evidence);write(out,'release-gate.json',gate)
    (out/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    write(out,'metrics-by-route.json',{route:aggregate(events,0,2000,4000,version=VERSION,route=route,mode='simulated') for route in ('self','guardian','guest','unknown')})
    (out/'dashboard.html').write_text(build(metrics,gate,alerts(metrics)))
    report={'work_item':'KR1-6','mode':'simulated','software_gate':'passed','tests':{'run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)},
        'dependency_hashes_verified':True,'logging_dropped_events':dropped,'real_user_study':'not_run','hardware_tests':'not_run',
        'production_deployment':'not_run','production_restore':'not_run','release_ready':False,
        'source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'version':VERSION}
    if dropped:raise RuntimeError('Synthetic demo lost telemetry')
    if gate['release_ready'] or users['actual_retest_participants']!=0:raise RuntimeError('Synthetic data incorrectly accepted as real validation')
    write(out,'report.json',report)
    (out/'report.md').write_text(f"# F2001-S04 개발 검증\n\nSoftware gate: passed; tests: {result.testsRun}; failures: 0; errors: 0.\n\n모든 Demo 데이터는 simulated입니다. 실사용 검증·실기 시험·운영 배포·복귀·Q1/R1 승인은 미수행이며 Release는 blocked입니다.\n\nDashboard: dashboard.html; 지표: metrics.json / metrics-by-route.json; 복원: sandbox-restore.json; Release: release-gate.json.\n")
    print(f'Software gate: passed; tests: {result.testsRun}; release: {gate["status"]}; actual study participants: 0; results: {out}')
    return 1 if args.require_release and not gate['release_ready'] else 0
if __name__=='__main__':raise SystemExit(main())
