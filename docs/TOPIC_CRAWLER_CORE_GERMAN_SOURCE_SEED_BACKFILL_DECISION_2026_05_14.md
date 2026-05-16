# TOPIC_CRAWLER_CORE_GERMAN_SOURCE_SEED_BACKFILL_DECISION_2026_05_14

## 1. Gate and scope

- Gate: `SOURCE_SEED_R222_GERMAN_LATEST_SCHEMA_BACKFILL_DECISION_DOC_PATCH_LOCAL_ONLY`
- Scope: local-only German backfill decision document.
- Language: German (`de`).
- Target schema: `source_families_v2`.
- Standard reference: `TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`.
- Baseline catalog: `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json`.
- This is a decision document only. It does not rewrite the German catalog.
- No DB insert, no live frontier activation, no crawler start.
- No pi51c sync is allowed in this gate.

## 2. User correction applied

The German catalog must not be weaker than the French/Turkish compact directory-first level.

Required minimums for this German backfill line:

| Metric | Required |
|---|---:|
| minimum source families after rewrite | 40 |
| minimum seed surfaces after rewrite | 80 |
| raw seed URL minimum | 80 |
| unique seed URL operating range | 70..95 |
| high_quality_A_MINUS_or_better minimum | 16 |

R221 projected only 76 seed surfaces, so R221B added `de_sgkv_combined_transport_members` and repaired the plan to 41 source families and 80 seed surfaces.

## 3. Projected German metrics

| Metric | Value |
|---|---:|
| baseline_de_source_family_count | 19 |
| baseline_de_seed_surface_count | 19 |
| baseline_de_seed_url_count | 23 |
| new_source_candidate_count | 22 |
| new_planned_seed_surface_count | 61 |
| new_planned_seed_url_count | 61 |
| projected_de_source_family_count | 41 |
| projected_de_seed_surface_count | 80 |
| projected_de_raw_seed_url_count | 84 |
| projected_de_unique_seed_url_count_after_exact_dedupe | 81 |
| required_unique_seed_url_range | 70..95 |
| high_quality_A_MINUS_or_better_count | 18 |
| hold_count | 0 |

## 4. Safety and activation policy

- `candidate_manifest`: true after catalog rewrite.
- `is_live`: false after catalog rewrite.
- `runtime_activation_policy`: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- `live_frontier_activation`: false.
- `db_insert_allowed`: false.
- `url_fetch_allowed_in_catalog_gate`: false.
- `crawler_start_allowed_in_catalog_gate`: false.
- `pi51c_sync_allowed_in_catalog_gate`: false.
- `direct_company_import`: false.
- PDF/download/list/exhibitor/member surfaces are candidate seed surfaces only.
- Crawler_Core stores discovered page links only as raw link evidence.
- Raw discovered links are not `added_seeds`.
- Parse_Core may later promote reviewed links into `added_seeds`.

## 5. Dedupe rule

Existing German overlaps are expected and must be folded or exact-deduped, not inserted as duplicate seed URLs.

Observed existing URL overlaps:

- `https://www.bgl-ev.de/`
- `https://www.freightnet.com/directory/p1/cDE/s30.htm`
- `https://www.wlw.de/de/suche/speditionen/deutschland`

Policy value:

`fold_or_exact_dedupe_under_existing_source_not_duplicate_seed_url`

## 6. Decision matrix

| # | source_code | quality_tier | decision_status | planned_seed_surfaces | canonical_url |
|---:|---|---|---|---:|---|
| 001 | `de_balm_transport_authority_reference` | A_PLUS | ACCEPT_REVIEW | 2 | https://www.balm.bund.de/DE/Themen/Marktzugang/marktzugang_node.html |
| 002 | `de_dslv_member_directory` | A_PLUS | ACCEPT_REVIEW | 2 | https://www.dslv.org/de/mitglieder |
| 003 | `de_bvl_network_member_directory` | A | ACCEPT_REVIEW | 2 | https://www.bvl.de/service/mitglieder |
| 004 | `de_biek_parcel_logistics_members` | A | ACCEPT_REVIEW | 2 | https://biek.de/mitglieder.html |
| 005 | `de_amoe_moving_forwarders_directory` | A | ACCEPT_REVIEW | 1 | https://www.amoe.de/umzugsspediteur-suchen/ |
| 006 | `de_bgl_road_haulage_association_reference` | A | ACCEPT_REVIEW | 2 | https://www.bgl-ev.de/ |
| 007 | `de_bwvl_transport_logistics_members` | A_MINUS | ACCEPT_REVIEW | 2 | https://www.bwvl.de/ |
| 008 | `de_hafen_hamburg_company_database` | A_PLUS | ACCEPT_REVIEW | 3 | https://www.hafen-hamburg.de/en/companies/ |
| 009 | `de_logistics_initiative_hamburg_members` | A | ACCEPT_REVIEW | 2 | https://www.hamburg-logistik.net/mitglieder/ |
| 010 | `de_aircargo_community_frankfurt_members` | A | ACCEPT_REVIEW | 2 | https://www.fra-fr8.com/members |
| 011 | `de_munich_airport_cargo_partners` | A_MINUS | ACCEPT_REVIEW | 2 | https://www.munich-airport.de/cargo |
| 012 | `de_dus_aircargo_logistics_partners` | A_MINUS | ACCEPT_REVIEW | 2 | https://www.dus.com/en/businesspartner/air-cargo |
| 013 | `de_duisport_logistics_partner_directory` | A_MINUS | ACCEPT_REVIEW | 2 | https://www.duisport.de/logistik/ |
| 014 | `de_bremenports_maritime_logistics_reference` | A_MINUS | ACCEPT_REVIEW | 2 | https://bremenports.de/ |
| 015 | `de_transport_logistic_exhibitor_directory` | A | ACCEPT_REVIEW | 5 | https://transportlogistic.de/en/trade-fair/exhibitors-products/exhibitor-directory/ |
| 016 | `de_logimat_exhibitor_directory` | A_MINUS | ACCEPT_REVIEW | 5 | https://www.logimat-messe.de/en/exhibitor-directory |
| 017 | `de_iaa_transportation_exhibitor_directory` | A_MINUS | ACCEPT_REVIEW | 4 | https://www.iaa-transportation.com/en/exhibitors-products/exhibitor-directory |
| 018 | `de_kompass_germany_transport_logistics` | B_PLUS | ACCEPT_REVIEW | 4 | https://de.kompass.com/a/transport-logistik/75/ |
| 019 | `de_wlw_germany_logistics_directory` | B_PLUS | ACCEPT_REVIEW | 4 | https://www.wlw.de/de/suche/logistikdienstleister/deutschland |
| 020 | `de_freightnet_germany_forwarders` | B_PLUS | ACCEPT_REVIEW | 4 | https://www.freightnet.com/directory/p1/cDE/s30.htm |
| 021 | `de_azfreight_germany_airfreight_directory` | B | ACCEPT_REVIEW | 3 | https://azfreight.com/country/germany/ |
| 022 | `de_sgkv_combined_transport_members` | A_MINUS | ACCEPT_REVIEW | 4 | https://sgkv.de/mitglieder/ |

## 7. Source details

### 001. `de_balm_transport_authority_reference`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `official_transport_authority_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.balm.bund.de/DE/Themen/Marktzugang/marktzugang_node.html`
- rationale: Official German federal logistics/transport authority reference surface; candidate verification, not direct company import.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.balm.bund.de/DE/Themen/Marktzugang/marktzugang_node.html
- SEED: https://www.balm.bund.de/DE/Themen/Unternehmen/unternehmen_node.html

### 002. `de_dslv_member_directory`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_forwarding_logistics_association_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.dslv.org/de/mitglieder`
- rationale: German forwarding/logistics association surface; high-value member and association reference.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.dslv.org/de/mitglieder
- SEED: https://www.dslv.org/de/mitgliedschaft

### 003. `de_bvl_network_member_directory`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_logistics_network_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.bvl.de/service/mitglieder`
- rationale: German logistics network member/reference surface; useful for controlled entity discovery.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.bvl.de/service/mitglieder
- SEED: https://www.bvl.de/

### 004. `de_biek_parcel_logistics_members`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `parcel_express_logistics_association_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://biek.de/mitglieder.html`
- rationale: Parcel/express logistics association member surface; high-signal German CEP sector coverage.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://biek.de/mitglieder.html
- SEED: https://biek.de/

### 005. `de_amoe_moving_forwarders_directory`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `moving_logistics_member_directory`
- planned_seed_surfaces: `1`
- canonical_url: `https://www.amoe.de/umzugsspediteur-suchen/`
- rationale: German moving/logistics association search surface; useful specialist logistics category.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.amoe.de/umzugsspediteur-suchen/

### 006. `de_bgl_road_haulage_association_reference`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `road_haulage_association_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.bgl-ev.de/`
- rationale: German road haulage/logistics association reference; duplicate root URL must fold under existing German source if already present.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.bgl-ev.de/
- SEED: https://www.bgl-ev.de/web/der-bgl/mitglieder.htm

### 007. `de_bwvl_transport_logistics_members`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `transport_logistics_association_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.bwvl.de/`
- rationale: German transport/logistics association surface; review required for current directory structure.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.bwvl.de/
- SEED: https://www.bwvl.de/mitglieder/

### 008. `de_hafen_hamburg_company_database`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `port_logistics_company_directory`
- planned_seed_surfaces: `3`
- canonical_url: `https://www.hafen-hamburg.de/en/companies/`
- rationale: Hamburg port company database; high-value maritime/logistics source with controlled filtering.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.hafen-hamburg.de/en/companies/
- SEED: https://www.hafen-hamburg.de/de/unternehmen/
- SEED: https://www.hafen-hamburg.de/de/

### 009. `de_logistics_initiative_hamburg_members`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `regional_logistics_cluster_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.hamburg-logistik.net/mitglieder/`
- rationale: Hamburg logistics cluster member surface; regional logistics ecosystem enrichment.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.hamburg-logistik.net/mitglieder/
- SEED: https://www.hamburg-logistik.net/

### 010. `de_aircargo_community_frankfurt_members`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `air_cargo_cluster_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.fra-fr8.com/members`
- rationale: Frankfurt air-cargo community member surface; strong German air-cargo cluster signal.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.fra-fr8.com/members
- SEED: https://www.fra-fr8.com/

### 011. `de_munich_airport_cargo_partners`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `airport_air_cargo_partner_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.munich-airport.de/cargo`
- rationale: Munich airport cargo reference surface; use only after airport/partner live review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.munich-airport.de/cargo
- SEED: https://www.munich-airport.de/air-cargo-772051

### 012. `de_dus_aircargo_logistics_partners`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `airport_air_cargo_partner_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.dus.com/en/businesspartner/air-cargo`
- rationale: Düsseldorf airport air-cargo surface; requires live structure review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.dus.com/en/businesspartner/air-cargo
- SEED: https://www.dus.com/de-de/businesspartner/air-cargo

### 013. `de_duisport_logistics_partner_directory`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `inland_port_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.duisport.de/logistik/`
- rationale: Duisburg inland port logistics reference; useful rail/inland-waterway/logistics cluster surface.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.duisport.de/logistik/
- SEED: https://www.duisport.de/

### 014. `de_bremenports_maritime_logistics_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `maritime_port_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://bremenports.de/`
- rationale: Bremen/Bremerhaven port reference surface; review required before entity extraction.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://bremenports.de/
- SEED: https://bremenports.de/unternehmen/

### 015. `de_transport_logistic_exhibitor_directory`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `logistics_trade_fair_exhibitor_directory`
- planned_seed_surfaces: `5`
- canonical_url: `https://transportlogistic.de/en/trade-fair/exhibitors-products/exhibitor-directory/`
- rationale: Major Germany-based logistics fair exhibitor directory; event freshness and category filtering required.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://transportlogistic.de/en/trade-fair/exhibitors-products/exhibitor-directory/
- SEED: https://exhibitors.transportlogistic.de/en/
- SEED: https://transportlogistic.de/de/messe/aussteller-produkte/ausstellerverzeichnis/
- SEED: https://transportlogistic.de/en/
- SEED: https://transportlogistic.de/de/

### 016. `de_logimat_exhibitor_directory`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `intralogistics_trade_fair_exhibitor_directory`
- planned_seed_surfaces: `5`
- canonical_url: `https://www.logimat-messe.de/en/exhibitor-directory`
- rationale: Intralogistics fair exhibitor directory; useful but needs event/year/category review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.logimat-messe.de/en/exhibitor-directory
- SEED: https://www.logimat-messe.de/de/ausstellerverzeichnis
- SEED: https://www.logimat-messe.de/en
- SEED: https://www.logimat-messe.de/de
- SEED: https://www.logimat-messe.de/

### 017. `de_iaa_transportation_exhibitor_directory`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `transport_trade_fair_exhibitor_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://www.iaa-transportation.com/en/exhibitors-products/exhibitor-directory`
- rationale: Transport/truck/logistics fair exhibitor directory; category filtering required.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.iaa-transportation.com/en/exhibitors-products/exhibitor-directory
- SEED: https://www.iaa-transportation.com/de/aussteller-produkte/ausstellerverzeichnis
- SEED: https://www.iaa-transportation.com/en/
- SEED: https://www.iaa-transportation.com/de/

### 018. `de_kompass_germany_transport_logistics`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_b2b_transport_logistics_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://de.kompass.com/a/transport-logistik/75/`
- rationale: Commercial B2B fallback; lower priority than official/association/port sources.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://de.kompass.com/a/transport-logistik/75/
- SEED: https://de.kompass.com/a/logistikdienstleistungen/80690/
- SEED: https://de.kompass.com/s/transporte-logistik/10/
- SEED: https://de.kompass.com/

### 019. `de_wlw_germany_logistics_directory`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_supplier_logistics_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://www.wlw.de/de/suche/logistikdienstleister/deutschland`
- rationale: Commercial supplier directory fallback; strict dedupe/noise control required.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.wlw.de/de/suche/logistikdienstleister/deutschland
- SEED: https://www.wlw.de/de/suche/speditionen/deutschland
- SEED: https://www.wlw.de/de/suche/transportlogistik/deutschland
- SEED: https://www.wlw.de/

### 020. `de_freightnet_germany_forwarders`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_freight_forwarder_country_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://www.freightnet.com/directory/p1/cDE/s30.htm`
- rationale: Commercial freight forwarder fallback; pagination and duplicate controls required.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://www.freightnet.com/directory/p1/cDE/s30.htm
- SEED: https://www.freightnet.com/directory/p1/cDE/s31.htm
- SEED: https://www.freightnet.com/directory/p2/cDE/s30.htm
- SEED: https://www.freightnet.com/directory/p3/cDE/s30.htm

### 021. `de_azfreight_germany_airfreight_directory`

- quality_tier: `B`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_airfreight_country_directory`
- planned_seed_surfaces: `3`
- canonical_url: `https://azfreight.com/country/germany/`
- rationale: Airfreight/freight commercial fallback; useful after airport and association sources.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://azfreight.com/country/germany/
- SEED: https://azfreight.com/country-facility/freight-forwarders-in-germany/
- SEED: https://azfreight.com/directory/

### 022. `de_sgkv_combined_transport_members`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `combined_transport_association_member_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://sgkv.de/mitglieder/`
- rationale: German combined-transport association/member surfaces lift German catalog to minimum 80 seed surfaces while keeping association/cluster-first quality.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`

- SEED: https://sgkv.de/mitglieder/
- SEED: https://sgkv.de/mitglieder/mitgliederliste/
- SEED: https://sgkv.de/verein/
- SEED: https://sgkv.de/der-kombinierte-verkehr/zugang-zu-kv/


## 8. Next gates

1. `SOURCE_SEED_R223_GERMAN_LATEST_SCHEMA_BACKFILL_DECISION_DOC_AUDIT_READONLY`
2. `SOURCE_SEED_R224_GERMAN_LATEST_SCHEMA_BACKFILL_DECISION_DOC_COMMIT_PUSH_GATE`
3. `SOURCE_SEED_R225_GERMAN_CATALOG_SCHEMA_BACKFILL_LOCAL_ONLY`

## 9. Non-touch assertion

This decision doc must not mutate catalogs, README, Git history, pi51c, DB, crawler, systemd, sync, URL fetch, or live probe.
