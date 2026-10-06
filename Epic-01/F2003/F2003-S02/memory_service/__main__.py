"""Synthetic API demo, production identities/consents are not provisioned by this CLI."""
import argparse,os
from pathlib import Path
from .fixtures import setup
from .api import server
from memory_contract import require

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--demo-dir',default='demo-data');parser.add_argument('--port',type=int,default=8083);args=parser.parse_args()
    token=os.environ.get('KER_MEMORY_DEV_TOKEN');require(isinstance(token,str) and len(token)>=32,'SET_KER_MEMORY_DEV_TOKEN')
    root=Path(args.demo_dir);require(not root.exists(),'USE_NEW_SYNTHETIC_DEMO_DIRECTORY');root.mkdir(parents=True)
    profiles,memory,pid=setup(root);http=server(memory,token,'demo-owner',pid,'demo-device',port=args.port)
    print('Synthetic development API on loopback; requires token. No production users or cloud adapter.')
    try:http.serve_forever()
    except KeyboardInterrupt:pass
    finally:http.server_close();memory.close();profiles.close()
if __name__=='__main__':main()
