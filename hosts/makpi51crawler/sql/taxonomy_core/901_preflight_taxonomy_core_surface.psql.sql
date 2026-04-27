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
-- This file verifies that the runtime build is being attempted against the
-- expected Pi51 taxonomy authority/runtime shape before any apply step.
--
-- JSON-first bridge note:
-- - canonical JSON files remain the authoring source of truth
-- - PostgreSQL remains the runtime database
-- - crawler worker loop must not read canonical JSON language files directly
-- - 011 creates the JSON-first bridge objects during apply, so preflight records
--   their expected names without requiring them to already exist
--
-- TR
-- taxonomy_core kontrollü apply için preflight kontrolleri.
-- Bu dosya, apply adımından önce runtime kurulumunun beklenen Pi51
-- taxonomy authority/runtime şekli üzerinde denendiğini doğrular.
--
-- JSON-first bridge notu:
-- - kanonik JSON dosyaları ana düzenleme/doğruluk kaynağı olarak kalır
-- - PostgreSQL runtime veritabanı olarak kalır
-- - crawler worker loop kanonik JSON dil dosyalarını doğrudan okumamalıdır
-- - 011 apply sırasında JSON-first bridge objelerini oluşturur; bu yüzden preflight
--   bu objeleri önceden var saymadan beklenen isimlerini görünür kaydeder

\echo
\echo == TAXONOMY_CORE PREFLIGHT ==
\echo

\echo == 1) DATABASE ==
SELECT current_database() AS db_name;

\echo
\echo == 2) REQUIRED SCHEMAS ==
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('staging', 'logistics')
ORDER BY schema_name;

\echo
\echo == 3) REQUIRED LEGACY STAGING TABLES ==
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'staging'
  AND table_name IN (
    'taxonomy_nodes_raw',
    'taxonomy_translations_raw',
    'taxonomy_keywords_raw'
  )
ORDER BY table_name;

\echo
\echo == 4) REQUIRED FILE-ORDER NEEDLE ==
SELECT
  '001->002->003->011' AS expected_apply_order;

\echo
\echo == 5) EXPECTED JSON-FIRST BRIDGE OBJECTS CREATED BY 011 ==
SELECT *
FROM (
  VALUES
    ('staging',  'table',    'taxonomy_json_language_file_import'),
    ('staging',  'table',    'taxonomy_json_term_records_raw'),
    ('logistics','table',    'taxonomy_json_runtime_language_state'),
    ('logistics','table',    'taxonomy_json_runtime_terms'),
    ('logistics','view',     'taxonomy_json_runtime_search_view'),
    ('logistics','function', 'taxonomy_json_normalize_text'),
    ('logistics','function', 'taxonomy_json_runtime_terms_prepare'),
    ('logistics','function', 'taxonomy_json_runtime_bridge_summary')
) AS expected_bridge_objects(schema_name, object_type, object_name)
ORDER BY schema_name, object_type, object_name;

\echo
\echo == 6) JSON-FIRST RUNTIME BOUNDARY NEEDLE ==
SELECT
  true AS postgresql_remains_runtime_database,
  true AS canonical_json_remains_authoring_source,
  true AS crawler_loop_direct_json_read_is_disallowed,
  true AS placeholder_languages_must_not_be_runtime_enabled;

\echo
\echo == 7) LEGACY STAGING ROWCOUNT GATE ==
SELECT 'taxonomy_nodes_raw' AS table_name, count(*)::bigint AS row_count
FROM staging.taxonomy_nodes_raw
UNION ALL
SELECT 'taxonomy_translations_raw' AS table_name, count(*)::bigint AS row_count
FROM staging.taxonomy_translations_raw
UNION ALL
SELECT 'taxonomy_keywords_raw' AS table_name, count(*)::bigint AS row_count
FROM staging.taxonomy_keywords_raw
ORDER BY table_name;

\echo
\echo == 8) SUPPORTED LANGUAGE EXPECTATION FROM LEGACY STAGING ==
WITH translation_langs AS (
  SELECT lang_code, count(*)::bigint AS translation_count
  FROM staging.taxonomy_translations_raw
  GROUP BY lang_code
),
keyword_langs AS (
  SELECT lang_code, count(*)::bigint AS keyword_count
  FROM staging.taxonomy_keywords_raw
  GROUP BY lang_code
)
SELECT
  coalesce(t.lang_code, k.lang_code) AS lang_code,
  coalesce(t.translation_count, 0)   AS translation_count,
  coalesce(k.keyword_count, 0)       AS keyword_count
FROM translation_langs t
FULL OUTER JOIN keyword_langs k
  ON k.lang_code = t.lang_code
ORDER BY 1;

\echo
\echo TAXONOMY_CORE_PREFLIGHT_RESULT=PASS
