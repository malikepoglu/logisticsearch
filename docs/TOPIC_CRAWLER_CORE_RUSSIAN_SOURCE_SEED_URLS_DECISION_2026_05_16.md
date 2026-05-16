# Russian Source-Seed URLs Decision / Russian (`ru`) Startpoint Plan

Gate: `R339_RU_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`

## 1. Scope / Kapsam

- Language code: `ru`
- Language name: Russian
- Target catalog path: `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json`
- This document is a local-only decision plan.
- No catalog JSON is created in R339.
- No Git add, commit, or push in R339.
- No pi51c sync or pi51c live runtime copy in R339.
- No DB mutation, DB insert, frontier activation, crawler start/stop, systemd mutation, or URL live probe in R339.

## 2. Canonical rule basis / Kanonik kural temeli

- Canonical rule doc: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Canonical rule SHA-256: `65b36104f039962f3b6c8cd3c70b2575e0de00f27e50732e18953749d89bb49d`
- Required schema: `source_families_v2`
- Required runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Required safety state: `candidate_only_not_live`

## 3. Selection policy / Seçim politikası

- Directory-first selection is applied in this decision plan.
- Association directories, member directories, port/airport company directories, freight-forwarder directories, logistics guide directories, terminal network directories, and official company-index surfaces are prioritized before individual commercial company pages.
- Individual company or terminal locator pages remain candidate fallback surfaces only after higher-authority directory surfaces.
- Crawler_Core collects raw evidence only.
- Crawler_Core-discovered links are raw links, not `added_seeds`.
- Parse_Core may later create candidate `added_seeds` after filtering and pre-ranking.
- Desktop_Import performs stricter validation and final ranking later.

## 4. Planned metrics / Planlanan metrikler

- Planned source families: 40
- Planned seed surfaces / seed URLs: 84
- Unique seed URLs: 84
- Duplicate seed URLs: 0
- Non-HTTPS seed URLs: 0
- Candidate source-seed catalogs are not live crawler activation.
- All planned URLs are structural candidates only until separate pi51c live-probe and DB/frontier gates.

## 5. Planned source families / Planlanan source family listesi

| # | source_code | name | category | quality | decision | seed_url_count | note |
|---:|---|---|---|---|---|---:|---|
| 1 | `RU001_FIATA_ARE` | FIATA Russia and FAR/ARE association directory surfaces | association_directory | A_PLUS | ACCEPT_REVIEW | 3 | Directory-first: FIATA country listing plus Russian freight forwarding association surfaces. |
| 2 | `RU002_FREIGHTNET_RUSSIA` | Freightnet Russia logistics directory | commercial_b2b_directory | A_MINUS | ACCEPT_REVIEW | 3 | Directory-first: freight and forwarding directory pages for Russia. |
| 3 | `RU003_FORWARDINGCOMPANIES_RU` | ForwardingCompanies Russian Federation directory | commercial_b2b_directory | A_MINUS | ACCEPT_REVIEW | 3 | Directory-first: country and association pages for freight forwarders. |
| 4 | `RU004_CARGO_YELLOW_PAGES` | CargoYellowPages Russia freight and cargo directories | commercial_b2b_directory | A_MINUS | ACCEPT_REVIEW | 3 | Directory-first: Russia country cargo agent and freight forwarder lists. |
| 5 | `RU005_AZFREIGHT_RUSSIA` | AZFreight Russia freight forwarder directory | commercial_b2b_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: logistics and freight forwarder country pages. |
| 6 | `RU006_JCTRANS_RUSSIA` | JCtrans Russia freight forwarder directory | commercial_b2b_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: country company list surface. |
| 7 | `RU007_RAILMARKET_RUSSIA` | RailMarket Russian Federation forwarding and logistics | rail_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: rail logistics and rail forwarder discovery surface. |
| 8 | `RU008_RUZAVE_RUSSIA` | Ruzave Russia shipping and freight directory | commercial_b2b_directory | B | ACCEPT_REVIEW | 2 | Directory-first: shipping and freight forwarding discovery pages. |
| 9 | `RU009_ROOLZ_RUSSIA` | Roolz Russia forwarder and carrier directory | commercial_b2b_directory | B | ACCEPT_REVIEW | 2 | Directory-first: country forwarder and carrier list candidates. |
| 10 | `RU010_SHIPPINGLINE_RUSSIA` | ShippingLine Russia freight forwarders directory | shipping_directory | B | ACCEPT_REVIEW | 2 | Directory-first: shipping catalogue and freight forwarder country pages. |
| 11 | `RU011_GOODFIRMS_RUSSIA` | GoodFirms Russia logistics company list | commercial_review_directory | B | ACCEPT_REVIEW | 2 | Discovery-only directory; keep candidate until live review. |
| 12 | `RU012_CLUTCH_RUSSIA` | Clutch Russia logistics company discovery | commercial_review_directory | B | ACCEPT_REVIEW | 2 | Discovery-only commercial directory candidate. |
| 13 | `RU013_KOMPASS_RUSSIA` | Kompass Russia logistics and transport directory | commercial_company_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: business directory candidate for logistics companies. |
| 14 | `RU014_EUROPAGES_RUSSIA` | Europages Russia transport and freight directory | commercial_company_directory | B | ACCEPT_REVIEW | 2 | Directory-first: European B2B directory surfaces for Russia. |
| 15 | `RU015_ALL_FORWARD_RUSSIA` | All Forward member directory Russia search | network_member_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: freight network member directory search surfaces. |
| 16 | `RU016_WCAWORLD_RUSSIA` | WCAworld directory Russia search | network_member_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: freight network member search candidate. |
| 17 | `RU017_SEARATES_RUSSIA` | SeaRates Russia freight and maritime directory surfaces | shipping_directory | B | ACCEPT_REVIEW | 2 | Directory-first: maritime and freight country discovery. |
| 18 | `RU018_WORLD_PORT_SOURCE_RUSSIA` | World Port Source Russia port directory | port_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: port geography source for later port-linked logistics discovery. |
| 19 | `RU019_PORTS_COM_RUSSIA` | Ports.com Russia port directory | port_directory | B | ACCEPT_REVIEW | 2 | Directory-first: port listing candidate; not live until probe. |
| 20 | `RU020_MARINETRAFFIC_RUSSIA_PORTS` | MarineTraffic Russia port discovery | port_directory | B | ACCEPT_REVIEW | 2 | Directory-first: port discovery candidate for sea logistics context. |
| 21 | `RU021_PORTNEWS_RUSSIA` | PortNews ports and company directories | port_and_company_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: sector news portal with ports/company directory surfaces. |
| 22 | `RU022_MORPORT_RUSSIA` | Association of Commercial Sea Ports Russia | association_directory | A | ACCEPT_REVIEW | 2 | Directory-first: official association/member style port surface. |
| 23 | `RU023_PORT_SPB` | Port of Saint Petersburg official directory surfaces | official_port_surface | A_MINUS | ACCEPT_REVIEW | 2 | Official port surface; directory-like port service discovery candidate. |
| 24 | `RU024_NOVOROSSIYSK_PORT` | Novorossiysk Commercial Sea Port official surfaces | official_port_surface | A_MINUS | ACCEPT_REVIEW | 2 | Official port/operator surface; candidate for port-linked logistics discovery. |
| 25 | `RU025_VLADIVOSTOK_PORT` | Vladivostok Sea Commercial Port official surfaces | official_port_surface | A_MINUS | ACCEPT_REVIEW | 2 | Official port/operator surface for Far East logistics discovery. |
| 26 | `RU026_GLOBAL_PORTS` | Global Ports terminal network | terminal_network_directory | A_MINUS | ACCEPT_REVIEW | 2 | Official terminal network directory candidate. |
| 27 | `RU027_FESCO` | FESCO locations and services | official_logistics_network | A_MINUS | ACCEPT_REVIEW | 2 | Official logistics network/location surface; fallback after directory pages. |
| 28 | `RU028_TRANSCONTAINER` | TransContainer terminal network | rail_terminal_network | A_MINUS | ACCEPT_REVIEW | 2 | Official rail container terminal network candidate. |
| 29 | `RU029_RZD_LOGISTICS` | RZD Logistics services and contacts | rail_logistics_operator | A_MINUS | ACCEPT_REVIEW | 2 | Official rail logistics operator surfaces; candidate fallback. |
| 30 | `RU030_RZD_CARGO` | Russian Railways cargo surfaces | rail_freight_surface | A_MINUS | ACCEPT_REVIEW | 2 | Official rail/cargo surfaces for rail logistics context. |
| 31 | `RU031_DELOVYE_LINII` | Delovye Linii terminal and city directory | domestic_terminal_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-like terminal/city locator; candidate only. |
| 32 | `RU032_PEK` | PEK contacts and terminal directory | domestic_terminal_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-like terminal locator; candidate only. |
| 33 | `RU033_CDEK` | CDEK office locator surfaces | parcel_office_directory | B | ACCEPT_REVIEW | 2 | Office locator directory candidate for logistics point discovery. |
| 34 | `RU034_BOXBERRY` | Boxberry office and courier directory surfaces | parcel_office_directory | B | ACCEPT_REVIEW | 2 | Office locator candidate; not a B2B priority but useful for parcel logistics discovery. |
| 35 | `RU035_DPD_RUSSIA` | DPD Russia contacts and home surfaces | parcel_network_surface | B | ACCEPT_REVIEW | 2 | Parcel/logistics network surface; candidate until live review. |
| 36 | `RU036_BAIKAL_SERVICE` | Baikal Service terminal directory | domestic_terminal_directory | B | ACCEPT_REVIEW | 2 | Directory-like terminal/contact surface; candidate only. |
| 37 | `RU037_KIT_TRANSPORT` | KIT transport terminal and contact surfaces | domestic_terminal_directory | B | ACCEPT_REVIEW | 2 | Terminal/contact locator candidate. |
| 38 | `RU038_MAJOR_EXPRESS` | Major Express branch directory | express_logistics_directory | B | ACCEPT_REVIEW | 2 | Branch directory candidate for express logistics discovery. |
| 39 | `RU039_PONY_EXPRESS` | Pony Express office directory | express_logistics_directory | B | ACCEPT_REVIEW | 2 | Office directory candidate for express logistics discovery. |
| 40 | `RU040_TRANSRUSSIA_EXHIBITOR_DIRECTORY` | TransRussia exhibitor directory | trade_fair_exhibitor_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first: industry exhibition directory candidate for Russian logistics suppliers. |

## 6. Planned seed URLs / Planlanan seed URL listesi

| seed_url_index | source_code | url | candidate_manifest | is_live | enabled | needs_live_check | runtime_activation_policy | safety_state |
|---:|---|---|---|---|---|---|---|---|
| 1 | `RU001_FIATA_ARE` | `https://fiata.org/directory/ru/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 2 | `RU001_FIATA_ARE` | `https://en.far-aerf.ru/overview` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 3 | `RU001_FIATA_ARE` | `https://far-aerf.ru/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 4 | `RU002_FREIGHTNET_RUSSIA` | `https://www.freightnet.com/directory/p1/cRU/s99.htm` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 5 | `RU002_FREIGHTNET_RUSSIA` | `https://www.freightnet.com/directory/p2/cRU/s99.htm` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 6 | `RU002_FREIGHTNET_RUSSIA` | `https://www.freightnet.com/directory/p1/cRU/s30.htm` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 7 | `RU003_FORWARDINGCOMPANIES_RU` | `https://forwardingcompanies.com/in/russian-federation` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 8 | `RU003_FORWARDINGCOMPANIES_RU` | `https://forwardingcompanies.com/association/the-russian-association-of-freight-forwarding-and-logistic-organizations-far-` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 9 | `RU003_FORWARDINGCOMPANIES_RU` | `https://forwardingcompanies.com/in/russian-federation/moscow` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 10 | `RU004_CARGO_YELLOW_PAGES` | `https://www.cargoyellowpages.com/russia_freight_forwarders_cargo_agents.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 11 | `RU004_CARGO_YELLOW_PAGES` | `https://www.cargoyellowpages.com/en/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 12 | `RU004_CARGO_YELLOW_PAGES` | `https://www.cargoyellowpages.com/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 13 | `RU005_AZFREIGHT_RUSSIA` | `https://azfreight.com/country-facility/freight-forwarders-in-russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 14 | `RU005_AZFREIGHT_RUSSIA` | `https://azfreight.com/countries/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 15 | `RU006_JCTRANS_RUSSIA` | `https://m.jctrans.com/en/company/listc/Russia/0-0` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 16 | `RU006_JCTRANS_RUSSIA` | `https://www.jctrans.com/en/company/listc/Russia/0-0` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 17 | `RU007_RAILMARKET_RUSSIA` | `https://railmarket.com/ap/russian-federation/forwarding-logistics` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 18 | `RU007_RAILMARKET_RUSSIA` | `https://railmarket.com/ap/russian-federation/rail-forwarders` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 19 | `RU008_RUZAVE_RUSSIA` | `https://ruzave.com/russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 20 | `RU008_RUZAVE_RUSSIA` | `https://ruzave.com/russia/freight-forwarders/freight-forwardingservices/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 21 | `RU009_ROOLZ_RUSSIA` | `https://roolz.net/companies/forwarders/russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 22 | `RU009_ROOLZ_RUSSIA` | `https://roolz.net/companies/carriers/russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 23 | `RU010_SHIPPINGLINE_RUSSIA` | `https://www.shippingline.org/company/ru/Russia-Freight_Forwarders-2.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 24 | `RU010_SHIPPINGLINE_RUSSIA` | `https://www.shippingline.org/company/ru/Russia-Logistics-1.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 25 | `RU011_GOODFIRMS_RUSSIA` | `https://www.goodfirms.co/supply-chain-logistics-companies/russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 26 | `RU011_GOODFIRMS_RUSSIA` | `https://www.goodfirms.co/supply-chain-logistics-companies/warehousing/russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 27 | `RU012_CLUTCH_RUSSIA` | `https://clutch.co/ru/logistics` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 28 | `RU012_CLUTCH_RUSSIA` | `https://clutch.co/ru/supply-chain/logistics` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 29 | `RU013_KOMPASS_RUSSIA` | `https://ru.kompass.com/a/logistics/90280/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 30 | `RU013_KOMPASS_RUSSIA` | `https://www.kompass.com/a/logistics-services/9028/c/russian-federation/ru/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 31 | `RU014_EUROPAGES_RUSSIA` | `https://www.europages.co.uk/companies/russia/transport%20and%20logistics.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 32 | `RU014_EUROPAGES_RUSSIA` | `https://www.europages.co.uk/companies/russia/freight%20forwarders.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 33 | `RU015_ALL_FORWARD_RUSSIA` | `https://www.all-forward.com/MembersDirectory` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 34 | `RU015_ALL_FORWARD_RUSSIA` | `https://www.all-forward.com/MembersDirectory?country=Russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 35 | `RU016_WCAWORLD_RUSSIA` | `https://www.wcaworld.com/Directory` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 36 | `RU016_WCAWORLD_RUSSIA` | `https://www.wcaworld.com/Directory?search=Russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 37 | `RU017_SEARATES_RUSSIA` | `https://www.searates.com/freight/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 38 | `RU017_SEARATES_RUSSIA` | `https://www.searates.com/maritime/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 39 | `RU018_WORLD_PORT_SOURCE_RUSSIA` | `https://www.worldportsource.com/ports/RUS.php` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 40 | `RU018_WORLD_PORT_SOURCE_RUSSIA` | `https://www.worldportsource.com/ports/index/RUS.php` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 41 | `RU019_PORTS_COM_RUSSIA` | `https://ports.com/russia/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 42 | `RU019_PORTS_COM_RUSSIA` | `https://ports.com/sea-route/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 43 | `RU020_MARINETRAFFIC_RUSSIA_PORTS` | `https://www.marinetraffic.com/en/ais/index/ports/all/per_country:RU` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 44 | `RU020_MARINETRAFFIC_RUSSIA_PORTS` | `https://www.marinetraffic.com/en/ais/index/search/all?keyword=Russia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 45 | `RU021_PORTNEWS_RUSSIA` | `https://en.portnews.ru/ports/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 46 | `RU021_PORTNEWS_RUSSIA` | `https://en.portnews.ru/companies/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 47 | `RU022_MORPORT_RUSSIA` | `https://morport.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 48 | `RU022_MORPORT_RUSSIA` | `https://morport.com/en/members/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 49 | `RU023_PORT_SPB` | `https://www.psp.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 50 | `RU023_PORT_SPB` | `https://www.psp.ru/en/port-services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 51 | `RU024_NOVOROSSIYSK_PORT` | `https://nmtp.info/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 52 | `RU024_NOVOROSSIYSK_PORT` | `https://nmtp.info/en/holding/stevedoring/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 53 | `RU025_VLADIVOSTOK_PORT` | `https://www.vmtp.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 54 | `RU025_VLADIVOSTOK_PORT` | `https://www.vmtp.ru/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 55 | `RU026_GLOBAL_PORTS` | `https://www.globalports.com/terminals/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 56 | `RU026_GLOBAL_PORTS` | `https://www.globalports.com/about/terminals/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 57 | `RU027_FESCO` | `https://www.fesco.ru/en/clients/locations/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 58 | `RU027_FESCO` | `https://www.fesco.ru/en/clients/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 59 | `RU028_TRANSCONTAINER` | `https://trcont.com/en/terminals-and-services/terminal-network/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 60 | `RU028_TRANSCONTAINER` | `https://trcont.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 61 | `RU029_RZD_LOGISTICS` | `https://www.rzdlog.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 62 | `RU029_RZD_LOGISTICS` | `https://www.rzdlog.com/en/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 63 | `RU030_RZD_CARGO` | `https://cargo.rzd.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 64 | `RU030_RZD_CARGO` | `https://eng.rzd.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 65 | `RU031_DELOVYE_LINII` | `https://www.dellin.ru/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 66 | `RU031_DELOVYE_LINII` | `https://www.dellin.ru/cities/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 67 | `RU032_PEK` | `https://pecom.ru/ru/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 68 | `RU032_PEK` | `https://pecom.ru/ru/contacts/terminaly/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 69 | `RU033_CDEK` | `https://www.cdek.ru/ru/offices/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 70 | `RU033_CDEK` | `https://www.cdek.ru/ru/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 71 | `RU034_BOXBERRY` | `https://boxberry.ru/find_an_office/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 72 | `RU034_BOXBERRY` | `https://boxberry.ru/courier-delivery/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 73 | `RU035_DPD_RUSSIA` | `https://www.dpd.ru/dpd/contacts/index.do2` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 74 | `RU035_DPD_RUSSIA` | `https://www.dpd.ru/dpd/home.do2` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 75 | `RU036_BAIKAL_SERVICE` | `https://www.baikalsr.ru/contacts/terminaly/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 76 | `RU036_BAIKAL_SERVICE` | `https://www.baikalsr.ru/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 77 | `RU037_KIT_TRANSPORT` | `https://tk-kit.com/contacts/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 78 | `RU037_KIT_TRANSPORT` | `https://tk-kit.com/terminal/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 79 | `RU038_MAJOR_EXPRESS` | `https://www.majorexpress.ru/branches/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 80 | `RU038_MAJOR_EXPRESS` | `https://www.majorexpress.ru/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 81 | `RU039_PONY_EXPRESS` | `https://www.ponyexpress.ru/offices/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 82 | `RU039_PONY_EXPRESS` | `https://www.ponyexpress.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 83 | `RU040_TRANSRUSSIA_EXHIBITOR_DIRECTORY` | `https://transrussia.ru/en/exhibitor-list/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 84 | `RU040_TRANSRUSSIA_EXHIBITOR_DIRECTORY` | `https://transrussia.ru/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |

## 7. R339 safety seal / R339 güvenlik mühürü

- `candidate_manifest=true` for every planned seed.
- `is_live=false` for every planned seed.
- `enabled=false` for every planned seed.
- `needs_live_check=true` for every planned seed.
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert` for every planned seed.
- `safety_state=candidate_only_not_live` for every planned seed.
- Russian catalog JSON must be created only in a later separate gated step.

