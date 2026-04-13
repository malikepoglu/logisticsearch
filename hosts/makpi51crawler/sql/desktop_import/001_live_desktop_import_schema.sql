--
-- PostgreSQL database dump
--

\restrict 6tPPrFBqxtfn9jofaeLd63uS1360kJchVPnlk2tB9Xmr6t5UnYk80O3hV31affh

-- Dumped from database version 18.3 (Ubuntu 18.3-1.pgdg24.04+1)
-- Dumped by pg_dump version 18.3 (Ubuntu 18.3-1.pgdg24.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: desktop_import; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA desktop_import;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: batch_intake; Type: TABLE; Schema: desktop_import; Owner: -
--

CREATE TABLE desktop_import.batch_intake (
    batch_key text NOT NULL,
    export_channel text NOT NULL,
    source_system text DEFAULT 'pi51'::text NOT NULL,
    source_repo_relpath text NOT NULL,
    source_repo_head text,
    source_commit_from_push_receipt text,
    item_count_expected integer NOT NULL,
    item_count_loaded integer NOT NULL,
    batch_payload_sha256 text NOT NULL,
    imported_at_utc timestamp with time zone NOT NULL,
    manifest_json jsonb NOT NULL,
    push_receipt_json jsonb NOT NULL,
    import_receipt_json jsonb NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_export_raw; Type: TABLE; Schema: desktop_import; Owner: -
--

CREATE TABLE desktop_import.page_export_raw (
    intake_row_id bigint NOT NULL,
    batch_key text NOT NULL,
    item_ordinal integer NOT NULL,
    export_item_id bigint,
    source_url_id bigint,
    source_snapshot_id bigint,
    canonical_url text,
    input_lang_code text,
    taxonomy_package_version text,
    top_candidate_count integer,
    top_score numeric,
    raw_item_json jsonb NOT NULL,
    raw_payload_json jsonb NOT NULL,
    imported_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_export_raw_intake_row_id_seq; Type: SEQUENCE; Schema: desktop_import; Owner: -
--

CREATE SEQUENCE desktop_import.page_export_raw_intake_row_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_export_raw_intake_row_id_seq; Type: SEQUENCE OWNED BY; Schema: desktop_import; Owner: -
--

ALTER SEQUENCE desktop_import.page_export_raw_intake_row_id_seq OWNED BY desktop_import.page_export_raw.intake_row_id;


--
-- Name: page_export_raw intake_row_id; Type: DEFAULT; Schema: desktop_import; Owner: -
--

ALTER TABLE ONLY desktop_import.page_export_raw ALTER COLUMN intake_row_id SET DEFAULT nextval('desktop_import.page_export_raw_intake_row_id_seq'::regclass);


--
-- Name: batch_intake batch_intake_pkey; Type: CONSTRAINT; Schema: desktop_import; Owner: -
--

ALTER TABLE ONLY desktop_import.batch_intake
    ADD CONSTRAINT batch_intake_pkey PRIMARY KEY (batch_key);


--
-- Name: page_export_raw desktop_import_page_export_raw_batch_ordinal_uniq; Type: CONSTRAINT; Schema: desktop_import; Owner: -
--

ALTER TABLE ONLY desktop_import.page_export_raw
    ADD CONSTRAINT desktop_import_page_export_raw_batch_ordinal_uniq UNIQUE (batch_key, item_ordinal);


--
-- Name: page_export_raw page_export_raw_pkey; Type: CONSTRAINT; Schema: desktop_import; Owner: -
--

ALTER TABLE ONLY desktop_import.page_export_raw
    ADD CONSTRAINT page_export_raw_pkey PRIMARY KEY (intake_row_id);


--
-- Name: desktop_import_page_export_raw_batch_idx; Type: INDEX; Schema: desktop_import; Owner: -
--

CREATE INDEX desktop_import_page_export_raw_batch_idx ON desktop_import.page_export_raw USING btree (batch_key);


--
-- Name: desktop_import_page_export_raw_export_item_idx; Type: INDEX; Schema: desktop_import; Owner: -
--

CREATE INDEX desktop_import_page_export_raw_export_item_idx ON desktop_import.page_export_raw USING btree (export_item_id);


--
-- Name: desktop_import_page_export_raw_source_url_idx; Type: INDEX; Schema: desktop_import; Owner: -
--

CREATE INDEX desktop_import_page_export_raw_source_url_idx ON desktop_import.page_export_raw USING btree (source_url_id);


--
-- Name: page_export_raw page_export_raw_batch_key_fkey; Type: FK CONSTRAINT; Schema: desktop_import; Owner: -
--

ALTER TABLE ONLY desktop_import.page_export_raw
    ADD CONSTRAINT page_export_raw_batch_key_fkey FOREIGN KEY (batch_key) REFERENCES desktop_import.batch_intake(batch_key) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 6tPPrFBqxtfn9jofaeLd63uS1360kJchVPnlk2tB9Xmr6t5UnYk80O3hV31affh

