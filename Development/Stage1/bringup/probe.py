"""Pi/UNO identity-only bring-up. Never emits actuator commands.
Linux serial support uses stdlib; opening USB can reset a board.
Disconnect actuator power before probing. Protocol identity is not authentication.
"""
import argparse, ipaddress, json, os, re, secrets, select, time
from pathlib import Path

MODEL='UNO_R4_MINIMA'
PATTERN=re.compile(r'[0-9a-f]{16}')

def validate_config(c):
    if not isinstance(c,dict) or c.get('schema')!='lumira-bringup-v1':raise ValueError('schema')
    if c.get('compute')!={'model':'PI5','ram_gb':8,'accelerator':'HAILO8L_13TOPS'}:raise ValueError('compute baseline')
    if c.get('motion_enabled') is not False:raise ValueError('identity-only mode required')
    if c.get('stage')!=1 or type(c['stage']) is not int:raise ValueError('stage')
    boards=c.get('boards')
    if not isinstance(boards,dict) or set(boards)!={'A','B'}:raise ValueError('board roles')
    paths=[]
    for role,b in boards.items():
        if not isinstance(b,dict) or b.get('model')!=MODEL:raise ValueError('unsupported board')
        path=b.get('port')
        if not isinstance(path,str) or not path.startswith('/dev/serial/by-id/') or '/' in path[len('/dev/serial/by-id/'): ] or not path[len('/dev/serial/by-id/'):]:raise ValueError('stable port required')
        if type(b.get('confirmed')) is not bool:raise ValueError('confirmation')
        paths.append(path)
    if len(set(paths))!=2:raise ValueError('duplicate port')
    net=c.get('network')
    if not isinstance(net,dict) or set(net)!={'pc','pi','nas','subnet'}:raise ValueError('network fields')
    if any(not isinstance(v,str) for v in net.values()):raise ValueError('network strings')
    subnet=ipaddress.ip_network(net['subnet'])
    ips=[ipaddress.ip_address(net[k]) for k in ('pc','pi','nas')]
    if subnet.version!=4 or len(set(ips))!=3 or any(ip not in subnet or ip in (subnet.network_address,subnet.broadcast_address) for ip in ips):raise ValueError('network addresses')
    return c

def request(nonce):
    if not isinstance(nonce,str) or not PATTERN.fullmatch(nonce):raise ValueError('nonce')
    return ('HELLO '+nonce+'\n').encode('ascii')

def parse_identity(line,nonce,role):
    request(nonce)
    if role not in ('A','B'):raise ValueError('role')
    if not isinstance(line,bytes) or len(line)>128 or not line.endswith(b'\n'):raise ValueError('frame')
    try:parts=line.decode('ascii').removesuffix('\n').removesuffix('\r').split(' ')
    except UnicodeDecodeError:raise ValueError('encoding') from None
    expected=['LUMIRA1',nonce,role,MODEL,'probe-1','MOTION_DISABLED']
    if parts!=expected:raise ValueError('identity mismatch')
    return {'role':role,'model':MODEL,'firmware':'probe-1','identity_matched':True,'motion_enabled':False,'physical_stop_verified':False}

def exchange(port,nonce,timeout=3.0):
    import termios, tty, fcntl
    if not 0<timeout<=10:raise ValueError('timeout')
    fd=os.open(port,os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK)
    exclusive=False
    try:
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        # Exclusive TTY ownership also rejects competing non-flock users on Linux.
        fcntl.ioctl(fd,termios.TIOCEXCL);exclusive=True
        tty.setraw(fd)
        attrs=termios.tcgetattr(fd);attrs[4]=termios.B115200;attrs[5]=termios.B115200
        attrs[0]&=~(termios.IXOFF|termios.IXANY)
        attrs[2]&=~(termios.PARENB|termios.CSTOPB|termios.CSIZE|getattr(termios,'CRTSCTS',0))
        attrs[2]|=termios.CS8|termios.CLOCAL|termios.CREAD
        termios.tcsetattr(fd,termios.TCSANOW,attrs)
        termios.tcflush(fd,termios.TCIFLUSH)
        deadline=time.monotonic()+timeout;pending=request(nonce);out=bytearray()
        while time.monotonic()<deadline:
            readable,writable,_=select.select([fd],[fd] if pending else [],[],max(0,deadline-time.monotonic()))
            if writable:
                try:pending=pending[os.write(fd,pending):]
                except BlockingIOError:pass
            if readable:
                try:chunk=os.read(fd,128)
                except BlockingIOError:continue
                if not chunk:raise ConnectionError('serial disconnected')
                out.extend(chunk)
                if len(out)>128:raise ValueError('frame too long')
                if b'\n' in out:return bytes(out)
        raise TimeoutError('identity timeout; board may have reset; retry after boot')
    finally:
        try:
            if exclusive:fcntl.ioctl(fd,termios.TIOCNXCL)
        finally:os.close(fd)

def run(c,mode,transport=exchange):
    validate_config(c)
    results=[]
    if mode not in ('check','simulate','probe'):raise ValueError('mode')
    for role,b in c['boards'].items():
        row={'role':role,'model_confirmed':b['confirmed'],'mode':mode}
        if mode=='check':row['port_exists']=Path(b['port']).exists()
        else:
            nonce=secrets.token_hex(8)
            if mode=='probe' and not b['confirmed']:raise ValueError('confirm physical UNO model before probe')
            line=(f'LUMIRA1 {nonce} {role} {MODEL} probe-1 MOTION_DISABLED\n'.encode() if mode=='simulate' else transport(b['port'],nonce))
            row.update(parse_identity(line,nonce,role))
        results.append(row)
    return {'mode':mode,'boards':results,'physical_transport_exercised':mode=='probe','motion_enabled':False,'release_ready':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default=str(Path(__file__).with_name('config.example.json')))
    p.add_argument('--mode',choices=['check','simulate','probe'],default='check');p.add_argument('--output')
    a=p.parse_args()
    try:r=run(json.loads(Path(a.config).read_text()),a.mode);code=0
    except (ValueError,OSError,TimeoutError,ConnectionError) as e:r={'error':str(e),'motion_enabled':False,'release_ready':False};code=2
    text=json.dumps(r,indent=2,ensure_ascii=False)
    if a.output:Path(a.output).write_text(text+'\n')
    print(text);return code
if __name__=='__main__':raise SystemExit(main())
