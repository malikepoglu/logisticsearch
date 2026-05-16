# Crawler Core Source-Seed Startpoint JSON Canonical Rules — 25 Language Standard

Status: canonical rule document
Scope: crawler_core source-seed startpoint catalogs
Schema: source_families_v2
Runtime state: candidate manifest only; never live by default.

This file is the mandatory rule authority for all 25 language source-seed startpoint catalogs.

## 1. Mandatory GitHub-first read gate

Before preparing, repairing, auditing, committing, syncing, or extending startpoints for any language, the first operation must be a read-only GitHub raw read of this exact rule document.

Canonical GitHub raw URL:

    https://raw.githubusercontent.com/malikepoglu/logisticsearch/main/docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md

For sealed gates, prefer a commit-pinned raw URL:

    https://raw.githubusercontent.com/malikepoglu/logisticsearch/<EXPECTED_HEAD>/docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md

Minimum required GitHub raw needles:

    source_families_v2
    candidate_manifest=true
    is_live=false
    pi51c_live_probe_required_before_db_or_frontier_insert
    no DB insert
    no frontier activation
    no URL fetch/live probe
    no pi51c live activation
    seed_urls
    source_families

Stop if GitHub raw read fails.
Stop if any required needle is missing.
Do not use memory, local assumptions, old chat text, copied snippets, or editor state as rule authority.

## 2. Non-negotiable safety boundary

Every startpoint catalog is candidate data only until a later explicit activation gate.

Required catalog state:

    candidate_manifest=true
    is_live=false
    runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert

Hard forbidden actions during source-seed authoring, repair, standardization, audit, commit, and normal repo-sync gates:

    no DB insert
    no frontier activation
    no crawler start
    no crawler stop
    no systemd mutation
    no URL fetch/live probe
    no pi51c live activation
    no secret/DSN/token/password print

pi51c repo sync is allowed only in a separate explicit sync gate.
pi51c live runtime copy is forbidden unless the exact live-copy target is explicitly named and gated.

## 3. Canonical top-level catalog shape

Every language catalog must use source_families_v2.

Required top-level keys:

    schema
    schema_version
    catalog_version
    language_code
    language_name
    language_alias
    candidate_manifest
    is_live
    runtime_activation_policy
    standardization_policy
    standardization_gate
    last_rewritten_by_gate
    safety_guards
    metrics
    dropped_empty_source_families
    source_families

Forbidden top-level keys:

    last_repaired_by_gate
    candidate_seed_urls
    seed_url
    source_url
    live_enabled
    frontier_inserted
    db_inserted

Required top-level values:

    schema=source_families_v2
    schema_version=source_families_v2
    catalog_version=<language_name_lowercase>_source_families_v2
    language_code=<ISO language code>
    candidate_manifest=true
    is_live=false
    runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert

## 4. Canonical source family shape

Required source family keys:

    source_family_index
    source_family_code
    source_family_name
    source_name
    source_root_url
    source_host
    source_categories
    language_code
    language_name
    source_quality_tier
    quality_tier
    source_decision
    decision
    candidate_manifest
    is_live
    enabled
    needs_live_check
    seed_surface_count
    seed_url_count
    family_metadata
    seed_surfaces

Required source family values:

    candidate_manifest=true
    is_live=false
    enabled=false
    needs_live_check=true

Allowed quality tiers:

    A+
    A
    A-
    B+
    B
    B-

Allowed decisions:

    ACCEPT
    ACCEPT_REVIEW
    HOLD

Source hierarchy rule:

A source family is normally the main host/source organization, not every country/path subsection. Multi-country pages under one host, such as FIATA country pages, must remain one coherent source family or a clearly subordinate seed surface under the correct source family.

## 5. Canonical seed surface shape

Required seed surface keys:

    seed_surface_index
    family_seed_surface_index
    seed_surface_code
    seed_surface_name
    source_family_code
    surface_type
    seed_quality_tier
    quality_tier
    seed_decision
    decision
    candidate_manifest
    is_live
    enabled
    needs_live_check
    surface_metadata
    seed_urls

Required seed surface values:

    candidate_manifest=true
    is_live=false
    enabled=false
    needs_live_check=true

The scalar field seed_url is forbidden. Use seed_urls only.

## 6. Canonical seed URL shape

Every URL must be represented as an object inside seed_urls.

Required seed URL object keys:

    seed_url_index
    url
    url_type
    is_primary
    candidate_manifest
    is_live
    enabled
    needs_live_check
    runtime_activation_policy
    safety_state

Required seed URL object values:

    candidate_manifest=true
    is_live=false
    enabled=false
    needs_live_check=true
    runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert

URL rules:

1. URL must be HTTPS.
2. Duplicate URLs are forbidden inside the same language catalog.
3. Empty URLs are forbidden.
4. URL fetch/live probe is forbidden while authoring the catalog.
5. URL validation in source-seed gates is structural only unless a later explicit live-probe gate is opened.

## 7. Required metrics

Every catalog must include metrics matching computed content.

Required metrics:

    source_family_count
    seed_surface_count
    seed_url_count
    unique_seed_url_count
    duplicate_seed_url_count
    non_https_seed_url_count

Required invariants:

    seed_url_count == unique_seed_url_count
    duplicate_seed_url_count == 0
    non_https_seed_url_count == 0

## 8. README behavior

docs/README.md must not contain ad-hoc per-language detailed blocks that only exist for one language.

Allowed README surfaces:

1. Current sealed startpoint catalogs table.
2. Source-seed policy and decision records list.
3. Link to this canonical rule document.
4. Short next-language decision block when needed.

Every rolled language must be represented consistently in the sealed catalog table.
Every language-specific decision document must be represented consistently under source-seed policy and decision records.

## 9. Required per-language workflow

For every language, use this order:

1. Read this canonical rule file from GitHub raw.
2. Verify required needles.
3. Read current repo state.
4. Confirm clean or intentional dirty scope.
5. Confirm target language catalog/doc absence or existing state.
6. Create or repair decision document.
7. Audit decision document.
8. Create or repair catalog JSON using this standard.
9. Audit catalog JSON.
10. Update README table/list consistently.
11. Audit README.
12. Commit/push in small scoped gates.
13. Post-push seal.
14. pi51c repo sync only in explicit sync gate.
15. pi51c live copy only in explicit live-copy gate.
16. Never activate DB/frontier/crawler during candidate source-seed rollout.

## 10. Canonical 25-language rollout order

    en
    tr
    de
    ar
    fr
    zh
    es
    it
    pt
    nl
    ru
    uk
    bg
    cs
    el
    hu
    ro
    ja
    ko
    hi
    bn
    ur
    id
    vi
    he

A later gate may change the order only by documenting the reason and updating this rule document.

## 11. Commit discipline

Use small, scoped commits.

Allowed commit patterns:

    docs(source-seed): add <Language> startpoint decision
    feat(source-seed): add <Language> startpoint catalog
    docs(source-seed): index <Language> startpoint catalog
    docs(source-seed): standardize rolled startpoint catalogs
    docs(source-seed): add canonical startpoint rules

Before every commit:

1. Verify exact dirty scope.
2. Verify exact staged scope.
3. Verify no unrelated file changed.
4. Verify no secrets.
5. Verify no live activation flags.
6. Verify no DB/frontier/crawler/systemd mutation.

## 12. Mandatory future prompt rule

When asking ChatGPT, Codex, or any assistant to work on a language startpoint catalog, the prompt must include:

    First read the canonical source-seed startpoint JSON rules from GitHub raw, verify the required needles, and stop if the rule file cannot be read. Do not use memory or local assumptions as the rule authority.

This sentence is mandatory for all future language-specific source-seed tasks.
