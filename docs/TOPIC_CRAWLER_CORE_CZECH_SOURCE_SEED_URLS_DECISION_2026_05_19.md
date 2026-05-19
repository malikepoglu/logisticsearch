# TOPIC — Czech Source Seed URLs Decision — 2026-05-19

## Gate

CS-02R2 — CS_SOURCE_SEED_DECISION_DOC_AND_CATALOG_LOCAL_ONLY_R2

## Scope

Language: Czech  
Language code: cs  
Catalog target: makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json  
Decision doc target: docs/TOPIC_CRAWLER_CORE_CZECH_SOURCE_SEED_URLS_DECISION_2026_05_19.md

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

## Decision summary

- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Duplicate seed URLs: 0
- Non-HTTPS seed URLs: 0
- Directory-first policy: applied
- Single-company homepages as primary startpoints: avoided
- Blog/listicle pages as primary startpoints: avoided

## Quality distribution

- A: 8
- A_MINUS: 14
- A_PLUS: 5
- B: 5
- B_PLUS: 13

## Decision distribution

- ACCEPT: 11
- ACCEPT_REVIEW: 33
- HOLD_REVIEW: 1

## Numbered source and seed list

| No | Source family link | Seed-1 link | Seed-2 link | Quality | Decision |
|---:|---|---|---|---|---|
| 1 | [SSL / Svaz spedice a logistiky ČR members](https://www.svazspedice.cz/) | [SSL — Seznam členů](https://www.svazspedice.cz/index.php/seznam-clenu-2/) | [SSL — Kontakty](https://www.svazspedice.cz/index.php/kontakty/) | A_PLUS | ACCEPT |
| 2 | [SSL membership / statutes / association policy](https://www.svazspedice.cz/index.php/dokumenty/) | [SSL — Přihláška za člena](https://www.svazspedice.cz/index.php/prihlaska-za-clena/) | [SSL — Stanovy SSL](https://www.svazspedice.cz/index.php/stanovy-ssl/) | A | ACCEPT_REVIEW |
| 3 | [FIATA Czech Republic member directory](https://fiata.org/directory/) | [FIATA — Czech Republic members](https://fiata.org/directory/cz/) | [FIATA — Directory root](https://fiata.org/directory/) | A_PLUS | ACCEPT |
| 4 | [IRU / CESMAD Bohemia road transport association reference](https://www.iru.org/news-resources/members-directory) | [IRU — CESMAD Bohemia](https://www.iru.org/news-resources/members-directory/cesmad-bohemia) | [IRU — Members directory](https://www.iru.org/news-resources/members-directory) | A_MINUS | ACCEPT_REVIEW |
| 5 | [Czech road transport operator registry search](https://rpsd.mdcr.cz/undertaker/search) | [RPSD — Search operator](https://rpsd.mdcr.cz/undertaker/search) | [Ministry of Transport CZ](https://md.gov.cz/?lang=en-gb) | A | ACCEPT_REVIEW |
| 6 | [Česká logistická asociace](https://czech-logistics.eu/) | [CLA — About us](https://czech-logistics.eu/en/about-us/) | [CLA root](https://czech-logistics.eu/) | B_PLUS | ACCEPT_REVIEW |
| 7 | [Firmy.cz logistic services category](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services) | [Firmy.cz — Logistic services CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services) | [Firmy.cz — Logistic services page 2](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services?page=2) | A_PLUS | ACCEPT |
| 8 | [Firmy.cz forwarding category](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Forwarding) | [Firmy.cz — Forwarding CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Forwarding) | [Firmy.cz — Forwarding page 2](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Forwarding?page=2) | A_PLUS | ACCEPT |
| 9 | [Firmy.cz transport and transportation root](https://en.firmy.cz/Travel-services/Transport-and-transportation) | [Firmy.cz — Transport and transportation](https://en.firmy.cz/Travel-services/Transport-and-transportation) | [Firmy.cz — Travel services root](https://en.firmy.cz/Travel-services) | A | ACCEPT |
| 10 | [Firmy.cz regional logistics Prague / Central Bohemia](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-praha) | [Firmy.cz — Logistic services Prague](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-praha) | [Firmy.cz — Logistic services Central Bohemian Region](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-stredocesky?page=3) | A | ACCEPT |
| 11 | [Firmy.cz regional logistics South Bohemia / Hradec Králové](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-jihocesky/ceske-budejovice?page=2) | [Firmy.cz — České Budějovice logistics](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-jihocesky/ceske-budejovice?page=2) | [Firmy.cz — Hradec Králové logistics](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-kralovehradecky/hradec-kralove) | A_MINUS | ACCEPT_REVIEW |
| 12 | [Firmy.cz regional logistics Liberec / Říkov](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-liberecky/liberec) | [Firmy.cz — Liberec logistics](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-liberecky/liberec) | [Firmy.cz — Říkov logistics](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/kraj-kralovehradecky/nachod/221-rikov) | A_MINUS | ACCEPT_REVIEW |
| 13 | [Firmy.cz road freight category](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport) | [Firmy.cz — Road freight CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport) | [Firmy.cz — Other freight carriers](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Other-freight-carriers) | A_PLUS | ACCEPT |
| 14 | [Firmy.cz road haulage category](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Road-haulage) | [Firmy.cz — Road haulage CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Road-haulage) | [Firmy.cz — Road haulage Brandýs nad Labem](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Road-haulage/kraj-stredocesky/praha-vychod/4152-brandys-nad-labem-stara-boleslav) | A | ACCEPT |
| 15 | [Firmy.cz international road haulage category](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Other-freight-carriers/International-road-haulage-carriers) | [Firmy.cz — International road haulage CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Other-freight-carriers/International-road-haulage-carriers) | [Firmy.cz — International haulage Mělník](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Other-freight-carriers/International-road-haulage-carriers/kraj-stredocesky/melnik) | A | ACCEPT |
| 16 | [Firmy.cz temperature-controlled transport](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Temperature-controlled-transport) | [Firmy.cz — Temperature-controlled transport CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Temperature-controlled-transport) | [Firmy.cz — Temperature-controlled transport page 2](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Temperature-controlled-transport?page=2) | A_MINUS | ACCEPT_REVIEW |
| 17 | [Firmy.cz oversized loads transport](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Transport-of-oversized-loads) | [Firmy.cz — Oversized loads CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Transport-of-oversized-loads) | [Firmy.cz — Oversized loads Olomouc Region](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Transport-of-oversized-loads/kraj-olomoucky) | A_MINUS | ACCEPT_REVIEW |
| 18 | [Firmy.cz container transport](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Container-transport) | [Firmy.cz — Container transport CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Container-transport) | [Firmy.cz — Container transport Plzeň](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Container-transport/kraj-plzensky/plzen-mesto) | B_PLUS | ACCEPT_REVIEW |
| 19 | [Firmy.cz van transport](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Van-transport) | [Firmy.cz — Van transport CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Van-transport) | [Firmy.cz — Van transport Plzeň page 2](https://en.firmy.cz/Travel-services/Transport-and-transportation/Road-freight-transport/Van-transport/kraj-plzensky/plzen-mesto?page=2) | B_PLUS | ACCEPT_REVIEW |
| 20 | [Firmy.cz air freight transport](https://en.firmy.cz/Travel-services/Transport-and-transportation/Air-carriers/Air-freight-transport) | [Firmy.cz — Air freight transport CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Air-carriers/Air-freight-transport) | [Firmy.cz — Air carriers root](https://en.firmy.cz/Travel-services/Transport-and-transportation/Air-carriers) | A_MINUS | ACCEPT_REVIEW |
| 21 | [Firmy.cz courier service](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service) | [Firmy.cz — Courier service CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service) | [Firmy.cz — Courier service page 6](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service?page=6) | B_PLUS | ACCEPT_REVIEW |
| 22 | [Firmy.cz national courier service](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service/National-courier-service) | [Firmy.cz — National courier service CZ](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service/National-courier-service) | [Firmy.cz — National courier service Prague](https://en.firmy.cz/Travel-services/Transport-and-transportation/Logistic-services/Courier-service/National-courier-service/kraj-praha) | B_PLUS | ACCEPT_REVIEW |
| 23 | [Firmy.cz customs clearance services root](https://en.firmy.cz/Travel-services/Customs-clearance-services) | [Firmy.cz — Customs clearance services CZ](https://en.firmy.cz/Travel-services/Customs-clearance-services) | [Firmy.cz — Customs clearance services Prague](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-praha) | A | ACCEPT |
| 24 | [Firmy.cz customs clearance category](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-clearance) | [Firmy.cz — Customs clearance CZ](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-clearance) | [Firmy.cz — Customs clearance page 2](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-clearance?page=2) | A | ACCEPT |
| 25 | [Firmy.cz customs bonded warehouses](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-bonded-warehouses) | [Firmy.cz — Customs bonded warehouses CZ](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-bonded-warehouses) | [Firmy.cz — Customs bonded warehouses Brno](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-bonded-warehouses/kraj-jihomoravsky/brno-mesto) | A_MINUS | ACCEPT_REVIEW |
| 26 | [Firmy.cz customs clearance Brno region](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-jihomoravsky/brno-mesto) | [Firmy.cz — Customs clearance Brno](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-jihomoravsky/brno-mesto) | [Firmy.cz — Customs bonded warehouses Prague](https://en.firmy.cz/Travel-services/Customs-clearance-services/Customs-bonded-warehouses/kraj-praha) | A_MINUS | ACCEPT_REVIEW |
| 27 | [Firmy.cz customs Prague-West / airport area](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-stredocesky/praha-zapad/4294-tuchomerice) | [Firmy.cz — Customs Tuchoměřice](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-stredocesky/praha-zapad/4294-tuchomerice) | [Firmy.cz — Customs Srbeč / Central Bohemian](https://en.firmy.cz/Travel-services/Customs-clearance-services/kraj-stredocesky/rakovnik/4360-srbec) | A_MINUS | ACCEPT_REVIEW |
| 28 | [Firmy.cz warehousing services](https://en.firmy.cz/top/All-for-business/Business-services/Warehousing-services) | [Firmy.cz — Warehousing services ranking](https://en.firmy.cz/top/All-for-business/Business-services/Warehousing-services) | [Firmy.cz — Business services root](https://en.firmy.cz/All-for-business/Business-services) | B_PLUS | ACCEPT_REVIEW |
| 29 | [Kompass Czech business and forwarding directory](https://www.kompass.com/businessplace/z/cz/) | [Kompass — Czech business directory](https://www.kompass.com/businessplace/z/cz/) | [Kompass — Shipping and forwarding agents CZ](https://www.kompass.com/z/cz/a/shipping-and-forwarding-agents/75780/) | A_MINUS | ACCEPT_REVIEW |
| 30 | [Freightnet Czech freight and logistics directory](https://www.freightnet.com/directory/) | [Freightnet — Freight forwarders Czech Rep](https://www.freightnet.com/directory/p1/cCZ/s30.htm) | [Freightnet — Freight/logistics Czech Rep](https://www.freightnet.com/directory/p1/cCZ/s99.htm) | A_MINUS | ACCEPT_REVIEW |
| 31 | [CargoYellowPages Czech Republic freight directory](https://www.cargoyellowpages.com/) | [CargoYellowPages — Czech Republic](https://www.cargoyellowpages.com/en/czech-republic/) | [CargoYellowPages root](https://www.cargoyellowpages.com/) | A_MINUS | ACCEPT_REVIEW |
| 32 | [AZFreight Czech freight forwarders](https://azfreight.com/) | [AZFreight — Freight forwarders in Czech Republic](https://azfreight.com/country-facility/freight-forwarders-in-czech-republic/) | [AZFreight — Countries root](https://azfreight.com/countries/) | A_MINUS | ACCEPT_REVIEW |
| 33 | [JCtrans Czech freight forwarder network list](https://www.jctrans.com/en/company/) | [JCtrans — Czech Republic forwarders](https://m.jctrans.com/en/company/listc/Czech%20Republic/0-0) | [JCtrans — Company list root](https://www.jctrans.com/en/company/) | B_PLUS | ACCEPT_REVIEW |
| 34 | [Ruzave Czech freight and warehouse directory](https://ruzave.com/czech-republic) | [Ruzave — Czech Republic freight directory](https://ruzave.com/czech-republic) | [Ruzave — Top warehouse companies CZ](https://ruzave.com/czech-republic/top-warehouse-companies/) | B_PLUS | ACCEPT_REVIEW |
| 35 | [Railmarket Czech logistics companies](https://railmarket.com/eu/czech-republic/logistics-companies) | [Railmarket — Logistics companies CZ](https://railmarket.com/eu/czech-republic/logistics-companies) | [Railmarket — Rail forwarders CZ](https://railmarket.com/eu/czech-republic/rail-forwarders) | A_MINUS | ACCEPT_REVIEW |
| 36 | [Railmarket Czech railway and logistics consulting companies](https://railmarket.com/eu/czech-republic/companies) | [Railmarket — Railway companies CZ](https://railmarket.com/eu/czech-republic/companies) | [Railmarket — Logistics consulting CZ](https://railmarket.com/eu/czech-republic/logistics-consulting) | B_PLUS | ACCEPT_REVIEW |
| 37 | [Overseas Project Cargo Czech freight forwarders](https://overseasprojectcargo.com/) | [OPCA — Czech freight forwarders](https://overseasprojectcargo.com/InternationalFreightForwarders/czech-republic-freight-forwarders/) | [OPCA — International freight forwarders root](https://overseasprojectcargo.com/InternationalFreightForwarders/) | B_PLUS | ACCEPT_REVIEW |
| 38 | [Pangea Network Czech freight forwarders](https://pangea-network.com/) | [Pangea — Czech Republic freight forwarders](https://pangea-network.com/freight-forwarders/czech-republic/) | [Pangea — Members/network root](https://pangea-network.com/) | B_PLUS | ACCEPT_REVIEW |
| 39 | [WCAworld global freight forwarder directory](https://www.wcaworld.com/directory) | [WCAworld — Directory](https://www.wcaworld.com/directory) | [WCAworld root](https://www.wcaworld.com/) | B_PLUS | ACCEPT_REVIEW |
| 40 | [ForwardingCompanies SSL association mirror](https://forwardingcompanies.com/) | [ForwardingCompanies — SSL members mirror](https://forwardingcompanies.com/association/association-of-forwarding-and-logistics-of-the-czech-republic-ssl-) | [ForwardingCompanies root](https://forwardingcompanies.com/) | B | ACCEPT_REVIEW |
| 41 | [Clutch Czech logistics and freight forwarder listings](https://clutch.co/cz/logistics/supply-chain-management) | [Clutch — Czech supply chain companies](https://clutch.co/cz/logistics/supply-chain-management) | [Clutch — Czech freight forwarders](https://clutch.co/cz/logistics/freight-forwarders) | B | ACCEPT_REVIEW |
| 42 | [Ensun Czechia freight trucking search](https://ensun.io/search/freight-trucking/czechia) | [Ensun — Freight trucking Czechia](https://ensun.io/search/freight-trucking/czechia) | [Ensun — Logistics search Czechia](https://ensun.io/search/logistics/czechia) | B | ACCEPT_REVIEW |
| 43 | [SeaRates Czech logistics service reference](https://www.searates.com/) | [SeaRates — Logistics service Czech Republic](https://www.searates.com/de/reference/logistics-service/czech_republic/) | [SeaRates reference root](https://www.searates.com/reference/) | B | ACCEPT_REVIEW |
| 44 | [Aerocean Network members directory](https://aeroceanetwork.net/directory/) | [Aerocean — Members directory](https://aeroceanetwork.net/directory/) | [Aerocean root](https://aeroceanetwork.net/) | B_PLUS | ACCEPT_REVIEW |
| 45 | [Fretador Czech freight forwarding marketplace search](https://www.fretador.com/) | [Fretador — Czech freight forwarding search](https://www.fretador.com/search/q/Freight-Forwarding/to-Germany/in-Czech-Republic?member=262-International-Chamber-of-Commerce-Czech-Republic-ICC) | [Fretador root](https://www.fretador.com/) | B | HOLD_REVIEW |

## Notes

Global/network directories remain candidate-only and require a future live probe gate before any DB/frontier promotion.  
Firmy.cz regional/category surfaces are used as Czech-local directory coverage, not as proof of live reachability.  
Fretador is intentionally HOLD_REVIEW because it is a marketplace/search surface and should not be promoted without a stronger later probe.
