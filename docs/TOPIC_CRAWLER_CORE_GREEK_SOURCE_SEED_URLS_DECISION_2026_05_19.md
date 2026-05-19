# TOPIC — Greek Source Seed URLs Decision — 2026-05-19

## Gate

EL-03R2 — GREEK_SOURCE_SEED_DECISION_DOC_AND_CATALOG_LOCAL_ONLY_R2

## Scope

Language: Greek  
Native name: Ελληνικά  
Language code: el  
Catalog target: makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json  
Decision doc target: docs/TOPIC_CRAWLER_CORE_GREEK_SOURCE_SEED_URLS_DECISION_2026_05_19.md

## Safety

This is a candidate-only source-seed decision. It is not a crawler activation list.

- candidate_manifest=true
- is_live=false
- enabled=false
- needs_live_check=true
- runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert
- safety_state=candidate_only_not_live
- No DB insert
- No frontier insert
- No crawler start
- No systemd mutation
- No public URL probe during this local-only gate

## R2 correction

EL-03R1 stopped safely because one Kompass seed URL was duplicated.  
EL-03R2 replaces the duplicate warehouse/customs secondary seed with a unique Kompass logistics-and-procurement services page.

## Decision summary

- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Duplicate seed URLs: 0
- Non-HTTPS seed URLs: 0
- Directory-first policy: applied
- Association, registry, local directory, freight network, port, airport cargo, rail, customs and warehouse surfaces: prioritized
- Single-company homepages as primary discovery startpoints: avoided except official port/airport/infrastructure surfaces
- Blog/listicle pages as primary startpoints: avoided

## Quality distribution

- A: 8
- A_MINUS: 15
- A_PLUS: 5
- B: 3
- B_PLUS: 14

## Decision distribution

- ACCEPT: 9
- ACCEPT_REVIEW: 35
- HOLD_REVIEW: 1

## Content language distribution

- el,en: 3
- en: 42

## Numbered source and seed list

| No | Source family link | Seed-1 link | Seed-2 link | Quality | Decision |
|---:|---|---|---|---|---|
| 1 | [IFFAG&L / SYNDDEL official association](https://www.synddel.gr/en/) | [IFFAG&L history / official identity](https://www.synddel.gr/en/synddel/history-of-synddel) | [IFFAG&L contact](https://www.synddel.gr/en/contact) | A_PLUS | ACCEPT |
| 2 | [FIATA Greece member directory](https://fiata.org/directory/gr/) | [FIATA Greece association member](https://fiata.org/directory/gr/) | [FIATA directory root](https://fiata.org/directory/) | A_PLUS | ACCEPT |
| 3 | [XO logistics freight forwarding and storage Greece](https://www.xo.gr/dir-az/L/Logistics-Freight-Forwarding-and-Storage/?lang=en) | [XO logistics Greece](https://www.xo.gr/dir-az/L/Logistics-Freight-Forwarding-and-Storage/?lang=en) | [XO logistics Attica](https://www.xo.gr/dir-az/L/Logistics-Freight-Forwarding-and-Storage/Attica/?lang=en) | A_PLUS | ACCEPT |
| 4 | [XO international transport Greece](https://www.xo.gr/dir-az/I/International-Transport/?lang=en) | [XO international transport Greece](https://www.xo.gr/dir-az/I/International-Transport/?lang=en) | [XO international transport Attica](https://www.xo.gr/dir-az/I/International-Transport/Attica/?lang=en) | A_PLUS | ACCEPT |
| 5 | [Freightnet Greece freight forwarders](https://www.freightnet.com/directory/p1/cGR/s30.htm) | [Freightnet freight forwarders Greece](https://www.freightnet.com/directory/p1/cGR/s30.htm) | [Freightnet freight and logistics Greece](https://www.freightnet.com/directory/p1/cGR/s99.htm) | A_PLUS | ACCEPT |
| 6 | [CargoYellowPages Greece freight forwarders](https://www.cargoyellowpages.com/greece_freight_forwarders_cargo_agents.html) | [CargoYellowPages Greece country list](https://www.cargoyellowpages.com/greece_freight_forwarders_cargo_agents.html) | [CargoYellowPages Athens](https://www.cargoyellowpages.com/en/greece/athens/) | A | ACCEPT |
| 7 | [AZFreight freight forwarders in Greece](https://azfreight.com/country-facility/freight-forwarders-in-greece/) | [AZFreight Greece forwarders](https://azfreight.com/country-facility/freight-forwarders-in-greece/) | [AZFreight countries root](https://azfreight.com/countries/) | A | ACCEPT |
| 8 | [Kompass Greece transport and logistics](https://gr.kompass.com/z/gr/s/transport-logistics/10/) | [Kompass transport and logistics Greece](https://gr.kompass.com/z/gr/s/transport-logistics/10/) | [Kompass shipping and forwarding agents Greece](https://gr.kompass.com/a/shipping-and-forwarding-agents/75780/) | A_MINUS | ACCEPT_REVIEW |
| 9 | [Kompass Greece warehouses and logistics procurement services](https://gr.kompass.com/a/warehouses-and-storage-sites/75880/) | [Kompass warehouses and storage Greece](https://gr.kompass.com/a/warehouses-and-storage-sites/75880/) | [Kompass logistics and procurement services Greece](https://gr.kompass.com/a/logistics-and-procurement-services/75940/) | A_MINUS | ACCEPT_REVIEW |
| 10 | [Ruzave Greece freight directory](https://ruzave.com/greece/) | [Ruzave Greece freight directory](https://ruzave.com/greece/) | [Ruzave Greece warehouse companies](https://ruzave.com/greece/top-warehouse-companies/) | A_MINUS | ACCEPT_REVIEW |
| 11 | [Overseas Project Cargo Greece freight forwarders](https://overseasprojectcargo.com/InternationalFreightForwarders/greece-freight-forwarders/) | [OPCA Greece freight forwarders](https://overseasprojectcargo.com/InternationalFreightForwarders/greece-freight-forwarders/) | [OPCA international freight forwarders root](https://overseasprojectcargo.com/InternationalFreightForwarders/) | A_MINUS | ACCEPT_REVIEW |
| 12 | [GoodFirms freight forwarding Greece](https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/greece) | [GoodFirms freight forwarding Greece](https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/greece) | [GoodFirms logistics companies Greece](https://www.goodfirms.co/supply-chain-logistics-companies/greece) | A_MINUS | ACCEPT_REVIEW |
| 13 | [ForwardingCompanies Greece freight forwarders](https://forwardingcompanies.com/in/greece) | [ForwardingCompanies Greece](https://forwardingcompanies.com/in/greece) | [ForwardingCompanies root](https://forwardingcompanies.com/) | A_MINUS | ACCEPT_REVIEW |
| 14 | [FFC Directory Greece](https://ffcdirectory.com/region/greece/) | [FFC Directory Greece page 1](https://ffcdirectory.com/region/greece/) | [FFC Directory Greece page 2](https://ffcdirectory.com/region/greece/page/2/) | B_PLUS | ACCEPT_REVIEW |
| 15 | [DF Alliance Greece freight forwarder network](https://www.df-alliance.com/freight-forwarder/greece) | [DF Alliance Greece](https://www.df-alliance.com/freight-forwarder/greece) | [DF Alliance freight forwarder root](https://www.df-alliance.com/freight-forwarder) | B_PLUS | ACCEPT_REVIEW |
| 16 | [JCtrans Greece freight forwarder network list](https://www.jctrans.com/en/company/) | [JCtrans Greece forwarders mobile list](https://m.jctrans.com/en/company/listc/Greece/0-0) | [JCtrans company list root](https://www.jctrans.com/en/company/) | B_PLUS | ACCEPT_REVIEW |
| 17 | [WCAworld global freight forwarder directory](https://www.wcaworld.com/directory) | [WCAworld directory](https://www.wcaworld.com/directory) | [WCAworld root](https://www.wcaworld.com/) | B_PLUS | ACCEPT_REVIEW |
| 18 | [Aerocean Network members directory](https://aeroceanetwork.net/directory/) | [Aerocean members directory](https://aeroceanetwork.net/directory/) | [Aerocean root](https://aeroceanetwork.net/) | B_PLUS | ACCEPT_REVIEW |
| 19 | [Pangea Network Greece freight forwarders](https://pangea-network.com/) | [Pangea freight forwarders Greece](https://pangea-network.com/freight-forwarders/greece/) | [Pangea network root](https://pangea-network.com/) | B_PLUS | ACCEPT_REVIEW |
| 20 | [Ensun Greece freight and logistics search](https://ensun.io/search/freight-broker/greece) | [Ensun freight broker Greece](https://ensun.io/search/freight-broker/greece) | [Ensun logistics Greece](https://ensun.io/search/logistics/greece) | B | ACCEPT_REVIEW |
| 21 | [Vrisko customs brokers Greece](https://www.vrisko.gr/en/dir/customs-brokers/) | [Vrisko customs brokers Greece](https://www.vrisko.gr/en/dir/customs-brokers/) | [Vrisko customs brokers Athens](https://www.vrisko.gr/en/dir/customs-brokers/athens/) | A | ACCEPT |
| 22 | [XO customs brokers Greece](https://www.xo.gr/dir-az/C/Customs-Brokers/?lang=en) | [XO customs brokers Greece](https://www.xo.gr/dir-az/C/Customs-Brokers/?lang=en) | [XO customs brokers Athens](https://www.xo.gr/dir-az/C/Customs-Brokers/Municipality%20Athens/?lang=en) | A | ACCEPT |
| 23 | [Europages Greece customs brokers and logistics](https://www.europages.co.uk/companies/greece/brokers-customs.html) | [Europages customs brokers Greece](https://www.europages.co.uk/companies/greece/brokers-customs.html) | [Europages logistics Greece](https://www.europages.co.uk/companies/greece/logistics.html) | A_MINUS | ACCEPT_REVIEW |
| 24 | [Kompass Greece customs clearance agents](https://gr.kompass.com/a/customs-clearance-agents-road-freight/7578030/) | [Kompass customs road freight Greece](https://gr.kompass.com/a/customs-clearance-agents-road-freight/7578030/) | [Kompass customs sea freight Greece](https://gr.kompass.com/a/customs-clearance-agents-sea-freight/7578010/) | A_MINUS | ACCEPT_REVIEW |
| 25 | [Enterprise Greece logistics sector](https://www.enterprisegreece.gov.gr/en/invest-in-greece/investment-sectors/logistics/) | [Enterprise Greece logistics](https://www.enterprisegreece.gov.gr/en/invest-in-greece/investment-sectors/logistics/) | [Enterprise Greece investment sectors](https://www.enterprisegreece.gov.gr/en/invest-in-greece/investment-sectors/) | A | ACCEPT_REVIEW |
| 26 | [Athens International Airport cargo development](https://www.aia.gr/en/business/cargo-development) | [AIA cargo development](https://www.aia.gr/en/business/cargo-development) | [AIA business services](https://www.aia.gr/en/business/) | A | ACCEPT_REVIEW |
| 27 | [IATA CargoLink Greece air-cargo directory](https://www.iata.org/en/publications/directories/cargolink/directory/) | [IATA CargoLink directory](https://www.iata.org/en/publications/directories/cargolink/directory/) | [IATA Greek Air Cargo SA entry](https://www.iata.org/en/publications/directories/cargolink/directory/greek-air-cargo-sa/9527/) | A_MINUS | ACCEPT_REVIEW |
| 28 | [Thessaloniki Port Authority](https://www.thpa.gr/) | [ThPA homepage](https://www.thpa.gr/) | [ThPA services](https://www.thpa.gr/index.php/en/services) | A | ACCEPT_REVIEW |
| 29 | [Piraeus Port Authority](https://www.olp.gr/en/) | [Piraeus Port Authority homepage](https://www.olp.gr/en/) | [Piraeus Port container terminal](https://www.olp.gr/en/services/container-terminal) | A | ACCEPT_REVIEW |
| 30 | [iContainers Port of Piraeus profile](https://www.icontainers.com/ports/piraeus/) | [iContainers Piraeus port](https://www.icontainers.com/ports/piraeus/) | [iContainers Greece ports](https://www.icontainers.com/ports/greece/) | A_MINUS | ACCEPT_REVIEW |
| 31 | [CargoRouter Greece ports directory](https://www.cargorouter.com/directory/ports/Greece/Thessaloniki/) | [CargoRouter Thessaloniki port](https://www.cargorouter.com/directory/ports/Greece/Thessaloniki/) | [CargoRouter Greece ports](https://www.cargorouter.com/directory/ports/Greece/) | A_MINUS | ACCEPT_REVIEW |
| 32 | [SeaRates Greece ports list](https://www.searates.com/maritime/greece) | [SeaRates Greece ports](https://www.searates.com/maritime/greece) | [SeaRates logistics reference root](https://www.searates.com/reference/) | B_PLUS | ACCEPT_REVIEW |
| 33 | [Railmarket Greece railway and logistics companies](https://railmarket.com/eu/greece/companies) | [Railmarket Greece companies](https://railmarket.com/eu/greece/companies) | [Railmarket Greece logistics companies](https://railmarket.com/eu/greece/logistics-companies) | B_PLUS | ACCEPT_REVIEW |
| 34 | [Railmarket Greece rail forwarders](https://railmarket.com/eu/greece/rail-forwarders) | [Railmarket Greece rail forwarders](https://railmarket.com/eu/greece/rail-forwarders) | [Railmarket Greece logistics consulting](https://railmarket.com/eu/greece/logistics-consulting) | B_PLUS | ACCEPT_REVIEW |
| 35 | [XO transport companies Greece](https://www.xo.gr/dir-az/T/Transport-Companies/?lang=en) | [XO transport companies Greece](https://www.xo.gr/dir-az/T/Transport-Companies/?lang=en) | [XO transport companies Attica](https://www.xo.gr/dir-az/T/Transport-Companies/Attica/?lang=en) | A_MINUS | ACCEPT_REVIEW |
| 36 | [XO road transport Greece](https://www.xo.gr/dir-az/R/Road-Transport/?lang=en) | [XO road transport Greece](https://www.xo.gr/dir-az/R/Road-Transport/?lang=en) | [XO road transport Thessaloniki](https://www.xo.gr/dir-az/R/Road-Transport/Thessaloniki/?lang=en) | A_MINUS | ACCEPT_REVIEW |
| 37 | [XO warehouses Greece](https://www.xo.gr/dir-az/W/Warehouses/?lang=en) | [XO warehouses Greece](https://www.xo.gr/dir-az/W/Warehouses/?lang=en) | [XO warehouses Attica](https://www.xo.gr/dir-az/W/Warehouses/Attica/?lang=en) | A_MINUS | ACCEPT_REVIEW |
| 38 | [XO industrial refrigerators cold storage Greece](https://www.xo.gr/dir-az/R/Refrigerators-Industrial/?lang=en) | [XO industrial refrigerators Greece](https://www.xo.gr/dir-az/R/Refrigerators-Industrial/?lang=en) | [XO cold storage Attica](https://www.xo.gr/dir-az/R/Refrigerators-Industrial/Attica/?lang=en) | A_MINUS | ACCEPT_REVIEW |
| 39 | [Vrisko transport companies Greece](https://www.vrisko.gr/en/dir/transport-companies/) | [Vrisko transport companies Greece](https://www.vrisko.gr/en/dir/transport-companies/) | [Vrisko transport companies Athens](https://www.vrisko.gr/en/dir/transport-companies/athens/) | B_PLUS | ACCEPT_REVIEW |
| 40 | [Vrisko warehouses Greece](https://www.vrisko.gr/en/dir/warehouses/) | [Vrisko warehouses Greece](https://www.vrisko.gr/en/dir/warehouses/) | [Vrisko warehouses Athens](https://www.vrisko.gr/en/dir/warehouses/athens/) | B_PLUS | ACCEPT_REVIEW |
| 41 | [Vrisko logistics Greece search surface](https://www.vrisko.gr/en/search/logistics/greece/) | [Vrisko logistics Greece](https://www.vrisko.gr/en/search/logistics/greece/) | [Vrisko logistics Athens](https://www.vrisko.gr/en/search/logistics/athens/) | B_PLUS | ACCEPT_REVIEW |
| 42 | [Clutch Greece supply-chain and freight forwarding listings](https://clutch.co/gr/logistics/supply-chain-management) | [Clutch supply-chain Greece](https://clutch.co/gr/logistics/supply-chain-management) | [Clutch freight forwarders Greece](https://clutch.co/gr/logistics/freight-forwarders) | B_PLUS | ACCEPT_REVIEW |
| 43 | [Fretador Greece freight forwarding search](https://www.fretador.com/) | [Fretador freight forwarding Greece search](https://www.fretador.com/search/q/Freight-Forwarding/in-Greece) | [Fretador root](https://www.fretador.com/) | B | HOLD_REVIEW |
| 44 | [Agents One freight forwarder directory](https://agentsone.net/directory.php) | [Agents One directory](https://agentsone.net/directory.php) | [Agents One root](https://agentsone.net/) | B | ACCEPT_REVIEW |
| 45 | [SeaRates Greece logistics service reference](https://www.searates.com/reference/logistics-service/greece/) | [SeaRates logistics service Greece](https://www.searates.com/reference/logistics-service/greece/) | [SeaRates port agent Greece](https://www.searates.com/reference/port-agent/greece/) | B_PLUS | ACCEPT_REVIEW |

## Notes

Greek (`el`) remains candidate-only until a future controlled live-probe gate explicitly promotes selected surfaces.  
Global/network directories are used only as candidate source discovery surfaces and require later live review.  
Fretador is intentionally HOLD_REVIEW because it is a marketplace/search surface and should not be promoted without a stronger later probe.
