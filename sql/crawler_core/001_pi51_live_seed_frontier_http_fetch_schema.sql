--
-- PostgreSQL database dump
--

\restrict dPwpDYLZXzFXQHl3ZcNRHh2GJU9t6i6006peqzeYIfaaugeNf7pDJwoPOh4n6CU

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: frontier; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA frontier;


--
-- Name: http_fetch; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA http_fetch;


--
-- Name: seed; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA seed;


--
-- Name: discovery_type_enum; Type: TYPE; Schema: frontier; Owner: -
--

CREATE TYPE frontier.discovery_type_enum AS ENUM (
    'seed',
    'sitemap',
    'html_link',
    'redirect',
    'manual',
    'revisit'
);


--
-- Name: host_status_enum; Type: TYPE; Schema: frontier; Owner: -
--

CREATE TYPE frontier.host_status_enum AS ENUM (
    'active',
    'paused',
    'blocked',
    'retired'
);


--
-- Name: robots_mode_enum; Type: TYPE; Schema: frontier; Owner: -
--

CREATE TYPE frontier.robots_mode_enum AS ENUM (
    'respect',
    'ignore',
    'manual_override'
);


--
-- Name: url_state_enum; Type: TYPE; Schema: frontier; Owner: -
--

CREATE TYPE frontier.url_state_enum AS ENUM (
    'queued',
    'leased',
    'fetched',
    'parse_pending',
    'parsed',
    'retry_wait',
    'blocked_robots',
    'dead',
    'paused'
);


--
-- Name: fetch_kind_enum; Type: TYPE; Schema: http_fetch; Owner: -
--

CREATE TYPE http_fetch.fetch_kind_enum AS ENUM (
    'page',
    'robots',
    'sitemap'
);


--
-- Name: fetch_outcome_enum; Type: TYPE; Schema: http_fetch; Owner: -
--

CREATE TYPE http_fetch.fetch_outcome_enum AS ENUM (
    'in_progress',
    'success',
    'redirect',
    'not_modified',
    'blocked_robots',
    'retryable_error',
    'permanent_error',
    'timeout',
    'network_error'
);


--
-- Name: robots_cache_state_enum; Type: TYPE; Schema: http_fetch; Owner: -
--

CREATE TYPE http_fetch.robots_cache_state_enum AS ENUM (
    'fresh',
    'stale',
    'missing',
    'error',
    'manual_override'
);


--
-- Name: robots_verdict_enum; Type: TYPE; Schema: http_fetch; Owner: -
--

CREATE TYPE http_fetch.robots_verdict_enum AS ENUM (
    'allow',
    'block',
    'allow_but_refresh_recommended',
    'allow_mode_ignore'
);


--
-- Name: seed_type_enum; Type: TYPE; Schema: seed; Owner: -
--

CREATE TYPE seed.seed_type_enum AS ENUM (
    'entrypoint',
    'sitemap',
    'listing_index',
    'search_surface',
    'manual'
);


--
-- Name: source_status_enum; Type: TYPE; Schema: seed; Owner: -
--

CREATE TYPE seed.source_status_enum AS ENUM (
    'active',
    'paused',
    'retired'
);


--
-- Name: claim_next_url(text, timestamp with time zone, interval, boolean); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.claim_next_url(p_worker_id text, p_now timestamp with time zone DEFAULT now(), p_lease_duration interval DEFAULT '00:10:00'::interval, p_reap_expired boolean DEFAULT true) RETURNS TABLE(url_id bigint, host_id bigint, canonical_url text, url_path text, url_query text, depth integer, priority integer, score numeric, lease_token uuid, lease_expires_at timestamp with time zone, scheme text, host text, port integer, authority_key text, user_agent_token text, robots_mode frontier.robots_mode_enum)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_worker_id IS NULL OR btrim(p_worker_id) = '' THEN
    RAISE EXCEPTION 'p_worker_id must be non-empty';
  END IF;

  IF p_lease_duration IS NULL OR p_lease_duration <= interval '0 seconds' THEN
    RAISE EXCEPTION 'p_lease_duration must be > 0';
  END IF;

  IF p_reap_expired THEN
    PERFORM 1
    FROM frontier.reap_expired_leases(p_now);
  END IF;

  RETURN QUERY
  WITH active_leases AS (
    SELECT
      u.host_id,
      count(*)::integer AS active_lease_count
    FROM frontier.url u
    WHERE u.state = 'leased'
      AND (
        u.lease_expires_at IS NULL
        OR u.lease_expires_at >= p_now
      )
    GROUP BY u.host_id
  ),
  candidate AS (
    SELECT
      u.url_id,
      u.host_id,
      u.canonical_url,
      u.url_path,
      u.url_query,
      u.depth,
      u.priority,
      u.score,
      h.scheme,
      h.host,
      h.port,
      h.authority_key,
      h.user_agent_token,
      h.robots_mode,
      h.min_delay_ms
    FROM frontier.url u
    JOIN frontier.host h
      ON h.host_id = u.host_id
    LEFT JOIN active_leases al
      ON al.host_id = h.host_id
    WHERE u.state IN ('queued', 'retry_wait')
      AND u.next_fetch_at <= p_now
      AND (u.revisit_not_before IS NULL OR u.revisit_not_before <= p_now)
      AND h.host_status = 'active'
      AND (h.pause_until IS NULL OR h.pause_until <= p_now)
      AND (h.backoff_until IS NULL OR h.backoff_until <= p_now)
      AND h.next_eligible_at <= p_now
      AND COALESCE(al.active_lease_count, 0) < h.max_concurrency
    ORDER BY
      u.priority DESC,
      u.score DESC,
      u.next_fetch_at ASC,
      u.url_id ASC
    LIMIT 1
    FOR UPDATE OF u, h SKIP LOCKED
  ),
  updated_url AS (
    UPDATE frontier.url u
       SET state = 'leased',
           lease_token = gen_random_uuid(),
           lease_owner = p_worker_id,
           lease_acquired_at = p_now,
           lease_expires_at = p_now + p_lease_duration,
           last_fetch_started_at = p_now,
           fetch_attempt_count = u.fetch_attempt_count + 1,
           updated_at = p_now
      FROM candidate c
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       u.host_id,
       u.canonical_url,
       u.url_path,
       u.url_query,
       u.depth,
       u.priority,
       u.score,
       u.lease_token,
       u.lease_expires_at
  ),
  updated_host AS (
    UPDATE frontier.host h
       SET last_fetch_started_at = p_now,
           next_eligible_at = p_now + make_interval(secs => h.min_delay_ms / 1000.0),
           updated_at = p_now
      FROM candidate c
     WHERE h.host_id = c.host_id
     RETURNING h.host_id
  )
  SELECT
    uu.url_id,
    uu.host_id,
    uu.canonical_url,
    uu.url_path,
    uu.url_query,
    uu.depth,
    uu.priority,
    uu.score,
    uu.lease_token,
    uu.lease_expires_at,
    c.scheme,
    c.host,
    c.port,
    c.authority_key,
    c.user_agent_token,
    c.robots_mode
  FROM updated_url uu
  JOIN candidate c
    ON c.url_id = uu.url_id;
END;
$$;


--
-- Name: FUNCTION claim_next_url(p_worker_id text, p_now timestamp with time zone, p_lease_duration interval, p_reap_expired boolean); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.claim_next_url(p_worker_id text, p_now timestamp with time zone, p_lease_duration interval, p_reap_expired boolean) IS 'Claims exactly one eligible frontier.url row with host gating, concurrency checks, lease acquisition, and optional expired-lease reap.';


--
-- Name: compute_retry_backoff(bigint, integer, timestamp with time zone); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.compute_retry_backoff(p_host_id bigint, p_consecutive_error_count integer, p_now timestamp with time zone DEFAULT now()) RETURNS TABLE(retry_delay interval, retry_at timestamp with time zone, base_ms integer, cap_ms integer, exponent integer, raw_ms numeric, effective_ms numeric)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_base_ms integer;
  v_cap_ms integer;
  v_exponent integer;
  v_raw_ms numeric;
  v_effective_ms numeric;
BEGIN
  IF p_host_id IS NULL THEN
    RAISE EXCEPTION 'p_host_id must not be null';
  END IF;

  SELECT
    h.retry_backoff_base_ms,
    h.retry_backoff_cap_ms
  INTO
    v_base_ms,
    v_cap_ms
  FROM frontier.host h
  WHERE h.host_id = p_host_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'frontier.host not found for host_id=%', p_host_id;
  END IF;

  v_exponent := GREATEST(COALESCE(p_consecutive_error_count, 1), 1) - 1;
  v_raw_ms := v_base_ms::numeric * power(2::numeric, v_exponent);
  v_effective_ms := LEAST(v_raw_ms, v_cap_ms::numeric);

  RETURN QUERY
  SELECT
    make_interval(secs => v_effective_ms / 1000.0),
    p_now + make_interval(secs => v_effective_ms / 1000.0),
    v_base_ms,
    v_cap_ms,
    v_exponent,
    v_raw_ms,
    v_effective_ms;
END;
$$;


--
-- Name: FUNCTION compute_retry_backoff(p_host_id bigint, p_consecutive_error_count integer, p_now timestamp with time zone); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.compute_retry_backoff(p_host_id bigint, p_consecutive_error_count integer, p_now timestamp with time zone) IS 'Computes host-level exponential retry backoff using frontier.host retry_backoff_base_ms and retry_backoff_cap_ms.';


--
-- Name: compute_success_next_fetch_at(bigint, timestamp with time zone); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.compute_success_next_fetch_at(p_url_id bigint, p_now timestamp with time zone DEFAULT now()) RETURNS TABLE(next_fetch_at timestamp with time zone, base_interval interval, jitter_pct smallint, jitter_factor numeric, source_reason text)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_base_interval interval;
  v_jitter_pct smallint;
  v_jitter_factor numeric;
  v_reason text;
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  SELECT
    COALESCE(su.recrawl_interval, ss.default_recrawl_interval, interval '7 days'),
    COALESCE(h.success_jitter_pct, 0),
    CASE
      WHEN su.seed_id IS NOT NULL THEN 'seed.seed_url.recrawl_interval'
      WHEN ss.source_id IS NOT NULL THEN 'seed.source.default_recrawl_interval'
      ELSE 'fallback_7_days'
    END
  INTO
    v_base_interval,
    v_jitter_pct,
    v_reason
  FROM frontier.url u
  JOIN frontier.host h
    ON h.host_id = u.host_id
  LEFT JOIN seed.seed_url su
    ON su.seed_id = u.seed_id
  LEFT JOIN seed.source ss
    ON ss.source_id = COALESCE(u.source_id, su.source_id)
  WHERE u.url_id = p_url_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'frontier.url not found for url_id=%', p_url_id;
  END IF;

  v_jitter_factor := 1 + (((random() * 2) - 1) * (v_jitter_pct::numeric / 100.0));

  IF v_jitter_factor < 0.10 THEN
    v_jitter_factor := 0.10;
  END IF;

  RETURN QUERY
  SELECT
    p_now + (v_base_interval * v_jitter_factor),
    v_base_interval,
    v_jitter_pct,
    v_jitter_factor,
    v_reason;
END;
$$;


--
-- Name: FUNCTION compute_success_next_fetch_at(p_url_id bigint, p_now timestamp with time zone); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.compute_success_next_fetch_at(p_url_id bigint, p_now timestamp with time zone) IS 'Computes next_fetch_at after success using seed-level recrawl_interval, else source default_recrawl_interval, else 7 days, with host success_jitter_pct applied.';


--
-- Name: finish_fetch_permanent_error(bigint, uuid, timestamp with time zone, integer, text, text); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.finish_fetch_permanent_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT NULL::integer, p_error_class text DEFAULT 'permanent_error'::text, p_error_message text DEFAULT NULL::text) RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_error_class text, last_error_message text, permanent_error_count integer, consecutive_error_count integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_lease_token IS NULL THEN
    RAISE EXCEPTION 'p_lease_token must not be null';
  END IF;

  IF p_http_status IS NOT NULL AND (p_http_status < 100 OR p_http_status > 599) THEN
    RAISE EXCEPTION 'p_http_status must be between 100 and 599 when provided';
  END IF;

  RETURN QUERY
  WITH candidate AS (
    SELECT
      u.url_id,
      u.host_id,
      u.state AS previous_state
    FROM frontier.url u
    WHERE u.url_id = p_url_id
      AND u.state = 'leased'
      AND u.lease_token = p_lease_token
    FOR UPDATE OF u
  ),
  updated_url AS (
    UPDATE frontier.url u
       SET state = 'dead',
           lease_token = NULL,
           lease_owner = NULL,
           lease_acquired_at = NULL,
           lease_expires_at = NULL,
           permanent_error_count = u.permanent_error_count + 1,
           consecutive_error_count = u.consecutive_error_count + 1,
           last_fetch_finished_at = p_now,
           last_http_status = p_http_status,
           last_outcome = 'permanent_error',
           last_error_class = p_error_class,
           last_error_message = p_error_message,
           updated_at = p_now
      FROM candidate c
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       u.host_id,
       c.previous_state,
       u.state,
       u.last_http_status,
       u.last_error_class,
       u.last_error_message,
       u.permanent_error_count,
       u.consecutive_error_count
  ),
  updated_host AS (
    UPDATE frontier.host h
       SET last_fetch_finished_at = p_now,
           last_error_at = p_now,
           last_error_class = p_error_class,
           updated_at = p_now
      FROM updated_url uu
     WHERE h.host_id = uu.host_id
     RETURNING h.host_id
  )
  SELECT
    uu.url_id,
    uu.host_id,
    uu.previous_state,
    uu.state,
    uu.last_http_status,
    uu.last_error_class,
    uu.last_error_message,
    uu.permanent_error_count,
    uu.consecutive_error_count
  FROM updated_url uu;
END;
$$;


--
-- Name: FUNCTION finish_fetch_permanent_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_error_class text, p_error_message text); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.finish_fetch_permanent_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_error_class text, p_error_message text) IS 'Finalizes a permanent leased fetch failure by moving frontier.url to dead, clearing lease fields, and recording permanent error metadata.';


--
-- Name: finish_fetch_retryable_error(bigint, uuid, timestamp with time zone, integer, text, text, interval); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.finish_fetch_retryable_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT NULL::integer, p_error_class text DEFAULT 'retryable_error'::text, p_error_message text DEFAULT NULL::text, p_retry_delay interval DEFAULT NULL::interval) RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_error_class text, last_error_message text, next_fetch_at timestamp with time zone, host_backoff_until timestamp with time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_lease_token IS NULL THEN
    RAISE EXCEPTION 'p_lease_token must not be null';
  END IF;

  IF p_http_status IS NOT NULL AND (p_http_status < 100 OR p_http_status > 599) THEN
    RAISE EXCEPTION 'p_http_status must be between 100 and 599 when provided';
  END IF;

  RETURN QUERY
  WITH candidate AS (
    SELECT
      u.url_id,
      u.host_id,
      u.state AS previous_state,
      (u.consecutive_error_count + 1) AS next_consecutive_error_count
    FROM frontier.url u
    WHERE u.url_id = p_url_id
      AND u.state = 'leased'
      AND u.lease_token = p_lease_token
    FOR UPDATE OF u
  ),
  computed_retry AS (
    SELECT
      c.url_id,
      c.host_id,
      COALESCE(
        p_retry_delay,
        (SELECT r.retry_delay
         FROM frontier.compute_retry_backoff(c.host_id, c.next_consecutive_error_count, p_now) r)
      ) AS effective_retry_delay
    FROM candidate c
  ),
  updated_url AS (
    UPDATE frontier.url u
       SET state = 'retry_wait',
           lease_token = NULL,
           lease_owner = NULL,
           lease_acquired_at = NULL,
           lease_expires_at = NULL,
           retryable_error_count = u.retryable_error_count + 1,
           consecutive_error_count = u.consecutive_error_count + 1,
           last_fetch_finished_at = p_now,
           last_http_status = p_http_status,
           last_outcome = 'retryable_error',
           last_error_class = p_error_class,
           last_error_message = p_error_message,
           next_fetch_at = p_now + cr.effective_retry_delay,
           updated_at = p_now
      FROM candidate c
      JOIN computed_retry cr
        ON cr.url_id = c.url_id
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       u.host_id,
       c.previous_state,
       u.state,
       u.last_http_status,
       u.last_error_class,
       u.last_error_message,
       u.next_fetch_at
  ),
  updated_host AS (
    UPDATE frontier.host h
       SET last_fetch_finished_at = p_now,
           last_error_at = p_now,
           last_error_class = p_error_class,
           backoff_until = p_now + cr.effective_retry_delay,
           updated_at = p_now
      FROM updated_url uu
      JOIN computed_retry cr
        ON cr.host_id = uu.host_id
     WHERE h.host_id = uu.host_id
     RETURNING
       h.host_id,
       h.backoff_until
  )
  SELECT
    uu.url_id,
    uu.host_id,
    uu.previous_state,
    uu.state,
    uu.last_http_status,
    uu.last_error_class,
    uu.last_error_message,
    uu.next_fetch_at,
    uh.backoff_until
  FROM updated_url uu
  JOIN updated_host uh
    ON uh.host_id = uu.host_id;
END;
$$;


--
-- Name: FUNCTION finish_fetch_retryable_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_error_class text, p_error_message text, p_retry_delay interval); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.finish_fetch_retryable_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_error_class text, p_error_message text, p_retry_delay interval) IS 'Finalizes a retryable leased fetch failure by moving frontier.url to retry_wait and using host retry-backoff policy when p_retry_delay is not explicitly provided.';


--
-- Name: finish_fetch_success(bigint, uuid, timestamp with time zone, integer, text, bigint, text, text, timestamp with time zone); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.finish_fetch_success(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT 200, p_content_type text DEFAULT NULL::text, p_body_bytes bigint DEFAULT NULL::bigint, p_etag text DEFAULT NULL::text, p_last_modified text DEFAULT NULL::text, p_next_fetch_at timestamp with time zone DEFAULT NULL::timestamp with time zone) RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_content_type text, last_body_bytes bigint, last_success_at timestamp with time zone, next_fetch_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  IF p_lease_token IS NULL THEN
    RAISE EXCEPTION 'p_lease_token must not be null';
  END IF;

  IF p_http_status IS NULL OR p_http_status < 100 OR p_http_status > 599 THEN
    RAISE EXCEPTION 'p_http_status must be between 100 and 599';
  END IF;

  RETURN QUERY
  WITH candidate AS (
    SELECT
      u.url_id,
      u.host_id,
      u.state AS previous_state
    FROM frontier.url u
    WHERE u.url_id = p_url_id
      AND u.state = 'leased'
      AND u.lease_token = p_lease_token
    FOR UPDATE OF u
  ),
  computed_next AS (
    SELECT
      c.url_id,
      COALESCE(
        p_next_fetch_at,
        (SELECT s.next_fetch_at
         FROM frontier.compute_success_next_fetch_at(c.url_id, p_now) s)
      ) AS effective_next_fetch_at
    FROM candidate c
  ),
  updated_url AS (
    UPDATE frontier.url u
       SET state = 'parse_pending',
           lease_token = NULL,
           lease_owner = NULL,
           lease_acquired_at = NULL,
           lease_expires_at = NULL,
           success_count = u.success_count + 1,
           consecutive_error_count = 0,
           last_fetch_finished_at = p_now,
           last_success_at = p_now,
           last_http_status = p_http_status,
           last_content_type = p_content_type,
           last_body_bytes = p_body_bytes,
           last_etag = p_etag,
           last_last_modified = p_last_modified,
           last_outcome = 'success',
           last_error_class = NULL,
           last_error_message = NULL,
           next_fetch_at = cn.effective_next_fetch_at,
           updated_at = p_now
      FROM candidate c
      JOIN computed_next cn
        ON cn.url_id = c.url_id
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       u.host_id,
       c.previous_state,
       u.state,
       u.last_http_status,
       u.last_content_type,
       u.last_body_bytes,
       u.last_success_at,
       u.next_fetch_at
  ),
  updated_host AS (
    UPDATE frontier.host h
       SET last_fetch_finished_at = p_now,
           last_success_at = p_now,
           last_error_at = NULL,
           last_error_class = NULL,
           updated_at = p_now
      FROM updated_url uu
     WHERE h.host_id = uu.host_id
     RETURNING h.host_id
  )
  SELECT
    uu.url_id,
    uu.host_id,
    uu.previous_state,
    uu.state,
    uu.last_http_status,
    uu.last_content_type,
    uu.last_body_bytes,
    uu.last_success_at,
    uu.next_fetch_at
  FROM updated_url uu;
END;
$$;


--
-- Name: FUNCTION finish_fetch_success(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_content_type text, p_body_bytes bigint, p_etag text, p_last_modified text, p_next_fetch_at timestamp with time zone); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.finish_fetch_success(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone, p_http_status integer, p_content_type text, p_body_bytes bigint, p_etag text, p_last_modified text, p_next_fetch_at timestamp with time zone) IS 'Finalizes a successful leased fetch by moving frontier.url to parse_pending, clearing lease fields, and computing next_fetch_at from policy when not explicitly provided.';


--
-- Name: reap_expired_leases(timestamp with time zone); Type: FUNCTION; Schema: frontier; Owner: -
--

CREATE FUNCTION frontier.reap_expired_leases(p_now timestamp with time zone DEFAULT now()) RETURNS TABLE(url_id bigint, previous_lease_owner text, previous_lease_expires_at timestamp with time zone, new_state frontier.url_state_enum)
    LANGUAGE plpgsql
    AS $$
BEGIN
  RETURN QUERY
  WITH candidates AS (
    SELECT
      u.url_id,
      u.lease_owner,
      u.lease_expires_at
    FROM frontier.url u
    WHERE u.state = 'leased'
      AND u.lease_expires_at IS NOT NULL
      AND u.lease_expires_at < p_now
    FOR UPDATE SKIP LOCKED
  ),
  updated AS (
    UPDATE frontier.url u
       SET state = 'queued',
           lease_token = NULL,
           lease_owner = NULL,
           lease_acquired_at = NULL,
           lease_expires_at = NULL,
           updated_at = p_now
      FROM candidates c
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       c.lease_owner,
       c.lease_expires_at,
       u.state
  )
  SELECT
    updated.url_id,
    updated.lease_owner,
    updated.lease_expires_at,
    updated.state
  FROM updated
  ORDER BY updated.url_id;
END;
$$;


--
-- Name: FUNCTION reap_expired_leases(p_now timestamp with time zone); Type: COMMENT; Schema: frontier; Owner: -
--

COMMENT ON FUNCTION frontier.reap_expired_leases(p_now timestamp with time zone) IS 'Releases expired leased frontier.url rows back to queued state for reboot/crash-safe resume.';


--
-- Name: compute_robots_allow_decision(bigint, text); Type: FUNCTION; Schema: http_fetch; Owner: -
--

CREATE FUNCTION http_fetch.compute_robots_allow_decision(p_host_id bigint, p_url_path text) RETURNS TABLE(host_id bigint, url_path text, robots_mode frontier.robots_mode_enum, cache_exists boolean, cache_state http_fetch.robots_cache_state_enum, matched_rule text, verdict http_fetch.robots_verdict_enum, decision_reason text)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_robots_mode frontier.robots_mode_enum;
  v_cache_state http_fetch.robots_cache_state_enum;
  v_parsed_rules jsonb;
  v_disallow jsonb;
  v_rule text;
BEGIN
  IF p_host_id IS NULL THEN
    RAISE EXCEPTION 'p_host_id must not be null';
  END IF;

  IF p_url_path IS NULL OR btrim(p_url_path) = '' THEN
    RAISE EXCEPTION 'p_url_path must be non-empty';
  END IF;

  SELECT h.robots_mode
  INTO v_robots_mode
  FROM frontier.host h
  WHERE h.host_id = p_host_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'frontier.host not found for host_id=%', p_host_id;
  END IF;

  IF v_robots_mode = 'ignore' THEN
    RETURN QUERY
    SELECT
      p_host_id,
      p_url_path,
      v_robots_mode,
      false,
      NULL::http_fetch.robots_cache_state_enum,
      NULL::text,
      'allow_mode_ignore'::http_fetch.robots_verdict_enum,
      'host_robots_mode_ignore'::text;
    RETURN;
  END IF;

  SELECT
    c.cache_state,
    c.parsed_rules
  INTO
    v_cache_state,
    v_parsed_rules
  FROM http_fetch.robots_txt_cache c
  WHERE c.host_id = p_host_id;

  IF NOT FOUND THEN
    RETURN QUERY
    SELECT
      p_host_id,
      p_url_path,
      v_robots_mode,
      false,
      NULL::http_fetch.robots_cache_state_enum,
      NULL::text,
      'allow_but_refresh_recommended'::http_fetch.robots_verdict_enum,
      'missing_robots_cache'::text;
    RETURN;
  END IF;

  v_disallow := COALESCE(v_parsed_rules -> 'disallow', '[]'::jsonb);

  IF jsonb_typeof(v_disallow) <> 'array' THEN
    RETURN QUERY
    SELECT
      p_host_id,
      p_url_path,
      v_robots_mode,
      true,
      v_cache_state,
      NULL::text,
      'allow_but_refresh_recommended'::http_fetch.robots_verdict_enum,
      'invalid_disallow_shape'::text;
    RETURN;
  END IF;

  FOR v_rule IN
    SELECT jsonb_array_elements_text(v_disallow)
  LOOP
    IF v_rule IS NULL OR btrim(v_rule) = '' THEN
      CONTINUE;
    END IF;

    IF p_url_path LIKE v_rule || '%' THEN
      RETURN QUERY
      SELECT
        p_host_id,
        p_url_path,
        v_robots_mode,
        true,
        v_cache_state,
        v_rule,
        'block'::http_fetch.robots_verdict_enum,
        'matched_disallow_prefix'::text;
      RETURN;
    END IF;
  END LOOP;

  RETURN QUERY
  SELECT
    p_host_id,
    p_url_path,
    v_robots_mode,
    true,
    v_cache_state,
    NULL::text,
    'allow'::http_fetch.robots_verdict_enum,
    'no_disallow_match'::text;
END;
$$;


--
-- Name: FUNCTION compute_robots_allow_decision(p_host_id bigint, p_url_path text); Type: COMMENT; Schema: http_fetch; Owner: -
--

COMMENT ON FUNCTION http_fetch.compute_robots_allow_decision(p_host_id bigint, p_url_path text) IS 'Computes a simple robots enforcement verdict using host robots_mode and parsed_rules.disallow prefix matching.';


--
-- Name: compute_robots_refresh_decision(bigint, timestamp with time zone); Type: FUNCTION; Schema: http_fetch; Owner: -
--

CREATE FUNCTION http_fetch.compute_robots_refresh_decision(p_host_id bigint, p_now timestamp with time zone DEFAULT now()) RETURNS TABLE(host_id bigint, robots_url text, cache_exists boolean, cache_state http_fetch.robots_cache_state_enum, fetched_at timestamp with time zone, expires_at timestamp with time zone, should_refresh boolean, refresh_reason text)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_scheme text;
  v_host text;
  v_port integer;

  v_cache_state http_fetch.robots_cache_state_enum;
  v_fetched_at timestamptz;
  v_expires_at timestamptz;

  v_robots_url text;
  v_should_refresh boolean;
  v_refresh_reason text;
BEGIN
  IF p_host_id IS NULL THEN
    RAISE EXCEPTION 'p_host_id must not be null';
  END IF;

  SELECT
    h.scheme,
    h.host,
    h.port
  INTO
    v_scheme,
    v_host,
    v_port
  FROM frontier.host h
  WHERE h.host_id = p_host_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'frontier.host not found for host_id=%', p_host_id;
  END IF;

  v_robots_url := v_scheme || '://' || v_host ||
    CASE
      WHEN (v_scheme = 'https' AND v_port = 443) OR (v_scheme = 'http' AND v_port = 80)
        THEN ''
      ELSE ':' || v_port::text
    END ||
    '/robots.txt';

  SELECT
    c.cache_state,
    c.fetched_at,
    c.expires_at
  INTO
    v_cache_state,
    v_fetched_at,
    v_expires_at
  FROM http_fetch.robots_txt_cache c
  WHERE c.host_id = p_host_id;

  IF NOT FOUND THEN
    v_should_refresh := true;
    v_refresh_reason := 'missing_cache';

    RETURN QUERY
    SELECT
      p_host_id,
      v_robots_url,
      false,
      NULL::http_fetch.robots_cache_state_enum,
      NULL::timestamptz,
      NULL::timestamptz,
      v_should_refresh,
      v_refresh_reason;
    RETURN;
  END IF;

  IF v_cache_state IN ('missing', 'error', 'stale') THEN
    v_should_refresh := true;
    v_refresh_reason := 'cache_state_requires_refresh';
  ELSIF v_expires_at IS NULL THEN
    v_should_refresh := true;
    v_refresh_reason := 'no_expiry';
  ELSIF v_expires_at <= p_now THEN
    v_should_refresh := true;
    v_refresh_reason := 'expired';
  ELSE
    v_should_refresh := false;
    v_refresh_reason := 'fresh';
  END IF;

  RETURN QUERY
  SELECT
    p_host_id,
    v_robots_url,
    true,
    v_cache_state,
    v_fetched_at,
    v_expires_at,
    v_should_refresh,
    v_refresh_reason;
END;
$$;


--
-- Name: FUNCTION compute_robots_refresh_decision(p_host_id bigint, p_now timestamp with time zone); Type: COMMENT; Schema: http_fetch; Owner: -
--

COMMENT ON FUNCTION http_fetch.compute_robots_refresh_decision(p_host_id bigint, p_now timestamp with time zone) IS 'Determines whether a host robots.txt cache should be refreshed based on cache presence, cache_state, and expiry.';


--
-- Name: upsert_robots_txt_cache(bigint, text, http_fetch.robots_cache_state_enum, integer, timestamp with time zone, timestamp with time zone, text, text, text, text, bigint, jsonb, jsonb, numeric, text, text, jsonb); Type: FUNCTION; Schema: http_fetch; Owner: -
--

CREATE FUNCTION http_fetch.upsert_robots_txt_cache(p_host_id bigint, p_robots_url text, p_cache_state http_fetch.robots_cache_state_enum, p_http_status integer DEFAULT NULL::integer, p_fetched_at timestamp with time zone DEFAULT now(), p_expires_at timestamp with time zone DEFAULT NULL::timestamp with time zone, p_etag text DEFAULT NULL::text, p_last_modified text DEFAULT NULL::text, p_raw_storage_path text DEFAULT NULL::text, p_raw_sha256 text DEFAULT NULL::text, p_raw_bytes bigint DEFAULT NULL::bigint, p_parsed_rules jsonb DEFAULT '{}'::jsonb, p_sitemap_urls jsonb DEFAULT '[]'::jsonb, p_crawl_delay_seconds numeric DEFAULT NULL::numeric, p_error_class text DEFAULT NULL::text, p_error_message text DEFAULT NULL::text, p_robots_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(robots_cache_id bigint, host_id bigint, robots_url text, cache_state http_fetch.robots_cache_state_enum, http_status integer, fetched_at timestamp with time zone, expires_at timestamp with time zone, etag text, last_modified text, crawl_delay_seconds numeric, error_class text, error_message text)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_host_id IS NULL THEN
    RAISE EXCEPTION 'p_host_id must not be null';
  END IF;

  IF p_robots_url IS NULL OR btrim(p_robots_url) = '' THEN
    RAISE EXCEPTION 'p_robots_url must be non-empty';
  END IF;

  IF p_cache_state IS NULL THEN
    RAISE EXCEPTION 'p_cache_state must not be null';
  END IF;

  IF p_http_status IS NOT NULL AND (p_http_status < 100 OR p_http_status > 599) THEN
    RAISE EXCEPTION 'p_http_status must be between 100 and 599 when provided';
  END IF;

  IF p_raw_bytes IS NOT NULL AND p_raw_bytes < 0 THEN
    RAISE EXCEPTION 'p_raw_bytes must be >= 0 when provided';
  END IF;

  IF p_crawl_delay_seconds IS NOT NULL AND p_crawl_delay_seconds < 0 THEN
    RAISE EXCEPTION 'p_crawl_delay_seconds must be >= 0 when provided';
  END IF;

  IF NOT EXISTS (
    SELECT 1
    FROM frontier.host h
    WHERE h.host_id = p_host_id
  ) THEN
    RAISE EXCEPTION 'frontier.host not found for host_id=%', p_host_id;
  END IF;

  RETURN QUERY
  INSERT INTO http_fetch.robots_txt_cache AS rtc (
    host_id,
    robots_url,
    cache_state,
    http_status,
    fetched_at,
    expires_at,
    etag,
    last_modified,
    raw_storage_path,
    raw_sha256,
    raw_bytes,
    parsed_rules,
    sitemap_urls,
    crawl_delay_seconds,
    robots_metadata,
    error_class,
    error_message,
    updated_at
  )
  VALUES (
    p_host_id,
    p_robots_url,
    p_cache_state,
    p_http_status,
    p_fetched_at,
    p_expires_at,
    p_etag,
    p_last_modified,
    p_raw_storage_path,
    p_raw_sha256,
    p_raw_bytes,
    COALESCE(p_parsed_rules, '{}'::jsonb),
    COALESCE(p_sitemap_urls, '[]'::jsonb),
    p_crawl_delay_seconds,
    COALESCE(p_robots_metadata, '{}'::jsonb),
    p_error_class,
    p_error_message,
    now()
  )
  ON CONFLICT ON CONSTRAINT robots_txt_cache_host_id_key
  DO UPDATE
     SET robots_url = EXCLUDED.robots_url,
         cache_state = EXCLUDED.cache_state,
         http_status = EXCLUDED.http_status,
         fetched_at = EXCLUDED.fetched_at,
         expires_at = EXCLUDED.expires_at,
         etag = EXCLUDED.etag,
         last_modified = EXCLUDED.last_modified,
         raw_storage_path = EXCLUDED.raw_storage_path,
         raw_sha256 = EXCLUDED.raw_sha256,
         raw_bytes = EXCLUDED.raw_bytes,
         parsed_rules = EXCLUDED.parsed_rules,
         sitemap_urls = EXCLUDED.sitemap_urls,
         crawl_delay_seconds = EXCLUDED.crawl_delay_seconds,
         robots_metadata = EXCLUDED.robots_metadata,
         error_class = EXCLUDED.error_class,
         error_message = EXCLUDED.error_message,
         updated_at = now()
  RETURNING
    rtc.robots_cache_id,
    rtc.host_id,
    rtc.robots_url,
    rtc.cache_state,
    rtc.http_status,
    rtc.fetched_at,
    rtc.expires_at,
    rtc.etag,
    rtc.last_modified,
    rtc.crawl_delay_seconds,
    rtc.error_class,
    rtc.error_message;
END;
$$;


--
-- Name: FUNCTION upsert_robots_txt_cache(p_host_id bigint, p_robots_url text, p_cache_state http_fetch.robots_cache_state_enum, p_http_status integer, p_fetched_at timestamp with time zone, p_expires_at timestamp with time zone, p_etag text, p_last_modified text, p_raw_storage_path text, p_raw_sha256 text, p_raw_bytes bigint, p_parsed_rules jsonb, p_sitemap_urls jsonb, p_crawl_delay_seconds numeric, p_error_class text, p_error_message text, p_robots_metadata jsonb); Type: COMMENT; Schema: http_fetch; Owner: -
--

COMMENT ON FUNCTION http_fetch.upsert_robots_txt_cache(p_host_id bigint, p_robots_url text, p_cache_state http_fetch.robots_cache_state_enum, p_http_status integer, p_fetched_at timestamp with time zone, p_expires_at timestamp with time zone, p_etag text, p_last_modified text, p_raw_storage_path text, p_raw_sha256 text, p_raw_bytes bigint, p_parsed_rules jsonb, p_sitemap_urls jsonb, p_crawl_delay_seconds numeric, p_error_class text, p_error_message text, p_robots_metadata jsonb) IS 'Creates or updates a host robots.txt cache record after fetch/parse.';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: host; Type: TABLE; Schema: frontier; Owner: -
--

CREATE TABLE frontier.host (
    host_id bigint NOT NULL,
    scheme text NOT NULL,
    host text NOT NULL,
    port integer NOT NULL,
    authority_key text GENERATED ALWAYS AS (((lower(host) || ':'::text) || (port)::text)) STORED,
    registrable_domain text,
    host_status frontier.host_status_enum DEFAULT 'active'::frontier.host_status_enum NOT NULL,
    robots_mode frontier.robots_mode_enum DEFAULT 'respect'::frontier.robots_mode_enum NOT NULL,
    user_agent_token text DEFAULT 'LogisticSearchBot'::text NOT NULL,
    max_concurrency smallint DEFAULT 1 NOT NULL,
    min_delay_ms integer DEFAULT 15000 NOT NULL,
    success_jitter_pct smallint DEFAULT 20 NOT NULL,
    retry_backoff_base_ms integer DEFAULT 60000 NOT NULL,
    retry_backoff_cap_ms integer DEFAULT 86400000 NOT NULL,
    next_eligible_at timestamp with time zone DEFAULT now() NOT NULL,
    backoff_until timestamp with time zone,
    pause_until timestamp with time zone,
    robots_last_checked_at timestamp with time zone,
    robots_etag text,
    robots_last_modified text,
    last_fetch_started_at timestamp with time zone,
    last_fetch_finished_at timestamp with time zone,
    last_success_at timestamp with time zone,
    last_error_at timestamp with time zone,
    last_error_class text,
    host_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT host_max_concurrency_check CHECK (((max_concurrency >= 1) AND (max_concurrency <= 16))),
    CONSTRAINT host_min_delay_ms_check CHECK (((min_delay_ms >= 0) AND (min_delay_ms <= 86400000))),
    CONSTRAINT host_port_check CHECK (((port >= 1) AND (port <= 65535))),
    CONSTRAINT host_retry_backoff_base_ms_check CHECK (((retry_backoff_base_ms >= 0) AND (retry_backoff_base_ms <= 86400000))),
    CONSTRAINT host_retry_backoff_cap_ms_check CHECK (((retry_backoff_cap_ms >= 0) AND (retry_backoff_cap_ms <= 604800000))),
    CONSTRAINT host_scheme_check CHECK ((scheme = ANY (ARRAY['http'::text, 'https'::text]))),
    CONSTRAINT host_success_jitter_pct_check CHECK (((success_jitter_pct >= 0) AND (success_jitter_pct <= 100)))
);


--
-- Name: host_host_id_seq; Type: SEQUENCE; Schema: frontier; Owner: -
--

CREATE SEQUENCE frontier.host_host_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: host_host_id_seq; Type: SEQUENCE OWNED BY; Schema: frontier; Owner: -
--

ALTER SEQUENCE frontier.host_host_id_seq OWNED BY frontier.host.host_id;


--
-- Name: url; Type: TABLE; Schema: frontier; Owner: -
--

CREATE TABLE frontier.url (
    url_id bigint NOT NULL,
    host_id bigint NOT NULL,
    canonical_url text NOT NULL,
    canonical_url_sha256 text GENERATED ALWAYS AS (encode(public.digest(canonical_url, 'sha256'::text), 'hex'::text)) STORED,
    url_path text NOT NULL,
    url_query text,
    source_id uuid,
    seed_id uuid,
    discovery_type frontier.discovery_type_enum DEFAULT 'seed'::frontier.discovery_type_enum NOT NULL,
    parent_url_id bigint,
    depth integer DEFAULT 0 NOT NULL,
    is_seed boolean DEFAULT false NOT NULL,
    state frontier.url_state_enum DEFAULT 'queued'::frontier.url_state_enum NOT NULL,
    priority integer DEFAULT 100 NOT NULL,
    score numeric(12,4) DEFAULT 0 NOT NULL,
    enqueue_reason text,
    first_seen_at timestamp with time zone DEFAULT now() NOT NULL,
    last_seen_at timestamp with time zone DEFAULT now() NOT NULL,
    last_enqueued_at timestamp with time zone DEFAULT now() NOT NULL,
    next_fetch_at timestamp with time zone DEFAULT now() NOT NULL,
    revisit_not_before timestamp with time zone,
    lease_token uuid,
    lease_owner text,
    lease_acquired_at timestamp with time zone,
    lease_expires_at timestamp with time zone,
    fetch_attempt_count integer DEFAULT 0 NOT NULL,
    success_count integer DEFAULT 0 NOT NULL,
    retryable_error_count integer DEFAULT 0 NOT NULL,
    permanent_error_count integer DEFAULT 0 NOT NULL,
    redirect_count integer DEFAULT 0 NOT NULL,
    consecutive_error_count integer DEFAULT 0 NOT NULL,
    last_fetch_started_at timestamp with time zone,
    last_fetch_finished_at timestamp with time zone,
    last_success_at timestamp with time zone,
    last_http_status integer,
    last_content_type text,
    last_body_bytes bigint,
    last_etag text,
    last_last_modified text,
    last_outcome http_fetch.fetch_outcome_enum,
    last_error_class text,
    last_error_message text,
    url_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT url_consecutive_error_count_check CHECK ((consecutive_error_count >= 0)),
    CONSTRAINT url_depth_check CHECK ((depth >= 0)),
    CONSTRAINT url_fetch_attempt_count_check CHECK ((fetch_attempt_count >= 0)),
    CONSTRAINT url_last_body_bytes_check CHECK ((last_body_bytes >= 0)),
    CONSTRAINT url_last_http_status_check CHECK (((last_http_status >= 100) AND (last_http_status <= 599))),
    CONSTRAINT url_permanent_error_count_check CHECK ((permanent_error_count >= 0)),
    CONSTRAINT url_redirect_count_check CHECK ((redirect_count >= 0)),
    CONSTRAINT url_retryable_error_count_check CHECK ((retryable_error_count >= 0)),
    CONSTRAINT url_success_count_check CHECK ((success_count >= 0))
);


--
-- Name: url_url_id_seq; Type: SEQUENCE; Schema: frontier; Owner: -
--

CREATE SEQUENCE frontier.url_url_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: url_url_id_seq; Type: SEQUENCE OWNED BY; Schema: frontier; Owner: -
--

ALTER SEQUENCE frontier.url_url_id_seq OWNED BY frontier.url.url_id;


--
-- Name: fetch_attempt; Type: TABLE; Schema: http_fetch; Owner: -
--

CREATE TABLE http_fetch.fetch_attempt (
    fetch_attempt_id bigint NOT NULL,
    url_id bigint,
    host_id bigint NOT NULL,
    fetch_kind http_fetch.fetch_kind_enum DEFAULT 'page'::http_fetch.fetch_kind_enum NOT NULL,
    lease_token uuid,
    worker_id text NOT NULL,
    worker_run_id uuid,
    request_method text DEFAULT 'GET'::text NOT NULL,
    request_url text NOT NULL,
    final_url text,
    request_headers jsonb DEFAULT '{}'::jsonb NOT NULL,
    response_headers jsonb DEFAULT '{}'::jsonb NOT NULL,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    first_byte_at timestamp with time zone,
    ended_at timestamp with time zone,
    outcome http_fetch.fetch_outcome_enum DEFAULT 'in_progress'::http_fetch.fetch_outcome_enum NOT NULL,
    http_status integer,
    remote_ip inet,
    redirect_location text,
    content_type text,
    content_encoding text,
    content_length bigint,
    body_storage_path text,
    body_sha256 text,
    body_bytes bigint,
    etag text,
    last_modified text,
    retry_after_seconds integer,
    error_class text,
    error_message text,
    fetch_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT fetch_attempt_body_bytes_check CHECK ((body_bytes >= 0)),
    CONSTRAINT fetch_attempt_content_length_check CHECK ((content_length >= 0)),
    CONSTRAINT fetch_attempt_http_status_check CHECK (((http_status >= 100) AND (http_status <= 599))),
    CONSTRAINT fetch_attempt_retry_after_seconds_check CHECK ((retry_after_seconds >= 0))
);


--
-- Name: fetch_attempt_fetch_attempt_id_seq; Type: SEQUENCE; Schema: http_fetch; Owner: -
--

CREATE SEQUENCE http_fetch.fetch_attempt_fetch_attempt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fetch_attempt_fetch_attempt_id_seq; Type: SEQUENCE OWNED BY; Schema: http_fetch; Owner: -
--

ALTER SEQUENCE http_fetch.fetch_attempt_fetch_attempt_id_seq OWNED BY http_fetch.fetch_attempt.fetch_attempt_id;


--
-- Name: robots_txt_cache; Type: TABLE; Schema: http_fetch; Owner: -
--

CREATE TABLE http_fetch.robots_txt_cache (
    robots_cache_id bigint NOT NULL,
    host_id bigint NOT NULL,
    robots_url text NOT NULL,
    cache_state http_fetch.robots_cache_state_enum DEFAULT 'fresh'::http_fetch.robots_cache_state_enum NOT NULL,
    http_status integer,
    fetched_at timestamp with time zone,
    expires_at timestamp with time zone,
    etag text,
    last_modified text,
    raw_storage_path text,
    raw_sha256 text,
    raw_bytes bigint,
    parsed_rules jsonb DEFAULT '{}'::jsonb NOT NULL,
    sitemap_urls jsonb DEFAULT '[]'::jsonb NOT NULL,
    crawl_delay_seconds numeric(12,3),
    robots_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    error_class text,
    error_message text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT robots_txt_cache_http_status_check CHECK (((http_status >= 100) AND (http_status <= 599))),
    CONSTRAINT robots_txt_cache_raw_bytes_check CHECK ((raw_bytes >= 0))
);


--
-- Name: robots_txt_cache_robots_cache_id_seq; Type: SEQUENCE; Schema: http_fetch; Owner: -
--

CREATE SEQUENCE http_fetch.robots_txt_cache_robots_cache_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: robots_txt_cache_robots_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: http_fetch; Owner: -
--

ALTER SEQUENCE http_fetch.robots_txt_cache_robots_cache_id_seq OWNED BY http_fetch.robots_txt_cache.robots_cache_id;


--
-- Name: seed_url; Type: TABLE; Schema: seed; Owner: -
--

CREATE TABLE seed.seed_url (
    seed_id uuid DEFAULT gen_random_uuid() NOT NULL,
    source_id uuid NOT NULL,
    seed_type seed.seed_type_enum DEFAULT 'entrypoint'::seed.seed_type_enum NOT NULL,
    submitted_url text NOT NULL,
    canonical_url text NOT NULL,
    canonical_url_sha256 text GENERATED ALWAYS AS (encode(public.digest(canonical_url, 'sha256'::text), 'hex'::text)) STORED,
    is_enabled boolean DEFAULT true NOT NULL,
    priority integer DEFAULT 100 NOT NULL,
    max_depth integer DEFAULT 2 NOT NULL,
    recrawl_interval interval DEFAULT '7 days'::interval NOT NULL,
    next_discover_at timestamp with time zone DEFAULT now() NOT NULL,
    last_discovered_at timestamp with time zone,
    last_enqueued_at timestamp with time zone,
    last_result text,
    seed_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT seed_url_max_depth_check CHECK ((max_depth >= 0))
);


--
-- Name: source; Type: TABLE; Schema: seed; Owner: -
--

CREATE TABLE seed.source (
    source_id uuid DEFAULT gen_random_uuid() NOT NULL,
    source_code text NOT NULL,
    source_name text NOT NULL,
    source_status seed.source_status_enum DEFAULT 'active'::seed.source_status_enum NOT NULL,
    homepage_url text,
    source_category text,
    allowed_schemes text[] DEFAULT ARRAY['https'::text, 'http'::text] NOT NULL,
    default_priority integer DEFAULT 100 NOT NULL,
    default_recrawl_interval interval DEFAULT '7 days'::interval NOT NULL,
    default_max_depth integer DEFAULT 2 NOT NULL,
    notes text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT source_default_max_depth_check CHECK ((default_max_depth >= 0))
);


--
-- Name: host host_id; Type: DEFAULT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.host ALTER COLUMN host_id SET DEFAULT nextval('frontier.host_host_id_seq'::regclass);


--
-- Name: url url_id; Type: DEFAULT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url ALTER COLUMN url_id SET DEFAULT nextval('frontier.url_url_id_seq'::regclass);


--
-- Name: fetch_attempt fetch_attempt_id; Type: DEFAULT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.fetch_attempt ALTER COLUMN fetch_attempt_id SET DEFAULT nextval('http_fetch.fetch_attempt_fetch_attempt_id_seq'::regclass);


--
-- Name: robots_txt_cache robots_cache_id; Type: DEFAULT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.robots_txt_cache ALTER COLUMN robots_cache_id SET DEFAULT nextval('http_fetch.robots_txt_cache_robots_cache_id_seq'::regclass);


--
-- Name: host host_authority_key_key; Type: CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.host
    ADD CONSTRAINT host_authority_key_key UNIQUE (authority_key);


--
-- Name: host host_pkey; Type: CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.host
    ADD CONSTRAINT host_pkey PRIMARY KEY (host_id);


--
-- Name: url url_canonical_url_sha256_key; Type: CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_canonical_url_sha256_key UNIQUE (canonical_url_sha256);


--
-- Name: url url_pkey; Type: CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_pkey PRIMARY KEY (url_id);


--
-- Name: fetch_attempt fetch_attempt_pkey; Type: CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.fetch_attempt
    ADD CONSTRAINT fetch_attempt_pkey PRIMARY KEY (fetch_attempt_id);


--
-- Name: robots_txt_cache robots_txt_cache_host_id_key; Type: CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.robots_txt_cache
    ADD CONSTRAINT robots_txt_cache_host_id_key UNIQUE (host_id);


--
-- Name: robots_txt_cache robots_txt_cache_pkey; Type: CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.robots_txt_cache
    ADD CONSTRAINT robots_txt_cache_pkey PRIMARY KEY (robots_cache_id);


--
-- Name: seed_url seed_url_pkey; Type: CONSTRAINT; Schema: seed; Owner: -
--

ALTER TABLE ONLY seed.seed_url
    ADD CONSTRAINT seed_url_pkey PRIMARY KEY (seed_id);


--
-- Name: seed_url seed_url_source_id_canonical_url_sha256_key; Type: CONSTRAINT; Schema: seed; Owner: -
--

ALTER TABLE ONLY seed.seed_url
    ADD CONSTRAINT seed_url_source_id_canonical_url_sha256_key UNIQUE (source_id, canonical_url_sha256);


--
-- Name: source source_pkey; Type: CONSTRAINT; Schema: seed; Owner: -
--

ALTER TABLE ONLY seed.source
    ADD CONSTRAINT source_pkey PRIMARY KEY (source_id);


--
-- Name: source source_source_code_key; Type: CONSTRAINT; Schema: seed; Owner: -
--

ALTER TABLE ONLY seed.source
    ADD CONSTRAINT source_source_code_key UNIQUE (source_code);


--
-- Name: frontier_host_pause_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_host_pause_idx ON frontier.host USING btree (pause_until, backoff_until);


--
-- Name: frontier_host_sched_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_host_sched_idx ON frontier.host USING btree (next_eligible_at, host_status);


--
-- Name: frontier_url_due_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_url_due_idx ON frontier.url USING btree (next_fetch_at, priority DESC, url_id) WHERE (state = ANY (ARRAY['queued'::frontier.url_state_enum, 'retry_wait'::frontier.url_state_enum]));


--
-- Name: frontier_url_host_due_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_url_host_due_idx ON frontier.url USING btree (host_id, next_fetch_at, priority DESC) WHERE (state = ANY (ARRAY['queued'::frontier.url_state_enum, 'retry_wait'::frontier.url_state_enum, 'leased'::frontier.url_state_enum]));


--
-- Name: frontier_url_lease_expiry_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_url_lease_expiry_idx ON frontier.url USING btree (lease_expires_at) WHERE (state = 'leased'::frontier.url_state_enum);


--
-- Name: frontier_url_parent_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_url_parent_idx ON frontier.url USING btree (parent_url_id);


--
-- Name: frontier_url_parse_pending_idx; Type: INDEX; Schema: frontier; Owner: -
--

CREATE INDEX frontier_url_parse_pending_idx ON frontier.url USING btree (last_fetch_finished_at, url_id) WHERE (state = 'parse_pending'::frontier.url_state_enum);


--
-- Name: fetch_attempt_host_time_idx; Type: INDEX; Schema: http_fetch; Owner: -
--

CREATE INDEX fetch_attempt_host_time_idx ON http_fetch.fetch_attempt USING btree (host_id, started_at DESC);


--
-- Name: fetch_attempt_open_idx; Type: INDEX; Schema: http_fetch; Owner: -
--

CREATE INDEX fetch_attempt_open_idx ON http_fetch.fetch_attempt USING btree (started_at) WHERE (outcome = 'in_progress'::http_fetch.fetch_outcome_enum);


--
-- Name: fetch_attempt_url_time_idx; Type: INDEX; Schema: http_fetch; Owner: -
--

CREATE INDEX fetch_attempt_url_time_idx ON http_fetch.fetch_attempt USING btree (url_id, started_at DESC);


--
-- Name: robots_cache_expiry_idx; Type: INDEX; Schema: http_fetch; Owner: -
--

CREATE INDEX robots_cache_expiry_idx ON http_fetch.robots_txt_cache USING btree (expires_at);


--
-- Name: seed_seed_url_due_idx; Type: INDEX; Schema: seed; Owner: -
--

CREATE INDEX seed_seed_url_due_idx ON seed.seed_url USING btree (next_discover_at, priority DESC) WHERE (is_enabled = true);


--
-- Name: url url_host_id_fkey; Type: FK CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_host_id_fkey FOREIGN KEY (host_id) REFERENCES frontier.host(host_id) ON DELETE RESTRICT;


--
-- Name: url url_parent_url_id_fkey; Type: FK CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_parent_url_id_fkey FOREIGN KEY (parent_url_id) REFERENCES frontier.url(url_id) ON DELETE SET NULL;


--
-- Name: url url_seed_id_fkey; Type: FK CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_seed_id_fkey FOREIGN KEY (seed_id) REFERENCES seed.seed_url(seed_id) ON DELETE SET NULL;


--
-- Name: url url_source_id_fkey; Type: FK CONSTRAINT; Schema: frontier; Owner: -
--

ALTER TABLE ONLY frontier.url
    ADD CONSTRAINT url_source_id_fkey FOREIGN KEY (source_id) REFERENCES seed.source(source_id) ON DELETE SET NULL;


--
-- Name: fetch_attempt fetch_attempt_host_id_fkey; Type: FK CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.fetch_attempt
    ADD CONSTRAINT fetch_attempt_host_id_fkey FOREIGN KEY (host_id) REFERENCES frontier.host(host_id) ON DELETE RESTRICT;


--
-- Name: fetch_attempt fetch_attempt_url_id_fkey; Type: FK CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.fetch_attempt
    ADD CONSTRAINT fetch_attempt_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: robots_txt_cache robots_txt_cache_host_id_fkey; Type: FK CONSTRAINT; Schema: http_fetch; Owner: -
--

ALTER TABLE ONLY http_fetch.robots_txt_cache
    ADD CONSTRAINT robots_txt_cache_host_id_fkey FOREIGN KEY (host_id) REFERENCES frontier.host(host_id) ON DELETE CASCADE;


--
-- Name: seed_url seed_url_source_id_fkey; Type: FK CONSTRAINT; Schema: seed; Owner: -
--

ALTER TABLE ONLY seed.seed_url
    ADD CONSTRAINT seed_url_source_id_fkey FOREIGN KEY (source_id) REFERENCES seed.source(source_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict dPwpDYLZXzFXQHl3ZcNRHh2GJU9t6i6006peqzeYIfaaugeNf7pDJwoPOh4n6CU

