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

## 8. Post-reconciliation and URL1003 exception update

Gate: `FULL_R4_P2C76AE3_HTTP_3XX_HISTORICAL_ALIGNMENT_DECISION_DOC_UPDATE_LOCAL_ONLY_R1`

This section updates the earlier decision after the following gates:

- `P2C76AB` counter mismatch reconciliation plan
- `FULL_R4_P2C76AC_HTTP_3XX_COUNTER_MISMATCH_RECONCILIATION_GATE_R1`
- `FULL_R4_P2C76AD_HTTP_3XX_COUNTER_MISMATCH_RECONCILIATION_POST_SEAL_READONLY_R1`
- `FULL_R4_P2C76AE_HTTP_3XX_HISTORICAL_ALIGNMENT_DECISION_READONLY_R1`
- `FULL_R4_P2C76AE2_HTTP_3XX_URL1003_HISTORICAL_EXCEPTION_ROOT_CAUSE_READONLY_R1`

### 8.1 Counter reconciliation result

The exact eight counter mismatch rows were reconciled.

| Metric | Value |
|---|---:|
| Reconciled URL ids | `748,749,775,776,1002,1733,1775,2078` |
| Reconciliation update count | `8` |
| HTTP 3xx mismatch rows after reconciliation | `0` |
| Global attempt mismatch rows after reconciliation | `223` |
| Retry-wait HTTP 3xx rows after reconciliation | `0` |
| Dead high-priority HTTP 3xx rows after reconciliation | `0` |

The reconciliation changed only `frontier.url.fetch_attempt_count` for the exact eight URL ids above so that the counter matched the real number of `http_fetch.fetch_attempt` rows.

### 8.2 Historical alignment result

Historical alignment count remains `13`.

For five URL ids, historical retryable rows are superseded by at least one terminal no-target attempt row:

| url_id | Historical retryable rows | Terminal no-target attempt rows |
|---:|---:|---:|
| `1732` | `2` | `1` |
| `1733` | `2` | `1` |
| `1734` | `2` | `1` |
| `1774` | `2` | `1` |
| `1775` | `2` | `1` |

For `url_id=1003`, the evidence chain is different and must be handled as an explicit exception.

### 8.3 URL1003 exception

`url_id=1003` is classified as:

`PRE_PATCH_FRONTIER_TERMINAL_STATE_WITHOUT_TERMINAL_FETCH_ATTEMPT_ROW`

Sealed URL1003 facts:

| Field | Value |
|---|---:|
| url_id | `1003` |
| canonical_url | `https://www.chamber.org.il/en/` |
| frontier state | `dead` |
| frontier last_error_class | `http_3xx_no_resolvable_redirect_target` |
| frontier last_http_status | `307` |
| frontier fetch_attempt_count | `3` |
| actual fetch_attempt rows | `3` |
| historical retryable attempts | `3` |
| terminal no-target attempts | `0` |
| mismatch_delta | `0` |

URL1003 attempt ids:

| fetch_attempt_id | outcome | error_class | http_status |
|---:|---|---|---:|
| `853` | `retryable_error` | `http_3xx_unresolved_redirect` | `307` |
| `1879` | `retryable_error` | `http_3xx_unresolved_redirect` | `307` |
| `1915` | `retryable_error` | `http_3xx_unresolved_redirect` | `307` |

Policy for URL1003:

`DOCUMENT_URL1003_EXCEPTION_AND_PRESERVE_FETCH_ATTEMPT_HISTORY_NO_REWRITE`

No synthetic `http_fetch.fetch_attempt` row is allowed for URL1003. No existing `http_fetch.fetch_attempt` row may be rewritten for URL1003. The frontier terminal state is preserved as the current canonical operational state, and the historical attempt rows remain audit evidence.

### 8.4 Final image item 4/5 close condition

Image item 4/5 can proceed to final seal only if the next read-only gate proves:

1. `retry_wait` HTTP 3xx rows remain `0`
2. dead high-priority HTTP 3xx rows remain `0`
3. HTTP 3xx mismatch rows remain `0`
4. URL1003 is documented as the single pre-patch frontier-terminal exception
5. no fetch-attempt history rewrite occurred
6. service remains inactive and disabled
7. crawler and browser process counts remain `0`
8. raw evidence count and byte total remain stable

Required next gate:

`FULL_R4_P2C76AE4_HTTP_3XX_HISTORICAL_ALIGNMENT_DECISION_DOC_AUDIT_READONLY_R1`

