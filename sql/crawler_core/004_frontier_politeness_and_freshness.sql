-- Derived from live Pi51 crawler-core function definitions

CREATE OR REPLACE FUNCTION frontier.compute_retry_backoff(p_host_id bigint, p_consecutive_error_count integer, p_now timestamp with time zone DEFAULT now())
 RETURNS TABLE(retry_delay interval, retry_at timestamp with time zone, base_ms integer, cap_ms integer, exponent integer, raw_ms numeric, effective_ms numeric)
 LANGUAGE plpgsql
AS $function$
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
$function$;


CREATE OR REPLACE FUNCTION frontier.compute_success_next_fetch_at(p_url_id bigint, p_now timestamp with time zone DEFAULT now())
 RETURNS TABLE(next_fetch_at timestamp with time zone, base_interval interval, jitter_pct smallint, jitter_factor numeric, source_reason text)
 LANGUAGE plpgsql
AS $function$
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
$function$;


