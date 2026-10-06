"""Development-only snapshot restoration with external deletion/revocation ledger."""
import json,sqlite3
from pathlib import Path
from profile_contract import require,CONSENTS
class RestoreLab:
    def __init__(self,root):
        self.root=Path(root);require(not self.root.is_symlink() and (self.root/'.ker-development-sandbox').is_file(),'SANDBOX_REQUIRED')
    def path(self,name):
        require(name in ('current.sqlite3','snapshot.sqlite3','restored.sqlite3','privacy-ledger.json'))
        p=self.root/name;require(not p.is_symlink(),'SYMLINK_FORBIDDEN');return p
    def schema(self,db):
        try:require(db.execute('SELECT version FROM schema_metadata').fetchall()==[(1,)],'INCOMPATIBLE_SCHEMA',409)
        except sqlite3.DatabaseError:raise ValueError('Missing profile schema')
    def backup(self):
        a=sqlite3.connect(self.path('current.sqlite3'));b=sqlite3.connect(self.path('snapshot.sqlite3'))
        try:self.schema(a);a.backup(b)
        finally:a.close();b.close()
    def restore(self):
        path=self.path('privacy-ledger.json');require(path.is_file(),'LATEST_PRIVACY_LEDGER_REQUIRED')
        records=json.loads(path.read_text());require(isinstance(records,list))
        for i,r in enumerate(records,1):
            require(isinstance(r,dict) and set(r)=={'seq','profile_id','operation','purpose'} and type(r['seq']) is int and r['seq']==i)
            require(isinstance(r['profile_id'],str) and len(r['profile_id'])==32 and all(c in '0123456789abcdef' for c in r['profile_id']))
            require(r['operation'] in ('delete','revoke'));require(r['purpose'] is None if r['operation']=='delete' else r['purpose'] in CONSENTS)
        source=sqlite3.connect(self.path('snapshot.sqlite3'));temp=sqlite3.connect(':memory:');destination=None
        try:
            self.schema(source);source.backup(temp)
            with temp:
                # Do not revive old acknowledgements or activate restored settings automatically.
                temp.execute('DELETE FROM acks');temp.execute("UPDATE applications SET state='invalidated',error='RESTORE_REAPPLY_REQUIRED'");temp.execute('UPDATE devices SET generation=generation+1,active=NULL')
                for r in records:
                    pid=r['profile_id'];row=temp.execute('SELECT data FROM profiles WHERE id=?',(pid,)).fetchone()
                    if r['operation']=='delete':
                        temp.execute('DELETE FROM profiles WHERE id=?',(pid,));temp.execute('DELETE FROM applications WHERE profile=?',(pid,));temp.execute('DELETE FROM mutations WHERE profile=?',(pid,));temp.execute('UPDATE imports SET profile=NULL WHERE profile=?',(pid,))
                    elif row:
                        d=json.loads(row[0]);d['consent'][r['purpose']]=False;temp.execute('UPDATE profiles SET data=?,revision=revision+1 WHERE id=?',(json.dumps(d),pid));temp.execute('DELETE FROM mutations WHERE profile=?',(pid,))
            destination=sqlite3.connect(self.path('restored.sqlite3'));temp.backup(destination)
            return {'status':'passed','scope':'development_sandbox','ledger_records':len(records),'old_acks_reused':False,'production_restore_verified':False}
        finally:
            source.close();temp.close()
            if destination:destination.close()
