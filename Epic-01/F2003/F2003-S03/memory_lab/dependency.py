from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
for name,expected in json.loads((ROOT/'dependencies.json').read_text()).items():
    if hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('Dependency hash mismatch: '+name)
sys.path.insert(0,str(ROOT.parent/'F2003-S02'))
import memory_service
