-- Derived from live Pi51 crawler-core function definitions

CREATE OR REPLACE FUNCTION frontier.claim_next_url(p_worker_id text, p_now timestamp with time zone DEFAULT now(), p_lease_duration interval DEFAULT '00:10:00'::interval, p_reap_expired boolean DEFAULT true)
 RETURNS TABLE(url_id bigint, host_id bigint, canonical_url text, url_path text, url_query text, depth integer, priority integer, score numeric, lease_token uuid, lease_expires_at timestamp with time zone, scheme text, host text, port integer, authority_key text, user_agent_token text, robots_mode frontier.robots_mode_enum)
 LANGUAGE plpgsql
AS $function$
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
$function$;


CREATE OR REPLACE FUNCTION frontier.reap_expired_leases(p_now timestamp with time zone DEFAULT now())
 RETURNS TABLE(url_id bigint, previous_lease_owner text, previous_lease_expires_at timestamp with time zone, new_state frontier.url_state_enum)
 LANGUAGE plpgsql
AS $function$
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
$function$;


