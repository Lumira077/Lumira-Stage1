"""Evaluate CI coverage; this script is not an operational approval authority."""
import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/"runtime"))
from operations import assess
if __name__=="__main__":
 print(json.dumps(assess("F2123",json.loads(pathlib.Path(sys.argv[1]).read_text())),ensure_ascii=False,indent=2))
