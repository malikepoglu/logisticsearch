-- psql-only apply bundle for outbox-core split surface
\set ON_ERROR_STOP on

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

\ir 001_outbox_base.sql
\ir 002_outbox_enqueue_and_batch_creation.sql
\ir 003_outbox_batch_attachment_and_state_transitions.sql
