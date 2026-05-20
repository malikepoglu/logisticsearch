# Hindi source-seed URLs decision

- Language code: `hi`
- Language name: Hindi
- Native name: हिन्दी
- Scope: India / Hindi locale coverage
- Catalog path: `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json`
- Candidate manifest: `true`
- Is live: `false`
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Safety: no DB insert, no frontier activation, no public URL probe, no crawler start.

## Decision table

| # | Source family | Quality | Decision | Type | Seed 1 | Seed 2 |
|---:|---|---|---|---|---|---|
| 1 | [Source family link](https://fiata.org/directory/in/) FIATA India members directory | `A_PLUS` | `ACCEPT` | `directory` | [Seed 1](https://fiata.org/directory/in/) | [Seed 2](https://fiata.org/directory/) |
| 2 | [Source family link](https://www.fffai.org/) FFFAI India freight forwarders association | `A_PLUS` | `ACCEPT` | `association` | [Seed 1](https://www.fffai.org/) | [Seed 2](https://azfreight.com/association/fffai-federation-of-freight-forwarders-associations-in-india/) |
| 3 | [Source family link](https://www.acaai.in/) ACAAI air cargo association India | `A_PLUS` | `ACCEPT` | `association` | [Seed 1](https://www.acaai.in/) | [Seed 2](https://www.indianlogisticsinfo.com/indian_logistics_profiles/the_air_cargo_agents_association_of_india.html) |
| 4 | [Source family link](https://www.iiff.in/) IIFF freight-forwarding training ecosystem | `A` | `ACCEPT_REVIEW` | `association_ecosystem` | [Seed 1](https://www.iiff.in/) | [Seed 2](https://www.iiff.in/about-us/) |
| 5 | [Source family link](https://www.cargoyellowpages.com/en/india/) CargoYellowPages India | `A` | `ACCEPT` | `directory` | [Seed 1](https://www.cargoyellowpages.com/en/india/) | [Seed 2](https://www.cargoyellowpages.com/india_freight_forwarders_cargo_agents.html) |
| 6 | [Source family link](https://www.cargoyellowpages.com/india3_freight_forwarders_cargo_agents.html) CargoYellowPages India continuation pages | `A_MINUS` | `ACCEPT_REVIEW` | `directory` | [Seed 1](https://www.cargoyellowpages.com/india3_freight_forwarders_cargo_agents.html) | [Seed 2](https://www.cargoyellowpages.com/india2_freight_forwarders_cargo_agents.html) |
| 7 | [Source family link](https://www.freightnet.com/directory/p1/cIN/s30.htm) Freightnet India freight forwarders | `A` | `ACCEPT` | `directory` | [Seed 1](https://www.freightnet.com/directory/p1/cIN/s30.htm) | [Seed 2](https://www.freightnet.com/directory/p1/cIN/s99.htm) |
| 8 | [Source family link](https://forwardingcompanies.com/in/india) ForwardingCompanies India | `A` | `ACCEPT` | `directory` | [Seed 1](https://forwardingcompanies.com/in/india) | [Seed 2](https://forwardingcompanies.com/) |
| 9 | [Source family link](https://azfreight.com/country-facility/freight-forwarders-in-india/) AZFreight India | `A` | `ACCEPT` | `directory` | [Seed 1](https://azfreight.com/country-facility/freight-forwarders-in-india/) | [Seed 2](https://azfreight.com/) |
| 10 | [Source family link](https://ruzave.com/india) Ruzave India shipping/freight directory | `B_PLUS` | `ACCEPT_REVIEW` | `directory` | [Seed 1](https://ruzave.com/india) | [Seed 2](https://ruzave.com/) |
| 11 | [Source family link](https://www.freightpages.org/) FreightPages global logistics directory | `B_PLUS` | `ACCEPT_REVIEW` | `directory` | [Seed 1](https://www.freightpages.org/) | [Seed 2](https://www.freightpages.org/freight-forwarders/) |
| 12 | [Source family link](https://www.indianlogisticsinfo.com/) Indian Logistics Info | `A_MINUS` | `ACCEPT_REVIEW` | `directory_media` | [Seed 1](https://www.indianlogisticsinfo.com/) | [Seed 2](https://www.indianlogisticsinfo.com/indian_logistics_profiles/) |
| 13 | [Source family link](https://indianyellowpages.net.in/cargo-logistics) Indian Yellow Pages cargo/logistics | `B_PLUS` | `ACCEPT_REVIEW` | `directory` | [Seed 1](https://indianyellowpages.net.in/cargo-logistics) | [Seed 2](https://indianyellowpages.net.in/cargo-logistics/global-shipping-forwarding) |
| 14 | [Source family link](https://in.kompass.com/a/logistics-and-procurement-services/75940/) Kompass India logistics/procurement | `B_PLUS` | `ACCEPT_REVIEW` | `directory` | [Seed 1](https://in.kompass.com/a/logistics-and-procurement-services/75940/) | [Seed 2](https://kompassindia.com/) |
| 15 | [Source family link](https://www.goodfirms.co/supply-chain-logistics-companies/india) GoodFirms India logistics list | `B_PLUS` | `ACCEPT_REVIEW` | `directory_ranking` | [Seed 1](https://www.goodfirms.co/supply-chain-logistics-companies/india) | [Seed 2](https://www.goodfirms.co/supply-chain-logistics-companies) |
| 16 | [Source family link](https://clutch.co/in/logistics/supply-chain-management) Clutch India logistics rankings | `B_PLUS` | `ACCEPT_REVIEW` | `directory_ranking` | [Seed 1](https://clutch.co/in/logistics/supply-chain-management) | [Seed 2](https://clutch.co/in/logistics/air-freight-companies) |
| 17 | [Source family link](https://www.wcaworld.com/directory) WCAworld India-discoverable directory | `A_MINUS` | `ACCEPT_REVIEW` | `network_directory` | [Seed 1](https://www.wcaworld.com/directory) | [Seed 2](https://www.wcaworld.com/home) |
| 18 | [Source family link](https://www.iata.org/en/publications/directories/cargolink/directory/) IATA CargoLink | `A` | `ACCEPT_REVIEW` | `air_cargo_directory` | [Seed 1](https://www.iata.org/en/publications/directories/cargolink/directory/) | [Seed 2](https://www.iata.org/en/publications/directories/cargolink/) |
| 19 | [Source family link](https://www.df-alliance.com/benefits/member-directory) DF Alliance member directory | `B_PLUS` | `ACCEPT_REVIEW` | `network_directory` | [Seed 1](https://www.df-alliance.com/benefits/member-directory) | [Seed 2](https://www.df-alliance.com/) |
| 20 | [Source family link](https://www.securitycargonetwork.com/members/) Security Cargo Network members | `B_PLUS` | `ACCEPT_REVIEW` | `network_directory` | [Seed 1](https://www.securitycargonetwork.com/members/) | [Seed 2](https://www.securitycargonetwork.com/) |
| 21 | [Source family link](https://aeroceanetwork.net/) AerOceaNetwork | `B` | `ACCEPT_REVIEW` | `network_directory` | [Seed 1](https://aeroceanetwork.net/) | [Seed 2](https://aeroceanetwork.net/about-us/) |
| 22 | [Source family link](https://overseasprojectcargo.com/InternationalFreightForwarders/india-freight-forwarders/) Overseas Project Cargo India directory | `B` | `ACCEPT_REVIEW` | `project_cargo_directory` | [Seed 1](https://overseasprojectcargo.com/InternationalFreightForwarders/india-freight-forwarders/) | [Seed 2](https://overseasprojectcargo.com/) |
| 23 | [Source family link](https://projectcargonetwork.com/) Project Cargo Network | `B` | `ACCEPT_REVIEW` | `project_cargo_network` | [Seed 1](https://projectcargonetwork.com/) | [Seed 2](https://projectcargonetwork.com/members/) |
| 24 | [Source family link](https://www.pangea-network.com/) Pangea Logistics Network | `B` | `ACCEPT_REVIEW` | `network_directory` | [Seed 1](https://www.pangea-network.com/) | [Seed 2](https://www.pangea-network.com/members/) |
| 25 | [Source family link](https://www.wcaprojects.com/) WCA Projects | `B_PLUS` | `ACCEPT_REVIEW` | `project_cargo_network` | [Seed 1](https://www.wcaprojects.com/) | [Seed 2](https://www.wcaprojects.com/news/) |
| 26 | [Source family link](https://goulip.in/) Unified Logistics Interface Platform India | `A_PLUS` | `ACCEPT` | `official_platform` | [Seed 1](https://goulip.in/) | [Seed 2](https://logixtics.nldsl.in/) |
| 27 | [Source family link](https://nlpmarine.gov.in/) National Logistics Portal Marine / Sagar Setu | `A_PLUS` | `ACCEPT` | `official_platform` | [Seed 1](https://nlpmarine.gov.in/) | [Seed 2](https://www.digitalindia.gov.in/initiative/national-logistics-portal-marine/) |
| 28 | [Source family link](https://www.fois.indianrail.gov.in/RailSAHAY/index.jsp) Indian Railways freight / FOIS | `A_PLUS` | `ACCEPT` | `official_platform` | [Seed 1](https://www.fois.indianrail.gov.in/RailSAHAY/index.jsp) | [Seed 2](https://www.fois.indianrail.gov.in/FOISWebPortal/index.jsp) |
| 29 | [Source family link](https://www.icegate.gov.in/) Customs / trade logistics official surfaces | `A_PLUS` | `ACCEPT` | `official_platform` | [Seed 1](https://www.icegate.gov.in/) | [Seed 2](https://www.cbic.gov.in/) |
| 30 | [Source family link](https://www.jnport.gov.in/) JNPA port logistics | `A` | `ACCEPT` | `official_port` | [Seed 1](https://www.jnport.gov.in/) | [Seed 2](https://mopsw.nic.in/sagarvidyakosh/index.php?title=Jawaharlal_Nehru_Port_Authority) |
| 31 | [Source family link](https://concorindia.co.in/) CONCOR intermodal/rail logistics | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://concorindia.co.in/) | [Seed 2](https://concorindia.co.in/terminal.aspx) |
| 32 | [Source family link](https://www.indiapost.gov.in/) India Post logistics/parcels | `A` | `ACCEPT_REVIEW` | `official_postal_logistics` | [Seed 1](https://www.indiapost.gov.in/) | [Seed 2](https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx) |
| 33 | [Source family link](https://www.bluedart.com/) Blue Dart Express | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.bluedart.com/) | [Seed 2](https://www.bluedart.com/tracking) |
| 34 | [Source family link](https://www.delhivery.com/) Delhivery | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.delhivery.com/) | [Seed 2](https://www.delhivery.com/track/package) |
| 35 | [Source family link](https://www.dtdc.in/) DTDC Express | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.dtdc.in/) | [Seed 2](https://www.dtdc.in/tracking.asp) |
| 36 | [Source family link](https://www.allcargologistics.com/) Allcargo Logistics | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.allcargologistics.com/) | [Seed 2](https://www.allcargologistics.com/services) |
| 37 | [Source family link](https://www.gati.com/) Allcargo Gati | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.gati.com/) | [Seed 2](https://www.gati.com/track/) |
| 38 | [Source family link](https://mahindralogistics.com/) Mahindra Logistics | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://mahindralogistics.com/) | [Seed 2](https://mahindralogistics.com/services/) |
| 39 | [Source family link](https://tcil.com/) Transport Corporation of India | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://tcil.com/) | [Seed 2](https://tcil.com/services/) |
| 40 | [Source family link](https://www.safexpress.com/) Safexpress | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.safexpress.com/) | [Seed 2](https://www.safexpress.com/track/) |
| 41 | [Source family link](https://cjdarcl.com/) CJ Darcl Logistics | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://cjdarcl.com/) | [Seed 2](https://cjdarcl.com/contact-us/) |
| 42 | [Source family link](https://www.tvsscs.com/) TVS Supply Chain Solutions India | `A` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.tvsscs.com/) | [Seed 2](https://www.tvsscs.com/india/) |
| 43 | [Source family link](https://www.snowman.in/) Snowman Logistics cold-chain | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.snowman.in/) | [Seed 2](https://www.snowman.in/warehousing/) |
| 44 | [Source family link](https://www.vrlgroup.in/) VRL Logistics | `A_MINUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.vrlgroup.in/) | [Seed 2](https://www.vrlgroup.in/vrl_branch_list.aspx) |
| 45 | [Source family link](https://www.navata.com/) Navata Road Transport | `B_PLUS` | `ACCEPT_REVIEW` | `company_official` | [Seed 1](https://www.navata.com/) | [Seed 2](https://www.navata.com/branch-locator/) |

## Counts

- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Unique seed URLs: 90
- Duplicate seed URLs: 0
- Non-HTTPS seed URLs: 0
- Empty seed URLs: 0

## Notes

- Directory sites are prioritized first, followed by associations, official platforms, ports, networks, and company official surfaces.
- Hindi-native logistics source surfaces are limited; this catalog intentionally models India/Hindi locale coverage with many English fallback public surfaces.
- All source families, surfaces, and seed URLs remain candidate-only and require pi51c live probe before any DB/frontier insertion.
