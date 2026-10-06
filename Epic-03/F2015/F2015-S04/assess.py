import json,sys
from pathlib import Path
if __name__=="__main__":
 r=json.loads(Path(sys.argv[1]).read_text());print(json.dumps({"feature":"F2015","source_commit":r.get("source_commit"),"simulation_passed":r.get("passed") is True and r.get("per_feature_tests",{}).get("F2015",0)>0,"release_ready":False,"actual_participants":0}))
