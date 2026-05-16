# Italian Source-Seed URLs Decision — 2026-05-16

## Scope

This document is the local-only R292 decision record for the Italian (`it`) LogisticSearch source-seed rollout.

R292 creates only this decision document. It does not create the Italian catalog JSON, does not activate any source, does not insert into DB/frontier, does not start crawler runtime, does not mutate systemd, does not sync pi51c, and does not perform URL live probes.

## Canonical rule authority

- Canonical rule doc: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Canonical rule SHA256: `65b36104f039962f3b6c8cd3c70b2575e0de00f27e50732e18953749d89bb49d`
- GitHub raw rule URL used by R292: `https://raw.githubusercontent.com/malikepoglu/logisticsearch/82d96558bcaf427cd5b23a105c158718ed471fbb/docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Sealed HEAD: `82d96558bcaf427cd5b23a105c158718ed471fbb`
- Parent: `8b1dd7173fbdeeb8d1541ba09d95b558b27a61ba`
- Commit subject: `fix(source-seed): standardize rolled startpoint catalogs`

The canonical rule doc must be read from GitHub raw before every language catalog/doc/audit/commit/sync step. Local memory, old chat text, VS Code state, or assumptions are not rule authority.

## Non-touch assertions

- No catalog JSON created in R292.
- No Git add, commit, or push in R292.
- No pi51c sync or pi51c live runtime copy in R292.
- No DB mutation, DB insert, frontier activation, crawler start/stop, systemd mutation, or URL live probe in R292.
- No secret, DSN, token, or password printing.

## Target paths

- Future Italian catalog target: `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json`
- This decision doc target: `docs/TOPIC_CRAWLER_CORE_ITALIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md`

## Italian source-seed plan summary

- Planned source families: 40
- Planned seed surfaces / seed URLs: 84
- All planned URLs are HTTPS candidate URLs.
- All planned URLs are candidate-manifest only and require later pi51c live probe before any DB/frontier/runtime use.
- Directory-first and authority-first preference is preserved: associations, public registries, port authorities, airport cargo surfaces, and interport/freight-village surfaces are prioritized before commercial fallback.

## Architecture boundary

- Crawler_Core collects raw evidence only.
- Crawler_Core-discovered links are raw links, not `added_seeds`.
- Parse_Core may later create candidate `added_seeds` after filtering and pre-ranking.
- Desktop_Import performs stricter validation, enrichment, heavy geocoding/location normalization, and final search-ready output.
- Candidate source-seed catalogs are not live crawler activation.

## Candidate source families

| # | source_code | name | category | quality | decision | seed_url_count | note |
|---:|---|---|---|---|---|---:|---|
| 1 | `it_fiata_directory` | FIATA Italy members directory | global_association_directory | A | ACCEPT_REVIEW | 1 | Italy member directory; shared FIATA host, not separate top-level live source until later gate. |
| 2 | `it_fedespedi` | Fedespedi | freight_forwarding_association | A_PLUS | ACCEPT_REVIEW | 3 | Primary Italian international freight forwarding association candidate. |
| 3 | `it_confetra` | Confetra | transport_logistics_confederation | A | ACCEPT_REVIEW | 3 | Transport and logistics confederation umbrella candidate. |
| 4 | `it_anita` | ANITA | road_transport_association | A_MINUS | ACCEPT_REVIEW | 2 | Road haulage and logistics company association candidate. |
| 5 | `it_albo_autotrasporto` | Albo Autotrasporto | official_road_haulage_registry | A_PLUS | ACCEPT_REVIEW | 2 | Official road haulage registry surface; live usage must be carefully gated. |
| 6 | `it_assologistica` | Assologistica | logistics_association | A_MINUS | ACCEPT_REVIEW | 2 | Italian logistics association candidate. |
| 7 | `it_assoporti` | Assoporti | ports_association | A | ACCEPT_REVIEW | 2 | Italian ports association candidate. |
| 8 | `it_confitarma` | Confitarma | shipping_association | A_MINUS | ACCEPT_REVIEW | 2 | Shipping association candidate. |
| 9 | `it_federagenti` | Federagenti | shipping_agents_association | A_MINUS | ACCEPT_REVIEW | 2 | Maritime agents federation candidate. |
| 10 | `it_assarmatori` | Assarmatori | shipowners_association | A_MINUS | ACCEPT_REVIEW | 2 | Shipowners association candidate. |
| 11 | `it_assiterminal` | Assiterminal | port_terminal_association | A_MINUS | ACCEPT_REVIEW | 2 | Port terminal operators association candidate. |
| 12 | `it_anama_air_cargo` | ANAMA | air_cargo_forwarding_association | A_MINUS | ACCEPT_REVIEW | 2 | Airfreight forwarding association candidate. |
| 13 | `it_unione_interporti_riuniti` | Unione Interporti Riuniti | freight_village_network_association | A_MINUS | ACCEPT_REVIEW | 2 | Interport/freight-village network association candidate. |
| 14 | `it_ports_genoa` | Ports of Genoa | port_authority | A_PLUS | ACCEPT_REVIEW | 2 | Western Ligurian Sea port authority candidate. |
| 15 | `it_port_trieste` | Port of Trieste | port_authority | A_PLUS | ACCEPT_REVIEW | 2 | Northern Adriatic gateway port candidate. |
| 16 | `it_port_laspezia_carrara` | AdSP Mar Ligure Orientale | port_authority | A | ACCEPT_REVIEW | 2 | La Spezia and Marina di Carrara port authority candidate. |
| 17 | `it_port_livorno` | AdSP Mar Tirreno Settentrionale | port_authority | A | ACCEPT_REVIEW | 2 | Livorno and northern Tyrrhenian port authority candidate. |
| 18 | `it_port_venice_chioggia` | Ports of Venice and Chioggia | port_authority | A | ACCEPT_REVIEW | 2 | North Adriatic Sea port authority candidate. |
| 19 | `it_port_ravenna` | Port of Ravenna | port_authority | A | ACCEPT_REVIEW | 2 | Ravenna port authority candidate. |
| 20 | `it_port_gioia_tauro` | Port of Gioia Tauro | port_authority | A | ACCEPT_REVIEW | 2 | Gioia Tauro port authority candidate. |
| 21 | `it_port_naples_salerno` | Ports of Naples and Salerno | port_authority | A | ACCEPT_REVIEW | 2 | Central Tyrrhenian port authority candidate. |
| 22 | `it_port_bari_brindisi` | AdSP Mare Adriatico Meridionale | port_authority | A | ACCEPT_REVIEW | 2 | Southern Adriatic port authority candidate. |
| 23 | `it_port_civitavecchia` | Ports of Rome | port_authority | A | ACCEPT_REVIEW | 2 | Civitavecchia, Fiumicino and Gaeta port authority candidate. |
| 24 | `it_port_taranto` | Port of Taranto | port_authority | A | ACCEPT_REVIEW | 2 | Taranto port authority candidate. |
| 25 | `it_port_ancona` | Port of Ancona | port_authority | A | ACCEPT_REVIEW | 2 | Central Adriatic port authority candidate. |
| 26 | `it_port_sardinia` | AdSP Mare di Sardegna | port_authority | A | ACCEPT_REVIEW | 2 | Sardinian port authority candidate. |
| 27 | `it_port_western_sicily` | AdSP Mare di Sicilia Occidentale | port_authority | A | ACCEPT_REVIEW | 2 | Western Sicily port authority candidate. |
| 28 | `it_port_eastern_sicily` | AdSP Mare di Sicilia Orientale | port_authority | A | ACCEPT_REVIEW | 2 | Eastern Sicily port authority candidate. |
| 29 | `it_malpensa_cargo` | Milano Malpensa Cargo | airport_cargo | A_PLUS | ACCEPT_REVIEW | 4 | Primary air cargo hub candidate; multiple cargo-community surfaces. |
| 30 | `it_adr_cargo` | Aeroporti di Roma Cargo | airport_cargo | A_MINUS | ACCEPT_REVIEW | 2 | Rome airport cargo candidate; live probe required before trust elevation. |
| 31 | `it_bologna_airport_cargo` | Bologna Airport Cargo | airport_cargo | A | ACCEPT_REVIEW | 3 | Bologna cargo and goods transport candidate. |
| 32 | `it_venice_airport_cargo` | Venice Airport Cargo | airport_cargo | B_PLUS | ACCEPT_REVIEW | 2 | Venice air cargo candidate; URL structure must be confirmed by later live probe. |
| 33 | `it_alha_group` | Alha Group | air_cargo_handler | B_PLUS | ACCEPT_REVIEW | 2 | Air cargo handling/trucking ecosystem candidate; commercial source, lower priority than official bodies. |
| 34 | `it_aircargo_italia` | Aircargo Italia | air_cargo_handler | B | ACCEPT_REVIEW | 2 | Air cargo handling/GSSA candidate; commercial source, live check required. |
| 35 | `it_interporto_bologna` | Interporto Bologna | interport_freight_village | A_MINUS | ACCEPT_REVIEW | 2 | Freight village/intermodal node candidate. |
| 36 | `it_interporto_padova` | Interporto Padova | interport_freight_village | A_MINUS | ACCEPT_REVIEW | 2 | Freight village/intermodal node candidate. |
| 37 | `it_quadrante_europa_verona` | Quadrante Europa Verona | interport_freight_village | A_MINUS | ACCEPT_REVIEW | 2 | Verona intermodal/freight village candidate. |
| 38 | `it_cim_novara` | CIM Novara | interport_freight_village | A_MINUS | ACCEPT_REVIEW | 2 | Novara intermodal terminal/freight village candidate. |
| 39 | `it_interporto_toscano` | Interporto Toscano Amerigo Vespucci | interport_freight_village | B_PLUS | ACCEPT_REVIEW | 2 | Tuscan freight village candidate. |
| 40 | `it_interporto_campano` | Interporto Campano | interport_freight_village | B_PLUS | ACCEPT_REVIEW | 2 | Campania freight village candidate. |

## Candidate seed surfaces

| seed_url_index | source_code | url | candidate_manifest | is_live | enabled | needs_live_check | runtime_activation_policy | safety_state |
|---:|---|---|---|---|---|---|---|---|
| 1 | `it_fiata_directory` | `https://fiata.org/directory/it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 2 | `it_fedespedi` | `https://www.fedespedi.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 3 | `it_fedespedi` | `https://www.fedespedi.it/fiata-2/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 4 | `it_fedespedi` | `https://www.fedespedi.it/category/news/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 5 | `it_confetra` | `https://www.confetra.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 6 | `it_confetra` | `https://www.confetra.com/abbreviazioni-comuni-i/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 7 | `it_confetra` | `https://www.confetra.com/category/news/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 8 | `it_anita` | `https://www.anita.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 9 | `it_anita` | `https://www.anita.it/associazione/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 10 | `it_albo_autotrasporto` | `https://www.alboautotrasporto.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 11 | `it_albo_autotrasporto` | `https://www.alboautotrasporto.it/web/portale-albo/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 12 | `it_assologistica` | `https://www.assologistica.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 13 | `it_assologistica` | `https://www.assologistica.it/chi-siamo/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 14 | `it_assoporti` | `https://www.assoporti.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 15 | `it_assoporti` | `https://www.assoporti.it/it/autorita-di-sistema-portuale/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 16 | `it_confitarma` | `https://www.confitarma.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 17 | `it_confitarma` | `https://www.confitarma.it/chi-siamo/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 18 | `it_federagenti` | `https://www.federagenti.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 19 | `it_federagenti` | `https://www.federagenti.it/associazione/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 20 | `it_assarmatori` | `https://www.assarmatori.eu/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 21 | `it_assarmatori` | `https://www.assarmatori.eu/associazione/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 22 | `it_assiterminal` | `https://www.assiterminal.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 23 | `it_assiterminal` | `https://www.assiterminal.it/associazione/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 24 | `it_anama_air_cargo` | `https://www.anama.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 25 | `it_anama_air_cargo` | `https://www.anama.it/chi-siamo/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 26 | `it_unione_interporti_riuniti` | `https://www.unioneinterportiriuniti.org/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 27 | `it_unione_interporti_riuniti` | `https://www.unioneinterportiriuniti.org/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 28 | `it_ports_genoa` | `https://www.portsofgenoa.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 29 | `it_ports_genoa` | `https://www.portsofgenoa.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 30 | `it_port_trieste` | `https://www.porto.trieste.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 31 | `it_port_trieste` | `https://www.porto.trieste.it/eng/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 32 | `it_port_laspezia_carrara` | `https://www.adspmarligureorientale.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 33 | `it_port_laspezia_carrara` | `https://www.adspmarligureorientale.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 34 | `it_port_livorno` | `https://www.portialtotirreno.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 35 | `it_port_livorno` | `https://www.portialtotirreno.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 36 | `it_port_venice_chioggia` | `https://www.port.venice.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 37 | `it_port_venice_chioggia` | `https://www.port.venice.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 38 | `it_port_ravenna` | `https://www.port.ravenna.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 39 | `it_port_ravenna` | `https://www.port.ravenna.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 40 | `it_port_gioia_tauro` | `https://www.portodigioiatauro.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 41 | `it_port_gioia_tauro` | `https://www.portodigioiatauro.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 42 | `it_port_naples_salerno` | `https://www.porto.napoli.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 43 | `it_port_naples_salerno` | `https://www.porto.napoli.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 44 | `it_port_bari_brindisi` | `https://www.adspmam.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 45 | `it_port_bari_brindisi` | `https://www.adspmam.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 46 | `it_port_civitavecchia` | `https://www.portidiroma.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 47 | `it_port_civitavecchia` | `https://www.portidiroma.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 48 | `it_port_taranto` | `https://www.port.taranto.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 49 | `it_port_taranto` | `https://www.port.taranto.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 50 | `it_port_ancona` | `https://www.porto.ancona.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 51 | `it_port_ancona` | `https://www.porto.ancona.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 52 | `it_port_sardinia` | `https://www.adspmaredisardegna.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 53 | `it_port_sardinia` | `https://www.adspmaredisardegna.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 54 | `it_port_western_sicily` | `https://www.adsppalermo.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 55 | `it_port_western_sicily` | `https://www.adsppalermo.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 56 | `it_port_eastern_sicily` | `https://www.adspmaresiciliaorientale.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 57 | `it_port_eastern_sicily` | `https://www.adspmaresiciliaorientale.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 58 | `it_malpensa_cargo` | `https://www.milanomalpensacargo.com/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 59 | `it_malpensa_cargo` | `https://www.milanomalpensacargo.com/en/cargo-city` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 60 | `it_malpensa_cargo` | `https://www.milanomalpensacargo.com/en/flights` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 61 | `it_malpensa_cargo` | `https://www.milanomalpensacargo.com/en/operators` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 62 | `it_adr_cargo` | `https://www.adr.it/web/aeroporti-di-roma-en/cargo` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 63 | `it_adr_cargo` | `https://www.adr.it/web/aeroporti-di-roma-en/business/cargo` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 64 | `it_bologna_airport_cargo` | `https://www.bologna-airport.it/en/the-company/business/aviation/cargo/?idC=62405` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 65 | `it_bologna_airport_cargo` | `https://www.bologna-airport.it/it/la-societa/business/aviation/cargo/?idC=62405` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 66 | `it_bologna_airport_cargo` | `https://www.bologna-airport.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 67 | `it_venice_airport_cargo` | `https://www.veneziaairport.it/en/transport/cargo.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 68 | `it_venice_airport_cargo` | `https://www.veneziaairport.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 69 | `it_alha_group` | `https://alhagroup.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 70 | `it_alha_group` | `https://alhagroup.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 71 | `it_aircargo_italia` | `https://www.aircargoitalia.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 72 | `it_aircargo_italia` | `https://www.aircargoitalia.it/en/about-us/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 73 | `it_interporto_bologna` | `https://www.bo.interporto.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 74 | `it_interporto_bologna` | `https://www.bo.interporto.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 75 | `it_interporto_padova` | `https://www.interportopd.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 76 | `it_interporto_padova` | `https://www.interportopd.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 77 | `it_quadrante_europa_verona` | `https://www.quadranteeuropa.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 78 | `it_quadrante_europa_verona` | `https://www.quadranteeuropa.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 79 | `it_cim_novara` | `https://www.cimspa.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 80 | `it_cim_novara` | `https://www.cimspa.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 81 | `it_interporto_toscano` | `https://www.interportotoscano.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 82 | `it_interporto_toscano` | `https://www.interportotoscano.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 83 | `it_interporto_campano` | `https://www.interportocampano.it/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 84 | `it_interporto_campano` | `https://www.interportocampano.it/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |

## Next gate

After R292 is audited, the next safe gate is expected to be:

`R293_IT_SOURCE_SEED_DECISION_DOC_AUDIT_READONLY`

Only after the decision doc passes audit should a separate local-only Italian catalog JSON creation gate be considered.

## R292 creation metadata

- Created by gate: `R292_IT_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`
- Created at: `2026-05-16T03:46:11+02:00`
- Mutation scope: exactly this decision doc only.
