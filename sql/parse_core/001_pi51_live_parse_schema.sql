--
-- PostgreSQL database dump
--

\restrict 3WYf7C8kCRl41tFg5MQuVhncb4Dp32Ei2yXRr7tlvueFa3YO5iEra19S3i70jg9

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: parse; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA parse;


--
-- Name: workflow_state_enum; Type: TYPE; Schema: parse; Owner: -
--

CREATE TYPE parse.workflow_state_enum AS ENUM (
    'pre_ranked',
    'review_hold',
    'export_ready',
    'exported',
    'discarded'
);


--
-- Name: persist_page_preranking_snapshot(bigint, text, text, integer, numeric, jsonb, jsonb, text, text, text); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.persist_page_preranking_snapshot(p_url_id bigint, p_input_lang_code text, p_taxonomy_package_version text, p_top_candidate_count integer DEFAULT 0, p_top_score numeric DEFAULT NULL::numeric, p_candidate_summary jsonb DEFAULT '[]'::jsonb, p_snapshot_metadata jsonb DEFAULT '{}'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_review_status text DEFAULT 'pre_ranked'::text) RETURNS TABLE(snapshot_id bigint, url_id bigint, top_candidate_count integer, top_score numeric, review_status text)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION persist_page_preranking_snapshot(p_url_id bigint, p_input_lang_code text, p_taxonomy_package_version text, p_top_candidate_count integer, p_top_score numeric, p_candidate_summary jsonb, p_snapshot_metadata jsonb, p_source_run_id text, p_source_note text, p_review_status text); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.persist_page_preranking_snapshot(p_url_id bigint, p_input_lang_code text, p_taxonomy_package_version text, p_top_candidate_count integer, p_top_score numeric, p_candidate_summary jsonb, p_snapshot_metadata jsonb, p_source_run_id text, p_source_note text, p_review_status text) IS 'Creates or updates the final Pi51 pre-ranking snapshot for one parsed URL after candidate consolidation.';


--
-- Name: persist_page_taxonomy_candidates(bigint, jsonb, text, text, boolean); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.persist_page_taxonomy_candidates(p_url_id bigint, p_candidates jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_replace_existing boolean DEFAULT true) RETURNS TABLE(persisted_count integer)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION persist_page_taxonomy_candidates(p_url_id bigint, p_candidates jsonb, p_source_run_id text, p_source_note text, p_replace_existing boolean); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.persist_page_taxonomy_candidates(p_url_id bigint, p_candidates jsonb, p_source_run_id text, p_source_note text, p_replace_existing boolean) IS 'Persists a batch of Pi51 taxonomy pre-ranking candidates for one parsed page/url from a JSON array payload.';


--
-- Name: persist_page_taxonomy_preranking(bigint, text, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, text, text, jsonb, boolean); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.persist_page_taxonomy_preranking(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb DEFAULT '[]'::jsonb, p_title_queries jsonb DEFAULT '[]'::jsonb, p_h1_queries jsonb DEFAULT '[]'::jsonb, p_breadcrumb_queries jsonb DEFAULT '[]'::jsonb, p_structured_data_queries jsonb DEFAULT '[]'::jsonb, p_anchor_queries jsonb DEFAULT '[]'::jsonb, p_body_queries jsonb DEFAULT '[]'::jsonb, p_candidates jsonb DEFAULT '[]'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_metadata jsonb DEFAULT '{}'::jsonb, p_replace_existing_candidates boolean DEFAULT true) RETURNS TABLE(snapshot_id bigint, persisted_candidate_count integer)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION persist_page_taxonomy_preranking(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb, p_title_queries jsonb, p_h1_queries jsonb, p_breadcrumb_queries jsonb, p_structured_data_queries jsonb, p_anchor_queries jsonb, p_body_queries jsonb, p_candidates jsonb, p_source_run_id text, p_source_note text, p_metadata jsonb, p_replace_existing_candidates boolean); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.persist_page_taxonomy_preranking(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb, p_title_queries jsonb, p_h1_queries jsonb, p_breadcrumb_queries jsonb, p_structured_data_queries jsonb, p_anchor_queries jsonb, p_body_queries jsonb, p_candidates jsonb, p_source_run_id text, p_source_note text, p_metadata jsonb, p_replace_existing_candidates boolean) IS 'Persists both page evidence snapshot and Pi51 taxonomy pre-ranking candidates for one parsed page/url in a single helper call.';


--
-- Name: persist_taxonomy_preranking_payload(jsonb); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.persist_taxonomy_preranking_payload(p_payload jsonb) RETURNS TABLE(url_id bigint, input_lang_code text, snapshot_id bigint, persisted_candidate_count integer, source_run_id text)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION persist_taxonomy_preranking_payload(p_payload jsonb); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.persist_taxonomy_preranking_payload(p_payload jsonb) IS 'Python-worker-facing payload contract for persisting page evidence snapshot and taxonomy pre-ranking candidates in one call.';


--
-- Name: upsert_page_evidence_snapshot(bigint, text, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, text, text, jsonb); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.upsert_page_evidence_snapshot(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb DEFAULT '[]'::jsonb, p_title_queries jsonb DEFAULT '[]'::jsonb, p_h1_queries jsonb DEFAULT '[]'::jsonb, p_breadcrumb_queries jsonb DEFAULT '[]'::jsonb, p_structured_data_queries jsonb DEFAULT '[]'::jsonb, p_anchor_queries jsonb DEFAULT '[]'::jsonb, p_body_queries jsonb DEFAULT '[]'::jsonb, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_snapshot_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(snapshot_id bigint, url_id bigint, input_lang_code text)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION upsert_page_evidence_snapshot(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb, p_title_queries jsonb, p_h1_queries jsonb, p_breadcrumb_queries jsonb, p_structured_data_queries jsonb, p_anchor_queries jsonb, p_body_queries jsonb, p_source_run_id text, p_source_note text, p_snapshot_metadata jsonb); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.upsert_page_evidence_snapshot(p_url_id bigint, p_input_lang_code text, p_url_queries jsonb, p_title_queries jsonb, p_h1_queries jsonb, p_breadcrumb_queries jsonb, p_structured_data_queries jsonb, p_anchor_queries jsonb, p_body_queries jsonb, p_source_run_id text, p_source_note text, p_snapshot_metadata jsonb) IS 'Creates or updates the raw page evidence snapshot that feeds Pi51 taxonomy pre-ranking.';


--
-- Name: upsert_page_taxonomy_candidate(bigint, text, text, uuid, uuid, text, text, text, jsonb, jsonb, jsonb, text, text, numeric, numeric, numeric, numeric, numeric, numeric, numeric, numeric, integer, text, text, text, jsonb); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.upsert_page_taxonomy_candidate(p_url_id bigint, p_taxonomy_package_version text, p_taxonomy_source_db text, p_taxonomy_package_id uuid, p_taxonomy_concept_id uuid, p_taxonomy_node_code text, p_taxonomy_concept_key text, p_input_lang_code text, p_matched_lang_codes jsonb DEFAULT '[]'::jsonb, p_matched_fields jsonb DEFAULT '[]'::jsonb, p_matched_queries jsonb DEFAULT '[]'::jsonb, p_domain_type text DEFAULT NULL::text, p_node_kind text DEFAULT NULL::text, p_url_score numeric DEFAULT 0, p_title_score numeric DEFAULT 0, p_h1_score numeric DEFAULT 0, p_breadcrumb_score numeric DEFAULT 0, p_structured_data_score numeric DEFAULT 0, p_anchor_score numeric DEFAULT 0, p_body_score numeric DEFAULT 0, p_total_score numeric DEFAULT 0, p_evidence_count integer DEFAULT 0, p_confidence_band text DEFAULT 'unreviewed'::text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_candidate_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(candidate_id bigint, url_id bigint, taxonomy_node_code text, taxonomy_concept_key text, total_score numeric, confidence_band text)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION upsert_page_taxonomy_candidate(p_url_id bigint, p_taxonomy_package_version text, p_taxonomy_source_db text, p_taxonomy_package_id uuid, p_taxonomy_concept_id uuid, p_taxonomy_node_code text, p_taxonomy_concept_key text, p_input_lang_code text, p_matched_lang_codes jsonb, p_matched_fields jsonb, p_matched_queries jsonb, p_domain_type text, p_node_kind text, p_url_score numeric, p_title_score numeric, p_h1_score numeric, p_breadcrumb_score numeric, p_structured_data_score numeric, p_anchor_score numeric, p_body_score numeric, p_total_score numeric, p_evidence_count integer, p_confidence_band text, p_source_run_id text, p_source_note text, p_candidate_metadata jsonb); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.upsert_page_taxonomy_candidate(p_url_id bigint, p_taxonomy_package_version text, p_taxonomy_source_db text, p_taxonomy_package_id uuid, p_taxonomy_concept_id uuid, p_taxonomy_node_code text, p_taxonomy_concept_key text, p_input_lang_code text, p_matched_lang_codes jsonb, p_matched_fields jsonb, p_matched_queries jsonb, p_domain_type text, p_node_kind text, p_url_score numeric, p_title_score numeric, p_h1_score numeric, p_breadcrumb_score numeric, p_structured_data_score numeric, p_anchor_score numeric, p_body_score numeric, p_total_score numeric, p_evidence_count integer, p_confidence_band text, p_source_run_id text, p_source_note text, p_candidate_metadata jsonb) IS 'Creates or updates a Pi51 pre-ranking taxonomy candidate for a parsed page/url using cross-database-safe taxonomy snapshot identifiers.';


--
-- Name: upsert_page_workflow_status(bigint, parse.workflow_state_enum, text, bigint, text, text, jsonb); Type: FUNCTION; Schema: parse; Owner: -
--

CREATE FUNCTION parse.upsert_page_workflow_status(p_url_id bigint, p_workflow_state parse.workflow_state_enum, p_state_reason text DEFAULT NULL::text, p_linked_snapshot_id bigint DEFAULT NULL::bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_status_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(status_id bigint, url_id bigint, workflow_state parse.workflow_state_enum, state_version integer, linked_snapshot_id bigint)
    LANGUAGE plpgsql
    AS $$
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
$$;


--
-- Name: FUNCTION upsert_page_workflow_status(p_url_id bigint, p_workflow_state parse.workflow_state_enum, p_state_reason text, p_linked_snapshot_id bigint, p_source_run_id text, p_source_note text, p_status_metadata jsonb); Type: COMMENT; Schema: parse; Owner: -
--

COMMENT ON FUNCTION parse.upsert_page_workflow_status(p_url_id bigint, p_workflow_state parse.workflow_state_enum, p_state_reason text, p_linked_snapshot_id bigint, p_source_run_id text, p_source_note text, p_status_metadata jsonb) IS 'Creates or updates the parse-layer workflow state for one URL after snapshot/review transitions.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: page_evidence_snapshot; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_evidence_snapshot (
    snapshot_id bigint NOT NULL,
    url_id bigint NOT NULL,
    input_lang_code text NOT NULL,
    url_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    title_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    h1_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    breadcrumb_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    structured_data_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    anchor_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    body_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    source_run_id text,
    source_note text,
    snapshot_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_evidence_snapshot_snapshot_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_evidence_snapshot_snapshot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_evidence_snapshot_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_evidence_snapshot_snapshot_id_seq OWNED BY parse.page_evidence_snapshot.snapshot_id;


--
-- Name: page_preranking_snapshot; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_preranking_snapshot (
    snapshot_id bigint NOT NULL,
    url_id bigint NOT NULL,
    input_lang_code text NOT NULL,
    taxonomy_package_version text,
    top_candidate_count integer DEFAULT 0 NOT NULL,
    top_score numeric,
    candidate_summary jsonb DEFAULT '[]'::jsonb NOT NULL,
    review_status text DEFAULT 'pre_ranked'::text NOT NULL,
    source_run_id text,
    source_note text,
    snapshot_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_preranking_snapshot_snapshot_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_preranking_snapshot_snapshot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_preranking_snapshot_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_preranking_snapshot_snapshot_id_seq OWNED BY parse.page_preranking_snapshot.snapshot_id;


--
-- Name: page_taxonomy_candidate; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_taxonomy_candidate (
    candidate_id bigint NOT NULL,
    url_id bigint NOT NULL,
    taxonomy_source_db text DEFAULT 'logisticsearch_taxonomy'::text NOT NULL,
    taxonomy_package_version text NOT NULL,
    taxonomy_package_id uuid NOT NULL,
    taxonomy_concept_id uuid NOT NULL,
    taxonomy_node_code text NOT NULL,
    taxonomy_concept_key text NOT NULL,
    input_lang_code text NOT NULL,
    matched_lang_codes jsonb DEFAULT '[]'::jsonb NOT NULL,
    matched_fields jsonb DEFAULT '[]'::jsonb NOT NULL,
    matched_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    domain_type text,
    node_kind text,
    url_score numeric(12,4) DEFAULT 0 NOT NULL,
    title_score numeric(12,4) DEFAULT 0 NOT NULL,
    h1_score numeric(12,4) DEFAULT 0 NOT NULL,
    breadcrumb_score numeric(12,4) DEFAULT 0 NOT NULL,
    structured_data_score numeric(12,4) DEFAULT 0 NOT NULL,
    anchor_score numeric(12,4) DEFAULT 0 NOT NULL,
    body_score numeric(12,4) DEFAULT 0 NOT NULL,
    total_score numeric(12,4) DEFAULT 0 NOT NULL,
    evidence_count integer DEFAULT 0 NOT NULL,
    confidence_band text DEFAULT 'unreviewed'::text NOT NULL,
    source_run_id text,
    source_note text,
    candidate_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_taxonomy_candidate_candidate_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_taxonomy_candidate_candidate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_taxonomy_candidate_candidate_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_taxonomy_candidate_candidate_id_seq OWNED BY parse.page_taxonomy_candidate.candidate_id;


--
-- Name: page_workflow_status; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_workflow_status (
    status_id bigint NOT NULL,
    url_id bigint NOT NULL,
    linked_snapshot_id bigint,
    workflow_state parse.workflow_state_enum NOT NULL,
    state_reason text,
    state_version integer DEFAULT 1 NOT NULL,
    source_run_id text,
    source_note text,
    status_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_workflow_status_status_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_workflow_status_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_workflow_status_status_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_workflow_status_status_id_seq OWNED BY parse.page_workflow_status.status_id;


--
-- Name: page_evidence_snapshot snapshot_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot ALTER COLUMN snapshot_id SET DEFAULT nextval('parse.page_evidence_snapshot_snapshot_id_seq'::regclass);


--
-- Name: page_preranking_snapshot snapshot_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot ALTER COLUMN snapshot_id SET DEFAULT nextval('parse.page_preranking_snapshot_snapshot_id_seq'::regclass);


--
-- Name: page_taxonomy_candidate candidate_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate ALTER COLUMN candidate_id SET DEFAULT nextval('parse.page_taxonomy_candidate_candidate_id_seq'::regclass);


--
-- Name: page_workflow_status status_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status ALTER COLUMN status_id SET DEFAULT nextval('parse.page_workflow_status_status_id_seq'::regclass);


--
-- Name: page_evidence_snapshot page_evidence_snapshot_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT page_evidence_snapshot_pkey PRIMARY KEY (snapshot_id);


--
-- Name: page_preranking_snapshot page_preranking_snapshot_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT page_preranking_snapshot_pkey PRIMARY KEY (snapshot_id);


--
-- Name: page_taxonomy_candidate page_taxonomy_candidate_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT page_taxonomy_candidate_pkey PRIMARY KEY (candidate_id);


--
-- Name: page_workflow_status page_workflow_status_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_pkey PRIMARY KEY (status_id);


--
-- Name: page_evidence_snapshot parse_page_evidence_snapshot_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT parse_page_evidence_snapshot_url_uniq UNIQUE (url_id);


--
-- Name: page_preranking_snapshot parse_page_preranking_snapshot_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT parse_page_preranking_snapshot_url_uniq UNIQUE (url_id);


--
-- Name: page_taxonomy_candidate parse_page_taxonomy_candidate_url_pkg_concept_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT parse_page_taxonomy_candidate_url_pkg_concept_uniq UNIQUE (url_id, taxonomy_package_version, taxonomy_concept_id);


--
-- Name: page_workflow_status parse_page_workflow_status_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT parse_page_workflow_status_url_uniq UNIQUE (url_id);


--
-- Name: parse_page_evidence_snapshot_lang_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_evidence_snapshot_lang_idx ON parse.page_evidence_snapshot USING btree (input_lang_code);


--
-- Name: parse_page_preranking_snapshot_review_status_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_preranking_snapshot_review_status_idx ON parse.page_preranking_snapshot USING btree (review_status);


--
-- Name: parse_page_preranking_snapshot_top_score_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_preranking_snapshot_top_score_idx ON parse.page_preranking_snapshot USING btree (top_score DESC);


--
-- Name: parse_page_tax_candidate_concept_key_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_concept_key_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_concept_key);


--
-- Name: parse_page_tax_candidate_node_code_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_node_code_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_node_code);


--
-- Name: parse_page_tax_candidate_package_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_package_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_package_version, total_score DESC);


--
-- Name: parse_page_tax_candidate_url_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_url_idx ON parse.page_taxonomy_candidate USING btree (url_id, total_score DESC);


--
-- Name: parse_page_workflow_status_snapshot_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_workflow_status_snapshot_idx ON parse.page_workflow_status USING btree (linked_snapshot_id);


--
-- Name: parse_page_workflow_status_state_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_workflow_status_state_idx ON parse.page_workflow_status USING btree (workflow_state);


--
-- Name: page_evidence_snapshot page_evidence_snapshot_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT page_evidence_snapshot_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_preranking_snapshot page_preranking_snapshot_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT page_preranking_snapshot_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_taxonomy_candidate page_taxonomy_candidate_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT page_taxonomy_candidate_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_workflow_status page_workflow_status_linked_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_linked_snapshot_id_fkey FOREIGN KEY (linked_snapshot_id) REFERENCES parse.page_preranking_snapshot(snapshot_id) ON DELETE SET NULL;


--
-- Name: page_workflow_status page_workflow_status_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 3WYf7C8kCRl41tFg5MQuVhncb4Dp32Ei2yXRr7tlvueFa3YO5iEra19S3i70jg9

