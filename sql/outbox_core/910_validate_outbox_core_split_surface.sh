#!/usr/bin/env bash
set -Eeuo pipefail

DB="${1:-logisticsearch_outbox_core_split_scratch}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STAGE_DIR="$(mktemp -d /tmp/outbox_core_validate.XXXXXX)"

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

echo "== OUTBOX CORE SPLIT SURFACE VALIDATION RUNNER =="
date -Is
echo "DB=$DB"
echo "SCRIPT_DIR=$SCRIPT_DIR"
echo "REPO_ROOT=$REPO_ROOT"
echo "STAGE_DIR=$STAGE_DIR"
echo

echo "== 0) PREPARE STAGING OUTBOX SQL SURFACE =="
for f in \
  001_outbox_base.sql \
  002_outbox_enqueue_and_batch_creation.sql \
  003_outbox_batch_attachment_and_state_transitions.sql \
  900_apply_outbox_core_split_surface.psql.sql \
  901_preflight_outbox_core_split_surface.psql.sql \
  902_presence_audit_outbox_core_split_surface.psql.sql
do
  copy_sql "$f"
done
echo "OK   staged outbox SQL files prepared"
echo

echo "== 0.1) STAGING ACCESS CHECK FOR postgres =="
sudo -u postgres test -x "$STAGE_DIR"
sudo -u postgres test -r "$STAGE_DIR/901_preflight_outbox_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/900_apply_outbox_core_split_surface.psql.sql"
sudo -u postgres test -r "$STAGE_DIR/902_presence_audit_outbox_core_split_surface.psql.sql"
echo "OK   postgres can access staged outbox SQL files"
echo

echo "== 1) PREPARE SCRATCH DB WITH PARSE-CORE UPSTREAM =="
"$REPO_ROOT/sql/parse_core/910_validate_parse_core_split_surface.sh" "$DB"
echo "OK   parse-core upstream dependency prepared"
echo

echo "== 2) RUN OUTBOX PREFLIGHT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/901_preflight_outbox_core_split_surface.psql.sql"
echo "OK   outbox preflight passed"
echo

echo "== 3) RUN OUTBOX APPLY BUNDLE =="
sudo -u postgres bash -lc \
  "cd '$STAGE_DIR' && psql -v ON_ERROR_STOP=1 -d '$DB' -f 900_apply_outbox_core_split_surface.psql.sql"
echo "OK   outbox apply bundle passed"
echo

echo "== 4) RUN OUTBOX PRESENCE AUDIT =="
sudo -u postgres psql -v ON_ERROR_STOP=1 -d "$DB" \
  -f "$STAGE_DIR/902_presence_audit_outbox_core_split_surface.psql.sql"
echo "OK   outbox presence audit passed"
echo

echo "VALIDATION_RESULT=PASS"
echo "VALIDATED_DB=$DB"
