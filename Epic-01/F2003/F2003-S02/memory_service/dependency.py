from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
for name,expected in json.loads((ROOT/'dependencies.json').read_text()).items():
    if hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('Dependency hash mismatch: '+name)
sys.path.insert(0,str(ROOT.parent/'F2003-S01'))
# Repository layout, plus local sibling checkout used by the development workspace.
F2002=ROOT.parent.parent/'F2002'
if not F2002.exists():F2002=ROOT.parent.parent/'ker-f2002'
for name,expected in json.loads((ROOT/'f2002-dependency.json').read_text())['sha256'].items():
    if hashlib.sha256((F2002/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('F2002 dependency hash mismatch: '+name)
sys.path.insert(0,str(F2002/'F2002-S02'))
import profile_service
