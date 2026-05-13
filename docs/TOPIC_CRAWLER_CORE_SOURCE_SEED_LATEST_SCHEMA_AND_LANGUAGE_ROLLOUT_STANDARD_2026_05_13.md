# TOPIC_CRAWLER_CORE_SOURCE_SEED_LATEST_SCHEMA_AND_LANGUAGE_ROLLOUT_STANDARD_2026_05_13

Status: canonical planning standard, not a runtime activation.
Created by gate: `SOURCE_SEED_R209C_GLOBAL_SCHEMA_AND_LANGUAGE_ROLLOUT_STANDARD_DOC_PATCH_LOCAL_ONLY`.
Reference commit before doc patch: `bdd3a441a47894fdefcbc25809427925312ca99d`.
Reference date: `2026-05-13`.

This document fixes the current source/seed catalog schema and language rollout rules for LogisticSearch crawler_core startpoint catalogs.

## 1. Purpose

This document exists so every rolled-out language catalog can be developed with the same standard instead of drifting by language.

The immediate goal is:

1. keep English sealed as the global super-expansion reference;
2. keep French sealed as the directory-first compact reference;
3. migrate/backfill Turkish, German, and Arabic to the same latest schema and roughly French-level scale;
4. normalize Chinese to the latest schema after the priority TR/DE/AR backfills;
5. keep pi51c sync, DB insert, live frontier activation, crawler start, systemd mutation, and URL fetch blocked until explicit later gates.

## 1.1 All-25-language schema principle

The latest `source_families_v2` standard applies to every one of the 25 LogisticSearch source/seed languages, not only Turkish, German, Arabic, English, Chinese, or French.

Every language must converge to the same schema, safety policy, not-live policy, README indexing discipline, decision-document discipline, and final-seal discipline.

Language differences are allowed only as explicit language-profile decisions, not as schema drift.

The allowed profile differences are:

1. `global_reference_language`: a world-scale reference language. English currently uses this profile.
2. `large_special_language`: a strategically large or structurally special language. Chinese currently uses this profile because it already has a large source/seed surface and may require country/script/platform-specific handling.
3. `compact_directory_first_language`: a normal high-quality language catalog profile. French currently proves this model.
4. `priority_backfill_language`: a rolled-out language that must be normalized and backfilled before pi51c sync. Turkish, German, and Arabic currently use this temporary work profile.
5. `future_rollout_language`: a language not yet rolled out as a startpoint catalog; it must start directly from the latest schema and must not repeat legacy schema shapes.

These profiles change target scale and research strategy only. They do not change the required schema, disabled/not-live runtime policy, or safety rules.

## 1.2 25-language rollout design rule

All remaining language catalogs must be designed from the latest schema on day one.

The full language rollout must not create a second-class schema for smaller languages.

For each language, the research plan must first declare its profile:

- global reference language;
- large special language;
- compact directory-first language;
- priority backfill language;
- future rollout language.

After the profile is declared, the plan must define the target range:

- English-like global/reference languages may exceed 150 source families and 300 seed surfaces when justified.
- Chinese-like special languages may use larger language-specific scale and special handling when justified.
- Compact directory-first languages should usually target about 35-45 source families and about 70-95 seed surfaces/URLs.
- Smaller markets may still use the same schema with fewer sources only if a documented research gate proves that high-quality sources are genuinely limited.
- No language may use a legacy schema merely because it has fewer sources.

## 1.3 Reference and special-language status

English is the current global reference language. It is intentionally larger than Chinese and functions as the broadest source/seed catalog model.

Chinese is a current large special language. Its special status is about scale, script/platform structure, and later schema normalization priority. It does not exempt Chinese from the latest schema.

French is the compact directory-first reference language. It proves that a language can be high-quality without English-scale volume.

Turkish, German, and Arabic are not the only target languages. They are only the immediate priority backfill languages because they were already rolled out in older or semi-legacy schema shapes and must be repaired before pi51c sync.

Every future language must use this same standard.


## 2. Current reference catalogs

### 2.1 English reference

English is the large global reference catalog.

- Catalog: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- SHA256: `e7c71305a77c4a37850d8dbea7317a8fff9e3e66db921a833103013758aa771c`
- Schema: `source_families_v2`
- Candidate manifest: `true`
- Live: `false`
- Source families: `171`
- Seed surfaces: `450`
- Seed URLs: `1350`
- Unique seed URLs: `450`
- Unique hosts: `150`
- Decision document: `docs/TOPIC_CRAWLER_CORE_ENGLISH_SOURCE_SEED_SUPER_EXPANSION_DECISION_2026_05_13.md`
- Decision document SHA256: `686f9e182bc6f1451b0d8c487f3d4f4dd7a4fad007b77d56b64aff4440fefd50`

English proves the large-scale model: shared host parents such as FIATA, WCA, IATA, FreightNet, and CargoYellowPages may own many subordinate country/category seed surfaces, while still keeping one source family per real source family.

### 2.2 French reference

French is the compact directory-first target model.

- Catalog: `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json`
- SHA256: `5fe55427ec02f960142e95158464d6a8938e3736418c688add9f7e8ff562af5d`
- Schema: `source_families_v2`
- Candidate manifest: `true`
- Live: `false`
- Source families: `37`
- Seed surfaces: `72`
- Seed URLs: `72`
- Unique seed URLs: `72`
- Unique hosts: `38`

French proves the smaller language target: about 35-45 source families and about 70-95 seed surfaces/URLs are enough when quality is high and directory-first sources are prioritized.

## 3. Latest schema standard

Every rolled-out language catalog must converge to this top-level contract:

- `schema`: `source_families_v2`
- `schema_version`: `source_families_v2`
- `catalog_version`: language-specific catalog version, for example `turkish_source_families_v2`
- `language_code`: ISO-style project language code, for example `tr`
- `language_alias`: same as the project language code unless intentionally different
- `language_name`: human-readable English language name
- `candidate_manifest`: `true`
- `is_live`: `false`
- `runtime_activation_policy`: `pi51c_live_probe_required_before_db_or_frontier_insert`
- `runtime_policy`: explicit not-live safety object
- `metrics`: internally consistent catalog metrics
- `source_families`: source family records

The standard reference catalogs are English and French.

## 4. Required runtime safety policy

Every catalog must stay non-live until a later explicit pi51c/live gate.

Required top-level runtime policy:

- `live_frontier_activation`: `false`
- `db_insert_allowed`: `false`
- `url_fetch_allowed_in_catalog_gate`: `false`
- `crawler_start_allowed_in_catalog_gate`: `false`
- `pi51c_sync_allowed_in_catalog_gate`: `false`
- `manual_review_required`: `true`
- `no_aggressive_pagination`: `true`
- `same_day_full_country_expansion`: `false`
- `max_initial_depth`: `0_or_1`

Required source-family flags:

- `is_enabled`: `false`
- `needs_live_check`: `true`
- `db_insert_allowed`: `false`
- `url_fetch_allowed_in_catalog_gate`: `false`

Required seed-surface flags:

- `is_enabled`: `false`
- `needs_live_check`: `true`
- `db_insert_allowed`: `false`
- `url_fetch_allowed_in_catalog_gate`: `false`

## 5. Crawler / Parse / Desktop boundary rule

Crawler_Core stores discovered page links only as raw link evidence.

Raw discovered links are not `added_seeds`.

Parse_Core creates `added_seeds` only after pre-ranking, dedupe, policy checks, and light validation.

Desktop_Import on Ubuntu Desktop converts pre-ranking into real ranking/final rank and performs heavier enrichment, normalization, and search-ready output generation.

## 6. Source quality priority order

For every language, prioritize sources in this order:

1. official government registers;
2. official customs broker / forwarder / transport authorization lists;
3. official port, airport, rail, and logistics-zone directories;
4. national freight forwarder, customs broker, road transport, maritime, warehouse, and cold-chain association member directories;
5. chamber category member directories when they have usable logistics/customs/freight categories;
6. trade fair exhibitor directories only when sector-focused and current enough;
7. commercial directories only as controlled fallback, never as the main authority layer.

Commercial fallback sources must be lower priority, manually reviewed, deduped, and prevented from dominating the scheduler.

## 7. URL policy

Every catalog must enforce:

- HTTPS-only seed URLs;
- no duplicate source family codes;
- no duplicate seed surface codes;
- no duplicate canonical seed URLs after exact dedupe;
- no direct company import from PDFs or mixed chamber/category pages;
- PDF/download/ZIP surfaces must declare handling gates;
- same source URL must not create two top-level source families;
- regional relevance can be folded into the parent source instead of duplicating canonical URLs.

## 8. Current rolled-out language state

| Language | Current status | Schema state | Source families | Seed surfaces | Seed URLs | Next action |
|---|---|---:|---:|---:|---:|---|
| English (`en`) | sealed super-expansion reference | latest | 171 | 450 | 1350 | keep unchanged |
| French (`fr`) | sealed compact directory-first reference | latest | 37 | 72 | 72 | keep unchanged except minor runtime-policy normalization if explicitly gated |
| Turkish (`tr`) | needs latest schema + backfill | legacy | 18 | 18 | 22 | normalize + backfill to about 40/80 |
| German (`de`) | needs latest schema + backfill | legacy | 19 | 19 | 23 | normalize + backfill to about 40/80 |
| Arabic (`ar`) | needs top-level latest schema + backfill | semi-legacy | 18 | 30 | 0 | normalize + backfill to about 40/80 |
| Chinese (`zh`) | needs latest schema normalization after priority backfills | semi-legacy | 105 | 106 | 106 | normalize after TR/DE/AR |

## 9. Language rollout targets

### 9.1 English target

English must remain globally dominant.

Current sealed target:

- source families: `171`
- seed surfaces: `450`
- seed URLs: `1350`

No further English expansion is needed before TR/DE/AR normalization/backfill.

### 9.2 French target

French is already in the compact target range:

- target source families: about 35-45
- target seed surfaces: about 70-95
- current source families: `37`
- current seed surfaces: `72`

### 9.3 Turkish, German, Arabic target

Turkish, German, and Arabic must be brought to roughly French-level quality and scale before pi51c sync.

Practical target per language:

- source families: about 40
- seed surfaces: about 80
- seed URLs: about 80
- target range: 35-45 source families and 70-95 seed surfaces/URLs

Each language must have a separate:

1. read-only research plan;
2. decision document local patch;
3. decision document audit;
4. decision document commit/push;
5. JSON latest-schema backfill local patch;
6. JSON audit;
7. JSON commit/push;
8. README index update;
9. final seal.

### 9.4 Chinese target

Chinese is already large enough for now:

- current source families: `105`
- current seed surfaces: `106`
- current seed URLs: `106`

Chinese should be normalized to latest schema after TR/DE/AR reach target. No immediate Chinese source-count backfill is required before TR/DE/AR.

## 10. Planned gate order

Immediate order after English seal:

1. classify any Turkish planning harness failure without mutation;
2. create and commit this global schema/language rollout standard document;
3. resume Turkish decision document and catalog rewrite;
4. finish Turkish final seal;
5. repeat for German;
6. repeat for Arabic;
7. normalize Chinese schema;
8. run all-language rollup;
9. only then evaluate pi51c sync preflight.

Current planned next language work:

- `SOURCE_SEED_R209B_FAILURE_CLASSIFICATION_READONLY`
- `SOURCE_SEED_R210_TURKISH_LATEST_SCHEMA_BACKFILL_DECISION_DOC_PATCH_LOCAL_ONLY`
- Turkish catalog latest-schema rewrite/backfill gates
- German latest-schema rewrite/backfill gates
- Arabic latest-schema rewrite/backfill gates
- Chinese latest-schema normalization gates

## 11. pi51c sync rule

pi51c sync is not allowed now.

pi51c sync remains deferred until:

1. English final seal is clean;
2. French reference remains clean;
3. Turkish reaches latest schema and about 40/80;
4. German reaches latest schema and about 40/80;
5. Arabic reaches latest schema and about 40/80;
6. Chinese schema normalization is either completed or explicitly deferred by a documented gate;
7. all catalog metrics, README index rows, decision docs, and GitHub main are aligned.

Until then:

- no DB insert;
- no frontier insert;
- no live probe;
- no crawler start;
- no systemd mutation;
- no pi51c runtime sync.

## 12. Required GitHub documentation rule

For every language, GitHub must contain:

1. source/seed decision document;
2. latest-schema catalog JSON;
3. README index row with current metrics;
4. final seal evidence in terminal output before moving to the next language.

README must be updated after each catalog metric change.

## 13. R209B Turkish note

R209B produced a planning harness failure because the exact unique URL expectation was too rigid.

Observed R209B facts:

- projected Turkish source families: 40;
- projected Turkish seed surfaces: 80;
- projected Turkish raw seed URL count: 84;
- projected Turkish unique seed URL count after exact dedupe: 77;
- target range check still passed because 77 is inside 70-95;
- UAB duplicate URLs were repaired by folding duplicate UAB references under `tr_uab_tio_official_registers`.

This should be classified as a harness expectation issue, not a content failure, before the Turkish decision document gate continues.

## 14. Non-negotiable rule

No language catalog becomes live merely because it is added to GitHub.

GitHub catalog state is a candidate manifest only.

Runtime activation requires a later, explicit, one-source-at-a-time pi51c live probe and controlled crawler_core readiness gate.
