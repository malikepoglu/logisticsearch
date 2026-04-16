-- SECTION1_WEBCRAWLER_CRAWLER_CORE_DISCOVERY_ENQUEUE_MINIMAL
-- EN
-- Minimal discovery enqueue surface for crawler_core.
-- Hard rules:
-- 1) host.authority_key is generated truth, so we must not insert it directly
-- 2) url.canonical_url_sha256 is generated truth, so we must not insert it directly
-- 3) parent source/seed identity must be inherited from the parent URL
-- 4) leased/parse_pending rows must not be force-reset during discovery upsert
-- 5) this surface is intentionally minimal and HTML-link oriented
--
-- TR
-- crawler_core için minimal discovery enqueue yüzeyi.
-- Sert kurallar:
-- 1) host.authority_key generated doğruluktur; bu yüzden doğrudan insert edilmemelidir
-- 2) url.canonical_url_sha256 generated doğruluktur; bu yüzden doğrudan insert edilmemelidir
-- 3) parent source/seed kimliği parent URL'den miras alınmalıdır
-- 4) discovery upsert sırasında leased/parse_pending satırları zorla sıfırlanmamalıdır
-- 5) bu yüzey bilinçli olarak minimaldir ve html-link odaklıdır

DROP FUNCTION IF EXISTS frontier.enqueue_discovered_url(
    bigint,
    text,
    text,
    integer,
    text,
    text,
    text,
    text,
    text,
    text,
    frontier.discovery_type_enum,
    integer,
    integer,
    text
);

CREATE FUNCTION frontier.enqueue_discovered_url(
    p_parent_url_id bigint,
    p_canonical_url text,
    p_canonical_url_sha256 text,
    p_port integer,
    p_scheme text,
    p_host text,
    p_authority_key text,
    p_registrable_domain text,
    p_url_path text,
    p_url_query text,
    p_discovery_type frontier.discovery_type_enum,
    p_depth integer,
    p_priority integer DEFAULT NULL,
    p_enqueue_reason text DEFAULT NULL
)
RETURNS TABLE(
    url_id bigint,
    host_id bigint,
    canonical_url text,
    state frontier.url_state_enum,
    discovery_type frontier.discovery_type_enum,
    depth integer,
    priority integer
)
LANGUAGE plpgsql
AS $function$
DECLARE
    v_parent_url frontier.url%ROWTYPE;
    v_parent_host frontier.host%ROWTYPE;
    v_host_id bigint;
    v_effective_priority integer;
BEGIN
    IF p_parent_url_id IS NULL OR p_parent_url_id <= 0 THEN
        RAISE EXCEPTION 'p_parent_url_id must be > 0';
    END IF;

    IF p_canonical_url IS NULL OR btrim(p_canonical_url) = '' THEN
        RAISE EXCEPTION 'p_canonical_url must be non-empty';
    END IF;

    IF p_scheme IS NULL OR btrim(p_scheme) = '' THEN
        RAISE EXCEPTION 'p_scheme must be non-empty';
    END IF;

    IF p_host IS NULL OR btrim(p_host) = '' THEN
        RAISE EXCEPTION 'p_host must be non-empty';
    END IF;

    IF p_port IS NULL OR p_port <= 0 THEN
        RAISE EXCEPTION 'p_port must be > 0';
    END IF;

    IF p_url_path IS NULL OR btrim(p_url_path) = '' THEN
        RAISE EXCEPTION 'p_url_path must be non-empty';
    END IF;

    IF p_discovery_type IS NULL THEN
        RAISE EXCEPTION 'p_discovery_type must not be null';
    END IF;

    IF p_depth IS NULL OR p_depth < 0 THEN
        RAISE EXCEPTION 'p_depth must be >= 0';
    END IF;

    -- EN: The caller still passes these values for compatibility with the
    -- EN: current narrow Python bridge, but generated columns remain the real truth.
    -- TR: Çağıran taraf mevcut dar Python köprüsüyle uyumluluk için bu değerleri
    -- TR: hâlâ geçirir; ancak gerçek doğruluk generated sütunlardadır.
    PERFORM p_canonical_url_sha256;
    PERFORM p_authority_key;

    SELECT parent_u.*
    INTO v_parent_url
    FROM frontier.url AS parent_u
    WHERE parent_u.url_id = p_parent_url_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'parent frontier.url row not found for url_id=%', p_parent_url_id;
    END IF;

    SELECT parent_h.*
    INTO v_parent_host
    FROM frontier.host AS parent_h
    WHERE parent_h.host_id = v_parent_url.host_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'parent frontier.host row not found for host_id=%', v_parent_url.host_id;
    END IF;

    v_effective_priority := COALESCE(p_priority, v_parent_url.priority, 0);

    INSERT INTO frontier.host AS h (
        scheme,
        host,
        port,
        registrable_domain,
        user_agent_token
    )
    VALUES (
        lower(p_scheme),
        lower(p_host),
        p_port,
        lower(COALESCE(NULLIF(p_registrable_domain, ''), p_host)),
        COALESCE(v_parent_host.user_agent_token, 'LogisticSearchBot')
    )
    ON CONFLICT (authority_key)
    DO UPDATE
       SET registrable_domain = EXCLUDED.registrable_domain,
           updated_at = now()
    RETURNING h.host_id
    INTO v_host_id;

    RETURN QUERY
    WITH upserted AS (
        INSERT INTO frontier.url AS u (
            host_id,
            canonical_url,
            url_path,
            url_query,
            source_id,
            seed_id,
            discovery_type,
            parent_url_id,
            depth,
            is_seed,
            state,
            priority,
            score,
            enqueue_reason,
            first_seen_at,
            last_seen_at,
            last_enqueued_at,
            next_fetch_at
        )
        VALUES (
            v_host_id,
            p_canonical_url,
            p_url_path,
            p_url_query,
            v_parent_url.source_id,
            v_parent_url.seed_id,
            p_discovery_type,
            p_parent_url_id,
            p_depth,
            false,
            'queued'::frontier.url_state_enum,
            v_effective_priority,
            0,
            p_enqueue_reason,
            now(),
            now(),
            now(),
            now()
        )
        ON CONFLICT (canonical_url_sha256)
        DO UPDATE
           SET host_id = EXCLUDED.host_id,
               parent_url_id = COALESCE(u.parent_url_id, EXCLUDED.parent_url_id),
               source_id = COALESCE(u.source_id, EXCLUDED.source_id),
               seed_id = COALESCE(u.seed_id, EXCLUDED.seed_id),
               depth = LEAST(u.depth, EXCLUDED.depth),
               priority = GREATEST(u.priority, EXCLUDED.priority),
               enqueue_reason = EXCLUDED.enqueue_reason,
               last_seen_at = now(),
               last_enqueued_at = CASE
                   WHEN u.state IN ('leased'::frontier.url_state_enum, 'parse_pending'::frontier.url_state_enum)
                       THEN u.last_enqueued_at
                   ELSE now()
               END,
               next_fetch_at = CASE
                   WHEN u.state IN ('leased'::frontier.url_state_enum, 'parse_pending'::frontier.url_state_enum)
                       THEN u.next_fetch_at
                   ELSE now()
               END,
               state = CASE
                   WHEN u.state IN ('leased'::frontier.url_state_enum, 'parse_pending'::frontier.url_state_enum)
                       THEN u.state
                   ELSE 'queued'::frontier.url_state_enum
               END,
               updated_at = now()
        RETURNING
            u.url_id,
            u.canonical_url,
            u.state,
            u.discovery_type,
            u.depth,
            u.priority
    )
    SELECT
        upserted.url_id,
        v_host_id,
        upserted.canonical_url,
        upserted.state,
        upserted.discovery_type,
        upserted.depth,
        upserted.priority
    FROM upserted;
END;
$function$;

GRANT EXECUTE ON FUNCTION frontier.enqueue_discovered_url(
    bigint,
    text,
    text,
    integer,
    text,
    text,
    text,
    text,
    text,
    text,
    frontier.discovery_type_enum,
    integer,
    integer,
    text
) TO makpi51;
