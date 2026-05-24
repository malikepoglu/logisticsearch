# Crawler Core Visit Policy and Runtime State Separation Seal - 2026-05-24

## Purpose

This document seals the crawler_core rule for separating static catalog policy from dynamic runtime state before the first post-reset activation test.

The crawler must not mutate live runtime JSON or catalog JSON as part of normal fetch scheduling.

Catalog JSON is policy input.

Runtime database tables are operational state.

## Current baseline

- Previous gate: TOMORROW_TEST_ACTIVATION_VISIT_POLICY_STATE_AUDIT_READONLY
- Previous gate result: PASS
- Canonical head: dd3d2f2cfa5f7e96eae1a66b6b51e974ee082393
- Ubuntu Desktop was aligned to cached origin/main.
- pi51c repo was aligned to the same head.
- crawler service remained inactive and disabled.
- crawler process count remained 0.
- DB audit was read-only.
- No public URL fetch occurred.
- No DB mutation occurred.
- No frontier insertion occurred.
- No crawler start occurred.
- No systemd mutation occurred.

## Non-negotiable rule

Static visit-frequency policy may live in catalog JSON.

Dynamic visit state must not live in catalog JSON.

This means:

- JSON may say how often a source, host, root domain, seed family, seed surface, or seed URL may be visited.
- JSON must not store changing last visit timestamps.
- JSON must not be rewritten after every crawler fetch.
- Live runtime JSON and canonical catalog JSON must remain stable unless an explicit catalog policy patch is performed through a gated repo workflow.

## Static policy belongs in JSON

JSON is allowed to store stable policy fields such as:

- host_budget_group
- recrawl_interval
- default_recrawl_interval
- crawl_depth_policy
- crawl_priority
- daily_family_budget_required
- source_family_visit_policy
- future explicit visit-frequency policy such as min_visit_interval_seconds

The audit confirmed existing policy-like keys across the 26 catalog JSON files:

- host_budget_group
- recrawl_interval
- default_recrawl_interval
- crawl_depth_policy
- crawl_priority
- daily_family_budget_required
- source_family_visit_policy

## Dynamic runtime state belongs in DB

Dynamic visit state belongs in runtime tables, not JSON.

The DB audit confirmed runtime state surfaces in:

- frontier.host
- frontier.url
- http_fetch.fetch_attempt
- http_fetch.robots_txt_cache
- seed.seed_url
- seed.source

Relevant frontier.host fields include:

- host
- registrable_domain
- host_status
- next_eligible_at
- robots_last_checked_at
- robots_last_modified
- last_fetch_started_at
- last_fetch_finished_at
- last_success_at
- last_error_at
- last_error_class
- host_metadata

Relevant frontier.url fields include:

- next_fetch_at
- revisit_not_before
- fetch_attempt_count
- success_count
- retryable_error_count
- permanent_error_count
- consecutive_error_count
- last_fetch_started_at
- last_fetch_finished_at
- last_success_at
- last_http_status
- last_content_type
- last_body_bytes
- last_outcome
- last_error_class
- last_error_message

Relevant http_fetch.fetch_attempt fields include:

- http_status
- retry_after_seconds
- fetch_metadata

Relevant seed.seed_url fields include:

- recrawl_interval
- next_discover_at
- last_discovered_at
- last_enqueued_at
- last_result

Therefore, the DB already has the correct kind of surface for runtime state.

## Semantic distinction

recrawl_interval is long-term rediscovery or revisit policy.

recrawl_interval must not be used as a 30-second host throttle.

Examples:

- recrawl_interval P14D means the same seed may be reconsidered after a long horizon.
- min_visit_interval_seconds 30 means the same normalized root domain should not be visited more often than every 30 seconds.
- next_fetch_at and next_eligible_at are runtime scheduling state and must be stored in DB.
- last_success_at, last_fetch_started_at, and last_fetch_finished_at are runtime observations and must be stored in DB.

## FIATA policy decision

fiata.org is a large repeated source across many catalogs and can be treated as a fast-domain override candidate after controlled patching.

Policy intent:

- Default initial cap: 6 per hour per root domain
- Equivalent default interval: 600 seconds
- FIATA candidate override: 30 seconds
- FIATA equivalent cap: 120 per hour per root domain

This must be implemented as a root-domain policy override, not as a per-catalog override.

Reason:

- The same root domain may appear across many catalog JSON files.
- If each catalog receives its own independent limit, the crawler may accidentally flood a shared domain.
- The safe key is normalized_root_domain.

## Required normalized-root-domain rule

The crawler must derive a stable normalized root domain from each seed URL before scheduling.

Examples:

- https://fiata.org/directory/de/ becomes fiata.org
- https://www.fiata.org/ becomes fiata.org
- https://mobile.cargoyellowpages.com/ should become cargoyellowpages.com when the registered-domain resolver supports it
- https://www.freightnet.com/ becomes freightnet.com

Correct scheduling budget key:

    budget_key = normalized_root_domain

Incorrect scheduling budget keys:

    budget_key = catalog_code
    budget_key = source_family_code_only
    budget_key = seed_surface_code_only
    budget_key = raw_hostname_only

## Runtime scheduling decision order

Before visiting any URL, crawler_core must evaluate this order:

1. Load candidate seed or root-domain policy from JSON-derived runtime projection.
2. Derive normalized_root_domain from the seed URL.
3. Read DB runtime state for the normalized root domain and URL.
4. Check whether the source or seed is enabled for activation.
5. Check whether live-probe and candidate-only guards allow promotion.
6. Check frontier.host.next_eligible_at.
7. Check frontier.url.next_fetch_at.
8. Check frontier.url.revisit_not_before.
9. Check retry state and http_fetch.fetch_attempt.retry_after_seconds.
10. Check robots policy and any crawl-delay discovered by robots handling.
11. Compute the effective interval.
12. If the selected domain is capped, do not sleep on that domain.
13. Select another eligible seed or root domain.
14. Sleep only if no eligible seed or root domain exists.

## Effective interval rule

The effective interval must be conservative.

Formula:

    effective_min_visit_interval_seconds = max(json_policy_min_visit_interval_seconds, robots_crawl_delay_seconds_if_present, retry_after_seconds_if_present, error_backoff_seconds_if_present, global_safety_floor_seconds)

For the FIATA initial override, the intended JSON policy value is:

    min_visit_interval_seconds = 30

The effective value may become larger if robots, retry-after, or errors require it.

## Candidate-only safety guard

The current catalog state is candidate-only.

The activation patch must not treat catalog presence as permission to crawl.

Required guards:

- Do not activate seed URLs merely because they exist in JSON.
- Do not activate source families merely because they exist in JSON.
- Honor candidate and live flags.
- Honor is_enabled or equivalent activation fields where present.
- Honor needs_live_check or live-probe requirement before broad insertion.
- Keep crawler service inactive until an explicit activation gate.

## JSON field decision

If a correct existing field for per-domain visit throttle is found, use that field.

If no correct existing field exists, add a clearly named policy field:

    min_visit_interval_seconds

Example policy value:

    min_visit_interval_seconds = 30

This field is a policy field and must not be updated during runtime fetches.

Do not use these fields inside catalog JSON for runtime operation:

- last_visit_at
- last_fetch_at
- last_success_at
- next_fetch_at
- retry_after_until
- last_http_status

These are DB/runtime state concepts.

## Patch order after this document

1. Read-only patch plan for runtime and JSON field selection.
2. Runtime patch local-only on Ubuntu Desktop.
3. Runtime patch audit read-only.
4. JSON policy patch only if required.
5. JSON policy audit read-only.
6. Commit and push after exact dirty scope is confirmed.
7. pi51c repo/live sync only after GitHub seal.
8. Activation test only after pi51c repo/live/runtime/DB preflight passes.

## Safety boundary

This document does not activate crawling.

This document does not permit public fetch.

This document does not permit frontier insertion.

This document does not permit DB mutation.

This document does not permit systemd mutation.

This document does not permit live runtime JSON mutation.

Next gate:

    TOMORROW_TEST_ACTIVATION_POLICY_STATE_DOCUMENTATION_AUDIT_READONLY
