-- Schema v2; fresh S02 development DB. No S01 production migration.
PRAGMA foreign_keys=ON;
CREATE TABLE applications (
          session_id TEXT PRIMARY KEY REFERENCES sessions(id), id TEXT UNIQUE NOT NULL,
          state TEXT NOT NULL, attempts INTEGER NOT NULL, context TEXT NOT NULL, error TEXT);

CREATE TABLE completions (
          session_id TEXT PRIMARY KEY REFERENCES sessions(id),
          mutation_id TEXT NOT NULL, response TEXT NOT NULL);

CREATE TABLE consent_events (
          profile_id TEXT NOT NULL REFERENCES profiles(id), purpose TEXT NOT NULL,
          granted INTEGER NOT NULL, policy_version TEXT NOT NULL, recorded_at REAL NOT NULL,
          PRIMARY KEY(profile_id,purpose));

CREATE TABLE module_acks (
          application_id TEXT NOT NULL REFERENCES applications(id), module TEXT NOT NULL,
          receipt TEXT NOT NULL, PRIMARY KEY(application_id,module));

CREATE TABLE profiles (
          id TEXT PRIMARY KEY, actor TEXT NOT NULL, device TEXT UNIQUE NOT NULL,
          data TEXT NOT NULL);

CREATE TABLE schema_metadata (version INTEGER PRIMARY KEY);

CREATE TABLE sessions (
          id TEXT PRIMARY KEY, actor TEXT NOT NULL, device TEXT NOT NULL,
          status TEXT NOT NULL, revision INTEGER NOT NULL, expires REAL NOT NULL,
          data TEXT NOT NULL, profile_id TEXT);
INSERT OR IGNORE INTO schema_metadata VALUES (2);
