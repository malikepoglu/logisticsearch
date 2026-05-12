# Arabic Source-Seed URLs Decision — 2026-05-12

## Metadata

- Project: LogisticSearch / logisticsearch.net
- Phase: Crawler_Core source-seed / startpoints rollout
- Language slot: `ar`
- Language label: Arabic
- Scope: Arabic-language and Arabic-region logistics/freight/customs directory candidate decisions
- Document status: decision plan only
- Catalog status: not created in this gate
- Runtime status: not live
- Frontier status: no insert
- DB status: no insert
- pi51c status: no sync
- Crawler status: no start
- Live-probe status: not executed

## Canonical architecture boundary

Crawler_Core collects raw evidence only.

Crawler_Core may record discovered links as raw link evidence, but raw links are not `added_seeds`.

Parse_Core is responsible for filtering raw links with source context, taxonomy keywords, page signals, and pre-ranking. Parse_Core may create `added_seeds` after pre-ranking.

Desktop_Import on Ubuntu Desktop converts pre-ranking into real ranking / final rank.

Therefore, this document does not activate any seed in the live frontier.

## Arabic rollout decision

Arabic source-seed rollout should not mean only Arabic-language pages.

For this project, Arabic rollout means:

1. Arabic-language surfaces where available.
2. Arabic-region logistics coverage where the authoritative source is English or bilingual.
3. MENA / GCC freight forwarding, customs broker, clearing agent, port, free zone, airport cargo, and logistics association coverage.
4. Directory-first source selection.

The user does not read Arabic fluently; therefore directory-quality, authority, visible structure, and live-probe safety matter more than broad crawling.

## Acceptance rules for Arabic source-seed candidates

A candidate should be preferred when it has one or more of these properties:

- Official association member directory.
- Official customs broker / clearing agent directory.
- Direct company/member list with contact or website fields.
- Transport/logistics/freight/customs specialization.
- Strong source authority.
- Low ambiguity that the listed entities are logistics-related.
- Stable country or association surface.
- Crawlable without login and without executing risky workflows.

A candidate should be demoted or held when it has these risks:

- Broad business directory with mixed industries.
- Search-form-only or interactive UI that requires live-probe before safe manifesting.
- Commercial SEO directory with duplicate/spam risk.
- Blog-style “best companies” article.
- Social media list.
- PDF/Scribd/copied spreadsheet.
- Single-company promotional page.
- Aggressive pagination requirement.
- Same host dominates too much of the seed catalog.

## Mandatory runtime safety fields for future catalog JSON

Every future Arabic catalog seed must start with:

- `is_enabled=false`
- `needs_live_check=true`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
- `manual_review_required=true` for commercial or mixed directories
- `no_aggressive_pagination=true`
- `same_day_full_country_expansion=false`
- `max_initial_depth=0` or `max_initial_depth=1`
- No live frontier activation
- No DB insert
- No crawler start
- Live probe must be a separate explicit gate

## Source decision matrix

### ACCEPT / A_PLUS — highest-value direct directories

| Decision | Tier | Proposed source_code | Source | URL | Why |
|---|---:|---|---|---|---|
| ACCEPT | A_PLUS | `ae_nafl_member_directory` | UAE NAFL Member List | `https://nafl.ae/member-list/` | Direct freight/logistics member list. Visible company rows include logistics company names and contact fields. Strong UAE/GCC directory seed. |
| ACCEPT | A_PLUS | `eg_eiffa_members_directory` | EIFFA Members Directory | `https://eiffa.com/members-directory/` | Egyptian International Freight Forwarding Association member directory. Direct Egypt freight-forwarding company coverage. |
| ACCEPT | A_PLUS | `sa_zatca_fasah_customs_brokers_directory` | Saudi ZATCA / Fasah customs brokers directory surface | `https://zatca.gov.sa/en/eServices/Pages/eServices_272.aspx` and `https://www.fasah.sa/trade/home/en/` | Official Saudi customs broker / customs license surface. Customs broker data is high-value logistics evidence. Needs live-probe because workflow may be form/search based. |
| ACCEPT | A_PLUS | `bh_customs_clearing_agencies_directory` | Bahrain eGov / Customs Affairs clearing agencies directory | `https://services.bahrain.bh/wps/portal/CCAS_en` | Official Bahrain customs clearing agencies directory. High authority and directly relevant. |
| ACCEPT | A_PLUS | `om_fiata_country_member_directory` | FIATA Oman country member directory | `https://fiata.org/directory/om/` | Direct individual freight/logistics members for Oman. Useful because official Oman Customs company surface may be harder to crawl reliably. |

### ACCEPT / A or A_MINUS — strong directories with controlled scope

| Decision | Tier | Proposed source_code | Source | URL | Why |
|---|---:|---|---|---|---|
| ACCEPT_REVIEW | A | `jo_jla_general_assembly_members` | Jordanian Logistics Association members | `https://www.jla.jo/en/companies.php` | Member directory with categories such as Sea Freight, Air Freight, Land Freight, Clearance, and Logistic. Needs live-probe for structure. |
| ACCEPT_REVIEW | A_MINUS | `ae_fta_clearing_companies` | UAE Federal Tax Authority clearing companies | `https://tax.gov.ae/en/tax.support/clearing.companies.aspx` | Official UAE clearing companies list. Page appears dated, therefore review and low depth. |
| ACCEPT_REVIEW | A_MINUS | `ae_tamm_clearing_agent_directory` | Abu Dhabi TAMM clearing agent directory | `https://www.tamm.abudhabi/wb/adc/delegate-clearing-agent/directory?lang=ar` | Official Abu Dhabi clearing-agent directory. Arabic surface. Needs live-probe because it may be interactive. |
| ACCEPT_REVIEW | B_PLUS | `ae_dubai_south_company_directory_logistics_filter` | Dubai South Company Directory | `https://dubaisouth.my.salesforce-sites.com/CompanyDirectory` | Official free-zone company directory with logistics/cargo/customs-broker activity signals. Mixed-sector risk, so filter and low depth. |
| ACCEPT_REVIEW | B_PLUS | `ae_emirates_shipping_association_members` | Emirates Shipping Association members | `https://7emirates.com/members/` | Maritime/shipping association member surface. Good for maritime logistics, but not pure freight-forwarder directory. |

### FIATA shared MENA / Arabic-region source-family

FIATA is a strong source, but it is a single host. To prevent domain dominance, FIATA country pages must not be modeled as many independent source families.

Recommended future catalog model:

- `source_code`: `fiata_mena_arabic_region_member_directory_shared`
- `source_host`: `fiata.org`
- `family_metadata.host_budget_group`: `fiata.org`
- `same_day_full_country_expansion`: `false`
- `recommended_rotation`: 1–2 country surfaces per day after live-probe
- `max_initial_depth`: 0 or 1
- `source_role`: `association_member_directory`
- `decision_status`: `ACCEPT`
- `domain_dominance_control`: required

| Decision | Tier | Country / surface | URL | Notes |
|---|---:|---|---|---|
| ACCEPT | A_PLUS | UAE | `https://fiata.org/directory/ae/` | Strong UAE member directory; should complement NAFL, not replace it. |
| ACCEPT | A | Saudi Arabia | `https://fiata.org/directory/sa/` | Individual freight/logistics members listed. |
| ACCEPT | A | Egypt | `https://fiata.org/directory/eg/` | Complements EIFFA directory. |
| ACCEPT | A | Oman | `https://fiata.org/directory/om/` | Individual members listed. |
| ACCEPT | A | Qatar | `https://fiata.org/directory/qa/` | Useful Qatar company coverage; QAFL page can remain authority context. |
| ACCEPT | A | Jordan | `https://fiata.org/directory/jo/` | Complements JLA member directory. |
| ACCEPT | A_MINUS | Bahrain | `https://fiata.org/directory/bh/` | Complements Bahrain clearing-agency directory. |
| ACCEPT_REVIEW | B_PLUS | Kuwait | `https://fiata.org/directory/kw/` | Smaller surface; low depth and review. |
| ACCEPT | A_MINUS | Tunisia | `https://fiata.org/directory/tn/` | Direct member list and useful North Africa coverage. |
| ACCEPT_REVIEW | B_PLUS | Algeria | `https://fiata.org/directory/dz/` | Direct member list; review due lower scale and quality uncertainty. |
| ACCEPT_REVIEW | B | Lebanon | `https://fiata.org/directory/lb/` | Smaller country surface; low depth. |
| HOLD | B_MINUS | Yemen | `https://fiata.org/directory/ye/` | Country risk and freshness/reliability concerns; hold for later review. |
| HOLD | reference | Morocco | `https://fiata.org/directory/ma/` | Association/reference value, but direct broad company directory was not clearly confirmed in this pass. |

### ACCEPT_REVIEW — commercial/global directories with manual controls

| Decision | Tier | Proposed source_code | Source | URL | Why / Control |
|---|---:|---|---|---|---|
| ACCEPT_REVIEW | B | `freightnet_arabic_region_country_pages` | Freightnet country/category pages | `https://www.freightnet.com/directory/` | Direct freight/logistics/cargo company directory surfaces by country/category. Commercial source, so low depth and no aggressive pagination. |
| ACCEPT_REVIEW | B_MINUS | `cargoyellowpages_arabic_region_country_pages` | CargoYellowPages country pages | `https://www.cargoyellowpages.com/` | Freight/cargo agent list surfaces exist. Commercial quality risk, so review only. |
| ACCEPT_REVIEW | B | `yellowpages_uae_logistics_freight_forwarders` | UAE YellowPages logistics/freight categories | `https://www.yellowpages-uae.com/` | Rich UAE category directory, but broad commercial directory and duplicate risk. |
| HOLD / ACCEPT_REVIEW | B_PLUS | `iata_cargolink_directory` | IATA CargoLink | `https://www.iata.org/en/publications/directories/cargolink/` | High authority, but search-form/interactive behavior requires live-probe before manifest inclusion. |
| HOLD / SHARED_REFERENCE | B_PLUS | `wcaworld_directory_shared` | WCAworld directory | `https://www.wcaworld.com/directory` | Large global forwarding network. Useful reference, but global/domain dominance and UI risks. |
| HOLD / ACCEPT_REVIEW | B | `jctrans_country_surfaces` | JCtrans company country surfaces | `https://www.jctrans.com/en/company/list` | Commercial global network. Use only after live-probe and low-depth policy. |
| HOLD | B | `lognet_global_directory` | Lognet Global directory | `https://www.lognetglobal.com/directory` | Potential global network reference, not a first Arabic-core priority. |

### HOLD / authority context

| Decision | Proposed source_code | Source | URL | Why |
|---|---|---|---|---|
| HOLD | `qa_qafl_authority_reference` | Qatar Association for Freight Forwarding and Logistics / Qatar Chamber | `https://www.qatarchamber.com/qafl/` | Strong authority context; direct operational company directory not confirmed as a stable crawl surface in this pass. |
| HOLD | `ma_affm_authority_reference` | Moroccan freight forwarders association / FIATA Morocco reference | `https://fiata.org/directory/ma/` | Association context; direct company directory not confirmed enough for core startpoint. |
| HOLD | `jo_jla_authority_context` | Jordanian Logistics Association general association page | `https://www.jla.jo/` | Authority context; actual directory candidate is the `/en/companies.php` surface. |
| HOLD | `ae_jafza_logistics_context` | JAFZA logistics/free-zone context | `https://www.jafza.ae/` | Important logistics ecosystem context, but not a direct firm directory startpoint by itself. |

### REJECT_FOR_CORE / manual-only evidence

| Decision | Source type | Why |
|---|---|---|
| REJECT_FOR_CORE | Scribd / copied spreadsheets / random PDFs | Source trust, freshness, copyright, and duplication risks. |
| REJECT_FOR_CORE | Facebook groups/pages | Poor crawl quality and unstable social content. |
| REJECT_FOR_CORE | “Best logistics companies” blog articles | SEO/promotional content; usually not a stable directory. |
| REJECT_FOR_CORE | Single company pages | A company can be an entity seed later, but not a multi-company source directory. |
| HOLD_ONLY | Broad chamber/business directories without logistics filter | Too noisy unless a stable logistics/customs/freight category is confirmed. |

## Recommended first Arabic catalog shape

For the future catalog JSON, do not include every candidate as a separate source family.

Recommended initial catalog shape:

- Approximate source families / grouped surfaces: 18–22
- Direct association/customs directories: 7–9
- FIATA grouped source-family: 1 family with multiple country seed surfaces
- Commercial directories: 3–5, all low-depth and manual-review
- Authority context / HOLD records: can be documented, but not necessarily included as enabled crawl candidates

Suggested first catalog group list:

1. `ae_nafl_member_directory`
2. `eg_eiffa_members_directory`
3. `sa_zatca_fasah_customs_brokers_directory`
4. `bh_customs_clearing_agencies_directory`
5. `jo_jla_general_assembly_members`
6. `ae_fta_clearing_companies`
7. `ae_tamm_clearing_agent_directory`
8. `ae_dubai_south_company_directory_logistics_filter`
9. `ae_emirates_shipping_association_members`
10. `fiata_mena_arabic_region_member_directory_shared`
11. `freightnet_arabic_region_country_pages`
12. `cargoyellowpages_arabic_region_country_pages`
13. `yellowpages_uae_logistics_freight_forwarders`
14. `iata_cargolink_directory`
15. `wcaworld_directory_shared`
16. `jctrans_country_surfaces`
17. `qa_qafl_authority_reference`
18. `ma_affm_authority_reference`

## Arabic-specific crawl policy notes

- Arabic-script pages must be UTF-8 safe.
- Arabic right-to-left content must not be normalized destructively.
- Arabic and English versions of the same source should not be counted as separate independent authority if they share the same host and same data.
- Use country/language/source context for Parse_Core; do not assume every Arabic-region company page is relevant.
- Customs broker directories are highly valuable even when not freight-forwarder-only, because customs clearance is a logistics network signal.
- Free-zone directories are valuable only when filtered to logistics, cargo, freight, customs broker, warehousing, port, terminal, or transport activities.
- Global commercial directories must not dominate the scheduler.

## Next gates

1. `SOURCE_SEED_R131_ARABIC_DECISION_DOC_AUDIT_READONLY`
2. `SOURCE_SEED_R132_ARABIC_DECISION_DOC_COMMIT_PUSH_GATE`
3. `SOURCE_SEED_R133_ARABIC_DECISION_DOC_POST_PUSH_SEAL_READONLY`
4. `SOURCE_SEED_R134_ARABIC_CATALOG_MANIFEST_PATCH_PLAN_READONLY`
5. `SOURCE_SEED_R135_ARABIC_CATALOG_MANIFEST_PATCH_LOCAL_ONLY`

## Non-mutation statement

This document is a decision plan only.

This gate does not:

- create Arabic catalog JSON
- insert into DB
- insert into frontier
- sync to pi51c
- start crawler
- mutate systemd
- live-probe URLs
- fetch page bodies
