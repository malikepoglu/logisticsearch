\set ON_ERROR_STOP on

-- EN
-- Controlled scratch bootstrap helper for crawler_core.
-- This file intentionally bootstraps one minimal source + seed + host + frontier entrypoint row.
-- It exists because seed rows alone do not automatically create claimable frontier work.
-- Current scope is explicit scratch/test bootstrap only.
--
-- TR
-- crawler_core için kontrollü scratch bootstrap yardımcı dosyası.
-- Bu dosya bilerek bir minimal source + seed + host + frontier entrypoint satırı bootstrap eder.
-- seed satırları tek başına claim edilebilir frontier işi üretmediği için bu dosya vardır.
-- Güncel kapsam yalnızca açık scratch/test bootstrap kapsamıdır.

\echo
\echo == CRAWLER CORE CONTROLLED SEED+FRONTIER ENTRYPOINT BOOTSTRAP ==
\echo

-- EN: Edit only these values when you deliberately want a different bootstrap entrypoint.
-- TR: Bilerek farklı bir bootstrap entrypoint istiyorsan yalnızca bu değerleri değiştir.

\set bootstrap_source_code 'manual_demo_example'
\set bootstrap_source_name 'Manual Demo Example'
\set bootstrap_homepage_url 'https://example.com/'
\set bootstrap_source_category 'manual_test'
\set bootstrap_default_priority '100'
\set bootstrap_default_recrawl_interval '7 days'
\set bootstrap_default_max_depth '2'
\set bootstrap_source_notes 'Controlled scratch bootstrap source for crawler_core test path.'

\set bootstrap_seed_type 'entrypoint'
\set bootstrap_submitted_url 'https://example.com/'
\set bootstrap_canonical_url 'https://example.com/'
\set bootstrap_is_enabled 'true'
\set bootstrap_priority '100'
\set bootstrap_max_depth '2'
\set bootstrap_recrawl_interval '7 days'
\set bootstrap_seed_notes 'Controlled scratch bootstrap seed entrypoint.'

\set bootstrap_scheme 'https'
\set bootstrap_host 'example.com'
\set bootstrap_port '443'
\set bootstrap_url_path '/'
\set bootstrap_url_query ''
\set bootstrap_user_agent_token 'LogisticSearchBot'
\set bootstrap_host_notes 'Controlled scratch bootstrap host.'
\set bootstrap_url_notes 'Controlled scratch bootstrap frontier entrypoint.'
\set bootstrap_enqueue_reason 'manual_seed_bootstrap'

\echo == 1) UPSERT seed.source ==

WITH upsert_source AS (
  INSERT INTO seed.source (
    source_code,
    source_name,
    homepage_url,
    source_category,
    default_priority,
    default_recrawl_interval,
    default_max_depth,
    notes
  )
  VALUES (
    :'bootstrap_source_code',
    :'bootstrap_source_name',
    :'bootstrap_homepage_url',
    :'bootstrap_source_category',
    :'bootstrap_default_priority'::integer,
    :'bootstrap_default_recrawl_interval'::interval,
    :'bootstrap_default_max_depth'::integer,
    :'bootstrap_source_notes'
  )
  ON CONFLICT (source_code) DO UPDATE
  SET source_name = EXCLUDED.source_name,
      homepage_url = EXCLUDED.homepage_url,
      source_category = EXCLUDED.source_category,
      default_priority = EXCLUDED.default_priority,
      default_recrawl_interval = EXCLUDED.default_recrawl_interval,
      default_max_depth = EXCLUDED.default_max_depth,
      notes = EXCLUDED.notes,
      updated_at = now()
  RETURNING source_id
)
SELECT source_id AS bootstrap_source_id
FROM upsert_source
\gset

\echo == 2) UPSERT seed.seed_url ==

WITH upsert_seed AS (
  INSERT INTO seed.seed_url (
    source_id,
    seed_type,
    submitted_url,
    canonical_url,
    is_enabled,
    priority,
    max_depth,
    recrawl_interval,
    next_discover_at,
    seed_metadata,
    notes
  )
  VALUES (
    :'bootstrap_source_id'::uuid,
    :'bootstrap_seed_type'::seed.seed_type_enum,
    :'bootstrap_submitted_url',
    :'bootstrap_canonical_url',
    :'bootstrap_is_enabled'::boolean,
    :'bootstrap_priority'::integer,
    :'bootstrap_max_depth'::integer,
    :'bootstrap_recrawl_interval'::interval,
    now(),
    '{}'::jsonb,
    :'bootstrap_seed_notes'
  )
  ON CONFLICT (source_id, canonical_url_sha256) DO UPDATE
  SET seed_type = EXCLUDED.seed_type,
      submitted_url = EXCLUDED.submitted_url,
      canonical_url = EXCLUDED.canonical_url,
      is_enabled = EXCLUDED.is_enabled,
      priority = EXCLUDED.priority,
      max_depth = EXCLUDED.max_depth,
      recrawl_interval = EXCLUDED.recrawl_interval,
      next_discover_at = now(),
      seed_metadata = EXCLUDED.seed_metadata,
      notes = EXCLUDED.notes,
      updated_at = now()
  RETURNING seed_id
)
SELECT seed_id AS bootstrap_seed_id
FROM upsert_seed
\gset

\echo == 3) UPSERT frontier.host ==

WITH upsert_host AS (
  INSERT INTO frontier.host (
    scheme,
    host,
    port,
    user_agent_token,
    notes
  )
  VALUES (
    :'bootstrap_scheme',
    :'bootstrap_host',
    :'bootstrap_port'::integer,
    :'bootstrap_user_agent_token',
    :'bootstrap_host_notes'
  )
  ON CONFLICT (authority_key) DO UPDATE
  SET user_agent_token = EXCLUDED.user_agent_token,
      notes = EXCLUDED.notes,
      updated_at = now()
  RETURNING host_id
)
SELECT host_id AS bootstrap_host_id
FROM upsert_host
\gset

\echo == 4) UPSERT frontier.url ==

WITH upsert_url AS (
  INSERT INTO frontier.url (
    host_id,
    canonical_url,
    url_path,
    url_query,
    source_id,
    seed_id,
    discovery_type,
    depth,
    is_seed,
    state,
    priority,
    enqueue_reason,
    next_fetch_at,
    url_metadata,
    notes
  )
  VALUES (
    :'bootstrap_host_id'::bigint,
    :'bootstrap_canonical_url',
    :'bootstrap_url_path',
    nullif(:'bootstrap_url_query', ''),
    :'bootstrap_source_id'::uuid,
    :'bootstrap_seed_id'::uuid,
    'seed'::frontier.discovery_type_enum,
    0,
    true,
    'queued'::frontier.url_state_enum,
    :'bootstrap_priority'::integer,
    :'bootstrap_enqueue_reason',
    now(),
    '{}'::jsonb,
    :'bootstrap_url_notes'
  )
  ON CONFLICT (canonical_url_sha256) DO UPDATE
  SET host_id = EXCLUDED.host_id,
      source_id = EXCLUDED.source_id,
      seed_id = EXCLUDED.seed_id,
      discovery_type = 'seed'::frontier.discovery_type_enum,
      depth = 0,
      is_seed = true,
      state = 'queued'::frontier.url_state_enum,
      priority = EXCLUDED.priority,
      enqueue_reason = EXCLUDED.enqueue_reason,
      next_fetch_at = now(),
      revisit_not_before = null,
      lease_token = null,
      lease_owner = null,
      lease_acquired_at = null,
      lease_expires_at = null,
      fetch_attempt_count = 0,
      success_count = 0,
      retryable_error_count = 0,
      permanent_error_count = 0,
      redirect_count = 0,
      consecutive_error_count = 0,
      last_fetch_started_at = null,
      last_fetch_finished_at = null,
      last_success_at = null,
      last_http_status = null,
      last_content_type = null,
      last_body_bytes = null,
      last_etag = null,
      last_last_modified = null,
      last_outcome = null,
      last_error_class = null,
      last_error_message = null,
      url_metadata = EXCLUDED.url_metadata,
      notes = EXCLUDED.notes,
      updated_at = now()
  RETURNING url_id
)
SELECT url_id AS bootstrap_url_id
FROM upsert_url
\gset

\echo == 5) BOOTSTRAP SUMMARY ==

SELECT
  :'bootstrap_source_id'::uuid   AS source_id,
  :'bootstrap_seed_id'::uuid     AS seed_id,
  :'bootstrap_host_id'::bigint   AS host_id,
  :'bootstrap_url_id'::bigint    AS url_id;

\echo == 6) TARGETED ROW SNAPSHOT / seed.source ==

SELECT
  source_id,
  source_code,
  source_name,
  source_status,
  homepage_url,
  default_priority,
  default_recrawl_interval,
  default_max_depth
FROM seed.source
WHERE source_id = :'bootstrap_source_id'::uuid;

\echo == 7) TARGETED ROW SNAPSHOT / seed.seed_url ==

SELECT
  seed_id,
  source_id,
  seed_type,
  submitted_url,
  canonical_url,
  is_enabled,
  priority,
  max_depth,
  recrawl_interval,
  next_discover_at
FROM seed.seed_url
WHERE seed_id = :'bootstrap_seed_id'::uuid;

\echo == 8) TARGETED ROW SNAPSHOT / frontier.url ==

SELECT
  url_id,
  host_id,
  canonical_url,
  source_id,
  seed_id,
  discovery_type,
  depth,
  is_seed,
  state,
  priority,
  next_fetch_at,
  lease_owner,
  lease_expires_at
FROM frontier.url
WHERE url_id = :'bootstrap_url_id'::bigint;

\echo == 9) CLAIMABLE WORK PROOF (NO CLAIM EXECUTED) ==

SELECT
  count(*)::bigint AS claimable_url_count
FROM frontier.url
WHERE url_id = :'bootstrap_url_id'::bigint
  AND state IN ('queued', 'retry_wait');

\echo
\echo BOOTSTRAP_RESULT=PASS
