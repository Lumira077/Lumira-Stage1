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
 'actual_hardware_calls':0,'actual_participants':0,'actual_robot_tests':0,'release_ready':False,
 'pending':['real_board_drivers_motors_sensors_BMS','URDF_calibration_feedback_safety_controller','real_time_QoS_clock_failures','production_auth_privacy_epoch_events','approved_parameters_and_freeze','actual_mission_Q1_R1_rollback']}
out=pathlib.Path(os.environ.get('EPIC06_EVIDENCE_DIR',str(ROOT/'runtime'/'evidence')));out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
raise SystemExit(0 if r.wasSuccessful() else 1)
