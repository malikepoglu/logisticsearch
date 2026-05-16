# TOPIC_CRAWLER_CORE_TURKISH_SOURCE_SEED_BACKFILL_DECISION_2026_05_13

Status: local decision document created by `SOURCE_SEED_R210_TURKISH_LATEST_SCHEMA_BACKFILL_DECISION_DOC_PATCH_LOCAL_ONLY`.

## 1. Scope

This document seals the Turkish (`tr`) source/seed backfill decision before any Turkish catalog rewrite.

The goal is to migrate the current Turkish catalog to the latest `source_families_v2` schema and raise Turkish coverage to roughly French-level quality while preserving the all-25-language rollout standard.

Reference standard document:

- `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Standard doc sha256: `986b76d80694296019f1392811a2fb9e7fb4fa360d36577af69458a2069bcf90`
- Current standard commit: `d63007236de62f45a9314b27b91ad5a7c2ad87fe`
- Current README index commit: `92931635911c49ba687ad18396bfb0fd5143705b`

## 2. Current Turkish baseline

| Metric | Value |
|---|---:|
| current_source_family_count | 18 |
| current_seed_surface_count | 18 |
| current_seed_url_count | 22 |
| current_unique_seed_url_count | 22 |
| current_unique_host_count | 19 |
| current_schema | legacy / not latest |

The current Turkish catalog must not be used as a schema reference. It is a useful seed inventory, but it requires latest-schema normalization.

## 3. Target metrics

| Metric | Target / decision |
|---|---:|
| new_source_candidate_count | 22 |
| new_planned_seed_surface_count | 52 |
| existing_source_enhancement_count | 4 |
| existing_source_enhancement_surface_count | 10 |
| projected_tr_source_family_count | 40 |
| projected_tr_seed_surface_count | 80 |
| projected_tr_raw_seed_url_count | 84 |
| projected_tr_unique_seed_url_count_after_exact_dedupe | 77 |
| required_unique_seed_url_range | 70..95 |
| high_quality_A_MINUS_or_better_count | 17 |
| hold_count | 0 |

The exact unique URL value `77` is accepted because the global rollout standard uses an approximate French-level target, not an exact 80-URL target. The valid Turkish range for this gate is `70..95` unique seed URLs after exact dedupe.

## 4. Safety and activation rules

- `candidate_manifest`: true after catalog rewrite.
- `is_live`: false after catalog rewrite.
- `runtime_activation_policy`: `pi51c_live_probe_required_before_db_or_frontier_insert`.
- `live_frontier_activation`: false.
- `db_insert_allowed`: false.
- `url_fetch_allowed_in_catalog_gate`: false.
- `crawler_start_allowed_in_catalog_gate`: false.
- `pi51c_sync_allowed_in_catalog_gate`: false.
- No DB insert, no live frontier activation, no crawler start.
- Crawler_Core stores discovered page links only as raw link evidence.
- Raw discovered links are not `added_seeds`.
- Parse_Core creates `added_seeds` after pre-ranking.
- Desktop_Import on Ubuntu Desktop performs final review/ranking.

## 5. Existing URL overlap and dedupe policy

The Turkish rewrite must treat known overlaps as fold/dedupe cases, not duplicated seed URLs.

Known overlap URLs:

- https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler
- https://www.denizticaretodasi.org.tr/tr/uyeler/tumu
- https://www.logitrans.istanbul/en-US/exhibitor-database
- https://www.lojider.org.tr/Uye-Listesi
- https://www.turklim.org/uye-limanlar/
- https://www.und.org.tr/uyelerimiz
- https://www.utikad.org.tr/UTIKAD-Uye-Listesi

Policy: `fold_or_exact_dedupe_under_existing_source_not_duplicate_seed_url`.

## 6. New Turkish source-family plan

| # | source_code | quality_tier | decision_status | source_type | planned_seed_surfaces | canonical_url | rationale |
|---:|---|---|---|---|---:|---|---|
| 1 | `tr_uab_tio_official_registers` | `A_PLUS` | `ACCEPT_REVIEW` | `official_transport_organizer_authority_and_lists` | 4 | https://uhdgm.uab.gov.tr/tasima-isleri-organizatorlugu-tio | Official UAB TİO authority/list surfaces; PDF/list/e-Devlet surfaces require controlled parser and manual review. |
| 2 | `tr_uab_yetki_belgesi_hizmetleri` | `A_PLUS` | `ACCEPT_REVIEW` | `official_transport_authorization_services` | 1 | https://uhdgm.uab.gov.tr/yetki-belgeleri-hizmetleri | Official UAB authorization-service hub. Duplicate firm-list/e-Devlet URLs are folded under tr_uab_tio_official_registers. |
| 3 | `tr_ticaret_ambar_kodlari` | `A_PLUS` | `ACCEPT_REVIEW` | `official_customs_warehouse_code_listing` | 1 | https://ticaret.gov.tr/gumruk-islemleri/dijital-gumruk-uygulamalari/edi-xml-referans-mesajlari/ambar-kodlari | Official customs warehouse/ambar code list; entity candidates are facility/operator records, not direct ranked companies. |
| 4 | `tr_ticaret_antrepo_kodlari` | `A_PLUS` | `ACCEPT_REVIEW` | `official_customs_bonded_warehouse_code_listing` | 1 | https://ticaret.gov.tr/gumruk-islemleri/dijital-gumruk-uygulamalari/edi-xml-referans-mesajlari/antrepo-kodlari | Official customs bonded warehouse/antrepo code list; parse as regulated facility candidates. |
| 5 | `tr_ticaret_ygm_rehberi_pdf` | `A` | `ACCEPT_REVIEW` | `official_customs_broker_reference_pdf` | 1 | https://ticaret.gov.tr/gumruk-islemleri/bilgi-bankasi | Official customs information-bank surface for YGM guide/download discovery; PDF/download handling required. |
| 6 | `tr_lojider_member_directory` | `A` | `ACCEPT_REVIEW` | `national_logistics_service_provider_member_directory` | 2 | https://www.lojider.org.tr/Uye-Listesi | LojiDer member list contains logistics/gümrük/forwarding companies with contact fields; useful association-style directory. |
| 7 | `tr_fiata_turkey_directory` | `A` | `ACCEPT_REVIEW` | `global_association_country_directory` | 1 | https://fiata.org/directory/tr/ | FIATA Turkey country page confirms UTIKAD country association surface; use as authority cross-check, not direct mass import. |
| 8 | `tr_bugumder_customs_broker_firms` | `A` | `ACCEPT_REVIEW` | `regional_customs_broker_firm_directory` | 2 | https://www.bugumder.org/uyelerimiz/firmalarimiz | Bursa customs brokers association firm directory; regional customs broker coverage. |
| 9 | `tr_mergumder_members_pdf` | `A_MINUS` | `ACCEPT_REVIEW` | `regional_customs_broker_members_pdf` | 1 | https://mergumder.org.tr/_yuklenenDosyalar/_dernekDuyurulari/uye_Listesi_16042025.pdf | Mersin customs brokers member PDF; important port-region customs surface, requires PDF handling gate. |
| 10 | `tr_ito_kargo_posta_depolama` | `A` | `ACCEPT_REVIEW` | `chamber_member_category_directory` | 4 | https://www.ito.org.tr/tr/meslek-komiteleri/uye-firmalar/kargo-posta-ve-depolama?page=0 | İTO logistics and storage/cargo chamber categories; high-volume but requires active/inactive status filtering. |
| 11 | `tr_izto_logistics_customs_group` | `A` | `ACCEPT_REVIEW` | `chamber_logistics_customs_group_directory` | 3 | https://izto.org.tr/tr/e-oda/meslek-komitesi-calismasi/lojistik-ve-gumruk-musavirligi-grubu | İZTO logistics/customs group and member-search surfaces; İzmir region coverage with category filtering. |
| 12 | `tr_koto_exporter_maritime_logistics` | `A_MINUS` | `ACCEPT_REVIEW` | `chamber_exporter_maritime_logistics_directory` | 1 | https://koto.org.tr/ihracatci-firmalar | Kocaeli chamber exporter/maritime transport category surface; regional port/logistics enrichment. |
| 13 | `tr_btso_registered_members_logistics` | `A_MINUS` | `ACCEPT_REVIEW` | `chamber_registered_member_query_reference` | 2 | https://www.btso.org.tr/?page=projects%2Flojistik.asp | BTSO registered-member/query and logistics project surfaces; useful Bursa industrial logistics reference with controlled filtering. |
| 14 | `tr_logitrans_exhibitor_database` | `A_MINUS` | `ACCEPT_REVIEW` | `logistics_trade_fair_exhibitor_directory` | 4 | https://www.logitrans.istanbul/tr-TR/katilimci-listesi | logitrans exhibitor database/list; strong sector surface but event freshness and exhibitor-category filtering required. |
| 15 | `tr_logitrans_air_cargo_turkey` | `A_MINUS` | `ACCEPT_REVIEW` | `air_cargo_trade_fair_special_area` | 1 | https://www.logitrans.istanbul/en-US/content/exhibition-directory/specials-areas/air-cargo-turkey/337 | Air Cargo Turkey special-area surface for air-cargo ecosystem discovery; not direct company import. |
| 16 | `tr_logitrans_rail_cargo_turkey` | `A_MINUS` | `ACCEPT_REVIEW` | `rail_cargo_trade_fair_special_area` | 1 | https://logitrans.istanbul/en-US/content/exhibition-directory/specials-areas/rail-cargo-turkey/338 | Rail Cargo Turkey special-area surface; railway/logistics-provider enrichment only after review. |
| 17 | `tr_kompass_turkey_transport_logistics` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_b2b_logistics_directory` | 4 | https://www.kompass.com/z/tr/a/transportation-and-logistics-services/75/ | Commercial B2B fallback for Turkey transportation/logistics; lower priority than official/association sources. |
| 18 | `tr_freightnet_turkey_forwarders` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_freight_forwarder_country_directory` | 5 | https://www.freightnet.com/directory/p1/cTR/s30.htm | Freightnet Turkey freight forwarder pages; commercial fallback with pagination and duplicate controls. |
| 19 | `tr_freightnet_turkey_logistics_companies` | `B` | `ACCEPT_REVIEW` | `commercial_logistics_country_directory` | 5 | https://www.freightnet.com/directory/p58/cTR/s99.htm | Freightnet logistics companies Turkey fallback; use only after stronger sources and with strict dedupe. |
| 20 | `tr_azfreight_turkey_airfreight_directory` | `B_PLUS` | `ACCEPT_REVIEW` | `commercial_airfreight_country_directory` | 4 | https://azfreight.com/country/turkey/ | AZFreight Turkey airfreight/freight directory fallback; useful for air-cargo categories after official SHGM surfaces. |
| 21 | `tr_tobb_logistics_chamber_reference` | `B_PLUS` | `ACCEPT_REVIEW` | `chamber_network_reference` | 2 | https://www.tobb.org.tr/ | TOBB chamber network reference; not direct company directory, but useful for later chamber-source discovery. |
| 22 | `tr_dto_members_all_maritime_directory` | `A_MINUS` | `ACCEPT_REVIEW` | `maritime_chamber_member_directory` | 2 | https://www.denizticaretodasi.org.tr/tr/uyeler/tumu | DTO all-members and logistics group 32 surfaces; maritime/logistics filtering required. |

### 6.1 New source seed URLs

#### 1. `tr_uab_tio_official_registers`

- https://uhdgm.uab.gov.tr/tasima-isleri-organizatorlugu-tio
- https://uhdgm.uab.gov.tr/uploads/pages/tio/tio-yetki-belgesi.pdf
- https://uhdgm.uab.gov.tr/yetki-belgeli-firma-listesi
- https://www.turkiye.gov.tr/ulastirma-ve-altyapi-bakanligi

#### 2. `tr_uab_yetki_belgesi_hizmetleri`

- https://uhdgm.uab.gov.tr/yetki-belgeleri-hizmetleri
- Folded duplicate reference, not counted as seed URL: `https://uhdgm.uab.gov.tr/yetki-belgeli-firma-listesi`
- Folded duplicate reference, not counted as seed URL: `https://www.turkiye.gov.tr/ulastirma-ve-altyapi-bakanligi`

#### 3. `tr_ticaret_ambar_kodlari`

- https://ticaret.gov.tr/gumruk-islemleri/dijital-gumruk-uygulamalari/edi-xml-referans-mesajlari/ambar-kodlari

#### 4. `tr_ticaret_antrepo_kodlari`

- https://ticaret.gov.tr/gumruk-islemleri/dijital-gumruk-uygulamalari/edi-xml-referans-mesajlari/antrepo-kodlari

#### 5. `tr_ticaret_ygm_rehberi_pdf`

- https://ticaret.gov.tr/gumruk-islemleri/bilgi-bankasi

#### 6. `tr_lojider_member_directory`

- https://www.lojider.org.tr/Uye-Listesi
- https://www.lojider.org.tr/

#### 7. `tr_fiata_turkey_directory`

- https://fiata.org/directory/tr/

#### 8. `tr_bugumder_customs_broker_firms`

- https://www.bugumder.org/uyelerimiz/firmalarimiz
- https://www.bugumder.org/

#### 9. `tr_mergumder_members_pdf`

- https://mergumder.org.tr/_yuklenenDosyalar/_dernekDuyurulari/uye_Listesi_16042025.pdf

#### 10. `tr_ito_kargo_posta_depolama`

- https://www.ito.org.tr/tr/meslek-komiteleri/uye-firmalar/kargo-posta-ve-depolama?page=0
- https://www.ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler?page=0
- https://www.ito.org.tr/tr/meslek-komiteleri/nace-kodu/lojistik-hizmetler
- https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler

#### 11. `tr_izto_logistics_customs_group`

- https://izto.org.tr/tr/e-oda/meslek-komitesi-calismasi/lojistik-ve-gumruk-musavirligi-grubu
- https://www.izto.org.tr/tr/tg/lojistik
- https://eoda.izto.org.tr/web/uye_firmalar_yeni.aspx?id=286

#### 12. `tr_koto_exporter_maritime_logistics`

- https://koto.org.tr/ihracatci-firmalar

#### 13. `tr_btso_registered_members_logistics`

- https://www.btso.org.tr/?page=projects%2Flojistik.asp
- https://www.btso.org.tr/?page=databank%2Fsectoralreport.asp

#### 14. `tr_logitrans_exhibitor_database`

- https://www.logitrans.istanbul/tr-TR/katilimci-listesi
- https://www.logitrans.istanbul/en-US/exhibitor-database
- https://logitrans.istanbul/
- https://www.logitrans.istanbul/tr-TR/icerik/fuar-bilgileri/bilgi/fuar-verileri/239

#### 15. `tr_logitrans_air_cargo_turkey`

- https://www.logitrans.istanbul/en-US/content/exhibition-directory/specials-areas/air-cargo-turkey/337

#### 16. `tr_logitrans_rail_cargo_turkey`

- https://logitrans.istanbul/en-US/content/exhibition-directory/specials-areas/rail-cargo-turkey/338

#### 17. `tr_kompass_turkey_transport_logistics`

- https://www.kompass.com/z/tr/a/transportation-and-logistics-services/75/
- https://lu.kompass.com/z/tr/s/transports-et-logistique/10/
- https://lu.kompass.com/z/tr/a/logistics-services/80690/
- https://www.kompass.com/

#### 18. `tr_freightnet_turkey_forwarders`

- https://www.freightnet.com/directory/p1/cTR/s30.htm
- https://www.freightnet.com/directory/p1/cTR/s31.htm
- https://www.freightnet.com/directory/p2/cTR/s30.htm
- https://www.freightnet.com/directory/p3/cTR/s30.htm
- https://www.freightnet.com/directory/p4/cTR/s30.htm

#### 19. `tr_freightnet_turkey_logistics_companies`

- https://www.freightnet.com/directory/p58/cTR/s99.htm
- https://www.freightnet.com/directory/p59/cTR/s99.htm
- https://www.freightnet.com/directory/p60/cTR/s99.htm
- https://www.freightnet.com/directory/p61/cTR/s99.htm
- https://www.freightnet.com/directory/p62/cTR/s99.htm

#### 20. `tr_azfreight_turkey_airfreight_directory`

- https://azfreight.com/country/turkey/
- https://azfreight.com/country-facility/freight-forwarders-in-turkey/
- https://azfreight.com/directory/
- https://azfreight.com/

#### 21. `tr_tobb_logistics_chamber_reference`

- https://www.tobb.org.tr/
- https://www.tobb.org.tr/Sayfalar/Eng/AnaSayfa.php

#### 22. `tr_dto_members_all_maritime_directory`

- https://www.denizticaretodasi.org.tr/tr/uyeler/tumu
- https://www.denizticaretodasi.org.tr/tr/meslek-grubu/grup/32

## 7. Existing Turkish source enhancement plan

| # | existing_code_hint | planned_extra_seed_surfaces | rationale |
|---:|---|---:|---|
| 1 | `utikad_org_tr` | 4 | Enhance existing UTIKAD source with city/member-list seed surfaces. |
| 2 | `und_org_tr` | 2 | Enhance UND source with current and legacy member-directory surfaces; parser must dedupe. |
| 3 | `turklim_org_tr` | 1 | Enhance TÜRKLİM source with direct member-port directory. |
| 4 | `shgm_hava_kargo_kuruluslari` | 3 | Enhance SHGM source with official page/PDF surfaces; PDF/list handling required. |

### 7.1 Existing-source extra seed URLs

#### 1. `utikad_org_tr`

- https://www.utikad.org.tr/UTIKAD-Uye-Listesi
- https://www.utikad.org.tr/UTIKAD-Uye-Listesi?Sehir=İSTANBUL
- https://www.utikad.org.tr/UTIKAD-Uye-Listesi?Sehir=İZMİR
- https://www.utikad.org.tr/UTIKAD-Uye-Listesi?Sehir=MERSİN

#### 2. `und_org_tr`

- https://www.und.org.tr/uyelerimiz
- https://eski.und.org.tr/tr/26/uyelerimiz

#### 3. `turklim_org_tr`

- https://www.turklim.org/uye-limanlar/

#### 4. `shgm_hava_kargo_kuruluslari`

- https://web.shgm.gov.tr/tr/havacilik-isletmeleri/83-kargo-acentalari
- https://web.shgm.gov.tr/documents/sivilhavacilik/files/havacilik_isletmeleri/hava_kargo_isletmeleri/B-Grubu-270524.pdf
- https://web.shgm.gov.tr/tr/havacilik-isletmeleri

## 8. Quality distribution

| Quality tier | Count |
|---|---:|
| `A` | 6 |
| `A_MINUS` | 7 |
| `A_PLUS` | 4 |
| `B` | 1 |
| `B_PLUS` | 4 |

| Decision status | Count |
|---|---:|
| `ACCEPT_REVIEW` | 22 |

Quality decision: official, association, chamber, port, air cargo, customs broker, and transport-authority sources are prioritized. Commercial fallback sources are allowed but tier-limited and must not dominate official/association/chamber sources.

## 9. PDF/download handling rule

PDF/download/list surfaces are candidate seed surfaces only. They require parser/download handling gates and manual review. `direct_company_import` remains false.

## 10. Next gates

- `SOURCE_SEED_R211_TURKISH_LATEST_SCHEMA_BACKFILL_DECISION_DOC_AUDIT_READONLY`
- `SOURCE_SEED_R212_TURKISH_LATEST_SCHEMA_BACKFILL_DECISION_DOC_COMMIT_PUSH_GATE`
- `SOURCE_SEED_R213_TURKISH_CATALOG_SCHEMA_BACKFILL_LOCAL_ONLY`
- `SOURCE_SEED_R214_TURKISH_CATALOG_SCHEMA_BACKFILL_AUDIT_READONLY`
- `SOURCE_SEED_R215_TURKISH_CATALOG_SCHEMA_BACKFILL_COMMIT_PUSH_GATE`
- `SOURCE_SEED_R216_TURKISH_README_INDEX_UPDATE_LOCAL_ONLY`
- `SOURCE_SEED_R217_TURKISH_FINAL_SEAL_READONLY`

pi51c sync remains deferred until English, Turkish, German, and Arabic backfill/schema targets pass.
