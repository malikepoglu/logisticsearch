-- psql-only preflight for crawler-core split surface
\set ON_ERROR_STOP on

SELECT current_database() AS current_database;

SELECT
  e.extname,
  n.nspname AS extension_schema
FROM pg_extension e
JOIN pg_namespace n
  ON n.oid = e.extnamespace
WHERE e.extname = 'pgcrypto';

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_extension
    WHERE extname = 'pgcrypto'
  ) THEN
    RAISE EXCEPTION 'Missing required extension: pgcrypto';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_proc p
    JOIN pg_namespace n
      ON n.oid = p.pronamespace
    WHERE n.nspname = 'public'
      AND p.proname = 'digest'
  ) THEN
    RAISE EXCEPTION 'Missing required function reference: public.digest';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM pg_proc p
    WHERE p.proname = 'gen_random_uuid'
  ) THEN
    RAISE EXCEPTION 'Missing required function: gen_random_uuid';
  END IF;
END
$$;
