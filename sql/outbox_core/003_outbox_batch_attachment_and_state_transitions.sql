-- Derived from live Pi51 outbox function definitions

CREATE OR REPLACE FUNCTION outbox.attach_export_item_to_batch(p_export_item_id bigint, p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(batch_item_id bigint, batch_id bigint, export_item_id bigint, export_state outbox.export_state_enum)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_export_item_id IS NULL OR p_export_item_id <= 0 THEN
    RAISE EXCEPTION 'p_export_item_id must be > 0';
  END IF;

  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  WITH batch_link AS (
    INSERT INTO outbox.export_batch_item AS oebi (
      batch_id,
      export_item_id,
      source_run_id,
      source_note,
      item_metadata,
      updated_at
    )
    VALUES (
      p_batch_id,
      p_export_item_id,
      p_source_run_id,
      p_source_note,
      COALESCE(p_item_metadata, '{}'::jsonb),
      now()
    )
    ON CONFLICT ON CONSTRAINT outbox_export_batch_item_export_item_uniq
    DO UPDATE
       SET batch_id = EXCLUDED.batch_id,
           source_run_id = EXCLUDED.source_run_id,
           source_note = EXCLUDED.source_note,
           item_metadata = EXCLUDED.item_metadata,
           updated_at = now()
    RETURNING
      oebi.batch_item_id,
      oebi.batch_id,
      oebi.export_item_id
  ),
  item_upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'materialized'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id = p_export_item_id
    RETURNING opei.export_state
  )
  SELECT
    bl.batch_item_id,
    bl.batch_id,
    bl.export_item_id,
    iu.export_state
  FROM batch_link bl
  CROSS JOIN item_upd iu;
END;
$function$;


CREATE OR REPLACE FUNCTION outbox.mark_export_batch_failed(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(batch_id bigint, batch_state outbox.batch_state_enum)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  UPDATE outbox.export_batch AS oeb
  SET batch_state = 'failed'::outbox.batch_state_enum,
      source_run_id = COALESCE(p_source_run_id, oeb.source_run_id),
      source_note = COALESCE(p_source_note, oeb.source_note),
      batch_metadata = COALESCE(oeb.batch_metadata, '{}'::jsonb) || COALESCE(p_batch_metadata, '{}'::jsonb),
      updated_at = now()
  WHERE oeb.batch_id = p_batch_id
  RETURNING oeb.batch_id, oeb.batch_state;
END;
$function$;


CREATE OR REPLACE FUNCTION outbox.mark_export_batch_pushed(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(batch_id bigint, batch_state outbox.batch_state_enum)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  UPDATE outbox.export_batch AS oeb
  SET batch_state = 'pushed'::outbox.batch_state_enum,
      source_run_id = COALESCE(p_source_run_id, oeb.source_run_id),
      source_note = COALESCE(p_source_note, oeb.source_note),
      batch_metadata = COALESCE(oeb.batch_metadata, '{}'::jsonb) || COALESCE(p_batch_metadata, '{}'::jsonb),
      updated_at = now()
  WHERE oeb.batch_id = p_batch_id
  RETURNING oeb.batch_id, oeb.batch_state;
END;
$function$;


CREATE OR REPLACE FUNCTION outbox.mark_export_items_pushed_by_batch(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(updated_count integer)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_count integer;
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  WITH upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'pushed'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id IN (
      SELECT ebi.export_item_id
      FROM outbox.export_batch_item ebi
      WHERE ebi.batch_id = p_batch_id
    )
    RETURNING 1
  )
  SELECT count(*) INTO v_count FROM upd;

  RETURN QUERY SELECT COALESCE(v_count, 0);
END;
$function$;


CREATE OR REPLACE FUNCTION outbox.requeue_export_items_by_batch(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(updated_count integer)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_count integer;
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  WITH upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'queued'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id IN (
      SELECT ebi.export_item_id
      FROM outbox.export_batch_item ebi
      WHERE ebi.batch_id = p_batch_id
    )
    RETURNING 1
  )
  SELECT count(*) INTO v_count FROM upd;

  RETURN QUERY SELECT COALESCE(v_count, 0);
END;
$function$;


