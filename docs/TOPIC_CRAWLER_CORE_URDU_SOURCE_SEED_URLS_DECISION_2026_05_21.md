# Urdu source-seed URLs decision

- Language code: `ur`
- Language name: Urdu
- Native name: اردو
- Canonical base HEAD: `62799a43688344a5a6b799088268e92dd8169160`
- Taxonomy: `makpi51crawler/taxonomy/languages/logisticsearch_taxonomy_urdu_ur.json`
- Taxonomy SHA: `b96cec8f9d426d01ba7f74f6f951b4030a5e31795cdf72e14cd368291cf12650`
- Catalog target: `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json`
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
| 1 | `urdupoint_pk_transport_logistics` | A | ACCEPT | [Source family link](https://www.urdupoint.com/) | [Seed 1](https://www.urdupoint.com/business/directory/54/transport-logistics.html) | [Seed 2](https://www.urdupoint.com/business/directory/1097/freight-forwarders-packers.html) | native; country_primary; not probed |
| 2 | `urdupoint_pk_city_freight_karachi_lahore` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.urdupoint.com/) | [Seed 1](https://www.urdupoint.com/business/directory/karachi/1097/freight-forwarders-packers.html) | [Seed 2](https://www.urdupoint.com/business/directory/lahore/1097/freight-forwarders-packers.html) | native; country_primary; not probed |
| 3 | `urdupoint_pk_city_freight_islamabad_rawalpindi` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.urdupoint.com/) | [Seed 1](https://www.urdupoint.com/business/directory/islamabad/1097/freight-forwarders-packers.html) | [Seed 2](https://www.urdupoint.com/business/directory/rawalpindi/1097/freight-forwarders-packers.html) | native; country_primary; not probed |
| 4 | `hamariweb_pk_freight_forwarders` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://hamariweb.com/) | [Seed 1](https://hamariweb.com/finance/directory/freight_forwarders_cid66.aspx) | [Seed 2](https://hamariweb.com/finance/directory/) | native; country_primary; not probed |
| 5 | `fiata_pk_members_directory` | A_PLUS | ACCEPT | [Source family link](https://fiata.org/) | [Seed 1](https://fiata.org/directory/) | [Seed 2](https://fiata.org/directory/pk/) | english_fallback; country_primary; not probed |
| 6 | `piffa_pk_official_members` | A_PLUS | ACCEPT | [Source family link](https://www.piffapk.com/) | [Seed 1](https://www.piffapk.com/) | [Seed 2](https://www.piffapk.com/members.php) | english_fallback; country_primary; not probed |
| 7 | `freightnet_pk_freight_forwarders` | A | ACCEPT | [Source family link](https://www.freightnet.com/) | [Seed 1](https://www.freightnet.com/directory/p1/cPK/s30.htm) | [Seed 2](https://www.freightnet.com/directory/p76/cPK/s30.htm) | english_fallback; country_primary; not probed |
| 8 | `freightnet_pk_logistics_companies` | A | ACCEPT | [Source family link](https://www.freightnet.com/) | [Seed 1](https://www.freightnet.com/directory/p1/cPK/s99.htm) | [Seed 2](https://www.freightnet.com/directory/) | english_fallback; country_primary; not probed |
| 9 | `forwardingcompanies_pk_directory` | A | ACCEPT_REVIEW | [Source family link](https://forwardingcompanies.com/) | [Seed 1](https://forwardingcompanies.com/in/pakistan) | [Seed 2](https://forwardingcompanies.com/in/pakistan/karachi) | english_fallback; country_primary; not probed |
| 10 | `azfreight_pk_freight_forwarders` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://azfreight.com/) | [Seed 1](https://azfreight.com/country-facility/freight-forwarders-in-pakistan/) | [Seed 2](https://azfreight.com/freight-forwarder/freight-forwarders-company-pakistan/) | english_fallback; country_primary; not probed |
| 11 | `cargoyellowpages_pk_directory` | A | ACCEPT | [Source family link](https://www.cargoyellowpages.com/) | [Seed 1](https://www.cargoyellowpages.com/en/pakistan/) | [Seed 2](https://www.cargoyellowpages.com/pakistan_freight_forwarders_cargo_agents.html) | english_fallback; country_primary; not probed |
| 12 | `cargoyellowpages_pk_karachi_profiles` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.cargoyellowpages.com/) | [Seed 1](https://www.cargoyellowpages.com/en/pakistan/karachi/freight-forwarders-fracht-pakistan-19519.html) | [Seed 2](https://www.cargoyellowpages.com/en/pakistan/karachi/freight-forwarders-cargo-xperts-19665.html) | english_fallback; country_primary; not probed |
| 13 | `cargoyellowpages_pk_mobile_profiles` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://mobile.cargoyellowpages.com/) | [Seed 1](https://mobile.cargoyellowpages.com/company/40619/sendmail/80350) | [Seed 2](https://mobile.cargoyellowpages.com/company/30660/sendmail/82685) | english_fallback; country_primary; not probed |
| 14 | `freightpages_pk_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.freightpages.org/) | [Seed 1](https://www.freightpages.org/) | [Seed 2](https://www.freightpages.org/companies/page/35/?service=general-cargo-freight-forwarding) | english_fallback; country_primary; not probed |
| 15 | `freightpages_pk_company_profiles` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.freightpages.org/) | [Seed 1](https://www.freightpages.org/company/accurate-services-pakistan/) | [Seed 2](https://www.freightpages.org/company/quick-freight-management-pakistan/) | english_fallback; country_primary; not probed |
| 16 | `freightpages_pk_more_profiles` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.freightpages.org/) | [Seed 1](https://www.freightpages.org/company/specialized-freight-forwarders/) | [Seed 2](https://www.freightpages.org/company/zeeyoon-shipping-services/) | english_fallback; country_primary; not probed |
| 17 | `jctrans_pk_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://m.jctrans.com/) | [Seed 1](https://m.jctrans.com/en/company/listc/Pakistan/0-0/) | [Seed 2](https://m.jctrans.com/en/company/listc/Pakistan_Karachi/0-0) | english_fallback; country_primary; not probed |
| 18 | `iata_cargolink_pk_supplier_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.iata.org/) | [Seed 1](https://www.iata.org/en/publications/directories/cargolink/directory/) | [Seed 2](https://www.iata.org/en/publications/directories/) | english_fallback; country_primary; not probed |
| 19 | `wcaworld_pk_member_directory` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.wcaworld.com/) | [Seed 1](https://www.wcaworld.com/Directory) | [Seed 2](https://www.wcaworld.com/Directory/Search) | english_fallback; country_primary; not probed |
| 20 | `pangea_network_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.pangea-network.com/) | [Seed 1](https://www.pangea-network.com/) | [Seed 2](https://www.pangea-network.com/members/) | english_fallback; country_primary; not probed |
| 21 | `df_alliance_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.df-alliance.com/) | [Seed 1](https://www.df-alliance.com/) | [Seed 2](https://www.df-alliance.com/members) | english_fallback; country_primary; not probed |
| 22 | `security_cargo_network_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.securitycargonetwork.com/) | [Seed 1](https://www.securitycargonetwork.com/) | [Seed 2](https://www.securitycargonetwork.com/members) | english_fallback; country_primary; not probed |
| 23 | `aeroceanetwork_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://aeroceanetwork.net/) | [Seed 1](https://aeroceanetwork.net/) | [Seed 2](https://aeroceanetwork.net/members/) | english_fallback; country_primary; not probed |
| 24 | `project_cargo_network_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://projectcargonetwork.com/) | [Seed 1](https://projectcargonetwork.com/members/) | [Seed 2](https://projectcargonetwork.com/) | english_fallback; country_primary; not probed |
| 25 | `overseas_project_cargo_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://overseasprojectcargo.com/) | [Seed 1](https://overseasprojectcargo.com/Directory/) | [Seed 2](https://overseasprojectcargo.com/) | english_fallback; country_primary; not probed |
| 26 | `freight_forwarders_family_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://freightforwardersfamily.com/) | [Seed 1](https://freightforwardersfamily.com/Directory/) | [Seed 2](https://freightforwardersfamily.com/) | english_fallback; country_primary; not probed |
| 27 | `freight_midpoint_pk_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://freightmidpoint.com/) | [Seed 1](https://freightmidpoint.com/Directory/) | [Seed 2](https://freightmidpoint.com/) | english_fallback; country_primary; not probed |
| 28 | `ruzave_pk_freight_forwarders` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://ruzave.com/) | [Seed 1](https://ruzave.com/pakistan/freight-forwarders/) | [Seed 2](https://ruzave.com/pakistan/freight-forwarders/perishable-freight-forwarders/) | english_fallback; country_primary; not probed |
| 29 | `ruzave_pk_shipping_logistics` | B | ACCEPT_REVIEW | [Source family link](https://ruzave.com/) | [Seed 1](https://ruzave.com/pakistan/shipping-agents/) | [Seed 2](https://ruzave.com/pakistan/customs-brokers/) | english_fallback; country_primary; not probed |
| 30 | `cpecb_pk_trusted_logistics_directory` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.cpecb.com/) | [Seed 1](https://www.cpecb.com/trusted-companies-verified-companies-partners-directory/) | [Seed 2](https://www.cpecb.com/) | english_fallback; country_primary; not probed |
| 31 | `goodfirms_pk_logistics_directory` | B | HOLD_REVIEW | [Source family link](https://www.goodfirms.co/) | [Seed 1](https://www.goodfirms.co/supply-chain-logistics-companies/pakistan) | [Seed 2](https://www.goodfirms.co/supply-chain-logistics-companies) | english_fallback; country_primary; not probed |
| 32 | `clutch_pk_logistics_directory` | B | HOLD_REVIEW | [Source family link](https://clutch.co/) | [Seed 1](https://clutch.co/pk/logistics) | [Seed 2](https://clutch.co/pk) | english_fallback; country_primary; not probed |
| 33 | `businesslist_pk_logistics_directory` | B | HOLD_REVIEW | [Source family link](https://www.businesslist.pk/) | [Seed 1](https://www.businesslist.pk/category/logistics) | [Seed 2](https://www.businesslist.pk/category/transport) | english_fallback; country_primary; not probed |
| 34 | `lookup_pk_logistics_directory` | B | HOLD_REVIEW | [Source family link](https://www.lookup.pk/) | [Seed 1](https://www.lookup.pk/search.php?what=Logistics&where=Pakistan) | [Seed 2](https://www.lookup.pk/search.php?what=Freight+Forwarding&where=Pakistan) | english_fallback; country_primary; not probed |
| 35 | `pakbiz_pk_logistics_directory` | B | HOLD_REVIEW | [Source family link](https://www.pakbiz.com/) | [Seed 1](https://www.pakbiz.com/profile/Freight-Forwarders/) | [Seed 2](https://www.pakbiz.com/profile/Transport-Logistics/) | english_fallback; country_primary; not probed |
| 36 | `d2dlogistics_pk_company_list` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://d2dlogistics.net/) | [Seed 1](https://d2dlogistics.net/list-of-logistics-companies/) | [Seed 2](https://d2dlogistics.net/) | english_fallback; country_primary; not probed |
| 37 | `gac_pk_freight_services` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.gac.com/) | [Seed 1](https://www.gac.com/pakistan/logistics/freight-services) | [Seed 2](https://www.gac.com/pakistan/logistics) | english_fallback; country_primary; not probed |
| 38 | `nlc_pk_official_logistics` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://nlc.com.pk/) | [Seed 1](https://nlc.com.pk/) | [Seed 2](https://nlc.com.pk/services/) | english_fallback; country_primary; not probed |
| 39 | `pakistan_single_window_trade_logistics` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.psw.gov.pk/) | [Seed 1](https://www.psw.gov.pk/) | [Seed 2](https://www.psw.gov.pk/services) | english_fallback; country_primary; not probed |
| 40 | `pakistan_customs_trade_logistics` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.customs.gov.pk/) | [Seed 1](https://www.customs.gov.pk/) | [Seed 2](https://weboc.gov.pk/) | english_fallback; country_primary; not probed |
| 41 | `karachi_port_trust_cargo_gateway` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://kpt.gov.pk/) | [Seed 1](https://kpt.gov.pk/) | [Seed 2](https://kpt.gov.pk/pages/operations) | english_fallback; country_primary; not probed |
| 42 | `port_qasim_authority_cargo_gateway` | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.pqa.gov.pk/) | [Seed 1](https://www.pqa.gov.pk/) | [Seed 2](https://www.pqa.gov.pk/en/port-operations) | english_fallback; country_primary; not probed |
| 43 | `gwadar_port_authority_cargo_gateway` | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.gwadarport.gov.pk/) | [Seed 1](https://www.gwadarport.gov.pk/) | [Seed 2](https://www.gwadarport.gov.pk/port-operations) | english_fallback; country_primary; not probed |
| 44 | `pakistan_railways_freight_gateway` | B_PLUS | HOLD_REVIEW | [Source family link](https://www.pakrail.gov.pk/) | [Seed 1](https://www.pakrail.gov.pk/) | [Seed 2](https://www.pakrail.gov.pk/Freight.aspx) | english_fallback; country_primary; not probed |
| 45 | `pakistan_air_cargo_airport_gateway` | B | HOLD_REVIEW | [Source family link](https://caapakistan.com.pk/) | [Seed 1](https://caapakistan.com.pk/) | [Seed 2](https://caapakistan.com.pk/airports.aspx) | english_fallback; country_primary; not probed |

## Quality distribution

```json
{"A": 5, "A_MINUS": 13, "A_PLUS": 2, "B": 7, "B_PLUS": 18}
```

## Decision distribution

```json
{"ACCEPT": 6, "ACCEPT_REVIEW": 32, "HOLD_REVIEW": 7}
```

