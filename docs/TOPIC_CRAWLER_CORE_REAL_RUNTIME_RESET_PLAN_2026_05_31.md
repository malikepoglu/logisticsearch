# Crawler Core Real Runtime Reset Plan

Gate: `FULL_R4_P2C81A_REAL_RUNTIME_RESET_PLAN_DECISION_DOC_LOCAL_ONLY_R1`

Canonical head before reset plan: `4f16e7b0aa7c72cf7df834d6028a2768f1f7993f`

Decision doc dependency: `docs/TOPIC_CRAWLER_CORE_26_JSON_ROTATION_MANIFEST_AND_RESET_DECISION_2026_05_31.md`

## 1. Non-negotiable rule

The test surface must be the real runtime surface.

`TEST_SURFACE_MUST_BE_THE_REAL_RUNTIME_SURFACE`

The Ubuntu Desktop independent 26 JSON rotation test must use the real existing startpoint catalog JSON files under:

`makpi51crawler/catalog/startpoints`

Separate testing directory, separate fixture JSON directory, separate test database, or synthetic JSON surface is forbidden.

## 2. Reset target

Reset target:

`CRAWLER_ZSTD_RAW_JSON_DB_AND_COUNTERS`

The reset is not performed by this document gate.

The reset must be performed only by a later explicit mutation gate after this document is audited, committed, pushed, synced to pi51c `/logisticsearch/repo`, and post-sync sealed.

## 3. Baseline captured by P2C81

| Metric | Value |
|---|---:|
| Desktop/GitHub/pi51c repo head | `4f16e7b0aa7c72cf7df834d6028a2768f1f7993f` |
| Repo JSON total | `56` |
| Real startpoint JSON count | `26` |
| Wrong testing surface exists | `FALSE` |
| Service active | `inactive` |
| Service enabled | `disabled` |
| Crawler process count | `0` |
| Browser process count | `0` |
| Raw file count | `6092` |
| Raw total bytes | `812424132` |
| Control state | `pause` |
| Control version | `85` |
| Max fetch_attempt_id | `1922` |
| frontier.url rows | `2105` |
| frontier.host rows | `722` |
| http_fetch.fetch_attempt rows | `1922` |
| http_fetch body path rows | `1883` |
| distinct body path rows | `1883` |
| body bytes sum | `454013656` |
| retry_wait HTTP 3xx rows | `0` |
| dead high-priority HTTP 3xx rows | `0` |
| HTTP 3xx mismatch rows | `0` |
| global mismatch rows | `223` |
| historical alignment count | `13` |
| retry_wait expired lease rows | `0` |
| non-retry_wait lease rows | `0` |

## 4. Reset-sensitive DB tables from P2C81 inventory

Only these current base tables were returned as reset-sensitive candidates:

| Schema | Table | Reset role |
|---|---|---|
| `frontier` | `host` | Host identity, user-agent token, robots and host-level crawler counters. |
| `frontier` | `url` | URL queue, state, lease, score, attempts and crawl scheduling. |
| `http_fetch` | `fetch_attempt` | Fetch attempt ledger and body storage path references. |
| `http_fetch` | `robots_txt_cache` | Robots cache used by crawler fetch policy. |
| `ops` | `webcrawler_runtime_control` | Runtime control row; must be reset only to safe paused state, not deleted blindly. |

## 5. Reset-sensitive sequences from P2C81 inventory

| Schema | Sequence |
|---|---|
| `frontier` | `host_host_id_seq` |
| `frontier` | `url_url_id_seq` |
| `http_fetch` | `fetch_attempt_fetch_attempt_id_seq` |
| `http_fetch` | `robots_txt_cache_robots_cache_id_seq` |

## 6. Raw evidence surface

Current raw root:

`/srv/webcrawler/raw_fetch`

Current raw evidence summary:

| Metric | Value |
|---|---:|
| raw file count | `6092` |
| raw total bytes | `812424132` |
| DB body path rows | `1883` |
| DB distinct body path rows | `1883` |
| DB body bytes sum | `454013656` |

The later reset mutation gate may remove or archive real raw evidence only if it states the exact raw root and verifies service/crawler/browser stillness before and after.

No raw delete, raw move, or raw compression is allowed in this document gate.

## 7. Forbidden reset scope

The reset must not mutate:

1. Git history,
2. Git tracked docs,
3. source catalog JSON files,
4. taxonomy JSON files,
5. real 26 startpoint catalog JSON files,
6. Python runtime source files,
7. PostgreSQL schema files in repo,
8. systemd enable state,
9. systemd unit files,
10. pi51c live runtime code by copy or rsync,
11. any separate testing directory,
12. any separate test database,
13. any synthetic replacement JSON.

## 8. Required reset mutation shape

The later reset mutation gate must be explicit and narrow.

Required shape:

1. verify Desktop/GitHub/pi51c repo clean and aligned,
2. verify service inactive and disabled,
3. verify crawler/browser process count is zero,
4. verify DSN is loaded without printing it,
5. capture DB row counts before mutation,
6. capture raw file count and bytes before mutation,
7. pause or preserve runtime control in safe `pause` state,
8. reset only approved crawler runtime DB rows/counters,
9. reset only approved raw evidence files under `/srv/webcrawler/raw_fetch`,
10. reset approved sequences only after table reset,
11. keep the 26 real startpoint JSON files untouched,
12. keep taxonomy and source catalogs untouched,
13. verify DB row counts after reset,
14. verify raw file count and bytes after reset,
15. verify service remains inactive/disabled,
16. verify crawler/browser process count remains zero,
17. produce a post-reset seal before any independent 26 JSON test.

## 9. Reset acceptance target

The exact post-reset counts must be decided in the next read-only audit before mutation.

Candidate post-reset target:

| Surface | Candidate post-reset expectation |
|---|---|
| `http_fetch.fetch_attempt` | `0` rows |
| `http_fetch.robots_txt_cache` | `0` rows unless deliberately retained |
| `frontier.url` | either rebuilt from real 26 startpoints or `0`; must be decided before mutation |
| `frontier.host` | either rebuilt from real 26 startpoints or preserved with LS token; must be decided before mutation |
| `ops.webcrawler_runtime_control` | preserved or recreated as safe `pause` |
| `/srv/webcrawler/raw_fetch` | `0` files only if explicit raw delete is approved |
| real 26 startpoint JSON | unchanged |
| taxonomy JSON | unchanged |

This document deliberately does not choose truncate order or SQL commands yet. That belongs to a dedicated reset execution plan after this document is sealed.

## 10. Next gate

Next required gate:

`FULL_R4_P2C81B_REAL_RUNTIME_RESET_PLAN_DECISION_DOC_AUDIT_READONLY_R1`

After that:

1. commit and push this reset plan decision doc,
2. post-push seal,
3. pi51c repo doc-only sync,
4. pi51c post-sync seal,
5. final reset plan seal,
6. write exact reset execution plan,
7. perform explicit reset mutation only after all previous gates pass.
