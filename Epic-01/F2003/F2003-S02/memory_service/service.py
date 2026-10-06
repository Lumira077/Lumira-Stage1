"""Consent-gated local memory with transactional search index and context tickets."""
import hashlib,json,sqlite3,time,uuid
from contextlib import contextmanager
from memory_contract import Error,require,text,validate,normalized,relevance,policy as content_policy,opaque,extract

def encode(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
class Service:
    def __init__(self,path,policy,clock=time.time):
        self.policy,self.clock=policy,clock;self.db=sqlite3.connect(path,isolation_level=None);self.db.execute('PRAGMA foreign_keys=ON');self.db.execute('PRAGMA busy_timeout=5000')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS schema_metadata(version INTEGER PRIMARY KEY);
        INSERT OR IGNORE INTO schema_metadata VALUES(1);
        CREATE TABLE IF NOT EXISTS scopes(profile TEXT PRIMARY KEY,owner TEXT);
        CREATE TABLE IF NOT EXISTS scope_blocks(profile TEXT PRIMARY KEY,reason TEXT);
        CREATE TABLE IF NOT EXISTS memories(id TEXT PRIMARY KEY,owner TEXT,profile TEXT,kind TEXT,topic TEXT,content TEXT,source TEXT,confidence REAL,state TEXT,created REAL,updated REAL,expires REAL,revision INTEGER);
        CREATE TABLE IF NOT EXISTS search_index(memory TEXT PRIMARY KEY REFERENCES memories(id) ON DELETE CASCADE,terms TEXT);
        CREATE TABLE IF NOT EXISTS mutations(owner TEXT,profile TEXT,key TEXT,digest TEXT,memory TEXT,revision INTEGER,PRIMARY KEY(owner,profile,key));
        CREATE TABLE IF NOT EXISTS retired_keys(profile TEXT,token TEXT,PRIMARY KEY(profile,token));
        CREATE TABLE IF NOT EXISTS tickets(id TEXT PRIMARY KEY,owner TEXT,profile TEXT,stamp TEXT,refs TEXT,expires REAL);
        CREATE TABLE IF NOT EXISTS privacy_ledger(seq INTEGER PRIMARY KEY,operation TEXT,profile TEXT,memory TEXT,stamp REAL);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,stamp REAL,version TEXT,kind TEXT,code TEXT);
        ''')
        require(self.db.execute('SELECT version FROM schema_metadata').fetchall()==[(1,)],'INCOMPATIBLE_SCHEMA',409)
    def close(self):self.db.close()
    @contextmanager
    def tx(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:yield;self.db.execute('COMMIT')
        except Exception:self.db.execute('ROLLBACK');raise
    def event(self,kind,code='OK'):self.db.execute('INSERT INTO events(stamp,version,kind,code) VALUES(?,?,?,?)',(self.clock(),'0.1.0',kind,code))
    def _privacy(self,operation,pid,mid=None):
        self.db.execute('INSERT INTO privacy_ledger(operation,profile,memory,stamp) VALUES(?,?,?,?)',(operation,pid,mid,self.clock()))
    @staticmethod
    def _key_token(actor,pid,key):return hashlib.sha256((actor+'\0'+pid+'\0'+key).encode()).hexdigest()[:32]
    def _retire(self,pid,mid=None):
        rows=self.db.execute('SELECT owner,key FROM mutations WHERE profile=?'+(' AND memory=?' if mid is not None else ''),(pid,mid) if mid is not None else (pid,)).fetchall()
        for actor,key in rows:
            token=self._key_token(actor,pid,key);self.db.execute('INSERT OR IGNORE INTO retired_keys VALUES(?,?)',(pid,token));self._privacy('retire_key',pid,token)
    def _purge(self,pid,operation='revoke'):
        self._retire(pid);self._privacy(operation,pid);self.db.execute('DELETE FROM memories WHERE profile=?',(pid,));self.db.execute('DELETE FROM mutations WHERE profile=?',(pid,));self.db.execute('DELETE FROM tickets WHERE profile=?',(pid,));self.event('scope_purged')
    def _known(self,actor,pid):return self.db.execute('SELECT 1 FROM scopes WHERE profile=? AND owner=?',(pid,actor)).fetchone() is not None
    def _authorize(self,actor,pid,device,active=True,consent=True):
        text(actor,80);require(opaque(pid),'INVALID_PROFILE')
        try:stamp=self.policy.inspect(actor,pid,device,active=active)
        except Error as e:
            # A wrong actor must never cause someone else's memory deletion.
            if e.code=='NOT_FOUND' and self._known(actor,pid):
                try:self.policy.inspect(actor,pid,active=False)
                except Error:
                    with self.tx():self._purge(pid,'profile_deleted')
            raise
        self.db.execute('INSERT OR IGNORE INTO scopes VALUES(?,?)',(pid,actor))
        if consent and not stamp['long_term_memory']:
            with self.tx():
                self._purge(pid);self.db.execute("INSERT OR REPLACE INTO scope_blocks VALUES(?,'CONSENT_REVOKED')",(pid,))
            raise Error('MEMORY_CONSENT_REQUIRED',403)
        if consent:require(not self.db.execute('SELECT 1 FROM scope_blocks WHERE profile=?',(pid,)).fetchone(),'SCOPE_REGRANT_REQUIRED',403)
        return stamp
    def _expire(self):
        expired=self.db.execute('SELECT id,profile FROM memories WHERE expires<=?',(self.clock(),)).fetchall()
        for mid,pid in expired:
            self._retire(pid,mid);self._privacy('expire',pid,mid);self.db.execute('DELETE FROM memories WHERE id=?',(mid,));self.db.execute('DELETE FROM mutations WHERE memory=?',(mid,));self.db.execute('DELETE FROM tickets WHERE profile=?',(pid,));self.event('memory_expired')
        self.db.execute('DELETE FROM tickets WHERE expires<=?',(self.clock(),))
    def _row(self,mid,actor,pid):
        r=self.db.execute('SELECT * FROM memories WHERE id=? AND owner=? AND profile=?',(mid,actor,pid)).fetchone();require(r is not None,'NOT_FOUND',404)
        return dict(zip(('memory_id','owner_id','profile_id','kind','topic','content','source_ref','confidence','state','created_at','updated_at','expires_at','revision'),r))
    def _mutation(self,actor,pid,key,payload):
        text(key,80);require(not self.db.execute('SELECT 1 FROM retired_keys WHERE profile=? AND token=?',(pid,self._key_token(actor,pid,key))).fetchone(),'RETIRED_REQUEST',410);digest=hashlib.sha256(encode(payload).encode()).hexdigest();old=self.db.execute('SELECT digest,memory,revision FROM mutations WHERE owner=? AND profile=? AND key=?',(actor,pid,key)).fetchone()
        if old:
            require(old[0]==digest,'IDEMPOTENCY_CONFLICT',409);r=self._row(old[1],actor,pid);require(r['revision']==old[2],'IDEMPOTENCY_SUPERSEDED',409);return digest,r
        return digest,None
    def _record(self,actor,pid,key,digest,row):self.db.execute('INSERT INTO mutations VALUES(?,?,?,?,?,?)',(actor,pid,key,digest,row['memory_id'],row['revision']))
    def _invalidate(self,pid):self.db.execute('DELETE FROM tickets WHERE profile=?',(pid,))
    def create(self,actor,pid,device,data,key):
        self._authorize(actor,pid,device);d=validate(data)
        with self.tx():
            self._expire();h,old=self._mutation(actor,pid,key,{'op':'create','data':d})
            if old:return old
            duplicate=next(((mid,) for mid,content in self.db.execute("SELECT id,content FROM memories WHERE profile=? AND kind=? AND topic=? AND state IN ('candidate','confirmed')",(pid,d['kind'],d['topic'])) if normalized(content)==normalized(d['content'])),None)
            if duplicate:
                r=self._row(duplicate[0],actor,pid);self._record(actor,pid,key,h,r);return r
            mid=uuid.uuid4().hex;now=self.clock();self.db.execute('INSERT INTO memories VALUES(?,?,?,?,?,?,?,?,?,?,?,?,1)',(mid,actor,pid,d['kind'],d['topic'],d['content'],d['source_ref'],d['confidence'],'candidate',now,now,now+min(d['ttl_seconds'],604800)))
            r=self._row(mid,actor,pid);self._record(actor,pid,key,h,r);self.event('candidate_created');return r
    def capture(self,actor,pid,device,utterance,source_ref,key):
        self._authorize(actor,pid,device)
        candidates=extract(utterance,source_ref)
        return [self.create(actor,pid,device,d,key+':'+str(i)) for i,d in enumerate(candidates)]
    def get(self,actor,pid,device,mid):
        self._authorize(actor,pid,device)
        with self.tx():self._expire();return self._row(mid,actor,pid)
    def list(self,actor,pid,device):
        self._authorize(actor,pid,device)
        with self.tx():
            self._expire();return [self._row(r[0],actor,pid) for r in self.db.execute("SELECT id FROM memories WHERE profile=? AND state IN ('candidate','confirmed') ORDER BY created,id",(pid,)).fetchall()]
    def _supersede(self,pid,kind,topic,except_mid):
        ids=self.db.execute("SELECT id FROM memories WHERE profile=? AND kind=? AND topic=? AND id!=? AND state='confirmed'",(pid,kind,topic,except_mid)).fetchall()
        for (mid,) in ids:
            self._retire(pid,mid);self.db.execute("UPDATE memories SET state='superseded',content='',revision=revision+1 WHERE id=?",(mid,));self.db.execute('DELETE FROM search_index WHERE memory=?',(mid,));self.db.execute('DELETE FROM mutations WHERE memory=?',(mid,));self._privacy('supersede',pid,mid)
    def confirm(self,actor,pid,device,mid,revision,key,ttl_seconds=2592000):
        self._authorize(actor,pid,device);require(type(revision) is int and revision>0,'INVALID_REVISION');require(type(ttl_seconds) is int and 60<=ttl_seconds<=31536000)
        with self.tx():
            self._expire();h,old=self._mutation(actor,pid,key,{'op':'confirm','mid':mid,'revision':revision,'ttl':ttl_seconds})
            if old:return old
            r=self._row(mid,actor,pid);require(r['revision']==revision,'REVISION_CONFLICT',409);require(r['state']=='candidate','CANDIDATE_REQUIRED',409);content_policy(r['content'])
            self._supersede(pid,r['kind'],r['topic'],mid)
            self.db.execute("UPDATE memories SET state='confirmed',confidence=1,revision=revision+1,updated=?,expires=? WHERE id=?",(self.clock(),self.clock()+ttl_seconds,mid))
            self.db.execute('INSERT INTO search_index VALUES(?,?)',(mid,normalized(r['content'])));self._invalidate(pid);r=self._row(mid,actor,pid);self._record(actor,pid,key,h,r);self.event('memory_confirmed');return r
    def correct(self,actor,pid,device,mid,content,revision,key):
        self._authorize(actor,pid,device);content=text(content);content_policy(content);require(type(revision) is int and revision>0,'INVALID_REVISION')
        with self.tx():
            self._expire();h,old=self._mutation(actor,pid,key,{'op':'correct','mid':mid,'content':content,'revision':revision})
            if old:return old
            r=self._row(mid,actor,pid);require(r['state']=='confirmed','CONFIRMED_REQUIRED',409);require(r['revision']==revision,'REVISION_CONFLICT',409)
            self._retire(pid,mid);self.db.execute('DELETE FROM mutations WHERE memory=?',(mid,))
            self.db.execute('UPDATE memories SET content=?,source=?,confidence=1,revision=revision+1,updated=? WHERE id=?',(content,uuid.uuid4().hex,self.clock(),mid))
            self.db.execute('UPDATE search_index SET terms=? WHERE memory=?',(normalized(content),mid));self._privacy('correct',pid,mid);self._invalidate(pid);r=self._row(mid,actor,pid);self._record(actor,pid,key,h,r);self.event('memory_corrected');return r
    def delete(self,actor,pid,mid,revision):
        self._authorize(actor,pid,None,active=False,consent=False);require(type(revision) is int and revision>0,'INVALID_REVISION')
        with self.tx():
            r=self._row(mid,actor,pid);require(r['revision']==revision,'REVISION_CONFLICT',409);self._retire(pid,mid);self._privacy('delete',pid,mid)
            self.db.execute('DELETE FROM memories WHERE id=?',(mid,));self.db.execute('DELETE FROM mutations WHERE memory=?',(mid,));self._invalidate(pid);self.event('memory_deleted')
    def delete_all(self,actor,pid):
        self._authorize(actor,pid,None,active=False,consent=False)
        with self.tx():self._purge(pid,'delete_all')
    def revoke(self,actor,pid):
        # Purge locally FIRST. Crash/failure during F2002 update leaves this scope blocked.
        self._authorize(actor,pid,None,active=False,consent=False)
        with self.tx():
            self._purge(pid);self.db.execute("INSERT OR REPLACE INTO scope_blocks VALUES(?,'CONSENT_REVOKED')",(pid,))
        p=self.policy.profiles.get(pid,actor);d=dict(p['data']['consent']);d['long_term_memory']=False
        self.policy.profiles.update(pid,actor,{'consent':d},p['revision'],'memory-revoke:'+uuid.uuid4().hex)
    def grant(self,actor,pid):
        # Explicit authenticated regrant; old memories are never restored.
        self._authorize(actor,pid,None,active=False,consent=False)
        p=self.policy.profiles.get(pid,actor);d=dict(p['data']['consent']);d['long_term_memory']=True
        self.policy.profiles.update(pid,actor,{'consent':d},p['revision'],'memory-grant:'+uuid.uuid4().hex)
        with self.tx():self.db.execute('DELETE FROM scope_blocks WHERE profile=?',(pid,));self._privacy('grant',pid);self.event('scope_regranted')
    def synchronize(self,actor,pid):return self._authorize(actor,pid,None,active=False)
    def search(self,actor,pid,device,query,limit=5):
        self._authorize(actor,pid,device);query=text(query,200);require(type(limit) is int and 1<=limit<=10)
        with self.tx():
            self._expire();rows=self.db.execute("SELECT m.id,i.terms FROM memories m JOIN search_index i ON i.memory=m.id WHERE m.profile=? AND m.state='confirmed' ORDER BY m.updated DESC,m.id",(pid,)).fetchall();ranked=[]
            for mid,terms in rows:
                score=relevance(query,terms)
                if score>=.25:ranked.append((score,self._row(mid,actor,pid)))
            ranked.sort(key=lambda x:(-x[0],-x[1]['updated_at'],x[1]['memory_id']));self.event('search_completed')
            return [{'memory_id':r['memory_id'],'revision':r['revision'],'content':r['content'],'source_ref':r['source_ref'],'score':score} for score,r in ranked[:limit]]
    def prepare(self,actor,pid,device,query):
        stamp=self._authorize(actor,pid,device);rows=self.search(actor,pid,device,query)
        ticket=uuid.uuid4().hex
        with self.tx():self.db.execute('INSERT INTO tickets VALUES(?,?,?,?,?,?)',(ticket,actor,pid,encode(stamp),encode([[r['memory_id'],r['revision']] for r in rows]),self.clock()+30))
        return {'ticket':ticket,'count':len(rows),'contains_memory_text':False}
    def release_context(self,actor,pid,device,ticket):
        stamp=self._authorize(actor,pid,device)
        with self.tx():
            self._expire();row=self.db.execute('SELECT * FROM tickets WHERE id=? AND owner=? AND profile=?',(ticket,actor,pid)).fetchone();require(row is not None,'STALE_CONTEXT',409)
            require(json.loads(row[3])==stamp,'STALE_CONTEXT',409);memories=[]
            for mid,revision in json.loads(row[4]):
                r=self._row(mid,actor,pid);require(r['state']=='confirmed' and r['revision']==revision,'STALE_CONTEXT',409)
                memories.append({'memory_id':mid,'revision':revision,'content':r['content'],'source_ref':r['source_ref'],'role':'reference_data'})
            self.db.execute('DELETE FROM tickets WHERE id=?',(ticket,));self.event('context_released')
            return {'contract_version':'f2003-context-v1','memories':memories,'executable_actions':[],'model_connected':False}
    def sync_status(self,actor,pid):
        stamp=self._authorize(actor,pid,None,active=False);require(stamp['cloud_transfer'],'CLOUD_CONSENT_REQUIRED',403)
        # A caller cannot accidentally export content through an unimplemented network adapter.
        return {'status':'not_connected','payload_exported':False,'cloud_adapter':None}
