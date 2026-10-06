"""Run the real HTTP API and demo in an isolated database with an ephemeral token."""
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen
root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env=dict(os.environ,KER_DEMO_TOKEN=secrets.token_urlsafe(32),KER_API_BASE=f'http://127.0.0.1:{port}')
    proc=subprocess.Popen([sys.executable,'-m','ker_onboarding.api','--db',str(Path(tmp)/'smoke.sqlite3'),'--port',str(port)],cwd=root,env=env,stdout=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                with urlopen(env['KER_API_BASE']+'/health',timeout=1) as res:assert res.status==200
                break
            except OSError:
                if proc.poll() is not None:raise RuntimeError('API startup failed')
                time.sleep(0.05)
        else:raise RuntimeError('API startup timeout')
        with urlopen(env['KER_API_BASE']+'/openapi.json',timeout=2) as res:assert res.status==200
        subprocess.run([sys.executable,'scripts/demo.py'],cwd=root,env=env,check=True,timeout=10)
        print('HTTP smoke PASS')
    finally:
        proc.terminate()
        try:proc.wait(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
