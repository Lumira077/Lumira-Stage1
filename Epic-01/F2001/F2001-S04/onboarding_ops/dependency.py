from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
S02=ROOT.parent/'F2001-S02';S03=ROOT.parent/'F2001-S03'
if not S02.is_dir():S02=ROOT.parent/'ker-f2001-s02'
if not S03.is_dir():S03=ROOT.parent/'ker-f2001-s03'
def verify():
    manifest=json.loads((ROOT/'docs/dependency.json').read_text())
    for name,base in [('S02',S02),('S03',S03)]:
        for relative,digest in manifest[name]['sha256'].items():
            path=base/relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise RuntimeError(name+' dependency mismatch: '+relative)
    return manifest
verify();sys.path.insert(0,str(S03))
