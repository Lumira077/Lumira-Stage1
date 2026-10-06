"""Start a real local API and replay three registration paths, including output retry."""
import os,secrets,socket,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.request import urlopen
root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env=dict(os.environ,KER_DEMO_TOKEN=secrets.token_urlsafe(32),KER_GUARDIAN_TOKEN=secrets.token_urlsafe(32),
             KER_API_BASE=f'http://127.0.0.1:{port}',KER_ADAPTER_MODE='simulated',KER_SIM_FAIL_ONCE='tts')
    proc=subprocess.Popen([sys.executable,'-m','ker_onboarding.api','--db',str(Path(tmp)/'prototype.sqlite3'),'--port',str(port)],cwd=root,env=env,stdout=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                with urlopen(env['KER_API_BASE']+'/health',timeout=1) as res:assert res.status==200
                break
            except OSError:
                if proc.poll() is not None:raise RuntimeError('API startup failed')
                time.sleep(.05)
        else:raise RuntimeError('API startup timeout')
        for path in ['/','/app.js','/style.css','/openapi.json']:
            with urlopen(env['KER_API_BASE']+path,timeout=2) as res:assert res.status==200
        subprocess.run([sys.executable,'scripts/demo.py'],cwd=root,env=env,check=True,timeout=15)
        print('HTTP smoke PASS: self + guest + guardian + failure retry; simulated only')
    finally:
        proc.terminate()
        try:proc.wait(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
