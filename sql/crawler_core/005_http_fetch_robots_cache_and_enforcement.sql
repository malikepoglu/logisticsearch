-- Derived from live Pi51 crawler-core function definitions

CREATE OR REPLACE FUNCTION http_fetch.upsert_robots_txt_cache(p_host_id bigint, p_robots_url text, p_cache_state http_fetch.robots_cache_state_enum, p_http_status integer DEFAULT NULL::integer, p_fetched_at timestamp with time zone DEFAULT now(), p_expires_at timestamp with time zone DEFAULT NULL::timestamp with time zone, p_etag text DEFAULT NULL::text, p_last_modified text DEFAULT NULL::text, p_raw_storage_path text DEFAULT NULL::text, p_raw_sha256 text DEFAULT NULL::text, p_raw_bytes bigint DEFAULT NULL::bigint, p_parsed_rules jsonb DEFAULT '{}'::jsonb, p_sitemap_urls jsonb DEFAULT '[]'::jsonb, p_crawl_delay_seconds numeric DEFAULT NULL::numeric, p_error_class text DEFAULT NULL::text, p_error_message text DEFAULT NULL::text, p_robots_metadata jsonb DEFAULT '{}'::jsonb)
 RETURNS TABLE(robots_cache_id bigint, host_id bigint, robots_url text, cache_state http_fetch.robots_cache_state_enum, http_status integer, fetched_at timestamp with time zone, expires_at timestamp with time zone, etag text, last_modified text, crawl_delay_seconds numeric, error_class text, error_message text)
 LANGUAGE plpgsql
AS $function$
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
$function$;


CREATE OR REPLACE FUNCTION http_fetch.compute_robots_refresh_decision(p_host_id bigint, p_now timestamp with time zone DEFAULT now())
 RETURNS TABLE(host_id bigint, robots_url text, cache_exists boolean, cache_state http_fetch.robots_cache_state_enum, fetched_at timestamp with time zone, expires_at timestamp with time zone, should_refresh boolean, refresh_reason text)
 LANGUAGE plpgsql
AS $function$
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
$function$;


CREATE OR REPLACE FUNCTION http_fetch.compute_robots_allow_decision(p_host_id bigint, p_url_path text)
 RETURNS TABLE(host_id bigint, url_path text, robots_mode frontier.robots_mode_enum, cache_exists boolean, cache_state http_fetch.robots_cache_state_enum, matched_rule text, verdict http_fetch.robots_verdict_enum, decision_reason text)
 LANGUAGE plpgsql
AS $function$
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
$function$;


