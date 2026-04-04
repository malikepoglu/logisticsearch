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

\unrestrict SnMYbWdXZK3obuHYdei6inDhVltfGsO0kThQRXKhKZyJF0dsEwQn4oxq6NGYfjJ

