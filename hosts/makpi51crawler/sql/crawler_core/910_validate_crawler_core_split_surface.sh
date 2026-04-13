#!/usr/bin/env bash
set -Eeuo pipefail

DB="${1:-logisticsearch_crawler_split_scratch}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE_DIR="$(mktemp -d /tmp/crawler_core_validate.XXXXXX)"

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT

chmod 0755 "$STAGE_DIR"

copy_sql() {
  local f="$1"
  [ -f "$SCRIPT_DIR/$f" ] || {
    echo "FAIL missing SQL file: $SCRIPT_DIR/$f" >&2
    exit 1
  }
  cp "$SCRIPT_DIR/$f" "$STAGE_DIR/$f"
  chmod 0644 "$STAGE_DIR/$f"
}

echo "== CRAWLER CORE SPLIT SURFACE VALIDATION RUNNER =="
date -Is
echo "DB=$DB"
echo "SCRIPT_DIR=$SCRIPT_DIR"
echo "STAGE_DIR=$STAGE_DIR"
echo

echo "== 0) PREPARE STAGING SQL SURFACE =="
for f in \
  001_seed_frontier_http_fetch_base.sql \
  002_frontier_claim_and_lease.sql \
  003_frontier_finish_transitions.sql \
  004_frontier_politeness_and_freshness.sql \
  005_http_fetch_robots_cache_and_enforcement.sql \
  900_apply_crawler_core_split_surface.psql.sql \
  901_preflight_crawler_core_split_surface.psql.sql \
  902_presence_audit_crawler_core_split_surface.psql.sql
do
  copy_sql "$f"
done
echo "OK   staged SQL files prepared"
echo

echo "== 0.1) STAGING ACCESS CHECK FOR postgres =="
sudo -u postgres test -x "$STAGE_DIR"
sudo -u postgres test -r "$STAGE_DIR/901_preflight_crawler_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/900_apply_crawler_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/902_presence_audit_crawler_core_split_surface.psql.sql"
echo "OK   postgres can access staged SQL files"
echo

echo "== 1) DROP SCRATCH DB IF EXISTS =="
sudo -u postgres dropdb --if-exists "$DB"
echo "OK   previous scratch DB removed if present"
echo

echo "== 2) CREATE SCRATCH DB =="
sudo -u postgres createdb "$DB"
echo "OK   scratch DB created"
echo

echo "== 3) ENSURE REQUIRED EXTENSION =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -c "CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;"
echo "OK   pgcrypto ensured in public schema"
echo

echo "== 4) RUN PREFLIGHT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/901_preflight_crawler_core_split_surface.psql.sql"
echo "OK   preflight passed"
echo

echo "== 5) RUN APPLY BUNDLE =="
sudo -u postgres bash -lc \
  "cd '$STAGE_DIR' && psql -v ON_ERROR_STOP=1 -d '$DB' -f 900_apply_crawler_core_split_surface.psql.sql"
echo "OK   apply bundle passed"
echo

echo "== 6) RUN PRESENCE AUDIT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/902_presence_audit_crawler_core_split_surface.psql.sql"
echo "OK   presence audit passed"
echo

echo "VALIDATION_RESULT=PASS"
echo "VALIDATED_DB=$DB"
