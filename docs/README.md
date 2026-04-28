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
