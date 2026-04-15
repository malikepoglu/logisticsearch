\set ON_ERROR_STOP on

-- EN
-- Preflight checks for taxonomy_core controlled apply.
-- This file verifies that the runtime build is being attempted against the
-- expected Pi51 taxonomy authority/runtime shape before any apply step.
--
-- TR
-- taxonomy_core kontrollü apply için preflight kontrolleri.
-- Bu dosya, apply adımından önce runtime kurulumunun beklenen Pi51
-- taxonomy authority/runtime şekli üzerinde denendiğini doğrular.

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
\echo == 3) REQUIRED STAGING TABLES ==
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
  '001->002->003' AS expected_apply_order;

\echo
\echo == 5) STAGING ROWCOUNT GATE ==
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
\echo == 6) SUPPORTED LANGUAGE EXPECTATION FROM STAGING ==
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
