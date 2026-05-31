# Crawler Core Real Runtime Reset Execution Plan

Gate: `FULL_R4_P2C82A_REAL_RUNTIME_RESET_EXECUTION_PLAN_DOC_LOCAL_ONLY_R1`

Canonical head: `48b285bf5c86ee10ddd4c4a78a986aadda2e1d0d`

Parent decision doc: `docs/TOPIC_CRAWLER_CORE_REAL_RUNTIME_RESET_PLAN_2026_05_31.md`

## 1. Absolute rule

`TEST_SURFACE_MUST_BE_THE_REAL_RUNTIME_SURFACE`

The independent 26 JSON test must use the real startpoint JSON files under `makpi51crawler/catalog/startpoints`.

No separate testing directory, no fixture JSON directory, no separate test database, no synthetic JSON replacement.

## 2. Reset target

`CRAWLER_ZSTD_RAW_JSON_DB_AND_COUNTERS`

This document is not the reset mutation gate.

## 3. P2C82 baseline

| Surface | Value |
|---|---:|
| repo head | `48b285bf5c86ee10ddd4c4a78a986aadda2e1d0d` |
| service active | `inactive` |
| service enabled | `disabled` |
| crawler count | `0` |
| browser count | `0` |
| raw root | `/srv/webcrawler/raw_fetch` |
| raw file count | `6092` |
| raw total bytes | `812424132` |
| frontier.host rows | `722` |
| frontier.url rows | `2105` |
| http_fetch.fetch_attempt rows | `1922` |
| http_fetch.robots_txt_cache rows | `722` |
| ops.webcrawler_runtime_control rows | `1` |
| control state | `pause` |
| control version | `85` |
| max fetch_attempt_id | `1922` |
| host token old LogisticSearchBot | `0` |
| host token LS | `722` |
| body path rows | `1883` |
| distinct body path rows | `1883` |
| body bytes sum | `454013656` |
| FK dependency rows | `0` |

## 4. Mutation gate guard list

The later mutation gate must stop immediately unless all are true:

1. Desktop, GitHub and pi51c repo are aligned at `48b285bf5c86ee10ddd4c4a78a986aadda2e1d0d`.
2. Desktop worktree is clean.
3. pi51c `/logisticsearch/repo` worktree is clean.
4. `logisticsearch-webcrawler.service` is inactive.
5. `logisticsearch-webcrawler.service` is disabled.
6. crawler process count is `0`.
7. browser process count is `0`.
8. live testing directory is absent.
9. real startpoint JSON count is `26`.
10. `LOGISTICSEARCH_CRAWLER_DSN` is loaded but never printed.

## 5. Approved DB reset order

FK dependency inventory returned `0` rows, but the reset order still remains conservative:

1. `http_fetch.fetch_attempt`
2. `http_fetch.robots_txt_cache`
3. `frontier.url`
4. `frontier.host`
5. `ops.webcrawler_runtime_control` preserved or recreated as safe `pause`

## 6. Approved sequence reset order

1. `http_fetch.fetch_attempt_fetch_attempt_id_seq`
2. `http_fetch.robots_txt_cache_robots_cache_id_seq`
3. `frontier.url_url_id_seq`
4. `frontier.host_host_id_seq`

P2C82 sequence baseline:

| Sequence | last_value | is_called |
|---|---:|---|
| `frontier.host_host_id_seq` | `752` | `t` |
| `frontier.url_url_id_seq` | `2110` | `t` |
| `http_fetch.fetch_attempt_fetch_attempt_id_seq` | `1922` | `t` |
| `http_fetch.robots_txt_cache_robots_cache_id_seq` | `3809` | `t` |

## 7. Approved raw reset surface

Only this raw root is in scope:

`/srv/webcrawler/raw_fetch`

Current raw count: `6092`

Current raw bytes: `812424132`

The later mutation gate may delete files only under this exact raw root after stillness guards pass.

## 8. Forbidden mutation scope

The reset must not mutate:

1. source catalog JSON,
2. taxonomy JSON,
3. the real 26 startpoint JSON files,
4. Python runtime source,
5. repo PostgreSQL schema files,
6. docs other than the reset execution result doc,
7. systemd unit files,
8. systemd enabled/disabled state,
9. live runtime code,
10. Git history,
11. any testing or fixture directory.

## 9. Post-reset expected state

| Surface | Expected after reset |
|---|---|
| `http_fetch.fetch_attempt` | `0` |
| `http_fetch.robots_txt_cache` | `0` |
| `frontier.url` | `0` before real 26 JSON reload |
| `frontier.host` | `0` before real 26 JSON reload |
| `ops.webcrawler_runtime_control` | one safe `pause` row |
| `/srv/webcrawler/raw_fetch` | `0` files if raw deletion is approved |
| real 26 startpoint JSON files | unchanged |
| taxonomy JSON | unchanged |
| service | inactive and disabled |
| crawler/browser process count | `0` |

## 10. Next gates

1. `FULL_R4_P2C82B_REAL_RUNTIME_RESET_EXECUTION_PLAN_DOC_AUDIT_READONLY_R1`
2. commit and push this execution plan doc
3. post-push seal
4. pi51c repo doc-only sync
5. final execution plan seal
6. explicit reset mutation gate
7. post-reset seal
8. Ubuntu Desktop independent 26 JSON rotation test
