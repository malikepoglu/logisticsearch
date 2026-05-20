# Bengali source-seed URLs decision — 2026-05-20

- Canonical base HEAD: `67b15516e67f01ba0a74648de07b98c7dd515ef4`
- Language code: `bn`
- Language name: Bengali
- Native name: বাংলা
- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Unique seed URLs: 90
- Status: candidate-only, not live.
- Live probe: not run.
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- Safety: no DB insert, no frontier activation, no crawler start.

## Decision table

| # | Source family | Quality | Decision | Source | Seed 1 | Seed 2 | Rationale |
|---:|---|---|---|---|---|---|---|
| 1 | FIATA Bangladesh directory | A_PLUS | ACCEPT | [Source family link](https://fiata.org/directory/bd/) | [Seed 1](https://fiata.org/directory/bd/) | [Seed 2](https://fiata.org/directory/) | global freight-forwarder association directory; Bangladesh member surface |
| 2 | BAFFA official | A_PLUS | ACCEPT | [Source family link](https://www.baffa-bd.org/) | [Seed 1](https://www.baffa-bd.org/) | [Seed 2](https://www.baffa-bd.org/member-list) | Bangladesh freight-forwarder association official surface |
| 3 | BAFFA member directory PDF | A | ACCEPT | [Source family link](https://www.baffa-bd.org/storage/files/1/news/DRAFT-MEMBERS-LIST-FOR-BAFFA-DIRECTORY-2021.pdf) | [Seed 1](https://www.baffa-bd.org/storage/files/1/news/DRAFT-MEMBERS-LIST-FOR-BAFFA-DIRECTORY-2021.pdf) | [Seed 2](https://www.baffa-bd.org/news) | official BAFFA member directory evidence surface |
| 4 | BSAA official | A_PLUS | ACCEPT | [Source family link](https://bsaa.com.bd/) | [Seed 1](https://bsaa.com.bd/) | [Seed 2](https://bsaa.com.bd/members-info/) | Bangladesh shipping agents association official member surface |
| 5 | Bangladesh Customs | A_PLUS | ACCEPT | [Source family link](https://customs.gov.bd/) | [Seed 1](https://customs.gov.bd/) | [Seed 2](https://customs.gov.bd/portal/services/billTracking/billTracking.jsf) | official customs and trade service surface |
| 6 | Bangladesh Customs agent system | A | ACCEPT | [Source family link](https://bdcams.bdcustoms.gov.bd/) | [Seed 1](https://bdcams.bdcustoms.gov.bd/) | [Seed 2](https://customs.gov.bd/portal/services) | customs agent management and customs service discovery surface |
| 7 | Chattogram Port / PCS | A_PLUS | ACCEPT | [Source family link](https://www.cpatos.gov.bd/pcs/) | [Seed 1](https://www.cpatos.gov.bd/pcs/) | [Seed 2](https://cpa.gov.bd/) | primary Bangladesh seaport and port community system |
| 8 | Mongla Port Authority | A_PLUS | ACCEPT | [Source family link](https://mpa.gov.bd/) | [Seed 1](https://mpa.gov.bd/) | [Seed 2](https://mpa.gov.bd/site/view/notices) | official Bangladesh seaport surface |
| 9 | Payra Port Authority | A | ACCEPT | [Source family link](https://ppa.gov.bd/) | [Seed 1](https://ppa.gov.bd/) | [Seed 2](https://ppa.gov.bd/site/view/notices) | official Bangladesh seaport surface |
| 10 | Chittagong C&F Agents Association | A | ACCEPT | [Source family link](https://cnfctg.net/) | [Seed 1](https://cnfctg.net/) | [Seed 2](https://cnfctg.net/contact-us/) | clearing and forwarding association for Chattogram logistics ecosystem |
| 11 | Dhaka Customs Agents Association | A | ACCEPT_REVIEW | [Source family link](https://www.dcaadhaka.org/) | [Seed 1](https://www.dcaadhaka.org/) | [Seed 2](https://www.dcaadhaka.org/about-us/) | Dhaka customs agents association discovery surface |
| 12 | Benapole C&F Association | A | ACCEPT_REVIEW | [Source family link](https://cnfbpl.com/) | [Seed 1](https://cnfbpl.com/) | [Seed 2](https://cnfbpl.com/weblinks) | land-port clearing and forwarding ecosystem surface |
| 13 | BICDA official | A_MINUS | ACCEPT_REVIEW | [Source family link](https://bicda.com.bd/) | [Seed 1](https://bicda.com.bd/) | [Seed 2](https://fbcci.org/web/members-details/167) | inland container depot association and FBCCI evidence surface |
| 14 | CargoYellowPages Bangladesh | A | ACCEPT | [Source family link](https://www.cargoyellowpages.com/bangladesh_freight_forwarders_cargo_agents.html) | [Seed 1](https://www.cargoyellowpages.com/bangladesh_freight_forwarders_cargo_agents.html) | [Seed 2](https://www.cargoyellowpages.com/) | directory-first Bangladesh freight-forwarder listing surface |
| 15 | Freightnet Bangladesh | A | ACCEPT | [Source family link](https://www.freightnet.com/directory/p1/cBD/s30.htm) | [Seed 1](https://www.freightnet.com/directory/p1/cBD/s30.htm) | [Seed 2](https://www.freightnet.com/directory/p5/cBD/s30.htm) | directory-first Bangladesh freight-forwarder listing surface |
| 16 | AZFreight Bangladesh | A | ACCEPT | [Source family link](https://azfreight.com/country-facility/freight-forwarders-in-bangladesh/) | [Seed 1](https://azfreight.com/country-facility/freight-forwarders-in-bangladesh/) | [Seed 2](https://azfreight.com/directory/) | air cargo/freight directory Bangladesh surface |
| 17 | Ruzave Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://ruzave.com/bangladesh) | [Seed 1](https://ruzave.com/bangladesh) | [Seed 2](https://ruzave.com/) | logistics marketplace/directory Bangladesh surface |
| 18 | GoodFirms Bangladesh logistics | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.goodfirms.co/supply-chain-logistics-companies/ocean-freight/bangladesh) | [Seed 1](https://www.goodfirms.co/supply-chain-logistics-companies/ocean-freight/bangladesh) | [Seed 2](https://www.goodfirms.co/supply-chain-logistics-companies/bangladesh) | review directory for Bangladesh logistics providers |
| 19 | ForwardingCompanies Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://forwardingcompanies.com/) | [Seed 1](https://forwardingcompanies.com/) | [Seed 2](https://forwardingcompanies.com/search/bangladesh) | freight-forwarding directory search surface |
| 20 | FreightPages Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.freightpages.org/) | [Seed 1](https://www.freightpages.org/) | [Seed 2](https://www.freightpages.org/search?q=Bangladesh) | freight directory search surface |
| 21 | WCAworld Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.wcaworld.com/) | [Seed 1](https://www.wcaworld.com/) | [Seed 2](https://www.wcaworld.com/Directory) | global logistics network directory with Bangladesh member discovery |
| 22 | Project Cargo Network Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.projectcargonetwork.com/) | [Seed 1](https://www.projectcargonetwork.com/) | [Seed 2](https://www.projectcargonetwork.com/members/) | project cargo network member discovery |
| 23 | Overseas Project Cargo Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://overseasprojectcargo.com/) | [Seed 1](https://overseasprojectcargo.com/) | [Seed 2](https://overseasprojectcargo.com/members/) | project cargo network member discovery |
| 24 | Security Cargo Network Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.securitycargonetwork.com/) | [Seed 1](https://www.securitycargonetwork.com/) | [Seed 2](https://www.securitycargonetwork.com/members/) | security cargo network member discovery |
| 25 | Aerocean Network Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://aeroceanetwork.net/) | [Seed 1](https://aeroceanetwork.net/) | [Seed 2](https://aeroceanetwork.net/members/) | aero/ocean logistics network member discovery |
| 26 | Pangea Network Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.pangea-network.com/) | [Seed 1](https://www.pangea-network.com/) | [Seed 2](https://www.pangea-network.com/members/) | freight-forwarder network member discovery |
| 27 | DF Alliance Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.df-alliance.com/) | [Seed 1](https://www.df-alliance.com/) | [Seed 2](https://www.df-alliance.com/members) | digital freight alliance member discovery |
| 28 | Kompass Bangladesh | A | ACCEPT_REVIEW | [Source family link](https://bd.kompass.com/) | [Seed 1](https://bd.kompass.com/) | [Seed 2](https://bd.kompass.com/a/transport-logistics/07/) | business directory transport/logistics Bangladesh surface |
| 29 | Bangladesh Yellow Pages | A | ACCEPT_REVIEW | [Source family link](https://www.yellowpages.com.bd/) | [Seed 1](https://www.yellowpages.com.bd/) | [Seed 2](https://www.yellowpages.com.bd/search/logistics) | local business directory logistics surface |
| 30 | Bangladesh Business Directory | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.bangladeshyp.com/) | [Seed 1](https://www.bangladeshyp.com/) | [Seed 2](https://www.bangladeshyp.com/category/Logistics) | local business directory logistics category |
| 31 | BD Trade Info | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.bdtradeinfo.com/) | [Seed 1](https://www.bdtradeinfo.com/) | [Seed 2](https://www.bdtradeinfo.com/search?keyword=freight%20forwarding) | Bangladesh trade directory freight search |
| 32 | Indian Logistics Info / Bengali corridor | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.indianlogisticsinfo.com/) | [Seed 1](https://www.indianlogisticsinfo.com/) | [Seed 2](https://www.indianlogisticsinfo.com/search?keyword=Kolkata) | Bengali regional corridor fallback for Kolkata/West Bengal logistics discovery |
| 33 | Justdial Kolkata freight forwarding | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.justdial.com/Kolkata/Freight-Forwarding-Agencies/nct-10216944) | [Seed 1](https://www.justdial.com/Kolkata/Freight-Forwarding-Agencies/nct-10216944) | [Seed 2](https://www.justdial.com/Kolkata/Freight-Forwarding-Agents/nct-10216958) | Kolkata/West Bengal Bengali-region freight-forwarding fallback |
| 34 | ExportersIndia West Bengal forwarders | B | HOLD_REVIEW | [Source family link](https://www.exportersindia.com/west-bengal/international-freight-forwarder.htm) | [Seed 1](https://www.exportersindia.com/west-bengal/international-freight-forwarder.htm) | [Seed 2](https://www.exportersindia.com/kolkata/freight-forwarding-services.htm) | West Bengal logistics fallback; useful only as weak regional discovery |
| 35 | Akij Logistics | A_MINUS | ACCEPT_REVIEW | [Source family link](https://akijresource.com/akij-logistics-limited/) | [Seed 1](https://akijresource.com/akij-logistics-limited/) | [Seed 2](https://akij.net/) | Bangladesh logistics company candidate surface |
| 36 | Active Logistics Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://activelogbd.com/) | [Seed 1](https://activelogbd.com/) | [Seed 2](https://activelogbd.com/contact/) | Bangladesh logistics company candidate surface |
| 37 | AEX Group Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.aexbd.com/) | [Seed 1](https://www.aexbd.com/) | [Seed 2](https://www.aexbd.com/contact-us/) | Bangladesh logistics company candidate surface |
| 38 | Allport Cargo Services Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.awl.com.bd/) | [Seed 1](https://www.awl.com.bd/) | [Seed 2](https://allportcargoservices.com/) | Bangladesh cargo services candidate surface |
| 39 | EFL Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://efl.global/) | [Seed 1](https://efl.global/) | [Seed 2](https://efl.global/locations/) | global logistics provider with Bangladesh location discovery |
| 40 | Kuehne+Nagel Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://home.kuehne-nagel.com/en/-/locations/bangladesh) | [Seed 1](https://home.kuehne-nagel.com/en/-/locations/bangladesh) | [Seed 2](https://home.kuehne-nagel.com/en/contact) | global logistics provider Bangladesh local entity surface |
| 41 | DHL Global Forwarding Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.dhl.com/bd-en/home.html) | [Seed 1](https://www.dhl.com/bd-en/home.html) | [Seed 2](https://www.dhl.com/bd-en/home/our-divisions/global-forwarding.html) | global forwarding provider Bangladesh local surface |
| 42 | DSV Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.dsv.com/en/countries/asia/bangladesh) | [Seed 1](https://www.dsv.com/en/countries/asia/bangladesh) | [Seed 2](https://www.dsv.com/en/solutions/modes-of-transport) | global forwarding provider Bangladesh country surface |
| 43 | Maersk Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.maersk.com/local-information/asia-pacific/bangladesh) | [Seed 1](https://www.maersk.com/local-information/asia-pacific/bangladesh) | [Seed 2](https://www.maersk.com/local-information) | carrier/logistics local information Bangladesh surface |
| 44 | CMA CGM Bangladesh | A_MINUS | ACCEPT_REVIEW | [Source family link](https://www.cma-cgm.com/local/bangladesh) | [Seed 1](https://www.cma-cgm.com/local/bangladesh) | [Seed 2](https://www.cma-cgm.com/local) | carrier/logistics local information Bangladesh surface |
| 45 | MSC Bangladesh | B_PLUS | ACCEPT_REVIEW | [Source family link](https://www.msc.com/en/local-information/asia-pacific/bangladesh) | [Seed 1](https://www.msc.com/en/local-information/asia-pacific/bangladesh) | [Seed 2](https://www.msc.com/en/local-information) | carrier/logistics local information Bangladesh surface |

## Metadata rule

- `target_language_code=bn`.
- `content_language_code in {bn,en,unknown}`; current selected candidate surfaces are predominantly English fallback and must remain `needs_native_alternative_check` until live/native-locale review.
- `url_locale_code in {bn,en,und}`.
- `covered_country_codes` includes `BD`; West Bengal/Kolkata fallback surfaces include `IN` and `BD`.
- `public_url_probe_status=not_probed` for every seed.
- All family/surface/seed objects are disabled and candidate-only.
