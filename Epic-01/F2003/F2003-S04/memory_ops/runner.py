import argparse,json,os,platform,subprocess,sys,tempfile,time,statistics,math,hashlib
from pathlib import Path
from .dependency import ROOT
from .operations import metrics,study,release,dashboard
from .restore import RestoreLab
from memory_service.fixtures import setup,candidate
from memory_contract import extract
from memory_lab.evaluation import evaluate

def stats(xs):return {'samples':len(xs),'unit':'ms','p50':statistics.median(xs),'p95':sorted(xs)[math.ceil(.95*len(xs))-1],'max':max(xs),'failed':0}
def benchmark(n):
    samples={k:[] for k in ('extract','candidate_save','search','context_prepare','context_release')}
    with tempfile.TemporaryDirectory() as tmp:
        p,s,pid=setup(tmp)
        try:
            for i in range(n):
                start=time.perf_counter();extract('나는 산책을 좋아해','a'*32);samples['extract'].append((time.perf_counter()-start)*1000)
                start=time.perf_counter();r=s.create('demo-owner',pid,'demo-device',candidate('산책 '+str(i),'activity_'+str(i)),str(i));samples['candidate_save'].append((time.perf_counter()-start)*1000)
                s.confirm('demo-owner',pid,'demo-device',r['memory_id'],1,'confirm'+str(i))
            for _ in range(n):
                start=time.perf_counter();s.search('demo-owner',pid,'demo-device','산책');samples['search'].append((time.perf_counter()-start)*1000)
                start=time.perf_counter();ticket=s.prepare('demo-owner',pid,'demo-device','산책')['ticket'];samples['context_prepare'].append((time.perf_counter()-start)*1000)
                start=time.perf_counter();ctx=s.release_context('demo-owner',pid,'demo-device',ticket);samples['context_release'].append((time.perf_counter()-start)*1000)
                assert ctx['memories'] and not ctx['executable_actions']
            events=s.db.execute('SELECT stamp,version,kind,code FROM events').fetchall()
        finally:s.close();p.close()
    return {'paths':{k:stats(v) for k,v in samples.items()},'scope':'in-process SQLite + rule extraction + lexical retrieval; no LLM/network/audio/motion',
            'confirmed_memory_count':n,'fixture_content':'short synthetic Korean strings','failure_rate':0},events

def restore_demo():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);(root/'.ker-development-sandbox').write_text('development only');p,s,pid=setup(root)
        try:
            r=s.create('demo-owner',pid,'demo-device',candidate(),'create');s.confirm('demo-owner',pid,'demo-device',r['memory_id'],1,'confirm');lab=RestoreLab(root);lab.backup();s.delete('demo-owner',pid,r['memory_id'],2);lab.export_latest_ledger();report=lab.restore()
            from memory_service import Service
            restored=Service(str(root/'restored.sqlite3'),s.policy)
            try:assert restored.search('demo-owner',pid,'demo-device','산책')==[];report['deletion_not_resurrected']=True
            finally:restored.close()
            return report
        finally:s.close();p.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='results');parser.add_argument('--samples',type=int,default=100);parser.add_argument('--require-release',action='store_true');args=parser.parse_args()
    if not 100<=args.samples<=5000:parser.error('samples must be 100..5000')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);reports={};total=failed=errors=0
    for name,package in [('F2003-S01','memory_contract'),('F2003-S02','memory_service'),('F2003-S03','memory_lab'),('F2003-S04','memory_ops')]:
        code="import "+package+";import unittest,json;r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));print(json.dumps({'run':r.testsRun,'failed':len(r.failures),'errors':len(r.errors)}));raise SystemExit(not r.wasSuccessful())"
        r=subprocess.run([sys.executable,'-c',code],cwd=ROOT.parent/name,capture_output=True,text=True,timeout=60);(out/(name+'-tests.txt')).write_text(r.stdout+r.stderr)
        try:d=json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:d={'run':0,'failed':0,'errors':1}
        if r.returncode!=0 and not d['failed']+d['errors']:d['errors']=1
        reports[name]=d;total+=d['run'];failed+=d['failed'];errors+=d['errors']
    report={'feature':'F2003','source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'python':platform.python_version(),'platform':platform.platform(),'mode':'synthetic_local','tests':reports,'total':total,'failed':failed,'errors':errors,'real_model_tests':'not_run','hardware_tests':'not_run','actual_user_study':'not_run','production_restore':'not_run','release_ready':False}
    def write(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    if failed or errors:write('report.json',report);print(json.dumps(report));return 1
    performance,events=benchmark(args.samples);dataset=ROOT.parent/'F2003-S03/evaluation-set.json';quality=evaluate(json.loads(dataset.read_text()));quality['dataset_sha256']=hashlib.sha256(dataset.read_bytes()).hexdigest()
    target_ok=all(v['p95']<=500 for v in performance['paths'].values())
    quality_ok=quality['extraction']['precision']==1 and quality['extraction']['recall']==1 and quality['extraction']['exact_content_accuracy']==1 and quality['retrieval']['top1_accuracy']==1
    report.update(software_gate='passed' if target_ok and quality_ok else 'failed',dependency_hashes_verified=True,proposed_local_path_p95_ms=500,latency_target_status='passed' if target_ok else 'failed',fixture_quality_gate='passed' if quality_ok else 'failed')
    m=metrics(events,0,time.time()+1);gate=release(report)
    for name,value in [('report.json',report),('performance.json',performance),('quality.json',quality),('metrics.json',m),('study.json',study([])),('release-gate.json',gate),('sandbox-restore.json',restore_demo())]:write(name,value)
    (out/'dashboard.html').write_text(dashboard(m,gate));(out/'report.md').write_text(f'# F2003 개발 검증\n\n자동 시험 {total}개 통과. 5경로 각각 {args.samples}회 측정. Software gate: {report["software_gate"]}.\n\n규칙·문자열 기반 소형 합성 fixture만 검증했으며 외부 LLM·클라우드·실제 로봇·실사용·운영 복귀는 미수행. Release blocked.\n')
    print(f'F2003 tests: {total}; software gate: {report["software_gate"]}; 5 paths x {args.samples}; release BLOCKED')
    return 1 if args.require_release or report['software_gate']!='passed' else 0
if __name__=='__main__':raise SystemExit(main())
