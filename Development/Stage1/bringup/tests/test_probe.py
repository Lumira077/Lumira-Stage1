import unittest,sys,json,copy,os,pty,threading,select
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from probe import validate_config,parse_identity,request,exchange,run
C=json.loads((Path(__file__).resolve().parents[1]/'config.example.json').read_text())
N='0123456789abcdef'
def frame(role='A',nonce=N):return f'LUMIRA1 {nonce} {role} UNO_R4_MINIMA probe-1 MOTION_DISABLED\n'.encode()
class ConfigTests(unittest.TestCase):
 def test_baseline(self):self.assertEqual(validate_config(copy.deepcopy(C))['compute']['ram_gb'],8)
 def test_no_motion(self):
  c=copy.deepcopy(C);c['motion_enabled']=True
  with self.assertRaises(ValueError):validate_config(c)
 def test_unsupported_model(self):
  c=copy.deepcopy(C);c['boards']['A']['model']='UNO_R3'
  with self.assertRaises(ValueError):validate_config(c)
 def test_duplicate_ports(self):
  c=copy.deepcopy(C);c['boards']['B']['port']=c['boards']['A']['port']
  with self.assertRaises(ValueError):validate_config(c)
 def test_unstable_port(self):
  c=copy.deepcopy(C);c['boards']['A']['port']='/dev/ttyACM0'
  with self.assertRaises(ValueError):validate_config(c)
 def test_wrong_network(self):
  c=copy.deepcopy(C);c['network']['pi']='10.0.0.2'
  with self.assertRaises(ValueError):validate_config(c)
 def test_duplicate_ip(self):
  c=copy.deepcopy(C);c['network']['pi']=c['network']['pc']
  with self.assertRaises(ValueError):validate_config(c)
 def test_unconfirmed_blocks_probe(self):
  with self.assertRaises(ValueError):run(C,'probe',lambda *a:self.fail('must not open'))
 def test_simulation_has_no_hardware_claim(self):
  r=run(C,'simulate');self.assertFalse(r['physical_transport_exercised']);self.assertFalse(r['release_ready'])
class ProtocolTests(unittest.TestCase):
 def test_roundtrip(self):self.assertTrue(parse_identity(frame(),N,'A')['identity_matched'])
 def test_wrong_role(self):
  with self.assertRaises(ValueError):parse_identity(frame('B'),N,'A')
 def test_stale_nonce(self):
  with self.assertRaises(ValueError):parse_identity(frame(nonce='0'*16),N,'A')
 def test_motion_enabled_rejected(self):
  with self.assertRaises(ValueError):parse_identity(frame().replace(b'DISABLED',b'ENABLED'),N,'A')
 def test_extra_line(self):
  with self.assertRaises(ValueError):parse_identity(frame()+b'\n',N,'A')
 def test_oversize(self):
  with self.assertRaises(ValueError):parse_identity(b'x'*129+b'\n',N,'A')
 def test_nonascii(self):
  with self.assertRaises(ValueError):parse_identity(b'\xff\n',N,'A')
 def test_nonce_injection(self):
  with self.assertRaises(ValueError):request('0'*16+'\nMOVE')
 def test_truncated(self):
  with self.assertRaises(ValueError):parse_identity(frame()[:-1],N,'A')
class SerialTests(unittest.TestCase):
 def test_real_os_pty_transport(self):
  master,slave=pty.openpty();errors=[];seen=[]
  def device():
   try:
    buf=b''
    while b'\n' not in buf:
     if not select.select([master],[],[],2)[0]:raise TimeoutError('host missing')
     buf+=os.read(master,128)
    seen.append(buf);os.write(master,frame())
   except Exception as e:errors.append(e)
  t=threading.Thread(target=device);t.start()
  try:
   self.assertEqual(exchange(os.ttyname(slave),N,2),frame());t.join(3)
   self.assertFalse(t.is_alive());self.assertEqual(errors,[]);self.assertEqual(seen,[request(N)])
  finally:os.close(master);os.close(slave)
 def test_timeout_closes_port(self):
  master,slave=pty.openpty()
  try:
   with self.assertRaises(TimeoutError):exchange(os.ttyname(slave),N,.03)
   # A second open succeeds because exclusive ownership was released on failure.
   with self.assertRaises(TimeoutError):exchange(os.ttyname(slave),N,.03)
  finally:os.close(master);os.close(slave)
