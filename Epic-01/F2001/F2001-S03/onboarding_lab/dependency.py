"""Resolve the adjacent, version-checked S02 source; no package download."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent.parent
S02=ROOT.parent/'F2001-S02'
if not S02.is_dir():S02=ROOT.parent/'ker-f2001-s02'  # local development layout

def verify():
    manifest=json.loads((ROOT/'docs/dependency.json').read_text())
    for relative,digest in manifest['sha256'].items():
        path=S02/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise RuntimeError('S02 dependency differs from pinned manifest: '+relative)
    return manifest

verify()
sys.path.insert(0,str(S02))
