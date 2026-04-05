-- psql-only preflight for parse-core split surface
\set ON_ERROR_STOP on

SELECT current_database() AS current_database;

DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_namespace
    WHERE nspname = 'parse'
  ) THEN
    RAISE EXCEPTION 'Target schema already exists: parse';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_namespace
    WHERE nspname = 'frontier'
  ) THEN
    RAISE EXCEPTION 'Missing required upstream schema: frontier';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_class c
    JOIN pg_namespace n
      ON n.oid = c.relnamespace
    WHERE n.nspname = 'frontier'
      AND c.relname = 'url'
      AND c.relkind = 'r'
  ) THEN
    RAISE EXCEPTION 'Missing required upstream table: frontier.url';
  END IF;
END
$$;
