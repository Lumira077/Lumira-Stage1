"""Single-process SQLite profile service. Identity is supplied by a trusted caller."""
import copy,hashlib,json,sqlite3,time,uuid
from contextlib import contextmanager
from profile_contract import Error,require,text,validate,patch,context,DEFAULTS,CONSENTS

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
class Service:
    def __init__(self,path,clock=time.time):
        self.clock=clock;self.db=sqlite3.connect(path,isolation_level=None);self.db.execute('PRAGMA foreign_keys=ON');self.db.execute('PRAGMA busy_timeout=5000')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS schema_metadata(version INTEGER PRIMARY KEY);
        INSERT OR IGNORE INTO schema_metadata VALUES(1);
        CREATE TABLE IF NOT EXISTS profiles(id TEXT PRIMARY KEY,owner TEXT,subject TEXT,data TEXT,revision INTEGER);
        CREATE TABLE IF NOT EXISTS devices(id TEXT PRIMARY KEY,owner TEXT,connected INTEGER,stopped INTEGER,active TEXT,generation INTEGER);
        CREATE TABLE IF NOT EXISTS mutations(owner TEXT,key TEXT,digest TEXT,profile TEXT,revision INTEGER,PRIMARY KEY(owner,key));
        CREATE TABLE IF NOT EXISTS applications(id TEXT PRIMARY KEY,profile TEXT,revision INTEGER,device TEXT,generation INTEGER,state TEXT,attempts INTEGER,error TEXT);
        CREATE TABLE IF NOT EXISTS acks(application TEXT,module TEXT,receipt TEXT,PRIMARY KEY(application,module));
        CREATE TABLE IF NOT EXISTS imports(source TEXT PRIMARY KEY,owner TEXT,profile TEXT);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,stamp REAL,kind TEXT,code TEXT);
        ''')
        require(self.db.execute('SELECT version FROM schema_metadata').fetchall()==[(1,)],'INCOMPATIBLE_SCHEMA',409)
    def close(self):self.db.close()
    @contextmanager
    def tx(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:yield;self.db.execute('COMMIT')
        except Exception:self.db.execute('ROLLBACK');raise
    def event(self,kind,code='OK'):self.db.execute('INSERT INTO events(stamp,kind,code) VALUES(?,?,?)',(self.clock(),kind,code))
    def get(self,pid,actor):
        row=self.db.execute('SELECT * FROM profiles WHERE id=?',(pid,)).fetchone();require(row is not None and row[1]==actor,'NOT_FOUND',404)
        return {'profile_id':row[0],'owner_id':row[1],'subject_id':row[2],'data':json.loads(row[3]),'revision':row[4]}
    def list(self,actor):return [self.get(x[0],actor) for x in self.db.execute('SELECT id FROM profiles WHERE owner=? ORDER BY id',(actor,)).fetchall()]
    def _mutation(self,actor,key,payload):
        text(actor,80);text(key,80);digest=hashlib.sha256(encode(payload).encode()).hexdigest()
        old=self.db.execute('SELECT digest,profile,revision FROM mutations WHERE owner=? AND key=?',(actor,key)).fetchone()
        if old:
            require(old[0]==digest,'IDEMPOTENCY_CONFLICT',409)
            p=self.get(old[1],actor);require(p['revision']==old[2],'IDEMPOTENCY_SUPERSEDED',409);return digest,p
        return digest,None
    def _record(self,actor,key,digest,p):self.db.execute('INSERT INTO mutations VALUES(?,?,?,?,?)',(actor,key,digest,p['profile_id'],p['revision']))
    def create(self,actor,data,key,subject=None,authorized_subjects=()):
        d=validate(data);subject=actor if subject is None else text(subject,80)
        require(subject==actor or subject in authorized_subjects,'SUBJECT_NOT_AUTHORIZED',403)
        with self.tx():
            h,old=self._mutation(actor,key,{'op':'create','subject':subject,'data':d})
            if old:return old
            pid=uuid.uuid4().hex;self.db.execute('INSERT INTO profiles VALUES(?,?,?,?,1)',(pid,actor,subject,encode(d)));p=self.get(pid,actor)
            self._record(actor,key,h,p);self.event('profile_created');return p
    def _invalidate(self,pid):
        ids=[r[0] for r in self.db.execute('SELECT id FROM applications WHERE profile=?',(pid,))]
        for aid in ids:self.db.execute('DELETE FROM acks WHERE application=?',(aid,))
        self.db.execute("UPDATE applications SET state='invalidated',error='PROFILE_CHANGED' WHERE profile=?",(pid,))
    def update(self,pid,actor,changes,revision,key):
        require(type(revision) is int and revision>0,'INVALID_REVISION')
        with self.tx():
            p=self.get(pid,actor);h,old=self._mutation(actor,key,{'op':'update','profile':pid,'changes':changes,'revision':revision})
            if old:return old
            require(p['revision']==revision,'REVISION_CONFLICT',409);d=patch(p['data'],changes)
            self.db.execute('UPDATE profiles SET data=?,revision=revision+1 WHERE id=?',(encode(d),pid));self._invalidate(pid)
            p=self.get(pid,actor);self._record(actor,key,h,p);self.event('profile_updated');return p
    def reset(self,pid,actor,revision,key):return self.update(pid,actor,{'preferences':copy.deepcopy(DEFAULTS)},revision,key)
    def delete(self,pid,actor,revision):
        require(type(revision) is int,'INVALID_REVISION')
        with self.tx():
            p=self.get(pid,actor);require(p['revision']==revision,'REVISION_CONFLICT',409);self._invalidate(pid)
            self.db.execute('DELETE FROM applications WHERE profile=?',(pid,));self.db.execute('DELETE FROM mutations WHERE profile=?',(pid,));self.db.execute('UPDATE imports SET profile=NULL WHERE profile=?',(pid,))
            self.db.execute('UPDATE devices SET active=NULL,generation=generation+1 WHERE active=?',(pid,));self.db.execute('DELETE FROM profiles WHERE id=?',(pid,));self.event('profile_deleted')
    def provision_device(self,device,owner):
        # Explicit trusted local fixture provisioning; never exposed through HTTP.
        text(device,80);text(owner,80)
        with self.tx():
            old=self.db.execute('SELECT owner FROM devices WHERE id=?',(device,)).fetchone();require(old is None or old[0]==owner,'DEVICE_NOT_AUTHORIZED',403)
            self.db.execute('INSERT OR IGNORE INTO devices VALUES(?,?,1,0,NULL,0)',(device,owner))
    def device(self,device,actor):
        r=self.db.execute('SELECT * FROM devices WHERE id=?',(device,)).fetchone();require(r is not None and r[1]==actor,'NOT_FOUND',404)
        return dict(zip(('device_id','owner','connected','stopped','active_profile','generation'),r))
    def set_device(self,device,actor,connected=None,stopped=None):
        require(connected is None or type(connected) is bool);require(stopped is None or type(stopped) is bool)
        with self.tx():
            self.device(device,actor)
            if connected is not None:self.db.execute('UPDATE devices SET connected=?,generation=generation+1 WHERE id=?',(int(connected),device))
            if stopped is not None:self.db.execute('UPDATE devices SET stopped=?,generation=generation+1 WHERE id=?',(int(stopped),device))
            self._invalidate_device(device)
    def _invalidate_device(self,device):
        for r in self.db.execute('SELECT id FROM applications WHERE device=?',(device,)).fetchall():self.db.execute('DELETE FROM acks WHERE application=?',r)
        self.db.execute("UPDATE applications SET state='invalidated',error='DEVICE_CHANGED' WHERE device=?",(device,))
    def activate(self,pid,actor,device,revision):
        require(type(revision) is int,'INVALID_REVISION')
        with self.tx():
            p=self.get(pid,actor);d=self.device(device,actor);require(p['revision']==revision,'REVISION_CONFLICT',409)
            require(d['connected'] and not d['stopped'],'DEVICE_NOT_READY',409)
            self._invalidate_device(device);self.db.execute('UPDATE devices SET active=?,generation=generation+1 WHERE id=?',(pid,device))
            generation=self.device(device,actor)['generation'];aid=uuid.uuid4().hex
            self.db.execute('INSERT INTO applications VALUES(?,?,?,?,?,?,0,NULL)',(aid,pid,revision,device,generation,'pending'));self.event('activation_requested')
            return self.application(aid,actor)
    def application(self,aid,actor):
        r=self.db.execute('SELECT * FROM applications WHERE id=?',(aid,)).fetchone();require(r is not None,'NOT_FOUND',404);self.get(r[1],actor);self.device(r[3],actor)
        return dict(zip(('application_id','profile_id','revision','device_id','generation','state','attempts','error_code'),r))
    def current_context(self,aid,actor):
        a=self.application(aid,actor);p=self.get(a['profile_id'],actor);d=self.device(a['device_id'],actor)
        require(a['state']!='invalidated' and p['revision']==a['revision'] and d['generation']==a['generation'] and d['active_profile']==p['profile_id'],'STALE_APPLICATION',409)
        require(d['connected'] and not d['stopped'],'DEVICE_NOT_READY',409)
        return context(p)
    def apply(self,aid,actor,outputs):
        # Adapters must be local/fast; no network IO while holding a DB transaction in production.
        from profile_contract import MODULES
        with self.tx():
            ctx=self.current_context(aid,actor);a=self.application(aid,actor)
            if a['state']=='applied':return a
            self.db.execute("UPDATE applications SET attempts=attempts+1,state='pending',error=NULL WHERE id=?",(aid,));self.event('apply_attempt')
            for module in MODULES:
                if self.db.execute('SELECT 1 FROM acks WHERE application=? AND module=?',(aid,module)).fetchone():continue
                try:
                    ack=outputs.apply(aid,module,ctx)
                    require(isinstance(ack,dict) and ack.get('ack') is True and ack.get('application_id')==aid and ack.get('module')==module and type(ack.get('revision')) is int and ack.get('revision')==a['revision'],'INVALID_ACK',409)
                    # Store receipt metadata only, never adapter payload/free text.
                    receipt={k:ack[k] for k in ('ack','application_id','module','revision')}
                    self.db.execute('INSERT INTO acks VALUES(?,?,?)',(aid,module,encode(receipt)))
                except Exception:
                    self.db.execute("UPDATE applications SET state='failed',error=? WHERE id=?",('MODULE_APPLY_FAILED:'+module,aid));self.event('apply_failed',module);return self.application(aid,actor)
            self.db.execute("UPDATE applications SET state='applied' WHERE id=?",(aid,));self.event('apply_succeeded');return self.application(aid,actor)
