-- SECTION1_WEBCRAWLER / TAXONOMY JSON-FIRST RUNTIME BRIDGE
-- File: 011_taxonomy_json_first_runtime_bridge.sql
--
-- EN:
-- This SQL file introduces the first PostgreSQL-side bridge for the
-- JSON-first canonical taxonomy model.
--
-- EN:
-- Canonical language-term authoring lives in JSON files under:
-- hosts/makpi51crawler/taxonomy/languages/
--
-- EN:
-- PostgreSQL remains the runtime database for crawler/search execution.
-- The crawler worker loop must not read canonical JSON files directly
-- during normal runtime execution.
--
-- EN:
-- This file intentionally does not delete or rewrite the legacy runtime
-- tables. The existing legacy runtime surface must remain available until
-- the JSON-first bridge is imported, audited in scratch, and promoted by
-- controlled live-swap discipline.
--
-- TR:
-- Bu SQL dosyası JSON-first kanonik taxonomy modeli için ilk PostgreSQL
-- tarafı bridge yüzeyini ekler.
--
-- TR:
-- Kanonik dil-terim düzenleme kaynağı şu dizindeki JSON dosyalarıdır:
-- hosts/makpi51crawler/taxonomy/languages/
--
-- TR:
-- PostgreSQL crawler/search çalışması için runtime veritabanı olarak kalır.
-- Crawler worker loop normal runtime sırasında kanonik JSON dosyalarını
-- doğrudan okumamalıdır.
--
-- TR:
-- Bu dosya legacy runtime tablolarını bilinçli olarak silmez veya yeniden
-- yazmaz. JSON-first bridge scratch içinde import edilip denetlenene ve
-- kontrollü live-swap disipliniyle canlıya alınana kadar mevcut legacy
-- runtime yüzeyi kullanılabilir kalmalıdır.

CREATE SCHEMA IF NOT EXISTS logistics;
CREATE SCHEMA IF NOT EXISTS staging;

CREATE OR REPLACE FUNCTION logistics.taxonomy_json_normalize_text(p_text text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT lower(regexp_replace(btrim(coalesce(p_text, '')), '\s+', ' ', 'g'));
$$;

CREATE TABLE IF NOT EXISTS staging.taxonomy_json_language_file_import (
    import_id bigserial PRIMARY KEY,
    source_file_name text NOT NULL,
    language_code text NOT NULL,
    file_sha256 text NULL,
    raw_json jsonb NOT NULL,
    is_placeholder boolean NOT NULL DEFAULT false,
    record_count bigint NOT NULL DEFAULT 0,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    CONSTRAINT chk_taxonomy_json_language_file_import_source_file_not_blank
        CHECK (btrim(source_file_name) <> ''),
    CONSTRAINT chk_taxonomy_json_language_file_import_language_not_blank
        CHECK (btrim(language_code) <> ''),
    CONSTRAINT chk_taxonomy_json_language_file_import_raw_json_array
        CHECK (jsonb_typeof(raw_json) = 'array'),
    CONSTRAINT chk_taxonomy_json_language_file_import_record_count_nonnegative
        CHECK (record_count >= 0),
    CONSTRAINT chk_taxonomy_json_language_file_import_placeholder_shape
        CHECK (
            (is_placeholder = true AND record_count = 0)
            OR
            (is_placeholder = false AND record_count > 0)
        ),
    CONSTRAINT chk_taxonomy_json_language_file_import_metadata_object
        CHECK (jsonb_typeof(metadata) = 'object')
);

CREATE TABLE IF NOT EXISTS staging.taxonomy_json_term_records_raw (
    import_id bigint NOT NULL REFERENCES staging.taxonomy_json_language_file_import(import_id) ON DELETE CASCADE,
    record_ordinal integer NOT NULL,
    term_id text NOT NULL,
    concept_id text NOT NULL,
    hierarchy_id text NOT NULL,
    unspsc_code text NULL,
    language text NOT NULL,
    term text NOT NULL,
    description text NULL,
    role text NOT NULL,
    synonyms jsonb NOT NULL DEFAULT '[]'::jsonb,
    is_searchable boolean NOT NULL DEFAULT true,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    raw_record jsonb NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT pk_taxonomy_json_term_records_raw
        PRIMARY KEY (import_id, term_id),
    CONSTRAINT uq_taxonomy_json_term_records_raw_import_ordinal
        UNIQUE (import_id, record_ordinal),
    CONSTRAINT chk_taxonomy_json_term_records_raw_record_ordinal_positive
        CHECK (record_ordinal >= 1),
    CONSTRAINT chk_taxonomy_json_term_records_raw_term_id_not_blank
        CHECK (btrim(term_id) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_concept_id_not_blank
        CHECK (btrim(concept_id) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_hierarchy_id_not_blank
        CHECK (btrim(hierarchy_id) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_language_not_blank
        CHECK (btrim(language) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_term_not_blank
        CHECK (btrim(term) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_role_not_blank
        CHECK (btrim(role) <> ''),
    CONSTRAINT chk_taxonomy_json_term_records_raw_synonyms_array
        CHECK (jsonb_typeof(synonyms) = 'array'),
    CONSTRAINT chk_taxonomy_json_term_records_raw_attributes_object
        CHECK (jsonb_typeof(attributes) = 'object'),
    CONSTRAINT chk_taxonomy_json_term_records_raw_raw_record_object
        CHECK (jsonb_typeof(raw_record) = 'object')
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_json_runtime_language_state (
    language_code text PRIMARY KEY,
    source_file_name text NOT NULL,
    file_sha256 text NULL,
    is_placeholder boolean NOT NULL DEFAULT false,
    is_runtime_enabled boolean NOT NULL DEFAULT false,
    record_count bigint NOT NULL DEFAULT 0,
    imported_at timestamptz NOT NULL DEFAULT now(),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    CONSTRAINT chk_taxonomy_json_runtime_language_state_language_not_blank
        CHECK (btrim(language_code) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_language_state_source_file_not_blank
        CHECK (btrim(source_file_name) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_language_state_record_count_nonnegative
        CHECK (record_count >= 0),
    CONSTRAINT chk_taxonomy_json_runtime_language_state_placeholder_disabled
        CHECK (
            (is_placeholder = true AND record_count = 0 AND is_runtime_enabled = false)
            OR
            (is_placeholder = false AND record_count > 0)
        ),
    CONSTRAINT chk_taxonomy_json_runtime_language_state_metadata_object
        CHECK (jsonb_typeof(metadata) = 'object')
);

CREATE TABLE IF NOT EXISTS logistics.taxonomy_json_runtime_terms (
    term_id text PRIMARY KEY,
    concept_id text NOT NULL,
    hierarchy_id text NOT NULL,
    unspsc_code text NULL,
    language text NOT NULL REFERENCES logistics.taxonomy_json_runtime_language_state(language_code) ON DELETE RESTRICT,
    term text NOT NULL,
    term_normalized text NOT NULL,
    description text NULL,
    role text NOT NULL,
    synonyms jsonb NOT NULL DEFAULT '[]'::jsonb,
    is_searchable boolean NOT NULL DEFAULT true,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    source_file_name text NOT NULL,
    source_file_sha256 text NULL,
    source_record_ordinal integer NOT NULL,
    imported_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_taxonomy_json_runtime_terms_language_hierarchy_role_term
        UNIQUE (language, hierarchy_id, role, term_normalized),
    CONSTRAINT chk_taxonomy_json_runtime_terms_term_id_not_blank
        CHECK (btrim(term_id) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_concept_id_not_blank
        CHECK (btrim(concept_id) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_hierarchy_id_not_blank
        CHECK (btrim(hierarchy_id) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_language_not_blank
        CHECK (btrim(language) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_term_not_blank
        CHECK (btrim(term) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_term_normalized_not_blank
        CHECK (btrim(term_normalized) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_role_not_blank
        CHECK (btrim(role) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_synonyms_array
        CHECK (jsonb_typeof(synonyms) = 'array'),
    CONSTRAINT chk_taxonomy_json_runtime_terms_attributes_object
        CHECK (jsonb_typeof(attributes) = 'object'),
    CONSTRAINT chk_taxonomy_json_runtime_terms_source_file_not_blank
        CHECK (btrim(source_file_name) <> ''),
    CONSTRAINT chk_taxonomy_json_runtime_terms_source_record_ordinal_positive
        CHECK (source_record_ordinal >= 1)
);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_terms_concept_id
    ON logistics.taxonomy_json_runtime_terms (concept_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_terms_hierarchy_id
    ON logistics.taxonomy_json_runtime_terms (hierarchy_id);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_terms_language
    ON logistics.taxonomy_json_runtime_terms (language);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_terms_term_normalized
    ON logistics.taxonomy_json_runtime_terms (term_normalized);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_terms_is_searchable
    ON logistics.taxonomy_json_runtime_terms (is_searchable);

CREATE INDEX IF NOT EXISTS idx_taxonomy_json_runtime_language_state_runtime_enabled
    ON logistics.taxonomy_json_runtime_language_state (is_runtime_enabled, is_placeholder);

CREATE OR REPLACE VIEW logistics.taxonomy_json_runtime_search_view AS
SELECT
    t.term_id,
    t.concept_id,
    t.hierarchy_id,
    t.hierarchy_id AS node_code,
    NULL::bigint AS node_id,
    t.unspsc_code,
    t.language AS lang_code,
    t.language,
    t.term,
    t.description,
    t.role,
    t.synonyms,
    t.is_searchable,
    t.attributes,
    t.term_normalized,
    'json_term'::text AS matched_surface,
    t.term AS matched_text,
    t.source_file_name,
    t.source_file_sha256,
    t.source_record_ordinal,
    s.is_placeholder,
    s.is_runtime_enabled
FROM logistics.taxonomy_json_runtime_terms AS t
JOIN logistics.taxonomy_json_runtime_language_state AS s
  ON s.language_code = t.language
WHERE t.is_searchable = true
  AND s.is_placeholder = false
  AND s.is_runtime_enabled = true;

CREATE OR REPLACE FUNCTION logistics.taxonomy_json_runtime_terms_prepare()
RETURNS bigint
LANGUAGE plpgsql
AS $$
DECLARE
    v_updated_count bigint := 0;
BEGIN
    UPDATE logistics.taxonomy_json_runtime_terms AS t
       SET term_normalized = logistics.taxonomy_json_normalize_text(t.term)
     WHERE t.term_normalized IS DISTINCT FROM logistics.taxonomy_json_normalize_text(t.term);

    GET DIAGNOSTICS v_updated_count = ROW_COUNT;

    RETURN v_updated_count;
END;
$$;

CREATE OR REPLACE FUNCTION logistics.taxonomy_json_runtime_bridge_summary()
RETURNS jsonb
LANGUAGE sql
STABLE
AS $$
    SELECT jsonb_build_object(
        'language_state_rows',
        (SELECT count(*)::bigint FROM logistics.taxonomy_json_runtime_language_state),
        'runtime_enabled_languages',
        (
            SELECT count(*)::bigint
            FROM logistics.taxonomy_json_runtime_language_state
            WHERE is_runtime_enabled = true
              AND is_placeholder = false
        ),
        'placeholder_languages',
        (
            SELECT count(*)::bigint
            FROM logistics.taxonomy_json_runtime_language_state
            WHERE is_placeholder = true
        ),
        'runtime_term_rows',
        (SELECT count(*)::bigint FROM logistics.taxonomy_json_runtime_terms),
        'searchable_runtime_term_rows',
        (
            SELECT count(*)::bigint
            FROM logistics.taxonomy_json_runtime_terms
            WHERE is_searchable = true
        ),
        'search_view_rows',
        (SELECT count(*)::bigint FROM logistics.taxonomy_json_runtime_search_view)
    );
$$;
