\set ON_ERROR_STOP on
\pset pager off

\echo '== DESKTOP_IMPORT PRESENCE AUDIT =='

SELECT
  'schemas' AS object_family,
  count(*)::int AS object_count
FROM pg_namespace
WHERE nspname = 'desktop_import'

UNION ALL

SELECT
  'tables' AS object_family,
  count(*)::int AS object_count
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'r'

UNION ALL

SELECT
  'sequences' AS object_family,
  count(*)::int AS object_count
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'S'

UNION ALL

SELECT
  'indexes' AS object_family,
  count(*)::int AS object_count
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'i'
ORDER BY 1;

\echo ''
\echo '== TABLE LIST =='
SELECT c.relname AS table_name
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'r'
ORDER BY 1;

\echo ''
\echo '== SEQUENCE LIST =='
SELECT c.relname AS sequence_name
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'S'
ORDER BY 1;

\echo ''
\echo '== INDEX LIST =='
SELECT c.relname AS index_name
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
  AND c.relkind = 'i'
ORDER BY 1;
