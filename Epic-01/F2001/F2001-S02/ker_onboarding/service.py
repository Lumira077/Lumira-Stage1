"""Prototype registration, durable application retry and personalization service."""
import json
import uuid
from .core import Service as Core, Error, require, validate, STEPS, CONSENTS
from .adapters import SimulatedDevice, ProfileAdapter, SimulatedOutputs

POLICY_VERSION = 'prototype-2026-10-v1'
class Service(Core):
    def __init__(self, db_path, clock=None, devices=None, outputs=None):
        super().__init__(db_path, **({'clock':clock} if clock else {}))
        self.devices = devices or SimulatedDevice()
        self.outputs = outputs or SimulatedOutputs()
        self.profile_adapter = ProfileAdapter()
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS schema_metadata (version INTEGER PRIMARY KEY);
        INSERT OR IGNORE INTO schema_metadata VALUES (2);
        CREATE TABLE IF NOT EXISTS applications (
          session_id TEXT PRIMARY KEY REFERENCES sessions(id), id TEXT UNIQUE NOT NULL,
          state TEXT NOT NULL, attempts INTEGER NOT NULL, context TEXT NOT NULL, error TEXT);
        CREATE TABLE IF NOT EXISTS module_acks (
          application_id TEXT NOT NULL REFERENCES applications(id), module TEXT NOT NULL,
          receipt TEXT NOT NULL, PRIMARY KEY(application_id,module));
        CREATE TABLE IF NOT EXISTS consent_events (
          profile_id TEXT NOT NULL REFERENCES profiles(id), purpose TEXT NOT NULL,
          granted INTEGER NOT NULL, policy_version TEXT NOT NULL, recorded_at REAL NOT NULL,
          PRIMARY KEY(profile_id,purpose));
        """)
    def create(self, actor, device, allowed_devices):
        require(isinstance(device,str) and 1 <= len(device) <= 80)
        require(device in allowed_devices, 'DEVICE_NOT_AUTHORIZED', 403)
        self.devices.ready(actor, device)
        return super().create(actor, device, allowed_devices)
    def get(self, sid, actor):
        session=super().get(sid,actor)
        if session['draft'].get('registration',{}).get('registration_type') == 'guest':
            require(self.clock() < session['expires_at'], 'SESSION_EXPIRED', 410)
        session['completed_steps']=[k for k in STEPS if k in session['draft']]
        session['current_step']=next((k for k in STEPS if k not in session['draft']), 'review')
        return session
    def save_step(self, sid, actor, step, data, revision):
        session = self._get(sid, actor)
        self.devices.ready(actor, session['device_id'])
        if step == 'registration':
            validate(step, data)
            kind, subject = data['registration_type'], data['subject_id']
            if kind == 'self':
                require(subject == actor, 'SUBJECT_NOT_AUTHORIZED', 403)
            elif kind == 'guardian':
                # An explicit fixture, not a production guardian permission check.
                require(actor == 'local-demo-guardian' and subject == 'demo-child-01',
                        'GUARDIAN_NOT_AUTHORIZED', 403)
            else:
                require(subject == 'guest', 'INVALID_GUEST_SUBJECT')
        if step == 'consent' and session['draft'].get('registration', {}).get('registration_type') == 'guest':
            validate(step, data)
            require(not any(data[k] for k in CONSENTS), 'GUEST_CONSENT_FORBIDDEN')
        return super().save_step(sid, actor, step, data, revision)
    def complete(self, sid, actor, mutation_id, revision):
        require(isinstance(mutation_id, str) and 1 <= len(mutation_id) <= 80)
        require(type(revision) is int, 'INVALID_REVISION')
        with self.transaction():
            session = self._get(sid, actor)
            old = self.db.execute('SELECT mutation_id,response FROM completions WHERE session_id=?',(sid,)).fetchone()
            if old:
                self.get(sid,actor)
                require(old[0] == mutation_id, 'ALREADY_COMPLETED', 409)
                return json.loads(old[1])
            self._active(session)
            self.devices.ready(actor, session['device_id'])
            require(session['revision'] == revision, 'REVISION_CONFLICT', 409)
            require(all(k in session['draft'] for k in STEPS), 'INCOMPLETE_SETUP', 409)
            draft = session['draft']
            guest = draft['registration']['registration_type'] == 'guest'
            require(not self.db.execute('SELECT 1 FROM profiles WHERE device=?',(session['device_id'],)).fetchone(),
                    'DEVICE_ALREADY_REGISTERED', 409)
            pid = None if guest else str(uuid.uuid4())
            if not guest:
                self.db.execute('INSERT INTO profiles VALUES (?,?,?,?)',
                                (pid,actor,session['device_id'],json.dumps(draft,ensure_ascii=False)))
                for purpose in CONSENTS:
                    self.db.execute('INSERT INTO consent_events VALUES (?,?,?,?,?)',
                                    (pid,purpose,int(draft['consent'][purpose]),POLICY_VERSION,self.clock()))
            context = self.profile_adapter.context(pid, actor, draft)
            application_id = str(uuid.uuid4())
            self.db.execute('INSERT INTO applications VALUES (?,?,?,?,?,?)',
                            (sid,application_id,'pending',0,json.dumps(context,ensure_ascii=False),None))
            self.db.execute('UPDATE sessions SET status=?,profile_id=?,revision=revision+1 WHERE id=?',
                            ('committed',pid,sid))
            result = {'session_id':sid,'profile_id':pid,'registration_status':'guest_ready' if guest else 'committed',
                      'application_id':application_id,'apply_status':'pending','adapter_mode':'simulated',
                      'hardware_connected':False,'revision':revision+1}
            self.db.execute('INSERT INTO completions VALUES (?,?,?)',(sid,mutation_id,json.dumps(result)))
            return result
    def _application(self, sid, actor):
        session = self._get(sid, actor)
        if session['draft'].get('registration',{}).get('registration_type') == 'guest':
            require(self.clock() < session['expires_at'], 'SESSION_EXPIRED', 410)
        row = self.db.execute('SELECT * FROM applications WHERE session_id=?',(sid,)).fetchone()
        require(row is not None, 'APPLICATION_NOT_FOUND', 404)
        return session, row
    def application(self, sid, actor):
        session, row = self._application(sid, actor)
        return {'session_id':sid,'application_id':row[1],'apply_status':row[2],'attempts':row[3],
                'error_code':row[5],'adapter_mode':'simulated','hardware_connected':False,
                'acks':[json.loads(r[0]) for r in self.db.execute(
                    'SELECT receipt FROM module_acks WHERE application_id=? ORDER BY module',(row[1],))]}
    def apply(self, sid, actor):
        with self.transaction():
            session, row = self._application(sid, actor)
            # Existing receipt can be inspected offline; a new output attempt requires connection.
            if row[2] == 'applied':
                return self.application(sid, actor)
            self.devices.ready(actor, session['device_id'])
            self.db.execute('UPDATE applications SET attempts=attempts+1,state=?,error=NULL WHERE session_id=?',
                            ('pending',sid))
            context = json.loads(row[4])
            for module in self.outputs.modules:
                if self.db.execute('SELECT 1 FROM module_acks WHERE application_id=? AND module=?',
                                   (row[1],module)).fetchone():
                    continue
                try:
                    receipt = self.outputs.apply(row[1],module,context)
                    require(receipt.get('ack') is True and receipt.get('application_id') == row[1] and
                            receipt.get('module') == module, 'INVALID_MODULE_ACK', 409)
                except Exception:
                    self.db.execute('UPDATE applications SET state=?,error=? WHERE session_id=?',
                                    ('failed','MODULE_APPLY_FAILED:'+module,sid))
                    return self.application(sid,actor)
                self.db.execute('INSERT INTO module_acks VALUES (?,?,?)',(row[1],module,json.dumps(receipt)))
            self.db.execute('UPDATE applications SET state=?,error=NULL WHERE session_id=?',('applied',sid))
            return self.application(sid,actor)
    def context(self, profile_id, actor):
        row = self.db.execute('SELECT actor,data FROM profiles WHERE id=?',(profile_id,)).fetchone()
        require(row is not None and row[0] == actor, 'NOT_FOUND', 404)
        return self.profile_adapter.context(profile_id,actor,json.loads(row[1]))
    def greeting(self, sid, actor):
        session, row = self._application(sid,actor)
        require(row[2] == 'applied', 'SETTINGS_NOT_APPLIED', 409)
        self.devices.ready(actor,session['device_id'])
        return self.outputs.greeting(json.loads(row[4]))
    def guide(self, sid, actor, step):
        session = self.get(sid,actor)
        require(step in STEPS, 'UNKNOWN_STEP', 404)
        ko = session['draft'].get('language',{}).get('language','ko-KR') == 'ko-KR'
        labels = {'registration':('등록 유형을 선택해 주세요.','Choose a registration type.'),
                  'language':('사용할 언어를 선택해 주세요.','Choose your language.'),
                  'profile':('닉네임과 호칭을 입력해 주세요.','Enter a nickname and preferred name.'),
                  'purpose':('사용 목적을 선택해 주세요.','Choose a purpose.'),
                  'preferences':('음성과 표현 설정을 확인해 주세요.','Review voice and expression preferences.'),
                  'consent':('각 목적의 동의를 선택해 주세요. 모두 거부해도 기본 인사가 가능합니다.','Choose consent for each purpose. Basic greetings work without consent.'),
                  'review':('설정을 확인한 후 등록해 주세요.','Confirm the settings before registering.')}
        return {'text':labels[step][0 if ko else 1],'adapter_mode':'simulated','robot_audio_played':False}
    def preview(self, sid, actor, preferences):
        session = self.get(sid,actor)
        self.devices.ready(actor,session['device_id'])
        validate('preferences',preferences)
        return {'text':'안녕하세요. 저는 루미라입니다. Hello, I am Lumira.',
                'preferences':preferences,'expression_preview_id':'sim-smile',
                'motion_preview_id':'sim-no-motion','adapter_mode':'simulated',
                'physical_action_performed':False,'robot_audio_played':False}
    def purge_expired(self):
        # Guest data is temporary: remove context/receipts/response, never create a profile.
        with self.transaction():
            rows=self.db.execute("SELECT id,data FROM sessions WHERE expires<=? AND status='committed'",(self.clock(),)).fetchall()
            for sid, data in rows:
                if json.loads(data).get('registration',{}).get('registration_type') != 'guest':continue
                row=self.db.execute('SELECT id FROM applications WHERE session_id=?',(sid,)).fetchone()
                if row:self.db.execute('DELETE FROM module_acks WHERE application_id=?',(row[0],))
                self.db.execute('DELETE FROM applications WHERE session_id=?',(sid,))
                self.db.execute('DELETE FROM completions WHERE session_id=?',(sid,))
                self.db.execute("UPDATE sessions SET data='{}',status='expired' WHERE id=?",(sid,))
            return super().purge_expired()+len([1 for _,d in rows if json.loads(d).get('registration',{}).get('registration_type')=='guest'])
