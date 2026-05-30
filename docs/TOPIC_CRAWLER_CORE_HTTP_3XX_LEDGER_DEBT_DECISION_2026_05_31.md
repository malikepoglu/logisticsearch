# Crawler Core HTTP 3xx Ledger Debt Decision

Gate: `FULL_R4_P2C76AA_HTTP_3XX_LEDGER_DEBT_DECISION_DOC_LOCAL_ONLY_R1`  
Image item: `4_OF_5_HTTP_3XX_REDIRECT_HANDLING_REMAINING_DEBT`  
Date: `2026-05-31`  
Canonical head: `2e32ebe8fa662fe8ebeccca9a75a55d3eb4c8fd1`  
Subject: `docs(crawler-core): document request identity token map`

## 1. Scope

This document records the decision after `P2C76Z` for the remaining HTTP 3xx ledger debt.

This is a decision document only. It does not allow crawler start, DB reset, raw deletion, git push, pi51c live copy, catalog mutation, systemd mutation, or bulk mutation.

## 2. Current sealed state after P2C76Y and P2C76Z

| Metric | Value |
|---|---:|
| Retry-wait HTTP 3xx rows | `0` |
| Dead high-priority HTTP 3xx rows | `0` |
| Historical alignment suspect rows | `13` |
| HTTP 3xx mismatch rows | `8` |
| Global attempt mismatch rows | `231` |
| Latest fetch attempt id | `1922` |
| Request identity old token count | `0` |
| Request identity LS token count | `722` |

## 3. What is solved

The live/actionable HTTP 3xx loop debt is solved.

The previous retry-wait unresolved 3xx rows were driven through controlled foreground runs and reached terminal `http_3xx_no_resolvable_redirect_target` or redirect-target-enqueued states. Test-induced high priority/score residue on dead 3xx rows was repaired in `P2C76Y`.

`P2C76Z` confirmed:

- `RETRY_WAIT_3XX=0`
- `DEAD_HIGH_PRIORITY_3XX=0`
- service remains inactive and disabled
- crawler process count is zero
- browser process count is zero
- raw evidence count and byte total stayed stable during the read-only report

## 4. Remaining historical alignment debt

`P2C76Z` reported `13` historical alignment suspect rows.

These are historical `http_fetch.fetch_attempt` rows where the attempt row still says:

- `outcome` is `retryable_error`
- `error_class` is `http_3xx_unresolved_redirect`

while the current frontier row is already terminal:

- `state=dead`
- `last_error_class=http_3xx_no_resolvable_redirect_target`

Affected URL groups:

| url_id | Historical suspect attempts |
|---:|---:|
| `1003` | `3` |
| `1732` | `2` |
| `1733` | `2` |
| `1734` | `2` |
| `1774` | `2` |
| `1775` | `2` |

Decision: preserve historical fetch attempt rows as evidence unless a separate, explicit, targeted backfill policy is approved.

## 5. Remaining counter mismatch debt

`P2C76Z` reported `8` HTTP 3xx-related mismatch rows.

Buckets:

| Bucket | Rows | Total delta |
|---|---:|---:|
| `BROWSER_RETRY_WAIT_COUNTER_AHEAD` | `6` | `6` |
| `DEAD_3XX_COUNTER_AHEAD` | `2` | `2` |

Rows:

| url_id | state | last_error_class | http_status | frontier count | actual attempts | delta |
|---:|---|---|---:|---:|---:|---:|
| `748` | `retry_wait` | `browser_navigation_error` | `302` | `3` | `2` | `1` |
| `749` | `retry_wait` | `browser_navigation_error` | `302` | `3` | `2` | `1` |
| `775` | `retry_wait` | `browser_navigation_error` | `307` | `3` | `2` | `1` |
| `776` | `retry_wait` | `browser_navigation_timeout` | `307` | `2` | `1` | `1` |
| `1002` | `retry_wait` | `browser_navigation_error` | `307` | `3` | `2` | `1` |
| `1733` | `dead` | `http_3xx_no_resolvable_redirect_target` | `302` | `4` | `3` | `1` |
| `1775` | `dead` | `http_3xx_no_resolvable_redirect_target` | `307` | `5` | `4` | `1` |
| `2078` | `retry_wait` | `browser_navigation_error` | `302` | `2` | `1` | `1` |

Decision: counter mismatch is not a crawler fetch failure, but it is lifecycle/accounting debt. It must be repaired with a targeted reconciliation gate that updates only `frontier.url.fetch_attempt_count` to the actual count derived from `http_fetch.fetch_attempt`, scoped to the eight sealed rows above.

## 6. Non-defer rule

Do not close image item 4/5 until the following are true:

1. retry-wait HTTP 3xx rows remain `0`
2. dead high-priority HTTP 3xx rows remain `0`
3. the eight counter mismatch rows are either repaired by targeted reconciliation or explicitly sealed with a stronger reason
4. historical fetch-attempt alignment debt is documented and either left immutable as evidence or handled by a separate explicit backfill plan
5. final item 4/5 seal proves service/process/raw/DB counters are stable

## 7. Required next gate

Next gate:

`FULL_R4_P2C76AB_HTTP_3XX_COUNTER_MISMATCH_RECONCILIATION_PLAN_READONLY_R1`

Purpose:

Read-only plan for the exact eight counter mismatch rows. It must prove the update scope before any mutation.

Allowed next mutation after that plan, if and only if the plan passes:

`frontier.url.fetch_attempt_count = actual_fetch_attempt_rows`

for exactly:

`748,749,775,776,1002,1733,1775,2078`

No fetch attempt history rewrite is allowed in that counter reconciliation gate.
