\set ON_ERROR_STOP on

-- EN
-- Minimal durable crawler runtime control truth.
-- The table is the durable source of truth.
-- Operators should use functions, not direct table writes.
--
-- Current sealed states:
--   run | pause | stop
--
-- Safety:
--   default state is stop
--   control changes are made through SECURITY DEFINER functions
--   runtime readers also use controlled functions
--
-- TR
-- Minimal kalıcı crawler runtime kontrol doğrusu.
-- Tablo kalıcı kaynak doğrudur.
-- Operatörler doğrudan tablo yazımı yerine fonksiyonları kullanmalıdır.
--
-- Güncel mühürlü durumlar:
--   run | pause | stop
--
-- Güvenlik:
--   varsayılan durum stop'tur
--   kontrol değişimleri SECURITY DEFINER fonksiyonlarıyla yapılır
--   runtime okuyucular da kontrollü fonksiyonlar kullanır

CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS ops.webcrawler_runtime_control (
    control_id smallint NOT NULL,
    desired_state text NOT NULL,
    state_reason text,
    requested_by text NOT NULL,
    state_version integer NOT NULL DEFAULT 1,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT webcrawler_runtime_control_pkey PRIMARY KEY (control_id),
    CONSTRAINT chk_webcrawler_runtime_control_singleton
        CHECK (control_id = 1),
    CONSTRAINT chk_webcrawler_runtime_control_state
        CHECK (desired_state IN ('run', 'pause', 'stop')),
    CONSTRAINT chk_webcrawler_runtime_control_requested_by_not_blank
        CHECK (btrim(requested_by) <> '')
);

COMMENT ON TABLE ops.webcrawler_runtime_control IS
'Singleton durable crawler runtime control truth for LogisticSearch webcrawler.';

COMMENT ON COLUMN ops.webcrawler_runtime_control.desired_state IS
'Current durable operator-requested runtime state: run | pause | stop.';

COMMENT ON COLUMN ops.webcrawler_runtime_control.state_reason IS
'Optional human-readable explanation for the latest control-state request.';

COMMENT ON COLUMN ops.webcrawler_runtime_control.requested_by IS
'Explicit operator or helper identity that wrote the current durable state.';

COMMENT ON COLUMN ops.webcrawler_runtime_control.state_version IS
'Monotonic version increased on each control-state change.';

INSERT INTO ops.webcrawler_runtime_control (
    control_id,
    desired_state,
    state_reason,
    requested_by
)
VALUES (
    1,
    'stop',
    'default_safe_boot_state',
    'system'
)
ON CONFLICT ON CONSTRAINT webcrawler_runtime_control_pkey DO NOTHING;

CREATE OR REPLACE FUNCTION ops.get_webcrawler_runtime_control()
RETURNS TABLE (
    control_id smallint,
    desired_state text,
    state_reason text,
    requested_by text,
    state_version integer,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, ops
AS $function$
BEGIN
    INSERT INTO ops.webcrawler_runtime_control (
        control_id,
        desired_state,
        state_reason,
        requested_by
    )
    VALUES (
        1,
        'stop',
        'default_safe_boot_state',
        'system'
    )
    ON CONFLICT ON CONSTRAINT webcrawler_runtime_control_pkey DO NOTHING;

    RETURN QUERY
    SELECT
        c.control_id,
        c.desired_state,
        c.state_reason,
        c.requested_by,
        c.state_version,
        c.created_at,
        c.updated_at
    FROM ops.webcrawler_runtime_control AS c
    WHERE c.control_id = 1;
END;
$function$;

CREATE OR REPLACE FUNCTION ops.set_webcrawler_runtime_control(
    p_desired_state text,
    p_requested_by text,
    p_state_reason text DEFAULT NULL
)
RETURNS TABLE (
    control_id smallint,
    desired_state text,
    state_reason text,
    requested_by text,
    state_version integer,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, ops
AS $function$
BEGIN
    IF p_desired_state IS NULL OR btrim(p_desired_state) = '' THEN
        RAISE EXCEPTION 'p_desired_state must be non-empty';
    END IF;

    IF p_desired_state NOT IN ('run', 'pause', 'stop') THEN
        RAISE EXCEPTION 'p_desired_state must be one of: run, pause, stop';
    END IF;

    IF p_requested_by IS NULL OR btrim(p_requested_by) = '' THEN
        RAISE EXCEPTION 'p_requested_by must be non-empty';
    END IF;

    RETURN QUERY
    INSERT INTO ops.webcrawler_runtime_control AS c (
        control_id,
        desired_state,
        state_reason,
        requested_by,
        state_version,
        created_at,
        updated_at
    )
    VALUES (
        1,
        p_desired_state,
        p_state_reason,
        p_requested_by,
        1,
        now(),
        now()
    )
    ON CONFLICT ON CONSTRAINT webcrawler_runtime_control_pkey
    DO UPDATE
       SET desired_state = EXCLUDED.desired_state,
           state_reason = EXCLUDED.state_reason,
           requested_by = EXCLUDED.requested_by,
           state_version = c.state_version + 1,
           updated_at = now()
    RETURNING
        c.control_id,
        c.desired_state,
        c.state_reason,
        c.requested_by,
        c.state_version,
        c.created_at,
        c.updated_at;
END;
$function$;

CREATE OR REPLACE FUNCTION ops.webcrawler_runtime_may_claim()
RETURNS TABLE (
    desired_state text,
    may_claim boolean,
    state_version integer,
    state_reason text,
    requested_by text,
    updated_at timestamp with time zone
)
LANGUAGE sql
SECURITY DEFINER
SET search_path = pg_catalog, ops
AS $function$
    SELECT
        c.desired_state,
        (c.desired_state = 'run') AS may_claim,
        c.state_version,
        c.state_reason,
        c.requested_by,
        c.updated_at
    FROM ops.get_webcrawler_runtime_control() AS c;
$function$;

REVOKE ALL ON ops.webcrawler_runtime_control FROM PUBLIC;
GRANT SELECT ON ops.webcrawler_runtime_control TO makpi51;

REVOKE ALL ON FUNCTION ops.get_webcrawler_runtime_control() FROM PUBLIC;
REVOKE ALL ON FUNCTION ops.set_webcrawler_runtime_control(text, text, text) FROM PUBLIC;
REVOKE ALL ON FUNCTION ops.webcrawler_runtime_may_claim() FROM PUBLIC;

GRANT USAGE ON SCHEMA ops TO makpi51;
GRANT EXECUTE ON FUNCTION ops.get_webcrawler_runtime_control() TO makpi51;
GRANT EXECUTE ON FUNCTION ops.set_webcrawler_runtime_control(text, text, text) TO makpi51;
GRANT EXECUTE ON FUNCTION ops.webcrawler_runtime_may_claim() TO makpi51;
