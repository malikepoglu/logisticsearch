# Queue Core / Queue Worker Canonical C++ Runtime Placeholder — 2026-06-13

## Status

This document defines the canonical placeholder for the future C++ queue layer.

This step is documentation and placeholder-directory only.

No runtime activation is allowed in this step.

- No DB mutation.
- No crawler start.
- No systemd mutation.
- No frontier insertion.
- No raw fetch mutation.
- No JSON feed activation.

## Canonical runtime names

| Type | Canonical names |
|---|---|
| Core layers | `preparation_core`, `crawler_core`, `process_core`, `ai_rank_core`, `port_core`, `compression_core`, `queue_core` |
| Worker/service/pipeline directories | `preparation_worker`, `crawler_worker`, `process_worker`, `ai_rank_worker`, `port_worker`, `compression_worker`, `queue_worker` |

## New C++ runtime placeholders

| Directory | Purpose |
|---|---|
| `makpi51crawler/cpp_live_runtime/queue_core/` | Future queue-layer core logic for selecting and preparing link-feed JSON. |
| `makpi51crawler/cpp_live_runtime/queue_worker/` | Future worker/service/pipeline side that will feed prepared link JSON to `crawler_core`. |

## Role boundary

`queue_core` and `queue_worker` belong to the C++ runtime.

They will work with:

- `process_core`
- `crawler_core`

Future role:

1. receive or derive new candidate links from controlled sources,
2. represent those links as JSON,
3. feed eligible new-link JSON to `crawler_core`,
4. keep ownership boundaries strict.

`crawler_core` remains limited to fetch/raw/finalize behavior and must not become the owner of broad new-link promotion policy.

## JSON direction

The future JSON feed format should be similar in discipline to the existing startpoint/source-family JSON catalog files.

The future queue JSON must be controlled, explicit, and auditable. It must not be activated from these placeholder directories until a later dedicated gate defines:

- schema,
- validation,
- ownership,
- enqueue rules,
- deduplication rules,
- DB boundary,
- runtime activation gate.

## Old-name correction debt

The canonical naming direction is:

- `parse_core` -> `process_core`
- `desktop_import` -> `port_core`
- `ai_ranking` / `ranking_neural` -> `ai_rank_core`
- `crawler_core_worker` -> `crawler_worker`

Existing physical paths may still contain older names during migration audits. Future documentation and comments should use the canonical names unless explicitly referring to legacy/current file paths.

## Immediate placeholder decision

The directories are intentionally empty except `.gitkeep`.

This step only creates the C++ placeholder directories and documentation so Desktop, GitHub, pi51c repo, and pi51c live can be aligned before continuing crawler-worker review work.
