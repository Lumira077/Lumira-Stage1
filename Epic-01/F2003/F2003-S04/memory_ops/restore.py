"""Development restore: latest external ledger anchored to snapshot ledger prefix."""
import json,sqlite3,time,hashlib
from pathlib import Path
from memory_contract import require,opaque
OPS={'retire_key','correct','delete','expire','supersede','delete_all','revoke','profile_deleted','grant'}
class RestoreLab:
    def __init__(self,root,clock=time.time):
        self.root=Path(root);self.clock=clock;require(not self.root.is_symlink() and (self.root/'.ker-development-sandbox').is_file(),'SANDBOX_REQUIRED')
    def path(self,name):
        require(name in ('current.sqlite3','snapshot.sqlite3','restored.sqlite3','privacy-ledger.json'));p=self.root/name;require(not p.is_symlink(),'SYMLINK_FORBIDDEN');return p
    def schema(self,db):
        require(db.execute('SELECT version FROM schema_metadata').fetchall()==[(1,)],'INCOMPATIBLE_SCHEMA',409)
    def backup(self):
        a=sqlite3.connect(self.path('current.sqlite3'));b=sqlite3.connect(self.path('snapshot.sqlite3'))
        try:self.schema(a);a.backup(b)
        finally:a.close();b.close()
    def export_latest_ledger(self):
        db=sqlite3.connect(self.path('current.sqlite3'))
        try:records=[dict(zip(('seq','operation','profile_id','memory_id','stamp'),row)) for row in db.execute('SELECT * FROM privacy_ledger ORDER BY seq')]
        finally:db.close()
        self.path('privacy-ledger.json').write_text(json.dumps(records,allow_nan=False))
    @staticmethod
    def retire(db,pid=None,mid=None):
        rows=db.execute('SELECT owner,profile,key FROM mutations WHERE '+('memory=?' if mid is not None else 'profile=?'),(mid if mid is not None else pid,)).fetchall()
        for actor,profile,key in rows:
            token=hashlib.sha256((actor+'\0'+profile+'\0'+key).encode()).hexdigest()[:32];db.execute('INSERT OR IGNORE INTO retired_keys VALUES(?,?)',(profile,token))
    def restore(self):
        p=self.path('privacy-ledger.json');require(p.is_file(),'LATEST_PRIVACY_LEDGER_REQUIRED');records=json.loads(p.read_text())
        require(isinstance(records,list))
        import math
        for i,r in enumerate(records,1):
            require(isinstance(r,dict) and set(r)=={'seq','operation','profile_id','memory_id','stamp'} and type(r['seq']) is int and r['seq']==i,'INVALID_LEDGER_SEQUENCE')
            require(r['operation'] in OPS and opaque(r['profile_id']))
            require(opaque(r['memory_id']) if r['operation'] in ('retire_key','correct','delete','expire','supersede') else r['memory_id'] is None)
            require(type(r['stamp']) in (int,float) and math.isfinite(r['stamp']) and r['stamp']>=0)
        source=sqlite3.connect(self.path('snapshot.sqlite3'));temp=sqlite3.connect(':memory:');temp.execute('PRAGMA foreign_keys=ON');destination=None
        try:
            self.schema(source);source.backup(temp);prefix=[dict(zip(('seq','operation','profile_id','memory_id','stamp'),row)) for row in temp.execute('SELECT * FROM privacy_ledger ORDER BY seq')]
            require(records[:len(prefix)]==prefix,'LEDGER_ANCHOR_MISMATCH')
            with temp:
                for r in records[len(prefix):]:
                    pid,mid,op=r['profile_id'],r['memory_id'],r['operation']
                    if op=='retire_key':temp.execute('INSERT OR IGNORE INTO retired_keys VALUES(?,?)',(pid,mid))
                    elif op in ('correct','delete','expire','supersede'):
                        self.retire(temp,mid=mid);temp.execute('DELETE FROM memories WHERE id=? AND profile=?',(mid,pid));temp.execute('DELETE FROM mutations WHERE memory=?',(mid,))
                    elif op in ('delete_all','revoke','profile_deleted'):
                        self.retire(temp,pid=pid);temp.execute('DELETE FROM memories WHERE profile=?',(pid,));temp.execute('DELETE FROM mutations WHERE profile=?',(pid,))
                        if op in ('revoke','profile_deleted'):temp.execute("INSERT OR REPLACE INTO scope_blocks VALUES(?,'RESTORED_PRIVACY_BLOCK')",(pid,))
                    elif op=='grant':temp.execute('DELETE FROM scope_blocks WHERE profile=?',(pid,))
                    temp.execute('INSERT INTO privacy_ledger VALUES(?,?,?,?,?)',(r['seq'],op,pid,mid,r['stamp']))
                temp.execute('DELETE FROM tickets')
                expired=[row[0] for row in temp.execute('SELECT id FROM memories WHERE expires<=?',(self.clock(),))]
                for mid in expired:self.retire(temp,mid=mid);temp.execute('DELETE FROM memories WHERE id=?',(mid,));temp.execute('DELETE FROM mutations WHERE memory=?',(mid,))
            destination=sqlite3.connect(self.path('restored.sqlite3'));temp.backup(destination)
            return {'status':'passed','scope':'development_sandbox','newer_ledger_records':len(records)-len(prefix),'expired_memories_removed':len(expired),'prepared_contexts_reused':False,'production_restore_verified':False}
        finally:
            source.close();temp.close()
            if destination:destination.close()
