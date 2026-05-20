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

<!-- SOURCE_SEED_SPANISH_METADATA_MODEL_RULE_BEGIN -->

## Spanish metadata model rule

Spanish metadata model rows follow the general source-seed standard, with these Spanish-specific interpretation rules:

- Top-level `language_code=es` means the rollout target is Spanish.
- Seed-level `target_language_code=es` is required for every Spanish catalog URL.
- Seed-level `content_language_code=es` is accepted only when URL/path/host/source semantics provide a Spanish signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Spanish logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Spanish content.
- `url_locale_code=es` records visible Spanish locale or Spanish-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Spanish rollout this may include `CO`, `DE`, `ES`, `GB`, and `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for this Spanish seal it is `ES` or `ZZ`.
- `country_primary` is used for Spanish-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Spanish-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Spanish source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Spanish coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Spanish-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Spanish metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_SPANISH_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_ITALIAN_METADATA_MODEL_RULE_BEGIN -->

## Italian metadata model rule

Italian metadata model rows follow the general source-seed standard, with these Italian-specific interpretation rules:

- Top-level `language_code=it` means the rollout target is Italian.
- Seed-level `target_language_code=it` is required for every Italian catalog URL.
- Seed-level `content_language_code=it` is accepted only when URL/path/host/source semantics provide an Italian signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Italian logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Italian content.
- `url_locale_code=it` records visible Italian locale or Italian-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Italian rollout this may include `EU`, `IT`, and `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for this Italian seal it is `IT` or `ZZ`.
- `country_primary` is used for Italian-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Italian-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Italian source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Italian coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where an Italian-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Italian metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_ITALIAN_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_PORTUGUESE_METADATA_MODEL_RULE_BEGIN -->

## Portuguese metadata model rule

Portuguese metadata model rows follow the general source-seed standard, with these Portuguese-specific interpretation rules:

- Top-level `language_code=pt` means the rollout target is Portuguese.
- Seed-level `target_language_code=pt` is required for every Portuguese catalog URL.
- Seed-level `content_language_code=pt` is accepted only when URL/path/host/source semantics provide a Portuguese signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Portuguese logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Portuguese content.
- `url_locale_code=pt` records visible Portuguese locale or Portuguese-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Portuguese rollout this may include `PT` and `ZZ`.
- `covered_country_codes` records covered country or region when inferable; for this Portuguese seal it is `PT` or `ZZ`.
- `country_primary` is used for Portuguese-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Portuguese-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Portuguese source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Portuguese coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Portuguese-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Portuguese metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_PORTUGUESE_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_DUTCH_METADATA_MODEL_RULE_BEGIN -->

## Dutch metadata model rule

Dutch metadata model rows follow the general source-seed standard, with these Dutch-specific interpretation rules:

- Top-level `language_code=nl` means the rollout target is Dutch.
- Seed-level `target_language_code=nl` is required for every Dutch catalog URL.
- Seed-level `content_language_code=nl` is accepted only when URL/path/host/source semantics provide a Dutch signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Dutch logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Dutch content.
- `url_locale_code=nl` records visible Dutch locale or Dutch-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Dutch rollout this may include `NL`, `ZZ`, `EU`, and `CO`.
- `covered_country_codes` records covered country or region when inferable; for this Dutch seal it is `NL` or `ZZ`.
- `country_primary` is used for Dutch-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Dutch-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Dutch source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Dutch coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Dutch-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Dutch metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_DUTCH_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_RUSSIAN_METADATA_MODEL_RULE_BEGIN -->

## Russian metadata model rule

Russian metadata model rows follow the general source-seed standard, with these Russian-specific interpretation rules:

- Top-level `language_code=ru` means the rollout target is Russian.
- Seed-level `target_language_code=ru` is required for every Russian catalog URL.
- Seed-level `content_language_code=ru` is accepted only when URL/path/host/source semantics provide a Russian signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Russian logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Russian content.
- `url_locale_code=ru` records visible Russian locale or Russian-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for Russian rollout this may include `RU`, `ZZ`, `CO`, and `GB`.
- `covered_country_codes` records covered country or region when inferable; for this Russian seal it is `RU` or `ZZ`.
- `country_primary` is used for Russian-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Russian-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Russian source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Russian coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Russian-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Russian metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_RUSSIAN_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_UKRAINIAN_METADATA_MODEL_RULE_BEGIN -->

## Ukrainian metadata model

Ukrainian metadata model rows follow the general source-seed standard, with these Ukrainian-specific interpretation rules:

- Top-level `language_code=uk` means the rollout target is Ukrainian.
- Seed-level `target_language_code=uk` is required for every Ukrainian catalog URL.
- Seed-level `content_language_code=uk` is accepted only when URL/path/host/source semantics provide a Ukrainian signal.
- Seed-level `content_language_code=en` records English fallback surfaces that may still be useful for Ukrainian logistics discovery.
- Seed-level `content_language_code=unknown` must stay under human/manual review and must not be treated as native Ukrainian content.
- `url_locale_code=uk` records visible Ukrainian locale, `/uk`, `/ua`, or Ukrainian-content URL signal.
- `url_locale_code=en` records visible English locale or English-content URL signal.
- `url_locale_code=und` records an undetermined URL locale.
- `source_country_codes` records source or organization origin when inferable; for this Ukrainian seal it may include `UA`, `ZZ`, and `CO`.
- `covered_country_codes` records covered country or region when inferable; for this Ukrainian seal it is `UA` or `ZZ`.
- `country_primary` is used for Ukrainian-country primary/local directory surfaces.
- `country_slice_of_global_directory` is used for Ukrainian-country slices inside global directories.
- `official_company_local_entity` is used for company/local-entity pages where Ukrainian source-country coverage is explicit enough.
- `regional_or_industry_context` is used for global, regional, or industry context where Ukrainian coverage is not a clean country slice.
- `needs_native_alternative_check` marks English fallback rows where a Ukrainian-native alternative should later be considered.
- `manual_review_required` marks unknown/undetermined rows that still need human review before any live activation.

Ukrainian metadata inference is not a public reachability result. Do not mark rows `broken_or_blocked` without a separate read-only public reachability probe gate.

<!-- SOURCE_SEED_UKRAINIAN_METADATA_MODEL_RULE_END -->

<!-- SOURCE_SEED_CS_RULE_STANDARD_PATCH_2026_05_19 -->

## Czech (`cs`) source-seed catalog standard record — 2026-05-19

The Czech source-seed catalog is tracked at:

- `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json`

Required Czech (`cs`) catalog facts:

- `schema=source_families_v2`
- `schema_version=2.0`
- `language_code=cs`
- `candidate_manifest=true`
- `is_live=false`
- `enabled=false`
- `needs_live_check=true`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- `safety_state=candidate_only_not_live`
- 45 source families
- 90 seed surfaces
- 90 seed URLs
- 0 duplicate seed URLs
- 0 non-HTTPS seed URLs

Czech (`cs`) remains candidate-only until a future controlled live-probe gate explicitly promotes selected surfaces. No DB/frontier/crawler activation is implied by this standards record.

## Greek (`el`) source-seed catalog standard record — 2026-05-19

The Greek source-seed catalog is tracked at:

- `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json`

Required Greek (`el`) catalog facts:

- `schema=source_families_v2`
- `schema_version=2.0`
- `language_code=el`
- `candidate_manifest=true`
- `is_live=false`
- `enabled=false`
- `needs_live_check=true`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- `safety_state=candidate_only_not_live`
- 45 source families
- 90 seed surfaces
- 90 seed URLs
- 0 duplicate seed URLs
- 0 non-HTTPS seed URLs
- quality distribution: `A=8`, `A_MINUS=15`, `A_PLUS=5`, `B=3`, `B_PLUS=14`
- decision distribution: `ACCEPT=9`, `ACCEPT_REVIEW=35`, `HOLD_REVIEW=1`

Greek (`el`) remains candidate-only until a future controlled live-probe gate explicitly promotes selected surfaces.
No DB/frontier/crawler activation is implied by this standards record.

## Hungarian (`hu`) source-seed catalog standard record

- Decision document: [`TOPIC_CRAWLER_CORE_HUNGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_19.md`](TOPIC_CRAWLER_CORE_HUNGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_19.md)
- Catalog path: `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json`
- Catalog SHA256: `2c2bc39e02679950410299288b08966222de494533990749deeb761125f3a2a1`
- Decision document SHA256: `5df6d40afaa10d61ace2d3979c3b99b1e9652db7eb262bb95ffa3fee0b2e839c`
- Final JSON truth head: `3c8700358f0b71e16ed55fde65b15e35ca20d19c`
- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Unique seed URLs: 90
- Duplicate seed URLs: 0
- Empty seed URLs: 0
- Non-HTTPS seed URLs: 0
- Required top-level safety state:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `review_state=needs_live_check`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Hungarian metadata standard:
  - `target_language_code=hu`
  - `content_language_code=hu` for native/local Hungarian surfaces; `content_language_code=en` only for English fallback surfaces.
  - `url_locale_code=hu` for Hungarian/local surfaces; `url_locale_code=en` only for English fallback surfaces.
  - `source_country_codes` includes `HU` for Hungarian/local or Hungary-targeted official-company surfaces.
  - `covered_country_codes` includes `HU`.
- Activation boundary: no DB insert, no frontier insert, no crawler activation, and no public source URL probe until an explicit future pi51c live-probe gate.

### Romanian (`ro`) source-seed catalog standard record

- Final JSON truth sealed head: `c86a2e72c235c6752df45b1d3a7993394f898c31`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_ROMANIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Decision doc SHA256: `3aafa89e5d09040151351d913910a6710314325a9508321da8b2c8231623cc1b`
- Catalog path: `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json`
- Catalog SHA256: `aec39f2cde047a65d970aff68c60317ce9b549a373a507fce6b20bdae5e33ca4`
- Taxonomy path: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_romanian_ro.json`
- Taxonomy SHA256: `3e38cbe8d12579fcb68d84d049f65c7771194293b100c0d6d37345775e4f32bb`
- Counts: 45 source families, 90 seed surfaces, 90 seed URLs.
- Required target language: `target_language_code=ro`
- Required content language model: `content_language_code=ro|en`
- Required URL locale model: `url_locale_code=ro|en`
- Required candidate flags: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`
- Required activation policy: `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- Required safety state: `safety_state=candidate_only_not_live`
- Public source URL probe status: not performed in this metadata/doc gate.

### Japanese (`ja`) source-seed catalog standard record

- Final JSON truth head: `b056ffaa185889815af09a89b98647dccbcb500a`
- Parent: `7911ca2028d73c10daec6a2e3fb06efa2b7cff6e`
- Tree: `f52fdccb546aaa4666e876a966a51c82ddfb90bb`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_JAPANESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Catalog: `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json`
- Taxonomy: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_japanese_ja.json`
- Decision doc SHA256: `e19590eabef76ab4f0b7ef253139bda8838303b0df8c116d270b44989d97d77d`
- Catalog SHA256: `ef766100e03d43c3d33d042753154ba0b18c702d718b91b21dd2a96888243cf9`
- Taxonomy SHA256: `d96868184073187c3283342a799f7c1b159c3e9b6703d6e76baa83bc2b324911`
- Counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique URLs
- Quality counts: A_PLUS=4, A=6, A_MINUS=8, B_PLUS=21, B=6
- Decision counts: ACCEPT=7, ACCEPT_REVIEW=38
- Required metadata model:
  - `target_language_code=ja`
  - `content_language_code=ja|en`
  - `url_locale_code=ja|en`
  - `covered_country_codes` must include `JP`
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `review_state=needs_live_check`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Runtime boundary: no DB insert, no frontier insert, no crawler activation, no systemd mutation, no public source URL probe before pi51c live review.

### Korean (`ko`) source-seed catalog standard record

- Final JSON truth head: `61b879102c2acb189866f7aec06c3a1e7f3bd5e2`
- Parent head before Korean catalog commit: `0cd76ff36a42e9d4d6d66fb1782f768d89d4a5b6`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_KOREAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Decision doc SHA256: `5d915489ae9e3b98edd3c7bb49ec4ad9dc9345640330ab35b3acbbb24ded8dfa`
- Catalog: `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json`
- Catalog SHA256: `fb4d9aa0a2e87b5b0fa7364bfc5408093f165abdfe6a5a49ce974341f353bca7`
- Taxonomy JSON: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_korean_ko.json`
- Taxonomy SHA256: `ec3175fcef4ec450a8c812c20ae7e5b8fa503bbfa14eea0055a5d8ec18aeaca3`
- Metrics: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique seed URLs.
- Required metadata model:
  - `target_language_code=ko`
  - `content_language_code=ko|en|unknown`
  - `url_locale_code=ko|en|und`
  - `covered_country_codes` must include `KR`
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `review_state=needs_live_check`
  - `safety_state=candidate_only_not_live`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- Public source URL probe status: not probed during catalog creation/final JSON truth gates.
- Completion rule: Korean is not fully complete until Ubuntu Desktop, GitHub, pi51c `/logisticsearch/repo`, and pi51c `/logisticsearch/makpi51crawler` tracked subtree equality all pass.

### Indonesian (`id`) source-seed catalog standard record

- Final JSON truth sealed head: `0e248abcce0a019c8ee23363787bc3e41a618c6e`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_INDONESIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Decision doc SHA256: `6e87a0d6d3cb135108042c7ca14e792e261dc2e22c1fe79ad92880c2ee39af45`
- Catalog path: `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json`
- Catalog SHA256: `adc44a4be281c5c8021295a024b083acae4852c6c235aee5ce50ccfaa610d80b`
- Taxonomy path: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_indonesian_id.json`
- Taxonomy SHA256: `658ab2385399b1109d244b62fd5599161763028d813cb44a70a76b4466ee0d88`
- Counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique seed URLs.
- Required metadata model:
  - `target_language_code=id`
  - `content_language_code=id|en|unknown`
  - `url_locale_code=id|en|und`
  - `covered_country_codes` must include `ID`
  - `source_country_codes` may be `ID` or `ZZ`
  - `language_fit` must be one of `native`, `english_fallback`, `unknown`
  - `coverage_fit` must be one of `country_primary`, `country_slice_of_global_directory`, `official_company_local_entity`, `regional_or_industry_context`
  - `public_url_probe_status=not_probed`
- Candidate-only runtime flags must remain: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `review_state=needs_live_check`, `safety_state=candidate_only_not_live`.
- Runtime activation policy remains `pi51c_live_probe_required_before_db_or_frontier_insert`.

### Vietnamese (`vi`) source-seed catalog standard record

- Final JSON truth head: `999d8ea78d7113945f30c289b8fd79ceab8ee4a3`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_VIETNAMESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Decision doc SHA256: `1657e27715188eb8760413a7e072aee0275b6d820b7356ecd96a93e02387e65a`
- Catalog path: `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json`
- Catalog SHA256: `2df88ebf0947f173f0ea8931d2b0a5fdfdf6d36e75843cad38abc38b16140280`
- Taxonomy path: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_vietnamese_vi.json`
- Taxonomy SHA256: `04de0caa3bcce317def635c3838e6091d92c278d384d036e7bc7fa5f51db2819`
- Counts: 45 source families / 90 seed surfaces / 90 seed URLs / 90 unique URLs.
- Quality distribution: `{'A': 11, 'A_MINUS': 9, 'A_PLUS': 6, 'B': 7, 'B_PLUS': 12}`
- Decision distribution: `{'ACCEPT': 15, 'ACCEPT_REVIEW': 29, 'HOLD_REVIEW': 1}`
- Candidate flags: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `review_state=needs_live_check`, `safety_state=candidate_only_not_live`.
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- Metadata rule: `target_language_code=vi`; `content_language_code=vi|en|unknown`; `url_locale_code=vi|en|und`; `covered_country_codes` must include `VN`; `public_url_probe_status=not_probed`.
- Source priority: directory sites first, then associations, official/company/port surfaces, networks, and marketplaces.
- Completion sync policy after docs commit: Ubuntu Desktop = GitHub = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` tracked subtree.

## Hindi (`hi`) source-seed final JSON truth — 2026-05-20

- Gate: `HI-08_HINDI_FINAL_JSON_TRUTH_SEAL_READONLY`
- Canonical GitHub HEAD: `7a70e6d8e668e4c5ff0b3222610f6d64ec5a405b`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_HINDI_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Decision doc SHA256: `2f2fe3093a73c8826d8f7e594cf2d6c516748c84a493671f5b614c6e32d0fe64`
- Catalog: `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json`
- Catalog SHA256: `73b7e54da70743e84e71c94bc0155b4fa8303ad1199142f55a63a27c00c652ff`
- Taxonomy: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_hindi_hi.json`
- Taxonomy SHA256: `0f4de3dc0f11a61b14df9cffad16fe89345f8c50b444cbc4262f60e73f96227f`
- Counts: 45 source families / 90 seed surfaces / 90 seed URLs / 90 unique URLs.
- Duplicate/empty/non-HTTPS seed URLs: 0 / 0 / 0.
- Candidate-only state: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`.
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- Metadata rule: `target_language_code=hi`; `content_language_code in {hi,en,unknown}`; `url_locale_code in {hi,en,und}`; `covered_country_codes` includes `IN`.
- Quality distribution: A 15 / A_MINUS 9 / A_PLUS 7 / B 4 / B_PLUS 10.
- Decision distribution: ACCEPT 12 / ACCEPT_REVIEW 33.
- Remaining source-seed rollout after Hindi: `bn,ur,he`.
- pi51c sync after Hindi: not done at this checkpoint.

### Bengali (`bn`) source-seed final JSON truth

- Head: `386003f96ae1eca4bf000d1105507dc1943cf840`.
- Decision doc: `docs/TOPIC_CRAWLER_CORE_BENGALI_SOURCE_SEED_URLS_DECISION_2026_05_20.md`.
- Catalog: `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json`.
- Taxonomy: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_bengali_bn.json`.
- Decision doc SHA: `f6b6126b0e72d99b692d9f5c44ccc6adeccf2448614ac2ae7a1439e5a213260f`.
- Catalog SHA: `0f50d0193656e612564fcb9d501998cea72470fad49a2dd53ddfc73635d1ed94`.
- Taxonomy SHA: `4167f8d5daff48d646939bbbddea1e6735b3f38bfd7c12e8d525ea9e5a15bdd5`.
- Counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique HTTPS URLs.
- Quality distribution: A=11, A_MINUS=15, A_PLUS=6, B=1, B_PLUS=12.
- Decision distribution: ACCEPT=13, ACCEPT_REVIEW=31, HOLD_REVIEW=1.
- Metadata rule: `target_language_code=bn`.
- Metadata rule: `content_language_code in {bn,en,unknown}`.
- Metadata rule: `url_locale_code in {bn,en,und}`.
- Coverage rule: `covered_country_codes` includes `BD`; West Bengal/Kolkata fallback can include `IN`.
- Candidate policy: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`.
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- Public URL probe: not run; no DB/frontier/crawler/systemd mutation.
