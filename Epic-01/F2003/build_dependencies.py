from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
for dest,dirs in [('F2003-S02',['F2003-S01']),('F2003-S03',['F2003-S01','F2003-S02']),('F2003-S04',['F2003-S01','F2003-S02','F2003-S03'])]:
    entries={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for d in dirs for p in (ROOT/d).rglob('*.py') if 'tests' not in p.parts}
    (ROOT/dest/'dependencies.json').write_text(json.dumps(entries,indent=2)+'\n')
base=ROOT.parent/'ker-f2002'
if not base.exists():base=ROOT.parent/'F2002'
entries={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ('F2002-S01','F2002-S02') for p in (base/d).rglob('*.py') if 'tests' not in p.parts}
(ROOT/'F2003-S02/f2002-dependency.json').write_text(json.dumps({'commit':'3fd646a51f0d437dc2a62829bcb7b602544c98ae','sha256':entries},indent=2)+'\n')
