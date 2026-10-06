"""Strict, pseudonymous event storage. No free text or user content fields."""
import hashlib,hmac,json,math,re,sqlite3,time
KINDS={'onboarding_started','step_entered','step_completed','step_failed','resume_attempt','onboarding_resumed',
       'registration_committed','apply_attempt','context_apply_failed','onboarding_ready','onboarding_cancelled',
       'support_requested','duplicate_registration'}
STEPS={'registration','language','profile','purpose','preferences','consent','review'}
ERRORS={'REVISION_CONFLICT','INVALID_INPUT','DEVICE_DISCONNECTED','MODULE_APPLY_FAILED','SESSION_EXPIRED','NOT_FOUND','INTERNAL_ERROR'}
FIELDS={'step','error_code','module','latency_ms','success','attempt_id'}
class Invalid(ValueError):pass

def check(ok,message):
    if not ok:raise Invalid(message)

class Sink:
    def __init__(self,path,key,version='0.4.0',clock=time.time,mode='simulated'):
        check(isinstance(key,bytes) and len(key)>=32,'Telemetry key must contain at least 32 bytes')
        check(bool(re.fullmatch(r'\d+\.\d+\.\d+',version)),'Invalid version')
        check(mode in ('simulated','observed'),'Invalid mode')
        self.key,self.version,self.clock,self.mode=key,version,clock,mode
        self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY,session TEXT,kind TEXT,stamp REAL,version TEXT,route TEXT,mode TEXT,data TEXT)')
        self.db.commit()
    def close(self):self.db.close()
    def digest(self,value):return hmac.new(self.key,value.encode(),hashlib.sha256).hexdigest()
    def emit(self,raw_session,kind,route='unknown',stable_key=None,**data):
        check(isinstance(raw_session,str) and raw_session,'Invalid session')
        check(kind in KINDS,'Unknown event');check(route in ('self','guardian','guest','unknown'),'Invalid route')
        check(set(data)<=FIELDS,'Forbidden telemetry fields')
        if 'step' in data:check(data['step'] in STEPS,'Invalid step')
        if 'error_code' in data:check(data['error_code'] in ERRORS,'Unapproved error code')
        if 'module' in data:check(data['module'] in ('context','tts','expression','motion'),'Invalid module')
        if 'latency_ms' in data:check(type(data['latency_ms']) in (int,float) and math.isfinite(data['latency_ms']) and 0<=data['latency_ms']<=86400000,'Invalid latency')
        if 'success' in data:check(type(data['success']) is bool,'Invalid success')
        if 'attempt_id' in data:check(bool(re.fullmatch(r'[0-9a-f]{32}',data['attempt_id'])),'Invalid attempt id')
        stamp=self.clock();check(type(stamp) in (int,float) and math.isfinite(stamp) and stamp>=0,'Invalid timestamp')
        session=self.digest('session:'+raw_session)
        import uuid
        event_id=self.digest('event:'+raw_session+':'+kind+':'+(stable_key or uuid.uuid4().hex))
        payload=json.dumps(data,sort_keys=True,allow_nan=False)
        old=self.db.execute('SELECT session,kind,version,route,mode,data FROM events WHERE event_id=?',(event_id,)).fetchone()
        values=(session,kind,self.version,route,self.mode,payload)
        if old:
            check(old==values,'Event idempotency conflict');return event_id
        self.db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?)',(event_id,session,kind,stamp,self.version,route,self.mode,payload));self.db.commit();return event_id
    def read(self):
        return [{'event_id':r[0],'session':r[1],'kind':r[2],'timestamp':r[3],'version':r[4],'route':r[5],'mode':r[6],**json.loads(r[7])}
                for r in self.db.execute('SELECT * FROM events ORDER BY stamp,event_id')]
    def purge_before(self,cutoff):
        check(type(cutoff) in (int,float) and math.isfinite(cutoff) and cutoff>=0,'Invalid cutoff')
        n=self.db.execute('DELETE FROM events WHERE stamp<?',(cutoff,)).rowcount;self.db.commit();return n
