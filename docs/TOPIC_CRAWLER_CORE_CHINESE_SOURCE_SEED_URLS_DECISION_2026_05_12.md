# Chinese Source-Seed URLs Decision — 2026-05-12

## Gate metadata

- Gate: `SOURCE_SEED_R148_CHINESE_DECISION_DOC_PATCH_LOCAL_ONLY`
- Machine: Ubuntu Desktop
- Scope: local-only decision document creation
- Canonical head at creation: `628f90173fb0a7d9974ff6e6edde6ad90f6910f8`
- Target language code: `zh`
- Target language name: Chinese
- Region scope values: `CN`, `HK`, `TW`
- Candidate source family count: `105`
- Candidate seed surface count: `106`
- Unique seed host count: `44`

## Hard boundary rule

Crawler_Core collects raw evidence only. Raw links are not `added_seeds`. Parse_Core may create `added_seeds` after pre-ranking. Desktop_Import on Ubuntu Desktop converts pre-ranking into real ranking / final rank.

This document is a decision plan only. It does not create Chinese catalog JSON, does not insert into DB, does not activate frontier rows, does not start crawler, and does not perform URL fetch or live probe.

## Language and region modeling

- `zh` is the language code for Chinese.
- `cn`, `hk`, and `tw` are not language codes in this source-seed rollout.
- `cn`, `hk`, and `tw` are country / region surfaces: China Mainland, Hong Kong China, and Taiwan China.
- Do not add taxonomy languages `cn`, `hk`, or `tw`.
- Future variant design, if needed, must use a separate explicit gate for variants such as `zh-CN`, `zh-HK`, `zh-TW`, `zh-Hans`, or `zh-Hant`.
- Chinese source-seed coverage should preserve `region_scope` / `country_scope` metadata for `CN`, `HK`, and `TW`.

## Runtime and safety policy

- is_enabled=false
- needs_live_check=true
- runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert
- manual_review_required=true
- no_aggressive_pagination=true
- same_day_full_country_expansion=false
- max_initial_depth=0_or_1
- no_live_frontier_activation=true
- no_db_insert=true
- no_crawler_start=true
- no_url_fetch_or_live_probe_in_decision_doc=true

## Shared-host / FIATA politeness note

FIATA is an excellent source for many languages and countries, but `fiata.org` is one shared root host. Chinese rollout may include FIATA CN/HK/TW surfaces as high-quality association country/region directory evidence, but future runtime activation must respect a separate shared-host politeness and budget policy.

Temporary modeling rule:

- `host_budget_group=fiata_global_shared`
- `same_day_full_country_expansion=false`
- `no_aggressive_pagination=true`
- `per_language_surface_activation=gated`

The final FIATA/shared-host crawl politeness policy will be defined later after source/startpoint rollout for Chinese and the remaining languages.

## Source-family candidate summary

- quality_tier_counts: `{'A': 11, 'A_MINUS': 23, 'A_PLUS': 11, 'B': 36, 'B_MINUS': 4, 'B_PLUS': 20}`
- decision_status_counts: `{'ACCEPT': 7, 'ACCEPT_REVIEW': 60, 'HOLD': 38}`
- region_scope_counts: `{'CN': 39, 'CN,GLOBAL': 3, 'CN,HK,TW': 1, 'CN,HK,TW,ASIA': 1, 'GLOBAL': 7, 'GLOBAL,HK': 1, 'HK': 38, 'TW': 15}`

| # | quality_tier | decision_status | source_family_code | source_role | region_scope | host_budget_group | note |
|---:|---|---|---|---|---|---|---|
| 1 | A_PLUS | ACCEPT | `fiata_china_region_member_directory_shared` | `shared_association_country_member_directory` | `CN,HK,TW` | `fiata.org` | FIATA CN/HK/TW region surfaces. Do not split cn/hk/tw as languages. |
| 2 | A_PLUS | ACCEPT | `cn_cifa_member_query_directory` | `association_member_query_directory` | `CN` | `zizhan.cifa-china.com` | Chinese CIFA member query; high-value Chinese-language directory surface. |
| 3 | A | HOLD | `cn_cifa_authority_reference` | `association_authority_reference` | `CN` | `zizhan.cifa-china.com|cifa-china.com` | Authority/context only unless direct stable member directory is confirmed. |
| 4 | B_PLUS | HOLD | `azfreight_cifa_crosscheck` | `commercial_association_crosscheck` | `CN` | `azfreight.com` | Cross-check only. |
| 5 | B_PLUS | ACCEPT_REVIEW | `forwardingcompanies_cifa_members` | `commercial_association_member_mirror` | `CN` | `forwardingcompanies.com` | Commercial mirror of CIFA-like member surface. |
| 6 | A_PLUS | ACCEPT | `hk_haffa_member_directory` | `association_member_directory` | `HK` | `haffa.com.hk` | Strong Hong Kong freight/logistics member directory. |
| 7 | A | ACCEPT_REVIEW | `hk_haffa_member_profile` | `association_profile_reference` | `HK` | `haffa.com.hk` | Profile/reference around HAFFA membership. |
| 8 | A_MINUS | HOLD | `hk_haffa_fiata_license_reference` | `association_authority_reference` | `HK` | `haffa.com.hk` | FIATA license/reference context. |
| 9 | A_PLUS | ACCEPT | `hk_mardep_shipping_directory` | `official_shipping_directory_root` | `HK` | `mardep.gov.hk` | Official HK Marine Department shipping directory root. |
| 10 | A_PLUS | ACCEPT | `hk_mardep_freight_forwarders_logistics_directory` | `official_freight_logistics_directory` | `HK` | `mardep.gov.hk` | Official freight forwarders/logistics directory. |
| 11 | A | ACCEPT_REVIEW | `hk_mardep_shipping_companies_directory` | `official_shipping_company_directory` | `HK` | `mardep.gov.hk` | Official shipping-company directory; logistics relevance review. |
| 12 | A | ACCEPT_REVIEW | `hk_mardep_local_shipping_agents_directory` | `official_shipping_agent_directory` | `HK` | `mardep.gov.hk` | Official local shipping agents directory. |
| 13 | A | ACCEPT_REVIEW | `hk_mardep_container_freight_stations_directory` | `official_container_freight_station_directory` | `HK` | `mardep.gov.hk` | Official container freight station directory. |
| 14 | A | ACCEPT_REVIEW | `hk_mardep_shipping_directory_csv` | `official_directory_dataset` | `HK` | `mardep.gov.hk` | CSV evidence surface for Marine Department directory. |
| 15 | A | ACCEPT_REVIEW | `hk_mpdb_freight_forwarders_logistics_directory` | `official_maritime_portal_directory` | `HK` | `hkmpdb.gov.hk` | HK maritime portal freight/logistics directory. |
| 16 | B_PLUS | ACCEPT_REVIEW | `hk_maritime_hub_directory_root` | `maritime_hub_directory_root` | `HK` | `hongkongmaritimehub.com` | Directory root; overlap review needed. |
| 17 | B_PLUS | ACCEPT_REVIEW | `hk_maritime_hub_freight_forwarders_directory` | `maritime_hub_freight_logistics_directory` | `HK` | `hongkongmaritimehub.com` | Freight/logistics directory; overlap with official surfaces likely. |
| 18 | B_PLUS | HOLD | `hk_maritime_hub_trade_shipping_orgs` | `industry_organization_context` | `HK` | `hongkongmaritimehub.com` | Organization context, not primary company crawl. |
| 19 | A_MINUS | HOLD | `hkgcc_haffa_reference` | `chamber_profile_reference` | `HK` | `chamber.org.hk` | HAFFA chamber profile/cross-check. |
| 20 | A_PLUS | ACCEPT | `hk_aat_freight_forwarder_directory` | `airport_freight_forwarder_directory` | `HK` | `aat.com.hk` | Airport freight-forwarder directory. |
| 21 | A_PLUS | ACCEPT_REVIEW | `hk_aat_freight_forwarder_directory_alpha_c` | `airport_freight_forwarder_directory_alpha` | `HK` | `aat.com.hk` | Alphabetic directory surface. |
| 22 | A_PLUS | ACCEPT_REVIEW | `hk_aat_freight_forwarder_directory_alpha_d` | `airport_freight_forwarder_directory_alpha` | `HK` | `aat.com.hk` | Alphabetic directory surface. |
| 23 | A_PLUS | ACCEPT_REVIEW | `hk_aat_freight_forwarder_directory_alpha_j` | `airport_freight_forwarder_directory_alpha` | `HK` | `aat.com.hk` | Alphabetic directory surface. |
| 24 | A_PLUS | ACCEPT_REVIEW | `hk_aat_freight_forwarder_directory_alpha_s` | `airport_freight_forwarder_directory_alpha` | `HK` | `aat.com.hk` | Alphabetic directory surface. |
| 25 | A | ACCEPT_REVIEW | `hk_aat_freight_forwarder_directory_zh_hant` | `airport_freight_forwarder_directory_zh_hant` | `HK` | `aat.com.hk` | Traditional Chinese directory surface. |
| 26 | A_MINUS | HOLD | `iata_cargolink_directory_shared` | `global_air_cargo_directory_reference` | `GLOBAL,HK` | `iata.org` | Global shared authority directory; live-probe required. |
| 27 | A_MINUS | HOLD | `iata_hactl_air_cargo_terminal_reference` | `air_cargo_terminal_reference` | `HK` | `iata.org` | HACTL IATA reference. |
| 28 | A_MINUS | HOLD | `hk_hactl_authority_reference` | `air_cargo_terminal_reference` | `HK` | `hactl.com` | Authority/context only. |
| 29 | A_MINUS | HOLD | `hk_customs_aeo_list` | `official_aeo_mixed_industry_list` | `HK` | `customs.gov.hk` | Official but mixed industry. |
| 30 | A_MINUS | HOLD | `hk_data_gov_aeo_dataset` | `official_aeo_dataset` | `HK` | `data.gov.hk` | Official dataset; mixed industry. |
| 31 | A_MINUS | HOLD | `hk_data_gov_aeo_resource` | `official_aeo_dataset_resource` | `HK` | `data.gov.hk` | Resource-level official evidence. |
| 32 | A_MINUS | HOLD | `hk_customs_aeo_dictionary_pdf` | `official_aeo_dictionary` | `HK` | `customs.gov.hk` | Schema/context only. |
| 33 | A_MINUS | HOLD | `wco_aeo_crosscheck` | `global_aeo_crosscheck` | `GLOBAL` | `wcoomd.org` | Cross-check only. |
| 34 | A_PLUS | ACCEPT | `tw_freight_forwarders_open_data` | `official_freight_forwarder_open_data` | `TW` | `data.gov.tw` | Official Taiwan freight-forwarder dataset. |
| 35 | A | ACCEPT_REVIEW | `tw_customs_area_open_data` | `official_customs_open_data` | `TW` | `data.gov.tw` | Customs-area dataset; review mapping. |
| 36 | A | ACCEPT_REVIEW | `tw_customs_declaration_open_data` | `official_customs_declaration_open_data` | `TW` | `data.gov.tw` | Customs declaration list. |
| 37 | A_MINUS | HOLD | `tw_customs_high_quality_enterprise_directory` | `official_quality_enterprise_dataset` | `TW` | `data.gov.tw` | Mixed enterprise dataset. |
| 38 | A_MINUS | HOLD | `tw_customs_aeo_portal` | `official_aeo_reference` | `TW` | `customs.gov.tw` | Official AEO reference. |
| 39 | A_MINUS | HOLD | `tw_customs_taichung_context` | `official_customs_context` | `TW` | `customs.gov.tw` | Context only. |
| 40 | A | ACCEPT_REVIEW | `fiata_taiwan_member_directory` | `shared_association_country_member_directory` | `TW` | `fiata.org` | Taiwan FIATA surface; may be grouped with FIATA shared family. |
| 41 | A_MINUS | HOLD | `iata_taipei_forwarders_logistics_association_reference` | `association_authority_reference` | `TW` | `iata.org` | Association reference. |
| 42 | B | ACCEPT_REVIEW | `freightnet_taiwan_forwarders` | `commercial_freight_forwarder_directory` | `TW` | `freightnet.com` | Commercial Taiwan forwarder directory. |
| 43 | B | ACCEPT_REVIEW | `freightnet_taiwan_customs_brokers` | `commercial_customs_broker_directory` | `TW` | `freightnet.com` | Commercial customs broker directory. |
| 44 | B | ACCEPT_REVIEW | `forwardingcompanies_taiwan_directory` | `commercial_freight_forwarder_directory` | `TW` | `forwardingcompanies.com` | Commercial Taiwan directory. |
| 45 | B | HOLD | `azfreight_taiwan_forwarders_directory` | `commercial_forwarder_crosscheck` | `TW` | `azfreight.com` | Cross-check. |
| 46 | B | HOLD | `azfreight_taiwan_directory` | `commercial_forwarder_crosscheck` | `TW` | `azfreight.com` | Cross-check. |
| 47 | B | HOLD | `jctrans_taiwan_directory` | `commercial_forwarder_directory` | `TW` | `jctrans.com` | Commercial/global; hold initially. |
| 48 | B_MINUS | ACCEPT_REVIEW | `cargoyellowpages_taiwan_directory` | `commercial_cargo_directory` | `TW` | `cargoyellowpages.com` | Commercial directory. |
| 49 | A_MINUS | HOLD | `cn_customs_english_root` | `official_customs_authority_reference` | `CN` | `english.customs.gov.cn` | Authority root. |
| 50 | A_MINUS | HOLD | `cn_customs_service_page` | `official_customs_service_reference` | `CN` | `english.customs.gov.cn` | Authority service context. |
| 51 | B_PLUS | ACCEPT_REVIEW | `shippingchina_nvocc_directory` | `commercial_nvocc_directory` | `CN` | `en.shippingchina.com` | NVOCC directory; review/probe required. |
| 52 | B_PLUS | ACCEPT_REVIEW | `shippingchina_company_directory` | `commercial_shipping_company_directory` | `CN` | `en.shippingchina.com` | Company directory page. |
| 53 | A_MINUS | HOLD | `shanghai_shipping_exchange_root` | `shipping_exchange_authority_reference` | `CN` | `en.sse.net.cn` | Authority/context. |
| 54 | A_MINUS | HOLD | `shanghai_shipping_exchange_contact` | `shipping_exchange_context` | `CN` | `en.sse.net.cn` | Context only. |
| 55 | B_PLUS | HOLD | `shanghai_ftz_services_context` | `free_zone_services_context` | `CN` | `en-shftz.pudong.gov.cn` | Free-zone context. |
| 56 | A_MINUS | HOLD | `china_a_level_logistics_enterprise_list_reference` | `authority_logistics_enterprise_reference` | `CN` | `hengyang.gov.cn` | A-level logistics enterprise reference. |
| 57 | B_PLUS | ACCEPT_REVIEW | `zhanjiang_cold_chain_member_directory` | `cold_chain_member_directory` | `CN` | `zjccla.com` | Cold-chain logistics association member list. |
| 58 | B_PLUS | ACCEPT_REVIEW | `asiafruit_logistica_china_cold_chain_exhibitors` | `trade_fair_exhibitor_directory` | `CN` | `asiafruitlogistica.com` | Cold-chain/fresh logistics exhibitor surface. |
| 59 | B | ACCEPT_REVIEW | `freightnet_china_forwarders_page_1` | `commercial_freight_forwarder_directory` | `CN` | `freightnet.com` | Commercial directory; low-depth. |
| 60 | B | ACCEPT_REVIEW | `freightnet_china_forwarders_page_53` | `commercial_freight_forwarder_directory_page` | `CN` | `freightnet.com` | Pagination seed; no aggressive crawl. |
| 61 | B | ACCEPT_REVIEW | `freightnet_china_forwarders_page_295` | `commercial_freight_forwarder_directory_page` | `CN` | `freightnet.com` | Pagination seed; no aggressive crawl. |
| 62 | B | ACCEPT_REVIEW | `freightnet_china_forwarders_page_299` | `commercial_freight_forwarder_directory_page` | `CN` | `freightnet.com` | Pagination seed; no aggressive crawl. |
| 63 | B | ACCEPT_REVIEW | `freightnet_china_logistics_companies` | `commercial_logistics_company_directory` | `CN` | `freightnet.com` | Commercial logistics directory. |
| 64 | B | ACCEPT_REVIEW | `freightnet_china_logistics_page_171` | `commercial_logistics_company_directory_page` | `CN` | `freightnet.com` | Pagination seed; no aggressive crawl. |
| 65 | B | ACCEPT_REVIEW | `freightnet_china_customs_brokers` | `commercial_customs_broker_directory` | `CN` | `freightnet.com` | Commercial customs brokers. |
| 66 | B | ACCEPT_REVIEW | `cargoyellowpages_china_directory_root` | `commercial_cargo_directory_root` | `CN` | `cargoyellowpages.com` | Commercial cargo directory. |
| 67 | B | ACCEPT_REVIEW | `cargoyellowpages_worldwide_directory` | `commercial_cargo_directory_root` | `GLOBAL` | `cargoyellowpages.com` | Worldwide index; use controlled. |
| 68 | B | ACCEPT_REVIEW | `cargoyellowpages_shanghai_city_directory` | `commercial_city_cargo_directory` | `CN` | `cargoyellowpages.com` | Shanghai city surface. |
| 69 | B | ACCEPT_REVIEW | `cargoyellowpages_ningbo_city_directory` | `commercial_city_cargo_directory` | `CN` | `cargoyellowpages.com` | Ningbo city surface. |
| 70 | B | ACCEPT_REVIEW | `cargoyellowpages_china_freight_agents_legacy` | `commercial_legacy_cargo_directory` | `CN` | `cargoyellowpages.com` | Legacy cargo agents surface. |
| 71 | B | ACCEPT_REVIEW | `jctrans_shanghai_directory` | `commercial_city_forwarder_directory` | `CN` | `jctrans.com` | Shanghai city surface. |
| 72 | B | HOLD | `jctrans_global_company_list` | `global_commercial_company_directory` | `GLOBAL` | `jctrans.com` | Global list; hold. |
| 73 | B | HOLD | `jctrans_group_list` | `global_commercial_group_directory` | `GLOBAL` | `jctrans.com` | Global group list; hold. |
| 74 | B | ACCEPT_REVIEW | `forwardingcompanies_shenzhen_directory` | `commercial_city_forwarder_directory` | `CN` | `forwardingcompanies.com` | Shenzhen city directory. |
| 75 | B | ACCEPT_REVIEW | `forwardingcompanies_shanghai_directory` | `commercial_city_forwarder_directory` | `CN` | `forwardingcompanies.com` | Shanghai city directory. |
| 76 | B_MINUS | HOLD | `schednet_asian_logistics_directory` | `regional_commercial_logistics_directory` | `CN,HK,TW,ASIA` | `schednet.com` | Regional commercial directory; hold. |
| 77 | B_MINUS | HOLD | `ddpchain_beijing_shipping_companies` | `low_trust_city_shipping_list` | `CN` | `ddpchain.com` | Low-trust city list. |
| 78 | B_MINUS | HOLD | `ddpchain_ningbo_shipping_companies` | `low_trust_city_shipping_list` | `CN` | `ddpchain.com` | Low-trust city list. |
| 79 | B | ACCEPT_REVIEW | `freightnet_hong_kong_forwarders` | `commercial_freight_forwarder_directory` | `HK` | `freightnet.com` | Commercial HK forwarder directory. |
| 80 | B | ACCEPT_REVIEW | `cargoyellowpages_hong_kong_directory` | `commercial_cargo_directory` | `HK` | `cargoyellowpages.com` | Commercial HK directory. |
| 81 | B | ACCEPT_REVIEW | `cargoyellowpages_hong_kong_legacy_1` | `commercial_cargo_directory` | `HK` | `cargoyellowpages.com` | Commercial HK legacy page. |
| 82 | B | ACCEPT_REVIEW | `cargoyellowpages_hong_kong_legacy_2` | `commercial_cargo_directory` | `HK` | `cargoyellowpages.com` | Commercial HK legacy page 2. |
| 83 | B | HOLD | `jctrans_hong_kong_china_directory` | `commercial_forwarder_directory` | `HK` | `jctrans.com` | Commercial/global; hold initially. |
| 84 | B_PLUS | ACCEPT_REVIEW | `hktdc_logistics_transportation_suppliers` | `commercial_b2b_logistics_supplier_directory` | `HK` | `sourcing.hktdc.com` | HKTDC supplier directory. |
| 85 | B_PLUS | ACCEPT_REVIEW | `hktdc_logistics_transportation_service_providers` | `commercial_b2b_logistics_service_directory` | `HK` | `sourcing.hktdc.com` | HKTDC service-provider directory. |
| 86 | B | ACCEPT_REVIEW | `hktdc_forwarder_service_search` | `commercial_b2b_service_search` | `HK` | `sourcing.hktdc.com` | Forwarder search surface. |
| 87 | B | ACCEPT_REVIEW | `hktdc_freight_forwarder_search` | `commercial_b2b_service_search` | `HK` | `sourcing.hktdc.com` | Freight forwarder search surface. |
| 88 | B | ACCEPT_REVIEW | `hktdc_logistic_service_search` | `commercial_b2b_service_search` | `HK` | `sourcing.hktdc.com` | Logistics search surface. |
| 89 | B | ACCEPT_REVIEW | `hktdc_logistics_transport_service_search` | `commercial_b2b_service_search` | `HK` | `sourcing.hktdc.com` | Logistics transport service search. |
| 90 | B | ACCEPT_REVIEW | `hktdc_international_freight_forwarding_search` | `commercial_b2b_supplier_search` | `HK` | `sourcing.hktdc.com` | International freight forwarding search. |
| 91 | B_PLUS | ACCEPT_REVIEW | `wiffa_member_verification_directory` | `freight_network_member_verification` | `CN,GLOBAL` | `wiffa.net` | WIFFA member verification. |
| 92 | B_PLUS | ACCEPT_REVIEW | `wiffa_english_root` | `freight_network_reference` | `CN,GLOBAL` | `wiffa.net` | Network root. |
| 93 | B | HOLD | `wiffa_meeting_directory` | `network_meeting_directory` | `CN,GLOBAL` | `wiffa.net` | Meeting directory; hold. |
| 94 | B_PLUS | HOLD | `wiffa_reference_network_list` | `network_crosscheck_reference` | `GLOBAL` | `gemslinks.com` | Cross-check reference. |
| 95 | A_MINUS | ACCEPT_REVIEW | `transport_logistic_shanghai_root` | `trade_fair_directory_root` | `CN` | `transportlogistic-china.com` | Trade fair root. |
| 96 | A_MINUS | ACCEPT_REVIEW | `transport_logistic_shanghai_exhibitor_directory` | `trade_fair_exhibitor_directory` | `CN` | `transportlogistic-china.com` | Official exhibitor directory. |
| 97 | A_MINUS | ACCEPT_REVIEW | `transport_logistic_shanghai_fulltext_exhibitors` | `trade_fair_fulltext_exhibitor_list` | `CN` | `transportlogistic.de` | Fulltext exhibitor list. |
| 98 | A_MINUS | ACCEPT_REVIEW | `transport_logistic_shanghai_brand_names` | `trade_fair_brand_directory` | `CN` | `transportlogistic.de` | Brand/exhibitor surface. |
| 99 | B_PLUS | ACCEPT_REVIEW | `cilf_shenzhen_root` | `trade_fair_directory_root` | `CN` | `scmfair.com` | CILF root. |
| 100 | B_PLUS | ACCEPT_REVIEW | `cilf_shenzhen_exhibitor_list` | `trade_fair_exhibitor_directory` | `CN` | `scmfair.com` | CILF exhibitor list. |
| 101 | B_PLUS | HOLD | `cisce_supply_chain_exhibitor_directory` | `broad_supply_chain_exhibitor_directory` | `CN` | `cisce.org.cn` | Broad supply-chain fair; hold. |
| 102 | B | HOLD | `transport_logistic_worldwide_reference` | `global_trade_fair_reference` | `GLOBAL` | `transportlogistic.de` | Worldwide reference. |
| 103 | B | HOLD | `transport_logistic_munich_reference` | `global_trade_fair_reference` | `GLOBAL` | `transportlogistic.de` | Munich reference only. |
| 104 | B_PLUS | ACCEPT_REVIEW | `let_china_logistics_exhibitor_pdf_context` | `trade_fair_pdf_context` | `CN` | `chinalet.cn` | LET China logistics fair PDF/context. |
| 105 | B_PLUS | HOLD | `ciie_exhibitors_logistics_context_pdf` | `broad_trade_fair_pdf_context` | `CN` | `ciie.org` | Broad CIIE context. |

## Seed-surface candidate list

| # | seed_surface_url | host |
|---:|---|---|
| 1 | <https://fiata.org/directory/cn/> | `fiata.org` |
| 2 | <https://fiata.org/directory/hk/> | `fiata.org` |
| 3 | <https://fiata.org/directory/tw/> | `fiata.org` |
| 4 | <https://zizhan.cifa-china.com/cn/member-query.html> | `zizhan.cifa-china.com` |
| 5 | <https://zizhan.cifa-china.com/en/cifa-intro.html> | `zizhan.cifa-china.com` |
| 6 | <https://zizhan.cifa-china.com/en/member-rights.html> | `zizhan.cifa-china.com` |
| 7 | <https://azfreight.com/association/cifa-china-international-freight-forwarders-association/> | `azfreight.com` |
| 8 | <https://forwardingcompanies.com/association/china-international-freight-forwarders-association-cifa-> | `forwardingcompanies.com` |
| 9 | <https://www.haffa.com.hk/en-HK/Membership/> | `www.haffa.com.hk` |
| 10 | <https://www.haffa.com.hk/en-HK/Membership/Profile.aspx> | `www.haffa.com.hk` |
| 11 | <https://www.haffa.com.hk/en-HK/Membership/Fiata/Introduction.aspx> | `www.haffa.com.hk` |
| 12 | <https://www.mardep.gov.hk/en/public-services/shipping-directory/index.html> | `www.mardep.gov.hk` |
| 13 | <https://www.mardep.gov.hk/en/public-services/shipping-directory/freiforw/index.html> | `www.mardep.gov.hk` |
| 14 | <https://www.mardep.gov.hk/en/public-services/shipping-directory/shipcomp/index.html> | `www.mardep.gov.hk` |
| 15 | <https://www.mardep.gov.hk/en/public-services/shipping-directory/locaship/index.html> | `www.mardep.gov.hk` |
| 16 | <https://www.mardep.gov.hk/en/public-services/shipping-directory/contfrei/index.html> | `www.mardep.gov.hk` |
| 17 | <https://www.mardep.gov.hk/filemanager/en/share/pub-services/pdf/sd.csv> | `www.mardep.gov.hk` |
| 18 | <https://www.hkmpdb.gov.hk/en/maritime-directory.php?cat=9> | `www.hkmpdb.gov.hk` |
| 19 | <https://www.hongkongmaritimehub.com/the-hub-3/the-hub-directory/> | `www.hongkongmaritimehub.com` |
| 20 | <https://www.hongkongmaritimehub.com/the-hub-3/the-hub-directory/directory-freight-forwarders-logistics/> | `www.hongkongmaritimehub.com` |
| 21 | <https://www.hongkongmaritimehub.com/the-hub-3/the-hub-directory/directory-trade-shipping-organisations/> | `www.hongkongmaritimehub.com` |
| 22 | <https://www.chamber.org.hk/en/membership/directory_detail.aspx?id=HKH0803&member_cate=> | `www.chamber.org.hk` |
| 23 | <https://www.aat.com.hk/en/yellow-pages/freight-forwarder-directory> | `www.aat.com.hk` |
| 24 | <https://www.aat.com.hk/en/yellow-pages/freight-forwarder-directory/c> | `www.aat.com.hk` |
| 25 | <https://www.aat.com.hk/en/yellow-pages/freight-forwarder-directory/d> | `www.aat.com.hk` |
| 26 | <https://www.aat.com.hk/en/yellow-pages/freight-forwarder-directory/j> | `www.aat.com.hk` |
| 27 | <https://www.aat.com.hk/en/yellow-pages/freight-forwarder-directory/s> | `www.aat.com.hk` |
| 28 | <https://www.aat.com.hk/zh-hant/yellow-pages/freight-forwarder-directory> | `www.aat.com.hk` |
| 29 | <https://www.iata.org/en/publications/directories/cargolink/> | `www.iata.org` |
| 30 | <https://www.iata.org/en/publications/directories/cargolink/directory/hong-kong-air-cargo-terminals-ltd/205/> | `www.iata.org` |
| 31 | <https://www.hactl.com/> | `www.hactl.com` |
| 32 | <https://www.customs.gov.hk/en/trade_facilitation/aeo/list/index.html> | `www.customs.gov.hk` |
| 33 | <https://data.gov.hk/en-data/dataset/hk-customs-ced_stat-aeo> | `data.gov.hk` |
| 34 | <https://data.gov.hk/en-data/dataset/hk-customs-ced_stat-aeo/resource/a2e4afa3-1ab5-4f47-b8cd-0d9215b5d9ad> | `data.gov.hk` |
| 35 | <https://www.customs.gov.hk/filemanager/common/pdf/aeo_dict_en.pdf> | `www.customs.gov.hk` |
| 36 | <https://aeo.wcoomd.org/search> | `aeo.wcoomd.org` |
| 37 | <https://data.gov.tw/en/datasets/8266> | `data.gov.tw` |
| 38 | <https://data.gov.tw/en/datasets/6704> | `data.gov.tw` |
| 39 | <https://data.gov.tw/en/datasets/8272> | `data.gov.tw` |
| 40 | <https://data.gov.tw/en/datasets/17077> | `data.gov.tw` |
| 41 | <https://aeo.customs.gov.tw/portal/aeop27?language=english> | `aeo.customs.gov.tw` |
| 42 | <https://web.customs.gov.tw/etaichung/singlehtml/ee1bc7abc2c84831b3de9951d2af42f0> | `web.customs.gov.tw` |
| 43 | <https://www.freightnet.com/directory/p1/cTW/s30.htm> | `www.freightnet.com` |
| 44 | <https://www.freightnet.com/directory/p1/cTW/s23.htm> | `www.freightnet.com` |
| 45 | <https://forwardingcompanies.com/in/taiwan-chinese-taipei> | `forwardingcompanies.com` |
| 46 | <https://azfreight.com/country-facility/freight-forwarders-in-taiwan/> | `azfreight.com` |
| 47 | <https://azfreight.com/freight-forwarder/taiwan/> | `azfreight.com` |
| 48 | <https://m.jctrans.com/en/company/listc/Taiwan-China/0-0> | `m.jctrans.com` |
| 49 | <https://www.cargoyellowpages.com/en/taiwan/> | `www.cargoyellowpages.com` |
| 50 | <https://english.customs.gov.cn/> | `english.customs.gov.cn` |
| 51 | <https://english.customs.gov.cn/service> | `english.customs.gov.cn` |
| 52 | <https://en.shippingchina.com/nvocc/index/index.html> | `en.shippingchina.com` |
| 53 | <https://en.shippingchina.com/companys/index/index/page/71.html> | `en.shippingchina.com` |
| 54 | <https://en.sse.net.cn/> | `en.sse.net.cn` |
| 55 | <https://en.sse.net.cn/brief/contactusen.jsp> | `en.sse.net.cn` |
| 56 | <https://en-shftz.pudong.gov.cn/investment/services/17.shtml> | `en-shftz.pudong.gov.cn` |
| 57 | <https://www.hengyang.gov.cn/fgw/xxgk/tzgg/20200118/i343950.html> | `www.hengyang.gov.cn` |
| 58 | <https://www.zjccla.com/page122?article_id=58> | `www.zjccla.com` |
| 59 | <https://www.asiafruitlogistica.com/zh-hans/catalogue/> | `www.asiafruitlogistica.com` |
| 60 | <https://www.freightnet.com/directory/p1/cCN/s30.htm> | `www.freightnet.com` |
| 61 | <https://www.freightnet.com/directory/p53/cCN/s30.htm> | `www.freightnet.com` |
| 62 | <https://www.freightnet.com/directory/p295/cCN/s30.htm> | `www.freightnet.com` |
| 63 | <https://www.freightnet.com/directory/p299/cCN/s30.htm> | `www.freightnet.com` |
| 64 | <https://www.freightnet.com/directory/p240/cCN/s99.htm> | `www.freightnet.com` |
| 65 | <https://www.freightnet.com/directory/p171/cCN/s99.htm> | `www.freightnet.com` |
| 66 | <https://www.freightnet.com/directory/p1/cCN/s23.htm> | `www.freightnet.com` |
| 67 | <https://www.cargoyellowpages.com/en/china/> | `www.cargoyellowpages.com` |
| 68 | <https://www.cargoyellowpages.com/en/directory.html> | `www.cargoyellowpages.com` |
| 69 | <https://mobile.cargoyellowpages.com/china/shanghai.html> | `mobile.cargoyellowpages.com` |
| 70 | <https://mobile.cargoyellowpages.com/china/ningbo.html> | `mobile.cargoyellowpages.com` |
| 71 | <https://paginasamarillasdelacarga.cargoyellowpages.com/china3_freight_forwarders_cargo_agents.html> | `paginasamarillasdelacarga.cargoyellowpages.com` |
| 72 | <https://m.jctrans.com/en/company/listc/China_Shanghai/0-0> | `m.jctrans.com` |
| 73 | <https://www.jctrans.com/en/company/list> | `www.jctrans.com` |
| 74 | <https://m.jctrans.com/en/company/list/0-GRP> | `m.jctrans.com` |
| 75 | <https://forwardingcompanies.com/in/shenzhen> | `forwardingcompanies.com` |
| 76 | <https://forwardingcompanies.com/in/shanghai> | `forwardingcompanies.com` |
| 77 | <https://www.schednet.com/asiainfo/asiainfo.asp> | `www.schednet.com` |
| 78 | <https://ddpchain.com/shipping-companies-in-beijing/> | `ddpchain.com` |
| 79 | <https://ddpchain.com/shipping-companies-in-ningbo/> | `ddpchain.com` |
| 80 | <https://www.freightnet.com/directory/p1/cHK/s30.htm> | `www.freightnet.com` |
| 81 | <https://www.cargoyellowpages.com/hong_kong_QT_freight_forwarders_cargo_agents.html> | `www.cargoyellowpages.com` |
| 82 | <https://www.cargoyellowpages.com/hong_kong_freight_forwarders_cargo_agents.html> | `www.cargoyellowpages.com` |
| 83 | <https://www.cargoyellowpages.com/hong_kong2_freight_forwarders_cargo_agents.html> | `www.cargoyellowpages.com` |
| 84 | <https://m.jctrans.com/en/membership/listc/HongKong-China/0-0?years=0> | `m.jctrans.com` |
| 85 | <https://sourcing.hktdc.com/en/Suppliers/Logistics-Transportation-0884688ce3a111ea883f06c82c63b760/1> | `sourcing.hktdc.com` |
| 86 | <https://sourcing.hktdc.com/en/Service-Provider/Logistics-Transportation-0884688ce3a111ea883f06c82c63b760/1> | `sourcing.hktdc.com` |
| 87 | <https://sourcing.hktdc.com/en/Service-Search/forwarder/1> | `sourcing.hktdc.com` |
| 88 | <https://sourcing.hktdc.com/en/Service-Search/freight%20forwaders/1> | `sourcing.hktdc.com` |
| 89 | <https://sourcing.hktdc.com/en/Service-Search/logistic/1> | `sourcing.hktdc.com` |
| 90 | <https://sourcing.hktdc.com/en/Service-Search/logistics%20%26%20transport%20service/1?catId=f45d19e4e3a011ea883f06c82c63b760> | `sourcing.hktdc.com` |
| 91 | <https://sourcing.hktdc.com/en/Supplier-Search/International%20Freight%20Forwarding/1> | `sourcing.hktdc.com` |
| 92 | <https://en.wiffa.net/memberverificationlist.html> | `en.wiffa.net` |
| 93 | <https://en.wiffa.net/> | `en.wiffa.net` |
| 94 | <https://www.wiffa.net/meeting2021/pren/directory?stype=3> | `www.wiffa.net` |
| 95 | <https://gemslinks.com/en/knowledge/freight-forwarder-network-reference/> | `gemslinks.com` |
| 96 | <https://www.transportlogistic-china.com/> | `www.transportlogistic-china.com` |
| 97 | <https://www.transportlogistic-china.com/exhibitor-directory> | `www.transportlogistic-china.com` |
| 98 | <https://exhibitors.transportlogistic.de/en/exhibitors-and-directories/exhibitors-brand-names-search/exhibitorFulltextlist/Exhibitors/All/?cHash=0c747bdc6b2e6fb10d7f7055d878a0c5> | `exhibitors.transportlogistic.de` |
| 99 | <https://exhibitors.transportlogistic.de/en/exhibitors-and-directories/exhibitors-brand-names> | `exhibitors.transportlogistic.de` |
| 100 | <https://www.scmfair.com/en/> | `www.scmfair.com` |
| 101 | <https://www.scmfair.com/en/h-col-154.html> | `www.scmfair.com` |
| 102 | <https://en.cisce.org.cn/overview/exhibitors.html> | `en.cisce.org.cn` |
| 103 | <https://transportlogistic.de/en/transport-logistic-worldwide/> | `transportlogistic.de` |
| 104 | <https://transportlogistic.de/en/trade-fair/exhibitor-directory/> | `transportlogistic.de` |
| 105 | <https://www.chinalet.cn/gw/sctu/202506250917201596.pdf> | `www.chinalet.cn` |
| 106 | <https://www.ciie.org/resource/upload/zbh/201910/22200146h725.pdf> | `www.ciie.org` |

## Catalog patch guidance for later gates

R149/R150 catalog work should not blindly promote all candidate surfaces as active runtime seeds. The first Chinese catalog may include a broad candidate manifest, but all entries must remain disabled and require live checks.

Recommended initial catalog guardrails:

- initial_catalog_source_family_target=45-60
- initial_catalog_seed_surface_target=85-110
- include broad candidate evidence, but keep risky pages as HOLD
- keep commercial/global/network/fair sources under ACCEPT_REVIEW or HOLD
- keep official/association/direct directory sources as ACCEPT or ACCEPT_REVIEW
- keep FIATA country/region pages grouped under shared FIATA modeling, not split into language codes

## Next gates

1. `SOURCE_SEED_R149_CHINESE_DECISION_DOC_AUDIT_READONLY`
2. `SOURCE_SEED_R150_CHINESE_DECISION_DOC_COMMIT_PUSH_GATE`
3. `SOURCE_SEED_R151_CHINESE_DECISION_DOC_POST_PUSH_SEAL_READONLY`
4. `SOURCE_SEED_R152_CHINESE_CATALOG_MANIFEST_PATCH_PLAN_READONLY`
