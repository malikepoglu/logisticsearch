-- Derived from live Pi51 parse function definitions

CREATE OR REPLACE FUNCTION parse.upsert_page_evidence_snapshot(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb DEFAULT '[]'::jsonb, p_title_queries jsonb DEFAULT '[]'::jsonb, p_h1_queries jsonb DEFAULT '[]'::jsonb, p_breadcrumb_queries jsonb DEFAULT '[]'::jsonb, p_structured_data_queries jsonb DEFAULT '[]'::jsonb, p_anchor_queries jsonb DEFAULT '[]'::jsonb, p_body_queries jsonb DEFAULT '[]'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_snapshot_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(snapshot_id bigint, url_id bigint, input_lang_code text)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_input_lang_code IS NULL OR btrim(p_input_lang_code) = '' THEN
    RAISE EXCEPTION 'p_input_lang_code must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO parse.page_evidence_snapshot AS pes (
    url_id,
    input_lang_code,
    url_queries,
    title_queries,
    h1_queries,
    breadcrumb_queries,
    structured_data_queries,
    anchor_queries,
    body_queries,
    source_run_id,
    source_note,
    snapshot_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_input_lang_code,
    COALESCE(p_url_queries, '[]'::jsonb),
    COALESCE(p_title_queries, '[]'::jsonb),
    COALESCE(p_h1_queries, '[]'::jsonb),
    COALESCE(p_breadcrumb_queries, '[]'::jsonb),
    COALESCE(p_structured_data_queries, '[]'::jsonb),
    COALESCE(p_anchor_queries, '[]'::jsonb),
    COALESCE(p_body_queries, '[]'::jsonb),
    p_source_run_id,
    p_source_note,
    COALESCE(p_snapshot_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT parse_page_evidence_snapshot_url_uniq
  DO UPDATE
     SET input_lang_code = EXCLUDED.input_lang_code,
         url_queries = EXCLUDED.url_queries,
         title_queries = EXCLUDED.title_queries,
         h1_queries = EXCLUDED.h1_queries,
         breadcrumb_queries = EXCLUDED.breadcrumb_queries,
         structured_data_queries = EXCLUDED.structured_data_queries,
         anchor_queries = EXCLUDED.anchor_queries,
         body_queries = EXCLUDED.body_queries,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         snapshot_metadata = EXCLUDED.snapshot_metadata,
         updated_at = now()
  RETURNING
    pes.snapshot_id,
    pes.url_id,
    pes.input_lang_code;
END;
$function$;


CREATE OR REPLACE FUNCTION parse.upsert_page_taxonomy_candidate(p_url_id bigint, p_taxonomy_package_version text, p_taxonomy_source_db text, p_taxonomy_package_id uuid, p_taxonomy_concept_id uuid, p_taxonomy_node_code text, p_taxonomy_concept_key text, p_input_lang_code text, p_matched_lang_codes jsonb DEFAULT '[]'::jsonb, p_matched_fields jsonb DEFAULT '[]'::jsonb, p_matched_queries jsonb DEFAULT '[]'::jsonb, p_domain_type text DEFAULT NULL::text, p_node_kind text DEFAULT NULL::text, p_url_score numeric DEFAULT 0, p_title_score numeric DEFAULT 0, p_h1_score numeric DEFAULT 0, p_breadcrumb_score numeric DEFAULT 0, p_structured_data_score numeric DEFAULT 0, p_anchor_score numeric DEFAULT 0, p_body_score numeric DEFAULT 0, p_total_score numeric DEFAULT 0, p_evidence_count integer DEFAULT 0, p_confidence_band text DEFAULT 'unreviewed'::text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_candidate_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(candidate_id bigint, url_id bigint, taxonomy_node_code text, taxonomy_concept_key text, total_score numeric, confidence_band text)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_taxonomy_package_version IS NULL OR btrim(p_taxonomy_package_version) = '' THEN
    RAISE EXCEPTION 'p_taxonomy_package_version must be non-empty';
  END IF;

  IF p_taxonomy_source_db IS NULL OR btrim(p_taxonomy_source_db) = '' THEN
    RAISE EXCEPTION 'p_taxonomy_source_db must be non-empty';
  END IF;

  IF p_taxonomy_package_id IS NULL THEN
    RAISE EXCEPTION 'p_taxonomy_package_id must not be null';
  END IF;

  IF p_taxonomy_concept_id IS NULL THEN
    RAISE EXCEPTION 'p_taxonomy_concept_id must not be null';
  END IF;

  IF p_taxonomy_node_code IS NULL OR btrim(p_taxonomy_node_code) = '' THEN
    RAISE EXCEPTION 'p_taxonomy_node_code must be non-empty';
  END IF;

  IF p_taxonomy_concept_key IS NULL OR btrim(p_taxonomy_concept_key) = '' THEN
    RAISE EXCEPTION 'p_taxonomy_concept_key must be non-empty';
  END IF;

  IF p_input_lang_code IS NULL OR btrim(p_input_lang_code) = '' THEN
    RAISE EXCEPTION 'p_input_lang_code must be non-empty';
  END IF;

  IF p_evidence_count IS NULL OR p_evidence_count < 0 THEN
    RAISE EXCEPTION 'p_evidence_count must be >= 0';
  END IF;

  RETURN QUERY
  INSERT INTO parse.page_taxonomy_candidate AS ptc (
    url_id,
    taxonomy_source_db,
    taxonomy_package_version,
    taxonomy_package_id,
    taxonomy_concept_id,
    taxonomy_node_code,
    taxonomy_concept_key,
    input_lang_code,
    matched_lang_codes,
    matched_fields,
    matched_queries,
    domain_type,
    node_kind,
    url_score,
    title_score,
    h1_score,
    breadcrumb_score,
    structured_data_score,
    anchor_score,
    body_score,
    total_score,
    evidence_count,
    confidence_band,
    source_run_id,
    source_note,
    candidate_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_taxonomy_source_db,
    p_taxonomy_package_version,
    p_taxonomy_package_id,
    p_taxonomy_concept_id,
    p_taxonomy_node_code,
    p_taxonomy_concept_key,
    p_input_lang_code,
    COALESCE(p_matched_lang_codes, '[]'::jsonb),
    COALESCE(p_matched_fields, '[]'::jsonb),
    COALESCE(p_matched_queries, '[]'::jsonb),
    p_domain_type,
    p_node_kind,
    COALESCE(p_url_score, 0),
    COALESCE(p_title_score, 0),
    COALESCE(p_h1_score, 0),
    COALESCE(p_breadcrumb_score, 0),
    COALESCE(p_structured_data_score, 0),
    COALESCE(p_anchor_score, 0),
    COALESCE(p_body_score, 0),
    COALESCE(p_total_score, 0),
    COALESCE(p_evidence_count, 0),
    COALESCE(p_confidence_band, 'unreviewed'),
    p_source_run_id,
    p_source_note,
    COALESCE(p_candidate_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT parse_page_taxonomy_candidate_url_pkg_concept_uniq
  DO UPDATE
     SET taxonomy_source_db = EXCLUDED.taxonomy_source_db,
         taxonomy_package_id = EXCLUDED.taxonomy_package_id,
         taxonomy_node_code = EXCLUDED.taxonomy_node_code,
         taxonomy_concept_key = EXCLUDED.taxonomy_concept_key,
         input_lang_code = EXCLUDED.input_lang_code,
         matched_lang_codes = EXCLUDED.matched_lang_codes,
         matched_fields = EXCLUDED.matched_fields,
         matched_queries = EXCLUDED.matched_queries,
         domain_type = EXCLUDED.domain_type,
         node_kind = EXCLUDED.node_kind,
         url_score = EXCLUDED.url_score,
         title_score = EXCLUDED.title_score,
         h1_score = EXCLUDED.h1_score,
         breadcrumb_score = EXCLUDED.breadcrumb_score,
         structured_data_score = EXCLUDED.structured_data_score,
         anchor_score = EXCLUDED.anchor_score,
         body_score = EXCLUDED.body_score,
         total_score = EXCLUDED.total_score,
         evidence_count = EXCLUDED.evidence_count,
         confidence_band = EXCLUDED.confidence_band,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         candidate_metadata = EXCLUDED.candidate_metadata,
         updated_at = now()
  RETURNING
    ptc.candidate_id,
    ptc.url_id,
    ptc.taxonomy_node_code,
    ptc.taxonomy_concept_key,
    ptc.total_score,
    ptc.confidence_band;
END;
$function$;


