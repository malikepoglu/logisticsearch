--
-- PostgreSQL database dump
--


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
-- Name: outbox; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA outbox;


--
-- Name: batch_state_enum; Type: TYPE; Schema: outbox; Owner: -
--

CREATE TYPE outbox.batch_state_enum AS ENUM (
    'materialized',
    'pushed',
    'failed'
);


--
-- Name: export_state_enum; Type: TYPE; Schema: outbox; Owner: -
--

CREATE TYPE outbox.export_state_enum AS ENUM (
    'queued',
    'materialized',
    'failed',
    'pushed'
);


--

-- Name: export_batch; Type: TABLE; Schema: outbox; Owner: -
--

CREATE TABLE outbox.export_batch (
    batch_id bigint NOT NULL,
    export_channel text NOT NULL,
    batch_key text NOT NULL,
    batch_state outbox.batch_state_enum DEFAULT 'materialized'::outbox.batch_state_enum NOT NULL,
    item_count integer DEFAULT 0 NOT NULL,
    payload_sha256 text NOT NULL,
    manifest jsonb NOT NULL,
    storage_relpath text NOT NULL,
    source_run_id text,
    source_note text,
    batch_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: export_batch_batch_id_seq; Type: SEQUENCE; Schema: outbox; Owner: -
--

CREATE SEQUENCE outbox.export_batch_batch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: export_batch_batch_id_seq; Type: SEQUENCE OWNED BY; Schema: outbox; Owner: -
--

ALTER SEQUENCE outbox.export_batch_batch_id_seq OWNED BY outbox.export_batch.batch_id;


--
-- Name: export_batch_item; Type: TABLE; Schema: outbox; Owner: -
--

CREATE TABLE outbox.export_batch_item (
    batch_item_id bigint NOT NULL,
    batch_id bigint NOT NULL,
    export_item_id bigint NOT NULL,
    source_run_id text,
    source_note text,
    item_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: export_batch_item_batch_item_id_seq; Type: SEQUENCE; Schema: outbox; Owner: -
--

CREATE SEQUENCE outbox.export_batch_item_batch_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: export_batch_item_batch_item_id_seq; Type: SEQUENCE OWNED BY; Schema: outbox; Owner: -
--

ALTER SEQUENCE outbox.export_batch_item_batch_item_id_seq OWNED BY outbox.export_batch_item.batch_item_id;


--
-- Name: page_export_item; Type: TABLE; Schema: outbox; Owner: -
--

CREATE TABLE outbox.page_export_item (
    export_item_id bigint NOT NULL,
    url_id bigint NOT NULL,
    snapshot_id bigint NOT NULL,
    workflow_status_id bigint NOT NULL,
    export_channel text DEFAULT 'github_batch_v1'::text NOT NULL,
    export_state outbox.export_state_enum DEFAULT 'queued'::outbox.export_state_enum NOT NULL,
    payload jsonb NOT NULL,
    payload_sha256 text NOT NULL,
    source_run_id text,
    source_note text,
    export_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_export_item_export_item_id_seq; Type: SEQUENCE; Schema: outbox; Owner: -
--

CREATE SEQUENCE outbox.page_export_item_export_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_export_item_export_item_id_seq; Type: SEQUENCE OWNED BY; Schema: outbox; Owner: -
--

ALTER SEQUENCE outbox.page_export_item_export_item_id_seq OWNED BY outbox.page_export_item.export_item_id;


--
-- Name: export_batch batch_id; Type: DEFAULT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch ALTER COLUMN batch_id SET DEFAULT nextval('outbox.export_batch_batch_id_seq'::regclass);


--
-- Name: export_batch_item batch_item_id; Type: DEFAULT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch_item ALTER COLUMN batch_item_id SET DEFAULT nextval('outbox.export_batch_item_batch_item_id_seq'::regclass);


--
-- Name: page_export_item export_item_id; Type: DEFAULT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item ALTER COLUMN export_item_id SET DEFAULT nextval('outbox.page_export_item_export_item_id_seq'::regclass);


--
-- Name: export_batch_item export_batch_item_pkey; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch_item
    ADD CONSTRAINT export_batch_item_pkey PRIMARY KEY (batch_item_id);


--
-- Name: export_batch export_batch_pkey; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch
    ADD CONSTRAINT export_batch_pkey PRIMARY KEY (batch_id);


--
-- Name: export_batch outbox_export_batch_batch_key_uniq; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch
    ADD CONSTRAINT outbox_export_batch_batch_key_uniq UNIQUE (batch_key);


--
-- Name: export_batch_item outbox_export_batch_item_export_item_uniq; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch_item
    ADD CONSTRAINT outbox_export_batch_item_export_item_uniq UNIQUE (export_item_id);


--
-- Name: page_export_item outbox_page_export_item_url_channel_snapshot_uniq; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item
    ADD CONSTRAINT outbox_page_export_item_url_channel_snapshot_uniq UNIQUE (url_id, export_channel, snapshot_id);


--
-- Name: page_export_item page_export_item_pkey; Type: CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item
    ADD CONSTRAINT page_export_item_pkey PRIMARY KEY (export_item_id);


--
-- Name: outbox_export_batch_item_batch_idx; Type: INDEX; Schema: outbox; Owner: -
--

CREATE INDEX outbox_export_batch_item_batch_idx ON outbox.export_batch_item USING btree (batch_id);


--
-- Name: outbox_export_batch_state_idx; Type: INDEX; Schema: outbox; Owner: -
--

CREATE INDEX outbox_export_batch_state_idx ON outbox.export_batch USING btree (batch_state, export_channel);


--
-- Name: outbox_page_export_item_payload_sha_idx; Type: INDEX; Schema: outbox; Owner: -
--

CREATE INDEX outbox_page_export_item_payload_sha_idx ON outbox.page_export_item USING btree (payload_sha256);


--
-- Name: outbox_page_export_item_state_idx; Type: INDEX; Schema: outbox; Owner: -
--

CREATE INDEX outbox_page_export_item_state_idx ON outbox.page_export_item USING btree (export_state, export_channel);


--
-- Name: export_batch_item export_batch_item_batch_id_fkey; Type: FK CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch_item
    ADD CONSTRAINT export_batch_item_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES outbox.export_batch(batch_id) ON DELETE CASCADE;


--
-- Name: export_batch_item export_batch_item_export_item_id_fkey; Type: FK CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.export_batch_item
    ADD CONSTRAINT export_batch_item_export_item_id_fkey FOREIGN KEY (export_item_id) REFERENCES outbox.page_export_item(export_item_id) ON DELETE CASCADE;


--
-- Name: page_export_item page_export_item_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item
    ADD CONSTRAINT page_export_item_snapshot_id_fkey FOREIGN KEY (snapshot_id) REFERENCES parse.page_preranking_snapshot(snapshot_id) ON DELETE CASCADE;


--
-- Name: page_export_item page_export_item_url_id_fkey; Type: FK CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item
    ADD CONSTRAINT page_export_item_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_export_item page_export_item_workflow_status_id_fkey; Type: FK CONSTRAINT; Schema: outbox; Owner: -
--

ALTER TABLE ONLY outbox.page_export_item
    ADD CONSTRAINT page_export_item_workflow_status_id_fkey FOREIGN KEY (workflow_status_id) REFERENCES parse.page_workflow_status(status_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


