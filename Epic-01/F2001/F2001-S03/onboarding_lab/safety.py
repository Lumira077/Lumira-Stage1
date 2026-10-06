"""Software output gating only. This is not a certified physical safety controller."""
from dataclasses import dataclass
import json,sqlite3,time,uuid

class Rejected(Exception):pass

def check(condition,code):
    if not condition:raise Rejected(code)

@dataclass(frozen=True)
class Policy:
    max_volume:int=20  # normalized software volume, NOT an acoustic dB measurement
    max_rate:float=1.2
    max_expression:int=1
    max_gesture_level:int=1
    command_ttl_seconds:float=3.0

class SimulatedTransport:
    mode='simulated'
    def __init__(self):self.events=[];self.fail_stop=False
    def execute(self,command_id,kind,payload):
        self.events.append({'command_id':command_id,'kind':kind})
        return {'command_id':command_id,'ack':True,'adapter_mode':'simulated','physical_output':False}
    def stop(self):
        if self.fail_stop:raise RuntimeError('injected stop failure')
        return {'ack':True,'adapter_mode':'simulated','physical_output':False}

class Broker:
    def __init__(self,path,transport=None,clock=time.time,policy=None):
        self.clock,self.policy,self.transport=clock,policy or Policy(),transport or SimulatedTransport()
        check(self.transport.mode=='simulated','HARDWARE_ADAPTER_NOT_IMPLEMENTED')
        self.db=sqlite3.connect(path,isolation_level=None)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS scopes(id TEXT PRIMARY KEY,actor TEXT NOT NULL,epoch INTEGER NOT NULL,
          enabled INTEGER NOT NULL,connected INTEGER NOT NULL,stopped INTEGER NOT NULL,context_hash TEXT);
        CREATE TABLE IF NOT EXISTS commands(id TEXT PRIMARY KEY,scope TEXT REFERENCES scopes(id),
          epoch INTEGER NOT NULL,kind TEXT NOT NULL,request_key TEXT NOT NULL,deadline REAL NOT NULL,
          payload TEXT NOT NULL,state TEXT NOT NULL,receipt TEXT,UNIQUE(scope,kind,request_key));
        ''')
        # On process startup, suppress queued or uncertain previous output. No automatic rearm.
        with self.db:
            self.db.execute("UPDATE commands SET state='cancelled' WHERE state IN ('queued','executing')")
            self.db.execute('UPDATE scopes SET enabled=0,epoch=epoch+1')
    def close(self):self.db.close()
    def _scope(self,sid,actor):
        row=self.db.execute('SELECT * FROM scopes WHERE id=?',(sid,)).fetchone()
        check(row is not None and row[1]==actor,'NOT_FOUND');return row
    def begin(self,sid,actor,context_hash=None):
        old=self.db.execute('SELECT id FROM scopes WHERE id=?',(sid,)).fetchone()
        if not old:self.db.execute('INSERT INTO scopes VALUES (?,?,1,1,1,0,?)',(sid,actor,context_hash))
        return self._scope(sid,actor)[2]
    def _ready(self,row,epoch):
        check(type(epoch) is int and row[2]==epoch,'STALE_EPOCH');check(not row[5],'STOP_LATCHED')
        check(row[3]==1,'OUTPUT_DISABLED');check(row[4]==1,'DISCONNECTED')
    def validate(self,kind,payload):
        check(isinstance(payload,dict),'INVALID_PAYLOAD')
        if kind in ('tts','first_greeting'):
            check(set(payload)=={'volume','speech_rate'},'INVALID_PAYLOAD')
            check(type(payload['volume']) is int and 0<=payload['volume']<=self.policy.max_volume,'VOLUME_LIMIT')
            check(type(payload['speech_rate']) in (int,float) and .7<=payload['speech_rate']<=self.policy.max_rate,'RATE_LIMIT')
        elif kind=='expression':
            check(set(payload)=={'level'} and type(payload['level']) is int and 0<=payload['level']<=self.policy.max_expression,'EXPRESSION_LIMIT')
        elif kind=='motion':
            check(set(payload)=={'gesture','level'} and payload['gesture']=='none','UNAPPROVED_MOTION')
            check(type(payload['level']) is int and 0<=payload['level']<=self.policy.max_gesture_level,'GESTURE_LIMIT')
        elif kind=='context':check(payload=={},'INVALID_PAYLOAD')
        else:raise Rejected('UNKNOWN_OUTPUT')
    def submit(self,sid,actor,epoch,kind,payload,request_key):
        row=self._scope(sid,actor);self._ready(row,epoch);self.validate(kind,payload)
        check(isinstance(request_key,str) and 1<=len(request_key)<=80,'INVALID_REQUEST_KEY')
        old=self.db.execute('SELECT id,payload FROM commands WHERE scope=? AND kind=? AND request_key=?',(sid,kind,request_key)).fetchone()
        encoded=json.dumps(payload,sort_keys=True,allow_nan=False)
        if old:check(old[1]==encoded,'IDEMPOTENCY_CONFLICT');return old[0]
        cid=str(uuid.uuid4());self.db.execute('INSERT INTO commands VALUES (?,?,?,?,?,?,?,?,?)',
            (cid,sid,epoch,kind,request_key,self.clock()+self.policy.command_ttl_seconds,encoded,'queued',None));return cid
    def dispatch(self,cid,actor):
        c=self.db.execute('SELECT * FROM commands WHERE id=?',(cid,)).fetchone();check(c is not None,'NOT_FOUND')
        scope=self._scope(c[1],actor)
        # Authorization and current safety state are checked even for duplicate requests.
        self._ready(scope,c[2]);check(c[7] in ('queued','done'),'COMMAND_CANCELLED')
        if c[7]=='done':return json.loads(c[8])
        if self.clock()>=c[5]:
            self.db.execute("UPDATE commands SET state='cancelled' WHERE id=?",(cid,));raise Rejected('COMMAND_EXPIRED')
        self.validate(c[3],json.loads(c[6]))
        self.db.execute("UPDATE commands SET state='executing' WHERE id=?",(cid,))
        try:
            receipt=self.transport.execute(cid,c[3],json.loads(c[6]))
            check(receipt.get('ack') is True and receipt.get('command_id')==cid and receipt.get('adapter_mode')=='simulated' and receipt.get('physical_output') is False,'INVALID_OUTPUT_ACK')
        except Exception:
            self.db.execute("UPDATE commands SET state='cancelled' WHERE id=?",(cid,));self.stop(c[1],actor)
            raise Rejected('OUTPUT_FAILED')
        self.db.execute("UPDATE commands SET state='done',receipt=? WHERE id=?",(json.dumps(receipt),cid));return receipt
    def stop(self,sid,actor,latch=True):
        self._scope(sid,actor)
        # Persist suppression BEFORE attempting stop on the transport.
        self.db.execute('UPDATE scopes SET enabled=0,epoch=epoch+1,stopped=MAX(stopped,?) WHERE id=?',(int(latch),sid))
        self.db.execute("UPDATE commands SET state='cancelled' WHERE scope=? AND state IN ('queued','executing')",(sid,))
        try:
            receipt=self.transport.stop();confirmed=receipt.get('ack') is True
        except Exception:confirmed=False
        return {'stop_ack':confirmed,'adapter_mode':'simulated','physical_stop_verified':False}
    def disconnect(self,sid,actor):
        result=self.stop(sid,actor,latch=False);self.db.execute('UPDATE scopes SET connected=0 WHERE id=?',(sid,));return result
    def rearm(self,sid,actor,inspection_confirmed=False):
        row=self._scope(sid,actor)
        check(inspection_confirmed is True,'EXPLICIT_INSPECTION_REQUIRED')
        self.db.execute('UPDATE scopes SET stopped=0,connected=1,enabled=1,epoch=epoch+1 WHERE id=?',(sid,))
        return self._scope(sid,actor)[2]


def confirmed_input(field,value,confirmed):
    check(field in ('preferred_name','consent'),'UNKNOWN_CRITICAL_FIELD')
    check(confirmed is True,'USER_CONFIRMATION_REQUIRED')
    if field=='consent':check(type(value) is bool,'INVALID_CONSENT')
    else:check(isinstance(value,str) and 1<=len(value.strip())<=40,'INVALID_NAME')
    return value
