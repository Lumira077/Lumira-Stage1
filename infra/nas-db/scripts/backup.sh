#!/bin/sh
set -eu
umask 077
cd "$(dirname "$0")/.."
mkdir -p backups
out=$(mktemp -d "backups/$(date -u +%Y%m%dT%H%M%SZ)-XXXXXX")
for db in lumira_service_dev lumira_engineering_dev lumira_partner_dev; do
 docker exec lumira-postgres-dev pg_dump -U lumira_admin -d "$db" -Fc --no-owner --no-acl > "$out/$db.dump.partial"
 mv "$out/$db.dump.partial" "$out/$db.dump"
 docker exec -i lumira-postgres-dev pg_restore --list < "$out/$db.dump" > "$out/$db.contents.txt"
done
(cd "$out" && sha256sum *.dump > SHA256SUMS)
docker exec lumira-postgres-dev psql -X -U lumira_admin -d postgres -Atc 'SELECT version()' > "$out/server-version.txt"
printf '%s\n' 'Logical dumps only. Runtime roles/ACL, secrets, files and WAL/PITR are excluded.' > "$out/SCOPE.txt"
touch "$out/COMPLETE"
printf '%s\n' "$out"
