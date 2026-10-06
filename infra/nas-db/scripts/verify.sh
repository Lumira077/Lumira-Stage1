#!/bin/sh
set -eu
sql() { docker exec lumira-postgres-dev psql -X -v ON_ERROR_STOP=1 -U lumira_admin -d postgres -Atc "$1"; }
[ "$(sql 'SHOW max_connections')" = 20 ]
[ "$(sql 'SHOW shared_buffers')" = 128MB ]
[ "$(sql 'SHOW password_encryption')" = scram-sha-256 ]
[ "$(sql "SELECT count(*) FROM pg_database WHERE datname IN ('lumira_service_dev','lumira_engineering_dev','lumira_partner_dev')")" = 3 ]
[ "$(docker inspect --format '{{.HostConfig.Memory}}' lumira-postgres-dev)" = 1073741824 ]
[ -z "$(docker port lumira-postgres-dev)" ]
cpu=$(docker inspect --format '{{.HostConfig.NanoCpus}}' lumira-postgres-dev)
if [ "$cpu" != 1000000000 ]; then
 quota=$(docker inspect --format '{{.HostConfig.CpuQuota}}' lumira-postgres-dev)
 period=$(docker inspect --format '{{.HostConfig.CpuPeriod}}' lumira-postgres-dev)
 [ "$quota" -gt 0 ] && [ "$quota" = "$period" ]
fi
for pair in 'service app' 'engineering engineering' 'partner partner'; do
 set -- $pair
 scope=$1; schema=$2
 db="lumira_${scope}_dev"; role="lumira_${scope}_runtime"
 [ "$(sql "SELECT rolcanlogin OR rolsuper OR rolcreatedb OR rolcreaterole FROM pg_roles WHERE rolname='$role'")" = f ]
 [ "$(sql "SELECT has_database_privilege('$role','$db','CONNECT')")" = t ]
 for other in service engineering partner; do
  [ "$scope" = "$other" ] && continue
  [ "$(sql "SELECT has_database_privilege('$role','lumira_${other}_dev','CONNECT')")" = f ]
 done
 [ "$(docker exec lumira-postgres-dev psql -X -U lumira_admin -d "$db" -Atc "SELECT version FROM $schema.schema_migrations")" = 001-bootstrap ]
done
echo 'PASS: resource caps, no published port, 3 databases, bootstrap versions and role isolation.'
echo 'Not tested: application LOGIN credentials, TLS, API authorization, RAID health or external backup.'
