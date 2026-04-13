-- Derived from live Pi51 parse function definitions

CREATE OR REPLACE FUNCTION parse.persist_page_preranking_snapshot(p_url_id bigint, p_input_lang_code text, p_taxonomy_package_version text, p_top_candidate_count integer DEFAULT 0, p_top_score numeric DEFAULT NULL::numeric, p_candidate_summary jsonb DEFAULT '[]'::jsonb, p_snapshot_metadata jsonb DEFAULT '{}'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_review_status text DEFAULT 'pre_ranked'::text)
 RETURNS TABLE(snapshot_id bigint, url_id bigint, top_candidate_count integer, top_score numeric, review_status text)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL OR p_url_id <= 0 THEN
    RAISE EXCEPTION 'p_url_id must be > 0';
  END IF;

  IF p_input_lang_code IS NULL OR btrim(p_input_lang_code) = '' THEN
    RAISE EXCEPTION 'p_input_lang_code must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO parse.page_preranking_snapshot AS pps (
    url_id,
    input_lang_code,
    taxonomy_package_version,
    top_candidate_count,
    top_score,
    candidate_summary,
    review_status,
    source_run_id,
    source_note,
    snapshot_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_input_lang_code,
    p_taxonomy_package_version,
    COALESCE(p_top_candidate_count, 0),
    p_top_score,
    COALESCE(p_candidate_summary, '[]'::jsonb),
    COALESCE(p_review_status, 'pre_ranked'),
    p_source_run_id,
    p_source_note,
    COALESCE(p_snapshot_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT parse_page_preranking_snapshot_url_uniq
  DO UPDATE
     SET input_lang_code = EXCLUDED.input_lang_code,
         taxonomy_package_version = EXCLUDED.taxonomy_package_version,
         top_candidate_count = EXCLUDED.top_candidate_count,
         top_score = EXCLUDED.top_score,
         candidate_summary = EXCLUDED.candidate_summary,
         review_status = EXCLUDED.review_status,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         snapshot_metadata = EXCLUDED.snapshot_metadata,
         updated_at = now()
  RETURNING
    pps.snapshot_id,
    pps.url_id,
    pps.top_candidate_count,
    pps.top_score,
    pps.review_status;
END;
$function$;


CREATE OR REPLACE FUNCTION parse.persist_page_taxonomy_candidates(p_url_id bigint, p_candidates jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_replace_existing boolean DEFAULT true)
 RETURNS TABLE(persisted_count integer)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_candidate jsonb;
  v_count integer := 0;
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_candidates IS NULL THEN
    RAISE EXCEPTION 'p_candidates must not be null';
  END IF;

  IF jsonb_typeof(p_candidates) <> 'array' THEN
    RAISE EXCEPTION 'p_candidates must be a jsonb array';
  END IF;

  IF p_replace_existing THEN
    DELETE FROM parse.page_taxonomy_candidate
    WHERE url_id = p_url_id;
  END IF;

  FOR v_candidate IN
    SELECT value
    FROM jsonb_array_elements(p_candidates)
  LOOP
    PERFORM parse.upsert_page_taxonomy_candidate(
      p_url_id := p_url_id,
      p_taxonomy_package_version := COALESCE(v_candidate->>'taxonomy_package_version', ''),
      p_taxonomy_source_db := COALESCE(v_candidate->>'taxonomy_source_db', 'logisticsearch_taxonomy'),
      p_taxonomy_package_id := NULLIF(v_candidate->>'taxonomy_package_id', '')::uuid,
      p_taxonomy_concept_id := NULLIF(v_candidate->>'taxonomy_concept_id', '')::uuid,
      p_taxonomy_node_code := COALESCE(v_candidate->>'taxonomy_node_code', ''),
      p_taxonomy_concept_key := COALESCE(v_candidate->>'taxonomy_concept_key', ''),
      p_input_lang_code := COALESCE(v_candidate->>'input_lang_code', ''),
      p_matched_lang_codes := COALESCE(v_candidate->'matched_lang_codes', '[]'::jsonb),
      p_matched_fields := COALESCE(v_candidate->'matched_fields', '[]'::jsonb),
      p_matched_queries := COALESCE(v_candidate->'matched_queries', '[]'::jsonb),
      p_domain_type := NULLIF(v_candidate->>'domain_type', ''),
      p_node_kind := NULLIF(v_candidate->>'node_kind', ''),
      p_url_score := COALESCE((v_candidate->>'url_score')::numeric, 0),
      p_title_score := COALESCE((v_candidate->>'title_score')::numeric, 0),
      p_h1_score := COALESCE((v_candidate->>'h1_score')::numeric, 0),
      p_breadcrumb_score := COALESCE((v_candidate->>'breadcrumb_score')::numeric, 0),
      p_structured_data_score := COALESCE((v_candidate->>'structured_data_score')::numeric, 0),
      p_anchor_score := COALESCE((v_candidate->>'anchor_score')::numeric, 0),
      p_body_score := COALESCE((v_candidate->>'body_score')::numeric, 0),
      p_total_score := COALESCE((v_candidate->>'total_score')::numeric, 0),
      p_evidence_count := COALESCE((v_candidate->>'evidence_count')::integer, 0),
      p_confidence_band := COALESCE(NULLIF(v_candidate->>'confidence_band', ''), 'unreviewed'),
      p_source_run_id := COALESCE(NULLIF(v_candidate->>'source_run_id', ''), p_source_run_id),
      p_source_note := COALESCE(NULLIF(v_candidate->>'source_note', ''), p_source_note),
      p_candidate_metadata := COALESCE(v_candidate->'candidate_metadata', '{}'::jsonb)
    );

    v_count := v_count + 1;
  END LOOP;

  RETURN QUERY
  SELECT v_count;
END;
$function$;


CREATE OR REPLACE FUNCTION parse.persist_page_taxonomy_preranking(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb DEFAULT '[]'::jsonb, p_title_queries jsonb DEFAULT '[]'::jsonb, p_h1_queries jsonb DEFAULT '[]'::jsonb, p_breadcrumb_queries jsonb DEFAULT '[]'::jsonb, p_structured_data_queries jsonb DEFAULT '[]'::jsonb, p_anchor_queries jsonb DEFAULT '[]'::jsonb, p_body_queries jsonb DEFAULT '[]'::jsonb, p_candidates jsonb DEFAULT '[]'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_metadata jsonb DEFAULT '{}'::jsonb, p_replace_existing_candidates boolean DEFAULT true)
 RETURNS TABLE(snapshot_id bigint, persisted_candidate_count integer)
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_snapshot_id bigint;
  v_persisted_candidate_count integer;
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_input_lang_code IS NULL OR btrim(p_input_lang_code) = '' THEN
    RAISE EXCEPTION 'p_input_lang_code must be non-empty';
  END IF;

  SELECT s.snapshot_id
  INTO v_snapshot_id
  FROM parse.upsert_page_evidence_snapshot(
    p_url_id := p_url_id,
    p_input_lang_code := p_input_lang_code,
    p_url_queries := COALESCE(p_url_queries, '[]'::jsonb),
    p_title_queries := COALESCE(p_title_queries, '[]'::jsonb),
    p_h1_queries := COALESCE(p_h1_queries, '[]'::jsonb),
    p_breadcrumb_queries := COALESCE(p_breadcrumb_queries, '[]'::jsonb),
    p_structured_data_queries := COALESCE(p_structured_data_queries, '[]'::jsonb),
    p_anchor_queries := COALESCE(p_anchor_queries, '[]'::jsonb),
    p_body_queries := COALESCE(p_body_queries, '[]'::jsonb),
    p_source_run_id := p_source_run_id,
    p_source_note := p_source_note,
    p_snapshot_metadata := COALESCE(p_metadata, '{}'::jsonb)
  ) s;

  SELECT p.persisted_count
  INTO v_persisted_candidate_count
  FROM parse.persist_page_taxonomy_candidates(
    p_url_id := p_url_id,
    p_candidates := COALESCE(p_candidates, '[]'::jsonb),
    p_source_run_id := p_source_run_id,
    p_source_note := p_source_note,
    p_replace_existing := p_replace_existing_candidates
  ) p;

  RETURN QUERY
  SELECT
    v_snapshot_id,
    COALESCE(v_persisted_candidate_count, 0);
END;
$function$;


