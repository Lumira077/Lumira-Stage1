"""Execute simulation suites and write honest, source-bound evidence."""
import importlib.util,json,os,pathlib,sys,time,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
for fid,module in [('F2004','family'),('F2005','policy'),('F2006','companion'),('F2007','pet'),('F2157','theme')]:
    sys.path.insert(0,str(ROOT/fid/(fid+'-S02')))
sys.path[:0]=[str(ROOT/'F2002'/'F2002-S01'),str(ROOT/'F2002'/'F2002-S02')]
def main():
    suite=unittest.TestSuite()
    for fid in ('F2004','F2005','F2006','F2007','F2157'):
        suite.addTests(unittest.defaultTestLoader.discover(str(ROOT/fid/(fid+'-S03')),pattern='test_*.py',top_level_dir=str(ROOT/fid/(fid+'-S03'))))
        # Each directory uses unique test module names, avoiding unittest module collisions.
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    blockers=['real_robot_not_connected','actual_user_study_not_run','production_auth_not_connected',
              'biometric_models_not_connected','content_and_package_approval_pending',
              'NFC_presence_hardware_pending','Q1_R1_approval_pending']
    report={'source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'scope':'local_simulation',
            'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'passed':result.wasSuccessful(),'release_ready':False,'blockers':blockers,
            'features':['F2004','F2005','F2006','F2007','F2157'],'actual_user_participants':0}
    out=pathlib.Path(os.environ.get('EPIC01_EVIDENCE_DIR',str(ROOT/'integration'/'evidence')))
    out.mkdir(parents=True,exist_ok=True); (out/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report)); return 0 if result.wasSuccessful() else 1
if __name__=='__main__': raise SystemExit(main())
