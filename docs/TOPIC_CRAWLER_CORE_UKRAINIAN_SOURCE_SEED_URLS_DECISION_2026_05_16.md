# Ukrainian Source-Seed URLs Decision / Ukraynaca Source-Seed URL Kararı

- Gate / Kapı: `R353_UK_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`
- Language / Dil: Ukrainian
- Language code / Dil kodu: `uk`
- Target catalog path / Hedef katalog yolu: `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json`
- Canonical rule doc / Kanonik kural dokümanı: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Canonical rule SHA256 / Kanonik kural SHA256: `65b36104f039962f3b6c8cd3c70b2575e0de00f27e50732e18953749d89bb49d`
- Base repository HEAD / Temel repo HEAD: `4b69d2c72c86bf0994a774291abd955a883876ce`
- Runtime activation policy / Runtime aktivasyon politikası: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Safety state / Güvenlik durumu: `candidate_only_not_live`

## Scope / Kapsam

This document records the candidate Ukrainian source-seed plan only. It does not create the JSON catalog and it does not activate any crawler/frontier/runtime surface.

Bu doküman yalnızca Ukraynaca candidate source-seed planını kaydeder. JSON katalog oluşturmaz ve crawler/frontier/runtime yüzeyini aktive etmez.

## Hard safety rules / Sert güvenlik kuralları

- Candidate source-seed catalogs are not live crawler activation.
- No catalog JSON is created in `R353`.
- No DB insert.
- No frontier activation.
- No URL fetch/live probe.
- No pi51c live activation.
- All future catalog entries must use `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`.
- Runtime policy must remain `pi51c_live_probe_required_before_db_or_frontier_insert` until an explicit pi51c live-probe gate is approved.

## Metrics / Metrikler

- Planned source families: `40`
- Planned seed surfaces / seed URLs: `56`
- Unique source codes: `40`
- Unique seed URLs: `56`
- Duplicate seed URLs: `0`
- Non-HTTPS seed URLs: `0`
- Empty seed URLs: `0`
- Directory-first selection is applied in this decision plan.
- Quality counts: `{'A': 3, 'A_MINUS': 8, 'A_PLUS': 3, 'B': 14, 'B_MINUS': 2, 'B_PLUS': 10}`
- Priority counts: `{'HIGH': 7, 'LOW': 2, 'MEDIUM': 10, 'MEDIUM_HIGH': 8, 'MEDIUM_LOW': 10, 'VERY_HIGH': 3}`
- Decision counts: `{'ACCEPT_REVIEW': 40}`

## Candidate source families and seed URLs / Candidate source families ve seed URL'leri

| # | Source family code | Quality | Priority | Decision | Rationale | Seed URLs |
|---:|---|---|---|---|---|---|
| 1 | `UK001_AIFFU_SEARCH_FORWARDER` | `A_PLUS` | `VERY_HIGH` | `ACCEPT_REVIEW` | National association forwarder search surface; first-class directory seed. | 1. [https://ameu.org.ua/en/search-forwarder](https://ameu.org.ua/en/search-forwarder)<br>2. [https://ameu.org.ua/en/search-forwarder?start=20](https://ameu.org.ua/en/search-forwarder?start=20)<br>3. [https://ameu.org.ua/en/search-forwarder?start=40](https://ameu.org.ua/en/search-forwarder?start=40)<br>4. [https://ameu.org.ua/en/search-forwarder?start=60](https://ameu.org.ua/en/search-forwarder?start=60) |
| 2 | `UK002_AIFFU_FULL_MEMBERS` | `A_PLUS` | `VERY_HIGH` | `ACCEPT_REVIEW` | AIFFU full-member pages; strong member directory candidate. | 1. [https://ameu.org.ua/en/members/active-members?dir=asc&order=f_vvvvvvvvvv&start=0](https://ameu.org.ua/en/members/active-members?dir=asc&order=f_vvvvvvvvvv&start=0)<br>2. [https://ameu.org.ua/en/members/active-members?start=20](https://ameu.org.ua/en/members/active-members?start=20)<br>3. [https://ameu.org.ua/en/members/active-members?start=40](https://ameu.org.ua/en/members/active-members?start=40)<br>4. [https://ameu.org.ua/en/members/active-members?start=60](https://ameu.org.ua/en/members/active-members?start=60) |
| 3 | `UK003_FIATA_UKRAINE_DIRECTORY` | `A_PLUS` | `VERY_HIGH` | `ACCEPT_REVIEW` | FIATA country directory for Ukraine; authoritative association cross-reference. | 1. [https://fiata.org/directory/ua/](https://fiata.org/directory/ua/) |
| 4 | `UK004_UKRZOVNISHTRANS_OFFICIAL_ASSOCIATION` | `A` | `HIGH` | `ACCEPT_REVIEW` | Official association/reference surface for Ukrainian forwarding and logistics representation. | 1. [https://www.atfl.org.ua/en](https://www.atfl.org.ua/en)<br>2. [https://www.atfl.org.ua/](https://www.atfl.org.ua/)<br>3. [https://www.atfl.org.ua/en/pro-nas/istoriya](https://www.atfl.org.ua/en/pro-nas/istoriya)<br>4. [https://www.atfl.org.ua/en/pidvishennya-kvalifikaciyi](https://www.atfl.org.ua/en/pidvishennya-kvalifikaciyi) |
| 5 | `UK005_CLECAT_UKRZOVNISHTRANS_REFERENCE` | `A_MINUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | European association reference page; useful for association verification. | 1. [https://www.clecat.org/members/associate-members](https://www.clecat.org/members/associate-members) |
| 6 | `UK006_CARGO_AGENT_NETWORK_UKRAINE_ASSOCIATION` | `A_MINUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Country directory for cargo agents in Ukraine. | 1. [https://www.cargoagentnetwork.com/country/ukraine/](https://www.cargoagentnetwork.com/country/ukraine/) |
| 7 | `UK007_AZFREIGHT_UKRZOVNISHTRANS_ASSOCIATION` | `B` | `MEDIUM` | `ACCEPT_REVIEW` | Secondary association profile/reference; not a primary directory. | 1. [https://azfreight.com/association/ukrzovnishtrans-association-of-transport-forwarding-organisations/](https://azfreight.com/association/ukrzovnishtrans-association-of-transport-forwarding-organisations/) |
| 8 | `UK008_FREIGHTNET_UKRAINE_FORWARDERS` | `A_MINUS` | `HIGH` | `ACCEPT_REVIEW` | Freight forwarding directory with Ukraine country pages. | 1. [https://www.freightnet.com/directory/p1/cUA/s30.htm](https://www.freightnet.com/directory/p1/cUA/s30.htm)<br>2. [https://www.freightnet.com/directory/p2/cUA/s30.htm](https://www.freightnet.com/directory/p2/cUA/s30.htm) |
| 9 | `UK009_FORWARDINGCOMPANIES_UKRAINE` | `A_MINUS` | `HIGH` | `ACCEPT_REVIEW` | Freight forwarding company directory for Ukraine. | 1. [https://forwardingcompanies.com/in/ukraine](https://forwardingcompanies.com/in/ukraine) |
| 10 | `UK010_RUZAVE_UKRAINE_SHIPPING_DIRECTORY` | `A_MINUS` | `HIGH` | `ACCEPT_REVIEW` | Shipping/logistics directory country surface. | 1. [https://ruzave.com/ukraine](https://ruzave.com/ukraine) |
| 11 | `UK011_RAILMARKET_UKRAINE_LOGISTICS_COMPANIES` | `A_MINUS` | `HIGH` | `ACCEPT_REVIEW` | Railmarket logistics company directory for Ukraine. | 1. [https://railmarket.com/eu/ukraine/logistics-companies](https://railmarket.com/eu/ukraine/logistics-companies) |
| 12 | `UK012_RAILMARKET_UKRAINE_RAILWAY_COMPANIES` | `B_PLUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Railway company directory; supports rail/logistics discovery. | 1. [https://railmarket.com/eu/ukraine/companies](https://railmarket.com/eu/ukraine/companies) |
| 13 | `UK013_JCTRANS_UKRAINE_FORWARDERS` | `B_PLUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Marketplace-style forwarder directory; candidate only. | 1. [https://m.jctrans.com/en/company/listc/Ukraine/0-0](https://m.jctrans.com/en/company/listc/Ukraine/0-0) |
| 14 | `UK014_ROOLZ_UKRAINE_FORWARDERS` | `B_PLUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Forwarder directory/marketplace surface. | 1. [https://roolz.net/companies/forwarders/ukraine](https://roolz.net/companies/forwarders/ukraine) |
| 15 | `UK015_GOODFIRMS_UKRAINE_LOGISTICS` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Commercial logistics company list; candidate with lower trust than associations. | 1. [https://www.goodfirms.co/supply-chain-logistics-companies/ukraine](https://www.goodfirms.co/supply-chain-logistics-companies/ukraine) |
| 16 | `UK016_CLUTCH_UKRAINE_FREIGHT_FORWARDERS` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Commercial review directory for freight forwarders. | 1. [https://clutch.co/ua/logistics/freight-forwarders](https://clutch.co/ua/logistics/freight-forwarders) |
| 17 | `UK017_CLUTCH_UKRAINE_RAIL_FREIGHT` | `B` | `MEDIUM` | `ACCEPT_REVIEW` | Rail freight company review/directory surface. | 1. [https://clutch.co/ua/logistics/rail-freight-companies](https://clutch.co/ua/logistics/rail-freight-companies) |
| 18 | `UK018_LOGISTICS_COMPANIES_DIRECTORY_UKRAINE` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Logistics company directory; candidate only. | 1. [https://logisticscompaniesdirectory.com/network-regions/ukraine/](https://logisticscompaniesdirectory.com/network-regions/ukraine/) |
| 19 | `UK019_OPCA_UKRAINE_FORWARDERS_TRUCKING` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Project cargo/forwarder directory for Ukraine. | 1. [https://overseasprojectcargo.com/InternationalFreightForwarders/ukraine-freight-forwarders/](https://overseasprojectcargo.com/InternationalFreightForwarders/ukraine-freight-forwarders/) |
| 20 | `UK020_FORWARDERSPAGES_UKRAINE` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Secondary forwarder directory. | 1. [https://www.forwarderspages.com/country/ukraine](https://www.forwarderspages.com/country/ukraine) |
| 21 | `UK021_SEARATES_UKRAINE_PORTS` | `B_PLUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Port and maritime reference surface. | 1. [https://www.searates.com/maritime/ukraine](https://www.searates.com/maritime/ukraine) |
| 22 | `UK022_CARGOROUTER_UKRAINE_PORTS` | `B` | `MEDIUM` | `ACCEPT_REVIEW` | Port directory reference. | 1. [https://www.cargorouter.com/directory/ports/Ukraine/](https://www.cargorouter.com/directory/ports/Ukraine/) |
| 23 | `UK023_MARINETRAFFIC_UKRAINE_MARITIME_COMPANIES` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Maritime company directory filtered to Ukraine. | 1. [https://www.marinetraffic.com/en/maritime-companies/directory/port%3A124/per_page%3A20/sublocation%3AUKRAINE](https://www.marinetraffic.com/en/maritime-companies/directory/port%3A124/per_page%3A20/sublocation%3AUKRAINE) |
| 24 | `UK024_MARINETRAFFIC_UKRAINE_PORT_AGENTS` | `B_PLUS` | `MEDIUM` | `ACCEPT_REVIEW` | Port agency directory filtered to Ukraine. | 1. [https://www.marinetraffic.com/en/maritime-companies/directory/secind%3A59/industry%3Aport%20agents/tag%3APort%20Agency/sublocation%3AUKRAINE](https://www.marinetraffic.com/en/maritime-companies/directory/secind%3A59/industry%3Aport%20agents/tag%3APort%20Agency/sublocation%3AUKRAINE) |
| 25 | `UK025_SHIPSGO_UKRAINE_PORTS` | `B` | `MEDIUM` | `ACCEPT_REVIEW` | Port reference surface. | 1. [https://shipsgo.com/ocean/ports/countries/ukraine](https://shipsgo.com/ocean/ports/countries/ukraine) |
| 26 | `UK026_INCODOCS_UKRAINE_PORTS` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Port reference surface; lower priority. | 1. [https://incodocs.com/ports/ua](https://incodocs.com/ports/ua) |
| 27 | `UK027_TARANGYA_UKRAINE_PORT_DIRECTORY` | `B_MINUS` | `LOW` | `ACCEPT_REVIEW` | Low-priority port directory reference. | 1. [https://www.tarangya.com/company/others/port-directory/country-wise/UA](https://www.tarangya.com/company/others/port-directory/country-wise/UA) |
| 28 | `UK028_BUSINESS_IN_UKRAINE_PORTS_TERMINALS` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Port and maritime terminal business category reference. | 1. [https://business-in-ukraine.online/business/category/ports-and-maritime-terminals/](https://business-in-ukraine.online/business/category/ports-and-maritime-terminals/) |
| 29 | `UK029_USPA_OFFICIAL_PORT_AUTHORITY` | `A` | `HIGH` | `ACCEPT_REVIEW` | Official Ukrainian Sea Ports Authority surface. | 1. [https://www.uspa.gov.ua/en/homepage-en](https://www.uspa.gov.ua/en/homepage-en) |
| 30 | `UK030_UKRZALIZNYTSIA_CARGO_RAIL` | `A` | `HIGH` | `ACCEPT_REVIEW` | Official Ukrainian Railways cargo transport and station directory surface. | 1. [https://uz.gov.ua/en/cargo_transportation/](https://uz.gov.ua/en/cargo_transportation/)<br>2. [https://uz.gov.ua/en/cargo_transportation/general_information/cargo_stations/](https://uz.gov.ua/en/cargo_transportation/general_information/cargo_stations/) |
| 31 | `UK031_UKRPOSHTA_BUSINESS_POSTAL_LOGISTICS` | `A_MINUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | National postal/logistics operator business and delivery surfaces. | 1. [https://www.ukrposhta.ua/en](https://www.ukrposhta.ua/en)<br>2. [https://www.ukrposhta.ua/en/ukrposhta-dlia-biznesu](https://www.ukrposhta.ua/en/ukrposhta-dlia-biznesu)<br>3. [https://www.ukrposhta.ua/en/dostavka-po-svitu](https://www.ukrposhta.ua/en/dostavka-po-svitu)<br>4. [https://track.ukrposhta.ua/tracking_EN.html](https://track.ukrposhta.ua/tracking_EN.html) |
| 32 | `UK032_NOVA_POST_BUSINESS_LOGISTICS` | `A_MINUS` | `MEDIUM_HIGH` | `ACCEPT_REVIEW` | Large parcel/logistics operator and business logistics surfaces. | 1. [https://novaposhta.ua/en/](https://novaposhta.ua/en/)<br>2. [https://novaposhtaglobal.ua/en/for-business/](https://novaposhtaglobal.ua/en/for-business/)<br>3. [https://nova.global/en-ua/](https://nova.global/en-ua/) |
| 33 | `UK033_MORDOR_UKRAINE_FREIGHT_COMPANIES` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Market report company list; secondary seed only. | 1. [https://www.mordorintelligence.com/industry-reports/ukraine-freight-and-logistics-market/companies](https://www.mordorintelligence.com/industry-reports/ukraine-freight-and-logistics-market/companies) |
| 34 | `UK034_ENSUN_UKRAINE_FORWARDING_COMPANIES` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Commercial directory/search surface. | 1. [https://ensun.io/search/freight-forwarding/ukraine](https://ensun.io/search/freight-forwarding/ukraine) |
| 35 | `UK035_DF_ALLIANCE_UKRAINE_FORWARDERS` | `B_MINUS` | `LOW` | `ACCEPT_REVIEW` | Low-priority forwarder reference. | 1. [https://www.df-alliance.com/freight-forwarder/ukraine](https://www.df-alliance.com/freight-forwarder/ukraine) |
| 36 | `UK036_EBA_UKRAINE_LOGISTICS_MEMBER_REFERENCES` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Business association member reference; not broad directory. | 1. [https://eba.com.ua/en/member/dsv-logistyka-tov/](https://eba.com.ua/en/member/dsv-logistyka-tov/) |
| 37 | `UK037_EKOL_UKRAINE_DIRECT_OPERATOR` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Direct operator surface; diversity/support seed. | 1. [https://ekol.com.ua/en/services/transport-solutions/](https://ekol.com.ua/en/services/transport-solutions/) |
| 38 | `UK038_STOLES_LOGISTIC_DIRECT_OPERATOR` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Direct operator logistics services surface. | 1. [https://stoles.com.ua/en/services/logistics/](https://stoles.com.ua/en/services/logistics/) |
| 39 | `UK039_CORCEL_UKRAINE_DIRECT_OPERATOR` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Direct operator logistics services surface. | 1. [https://corcel.com.ua/en/our-services/logistics-services/](https://corcel.com.ua/en/our-services/logistics-services/) |
| 40 | `UK040_STAR_LOGISTICS_DIRECT_OPERATOR` | `B` | `MEDIUM_LOW` | `ACCEPT_REVIEW` | Direct operator logistics services surface. | 1. [https://starlogistics.com.ua/en](https://starlogistics.com.ua/en) |

## Next gate / Sıradaki kapı

`R354_UK_SOURCE_SEED_DECISION_DOC_AUDIT_READONLY`

The next gate must be read-only and must verify this document before any JSON catalog creation.
