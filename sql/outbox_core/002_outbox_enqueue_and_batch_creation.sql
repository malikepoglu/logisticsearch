-- Derived from live Pi51 outbox function definitions

CREATE OR REPLACE FUNCTION outbox.create_export_batch(p_export_channel text, p_batch_key text, p_item_count integer, p_payload_sha256 text, p_manifest jsonb, p_storage_relpath text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(batch_id bigint, export_channel text, batch_key text, batch_state outbox.batch_state_enum, item_count integer, payload_sha256 text)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_export_channel IS NULL OR btrim(p_export_channel) = '' THEN
    RAISE EXCEPTION 'p_export_channel must be non-empty';
  END IF;

  IF p_batch_key IS NULL OR btrim(p_batch_key) = '' THEN
    RAISE EXCEPTION 'p_batch_key must be non-empty';
  END IF;

  IF p_payload_sha256 IS NULL OR btrim(p_payload_sha256) = '' THEN
    RAISE EXCEPTION 'p_payload_sha256 must be non-empty';
  END IF;

  IF p_storage_relpath IS NULL OR btrim(p_storage_relpath) = '' THEN
    RAISE EXCEPTION 'p_storage_relpath must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO outbox.export_batch AS oeb (
    export_channel,
    batch_key,
    batch_state,
    item_count,
    payload_sha256,
    manifest,
    storage_relpath,
    source_run_id,
    source_note,
    batch_metadata,
    updated_at
  )
  VALUES (
    p_export_channel,
    p_batch_key,
    'materialized'::outbox.batch_state_enum,
    COALESCE(p_item_count, 0),
    p_payload_sha256,
    COALESCE(p_manifest, '{}'::jsonb),
    p_storage_relpath,
    p_source_run_id,
    p_source_note,
    COALESCE(p_batch_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT outbox_export_batch_batch_key_uniq
  DO UPDATE
     SET export_channel = EXCLUDED.export_channel,
         batch_state = 'materialized'::outbox.batch_state_enum,
         item_count = EXCLUDED.item_count,
         payload_sha256 = EXCLUDED.payload_sha256,
         manifest = EXCLUDED.manifest,
         storage_relpath = EXCLUDED.storage_relpath,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         batch_metadata = EXCLUDED.batch_metadata,
         updated_at = now()
  RETURNING
    oeb.batch_id,
    oeb.export_channel,
    oeb.batch_key,
    oeb.batch_state,
    oeb.item_count,
    oeb.payload_sha256;
END;
$function$;


CREATE OR REPLACE FUNCTION outbox.enqueue_page_export_item(p_url_id bigint, p_snapshot_id bigint, p_workflow_status_id bigint, p_export_channel text, p_payload jsonb, p_payload_sha256 text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_export_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(export_item_id bigint, url_id bigint, snapshot_id bigint, workflow_status_id bigint, export_channel text, export_state outbox.export_state_enum, payload_sha256 text)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL OR p_url_id <= 0 THEN
    RAISE EXCEPTION 'p_url_id must be > 0';
  END IF;

  IF p_snapshot_id IS NULL OR p_snapshot_id <= 0 THEN
    RAISE EXCEPTION 'p_snapshot_id must be > 0';
  END IF;

  IF p_workflow_status_id IS NULL OR p_workflow_status_id <= 0 THEN
    RAISE EXCEPTION 'p_workflow_status_id must be > 0';
  END IF;

  IF p_export_channel IS NULL OR btrim(p_export_channel) = '' THEN
    RAISE EXCEPTION 'p_export_channel must be non-empty';
  END IF;

  IF p_payload IS NULL THEN
    RAISE EXCEPTION 'p_payload must not be null';
  END IF;

  IF p_payload_sha256 IS NULL OR btrim(p_payload_sha256) = '' THEN
    RAISE EXCEPTION 'p_payload_sha256 must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO outbox.page_export_item AS opei (
    url_id,
    snapshot_id,
    workflow_status_id,
    export_channel,
    export_state,
    payload,
    payload_sha256,
    source_run_id,
    source_note,
    export_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_snapshot_id,
    p_workflow_status_id,
    p_export_channel,
    'queued'::outbox.export_state_enum,
    p_payload,
    p_payload_sha256,
    p_source_run_id,
    p_source_note,
    COALESCE(p_export_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT outbox_page_export_item_url_channel_snapshot_uniq
  DO UPDATE
     SET workflow_status_id = EXCLUDED.workflow_status_id,
         export_state = 'queued'::outbox.export_state_enum,
         payload = EXCLUDED.payload,
         payload_sha256 = EXCLUDED.payload_sha256,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         export_metadata = EXCLUDED.export_metadata,
         updated_at = now()
  RETURNING
    opei.export_item_id,
    opei.url_id,
    opei.snapshot_id,
    opei.workflow_status_id,
    opei.export_channel,
    opei.export_state,
    opei.payload_sha256;
END;
$function$;


