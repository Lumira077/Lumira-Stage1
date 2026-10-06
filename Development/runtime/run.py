import unittest,json,os,sys,hashlib
from pathlib import Path
from review import review
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
suite=unittest.defaultTestLoader.discover(str(Path(__file__).parent),pattern='test*.py')
result=unittest.TextTestRunner(verbosity=1).run(suite)
catalog=json.loads((ROOT/'Development/catalog.json').read_text());tasks=json.loads((ROOT/'Development/tasks.json').read_text())
catalog=[json.loads((ROOT/c['path']).read_text()) for c in catalog]
tasks=[json.loads((ROOT/t['path']).read_text()) for t in tasks]
for c in catalog:review(c)
assert len({c['feature'] for c in catalog})==148 and len(tasks)==557
for t in tasks:
 assert t['completed'] is False and t['actual_external_calls']==0
 assert t['parent'] in {c['jira'] for c in catalog}
report={'source_commit':os.environ.get('GITHUB_SHA','local-uncommitted'),'scope':'offline_partial_utilities_and_spec_tooling','tests':result.testsRun,'passed':result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors),'feature_contracts_checked':len(catalog),'subtask_contracts_checked':len(tasks),'partial_utility_feature_mappings':sum(bool(c['implementation']) for c in catalog),'actual_hardware_calls':0,'actual_provider_calls':0,'actual_participants':0,'actual_notifications':0,'actual_payments':0,'actual_patent_filings':0,'actual_outreach':0,'release_ready':False,'pending':['real adapters and integrated service implementation','hardware and user validation','production identity/KMS/OTA signatures/bootloader','PG/notification/Cloud/CAD/search/CRM service connections','expert legal/financial/content/safety reviews','verified real execution receipts and releases']}
p=ROOT/'Development/evidence';p.mkdir(exist_ok=True);(p/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False));sys.exit(0 if result.wasSuccessful() else 1)
