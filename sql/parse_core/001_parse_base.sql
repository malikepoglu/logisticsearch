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
-- Name: parse; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA parse;


--
-- Name: workflow_state_enum; Type: TYPE; Schema: parse; Owner: -
--

CREATE TYPE parse.workflow_state_enum AS ENUM (
    'pre_ranked',
    'review_hold',
    'export_ready',
    'exported',
    'discarded'
);


--
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: page_evidence_snapshot; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_evidence_snapshot (
    snapshot_id bigint NOT NULL,
    url_id bigint NOT NULL,
    input_lang_code text NOT NULL,
    url_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    title_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    h1_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    breadcrumb_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    structured_data_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    anchor_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    body_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    source_run_id text,
    source_note text,
    snapshot_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_evidence_snapshot_snapshot_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_evidence_snapshot_snapshot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_evidence_snapshot_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_evidence_snapshot_snapshot_id_seq OWNED BY parse.page_evidence_snapshot.snapshot_id;


--
-- Name: page_preranking_snapshot; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_preranking_snapshot (
    snapshot_id bigint NOT NULL,
    url_id bigint NOT NULL,
    input_lang_code text NOT NULL,
    taxonomy_package_version text,
    top_candidate_count integer DEFAULT 0 NOT NULL,
    top_score numeric,
    candidate_summary jsonb DEFAULT '[]'::jsonb NOT NULL,
    review_status text DEFAULT 'pre_ranked'::text NOT NULL,
    source_run_id text,
    source_note text,
    snapshot_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_preranking_snapshot_snapshot_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_preranking_snapshot_snapshot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_preranking_snapshot_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_preranking_snapshot_snapshot_id_seq OWNED BY parse.page_preranking_snapshot.snapshot_id;


--
-- Name: page_taxonomy_candidate; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_taxonomy_candidate (
    candidate_id bigint NOT NULL,
    url_id bigint NOT NULL,
    taxonomy_source_db text DEFAULT 'logisticsearch_taxonomy'::text NOT NULL,
    taxonomy_package_version text NOT NULL,
    taxonomy_package_id uuid NOT NULL,
    taxonomy_concept_id uuid NOT NULL,
    taxonomy_node_code text NOT NULL,
    taxonomy_concept_key text NOT NULL,
    input_lang_code text NOT NULL,
    matched_lang_codes jsonb DEFAULT '[]'::jsonb NOT NULL,
    matched_fields jsonb DEFAULT '[]'::jsonb NOT NULL,
    matched_queries jsonb DEFAULT '[]'::jsonb NOT NULL,
    domain_type text,
    node_kind text,
    url_score numeric(12,4) DEFAULT 0 NOT NULL,
    title_score numeric(12,4) DEFAULT 0 NOT NULL,
    h1_score numeric(12,4) DEFAULT 0 NOT NULL,
    breadcrumb_score numeric(12,4) DEFAULT 0 NOT NULL,
    structured_data_score numeric(12,4) DEFAULT 0 NOT NULL,
    anchor_score numeric(12,4) DEFAULT 0 NOT NULL,
    body_score numeric(12,4) DEFAULT 0 NOT NULL,
    total_score numeric(12,4) DEFAULT 0 NOT NULL,
    evidence_count integer DEFAULT 0 NOT NULL,
    confidence_band text DEFAULT 'unreviewed'::text NOT NULL,
    source_run_id text,
    source_note text,
    candidate_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_taxonomy_candidate_candidate_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_taxonomy_candidate_candidate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_taxonomy_candidate_candidate_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_taxonomy_candidate_candidate_id_seq OWNED BY parse.page_taxonomy_candidate.candidate_id;


--
-- Name: page_workflow_status; Type: TABLE; Schema: parse; Owner: -
--

CREATE TABLE parse.page_workflow_status (
    status_id bigint NOT NULL,
    url_id bigint NOT NULL,
    linked_snapshot_id bigint,
    workflow_state parse.workflow_state_enum NOT NULL,
    state_reason text,
    state_version integer DEFAULT 1 NOT NULL,
    source_run_id text,
    source_note text,
    status_metadata jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: page_workflow_status_status_id_seq; Type: SEQUENCE; Schema: parse; Owner: -
--

CREATE SEQUENCE parse.page_workflow_status_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: page_workflow_status_status_id_seq; Type: SEQUENCE OWNED BY; Schema: parse; Owner: -
--

ALTER SEQUENCE parse.page_workflow_status_status_id_seq OWNED BY parse.page_workflow_status.status_id;


--
-- Name: page_evidence_snapshot snapshot_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot ALTER COLUMN snapshot_id SET DEFAULT nextval('parse.page_evidence_snapshot_snapshot_id_seq'::regclass);


--
-- Name: page_preranking_snapshot snapshot_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot ALTER COLUMN snapshot_id SET DEFAULT nextval('parse.page_preranking_snapshot_snapshot_id_seq'::regclass);


--
-- Name: page_taxonomy_candidate candidate_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate ALTER COLUMN candidate_id SET DEFAULT nextval('parse.page_taxonomy_candidate_candidate_id_seq'::regclass);


--
-- Name: page_workflow_status status_id; Type: DEFAULT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status ALTER COLUMN status_id SET DEFAULT nextval('parse.page_workflow_status_status_id_seq'::regclass);


--
-- Name: page_evidence_snapshot page_evidence_snapshot_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT page_evidence_snapshot_pkey PRIMARY KEY (snapshot_id);


--
-- Name: page_preranking_snapshot page_preranking_snapshot_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT page_preranking_snapshot_pkey PRIMARY KEY (snapshot_id);


--
-- Name: page_taxonomy_candidate page_taxonomy_candidate_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT page_taxonomy_candidate_pkey PRIMARY KEY (candidate_id);


--
-- Name: page_workflow_status page_workflow_status_pkey; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_pkey PRIMARY KEY (status_id);


--
-- Name: page_evidence_snapshot parse_page_evidence_snapshot_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT parse_page_evidence_snapshot_url_uniq UNIQUE (url_id);


--
-- Name: page_preranking_snapshot parse_page_preranking_snapshot_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT parse_page_preranking_snapshot_url_uniq UNIQUE (url_id);


--
-- Name: page_taxonomy_candidate parse_page_taxonomy_candidate_url_pkg_concept_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT parse_page_taxonomy_candidate_url_pkg_concept_uniq UNIQUE (url_id, taxonomy_package_version, taxonomy_concept_id);


--
-- Name: page_workflow_status parse_page_workflow_status_url_uniq; Type: CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT parse_page_workflow_status_url_uniq UNIQUE (url_id);


--
-- Name: parse_page_evidence_snapshot_lang_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_evidence_snapshot_lang_idx ON parse.page_evidence_snapshot USING btree (input_lang_code);


--
-- Name: parse_page_preranking_snapshot_review_status_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_preranking_snapshot_review_status_idx ON parse.page_preranking_snapshot USING btree (review_status);


--
-- Name: parse_page_preranking_snapshot_top_score_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_preranking_snapshot_top_score_idx ON parse.page_preranking_snapshot USING btree (top_score DESC);


--
-- Name: parse_page_tax_candidate_concept_key_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_concept_key_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_concept_key);


--
-- Name: parse_page_tax_candidate_node_code_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_node_code_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_node_code);


--
-- Name: parse_page_tax_candidate_package_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_package_idx ON parse.page_taxonomy_candidate USING btree (taxonomy_package_version, total_score DESC);


--
-- Name: parse_page_tax_candidate_url_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_tax_candidate_url_idx ON parse.page_taxonomy_candidate USING btree (url_id, total_score DESC);


--
-- Name: parse_page_workflow_status_snapshot_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_workflow_status_snapshot_idx ON parse.page_workflow_status USING btree (linked_snapshot_id);


--
-- Name: parse_page_workflow_status_state_idx; Type: INDEX; Schema: parse; Owner: -
--

CREATE INDEX parse_page_workflow_status_state_idx ON parse.page_workflow_status USING btree (workflow_state);


--
-- Name: page_evidence_snapshot page_evidence_snapshot_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_evidence_snapshot
    ADD CONSTRAINT page_evidence_snapshot_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_preranking_snapshot page_preranking_snapshot_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_preranking_snapshot
    ADD CONSTRAINT page_preranking_snapshot_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_taxonomy_candidate page_taxonomy_candidate_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_taxonomy_candidate
    ADD CONSTRAINT page_taxonomy_candidate_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- Name: page_workflow_status page_workflow_status_linked_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_linked_snapshot_id_fkey FOREIGN KEY (linked_snapshot_id) REFERENCES parse.page_preranking_snapshot(snapshot_id) ON DELETE SET NULL;


--
-- Name: page_workflow_status page_workflow_status_url_id_fkey; Type: FK CONSTRAINT; Schema: parse; Owner: -
--

ALTER TABLE ONLY parse.page_workflow_status
    ADD CONSTRAINT page_workflow_status_url_id_fkey FOREIGN KEY (url_id) REFERENCES frontier.url(url_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
