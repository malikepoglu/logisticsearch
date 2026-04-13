-- psql-only apply bundle for parse-core split surface
\set ON_ERROR_STOP on

\ir 001_parse_base.sql
\ir 002_parse_evidence_and_candidate_upserts.sql
\ir 003_parse_preranking_persistence.sql
\ir 004_parse_workflow_state_and_payload.sql
