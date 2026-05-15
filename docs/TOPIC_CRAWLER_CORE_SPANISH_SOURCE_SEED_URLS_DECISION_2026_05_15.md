# TOPIC: Spanish Source Seed URLs Decision - 2026-05-15

## Gate

- Gate: `SOURCE_SEED_R264C_ES_SOURCE_SEED_DECISION_DOC_EXPAND_LOCAL_ONLY_DEDUP_RETRY`
- Language: `es` / Spanish
- Scope: local decision-document rewrite only
- Catalog write: no
- README write: no
- Git add/commit/push/fetch/pull/reset: no
- Pi51c / DB / crawler / systemd / sync / URL fetch / live probe: no
- Runtime policy for future catalog: `candidate_manifest=true`, `is_live=false`, `pi51c_live_probe_required_before_db_or_frontier_insert`

## R264B failure correction

R264B stopped before writing because the seed URL `https://www.feteia.org/ateias.php` appeared more than once. R264C removes that duplicate risk and validates the final seed list as unique before writing this document.

## Quality legend

| Tier | Meaning |
| --- | --- |
| A+ | Official/national/international directory or highly direct member/company surface |
| A | Official association, customs, port, airport, or authority-adjacent source |
| A- | Official or quasi-official community/reference surface, but less direct than A/A+ |
| B+ | Strong industry exhibition or specialized logistics directory fallback |
| B | Broad industry/B2B directory fallback requiring later live check |
| B- | Commercial/editorial fallback; keep disabled and review carefully before activation |

## Compact metrics

- Source families: `45`
- Seed URLs: `95`
- Unique seed URLs: `95`
- Duplicate seed URLs: `0`
- Non-HTTPS seed URLs: `0`
- Directory-first priority: official/member/company directories first, commercial fallbacks last

## Numbered clickable source list

| # | Quality | Source family code | Source | Why candidate |
| ---: | --- | --- | --- | --- |
| 1 | A+ | `es_fiata_spain_member_directory` | [FIATA Spain member directory](https://fiata.org/directory/es/) | International freight-forwarder member directory with Spain country surface. |
| 2 | A+ | `es_feteia_oltra_federation` | [FETEIA-OLTRA Spanish freight forwarder federation](https://www.feteia.org/) | National federation reference for freight forwarding, logistics transport and customs representation. |
| 3 | A | `es_ateia_euskadi_forwarders` | [ATEIA Euskadi freight forwarder association](https://www.ateia-euskadi.org/) | Regional ATEIA association surface connected to FETEIA ecosystem. |
| 4 | A | `es_ateia_barcelona_forwarders` | [ATEIA Barcelona freight forwarder association](https://www.ateia.com/) | Barcelona regional freight forwarder association candidate member surface. |
| 5 | A | `es_ateia_madrid_forwarders` | [ATEIA Madrid freight forwarder association](https://www.ateiamadrid.com/) | Madrid regional freight forwarder association candidate member surface. |
| 6 | A | `es_ateia_valencia_forwarders` | [ATEIA Valencia freight forwarder association](https://www.ateia-valencia.com/) | Valencia regional freight forwarder association candidate member surface. |
| 7 | A | `es_ateia_algeciras_forwarders` | [ATEIA Algeciras freight forwarder association](https://www.ateia-oltra-algeciras.org/) | Algeciras regional freight forwarder association candidate member surface. |
| 8 | A | `es_ateia_aragon_forwarders` | [ATEIA Aragón freight forwarder association](https://www.ateiaaragon.org/) | Aragón regional association and member-surface candidate. |
| 9 | A | `es_ateia_baleares_forwarders` | [ATEIA Baleares freight forwarder association](https://www.ateiabaleares.com/) | Balearic freight forwarder association candidate surface. |
| 10 | A | `es_ateia_galicia_forwarders` | [ATEIA Galicia freight forwarder association](https://www.ateiagalicia.com/) | Galicia regional freight forwarder association candidate surface. |
| 11 | A | `es_ateia_canarias_forwarders` | [ATEIA Canarias freight forwarder association](https://www.ateiacanarias.com/) | Canary Islands regional freight forwarder association candidate surface. |
| 12 | A+ | `es_consejo_aduanas_customs_brokers` | [Spanish customs brokers council](https://www.consejoaduanas.org/) | National customs broker council and official college index candidate. |
| 13 | A | `es_coacab_barcelona_customs_brokers` | [Barcelona customs brokers college](https://www.coacab.com/) | Regional customs broker college candidate directory surface. |
| 14 | A | `es_coacav_valencia_customs_brokers` | [Valencia customs brokers college](https://www.coacav.com/) | Valencia customs broker college candidate member surface. |
| 15 | A | `es_coacam_madrid_customs_brokers` | [Madrid customs brokers college](https://www.coacam.es/) | Madrid customs broker college candidate member surface. |
| 16 | A+ | `es_port_barcelona_business_directory` | [Port of Barcelona business directory](https://www.portdebarcelona.cat/en/web/port-dels-negocis/directori-empreses) | Official port business/company directory surface. |
| 17 | A | `es_valenciaport_services` | [Valenciaport services and port community](https://www.valenciaport.com/en/) | Official port services and port-community reference candidate. |
| 18 | A+ | `es_bilbaoport_directory` | [Port of Bilbao port directory](https://www.bilbaoport.eus/en/services/port-directory/) | Official port directory surface. |
| 19 | A | `es_algeciras_port_services` | [Port of Algeciras services reference](https://www.apba.es/en/) | Official major-port services surface for logistics entity discovery. |
| 20 | A | `es_tarragona_port_services` | [Port of Tarragona services reference](https://www.porttarragona.cat/en/) | Official port services candidate surface. |
| 21 | A | `es_castellon_port_community` | [PortCastelló port community](https://www.portcastello.com/en/) | Official port-community candidate surface. |
| 22 | A | `es_seville_port_community` | [Port of Seville port community](https://www.puertodesevilla.com/en/) | Official port-community candidate surface. |
| 23 | A | `es_vigo_port_services` | [Port of Vigo services reference](https://www.apvigo.es/en/) | Official port services candidate surface. |
| 24 | A | `es_cartagena_port_services` | [Port of Cartagena services reference](https://www.apc.es/webapc/) | Official port services candidate surface. |
| 25 | A | `es_puertos_del_estado_reference` | [Puertos del Estado reference](https://www.puertos.es/) | National public port-system reference surface. |
| 26 | A | `es_aena_air_cargo_surfaces` | [AENA Spanish air-cargo surfaces](https://www.aena.es/en/cargo.html) | Official airport cargo surfaces for Madrid, Barcelona and national cargo discovery. |
| 27 | A- | `es_barcelona_air_cargo_members` | [Barcelona Air Cargo members](https://barcelona-air-cargo.com/) | Airport cargo community and member-surface candidate. |
| 28 | A- | `es_madrid_air_cargo_forum_members` | [Madrid Air Cargo Forum members](https://www.madridaircargoforum.com/) | Airport cargo community and member-surface candidate. |
| 29 | A- | `es_zaragoza_airport_cargo` | [Zaragoza Airport cargo reference](https://www.aena.es/en/zaragoza/airport-services/cargo.html) | Official AENA cargo airport surface for Spain’s freight airport network. |
| 30 | B+ | `es_sil_barcelona_participating_companies` | [SIL Barcelona participating companies](https://www.silbcn.com/en/companies.html) | Major Spanish logistics exhibition participating-company directory. |
| 31 | B+ | `es_logistics_automation_madrid_exhibitors` | [Logistics & Automation Madrid exhibitors](https://www.logisticsautomationmadrid.com/en/exhibitors/) | Spanish logistics exhibition exhibitor directory. |
| 32 | B | `es_empack_madrid_exhibitors` | [Empack Madrid exhibitors](https://www.empackmadrid.com/en/exhibitors/) | Packaging/logistics trade-show exhibitor directory candidate. |
| 33 | B | `es_pickpack_expo_exhibitors` | [Pick&Pack Expo exhibitors](https://www.pickpackexpo.com/exhibitors/) | Supply-chain and packaging event exhibitor directory candidate. |
| 34 | B+ | `es_transport_logistic_exhibitor_directory` | [transport logistic exhibitor directory Spain candidates](https://exhibitors.transportlogistic.de/en/) | International logistics fair exhibitor directory with Spain company coverage. |
| 35 | B+ | `es_azfreight_spain_forwarders` | [AZFreight Spain freight forwarders](https://azfreight.com/country-facility/freight-forwarders-in-spain/) | Industry directory fallback with Spain freight-forwarder country/facility surfaces. |
| 36 | B+ | `es_freightnet_spain_forwarders` | [Freightnet Spain freight forwarders](https://www.freightnet.com/directory/p1/cES/s30.htm) | Industry directory fallback with paginated Spain freight-forwarder surfaces. |
| 37 | B | `es_freightnet_spain_logistics_companies` | [Freightnet Spain logistics companies](https://www.freightnet.com/directory/p1/cES/s99.htm) | Industry directory fallback with Spain logistics-company surfaces. |
| 38 | B | `es_cargoyellowpages_spain` | [CargoYellowPages Spain freight directory](https://www.cargoyellowpages.com/en/spain/) | Cargo and logistics directory fallback for Spain. |
| 39 | B | `es_europages_forwarding_agents` | [Europages Spain forwarding agents](https://www.europages.co.uk/companies/spain/forwarding-agents.html) | B2B directory fallback for Spain forwarding and logistics suppliers. |
| 40 | B | `es_kompass_spain_transport_logistics` | [Kompass Spain transport and logistics](https://es.kompass.com/a/transporte-logistica/75/) | B2B directory fallback with Spain transport/logistics category surfaces. |
| 41 | B- | `es_paginas_amarillas_transport_logistics` | [Páginas Amarillas Spain transport/logistics directory](https://www.paginasamarillas.es/) | General commercial directory fallback; requires later live quality review. |
| 42 | B- | `es_einforma_transport_logistics` | [eInforma Spain transport and logistics directory](https://www.einforma.com/) | Commercial business-information directory fallback; requires later live quality review. |
| 43 | B- | `es_axesor_logistics_transport` | [Axesor Spain logistics and transport directory](https://www.axesor.es/) | Commercial business directory fallback; requires later live quality review. |
| 44 | B- | `es_goodfirms_spain_logistics` | [GoodFirms Spain logistics company directory](https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/spain) | Commercial list fallback; useful only after later live/human review. |
| 45 | B- | `es_freightos_top_forwarders_spain` | [Freightos Spain freight forwarder reference](https://www.freightos.com/freight-resources/top-freight-forwarders-in-spain/) | Editorial/commercial fallback seed for later review, not direct activation. |

## Numbered clickable seed list

| Seed # | Source # | Quality | Seed role | Seed URL |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | A+ | FIATA Spain country directory | [https://fiata.org/directory/es/](https://fiata.org/directory/es/) |
| 2 | 1 | A+ | FIATA global members directory | [https://fiata.org/directory/](https://fiata.org/directory/) |
| 3 | 2 | A+ | FETEIA federation homepage | [https://www.feteia.org/](https://www.feteia.org/) |
| 4 | 2 | A+ | FETEIA federation profile | [https://www.feteia.org/quienes-somos/](https://www.feteia.org/quienes-somos/) |
| 5 | 3 | A | ATEIA Euskadi homepage | [https://www.ateia-euskadi.org/](https://www.ateia-euskadi.org/) |
| 6 | 3 | A | ATEIA Euskadi FETEIA reference | [https://www.ateia-euskadi.org/en-feteia](https://www.ateia-euskadi.org/en-feteia) |
| 7 | 4 | A | ATEIA Barcelona homepage | [https://www.ateia.com/](https://www.ateia.com/) |
| 8 | 4 | A | ATEIA Barcelona associates candidate | [https://www.ateia.com/asociados/](https://www.ateia.com/asociados/) |
| 9 | 5 | A | ATEIA Madrid homepage | [https://www.ateiamadrid.com/](https://www.ateiamadrid.com/) |
| 10 | 5 | A | ATEIA Madrid associates candidate | [https://www.ateiamadrid.com/asociados/](https://www.ateiamadrid.com/asociados/) |
| 11 | 6 | A | ATEIA Valencia homepage | [https://www.ateia-valencia.com/](https://www.ateia-valencia.com/) |
| 12 | 6 | A | ATEIA Valencia associates candidate | [https://www.ateia-valencia.com/asociados/](https://www.ateia-valencia.com/asociados/) |
| 13 | 7 | A | ATEIA Algeciras homepage | [https://www.ateia-oltra-algeciras.org/](https://www.ateia-oltra-algeciras.org/) |
| 14 | 7 | A | ATEIA Algeciras associates candidate | [https://www.ateia-oltra-algeciras.org/asociados/](https://www.ateia-oltra-algeciras.org/asociados/) |
| 15 | 8 | A | ATEIA Aragón homepage | [https://www.ateiaaragon.org/](https://www.ateiaaragon.org/) |
| 16 | 8 | A | ATEIA Aragón associates candidate | [https://www.ateiaaragon.org/asociados/](https://www.ateiaaragon.org/asociados/) |
| 17 | 9 | A | ATEIA Baleares homepage | [https://www.ateiabaleares.com/](https://www.ateiabaleares.com/) |
| 18 | 9 | A | ATEIA Baleares associates candidate | [https://www.ateiabaleares.com/asociados/](https://www.ateiabaleares.com/asociados/) |
| 19 | 10 | A | ATEIA Galicia homepage | [https://www.ateiagalicia.com/](https://www.ateiagalicia.com/) |
| 20 | 10 | A | ATEIA Galicia associates candidate | [https://www.ateiagalicia.com/asociados/](https://www.ateiagalicia.com/asociados/) |
| 21 | 11 | A | ATEIA Canarias homepage | [https://www.ateiacanarias.com/](https://www.ateiacanarias.com/) |
| 22 | 11 | A | ATEIA Canarias associates candidate | [https://www.ateiacanarias.com/asociados/](https://www.ateiacanarias.com/asociados/) |
| 23 | 12 | A+ | Customs brokers council homepage | [https://www.consejoaduanas.org/](https://www.consejoaduanas.org/) |
| 24 | 12 | A+ | Customs broker colleges candidate | [https://www.consejoaduanas.org/colegios/](https://www.consejoaduanas.org/colegios/) |
| 25 | 13 | A | COACAB homepage | [https://www.coacab.com/](https://www.coacab.com/) |
| 26 | 13 | A | COACAB members candidate | [https://www.coacab.com/colegiados/](https://www.coacab.com/colegiados/) |
| 27 | 14 | A | COACAV homepage | [https://www.coacav.com/](https://www.coacav.com/) |
| 28 | 14 | A | COACAV members candidate | [https://www.coacav.com/colegiados/](https://www.coacav.com/colegiados/) |
| 29 | 15 | A | COACAM homepage | [https://www.coacam.es/](https://www.coacam.es/) |
| 30 | 15 | A | COACAM members candidate | [https://www.coacam.es/colegiados/](https://www.coacam.es/colegiados/) |
| 31 | 16 | A+ | Port of Barcelona company directory | [https://www.portdebarcelona.cat/en/web/port-dels-negocis/directori-empreses](https://www.portdebarcelona.cat/en/web/port-dels-negocis/directori-empreses) |
| 32 | 16 | A+ | Port of Barcelona business area | [https://www.portdebarcelona.cat/en/business](https://www.portdebarcelona.cat/en/business) |
| 33 | 17 | A | Valenciaport English homepage | [https://www.valenciaport.com/en/](https://www.valenciaport.com/en/) |
| 34 | 17 | A | Valenciaport port services | [https://www.valenciaport.com/en/port-services/](https://www.valenciaport.com/en/port-services/) |
| 35 | 18 | A+ | Port of Bilbao directory | [https://www.bilbaoport.eus/en/services/port-directory/](https://www.bilbaoport.eus/en/services/port-directory/) |
| 36 | 18 | A+ | Port of Bilbao English homepage | [https://www.bilbaoport.eus/en/](https://www.bilbaoport.eus/en/) |
| 37 | 19 | A | Port of Algeciras English homepage | [https://www.apba.es/en/](https://www.apba.es/en/) |
| 38 | 19 | A | Port of Algeciras services | [https://www.apba.es/en/port-services/](https://www.apba.es/en/port-services/) |
| 39 | 20 | A | Port of Tarragona English homepage | [https://www.porttarragona.cat/en/](https://www.porttarragona.cat/en/) |
| 40 | 20 | A | Port of Tarragona services | [https://www.porttarragona.cat/en/services](https://www.porttarragona.cat/en/services) |
| 41 | 21 | A | PortCastelló English homepage | [https://www.portcastello.com/en/](https://www.portcastello.com/en/) |
| 42 | 21 | A | PortCastelló port community | [https://www.portcastello.com/en/port-community](https://www.portcastello.com/en/port-community) |
| 43 | 22 | A | Port of Seville English homepage | [https://www.puertodesevilla.com/en/](https://www.puertodesevilla.com/en/) |
| 44 | 22 | A | Port of Seville port community | [https://www.puertodesevilla.com/en/port-community](https://www.puertodesevilla.com/en/port-community) |
| 45 | 23 | A | Port of Vigo English homepage | [https://www.apvigo.es/en/](https://www.apvigo.es/en/) |
| 46 | 23 | A | Port of Vigo services | [https://www.apvigo.es/en/port-services](https://www.apvigo.es/en/port-services) |
| 47 | 24 | A | Port of Cartagena homepage | [https://www.apc.es/webapc/](https://www.apc.es/webapc/) |
| 48 | 24 | A | Port of Cartagena services | [https://www.apc.es/webapc/servicios/](https://www.apc.es/webapc/servicios/) |
| 49 | 25 | A | Puertos del Estado homepage | [https://www.puertos.es/](https://www.puertos.es/) |
| 50 | 25 | A | Puertos del Estado English surface | [https://www.puertos.es/en-us/Pages/default.aspx](https://www.puertos.es/en-us/Pages/default.aspx) |
| 51 | 26 | A | AENA cargo overview | [https://www.aena.es/en/cargo.html](https://www.aena.es/en/cargo.html) |
| 52 | 26 | A | Madrid Barajas cargo | [https://www.aena.es/en/adolfo-suarez-madrid-barajas/airport-services/cargo.html](https://www.aena.es/en/adolfo-suarez-madrid-barajas/airport-services/cargo.html) |
| 53 | 26 | A | Barcelona El Prat cargo | [https://www.aena.es/en/josep-tarradellas-barcelona-el-prat/airport-services/cargo.html](https://www.aena.es/en/josep-tarradellas-barcelona-el-prat/airport-services/cargo.html) |
| 54 | 27 | A- | Barcelona Air Cargo homepage | [https://barcelona-air-cargo.com/](https://barcelona-air-cargo.com/) |
| 55 | 27 | A- | Barcelona Air Cargo members | [https://barcelona-air-cargo.com/en/members/](https://barcelona-air-cargo.com/en/members/) |
| 56 | 28 | A- | Madrid Air Cargo Forum homepage | [https://www.madridaircargoforum.com/](https://www.madridaircargoforum.com/) |
| 57 | 28 | A- | Madrid Air Cargo Forum members candidate | [https://www.madridaircargoforum.com/socios/](https://www.madridaircargoforum.com/socios/) |
| 58 | 29 | A- | Zaragoza airport cargo | [https://www.aena.es/en/zaragoza/airport-services/cargo.html](https://www.aena.es/en/zaragoza/airport-services/cargo.html) |
| 59 | 29 | A- | Zaragoza cargo destinations candidate | [https://www.aena.es/en/zaragoza/airlines-and-destinations/cargo.html](https://www.aena.es/en/zaragoza/airlines-and-destinations/cargo.html) |
| 60 | 30 | B+ | SIL Barcelona participating companies | [https://www.silbcn.com/en/companies.html](https://www.silbcn.com/en/companies.html) |
| 61 | 30 | B+ | SIL Barcelona homepage | [https://www.silbcn.com/en/](https://www.silbcn.com/en/) |
| 62 | 31 | B+ | Logistics & Automation Madrid exhibitors | [https://www.logisticsautomationmadrid.com/en/exhibitors/](https://www.logisticsautomationmadrid.com/en/exhibitors/) |
| 63 | 31 | B+ | Logistics & Automation Madrid homepage | [https://www.logisticsautomationmadrid.com/en/](https://www.logisticsautomationmadrid.com/en/) |
| 64 | 32 | B | Empack Madrid exhibitors | [https://www.empackmadrid.com/en/exhibitors/](https://www.empackmadrid.com/en/exhibitors/) |
| 65 | 32 | B | Empack Madrid homepage | [https://www.empackmadrid.com/en/](https://www.empackmadrid.com/en/) |
| 66 | 33 | B | Pick&Pack exhibitors | [https://www.pickpackexpo.com/exhibitors/](https://www.pickpackexpo.com/exhibitors/) |
| 67 | 33 | B | Pick&Pack homepage | [https://www.pickpackexpo.com/](https://www.pickpackexpo.com/) |
| 68 | 34 | B+ | transport logistic exhibitor database | [https://exhibitors.transportlogistic.de/en/](https://exhibitors.transportlogistic.de/en/) |
| 69 | 34 | B+ | transport logistic exhibitor directory hub | [https://transportlogistic.de/en/trade-fair/exhibitors-products/exhibitor-directory/](https://transportlogistic.de/en/trade-fair/exhibitors-products/exhibitor-directory/) |
| 70 | 35 | B+ | AZFreight Spain country page | [https://azfreight.com/country/spain/](https://azfreight.com/country/spain/) |
| 71 | 35 | B+ | AZFreight freight forwarders in Spain | [https://azfreight.com/country-facility/freight-forwarders-in-spain/](https://azfreight.com/country-facility/freight-forwarders-in-spain/) |
| 72 | 36 | B+ | Freightnet Spain forwarders page 1 | [https://www.freightnet.com/directory/p1/cES/s30.htm](https://www.freightnet.com/directory/p1/cES/s30.htm) |
| 73 | 36 | B+ | Freightnet Spain forwarders page 2 | [https://www.freightnet.com/directory/p2/cES/s30.htm](https://www.freightnet.com/directory/p2/cES/s30.htm) |
| 74 | 36 | B+ | Freightnet Spain forwarders page 3 | [https://www.freightnet.com/directory/p3/cES/s30.htm](https://www.freightnet.com/directory/p3/cES/s30.htm) |
| 75 | 36 | B+ | Freightnet Spain air freight forwarders | [https://www.freightnet.com/directory/p1/cES/s31.htm](https://www.freightnet.com/directory/p1/cES/s31.htm) |
| 76 | 37 | B | Freightnet Spain logistics page 1 | [https://www.freightnet.com/directory/p1/cES/s99.htm](https://www.freightnet.com/directory/p1/cES/s99.htm) |
| 77 | 37 | B | Freightnet Spain logistics page 2 | [https://www.freightnet.com/directory/p2/cES/s99.htm](https://www.freightnet.com/directory/p2/cES/s99.htm) |
| 78 | 37 | B | Freightnet Spain logistics page 3 | [https://www.freightnet.com/directory/p3/cES/s99.htm](https://www.freightnet.com/directory/p3/cES/s99.htm) |
| 79 | 38 | B | CargoYellowPages Spain | [https://www.cargoyellowpages.com/en/spain/](https://www.cargoyellowpages.com/en/spain/) |
| 80 | 38 | B | CargoYellowPages mobile Spain | [https://mobile.cargoyellowpages.com/spain/](https://mobile.cargoyellowpages.com/spain/) |
| 81 | 39 | B | Europages Spain forwarding agents | [https://www.europages.co.uk/companies/spain/forwarding-agents.html](https://www.europages.co.uk/companies/spain/forwarding-agents.html) |
| 82 | 39 | B | Europages Spain transport and logistics | [https://www.europages.co.uk/companies/spain/transport%20and%20logistics.html](https://www.europages.co.uk/companies/spain/transport%20and%20logistics.html) |
| 83 | 40 | B | Kompass Spain transport logistics category | [https://es.kompass.com/a/transporte-logistica/75/](https://es.kompass.com/a/transporte-logistica/75/) |
| 84 | 40 | B | Kompass Spain transport logistics search | [https://es.kompass.com/s/transporte-logistica/10/](https://es.kompass.com/s/transporte-logistica/10/) |
| 85 | 40 | B | Kompass Spain logistics services | [https://es.kompass.com/a/servicios-logisticos/80690/](https://es.kompass.com/a/servicios-logisticos/80690/) |
| 86 | 41 | B- | Páginas Amarillas transport logistics search | [https://www.paginasamarillas.es/search/transporte-logistica/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1](https://www.paginasamarillas.es/search/transporte-logistica/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1) |
| 87 | 41 | B- | Páginas Amarillas transport agencies search | [https://www.paginasamarillas.es/search/agencias-de-transporte/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1](https://www.paginasamarillas.es/search/agencias-de-transporte/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1) |
| 88 | 42 | B- | eInforma transport and logistics companies | [https://www.einforma.com/servlet/app/portal/ENTP/prod/ETIQUETA_EMPRESAS/etiqueta/transportes-y-logistica](https://www.einforma.com/servlet/app/portal/ENTP/prod/ETIQUETA_EMPRESAS/etiqueta/transportes-y-logistica) |
| 89 | 42 | B- | eInforma company information portal | [https://www.einforma.com/informacion-empresa](https://www.einforma.com/informacion-empresa) |
| 90 | 43 | B- | Axesor logistics companies | [https://www.axesor.es/directorio-informacion-empresas/empresas-de-logistica](https://www.axesor.es/directorio-informacion-empresas/empresas-de-logistica) |
| 91 | 43 | B- | Axesor transport companies | [https://www.axesor.es/directorio-informacion-empresas/empresas-de-transporte](https://www.axesor.es/directorio-informacion-empresas/empresas-de-transporte) |
| 92 | 44 | B- | GoodFirms Spain freight forwarding | [https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/spain](https://www.goodfirms.co/supply-chain-logistics-companies/freight-forwarding/spain) |
| 93 | 44 | B- | GoodFirms Spain supply-chain logistics | [https://www.goodfirms.co/supply-chain-logistics-companies/spain](https://www.goodfirms.co/supply-chain-logistics-companies/spain) |
| 94 | 45 | B- | Freightos top forwarders Spain | [https://www.freightos.com/freight-resources/top-freight-forwarders-in-spain/](https://www.freightos.com/freight-resources/top-freight-forwarders-in-spain/) |
| 95 | 45 | B- | Freightos freight resources | [https://www.freightos.com/freight-resources/](https://www.freightos.com/freight-resources/) |

## Future catalog creation requirements

When this decision document passes read-only audit, the next catalog creation gate must create only:

`makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json`

Required future catalog guards:

- `schema=source_families_v2`
- `schema_version=source_families_v2`
- `catalog_version=spanish_source_families_v2`
- `language_code=es`
- `candidate_manifest=true`
- `is_live=false`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- no DB insert
- no frontier activation
- no URL fetch/live probe during catalog creation
- all source/seed surfaces remain candidate-only until a separate live-check gate

## Final decision

Spanish source-seed decision document is expanded and ready for read-only audit.

Next gate: `SOURCE_SEED_R265_ES_SOURCE_SEED_DECISION_DOC_AUDIT_READONLY`
