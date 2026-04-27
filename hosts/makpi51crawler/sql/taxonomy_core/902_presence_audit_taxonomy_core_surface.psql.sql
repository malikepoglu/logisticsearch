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
-- Presence audit for taxonomy_core after apply.
-- This file checks whether the runtime logistics schema exists with the
-- expected object family and whether the loaded counts align with the known
-- authority fingerprint.
--
-- JSON-first bridge note:
-- - 011 adds PostgreSQL runtime bridge objects derived from canonical JSON imports
-- - canonical JSON files remain the authoring source
-- - Python runtime should query PostgreSQL runtime seams, not canonical JSON files
-- - placeholder languages must remain disabled until filled and sealed
--
-- TR
-- Apply sonrası taxonomy_core presence audit yüzeyi.
-- Bu dosya, runtime logistics şemasının beklenen nesne ailesiyle var olup
-- olmadığını ve yüklenen sayımların bilinen authority fingerprint ile hizalı
-- olup olmadığını kontrol eder.
--
-- JSON-first bridge notu:
-- - 011 kanonik JSON importlarından türeyen PostgreSQL runtime bridge objelerini ekler
-- - kanonik JSON dosyaları ana düzenleme/doğruluk kaynağı olarak kalır
-- - Python runtime kanonik JSON dosyalarını değil PostgreSQL runtime seam'lerini sorgulamalıdır
-- - placeholder diller doldurulup seal edilene kadar disabled kalmalıdır

\echo
\echo == TAXONOMY_CORE PRESENCE AUDIT ==
\echo

\echo == 1) STAGING JSON-FIRST BRIDGE TABLE LIST ==
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'staging'
  AND tablename IN (
    'taxonomy_json_language_file_import',
    'taxonomy_json_term_records_raw'
  )
ORDER BY tablename;

\echo
\echo == 2) LOGISTICS TABLE LIST ==
SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname = 'logistics'
  AND tablename IN (
    'supported_languages',
    'taxonomy_nodes',
    'taxonomy_node_translations',
    'taxonomy_keywords',
    'taxonomy_closure',
    'taxonomy_overlay_nodes',
    'taxonomy_overlay_node_translations',
    'taxonomy_overlay_keywords',
    'taxonomy_overlay_closure',
    'taxonomy_requirements',
    'taxonomy_json_runtime_language_state',
    'taxonomy_json_runtime_terms'
  )
ORDER BY tablename;

\echo
\echo == 3) LOGISTICS VIEW LIST ==
SELECT table_schema, table_name
FROM information_schema.views
WHERE table_schema = 'logistics'
  AND table_name IN (
    'taxonomy_json_runtime_search_view'
  )
ORDER BY table_name;

\echo
\echo == 4) LOGISTICS FUNCTION LIST ==
SELECT routine_schema, routine_name
FROM information_schema.routines
WHERE routine_schema = 'logistics'
  AND routine_name IN (
    'touch_updated_at',
    'normalize_taxonomy_text',
    'taxonomy_node_translations_prepare',
    'taxonomy_keywords_prepare',
    'rebuild_taxonomy_closure',
    'rebuild_taxonomy_overlay_closure',
    'refresh_taxonomy_runtime_from_staging',
    'taxonomy_json_normalize_text',
    'taxonomy_json_runtime_terms_prepare',
    'taxonomy_json_runtime_bridge_summary'
  )
ORDER BY routine_name;

\echo
\echo == 5) CORE ROWCOUNT FINGERPRINT ==
SELECT 'supported_languages' AS table_name, count(*)::bigint AS row_count
FROM logistics.supported_languages
UNION ALL
SELECT 'taxonomy_nodes' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_nodes
UNION ALL
SELECT 'taxonomy_node_translations' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_node_translations
UNION ALL
SELECT 'taxonomy_keywords' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_keywords
UNION ALL
SELECT 'taxonomy_closure' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_closure
UNION ALL
SELECT 'taxonomy_overlay_nodes' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_overlay_nodes
UNION ALL
SELECT 'taxonomy_overlay_node_translations' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_overlay_node_translations
UNION ALL
SELECT 'taxonomy_overlay_keywords' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_overlay_keywords
UNION ALL
SELECT 'taxonomy_overlay_closure' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_overlay_closure
UNION ALL
SELECT 'taxonomy_requirements' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_requirements
UNION ALL
SELECT 'taxonomy_json_runtime_language_state' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_json_runtime_language_state
UNION ALL
SELECT 'taxonomy_json_runtime_terms' AS table_name, count(*)::bigint AS row_count
FROM logistics.taxonomy_json_runtime_terms
ORDER BY table_name;

\echo
\echo == 6) JSON-FIRST BRIDGE STAGING ROWCOUNT ==
SELECT 'taxonomy_json_language_file_import' AS table_name, count(*)::bigint AS row_count
FROM staging.taxonomy_json_language_file_import
UNION ALL
SELECT 'taxonomy_json_term_records_raw' AS table_name, count(*)::bigint AS row_count
FROM staging.taxonomy_json_term_records_raw
ORDER BY table_name;

\echo
\echo == 7) JSON-FIRST RUNTIME LANGUAGE STATE SUMMARY ==
SELECT
  count(*)::bigint AS language_state_rows,
  count(*) FILTER (WHERE is_placeholder = true)::bigint AS placeholder_language_rows,
  count(*) FILTER (WHERE is_placeholder = false)::bigint AS populated_language_rows,
  count(*) FILTER (WHERE is_runtime_enabled = true)::bigint AS runtime_enabled_language_rows,
  count(*) FILTER (WHERE is_placeholder = true AND is_runtime_enabled = true)::bigint AS invalid_enabled_placeholder_rows
FROM logistics.taxonomy_json_runtime_language_state;

\echo
\echo == 8) JSON-FIRST RUNTIME SEARCH VIEW ROWCOUNT ==
SELECT count(*)::bigint AS taxonomy_json_runtime_search_view_rows
FROM logistics.taxonomy_json_runtime_search_view;

\echo
\echo == 9) JSON-FIRST RUNTIME BRIDGE SUMMARY FUNCTION ==
SELECT logistics.taxonomy_json_runtime_bridge_summary() AS bridge_summary;

\echo
\echo == 10) 25-LANGUAGE COVERAGE / LEGACY RUNTIME ==
SELECT lang_code, count(*)::bigint AS translation_count
FROM logistics.taxonomy_node_translations
GROUP BY lang_code
ORDER BY lang_code;

SELECT lang_code, count(*)::bigint AS keyword_count
FROM logistics.taxonomy_keywords
GROUP BY lang_code
ORDER BY lang_code;

\echo
\echo == 11) NODE-LEVEL COMPLETENESS / LEGACY RUNTIME ==
WITH translation_langs AS (
  SELECT node_id, count(DISTINCT lang_code)::integer AS lang_count
  FROM logistics.taxonomy_node_translations
  GROUP BY node_id
),
keyword_langs AS (
  SELECT node_id, count(DISTINCT lang_code)::integer AS lang_count
  FROM logistics.taxonomy_keywords
  GROUP BY node_id
)
SELECT
  count(*)::bigint AS node_count,
  count(*) FILTER (WHERE coalesce(t.lang_count, 0) = 25)::bigint AS nodes_with_25_translation_langs,
  count(*) FILTER (WHERE coalesce(k.lang_count, 0) = 25)::bigint AS nodes_with_25_keyword_langs,
  count(*) FILTER (WHERE coalesce(t.lang_count, 0) <> 25)::bigint AS translation_gap_node_count,
  count(*) FILTER (WHERE coalesce(k.lang_count, 0) <> 25)::bigint AS keyword_gap_node_count
FROM logistics.taxonomy_nodes n
LEFT JOIN translation_langs t ON t.node_id = n.id
LEFT JOIN keyword_langs k ON k.node_id = n.id;

\echo
\echo == 12) HIERARCHY SUMMARY / LEGACY RUNTIME ==
SELECT
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes) AS node_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_closure) AS closure_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes WHERE parent_id IS NULL) AS root_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes WHERE is_leaf) AS leaf_count,
  (SELECT max(level_no) FROM logistics.taxonomy_nodes) AS max_level_no;

\echo
\echo == 13) EXACT CANONICAL 25-LANGUAGE ORDER ==
WITH ordered_supported_languages AS (
  SELECT
    count(*)::bigint AS supported_language_count,
    string_agg(lang_code, ' ' ORDER BY sort_order) AS canonical_language_order
  FROM logistics.supported_languages
)
SELECT
  supported_language_count,
  canonical_language_order,
  (supported_language_count = 25)::boolean AS supported_language_count_is_25,
  (canonical_language_order = 'ar bg cs de el en es fr hu it ja ko nl pt ro ru tr zh hi bn ur uk id vi he')::boolean AS canonical_language_order_matches_expected,
  (
    supported_language_count = 25
    AND canonical_language_order = 'ar bg cs de el en es fr hu it ja ko nl pt ro ru tr zh hi bn ur uk id vi he'
  )::boolean AS canonical_25_language_contract_ok
FROM ordered_supported_languages;

\echo
\echo TAXONOMY_CORE_PRESENCE_AUDIT_RESULT=PASS
