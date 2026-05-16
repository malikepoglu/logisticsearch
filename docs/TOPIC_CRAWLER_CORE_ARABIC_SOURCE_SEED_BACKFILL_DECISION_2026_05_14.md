# TOPIC_CRAWLER_CORE_ARABIC_SOURCE_SEED_BACKFILL_DECISION_2026_05_14

TR: Bu belge Arabic (`ar`) source-seed katalog normalizasyonu ve backfill kararıdır. Amaç Arabic katalogu latest `source_families_v2` şemasına taşımak, en az 40 source family ve en az 80 seed surface seviyesine çıkarmaktır. Bu belge karar dokümanıdır; catalog yazımı, README yazımı, pi51c sync, DB insert, crawler start veya URL fetch yapmaz.

EN: This document records the Arabic (`ar`) source-seed catalog normalization and backfill decision. The goal is to move Arabic to the latest `source_families_v2` schema and raise it to at least 40 source families and at least 80 seed surfaces. This is a decision document only; it does not write the catalog, README, pi51c, DB, crawler, or live URLs.

## Gate identity / Kapı kimliği

| Field | Value |
|---|---|
| gate | SOURCE_SEED_R235_ARABIC_LATEST_SCHEMA_BACKFILL_DECISION_DOC_PATCH_LOCAL_ONLY |
| previous research gate | SOURCE_SEED_R234_ARABIC_LATEST_SCHEMA_BACKFILL_RESEARCH_PLAN_READONLY |
| language | Arabic (`ar`) |
| target schema | `source_families_v2` |
| standard reference | `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md` |
| standard sha256 | `986b76d80694296019f1392811a2fb9e7fb4fa360d36577af69458a2069bcf90` |
| runtime activation policy | `pi51c_live_probe_required_before_db_or_frontier_insert` |
| pi51c sync allowed now | false |
| DB insert allowed now | false |
| crawler start allowed now | false |
| URL fetch/live probe allowed now | false |

## Baseline and projected metrics / Başlangıç ve hedef metrikleri

| Metric | Value |
|---|---:|
| baseline_ar_source_family_count | 18 |
| baseline_ar_seed_surface_count | 30 |
| baseline_ar_seed_url_count_from_README | 30 |
| new_source_candidate_count | 22 |
| new_planned_seed_surface_count | 50 |
| new_planned_seed_url_count | 50 |
| projected_ar_source_family_count | 40 |
| projected_ar_seed_surface_count | 80 |
| projected_ar_raw_seed_url_count | 80 |
| projected_ar_unique_seed_url_count_after_exact_dedupe | 80 |
| minimum source families after rewrite | 40 |
| minimum seed surfaces after rewrite | 80 |
| raw seed URL minimum | 80 |
| required_unique_seed_url_range | 70..95 |
| high_quality_A_MINUS_or_better_count | 17 |
| high_quality_A_MINUS_or_better minimum | 14 |
| hold_count | 0 |

## Core policy decisions / Ana politika kararları

- TR: Arabic katalog latest `source_families_v2` şemasına geçirilecek; legacy/semi-legacy yapı korunmayacak.
- EN: The Arabic catalog must be migrated to the latest `source_families_v2` schema; legacy/semi-legacy structure must not remain.
- TR: FIATA tek source family kalacak. `fiata.org` altındaki Arap ülke sayfaları ayrı top-level source family yapılmayacak.
- EN: FIATA remains one source family. Arab country pages under `fiata.org` are subordinate seed surfaces, not separate top-level source families.
- TR: Official, association, port, free-zone, air-cargo ve logistics-hub kaynakları commercial fallback kaynaklardan önce gelir.
- EN: Official, association, port, free-zone, air-cargo, and logistics-hub sources outrank commercial fallback sources.
- TR: Commercial fallback kaynaklar `B` / `B_PLUS` tier ile sınırlıdır ve strict review/dedupe gerektirir.
- EN: Commercial fallback sources are limited to `B` / `B_PLUS` tier and require strict review/dedupe.
- TR: `fold_or_exact_dedupe_under_existing_source_not_duplicate_seed_url` zorunludur.
- EN: `fold_or_exact_dedupe_under_existing_source_not_duplicate_seed_url` is mandatory.
- TR: Crawler_Core stores discovered page links only as raw link evidence.
- EN: Crawler_Core stores discovered page links only as raw link evidence.
- TR: Raw discovered links are not `added_seeds`.
- EN: Raw discovered links are not `added_seeds`.
- TR: No DB insert, no live frontier activation, no crawler start.
- EN: No DB insert, no live frontier activation, no crawler start.

## Planned Arabic source-family additions / Planlanan Arabic source-family ekleri

### 01. `ar_fiata_arab_country_directories`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `international_freight_forwarding_association_country_directory`
- planned_seed_surfaces: `8`
- canonical_url: `https://fiata.org/directory/`
- rationale: FIATA must remain one source family. Arab country pages are subordinate seed surfaces, not separate top-level sources.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://fiata.org/directory/sa/`
  - `https://fiata.org/directory/ae/`
  - `https://fiata.org/directory/eg/`
  - `https://fiata.org/directory/jo/`
  - `https://fiata.org/directory/lb/`
  - `https://fiata.org/directory/qa/`
  - `https://fiata.org/directory/om/`
  - `https://fiata.org/directory/ma/`
### 02. `ar_nafl_uae_member_list`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_freight_logistics_association_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://nafl.ae/member-list/`
- rationale: UAE freight/logistics association member-list source.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://nafl.ae/member-list/`
  - `https://nafl.ae/`
### 03. `ar_eiffa_egypt_members_directory`

- quality_tier: `A_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_freight_forwarding_association_member_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://eiffa.com/members-directory/`
- rationale: Egyptian freight forwarding association member directory.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://eiffa.com/members-directory/`
  - `https://eiffa.com/`
### 04. `ar_lfs_lebanon_forwarders_syndicate`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_forwarders_syndicate_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.lfs-lb.org/`
- rationale: Lebanese Forwarders Syndicate reference and directory surfaces.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.lfs-lb.org/`
  - `https://www.lfs-lb.org/directory-f/`
### 05. `ar_qafl_qatar_chamber_logistics`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_freight_forwarding_logistics_association_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.qatarchamber.com/qafl/`
- rationale: Qatar Association for Freight Forwarding and Logistics reference under Qatar Chamber.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.qatarchamber.com/qafl/`
  - `https://www.qatarchamber.com/`
### 06. `ar_mawani_saudi_ports_logistics_reference`

- quality_tier: `A`
- decision_status: `ACCEPT_REVIEW`
- source_type: `official_port_authority_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://mawani.gov.sa/`
- rationale: Saudi Ports Authority reference for port/logistics ecosystem discovery.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://mawani.gov.sa/`
  - `https://mawani.gov.sa/en-us/`
### 07. `ar_saudi_logistics_hub_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `official_logistics_hub_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.logisti.sa/`
- rationale: Saudi logistics hub reference for controlled country logistics discovery.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.logisti.sa/`
  - `https://www.logisti.sa/en/`
### 08. `ar_jafza_logistics_business_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `free_zone_logistics_business_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.jafza.ae/`
- rationale: JAFZA free-zone logistics reference requiring parse/review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.jafza.ae/`
  - `https://www.jafza.ae/industries/logistics/`
### 09. `ar_dubai_south_logistics_district_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `logistics_district_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.dubaisouth.ae/`
- rationale: Dubai South logistics district reference surface.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.dubaisouth.ae/`
  - `https://www.dubaisouth.ae/logistics-district`
### 10. `ar_ad_ports_kizad_logistics_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `port_free_zone_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.adportsgroup.com/`
- rationale: AD Ports trade/logistics reference surface.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.adportsgroup.com/`
  - `https://www.adportsgroup.com/en/trade-and-logistics`
### 11. `ar_asyad_oman_logistics_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `national_logistics_group_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://asyad.om/`
- rationale: Oman ASYAD logistics reference; candidate discovery only.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://asyad.om/`
  - `https://asyad.om/services`
### 12. `ar_salalah_port_logistics_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `port_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://salalahport.com/`
- rationale: Oman Salalah port/logistics reference requiring live probe.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://salalahport.com/`
  - `https://salalahport.com/services/`
### 13. `ar_aqaba_logistics_port_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `port_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.adc.jo/`
- rationale: Aqaba/Jordan logistics-port ecosystem reference.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.adc.jo/`
  - `https://www.adc.jo/en-us`
### 14. `ar_suez_canal_economic_zone_logistics`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `economic_zone_logistics_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://sczone.eg/`
- rationale: Egypt SCZone logistics/economic-zone reference.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://sczone.eg/`
  - `https://sczone.eg/investment-opportunities/`
### 15. `ar_alexandria_port_authority_reference`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `port_authority_reference`
- planned_seed_surfaces: `2`
- canonical_url: `https://apa.gov.eg/`
- rationale: Alexandria port reference for maritime/logistics clues.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://apa.gov.eg/`
  - `https://apa.gov.eg/en/`
### 16. `ar_freightnet_gulf_levant_forwarders`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_freight_forwarder_country_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.freightnet.com/`
- rationale: Commercial fallback for Gulf/Levant forwarder discovery; lower priority than official sources.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.freightnet.com/directory/p1/cSA/s30.htm`
  - `https://www.freightnet.com/directory/p12/cAE/s30.htm`
### 17. `ar_freightnet_egypt_qatar_oman`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_freight_logistics_country_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.freightnet.com/`
- rationale: Commercial fallback for Egypt/Qatar/Oman logistics pages; strict review required.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.freightnet.com/directory/p1/cEG/s99.htm`
  - `https://www.freightnet.com/directory/p1/cQA/s30.htm`
### 18. `ar_freightnet_oman_jordan_lebanon`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_freight_forwarder_country_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://www.freightnet.com/`
- rationale: Commercial fallback for Oman/Jordan/Lebanon forwarders.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.freightnet.com/directory/p4/cOM/s30.htm`
  - `https://www.freightnet.com/directory/p5/cJO/s30.htm`
### 19. `ar_azfreight_arab_forwarders`

- quality_tier: `B`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_airfreight_forwarder_country_directory`
- planned_seed_surfaces: `2`
- canonical_url: `https://azfreight.com/`
- rationale: Airfreight/commercial fallback after official and association sources.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://azfreight.com/country-facility/freight-forwarders-in-saudi-arabia/`
  - `https://azfreight.com/association/lfs-lebanese-forwarders-syndicate/`
### 20. `ar_opca_arab_project_cargo_forwarders`

- quality_tier: `B_PLUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `commercial_project_cargo_forwarder_country_directory`
- planned_seed_surfaces: `4`
- canonical_url: `https://overseasprojectcargo.com/`
- rationale: Project-cargo commercial fallback with strict category and duplicate controls.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://overseasprojectcargo.com/InternationalFreightForwarders/saudi-arabia-freight-forwarders/`
  - `https://overseasprojectcargo.com/InternationalFreightForwarders/jordan-freight-forwarders/`
  - `https://overseasprojectcargo.com/InternationalFreightForwarders/oman-freight-forwarders/`
  - `https://overseasprojectcargo.com/InternationalFreightForwarders/lebanon-freight-forwarders/`
### 21. `ar_iata_cargolink_mena_air_cargo_directory`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `air_cargo_supplier_directory`
- planned_seed_surfaces: `1`
- canonical_url: `https://www.iata.org/en/publications/directories/cargolink/directory/`
- rationale: IATA CargoLink reference for air-cargo supplier discovery after terms/manual review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.iata.org/en/publications/directories/cargolink/directory/`
### 22. `ar_iela_middle_east_africa_exhibition_logistics`

- quality_tier: `A_MINUS`
- decision_status: `ACCEPT_REVIEW`
- source_type: `exhibition_logistics_member_directory`
- planned_seed_surfaces: `1`
- canonical_url: `https://www.iela.org/members/find-an-iela-member.html`
- rationale: IELA specialist exhibition-logistics directory for Middle East/Africa review.
- handling_policy: `direct_company_import=false`, `manual_review_required=true`, `parse_core_required=true`, `requires_live_probe_before_frontier=true`
- seed_urls:
  - `https://www.iela.org/members/find-an-iela-member.html`


## Safety contract / Güvenlik sözleşmesi

| Policy field | Required value |
|---|---:|
| `candidate_manifest` | true after catalog rewrite |
| `is_live` | false after catalog rewrite |
| `live_frontier_activation` | false |
| `db_insert_allowed` | false |
| `url_fetch_allowed_in_catalog_gate` | false |
| `crawler_start_allowed_in_catalog_gate` | false |
| `pi51c_sync_allowed_in_catalog_gate` | false |
| `direct_company_import` | false |
| `manual_review_required` | true |
| `parse_core_required` | true |
| `needs_live_check` | true |

## Next gate / Sonraki kapı

`SOURCE_SEED_R236_ARABIC_LATEST_SCHEMA_BACKFILL_DECISION_DOC_AUDIT_READONLY`

TR: Sonraki kapı sadece read-only audit olmalıdır. Catalog, README, Git, pi51c, DB, crawler, systemd ve URL fetch/live probe yapılmamalıdır.

EN: The next gate must be read-only audit only. It must not touch catalog, README, Git, pi51c, DB, crawler, systemd, or URL fetch/live probe.
