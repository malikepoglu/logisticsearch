# Docs / Documentation Hub

## What this folder is

This `docs/` directory is the main human-readable documentation hub of the LogisticSearch repository.

Its job is to explain the project in plain language, preserve operational truth, and give a disciplined reading path for both:

- a complete beginner starting from zero
- an advanced maintainer returning later and needing exact project continuity

This folder is not random note storage.

It is intended to function as:

- a recipe
- an operational handbook
- a continuity ledger
- a design-contract surface
- a decision memory layer

In short:

If code and SQL define **what the system does**, the `docs/` folder must explain **what exists, why it exists, what it guarantees, what it does not yet guarantee, and how it should be operated safely**.

---

## Bu klasör nedir

Bu `docs/` dizini, LogisticSearch deposunun ana insan-okunur dokümantasyon merkezidir.

Görevi; projeyi sade dille açıklamak, operasyon doğrusunu korumak ve şu iki kitle için disiplinli bir okuma yolu vermektir:

- sıfırdan başlayan tam bir acemi
- daha sonra geri dönüp proje sürekliliğini tam olarak anlaması gereken ileri seviye bakımcı

Bu klasör rastgele not depolama alanı değildir.

Şunlar gibi çalışması amaçlanır:

- bir reçete
- bir operasyon el kitabı
- bir süreklilik defteri
- bir tasarım-sözleşme yüzeyi
- bir karar hafızası katmanı

Kısacası:

Kod ve SQL sistemin **ne yaptığını** tanımlıyorsa, `docs/` klasörü de **nelerin mevcut olduğunu, neden mevcut olduğunu, neyi garanti ettiğini, henüz neyi garanti etmediğini ve güvenli biçimde nasıl işletilmesi gerektiğini** açıklamalıdır.

---

## Current visible scope in this folder

At the current repository point, this folder contains top-level topic documents rather than subfolders.

That means:

- the required root explanation surface `docs/README.md` now exists
- there is currently no subdirectory README backlog inside `docs/`
- if subdirectories are introduced later, each must receive its own bilingual `README.md`

Current topic surface in this folder:
  * `TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md`
  * `TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`

- `SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `SECTION1_WEBCRAWLER_CONTROLS.md`
- `SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
- `SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
- `SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`
- `TOPIC_PI51_POSTGRESQL_18_MAJOR_UPGRADE_SEAL_2026-04-06.md`
- `TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
- `TOPIC_RUNBOOK_AUTHORING_AND_EXECUTION_DISCIPLINE.md`

---

## Bu klasörde görünen mevcut kapsam

Mevcut repository noktasında bu klasör, alt klasörlerden ziyade kök seviyede topic belgeleri içerir.

Bu şu anlama gelir:

- zorunlu kök açıklama yüzeyi olan `docs/README.md` artık mevcuttur
- şu anda `docs/` içinde alt klasör README borcu yoktur
- ileride alt klasörler eklenirse, her biri kendi çift dilli `README.md` dosyasını almak zorundadır

Bu klasördeki mevcut topic yüzeyi:
  * `TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md`
  * `TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`

- `SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `SECTION1_WEBCRAWLER_CONTROLS.md`
- `SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
- `SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
- `SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`
- `TOPIC_PI51_POSTGRESQL_18_MAJOR_UPGRADE_SEAL_2026-04-06.md`
- `TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
- `TOPIC_RUNBOOK_AUTHORING_AND_EXECUTION_DISCIPLINE.md`

---

## How to read this folder if you are starting from zero

Do **not** open files randomly.

Use this reading order.

### Reading path A — beginner path for crawler lifecycle understanding

1. `SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
   Start here to understand the big picture of URL lifecycle, ownership, retry, revisit, recovery, and current known gaps.

2. `SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
   Read this second to understand what a crawler worker is expected to do in practice.

3. `SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
   Read this third to understand the lease-renewal SQL surface and why it was added.

4. `SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
   Read this fourth to understand the strict worker-side rule around lease renewal.

5. `SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
   Read this fifth to understand deliberate stop behavior, drain mode, bounded shutdown, and recovery expectations.
6. `SECTION1_WEBCRAWLER_CONTROLS.md`
   Read this sixth to understand the full top-level control family and its boundary against shutdown-class commands.

### Reading path B — repo governance / documentation discipline

1. `TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
   Read this to understand how repository artifacts and controlled work surfaces are named and kept disciplined.
2. `TOPIC_RUNBOOK_AUTHORING_AND_EXECUTION_DISCIPLINE.md`
   Read this next to understand how real runbooks must be authored, audited, and kept aligned with the repository explanation surfaces.

### Reading path C — specific historical operational seal

1. `TOPIC_PI51_POSTGRESQL_18_MAJOR_UPGRADE_SEAL_2026-04-06.md`
   Read this only when you specifically need the recorded truth of that PostgreSQL major-upgrade seal point.

### Reading path D — geospatial application surface boundary

1. `SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`
   Read this when you need the current boundary between crawler-side geospatial acquisition/enrichment and later application-side map rendering, live tracking, and operator-facing geospatial screens.

---

## Sıfırdan başlıyorsan bu klasör nasıl okunmalı

Dosyaları rastgele açma.

Şu okuma sırasını kullan.

### Okuma yolu A — crawler yaşam döngüsünü anlamak için başlangıç yolu

1. `SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
   Büyük resmi anlamak için buradan başla: URL yaşam döngüsü, sahiplik, retry, revisit, recovery ve mevcut bilinen boşluklar.

2. `SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
   Crawler worker’ın pratikte ne yapmasının beklendiğini anlamak için bunu ikinci sırada oku.

3. `SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
   Lease-renewal SQL yüzeyini ve neden eklendiğini anlamak için bunu üçüncü sırada oku.

4. `SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
   Lease renewal etrafındaki katı worker-tarafı kuralı anlamak için bunu dördüncü sırada oku.

5. `SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
   Bilinçli durdurma davranışını, drain mode’u, bounded shutdown’ı ve recovery beklentilerini anlamak için bunu beşinci sırada oku.
6. `SECTION1_WEBCRAWLER_CONTROLS.md`
   Tüm üst-seviye kontrol ailesini ve bunun shutdown-sınıfı komutlardan sınırını anlamak için bunu altıncı sırada oku.

### Okuma yolu B — repo yönetişimi / dokümantasyon disiplini

1. `TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
   Repository artefact’larının ve kontrollü çalışma yüzeylerinin nasıl adlandırıldığını ve disiplinli tutulduğunu anlamak için bunu oku.
2. `TOPIC_RUNBOOK_AUTHORING_AND_EXECUTION_DISCIPLINE.md`
   Gerçek runbook’ların nasıl yazılması, audit edilmesi ve repository açıklama yüzeyleriyle hizalı tutulması gerektiğini anlamak için bunu ardından oku.

### Okuma yolu C — belirli tarihsel operasyon mührü

1. `TOPIC_PI51_POSTGRESQL_18_MAJOR_UPGRADE_SEAL_2026-04-06.md`
   Bunu yalnızca o PostgreSQL major-upgrade mühür noktasının kaydedilmiş doğrusuna özel olarak ihtiyaç duyduğunda oku.

### Okuma yolu D — coğrafi uygulama yüzeyi sınırı

1. `SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`
   Bunu, crawler tarafındaki coğrafi veri edinimi/zenginleştirmesi ile daha sonraki uygulama tarafı harita gösterimi, canlı takip ve operatör-yüzlü coğrafi ekranlar arasındaki güncel sınırı anlaman gerektiğinde oku.

---

## What these crawler documents mean, in plain language

### 1. Lifecycle contract

This document explains the end-to-end lifecycle truth of crawler ownership and processing.

It answers questions like:

- how a URL becomes eligible for work
- how it becomes leased
- how it is finalized
- how retry and revisit timing work
- where the system is still intentionally incomplete

### 2. Worker operational contract

This document explains what a worker process is operationally allowed and expected to do.

It is the bridge between SQL truth and real future Python worker behavior.

### 3. Lease-renewal contract

This document explains the lease-renewal SQL surface.

It exists because long-running work can exceed initial lease duration, which creates duplicate-claim risk unless renewal is explicit and strict.

### 4. Worker heartbeat operating rule

This document explains how a worker must behave around the lease-renewal function.

It answers questions like:

- when to renew
- when not to renew
- what lease loss means
- how not to confuse runtime memory with durable truth

### 5. Drain and graceful-shutdown contract

This document explains how intentional stop behavior must work.

It answers questions like:

- when to stop taking new work
- what to do with in-flight work
- whether renewal is still allowed during shutdown
- how bounded shutdown differs from infinite waiting
- how recovery works after incomplete shutdown

---

## Bu crawler belgeleri sade dille ne anlatır

### 1. Yaşam döngüsü sözleşmesi

Bu belge crawler sahipliği ve işleme sürecinin uçtan uca yaşam döngüsü doğrusunu açıklar.

Şu sorulara cevap verir:

- bir URL nasıl iş için uygun hale gelir
- nasıl leased olur
- nasıl finalize edilir
- retry ve revisit zamanlaması nasıl çalışır
- sistemin hangi noktalarının bilinçli olarak henüz tamamlanmadığı

### 2. Worker operasyon sözleşmesi

Bu belge worker sürecinin operasyonel olarak ne yapmaya izinli ve ne yapmasının beklendiğini açıklar.

SQL doğrusuyla gelecekteki gerçek Python worker davranışı arasındaki köprüdür.

### 3. Lease-renewal sözleşmesi

Bu belge lease-renewal SQL yüzeyini açıklar.

Uzun süren işlerin ilk lease süresini aşabilmesi nedeniyle vardır; aksi halde açık ve katı renewal olmadan duplicate-claim riski doğar.

### 4. Worker heartbeat işletim kuralı

Bu belge worker’ın lease-renewal fonksiyonu etrafında nasıl davranması gerektiğini açıklar.

Şu sorulara cevap verir:

- ne zaman renew yapılmalı
- ne zaman yapılmamalı
- lease kaybı ne anlama gelir
- çalışma anı belleği ile kalıcı doğruluğun nasıl karıştırılmaması gerektiği

### 5. Drain ve graceful-shutdown sözleşmesi

Bu belge bilinçli durdurma davranışının nasıl işlemesi gerektiğini açıklar.

Şu sorulara cevap verir:

- ne zaman yeni iş alımı durmalı
- in-flight işlerle ne yapılmalı
- shutdown sırasında renewal hâlâ izinli mi
- bounded shutdown ile sonsuz bekleme arasındaki fark nedir
- eksik kapanış sonrası recovery nasıl çalışır

## Current judgement

At the current repository point, `docs/README.md` is the required root explanation surface.

It must remain present, bilingual, and beginner-first.

It may become longer later; however, it must never become less explanatory or less structured.

## Mevcut hüküm

Mevcut repository noktasında `docs/README.md`, zorunlu kök açıklama yüzeyidir.

Mevcut kalmalı, çift dilli olmalı ve başlangıç dostu olmalıdır.

İleride uzayabilir; ancak asla daha az açıklayıcı veya daha az düzenli hale gelmemelidir.

## Documentation rules for this folder

Every document in `docs/` should follow these rules.

### Rule 1 — bilingual by default

Human explanation layers should be bilingual:

- English
- Turkish

### Rule 2 — file paths, commands, identifiers stay in English

To keep technical consistency, keep these in English:

- file paths
- filenames
- SQL function names
- commands
- code identifiers
- schema names
- database object names

### Rule 3 — contract language must be explicit

Avoid vague text like:

- “it should probably be fine”
- “this is roughly how it works”
- “we can assume this exists”

Prefer explicit statements such as:

- current guarantee
- current non-guarantee
- current gap
- future required work
- prohibited assumption
- required operator behavior

### Rule 4 — beginner-first clarity

A new person should be able to understand:

- what the document is about
- why it exists
- what problem it solves
- what it assumes
- what it forbids
- what to read next

### Rule 5 — no silent reality drift

If implementation reality changes, documentation must be updated quickly.

The docs must not remain frozen in an older truth after SQL, workflow, or operational contracts change.

---

## Bu klasör için dokümantasyon kuralları

`docs/` içindeki her belge şu kurallara uymalıdır.

### Kural 1 — varsayılan olarak çift dilli

İnsan açıklama katmanları çift dilli olmalıdır:

- İngilizce
- Türkçe

### Kural 2 — dosya yolları, komutlar, kimlikler İngilizce kalır

Teknik tutarlılığı korumak için şunlar İngilizce kalmalıdır:

- dosya yolları
- dosya adları
- SQL fonksiyon adları
- komutlar
- kod kimlikleri
- şema adları
- veritabanı nesne adları

### Kural 3 — sözleşme dili açık olmalıdır

Şu tür muğlak ifadelerden kaçın:

- “muhtemelen sorun olmaz”
- “aşağı yukarı böyle çalışır”
- “bunun mevcut olduğunu varsayabiliriz”

Bunun yerine açık ifadeler tercih et:

- mevcut garanti
- mevcut garanti etmeme durumu
- mevcut boşluk
- gerekli gelecek işi
- yasak varsayım
- zorunlu operatör davranışı

### Kural 4 — başlangıç seviyesi dostu açıklık

Yeni gelen biri şunları anlayabilmelidir:

- bu belgenin ne hakkında olduğu
- neden var olduğu
- hangi problemi çözdüğü
- neyi varsaydığı
- neyi yasakladığı
- sırada neyi okuması gerektiği

### Kural 5 — gerçeklik sessizce kaymamalı

Implementasyon gerçeği değişirse dokümantasyon da hızlıca güncellenmelidir.

SQL, iş akışı veya operasyon sözleşmeleri değiştikten sonra dokümanlar eski doğruda donup kalmamalıdır.

---

## README policy for future docs subdirectories

At the moment, `docs/` has no subdirectories.

If subdirectories are added later, every new docs subdirectory must receive its own `README.md`.

That future README must explain:

- the scope of that subdirectory
- why it exists
- how to read it
- file map of that subdirectory
- update rules
- relation to parent `docs/README.md`
- relation to sibling surfaces when relevant

No documentation subdirectory should remain unexplained.

---

## Gelecekteki docs alt klasörleri için README politikası

Şu anda `docs/` içinde alt klasör yoktur.

İleride alt klasör eklenirse, her yeni docs alt klasörü kendi `README.md` dosyasını almak zorundadır.

Bu gelecekteki README şunları açıklamalıdır:

- o alt klasörün kapsamı
- neden var olduğu
- nasıl okunması gerektiği
- o alt klasörün dosya haritası
- güncelleme kuralları
- üst `docs/README.md` ile ilişkisi
- gerekiyorsa kardeş yüzeylerle ilişkisi

Açıklamasız bırakılmış hiçbir dokümantasyon alt klasörü olmamalıdır.

---

## Practical maintenance rule

Whenever you add one of these:

- a new topic contract
- a new runbook
- a new seal record worth keeping in docs
- a new docs subdirectory
- a new major operational truth

you should ask:

1. does `docs/README.md` need an update
2. does the reading order need an update
3. does a cross-reference need to be added
4. does a new subdirectory need its own README

If the answer is yes, update the documentation immediately in the same disciplined step.

---

## Pratik bakım kuralı

Şunlardan biri eklendiğinde:

- yeni bir topic sözleşmesi
- yeni bir runbook
- docs içinde tutulmaya değer yeni bir seal kaydı
- yeni bir docs alt klasörü
- yeni bir büyük operasyon doğrusu

şunu sormalısın:

1. `docs/README.md` güncellenmeli mi
2. okuma sırası güncellenmeli mi
3. yeni bir çapraz referans eklenmeli mi
4. yeni alt klasör kendi README’sini almalı mı

Cevap evetse, dokümantasyonu aynı disiplinli adım içinde hemen güncelle.

---

## Processed-data storage tier surfaces

Read these together when working on removable processed-data storage tiers for the webcrawler line:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`
- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`

## İşlenmiş-veri depolama katmanı yüzeyleri

Webcrawler hattındaki çıkarılabilir işlenmiş-veri depolama katmanları üzerinde çalışırken bunları birlikte oku:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`
- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`

## EN — Reading path D — raw fetch / parse / taxonomy boundary

1. `TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
Read this when you need the strict beginner-first boundary between raw fetch, parse, taxonomy, later selection order, and non-logistics handling.

## TR — Okuma yolu D — raw fetch / parse / taxonomy sınırı

1. `TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
Raw fetch, parse, taxonomy, sonraki selection sırası ve lojistik dışı sayfaların ele alınışı arasındaki katı beginner-first sınırı anlaman gerektiğinde bunu oku.

<!-- BEGIN PI51C_THERMAL_FAN_WIFI_LINKS -->
## EN — Pi51c thermal, fan, and Wi-Fi host-control layer

- [Pi51c thermal, fan, and Wi-Fi control contract](TOPIC_PI51C_THERMAL_FAN_WIFI_CONTROL_CONTRACT.md)
- [Runbook: Pi51c thermal, fan, and Wi-Fi control](RUNBOOK_PI51C_THERMAL_FAN_WIFI_CONTROL.md)

## TR — Pi51c termal, fan ve Wi-Fi host-control katmanı

- [Pi51c termal, fan ve Wi-Fi kontrol sözleşmesi](TOPIC_PI51C_THERMAL_FAN_WIFI_CONTROL_CONTRACT.md)
- [Runbook: Pi51c termal, fan ve Wi-Fi kontrolü](RUNBOOK_PI51C_THERMAL_FAN_WIFI_CONTROL.md)
<!-- END PI51C_THERMAL_FAN_WIFI_LINKS -->

## Taxonomy seals / Taksonomi mühürleri

- [Stage1 English baseline taxonomy review seal](TOPIC_TAXONOMY_STAGE1_ENGLISH_BASELINE_REVIEW_SEAL_2026_04_25.md)
- [Stage2 Turkish leasing taxonomy patch/sync/live-swap seal](TOPIC_TAXONOMY_STAGE2_TURKISH_LEASING_PATCH_SYNC_SEAL_2026_04_25.md)
- [Stage3 German baseline taxonomy review seal](TOPIC_TAXONOMY_STAGE3_GERMAN_BASELINE_REVIEW_SEAL_2026_04_25.md)
- [Stage4 Arabic taxonomy patch/review/sync/live-swap seal](TOPIC_TAXONOMY_STAGE4_ARABIC_PATCH_REVIEW_SYNC_SEAL_2026_04_25.md)
- [Stage5 Bulgarian taxonomy patch/review/sync/live-swap seal](TOPIC_TAXONOMY_STAGE5_BULGARIAN_PATCH_REVIEW_SYNC_SEAL_2026_04_25.md)

<!-- TAXONOMY_JSON_ALL_25_COMPLETION_SEAL_LINK_START -->
- [Taxonomy aircraft description and hi/bn/ur term repair seal - 2026-05-02](TOPIC_TAXONOMY_AIRCRAFT_DESCRIPTION_AND_HI_BN_UR_TERM_REPAIR_SEAL_2026_05_02.md)

## Taxonomy JSON all-25-language completion seal / 25 dil taxonomy JSON tamamlama mührü

- [Taxonomy JSON all-25-language completion seal — 2026-05-01](TOPIC_TAXONOMY_JSON_ALL_25_LANGUAGES_COMPLETION_SEAL_2026_05_01.md)
<!-- TAXONOMY_JSON_ALL_25_COMPLETION_SEAL_LINK_END -->
## 2026-05-02 taxonomy aircraft repair seal / 2026-05-02 taxonomy aircraft repair mührü

- [`docs/TOPIC_TAXONOMY_AIRCRAFT_DESCRIPTION_AND_HI_BN_UR_TERM_REPAIR_SEAL_2026_05_02.md`](TOPIC_TAXONOMY_AIRCRAFT_DESCRIPTION_AND_HI_BN_UR_TERM_REPAIR_SEAL_2026_05_02.md) — [EN] Seal document for the all-25 taxonomy aircraft description repair and the exact Hindi/Bengali/Urdu term repair cycle. It records commit `5ec833d937059a15dafe9f161861f939b2e38737`, 25 loaded language files, 8,375 records, 450 patched-description guards, 54 hi/bn/ur term guards, and confirms that Pi51c, DB, SQL, runtime, systemd, and node expansion were not touched.
- [`docs/TOPIC_TAXONOMY_AIRCRAFT_DESCRIPTION_AND_HI_BN_UR_TERM_REPAIR_SEAL_2026_05_02.md`](TOPIC_TAXONOMY_AIRCRAFT_DESCRIPTION_AND_HI_BN_UR_TERM_REPAIR_SEAL_2026_05_02.md) — [TR] All-25 taxonomy aircraft description repair ve Hindi/Bengali/Urdu exact term repair döngüsünü mühürleyen dokümandır. Commit `5ec833d937059a15dafe9f161861f939b2e38737`, 25 yüklü dil dosyası, 8.375 kayıt, 450 patched-description guard, 54 hi/bn/ur term guard bilgisini kaydeder ve Pi51c, DB, SQL, runtime, systemd ile node expansion yüzeylerine dokunulmadığını doğrular.

<!-- TASK11_RUNTIME_CLEANUP_CRAWLER_CORE_RETURN_LINKS_BEGIN -->
## Task11 runtime cleanup and crawler_core return

- [Task11 runtime cleanup, boot/shutdown decision, and crawler_core return seal](TOPIC_TASK11_RUNTIME_CLEANUP_BOOT_DECISION_AND_CRAWLER_CORE_RETURN_2026_05_04.md)
- [TODO - Crawler core return after Task11](TODO_CRAWLER_CORE_RETURN_AFTER_TASK11_2026_05_04.md)
<!-- TASK11_RUNTIME_CLEANUP_CRAWLER_CORE_RETURN_LINKS_END -->

### Crawler core entrypoint invocation contract — 2026-05-05

- [Crawler Core EntryPoint Invocation Contract — 2026-05-05](TOPIC_CRAWLER_CORE_ENTRYPOINT_INVOCATION_CONTRACT_2026_05_05.md)

### Crawler core systemd service invocation patch seal — 2026-05-05

- [Crawler Core Systemd Service Invocation Patch Seal — 2026-05-05](TOPIC_CRAWLER_CORE_SYSTEMD_SERVICE_INVOCATION_PATCH_SEAL_2026_05_05.md)

### Sync runtime process guard false-positive fix seal — 2026-05-05

- [Sync Runtime Process Guard False-Positive Fix Seal — 2026-05-05](TOPIC_SYNC_RUNTIME_PROCESS_GUARD_FALSE_POSITIVE_FIX_SEAL_2026_05_05.md)

<!-- LS:R112-CONTROLS-RUN-POLICY-LINK:BEGIN -->
### Controls run policy and safety classification

- [Controls Run Policy and Safety Classification — 2026-05-06](TOPIC_CONTROLS_RUN_POLICY_AND_SAFETY_CLASSIFICATION_2026_05_06.md) — canonical R112 controls safety-classification seal for A0/B1/C2/D3/E4/F5 control classes, including the rule that inventory and crawler-core trace work must not execute control scripts.
<!-- LS:R112-CONTROLS-RUN-POLICY-LINK:END -->

## PostgreSQL JSON Runtime Topology / PostgreSQL JSON Runtime Topolojisi

- [PostgreSQL JSON Runtime Topology and Raw Fetch Manifest Standard — 2026-05-07](TOPIC_POSTGRESQL_JSON_RUNTIME_TOPOLOGY_AND_RAW_FETCH_MANIFEST_STANDARD_2026_05_07.md)
  - EN: Defines the lean PostgreSQL runtime authority plus JSON/JSONB controlled representation rule for crawler_core raw fetch manifests.
  - TR: crawler_core ham veri manifestleri için yalın PostgreSQL runtime otoritesi ve JSON/JSONB kontrollü temsil kuralını tanımlar.

## Crawler core / Runtime seals

- [R115 enqueue conflict patch and runtime impact seal](TOPIC_CRAWLER_CORE_R115_ENQUEUE_CONFLICT_PATCH_AND_RUNTIME_IMPACT_SEAL_2026_05_08.md)

## Crawler Core Source/Seed Strategy

- [Crawler Core 25 Language Source/Seed Strategy](TOPIC_CRAWLER_CORE_25_LANGUAGE_SOURCE_SEED_STRATEGY_2026_05_10.md)
<!-- SOURCE_SEED_R5B_README_INDEX_START -->

## Crawler Core 25 Language Source/Seed Strategy

- Canonical strategy doc: `docs/TOPIC_CRAWLER_CORE_25_LANGUAGE_SOURCE_SEED_STRATEGY_2026_05_10.md`
- Scope: all 25 languages under `makpi51crawler/catalog/startpoints/<lang>/`.
- Boundary: Ubuntu Desktop + GitHub only until a later explicit pi51c sync gate; no runtime, DB, crawler, or systemd mutation from this documentation step.

<!-- SOURCE_SEED_R5B_README_INDEX_END -->

<!-- SOURCE_SEED_STARTPOINTS_INDEX_2026_05_12_BEGIN -->

## Crawler Core source-seed / startpoints index

This index anchors the current crawler_core source/seed catalog work so the 25-language rollout does not drift.

### Current sealed startpoint catalogs

| Language | Catalog | Status | Source families | Seed surfaces | Seed URLs |
|---|---|---:|---:|---:|---:|
| English (`en`) | [`english_source_families_v2.json`](../makpi51crawler/catalog/startpoints/en/english_source_families_v2.json) | sealed candidate manifest, not live | 171 | 561 | 561 |
| Turkish (`tr`) | [`turkish_source_families_v2.json`](../makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| German (`de`) | [`german_source_families_v2.json`](../makpi51crawler/catalog/startpoints/de/german_source_families_v2.json) | sealed candidate manifest, not live | 41 | 87 | 87 |
| Arabic (`ar`) | [`arabic_source_families_v2.json`](../makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| Chinese (`zh`) | [`chinese_source_families_v2.json`](../makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json) | sealed candidate manifest, not live | 105 | 148 | 148 |
| French (`fr`) | [`french_source_families_v2.json`](../makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json) | sealed candidate manifest, not live | 37 | 107 | 107 |
| Spanish (`es`) | [`spanish_source_families_v2.json`](../makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json) | sealed candidate manifest, not live | 45 | 98 | 98 |
| Italian (`it`) | [`italian_source_families_v2.json`](../makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| Portuguese (`pt`) | [`portuguese_source_families_v2.json`](../makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| Dutch (`nl`) | [`dutch_source_families_v2.json`](../makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| Russian (`ru`) | [`russian_source_families_v2.json`](../makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json) | sealed candidate manifest, not live | 40 | 84 | 84 |
| Ukrainian (`uk`) | [ukrainian_source_families_v2.json](../makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json) | sealed candidate manifest, not live | 40 | 56 | 56 |
| Bulgarian (`bg`) | [bulgarian_source_families_v2.json](../makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json) | sealed candidate manifest, not live; minimum seed target repaired | 40 | 50 | 50 |
| Czech (`cs`) | [`czech_source_families_v2.json`](../makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Greek (`el`) | [`greek_source_families_v2.json`](../makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Hungarian (`hu`) | [`hungarian_source_families_v2.json`](../makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Romanian (`ro`) | [`romanian_source_families_v2.json`](../makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Japanese (`ja`) | [`japanese_source_families_v2.json`](../makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Korean (`ko`) | [`korean_source_families_v2.json`](../makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Indonesian (`id`) | [`indonesian_source_families_v2.json`](../makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Vietnamese (`vi`) | [`vietnamese_source_families_v2.json`](../makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |
| Hindi (`hi`) | [`hindi_source_families_v2.json`](../makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json) | sealed candidate manifest, not live | 45 | 90 | 90 |

### Source-seed policy and decision records

- [`TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`](TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_SOURCE_FAMILY_DAILY_BUDGET_AND_COUNTRY_SEED_POLICY_2026_05_11.md`](TOPIC_CRAWLER_CORE_SOURCE_FAMILY_DAILY_BUDGET_AND_COUNTRY_SEED_POLICY_2026_05_11.md)
- [`TOPIC_CRAWLER_CORE_ENGLISH_SOURCE_SEED_SUPER_EXPANSION_DECISION_2026_05_13.md`](TOPIC_CRAWLER_CORE_ENGLISH_SOURCE_SEED_SUPER_EXPANSION_DECISION_2026_05_13.md)
- [`TOPIC_CRAWLER_CORE_TURKISH_SOURCE_SEED_BACKFILL_DECISION_2026_05_13.md`](TOPIC_CRAWLER_CORE_TURKISH_SOURCE_SEED_BACKFILL_DECISION_2026_05_13.md)
- [`TOPIC_CRAWLER_CORE_GERMAN_SOURCE_SEED_BACKFILL_DECISION_2026_05_14.md`](TOPIC_CRAWLER_CORE_GERMAN_SOURCE_SEED_BACKFILL_DECISION_2026_05_14.md)
- [`TOPIC_CRAWLER_CORE_ARABIC_SOURCE_SEED_BACKFILL_DECISION_2026_05_14.md`](TOPIC_CRAWLER_CORE_ARABIC_SOURCE_SEED_BACKFILL_DECISION_2026_05_14.md)
- [`TOPIC_CRAWLER_CORE_GERMAN_SOURCE_SEED_URLS_DECISION_2026_05_11.md`](TOPIC_CRAWLER_CORE_GERMAN_SOURCE_SEED_URLS_DECISION_2026_05_11.md)
- [`TOPIC_CRAWLER_CORE_ARABIC_SOURCE_SEED_URLS_DECISION_2026_05_12.md`](TOPIC_CRAWLER_CORE_ARABIC_SOURCE_SEED_URLS_DECISION_2026_05_12.md)
- [`TOPIC_CRAWLER_CORE_CHINESE_SOURCE_SEED_URLS_DECISION_2026_05_12.md`](TOPIC_CRAWLER_CORE_CHINESE_SOURCE_SEED_URLS_DECISION_2026_05_12.md)
- [`TOPIC_CRAWLER_CORE_FRENCH_SOURCE_SEED_URLS_DECISION_2026_05_12.md`](TOPIC_CRAWLER_CORE_FRENCH_SOURCE_SEED_URLS_DECISION_2026_05_12.md)
- [`TOPIC_CRAWLER_CORE_SPANISH_SOURCE_SEED_URLS_DECISION_2026_05_15.md`](TOPIC_CRAWLER_CORE_SPANISH_SOURCE_SEED_URLS_DECISION_2026_05_15.md)
- [`TOPIC_CRAWLER_CORE_ITALIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md`](TOPIC_CRAWLER_CORE_ITALIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_PORTUGUESE_SOURCE_SEED_URLS_DECISION_2026_05_16.md`](TOPIC_CRAWLER_CORE_PORTUGUESE_SOURCE_SEED_URLS_DECISION_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_DUTCH_SOURCE_SEED_URLS_DECISION_2026_05_16.md`](TOPIC_CRAWLER_CORE_DUTCH_SOURCE_SEED_URLS_DECISION_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_RUSSIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md`](TOPIC_CRAWLER_CORE_RUSSIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_UKRAINIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md`](TOPIC_CRAWLER_CORE_UKRAINIAN_SOURCE_SEED_URLS_DECISION_2026_05_16.md)
- [`TOPIC_CRAWLER_CORE_BULGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_17.md`](TOPIC_CRAWLER_CORE_BULGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_17.md)
- [`TOPIC_CRAWLER_CORE_CZECH_SOURCE_SEED_URLS_DECISION_2026_05_19.md`](TOPIC_CRAWLER_CORE_CZECH_SOURCE_SEED_URLS_DECISION_2026_05_19.md)
- [`TOPIC_CRAWLER_CORE_GREEK_SOURCE_SEED_URLS_DECISION_2026_05_19.md`](TOPIC_CRAWLER_CORE_GREEK_SOURCE_SEED_URLS_DECISION_2026_05_19.md)
- [`TOPIC_CRAWLER_CORE_HUNGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_19.md`](TOPIC_CRAWLER_CORE_HUNGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_19.md)

- [`TOPIC_CRAWLER_CORE_ROMANIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_ROMANIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md)
- [`TOPIC_CRAWLER_CORE_JAPANESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_JAPANESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md)
- [`TOPIC_CRAWLER_CORE_KOREAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_KOREAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md)
- [`TOPIC_CRAWLER_CORE_INDONESIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_INDONESIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md)
- [`TOPIC_CRAWLER_CORE_VIETNAMESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_VIETNAMESE_SOURCE_SEED_URLS_DECISION_2026_05_20.md)
- [`TOPIC_CRAWLER_CORE_HINDI_SOURCE_SEED_URLS_DECISION_2026_05_20.md`](TOPIC_CRAWLER_CORE_HINDI_SOURCE_SEED_URLS_DECISION_2026_05_20.md)

### Boundary rule

Crawler_Core stores discovered page links only as raw link evidence.
Raw links are not `added_seeds`. Parse_Core creates `added_seeds` after pre-ranking. Desktop_Import on Ubuntu Desktop converts pre-ranking into real ranking/final rank.

## Source-seed next-language rollout decision / Sıradaki dil rollout karar mühürü
- Gate / Kapı: `R379J_BG_SOURCE_SEED_MINIMUM_EXPANSION_REPAIR_LOCAL_ONLY`
- Current local repair / Mevcut lokal onarım: Bulgarian catalog expanded from `40/40/40/40 unique` to `40/50/50/50 unique` using 10 NSBS member-profile seed surfaces.
- Rolled-out tracked catalogs / Tamamlanmış kataloglar: `en,tr,de,ar,zh,fr,es,it,pt,nl,ru,uk,bg`
- Current priority / Mevcut öncelik: audit this Bulgarian minimum expansion repair, commit/push the three-file repair, post-push seal GitHub, rerun metric target audit, and only then redo the pi51c sync decision.
## Source-seed canonical startpoint schema standard

This standard is authoritative for all 25 language startpoint catalogs.

Standard ID: `SOURCE_SEED_CANONICAL_STARTPOINT_SCHEMA_STANDARD`

Applies to all startpoint catalog JSON files under:

`makpi51crawler/catalog/startpoints/<lang>/<language>_source_families_v2.json`

Required top-level catalog fields:

- `schema`: must be `source_families_v2`
- `schema_version`: must be `source_families_v2`
- `catalog_version`: must match the language catalog name
- `language_code`: must be one of the 25 canonical language codes
- `candidate_manifest`: must be `true` until live activation is explicitly approved
- `is_live`: must be `false` until pi51c live probe and explicit activation gate pass
- `runtime_activation_policy`: must be `pi51c_live_probe_required_before_db_or_frontier_insert`
- `source_families`: must be a non-empty list for rolled languages

Required source-family object fields:

- `source_family_code`: stable internal code, not a URL
- `source_family_name`: human-readable source family name
- `source_host`: hostname only
- `source_root_url`: HTTPS root URL for the family
- `quality_tier`: required; allowed values are `A+`, `A`, `A-`, `B+`, `B`, `B-`
- `decision`: required; allowed values are `ACCEPT`, `ACCEPT_REVIEW`, `HOLD`, `REJECT`
- `seed_surfaces`: required list; every accepted/review family must have at least one seed surface

Required seed-surface object fields:

- `seed_surface_code`: stable internal seed surface code
- `seed_surface_name`: human-readable seed surface name
- `surface_type`: controlled descriptive surface type
- `quality_tier`: required; allowed values are `A+`, `A`, `A-`, `B+`, `B`, `B-`
- `decision`: required; allowed values are `ACCEPT`, `ACCEPT_REVIEW`, `HOLD`, `REJECT`
- `seed_urls`: required list of URL objects

Required seed URL object fields:

- `url`: HTTPS seed URL
- legacy scalar `seed_url` is forbidden
- URL values must be unique inside the language catalog
- non-HTTPS URLs are forbidden
- duplicate seed URLs are forbidden

Safety rules:

- `candidate_manifest=true` means catalog data is not live runtime input yet.
- `is_live=false` means no DB insert is allowed.
- `is_live=false` means no frontier activation is allowed.
- `is_live=false` means no URL fetch/live probe is allowed.
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert` is mandatory before any DB or frontier insertion.
- pi51c live probe must happen before DB/frontier insert for every language catalog.
- Crawler runtime must not treat catalog rows as live seeds until a separate activation gate sets the approved live state.

Normalization rules:

- All rolled language catalogs must use one canonical `source_families_v2` shape.
- Every source family must have `quality_tier` and `decision`.
- Every seed surface must have `quality_tier` and `decision`.
- Every seed surface must use `seed_urls` as a list of URL objects.
- Empty source families are forbidden.
- Empty seed surfaces are forbidden.
- Duplicate source family codes are forbidden.
- Duplicate seed surface codes are forbidden.
- Duplicate seed URLs are forbidden.
- Host/source hierarchy must stay coherent: one source family can contain multiple country, language, or section seed surfaces.
- FIATA-style multi-country paths must not become separate top-level sources only because country path differs.

Documentation rule:

- `docs/README.md` must list every rolled catalog in `Current sealed startpoint catalogs`.
- `Source-seed policy and decision records` must index each language decision document when it exists.
- Per-language one-off blocks are not preferred; shared rules belong in this canonical standard block.
<!-- SOURCE_SEED_CANONICAL_STARTPOINT_SCHEMA_STANDARD_END -->

<!-- SOURCE_SEED_CANONICAL_RULES_READ_FIRST_BEGIN -->
## Source-seed canonical startpoint JSON rules

- [Crawler Core source-seed startpoint JSON canonical rules](TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md)
- Canonical repository path: `docs/TOPIC_CRAWLER_CORE_SOURCE_SEED_STARTPOINT_JSON_CANONICAL_RULES_2026_05_16.md`
- Mandatory first operation for every language: read the GitHub raw version of this rule document before startpoint planning, writing, audit, commit, push, sync, or activation.
<!-- SOURCE_SEED_CANONICAL_RULES_READ_FIRST_END -->

## Source-seed rollout discipline

- [Source-seed language rollout 17-step discipline / Source-seed dil rollout 17 adım disiplini](TOPIC_CRAWLER_CORE_SOURCE_SEED_LANGUAGE_ROLLOUT_17_STEP_DISCIPLINE_2026_05_17.md) - Permanent 17-step source-seed language rollout standard, including mandatory candidate-list user-review wording.

<!-- SOURCE_SEED_JSON_METADATA_STANDARDS_SUMMARY_BEGIN -->

## Source-seed JSON metadata, standards, and format checkpoint

This README section summarizes the current source-seed JSON standard used after the Bulgarian final JSON truth seal.

### Canonical source-seed JSON format

Every rolled `source_families_v2` catalog remains a candidate manifest until a separate activation gate says otherwise.

Required top-level safety fields:

- `schema`: `source_families_v2`
- `schema_version`: `2.0`
- `candidate_manifest`: `true`
- `is_live`: `false`
- `enabled`: `false`
- `needs_live_check`: `true`
- `runtime_activation_policy`: `pi51c_live_probe_required_before_db_or_frontier_insert`
- `safety_state`: `candidate_only_not_live`

Required seed-level metadata fields:

- `target_language_code`
- `content_language_code`
- `url_locale_code`
- `source_country_codes`
- `covered_country_codes`
- `language_fit`
- `coverage_fit`
- `locale_review_status`

### Language, locale, and country separation

Top-level `language_code` is the rollout target language. It is not proof that every URL is written in that language.

Seed-level `content_language_code` records the actual content language.

Seed-level `url_locale_code` records the visible URL locale signal when available.

Seed-level `source_country_codes` records the source or organization origin.

Seed-level `covered_country_codes` records the country coverage of the page or listing.

Do not add a plain ambiguous `language` field to new source-seed JSON work.

### Reachability and review status format

`locale_review_status=broken_or_blocked` is the canonical candidate-only marker for URL rows that are currently unusable because of HTTP 4xx/5xx, DNS/network/TLS failure, or equivalent blocking found in a controlled read-only reachability probe.

`broken_or_blocked` does not delete the URL and does not activate anything. It preserves the evidence for later repair or replacement.

Rate-limited rows should not be forced into `broken_or_blocked` unless a separate gate decides the block is persistent. Temporary `429` rows may remain as `needs_native_alternative_check` or another explicitly documented review state.

### Bulgarian final JSON truth status

Bulgarian catalog final JSON truth was sealed at:

- Head: `0d912774e0f0522b62743fb755b12812d5979e2b`
- Catalog: `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json`
- SHA256: `cd901adcc5472c8d333c59186894565d22c39846222cce1d342824a83c02d2cc`
- Metrics: 40 source families, 50 seed surfaces, 50 seed URLs, 50 unique HTTPS URLs
- Final status split:
  - `broken_or_blocked`: 14
  - `native_locale_verified`: 3
  - `needs_native_alternative_check`: 26
  - `manual_review_required`: 7

The Bulgarian catalog remains candidate-only and not live.

### Mandatory next-order rule

Before moving into broad `ROLLED_STARTPOINT_JSON_METADATA_GAP_AUDIT_READONLY`, keep documentation and standards aligned first.

25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

No DB insert, no frontier activation, no crawler start, no systemd mutation, no pi51c sync, and no live copy are allowed from source-seed metadata or documentation gates.

<!-- SOURCE_SEED_JSON_METADATA_STANDARDS_SUMMARY_END -->

<!-- SOURCE_SEED_EN_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## English final JSON truth

`ENGLISH_FINAL_JSON_TRUTH_SEALED_HEAD`: `c44c06ae88cdeb6505c0cedf9b28a1ee872c06d7`

English source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- SHA256: `b2b0abc4985dc78fe08b450387a380f8f0579ed3df3549404fbce4743c5e3421`
- Metrics: 171 source families, 561 seed surfaces, 561 seed URLs, 561 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: en=561
  - `content_language_code: en=417, unknown=144`
  - `url_locale_code`: en=417, und=144
  - `language_fit`: native=417, unknown=144
  - `locale_review_status`: native_locale_verified: 417, manual_review_required: 144
  - `coverage_fit`: country_slice_of_global_directory=306, official_company_local_entity=91, regional_or_industry_context=164
- Quality split:
  - A_PLUS=154
  - A=178
  - A_MINUS=81
  - B_PLUS=91
  - B=27
  - B_MINUS=30

English remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_EN_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_TR_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Turkish final JSON truth

`TURKISH_FINAL_JSON_TRUTH_SEALED_HEAD`: `b7534e206ad00314b55578587cad163d3d3708e0`

Turkish source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json`
- SHA256: `d6ec82bc0b2fc91717ecfa080e85ae2fe826cc469dd47c48b86542158957c1cf`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: tr=84
  - `content_language_code: tr=44, en=15, unknown=25`
  - `url_locale_code`: tr=44, en=15, und=25
  - `source_country_codes`: TR=48, ZZ=36
  - `covered_country_codes: TR=58, ZZ=26`
  - `language_fit`: native=44, english_fallback=15, unknown=25
  - `locale_review_status`: native_locale_verified: 44, needs_native_alternative_check: 15, manual_review_required: 25
  - `coverage_fit`: country_primary=16, country_slice_of_global_directory=10, official_company_local_entity=32, regional_or_industry_context=26
- Quality split:
  - A_PLUS=13
  - A=31
  - B_PLUS=15
  - B_MINUS=25

Turkish remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_TR_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_DE_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## German final JSON truth

`GERMAN_FINAL_JSON_TRUTH_SEALED_HEAD`: `e50770241600b9fdbcc0d577fdfb304b6753cda5`

German source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json`
- SHA256: `ce383ba327b70e8246218ffa3e1af72b4094c0a10a8c2e3c01664c31846182cb`
- Metrics: 41 source families, 87 seed surfaces, 87 seed URLs, 87 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: de=87
  - `content_language_code: de=52, en=16, unknown=19`
  - `url_locale_code`: de=52, en=16, und=19
  - `source_country_codes`: DE=51, ZZ=36
  - `covered_country_codes: DE=62, ZZ=25`
  - `language_fit`: native=52, english_fallback=16, unknown=19
  - `locale_review_status`: native_locale_verified: 52, needs_native_alternative_check: 16, manual_review_required: 19
  - `coverage_fit`: country_primary=18, country_slice_of_global_directory=11, official_company_local_entity=33, regional_or_industry_context=25
- Quality split:
  - A_PLUS=17
  - A=35
  - B_PLUS=16
  - B_MINUS=19

German remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_DE_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_AR_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Arabic final JSON truth

`ARABIC_FINAL_JSON_TRUTH_SEALED_HEAD`: `c14b303acf5656a04299f4e734caac7ed63129fe`

Arabic source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json`
- SHA256: `f20349f43bba5ce52d4031619f20f03df2c33ab25fd467ba91bb01195a37a7de`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: ar=84
  - `content_language_code: ar=1, en=63, unknown=20`
  - `url_locale_code`: ar=1, en=63, und=20
  - `source_country_codes`: AE=8, BH=1, EG=4, JO=3, OM=3, SA=6, ZZ=59
  - `covered_country_codes: AE=12, BH=1, EG=4, JO=4, LB=1, OM=4, QA=3, SA=8, ZZ=47`
  - `language_fit`: native=1, english_fallback=63, unknown=20
  - `locale_review_status`: native_locale_verified: 1, needs_native_alternative_check: 63, manual_review_required: 20
  - `coverage_fit`: country_primary=7, country_slice_of_global_directory=12, official_company_local_entity=18, regional_or_industry_context=47
- Quality split:
  - A_PLUS=1
  - A_MINUS=21
  - B_PLUS=42
  - B=2
  - B_MINUS=18

Arabic remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_AR_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_ZH_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Chinese final JSON truth

`CHINESE_FINAL_JSON_TRUTH_SEALED_HEAD`: `28c3f6427c3997ce19e6ccf8a3fd25f6f8e456cb`

Chinese source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json`
- SHA256: `cff8cbd975ea6a203aa6b392d9d56e73e5316677a3cbb4a3c30f9c587324403d`
- Metrics: 105 source families, 148 seed surfaces, 148 seed URLs, 148 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: zh=148
  - `content_language_code: zh=24, en=100, unknown=24`
  - `url_locale_code`: zh=24, en=100, und=24
  - `source_country_codes`: CN=11, DE=5, HK=32, TW=11, ZZ=89
  - `covered_country_codes: CN=44, HK=49, TW=23, ZZ=32`
  - `language_fit`: native=24, english_fallback=100, unknown=24
  - `locale_review_status`: native_locale_verified: 24, needs_native_alternative_check: 100, manual_review_required: 24
  - `coverage_fit`: country_primary=17, country_slice_of_global_directory=62, official_company_local_entity=37, regional_or_industry_context=32
- Quality split:
  - A_PLUS=1
  - A=23
  - A_MINUS=79
  - B_PLUS=21
  - B=1
  - B_MINUS=23

Chinese remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_ZH_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_FR_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## French final JSON truth

`FRENCH_FINAL_JSON_TRUTH_SEALED_HEAD`: `78414f3a3670ab6f46a80aee1ae42449bc7d065c`

French source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json`
- SHA256: `69eeefa0cdacdc974b5583aca5a3a219b7f91598792be3ede6ef686b1fe548ad`
- Metrics: 37 source families, 107 seed surfaces, 107 seed URLs, 107 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: fr=107
  - `content_language_code: fr=8, en=63, unknown=36`
  - `url_locale_code`: fr=8, en=63, und=36
  - `source_country_codes`: BE=3, EU=5, FR=19, LU=8, MA=2, MC=2, ZZ=68
  - `covered_country_codes: BE=15, CH=2, FR=41, LU=6, MA=2, MC=3, SN=1, TN=1, ZZ=36`
  - `language_fit`: native=8, english_fallback=63, unknown=36
  - `locale_review_status`: native_locale_verified: 8, needs_native_alternative_check: 63, manual_review_required: 36
  - `coverage_fit`: country_primary=13, country_slice_of_global_directory=39, official_company_local_entity=19, regional_or_industry_context=36
- Quality split:
  - A_PLUS=1
  - A=7
  - A_MINUS=41
  - B_PLUS=22
  - B=3
  - B_MINUS=33

French remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_FR_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_ES_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Spanish final JSON truth

`SPANISH_FINAL_JSON_TRUTH_SEALED_HEAD`: `878b69c28358e05a47a0bf211a1865097d876c8e`

Spanish source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json`
- SHA256: `b68585e8dc69364eb723f305f3d18f1977c37e78dcb0c7a068136d3753f2a4a3`
- Metrics: 45 source families, 98 seed surfaces, 98 seed URLs, 98 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: es=98
  - `content_language_code: es=19, en=44, unknown=35`
  - `url_locale_code`: es=19, en=44, und=35
  - `source_country_codes`: CO=2, DE=2, ES=21, GB=2, ZZ=71
  - `covered_country_codes: ES=46, ZZ=52`
  - `language_fit`: native=19, english_fallback=44, unknown=35
  - `locale_review_status`: native_locale_verified: 19, needs_native_alternative_check: 44, manual_review_required: 35
  - `coverage_fit`: country_primary=9, country_slice_of_global_directory=25, official_company_local_entity=12, regional_or_industry_context=52
- Quality split:
  - A_PLUS=4
  - A=15
  - A_MINUS=22
  - B_PLUS=22
  - B=4
  - B_MINUS=31

Spanish remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_ES_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_IT_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Italian final JSON truth

`ITALIAN_FINAL_JSON_TRUTH_SEALED_HEAD`: `9765f095f674a61192695bd3d605310866d7ca8f`

Italian source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json`
- SHA256: `d2b8f017a757839f784b54a9fbc8c34ac86d60630e6d63cb65bf82fe0ef1be7a`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: it=84
  - `content_language_code: it=21, en=28, unknown=35`
  - `url_locale_code`: it=21, en=28, und=35
  - `source_country_codes`: EU=2, IT=66, ZZ=16
  - `covered_country_codes: IT=70, ZZ=14`
  - `language_fit`: native=21, english_fallback=28, unknown=35
  - `locale_review_status`: native_locale_verified: 21, needs_native_alternative_check: 28, manual_review_required: 35
  - `coverage_fit`: country_primary=14, country_slice_of_global_directory=4, official_company_local_entity=52, regional_or_industry_context=14
- Quality split:
  - A_PLUS=10
  - A=11
  - A_MINUS=24
  - B_PLUS=4
  - B_MINUS=35

Italian remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_IT_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_PT_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Portuguese final JSON truth

`PORTUGUESE_FINAL_JSON_TRUTH_SEALED_HEAD`: `0a90002be0efff93a3c59a4bfe83dfe3d221d4b6`

Portuguese source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json`
- SHA256: `7a429b8995e29e3634452fb71e463d0237e498a6498ff9227a3ae753febc984d`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: pt=84
  - `content_language_code: pt=13, en=56, unknown=15`
  - `url_locale_code`: pt=13, en=56, und=15
  - `source_country_codes`: PT=59, ZZ=25
  - `covered_country_codes: PT=60, ZZ=24`
  - `language_fit`: native=13, english_fallback=56, unknown=15
  - `locale_review_status`: native_locale_verified: 13, needs_native_alternative_check: 56, manual_review_required: 15
  - `coverage_fit`: country_primary=8, country_slice_of_global_directory=1, official_company_local_entity=51, regional_or_industry_context=24
- Quality split:
  - A_PLUS=3
  - A=10
  - A_MINUS=40
  - B_PLUS=16
  - B_MINUS=15

Portuguese remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_PT_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_NL_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Dutch final JSON truth

`DUTCH_FINAL_JSON_TRUTH_SEALED_HEAD`: `24b70c7821136fcd66d182cd4e49a3f4b234766f`

Dutch source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json`
- SHA256: `b364a2849fe2d62fa6213d1f4cf6b3ec7e30935598e39faeef91b5bd63a82594`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: nl=84
  - `content_language_code: nl=41, en=30, unknown=13`
  - `url_locale_code`: nl=41, en=30, und=13
  - `source_country_codes`: NL=23, ZZ=55, EU=4, CO=2
  - `covered_country_codes: NL=41, ZZ=43`
  - `language_fit`: native=41, english_fallback=30, unknown=13
  - `locale_review_status`: native_locale_verified: 41, needs_native_alternative_check: 30, manual_review_required: 13
  - `coverage_fit`: country_primary=13, country_slice_of_global_directory=18, official_company_local_entity=10, regional_or_industry_context=43
- Quality split:
  - A_PLUS=9
  - A=32
  - A_MINUS=8
  - B_PLUS=22
  - B_MINUS=13

Dutch remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_NL_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_RU_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Russian final JSON truth

`RUSSIAN_FINAL_JSON_TRUTH_SEALED_HEAD`: `9fc0a004520045e62a03d427b945134f18552372`

Russian source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json`
- SHA256: `18a36e0051b46b0200a001d42cbe17bb22468e4257ce729465c8d065dced128c`
- Metrics: 40 source families, 84 seed surfaces, 84 seed URLs, 84 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
- Seed metadata completeness:
  - `target_language_code`: ru=84
  - `content_language_code: ru=38, en=25, unknown=21`
  - `url_locale_code`: ru=38, en=25, und=21
  - `source_country_codes`: RU=30, ZZ=48, CO=4, GB=2
  - `covered_country_codes: RU=59, ZZ=25`
  - `language_fit`: native=38, english_fallback=25, unknown=21
  - `locale_review_status`: native_locale_verified: 38, needs_native_alternative_check: 25, manual_review_required: 21
  - `coverage_fit`: country_primary=4, country_slice_of_global_directory=29, official_company_local_entity=26, regional_or_industry_context=25
- Quality split:
  - A_PLUS=1
  - A=37
  - A_MINUS=10
  - B_PLUS=15
  - B_MINUS=21

Russian remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_RU_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_UK_FINAL_JSON_TRUTH_STATUS_BEGIN -->

## Ukrainian final JSON truth

`UKRAINIAN_FINAL_JSON_TRUTH_SEALED_HEAD`: `274260de62e11f04db35f34852f196be3b5f09f5`

Ukrainian source-seed catalog final JSON truth is sealed for the current metadata model.

- Catalog: `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json`
- SHA256: `5588b73db4f418c16157559b3447325ae39ebb5a7f0aa119a8cb139c4179ecf0`
- Metrics: 40 source families, 56 seed surfaces, 56 seed URLs, 56 unique HTTPS URLs
- Candidate/runtime safety:
  - `candidate_manifest=true`
  - `is_live=false`
  - `enabled=false`
  - `needs_live_check=true`
  - `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`
  - `safety_state=candidate_only_not_live`
  - `review_state=needs_live_check`
- Seed metadata completeness:
  - `target_language_code`: uk=56
  - `content_language_code: uk=23, en=30, unknown=3`
  - `url_locale_code`: uk=23, en=30, und=3
  - `source_country_codes`: UA=26, ZZ=27, CO=3
  - `covered_country_codes: UA=45, ZZ=11`
  - `language_fit`: native=23, english_fallback=30, unknown=3
  - `locale_review_status`: native_locale_verified: 23, needs_native_alternative_check: 30, manual_review_required: 3
  - `coverage_fit`: country_primary=15, country_slice_of_global_directory=20, official_company_local_entity=10, regional_or_industry_context=11
- Quality split:
  - A=23
  - A_MINUS=23
  - B_PLUS=7
  - B_MINUS=3

Ukrainian remains candidate-only. This seal does not allow DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_UK_FINAL_JSON_TRUTH_STATUS_END -->

<!-- SOURCE_SEED_CS_DOCS_STANDARD_PATCH_2026_05_19 -->

## Source-seed rollout update — Czech (`cs`) — 2026-05-19

Czech (`cs`) is now recorded as a candidate-only source-seed rollout language.

- Language: Czech
- Language code: `cs`
- Decision document: `docs/TOPIC_CRAWLER_CORE_CZECH_SOURCE_SEED_URLS_DECISION_2026_05_19.md`
- Candidate catalog: `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json`
- Source families: 45 source families
- Seed surfaces: 90 seed surfaces
- Seed URLs: 90 seed URLs
- Candidate state: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Safety state: `candidate_only_not_live`
- Commit subject: `feat(source-seed): add Czech startpoint catalog`

This README entry is an index/standards pointer only. It does not authorize DB insertion, frontier insertion, crawler start, systemd mutation, pi51c sync, or public URL probing.
