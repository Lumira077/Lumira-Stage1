"""Emit measured local software results with explicit unperformed hardware coverage."""
import argparse,hashlib,json,math,os,platform,statistics,subprocess,sys,tempfile,time,unittest
from pathlib import Path
from .dependency import ROOT,S02,verify
from .adapters import GuardedOutputs,LabService
from .safety import Broker
from ker_onboarding.core import STEPS,DEFAULTS,CONSENTS
from ker_onboarding.service import POLICY_VERSION

class Result(unittest.TextTestResult):
    def __init__(self,*args):super().__init__(*args);self.records=[]
    def addSuccess(self,test):super().addSuccess(test);self.records.append({'test':test.id(),'status':'passed','mode':'simulated'})
    def addFailure(self,test,err):super().addFailure(test,err);self.records.append({'test':test.id(),'status':'failed','mode':'simulated'})
    def addError(self,test,err):super().addError(test,err);self.records.append({'test':test.id(),'status':'error','mode':'simulated'})

def stats(samples,proposed=None):
    ordered=sorted(samples);n=len(ordered)
    return {'samples':n,'unit':'ms','p50':statistics.median(ordered),'p95':ordered[math.ceil(.95*n)-1],
            'max':max(ordered),'failure_rate':0,'proposed_target_ms':proposed,
            'target_status':'not_defined' if proposed is None else 'passed' if ordered[math.ceil(.95*n)-1]<=proposed else 'failed'}

def benchmark(iterations):
    saves=[];applies=[];greetings=[]
    for _ in range(iterations):
        with tempfile.TemporaryDirectory() as tmp:
            broker=Broker(str(Path(tmp)/'out.db'));s=LabService(str(Path(tmp)/'service.db'),outputs=GuardedOutputs(broker))
            try:
                actor='local-demo-owner';x=s.create(actor,'demo-device-01',['demo-device-01']);sid=x['session_id']
                values={'registration':{'registration_type':'self','subject_id':actor},'language':{'language':'ko-KR'},
                    'profile':{'nickname':'fixture','preferred_name':'샘플'},'purpose':{'purpose':'companion'},'preferences':dict(DEFAULTS),
                    'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY_VERSION},'review':{'confirmed':True}}
                for step in STEPS:
                    start=time.perf_counter();x=s.save_step(sid,actor,step,values[step],x['revision'])
                    if step=='profile':saves.append((time.perf_counter()-start)*1000)
                start=time.perf_counter();s.complete(sid,actor,'measurement',x['revision']);a=s.apply(sid,actor)
                if a['apply_status']!='applied':raise RuntimeError('Benchmark application failed')
                applies.append((time.perf_counter()-start)*1000)
                start=time.perf_counter();s.greeting(sid,actor);greetings.append((time.perf_counter()-start)*1000)
            finally:s.close();broker.close()
    return {'scope':'local in-process SQLite and simulated ACK; excludes network, real audio onset and physical motion',
            'step_save':stats(saves,500),'registration_to_simulated_ACK':stats(applies,1000),
            'greeting_text_and_simulated_dispatch':stats(greetings),'real_voice_onset':'not_measured'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='results');parser.add_argument('--samples',type=int,default=100)
    parser.add_argument('--mode',choices=['simulated'],default='simulated');args=parser.parse_args()
    if args.samples<100:parser.error('At least 100 samples per latency path are required.')
    manifest=verify();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    with (out/'tests.txt').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Result).run(suite)
    records=result.records
    report={'schema_version':1,'work_item':'KR1-5','feature':'F2001','mode':'simulated','hardware_connected':False,
            'release_ready':False,'s03_acceptance':'pending_hardware_and_Q1_R1_review',
            'environment':{'python':platform.python_version(),'platform':platform.platform(),
                's03_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'s02_commit':manifest['s02_commit'],
                's02_hashes_verified':True,'firmware':None,'robot_serial':None,'control_model':None},
            'tests':{'run':result.testsRun,'failed':len(result.failures),'errors':len(result.errors),'cases':records},
            'hardware_tests':{'status':'not_run','reason':'No authenticated hardware adapter, robot or approved physical safety parameters',
                'required':['real pairing/ownership','STT noisy environment/recognition confirmation','speaker dB/mute/onset',
                            'joint limits/speed/torque/stop time','power interruption during storage/output',
                            'controller/sensor fault and safe-state validation']}}
    report['scenarios']=[{'id':f'ONB-{i:02d}','software_status':next((r['status'] for r in records if f'test_ONB_{i:02d}_' in r['test']),'not_run'),
                          'evidence_scope':'software/fixture; see docs/traceability.md','real_robot_status':'not_run'} for i in range(1,17)]
    if result.wasSuccessful():
        try:report['performance']=benchmark(args.samples)
        except Exception:report['performance']={'status':'failed','error_code':'BENCHMARK_FAILED'}
        try:
            smoke=subprocess.run([sys.executable,'scripts/smoke.py'],cwd=S02,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
            (out/'http-smoke.txt').write_text(smoke.stdout);report['s02_HTTP_regression']='passed' if smoke.returncode==0 else 'failed'
        except Exception:
            report['s02_HTTP_regression']='failed';(out/'http-smoke.txt').write_text('HTTP_SMOKE_FAILED_OR_TIMEOUT\n')
    else:report['performance']={'status':'not_run_due_to_test_failure'};report['s02_HTTP_regression']='not_run'
    passed=result.wasSuccessful() and report['s02_HTTP_regression']=='passed' and report['performance'].get('status')!='failed' and all(
        v.get('target_status')!='failed' for v in report['performance'].values() if isinstance(v,dict))
    report['software_gate']='passed' if passed else 'failed'
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    lines=['# F2001-S03 software integration results',f"Software gate: {report['software_gate']}",
           f"Tests: {result.testsRun}; failures: {len(result.failures)}; errors: {len(result.errors)}",'Mode: simulated; hardware tests NOT RUN; release ready: false','',
           '| Latency path | n | p50 ms | p95 ms | max ms | Proposed software target |','|---|---:|---:|---:|---:|---|']
    for k,v in report['performance'].items():
        if isinstance(v,dict) and 'p95' in v:lines.append(f"| {k} | {v['samples']} | {v['p50']:.3f} | {v['p95']:.3f} | {v['max']:.3f} | {v['target_status']} |")
    lines+=['','Measurement excludes real voice onset/network/motion. Targets are initial proposals, not hardware acceptance.','Q1/R1 approval and physical measurements remain pending.']
    (out/'report.md').write_text('\n'.join(lines)+'\n');print(f'Software gate: {report["software_gate"]}; tests: {result.testsRun}; hardware NOT RUN; results: {out}')
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
