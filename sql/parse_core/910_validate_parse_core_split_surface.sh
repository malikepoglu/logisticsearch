#!/usr/bin/env bash
set -Eeuo pipefail

DB="${1:-logisticsearch_parse_core_split_scratch}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CRAWLER_RUNNER="$REPO_ROOT/sql/crawler_core/910_validate_crawler_core_split_surface.sh"
STAGE_DIR="$(mktemp -d /tmp/parse_core_validate.XXXXXX)"

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

[ -x "$CRAWLER_RUNNER" ] || {
  echo "FAIL missing executable crawler runner: $CRAWLER_RUNNER" >&2
  exit 1
}

echo "== PARSE CORE SPLIT SURFACE VALIDATION RUNNER =="
date -Is
echo "DB=$DB"
echo "SCRIPT_DIR=$SCRIPT_DIR"
echo "REPO_ROOT=$REPO_ROOT"
echo "STAGE_DIR=$STAGE_DIR"
echo

echo "== 0) PREPARE STAGING PARSE SQL SURFACE =="
for f in \
  001_parse_base.sql \
  002_parse_evidence_and_candidate_upserts.sql \
  003_parse_preranking_persistence.sql \
  004_parse_workflow_state_and_payload.sql \
  900_apply_parse_core_split_surface.psql.sql \
  901_preflight_parse_core_split_surface.psql.sql \
  902_presence_audit_parse_core_split_surface.psql.sql
do
  copy_sql "$f"
done
echo "OK   staged parse SQL files prepared"
echo

echo "== 0.1) STAGING ACCESS CHECK FOR postgres =="
sudo -u postgres test -x "$STAGE_DIR"
sudo -u postgres test -r "$STAGE_DIR/900_apply_parse_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/901_preflight_parse_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/902_presence_audit_parse_core_split_surface.psql.sql"
echo "OK   postgres can access staged parse SQL files"
echo

echo "== 1) PREPARE SCRATCH DB WITH CRAWLER CORE UPSTREAM =="
"$CRAWLER_RUNNER" "$DB"
echo "OK   crawler-core upstream dependency prepared"
echo

echo "== 2) RUN PARSE PREFLIGHT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/901_preflight_parse_core_split_surface.psql.sql"
echo "OK   parse preflight passed"
echo

echo "== 3) RUN PARSE APPLY BUNDLE =="
sudo -u postgres bash -lc \
  "cd '$STAGE_DIR' && psql -v ON_ERROR_STOP=1 -d '$DB' -f 900_apply_parse_core_split_surface.psql.sql"
echo "OK   parse apply bundle passed"
echo

echo "== 4) RUN PARSE PRESENCE AUDIT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/902_presence_audit_parse_core_split_surface.psql.sql"
echo "OK   parse presence audit passed"
echo

echo "VALIDATION_RESULT=PASS"
echo "VALIDATED_DB=$DB"
