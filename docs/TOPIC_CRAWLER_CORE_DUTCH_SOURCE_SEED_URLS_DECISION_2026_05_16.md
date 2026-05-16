# Dutch Source-Seed URLs Decision — 2026-05-16

## Scope

This document is the local-only R319B decision record for the Dutch (`nl`) LogisticSearch source-seed rollout.

R319B creates only this decision document. It does not create the Dutch catalog JSON, does not activate any source, does not insert into DB/frontier, does not start crawler runtime, does not mutate systemd, does not sync pi51c, and does not perform URL live probes.

## R319 fail-safe correction

- R319 stopped safely before writing because the in-memory Dutch plan had 79 seed URLs instead of 84 and had one duplicate URL.
- R319B corrects the plan to 40 source families and 84 unique HTTPS seed URLs.
- Mutation scope remains local-only and limited to this decision document.

## Canonical rule authority

- Canonical rule doc: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Canonical rule SHA256: `65b36104f039962f3b6c8cd3c70b2575e0de00f27e50732e18953749d89bb49d`
- GitHub raw rule URL used by R319B: `https://raw.githubusercontent.com/malikepoglu/logisticsearch/caa45bb50c9ab32a905ce1a7910f793958b720fb/docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Sealed HEAD: `caa45bb50c9ab32a905ce1a7910f793958b720fb`
- Parent: `521b0337c881b3474c7f79106d54889b7e160f5f`
- Commit subject: `docs(source-seed): index Portuguese startpoint catalog`

The canonical rule doc must be read from GitHub raw before every language catalog/doc/audit/commit/sync step. Local memory, old chat text, editor state, or copied snippets are not rule authority.

## Source and seed priority rule applied in this Dutch plan

- Directory-first selection is applied in this decision plan.
- Association directories, member directories, port/airport company directories, logistics guide directories, and official company-index surfaces are prioritized before individual commercial company pages.
- Individual company pages remain candidate fallback surfaces only after higher-authority directory surfaces.
- This priority rule should later be added to the canonical markdown rule document through a separate controlled rule-doc patch gate if it is not already present.

## Non-touch assertions

- No catalog JSON created in R319B.
- No Git add, commit, or push in R319B.
- No pi51c sync or pi51c live runtime copy in R319B.
- No DB mutation, DB insert, frontier activation, crawler start/stop, systemd mutation, or URL live probe in R319B.
- No secret, DSN, token, or password printing.

## Target paths

- Future Dutch catalog target: `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json`
- This decision doc target: `docs/TOPIC_CRAWLER_CORE_DUTCH_SOURCE_SEED_URLS_DECISION_2026_05_16.md`

## Dutch source-seed plan summary

- Planned source families: 40
- Planned seed surfaces / seed URLs: 84
- All planned URLs are HTTPS candidate URLs.
- All planned URLs are unique in this decision plan.
- All planned URLs are candidate-manifest only and require later pi51c live probe before any DB/frontier/runtime use.
- Directory-first preference is preserved: official association/member/company directories and port/airport/logistics directories come before individual commercial company pages.

## Architecture boundary

- Crawler_Core collects raw evidence only.
- Crawler_Core-discovered links are raw links, not `added_seeds`.
- Parse_Core may later create candidate `added_seeds` after filtering and pre-ranking.
- Desktop_Import performs stricter validation, enrichment, heavy geocoding/location normalization, and final search-ready output.
- Candidate source-seed catalogs are not live crawler activation.

## Candidate source families

| # | source_code | name | category | quality | decision | seed_url_count | note |
|---:|---|---|---|---|---|---:|---|
| 1 | `nl_fiata_directory` | FIATA Netherlands members directory | global_association_directory | A | ACCEPT_REVIEW | 2 | Directory-first source. Netherlands FIATA member surface for FENEX; candidate-only subordinate directory surface. |
| 2 | `nl_fenex_rotterdamtransport_members` | FENEX members on RotterdamTransport | freight_forwarding_association_member_directory | A_PLUS | ACCEPT_REVIEW | 3 | Directory-first source. FENEX member directory surface under RotterdamTransport; high value for forwarding/logistics companies. |
| 3 | `nl_port_rotterdam_logistics_index` | Port of Rotterdam logistics and company index | port_logistics_company_directory | A_PLUS | ACCEPT_REVIEW | 3 | Directory-first source. Port/logistics index and company/warehousing directory surface around Rotterdam. |
| 4 | `nl_transport_guide_rotterdam` | Transport Guide Rotterdam | rotterdam_transport_directory | A | ACCEPT_REVIEW | 2 | Directory-first source. Rotterdam transport guide directory grouped by transport mode. |
| 5 | `nl_north_sea_port_business_directory` | North Sea Port business directory | port_business_directory | A | ACCEPT_REVIEW | 3 | Directory-first source. Cross-border North Sea Port directory; Netherlands/Belgium port cluster relevance. |
| 6 | `nl_tln_association` | TLN - Transport en Logistiek Nederland | transport_logistics_association | A | ACCEPT_REVIEW | 2 | Association source. Dutch transport and logistics association; direct directory/member surfaces may be added after later live check. |
| 7 | `nl_evofenedex` | evofenedex | trade_logistics_association | A_MINUS | ACCEPT_REVIEW | 2 | Association source for trade/logistics/shippers ecosystem; candidate-only. |
| 8 | `nl_azfreight_forwarders` | AZFreight Netherlands freight forwarders | commercial_freight_directory | B_PLUS | ACCEPT_REVIEW | 2 | Directory-first commercial fallback for freight forwarders; lower priority than official/association/port directories. |
| 9 | `nl_freightnet_forwarders` | Freightnet Netherlands freight forwarders | commercial_freight_directory | B | ACCEPT_REVIEW | 2 | Directory-first commercial fallback. Must not dominate scheduler over official/association directories. |
| 10 | `nl_kompass_shipping_forwarding` | Kompass Netherlands shipping and forwarding agents | commercial_business_directory | B | ACCEPT_REVIEW | 2 | Directory-first commercial business directory; lower priority fallback. |
| 11 | `nl_port_amsterdam` | Port of Amsterdam | port_authority | A | ACCEPT_REVIEW | 2 | Official port authority candidate. |
| 12 | `nl_groningen_seaports` | Groningen Seaports | port_authority | A_MINUS | ACCEPT_REVIEW | 2 | Dutch seaport authority candidate for Eemshaven/Delfzijl. |
| 13 | `nl_port_of_moerdijk` | Port of Moerdijk | port_authority | A_MINUS | ACCEPT_REVIEW | 2 | Official inland/short-sea/industrial port candidate. |
| 14 | `nl_schiphol_cargo` | Schiphol Cargo | air_cargo_airport | A | ACCEPT_REVIEW | 3 | Official airport cargo ecosystem candidate with partners/handlers directory surface. |
| 15 | `nl_air_cargo_netherlands` | Air Cargo Netherlands | air_cargo_association | A_MINUS | ACCEPT_REVIEW | 2 | Dutch air cargo association candidate; directory/member surface may be expanded later. |
| 16 | `nl_deltalinqs` | Deltalinqs | port_industry_association | A_MINUS | ACCEPT_REVIEW | 2 | Rotterdam port and industrial association candidate. |
| 17 | `nl_dutch_fresh_port` | Dutch Fresh Port | fresh_logistics_cluster | B_PLUS | ACCEPT_REVIEW | 2 | Fresh logistics cluster candidate; useful for cold chain / reefer logistics. |
| 18 | `nl_venlo_logistics_hotspot` | Logistics Hotspot Venlo | logistics_cluster | B_PLUS | ACCEPT_REVIEW | 2 | Regional logistics cluster candidate. |
| 19 | `nl_prorail_freight` | ProRail rail freight | rail_freight_infrastructure | A_MINUS | ACCEPT_REVIEW | 2 | Rail freight infrastructure / official railway capacity candidate. |
| 20 | `nl_railcargo_information` | Rail Cargo Information Netherlands | rail_freight_information | B_PLUS | ACCEPT_REVIEW | 2 | Rail freight information candidate. |
| 21 | `nl_kuehne_nagel` | Kuehne+Nagel Netherlands | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Netherlands surface candidate; lower priority than directories. |
| 22 | `nl_dbschenker` | DB Schenker Netherlands | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Netherlands surface candidate. |
| 23 | `nl_dhl_global_forwarding` | DHL Global Forwarding Netherlands | global_forwarding_operator | B | ACCEPT_REVIEW | 2 | Global forwarding Netherlands surface candidate. |
| 24 | `nl_dsv` | DSV Netherlands | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Netherlands surface candidate. |
| 25 | `nl_ceva_logistics` | CEVA Logistics Netherlands | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Netherlands surface candidate. |
| 26 | `nl_geodis` | GEODIS Netherlands | global_logistics_operator | B | ACCEPT_REVIEW | 2 | Global logistics operator Netherlands surface candidate. |
| 27 | `nl_mainfreight` | Mainfreight Netherlands | logistics_operator | B | ACCEPT_REVIEW | 2 | Logistics operator Netherlands surface candidate. |
| 28 | `nl_rhenus` | Rhenus Netherlands | logistics_operator | B | ACCEPT_REVIEW | 2 | Logistics operator Netherlands surface candidate. |
| 29 | `nl_nippon_express` | Nippon Express Netherlands | global_logistics_operator | B_MINUS | ACCEPT_REVIEW | 2 | Global forwarding/logistics Netherlands surface candidate. |
| 30 | `nl_bollore_logistics` | Bolloré Logistics Netherlands | global_logistics_operator | B_MINUS | ACCEPT_REVIEW | 2 | Global logistics Netherlands surface candidate. |
| 31 | `nl_bleckmann` | Bleckmann | contract_logistics_ecommerce | B_PLUS | ACCEPT_REVIEW | 2 | Contract logistics / fashion / e-commerce logistics candidate. |
| 32 | `nl_broekman_logistics` | Broekman Logistics | logistics_terminal_operator | B_PLUS | ACCEPT_REVIEW | 2 | Dutch logistics and terminal services candidate. |
| 33 | `nl_hartman_expedition` | Hartman Expeditie | freight_forwarder | B | ACCEPT_REVIEW | 2 | Commercial freight forwarding candidate. |
| 34 | `nl_rotra` | Rotra | freight_forwarding_logistics_operator | B | ACCEPT_REVIEW | 2 | Commercial forwarding/logistics candidate. |
| 35 | `nl_neele_vat` | Neele-Vat Logistics | freight_forwarding_logistics_operator | B_PLUS | ACCEPT_REVIEW | 2 | Dutch logistics and forwarding operator candidate. |
| 36 | `nl_dj_middelkoop` | D.J. Middelkoop | transport_operator | B_MINUS | ACCEPT_REVIEW | 2 | Transport operator candidate. |
| 37 | `nl_van_der_helm` | Van der Helm Logistics | logistics_operator | B | ACCEPT_REVIEW | 2 | Dutch logistics operator candidate. |
| 38 | `nl_jordex` | Jordex | freight_forwarding_logistics_operator | B | ACCEPT_REVIEW | 2 | Dutch forwarding/logistics candidate. |
| 39 | `nl_hoyer_netherlands` | HOYER Netherlands | bulk_liquid_logistics_operator | B | ACCEPT_REVIEW | 2 | Bulk/liquid logistics Netherlands surface candidate. |
| 40 | `nl_clutch_forwarders` | Clutch Netherlands freight forwarders | commercial_service_directory | B_MINUS | ACCEPT_REVIEW | 2 | Commercial service directory fallback; keep below official/member directories. |

## Candidate seed surfaces

| seed_url_index | source_code | url | candidate_manifest | is_live | enabled | needs_live_check | runtime_activation_policy | safety_state |
|---:|---|---|---|---|---|---|---|---|
| 1 | `nl_fiata_directory` | `https://fiata.org/directory/nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 2 | `nl_fiata_directory` | `https://fiata.org/directory/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 3 | `nl_fenex_rotterdamtransport_members` | `https://rotterdamtransport.com/membership/fenex-netherlands-association-for-forwarding-logistics/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 4 | `nl_fenex_rotterdamtransport_members` | `https://rotterdamtransport.com/companies/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 5 | `nl_fenex_rotterdamtransport_members` | `https://rotterdamtransport.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 6 | `nl_port_rotterdam_logistics_index` | `https://www.portofrotterdam.com/en/logistics` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 7 | `nl_port_rotterdam_logistics_index` | `https://www.portofrotterdam.com/en/logistics/connections` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 8 | `nl_port_rotterdam_logistics_index` | `https://www.portofrotterdam.com/en/logistics/storage-and-transhipment/warehousing/warehousing-options-in-the-rotterdam-port-area` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 9 | `nl_transport_guide_rotterdam` | `https://www.transportguiderotterdam.com/companies` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 10 | `nl_transport_guide_rotterdam` | `https://www.transportguiderotterdam.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 11 | `nl_north_sea_port_business_directory` | `https://www.northseaport.com/en/business-directory` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 12 | `nl_north_sea_port_business_directory` | `https://www.northseaport.com/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 13 | `nl_north_sea_port_business_directory` | `https://www.northseaport.com/en/doing-business` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 14 | `nl_tln_association` | `https://www.tln.nl/over-tln/about-tln` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 15 | `nl_tln_association` | `https://www.tln.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 16 | `nl_evofenedex` | `https://www.evofenedex.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 17 | `nl_evofenedex` | `https://www.evofenedex.nl/kennis/logistiek` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 18 | `nl_azfreight_forwarders` | `https://azfreight.com/country-facility/freight-forwarders-in-netherlands/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 19 | `nl_azfreight_forwarders` | `https://azfreight.com/association/fenex-netherlands-association-for-forwarding-and-logistics/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 20 | `nl_freightnet_forwarders` | `https://www.freightnet.com/directory/p1/cNL/s30.htm` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 21 | `nl_freightnet_forwarders` | `https://www.freightnet.com/directory/p1/cNL/s11.htm` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 22 | `nl_kompass_shipping_forwarding` | `https://lb.kompass.com/z/nl/a/shipping-and-forwarding-agents/75780/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 23 | `nl_kompass_shipping_forwarding` | `https://nl.kompass.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 24 | `nl_port_amsterdam` | `https://www.portofamsterdam.com/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 25 | `nl_port_amsterdam` | `https://www.portofamsterdam.com/en/business` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 26 | `nl_groningen_seaports` | `https://www.groningen-seaports.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 27 | `nl_groningen_seaports` | `https://www.groningen-seaports.com/en/ports/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 28 | `nl_port_of_moerdijk` | `https://www.portofmoerdijk.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 29 | `nl_port_of_moerdijk` | `https://www.portofmoerdijk.nl/en/doing-business/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 30 | `nl_schiphol_cargo` | `https://www.schiphol.nl/en/cargo/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 31 | `nl_schiphol_cargo` | `https://www.schiphol.nl/en/cargo/schiphols-facilities-and-partners-cargo` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 32 | `nl_schiphol_cargo` | `https://www.schiphol.nl/en/cargo/smart-cargo-mainport-program` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 33 | `nl_air_cargo_netherlands` | `https://www.aircargonetherlands.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 34 | `nl_air_cargo_netherlands` | `https://www.aircargonetherlands.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 35 | `nl_deltalinqs` | `https://www.deltalinqs.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 36 | `nl_deltalinqs` | `https://www.deltalinqs.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 37 | `nl_dutch_fresh_port` | `https://www.dutchfreshport.eu/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 38 | `nl_dutch_fresh_port` | `https://www.dutchfreshport.eu/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 39 | `nl_venlo_logistics_hotspot` | `https://www.logisticsinsight.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 40 | `nl_venlo_logistics_hotspot` | `https://www.logisticsinsight.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 41 | `nl_prorail_freight` | `https://www.prorail.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 42 | `nl_prorail_freight` | `https://www.prorail.nl/over-prorail/vervoer/goederenvervoer` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 43 | `nl_railcargo_information` | `https://www.railcargo.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 44 | `nl_railcargo_information` | `https://www.railcargo.nl/english/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 45 | `nl_kuehne_nagel` | `https://nl.kuehne-nagel.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 46 | `nl_kuehne_nagel` | `https://nl.kuehne-nagel.com/en/-/services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 47 | `nl_dbschenker` | `https://www.dbschenker.com/nl-en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 48 | `nl_dbschenker` | `https://www.dbschenker.com/nl-en/products` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 49 | `nl_dhl_global_forwarding` | `https://www.dhl.com/nl-en/home/our-divisions/global-forwarding.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 50 | `nl_dhl_global_forwarding` | `https://www.dhl.com/nl-en/home/our-divisions/global-forwarding/freight-forwarding.html` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 51 | `nl_dsv` | `https://www.dsv.com/en-nl` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 52 | `nl_dsv` | `https://www.dsv.com/en-nl/our-solutions` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 53 | `nl_ceva_logistics` | `https://www.cevalogistics.com/en/where-we-are/europe/netherlands` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 54 | `nl_ceva_logistics` | `https://www.cevalogistics.com/en/our-services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 55 | `nl_geodis` | `https://geodis.com/nl/en` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 56 | `nl_geodis` | `https://geodis.com/nl/en/services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 57 | `nl_mainfreight` | `https://www.mainfreight.com/netherlands/en-nz` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 58 | `nl_mainfreight` | `https://www.mainfreight.com/netherlands/en-nz/services` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 59 | `nl_rhenus` | `https://www.rhenus.group/nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 60 | `nl_rhenus` | `https://www.rhenus.group/nl/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 61 | `nl_nippon_express` | `https://www.nipponexpress.com/nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 62 | `nl_nippon_express` | `https://www.nipponexpress.com/nl/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 63 | `nl_bollore_logistics` | `https://www.bollore-logistics.com/en/country/netherlands/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 64 | `nl_bollore_logistics` | `https://www.bollore-logistics.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 65 | `nl_bleckmann` | `https://www.bleckmann.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 66 | `nl_bleckmann` | `https://www.bleckmann.com/solutions/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 67 | `nl_broekman_logistics` | `https://www.broekmanlogistics.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 68 | `nl_broekman_logistics` | `https://www.broekmanlogistics.com/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 69 | `nl_hartman_expedition` | `https://www.hartmanexpeditie.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 70 | `nl_hartman_expedition` | `https://www.hartmanexpeditie.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 71 | `nl_rotra` | `https://www.rotra.eu/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 72 | `nl_rotra` | `https://www.rotra.eu/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 73 | `nl_neele_vat` | `https://www.neelevat.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 74 | `nl_neele_vat` | `https://www.neelevat.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 75 | `nl_dj_middelkoop` | `https://www.djmiddelkoop.nl/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 76 | `nl_dj_middelkoop` | `https://www.djmiddelkoop.nl/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 77 | `nl_van_der_helm` | `https://www.vanderhelm.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 78 | `nl_van_der_helm` | `https://www.vanderhelm.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 79 | `nl_jordex` | `https://www.jordex.com/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 80 | `nl_jordex` | `https://www.jordex.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 81 | `nl_hoyer_netherlands` | `https://www.hoyer-group.com/en/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 82 | `nl_hoyer_netherlands` | `https://www.hoyer-group.com/en/services/` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 83 | `nl_clutch_forwarders` | `https://clutch.co/nl/logistics/freight-forwarders` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |
| 84 | `nl_clutch_forwarders` | `https://clutch.co/nl/logistics` | true | false | false | true | pi51c_live_probe_required_before_db_or_frontier_insert | candidate_only_not_live |

## Next gate

After R319B is audited, the next safe gate is expected to be:

`R320_NL_SOURCE_SEED_DECISION_DOC_AUDIT_READONLY`

Only after the decision doc passes audit should a separate commit/push gate be considered.

## R319B creation metadata

- Created by gate: `R319B_NL_SOURCE_SEED_DECISION_DOC_LOCAL_ONLY`
- Created at: `2026-05-16T14:01:59+02:00`
- Mutation scope: exactly this decision doc only.
