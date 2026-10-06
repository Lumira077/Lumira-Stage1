#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
case "${PREFLIGHT_MODE:-healthy}" in
 healthy)
  [ "${STORAGE_HEALTH_VERIFIED:-}" = yes ] && [ "${EXTERNAL_RESTORE_VERIFIED:-}" = yes ] || { echo 'Blocked: verify healthy storage and independent restoration.' >&2; exit 1; } ;;
 synthetic)
  [ "${SYNTHETIC_ONLY:-}" = yes ] && [ "${STORAGE_STATE:-}" = degraded ] || { echo 'Blocked: explicitly acknowledge disposable synthetic data and degraded storage.' >&2; exit 1; }
  echo 'LIMITED TEST ONLY: no real data or load test; stop before disk replacement.' ;;
 *) echo 'Unknown preflight mode.' >&2; exit 1 ;;
esac
command -v docker >/dev/null
docker info >/dev/null
[ -f secrets/db_admin_password ] && [ ! -L secrets/db_admin_password ] || { echo 'Missing regular secret file.' >&2; exit 1; }
[ "$(wc -c < secrets/db_admin_password)" -ge 32 ] || { echo 'Secret too short.' >&2; exit 1; }
[ "$(stat -c %a secrets/db_admin_password)" = 600 ] || { echo 'Secret permissions must be 600.' >&2; exit 1; }
if docker compose version >/dev/null 2>&1; then
 docker compose -f docker-compose.yml config >/dev/null
elif command -v docker-compose >/dev/null; then
 docker-compose -f docker-compose.yml config >/dev/null
else
 echo 'Compose unavailable: review deployment method; do not install unofficial packages.' >&2; exit 1
fi
echo 'Preflight passed; flags are operator attestations, not automatic RAID/backup diagnostics.'
