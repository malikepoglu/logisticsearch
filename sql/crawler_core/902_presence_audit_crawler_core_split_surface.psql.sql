-- psql-only presence audit for crawler-core split surface
\set ON_ERROR_STOP on
\pset pager off
\pset format aligned

\echo '== 1) EXTENSION / PREREQUISITE PRESENCE =='
WITH expected(kind, schema_name, object_name) AS (
  VALUES
    ('extension', 'public', 'pgcrypto'),
    ('function',  'public', 'digest'),
    ('function',  '',       'gen_random_uuid')
)
SELECT
  e.kind,
  e.schema_name,
  e.object_name,
  CASE
    WHEN e.kind = 'extension' AND EXISTS (
      SELECT 1
      FROM pg_extension x
      JOIN pg_namespace n ON n.oid = x.extnamespace
      WHERE x.extname = e.object_name
        AND n.nspname = e.schema_name
    ) THEN 'OK'
    WHEN e.kind = 'function' AND e.schema_name <> '' AND EXISTS (
      SELECT 1
      FROM pg_proc p
      JOIN pg_namespace n ON n.oid = p.pronamespace
      WHERE p.proname = e.object_name
        AND n.nspname = e.schema_name
    ) THEN 'OK'
    WHEN e.kind = 'function' AND e.schema_name = '' AND EXISTS (
      SELECT 1
      FROM pg_proc p
      WHERE p.proname = e.object_name
    ) THEN 'OK'
    ELSE 'MISSING'
  END AS status
FROM expected e
ORDER BY 1,2,3;

\echo
\echo '== 2) SCHEMA PRESENCE =='
WITH expected(schema_name) AS (
  VALUES ('seed'), ('frontier'), ('http_fetch')
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
    ('frontier','discovery_type_enum'),
    ('frontier','host_status_enum'),
    ('frontier','robots_mode_enum'),
    ('frontier','url_state_enum'),
    ('http_fetch','fetch_kind_enum'),
    ('http_fetch','fetch_outcome_enum'),
    ('http_fetch','robots_cache_state_enum'),
    ('http_fetch','robots_verdict_enum'),
    ('seed','seed_type_enum'),
    ('seed','source_status_enum')
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
    ('frontier','host'),
    ('frontier','url'),
    ('http_fetch','fetch_attempt'),
    ('http_fetch','robots_txt_cache'),
    ('seed','seed_url'),
    ('seed','source')
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
    ('frontier','claim_next_url'),
    ('frontier','reap_expired_leases'),
    ('frontier','finish_fetch_success'),
    ('frontier','finish_fetch_retryable_error'),
    ('frontier','finish_fetch_permanent_error'),
    ('frontier','compute_retry_backoff'),
    ('frontier','compute_success_next_fetch_at'),
    ('http_fetch','upsert_robots_txt_cache'),
    ('http_fetch','compute_robots_refresh_decision'),
    ('http_fetch','compute_robots_allow_decision')
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
    ('frontier','frontier_host_pause_idx'),
    ('frontier','frontier_host_sched_idx'),
    ('frontier','frontier_url_due_idx'),
    ('frontier','frontier_url_host_due_idx'),
    ('frontier','frontier_url_lease_expiry_idx'),
    ('frontier','frontier_url_parent_idx'),
    ('frontier','frontier_url_parse_pending_idx'),
    ('http_fetch','fetch_attempt_host_time_idx'),
    ('http_fetch','fetch_attempt_open_idx'),
    ('http_fetch','fetch_attempt_url_time_idx'),
    ('http_fetch','robots_cache_expiry_idx'),
    ('seed','seed_seed_url_due_idx')
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
WITH expected_schema(schema_name) AS (
  VALUES ('seed'), ('frontier'), ('http_fetch')
),
expected_type(schema_name, type_name) AS (
  VALUES
    ('frontier','discovery_type_enum'),
    ('frontier','host_status_enum'),
    ('frontier','robots_mode_enum'),
    ('frontier','url_state_enum'),
    ('http_fetch','fetch_kind_enum'),
    ('http_fetch','fetch_outcome_enum'),
    ('http_fetch','robots_cache_state_enum'),
    ('http_fetch','robots_verdict_enum'),
    ('seed','seed_type_enum'),
    ('seed','source_status_enum')
),
expected_table(schema_name, table_name) AS (
  VALUES
    ('frontier','host'),
    ('frontier','url'),
    ('http_fetch','fetch_attempt'),
    ('http_fetch','robots_txt_cache'),
    ('seed','seed_url'),
    ('seed','source')
),
expected_function(schema_name, function_name) AS (
  VALUES
    ('frontier','claim_next_url'),
    ('frontier','reap_expired_leases'),
    ('frontier','finish_fetch_success'),
    ('frontier','finish_fetch_retryable_error'),
    ('frontier','finish_fetch_permanent_error'),
    ('frontier','compute_retry_backoff'),
    ('frontier','compute_success_next_fetch_at'),
    ('http_fetch','upsert_robots_txt_cache'),
    ('http_fetch','compute_robots_refresh_decision'),
    ('http_fetch','compute_robots_allow_decision')
),
expected_index(schema_name, index_name) AS (
  VALUES
    ('frontier','frontier_host_pause_idx'),
    ('frontier','frontier_host_sched_idx'),
    ('frontier','frontier_url_due_idx'),
    ('frontier','frontier_url_host_due_idx'),
    ('frontier','frontier_url_lease_expiry_idx'),
    ('frontier','frontier_url_parent_idx'),
    ('frontier','frontier_url_parse_pending_idx'),
    ('http_fetch','fetch_attempt_host_time_idx'),
    ('http_fetch','fetch_attempt_open_idx'),
    ('http_fetch','fetch_attempt_url_time_idx'),
    ('http_fetch','robots_cache_expiry_idx'),
    ('seed','seed_seed_url_due_idx')
),
missing_checks AS (
  SELECT count(*)::int AS miss_count
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
