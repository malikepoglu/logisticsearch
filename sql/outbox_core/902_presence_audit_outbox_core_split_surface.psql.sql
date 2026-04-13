-- psql-only presence audit for outbox-core split surface
\set ON_ERROR_STOP on
\pset pager off
\pset format aligned

\echo '== 1) REQUIRED UPSTREAM DEPENDENCY =='
WITH expected(schema_name, table_name) AS (
  VALUES
    ('frontier', 'url'),
    ('parse', 'page_preranking_snapshot'),
    ('parse', 'page_workflow_status')
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
ORDER BY e.schema_name, e.table_name;

\echo
\echo '== 2) SCHEMA PRESENCE =='
WITH expected(schema_name) AS (
  VALUES ('outbox')
)
SELECT
  e.schema_name,
  CASE WHEN EXISTS (
    SELECT 1 FROM pg_namespace n WHERE n.nspname = e.schema_name
  ) THEN 'OK' ELSE 'MISSING' END AS status
FROM expected e
ORDER BY e.schema_name;

\echo
\echo '== 3) ENUM TYPE PRESENCE =='
WITH expected(schema_name, type_name) AS (
  VALUES
    ('outbox','batch_state_enum'),
    ('outbox','export_state_enum')
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
FROM expected e
ORDER BY e.schema_name, e.type_name;

\echo
\echo '== 4) TABLE PRESENCE =='
WITH expected(schema_name, table_name) AS (
  VALUES
    ('outbox','export_batch'),
    ('outbox','export_batch_item'),
    ('outbox','page_export_item')
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
ORDER BY e.schema_name, e.table_name;

\echo
\echo '== 5) FUNCTION PRESENCE =='
WITH expected(schema_name, function_name) AS (
  VALUES
    ('outbox','attach_export_item_to_batch'),
    ('outbox','create_export_batch'),
    ('outbox','enqueue_page_export_item'),
    ('outbox','mark_export_batch_failed'),
    ('outbox','mark_export_batch_pushed'),
    ('outbox','mark_export_items_pushed_by_batch'),
    ('outbox','requeue_export_items_by_batch')
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
ORDER BY e.schema_name, e.function_name;

\echo
\echo '== 6) INDEX PRESENCE =='
WITH expected(schema_name, index_name) AS (
  VALUES
    ('outbox','export_batch_item_pkey'),
    ('outbox','export_batch_pkey'),
    ('outbox','outbox_export_batch_batch_key_uniq'),
    ('outbox','outbox_export_batch_item_batch_idx'),
    ('outbox','outbox_export_batch_item_export_item_uniq'),
    ('outbox','outbox_export_batch_state_idx'),
    ('outbox','outbox_page_export_item_payload_sha_idx'),
    ('outbox','outbox_page_export_item_state_idx'),
    ('outbox','outbox_page_export_item_url_channel_snapshot_uniq'),
    ('outbox','page_export_item_pkey')
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
ORDER BY e.schema_name, e.index_name;

\echo
\echo '== 7) SUMMARY =='
WITH expected_upstream(schema_name, table_name) AS (
  VALUES
    ('frontier', 'url'),
    ('parse', 'page_preranking_snapshot'),
    ('parse', 'page_workflow_status')
),
expected_schema(schema_name) AS (
  VALUES ('outbox')
),
expected_type(schema_name, type_name) AS (
  VALUES
    ('outbox','batch_state_enum'),
    ('outbox','export_state_enum')
),
expected_table(schema_name, table_name) AS (
  VALUES
    ('outbox','export_batch'),
    ('outbox','export_batch_item'),
    ('outbox','page_export_item')
),
expected_function(schema_name, function_name) AS (
  VALUES
    ('outbox','attach_export_item_to_batch'),
    ('outbox','create_export_batch'),
    ('outbox','enqueue_page_export_item'),
    ('outbox','mark_export_batch_failed'),
    ('outbox','mark_export_batch_pushed'),
    ('outbox','mark_export_items_pushed_by_batch'),
    ('outbox','requeue_export_items_by_batch')
),
expected_index(schema_name, index_name) AS (
  VALUES
    ('outbox','export_batch_item_pkey'),
    ('outbox','export_batch_pkey'),
    ('outbox','outbox_export_batch_batch_key_uniq'),
    ('outbox','outbox_export_batch_item_batch_idx'),
    ('outbox','outbox_export_batch_item_export_item_uniq'),
    ('outbox','outbox_export_batch_state_idx'),
    ('outbox','outbox_page_export_item_payload_sha_idx'),
    ('outbox','outbox_page_export_item_state_idx'),
    ('outbox','outbox_page_export_item_url_channel_snapshot_uniq'),
    ('outbox','page_export_item_pkey')
),
missing_checks AS (
  SELECT count(*)::int AS miss_count
  FROM expected_upstream e
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
