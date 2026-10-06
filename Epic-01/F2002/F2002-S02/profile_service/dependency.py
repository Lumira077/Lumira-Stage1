from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent
manifest=ROOT/'dependencies.json'
for name,expected in json.loads(manifest.read_text()).items():
    p=BASE/name
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise RuntimeError('Dependency hash mismatch: '+name)
sys.path.insert(0,str(BASE/'F2002-S01'))
