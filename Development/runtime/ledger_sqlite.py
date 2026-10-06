"""Local durable usage accounting prototype. No payment/provider calls.
One database per quota account; quota is immutable after creation.
BEGIN IMMEDIATE serializes competing writers; refunded IDs remain tombstones.
"""
import sqlite3
from contextlib import contextmanager
from core import integer

class SQLiteUsageLedger:
    def __init__(self,path,quota):
        integer(quota)
        self.db=sqlite3.connect(path,timeout=5,isolation_level=None)
        try:
            with self._transaction():
                self.db.execute('CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY CHECK(id=1), quota INTEGER NOT NULL CHECK(quota>=0))')
                self.db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, units INTEGER NOT NULL CHECK(units>0), refunded INTEGER NOT NULL DEFAULT 0 CHECK(refunded IN (0,1)))')
                self.db.execute('INSERT OR IGNORE INTO account VALUES (1,?)',(quota,))
                if self.db.execute('SELECT quota FROM account WHERE id=1').fetchone()[0]!=quota:raise ValueError('quota mismatch')
        except Exception:
            self.db.close();raise
    @contextmanager
    def _transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.db.execute('COMMIT')
        except BaseException:
            self.db.execute('ROLLBACK');raise
    @staticmethod
    def _id(event_id):
        if not isinstance(event_id,str) or not event_id or len(event_id)>128:raise ValueError('id')
    @property
    def used(self):
        return self.db.execute('SELECT COALESCE(SUM(units),0) FROM events WHERE refunded=0').fetchone()[0]
    def charge(self,event_id,units):
        self._id(event_id);integer(units,1)
        with self._transaction():
            row=self.db.execute('SELECT units FROM events WHERE id=?',(event_id,)).fetchone()
            if row:
                if row[0]!=units:raise ValueError('id conflict')
            else:
                quota=self.db.execute('SELECT quota FROM account WHERE id=1').fetchone()[0]
                if self.used+units>quota:raise ValueError('quota')
                self.db.execute('INSERT INTO events(id,units) VALUES (?,?)',(event_id,units))
            return self.used
    def refund(self,event_id):
        self._id(event_id)
        with self._transaction():
            if not self.db.execute('SELECT 1 FROM events WHERE id=?',(event_id,)).fetchone():raise ValueError('unknown event')
            self.db.execute('UPDATE events SET refunded=1 WHERE id=?',(event_id,))
            return self.used
    def close(self):self.db.close()
