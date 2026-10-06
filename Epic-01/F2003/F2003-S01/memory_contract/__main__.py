import argparse,json
from pathlib import Path
from . import validate,Error

def main():
    p=argparse.ArgumentParser();p.add_argument('file');args=p.parse_args()
    try:validate(json.loads(Path(args.file).read_text()));print('MEMORY_CONTRACT_VALID');return 0
    except (Error,ValueError,OSError):print('INVALID_MEMORY_DOCUMENT');return 1
if __name__=='__main__':raise SystemExit(main())
