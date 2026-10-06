#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
sh scripts/preflight.sh
if docker inspect lumira-postgres-dev >/dev/null 2>&1; then
 echo 'Container exists. Review it; this script does not replace deployments.' >&2; exit 1
fi
if [ -d data ] && [ -n "$(ls -A data)" ]; then
 echo 'Data directory is not empty. Do not reinitialize; review recovery/migration.' >&2; exit 1
fi
mkdir -p data backups
if docker compose version >/dev/null 2>&1; then
 docker compose -f docker-compose.yml up -d
else
 docker-compose -f docker-compose.yml up -d
fi
echo 'Container requested. Wait for health, then run verify.sh; initialization is not yet verified.'
