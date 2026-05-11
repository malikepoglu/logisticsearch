# LogisticSearch crawler_core source family daily budget and country seed policy

Date: 2026-05-11
Gate: `R102B_R6_SHORT_PROGRAMMATIC_POLICY_DOC_PATCH`
Scope: Ubuntu Desktop + GitHub only. pi51c live runtime is not touched.

## 1. Canonical decision

Source and seed expansion must use a source-family budget model. A source family is the main operational site or source group. A seed surface is a concrete crawl entry point under that family.

Existing catalog fields remain canonical:

- `source_family_code`
- `source_family_name`
- `source_host`
- `source_root_url`
- `source_quality_tier`
- `default_priority`
- `default_max_depth`
- `default_recrawl_interval`
- `family_metadata.host_budget_group`
- `seed_surfaces`

No new random top-level `source_family` field is introduced now. The existing model is strengthened.

## 2. source_family versus seed_surface

`source_family` owns politeness, rate-limit, daily cap, recrawl interval, scheduler budget, and domain-diversity policy.

`seed_surface` is a crawl entry surface under that family, such as a root directory, country directory, alphabet page, company directory, or event exhibitor directory.

Examples:

- `wcaworld_com` family with `country=NL` seed surface
- `lognetglobal_com` family with `country=TR` seed surface
- `freightnet_com` family with country/category seed surface
- `jctrans_com` family with company-directory seed surface
- `trademo_com` family with alphabet/page seed surface
- `lane_list_com` family with English lane/carrier seed surface
- `nationallogisticsdirectory_com` family with US directory seed surface

## 3. Daily budget rule

Rate-limit and politeness controls are applied first at `source_family_code` or `host_budget_group` level, not only at single URL level.

Canonical metadata keys under `family_metadata`:

```json
{
  "host_budget_group": "wcaworld_com",
  "source_family_daily_visit_cap": 1,
  "source_family_daily_visit_cap_unit": "seed_surface",
  "source_family_visit_policy": "max_one_seed_surface_per_day_until_rate_limit_policy_is_known",
  "country_rotation_enabled": true,
  "country_rotation_value_kind": "ISO_3166_ALPHA2",
  "runtime_activation_policy": "manual_review_required_before_frontier"
}
```

The catalog may store many seed surfaces. Runtime should activate only the allowed subset for the current source-family budget window.

## 4. Country-code and parameterized seed rule

Sources with `country=NL`, `country=TR`, `country=DE`, `pageIndex=1`, alphabet letters, or internal site codes must be modeled as templates or controlled seed surfaces.

Rules:

- store the pattern under `seed_surfaces`
- store template variables under `surface_metadata`
- materialize country-code seeds carefully
- never crawl all countries on the same day for unknown or rate-limited families
- default unknown country-parameterized families to one seed surface per family per day

Example metadata:

```json
{
  "surface_type": "country_parameterized_directory",
  "surface_metadata": {
    "template_variables": ["country_code"],
    "country_code_value_kind": "ISO_3166_ALPHA2",
    "daily_family_budget_required": true,
    "materialization_policy": "planner_expands_one_country_per_family_budget_window"
  }
}
```

## 5. B_MINUS source acceptance policy

B_MINUS sources are allowed because source diversity is important. B_MINUS does not mean bad. It means conservative crawler treatment.

B_MINUS rules:

- low priority
- low max depth
- long recrawl interval
- manual review note required
- no aggressive pagination
- no same-day all-country expansion
- must not dominate scheduler selection

Recommended defaults:

```text
source_quality_tier=B_MINUS
default_priority=low
default_max_depth=1
default_recrawl_interval=60 days or 90 days
family_metadata.manual_review_priority=low
family_metadata.runtime_activation_policy=manual_review_required_before_frontier
family_metadata.noise_risk=medium_or_high
```

## 6. High-value and rate-limited family policies

### WCAworld

```text
source_family_code=wcaworld_com
host_budget_group=wcaworld_com
source_family_daily_visit_cap=1
country_rotation_enabled=true
country_rotation_value_kind=ISO_3166_ALPHA2
rate_limit_observed_by_operator=true
```

### Lognet Global

```text
source_family_code=lognetglobal_com
host_budget_group=lognetglobal_com
source_family_daily_visit_cap=1
country_rotation_enabled=true
country_rotation_value_kind=ISO_3166_ALPHA2
```

### Freightnet

Freightnet produced useful evidence in R96/R99A, but it dominated samples. It needs diversity control.

```text
source_family_code=freightnet_com
host_budget_group=freightnet_com
domain_dominance_limit_required=true
scheduler_diversity_penalty_required=true
```

### JCTrans

```text
source_family_code=jctrans_com
host_budget_group=jctrans_com
strict_robots_review_required=true
country_or_slug_template_discovery_required=true
```

### Trademo

```text
source_family_code=trademo_com
host_budget_group=trademo_com
template_variables=letter,page
low_frequency_alphabet_page_rotation=true
```

### LaneList

```text
source_family_code=lane_list_com
host_budget_group=lane_list_com
source_root_url=https://www.lane-list.com/
seed_surface=https://www.lane-list.com/en/
source_category=lane_carrier_directory
source_quality_tier=B_PLUS_OR_B_AFTER_REVIEW
```

LaneList is reviewed as a lane/carrier discovery source. Origin country, destination country, and transport type filters may become later seed-surface templates.

### National Logistics Directory

```text
source_family_code=nationallogisticsdirectory_com
host_budget_group=nationallogisticsdirectory_com
source_root_url=https://nationallogisticsdirectory.com/
seed_surface=https://nationallogisticsdirectory.com/
source_category=us_logistics_directory
source_quality_tier=B_PLUS_OR_B_AFTER_REVIEW
```

National Logistics Directory is reviewed as a US logistics directory source for 3PL, freight forwarder, warehousing, and logistics partner discovery.

## 7. Multi-language policy

This policy applies to all language catalogs, not only English.

Initial rollout order:

1. English
2. Turkish
3. German
4. Arabic
5. Chinese
6. Remaining 20 languages

Each language may have different local sources, but the same source-family / seed-surface / host-budget / daily-cap model applies.

## 8. Future scheduler target

The future scheduler should support:

- strict per-domain politeness
- source-family daily cap
- host-budget-group cap
- country-code rotation
- language/source/domain diversity
- no unnecessary global sleep when another eligible domain exists
- B_MINUS sources included with low priority
- domain dominance metrics in every duration test

This document is not a runtime scheduler patch. Runtime scheduler changes require a separate audit, test, and sync gate.

## 9. Immediate next gates

```text
R103_ENGLISH_SOURCE_FAMILY_EXPANSION_PATCH_INCLUDE_LANE_LIST_AND_NLD
R104_TURKISH_POLICY_ALIGNMENT_PATCH
R105_GERMAN_BASELINE_SOURCE_SEED_START
R106_ARABIC_BASELINE_SOURCE_SEED_START
R107_CHINESE_BASELINE_SOURCE_SEED_START
```

R103 should add or update controlled English catalog entries for:

- zendeq_com
- logisticslist_com
- ruzave_com
- transportlogistic_exhibitors
- lognetglobal_com
- trademo_com
- indianlogisticsinfo_com
- freightvaluation_com
- searates_com
- fleetdirectory_com
- ttnews_com
- big_picture_logistics
- lane_list_com
- nationallogisticsdirectory_com

R103 should add seed surfaces to existing source families where needed:

- freightnet_com
- jctrans_com
- wcaworld_com
- cargoyellowpages_com if needed

## 10. Final rule

Increasing source count is valuable. Every new source must carry controlled metadata: quality tier, host budget group, daily cap, recrawl interval, max depth, robots review, live-check requirement, and scheduler diversity note.
