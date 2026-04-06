\set ON_ERROR_STOP on
\pset pager off

\echo '== DESKTOP_IMPORT PREFLIGHT =='

SELECT current_database() AS db_name;

SELECT
  n.nspname AS schema_name
FROM pg_namespace n
WHERE n.nspname = 'desktop_import';

SELECT
  c.relname AS existing_relation,
  c.relkind AS relkind
FROM pg_class c
JOIN pg_namespace n
  ON n.oid = c.relnamespace
WHERE n.nspname = 'desktop_import'
ORDER BY c.relkind, c.relname;
