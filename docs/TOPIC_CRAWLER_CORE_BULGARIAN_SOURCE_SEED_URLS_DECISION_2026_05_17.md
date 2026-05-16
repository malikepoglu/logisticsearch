# Bulgarian (`bg`) source-seed URLs decision / Bulgarca source-seed URL karar dokümanı

Gate / Kapı: `R366_BG_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`  
Language step / Dil adımı: `3/17`  
Status / Durum: `LOCAL_ONLY_DECISION_DOC_CANDIDATE_REVIEW`  
Canonical rule doc / Kanonik kural dokümanı: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`  
Target catalog / Hedef katalog: `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json`  
Target decision doc / Hedef karar dokümanı: `docs/TOPIC_CRAWLER_CORE_BULGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_17.md`

## Decision summary / Karar özeti

Bulgarian source-seed rollout starts from a directory-first and official-provider balanced candidate set.

This document is not a live crawler activation surface. It is a candidate decision document only.

## Safety contract / Güvenlik sözleşmesi

- No catalog JSON is created in `R366`.
- No `docs/README.md` update is performed in `R366`.
- No Git add, commit, or push is performed in `R366`.
- No pi51c repo sync or pi51c live copy is performed in `R366`.
- No DB mutation, DB insert, frontier activation, crawler start/stop, systemd mutation, URL fetch, or live probe is performed in `R366`.
- Candidate source-seed catalogs are not live crawler activation.
- Crawler_Core collects raw evidence only.
- Crawler_Core discovered page links are raw link evidence, not added_seeds.
- Parse_Core may later create candidate added_seeds after filtering and pre-ranking.
- Desktop_Import performs stricter validation and final enrichment.
- Runtime activation policy must remain `pi51c_live_probe_required_before_db_or_frontier_insert`.
- Safety state must remain `candidate_only_not_live`.

## Metrics / Ölçüler

| Metric | Value |
|---|---:|
| Source family count | 40 |
| Seed surface count | 40 |
| Seed URL count | 40 |
| Unique seed URL count | 38 |
| Non-HTTPS seed URL count | 0 |
| Empty seed URL count | 0 |
| Quality counts | `{'A_PLUS': 3, 'A': 5, 'A_MINUS': 18, 'B_PLUS': 5, 'B': 7, 'B_MINUS': 2}` |

## Source family decisions / Kaynak aile kararları

| # | Source code | Quality | Decision | Note | Seed count |
|---:|---|---|---|---|---:|
| 1 | `BG001_NSBS_MEMBERS` | `A_PLUS` | `ACCEPT_REVIEW` | Bulgarian freight forwarding/logistics association member directory. | 1 |
| 2 | `BG002_NSBS_HOME` | `A_PLUS` | `ACCEPT_REVIEW` | National association context for transport, freight forwarding, and logistics. | 1 |
| 3 | `BG003_FIATA_BG_DIRECTORY` | `A_PLUS` | `ACCEPT_REVIEW` | FIATA Bulgaria member directory / authoritative cross-check surface. | 1 |
| 4 | `BG004_LOGISTIKA_WHOISWHO` | `A` | `ACCEPT_REVIEW` | Who Is Who in Transport and Freight Forwarding in Bulgaria. | 1 |
| 5 | `BG005_FREIGHTNET_LOGISTICS_BG` | `A_MINUS` | `ACCEPT_REVIEW` | Bulgaria freight/logistics company directory. | 1 |
| 6 | `BG006_FREIGHTNET_FORWARDERS_BG` | `A_MINUS` | `ACCEPT_REVIEW` | Bulgaria freight forwarders directory. | 1 |
| 7 | `BG007_INVESTBULGARIA_TRANSPORT_LOGISTICS` | `A_MINUS` | `ACCEPT_REVIEW` | Bulgarian transportation and logistics company index. | 1 |
| 8 | `BG008_RAILMARKET_LOGISTICS_BG` | `B_PLUS` | `ACCEPT_REVIEW` | Rail/intermodal/logistics oriented Bulgaria company directory. | 1 |
| 9 | `BG009_CARGOYELLOWPAGES_BG` | `B_PLUS` | `ACCEPT_REVIEW` | Cargo agents / freight forwarders discovery directory. | 1 |
| 10 | `BG010_OPCA_BG_FORWARDERS` | `B_PLUS` | `ACCEPT_REVIEW` | Freight forwarders / project cargo discovery directory. | 1 |
| 11 | `BG011_RUZAVE_BG` | `B` | `ACCEPT_REVIEW` | Shipping/freight forwarding discovery directory. | 1 |
| 12 | `BG012_KOMPASS_BG_TRANSPORT_LOGISTICS` | `B` | `ACCEPT_REVIEW` | General business directory; logistics discovery fallback. | 1 |
| 13 | `BG013_GOODFIRMS_BG_LOGISTICS` | `B` | `ACCEPT_REVIEW` | Supply-chain/logistics discovery surface. | 1 |
| 14 | `BG014_CLUTCH_BG_FREIGHT_FORWARDERS` | `B` | `ACCEPT_REVIEW` | Current freight-forwarder discovery surface. | 1 |
| 15 | `BG015_CLUTCH_BG_SUPPLY_CHAIN` | `B` | `ACCEPT_REVIEW` | Current supply-chain/logistics discovery surface. | 1 |
| 16 | `BG016_ENSUN_BG_LOGISTICS` | `B_MINUS` | `ACCEPT_REVIEW` | Long-tail company discovery surface; needs live check. | 1 |
| 17 | `BG017_LUSHA_BG_TRANSPORT_LOGISTICS` | `B_MINUS` | `ACCEPT_REVIEW` | Discovery/paywall-like business directory; not authority. | 1 |
| 18 | `BG018_CLECAT_NSBS_CONTEXT` | `A_MINUS` | `ACCEPT_REVIEW` | European association context for Bulgarian member body. | 1 |
| 19 | `BG019_BBLF_TRANSPORT_INDUSTRY` | `B` | `ACCEPT_REVIEW` | Business network discovery for transport/logistics firms. | 1 |
| 20 | `BG020_BCCI_GENERAL_CONTEXT` | `B` | `ACCEPT_REVIEW` | General chamber context; discovery-only. | 1 |
| 21 | `BG021_GOPET_TRANS` | `A` | `ACCEPT_REVIEW` | Official logistics provider seed. | 1 |
| 22 | `BG022_GOPET_WAREHOUSING` | `A_MINUS` | `ACCEPT_REVIEW` | Official warehousing/logistics service seed. | 1 |
| 23 | `BG023_GOPET_CONTACT` | `A_MINUS` | `ACCEPT_REVIEW` | Official contact/address extraction seed. | 1 |
| 24 | `BG024_UNIMASTERS_HOME` | `A` | `ACCEPT_REVIEW` | Official logistics company seed. | 1 |
| 25 | `BG025_UNIMASTERS_CONTACTS` | `A_MINUS` | `ACCEPT_REVIEW` | Official multi-location contact extraction seed. | 1 |
| 26 | `BG026_EUROSPED_HOME` | `A` | `ACCEPT_REVIEW` | Official Eurosped logistics service seed. | 1 |
| 27 | `BG027_EUROSPED_BG_TRANSPORT` | `A_MINUS` | `ACCEPT_REVIEW` | Domestic forwarding/transport/groupage seed. | 1 |
| 28 | `BG028_EUROSPED_WAREHOUSE` | `A_MINUS` | `ACCEPT_REVIEW` | Warehouse / 4PL / supply-chain seed. | 1 |
| 29 | `BG029_NTZ_HOME` | `A` | `ACCEPT_REVIEW` | Official NTZ logistics/freight forwarding seed. | 1 |
| 30 | `BG030_NTZ_ABOUT` | `A_MINUS` | `ACCEPT_REVIEW` | Official company profile seed. | 1 |
| 31 | `BG031_NTZ_CONTACTS` | `A_MINUS` | `ACCEPT_REVIEW` | Official contact/address extraction seed. | 1 |
| 32 | `BG032_INTERLOGISTICA_ABOUT` | `A_MINUS` | `ACCEPT_REVIEW` | Official Bulgarian transport/logistics company profile seed. | 1 |
| 33 | `BG033_WTO_BG_HOME` | `A_MINUS` | `ACCEPT_REVIEW` | Official freight/logistics company seed. | 1 |
| 34 | `BG034_DACHSER_BG` | `B_PLUS` | `ACCEPT_REVIEW` | Global logistics provider Bulgaria surface. | 1 |
| 35 | `BG035_DSV_BG` | `B_PLUS` | `ACCEPT_REVIEW` | Global logistics provider Bulgaria surface. | 1 |
| 36 | `BG036_FLEXYTRANS_HOME` | `A_MINUS` | `ACCEPT_REVIEW` | Official transport/forwarding company seed. | 1 |
| 37 | `BG037_EUROSPEED_HOME` | `A_MINUS` | `ACCEPT_REVIEW` | Official Bulgarian cargo transport company seed. | 1 |
| 38 | `BG038_ORBIT_WAREHOUSE` | `A_MINUS` | `ACCEPT_REVIEW` | Warehouse logistics service seed. | 1 |
| 39 | `BG039_BON_MARINE_FROM_FIATA_NSBS` | `A_MINUS` | `ACCEPT_REVIEW` | FIATA/NSBS-listed company candidate; official domain to be extracted later. | 1 |
| 40 | `BG040_DESPRED_FROM_FIATA` | `A_MINUS` | `ACCEPT_REVIEW` | FIATA-listed Bulgarian freight/logistics candidate; official domain to be confirmed later. | 1 |

## Seed surface candidates / Seed yüzeyi adayları

| # | Source code | URL | URL type | candidate_manifest | is_live | enabled | needs_live_check | runtime_activation_policy | safety_state |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `BG001_NSBS_MEMBERS` | `https://nsbs.bg/en/members` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 2 | `BG002_NSBS_HOME` | `https://nsbs.bg/en/home` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 3 | `BG003_FIATA_BG_DIRECTORY` | `https://fiata.org/directory/bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 4 | `BG004_LOGISTIKA_WHOISWHO` | `https://www.whoiswho.logistika.bg/en/index.php` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 5 | `BG005_FREIGHTNET_LOGISTICS_BG` | `https://www.freightnet.com/directory/p1/cBG/s99.htm` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 6 | `BG006_FREIGHTNET_FORWARDERS_BG` | `https://www.freightnet.com/directory/p2/cBG/s30.htm` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 7 | `BG007_INVESTBULGARIA_TRANSPORT_LOGISTICS` | `https://www.investbulgaria.com/Bulgarian-Transportation-and-Logistics-Companies/130` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 8 | `BG008_RAILMARKET_LOGISTICS_BG` | `https://railmarket.com/eu/bulgaria/logistics-companies` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 9 | `BG009_CARGOYELLOWPAGES_BG` | `https://www.cargoyellowpages.com/bulgaria_freight_forwarders_cargo_agents.html` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 10 | `BG010_OPCA_BG_FORWARDERS` | `https://overseasprojectcargo.com/InternationalFreightForwarders/bulgaria-freight-forwarders/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 11 | `BG011_RUZAVE_BG` | `https://ruzave.com/bulgaria` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 12 | `BG012_KOMPASS_BG_TRANSPORT_LOGISTICS` | `https://bg.kompass.com/s/transport-logistics/10/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 13 | `BG013_GOODFIRMS_BG_LOGISTICS` | `https://www.goodfirms.co/supply-chain-logistics-companies/bulgaria` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 14 | `BG014_CLUTCH_BG_FREIGHT_FORWARDERS` | `https://clutch.co/bg/logistics/freight-forwarders` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 15 | `BG015_CLUTCH_BG_SUPPLY_CHAIN` | `https://clutch.co/bg/logistics/supply-chain-management` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 16 | `BG016_ENSUN_BG_LOGISTICS` | `https://ensun.io/search/logistic/bulgaria` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 17 | `BG017_LUSHA_BG_TRANSPORT_LOGISTICS` | `https://www.lusha.com/company-search/transportation-logistics-and-storage/a64fd456c3/bulgaria/199/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 18 | `BG018_CLECAT_NSBS_CONTEXT` | `https://www.clecat.org/members/full-members` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 19 | `BG019_BBLF_TRANSPORT_INDUSTRY` | `https://www.bblf.bg/en/industries` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 20 | `BG020_BCCI_GENERAL_CONTEXT` | `https://www.bcci.bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 21 | `BG021_GOPET_TRANS` | `https://gopettrans.com/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 22 | `BG022_GOPET_WAREHOUSING` | `https://gopettrans.com/warehousing-logistics/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 23 | `BG023_GOPET_CONTACT` | `https://gopettrans.com/contact/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 24 | `BG024_UNIMASTERS_HOME` | `https://www.unimasters.com/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 25 | `BG025_UNIMASTERS_CONTACTS` | `https://www.unimasters.com/page/6/Contacts.html` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 26 | `BG026_EUROSPED_HOME` | `https://www.eurosped.bg/en/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 27 | `BG027_EUROSPED_BG_TRANSPORT` | `https://www.eurosped.bg/en/transport-in-bulgaria/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 28 | `BG028_EUROSPED_WAREHOUSE` | `https://www.eurosped.bg/en/eurolog-warehouse-logistics-4pl/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 29 | `BG029_NTZ_HOME` | `https://ntz.bg/en/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 30 | `BG030_NTZ_ABOUT` | `https://ntz.bg/en/about-us/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 31 | `BG031_NTZ_CONTACTS` | `https://ntz.bg/en/contacts/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 32 | `BG032_INTERLOGISTICA_ABOUT` | `https://www.interlogistica.bg/en/info/about/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 33 | `BG033_WTO_BG_HOME` | `https://www.wto.bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 34 | `BG034_DACHSER_BG` | `https://www.dachser.bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 35 | `BG035_DSV_BG` | `https://www.bg.dsv.com/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 36 | `BG036_FLEXYTRANS_HOME` | `https://www.flexytrans.bg/en/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 37 | `BG037_EUROSPEED_HOME` | `https://eu-speed.com/en/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 38 | `BG038_ORBIT_WAREHOUSE` | `https://www.orbit.bg/en/service/warehouse-logistics/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 39 | `BG039_BON_MARINE_FROM_FIATA_NSBS` | `https://fiata.org/directory/bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |
| 40 | `BG040_DESPRED_FROM_FIATA` | `https://fiata.org/directory/bg/` | `directory_or_official_candidate` | `true` | `false` | `false` | `true` | `pi51c_live_probe_required_before_db_or_frontier_insert` | `candidate_only_not_live` |

## Review notes / İnceleme notları

- `A_PLUS`, `A`, and `A_MINUS` sources should receive priority during later JSON conversion.
- `B`, `B_PLUS`, and `B_MINUS` discovery surfaces must stay candidate-only and require later live check before any DB/frontier insertion.
- Multi-country directory hosts such as FIATA, Freightnet, Clutch, GoodFirms, Ensun, Lusha, Ruzave, CargoYellowPages, Kompass, and OPCA must remain discovery surfaces unless a later live check confirms exact Bulgarian official company pages.
- Official company pages may later be split into multiple seed surfaces in the JSON stage if strict catalog metrics require richer service/contact segmentation.
- This decision doc intentionally does not create or activate frontier seeds.
