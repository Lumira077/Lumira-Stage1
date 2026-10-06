#!/bin/sh
# Restores only into brand-new uniquely named disposable databases.
set -eu
umask 077
cd "$(dirname "$0")/.."
[ "$#" = 1 ] || { echo 'Usage: sh scripts/restore-smoke.sh backups/<completed-directory>' >&2; exit 1; }
backup=$1
[ -f "$backup/COMPLETE" ] || { echo 'Incomplete backup set.' >&2; exit 1; }
(cd "$backup" && sha256sum -c SHA256SUMS)
suffix="$(date -u +%Y%m%d%H%M%S)_$$"
for pair in 'service app' 'engineering engineering' 'partner partner'; do
 set -- $pair
 scope=$1; schema=$2
 target="lumira_restore_${scope}_$suffix"
 docker exec lumira-postgres-dev createdb -U lumira_admin "$target"
 docker exec -i lumira-postgres-dev pg_restore -U lumira_admin -d "$target" --no-owner --no-acl --exit-on-error < "$backup/lumira_${scope}_dev.dump"
 actual=$(docker exec lumira-postgres-dev psql -X -v ON_ERROR_STOP=1 -U lumira_admin -d "$target" -Atc "SELECT version FROM $schema.schema_migrations")
 [ "$actual" = 001-bootstrap ] || { echo "Restore verification failed; retained $target" >&2; exit 1; }
 docker exec lumira-postgres-dev dropdb -U lumira_admin "$target"
done
echo 'PASS: 3 custom dumps restored into fresh disposable DBs; bootstrap versions match.'
echo 'Same-host smoke test only, not independent/off-site recovery proof.'
