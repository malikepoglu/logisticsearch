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

<!-- SOURCE_SEED_METADATA_MODEL_CANONICAL_EXTENSION_BEGIN -->

## Source-seed language / locale / country metadata model

This section is the canonical extension for separating catalog target language from real URL content language and country coverage.

### Required seed-level metadata fields

Every `seed_urls[]` entry must carry the following metadata before a catalog can be treated as final-sealed:

- `target_language_code`
  - Catalog rollout target language.
  - Example: Bulgarian catalog uses `bg`.
- `content_language_code`
  - Actual readable content language of the URL.
  - Example: `/en/members` uses `en` even when the catalog target is `bg`.
- `url_locale_code`
  - URL path or locale signal when available.
  - Example: `/en/...` uses `en`, `/bg/...` uses `bg`.
- `source_country_codes`
  - ISO-like uppercase country codes for the site or organization origin.
  - Example: Bulgarian association source uses `["BG"]`.
- `covered_country_codes`
  - ISO-like uppercase country codes for companies, listings, or geography covered by the page.
  - Example: Bulgaria member directory uses `["BG"]`.
- `language_fit`
  - Controlled enum describing how the URL language fits the target catalog.
- `coverage_fit`
  - Controlled enum describing how the URL country coverage fits the catalog.
- `locale_review_status`
  - Controlled enum describing whether locale/native/fallback status was reviewed.

### `language_fit` enum

Allowed values:

- `native`
  - Content language matches the catalog target language.
- `multilingual`
  - Page has multiple language surfaces and includes the target language.
- `english_fallback`
  - Content is English, but the source is country-relevant and no verified native alternative has been accepted yet.
- `foreign_language_country_relevant`
  - Content is not target language and not English, but the source is still country-relevant.
- `unknown`
  - Language must be manually reviewed before activation.

### `coverage_fit` enum

Allowed values:

- `country_primary`
  - The page primarily covers the catalog country.
- `country_slice_of_global_directory`
  - The page is a country-specific slice inside a global or regional directory.
- `official_company_local_entity`
  - The page is an official local entity, office, or branch page.
- `regional_or_industry_context`
  - The page is useful regional or industry context but not a pure country directory.
- `weak_discovery`
  - Weak source used only as a discovery candidate and requiring manual review.

### `locale_review_status` enum

Allowed values:

- `native_locale_verified`
  - Native target-language page is verified.
- `english_fallback_verified`
  - English fallback is intentionally accepted as country-relevant.
- `needs_native_alternative_check`
  - English or foreign-language URL may be useful, but native alternative must still be searched.
- `broken_or_blocked`
  - URL is broken, blocked, or returns persistent failure in live/reachability checks.
- `manual_review_required`
  - Human review required before activation.

### Naming rule

Top-level `language_code` remains the catalog rollout target language.

Seed-level actual content language must be represented as `content_language_code`.

Do not use a plain ambiguous `language` field for new schema work. If compatibility ever requires a `language` field, it must be documented as a seed-level alias of `content_language_code`, not as the catalog target language.

### Correct modeling example

Indented JSON example:

    {
      "url": "https://nsbs.bg/en/members",
      "quality_status": "A_PLUS",
      "target_language_code": "bg",
      "content_language_code": "en",
      "url_locale_code": "en",
      "source_country_codes": ["BG"],
      "covered_country_codes": ["BG"],
      "language_fit": "english_fallback",
      "coverage_fit": "country_primary",
      "locale_review_status": "needs_native_alternative_check",
      "candidate_manifest": true,
      "is_live": false,
      "enabled": false,
      "needs_live_check": true,
      "runtime_activation_policy": "pi51c_live_probe_required_before_db_or_frontier_insert"
    }

### Activation boundary

These metadata fields do not make a URL live.

A seed remains candidate-only until a separate gated live/reachability probe, locale review, country coverage review, commit/push seal, and later pi51c sync line explicitly approve it.

<!-- SOURCE_SEED_METADATA_MODEL_CANONICAL_EXTENSION_END -->

<!-- SOURCE_SEED_REACHABILITY_STATUS_FORMAT_RULE_BEGIN -->

## Reachability status format rule

`locale_review_status` may encode candidate-only reachability review outcomes when a source-seed URL has been checked by a controlled read-only probe.

Allowed reachability-related use:

- `broken_or_blocked`
  - Use for persistent or material HTTP 4xx/5xx failure, DNS/network/TLS failure, blocked source, or equivalent access failure.
  - This is a candidate-review marker only.
  - It must not delete the URL.
  - It must not activate DB/frontier/crawler/runtime behavior.
  - It must preserve enough context for later repair, replacement, or retest.
- `needs_native_alternative_check`
  - Keep for reachable English fallback rows that still need native-language search.
  - Temporary rate-limit rows may stay here unless a later explicit reachability schema adds a separate retry field.
- `manual_review_required`
  - Use when locale or content language cannot be determined without human review.
- `native_locale_verified`
  - Use only when the URL itself is verified as native target-language content.
- `english_fallback_verified`
  - Use only when English fallback was intentionally accepted after review.

Do not overload `language_fit`, `coverage_fit`, or `content_language_code` to represent HTTP reachability.

Do not introduce runtime activation from this metadata.

<!-- SOURCE_SEED_REACHABILITY_STATUS_FORMAT_RULE_END -->

<!-- SOURCE_SEED_ENGLISH_METADATA_MODEL_RULE_BEGIN -->

## English metadata model rule

English metadata model rows follow the same general source-seed standard, with these English-specific interpretation rules:

- Top-level `language_code=en` means the rollout target is English.
- Seed-level `target_language_code=en` is required for every English catalog URL.
- Seed-level `content_language_code=en` is only accepted when URL/path/host/source semantics provide an English signal.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native English content.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; otherwise `ZZ`.
- `covered_country_codes` records covered country or region when inferable; otherwise `ZZ`.
- `country_slice_of_global_directory` is used for global directories or directory pages that represent country-specific slices.
- `official_company_local_entity` is used for company/local-entity pages where source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where country coverage is not a clean country slice.

English metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_ENGLISH_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_TURKISH_METADATA_MODEL_RULE_BEGIN -->

## Turkish metadata model rule

Turkish metadata model rows follow the general source-seed standard, with these Turkish-specific interpretation rules:

- Top-level `language_code=tr` means the rollout target is Turkish.
- Seed-level `target_language_code=tr` is required for every Turkish catalog URL.
- Seed-level `content_language_code=tr` is accepted only when URL/path/host/source semantics provide a Turkish signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Turkish logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Turkish content.
- `url_locale_code=tr` records visible Turkish locale or Turkish-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; otherwise `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for Turkish country coverage this is `TR`, otherwise `ZZ`.
- `country_primary` is used for Turkish country-primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Turkey slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Turkish source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Turkish coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Turkish-native alternative should later be considered.

Turkish metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_TURKISH_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_GERMAN_METADATA_MODEL_RULE_BEGIN -->

## German metadata model rule

German metadata model rows follow the general source-seed standard, with these German-specific interpretation rules:

- Top-level `language_code=de` means the rollout target is German.
- Seed-level `target_language_code=de` is required for every German catalog URL.
- Seed-level `content_language_code=de` is accepted only when URL/path/host/source semantics provide a German signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for German logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native German content.
- `url_locale_code=de` records visible German locale or German-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; otherwise `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for German country coverage this is `DE`, otherwise `ZZ`.
- `country_primary` is used for German country-primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Germany slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where German source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where German coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a German-native alternative should later be considered.

German metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_GERMAN_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_ARABIC_METADATA_MODEL_RULE_BEGIN -->

## Arabic metadata model rule

Arabic metadata model rows follow the general source-seed standard, with these Arabic-specific interpretation rules:

- Top-level `language_code=ar` means the rollout target is Arabic.
- Seed-level `target_language_code=ar` is required for every Arabic catalog URL.
- Seed-level `content_language_code=ar` is accepted only when URL/path/host/source semantics provide an Arabic signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Arabic logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Arabic content.
- `url_locale_code=ar` records visible Arabic locale or Arabic-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; otherwise `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for Arabic-region coverage this may include `AE`, `BH`, `EG`, `JO`, `LB`, `OM`, `QA`, `SA`; otherwise `ZZ`.
- `country_primary` is used for Arabic-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Arabic-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Arabic-region source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Arabic-region coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where an Arabic-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Arabic metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_ARABIC_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_CHINESE_METADATA_MODEL_RULE_BEGIN -->

## Chinese metadata model rule

Chinese metadata model rows follow the general source-seed standard, with these Chinese-specific interpretation rules:

- Top-level `language_code=zh` means the rollout target is Chinese.
- Seed-level `target_language_code=zh` is required for every Chinese catalog URL.
- Seed-level `content_language_code=zh` is accepted only when URL/path/host/source semantics provide a Chinese signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Chinese logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Chinese content.
- `url_locale_code=zh` records visible Chinese locale or Chinese-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Chinese-region surfaces this may include `CN`, `HK`, and `TW`; otherwise `ZZ` or another explicit non-target source country such as `DE`.
- `covered_country_codes` records covered country or region when inferable; for Chinese-region coverage this may include `CN`, `HK`, and `TW`; otherwise `ZZ`.
- `country_primary` is used for Chinese-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Chinese-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Chinese-region source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Chinese-region coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Chinese-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Chinese metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_CHINESE_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_FRENCH_METADATA_MODEL_RULE_BEGIN -->

## French metadata model rule

French metadata model rows follow the general source-seed standard, with these French-specific interpretation rules:

- Top-level `language_code=fr` means the rollout target is French.
- Seed-level `target_language_code=fr` is required for every French catalog URL.
- Seed-level `content_language_code=fr` is accepted only when URL/path/host/source semantics provide a French signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for French logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native French content.
- `url_locale_code=fr` records visible French locale or French-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for French-region surfaces this may include `BE`, `CH`, `FR`, `LU`, `MA`, `MC`, `SN`, and `TN`; otherwise `ZZ` or another explicit non-target source country/region such as `EU`.
- `covered_country_codes` records covered country or region when inferable; for French-region coverage this may include `BE`, `CH`, `FR`, `LU`, `MA`, `MC`, `SN`, and `TN`; otherwise `ZZ`.
- `country_primary` is used for French-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for French-country or French-region slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where French-region source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where French-region coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a French-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

French metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_FRENCH_METADATA_MODEL_RULE_END -->
