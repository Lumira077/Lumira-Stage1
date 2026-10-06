"""Run from repository root with a CI report path; approval system is not connected."""
import json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'integration'))
from operations import release_assessment
if __name__=='__main__':
    result=release_assessment(json.loads(pathlib.Path(sys.argv[1]).read_text()))
    print(json.dumps({'feature':'F2157',**result},ensure_ascii=False,indent=2))
