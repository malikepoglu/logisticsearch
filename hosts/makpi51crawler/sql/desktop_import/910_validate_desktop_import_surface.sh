#!/usr/bin/env bash
set -Eeuo pipefail

DB_DEFAULT="logisticsearch_desktop_import_surface_scratch"
DB="${1:-$DB_DEFAULT}"
PSQL="sudo -u postgres psql -v ON_ERROR_STOP=1"

echo "== DESKTOP_IMPORT / SCRATCH VALIDATION RUNNER =="
date -Is
echo "DB=$DB"
echo

echo "== 1) RECREATE SCRATCH DB =="
sudo -u postgres dropdb --if-exists "$DB"
sudo -u postgres createdb "$DB"
echo "OK   scratch DB recreated"
echo

echo "== 2) PREFLIGHT =="
$PSQL -d "$DB" -f sql/desktop_import/901_preflight_desktop_import_surface.psql.sql
echo
echo "OK   preflight passed"
echo

echo "== 3) APPLY SURFACE =="
$PSQL -d "$DB" -f sql/desktop_import/900_apply_desktop_import_surface.psql.sql
echo
echo "OK   apply passed"
echo

echo "== 4) PRESENCE AUDIT =="
$PSQL -d "$DB" -f sql/desktop_import/902_presence_audit_desktop_import_surface.psql.sql
echo
echo "OK   presence audit passed"
echo

echo "== 5) FINAL SUMMARY =="
echo "VALIDATION_RESULT=PASS"
echo "SCRATCH_DB=$DB"
