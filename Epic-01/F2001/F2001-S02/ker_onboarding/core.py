"""Onboarding contracts, validation, state transitions and atomic registration."""
import json
import sqlite3
import time
import uuid
from contextlib import contextmanager

STEPS = ('registration', 'language', 'profile', 'purpose', 'preferences', 'consent', 'review')
PURPOSES = ('companion', 'education', 'care', 'home')
CONSENTS = ('long_term_memory', 'conversation_storage', 'biometric_identity', 'cloud_transfer')
DEFAULTS = {'voice_id': 'device_default', 'speech_rate': 1.0, 'volume': 20,
            'expression_level': 1, 'gesture_level': 1}

class Error(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code
        super().__init__(code)

def require(condition, code='INVALID_INPUT', status=422):
    if not condition:
        raise Error(status, code)

def validate(step, data):
    require(isinstance(data, dict))
    if step == 'registration':
        require(set(data) == {'registration_type', 'subject_id'})
        require(data['registration_type'] in ('self', 'guardian', 'guest'))
        require(isinstance(data['subject_id'], str) and 1 <= len(data['subject_id']) <= 80)
    elif step == 'language':
        require(set(data) == {'language'})
        require(data['language'] in ('ko-KR', 'en-US'), 'UNSUPPORTED_LANGUAGE')
    elif step == 'profile':
        require(set(data) == {'nickname', 'preferred_name'})
        for value in data.values():
            require(isinstance(value, str) and 1 <= len(value.strip()) <= 40)
            require(not any(ord(c) < 32 for c in value))
        data = {k: v.strip() for k, v in data.items()}
    elif step == 'purpose':
        require(set(data) == {'purpose'} and data['purpose'] in PURPOSES)
    elif step == 'preferences':
        require(set(data) == set(DEFAULTS))
        require(data['voice_id'] in ('device_default', 'demo_voice_a'), 'UNSUPPORTED_VOICE')
        for key, low, high in [('volume', 0, 100), ('expression_level', 0, 3), ('gesture_level', 0, 3)]:
            require(type(data[key]) is int and low <= data[key] <= high)
        require(type(data['speech_rate']) in (int, float) and 0.7 <= data['speech_rate'] <= 1.3)
    elif step == 'consent':
        require(set(data) == set(CONSENTS) | {'policy_version'})
        require(data['policy_version'] == 'prototype-2026-10-v1', 'POLICY_VERSION_MISMATCH')
        require(all(type(data[key]) is bool for key in CONSENTS))
    elif step == 'review':
        require(set(data) == {'confirmed'} and data['confirmed'] is True)
    else:
        raise Error(404, 'UNKNOWN_STEP')
    return data

class Service:
    def __init__(self, db_path, clock=time.time):
        self.clock = clock
        self.db = sqlite3.connect(db_path, isolation_level=None)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA busy_timeout=5000')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS sessions (
          id TEXT PRIMARY KEY, actor TEXT NOT NULL, device TEXT NOT NULL,
          status TEXT NOT NULL, revision INTEGER NOT NULL, expires REAL NOT NULL,
          data TEXT NOT NULL, profile_id TEXT);
        CREATE TABLE IF NOT EXISTS profiles (
          id TEXT PRIMARY KEY, actor TEXT NOT NULL, device TEXT UNIQUE NOT NULL,
          data TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS completions (
          session_id TEXT PRIMARY KEY REFERENCES sessions(id),
          mutation_id TEXT NOT NULL, response TEXT NOT NULL);
        ''')

    @contextmanager
    def transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.db.execute('COMMIT')
        except Exception:
            self.db.execute('ROLLBACK')
            raise

    def close(self):
        self.db.close()

    def _get(self, sid, actor):
        row = self.db.execute('SELECT * FROM sessions WHERE id=?', (sid,)).fetchone()
        # Same response for unknown and other-actor IDs.
        require(row is not None and row[1] == actor, 'NOT_FOUND', 404)
        return {'session_id': row[0], 'actor_id': row[1], 'device_id': row[2],
                'status': row[3], 'revision': row[4], 'expires_at': row[5],
                'draft': json.loads(row[6]), 'profile_id': row[7]}

    def _active(self, session):
        require(session['status'] == 'in_progress', 'SESSION_NOT_ACTIVE', 409)
        require(self.clock() < session['expires_at'], 'SESSION_EXPIRED', 410)

    def create(self, actor, device, allowed_devices):
        require(isinstance(device, str) and 1 <= len(device) <= 80)
        require(device in allowed_devices, 'DEVICE_NOT_AUTHORIZED', 403)
        with self.transaction():
            require(not self.db.execute('SELECT 1 FROM profiles WHERE device=?', (device,)).fetchone(),
                    'DEVICE_ALREADY_REGISTERED', 409)
            # One live draft per actor/device; repeated start resumes it.
            existing = self.db.execute('SELECT id FROM sessions WHERE actor=? AND device=? '
                                       'AND status=? AND expires>?',
                                       (actor, device, 'in_progress', self.clock())).fetchone()
            if existing:
                return self._get(existing[0], actor)
            sid = str(uuid.uuid4())
            self.db.execute('INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?)',
                            (sid, actor, device, 'in_progress', 1, self.clock()+86400, '{}', None))
            return self._get(sid, actor)

    def get(self, sid, actor):
        session = self._get(sid, actor)
        if session['status'] == 'in_progress' and self.clock() >= session['expires_at']:
            # Reading cannot revive an expired draft.
            raise Error(410, 'SESSION_EXPIRED')
        return session

    def save_step(self, sid, actor, step, data, revision):
        require(type(revision) is int, 'INVALID_REVISION')
        value = validate(step, data)
        with self.transaction():
            session = self._get(sid, actor)
            self._active(session)
            require(session['revision'] == revision, 'REVISION_CONFLICT', 409)
            index = STEPS.index(step)
            draft = session['draft']
            require(all(s in draft for s in STEPS[:index]), 'PREVIOUS_STEP_REQUIRED', 409)
            # Editing a prior step invalidates all later decisions, including review.
            draft = {k: v for k, v in draft.items() if k in STEPS[:index]}
            draft[step] = value
            self.db.execute('UPDATE sessions SET data=?, revision=revision+1 WHERE id=?',
                            (json.dumps(draft, ensure_ascii=False), sid))
            return self._get(sid, actor)

    def complete(self, sid, actor, mutation_id, revision):
        require(isinstance(mutation_id, str) and 1 <= len(mutation_id) <= 80)
        require(type(revision) is int, 'INVALID_REVISION')
        with self.transaction():
            session = self._get(sid, actor)
            previous = self.db.execute('SELECT mutation_id,response FROM completions WHERE session_id=?',
                                       (sid,)).fetchone()
            if previous:
                require(previous[0] == mutation_id, 'ALREADY_COMPLETED', 409)
                return json.loads(previous[1])
            self._active(session)
            require(session['revision'] == revision, 'REVISION_CONFLICT', 409)
            require(all(s in session['draft'] for s in STEPS), 'INCOMPLETE_SETUP', 409)
            require(not self.db.execute('SELECT 1 FROM profiles WHERE device=?',
                                        (session['device_id'],)).fetchone(), 'DEVICE_ALREADY_REGISTERED', 409)
            pid = str(uuid.uuid4())
            self.db.execute('INSERT INTO profiles VALUES (?,?,?,?)',
                            (pid, actor, session['device_id'], json.dumps(session['draft'], ensure_ascii=False)))
            self.db.execute('UPDATE sessions SET status=?,profile_id=?,revision=revision+1 WHERE id=?',
                            ('committed', pid, sid))
            # No fabricated hardware ACK: S02/S03 must implement application adapters.
            result = {'session_id': sid, 'profile_id': pid, 'registration_status': 'committed',
                      'apply_status': 'pending', 'hardware_connected': False,
                      'revision': revision+1}
            self.db.execute('INSERT INTO completions VALUES (?,?,?)',
                            (sid, mutation_id, json.dumps(result)))
            return result

    def cancel(self, sid, actor):
        with self.transaction():
            session = self._get(sid, actor)
            require(session['status'] in ('in_progress', 'cancelled'), 'ALREADY_COMPLETED', 409)
            if session['status'] != 'cancelled':
                self.db.execute('UPDATE sessions SET status=?,data=?,revision=revision+1 WHERE id=?',
                                ('cancelled', '{}', sid))
            return self._get(sid, actor)

    def purge_expired(self):
        # No committed profiles or consent history removed by draft cleanup.
        cur = self.db.execute('UPDATE sessions SET status=?,data=? WHERE status=? AND expires<=?',
                              ('expired', '{}', 'in_progress', self.clock()))
        return cur.rowcount
