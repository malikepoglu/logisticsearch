# Crawler Core R113 Durable Claim Fetch / Parse / Discovery Seal — 2026-05-07

## 1. Purpose

This document seals the R113 crawler_core validation line after the corrected durable one-claim runtime path proved that the crawler can fetch, store raw HTML, parse minimal page evidence, enqueue discovery links, and degrade taxonomy lookup failures without rolling back crawler-core truth.

This is not a taxonomy-ranking completion seal. Taxonomy DB privileges are intentionally still blocked and must remain a separate controlled design decision.

## 2. Canonical Git / Runtime State

Canonical repository head at seal time:

- `9c3b91c7154b2a9f5af3fd5826e6611a0eaaec04`
- commit subject: `fix(parse-runtime): degrade unavailable taxonomy lookup`

Validated file hashes:

- `makpi51crawler/python_live_runtime/logisticsearch1_1_2_6_parse_runtime.py`
  - sha256: `74f72fcc9ec7f2490a135b7d52b9591c22ceae32aeb1831696ee4167e468aaa4`
- `makpi51crawler/python_live_runtime/logisticsearch1_1_2_worker_runtime.py`
  - sha256: `5e5b2649c72049fe2987c3c2684ccd18909c1459952f9d332c412930978f4159`

Pi51c repo and live runtime were synchronized to the same canonical head before durable runtime validation.

Service and process state during the validation line:

- `logisticsearch-webcrawler.service` remained disabled.
- `logisticsearch-webcrawler.service` remained inactive.
- No long-running crawler loop was started.
- Only explicit one-claim CLI invocations were used.

## 3. R113 Parse Runtime Fix Sealed

R113 introduced a one-file parse runtime patch in:

- `makpi51crawler/python_live_runtime/logisticsearch1_1_2_6_parse_runtime.py`

Patch scope:

- Wrap taxonomy candidate lookup inside `apply_minimal_parse_entry`.
- Treat taxonomy runtime / DB privilege failure as non-fatal for crawler_core validation.
- Preserve fetch, raw storage, parse metadata, and discovery evidence.
- Store visible metadata:
  - `taxonomy_lookup_degraded`
  - `taxonomy_lookup_degraded_reason`
  - `taxonomy_lookup_error_class`
  - `taxonomy_lookup_error_message`
- Force workflow to `review_hold` with:
  - `taxonomy_lookup_unavailable_manual_review_required`

Explicitly not changed in R113:

- No taxonomy DB privilege grant.
- No SQL schema mutation.
- No worker-runtime logic patch.
- No systemd mutation.
- No long loop start.

## 4. First Corrected Durable Claim Evidence

Step:

- `R113_STEP4AQ_CORRECTED_DURABLE_ONE_CLAIM_VALIDATION`
- final read-only seal: `R113_STEP4AR`

Claimed URL:

- `url_id=64`
- `canonical_url=https://fiata.org/directory/`

Fetch evidence:

- `fetch_attempt_id=150`
- HTTP status: `200`
- content type: `text/html; charset=utf-8`
- body bytes: `222360`
- raw storage path: `/srv/webcrawler/raw_fetch/2026/05/06/url_64_20260506T213537Z.body.bin`
- raw sha256: `e5498d20f738bed2259f4e4ad35cde05a61309116cda22c87aa0202bf4a7114a`

Crawler-core result:

- Fetch confirmed.
- Raw storage confirmed.
- Minimal parse confirmed.
- Discovery confirmed.
- Lease released.
- Frontier returned to `queued`.
- Next success revisit time computed into the future before later discovery requeue exposure.

Discovery evidence:

- discovered href count: `182`
- normalized URL count: `25`
- enqueued URL count: `25`
- degraded enqueue count: `0`

Taxonomy state:

- Taxonomy lookup degraded visibly.
- Error class: `InsufficientPrivilege`
- Workflow state: `review_hold`
- Workflow reason: `taxonomy_lookup_unavailable_manual_review_required`

## 5. Second Corrected Durable Claim Evidence

Step:

- `R113_STEP4AU_R2_SECOND_DURABLE_ONE_CLAIM_VALIDATION_FIXED_AUDIT`
- final read-only seal: `R113_STEP4AV`

Claimed URL:

- `url_id=590`
- `canonical_url=https://fiata.org/directory/gb/`

Fetch evidence:

- `fetch_attempt_id=151`
- HTTP status: `200`
- content type: `text/html; charset=utf-8`
- body bytes: `1171113`
- raw storage path: `/srv/webcrawler/raw_fetch/2026/05/06/url_590_20260506T220702Z.body.bin`
- raw sha256: `50d6e63590e2345503b82ddb82ae6b90d99852f9005f0ad79edabe602ad8a2c6`

Crawler-core result:

- Second fetch confirmed.
- Second raw storage confirmed.
- Second minimal parse confirmed.
- Second discovery confirmed.
- Lease released.
- Frontier returned to `queued`.

Discovery evidence:

- discovered href count: `1064`
- normalized URL count: `16`
- enqueued URL count: `16`
- degraded enqueue count: `0`

DB child-row note:

- Output showed 16 enqueue receipts.
- DB child count for parent `590` was 7.
- Read-only classification showed that output enqueue receipts may include existing/reused rows whose durable parent remains elsewhere.

Taxonomy state:

- Taxonomy lookup degraded visibly.
- Error class: `InsufficientPrivilege`
- Workflow state: `review_hold`
- Workflow reason: `taxonomy_lookup_unavailable_manual_review_required`

## 6. Important R113 Gap Discovered During Seal

Step:

- `R113_STEP4AX_R2_DISCOVERY_REQUEUE_OVERWRITE_CLASSIFICATION_READONLY`

Final classification:

- `DISCOVERY_REQUEUE_OVERWRITES_REVISIT_SCHEDULE`

Observed behavior:

- During parsing of `url_id=590`, discovery output included `url_id=64`.
- `url_id=64` had already fetched successfully in R113.
- The existing `url_id=64` row was re-seen through discovery and became immediately due again.

Relevant DB truth after AX_R2:

- `url_id=64`
- `canonical_url=https://fiata.org/directory/`
- `state=queued`
- `discovery_type=seed`
- `parent_url_id=64`
- `is_seed=False`
- `priority=230`
- `enqueue_reason=minimal_html_link_discovery_from_parse_runtime`
- `last_enqueued_at=2026-05-07 00:07:02.232232+02:00`
- `next_fetch_at=2026-05-07 00:07:02.232232+02:00`
- `next_fetch_due=True`
- `last_success_at=2026-05-06 23:35:36.878644+02:00`
- `last_http_status=200`

SQL function evidence:

- `frontier.enqueue_discovered_url(...)` contains conflict-update logic that can set:
  - `last_seen_at = now()`
  - `last_enqueued_at = CASE ... ELSE now()`
  - `next_fetch_at = CASE ... ELSE now()`

Impact:

- Existing successfully fetched pages can be requeued immediately when rediscovered.
- This can override intended success revisit scheduling.
- This can create avoidable repeat fetch pressure before broader crawler loop activation.

## 7. R113 Final Decision

R113 is sealed as a crawler_core fetch / raw storage / parse / discovery validation success.

Confirmed:

- Controlled durable claim invocation works when `--durable-claim` is used.
- Probe-only early return was correctly classified and is not a fetch failure.
- HTTP acquisition worked for two separate URLs.
- Raw files were stored with verified sha256.
- Fetch attempts were recorded successfully.
- Parse evidence was persisted.
- Preranking snapshot rows were persisted in `review_hold`.
- Workflow state was persisted in `review_hold`.
- Discovery ran and enqueued URLs without degraded enqueue failures.
- Taxonomy lookup unavailability no longer rolls back crawler-core evidence.
- Service remained disabled/inactive.
- No crawler loop was started.

Not sealed as complete:

- Taxonomy DB privilege / runtime lookup readiness.
- Ranking quality.
- Full discovery policy.
- Discovery requeue / revisit-schedule protection.
- Long-running crawler loop readiness.

## 8. Next Required Line: R114

R114 should be a separate controlled line for the discovery requeue scheduling bug.

Recommended R114 scope:

1. Read-only design/audit:
   - inspect `frontier.enqueue_discovered_url(...)`
   - inspect Python caller expectations in parse/discovery runtime
   - classify existing-row behavior:
     - new URL insert
     - existing unseen URL
     - existing successful URL with future `next_fetch_at`
     - existing failed/retry URL
     - existing seed URL rediscovered as child link

2. Patch policy should likely preserve future revisit schedules for existing successful URLs.

3. Candidate invariant:
   - Discovery may update `last_seen_at`.
   - Discovery must not blindly move `next_fetch_at` to `now()` for an existing URL that already has successful fetch history and a future revisit time.
   - Existing seed/root identity should not be degraded by rediscovery.

4. Validation:
   - scratch or controlled local DB test first where practical
   - then pi51c read-only preflight
   - then one controlled durable claim only after patch is synced
   - no service start
   - no loop start

## 9. Future Parallel Architecture Note

After crawler_core fetch / parse / discovery is stable, a separate incremental PostgreSQL JSON/JSONB design track should begin.

That track must not distract from crawler_core stabilization. It should grow step-by-step as functionality increases and should be documented in GitHub with the same controlled audit/patch/seal discipline.
