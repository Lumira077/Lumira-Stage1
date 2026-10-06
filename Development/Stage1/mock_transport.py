"""Two processes, localhost TCP. NOT ROS/DDS; hardware execution always false."""
import socket,subprocess,sys,json,time,platform,hashlib
from pathlib import Path
from contract_core import Validator,envelope,fixtures,Reject
P=Path(__file__).parent
if len(sys.argv)>1 and sys.argv[1]=='publisher':
 with socket.create_connection(('127.0.0.1',int(sys.argv[2])),timeout=5) as s:
  for i,(t,p) in enumerate(fixtures()):s.sendall((json.dumps(envelope(t,p,i))+'\n').encode())
 sys.exit(0)
rows=[];v=Validator('sprint1_demo')
with socket.socket() as listener:
 listener.bind(('127.0.0.1',0));listener.listen(1);listener.settimeout(5)
 proc=subprocess.Popen([sys.executable,__file__,'publisher',str(listener.getsockname()[1])])
 conn,_=listener.accept()
 with conn,conn.makefile('rb') as f:
  for line in f:
   m=json.loads(line);now=time.monotonic_ns()
   try:r=v.accept(m,now);r['result']='accepted'
   except Reject as e:r={'result':'rejected','reason':str(e),'hardware_execution':False}
   rows.append({'transport':'localhost_tcp_not_dds','subscriber_pid':__import__('os').getpid(),'publisher_pid':proc.pid,'seq':m['seq'],'topic':m['topic'],'latency_ms':(now-m['sent_monotonic_ns'])/1e6,**r})
 if proc.wait(timeout=5)!=0:raise RuntimeError('publisher failed')
expected=['accepted']*6+['rejected']
assert [r['result'] for r in rows]==expected,rows
assert rows[-1]['reason']=='inhibited'
(P/'evidence/mock_transport.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
summary={'mode':'Python TCP mock only; not DDS','messages':len(rows),'accepted':6,'expected_rejections':1,'unexpected_results':0,'ros2_executed':False,'hardware_execution':False,'release_ready':False,'python':sys.version,'platform':platform.platform(),'source_sha256':hashlib.sha256((P/'contract_core.py').read_bytes()).hexdigest()}
(P/'evidence/mock_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
