--
-- PostgreSQL database dump
--

\restrict hIspsdzUQAJV3nAxwerGEp0b6sF81upf6GUIwwkMVWSOeVGTsgqr7wMFx0RyOCh

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
-- Name: attach_export_item_to_batch(bigint, bigint, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.attach_export_item_to_batch(p_export_item_id bigint, p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(batch_item_id bigint, batch_id bigint, export_item_id bigint, export_state outbox.export_state_enum)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_export_item_id IS NULL OR p_export_item_id <= 0 THEN
    RAISE EXCEPTION 'p_export_item_id must be > 0';
  END IF;

  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  WITH batch_link AS (
    INSERT INTO outbox.export_batch_item AS oebi (
      batch_id,
      export_item_id,
      source_run_id,
      source_note,
      item_metadata,
      updated_at
    )
    VALUES (
      p_batch_id,
      p_export_item_id,
      p_source_run_id,
      p_source_note,
      COALESCE(p_item_metadata, '{}'::jsonb),
      now()
    )
    ON CONFLICT ON CONSTRAINT outbox_export_batch_item_export_item_uniq
    DO UPDATE
       SET batch_id = EXCLUDED.batch_id,
           source_run_id = EXCLUDED.source_run_id,
           source_note = EXCLUDED.source_note,
           item_metadata = EXCLUDED.item_metadata,
           updated_at = now()
    RETURNING
      oebi.batch_item_id,
      oebi.batch_id,
      oebi.export_item_id
  ),
  item_upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'materialized'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id = p_export_item_id
    RETURNING opei.export_state
  )
  SELECT
    bl.batch_item_id,
    bl.batch_id,
    bl.export_item_id,
    iu.export_state
  FROM batch_link bl
  CROSS JOIN item_upd iu;
END;
$$;


--
-- Name: FUNCTION attach_export_item_to_batch(p_export_item_id bigint, p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.attach_export_item_to_batch(p_export_item_id bigint, p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb) IS 'Attaches one export item to a materialized batch and advances item state to materialized.';


--
-- Name: create_export_batch(text, text, integer, text, jsonb, text, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.create_export_batch(p_export_channel text, p_batch_key text, p_item_count integer, p_payload_sha256 text, p_manifest jsonb, p_storage_relpath text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(batch_id bigint, export_channel text, batch_key text, batch_state outbox.batch_state_enum, item_count integer, payload_sha256 text)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_export_channel IS NULL OR btrim(p_export_channel) = '' THEN
    RAISE EXCEPTION 'p_export_channel must be non-empty';
  END IF;

  IF p_batch_key IS NULL OR btrim(p_batch_key) = '' THEN
    RAISE EXCEPTION 'p_batch_key must be non-empty';
  END IF;

  IF p_payload_sha256 IS NULL OR btrim(p_payload_sha256) = '' THEN
    RAISE EXCEPTION 'p_payload_sha256 must be non-empty';
  END IF;

  IF p_storage_relpath IS NULL OR btrim(p_storage_relpath) = '' THEN
    RAISE EXCEPTION 'p_storage_relpath must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO outbox.export_batch AS oeb (
    export_channel,
    batch_key,
    batch_state,
    item_count,
    payload_sha256,
    manifest,
    storage_relpath,
    source_run_id,
    source_note,
    batch_metadata,
    updated_at
  )
  VALUES (
    p_export_channel,
    p_batch_key,
    'materialized'::outbox.batch_state_enum,
    COALESCE(p_item_count, 0),
    p_payload_sha256,
    COALESCE(p_manifest, '{}'::jsonb),
    p_storage_relpath,
    p_source_run_id,
    p_source_note,
    COALESCE(p_batch_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT outbox_export_batch_batch_key_uniq
  DO UPDATE
     SET export_channel = EXCLUDED.export_channel,
         batch_state = 'materialized'::outbox.batch_state_enum,
         item_count = EXCLUDED.item_count,
         payload_sha256 = EXCLUDED.payload_sha256,
         manifest = EXCLUDED.manifest,
         storage_relpath = EXCLUDED.storage_relpath,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         batch_metadata = EXCLUDED.batch_metadata,
         updated_at = now()
  RETURNING
    oeb.batch_id,
    oeb.export_channel,
    oeb.batch_key,
    oeb.batch_state,
    oeb.item_count,
    oeb.payload_sha256;
END;
$$;


--
-- Name: FUNCTION create_export_batch(p_export_channel text, p_batch_key text, p_item_count integer, p_payload_sha256 text, p_manifest jsonb, p_storage_relpath text, p_source_run_id text, p_source_note text, p_batch_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.create_export_batch(p_export_channel text, p_batch_key text, p_item_count integer, p_payload_sha256 text, p_manifest jsonb, p_storage_relpath text, p_source_run_id text, p_source_note text, p_batch_metadata jsonb) IS 'Creates or updates one materialized export batch record for GitHub-bound page exports.';


--
-- Name: enqueue_page_export_item(bigint, bigint, bigint, text, jsonb, text, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.enqueue_page_export_item(p_url_id bigint, p_snapshot_id bigint, p_workflow_status_id bigint, p_export_channel text, p_payload jsonb, p_payload_sha256 text, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_export_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(export_item_id bigint, url_id bigint, snapshot_id bigint, workflow_status_id bigint, export_channel text, export_state outbox.export_state_enum, payload_sha256 text)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_url_id IS NULL OR p_url_id <= 0 THEN
    RAISE EXCEPTION 'p_url_id must be > 0';
  END IF;

  IF p_snapshot_id IS NULL OR p_snapshot_id <= 0 THEN
    RAISE EXCEPTION 'p_snapshot_id must be > 0';
  END IF;

  IF p_workflow_status_id IS NULL OR p_workflow_status_id <= 0 THEN
    RAISE EXCEPTION 'p_workflow_status_id must be > 0';
  END IF;

  IF p_export_channel IS NULL OR btrim(p_export_channel) = '' THEN
    RAISE EXCEPTION 'p_export_channel must be non-empty';
  END IF;

  IF p_payload IS NULL THEN
    RAISE EXCEPTION 'p_payload must not be null';
  END IF;

  IF p_payload_sha256 IS NULL OR btrim(p_payload_sha256) = '' THEN
    RAISE EXCEPTION 'p_payload_sha256 must be non-empty';
  END IF;

  RETURN QUERY
  INSERT INTO outbox.page_export_item AS opei (
    url_id,
    snapshot_id,
    workflow_status_id,
    export_channel,
    export_state,
    payload,
    payload_sha256,
    source_run_id,
    source_note,
    export_metadata,
    updated_at
  )
  VALUES (
    p_url_id,
    p_snapshot_id,
    p_workflow_status_id,
    p_export_channel,
    'queued'::outbox.export_state_enum,
    p_payload,
    p_payload_sha256,
    p_source_run_id,
    p_source_note,
    COALESCE(p_export_metadata, '{}'::jsonb),
    now()
  )
  ON CONFLICT ON CONSTRAINT outbox_page_export_item_url_channel_snapshot_uniq
  DO UPDATE
     SET workflow_status_id = EXCLUDED.workflow_status_id,
         export_state = 'queued'::outbox.export_state_enum,
         payload = EXCLUDED.payload,
         payload_sha256 = EXCLUDED.payload_sha256,
         source_run_id = EXCLUDED.source_run_id,
         source_note = EXCLUDED.source_note,
         export_metadata = EXCLUDED.export_metadata,
         updated_at = now()
  RETURNING
    opei.export_item_id,
    opei.url_id,
    opei.snapshot_id,
    opei.workflow_status_id,
    opei.export_channel,
    opei.export_state,
    opei.payload_sha256;
END;
$$;


--
-- Name: FUNCTION enqueue_page_export_item(p_url_id bigint, p_snapshot_id bigint, p_workflow_status_id bigint, p_export_channel text, p_payload jsonb, p_payload_sha256 text, p_source_run_id text, p_source_note text, p_export_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.enqueue_page_export_item(p_url_id bigint, p_snapshot_id bigint, p_workflow_status_id bigint, p_export_channel text, p_payload jsonb, p_payload_sha256 text, p_source_run_id text, p_source_note text, p_export_metadata jsonb) IS 'Creates or updates one GitHub-bound export outbox item for a pre-ranked page snapshot.';


--
-- Name: mark_export_batch_failed(bigint, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.mark_export_batch_failed(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(batch_id bigint, batch_state outbox.batch_state_enum)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  UPDATE outbox.export_batch AS oeb
  SET batch_state = 'failed'::outbox.batch_state_enum,
      source_run_id = COALESCE(p_source_run_id, oeb.source_run_id),
      source_note = COALESCE(p_source_note, oeb.source_note),
      batch_metadata = COALESCE(oeb.batch_metadata, '{}'::jsonb) || COALESCE(p_batch_metadata, '{}'::jsonb),
      updated_at = now()
  WHERE oeb.batch_id = p_batch_id
  RETURNING oeb.batch_id, oeb.batch_state;
END;
$$;


--
-- Name: FUNCTION mark_export_batch_failed(p_batch_id bigint, p_source_run_id text, p_source_note text, p_batch_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.mark_export_batch_failed(p_batch_id bigint, p_source_run_id text, p_source_note text, p_batch_metadata jsonb) IS 'Marks one export batch as failed when its local batch files are stale/missing or push processing cannot safely continue.';


--
-- Name: mark_export_batch_pushed(bigint, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.mark_export_batch_pushed(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_batch_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(batch_id bigint, batch_state outbox.batch_state_enum)
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  RETURN QUERY
  UPDATE outbox.export_batch AS oeb
  SET batch_state = 'pushed'::outbox.batch_state_enum,
      source_run_id = COALESCE(p_source_run_id, oeb.source_run_id),
      source_note = COALESCE(p_source_note, oeb.source_note),
      batch_metadata = COALESCE(oeb.batch_metadata, '{}'::jsonb) || COALESCE(p_batch_metadata, '{}'::jsonb),
      updated_at = now()
  WHERE oeb.batch_id = p_batch_id
  RETURNING oeb.batch_id, oeb.batch_state;
END;
$$;


--
-- Name: FUNCTION mark_export_batch_pushed(p_batch_id bigint, p_source_run_id text, p_source_note text, p_batch_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.mark_export_batch_pushed(p_batch_id bigint, p_source_run_id text, p_source_note text, p_batch_metadata jsonb) IS 'Marks one materialized export batch as pushed after successful GitHub push.';


--
-- Name: mark_export_items_pushed_by_batch(bigint, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.mark_export_items_pushed_by_batch(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(updated_count integer)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_count integer;
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  WITH upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'pushed'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id IN (
      SELECT ebi.export_item_id
      FROM outbox.export_batch_item ebi
      WHERE ebi.batch_id = p_batch_id
    )
    RETURNING 1
  )
  SELECT count(*) INTO v_count FROM upd;

  RETURN QUERY SELECT COALESCE(v_count, 0);
END;
$$;


--
-- Name: FUNCTION mark_export_items_pushed_by_batch(p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.mark_export_items_pushed_by_batch(p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb) IS 'Marks all export items attached to a batch as pushed after successful GitHub push.';


--
-- Name: requeue_export_items_by_batch(bigint, text, text, jsonb); Type: FUNCTION; Schema: outbox; Owner: -
--

CREATE FUNCTION outbox.requeue_export_items_by_batch(p_batch_id bigint, p_source_run_id text DEFAULT NULL::text, p_source_note text DEFAULT NULL::text, p_item_metadata jsonb DEFAULT '{}'::jsonb) RETURNS TABLE(updated_count integer)
    LANGUAGE plpgsql
    AS $$
DECLARE
  v_count integer;
BEGIN
  IF p_batch_id IS NULL OR p_batch_id <= 0 THEN
    RAISE EXCEPTION 'p_batch_id must be > 0';
  END IF;

  WITH upd AS (
    UPDATE outbox.page_export_item AS opei
    SET export_state = 'queued'::outbox.export_state_enum,
        source_run_id = COALESCE(p_source_run_id, opei.source_run_id),
        source_note = COALESCE(p_source_note, opei.source_note),
        export_metadata = COALESCE(opei.export_metadata, '{}'::jsonb) || COALESCE(p_item_metadata, '{}'::jsonb),
        updated_at = now()
    WHERE opei.export_item_id IN (
      SELECT ebi.export_item_id
      FROM outbox.export_batch_item ebi
      WHERE ebi.batch_id = p_batch_id
    )
    RETURNING 1
  )
  SELECT count(*) INTO v_count FROM upd;

  RETURN QUERY SELECT COALESCE(v_count, 0);
END;
$$;


--
-- Name: FUNCTION requeue_export_items_by_batch(p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb); Type: COMMENT; Schema: outbox; Owner: -
--

COMMENT ON FUNCTION outbox.requeue_export_items_by_batch(p_batch_id bigint, p_source_run_id text, p_source_note text, p_item_metadata jsonb) IS 'Resets all export items attached to a failed batch back to queued so they can be materialized again.';


SET default_tablespace = '';

SET default_table_access_method = heap;

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

\unrestrict hIspsdzUQAJV3nAxwerGEp0b6sF81upf6GUIwwkMVWSOeVGTsgqr7wMFx0RyOCh

