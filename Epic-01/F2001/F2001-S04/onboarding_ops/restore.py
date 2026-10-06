"""Sandbox restore lab with an independent post-backup deletion/revocation ledger."""
import json,sqlite3
from pathlib import Path
from .telemetry import check
class RestoreLab:
    def __init__(self,root):
        self.root=Path(root)
        check(not self.root.is_symlink(),'Refuse symlink sandbox')
        check((self.root/'.ker-development-sandbox').is_file(),'Development sandbox marker required')
    def path(self,name):
        check(name in ('current.sqlite3','snapshot.sqlite3','restored.sqlite3','privacy-ledger.json'),'Unknown sandbox file')
        p=self.root/name;check(not p.is_symlink(),'Refuse symlink file');return p
    @staticmethod
    def schema(db):
        try:versions=db.execute('SELECT version FROM schema_metadata').fetchall()
        except sqlite3.DatabaseError:raise ValueError('Unsupported schema')
        check(versions==[(2,)],'Incompatible schema: block simple rollback')
    def backup(self):
        source=sqlite3.connect(self.path('current.sqlite3'));target=sqlite3.connect(self.path('snapshot.sqlite3'))
        try:self.schema(source);source.backup(target)
        finally:source.close();target.close()
    def restore(self):
        ledger_path=self.path('privacy-ledger.json');check(ledger_path.is_file(),'Latest privacy ledger required')
        ledger=json.loads(ledger_path.read_text());check(isinstance(ledger,list),'Invalid ledger')
        for n,record in enumerate(ledger,1):
            check(set(record)=={'seq','operation','profile_id','purpose'} and record['seq']==n and type(record['seq']) is int,'Invalid ledger sequence')
            check(record['operation'] in ('delete_profile','revoke_consent'),'Invalid operation')
            check(isinstance(record['profile_id'],str) and record['profile_id'],'Invalid profile')
            check(record['purpose'] in (None,'long_term_memory','conversation_storage','biometric_identity','cloud_transfer'),'Invalid purpose')
            check(record['operation']!='revoke_consent' or record['purpose'] is not None,'Missing consent purpose')
        source=sqlite3.connect(self.path('snapshot.sqlite3'));target=sqlite3.connect(':memory:');target.execute('PRAGMA foreign_keys=ON')
        destination=None
        try:
            self.schema(source);source.backup(target)
            with target:
                for record in ledger:
                    pid,purpose=record['profile_id'],record['purpose']
                    row=target.execute('SELECT data FROM profiles WHERE id=?',(pid,)).fetchone()
                    if row is None:continue
                    sids=[x[0] for x in target.execute('SELECT id FROM sessions WHERE profile_id=?',(pid,))]
                    if record['operation']=='delete_profile':
                        for sid in sids:
                            app=target.execute('SELECT id FROM applications WHERE session_id=?',(sid,)).fetchone()
                            if app:target.execute('DELETE FROM module_acks WHERE application_id=?',(app[0],))
                            target.execute('DELETE FROM applications WHERE session_id=?',(sid,));target.execute('DELETE FROM completions WHERE session_id=?',(sid,))
                            target.execute("UPDATE sessions SET status='cancelled',data='{}',profile_id=NULL WHERE id=?",(sid,))
                        target.execute('DELETE FROM consent_events WHERE profile_id=?',(pid,));target.execute('DELETE FROM profiles WHERE id=?',(pid,))
                    else:
                        data=json.loads(row[0]);data['consent'][purpose]=False;target.execute('UPDATE profiles SET data=? WHERE id=?',(json.dumps(data),pid))
                        target.execute('UPDATE consent_events SET granted=0 WHERE profile_id=? AND purpose=?',(pid,purpose))
                        for sid in sids:
                            draft=json.loads(target.execute('SELECT data FROM sessions WHERE id=?',(sid,)).fetchone()[0]);draft['consent'][purpose]=False
                            target.execute('UPDATE sessions SET data=? WHERE id=?',(json.dumps(draft),sid))
                            app=target.execute('SELECT id,context FROM applications WHERE session_id=?',(sid,)).fetchone()
                            if app:
                                context=json.loads(app[1]);context['permissions'][purpose]=False
                                target.execute("UPDATE applications SET context=?,state='pending',error=NULL WHERE id=?",(json.dumps(context),app[0]))
                                target.execute('DELETE FROM module_acks WHERE application_id=?',(app[0],))
            # Only a sandbox DB is replaced. Real deployments need service quiescence and an approved restore procedure.
            destination=sqlite3.connect(self.path('restored.sqlite3'));target.backup(destination)
            return {'status':'passed','scope':'development_sandbox','ledger_records':len(ledger),'production_restore_verified':False}
        finally:
            source.close();target.close()
            if destination:destination.close()
