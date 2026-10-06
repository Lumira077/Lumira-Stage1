"""Run each work package independently and retain honest simulation evidence."""
import argparse,json,os,platform,subprocess,sys,tempfile,time,statistics,math,hashlib
from pathlib import Path
from .dependency import ROOT
from .operations import metrics,study,release,dashboard
from .restore import RestoreLab
from profile_service import Service
from profile_contract import DEFAULTS,CONSENTS,POLICY
from profile_lab.adapters import SimulatedOutputs

def data():return {'language':'ko-KR','nickname':'synthetic','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
def stats(xs):return {'unit':'ms','samples':len(xs),'p50':statistics.median(xs),'p95':sorted(xs)[math.ceil(.95*len(xs))-1],'max':max(xs),'scope':'in-process SQLite + simulated setting ACK; excludes real hardware, network and audio onset'}
def benchmark(n):
    saves=[];applies=[]
    with tempfile.TemporaryDirectory() as tmp:
        s=Service(str(Path(tmp)/'lab.db'));s.provision_device('d','owner')
        try:
            p=s.create('owner',data(),'create')
            for i in range(n):
                start=time.perf_counter();p=s.update(p['profile_id'],'owner',{'preferences':{**DEFAULTS,'volume':i%41}},p['revision'],f'edit-{i}');saves.append((time.perf_counter()-start)*1000)
                a=s.activate(p['profile_id'],'owner','d',p['revision']);start=time.perf_counter();r=s.apply(a['application_id'],'owner',SimulatedOutputs());applies.append((time.perf_counter()-start)*1000)
                if r['state']!='applied':raise RuntimeError('Benchmark failed')
            events=s.db.execute('SELECT stamp,kind,code FROM events').fetchall()
        finally:s.close()
    return {'save':stats(saves),'apply':stats(applies)},events

def restore_demo():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);(root/'.ker-development-sandbox').write_text('development')
        s=Service(str(root/'current.sqlite3'));p=s.create('owner',data(),'create');d=data();d['consent']['long_term_memory']=True;second=s.create('owner',d,'second')
        try:
            lab=RestoreLab(root);lab.backup();(root/'privacy-ledger.json').write_text(json.dumps([{'seq':1,'profile_id':p['profile_id'],'operation':'delete','purpose':None},{'seq':2,'profile_id':second['profile_id'],'operation':'revoke','purpose':'long_term_memory'}]));report=lab.restore()
            restored=Service(str(root/'restored.sqlite3'))
            try:
                require_result=restored.list('owner');assert len(require_result)==1 and not require_result[0]['data']['consent']['long_term_memory']
                report['deletion_and_revocation_reapplied']=True
            finally:restored.close()
            return report
        finally:s.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='results');parser.add_argument('--samples',type=int,default=100);parser.add_argument('--require-release',action='store_true');args=parser.parse_args()
    if args.samples<100:parser.error('At least 100 samples required')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);reports={};failed=errors=total=0
    for name,package in [('F2002-S01','profile_contract'),('F2002-S02','profile_service'),('F2002-S03','profile_lab'),('F2002-S04','profile_ops')]:
        script="import unittest,json;import "+package+";r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));print(json.dumps({'run':r.testsRun,'failed':len(r.failures),'errors':len(r.errors)}));raise SystemExit(not r.wasSuccessful())"
        r=subprocess.run([sys.executable,'-c',script],cwd=ROOT.parent/name,capture_output=True,text=True,timeout=60)
        (out/(name+'-tests.txt')).write_text(r.stdout+r.stderr)
        try:d=json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:d={'run':0,'failed':0,'errors':1}
        if r.returncode!=0 and d['failed']+d['errors']==0:d['errors']=1
        reports[name]=d;total+=d['run'];failed+=d['failed'];errors+=d['errors']
    report={'feature':'F2002','source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'python':platform.python_version(),'mode':'simulated','tests':reports,'total':total,'failed':failed,'errors':errors,'hardware_tests':'not_run','actual_user_study':'not_run','production_rollback':'not_run','release_ready':False}
    if failed or errors:
        (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));return 1
    perf,events=benchmark(args.samples);report['software_gate']='passed';report['dependency_hashes_verified']=True;report['proposed_latency_targets']={'save_p95_ms':500,'apply_p95_ms':1000,'status':'passed' if perf['save']['p95']<=500 and perf['apply']['p95']<=1000 else 'failed'};m=metrics(events,0,time.time()+1);u=study([]);gate=release(report,u)
    for name,value in [('report.json',report),('performance.json',perf),('metrics.json',m),('study.json',u),('release-gate.json',gate),('sandbox-restore.json',restore_demo())]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    (out/'dashboard.html').write_text(dashboard(m,gate))
    (out/'report.md').write_text(f'# F2002 개발 검증\n\n소프트웨어 시험 {total}개 통과; 실패/오류 0. 모드 simulated. 저장·적용 각각 {args.samples}회 지연 측정.\n\n실사용·실기·운영 복귀 및 Q1/R1 승인 미수행; release_ready=false.\n')
    print(f'F2002 software tests: {total} passed; samples: {args.samples} per path; hardware NOT RUN; release BLOCKED')
    return 1 if args.require_release or report['proposed_latency_targets']['status']=='failed' else 0
if __name__=='__main__':raise SystemExit(main())
