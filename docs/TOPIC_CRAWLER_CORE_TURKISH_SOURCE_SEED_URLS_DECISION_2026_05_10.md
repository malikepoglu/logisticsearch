# Crawler Core Turkish Source/Seed URL Decision

# Crawler Core Türkçe Source/Seed URL Kararı

## English

### Purpose

This document records the Turkish source/seed URL decision plan for crawler_core. It is a documentation-only decision surface. It does not create catalog JSON files, it does not patch runtime scheduler code, it does not write to PostgreSQL, it does not touch pi51c, and it does not start crawler_core.

### Scope

- Language: `tr` / Turkish.
- Format applies to all 25 languages.
- English/default must be aligned later to the same `source_category`, `seed_surfaces`, and `candidate_seed_urls` array standard.
- This document stores candidate seed URLs as strings only; it does not fetch them.
- Every live use still requires robots review, live probe, manual review, and a later explicit runtime/frontier gate.

### Decision summary

- Total Turkish source families reviewed: `25`.
- ACCEPT / ACCEPT_REVIEW source families: `18`.
- HOLD source families: `7`.
- Candidate seed URLs: `29`.
- Unique candidate seed URLs: `29`.
- `source_category` is always an array.
- `seed_surfaces` is always an array.
- `candidate_seed_urls` is always an array.

### Quality distribution

- `A`: `6`
- `A_MINUS`: `9`
- `A_PLUS`: `3`
- `B`: `2`
- `B_MINUS`: `2`
- `B_PLUS`: `3`

### Decision status distribution

- `ACCEPT`: `12`
- `ACCEPT_REVIEW`: `6`
- `HOLD_ACCESS_REVIEW`: `1`
- `HOLD_AUTHORITY_REFERENCE`: `1`
- `HOLD_CONTEXT_SOURCE`: `3`
- `HOLD_ENTITY_SOURCE`: `2`

### Accepted core source families

| # | source_family_code | quality | decision_status | source_url |
|---:|---|---|---|---|
| 1 | `ticaret_gov_tr_gmbs` | `A_PLUS` | `ACCEPT` | https://uygulama.gtb.gov.tr/GMBS/MusavirBilgileri.aspx |
| 2 | `shgm_hava_kargo_kuruluslari` | `A_PLUS` | `ACCEPT_REVIEW` | https://web.shgm.gov.tr/tr/havacilik-isletmeleri/2060-hava-kargo-kuruluslari |
| 3 | `utikad_org_tr` | `A` | `ACCEPT` | https://www.utikad.org.tr/UTIKAD-Uye-Listesi |
| 4 | `turklim_org_tr` | `A` | `ACCEPT` | https://www.turklim.org/uye-limanlar/ |
| 5 | `und_org_tr` | `A` | `ACCEPT` | https://www.und.org.tr/uyelerimiz |
| 6 | `ito_lojistik_hizmetler` | `A` | `ACCEPT` | https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler |
| 7 | `igmd_org_tr` | `A` | `ACCEPT` | https://www.igmd.org.tr/uye-bul |
| 8 | `izmgmd_org_tr` | `A_MINUS` | `ACCEPT` | https://www.izmgmd.org.tr/?go=uyeler |
| 9 | `denizticaretodasi_org_tr` | `A_MINUS` | `ACCEPT_REVIEW` | https://www.denizticaretodasi.org.tr/tr/uyeler/tumu |
| 10 | `tcdd_lojistik_merkezler` | `A_MINUS` | `ACCEPT_REVIEW` | https://www.tcdd.gov.tr/ |
| 11 | `turkishcargo_authorized_agents` | `A_MINUS` | `ACCEPT` | https://www.turkishcargo.com/en/authorized-agents |
| 12 | `iga_istanbul_airport_cargo` | `A_MINUS` | `ACCEPT_REVIEW` | https://www.igairport.aero/en/aviation/cargo-and-logistics-center/cargo-and-lojistics/ |
| 13 | `karid_org_tr` | `A_MINUS` | `ACCEPT` | https://karid.org.tr/portfolio_category/uye-sirketler/ |
| 14 | `logitrans_istanbul` | `B_PLUS` | `ACCEPT` | https://www.logitrans.istanbul/en-US/exhibitor-database |
| 15 | `lojider_org_tr` | `B_PLUS` | `ACCEPT` | https://www.lojider.org.tr/Uye-Listesi |
| 16 | `find_com_tr_lojistik_tasimacilik` | `B_PLUS` | `ACCEPT_REVIEW` | https://www.find.com.tr/List/lojistik-ve-tasimacilik?Sorting=3 |
| 17 | `nakliyerehberim_com` | `B` | `ACCEPT` | https://www.nakliyerehberim.com/ |
| 18 | `tnd_org_tr_firmalar` | `B` | `ACCEPT_REVIEW` | https://www.tnd.org.tr/firmalar-tumu-1.html |

### Hold source families

| # | source_family_code | quality | decision_status | source_url |
|---:|---|---|---|---|
| 1 | `uab_tehlikeli_madde_yetkili_kuruluslar` | `A_PLUS` | `HOLD_ACCESS_REVIEW` | https://uhdgm.uab.gov.tr/yetkilendirilen-kisi-ve-kuruluslar |
| 2 | `tcddtasimacilik_yuk` | `A` | `HOLD_ENTITY_SOURCE` | https://www.tcddtasimacilik.gov.tr/sayfa/yurtici-yuk-tasimaciligi/ |
| 3 | `dhmi_airport_cargo_reference` | `A_MINUS` | `HOLD_CONTEXT_SOURCE` | https://www.dhmi.gov.tr/ |
| 4 | `ptt_kargo_lojistik` | `A_MINUS` | `HOLD_ENTITY_SOURCE` | https://www.ptt.gov.tr/ |
| 5 | `tobb_tasima_lojistik_dairesi` | `A_MINUS` | `HOLD_AUTHORITY_REFERENCE` | https://tobb.org.tr/TasimaveLojistik/Sayfalar/AnaSayfa.php |
| 6 | `dgd_org_tr` | `B_MINUS` | `HOLD_CONTEXT_SOURCE` | https://www.dgd.org.tr/dgd/hedeflerimiz |
| 7 | `loder_org_tr` | `B_MINUS` | `HOLD_CONTEXT_SOURCE` | https://www.loder.org.tr/ |

### Turkish source/seed URL records

```json
[
  {
    "source_family_code": "ticaret_gov_tr_gmbs",
    "source_url": "https://uygulama.gtb.gov.tr/GMBS/MusavirBilgileri.aspx",
    "quality": "A_PLUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "customs_broker_directory",
      "public_registry_or_chamber"
    ],
    "seed_surfaces": [
      "gmbs_search_form",
      "gmbs_region_filter",
      "gmbs_result_rows",
      "ggm_authority_reference_page"
    ],
    "candidate_seed_urls": [
      "https://uygulama.gtb.gov.tr/GMBS/MusavirBilgileri.aspx",
      "https://ggm.ticaret.gov.tr/uygulamalar/gumruk-musavirleri-iletisim-bilgileri"
    ],
    "notes": "GMBS ana entity extraction source; GGM ayrı source değil, official reference seed surface."
  },
  {
    "source_family_code": "uab_tehlikeli_madde_yetkili_kuruluslar",
    "source_url": "https://uhdgm.uab.gov.tr/yetkilendirilen-kisi-ve-kuruluslar",
    "quality": "A_PLUS",
    "decision_status": "HOLD_ACCESS_REVIEW",
    "source_category": [
      "dangerous_goods_logistics_directory",
      "public_registry_or_chamber"
    ],
    "seed_surfaces": [
      "yetkilendirilen_kisi_ve_kuruluslar",
      "tmgdk_listesi_pdf",
      "src5_egitim_kuruluslari",
      "rid_yetkili_kuruluslar",
      "tmfb_dmr_isletmeleri",
      "acep_konteyner_operatorleri"
    ],
    "candidate_seed_urls": [
      "https://uhdgm.uab.gov.tr/yetkilendirilen-kisi-ve-kuruluslar"
    ],
    "notes": "TR dışı erişim riski bildirildi; pi51c/live probe geçmeden frontier yok."
  },
  {
    "source_family_code": "shgm_hava_kargo_kuruluslari",
    "source_url": "https://web.shgm.gov.tr/tr/havacilik-isletmeleri/2060-hava-kargo-kuruluslari",
    "quality": "A_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "air_cargo_directory",
      "public_registry_or_chamber"
    ],
    "seed_surfaces": [
      "hava_kargo_kuruluslari_page",
      "a_grubu_yetkili_acente_pdf",
      "b_grubu_yetkili_acente_pdf",
      "known_consignor_or_authorized_agent_context"
    ],
    "candidate_seed_urls": [
      "https://web.shgm.gov.tr/tr/havacilik-isletmeleri/2060-hava-kargo-kuruluslari"
    ],
    "notes": "PDF/link extraction gerektirebilir; seed_urls later live/probe ile netleşmeli."
  },
  {
    "source_family_code": "utikad_org_tr",
    "source_url": "https://www.utikad.org.tr/UTIKAD-Uye-Listesi",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_category": [
      "official_association_directory",
      "freight_forwarder_directory"
    ],
    "seed_surfaces": [
      "utikad_member_list",
      "utikad_city_filter",
      "utikad_download_member_list",
      "utikad_member_rows"
    ],
    "candidate_seed_urls": [
      "https://www.utikad.org.tr/UTIKAD-Uye-Listesi"
    ],
    "notes": "TR freight forwarding/logistics official association directory."
  },
  {
    "source_family_code": "turklim_org_tr",
    "source_url": "https://www.turklim.org/uye-limanlar/",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_category": [
      "port_authority_or_port_directory",
      "port_operator_directory"
    ],
    "seed_surfaces": [
      "turklim_member_ports",
      "region_filter",
      "cargo_type_filter",
      "port_operator_cards"
    ],
    "candidate_seed_urls": [
      "https://www.turklim.org/uye-limanlar/"
    ],
    "notes": "TR port/operator member directory."
  },
  {
    "source_family_code": "und_org_tr",
    "source_url": "https://www.und.org.tr/uyelerimiz",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_category": [
      "road_freight_directory",
      "official_association_directory"
    ],
    "seed_surfaces": [
      "und_members_current",
      "und_search_by_company",
      "und_company_detail_pages",
      "road_freight_member_rows"
    ],
    "candidate_seed_urls": [
      "https://www.und.org.tr/uyelerimiz"
    ],
    "notes": "TR road freight member directory."
  },
  {
    "source_family_code": "ito_lojistik_hizmetler",
    "source_url": "https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_category": [
      "public_registry_or_chamber",
      "commercial_logistics_directory"
    ],
    "seed_surfaces": [
      "ito_logistics_services_member_firms",
      "ito_paginated_member_pages",
      "ito_status_fields",
      "ito_nace_fields"
    ],
    "candidate_seed_urls": [
      "https://ito.org.tr/tr/meslek-komiteleri/uye-firmalar/lojistik-hizmetler"
    ],
    "notes": "Chamber-backed logistics member firm pages; pagination likely."
  },
  {
    "source_family_code": "igmd_org_tr",
    "source_url": "https://www.igmd.org.tr/uye-bul",
    "quality": "A",
    "decision_status": "ACCEPT",
    "source_category": [
      "customs_broker_directory",
      "official_association_directory"
    ],
    "seed_surfaces": [
      "igmd_uye_bul",
      "igmd_firma_bul",
      "member_type_filters",
      "customs_broker_firm_pages"
    ],
    "candidate_seed_urls": [
      "https://www.igmd.org.tr/uye-bul",
      "https://www.igmd.org.tr/firma-bul"
    ],
    "notes": "Regional customs broker association with member/company find surfaces."
  },
  {
    "source_family_code": "izmgmd_org_tr",
    "source_url": "https://www.izmgmd.org.tr/?go=uyeler",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "customs_broker_directory",
      "official_association_directory"
    ],
    "seed_surfaces": [
      "izmir_gmd_members",
      "member_role_filter",
      "registered_member_rows",
      "member_detail_surface"
    ],
    "candidate_seed_urls": [
      "https://www.izmgmd.org.tr/?go=uyeler"
    ],
    "notes": "Regional customs broker member directory."
  },
  {
    "source_family_code": "denizticaretodasi_org_tr",
    "source_url": "https://www.denizticaretodasi.org.tr/tr/uyeler/tumu",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "sea_freight_directory",
      "public_registry_or_chamber",
      "maritime_directory"
    ],
    "seed_surfaces": [
      "dto_uyeler_tumu",
      "dto_branch_member_pages",
      "dto_uye_sorgulama",
      "gemi_sorgulama",
      "meslek_gruplari"
    ],
    "candidate_seed_urls": [
      "https://www.denizticaretodasi.org.tr/tr/uyeler/tumu"
    ],
    "notes": "Maritime chamber source; searchable member/ship surfaces need live review."
  },
  {
    "source_family_code": "tcddtasimacilik_yuk",
    "source_url": "https://www.tcddtasimacilik.gov.tr/sayfa/yurtici-yuk-tasimaciligi/",
    "quality": "A",
    "decision_status": "HOLD_ENTITY_SOURCE",
    "source_category": [
      "rail_freight_operator",
      "rail_freight_authority_reference",
      "state_owned_operator"
    ],
    "seed_surfaces": [
      "yurtici_yuk_tasimaciligi",
      "yurtdisi_yuk_tasimaciligi",
      "yuk_iletisim",
      "mtys_customer_demand_system",
      "lojistik_mudurlukleri_pdf",
      "yurtici_yuk_tarife_pdf"
    ],
    "candidate_seed_urls": [
      "https://www.tcddtasimacilik.gov.tr/sayfa/yurtici-yuk-tasimaciligi/"
    ],
    "notes": "Devlet firması/operator; directory değil, entity/operator/reference source."
  },
  {
    "source_family_code": "tcdd_lojistik_merkezler",
    "source_url": "https://www.tcdd.gov.tr/",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "rail_logistics_infrastructure",
      "public_infrastructure_reference"
    ],
    "seed_surfaces": [
      "lojistik_merkezler",
      "rail_logistics_center_context",
      "location_based_logistics_infrastructure"
    ],
    "candidate_seed_urls": [
      "https://www.tcdd.gov.tr/"
    ],
    "notes": "Exact logistics centers URL requires later live/link review; source family retained as infrastructure reference."
  },
  {
    "source_family_code": "turkishcargo_authorized_agents",
    "source_url": "https://www.turkishcargo.com/en/authorized-agents",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "air_cargo_directory",
      "freight_forwarder_directory"
    ],
    "seed_surfaces": [
      "authorized_agents_search",
      "nearest_cargo_agents",
      "freight_forwarder_agent_results",
      "station_qualification_context"
    ],
    "candidate_seed_urls": [
      "https://www.turkishcargo.com/en/authorized-agents"
    ],
    "notes": "Authorized air cargo agent surface; likely dynamic/search form."
  },
  {
    "source_family_code": "iga_istanbul_airport_cargo",
    "source_url": "https://www.igairport.aero/en/aviation/cargo-and-logistics-center/cargo-and-lojistics/",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "airport_cargo_authority_or_directory",
      "air_cargo_directory"
    ],
    "seed_surfaces": [
      "cargo_and_logistics_center",
      "cargo_hub_logistics_center",
      "airport_cargo_context_pages",
      "cargo_city_company_context"
    ],
    "candidate_seed_urls": [
      "https://www.igairport.aero/en/aviation/cargo-and-logistics-center/cargo-and-lojistics/"
    ],
    "notes": "Airport cargo context source; company directory status requires review."
  },
  {
    "source_family_code": "dhmi_airport_cargo_reference",
    "source_url": "https://www.dhmi.gov.tr/",
    "quality": "A_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_category": [
      "airport_cargo_authority_or_directory",
      "public_infrastructure_reference"
    ],
    "seed_surfaces": [
      "airport_cargo_statistics_reference",
      "airport_cargo_authority_context",
      "airport_freight_volume_context"
    ],
    "candidate_seed_urls": [
      "https://www.dhmi.gov.tr/"
    ],
    "notes": "Authority/context source; exact cargo/company discovery surface requires later review."
  },
  {
    "source_family_code": "ptt_kargo_lojistik",
    "source_url": "https://www.ptt.gov.tr/",
    "quality": "A_MINUS",
    "decision_status": "HOLD_ENTITY_SOURCE",
    "source_category": [
      "courier_express_parcel_directory",
      "state_owned_operator",
      "logistics_operator"
    ],
    "seed_surfaces": [
      "ptt_yurtici_kargo_hizmetleri",
      "ptt_yurtdisi_kargo_hizmetleri",
      "ptt_lojistik_hizmetleri",
      "ptt_kargomat",
      "ptt_references_if_available"
    ],
    "candidate_seed_urls": [
      "https://www.ptt.gov.tr/"
    ],
    "notes": "State-owned operator/entity; not a multi-company directory."
  },
  {
    "source_family_code": "tobb_tasima_lojistik_dairesi",
    "source_url": "https://tobb.org.tr/TasimaveLojistik/Sayfalar/AnaSayfa.php",
    "quality": "A_MINUS",
    "decision_status": "HOLD_AUTHORITY_REFERENCE",
    "source_category": [
      "public_registry_or_chamber",
      "logistics_policy_reference"
    ],
    "seed_surfaces": [
      "tobb_tasima_lojistik_home",
      "tobb_transport_logistics_contact",
      "tobb_tir_islemleri_context",
      "policy_reference_pages"
    ],
    "candidate_seed_urls": [
      "https://tobb.org.tr/TasimaveLojistik/Sayfalar/AnaSayfa.php"
    ],
    "notes": "Authority/reference, not direct multi-company directory."
  },
  {
    "source_family_code": "karid_org_tr",
    "source_url": "https://karid.org.tr/portfolio_category/uye-sirketler/",
    "quality": "A_MINUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "courier_express_parcel_directory",
      "official_association_directory"
    ],
    "seed_surfaces": [
      "karid_member_companies",
      "cargo_courier_post_member_cards",
      "member_company_profile_pages"
    ],
    "candidate_seed_urls": [
      "https://karid.org.tr/portfolio_category/uye-sirketler/"
    ],
    "notes": "Courier/cargo/post member company directory."
  },
  {
    "source_family_code": "logitrans_istanbul",
    "source_url": "https://www.logitrans.istanbul/en-US/exhibitor-database",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "trade_fair_exhibitor_directory",
      "commercial_logistics_directory"
    ],
    "seed_surfaces": [
      "exhibitor_database",
      "year_filter_surfaces",
      "product_service_group_filters",
      "exhibitor_company_rows"
    ],
    "candidate_seed_urls": [
      "https://www.logitrans.istanbul/en-US/exhibitor-database"
    ],
    "notes": "Trade fair exhibitor discovery."
  },
  {
    "source_family_code": "lojider_org_tr",
    "source_url": "https://www.lojider.org.tr/Uye-Listesi",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT",
    "source_category": [
      "third_party_logistics_3pl_directory",
      "official_association_directory"
    ],
    "seed_surfaces": [
      "lojider_member_list",
      "member_rows",
      "member_contact_fields",
      "member_website_links"
    ],
    "candidate_seed_urls": [
      "https://www.lojider.org.tr/Uye-Listesi"
    ],
    "notes": "Private/newer logistics association member list."
  },
  {
    "source_family_code": "find_com_tr_lojistik_tasimacilik",
    "source_url": "https://www.find.com.tr/List/lojistik-ve-tasimacilik?Sorting=3",
    "quality": "B_PLUS",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "commercial_logistics_directory",
      "courier_express_parcel_directory",
      "road_freight_directory"
    ],
    "seed_surfaces": [
      "lojistik_ve_tasimacilik_category",
      "company_detail_pages",
      "subcategory_filters",
      "city_filters"
    ],
    "candidate_seed_urls": [
      "https://www.find.com.tr/List/lojistik-ve-tasimacilik?Sorting=3"
    ],
    "notes": "Commercial directory; good discovery but live/noise review required."
  },
  {
    "source_family_code": "nakliyerehberim_com",
    "source_url": "https://www.nakliyerehberim.com/",
    "quality": "B",
    "decision_status": "ACCEPT",
    "source_category": [
      "commercial_logistics_directory",
      "road_freight_directory"
    ],
    "seed_surfaces": [
      "directory_root",
      "ulkelere_gore_lojistikci_uyeler",
      "calistigi_ulkelere_gore_nakliyeciler",
      "harita_detay_country_pages",
      "karayolu_nakliye_country_pages",
      "parsiyel_tasima_country_pages"
    ],
    "candidate_seed_urls": [
      "https://www.nakliyerehberim.com/",
      "https://www.nakliyerehberim.com/lojistik.aspx",
      "https://www.nakliyerehberim.com/calistiklari-ulkelere-gore-nakliyeci-uyelerimiz-liste.aspx?sayfasi=5&ulke=Almanya"
    ],
    "notes": "User-approved B-tier Turkish commercial/road freight discovery source."
  },
  {
    "source_family_code": "tnd_org_tr_firmalar",
    "source_url": "https://www.tnd.org.tr/firmalar-tumu-1.html",
    "quality": "B",
    "decision_status": "ACCEPT_REVIEW",
    "source_category": [
      "road_freight_directory",
      "commercial_logistics_directory"
    ],
    "seed_surfaces": [
      "firmalar_tumu",
      "firma_name_rows",
      "firm_detail_pages_if_available"
    ],
    "candidate_seed_urls": [
      "https://www.tnd.org.tr/firmalar-tumu-1.html"
    ],
    "notes": "Company rows exist; data hygiene/live review required."
  },
  {
    "source_family_code": "dgd_org_tr",
    "source_url": "https://www.dgd.org.tr/dgd/hedeflerimiz",
    "quality": "B_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_category": [
      "cold_chain_directory",
      "food_logistics_reference"
    ],
    "seed_surfaces": [
      "cold_chain_goal_pages",
      "frozen_food_supply_chain_context",
      "cold_chain_sector_reference"
    ],
    "candidate_seed_urls": [
      "https://www.dgd.org.tr/dgd/hedeflerimiz"
    ],
    "notes": "Cold chain context; no strong company directory yet."
  },
  {
    "source_family_code": "loder_org_tr",
    "source_url": "https://www.loder.org.tr/",
    "quality": "B_MINUS",
    "decision_status": "HOLD_CONTEXT_SOURCE",
    "source_category": [
      "logistics_professional_body",
      "cold_chain_reference",
      "sector_reference"
    ],
    "seed_surfaces": [
      "loder_cold_chain_symposium",
      "professional_body_context",
      "sector_event_pages"
    ],
    "candidate_seed_urls": [
      "https://www.loder.org.tr/"
    ],
    "notes": "Professional/academic sector reference; not firm directory."
  }
]
```

### Runtime boundary

This document is not a live manifest and is not a live frontier activation target. Runtime activation requires a later explicit gate. No DB mutation, no crawler start, no systemd mutation, no pi51c sync, and no runtime scheduler patch is performed here.

## Türkçe

### Amaç

Bu doküman crawler_core için Türkçe source/seed URL karar planını kaydeder. Bu yalnızca dokümantasyon yüzeyidir. Catalog JSON dosyası oluşturmaz, runtime scheduler kodu patch etmez, PostgreSQL'e yazmaz, pi51c'ye dokunmaz ve crawler_core başlatmaz.

### Kapsam

- Dil: `tr` / Turkish.
- Format 25 dilin tamamına uygulanacaktır.
- English/default tarafı daha sonra aynı `source_category`, `seed_surfaces` ve `candidate_seed_urls` array standardına hizalanmalıdır.
- Bu doküman candidate seed URL'leri yalnızca string olarak yazar; URL fetch yapmaz.
- Her canlı kullanım hâlâ robots review, live probe, manual review ve daha sonra ayrı açık runtime/frontier gate gerektirir.

### Karar özeti

- İncelenen toplam Türkçe source family: `25`.
- ACCEPT / ACCEPT_REVIEW source family: `18`.
- HOLD source family: `7`.
- Candidate seed URL sayısı: `29`.
- Unique candidate seed URL sayısı: `29`.
- `source_category` her zaman array'dir.
- `seed_surfaces` her zaman array'dir.
- `candidate_seed_urls` her zaman array'dir.

### Canlı kullanım sınırı

Bu doküman canlı manifest değildir ve frontier'e yazılacak canlı aktivasyon hedefi değildir. Runtime aktivasyonu daha sonra ayrı ve açık gate gerektirir. Burada DB mutation yok, crawler start yok, systemd mutation yok, pi51c sync yok ve runtime scheduler patch yoktur.
