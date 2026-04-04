BEGIN;

CREATE SCHEMA IF NOT EXISTS desktop_import;

CREATE TABLE IF NOT EXISTS desktop_import.batch_intake (
  batch_key text PRIMARY KEY,
  export_channel text NOT NULL,
  source_system text NOT NULL DEFAULT 'pi51',
  source_repo_relpath text NOT NULL,
  source_repo_head text,
  source_commit_from_push_receipt text,
  item_count_expected integer NOT NULL,
  item_count_loaded integer NOT NULL,
  batch_payload_sha256 text NOT NULL,
  imported_at_utc timestamptz NOT NULL,
  manifest_json jsonb NOT NULL,
  push_receipt_json jsonb NOT NULL,
  import_receipt_json jsonb NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS desktop_import.page_export_raw (
  intake_row_id bigserial PRIMARY KEY,

  batch_key text NOT NULL REFERENCES desktop_import.batch_intake(batch_key) ON DELETE CASCADE,
  item_ordinal integer NOT NULL,

  export_item_id bigint,
  source_url_id bigint,
  source_snapshot_id bigint,

  canonical_url text,
  input_lang_code text,
  taxonomy_package_version text,
  top_candidate_count integer,
  top_score numeric,

  raw_item_json jsonb NOT NULL,
  raw_payload_json jsonb NOT NULL,

  imported_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),

  CONSTRAINT desktop_import_page_export_raw_batch_ordinal_uniq
    UNIQUE (batch_key, item_ordinal)
);

CREATE INDEX IF NOT EXISTS desktop_import_page_export_raw_batch_idx
  ON desktop_import.page_export_raw (batch_key);

CREATE INDEX IF NOT EXISTS desktop_import_page_export_raw_export_item_idx
  ON desktop_import.page_export_raw (export_item_id);

CREATE INDEX IF NOT EXISTS desktop_import_page_export_raw_source_url_idx
  ON desktop_import.page_export_raw (source_url_id);

COMMIT;
