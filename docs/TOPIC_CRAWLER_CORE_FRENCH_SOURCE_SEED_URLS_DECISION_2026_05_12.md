# TOPIC_CRAWLER_CORE_FRENCH_SOURCE_SEED_URLS_DECISION_2026_05_12

## Gate

- Gate: `SOURCE_SEED_R166_FRENCH_DECISION_DOC_PATCH_LOCAL_ONLY`
- Machine: `Ubuntu Desktop`
- Created at: `2026-05-12`
- Canonical head before patch: `9122e5114ae916937b17af5e5222365054d91df9`
- Language code: `fr`
- LANGUAGE_CODE: `fr`
- Language name: `French`
- Decision doc path: `docs/TOPIC_CRAWLER_CORE_FRENCH_SOURCE_SEED_URLS_DECISION_2026_05_12.md`
- Future catalog path: `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json`

## Non-touch assertions

- No catalog JSON was created in this gate.
- No README update was made in this gate.
- No git add, commit, push, fetch, reset, or checkout was executed by this gate.
- No pi51c command was executed.
- No database command was executed.
- No crawler command was executed.
- No systemd command was executed.
- No URL fetch or live probe was executed.
- This document is a source-seed decision plan only.

## Global source-seed policy

| Policy key | Value |
|---|---|
| catalog_state | `candidate_not_live` |
| all_families_initial_enabled | `false` |
| all_families_need_live_check | `true` |
| runtime_activation_policy | `pi51c_live_probe_required_before_db_or_frontier_insert` |
| live_frontier_activation | `false` |
| db_insert_allowed | `false` |
| url_fetch_allowed_in_catalog_gate | `false` |
| crawler_start_allowed_in_catalog_gate | `false` |
| pi51c_sync_allowed_in_catalog_gate | `false` |
| manual_review_required | `true` |
| no_aggressive_pagination | `true` |
| same_day_full_country_expansion | `false` |
| max_initial_depth | `0_or_1` |

## French rollout scope

French is treated as a multi-region high-coverage source-seed language. The first decision plan covers France and high-value francophone or French-relevant logistics surfaces, including Belgium, Switzerland, Luxembourg, Monaco, Canada/Quebec, Maghreb, francophone Africa, Mauritius, and global French-relevant logistics networks.

The catalog language code remains `fr`. Country and region scopes such as `FR`, `BE`, `CH`, `LU`, `MC`, `CA/QC`, `MA`, `TN`, `CI`, `SN`, `CM`, `MG`, and `MU` are region metadata, not taxonomy language codes.

## Source hierarchy decisions

- Main host/source-family hierarchy must be preserved.
- FIATA country pages remain subordinate seed surfaces under one shared FIATA source family.
- FIATA France, Belgium, Switzerland, Canada, Morocco, Tunisia, Côte d'Ivoire, Senegal, Cameroon, Madagascar, and Mauritius pages must not become separate top-level source families; in short, they are not separate top-level source families.
- Commercial directories are kept as fallback/review surfaces unless official, association, customs, port, airport, or chamber sources are insufficient.
- Single-company surfaces are generally `HOLD` and reserved for later entity enrichment, not source-family activation.
- PDF surfaces require a later PDF-handling/live-probe gate before any runtime activation.

## Metrics

| Metric | Value |
|---|---:|
| source_family_candidate_count | 49 |
| seed_surface_candidate_count | 88 |
| unique_seed_url_count | 88 |
| unique_host_count | 51 |

## Quality / decision distribution

| Distribution | Counts |
|---|---|
| quality_tiers | `A: 8, A_MINUS: 11, A_PLUS: 4, B: 9, B_MINUS: 9, B_PLUS: 8` |
| decision_status | `ACCEPT: 2, ACCEPT_REVIEW: 26, HOLD: 21` |
| source_types | `aeo_operator_directory: 1, air_cargo_directory: 1, air_cargo_station_reference: 1, association_home: 1, association_member_directory: 4, chamber_member_directory: 1, commercial_air_freight_directory: 1, commercial_cargo_directory: 1, commercial_forwarder_directory: 1, commercial_freight_directory: 1, commercial_freight_network: 2, commercial_freight_network_directory: 1, commercial_logistics_directory: 5, commercial_project_cargo_directory: 1, company_group_reference: 1, european_association_reference: 1, freight_forwarder_association: 2, government_logistics_partner_reference: 1, local_business_directory: 1, logistics_cluster_member_surface: 1, maritime_association_member_directory: 1, maritime_cluster_member_directory: 1, official_air_cargo_surface: 1, official_airport_cargo_forwarder_surface: 1, official_customs_reference: 2, official_forwarding_agents_pdf: 1, official_members_directory: 1, official_port_logistics_surface: 2, regional_transport_directory: 2, secondary_air_cargo_reference: 1, secondary_air_cargo_terminal_directory: 1, secondary_association_member_mirror: 1, single_company_air_cargo_reference: 1, single_company_regional_branch_reference: 1, single_company_secondary_reference: 1, trade_fair_country_hub: 1, trade_fair_exhibitor_directory: 1` |
| region_scopes | `BE: 1, CA/QC: 1, CH: 1, EU: 1, EU/FR/BE: 1, FR: 11, FR/BE/CH/CA/MA/TN/CI/SN/CM/MG/MU: 1, FR/BE/LU/MC/TN/SN/CM/MG/MU: 1, FR/EU: 3, FR/LU/MC/SN/MG: 1, FR/MA: 1, FR/MC/MA/TN: 1, GLOBAL: 2, GLOBAL/CI: 1, GLOBAL/FR: 3, LU: 4, LU/SN/CM/MG: 1, MA: 1, MC: 3, MC/FR: 1, MG: 2, MU: 3, QC: 2, SN/CM: 1, SN/MG: 1` |

## Decision matrix

| # | source_code | decision | tier | region_scope | source_type | family_model | seed_surfaces | canonical_url | rationale |
|---:|---|---|---|---|---|---|---:|---|---|
| 1 | `fr_fiata_members_directory` | `ACCEPT` | `A_PLUS` | `FR/BE/CH/CA/MA/TN/CI/SN/CM/MG/MU` | `official_members_directory` | `shared_host_parent_with_country_surfaces` | 11 | https://fiata.org/directory/ | FIATA shared host; country pages remain subordinate seed surfaces, not separate top-level families. |
| 2 | `fr_tlf_overseas_annuaire` | `ACCEPT` | `A_PLUS` | `FR` | `association_member_directory` | `single_host_directory` | 1 | https://e-tlf.com/annuaire/ | French transport/logistics professional association member directory. |
| 3 | `fr_tlf_association` | `ACCEPT_REVIEW` | `A` | `FR` | `association_home` | `single_host_reference` | 1 | https://e-tlf.com/ | Association reference surface; directory page remains the stronger seed. |
| 4 | `fr_clecat_full_members` | `ACCEPT_REVIEW` | `A_MINUS` | `EU/FR/BE` | `european_association_reference` | `single_host_reference` | 1 | https://www.clecat.org/members/full-members | European forwarding/logistics association member reference; useful for national association cross-check. |
| 5 | `fr_eu_aeo_directory_france` | `ACCEPT_REVIEW` | `A_MINUS` | `FR/EU` | `aeo_operator_directory` | `single_host_search_surface` | 1 | https://www.aeodirectory.com/aeo/search/?country=France | AEO surface includes mixed industries; logistics-service rows need later filtering. |
| 6 | `fr_eu_aeo_reference` | `ACCEPT_REVIEW` | `A` | `EU` | `official_customs_reference` | `single_host_reference` | 1 | https://taxation-customs.ec.europa.eu/customs/authorised-economic-operator_en | Official EU AEO reference; not a company directory by itself. |
| 7 | `fr_douane_registered_customs_representatives` | `ACCEPT_REVIEW` | `A` | `FR` | `official_customs_reference` | `single_host_reference` | 1 | https://www.douane.gouv.fr/fiche/registered-customs-representatives | French customs representative registration reference; later needs list/download discovery if available. |
| 8 | `fr_iata_cargolink_directory` | `ACCEPT_REVIEW` | `A_MINUS` | `GLOBAL/FR` | `air_cargo_directory` | `shared_host_directory_with_example_surface` | 2 | https://www.iata.org/en/publications/directories/cargolink/directory/ | Air-cargo supplier directory; country filtering/search behavior needs live probe later. |
| 9 | `fr_sitl_exhibitors` | `ACCEPT_REVIEW` | `A_MINUS` | `FR/EU` | `trade_fair_exhibitor_directory` | `single_host_event_directory` | 2 | https://www.sitl.eu/fr-fr/qui-participe/liste-des-exposants.html | French transport/logistics trade fair exhibitor surface; event-year freshness must be rechecked before activation. |
| 10 | `fr_transport_logistic_hub_france` | `ACCEPT_REVIEW` | `B_PLUS` | `FR/EU` | `trade_fair_country_hub` | `single_host_event_reference` | 1 | https://exhibitors.transportlogistic.de/en/exhibitors-and-directories/exhibitors-brand-names/exhibitors-brand-names-details/exhibitorDetail/ID/1415725/ | Country hub/exhibitor reference; not final company directory without deeper event surface check. |
| 11 | `fr_haropa_port` | `ACCEPT_REVIEW` | `A_MINUS` | `FR` | `official_port_logistics_surface` | `single_host_port_surface` | 1 | https://www.haropaport.com/en | Official French port/logistics ecosystem surface; may expose terminals/operators/publications later. |
| 12 | `fr_marseille_fos_logistics` | `ACCEPT_REVIEW` | `A_MINUS` | `FR` | `official_port_logistics_surface` | `single_host_port_surface` | 1 | https://www.marseille-port.fr/en/filieres/logistics | Official Marseille-Fos logistics surface; likely useful for port/logistics zone evidence. |
| 13 | `fr_paris_aeroport_cargo` | `ACCEPT_REVIEW` | `A_MINUS` | `FR` | `official_air_cargo_surface` | `single_host_air_cargo_surface` | 3 | https://www.parisaeroport.fr/en/professionals/cargo | Official Paris airport cargo surface; operator/list behavior needs later live probe. |
| 14 | `fr_umf_adherents` | `ACCEPT_REVIEW` | `A_MINUS` | `FR` | `maritime_association_member_directory` | `single_host_maritime_directory` | 1 | https://umf.asso.fr/en/umf-adherents | Maritime/Fos ecosystem adherents; contains shipping, forwarding, terminal and goods-interface categories. |
| 15 | `fr_sas_cargo_cdg_station` | `HOLD` | `B_PLUS` | `FR` | `air_cargo_station_reference` | `single_host_airline_station_reference` | 1 | https://sascargo.com/Station-Information/Overview/CDG | Station handler evidence, not broad source-family directory; keep HOLD until air-cargo model is explicit. |
| 16 | `fr_forward_belgium` | `ACCEPT_REVIEW` | `A` | `BE` | `association_member_directory` | `single_host_directory_with_pdf_surface` | 2 | https://forwardbelgium.be/find-a-forwarder | Belgian forwarding/customs/logistics association; French-language relevance but not France-only. |
| 17 | `fr_spedlogswiss_members` | `ACCEPT_REVIEW` | `A_PLUS` | `CH` | `association_member_directory` | `single_host_multilingual_member_directory` | 2 | https://spedlogswiss.com/enUK/association/members | Swiss forwarding/logistics member directory; Swiss French relevance through CH region scope. |
| 18 | `fr_cluster_logistics_luxembourg` | `ACCEPT_REVIEW` | `A` | `LU` | `logistics_cluster_member_surface` | `single_host_cluster_surface` | 1 | https://www.clusterforlogistics.lu/members | Luxembourg logistics cluster member surface. |
| 19 | `fr_logistics_public_lu_partners` | `ACCEPT_REVIEW` | `A_MINUS` | `LU` | `government_logistics_partner_reference` | `single_host_public_reference` | 1 | https://logistics.public.lu/en/setup-business/key-players.html | Luxembourg official logistics partner guidance; may route to approved directories. |
| 20 | `fr_lux_airport_cargo_forwarders` | `ACCEPT_REVIEW` | `A_MINUS` | `LU` | `official_airport_cargo_forwarder_surface` | `single_host_air_cargo_surface` | 1 | https://www.lux-airport.lu/corporate/business-partners/cargo/ | Luxembourg airport cargo page references freight forwarders with presence in Luxembourg. |
| 21 | `fr_cluster_maritime_luxembourg` | `ACCEPT_REVIEW` | `B_PLUS` | `LU` | `maritime_cluster_member_directory` | `single_host_maritime_directory` | 1 | https://www.cluster-maritime.lu/members-list/ | Luxembourg maritime cluster member list; mixed maritime/logistics scope. |
| 22 | `fr_montecarlo_import_export_directory` | `HOLD` | `B_PLUS` | `MC` | `local_business_directory` | `single_host_local_directory` | 1 | https://www.monte-carlo.mc/en/directory/transportation-logistics/import-export/ | Small Monaco local directory; keep HOLD until quality and scope are verified. |
| 23 | `fr_mathez_monaco_group` | `HOLD` | `B_PLUS` | `MC/FR` | `company_group_reference` | `single_company_reference` | 2 | https://www.mathezfreight.com/en/about/ | Single company/group reference, not a directory; keep HOLD for possible later entity enrichment. |
| 24 | `fr_ciffa_member_directory` | `ACCEPT_REVIEW` | `A` | `CA/QC` | `association_member_directory` | `single_host_member_directory` | 1 | https://www.ciffa.com/member-directory/ | Canadian freight-forwarder association directory; Quebec/French surface requires later filtering. |
| 25 | `fr_truckstopquebec_annuaire` | `ACCEPT_REVIEW` | `B_PLUS` | `QC` | `regional_transport_directory` | `single_host_regional_directory` | 1 | https://www.truckstopquebec.com/annuaire/ | French-language Quebec transport directory; quality/pagination must be verified later. |
| 26 | `fr_fleetdirectory_quebec` | `HOLD` | `B` | `QC` | `regional_transport_directory` | `single_host_secondary_directory` | 1 | https://www.fleetdirectory.com/bylocation/canada/Quebec.htm | Secondary Quebec fleet directory; keep HOLD until better official source is unavailable. |
| 27 | `fr_affm_morocco` | `ACCEPT_REVIEW` | `A` | `MA` | `freight_forwarder_association` | `single_host_association_reference` | 1 | https://www.affm.ma | Morocco freight-forwarder association reference; member-directory surface must be verified later. |
| 28 | `fr_apt_mauritius` | `ACCEPT_REVIEW` | `A` | `MU` | `freight_forwarder_association` | `single_host_association_reference` | 1 | https://www.aptmu.com/ | Mauritius freight-forwarder association; useful for francophone/Indian Ocean coverage. |
| 29 | `fr_mra_mauritius_forwarding_agents_pdf` | `ACCEPT_REVIEW` | `A_PLUS` | `MU` | `official_forwarding_agents_pdf` | `single_host_official_pdf` | 1 | https://www.mra.mu/download/ForwardingFreightAgentsList.pdf | Official active freight-forwarding agents list PDF; needs PDF handling gate before activation. |
| 30 | `fr_mcci_mauritius_members_directory` | `ACCEPT_REVIEW` | `A_MINUS` | `MU` | `chamber_member_directory` | `single_host_chamber_directory` | 1 | https://www.mcci.org/en/membership/members-directory/?alph=F | Mauritius chamber member directory; logistics categories need later filtering. |
| 31 | `fr_freightnet_directory` | `ACCEPT_REVIEW` | `B` | `FR/BE/LU/MC/TN/SN/CM/MG/MU` | `commercial_freight_directory` | `shared_host_country_surfaces` | 9 | https://www.freightnet.com/directory/p3/cFR/s99.htm | Commercial directory; useful only as fallback/comparison after official sources. |
| 32 | `fr_cargoyellowpages_directory` | `ACCEPT_REVIEW` | `B` | `FR/MC/MA/TN` | `commercial_cargo_directory` | `shared_host_country_surfaces` | 4 | https://paginasamarillasdelacarga.cargoyellowpages.com/france_freight_forwarders_cargo_agents.html | Commercial cargo directory; lower trust than associations/customs sources. |
| 33 | `fr_azfreight_directory` | `HOLD` | `B` | `LU/SN/CM/MG` | `commercial_air_freight_directory` | `shared_host_country_surfaces` | 4 | https://azfreight.com/country-facility/freight-forwarders-in-luxembourg/ | Commercial directory; keep HOLD until official/association surfaces are exhausted. |
| 34 | `fr_ruzave_directory` | `HOLD` | `B_MINUS` | `FR/LU/MC/SN/MG` | `commercial_logistics_directory` | `shared_host_country_surfaces` | 5 | https://ruzave.com/france | Commercial directory; HOLD due lower authority and possible promotional listings. |
| 35 | `fr_jctrans_directory` | `HOLD` | `B_MINUS` | `GLOBAL/CI` | `commercial_freight_network` | `shared_host_directory` | 2 | https://www.jctrans.com/en/company/list | Commercial network; HOLD until search/filter behavior is explicitly probed. |
| 36 | `fr_globalia_directory` | `HOLD` | `B` | `GLOBAL` | `commercial_freight_network` | `single_host_network` | 1 | https://www.globalialogisticsnetwork.com/ | Global network; HOLD until country/member search exposure is verified. |
| 37 | `fr_aeroceanetwork_directory` | `HOLD` | `B` | `GLOBAL/FR` | `commercial_freight_network_directory` | `single_host_network_directory` | 1 | https://aeroceanetwork.net/directory/ | Global network directory; HOLD pending country filter/live behavior check. |
| 38 | `fr_forwardingcompanies_association_mirrors` | `HOLD` | `B` | `FR/MA` | `secondary_association_member_mirror` | `shared_host_association_mirror` | 2 | https://forwardingcompanies.com/association/union-des-entreprises-de-transport-et-logistique-de-france-tlf- | Secondary mirror of association members; HOLD unless official pages are insufficient. |
| 39 | `fr_searates_monaco` | `HOLD` | `B_MINUS` | `MC` | `commercial_logistics_directory` | `single_host_secondary_directory` | 1 | https://www.searates.com/reference/logistics-service/monaco/ | Commercial Monaco logistics page; HOLD because official/local directory is preferable. |
| 40 | `fr_opca_monaco` | `HOLD` | `B_MINUS` | `MC` | `commercial_project_cargo_directory` | `single_host_secondary_directory` | 1 | https://overseasprojectcargo.com/InternationalFreightForwarders/monaco-freight-forwarders/ | Commercial Monaco/project-cargo directory; HOLD. |
| 41 | `fr_cargoenter_cdg` | `HOLD` | `B` | `FR` | `secondary_air_cargo_terminal_directory` | `single_host_air_cargo_secondary` | 1 | https://cargoenter.com/cargo-tools/airport-cargo-terminals/cdg | Secondary CDG cargo terminal reference; HOLD behind official ADP/IATA surfaces. |
| 42 | `fr_parcelsapp_cdg` | `HOLD` | `B_MINUS` | `FR` | `secondary_air_cargo_reference` | `single_host_air_cargo_secondary` | 1 | https://parcelsapp.com/en/airports/cdg-paris-charles-de-gaulle-airport | Secondary airport cargo guide; HOLD. |
| 43 | `fr_kales_paris_gssa` | `HOLD` | `B_PLUS` | `FR` | `single_company_air_cargo_reference` | `single_company_reference` | 1 | https://kales.com/office/paris/ | Single GSSA company surface; not a broad source family. |
| 44 | `fr_freighthub_directory` | `HOLD` | `B_MINUS` | `GLOBAL/FR` | `commercial_logistics_directory` | `single_host_secondary_directory` | 1 | https://freighthub.co/ | Commercial global directory; HOLD pending relevance and country filtering. |
| 45 | `fr_freightvaluation_directory` | `HOLD` | `B_MINUS` | `GLOBAL` | `commercial_logistics_directory` | `single_host_secondary_directory` | 1 | https://www.freightvaluation.com/logistics-directory | Commercial directory; HOLD. |
| 46 | `fr_logisticscompaniesdirectory_madagascar` | `HOLD` | `B_MINUS` | `MG` | `commercial_logistics_directory` | `single_host_secondary_directory` | 1 | https://logisticscompaniesdirectory.com/network-regions/madagascar/ | Secondary Madagascar logistics directory; HOLD behind FIATA/official options. |
| 47 | `fr_forwardingcompanies_senegal_cameroon` | `HOLD` | `B` | `SN/CM` | `commercial_forwarder_directory` | `shared_host_country_surfaces` | 2 | https://forwardingcompanies.com/in/senegal | Secondary country forwarder directory; HOLD unless official/FIATA surfaces are insufficient. |
| 48 | `fr_sifa_francophone_africa` | `HOLD` | `B_PLUS` | `SN/MG` | `single_company_regional_branch_reference` | `single_company_reference` | 2 | https://sifalogistics.com/en/our-freight-forwaders/sifa-senegal/ | Single company branch pages; potential entity enrichment only, not source directory. |
| 49 | `fr_freightpages_madagascar_auximad` | `HOLD` | `B_MINUS` | `MG` | `single_company_secondary_reference` | `single_company_reference` | 1 | https://www.freightpages.org/company/auximad/ | Single company reference; HOLD. |

## Seed surface appendix

| source_code | seed_surface |
|---|---|
| `fr_fiata_members_directory` | https://fiata.org/directory/fr/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/be/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/ch/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/ca/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/ma/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/tn/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/ci/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/sn/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/cm/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/mg/ |
| `fr_fiata_members_directory` | https://fiata.org/directory/mu/ |
| `fr_tlf_overseas_annuaire` | https://e-tlf.com/annuaire/ |
| `fr_tlf_association` | https://e-tlf.com/ |
| `fr_clecat_full_members` | https://www.clecat.org/members/full-members |
| `fr_eu_aeo_directory_france` | https://www.aeodirectory.com/aeo/search/?country=France |
| `fr_eu_aeo_reference` | https://taxation-customs.ec.europa.eu/customs/authorised-economic-operator_en |
| `fr_douane_registered_customs_representatives` | https://www.douane.gouv.fr/fiche/registered-customs-representatives |
| `fr_iata_cargolink_directory` | https://www.iata.org/en/publications/directories/cargolink/directory/ |
| `fr_iata_cargolink_directory` | https://www.iata.org/en/publications/directories/cargolink/directory/france-cargo-international-company-sas/9052/ |
| `fr_sitl_exhibitors` | https://www.sitl.eu/fr-fr/qui-participe/liste-des-exposants.html |
| `fr_sitl_exhibitors` | https://www.sitl.eu/en-gb/who-is-coming/Liste_des_exposants_2027.html |
| `fr_transport_logistic_hub_france` | https://exhibitors.transportlogistic.de/en/exhibitors-and-directories/exhibitors-brand-names/exhibitors-brand-names-details/exhibitorDetail/ID/1415725/ |
| `fr_haropa_port` | https://www.haropaport.com/en |
| `fr_marseille_fos_logistics` | https://www.marseille-port.fr/en/filieres/logistics |
| `fr_paris_aeroport_cargo` | https://www.parisaeroport.fr/en/professionals/cargo |
| `fr_paris_aeroport_cargo` | https://www.parisaeroport.fr/en/professionals/cargo/discover/welcome-to-cargo-city |
| `fr_paris_aeroport_cargo` | https://www.parisaeroport.fr/en/professionals/cargo/discover/les-vols-cargo |
| `fr_umf_adherents` | https://umf.asso.fr/en/umf-adherents |
| `fr_sas_cargo_cdg_station` | https://sascargo.com/Station-Information/Overview/CDG |
| `fr_forward_belgium` | https://forwardbelgium.be/find-a-forwarder |
| `fr_forward_belgium` | https://forwardbelgium.be/Flexpage/DownloadFile?id=57009 |
| `fr_spedlogswiss_members` | https://spedlogswiss.com/enUK/association/members |
| `fr_spedlogswiss_members` | https://www.spedlogswiss.com/deCH/verband/mitglieder |
| `fr_cluster_logistics_luxembourg` | https://www.clusterforlogistics.lu/members |
| `fr_logistics_public_lu_partners` | https://logistics.public.lu/en/setup-business/key-players.html |
| `fr_lux_airport_cargo_forwarders` | https://www.lux-airport.lu/corporate/business-partners/cargo/ |
| `fr_cluster_maritime_luxembourg` | https://www.cluster-maritime.lu/members-list/ |
| `fr_montecarlo_import_export_directory` | https://www.monte-carlo.mc/en/directory/transportation-logistics/import-export/ |
| `fr_mathez_monaco_group` | https://www.mathezfreight.com/en/about/ |
| `fr_mathez_monaco_group` | https://www.mathez-monaco.com/en/legal/ |
| `fr_ciffa_member_directory` | https://www.ciffa.com/member-directory/ |
| `fr_truckstopquebec_annuaire` | https://www.truckstopquebec.com/annuaire/ |
| `fr_fleetdirectory_quebec` | https://www.fleetdirectory.com/bylocation/canada/Quebec.htm |
| `fr_affm_morocco` | https://www.affm.ma |
| `fr_apt_mauritius` | https://www.aptmu.com/ |
| `fr_mra_mauritius_forwarding_agents_pdf` | https://www.mra.mu/download/ForwardingFreightAgentsList.pdf |
| `fr_mcci_mauritius_members_directory` | https://www.mcci.org/en/membership/members-directory/?alph=F |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p3/cFR/s99.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cBE/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cLU/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cMC/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cTN/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cSN/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p5/cCM/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cMG/s30.htm |
| `fr_freightnet_directory` | https://www.freightnet.com/directory/p1/cMU/s30.htm |
| `fr_cargoyellowpages_directory` | https://paginasamarillasdelacarga.cargoyellowpages.com/france_freight_forwarders_cargo_agents.html |
| `fr_cargoyellowpages_directory` | https://mobile.cargoyellowpages.com/monaco/monaco.html |
| `fr_cargoyellowpages_directory` | https://paginasamarillasdelacarga.cargoyellowpages.com/morocco_freight_forwarders_cargo_agents.html |
| `fr_cargoyellowpages_directory` | https://mobile.cargoyellowpages.com/tunisia/tunis.html |
| `fr_azfreight_directory` | https://azfreight.com/country-facility/freight-forwarders-in-luxembourg/ |
| `fr_azfreight_directory` | https://azfreight.com/country-facility/freight-forwarders-in-senegal/ |
| `fr_azfreight_directory` | https://azfreight.com/country-facility/freight-forwarders-in-cameroon/ |
| `fr_azfreight_directory` | https://azfreight.com/country-facility/freight-forwarders-in-madagascar/ |
| `fr_ruzave_directory` | https://ruzave.com/france |
| `fr_ruzave_directory` | https://ruzave.com/luxembourg |
| `fr_ruzave_directory` | https://ruzave.com/monaco |
| `fr_ruzave_directory` | https://ruzave.com/senegal |
| `fr_ruzave_directory` | https://ruzave.com/madagascar |
| `fr_jctrans_directory` | https://www.jctrans.com/en/company/list |
| `fr_jctrans_directory` | https://m.jctrans.com/en/membership/listc/Cote%20d%27lvoire/0-0 |
| `fr_globalia_directory` | https://www.globalialogisticsnetwork.com/ |
| `fr_aeroceanetwork_directory` | https://aeroceanetwork.net/directory/ |
| `fr_forwardingcompanies_association_mirrors` | https://forwardingcompanies.com/association/union-des-entreprises-de-transport-et-logistique-de-france-tlf- |
| `fr_forwardingcompanies_association_mirrors` | https://forwardingcompanies.com/association/association-des-freight-forwarders-du-maroc-affm- |
| `fr_searates_monaco` | https://www.searates.com/reference/logistics-service/monaco/ |
| `fr_opca_monaco` | https://overseasprojectcargo.com/InternationalFreightForwarders/monaco-freight-forwarders/ |
| `fr_cargoenter_cdg` | https://cargoenter.com/cargo-tools/airport-cargo-terminals/cdg |
| `fr_parcelsapp_cdg` | https://parcelsapp.com/en/airports/cdg-paris-charles-de-gaulle-airport |
| `fr_kales_paris_gssa` | https://kales.com/office/paris/ |
| `fr_freighthub_directory` | https://freighthub.co/ |
| `fr_freightvaluation_directory` | https://www.freightvaluation.com/logistics-directory |
| `fr_logisticscompaniesdirectory_madagascar` | https://logisticscompaniesdirectory.com/network-regions/madagascar/ |
| `fr_forwardingcompanies_senegal_cameroon` | https://forwardingcompanies.com/in/senegal |
| `fr_forwardingcompanies_senegal_cameroon` | https://forwardingcompanies.com/in/cameroon |
| `fr_sifa_francophone_africa` | https://sifalogistics.com/en/our-freight-forwaders/sifa-senegal/ |
| `fr_sifa_francophone_africa` | https://sifalogistics.com/en/our-freight-forwaders/sifa-madagascar/ |
| `fr_freightpages_madagascar_auximad` | https://www.freightpages.org/company/auximad/ |

## Host distribution

| host | seed_surface_count |
|---|---:|
| `fiata.org` | 11 |
| `www.freightnet.com` | 9 |
| `ruzave.com` | 5 |
| `azfreight.com` | 4 |
| `forwardingcompanies.com` | 4 |
| `www.parisaeroport.fr` | 3 |
| `e-tlf.com` | 2 |
| `forwardbelgium.be` | 2 |
| `mobile.cargoyellowpages.com` | 2 |
| `paginasamarillasdelacarga.cargoyellowpages.com` | 2 |
| `sifalogistics.com` | 2 |
| `www.iata.org` | 2 |
| `www.sitl.eu` | 2 |
| `aeroceanetwork.net` | 1 |
| `cargoenter.com` | 1 |
| `exhibitors.transportlogistic.de` | 1 |
| `freighthub.co` | 1 |
| `kales.com` | 1 |
| `logistics.public.lu` | 1 |
| `logisticscompaniesdirectory.com` | 1 |
| `m.jctrans.com` | 1 |
| `overseasprojectcargo.com` | 1 |
| `parcelsapp.com` | 1 |
| `sascargo.com` | 1 |
| `spedlogswiss.com` | 1 |
| `taxation-customs.ec.europa.eu` | 1 |
| `umf.asso.fr` | 1 |
| `www.aeodirectory.com` | 1 |
| `www.affm.ma` | 1 |
| `www.aptmu.com` | 1 |
| `www.ciffa.com` | 1 |
| `www.clecat.org` | 1 |
| `www.cluster-maritime.lu` | 1 |
| `www.clusterforlogistics.lu` | 1 |
| `www.douane.gouv.fr` | 1 |
| `www.fleetdirectory.com` | 1 |
| `www.freightpages.org` | 1 |
| `www.freightvaluation.com` | 1 |
| `www.globalialogisticsnetwork.com` | 1 |
| `www.haropaport.com` | 1 |
| `www.jctrans.com` | 1 |
| `www.lux-airport.lu` | 1 |
| `www.marseille-port.fr` | 1 |
| `www.mathez-monaco.com` | 1 |
| `www.mathezfreight.com` | 1 |
| `www.mcci.org` | 1 |
| `www.monte-carlo.mc` | 1 |
| `www.mra.mu` | 1 |
| `www.searates.com` | 1 |
| `www.spedlogswiss.com` | 1 |
| `www.truckstopquebec.com` | 1 |

## Activation warning

This decision document does not authorize live crawling. The French source families and seed surfaces listed here remain disabled candidates until a separate live-probe gate validates availability, robots behavior, fetch safety, pagination behavior, content quality, and source-family budget impact.

## Crawler-core / parse-core boundary

- Crawler_Core may collect raw evidence only.
- Raw discovered links are not `added_seeds`.
- Parse_Core may create `added_seeds` only after taxonomy/source-context pre-ranking.
- Desktop_Import on Ubuntu Desktop converts pre-ranking into final rank/review state.

## Next gate

`SOURCE_SEED_R167_FRENCH_DECISION_DOC_AUDIT_READONLY`
