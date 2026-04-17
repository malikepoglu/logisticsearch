-- Derived from live Pi51 crawler-core function definitions

CREATE OR REPLACE FUNCTION frontier.finish_fetch_success(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT 200, p_content_type text DEFAULT NULL::text, p_body_bytes bigint DEFAULT NULL::bigint, p_etag text DEFAULT NULL::text, p_last_modified text DEFAULT NULL::text, p_next_fetch_at timestamp with time zone DEFAULT NULL::timestamp with time zone)
 RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_content_type text, last_body_bytes bigint, last_success_at timestamp with time zone, next_fetch_at timestamp with time zone)
 LANGUAGE plpgsql
AS $function$
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
$function$;



CREATE OR REPLACE FUNCTION frontier.release_parse_pending_to_queued(p_url_id bigint, p_now timestamp with time zone DEFAULT now())
 RETURNS TABLE(url_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, next_fetch_at timestamp with time zone, updated_at timestamp with time zone)
 LANGUAGE plpgsql
AS $function$
BEGIN
  IF p_url_id IS NULL THEN
    RAISE EXCEPTION 'p_url_id must not be null';
  END IF;

  RETURN QUERY
  WITH candidate AS (
    SELECT
      u.url_id,
      u.state AS previous_state,
      u.next_fetch_at
    FROM frontier.url u
    WHERE u.url_id = p_url_id
      AND u.state = 'parse_pending'
    FOR UPDATE OF u
  ),
  updated_url AS (
    UPDATE frontier.url u
       SET state = 'queued',
           updated_at = p_now
      FROM candidate c
     WHERE u.url_id = c.url_id
     RETURNING
       u.url_id,
       c.previous_state,
       u.state,
       u.next_fetch_at,
       u.updated_at
  )
  SELECT
    uu.url_id,
    uu.previous_state,
    uu.state,
    uu.next_fetch_at,
    uu.updated_at
  FROM updated_url uu;
END;
$function$;


CREATE OR REPLACE FUNCTION frontier.finish_fetch_retryable_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT NULL::integer, p_error_class text DEFAULT 'retryable_error'::text, p_error_message text DEFAULT NULL::text, p_retry_delay interval DEFAULT NULL::interval)
 RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_error_class text, last_error_message text, next_fetch_at timestamp with time zone, host_backoff_until timestamp with time zone)
 LANGUAGE plpgsql
AS $function$
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
$function$;


CREATE OR REPLACE FUNCTION frontier.finish_fetch_permanent_error(p_url_id bigint, p_lease_token uuid, p_now timestamp with time zone DEFAULT now(), p_http_status integer DEFAULT NULL::integer, p_error_class text DEFAULT 'permanent_error'::text, p_error_message text DEFAULT NULL::text)
 RETURNS TABLE(url_id bigint, host_id bigint, previous_state frontier.url_state_enum, new_state frontier.url_state_enum, last_http_status integer, last_error_class text, last_error_message text, permanent_error_count integer, consecutive_error_count integer)
 LANGUAGE plpgsql
AS $function$
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
$function$;


