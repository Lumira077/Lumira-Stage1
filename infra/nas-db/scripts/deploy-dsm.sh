#!/bin/sh
# Run by the NAS administrator after reviewing this file.
# Creates only the new synthetic-test DB stack; no published ports or host network.
set -eu
umask 077
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH
cd "$(dirname "$0")/.."
base=$(pwd -P)
[ "${CREATE_LOCAL_ADMIN_SECRET:-}" = yes ] || { echo 'Administrator must explicitly authorize local credential creation.' >&2; exit 1; }
[ "${SYNTHETIC_ONLY:-}" = yes ] || { echo 'Synthetic-data-only acknowledgement required.' >&2; exit 1; }
[ -f sql/001-databases.sql ] || exit 1
command -v openssl >/dev/null
docker image inspect postgres:17-bookworm >/dev/null
if docker inspect lumira-postgres-dev >/dev/null 2>&1; then
 echo 'Container exists; stop and inspect. No changes made.' >&2; exit 1
fi
if docker network inspect lumira-db-private >/dev/null 2>&1; then
 echo 'Network exists; stop and inspect. No changes made.' >&2; exit 1
fi
if [ -d data ] && [ -n "$(ls -A data)" ]; then
 echo 'Data directory is not empty; stop. Never erase it to retry.' >&2; exit 1
fi
[ ! -e secrets/db_admin_password ] || { echo 'Secret exists; stop without replacing it.' >&2; exit 1; }
mkdir -p secrets data backups
chmod 700 secrets
(set -C; openssl rand -hex 32 > secrets/db_admin_password)
chmod 600 secrets/db_admin_password
docker network create --driver bridge --internal lumira-db-private
image=$(docker image inspect --format '{{index .RepoDigests 0}}' postgres:17-bookworm)
[ -n "$image" ] && [ "$image" != '<no value>' ]
printf '%s\n' "$image" > image-digest.txt
docker run -d --name lumira-postgres-dev --restart=no \
 --cpus=1 --memory=1024m --shm-size=128m \
 --network=lumira-db-private \
 --log-driver=json-file --log-opt=max-size=10m --log-opt=max-file=3 \
 --mount "type=bind,src=$base/data,dst=/var/lib/postgresql/data" \
 --mount "type=bind,src=$base/sql,dst=/docker-entrypoint-initdb.d,readonly" \
 --mount "type=bind,src=$base/secrets/db_admin_password,dst=/run/secrets/db_admin_password,readonly" \
 -e POSTGRES_USER=lumira_admin -e POSTGRES_DB=postgres \
 -e POSTGRES_PASSWORD_FILE=/run/secrets/db_admin_password \
 -e 'POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256 --auth-local=trust' -e TZ=UTC \
 --health-cmd='pg_isready -U lumira_admin -d postgres' \
 --health-interval=10s --health-timeout=5s --health-retries=6 \
 "$image" postgres -c max_connections=20 -c shared_buffers=128MB \
 -c password_encryption=scram-sha-256 -c timezone=UTC \
 -c log_statement=none -c log_min_duration_statement=-1
n=0
until [ "$(docker inspect --format '{{.State.Health.Status}}' lumira-postgres-dev)" = healthy ]; do
 n=$((n+1))
 [ "$n" -le 60 ] || { echo 'Health timeout. Keep data and inspect logs; do not rerun initialization.' >&2; exit 1; }
 sleep 2
done
sh scripts/verify.sh
backup=$(sh scripts/backup.sh)
sh scripts/restore-smoke.sh "$backup"
echo 'DEPLOYMENT_AND_SAME_HOST_RESTORE_OK'
echo 'External backup, API account/TLS and NAS restart/persistence verification remain separate.'
