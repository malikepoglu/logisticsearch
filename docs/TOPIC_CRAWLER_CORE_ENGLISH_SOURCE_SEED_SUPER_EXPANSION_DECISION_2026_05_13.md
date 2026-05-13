# TOPIC_CRAWLER_CORE_ENGLISH_SOURCE_SEED_SUPER_EXPANSION_DECISION_2026_05_13

## Gate

- Created by gate: `SOURCE_SEED_R190B_ENGLISH_SUPER_EXPANSION_DECISION_DOC_PATCH_LOCAL_ONLY`
- Previous failed gate: `SOURCE_SEED_R190_ENGLISH_SUPER_EXPANSION_DECISION_DOC_PATCH_LOCAL_ONLY`
- Previous repaired planning gate: `SOURCE_SEED_R189B_ENGLISH_SUPER_EXPANSION_RESEARCH_PLAN_READONLY`
- Language code: `en`
- Language name: `English`
- Catalog path: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- Decision doc path: `docs/TOPIC_CRAWLER_CORE_ENGLISH_SOURCE_SEED_SUPER_EXPANSION_DECISION_2026_05_13.md`
- Repository head at planning: `b143becafe79780bfa7d0e3a4d05115721bab24d`

## Intent

English must be globally dominant versus the current Chinese catalog. The English catalog is a global working language for logistics, freight forwarding, customs brokerage, air cargo, port logistics, warehousing, cold chain, 3PL, project cargo, and trade-fair discovery surfaces.

This decision plan expands English with directory-first, association-first, official-registry-first, and high-quality commercial fallback sources. This is still a candidate source-seed plan, not live crawler activation.

## R190 failure repair note

- Removed duplicate source-code audit trail needle: `en_ciffa_member_directory_quebec_surface`
- Kept canonical CIFFA parent source: `en_ciffa_members_directory`
- Reason: the duplicate Quebec CIFFA candidate used the same canonical URL, `https://www.ciffa.com/member-directory/`, so Quebec relevance is folded under the main CIFFA parent and must not become a separate source family.
- `en_ciffa_member_directory_quebec_surface` is intentionally present only in this audit-trail section, not in the decision matrix.

## Current baseline

| Metric | Value |
|---|---:|
| current_en_source_family_count | 41 |
| current_en_seed_surface_count | 60 |
| current_en_seed_url_count_legacy_observed | 0 |
| current_zh_source_family_count | 105 |
| current_zh_seed_surface_count | 106 |
| current_fr_source_family_count | 37 |
| current_fr_seed_surface_count | 72 |

Note: the legacy English catalog reports `seed_url_count=0` because the old schema did not expose normalized `seed_urls` the same way as the newer French-style catalog. For projection, the existing 60 English seed surfaces are treated as normalizable seed URLs during the later catalog rewrite.

## Target

| Target | Required | Projected after this plan | Verdict |
|---|---:|---:|---|
| English source families | >= 150 | 171 | PASS |
| English seed surfaces | >= 320 | 450 | PASS |
| English seed URLs | >= 320 | 450 | PASS |
| English must dominate Chinese source count | > 105 | 171 | PASS |
| English must dominate Chinese seed surface count | > 106 | 450 | PASS |

## Planned add metrics

| Metric | Value |
|---|---:|
| new_source_family_candidate_count | 130 |
| new_planned_seed_surface_count | 390 |
| new_planned_seed_url_count | 390 |
| new_unique_host_count | 124 |
| high_quality_A_MINUS_or_better_count | 96 |
| hold_count | 5 |

## Quality tier counts

| Quality tier | Count |
|---|---:|
| `A_PLUS` | 26 |
| `A` | 24 |
| `A_MINUS` | 46 |
| `B_PLUS` | 23 |
| `B` | 10 |
| `B_MINUS` | 1 |

## Decision status counts

| Decision status | Count |
|---|---:|
| `ACCEPT` | 10 |
| `ACCEPT_REVIEW` | 115 |
| `HOLD` | 5 |

## Model decisions

- English super-expansion target: `150+ source families`, `320+ seed surfaces`, `320+ seed URLs`.
- FIATA country pages remain subordinate seed surfaces under a single shared FIATA source family; they must not become separate top-level source families.
- WCA country/network pages remain subordinate seed surfaces under one WCA source family.
- IATA CargoLink remains a shared-host air cargo directory with search/category seed surfaces.
- CIFFA Quebec relevance is folded under `en_ciffa_members_directory`; it is not a separate source family because it uses the same canonical URL.
- Commercial fallback directories are allowed only after official, association, government, port, airport, and high-quality industry sources.
- PDF/download/ZIP sources require later controlled handling gates and must not be direct company imports.
- All new source families must remain `is_enabled=false` and `needs_live_check=true`.
- Runtime activation policy remains `pi51c_live_probe_required_before_db_or_frontier_insert`.
- No DB insert, no live frontier activation, no crawler start, no systemd mutation, no URL fetch/live probe, and no pi51c sync are allowed in this catalog planning line.

## Planned source-family decision matrix

| # | source_code | quality_tier | decision_status | source_type | planned_seed_surfaces | clickable canonical URL | rationale |
|---:|---|---|---|---|---:|---|---|
| 1 | `en_fiata_members_directory` | `A_PLUS` | `ACCEPT` | `official_global_association_members_directory` | 62 | [https://fiata.org/directory/](https://fiata.org/directory/) | Global FIATA members directory; country pages remain subordinate seed surfaces under one shared source family. |
| 2 | `en_iata_cargolink_directory` | `A_PLUS` | `ACCEPT` | `official_air_cargo_directory` | 16 | [https://www.iata.org/en/publications/directories/cargolink/directory/](https://www.iata.org/en/publications/directories/cargolink/directory/) | IATA CargoLink air-cargo supply-chain directory. |
| 3 | `en_wca_directory` | `A_PLUS` | `ACCEPT_REVIEW` | `global_freight_forwarder_network_directory` | 34 | [https://www.wcaworld.com/directory](https://www.wcaworld.com/directory) | Large global independent freight forwarder network directory. |
| 4 | `en_ncbfaa_membership_directory` | `A_PLUS` | `ACCEPT` | `national_association_member_directory` | 2 | [https://members.ncbfaa.org/directory/Member/index.html](https://members.ncbfaa.org/directory/Member/index.html) | US customs broker and freight forwarder membership directory. |
| 5 | `en_ncbfaa_search_membership` | `A_PLUS` | `ACCEPT` | `national_association_member_search` | 1 | [https://ncbfaa.org/search-our-membership](https://ncbfaa.org/search-our-membership) | US customs broker/freight forwarder search surface. |
| 6 | `en_cbp_permitted_customs_brokers` | `A_PLUS` | `ACCEPT` | `official_customs_broker_listing` | 3 | [https://www.cbp.gov/about/contact/brokers-listing](https://www.cbp.gov/about/contact/brokers-listing) | Official US CBP permitted customs brokers listing. |
| 7 | `en_fmc_oti_nvoccs` | `A_PLUS` | `ACCEPT` | `official_ocean_transport_intermediary_listing` | 4 | [https://www2.fmc.gov/oti/NVOCC.aspx](https://www2.fmc.gov/oti/NVOCC.aspx) | Official US FMC OTI/NVOCC search/download surface. |
| 8 | `en_govuk_customs_agents_register` | `A_PLUS` | `ACCEPT_REVIEW` | `official_customs_agent_register` | 2 | [https://www.gov.uk/guidance/list-of-customs-agents-and-fast-parcel-operators](https://www.gov.uk/guidance/list-of-customs-agents-and-fast-parcel-operators) | UK customs agents and fast parcel operators register. |
| 9 | `en_bifa_members_directory` | `A_PLUS` | `ACCEPT` | `national_association_member_directory` | 2 | [https://bifa.org/members/](https://bifa.org/members/) | UK freight forwarder association directory. |
| 10 | `en_ciffa_members_directory` | `A_PLUS` | `ACCEPT` | `national_association_member_directory` | 2 | [https://www.ciffa.com/member-directory/](https://www.ciffa.com/member-directory/) | Canadian freight forwarder association member directory; Quebec relevance stays under this parent, not a duplicate source family. |
| 11 | `en_cscb_customs_broker_search` | `A_PLUS` | `ACCEPT_REVIEW` | `customs_broker_member_search` | 1 | [https://cscb.ca/en/customs-broker-search](https://cscb.ca/en/customs-broker-search) | Canadian customs broker search directory. |
| 12 | `en_ifcbaa_member_directory` | `A_PLUS` | `ACCEPT` | `national_association_member_directory` | 2 | [https://www.ifcbaa.com/IFCBAA/IFCBAA/About/Member_Directory.aspx](https://www.ifcbaa.com/IFCBAA/IFCBAA/About/Member_Directory.aspx) | Australia customs broker/freight forwarder member directory. |
| 13 | `en_cbaff_business_directory` | `A_PLUS` | `ACCEPT` | `national_association_business_directory` | 2 | [https://www.cbaff.org.nz/business-directory](https://www.cbaff.org.nz/business-directory) | New Zealand customs broker/freight forwarder business directory. |
| 14 | `en_ifcba_members` | `A_PLUS` | `ACCEPT_REVIEW` | `customs_broker_association_of_associations` | 1 | [https://www.ifcba.org/members](https://www.ifcba.org/members) | Global customs brokers association member association directory. |
| 15 | `en_iifa_ireland_members` | `A` | `ACCEPT_REVIEW` | `national_association_member_directory` | 1 | [https://iifa.ie/members](https://iifa.ie/members) | Ireland freight forwarder association member list. |
| 16 | `en_tia_member_directory` | `A` | `ACCEPT_REVIEW` | `third_party_logistics_member_directory` | 2 | [https://tianet.org/TIA/TIAnetOrg/TIA-Member-Directory.aspx](https://tianet.org/TIA/TIAnetOrg/TIA-Member-Directory.aspx) | US/North America 3PL member directory. |
| 17 | `en_airforwarders_member_marketplace` | `A_MINUS` | `ACCEPT_REVIEW` | `air_forwarder_association_marketplace` | 2 | [https://airforwarders.org/member-marketplace/](https://airforwarders.org/member-marketplace/) | Airforwarders Association marketplace / member surface. |
| 18 | `en_sla_member_directory` | `A_PLUS` | `ACCEPT_REVIEW` | `national_logistics_association_member_directory` | 2 | [https://www.sla.org.sg/memberDirectory](https://www.sla.org.sg/memberDirectory) | Singapore Logistics Association member directory. |
| 19 | `en_saaa_members` | `A_PLUS` | `ACCEPT_REVIEW` | `aircargo_agents_member_directory` | 2 | [https://www.saaa.org.sg/listing-of-saaa-members/](https://www.saaa.org.sg/listing-of-saaa-members/) | Singapore Aircargo Agents Association member list. |
| 20 | `en_fffai_membership_search` | `A_PLUS` | `ACCEPT_REVIEW` | `national_forwarder_association_member_search` | 2 | [https://fffai.org/user/membership/membership-search](https://fffai.org/user/membership/membership-search) | India freight forwarder/customs broker association membership search. |
| 21 | `en_acaai_members` | `A_PLUS` | `ACCEPT_REVIEW` | `aircargo_agents_member_directory` | 1 | [https://www.acaai.in/list-of-members/](https://www.acaai.in/list-of-members/) | India air cargo agents association member list. |
| 22 | `en_nafl_uae_members` | `A_PLUS` | `ACCEPT_REVIEW` | `national_logistics_association_member_directory` | 1 | [https://nafl.ae/member-list/](https://nafl.ae/member-list/) | UAE freight/logistics association member list. |
| 23 | `en_saaff_south_africa` | `A` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://saaff.org.za/](https://saaff.org.za/) | South Africa freight forwarding association reference/member surface. |
| 24 | `en_fcfasa_members` | `A` | `ACCEPT_REVIEW` | `regional_forwarder_association_member_directory` | 1 | [https://www.fcfasa.org/members](https://www.fcfasa.org/members) | African freight forwarding/customs association members. |
| 25 | `en_kiffwa_kenya` | `A` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://www.kiffwa.com/](https://www.kiffwa.com/) | Kenya freight forwarding association reference/member discovery surface. |
| 26 | `en_uffa_uganda` | `A_MINUS` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://www.uffa.co.ug/](https://www.uffa.co.ug/) | Uganda freight forwarding association reference/member discovery surface. |
| 27 | `en_taffa_tanzania` | `A_MINUS` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://taffa.or.tz/](https://taffa.or.tz/) | Tanzania freight forwarding association reference/member discovery surface. |
| 28 | `en_giff_ghana` | `A_MINUS` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://giff.org.gh/](https://giff.org.gh/) | Ghana freight forwarder association reference/member discovery surface. |
| 29 | `en_crffn_nigeria` | `A_MINUS` | `ACCEPT_REVIEW` | `official_forwarder_regulator_reference` | 1 | [https://crffn.gov.ng/](https://crffn.gov.ng/) | Nigeria freight forwarding regulator/reference surface. |
| 30 | `en_slcba_sri_lanka` | `A_MINUS` | `ACCEPT_REVIEW` | `customs_broker_association_reference` | 1 | [https://slcba.lk/](https://slcba.lk/) | Sri Lanka customs broker association reference/member discovery surface. |
| 31 | `en_iwla_find_warehouse` | `A_PLUS` | `ACCEPT_REVIEW` | `warehouse_logistics_directory` | 8 | [https://iwla.com/](https://iwla.com/) | IWLA warehouse logistics provider search surface. |
| 32 | `en_findawarehouse_iwla` | `A_PLUS` | `ACCEPT_REVIEW` | `warehouse_logistics_directory` | 8 | [https://www.findawarehouse.org/](https://www.findawarehouse.org/) | IWLA Find A Warehouse directory surface. |
| 33 | `en_gcca_global_directory` | `A_PLUS` | `ACCEPT_REVIEW` | `cold_chain_directory` | 8 | [https://www.gcca.org/directory/](https://www.gcca.org/directory/) | Global cold-chain facility/supplier directory. |
| 34 | `en_gcca_top25_reference` | `A_MINUS` | `ACCEPT_REVIEW` | `cold_chain_reference` | 1 | [https://www.gcca.org/resource/top-25-lists/](https://www.gcca.org/resource/top-25-lists/) | Cold-chain top facility reference; not direct frontier insert. |
| 35 | `en_cold_chain_federation_operators` | `A` | `ACCEPT_REVIEW` | `cold_chain_operator_directory` | 2 | [https://www.coldchainfederation.org.uk/members/operators-members/](https://www.coldchainfederation.org.uk/members/operators-members/) | UK temperature-controlled storage and distribution operator directory. |
| 36 | `en_cold_chain_federation_innovators` | `A_MINUS` | `ACCEPT_REVIEW` | `cold_chain_supplier_directory` | 1 | [https://www.coldchainfederation.org.uk/members/innovators-inventors-disruptors-members/](https://www.coldchainfederation.org.uk/members/innovators-inventors-disruptors-members/) | Cold-chain supplier directory requiring category filter. |
| 37 | `en_cool_chain_association_directory` | `A` | `ACCEPT_REVIEW` | `cool_chain_membership_directory` | 1 | [https://coolchain.org/membership/membership-directory/](https://coolchain.org/membership/membership-directory/) | Air/cool-chain membership directory. |
| 38 | `en_bfff_members` | `A_MINUS` | `ACCEPT_REVIEW` | `cold_chain_industry_member_directory` | 1 | [https://bfff.co.uk/members/](https://bfff.co.uk/members/) | Frozen food/cold-chain members; logistics filtering needed. |
| 39 | `en_ukwa_find_member` | `A_MINUS` | `ACCEPT_REVIEW` | `warehouse_association_member_directory` | 1 | [https://www.ukwa.org.uk/find-a-member/](https://www.ukwa.org.uk/find-a-member/) | UK Warehousing Association find-a-member surface. |
| 40 | `en_cold_chain_news_members` | `B_PLUS` | `ACCEPT_REVIEW` | `cold_chain_trade_member_directory` | 1 | [https://www.coldchainnews.com/members/](https://www.coldchainnews.com/members/) | Cold-chain trade directory; lower authority than association directories. |
| 41 | `en_iwla_pdf_directory` | `A_MINUS` | `HOLD` | `warehouse_directory_pdf` | 1 | [https://www.iwla.com/wp-content/uploads/2021/07/2021-2022-Directory-of-Warehouse-Logistics-Providers-and-Partner-PDF.pdf](https://www.iwla.com/wp-content/uploads/2021/07/2021-2022-Directory-of-Warehouse-Logistics-Providers-and-Partner-PDF.pdf) | Warehouse directory PDF; requires PDF handling gate. |
| 42 | `en_aapa_directory` | `A` | `ACCEPT_REVIEW` | `port_association_directory` | 1 | [https://www.aapaseaports.com/index.php/aapa-directory/](https://www.aapaseaports.com/index.php/aapa-directory/) | AAPA seaport directory/reference. |
| 43 | `en_marad_ports_list` | `A_PLUS` | `ACCEPT_REVIEW` | `official_port_listing` | 1 | [https://www.maritime.dot.gov/data-reports/ports/list](https://www.maritime.dot.gov/data-reports/ports/list) | US MARAD official port list/reference. |
| 44 | `en_georgia_ports_services_directory` | `A` | `ACCEPT_REVIEW` | `official_port_services_directory` | 3 | [https://gaports.com/port-services-directory/](https://gaports.com/port-services-directory/) | Georgia Ports official port services directory. |
| 45 | `en_georgia_ports_logistics_companies` | `A` | `ACCEPT_REVIEW` | `official_port_logistics_company_directory` | 2 | [https://gaports.com/logistics-companies/](https://gaports.com/logistics-companies/) | Georgia Ports logistics companies surface. |
| 46 | `en_savannah_chamber_ports_logistics` | `A_MINUS` | `ACCEPT_REVIEW` | `chamber_ports_logistics_member_directory` | 1 | [https://www.savannahchamber.com/membership/member-directory/ports-marine-and-logistics/](https://www.savannahchamber.com/membership/member-directory/ports-marine-and-logistics/) | Savannah ports/marine/logistics member category. |
| 47 | `en_port_greater_baton_rouge_forwarders` | `A_MINUS` | `ACCEPT_REVIEW` | `official_port_forwarder_directory` | 1 | [https://www.portgbr.com/port-directory-freight-forwarders](https://www.portgbr.com/port-directory-freight-forwarders) | Port of Greater Baton Rouge freight forwarder directory. |
| 48 | `en_lacbffa_directory` | `A` | `ACCEPT_REVIEW` | `regional_customs_broker_forwarder_directory` | 1 | [https://www.lacbffa.org/directory](https://www.lacbffa.org/directory) | Los Angeles customs brokers/freight forwarders directory. |
| 49 | `en_los_angeles_forwarders_brokers` | `B_PLUS` | `ACCEPT_REVIEW` | `regional_forwarder_broker_directory` | 1 | [https://losangelesforwardersandbrokers.com/](https://losangelesforwardersandbrokers.com/) | LA forwarder/broker directory; cross-check source. |
| 50 | `en_hcbffa_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `regional_customs_broker_forwarder_directory` | 1 | [https://hcbffa.org/directory.php](https://hcbffa.org/directory.php) | Houston customs brokers/freight forwarders directory. |
| 51 | `en_greater_houston_port_bureau_members` | `A_MINUS` | `ACCEPT_REVIEW` | `port_bureau_member_directory` | 1 | [https://www.txgulf.org/member-directory-public](https://www.txgulf.org/member-directory-public) | Greater Houston port-region member directory. |
| 52 | `en_oakland_customs_brokers_forwarders_pdf` | `A_MINUS` | `HOLD` | `port_customs_forwarder_pdf` | 1 | [https://www.oaklandseaport.com/wp-content/uploads/2019/08/Customs-Brokers-Freight-Forwarders.pdf](https://www.oaklandseaport.com/wp-content/uploads/2019/08/Customs-Brokers-Freight-Forwarders.pdf) | Oakland customs brokers/freight forwarders PDF; requires PDF handling gate. |
| 53 | `en_fpua_members` | `A_MINUS` | `ACCEPT_REVIEW` | `port_users_member_directory` | 1 | [https://www.fpua.co.uk/members/](https://www.fpua.co.uk/members/) | Felixstowe Port Users Association members. |
| 54 | `en_chamber_shipping_canada_members` | `A_MINUS` | `ACCEPT_REVIEW` | `maritime_member_directory` | 1 | [https://shippingmatters.ca/about-cos/membership-directory/](https://shippingmatters.ca/about-cos/membership-directory/) | Canada maritime/logistics ecosystem directory. |
| 55 | `en_bremenports_directory` | `A` | `ACCEPT_REVIEW` | `official_port_directory` | 1 | [https://www.bremenports.de/en/directory](https://www.bremenports.de/en/directory) | Bremenports official directory. |
| 56 | `en_container_intermodal_vancouver_drayage` | `B_PLUS` | `ACCEPT_REVIEW` | `drayage_intermodal_directory` | 1 | [https://containerintermodal.ca/drayage-directory/vancouver/](https://containerintermodal.ca/drayage-directory/vancouver/) | Vancouver drayage/intermodal directory. |
| 57 | `en_drayage_lax_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `drayage_intermodal_directory` | 1 | [https://www.drayage.com/directory/results.cfm?OceanCntrs=y&city=LAX&port=y&sortby=2](https://www.drayage.com/directory/results.cfm?OceanCntrs=y&city=LAX&port=y&sortby=2) | LA/LB drayage directory. |
| 58 | `en_drayage_vancouver_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `drayage_intermodal_directory` | 1 | [https://www.drayage.com/directory/results.cfm?city=VAN](https://www.drayage.com/directory/results.cfm?city=VAN) | Vancouver drayage directory. |
| 59 | `en_loadmatch_us_3pl_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_3pl_directory` | 3 | [https://www.loadmatch.com/directory/results.cfm?category=3rd-party&state_code=ca](https://www.loadmatch.com/directory/results.cfm?category=3rd-party&state_code=ca) | US 3PL/IMC/NVO/forwarder/broker directory. |
| 60 | `en_mgn_maritime_directory` | `B` | `ACCEPT_REVIEW` | `commercial_maritime_directory` | 2 | [https://www.mgn.com/directory](https://www.mgn.com/directory) | Commercial maritime directory; category filtering needed. |
| 61 | `en_ports_agents_network` | `B` | `ACCEPT_REVIEW` | `commercial_port_agents_network` | 2 | [https://port-agents.com/network](https://port-agents.com/network) | Port agents network directory; quality live check required. |
| 62 | `en_searates_maritime_reference` | `B` | `HOLD` | `port_reference` | 1 | [https://www.searates.com/maritime](https://www.searates.com/maritime) | Port/reference surface, not direct company directory. |
| 63 | `en_icontainers_ports_reference` | `B` | `HOLD` | `port_reference` | 1 | [https://www.icontainers.com/ports/](https://www.icontainers.com/ports/) | Port reference/enrichment surface, not direct company directory. |
| 64 | `en_transport_logistic_exhibitor_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `trade_fair_exhibitor_directory` | 3 | [https://transportlogistic.de/en/trade-fair/exhibitor-directory/](https://transportlogistic.de/en/trade-fair/exhibitor-directory/) | Major logistics trade fair exhibitor directory. |
| 65 | `en_air_cargo_europe_exhibitor_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `air_cargo_trade_fair_directory` | 2 | [https://transportlogistic.de/en/aircargoeurope/exhibitor-directory/exhibitors-sectors/](https://transportlogistic.de/en/aircargoeurope/exhibitor-directory/exhibitors-sectors/) | Air cargo Europe exhibitor sectors/directory. |
| 66 | `en_breakbulk_americas_exhibitors` | `A_MINUS` | `ACCEPT_REVIEW` | `breakbulk_project_cargo_exhibitor_directory` | 2 | [https://americas.breakbulk.com/exhibitors](https://americas.breakbulk.com/exhibitors) | Breakbulk/project cargo exhibitor directory. |
| 67 | `en_multimodal_uk_exhibitors` | `A_MINUS` | `ACCEPT_REVIEW` | `logistics_trade_fair_exhibitor_directory` | 1 | [https://www.multimodal.org.uk/exhibitor-list-2026](https://www.multimodal.org.uk/exhibitor-list-2026) | UK multimodal logistics exhibitor list. |
| 68 | `en_transport_logistic_americas_exhibitors` | `A_MINUS` | `ACCEPT_REVIEW` | `trade_fair_exhibitor_directory` | 1 | [https://transportlogistic-americas.com/en/trade-show/exhibitor-directory/](https://transportlogistic-americas.com/en/trade-show/exhibitor-directory/) | Transport logistic Americas exhibitor directory; event freshness review needed. |
| 69 | `en_air_cargo_sea_exhibitors` | `B_PLUS` | `ACCEPT_REVIEW` | `air_cargo_trade_fair_directory` | 1 | [https://aircargosea.com/exhibitors-directory-2025/](https://aircargosea.com/exhibitors-directory-2025/) | Southeast Asia air cargo exhibitor directory. |
| 70 | `en_project_cargo_summit_exhibitors` | `B_PLUS` | `ACCEPT_REVIEW` | `project_cargo_trade_fair_reference` | 1 | [https://projectcargosummit.com/](https://projectcargosummit.com/) | Project cargo event/exhibitor discovery surface. |
| 71 | `en_logistics_uk_events` | `B_PLUS` | `ACCEPT_REVIEW` | `logistics_event_reference` | 1 | [https://logistics.org.uk/events](https://logistics.org.uk/events) | Logistics UK events/exhibitor discovery surface. |
| 72 | `en_sitl_exhibitors_fallback` | `B_PLUS` | `ACCEPT_REVIEW` | `trade_fair_exhibitor_directory` | 1 | [https://www.sitl.eu/fr-fr/qui-participe/liste-des-exposants.html](https://www.sitl.eu/fr-fr/qui-participe/liste-des-exposants.html) | French/EU logistics trade fair fallback in English super-expansion. |
| 73 | `en_project_cargo_network_members` | `A_MINUS` | `ACCEPT_REVIEW` | `project_cargo_network_member_directory` | 1 | [https://www.projectcargonetwork.com/about/global](https://www.projectcargonetwork.com/about/global) | Project cargo network member directory/reference. |
| 74 | `en_wwpc_member_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `project_cargo_network_member_directory` | 1 | [https://wwpc.eu.com/member-directory/](https://wwpc.eu.com/member-directory/) | Worldwide Project Consortium member directory. |
| 75 | `en_opca_project_cargo_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `project_cargo_commercial_directory` | 1 | [https://overseasprojectcargo.com/Directory/](https://overseasprojectcargo.com/Directory/) | Commercial project cargo directory. |
| 76 | `en_gln_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `global_freight_network_directory` | 1 | [https://go2gln.com/](https://go2gln.com/) | Global Logistics Network directory/reference. |
| 77 | `en_globalink_members` | `B_PLUS` | `ACCEPT_REVIEW` | `global_freight_network_directory` | 1 | [https://www.glnk.com/freight-forwarder-network/members](https://www.glnk.com/freight-forwarder-network/members) | Globalink freight forwarder network members. |
| 78 | `en_fnc_network_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `global_freight_network_directory` | 1 | [https://fncnetwork.com/directory](https://fncnetwork.com/directory) | FNC freight network directory. |
| 79 | `en_df_alliance_member_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `digital_freight_network_directory` | 1 | [https://www.df-alliance.com/benefits/member-directory](https://www.df-alliance.com/benefits/member-directory) | Digital Freight Alliance member directory. |
| 80 | `en_all_forward_members_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `global_freight_network_directory` | 1 | [https://www.all-forward.com/MembersDirectory](https://www.all-forward.com/MembersDirectory) | All Forward members directory. |
| 81 | `en_aeroceanetwork_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `air_ocean_freight_network_directory` | 1 | [https://aeroceanetwork.net/directory/](https://aeroceanetwork.net/directory/) | AeroOceaNetwork directory. |
| 82 | `en_freight_midpoint_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `freight_network_directory` | 1 | [https://freightmidpoint.com/Directory/](https://freightmidpoint.com/Directory/) | Freight Midpoint member directory. |
| 83 | `en_jctrans_company_list` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_freight_company_directory` | 12 | [https://www.jctrans.com/en/company/list](https://www.jctrans.com/en/company/list) | JCtrans company list; commercial fallback with country/filter surfaces. |
| 84 | `en_gla_family_member_directory` | `B` | `ACCEPT_REVIEW` | `global_logistics_network_directory` | 1 | [https://www.glafamily.com/en/member-directory](https://www.glafamily.com/en/member-directory) | GLA Family member directory. |
| 85 | `en_lognet_global_directory` | `B` | `ACCEPT_REVIEW` | `global_freight_network_directory` | 1 | [https://www.lognetglobal.com/directory](https://www.lognetglobal.com/directory) | Lognet Global directory. |
| 86 | `en_digifreight_member_list` | `B` | `ACCEPT_REVIEW` | `digital_freight_network_directory` | 1 | [https://www.digifreight.live/member-list/](https://www.digifreight.live/member-list/) | DigiFreight member list. |
| 87 | `en_freightnet_global_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_global_freight_directory` | 48 | [https://www.freightnet.com/directory/](https://www.freightnet.com/directory/) | FreightNet commercial global country/category directory surfaces. |
| 88 | `en_cargoyellowpages_global` | `B` | `ACCEPT_REVIEW` | `commercial_global_cargo_directory` | 24 | [https://www.cargoyellowpages.com/home.html](https://www.cargoyellowpages.com/home.html) | Cargo Yellow Pages commercial fallback country pages. |
| 89 | `en_shippers_list_directory` | `B` | `ACCEPT_REVIEW` | `commercial_directory` | 1 | [https://shippers-list.com/](https://shippers-list.com/) | Commercial logistics/freight directory; fallback only. |
| 90 | `en_freight_forwarder_services_directory` | `B` | `ACCEPT_REVIEW` | `commercial_forwarder_directory` | 1 | [https://freightforwarderservices.com/](https://freightforwarderservices.com/) | Commercial freight forwarder service directory. |
| 91 | `en_freighthub_directory` | `B_MINUS` | `HOLD` | `commercial_logistics_directory` | 1 | [https://freighthub.co/](https://freighthub.co/) | Low-priority commercial directory; HOLD unless needed. |
| 92 | `en_azfreight_country_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_air_freight_country_directory` | 12 | [https://azfreight.com/](https://azfreight.com/) | AZFreight country/facility pages; commercial fallback. |
| 93 | `en_clecat_members` | `A_MINUS` | `ACCEPT_REVIEW` | `european_association_member_reference` | 1 | [https://www.clecat.org/members/full-members](https://www.clecat.org/members/full-members) | European forwarding/logistics association member reference. |
| 94 | `en_spedlogswiss_members` | `A` | `ACCEPT_REVIEW` | `national_association_member_directory` | 1 | [https://spedlogswiss.com/enUK/association/members](https://spedlogswiss.com/enUK/association/members) | Swiss forwarding/logistics member directory. |
| 95 | `en_forward_belgium_find_forwarder` | `A` | `ACCEPT_REVIEW` | `national_association_member_directory` | 1 | [https://forwardbelgium.be/find-a-forwarder](https://forwardbelgium.be/find-a-forwarder) | Belgian forwarder association directory. |
| 96 | `en_tlf_france_directory` | `A` | `ACCEPT_REVIEW` | `national_association_member_directory` | 1 | [https://e-tlf.com/annuaire/](https://e-tlf.com/annuaire/) | French transport/logistics association member directory. |
| 97 | `en_dslv_germany_members_reference` | `A` | `ACCEPT_REVIEW` | `national_association_reference` | 1 | [https://www.dslv.org/](https://www.dslv.org/) | Germany freight forwarding/logistics association reference; member directory discovery needed. |
| 98 | `en_fedespedi_italy_members` | `A_MINUS` | `ACCEPT_REVIEW` | `national_association_reference` | 1 | [https://www.fedespedi.it/](https://www.fedespedi.it/) | Italian freight forwarder association reference/member discovery. |
| 99 | `en_feteia_spain_members` | `A_MINUS` | `ACCEPT_REVIEW` | `national_association_reference` | 1 | [https://www.feteia.org/](https://www.feteia.org/) | Spanish freight forwarder association reference/member discovery. |
| 100 | `en_apat_portugal_members` | `A_MINUS` | `ACCEPT_REVIEW` | `national_association_reference` | 1 | [https://www.apat.pt/](https://www.apat.pt/) | Portuguese freight forwarder association reference/member discovery. |
| 101 | `en_fenex_netherlands_members` | `A_MINUS` | `ACCEPT_REVIEW` | `national_association_reference` | 1 | [https://www.fenex.nl/](https://www.fenex.nl/) | Netherlands forwarding/logistics association reference. |
| 102 | `en_bgl_germany_transport_association` | `A_MINUS` | `ACCEPT_REVIEW` | `transport_association_reference` | 1 | [https://www.bgl-ev.de/](https://www.bgl-ev.de/) | German road transport association reference/member discovery. |
| 103 | `en_dvfv_germany_rail_freight` | `A_MINUS` | `ACCEPT_REVIEW` | `rail_freight_association_reference` | 1 | [https://www.die-gueterbahnen.com/](https://www.die-gueterbahnen.com/) | German rail freight association reference. |
| 104 | `en_hafen_hamburg_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `port_logistics_directory` | 2 | [https://www.hafen-hamburg.de/en/](https://www.hafen-hamburg.de/en/) | Hamburg port logistics/directory surfaces. |
| 105 | `en_frankfurt_cargohub` | `A_MINUS` | `ACCEPT_REVIEW` | `airport_cargo_cluster_directory` | 1 | [https://www.cargohub-frankfurt.de/](https://www.cargohub-frankfurt.de/) | Frankfurt air cargo cluster directory/reference. |
| 106 | `en_aircargo_community_frankfurt` | `A_MINUS` | `ACCEPT_REVIEW` | `air_cargo_community_directory` | 1 | [https://www.aircargocommunity.de/](https://www.aircargocommunity.de/) | Frankfurt Air Cargo Community member/reference surface. |
| 107 | `en_bsk_heavy_transport_germany` | `A_MINUS` | `ACCEPT_REVIEW` | `heavy_transport_association_reference` | 1 | [https://www.bsk-ffm.de/](https://www.bsk-ffm.de/) | German crane/heavy transport association reference. |
| 108 | `en_utikad_turkey_members` | `A` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://www.utikad.org.tr/](https://www.utikad.org.tr/) | Turkish freight forwarder/logistics association reference. |
| 109 | `en_und_turkey_road_transport` | `A_MINUS` | `ACCEPT_REVIEW` | `road_transport_association_reference` | 1 | [https://www.und.org.tr/](https://www.und.org.tr/) | Turkish road transport association reference. |
| 110 | `en_igmd_turkey_customs_brokers` | `A_MINUS` | `ACCEPT_REVIEW` | `customs_broker_association_reference` | 1 | [https://www.igmd.org.tr/](https://www.igmd.org.tr/) | Istanbul customs brokers association reference. |
| 111 | `en_affm_morocco` | `A` | `ACCEPT_REVIEW` | `national_forwarder_association_reference` | 1 | [https://www.affm.ma/](https://www.affm.ma/) | Morocco freight forwarder association reference. |
| 112 | `en_apt_mauritius_members` | `A` | `ACCEPT_REVIEW` | `national_forwarder_association_member_directory` | 1 | [https://www.aptmu.com/members/](https://www.aptmu.com/members/) | Mauritius freight forwarder association members. |
| 113 | `en_mra_mauritius_forwarding_agents_pdf` | `A_PLUS` | `ACCEPT_REVIEW` | `official_forwarding_agents_pdf` | 1 | [https://www.mra.mu/download/ForwardingFreightAgentsList.pdf](https://www.mra.mu/download/ForwardingFreightAgentsList.pdf) | Official Mauritius forwarding agents PDF; requires PDF handling gate. |
| 114 | `en_mra_mauritius_customs_brokers_pdf` | `A_PLUS` | `ACCEPT_REVIEW` | `official_customs_brokers_pdf` | 1 | [https://www.mra.mu/download/CustomsBrokersList.pdf](https://www.mra.mu/download/CustomsBrokersList.pdf) | Official Mauritius customs brokers PDF; requires PDF handling gate. |
| 115 | `en_port_boulogne_calais_rde` | `A` | `ACCEPT_REVIEW` | `official_port_customs_representative_directory` | 3 | [https://www.portboulognecalais.fr/services-aux-professionnels/services-a-la-marchandise/](https://www.portboulognecalais.fr/services-aux-professionnels/services-a-la-marchandise/) | Official port customs representative directory surfaces. |
| 116 | `en_union_ports_france_members` | `A` | `ACCEPT_REVIEW` | `official_port_association_member_directory` | 2 | [https://www.port.fr/liste-des-membres](https://www.port.fr/liste-des-membres) | Union des Ports de France members directory. |
| 117 | `en_haropa_port_logistics` | `A_MINUS` | `ACCEPT_REVIEW` | `official_port_logistics_reference` | 1 | [https://www.haropaport.com/en](https://www.haropaport.com/en) | Official port/logistics ecosystem surface. |
| 118 | `en_marseille_fos_logistics` | `A_MINUS` | `ACCEPT_REVIEW` | `official_port_logistics_reference` | 1 | [https://www.marseille-port.fr/en/filieres/logistics](https://www.marseille-port.fr/en/filieres/logistics) | Official Marseille-Fos logistics surface. |
| 119 | `en_paris_aeroport_cargo` | `A_MINUS` | `ACCEPT_REVIEW` | `official_airport_cargo_surface` | 3 | [https://www.parisaeroport.fr/en/professionals/cargo](https://www.parisaeroport.fr/en/professionals/cargo) | Paris airport cargo/operator surfaces. |
| 120 | `en_umf_marseille_fos_adherents` | `A_MINUS` | `ACCEPT_REVIEW` | `maritime_association_member_directory` | 1 | [https://umf.asso.fr/en/umf-adherents](https://umf.asso.fr/en/umf-adherents) | Marseille-Fos maritime/logistics adherents. |
| 121 | `en_cluster_logistics_luxembourg_members` | `A` | `ACCEPT_REVIEW` | `logistics_cluster_member_directory` | 1 | [https://www.clusterforlogistics.lu/members](https://www.clusterforlogistics.lu/members) | Luxembourg logistics cluster members. |
| 122 | `en_logistics_public_lu_key_players` | `A_MINUS` | `ACCEPT_REVIEW` | `official_logistics_partner_reference` | 1 | [https://logistics.public.lu/en/setup-business/key-players.html](https://logistics.public.lu/en/setup-business/key-players.html) | Luxembourg official logistics key players surface. |
| 123 | `en_lux_airport_cargo` | `A_MINUS` | `ACCEPT_REVIEW` | `official_airport_cargo_surface` | 1 | [https://www.lux-airport.lu/corporate/business-partners/cargo/](https://www.lux-airport.lu/corporate/business-partners/cargo/) | Luxembourg airport cargo partners surface. |
| 124 | `en_cluster_maritime_luxembourg_members` | `B_PLUS` | `ACCEPT_REVIEW` | `maritime_cluster_member_directory` | 1 | [https://www.cluster-maritime.lu/members-list/](https://www.cluster-maritime.lu/members-list/) | Luxembourg maritime cluster member list. |
| 125 | `en_truckstopquebec_annuaire` | `B_PLUS` | `ACCEPT_REVIEW` | `regional_transport_directory` | 1 | [https://www.truckstopquebec.com/annuaire/](https://www.truckstopquebec.com/annuaire/) | Quebec transport directory; live check required. |
| 126 | `en_mcci_mauritius_members_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `chamber_member_directory` | 1 | [https://www.mcci.org/en/membership/members-directory/?alph=F](https://www.mcci.org/en/membership/members-directory/?alph=F) | Mauritius chamber directory requiring logistics category filter. |
| 127 | `en_eu_aeo_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `aeo_operator_directory` | 5 | [https://www.aeodirectory.com/aeo/search/](https://www.aeodirectory.com/aeo/search/) | AEO directory; mixed industries, logistics filtering required. |
| 128 | `en_eu_aeo_reference` | `A` | `ACCEPT_REVIEW` | `official_customs_reference` | 1 | [https://taxation-customs.ec.europa.eu/customs/authorised-economic-operator_en](https://taxation-customs.ec.europa.eu/customs/authorised-economic-operator_en) | Official EU AEO reference; not direct company directory. |
| 129 | `en_douane_france_customs_representatives` | `A` | `ACCEPT_REVIEW` | `official_customs_reference` | 1 | [https://www.douane.gouv.fr/fiche/registered-customs-representatives](https://www.douane.gouv.fr/fiche/registered-customs-representatives) | French customs representatives official reference. |
| 130 | `en_official_fr_transport_registers` | `A_PLUS` | `ACCEPT_REVIEW` | `official_transport_register_download_page` | 1 | [https://www.ecologie.gouv.fr/politiques-publiques/liste-entreprises-inscrites-registre-electronique-national-entreprises](https://www.ecologie.gouv.fr/politiques-publiques/liste-entreprises-inscrites-registre-electronique-national-entreprises) | French national transport register gateway; requires download/zip handling gate. |

## Source type distribution

| Source type | Count |
|---|---:|
| `aeo_operator_directory` | 1 |
| `air_cargo_community_directory` | 1 |
| `air_cargo_trade_fair_directory` | 2 |
| `air_forwarder_association_marketplace` | 1 |
| `air_ocean_freight_network_directory` | 1 |
| `aircargo_agents_member_directory` | 2 |
| `airport_cargo_cluster_directory` | 1 |
| `breakbulk_project_cargo_exhibitor_directory` | 1 |
| `chamber_member_directory` | 1 |
| `chamber_ports_logistics_member_directory` | 1 |
| `cold_chain_directory` | 1 |
| `cold_chain_industry_member_directory` | 1 |
| `cold_chain_operator_directory` | 1 |
| `cold_chain_reference` | 1 |
| `cold_chain_supplier_directory` | 1 |
| `cold_chain_trade_member_directory` | 1 |
| `commercial_3pl_directory` | 1 |
| `commercial_air_freight_country_directory` | 1 |
| `commercial_directory` | 1 |
| `commercial_forwarder_directory` | 1 |
| `commercial_freight_company_directory` | 1 |
| `commercial_global_cargo_directory` | 1 |
| `commercial_global_freight_directory` | 1 |
| `commercial_logistics_directory` | 1 |
| `commercial_maritime_directory` | 1 |
| `commercial_port_agents_network` | 1 |
| `cool_chain_membership_directory` | 1 |
| `customs_broker_association_of_associations` | 1 |
| `customs_broker_association_reference` | 2 |
| `customs_broker_member_search` | 1 |
| `digital_freight_network_directory` | 2 |
| `drayage_intermodal_directory` | 3 |
| `european_association_member_reference` | 1 |
| `freight_network_directory` | 1 |
| `global_freight_forwarder_network_directory` | 1 |
| `global_freight_network_directory` | 5 |
| `global_logistics_network_directory` | 1 |
| `heavy_transport_association_reference` | 1 |
| `logistics_cluster_member_directory` | 1 |
| `logistics_event_reference` | 1 |
| `logistics_trade_fair_exhibitor_directory` | 1 |
| `maritime_association_member_directory` | 1 |
| `maritime_cluster_member_directory` | 1 |
| `maritime_member_directory` | 1 |
| `national_association_business_directory` | 1 |
| `national_association_member_directory` | 8 |
| `national_association_member_search` | 1 |
| `national_association_reference` | 5 |
| `national_forwarder_association_member_directory` | 1 |
| `national_forwarder_association_member_search` | 1 |
| `national_forwarder_association_reference` | 7 |
| `national_logistics_association_member_directory` | 2 |
| `official_air_cargo_directory` | 1 |
| `official_airport_cargo_surface` | 2 |
| `official_customs_agent_register` | 1 |
| `official_customs_broker_listing` | 1 |
| `official_customs_brokers_pdf` | 1 |
| `official_customs_reference` | 2 |
| `official_forwarder_regulator_reference` | 1 |
| `official_forwarding_agents_pdf` | 1 |
| `official_global_association_members_directory` | 1 |
| `official_logistics_partner_reference` | 1 |
| `official_ocean_transport_intermediary_listing` | 1 |
| `official_port_association_member_directory` | 1 |
| `official_port_customs_representative_directory` | 1 |
| `official_port_directory` | 1 |
| `official_port_forwarder_directory` | 1 |
| `official_port_listing` | 1 |
| `official_port_logistics_company_directory` | 1 |
| `official_port_logistics_reference` | 2 |
| `official_port_services_directory` | 1 |
| `official_transport_register_download_page` | 1 |
| `port_association_directory` | 1 |
| `port_bureau_member_directory` | 1 |
| `port_customs_forwarder_pdf` | 1 |
| `port_logistics_directory` | 1 |
| `port_reference` | 2 |
| `port_users_member_directory` | 1 |
| `project_cargo_commercial_directory` | 1 |
| `project_cargo_network_member_directory` | 2 |
| `project_cargo_trade_fair_reference` | 1 |
| `rail_freight_association_reference` | 1 |
| `regional_customs_broker_forwarder_directory` | 2 |
| `regional_forwarder_association_member_directory` | 1 |
| `regional_forwarder_broker_directory` | 1 |
| `regional_transport_directory` | 1 |
| `road_transport_association_reference` | 1 |
| `third_party_logistics_member_directory` | 1 |
| `trade_fair_exhibitor_directory` | 3 |
| `transport_association_reference` | 1 |
| `warehouse_association_member_directory` | 1 |
| `warehouse_directory_pdf` | 1 |
| `warehouse_logistics_directory` | 2 |

## Safety boundary

- `candidate_manifest`: true after catalog rewrite.
- `is_live`: false after catalog rewrite.
- `live_frontier_activation`: false.
- `db_insert_allowed`: false.
- `url_fetch_allowed_in_catalog_gate`: false.
- `crawler_start_allowed_in_catalog_gate`: false.
- `pi51c_sync_allowed_in_catalog_gate`: false.
- `manual_review_required`: true.
- `no_aggressive_pagination`: true.
- `same_day_full_country_expansion`: false.
- `max_initial_depth`: `0_or_1`.

## Next expected gates

1. `SOURCE_SEED_R191_ENGLISH_SUPER_EXPANSION_DECISION_DOC_AUDIT_READONLY`
2. `SOURCE_SEED_R192_ENGLISH_SUPER_EXPANSION_DECISION_DOC_COMMIT_PUSH_GATE`
3. `SOURCE_SEED_R193_ENGLISH_SUPER_EXPANSION_DECISION_DOC_POST_PUSH_SEAL_READONLY`
4. Later: English catalog rewrite/repair to French-style candidate manifest schema.
