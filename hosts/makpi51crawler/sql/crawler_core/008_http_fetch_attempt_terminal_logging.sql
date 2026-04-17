-- EN
-- This surface adds the first canonical durable fetch-attempt write entry point.
-- The current live crawler proves that raw files can be written and frontier state can move,
-- but http_fetch.fetch_attempt is still empty in live production truth.
-- That means crawler_core currently lacks durable per-attempt fetch logging.
--
-- This function is intentionally terminal-only:
-- - it writes one completed fetch-attempt row
-- - it does not mutate frontier state
-- - it does not try to model a separate "begin" row yet
-- - it forbids outcome = 'in_progress'
--
-- The goal is to create the smallest safe canonical write surface that the live worker
-- can call on both success and failure paths before we add broader fetch-lifecycle detail.
--
-- TR
-- Bu yüzey ilk kanonik kalıcı fetch-attempt yazma giriş noktasını ekler.
-- Mevcut canlı crawler, ham dosya yazabildiğini ve frontier durumunu ilerletebildiğini
-- kanıtlıyor; fakat http_fetch.fetch_attempt canlı üretim gerçeğinde hâlâ boş.
-- Bu da crawler_core içinde kalıcı deneme-bazlı fetch loglamasının eksik olduğunu gösterir.
--
-- Bu fonksiyon bilinçli olarak yalnızca terminal kayıt içindir:
-- - tek bir tamamlanmış fetch-attempt satırı yazar
-- - frontier durumunu değiştirmez
-- - şimdilik ayrı bir "begin" satırı modellemeye çalışmaz
-- - outcome = 'in_progress' değerini yasaklar
--
-- Amaç, canlı worker'ın hem başarı hem hata yollarında çağırabileceği,
-- daha geniş fetch yaşam döngüsü ayrıntılarını eklemeden önceki en küçük güvenli
-- kanonik write surface'i oluşturmaktır.

CREATE OR REPLACE FUNCTION http_fetch.log_fetch_attempt_terminal(
    p_url_id bigint,
    p_host_id bigint,
    p_worker_id text,
    p_request_url text,
    p_outcome http_fetch.fetch_outcome_enum,

    p_fetch_kind http_fetch.fetch_kind_enum DEFAULT 'page'::http_fetch.fetch_kind_enum,
    p_lease_token uuid DEFAULT NULL,
    p_worker_run_id uuid DEFAULT NULL,
    p_request_method text DEFAULT 'GET',
    p_final_url text DEFAULT NULL,
    p_request_headers jsonb DEFAULT '{}'::jsonb,
    p_response_headers jsonb DEFAULT '{}'::jsonb,
    p_started_at timestamp with time zone DEFAULT now(),
    p_first_byte_at timestamp with time zone DEFAULT NULL,
    p_ended_at timestamp with time zone DEFAULT now(),
    p_http_status integer DEFAULT NULL,
    p_remote_ip inet DEFAULT NULL,
    p_redirect_location text DEFAULT NULL,
    p_content_type text DEFAULT NULL,
    p_content_encoding text DEFAULT NULL,
    p_content_length bigint DEFAULT NULL,
    p_body_storage_path text DEFAULT NULL,
    p_body_sha256 text DEFAULT NULL,
    p_body_bytes bigint DEFAULT NULL,
    p_etag text DEFAULT NULL,
    p_last_modified text DEFAULT NULL,
    p_retry_after_seconds integer DEFAULT NULL,
    p_error_class text DEFAULT NULL,
    p_error_message text DEFAULT NULL,
    p_fetch_metadata jsonb DEFAULT '{}'::jsonb
)
RETURNS SETOF http_fetch.fetch_attempt
LANGUAGE plpgsql
AS $function$
BEGIN
    -- EN: host_id is mandatory because fetch_attempt is always anchored to one host truth row.
    -- TR: fetch_attempt her zaman tek bir host truth satırına bağlı olduğu için host_id zorunludur.
    IF p_host_id IS NULL THEN
        RAISE EXCEPTION 'p_host_id must not be null';
    END IF;

    -- EN: worker identity must stay explicit so later audits can tell which worker wrote the row.
    -- TR: Daha sonraki denetimler satırı hangi worker'ın yazdığını anlayabilsin diye worker kimliği açık olmalıdır.
    IF p_worker_id IS NULL OR btrim(p_worker_id) = '' THEN
        RAISE EXCEPTION 'p_worker_id must not be null or empty';
    END IF;

    -- EN: request URL must be explicit because it is the operator-visible fetch target.
    -- TR: request URL, operatörün görebildiği fetch hedefi olduğu için açık olmalıdır.
    IF p_request_url IS NULL OR btrim(p_request_url) = '' THEN
        RAISE EXCEPTION 'p_request_url must not be null or empty';
    END IF;

    -- EN: This surface is terminal-only by design. The live gap is missing durable completed rows.
    -- TR: Bu yüzey tasarım gereği yalnızca terminal kayıttır. Canlı boşluk, kalıcı tamamlanmış satır eksikliğidir.
    IF p_outcome = 'in_progress'::http_fetch.fetch_outcome_enum THEN
        RAISE EXCEPTION 'p_outcome must be terminal, not in_progress';
    END IF;

    -- EN: End time must not move backwards relative to start time.
    -- TR: Bitiş zamanı başlangıç zamanına göre geriye gitmemelidir.
    IF p_started_at IS NOT NULL
       AND p_ended_at IS NOT NULL
       AND p_ended_at < p_started_at THEN
        RAISE EXCEPTION 'p_ended_at must be greater than or equal to p_started_at';
    END IF;

    -- EN: We insert one durable terminal row and return the exact stored record.
    -- TR: Tek bir kalıcı terminal satır ekliyor ve tam saklanan kaydı geri döndürüyoruz.
    RETURN QUERY
    INSERT INTO http_fetch.fetch_attempt (
        url_id,
        host_id,
        fetch_kind,
        lease_token,
        worker_id,
        worker_run_id,
        request_method,
        request_url,
        final_url,
        request_headers,
        response_headers,
        started_at,
        first_byte_at,
        ended_at,
        outcome,
        http_status,
        remote_ip,
        redirect_location,
        content_type,
        content_encoding,
        content_length,
        body_storage_path,
        body_sha256,
        body_bytes,
        etag,
        last_modified,
        retry_after_seconds,
        error_class,
        error_message,
        fetch_metadata
    )
    VALUES (
        p_url_id,
        p_host_id,
        COALESCE(p_fetch_kind, 'page'::http_fetch.fetch_kind_enum),
        p_lease_token,
        p_worker_id,
        p_worker_run_id,
        COALESCE(NULLIF(btrim(p_request_method), ''), 'GET'),
        p_request_url,
        COALESCE(NULLIF(p_final_url, ''), p_request_url),
        COALESCE(p_request_headers, '{}'::jsonb),
        COALESCE(p_response_headers, '{}'::jsonb),
        COALESCE(p_started_at, now()),
        p_first_byte_at,
        COALESCE(p_ended_at, COALESCE(p_first_byte_at, p_started_at, now())),
        p_outcome,
        p_http_status,
        p_remote_ip,
        p_redirect_location,
        p_content_type,
        p_content_encoding,
        p_content_length,
        p_body_storage_path,
        p_body_sha256,
        p_body_bytes,
        p_etag,
        p_last_modified,
        p_retry_after_seconds,
        p_error_class,
        p_error_message,
        COALESCE(p_fetch_metadata, '{}'::jsonb)
    )
    RETURNING *;
END;
$function$;

-- EN
-- This comment keeps the operational purpose explicit in schema-level introspection.
--
-- TR
-- Bu yorum, operasyonel amacı şema-seviyesi incelemede açık tutar.
COMMENT ON FUNCTION http_fetch.log_fetch_attempt_terminal(
    bigint,
    bigint,
    text,
    text,
    http_fetch.fetch_outcome_enum,
    http_fetch.fetch_kind_enum,
    uuid,
    uuid,
    text,
    text,
    jsonb,
    jsonb,
    timestamp with time zone,
    timestamp with time zone,
    timestamp with time zone,
    integer,
    inet,
    text,
    text,
    text,
    bigint,
    text,
    text,
    bigint,
    text,
    text,
    integer,
    text,
    text,
    jsonb
) IS
'Records one completed durable http_fetch.fetch_attempt row without mutating frontier state. Terminal-only logging surface for live worker success/failure paths.';
