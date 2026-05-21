# Hebrew source-seed URLs decision

- Language code: `he`
- Language name: Hebrew
- Native name: עברית
- Canonical base HEAD: `7e0d632166e96097a7ce7b9d1f56268e2f8cfad5`
- Taxonomy: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_hebrew_he.json`
- Taxonomy SHA: `15cfd433e3708c280e284163a06c204e8cf2ab8d041b5f05887a63ed4145b50b`
- Catalog target: `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json`
- Candidate status: candidate-only, not live
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Public URL probe: not run
- DB/frontier/crawler/systemd mutation: not run
- Source priority: directory sites first, then associations, officials, networks, marketplaces
- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Unique seed URLs: 90

## Candidate source families

| # | source_family_code | Quality | Decision | Source | Seed 1 | Seed 2 | Notes |
|---:|---|---|---|---|---|---|---|
| 1 | `he_01_fiata_israel_member_directory` | A_PLUS | ACCEPT | [Source family link](https://fiata.org/) | [Seed 1](https://fiata.org/directory/il/) | [Seed 2](https://fiata.org/directory/) | english_fallback; country_primary; not probed |
| 2 | `he_02_iffcca_federation_directory_surface` | A_PLUS | ACCEPT | [Source family link](https://azfreight.com/) | [Seed 1](https://azfreight.com/association/iffcca-israeli-fed-of-freight-forwarders-customs-clearing-agents/) | [Seed 2](https://forwardingcompanies.com/association/the-israeli-federation-of-forwarders-and-customs-clearing-agents-iffcca-) | english_fallback; country_primary; not probed |
| 3 | `he_03_forwardingcompanies_israel` | A_PLUS | ACCEPT | [Source family link](https://forwardingcompanies.com/) | [Seed 1](https://forwardingcompanies.com/in/israel) | [Seed 2](https://forwardingcompanies.com/countries) | english_fallback; country_primary; not probed |
| 4 | `he_04_freightnet_israel_freight_forwarders` | A | ACCEPT | [Source family link](https://www.freightnet.com/) | [Seed 1](https://www.freightnet.com/directory/p1/cIL/s30.htm) | [Seed 2](https://www.freightnet.com/directory/p7/cIL/s30.htm) | english_fallback; country_primary; not probed |
| 5 | `he_05_freightnet_israel_logistics_categories` | A | ACCEPT | [Source family link](https://www.freightnet.com/) | [Seed 1](https://www.freightnet.com/directory/p1/cIL/s99.htm) | [Seed 2](https://www.freightnet.com/directory/p1/cIL/s31.htm) | english_fallback; country_primary; not probed |
| 6 | `he_06_cargoyellowpages_israel` | A | ACCEPT | [Source family link](https://www.cargoyellowpages.com/) | [Seed 1](https://www.cargoyellowpages.com/israel_freight_forwarders_cargo_agents.html) | [Seed 2](https://mobile.cargoyellowpages.com/israel.html) | english_fallback; country_primary; not probed |
| 7 | `he_07_cargoyellowpages_israel_city_surfaces` | A | ACCEPT | [Source family link](https://mobile.cargoyellowpages.com/) | [Seed 1](https://mobile.cargoyellowpages.com/israel/ashdod.html) | [Seed 2](https://mobile.cargoyellowpages.com/israel/haifa.html) | english_fallback; country_primary; not probed |
| 8 | `he_08_azfreight_israel` | A | ACCEPT | [Source family link](https://azfreight.com/) | [Seed 1](https://azfreight.com/country-facility/freight-forwarders-in-israel/) | [Seed 2](https://azfreight.com/directory/) | english_fallback; country_primary; not probed |
| 9 | `he_09_azfreight_directory_search` | A | ACCEPT | [Source family link](https://azfreight.com/) | [Seed 1](https://azfreight.com/) | [Seed 2](https://azfreight.com/countries/) | english_fallback; country_primary; not probed |
| 10 | `he_10_b144_hebrew_international_courier_shipping` | A | ACCEPT | [Source family link](https://www.b144.co.il/) | [Seed 1](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/) | [Seed 2](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%90%D7%96%D7%95%D7%A8-%D7%90%D7%A9%D7%93%D7%95%D7%93-%D7%95%D7%94%D7%A1%D7%91%D7%99%D7%91%D7%94/) | native; country_primary; not probed |
| 11 | `he_11_b144_hebrew_city_pages` | A | ACCEPT | [Source family link](https://www.b144.co.il/) | [Seed 1](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%A4%D7%AA%D7%97-%D7%AA%D7%A7%D7%95%D7%95%D7%94/) | [Seed 2](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%97%D7%99%D7%A4%D7%94/) | native; country_primary; not probed |
| 12 | `he_12_b144_central_israel_surfaces` | A | ACCEPT | [Source family link](https://www.b144.co.il/) | [Seed 1](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%9C%D7%95%D7%93/) | [Seed 2](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%99%D7%A8%D7%95%D7%A9%D7%9C%D7%99%D7%9D/) | native; country_primary; not probed |
| 13 | `he_13_d_co_il_hebrew_international_shipping` | A | ACCEPT | [Source family link](https://www.d.co.il/) | [Seed 1](https://www.d.co.il/h-c32640-e0-p0-l0/) | [Seed 2](https://www.d.co.il/ArticleLoby-c32640/) | native; country_primary; not probed |
| 14 | `he_14_d_co_il_hebrew_region_pages` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.d.co.il/) | [Seed 1](https://www.d.co.il/h-c32640-e3-p0-l0/) | [Seed 2](https://www.d.co.il/h-c32640-e2-p0-l0-t19420.na1/) | native; country_primary; not probed |
| 15 | `he_15_d_co_il_hebrew_customs_shipping_filters` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.d.co.il/) | [Seed 1](https://www.d.co.il/h-c32640-e0-p0-l0-city7900-t40061830.nb1/) | [Seed 2](https://www.d.co.il/h-c32640-e0-p0-l0-t40061844.na1/) | native; country_primary; not probed |
| 16 | `he_16_d_co_il_hebrew_route_service_filters` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.d.co.il/) | [Seed 1](https://www.d.co.il/h-c32640-e3-p0-l0-t40061723.na1/) | [Seed 2](https://www.d.co.il/h-c32640-e7-p0-l0/recommended/) | native; country_primary; not probed |
| 17 | `he_17_searates_israel_logistics_reference` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.searates.com/) | [Seed 1](https://www.searates.com/reference/logistics-service/israel/) | [Seed 2](https://www.searates.com/reference/) | english_fallback; country_primary; not probed |
| 18 | `he_18_duns100_israel_logistics_rankings` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.duns100.co.il/) | [Seed 1](https://www.duns100.co.il/en/rating/Service_%26_Trade/Logistics_Services) | [Seed 2](https://www.duns100.co.il/en/rating/Transportation_%26_Vehicles/Transportation_Services) | native; country_primary; not probed |
| 19 | `he_19_duns100_archive_category_surfaces` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.duns100.co.il/) | [Seed 1](https://www.duns100.co.il/en/rating/Service_%26_Trade/Logistics_Services/2023) | [Seed 2](https://www.duns100.co.il/en/rating/Service_%26_Trade/Largest_Services_Companies/2020) | native; country_primary; not probed |
| 20 | `he_20_dun_bradstreet_israel_business_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.dnb.com/) | [Seed 1](https://www.dnb.com/business-directory/company-information.transportation_and_warehousing.il.html) | [Seed 2](https://www.dnb.com/business-directory.html) | english_fallback; country_primary; not probed |
| 21 | `he_21_goodfirms_israel_logistics` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.goodfirms.co/) | [Seed 1](https://www.goodfirms.co/supply-chain-logistics-companies/israel) | [Seed 2](https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/israel) | english_fallback; country_primary; not probed |
| 22 | `he_22_ensun_israel_logistics_search` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://ensun.io/) | [Seed 1](https://ensun.io/search/freight-forwarding/israel) | [Seed 2](https://ensun.io/search/project-logistics/israel) | english_fallback; country_primary; not probed |
| 23 | `he_23_opca_israel_forwarding_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://overseasprojectcargo.com/) | [Seed 1](https://overseasprojectcargo.com/InternationalFreightForwarders/israel-freight-forwarders/) | [Seed 2](https://overseasprojectcargo.com/InternationalFreightForwarders/) | english_fallback; country_primary; not probed |
| 24 | `he_24_ruzave_israel_logistics_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://ruzave.com/) | [Seed 1](https://ruzave.com/israel/ashdod-sea-port-israel-2/freight-forwarders/freight-forwardingservices/) | [Seed 2](https://ruzave.com/israel/iksal/maritime/organization-association/) | english_fallback; country_primary; not probed |
| 25 | `he_25_iata_cargolink_directory_israel_discovery` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.iata.org/) | [Seed 1](https://www.iata.org/en/publications/directories/cargolink/directory/) | [Seed 2](https://www.iata.org/en/publications/directories/cargolink/) | english_fallback; country_primary; not probed |
| 26 | `he_26_wcaworld_global_directory_israel_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.wcaworld.com/) | [Seed 1](https://www.wcaworld.com/directory) | [Seed 2](https://www.wcaworld.com/) | english_fallback; country_primary; not probed |
| 27 | `he_27_freight_midpoint_member_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://freightmidpoint.com/) | [Seed 1](https://freightmidpoint.com/Directory/) | [Seed 2](https://freightmidpoint.com/) | english_fallback; country_primary; not probed |
| 28 | `he_28_loglink_israel_logistics_search` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://loglink.com/) | [Seed 1](https://loglink.com/search.asp?m=all&query=Israel&sm=cou&ss=ns) | [Seed 2](https://loglink.com/) | english_fallback; country_primary; not probed |
| 29 | `he_29_shipping_data_israel_business_search` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://shipping-data.com/) | [Seed 1](https://shipping-data.com/business/israel) | [Seed 2](https://shipping-data.com/business/israel/tel-aviv/israeli-federation-freight-forwarders-customs-clearing-agents) | english_fallback; country_primary; not probed |
| 30 | `he_30_kompass_israel_transportation_logistics` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://il.kompass.com/) | [Seed 1](https://il.kompass.com/) | [Seed 2](https://il.kompass.com/a/transport-logistics/80/) | english_fallback; country_primary; not probed |
| 31 | `he_31_europages_israel_logistics_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.europages.co.uk/) | [Seed 1](https://www.europages.co.uk/companies/israel.html) | [Seed 2](https://www.europages.co.uk/companies/israel/transport%20and%20logistics.html) | english_fallback; country_primary; not probed |
| 32 | `he_32_yellow_pages_israel_dapei_zahav_category` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.d.co.il/) | [Seed 1](https://www.d.co.il/) | [Seed 2](https://www.d.co.il/Cat/?i=32640) | native; country_primary; not probed |
| 33 | `he_33_b144_israel_broad_category_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.b144.co.il/) | [Seed 1](https://www.b144.co.il/%D7%91%D7%9C%D7%93%D7%A8%D7%95%D7%AA-%D7%95%D7%A9%D7%99%D7%9C%D7%95%D7%97-%D7%91%D7%99%D7%A0%D7%9C%D7%90%D7%95%D7%9E%D7%99/%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/) | [Seed 2](https://www.b144.co.il/) | native; country_primary; not probed |
| 34 | `he_34_israel_government_customs_audience` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.gov.il/) | [Seed 1](https://www.gov.il/en/departments/targetaudience/taxes-audience-international-freight-forwarder/govil-landing-page) | [Seed 2](https://www.gov.il/en/departments/israel_tax_authority/govil-landing-page) | native; country_primary; not probed |
| 35 | `he_35_chamber_federation_umbrella_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.chamber.org.il/) | [Seed 1](https://www.chamber.org.il/) | [Seed 2](https://www.chamber.org.il/en/) | native; country_primary; not probed |
| 36 | `he_36_opencorporates_israel_logistics_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://opencorporates.com/) | [Seed 1](https://opencorporates.com/companies/il) | [Seed 2](https://opencorporates.com/companies?q=logistics+israel) | english_fallback; country_primary; not probed |
| 37 | `he_37_dunguide_israel_business_discovery` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.duns100.co.il/) | [Seed 1](https://www.duns100.co.il/en/rating) | [Seed 2](https://www.duns100.co.il/en/rating/Service_%26_Trade) | native; country_primary; not probed |
| 38 | `he_38_freightbook_network_directory` | B | HOLD_REVIEW | [Source family link](https://www.freightbook.net/) | [Seed 1](https://www.freightbook.net/directory/) | [Seed 2](https://www.freightbook.net/) | english_fallback; country_primary; not probed |
| 39 | `he_39_jctrans_network_directory` | B | HOLD_REVIEW | [Source family link](https://www.jctrans.com/) | [Seed 1](https://www.jctrans.com/en/membership/directory.html) | [Seed 2](https://www.jctrans.com/) | english_fallback; country_primary; not probed |
| 40 | `he_40_global_logistics_network_directory` | B | HOLD_REVIEW | [Source family link](https://www.go2gln.com/) | [Seed 1](https://www.go2gln.com/members-directory/) | [Seed 2](https://www.go2gln.com/) | english_fallback; country_primary; not probed |
| 41 | `he_41_cargopedia_israel_transport_directory` | B | HOLD_REVIEW | [Source family link](https://www.cargopedia.net/) | [Seed 1](https://www.cargopedia.net/europe/israel-transport-companies) | [Seed 2](https://www.cargopedia.net/) | english_fallback; country_primary; not probed |
| 42 | `he_42_freightquote_freight_resources_discovery` | B | HOLD_REVIEW | [Source family link](https://www.freightquote.com/) | [Seed 1](https://www.freightquote.com/) | [Seed 2](https://www.freightquote.com/freight-shipping/) | english_fallback; country_primary; not probed |
| 43 | `he_43_logistics_list_israel_discovery` | B | HOLD_REVIEW | [Source family link](https://www.logisticslist.com/) | [Seed 1](https://www.logisticslist.com/) | [Seed 2](https://www.logisticslist.com/search) | english_fallback; country_primary; not probed |
| 44 | `he_44_cybo_israel_logistics_category_discovery` | B | HOLD_REVIEW | [Source family link](https://www.cybo.com/) | [Seed 1](https://www.cybo.com/IL/) | [Seed 2](https://www.cybo.com/IL-biz/logistics/) | english_fallback; country_primary; not probed |
| 45 | `he_45_yalwa_israel_transport_logistics_discovery` | B | HOLD_REVIEW | [Source family link](https://www.yalwa.co.il/) | [Seed 1](https://www.yalwa.co.il/) | [Seed 2](https://www.yalwa.co.il/Transportation-Logistics/801/) | native; country_primary; not probed |

## Quality distribution

```json
{"A": 10, "A_MINUS": 12, "A_PLUS": 3, "B": 8, "B_PLUS": 12}
```

## Decision distribution

```json
{"ACCEPT": 13, "ACCEPT_REVIEW": 24, "HOLD_REVIEW": 8}
```

