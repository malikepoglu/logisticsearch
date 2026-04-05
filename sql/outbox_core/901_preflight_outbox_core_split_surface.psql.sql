-- psql-only preflight for outbox-core split surface
\set ON_ERROR_STOP on

SELECT current_database() AS current_database;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_namespace n
    JOIN pg_class c
      ON c.relnamespace = n.oid
    WHERE n.nspname = 'frontier'
      AND c.relname = 'url'
      AND c.relkind = 'r'
  ) THEN
    RAISE EXCEPTION 'Missing required upstream table: frontier.url';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_namespace n
    JOIN pg_class c
      ON c.relnamespace = n.oid
    WHERE n.nspname = 'parse'
      AND c.relname = 'page_preranking_snapshot'
      AND c.relkind = 'r'
  ) THEN
    RAISE EXCEPTION 'Missing required upstream table: parse.page_preranking_snapshot';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_namespace n
    JOIN pg_class c
      ON c.relnamespace = n.oid
    WHERE n.nspname = 'parse'
      AND c.relname = 'page_workflow_status'
      AND c.relkind = 'r'
  ) THEN
    RAISE EXCEPTION 'Missing required upstream table: parse.page_workflow_status';
  END IF;
END
$$;
