import csv,json
from pathlib import Path
from core import study_metrics,freeze_readiness
p=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader(open(p/'studies/synthetic_fixture.csv')))
for r in rows:
 for k in ['consent','withdrawn','completed']:r[k]=r[k]=='true'
 r['duration_s']=float(r['duration_s']) if r['duration_s'] else None
 r['assistance_count']=int(r['assistance_count'])
f=json.load(open(p/'F2118/freeze_fixture.json'))
report={'data_type':'synthetic_fixture','user_test_performed':False,'metrics':study_metrics(rows),'freeze':freeze_readiness(f['assets'],f['issues'])}
(p/'synthetic_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
