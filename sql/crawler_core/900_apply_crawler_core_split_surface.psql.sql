-- psql-only apply bundle for crawler-core split surface
\set ON_ERROR_STOP on

\ir 001_seed_frontier_http_fetch_base.sql
\ir 002_frontier_claim_and_lease.sql
\ir 003_frontier_finish_transitions.sql
\ir 004_frontier_politeness_and_freshness.sql
\ir 005_http_fetch_robots_cache_and_enforcement.sql
