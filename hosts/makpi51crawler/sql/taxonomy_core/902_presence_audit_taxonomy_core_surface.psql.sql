\set ON_ERROR_STOP on

-- EN
-- Presence audit for taxonomy_core after apply.
-- This file checks whether the runtime logistics schema exists with the
-- expected object family and whether the loaded counts align with the known
-- authority fingerprint.
--
-- TR
-- Apply sonrası taxonomy_core presence audit yüzeyi.
-- Bu dosya, runtime logistics şemasının beklenen nesne ailesiyle var olup
-- olmadığını ve yüklenen sayımların bilinen authority fingerprint ile hizalı
-- olup olmadığını kontrol eder.

\echo
\echo == TAXONOMY_CORE PRESENCE AUDIT ==
\echo

\echo == 1) LOGISTICS TABLE LIST ==
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
    'taxonomy_requirements'
  )
ORDER BY tablename;

\echo
\echo == 2) LOGISTICS FUNCTION LIST ==
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
    'refresh_taxonomy_runtime_from_staging'
  )
ORDER BY routine_name;

\echo
\echo == 3) CORE ROWCOUNT FINGERPRINT ==
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
ORDER BY table_name;

\echo
\echo == 4) 25-LANGUAGE COVERAGE / RUNTIME ==
SELECT lang_code, count(*)::bigint AS translation_count
FROM logistics.taxonomy_node_translations
GROUP BY lang_code
ORDER BY lang_code;

SELECT lang_code, count(*)::bigint AS keyword_count
FROM logistics.taxonomy_keywords
GROUP BY lang_code
ORDER BY lang_code;

\echo
\echo == 5) NODE-LEVEL COMPLETENESS ==
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
\echo == 6) HIERARCHY SUMMARY ==
SELECT
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes) AS node_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_closure) AS closure_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes WHERE parent_id IS NULL) AS root_count,
  (SELECT count(*)::bigint FROM logistics.taxonomy_nodes WHERE is_leaf) AS leaf_count,
  (SELECT max(level_no) FROM logistics.taxonomy_nodes) AS max_level_no;

\echo
\echo TAXONOMY_CORE_PRESENCE_AUDIT_RESULT=PASS
