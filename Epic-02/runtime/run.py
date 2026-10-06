"""Source-bound synthetic-input suite; no live provider calls."""
import os,json,pathlib,sys,unittest,time,statistics
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from core import PolicyEngine
ROOT=pathlib.Path(__file__).resolve().parents[1]
def leaves(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from leaves(t)
        else:yield t
def main():
    suite=unittest.TestSuite();counts={}
    for path in sorted(ROOT.glob('F*/F*-S03')):
        part=unittest.defaultTestLoader.discover(str(path),pattern='test_*.py',top_level_dir=str(path))
        counts[path.parent.name]=sum(1 for _ in leaves(part));suite.addTests(part)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    x={'sensitivity':'public','safety_command':False,'cloud_consent':True,'visual_needed':False,'network_ok':True,'credits':1,'robot_ready':True}
    sample=[]
    for _ in range(100):
        start=time.perf_counter();PolicyEngine().decide(x);sample.append((time.perf_counter()-start)*1000)
    sample.sort()
    report={'source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'scope':'synthetic_local_prototype',
            'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful(),
            'per_feature_tests':counts,'release_ready':False,'actual_provider_calls':0,'actual_participants':0,
            'policy_cpu_benchmark':{'samples':100,'p50_ms':sample[49],'p95_ms':sample[94],'scope':'pure function only; not real model or robot latency'},
            'pending':['real_provider_credentials','microphone_camera_speaker_robot','real_models_and_eval_data',
                       'approved_thresholds_and_policies','production_auth_privacy_billing','Q1_R1_review']}
    out=pathlib.Path(os.environ.get('EPIC02_EVIDENCE_DIR',str(ROOT/'runtime'/'evidence')));out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
