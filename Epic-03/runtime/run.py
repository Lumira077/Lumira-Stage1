import unittest,pathlib,sys,os,json,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
suite=unittest.TestSuite();counts={}
for path in sorted(ROOT.glob('F*/F*-S03/test_*.py')):
 spec=importlib.util.spec_from_file_location(path.stem,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 part=unittest.defaultTestLoader.loadTestsFromModule(module);counts[path.parents[1].name]=part.countTestCases();suite.addTests(part)
r=unittest.TextTestRunner(verbosity=2).run(suite)
report={'source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'scope':'synthetic_local_contract_prototype',
 'tests':r.testsRun,'per_feature_tests':counts,'passed':r.wasSuccessful(),'failures':len(r.failures),'errors':len(r.errors),
 'actual_models':0,'actual_participants':0,'actual_robot_tests':0,'release_ready':False,
 'pending':['trained_models_and_licensed_weights','consented_subject_split_evaluation_calibration','physical_camera_microphone_robot','production_auth_consent_epoch_events','approved_thresholds','Q1_R1_user_release_validation']}
out=pathlib.Path(os.environ.get('EPIC03_EVIDENCE_DIR',str(ROOT/'runtime'/'evidence')));out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
raise SystemExit(0 if r.wasSuccessful() else 1)
