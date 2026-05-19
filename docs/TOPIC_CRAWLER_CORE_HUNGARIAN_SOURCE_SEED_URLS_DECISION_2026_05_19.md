# Hungarian source-seed URLs decision — 2026-05-19

Language: Hungarian  
Native name: Magyar  
Language code: `hu`

## Safety state

- `candidate_manifest=true`
- `is_live=false`
- `enabled=false`
- `needs_live_check=true`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- `safety_state=candidate_only_not_live`
- No DB insert.
- No frontier insert.
- No crawler activation.
- No public source URL probe in this gate.

## Decision summary

- Source families: 45
- Seed surfaces: 90
- Seed URLs: 90
- Duplicate seed URLs: 0
- Non-HTTPS seed URLs: 0
- Empty seed URLs: 0
- Quality distribution: `{'A': 11, 'A_MINUS': 16, 'A_PLUS': 5, 'B': 2, 'B_PLUS': 11}`
- Decision distribution: `{'ACCEPT': 12, 'ACCEPT_REVIEW': 31, 'HOLD_REVIEW': 2}`

## Source and seed review table

| # | Source family | Source family link | Seed-1 link | Seed-2 link | Quality | Decision |
|---:|---|---|---|---|---|---|
| 1 | FIATA Hungary directory | [fiata.org](https://fiata.org/directory/hu/) | [Seed-1](https://fiata.org/directory/hu/) | [Seed-2](https://www.szallitmanyozok.hu/en) | A_PLUS | ACCEPT |
| 2 | Association of Hungarian Forwarders members | [szallitmanyozok.hu](https://szallitmanyozok.hu/en/members) | [Seed-1](https://szallitmanyozok.hu/en/members) | [Seed-2](https://szallitmanyozok.hu/en) | A_PLUS | ACCEPT |
| 3 | Hungarian Road Transport Association / MKFE | [www.mkfe.hu](https://www.mkfe.hu/en/about-us.html) | [Seed-1](https://www.mkfe.hu/en/about-us.html) | [Seed-2](https://www.iru.org/news-resources/members-directory/mkfe) | A_PLUS | ACCEPT |
| 4 | CLECAT / Hungarian logistics contact surface | [www.clecat.org](https://www.clecat.org/members/full-members) | [Seed-1](https://www.clecat.org/members/full-members) | [Seed-2](https://www.uirr.com/peers/mszsz) | A | ACCEPT |
| 5 | Freightnet Hungary directory | [www.freightnet.com](https://www.freightnet.com/directory/p3/cHU/s99.htm) | [Seed-1](https://www.freightnet.com/directory/p3/cHU/s99.htm) | [Seed-2](https://www.freightnet.com/directory/p1/cHU.htm) | A | ACCEPT_REVIEW |
| 6 | AZFreight Hungary freight forwarders | [azfreight.com](https://azfreight.com/country-facility/freight-forwarders-in-hungary/) | [Seed-1](https://azfreight.com/country-facility/freight-forwarders-in-hungary/) | [Seed-2](https://azfreight.com/country-facility/air-freight-in-hungary/) | A | ACCEPT_REVIEW |
| 7 | SeaRates Hungary logistics services | [www.searates.com](https://www.searates.com/reference/logistics-service/hungary/) | [Seed-1](https://www.searates.com/reference/logistics-service/hungary/) | [Seed-2](https://www.searates.com/reference/portdistance/) | A | ACCEPT_REVIEW |
| 8 | Ruzave Hungary freight directory | [ruzave.com](https://ruzave.com/hungary) | [Seed-1](https://ruzave.com/hungary) | [Seed-2](https://ruzave.com/hungary/freight-forwarders/freight-forwardingservices/) | A_MINUS | ACCEPT_REVIEW |
| 9 | ForwardingCompanies Budapest | [forwardingcompanies.com](https://forwardingcompanies.com/in/budapest) | [Seed-1](https://forwardingcompanies.com/in/budapest) | [Seed-2](https://forwardingcompanies.com/in/hungary) | A_MINUS | ACCEPT_REVIEW |
| 10 | RailMarket Hungary logistics companies | [railmarket.com](https://railmarket.com/eu/hungary/logistics-companies) | [Seed-1](https://railmarket.com/eu/hungary/logistics-companies) | [Seed-2](https://railmarket.com/eu/hungary/rail-freight) | A | ACCEPT_REVIEW |
| 11 | Kompass Hungary logistics category | [hu.kompass.com](https://hu.kompass.com/) | [Seed-1](https://hu.kompass.com/a/tartalykocsis-szallitmanyozas/75040/) | [Seed-2](https://hu.kompass.com/a/szallitmanyozas/75/) | A_MINUS | ACCEPT_REVIEW |
| 12 | GoodFirms Hungary logistics list | [www.goodfirms.co](https://www.goodfirms.co/supply-chain-logistics-companies/hungary) | [Seed-1](https://www.goodfirms.co/supply-chain-logistics-companies/hungary) | [Seed-2](https://www.goodfirms.co/directory/country/top-supply-chain-logistics-companies/hu) | B_PLUS | ACCEPT_REVIEW |
| 13 | Mordor Hungary freight and logistics company list | [www.mordorintelligence.com](https://www.mordorintelligence.com/industry-reports/hungary-freight-and-logistics-market/companies) | [Seed-1](https://www.mordorintelligence.com/industry-reports/hungary-freight-and-logistics-market/companies) | [Seed-2](https://www.mordorintelligence.com/industry-reports/hungary-freight-and-logistics-market) | B_PLUS | ACCEPT_REVIEW |
| 14 | Lusha Hungary transportation logistics list | [www.lusha.com](https://www.lusha.com/company-search/transportation-logistics-and-storage/a64fd456c3/hungary/139/) | [Seed-1](https://www.lusha.com/company-search/transportation-logistics-and-storage/a64fd456c3/hungary/139/) | [Seed-2](https://www.lusha.com/company-search/truck-transportation/b7152ac602/hungary/139/) | B | HOLD_REVIEW |
| 15 | CompanyData Hungary logistics companies | [companydata.com](https://companydata.com/hungary/logistics-companies-hungary/) | [Seed-1](https://companydata.com/hungary/logistics-companies-hungary/) | [Seed-2](https://companydata.com/hungary/transport-companies-hungary/) | B | HOLD_REVIEW |
| 16 | Waberer's Group Hungary | [www.waberers.com](https://www.waberers.com/en) | [Seed-1](https://www.waberers.com/en) | [Seed-2](https://www.waberers.com/en/about-us/about-waberers) | A_PLUS | ACCEPT |
| 17 | Trans-Sped Hungary | [www.trans-sped.hu](https://www.trans-sped.hu/en/introduction) | [Seed-1](https://www.trans-sped.hu/en/introduction) | [Seed-2](https://www.trans-sped.hu/en/services) | A_PLUS | ACCEPT |
| 18 | DSV Hungary | [www.dsv.com](https://www.dsv.com/en/countries/europe/hungary) | [Seed-1](https://www.dsv.com/en/countries/europe/hungary) | [Seed-2](https://www.dsv.com/en-nl/destinations/transport-europe/transport-hungary) | A | ACCEPT |
| 19 | DHL Hungary logistics | [www.dhl.com](https://www.dhl.com/hu-en/home/our-divisions/supply-chain.html) | [Seed-1](https://www.dhl.com/hu-en/home/our-divisions/supply-chain.html) | [Seed-2](https://www.dhl.com/hu-en/home/our-divisions/global-forwarding.html) | A | ACCEPT |
| 20 | Kuehne+Nagel Hungary | [hu.kuehne-nagel.com](https://hu.kuehne-nagel.com/) | [Seed-1](https://hu.kuehne-nagel.com/) | [Seed-2](https://hu.kuehne-nagel.com/en/-/services) | A | ACCEPT |
| 21 | Raben Hungary | [hungary.raben-group.com](https://hungary.raben-group.com/) | [Seed-1](https://hungary.raben-group.com/) | [Seed-2](https://hungary.raben-group.com/en/services) | A | ACCEPT |
| 22 | Gebrüder Weiss Hungary | [www.gw-world.com](https://www.gw-world.com/hu/) | [Seed-1](https://www.gw-world.com/hu/) | [Seed-2](https://www.gw-world.com/hu/szolgaltatasok/) | A | ACCEPT |
| 23 | HGL Group Hungary | [hgllog.com](https://hgllog.com/) | [Seed-1](https://hgllog.com/) | [Seed-2](https://hgllog.com/services/) | A_MINUS | ACCEPT_REVIEW |
| 24 | Rail Cargo Hungaria | [rch.railcargo.com](https://rch.railcargo.com/hu/) | [Seed-1](https://rch.railcargo.com/hu/) | [Seed-2](https://rch.railcargo.com/hu/szolgaltatasok) | A | ACCEPT |
| 25 | Airmax Cargo Budapest | [hu.kompass.com](https://hu.kompass.com/c/airmax-cargo-budapest-zrt/hu1167024/) | [Seed-1](https://hu.kompass.com/c/airmax-cargo-budapest-zrt/hu1167024/) | [Seed-2](https://www.airmaxcargo.com/) | A_MINUS | ACCEPT_REVIEW |
| 26 | Logwin Air+Ocean Hungary | [hu.kompass.com](https://hu.kompass.com/c/logwin-air-ocean-hungary/hu0058646/) | [Seed-1](https://hu.kompass.com/c/logwin-air-ocean-hungary/hu0058646/) | [Seed-2](https://www.logwin-logistics.com/) | A_MINUS | ACCEPT_REVIEW |
| 27 | MASPED Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/masped-logisztika-kft/hu0052061/) | [Seed-1](https://hu.kompass.com/c/masped-logisztika-kft/hu0052061/) | [Seed-2](https://www.masped.hu/) | A_MINUS | ACCEPT_REVIEW |
| 28 | Quehenberger Logistics HU | [hu.kompass.com](https://hu.kompass.com/c/quehenberger-logistics-hu-kft/hu0017789/) | [Seed-1](https://hu.kompass.com/c/quehenberger-logistics-hu-kft/hu0017789/) | [Seed-2](https://www.quehenberger.com/) | A_MINUS | ACCEPT_REVIEW |
| 29 | Rhenus Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/rhenus-logistics-hungary-kft/hu1144896/) | [Seed-1](https://hu.kompass.com/c/rhenus-logistics-hungary-kft/hu1144896/) | [Seed-2](https://www.rhenus.group/hu/en/) | A_MINUS | ACCEPT_REVIEW |
| 30 | Rohlig SUUS Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/rohlig-suus-logistics-hungary-kft/hu0099925/) | [Seed-1](https://hu.kompass.com/c/rohlig-suus-logistics-hungary-kft/hu0099925/) | [Seed-2](https://www.suus.com/) | A_MINUS | ACCEPT_REVIEW |
| 31 | DP World Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/syncreon-technology-hungary-kft/hu1242051/) | [Seed-1](https://hu.kompass.com/c/syncreon-technology-hungary-kft/hu1242051/) | [Seed-2](https://www.dpworld.com/) | A_MINUS | ACCEPT_REVIEW |
| 32 | Eurasia Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/eurasia-logistics-kft/hu0014479/) | [Seed-1](https://hu.kompass.com/c/eurasia-logistics-kft/hu0014479/) | [Seed-2](https://www.eurasialogistics.hu/) | A_MINUS | ACCEPT_REVIEW |
| 33 | Ekol Logistics Hungary | [hu.kompass.com](https://hu.kompass.com/c/ekol-logistics-kft/hu1219171/) | [Seed-1](https://hu.kompass.com/c/ekol-logistics-kft/hu1219171/) | [Seed-2](https://www.ekol.com/) | A_MINUS | ACCEPT_REVIEW |
| 34 | Intertranscoop Logistics | [hu.kompass.com](https://hu.kompass.com/hu/c/intertranscoop-logisztika-kft/hu9682785/) | [Seed-1](https://hu.kompass.com/hu/c/intertranscoop-logisztika-kft/hu9682785/) | [Seed-2](https://www.intertranscoop.hu/) | A_MINUS | ACCEPT_REVIEW |
| 35 | Botlik-Trans Hungary | [hu.kompass.com](https://hu.kompass.com/c/botlik-trans-kft/hu0767072/) | [Seed-1](https://hu.kompass.com/c/botlik-trans-kft/hu0767072/) | [Seed-2](https://www.botliktrans.hu/) | B_PLUS | ACCEPT_REVIEW |
| 36 | Hellmann Hungary | [www.hellmann.com](https://www.hellmann.com/en/hungary) | [Seed-1](https://www.hellmann.com/en/hungary) | [Seed-2](https://hu.kompass.com/c/innight-hungary-express-kft/hu0346352/) | A_MINUS | ACCEPT_REVIEW |
| 37 | CEVA Logistics Hungary | [www.cevalogistics.com](https://www.cevalogistics.com/en/country/hungary) | [Seed-1](https://www.cevalogistics.com/en/country/hungary) | [Seed-2](https://www.cevalogistics.com/en/services) | A_MINUS | ACCEPT_REVIEW |
| 38 | Nippon Express Hungary | [www.nipponexpress.com](https://www.nipponexpress.com/) | [Seed-1](https://www.nipponexpress.com/local/hu/) | [Seed-2](https://www.nipponexpress.com/service/) | B_PLUS | ACCEPT_REVIEW |
| 39 | Yusen Logistics Hungary | [www.yusen-logistics.com](https://www.yusen-logistics.com/) | [Seed-1](https://www.yusen-logistics.com/en/europe/hungary) | [Seed-2](https://www.yusen-logistics.com/en/services) | B_PLUS | ACCEPT_REVIEW |
| 40 | C.H. Robinson Hungary | [www.chrobinson.com](https://www.chrobinson.com/) | [Seed-1](https://www.chrobinson.com/en-us/about-us/global-offices/europe/hungary/) | [Seed-2](https://www.chrobinson.com/en-us/shippers/freight-services/) | B_PLUS | ACCEPT_REVIEW |
| 41 | FIEGE Hungary | [www.fiege.com](https://www.fiege.com/en) | [Seed-1](https://www.fiege.com/en/locations/hungary) | [Seed-2](https://www.fiege.com/en/services) | B_PLUS | ACCEPT_REVIEW |
| 42 | Plimsoll Hungary / RailMarket | [railmarket.com](https://railmarket.com/eu/hungary/logistics-companies) | [Seed-1](https://railmarket.com/eu/profile/plimsoll-zrt) | [Seed-2](https://railmarket.com/eu/hungary/companies) | B_PLUS | ACCEPT_REVIEW |
| 43 | Baja Public Port / RailMarket | [railmarket.com](https://railmarket.com/eu/hungary/logistics-companies) | [Seed-1](https://railmarket.com/eu/profile/baja-public-port-ltd) | [Seed-2](https://www.bajaport.hu/) | B_PLUS | ACCEPT_REVIEW |
| 44 | Den Hartogh Hungary / RailMarket | [railmarket.com](https://railmarket.com/eu/hungary/logistics-companies) | [Seed-1](https://railmarket.com/eu/profile/den-hartogh-hungary) | [Seed-2](https://www.denhartogh.com/) | B_PLUS | ACCEPT_REVIEW |
| 45 | HOPI Hungary | [www.goodfirms.co](https://www.goodfirms.co/supply-chain-logistics-companies/hungary) | [Seed-1](https://www.goodfirms.co/supply-chain-logistics-companies/hungary/hopi) | [Seed-2](https://www.hopi.hu/) | B_PLUS | ACCEPT_REVIEW |

## Boundary rule

Crawler Core stores discovered page links only as raw link evidence. Raw links are not `added_seeds`.
Parse Core creates `added_seeds` after pre-ranking.
Desktop Import on Ubuntu Desktop converts pre-ranking into true ranking/final rank.

## Activation rule

This Hungarian catalog remains candidate-only until a future controlled pi51c live-probe gate explicitly promotes selected surfaces.
