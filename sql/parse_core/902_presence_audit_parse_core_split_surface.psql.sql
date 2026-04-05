-- psql-only presence audit for parse-core split surface
\set ON_ERROR_STOP on
\pset pager off
\pset format aligned

\echo '== 1) REQUIRED UPSTREAM DEPENDENCY =='
WITH expected(schema_name, table_name) AS (
  VALUES ('frontier', 'url')
)
SELECT
  e.schema_name,
  e.table_name,
  CASE WHEN EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.table_name
      AND c.relkind = 'r'
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e;

\echo
\echo '== 2) SCHEMA PRESENCE =='
WITH expected(schema_name) AS (
  VALUES ('parse')
)
SELECT
  e.schema_name,
  CASE WHEN EXISTS (
    SELECT 1 FROM pg_namespace n WHERE n.nspname = e.schema_name
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e;

\echo
\echo '== 3) ENUM TYPE PRESENCE =='
WITH expected(schema_name, type_name) AS (
  VALUES
    ('parse','workflow_state_enum')
)
SELECT
  e.schema_name,
  e.type_name,
  CASE WHEN EXISTS (
    SELECT 1
    FROM pg_type t
    JOIN pg_namespace n ON n.oid = t.typnamespace
    WHERE n.nspname = e.schema_name
      AND t.typname = e.type_name
      AND t.typtype = 'e'
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e;

\echo
\echo '== 4) TABLE PRESENCE =='
WITH expected(schema_name, table_name) AS (
  VALUES
    ('parse','page_evidence_snapshot'),
    ('parse','page_preranking_snapshot'),
    ('parse','page_taxonomy_candidate'),
    ('parse','page_workflow_status')
)
SELECT
  e.schema_name,
  e.table_name,
  CASE WHEN EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.table_name
      AND c.relkind = 'r'
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e
ORDER BY e.table_name;

\echo
\echo '== 5) FUNCTION PRESENCE =='
WITH expected(schema_name, function_name) AS (
  VALUES
    ('parse','persist_page_preranking_snapshot'),
    ('parse','persist_page_taxonomy_candidates'),
    ('parse','persist_page_taxonomy_preranking'),
    ('parse','persist_taxonomy_preranking_payload'),
    ('parse','upsert_page_evidence_snapshot'),
    ('parse','upsert_page_taxonomy_candidate'),
    ('parse','upsert_page_workflow_status')
)
SELECT
  e.schema_name,
  e.function_name,
  CASE WHEN EXISTS (
    SELECT 1
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE n.nspname = e.schema_name
      AND p.proname = e.function_name
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e
ORDER BY e.function_name;

\echo
\echo '== 6) INDEX PRESENCE =='
WITH expected(schema_name, index_name) AS (
  VALUES
    ('parse','page_evidence_snapshot_pkey'),
    ('parse','page_preranking_snapshot_pkey'),
    ('parse','page_taxonomy_candidate_pkey'),
    ('parse','page_workflow_status_pkey'),
    ('parse','parse_page_evidence_snapshot_lang_idx'),
    ('parse','parse_page_evidence_snapshot_url_uniq'),
    ('parse','parse_page_preranking_snapshot_review_status_idx'),
    ('parse','parse_page_preranking_snapshot_top_score_idx'),
    ('parse','parse_page_preranking_snapshot_url_uniq'),
    ('parse','parse_page_tax_candidate_concept_key_idx'),
    ('parse','parse_page_tax_candidate_node_code_idx'),
    ('parse','parse_page_tax_candidate_package_idx'),
    ('parse','parse_page_tax_candidate_url_idx'),
    ('parse','parse_page_taxonomy_candidate_url_pkg_concept_uniq'),
    ('parse','parse_page_workflow_status_snapshot_idx'),
    ('parse','parse_page_workflow_status_state_idx'),
    ('parse','parse_page_workflow_status_url_uniq')
)
SELECT
  e.schema_name,
  e.index_name,
  CASE WHEN EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.index_name
      AND c.relkind = 'i'
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e
ORDER BY e.index_name;

\echo
\echo '== 7) SUMMARY =='
WITH expected_dep(schema_name, table_name) AS (
  VALUES ('frontier','url')
),
expected_schema(schema_name) AS (
  VALUES ('parse')
),
expected_type(schema_name, type_name) AS (
  VALUES ('parse','workflow_state_enum')
),
expected_table(schema_name, table_name) AS (
  VALUES
    ('parse','page_evidence_snapshot'),
    ('parse','page_preranking_snapshot'),
    ('parse','page_taxonomy_candidate'),
    ('parse','page_workflow_status')
),
expected_function(schema_name, function_name) AS (
  VALUES
    ('parse','persist_page_preranking_snapshot'),
    ('parse','persist_page_taxonomy_candidates'),
    ('parse','persist_page_taxonomy_preranking'),
    ('parse','persist_taxonomy_preranking_payload'),
    ('parse','upsert_page_evidence_snapshot'),
    ('parse','upsert_page_taxonomy_candidate'),
    ('parse','upsert_page_workflow_status')
),
expected_index(schema_name, index_name) AS (
  VALUES
    ('parse','page_evidence_snapshot_pkey'),
    ('parse','page_preranking_snapshot_pkey'),
    ('parse','page_taxonomy_candidate_pkey'),
    ('parse','page_workflow_status_pkey'),
    ('parse','parse_page_evidence_snapshot_lang_idx'),
    ('parse','parse_page_evidence_snapshot_url_uniq'),
    ('parse','parse_page_preranking_snapshot_review_status_idx'),
    ('parse','parse_page_preranking_snapshot_top_score_idx'),
    ('parse','parse_page_preranking_snapshot_url_uniq'),
    ('parse','parse_page_tax_candidate_concept_key_idx'),
    ('parse','parse_page_tax_candidate_node_code_idx'),
    ('parse','parse_page_tax_candidate_package_idx'),
    ('parse','parse_page_tax_candidate_url_idx'),
    ('parse','parse_page_taxonomy_candidate_url_pkg_concept_uniq'),
    ('parse','parse_page_workflow_status_snapshot_idx'),
    ('parse','parse_page_workflow_status_state_idx'),
    ('parse','parse_page_workflow_status_url_uniq')
),
missing_checks AS (
  SELECT count(*)::int AS miss_count
  FROM expected_dep e
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.table_name
      AND c.relkind = 'r'
  )
  UNION ALL
  SELECT count(*)::int
  FROM expected_schema e
  WHERE NOT EXISTS (
    SELECT 1 FROM pg_namespace n WHERE n.nspname = e.schema_name
  )
  UNION ALL
  SELECT count(*)::int
  FROM expected_type e
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_type t
    JOIN pg_namespace n ON n.oid = t.typnamespace
    WHERE n.nspname = e.schema_name
      AND t.typname = e.type_name
      AND t.typtype = 'e'
  )
  UNION ALL
  SELECT count(*)::int
  FROM expected_table e
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.table_name
      AND c.relkind = 'r'
  )
  UNION ALL
  SELECT count(*)::int
  FROM expected_function e
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_proc p
    JOIN pg_namespace n ON n.oid = p.pronamespace
    WHERE n.nspname = e.schema_name
      AND p.proname = e.function_name
  )
  UNION ALL
  SELECT count(*)::int
  FROM expected_index e
  WHERE NOT EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = e.schema_name
      AND c.relname = e.index_name
      AND c.relkind = 'i'
  )
)
SELECT 'MISSING_CHECK_COUNT=' || sum(miss_count) FROM missing_checks;
