# Portuguese Source-Seed URLs Decision — 2026-05-16

## Scope

This document is the local-only R305 decision record for the Portuguese (`pt`) LogisticSearch source-seed rollout.

R305 creates only this decision document. It does not create the Portuguese catalog JSON, does not activate any source, does not insert into DB/frontier, does not start crawler runtime, does not mutate systemd, does not sync pi51c, and does not perform URL live probes.

## Canonical rule authority

- Canonical rule doc: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Canonical rule SHA256: `65b36104f039962f3b6c8cd3c70b2575e0de00f27e50732e18953749d89bb49d`
- GitHub raw rule URL used by R305: `https://raw.githubusercontent.com/malikepoglu/logisticsearch/1987530b93ccb88a77fabc9178431494f9843527/docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Sealed HEAD: `1987530b93ccb88a77fabc9178431494f9843527`
- Parent: `2e89fa2a65894dd605f6f5d0e4e4a958cb0d98be`
- Commit subject: `docs(source-seed): index Italian startpoint catalog`

The canonical rule doc must be read from GitHub raw before every language catalog/doc/audit/commit/sync step. Local memory, old chat text, editor state, or copied snippets are not rule authority.

## Non-touch assertions

- No catalog JSON created in R305.
- No Git add, commit, or push in R305.
- No pi51c sync or pi51c live runtime copy in R305.
- No DB mutation, DB insert, frontier activation, crawler start/stop, systemd mutation, or URL live probe in R305.
- No secret, DSN, token, or password printing.

## Target paths

- Future Portuguese catalog target: `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json`
- This decision doc target: `docs/TOPIC_CRAWLER_CORE_PORTUGUESE_SOURCE_SEED_URLS_DECISION_2026_05_16.md`

## Portuguese source-seed plan summary

- Planned source families: 40
- Planned seed surfaces / seed URLs: 84
- All planned URLs are HTTPS candidate URLs.
- All planned URLs are candidate-manifest only and require later pi51c live probe before any DB/frontier/runtime use.
- Authority-first preference is preserved: associations, official authorities, port authorities, airport/cargo surfaces, rail/intermodal and terminal surfaces come before commercial fallback directories.

## Architecture boundary

- Crawler_Core collects raw evidence only.
- Crawler_Core-discovered links are raw links, not `added_seeds`.
- Parse_Core may later create candidate `added_seeds` after filtering and pre-ranking.
- Desktop_Import performs stricter validation, enrichment, heavy geocoding/location normalization, and final search-ready output.
- Candidate source-seed catalogs are not live crawler activation.

## Candidate source families

| # | source_code | name | category | quality | decision | seed_url_count | note |
|---:|---|---|---|---|---|---:|---|
| 1 | `pt_fiata_directory` | FIATA Portugal members directory | global_association_directory | A | ACCEPT_REVIEW | 1 | Portugal member page under FIATA shared host; candidate-only subordinate surface. |
| 2 | `pt_apat` | APAT - Associação dos Transitários de Portugal | freight_forwarding_association | A_PLUS | ACCEPT_REVIEW | 3 | National Portuguese freight forwarders association candidate. |
| 3 | `pt_antram` | ANTRAM | road_freight_association | A_MINUS | ACCEPT_REVIEW | 2 | Portuguese road freight transport association candidate. |
| 4 | `pt_aplog` | APLOG - Associação Portuguesa de Logística | logistics_association | A_MINUS | ACCEPT_REVIEW | 2 | Portuguese logistics association candidate. |
| 5 | `pt_associacao_portos_portugal` | Associação dos Portos de Portugal | ports_association | A_MINUS | ACCEPT_REVIEW | 2 | Portuguese ports association / port-sector reference candidate. |
| 6 | `pt_janela_unica_logistica` | Janela Única Logística project | logistics_single_window | A_MINUS | ACCEPT_REVIEW | 2 | National logistics single-window ecosystem candidate; no runtime activation. |
| 7 | `pt_imt_transportes` | IMT Portugal | official_transport_authority | A | ACCEPT_REVIEW | 2 | Official transport authority candidate; structural-only URL validation. |
| 8 | `pt_port_lisbon` | Port of Lisbon | port_authority | A_PLUS | ACCEPT_REVIEW | 2 | Major Portuguese port authority candidate. |
| 9 | `pt_port_sines_algarve` | Ports of Sines and Algarve | port_authority | A_PLUS | ACCEPT_REVIEW | 3 | Sines is a major Portuguese cargo/container platform; candidate-only. |
| 10 | `pt_port_leixoes_apdl` | APDL / Port of Leixões | port_authority | A_PLUS | ACCEPT_REVIEW | 3 | Northern Portugal / Leixões port authority candidate. |
| 11 | `pt_port_aveiro` | Port of Aveiro | port_authority | A | ACCEPT_REVIEW | 2 | Central Portugal port authority candidate. |
| 12 | `pt_port_setubal_sesimbra` | Ports of Setúbal and Sesimbra | port_authority | A | ACCEPT_REVIEW | 2 | Setúbal/Sesimbra port authority candidate. |
| 13 | `pt_port_viana_castelo` | Port of Viana do Castelo | port_authority | A_MINUS | ACCEPT_REVIEW | 2 | Northern regional port candidate. |
| 14 | `pt_ports_madeira` | APRAM / Ports of Madeira | port_authority | A_MINUS | ACCEPT_REVIEW | 2 | Madeira ports authority candidate. |
| 15 | `pt_ports_azores` | Ports of Azores | port_authority | A_MINUS | ACCEPT_REVIEW | 2 | Azores ports authority candidate. |
| 16 | `pt_tap_air_cargo` | TAP Air Cargo | air_cargo_carrier | A | ACCEPT_REVIEW | 3 | Portuguese air cargo carrier candidate. |
| 17 | `pt_portway` | Portway Handling de Portugal | airport_cargo_handler | A_MINUS | ACCEPT_REVIEW | 3 | Portuguese airport ground/cargo handling candidate. |
| 18 | `pt_ana_airports` | ANA Aeroportos de Portugal | airport_operator | A_MINUS | ACCEPT_REVIEW | 2 | Portuguese airport operator candidate. |
| 19 | `pt_groundforce_portugal` | Groundforce Portugal | airport_ground_cargo_handler | B_PLUS | ACCEPT_REVIEW | 2 | Airport handling/cargo candidate; live check required later. |
| 20 | `pt_portocargo` | PORTOCARGO | freight_forwarder | B_PLUS | ACCEPT_REVIEW | 3 | Commercial freight forwarder candidate; below official/association priority. |
| 21 | `pt_igacargo` | IGACARGO | freight_forwarder_air_cargo | B_PLUS | ACCEPT_REVIEW | 2 | Customs and air cargo services candidate. |
| 22 | `pt_navigomes` | NAVIGOMES | freight_forwarder | B | ACCEPT_REVIEW | 2 | Commercial freight forwarder candidate. |
| 23 | `pt_luis_simoes` | Luís Simões | road_transport_logistics_operator | B_PLUS | ACCEPT_REVIEW | 2 | Iberian road transport/logistics operator candidate. |
| 24 | `pt_torrestir` | Torrestir | transport_logistics_operator | B | ACCEPT_REVIEW | 2 | Commercial transport/logistics operator candidate. |
| 25 | `pt_garland` | Garland | freight_forwarding_logistics_operator | B_PLUS | ACCEPT_REVIEW | 2 | Commercial forwarding/logistics operator candidate. |
| 26 | `pt_rangel` | Rangel Logistics Solutions | logistics_operator | B_PLUS | ACCEPT_REVIEW | 2 | Portuguese logistics operator candidate. |
| 27 | `pt_olicargo` | Olicargo | freight_forwarding_logistics_operator | B | ACCEPT_REVIEW | 2 | Commercial forwarding/logistics candidate. |
| 28 | `pt_transitex` | Transitex | freight_forwarding_logistics_operator | B | ACCEPT_REVIEW | 2 | Commercial freight forwarding/logistics candidate. |
| 29 | `pt_jomatir` | Jomatir | road_transport_operator | B | ACCEPT_REVIEW | 2 | Portuguese road transport candidate. |
| 30 | `pt_medway` | MEDWAY Iberia | rail_freight_operator | A_MINUS | ACCEPT_REVIEW | 2 | Rail freight/intermodal operator candidate. |
| 31 | `pt_takargo` | Takargo | rail_freight_operator | B_PLUS | ACCEPT_REVIEW | 2 | Rail freight operator candidate. |
| 32 | `pt_psa_sines` | PSA Sines | container_terminal_operator | A_MINUS | ACCEPT_REVIEW | 2 | Sines container terminal operator candidate. |
| 33 | `pt_yilport_leixoes` | YILPORT Leixões | port_terminal_operator | B_PLUS | ACCEPT_REVIEW | 2 | Leixões terminal operator candidate. |
| 34 | `pt_liscont` | LISCONT | container_terminal_operator | B_PLUS | ACCEPT_REVIEW | 2 | Lisbon container terminal operator candidate. |
| 35 | `pt_tcl_leixoes` | TCL Leixões | container_terminal_operator | B_PLUS | ACCEPT_REVIEW | 2 | Leixões container terminal candidate. |
| 36 | `pt_sotagus` | Sotagus | container_terminal_operator | B | ACCEPT_REVIEW | 2 | Container terminal / logistics terminal candidate. |
| 37 | `pt_noatum_logistics_portugal` | Noatum Logistics Portugal | freight_forwarding_logistics_operator | B | ACCEPT_REVIEW | 2 | Commercial logistics operator candidate. |
| 38 | `pt_dbschenker_portugal` | DB Schenker Portugal | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Portugal surface candidate. |
| 39 | `pt_dhl_global_forwarding_portugal` | DHL Global Forwarding Portugal | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global forwarding Portugal surface candidate. |
| 40 | `pt_cargoyellowpages_directory` | Cargo Yellow Pages Portugal | commercial_freight_directory | B_MINUS | ACCEPT_REVIEW | 1 | Lower-priority commercial directory candidate; must not dominate scheduler. |

## Candidate seed surfaces

| seed_url_index | source_code | url | candidate_manifest | is_live | enabled | needs_live_check | runtime_activation_policy | safety_state |
|---:|---|---|---|---|---|---|---|---|
| 1 | `pt_fiata_directory` | `https://fiata.org/directory/pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 2 | `pt_apat` | `https://www.apat.pt/en/home` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 3 | `pt_apat` | `https://www.apat.pt/en/a_associacao` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 4 | `pt_apat` | `https://www.apat.pt/en/vantagens_associados` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 5 | `pt_antram` | `https://www.antram.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 6 | `pt_antram` | `https://www.antram.pt/associacao/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 7 | `pt_aplog` | `https://aplog.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 8 | `pt_aplog` | `https://aplog.pt/a-aplog/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 9 | `pt_associacao_portos_portugal` | `https://www.portosdeportugal.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 10 | `pt_associacao_portos_portugal` | `https://www.portosdeportugal.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 11 | `pt_janela_unica_logistica` | `https://www.projeto-jul.pt/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 12 | `pt_janela_unica_logistica` | `https://www.projeto-jul.pt/en/entities-involved` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 13 | `pt_imt_transportes` | `https://www.imt-ip.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 14 | `pt_imt_transportes` | `https://www.imt-ip.pt/sites/IMTT/Portugues/TransportesRodoviarios/TransporteMercadorias/Paginas/TransporteMercadorias.aspx` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 15 | `pt_port_lisbon` | `https://www.portodelisboa.pt/en/home` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 16 | `pt_port_lisbon` | `https://www.portodelisboa.pt/en/business` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 17 | `pt_port_sines_algarve` | `https://www.apsinesalgarve.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 18 | `pt_port_sines_algarve` | `https://www.apsinesalgarve.pt/en/ports/port-of-sines/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 19 | `pt_port_sines_algarve` | `https://www.apsinesalgarve.pt/en/ports/port-of-portimao/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 20 | `pt_port_leixoes_apdl` | `https://www.apdl.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 21 | `pt_port_leixoes_apdl` | `https://leixoes.apdl.pt/en/the-port/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 22 | `pt_port_leixoes_apdl` | `https://www.apdl.pt/en/ports/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 23 | `pt_port_aveiro` | `https://portodeaveiro.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 24 | `pt_port_aveiro` | `https://portodeaveiro.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 25 | `pt_port_setubal_sesimbra` | `https://www.portodesetubal.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 26 | `pt_port_setubal_sesimbra` | `https://www.portodesetubal.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 27 | `pt_port_viana_castelo` | `https://www.portodeviana.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 28 | `pt_port_viana_castelo` | `https://www.portodeviana.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 29 | `pt_ports_madeira` | `https://www.apram.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 30 | `pt_ports_madeira` | `https://www.apram.pt/site/index.php/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 31 | `pt_ports_azores` | `https://www.portosdosacores.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 32 | `pt_ports_azores` | `https://www.portosdosacores.pt/index.php/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 33 | `pt_tap_air_cargo` | `https://www.tapcargo.com/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 34 | `pt_tap_air_cargo` | `https://www.tapcargo.com/en/products` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 35 | `pt_tap_air_cargo` | `https://www.tapcargo.com/en/network` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 36 | `pt_portway` | `https://www.portway.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 37 | `pt_portway` | `https://www.portway.pt/en/our-business` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 38 | `pt_portway` | `https://www.portway.pt/en/contacts` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 39 | `pt_ana_airports` | `https://www.ana.pt/en/lis/home` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 40 | `pt_ana_airports` | `https://www.ana.pt/en/opo/home` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 41 | `pt_groundforce_portugal` | `https://www.groundforce.pt/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 42 | `pt_groundforce_portugal` | `https://www.groundforce.pt/en/services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 43 | `pt_portocargo` | `https://portocargo.pt/en/home/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 44 | `pt_portocargo` | `https://portocargo.pt/en/sea-freight/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 45 | `pt_portocargo` | `https://portocargo.pt/en/air-freight/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 46 | `pt_igacargo` | `https://www.igacargo.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 47 | `pt_igacargo` | `https://www.igacargo.pt/en/history/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 48 | `pt_navigomes` | `https://www.navigomes.pt/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 49 | `pt_navigomes` | `https://www.navigomes.pt/en/node/57` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 50 | `pt_luis_simoes` | `https://www.luis-simoes.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 51 | `pt_luis_simoes` | `https://www.luis-simoes.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 52 | `pt_torrestir` | `https://www.torrestir.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 53 | `pt_torrestir` | `https://www.torrestir.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 54 | `pt_garland` | `https://www.garland.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 55 | `pt_garland` | `https://www.garland.pt/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 56 | `pt_rangel` | `https://www.rangel.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 57 | `pt_rangel` | `https://www.rangel.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 58 | `pt_olicargo` | `https://www.olicargo.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 59 | `pt_olicargo` | `https://www.olicargo.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 60 | `pt_transitex` | `https://www.transitex.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 61 | `pt_transitex` | `https://www.transitex.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 62 | `pt_jomatir` | `https://www.jomatir.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 63 | `pt_jomatir` | `https://www.jomatir.pt/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 64 | `pt_medway` | `https://www.medway-iberia.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 65 | `pt_medway` | `https://www.medway-iberia.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 66 | `pt_takargo` | `https://www.takargo.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 67 | `pt_takargo` | `https://www.takargo.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 68 | `pt_psa_sines` | `https://www.psasines.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 69 | `pt_psa_sines` | `https://www.psasines.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 70 | `pt_yilport_leixoes` | `https://www.yilport.com/en/port-terminals/yilport-iberia/yilport-leixoes` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 71 | `pt_yilport_leixoes` | `https://www.yilport.com/en/port-terminals/yilport-iberia` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 72 | `pt_liscont` | `https://www.liscont.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 73 | `pt_liscont` | `https://www.liscont.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 74 | `pt_tcl_leixoes` | `https://www.tcl-leixoes.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 75 | `pt_tcl_leixoes` | `https://www.tcl-leixoes.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 76 | `pt_sotagus` | `https://www.sotagus.pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 77 | `pt_sotagus` | `https://www.sotagus.pt/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 78 | `pt_noatum_logistics_portugal` | `https://www.noatumlogistics.com/pt/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 79 | `pt_noatum_logistics_portugal` | `https://www.noatumlogistics.com/pt/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 80 | `pt_dbschenker_portugal` | `https://www.dbschenker.com/pt-en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 81 | `pt_dbschenker_portugal` | `https://www.dbschenker.com/pt-en/products` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 82 | `pt_dhl_global_forwarding_portugal` | `https://www.dhl.com/pt-en/home/our-divisions/global-forwarding.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 83 | `pt_dhl_global_forwarding_portugal` | `https://www.dhl.com/pt-en/home/our-divisions/global-forwarding/freight-forwarding.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 84 | `pt_cargoyellowpages_directory` | `https://www.cargoyellowpages.com/portugal_freight_forwarders_cargo_agents.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |

## Next gate

After R305 is audited, the next safe gate is expected to be:

`R306_PT_SOURCE_SEED_DECISION_DOC_AUDIT_READONLY`

Only after the decision doc passes audit should a separate commit/push gate be considered.

## R305 creation metadata

- Created by gate: `R305_PT_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`
- Created at: `2026-05-16T12:30:08+02:00`
- Mutation scope: exactly this decision doc only.
