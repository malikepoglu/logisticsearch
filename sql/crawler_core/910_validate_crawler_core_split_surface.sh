#!/usr/bin/env bash
set -Eeuo pipefail

DB="${1:-logisticsearch_crawler_split_scratch}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_psql_file() {
  local file="$1"
  [ -f "$file" ] || {
    echo "FAIL missing SQL file: $file" >&2
    exit 1
  }
  sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" < "$file"
}

echo "== CRAWLER CORE SPLIT SURFACE VALIDATION RUNNER =="
date -Is
echo "DB=$DB"
echo "SCRIPT_DIR=$SCRIPT_DIR"
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
run_psql_file "$SCRIPT_DIR/901_preflight_crawler_core_split_surface.psql.sql"
echo "OK   preflight passed"
echo

echo "== 5) RUN APPLY BUNDLE =="
run_psql_file "$SCRIPT_DIR/900_apply_crawler_core_split_surface.psql.sql"
echo "OK   apply bundle passed"
echo

echo "== 6) RUN PRESENCE AUDIT =="
run_psql_file "$SCRIPT_DIR/902_presence_audit_crawler_core_split_surface.psql.sql"
echo "OK   presence audit passed"
echo

echo "VALIDATION_RESULT=PASS"
echo "VALIDATED_DB=$DB"
