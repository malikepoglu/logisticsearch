-- EN: Canonical 25-language order for taxonomy authority and all crawler/parse
-- EN: consumers is exactly: 'ar', 'bg', 'cs', 'de', 'el', 'en', 'es', 'fr', 'hu', 'it', 'ja', 'ko', 'nl', 'pt', 'ro', 'ru', 'tr', 'zh', 'hi', 'bn', 'ur', 'uk', 'id', 'vi', 'he'.
-- EN: This surface must not define, assume, or drift into any narrower subset or
-- EN: alternative order. Canonical authority lives in 001_taxonomy_runtime_base.sql.
-- TR: Taxonomy otoritesi ve tüm crawler/parse tüketicileri için kanonik 25 dil
-- TR: sırası tam olarak şöyledir: 'ar', 'bg', 'cs', 'de', 'el', 'en', 'es', 'fr', 'hu', 'it', 'ja', 'ko', 'nl', 'pt', 'ro', 'ru', 'tr', 'zh', 'hi', 'bn', 'ur', 'uk', 'id', 'vi', 'he'.
-- TR: Bu yüzey daha dar bir alt kümeye veya alternatif bir sıraya kaymamalı ve
-- TR: böyle bir varsayım kurmamalıdır. Kanonik otorite 001_taxonomy_runtime_base.sql içindedir.

\set ON_ERROR_STOP on

-- EN
-- Preflight checks for taxonomy_core controlled apply.
-- This file verifies the expected database/schema/apply-order surface before apply.
-- It must stay non-mutating and must not depend on missing legacy staging tables.
--
-- TR
-- taxonomy_core kontrollü apply için preflight kontrolleri.
-- Bu dosya apply öncesinde beklenen database/schema/apply-order yüzeyini doğrular.
-- Mutation yapmamalı ve eksik legacy staging tablolarına doğrudan bağımlı olmamalıdır.

\echo
\echo == TAXONOMY_CORE PREFLIGHT ==
\echo

\echo == 1) DATABASE ==
SELECT current_database() AS db_name;

\echo
\echo == 2) REQUIRED SCHEMAS ==
SELECT
  expected_schema.schema_name,
  EXISTS (
    SELECT 1
    FROM information_schema.schemata s
    WHERE s.schema_name = expected_schema.schema_name
  ) AS exists_now
FROM (
  VALUES
    ('staging'),
    ('logistics')
) AS expected_schema(schema_name)
ORDER BY expected_schema.schema_name;

\echo
\echo == 3) LEGACY STAGING READINESS / DIAGNOSTIC ONLY ==
WITH expected_legacy_staging(table_name) AS (
  VALUES
    ('taxonomy_nodes_raw'),
    ('taxonomy_translations_raw'),
    ('taxonomy_keywords_raw')
),
legacy_staging_state AS (
  SELECT
    e.table_name,
    EXISTS (
      SELECT 1
      FROM information_schema.tables t
      WHERE t.table_schema = 'staging'
        AND t.table_name = e.table_name
        AND t.table_type = 'BASE TABLE'
    ) AS exists_now
  FROM expected_legacy_staging e
)
SELECT
  table_name,
  exists_now,
  CASE
    WHEN exists_now THEN 'legacy_staging_available'
    ELSE 'legacy_staging_absent_json_first_bridge_can_still_apply'
  END AS readiness_note
FROM legacy_staging_state
ORDER BY table_name;

\echo
\echo == 4) REQUIRED FILE-ORDER NEEDLE ==
SELECT
  '001->002->003->011' AS expected_apply_order;

\echo
\echo == 5) JSON-FIRST BRIDGE EXPECTED OBJECT INVENTORY / NON-MUTATING ==
WITH expected_json_bridge_objects(schema_name, object_kind, object_name) AS (
  VALUES
    ('staging',  'table',    'taxonomy_json_language_file_import'),
    ('staging',  'table',    'taxonomy_json_term_records_raw'),
    ('logistics','table',    'taxonomy_json_runtime_language_state'),
    ('logistics','table',    'taxonomy_json_runtime_terms'),
    ('logistics','view',     'taxonomy_json_runtime_search_view'),
    ('logistics','function', 'taxonomy_json_normalize_text'),
    ('logistics','function', 'taxonomy_json_runtime_terms_prepare'),
    ('logistics','function', 'taxonomy_json_runtime_bridge_summary')
)
SELECT
  schema_name,
  object_kind,
  object_name
FROM expected_json_bridge_objects
ORDER BY schema_name, object_kind, object_name;

\echo
\echo == 6) JSON-FIRST BRIDGE OBJECT VISIBILITY / SAFE BEFORE OR AFTER APPLY ==
WITH expected_json_bridge_objects(schema_name, object_kind, object_name) AS (
  VALUES
    ('staging',  'table',    'taxonomy_json_language_file_import'),
    ('staging',  'table',    'taxonomy_json_term_records_raw'),
    ('logistics','table',    'taxonomy_json_runtime_language_state'),
    ('logistics','table',    'taxonomy_json_runtime_terms'),
    ('logistics','view',     'taxonomy_json_runtime_search_view'),
    ('logistics','function', 'taxonomy_json_normalize_text'),
    ('logistics','function', 'taxonomy_json_runtime_terms_prepare'),
    ('logistics','function', 'taxonomy_json_runtime_bridge_summary')
)
SELECT
  e.schema_name,
  e.object_kind,
  e.object_name,
  CASE
    WHEN e.object_kind = 'table' THEN EXISTS (
      SELECT 1
      FROM information_schema.tables t
      WHERE t.table_schema = e.schema_name
        AND t.table_name = e.object_name
        AND t.table_type = 'BASE TABLE'
    )
    WHEN e.object_kind = 'view' THEN EXISTS (
      SELECT 1
      FROM information_schema.views v
      WHERE v.table_schema = e.schema_name
        AND v.table_name = e.object_name
    )
    WHEN e.object_kind = 'function' THEN EXISTS (
      SELECT 1
      FROM information_schema.routines r
      WHERE r.routine_schema = e.schema_name
        AND r.routine_name = e.object_name
    )
    ELSE false
  END AS exists_now,
  CASE
    WHEN e.object_kind = 'table' THEN 'safe_catalog_table_check'
    WHEN e.object_kind = 'view' THEN 'safe_catalog_view_check'
    WHEN e.object_kind = 'function' THEN 'safe_catalog_function_check'
    ELSE 'unknown_object_kind'
  END AS check_mode
FROM expected_json_bridge_objects e
ORDER BY e.schema_name, e.object_kind, e.object_name;

\echo
\echo == 7) RUNTIME BOUNDARY MARKER ==
SELECT
  true AS crawler_loop_direct_json_read_is_disallowed,
  'crawler runtime must query PostgreSQL runtime seam, not canonical JSON files directly' AS boundary_contract;

\echo
\echo == 8) 901 PREFLIGHT MODE ==
SELECT
  'json_first_bridge_safe_preflight' AS preflight_mode,
  'legacy staging tables are diagnostic only; direct legacy staging SELECTs are intentionally avoided' AS legacy_staging_policy,
  'mutation_free' AS mutation_policy;

\echo
\echo TAXONOMY_CORE_PREFLIGHT_RESULT=PASS
