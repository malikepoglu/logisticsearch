# Crawler Core German Source/Seed URL Decision
# Crawler Core Almanca Source/Seed URL Kararı

## English

### Purpose

This document records the German source/seed decision for crawler_core startpoints. It is a decision document only. It does not activate live crawling, does not insert frontier rows, does not mutate PostgreSQL, does not start crawler runtime, and does not sync pi51c.

### Important refinement: source role is not always directory

Not every accepted German source is a direct company directory. Some accepted records are directory candidates, while others are discovery surfaces, context surfaces, association surfaces, commercial discovery surfaces, or entity/context seeds. The crawler may use these links to discover outbound/internal links, but extraction claims must depend on the actual discovered page evidence.

This refinement applies to all 25 languages. English and Turkish must receive a later read-only parity gap audit and, if needed, a catalog or doc patch so their catalogs can also distinguish directory candidates, discovery surfaces, entity/context seeds, shared global surfaces, and low-priority commercial discovery surfaces.

### Added user-provided German candidates

The user-provided direct-list candidates were added to the decision model. RailMarket, BVL Firmenmitglieder, Firmendatenbanken, and CargoYellowPages Germany root are accepted for review. Wikipedia category remains context-only. Wer-zu-wem remains access-review hold until live check confirms availability.

### Scope

- Language: German
- Planned language code: `de`
- Planned catalog path: `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json`
- Current action: decision document only
- Catalog patch: later explicit gate
- pi51c sync: later explicit gate
- Runtime activation: not allowed in this document

### Canonical standard

- `source_family_code` is a stable internal code, not a URL.
- `source_host` is the domain.
- `source_root_url` is the source root.
- `source_category` must be an array.
- `seed_surfaces` must be an array.
- `seed_urls` must be an array.
- `source_role` must classify how the source is intended to be used.
- `directory_confidence` must distinguish strong directories from discovery/context/entity sources.
- `catalog_activation_class` must say whether the source can enter catalog as disabled candidate, shared reference, or hold.
- `candidate_seed_urls` remains a decision/research-document field and must not be added to catalog JSON unless a later explicit contract change allows it.
- All German seed URLs must start disabled before live review.
- Runtime activation policy must remain `manual_review_required_before_frontier` or an equivalent gated policy requiring pi51c live probe before DB/frontier insert.
- HOLD sources must not enter the initial active catalog manifest.
- Shared FIATA German surface must not be copied as an independent German-owned source family.
- New links discovered by crawler_core can become Added Seeds after parse_core pre-ranking and desktop_import review on Ubuntu Desktop.

### Hard runtime boundary

- NO DB insert/update/delete permission exists in this document.
- No crawler run is authorized by this document.
- No systemd mutation is authorized by this document.
- No pi51c sync is authorized by this document.
- Live frontier activation permission does not exist in this document.

### Decision summary after user-source addition

- German candidate source family count: 28
- Accepted core source family count: 19
- HOLD source count: 8
- Shared reference surface count: 1
- Total candidate seed URL count: 32
- Accepted core seed URL count: 23
- WLW logistics and spedition search surfaces are merged under one `wlw_de` source family.
- `biek_kep_reference` is the canonical parcel/express association reference code.
- `cargoyellowpages_de` now owns both Germany root and Frankfurt airport page as seed URLs.

### Quality distribution

- `A`: 3
- `A_MINUS`: 9
- `A_PLUS`: 2
- `B`: 7
- `B_MINUS`: 3
- `B_PLUS`: 4

### Decision status distribution

- `ACCEPT`: 1
- `ACCEPT_REVIEW`: 18
- `HOLD_ACCESS_REVIEW`: 1
- `HOLD_CONTEXT_SOURCE`: 4
- `HOLD_ENTITY_SOURCE`: 3
- `REFERENCE_SHARED_SOURCE_SURFACE`: 1

### Source role distribution

- `airport_context_discovery_surface`: 1
- `association_context_discovery_surface`: 1
- `association_context_source`: 1
- `association_discovery_surface`: 3
- `association_member_directory_candidate`: 1
- `association_structure_discovery_surface`: 1
- `commercial_directory_candidate`: 7
- `commercial_discovery_surface`: 2
- `commercial_rail_logistics_directory_candidate`: 1
- `community_context_discovery_surface`: 1
- `company_entity_seed`: 3
- `directory_candidate`: 1
- `encyclopedic_entity_reference`: 1
- `port_context_source`: 1
- `sector_reference_source`: 1
- `shared_global_source_surface`: 1
- `trade_fair_discovery_surface`: 1

### Directory confidence distribution

- `high`: 5
- `low`: 8
- `medium`: 10
- `none`: 4
- `unknown`: 1

### Catalog activation class distribution

- `accepted_disabled_commercial_discovery_seed`: 7
- `accepted_disabled_directory_seed`: 2
- `accepted_disabled_discovery_seed`: 8
- `accepted_disabled_low_priority_discovery_seed`: 2
- `hold_access_review_required`: 1
- `hold_entity_not_directory`: 3
- `hold_not_active_startpoint`: 4
- `shared_reference_not_german_owned`: 1

### Accepted core German sources

#### Accepted 01: `dslv_org`

- Quality: `A_PLUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_discovery_surface`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `official_association_directory, freight_forwarder_directory`
- Root URL: https://www.dslv.org/
- Notes: German federal freight forwarding/logistics association. Strong authority; direct member/company extraction surface must be verified.
- Seed URLs:
  - https://www.dslv.org/

#### Accepted 02: `bgl_ev`

- Quality: `A`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_structure_discovery_surface`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `road_freight_directory, official_association_directory`
- Root URL: https://www.bgl-ev.de/
- Notes: German road freight/logistics association. Useful for association structure and outgoing links; direct company list must be verified.
- Seed URLs:
  - https://www.bgl-ev.de/
  - https://www.bgl-ev.de/unsere-verbandsstruktur/

#### Accepted 03: `hafen_hamburg_branchenbuch`

- Quality: `A`
- Decision status: `ACCEPT`
- Source role: `directory_candidate`
- Directory confidence: `high`
- Catalog activation class: `accepted_disabled_directory_seed`
- Categories: `port_authority_or_port_directory, commercial_logistics_directory, sea_freight_directory`
- Root URL: https://www.hafen-hamburg.de/de/hafenbranchenbuch/
- Notes: Strong Hamburg port logistics directory candidate.
- Seed URLs:
  - https://www.hafen-hamburg.de/de/hafenbranchenbuch/

#### Accepted 04: `frankfurt_cargohub`

- Quality: `A_MINUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `airport_context_discovery_surface`
- Directory confidence: `low`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `airport_cargo_authority_or_directory, air_cargo_directory`
- Root URL: https://www.frankfurt-cargohub.com/en.html
- Notes: Frankfurt air cargo hub/context source. Useful for link discovery; company listing surface must be checked before extraction claims.
- Seed URLs:
  - https://www.frankfurt-cargohub.com/en.html

#### Accepted 05: `aircargo_community_frankfurt`

- Quality: `A_MINUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `community_context_discovery_surface`
- Directory confidence: `low`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `airport_cargo_authority_or_directory, air_cargo_directory, network_directory`
- Root URL: https://www.aircargocommunity.com/en/standort/
- Notes: Frankfurt cargo community/location context. Useful for outgoing link discovery; member/company extraction needs review.
- Seed URLs:
  - https://www.aircargocommunity.com/en/standort/

#### Accepted 06: `die_gueterbahnen`

- Quality: `A_MINUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_discovery_surface`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `rail_freight_directory, official_association_directory`
- Root URL: https://die-gueterbahnen.com/
- Notes: Rail freight association/network candidate. Member/list surface must be validated.
- Seed URLs:
  - https://die-gueterbahnen.com/

#### Accepted 07: `vdv_de`

- Quality: `A_MINUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_context_discovery_surface`
- Directory confidence: `low`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `rail_freight_directory, official_association_directory, public_transport_logistics_reference`
- Root URL: https://www.vdv.de/
- Notes: German transport association. Use only if a freight/logistics member surface is found; otherwise downgrade to hold.
- Seed URLs:
  - https://www.vdv.de/

#### Accepted 08: `bsk_kran_schwertransport`

- Quality: `B_PLUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_discovery_surface`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `project_cargo_directory, heavy_lift_directory, official_association_directory`
- Root URL: https://www.bsk-ffm.de/
- Notes: Heavy transport/crane association candidate. Member directory surface requires review.
- Seed URLs:
  - https://www.bsk-ffm.de/

#### Accepted 09: `transport_logistic_exhibitor_directory`

- Quality: `B_PLUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `trade_fair_discovery_surface`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_discovery_seed`
- Categories: `trade_fair_exhibitor_directory, commercial_logistics_directory`
- Root URL: https://transportlogistic.de/
- Notes: German logistics trade fair source. Exact exhibitor directory URL must be verified before catalog activation.
- Seed URLs:
  - https://transportlogistic.de/

#### Accepted 10: `wlw_de`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, b2b_supplier_directory, road_freight_directory`
- Root URL: https://www.wlw.de/
- Notes: Commercial B2B discovery source. Combines logistics and spedition search surfaces under one source family to avoid duplicate host/source-family identity.
- Seed URLs:
  - https://www.wlw.de/de/suche/logistik/deutschland
  - https://www.wlw.de/de/suche/speditionen/deutschland

#### Accepted 11: `kompass_de_transport_logistics`

- Quality: `B_PLUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, b2b_supplier_directory`
- Root URL: https://www.kompass.com/
- Notes: Commercial directory already used in English seed family. Later decide whether German catalog owns local surface or references shared commercial source.
- Seed URLs:
  - https://www.kompass.com/z/de/a/transportation-and-logistics-services/75/

#### Accepted 12: `freightnet_de`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, freight_forwarder_directory, air_cargo_directory`
- Root URL: https://www.freightnet.com/
- Notes: Commercial freight directory Germany pages. Useful discovery, not authority; apply low budget and diversity penalty.
- Seed URLs:
  - https://www.freightnet.com/directory/p1/cDE/s30.htm
  - https://www.freightnet.com/directory/p1/cDE/s4.htm

#### Accepted 13: `cargoyellowpages_de`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, air_cargo_directory`
- Root URL: https://www.cargoyellowpages.com/
- Notes: Commercial cargo directory. Germany root is better than only Frankfurt airport page because it exposes city/airport route fan-out.
- Seed URLs:
  - https://mobile.cargoyellowpages.com/germany/
  - https://mobile.cargoyellowpages.com/germany/frankfurt-am-main-airport.html

#### Accepted 14: `gelbe_seiten_spedition`

- Quality: `B_MINUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_discovery_surface`
- Directory confidence: `low`
- Catalog activation class: `accepted_disabled_low_priority_discovery_seed`
- Categories: `commercial_logistics_directory, road_freight_directory`
- Root URL: https://www.gelbeseiten.de/
- Notes: Commercial local directory. Root is broad; exact query URL must be found before strong activation.
- Seed URLs:
  - https://www.gelbeseiten.de/

#### Accepted 15: `europages_de_transport_logistik`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_discovery_surface`
- Directory confidence: `low`
- Catalog activation class: `accepted_disabled_low_priority_discovery_seed`
- Categories: `commercial_logistics_directory, b2b_supplier_directory`
- Root URL: https://www.europages.de/
- Notes: Commercial B2B discovery. Root is broad; exact category/query URL must be verified.
- Seed URLs:
  - https://www.europages.de/

#### Accepted 16: `hamburg_de_logistik_branchenbuch`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `medium`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, city_business_directory`
- Root URL: https://www.hamburg.de/
- Notes: City/business directory discovery. Keep separate from Hafen Hamburg authority directory.
- Seed URLs:
  - https://www.hamburg.de/branchenbuch/hamburg/hafencity/10239793/n0/

#### Accepted 17: `railmarket_de_logistics_companies`

- Quality: `B_PLUS`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_rail_logistics_directory_candidate`
- Directory confidence: `high`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `rail_freight_directory, commercial_logistics_directory, b2b_supplier_directory`
- Root URL: https://de.railmarket.com/
- Notes: German RailMarket logistics-company listing. Direct company rows exist; rail/logistics scope is valuable but commercial and rail-biased.
- Seed URLs:
  - https://de.railmarket.com/eu/germany/logistics-companies

#### Accepted 18: `bvl_firmenmitglieder`

- Quality: `A`
- Decision status: `ACCEPT_REVIEW`
- Source role: `association_member_directory_candidate`
- Directory confidence: `high`
- Catalog activation class: `accepted_disabled_directory_seed`
- Categories: `official_association_directory, logistics_network_directory, company_member_directory`
- Root URL: https://www.bvl.de/firmenmitglieder
- Notes: BVL company-member profile directory. Strong association/member source; includes companies, universities, and research institutions, so extraction must classify entity type carefully.
- Seed URLs:
  - https://www.bvl.de/firmenmitglieder

#### Accepted 19: `firmendatenbanken_logistik_unternehmen`

- Quality: `B`
- Decision status: `ACCEPT_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `high`
- Catalog activation class: `accepted_disabled_commercial_discovery_seed`
- Categories: `commercial_logistics_directory, company_directory, b2b_supplier_directory`
- Root URL: https://www.firmendatenbanken.de/
- Notes: Direct logistics-company list with firm detail links and pagination. Some data freshness indicators are older than one year, so keep B quality and review before activation.
- Seed URLs:
  - https://www.firmendatenbanken.de/firmen/liste/logistik-unternehmen/1.html

### HOLD German sources

#### HOLD 01: `bremenports`

- Quality: `A_MINUS`
- Decision status: `HOLD_CONTEXT_SOURCE`
- Source role: `port_context_source`
- Directory confidence: `low`
- Catalog activation class: `hold_not_active_startpoint`
- Categories: `port_authority_or_port_directory, public_infrastructure_reference`
- Root URL: https://bremenports.de/
- Why HOLD: Port authority/context source. Needs exact directory/company surface before manifest-core acceptance.
- Candidate seed URLs:
  - https://bremenports.de/

#### HOLD 02: `duisport`

- Quality: `A_MINUS`
- Decision status: `HOLD_ENTITY_SOURCE`
- Source role: `company_entity_seed`
- Directory confidence: `none`
- Catalog activation class: `hold_entity_not_directory`
- Categories: `inland_port_logistics, logistics_operator, public_infrastructure_reference`
- Root URL: https://www.duisport.de/
- Why HOLD: Important inland port/operator entity. Keep as entity/context unless clear company directory is found.
- Candidate seed URLs:
  - https://www.duisport.de/

#### HOLD 03: `deutsche_bahn_cargo`

- Quality: `A_MINUS`
- Decision status: `HOLD_ENTITY_SOURCE`
- Source role: `company_entity_seed`
- Directory confidence: `none`
- Catalog activation class: `hold_entity_not_directory`
- Categories: `rail_freight_operator, rail_freight_directory`
- Root URL: https://www.dbcargo.com/
- Why HOLD: Major rail freight company/operator, not a multi-company directory.
- Candidate seed URLs:
  - https://www.dbcargo.com/

#### HOLD 04: `biek_kep_reference`

- Quality: `A_MINUS`
- Decision status: `HOLD_CONTEXT_SOURCE`
- Source role: `association_context_source`
- Directory confidence: `low`
- Catalog activation class: `hold_not_active_startpoint`
- Categories: `courier_express_parcel_directory, official_association_directory`
- Root URL: https://www.biek.de/
- Why HOLD: Parcel/express association reference. Use only if a member/company list surface exists.
- Candidate seed URLs:
  - https://www.biek.de/

#### HOLD 05: `kombiverkehr`

- Quality: `A_MINUS`
- Decision status: `HOLD_ENTITY_SOURCE`
- Source role: `company_entity_seed`
- Directory confidence: `none`
- Catalog activation class: `hold_entity_not_directory`
- Categories: `rail_freight_operator, intermodal_logistics, logistics_operator`
- Root URL: https://www.kombiverkehr.de/
- Why HOLD: Intermodal operator/entity. Useful seed later, but not a directory source.
- Candidate seed URLs:
  - https://www.kombiverkehr.de/

#### HOLD 06: `deutsche_verkehrszeitung_directory_reference`

- Quality: `B_MINUS`
- Decision status: `HOLD_CONTEXT_SOURCE`
- Source role: `sector_reference_source`
- Directory confidence: `none`
- Catalog activation class: `hold_not_active_startpoint`
- Categories: `sector_reference, logistics_news_reference`
- Root URL: https://www.dvz.de/
- Why HOLD: Sector reference/news, not direct source manifest candidate.
- Candidate seed URLs:
  - https://www.dvz.de/

#### HOLD 07: `wikipedia_de_logistikunternehmen_category`

- Quality: `B_MINUS`
- Decision status: `HOLD_CONTEXT_SOURCE`
- Source role: `encyclopedic_entity_reference`
- Directory confidence: `low`
- Catalog activation class: `hold_not_active_startpoint`
- Categories: `sector_reference, company_entity_reference`
- Root URL: https://de.wikipedia.org/
- Why HOLD: Wikipedia category has structured subcategories and entity links but is not a primary logistics directory source. Keep as context/reference only.
- Candidate seed URLs:
  - https://de.wikipedia.org/wiki/Kategorie:Logistikunternehmen_(Deutschland)

#### HOLD 08: `wer_zu_wem_logistik`

- Quality: `B`
- Decision status: `HOLD_ACCESS_REVIEW`
- Source role: `commercial_directory_candidate`
- Directory confidence: `unknown`
- Catalog activation class: `hold_access_review_required`
- Categories: `commercial_logistics_directory, company_directory`
- Root URL: https://www.wer-zu-wem.de/
- Why HOLD: User-provided direct logistics-service provider list. Keep out of active manifest until pi51c/live check confirms availability.
- Candidate seed URLs:
  - https://www.wer-zu-wem.de/dienstleister/logistik.html

### Shared reference surfaces

#### Shared 01: `fiata_directory_de_reference`

- Quality: `A_PLUS`
- Decision status: `REFERENCE_SHARED_SOURCE_SURFACE`
- Source role: `shared_global_source_surface`
- Directory confidence: `high`
- Catalog activation class: `shared_reference_not_german_owned`
- Categories: `official_association_directory, freight_forwarder_directory`
- Root URL: https://fiata.org/directory/de/
- Rule: Shared FIATA German surface. Do not duplicate as an independent German-owned source family.
- Candidate seed URLs:
  - https://fiata.org/directory/de/

### German catalog patch rule

The first German catalog manifest patch may include only records with decision status `ACCEPT` or `ACCEPT_REVIEW`. Records with decision status beginning with `HOLD_` must remain outside the initial catalog manifest. Records with `REFERENCE_SHARED_SOURCE_SURFACE` must not be copied as independent German-owned source families.

### Added Seeds lifecycle

New main links discovered by crawler_core should not be blindly activated. They can be stored as Added Seeds candidates, processed by parse_core for pre-ranking, then reviewed through desktop_import on Ubuntu Desktop. After review, they may become accepted seeds, lower-priority discovery seeds, entity/context seeds, duplicate references, or rejected noise.

### Required EN/TR parity follow-up

Because this is a system-model improvement, English and Turkish must receive a later read-only parity gap audit and, if needed, a catalog/doc patch that adds equivalent role semantics without changing existing URLs or activation safety.

## Türkçe

### Amaç

Bu doküman crawler_core startpoints hattında Almanca source/seed kararını kaydeder. Bu yalnızca karar dokümanıdır. Canlı crawl başlatmaz, frontier satırı yazmaz, PostgreSQL değiştirmez, crawler runtime başlatmaz ve pi51c sync yapmaz.

### Önemli iyileştirme: source her zaman directory değildir

Almanca listedeki her accepted kaynak doğrudan firma directory değildir. Bazıları directory adayıdır; bazıları discovery surface, context surface, association surface, commercial discovery surface veya entity/context seed olarak kullanılmalıdır. Crawler bu linkleri link keşfi/yayılma için kullanabilir, fakat firma extraction iddiası sadece canlı sayfa kanıtına göre yapılmalıdır.

Bu iyileştirme 25 dilin tamamı için geçerlidir. English ve Turkish catalog tarafına da daha sonra parity audit/patch ile aynı source role modeli uygulanmalıdır.

### Kullanıcının verdiği yeni adaylar

Kullanıcının verdiği direkt liste adayları karar modeline eklendi. RailMarket, BVL Firmenmitglieder, Firmendatenbanken ve CargoYellowPages Germany root accepted review olarak değerlendirildi. Wikipedia category context-only olarak tutuldu. Wer-zu-wem live/access kontrol geçmeden hold kalır.

### Added Seeds yaşam döngüsü

crawler_core tarafından toplanan yeni ana linkler körlemesine aktif edilmez. Bunlar Added Seeds adayı olarak saklanabilir, parse_core ile pre-ranking yapılır, desktop_import ile Ubuntu Desktop tarafına geldikten sonra incelenir. İnceleme sonrası accepted seed, düşük öncelikli discovery seed, entity/context seed, duplicate reference veya noise/reject olarak sınıflandırılır.

### Canlı kullanım sınırı

- NO DB insert/update/delete bu dokümanla yetkilendirilmez.
- Crawler run yoktur.
- systemd mutation yoktur.
- pi51c sync yoktur.
- live frontier activation yoktur.

### Karar özeti

- Almanca aday source family sayısı: 28
- Accepted core source family sayısı: 19
- HOLD source sayısı: 8
- Shared reference surface sayısı: 1
- Toplam aday seed URL sayısı: 32
- Accepted core seed URL sayısı: 23
- WLW logistics ve spedition search surface kayıtları tek `wlw_de` source family altında birleştirildi.
- `biek_kep_reference` kanonik parcel/express association reference kodudur.
- `cargoyellowpages_de` artık Germany root ve Frankfurt airport page seed URL'lerini birlikte taşır.

## Machine-readable decision records

```json
[
  {
    "code": "dslv_org",
    "quality": "A_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_discovery_surface",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "official_association_directory",
      "freight_forwarder_directory"
    ],
    "root_url": "https://www.dslv.org/",
    "notes": "German federal freight forwarding/logistics association. Strong authority; direct member/company extraction surface must be verified.",
    "seed_urls": [
      "https://www.dslv.org/"
    ]
  },
  {
    "code": "bgl_ev",
    "quality": "A",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_structure_discovery_surface",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "road_freight_directory",
      "official_association_directory"
    ],
    "root_url": "https://www.bgl-ev.de/",
    "notes": "German road freight/logistics association. Useful for association structure and outgoing links; direct company list must be verified.",
    "seed_urls": [
      "https://www.bgl-ev.de/",
      "https://www.bgl-ev.de/unsere-verbandsstruktur/"
    ]
  },
  {
    "code": "hafen_hamburg_branchenbuch",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_role": "directory_candidate",
    "directory_confidence": "high",
    "catalog_activation_class": "accepted_disabled_directory_seed",
    "categories": [
      "port_authority_or_port_directory",
      "commercial_logistics_directory",
      "sea_freight_directory"
    ],
    "root_url": "https://www.hafen-hamburg.de/de/hafenbranchenbuch/",
    "notes": "Strong Hamburg port logistics directory candidate.",
    "seed_urls": [
      "https://www.hafen-hamburg.de/de/hafenbranchenbuch/"
    ]
  },
  {
    "code": "frankfurt_cargohub",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "airport_context_discovery_surface",
    "directory_confidence": "low",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "airport_cargo_authority_or_directory",
      "air_cargo_directory"
    ],
    "root_url": "https://www.frankfurt-cargohub.com/en.html",
    "notes": "Frankfurt air cargo hub/context source. Useful for link discovery; company listing surface must be checked before extraction claims.",
    "seed_urls": [
      "https://www.frankfurt-cargohub.com/en.html"
    ]
  },
  {
    "code": "aircargo_community_frankfurt",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "community_context_discovery_surface",
    "directory_confidence": "low",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "airport_cargo_authority_or_directory",
      "air_cargo_directory",
      "network_directory"
    ],
    "root_url": "https://www.aircargocommunity.com/en/standort/",
    "notes": "Frankfurt cargo community/location context. Useful for outgoing link discovery; member/company extraction needs review.",
    "seed_urls": [
      "https://www.aircargocommunity.com/en/standort/"
    ]
  },
  {
    "code": "fiata_directory_de_reference",
    "quality": "A_PLUS",
    "decision_status": "REFERENCE_SHARED_SOURCE_SURFACE",
    "source_role": "shared_global_source_surface",
    "directory_confidence": "high",
    "catalog_activation_class": "shared_reference_not_german_owned",
    "categories": [
      "official_association_directory",
      "freight_forwarder_directory"
    ],
    "root_url": "https://fiata.org/directory/de/",
    "notes": "Shared FIATA German surface. Do not duplicate as an independent German-owned source family.",
    "seed_urls": [
      "https://fiata.org/directory/de/"
    ]
  },
  {
    "code": "bremenports",
    "quality": "A_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_role": "port_context_source",
    "directory_confidence": "low",
    "catalog_activation_class": "hold_not_active_startpoint",
    "categories": [
      "port_authority_or_port_directory",
      "public_infrastructure_reference"
    ],
    "root_url": "https://bremenports.de/",
    "notes": "Port authority/context source. Needs exact directory/company surface before manifest-core acceptance.",
    "seed_urls": [
      "https://bremenports.de/"
    ]
  },
  {
    "code": "duisport",
    "quality": "A_MINUS",
    "decision_status": "HOLD_ENTITY_SOURCE",
    "source_role": "company_entity_seed",
    "directory_confidence": "none",
    "catalog_activation_class": "hold_entity_not_directory",
    "categories": [
      "inland_port_logistics",
      "logistics_operator",
      "public_infrastructure_reference"
    ],
    "root_url": "https://www.duisport.de/",
    "notes": "Important inland port/operator entity. Keep as entity/context unless clear company directory is found.",
    "seed_urls": [
      "https://www.duisport.de/"
    ]
  },
  {
    "code": "deutsche_bahn_cargo",
    "quality": "A_MINUS",
    "decision_status": "HOLD_ENTITY_SOURCE",
    "source_role": "company_entity_seed",
    "directory_confidence": "none",
    "catalog_activation_class": "hold_entity_not_directory",
    "categories": [
      "rail_freight_operator",
      "rail_freight_directory"
    ],
    "root_url": "https://www.dbcargo.com/",
    "notes": "Major rail freight company/operator, not a multi-company directory.",
    "seed_urls": [
      "https://www.dbcargo.com/"
    ]
  },
  {
    "code": "die_gueterbahnen",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_discovery_surface",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "rail_freight_directory",
      "official_association_directory"
    ],
    "root_url": "https://die-gueterbahnen.com/",
    "notes": "Rail freight association/network candidate. Member/list surface must be validated.",
    "seed_urls": [
      "https://die-gueterbahnen.com/"
    ]
  },
  {
    "code": "vdv_de",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_context_discovery_surface",
    "directory_confidence": "low",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "rail_freight_directory",
      "official_association_directory",
      "public_transport_logistics_reference"
    ],
    "root_url": "https://www.vdv.de/",
    "notes": "German transport association. Use only if a freight/logistics member surface is found; otherwise downgrade to hold.",
    "seed_urls": [
      "https://www.vdv.de/"
    ]
  },
  {
    "code": "bsk_kran_schwertransport",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_discovery_surface",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "project_cargo_directory",
      "heavy_lift_directory",
      "official_association_directory"
    ],
    "root_url": "https://www.bsk-ffm.de/",
    "notes": "Heavy transport/crane association candidate. Member directory surface requires review.",
    "seed_urls": [
      "https://www.bsk-ffm.de/"
    ]
  },
  {
    "code": "transport_logistic_exhibitor_directory",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "trade_fair_discovery_surface",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_discovery_seed",
    "categories": [
      "trade_fair_exhibitor_directory",
      "commercial_logistics_directory"
    ],
    "root_url": "https://transportlogistic.de/",
    "notes": "German logistics trade fair source. Exact exhibitor directory URL must be verified before catalog activation.",
    "seed_urls": [
      "https://transportlogistic.de/"
    ]
  },
  {
    "code": "wlw_de",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "b2b_supplier_directory",
      "road_freight_directory"
    ],
    "root_url": "https://www.wlw.de/",
    "notes": "Commercial B2B discovery source. Combines logistics and spedition search surfaces under one source family to avoid duplicate host/source-family identity.",
    "seed_urls": [
      "https://www.wlw.de/de/suche/logistik/deutschland",
      "https://www.wlw.de/de/suche/speditionen/deutschland"
    ]
  },
  {
    "code": "kompass_de_transport_logistics",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "b2b_supplier_directory"
    ],
    "root_url": "https://www.kompass.com/",
    "notes": "Commercial directory already used in English seed family. Later decide whether German catalog owns local surface or references shared commercial source.",
    "seed_urls": [
      "https://www.kompass.com/z/de/a/transportation-and-logistics-services/75/"
    ]
  },
  {
    "code": "freightnet_de",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "freight_forwarder_directory",
      "air_cargo_directory"
    ],
    "root_url": "https://www.freightnet.com/",
    "notes": "Commercial freight directory Germany pages. Useful discovery, not authority; apply low budget and diversity penalty.",
    "seed_urls": [
      "https://www.freightnet.com/directory/p1/cDE/s30.htm",
      "https://www.freightnet.com/directory/p1/cDE/s4.htm"
    ]
  },
  {
    "code": "cargoyellowpages_de",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "air_cargo_directory"
    ],
    "root_url": "https://www.cargoyellowpages.com/",
    "notes": "Commercial cargo directory. Germany root is better than only Frankfurt airport page because it exposes city/airport route fan-out.",
    "seed_urls": [
      "https://mobile.cargoyellowpages.com/germany/",
      "https://mobile.cargoyellowpages.com/germany/frankfurt-am-main-airport.html"
    ]
  },
  {
    "code": "gelbe_seiten_spedition",
    "quality": "B_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_discovery_surface",
    "directory_confidence": "low",
    "catalog_activation_class": "accepted_disabled_low_priority_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "road_freight_directory"
    ],
    "root_url": "https://www.gelbeseiten.de/",
    "notes": "Commercial local directory. Root is broad; exact query URL must be found before strong activation.",
    "seed_urls": [
      "https://www.gelbeseiten.de/"
    ]
  },
  {
    "code": "europages_de_transport_logistik",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_discovery_surface",
    "directory_confidence": "low",
    "catalog_activation_class": "accepted_disabled_low_priority_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "b2b_supplier_directory"
    ],
    "root_url": "https://www.europages.de/",
    "notes": "Commercial B2B discovery. Root is broad; exact category/query URL must be verified.",
    "seed_urls": [
      "https://www.europages.de/"
    ]
  },
  {
    "code": "biek_kep_reference",
    "quality": "A_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_role": "association_context_source",
    "directory_confidence": "low",
    "catalog_activation_class": "hold_not_active_startpoint",
    "categories": [
      "courier_express_parcel_directory",
      "official_association_directory"
    ],
    "root_url": "https://www.biek.de/",
    "notes": "Parcel/express association reference. Use only if a member/company list surface exists.",
    "seed_urls": [
      "https://www.biek.de/"
    ]
  },
  {
    "code": "kombiverkehr",
    "quality": "A_MINUS",
    "decision_status": "HOLD_ENTITY_SOURCE",
    "source_role": "company_entity_seed",
    "directory_confidence": "none",
    "catalog_activation_class": "hold_entity_not_directory",
    "categories": [
      "rail_freight_operator",
      "intermodal_logistics",
      "logistics_operator"
    ],
    "root_url": "https://www.kombiverkehr.de/",
    "notes": "Intermodal operator/entity. Useful seed later, but not a directory source.",
    "seed_urls": [
      "https://www.kombiverkehr.de/"
    ]
  },
  {
    "code": "hamburg_de_logistik_branchenbuch",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "medium",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "city_business_directory"
    ],
    "root_url": "https://www.hamburg.de/",
    "notes": "City/business directory discovery. Keep separate from Hafen Hamburg authority directory.",
    "seed_urls": [
      "https://www.hamburg.de/branchenbuch/hamburg/hafencity/10239793/n0/"
    ]
  },
  {
    "code": "deutsche_verkehrszeitung_directory_reference",
    "quality": "B_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_role": "sector_reference_source",
    "directory_confidence": "none",
    "catalog_activation_class": "hold_not_active_startpoint",
    "categories": [
      "sector_reference",
      "logistics_news_reference"
    ],
    "root_url": "https://www.dvz.de/",
    "notes": "Sector reference/news, not direct source manifest candidate.",
    "seed_urls": [
      "https://www.dvz.de/"
    ]
  },
  {
    "code": "railmarket_de_logistics_companies",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_rail_logistics_directory_candidate",
    "directory_confidence": "high",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "rail_freight_directory",
      "commercial_logistics_directory",
      "b2b_supplier_directory"
    ],
    "root_url": "https://de.railmarket.com/",
    "notes": "German RailMarket logistics-company listing. Direct company rows exist; rail/logistics scope is valuable but commercial and rail-biased.",
    "seed_urls": [
      "https://de.railmarket.com/eu/germany/logistics-companies"
    ]
  },
  {
    "code": "bvl_firmenmitglieder",
    "quality": "A",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "association_member_directory_candidate",
    "directory_confidence": "high",
    "catalog_activation_class": "accepted_disabled_directory_seed",
    "categories": [
      "official_association_directory",
      "logistics_network_directory",
      "company_member_directory"
    ],
    "root_url": "https://www.bvl.de/firmenmitglieder",
    "notes": "BVL company-member profile directory. Strong association/member source; includes companies, universities, and research institutions, so extraction must classify entity type carefully.",
    "seed_urls": [
      "https://www.bvl.de/firmenmitglieder"
    ]
  },
  {
    "code": "firmendatenbanken_logistik_unternehmen",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "high",
    "catalog_activation_class": "accepted_disabled_commercial_discovery_seed",
    "categories": [
      "commercial_logistics_directory",
      "company_directory",
      "b2b_supplier_directory"
    ],
    "root_url": "https://www.firmendatenbanken.de/",
    "notes": "Direct logistics-company list with firm detail links and pagination. Some data freshness indicators are older than one year, so keep B quality and review before activation.",
    "seed_urls": [
      "https://www.firmendatenbanken.de/firmen/liste/logistik-unternehmen/1.html"
    ]
  },
  {
    "code": "wikipedia_de_logistikunternehmen_category",
    "quality": "B_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_role": "encyclopedic_entity_reference",
    "directory_confidence": "low",
    "catalog_activation_class": "hold_not_active_startpoint",
    "categories": [
      "sector_reference",
      "company_entity_reference"
    ],
    "root_url": "https://de.wikipedia.org/",
    "notes": "Wikipedia category has structured subcategories and entity links but is not a primary logistics directory source. Keep as context/reference only.",
    "seed_urls": [
      "https://de.wikipedia.org/wiki/Kategorie:Logistikunternehmen_(Deutschland)"
    ]
  },
  {
    "code": "wer_zu_wem_logistik",
    "quality": "B",
    "decision_status": "HOLD_ACCESS_REVIEW",
    "source_role": "commercial_directory_candidate",
    "directory_confidence": "unknown",
    "catalog_activation_class": "hold_access_review_required",
    "categories": [
      "commercial_logistics_directory",
      "company_directory"
    ],
    "root_url": "https://www.wer-zu-wem.de/",
    "notes": "User-provided direct logistics-service provider list. Keep out of active manifest until pi51c/live check confirms availability.",
    "seed_urls": [
      "https://www.wer-zu-wem.de/dienstleister/logistik.html"
    ]
  }
]
```
