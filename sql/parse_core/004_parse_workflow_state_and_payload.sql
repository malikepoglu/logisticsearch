-- Derived from live Pi51 parse function definitions

CREATE OR REPLACE FUNCTION parse.persist_taxonomy_preranking_payload(p_payload jsonb)
 RETURNS TABLE(url_id bigint, input_lang_code text, snapshot_id bigint, persisted_candidate_count integer, source_run_id text)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_url_id bigint;
  v_input_lang_code text;
  v_source_run_id text;
  v_snapshot_id bigint;
  v_persisted_candidate_count integer;
BEGIN
  IF p_payload IS NULL THEN
    RAISE EXCEPTION 'p_payload must not be null';
  END IF;

  IF jsonb_typeof(p_payload) <> 'object' THEN
    RAISE EXCEPTION 'p_payload must be a jsonb object';
  END IF;

  v_url_id := NULLIF(p_payload->>'url_id', '')::bigint;
  v_input_lang_code := NULLIF(p_payload->>'input_lang_code', '');
  v_source_run_id := NULLIF(p_payload->>'source_run_id', '');

  IF v_url_id IS NULL THEN
    RAISE EXCEPTION 'payload.url_id must not be null';
  END IF;

  IF v_input_lang_code IS NULL OR btrim(v_input_lang_code) = '' THEN
    RAISE EXCEPTION 'payload.input_lang_code must be non-empty';
  END IF;

  SELECT p.snapshot_id, p.persisted_candidate_count
  INTO v_snapshot_id, v_persisted_candidate_count
  FROM parse.persist_page_taxonomy_preranking(
    p_url_id := v_url_id,
    p_input_lang_code := v_input_lang_code,
    p_url_queries := COALESCE(p_payload->'url_queries', '[]'::jsonb),
    p_title_queries := COALESCE(p_payload->'title_queries', '[]'::jsonb),
    p_h1_queries := COALESCE(p_payload->'h1_queries', '[]'::jsonb),
    p_breadcrumb_queries := COALESCE(p_payload->'breadcrumb_queries', '[]'::jsonb),
    p_structured_data_queries := COALESCE(p_payload->'structured_data_queries', '[]'::jsonb),
    p_anchor_queries := COALESCE(p_payload->'anchor_queries', '[]'::jsonb),
    p_body_queries := COALESCE(p_payload->'body_queries', '[]'::jsonb),
    p_candidates := COALESCE(p_payload->'candidates', '[]'::jsonb),
    p_source_run_id := v_source_run_id,
    p_source_note := NULLIF(p_payload->>'source_note', ''),
    p_metadata := COALESCE(p_payload->'metadata', '{}'::jsonb),
    p_replace_existing_candidates := COALESCE((p_payload->>'replace_existing_candidates')::boolean, true)
  ) p;

  RETURN QUERY
  SELECT
    v_url_id,
    v_input_lang_code,
    v_snapshot_id,
    COALESCE(v_persisted_candidate_count, 0),
    v_source_run_id;
END;
$function$;


CREATE OR REPLACE FUNCTION parse.upsert_page_workflow_status(p_url_id bigint, p_workflow_state parse.workflow_state_enum, p_state_reason text DEFAULT NULL::text, p_linked_snapshot_id bigint DEFAULT NULL::bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_status_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(status_id bigint, url_id bigint, workflow_state parse.workflow_state_enum, state_version integer, linked_snapshot_id bigint)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL OR p_url_id <= 0 THEN
    RAISE EXCEPTION 'p_url_id must be > 0';
  END IF;

  RETURN QUERY
  INSERT INTO parse.page_workflow_status AS pws (
    url_id,
    linked_snapshot_id,
    workflow_state,
    state_reason,
    source_run_id,
    source_note,
    status_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_linked_snapshot_id,
    p_workflow_state,
    p_state_reason,
    p_source_run_id,
    p_source_note,
    COALESCE(p_status_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT parse_page_workflow_status_url_uniq
  DO UPDATE
     SET linked_snapshot_id = EXCLUDED.linked_snapshot_id,
         workflow_state = EXCLUDED.workflow_state,
         state_reason = EXCLUDED.state_reason,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         status_metadata = EXCLUDED.status_metadata,
         state_version = pws.state_version + 1,
         updated_at = now()
  RETURNING
    pws.status_id,
    pws.url_id,
    pws.workflow_state,
    pws.state_version,
    pws.linked_snapshot_id;
END;
$function$;


