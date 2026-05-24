# Global directories runtime schema and four-layer seal / Küresel dizin runtime schema ve dört katman mührü

## 1. Purpose / Amaç

EN: This document records the final LogisticSearch global directories source-seed work after runtime-schema alignment and four-layer synchronization. It is the continuation of `TOPIC_CRAWLER_CORE_GLOBAL_DIRECTORIES_SOURCE_SEED_URLS_DECISION_2026_05_22.md`.

TR: Bu belge, runtime schema hizalaması ve dört katman senkronizasyonu sonrası LogisticSearch global directories source-seed çalışmasının final doğrusunu kaydeder. `TOPIC_CRAWLER_CORE_GLOBAL_DIRECTORIES_SOURCE_SEED_URLS_DECISION_2026_05_22.md` belgesinin devamıdır.

## 2. Final sealed repository identity / Final mühürlü repository kimliği

| Field | Value |
|---|---|
| Final gate | `GLOBAL_DIR_R2A71_FOUR_LAYER_SEAL_READONLY` |
| Sealed time | `2026-05-23 23:42 Europe/Berlin` |
| Branch | `main` |
| HEAD | `934a9b4628127e96c61324cd236ee3e33708d84d` |
| Parent | `d2db6db2a16e7a46159b285ae1ee4f5be4df534a` |
| Tree | `8036d27d8bb4bf21aa643fc08ae507087b0804ca` |
| Commit subject | `fix(source-seed): align global directories runtime schema` |
| Tracked file count | `207` |

## 3. Final sealed catalog identity / Final mühürlü katalog kimliği

| Field | Value |
|---|---|
| Catalog path | `makpi51crawler/catalog/startpoints/global/global_directories_source_families_v2.json` |
| Language code | `global` |
| Catalog scope | `global_directories` |
| Catalog status | `candidate_only_not_live` |
| Seed contract basis | `source_family_seed_surface_seed_url_v2` |
| Current SHA256 | `d58b7e2cbdbeee71e170c2636c199421c60951b5570b32f1f4329c407bfe0363` |
| Current line count | `122178` |
| Current byte count | `5272821` |
| First canonical JSON SHA256 | `2b158159e0746e014a8176f31c8fb910d868fee219e542ec764a1bc1c24b55c1` |
| First canonical JSON line count | `93639` |
| First canonical JSON byte count | `3993229` |

EN: The first canonical JSON identity and the final runtime-schema identity are intentionally both recorded. The first identity proves the original deduplicated 696-source decision. The final identity is the current operational truth after adding runtime-required schema fields.

TR: İlk canonical JSON kimliği ve final runtime-schema kimliği bilinçli olarak birlikte kaydedilmiştir. İlk kimlik, 696 kaynaklık özgün deduplication kararını kanıtlar. Final kimlik ise runtime-required schema alanları eklendikten sonraki güncel operasyon doğrusudur.

## 4. Raw reference arithmetic / Ham referans aritmetiği

| Metric | Value |
|---|---:|
| Operator batch arithmetic | `960 + 50 + 50 + 9 + 3 = 1072` |
| Raw rows reviewed | `1072` |
| Canonical source families | `696` |
| Seed surfaces | `696` |
| Seed URLs | `696` |
| Unique normalized hosts | `696` |
| Duplicate root-domain groups | `204` |
| Duplicate raw records inside duplicate groups | `580` |
| Merge-excess raw records | `376` |
| Exact URL exception rows | `1` |
| HOLD_VERIFY rows | `1` |
| HTTP canonical URLs | `6` |
| HTTPS canonical URLs | `690` |

EN: The reduction from 1,072 raw references to 696 canonical sources was caused by deterministic duplicate merging and normalized-host canonicalization. The reduction was not caused by crawler execution, DB insertion, frontier filtering, or public URL probing.

TR: 1.072 ham referanstan 696 canonical kaynağa düşüş deterministik duplicate merge ve normalized-host canonicalization nedeniyle olmuştur. Bu düşüş crawler çalıştırılması, DB insert, frontier filtresi veya public URL probe sonucu değildir.

## 5. Duplicate and canonicalization truth / Duplicate ve canonicalization doğrusu

EN: Repeated raw rows were not silently discarded. They were collapsed into canonical source families by normalized root host while preserving the decision basis as metadata. The exact arithmetic is:

`1072 raw refs - 696 canonical source families = 376 merge-excess raw records`

The duplicate-group arithmetic is:

`580 duplicate-group raw refs - 204 canonical duplicate-group representatives = 376 merge-excess raw records`

TR: Tekrar eden ham kayıtlar sessizce silinmedi. Normalized root host üzerinden canonical source family seviyesine indirildi ve karar gerekçesi metadata olarak korundu. Kesin aritmetik şudur:

`1072 raw refs - 696 canonical source families = 376 merge-excess raw records`

Duplicate-group aritmetiği şudur:

`580 duplicate-group raw refs - 204 canonical duplicate-group representatives = 376 merge-excess raw records`

## 6. Final source-family policy distribution / Final source-family policy dağılımı

| Policy | Count |
|---|---:|
| `KEEP_SINGLETON_CANONICAL` | `490` |
| `KEEP_CANONICAL_MERGE_DUPLICATE_METADATA` | `204` |
| `KEEP_EXACT_URL_EXCEPTION_AS_SEED_SURFACE` | `1` |
| `HOLD_VERIFY_BEFORE_JSON` | `1` |
| Total | `696` |

EN: Kompass and Europages were intentionally kept as root-domain source families. They are broad B2B directories, but strategically important global discovery surfaces. Logistics-specific filtering is deferred to parse_core and taxonomy/language filters.

TR: Kompass ve Europages bilinçli olarak root-domain source family şeklinde tutuldu. Geniş B2B dizinlerdir, fakat stratejik global keşif yüzeyleridir. Lojistik odaklı ilk ayrıştırma parse_core ve taxonomy/language filtrelerine bırakılmıştır.

## 7. Runtime schema alignment / Runtime schema hizalaması

EN: The following runtime-required fields were added or repaired after the first canonical JSON seal:

- Root-level `catalog_status`
- Root-level `catalog_scope`
- Root-level `seed_contract_basis`
- `source_families[*].source_status`
- `source_families[*].source_category`
- `source_families[*].allowed_schemes`
- `source_families[*].default_priority`
- `source_families[*].default_recrawl_interval`
- `source_families[*].default_max_depth`
- Required `family_metadata` keys
- Required `seed_surfaces[*]` compatibility keys
- Required `seed_urls[*]` compatibility keys:
  - `seed_type`
  - `submitted_url`
  - `canonical_url`
  - `is_enabled`
  - `priority`
  - `max_depth`
  - `recrawl_interval`
  - `seed_metadata`

TR: İlk canonical JSON mühründen sonra aşağıdaki runtime-required alanlar eklendi veya onarıldı:

- Root-level `catalog_status`
- Root-level `catalog_scope`
- Root-level `seed_contract_basis`
- `source_families[*].source_status`
- `source_families[*].source_category`
- `source_families[*].allowed_schemes`
- `source_families[*].default_priority`
- `source_families[*].default_recrawl_interval`
- `source_families[*].default_max_depth`
- Zorunlu `family_metadata` anahtarları
- Zorunlu `seed_surfaces[*]` uyumluluk anahtarları
- Zorunlu `seed_urls[*]` uyumluluk anahtarları:
  - `seed_type`
  - `submitted_url`
  - `canonical_url`
  - `is_enabled`
  - `priority`
  - `max_depth`
  - `recrawl_interval`
  - `seed_metadata`

## 8. Final runtime distribution / Final runtime dağılımı

| Runtime field | Distribution |
|---|---|
| `source_status` | `candidate_only_not_live=696` |
| `allowed_schemes` | `https=690`, `http=6` |
| `seed_type` | `root_domain=695`, `exact_url=1` |
| `is_enabled` | `false=696` |
| `priority` | `70=695`, `20=1` |
| `max_depth` | `2=694`, `1=2` |
| `recrawl_interval` | `P14D=695`, `P30D=1` |
| `seed_metadata` | `dict=696` |

EN: `source_category` is intentionally not forced to the literal value `global_directory`. It is a taxonomy/source category label and category diversity is allowed. The corrected audit expectation is: present for 696 rows, string, non-empty.

TR: `source_category` bilinçli olarak literal `global_directory` değerine zorlanmaz. Bu alan taxonomy/source category etiketidir ve kategori çeşitliliği kabul edilir. Düzeltilmiş audit beklentisi şudur: 696 satırda mevcut, string, boş değil.

## 9. Four-layer synchronization seal / Dört katman senkronizasyon mührü

| Layer | Sealed state |
|---|---|
| Ubuntu Desktop local repo | `HEAD=934a9b4628127e96c61324cd236ee3e33708d84d`, worktree clean |
| GitHub origin/main and remote main | `HEAD=934a9b4628127e96c61324cd236ee3e33708d84d` |
| pi51c repo `/logisticsearch/repo` | `HEAD=934a9b4628127e96c61324cd236ee3e33708d84d`, worktree clean |
| pi51c live runtime `/logisticsearch/makpi51crawler` | global JSON SHA `d58b7e2cbdbeee71e170c2636c199421c60951b5570b32f1f4329c407bfe0363` |

EN: pi51c repo and pi51c live runtime global JSON files were byte-identical at final seal. The live startpoint catalog count was 26, including the global catalog.

TR: Final mühürde pi51c repo ve pi51c live runtime global JSON dosyaları byte seviyesinde eşitti. Live startpoint catalog sayısı global catalog dahil 26 idi.

## 10. Validator and projection return-shape seal / Validator ve projection return-shape mührü

| Surface | Validator state | Return type | Top-level keys | `projected_sources` rows | `projected_seed_urls` rows |
|---|---|---|---|---:|---:|
| Ubuntu Desktop local runtime validator | `OK` | `dict` | `projected_sources`, `projected_seed_urls` | `696` | `696` |
| pi51c repo runtime validator | `OK` | `dict` | `projected_sources`, `projected_seed_urls` | `696` | `696` |
| pi51c live runtime validator | `OK` | `dict` | `projected_sources`, `projected_seed_urls` | `696` | `696` |

EN: The earlier `projected_rows` value `2` wording was not a loss of 694 seed rows. It was Python `len(...)` on a dictionary with two top-level keys. `project_catalog_to_seed_rows()` returns two row groups: `projected_sources` and `projected_seed_urls`. Each group contains 696 rows.

TR: Önceki `projected_rows` değeri `2` ifadesi 694 seed row kaybı değildir. İki top-level key içeren dictionary üzerinde Python `len(...)` sonucudur. `project_catalog_to_seed_rows()` iki row group döndürür: `projected_sources` ve `projected_seed_urls`. Her iki grup da 696 satır içerir.

EN: This confirms that the catalog contains 696 source projections and 696 seed URL projections while still remaining candidate-only, disabled, not live, and not DB/frontier inserted.

TR: Bu sonuç, katalogda 696 source projection ve 696 seed URL projection bulunduğunu; buna rağmen katalog hâlâ candidate-only, disabled, not live ve DB/frontier’e insert edilmemiş durumda kaldığını doğrular.

## 11. Safety and non-touch assertions / Güvenlik ve dokunmama beyanları

EN: The global directories catalog remains candidate-only and not live.

- No DB insert occurred.
- No frontier activation occurred.
- No crawler start occurred.
- No systemd mutation occurred.
- No public source URL probe occurred.
- No source was promoted to a live queue.
- pi51c service remained inactive.
- pi51c service remained disabled.
- crawler process count remained `0`.

TR: Global directories kataloğu candidate-only ve live değildir.

- DB insert yapılmadı.
- Frontier activation yapılmadı.
- Crawler start yapılmadı.
- Systemd mutation yapılmadı.
- Public source URL probe yapılmadı.
- Hiçbir kaynak live queue seviyesine yükseltilmedi.
- pi51c service inactive kaldı.
- pi51c service disabled kaldı.
- crawler process count `0` kaldı.

## 12. Next required work / Sonraki zorunlu iş

EN: Projection return shape is now understood and does not require a runtime patch. Before any DB/frontier activation, the next safe phase is a read-only activation-plan gate that selects a tiny public reachability probe candidate subset. This future probe must still avoid DB insert, frontier activation, crawler service start, systemd mutation, and broad queue activation.

TR: Projection return shape artık anlaşılmıştır ve runtime patch gerektirmez. DB/frontier aktivasyonundan önceki güvenli sonraki faz, çok küçük bir public reachability probe candidate subset seçen read-only activation-plan gate olmalıdır. Bu gelecek probe yine DB insert, frontier activation, crawler service start, systemd mutation ve geniş queue activation yapmamalıdır.
