# PostgreSQL JSON Runtime Topology and Raw Fetch Manifest Standard — 2026-05-07

## 1. Purpose / Amaç

EN:
This document defines the lean PostgreSQL plus JSON runtime topology for LogisticSearch crawler work.
It exists because crawler_core must be understandable, reproducible, and safe without resurrecting loose SQL directories.

TR:
Bu belge LogisticSearch crawler çalışmaları için yalın PostgreSQL artı JSON runtime topolojisini tanımlar.
Bu belge gereklidir; çünkü crawler_core gevşek SQL klasörlerini geri getirmeden anlaşılır, tekrar üretilebilir ve güvenli olmalıdır.

EN:
The rule is strict: PostgreSQL is the runtime authority, JSON and JSONB are the controlled representation layer.

TR:
Kural katıdır: PostgreSQL runtime otoritesidir, JSON ve JSONB kontrollü temsil katmanıdır.

## 2. Non-Negotiable Architecture Rule / Esnetilemez Mimari Kural

EN:
Do not create or restore these retired surfaces:

- top-level sql/
- makpi51crawler/sql/
- loose standalone SQL ownership files

TR:
Şu emekli yüzeyler oluşturulmayacak veya geri getirilmeyecek:

- kök dizinde sql/
- makpi51crawler/sql/
- bağımsız ve gevşek SQL sahiplik dosyaları

EN:
SQL text may exist inside controlled PostgreSQL JSON manifests when a function or runtime object must be represented before a gated PostgreSQL apply step.

TR:
Bir fonksiyon veya runtime nesnesi kontrollü PostgreSQL apply adımından önce temsil edilecekse SQL metni kontrollü PostgreSQL JSON manifestleri içinde bulunabilir.

## 3. Repository Topology / Repository Topolojisi

EN:
The intended repository topology is:

- makpi51crawler/postgresql/README.md
- makpi51crawler/postgresql/schemas/postgresql_runtime_manifest.v1.schema.json
- makpi51crawler/postgresql/databases/logisticsearch_crawler/README.md
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/README.md
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/frontier_queue.v1.json
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/http_raw_capture.v1.json

TR:
Hedef repository topolojisi şudur:

- makpi51crawler/postgresql/README.md
- makpi51crawler/postgresql/schemas/postgresql_runtime_manifest.v1.schema.json
- makpi51crawler/postgresql/databases/logisticsearch_crawler/README.md
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/README.md
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/frontier_queue.v1.json
- makpi51crawler/postgresql/databases/logisticsearch_crawler/raw_fetch/http_raw_capture.v1.json

EN:
This topology is intentionally small. It separates database ownership, raw fetch ownership, queue intent, and raw HTTP capture truth.

TR:
Bu topoloji özellikle küçük tutulmuştur. Veritabanı sahipliği, ham fetch sahipliği, kuyruk niyeti ve ham HTTP capture doğrusu birbirinden ayrılır.

## 4. Meaning of Each Directory / Her Dizinin Anlamı

### 4.1 makpi51crawler/postgresql/

EN:
This is the PostgreSQL runtime representation root.
It does not mean PostgreSQL is replaced by files.
It means repository-side controlled JSON descriptions live here.

TR:
Burası PostgreSQL runtime temsil köküdür.
Bu, PostgreSQL dosyalarla değiştiriliyor anlamına gelmez.
Repository tarafındaki kontrollü JSON tanımları burada yaşar.

### 4.2 makpi51crawler/postgresql/schemas/

EN:
This directory contains JSON Schema files.
All PostgreSQL-related manifest schemas stay together here.
Separation is done by file name, not by unnecessary nested folders.

TR:
Bu dizin JSON Schema dosyalarını içerir.
PostgreSQL ile ilgili tüm manifest şemaları burada birlikte durur.
Ayrım gereksiz iç klasörlerle değil, dosya adıyla yapılır.

### 4.3 makpi51crawler/postgresql/databases/

EN:
This directory groups repository-side JSON descriptions by logical PostgreSQL database name.

TR:
Bu dizin repository tarafındaki JSON tanımları mantıksal PostgreSQL veritabanı adına göre gruplar.

### 4.4 logisticsearch_crawler/

EN:
This directory represents the crawler runtime database area.
It is not the physical database itself.
The physical authority is still PostgreSQL.

TR:
Bu dizin crawler runtime veritabanı alanını temsil eder.
Fiziksel veritabanının kendisi değildir.
Fiziksel otorite hâlâ PostgreSQL’dir.

### 4.5 raw_fetch/

EN:
This directory is for the first crawler_core acquisition layer.
It describes the queue and raw HTTP capture standards before parse, ranking, taxonomy, or desktop import.

TR:
Bu dizin crawler_core’un ilk veri alma katmanı içindir.
Parse, ranking, taxonomy veya desktop import öncesindeki queue ve ham HTTP capture standartlarını tanımlar.

## 5. frontier_queue.v1.json / Kuyruk Manifesti

EN:
frontier_queue.v1.json describes the durable URL queue intent.
It answers simple questions:

- Which URL is known?
- Why is it known?
- Is it a seed or discovered link?
- When may it be fetched?
- What state is it in?
- What priority does it have?

TR:
frontier_queue.v1.json kalıcı URL kuyruğu niyetini tanımlar.
Basit sorulara cevap verir:

- Hangi URL biliniyor?
- Neden biliniyor?
- Seed mi, keşfedilmiş link mi?
- Ne zaman fetch edilebilir?
- Hangi durumda?
- Önceliği nedir?

EN:
This file does not store fetched page bodies.
It describes the queue model that PostgreSQL frontier tables enforce.

TR:
Bu dosya fetch edilmiş sayfa gövdelerini saklamaz.
PostgreSQL frontier tablolarının uyguladığı queue modelini tanımlar.

## 6. http_raw_capture.v1.json / İlk Ham Veri Manifesti

EN:
http_raw_capture.v1.json is the first raw data manifest for crawler_core.
It describes what is captured when crawler_core performs an HTTP fetch.

TR:
http_raw_capture.v1.json crawler_core için ilk ham veri manifestidir.
crawler_core HTTP fetch yaptığında neyin yakalandığını tanımlar.

EN:
This is where the first raw acquisition truth belongs.
The actual large body file may live on controlled storage, for example under raw_fetch storage paths.
The JSON manifest describes identity, metadata, checksums, content type, byte count, and storage path.

TR:
İlk ham veri alma doğrusu burada tanımlanır.
Büyük body dosyasının kendisi kontrollü storage altında, örneğin raw_fetch storage path içinde bulunabilir.
JSON manifest ise kimlik, metadata, checksum, content type, byte sayısı ve storage path bilgisini tanımlar.

EN:
The shape of http_raw_capture.v1.json will evolve while crawler_core becomes stricter.
That evolution must be controlled, documented, and backward-aware.

TR:
http_raw_capture.v1.json yapısı crawler_core sertleştikçe gelişecektir.
Bu gelişim kontrollü, belgelenmiş ve geriye dönük uyumluluğu düşünen şekilde yapılmalıdır.

## 7. Current R114 Decision / Güncel R114 Kararı

EN:
The earlier patch_manifests naming is not ideal for the long-term lean topology.
Because the system is being built cleanly, the design should prefer runtime topology and object manifests rather than patch-centered language.

TR:
Önceki patch_manifests adlandırması uzun vadeli yalın topoloji için ideal değildir.
Sistem temiz şekilde kurulduğu için tasarım patch merkezli dil yerine runtime topolojisi ve object manifest yaklaşımını tercih etmelidir.

EN:
R114 must continue without resurrecting SQL directories.
The next design step should move toward the topology defined in this document.

TR:
R114 SQL dizinlerini geri getirmeden devam etmelidir.
Sonraki tasarım adımı bu belgede tanımlanan topolojiye doğru ilerlemelidir.

---

## R115 — Crawl Map / Resume JSONB Standard

EN: This section defines the lean JSONB context standard for `frontier.url.url_metadata`. PostgreSQL columns remain the durable runtime authority; JSONB only carries lightweight crawl-map, discovery, resume, and policy context.

TR: Bu bölüm `frontier.url.url_metadata` için yalın JSONB bağlam standardını tanımlar. Dayanıklı runtime otoritesi PostgreSQL kolonlarıdır; JSONB yalnızca hafif crawl-map, keşif, resume ve policy bağlamını taşır.

### EN: Runtime authority / TR: Runtime otoritesi

EN: The following PostgreSQL columns remain the source of truth: `parent_url_id`, `depth`, `discovery_type`, `host_id`, `state`, `next_fetch_at`, `lease_token`, `lease_expires_at`, `last_success_at`, and `success_count`.

TR: Aşağıdaki PostgreSQL kolonları gerçek kaynak olarak kalır: `parent_url_id`, `depth`, `discovery_type`, `host_id`, `state`, `next_fetch_at`, `lease_token`, `lease_expires_at`, `last_success_at` ve `success_count`.

### EN: JSONB schema / TR: JSONB şeması

EN: The approved schema marker is `crawler_url_metadata.v1`.

TR: Onaylı şema işareti `crawler_url_metadata.v1` değeridir.

Allowed JSONB sections:

- `crawl_map`: `root_url_id`, `branch_role`, `branch_label`, `crawl_path_hint`
- `discovered_from`: `surface`, `source_url_id`, `link_text_normalized`, `selector_hint`, `source_content_type`
- `resume`: `last_checkpoint_phase`, `last_checkpoint_at`, `last_worker_id`, `last_safe_resume_action`
- `policy`: `crawl_reason`, `robots_allowed`, `nofollow_seen`, `noindex_seen`, `politeness_bucket`

### EN: Resume state interpretation / TR: Resume state yorumu

EN: `queued` is a durable waiting point. The crawler may claim it only when `next_fetch_at` is due.

TR: `queued` dayanıklı bekleme noktasıdır. Crawler bunu yalnızca `next_fetch_at` zamanı geldiğinde claim edebilir.

EN: `leased` is in-flight work. The crawler must not duplicate it while the lease is valid; expired leases may be reclaimed by the controlled claim path.

TR: `leased` devam eden iştir. Lease geçerliyken duplicate iş yapılmaz; süresi dolmuş lease yalnızca kontrollü claim yolu ile geri alınabilir.

EN: `parse_pending` means fetch finished and parse_core should process the raw capture or release the URL through a controlled path.

TR: `parse_pending` fetch’in bittiğini ve parse_core’un raw capture verisini işlemesi ya da URL’yi kontrollü yolla bırakması gerektiğini gösterir.

EN: `retry_wait` is an error/backoff state. `next_fetch_at` must be preserved until retry time is due.

TR: `retry_wait` hata/backoff durumudur. Retry zamanı gelene kadar `next_fetch_at` korunmalıdır.

### EN: Forbidden topology / TR: Yasak topoloji

EN: Do not resurrect `sql/`, `makpi51crawler/sql/`, `patch_manifests/`, or `runtime_changes/`.

TR: `sql/`, `makpi51crawler/sql/`, `patch_manifests/` veya `runtime_changes/` geri getirilmez.

EN: `http_raw_capture.v1.json` is a manifest, not a database name. The live PostgreSQL logical database name remains `logisticsearch_crawler`; the repository topology key remains `crawler_core`.

TR: `http_raw_capture.v1.json` bir manifesttir, veritabanı adı değildir. Canlı PostgreSQL mantıksal veritabanı adı `logisticsearch_crawler`; repo topoloji anahtarı `crawler_core` olarak kalır.



### EN: R115 first queue patch target / TR: R115 ilk queue patch hedefi

EN: Read-only DB audits R115_R5A through R115_R5C identified `frontier.enqueue_discovered_url` as the first queue correctness patch target.

TR: R115_R5A ile R115_R5C arasındaki read-only DB auditleri, ilk queue doğruluk patch hedefi olarak `frontier.enqueue_discovered_url` fonksiyonunu belirledi.

EN: The patch must prevent rediscovery from forcing already-successful queued URLs back to immediate due status by rewriting `next_fetch_at` to `now()`.

TR: Patch, rediscovery sırasında daha önce başarılı olmuş queued URL’lerin `next_fetch_at` değeri `now()` yapılarak hemen due hale zorlanmasını engellemelidir.

EN: No `sql/`, `makpi51crawler/sql/`, `patch_manifests/`, or `runtime_changes/` surface is introduced by this decision. The live DB patch remains a separate controlled apply gate.

TR: Bu karar `sql/`, `makpi51crawler/sql/`, `patch_manifests/` veya `runtime_changes/` yüzeyi oluşturmaz. Canlı DB patch’i ayrı kontrollü apply gate olarak kalır.


EN: Exact queue safety invariant: Do not overwrite future next_fetch_at for successful queued rows. New URL inserts must remain immediately crawlable.

TR: Exact queue güvenlik invariantı: başarılı queued URL satırlarında gelecekteki `next_fetch_at` ezilmez. Yeni URL insert’leri hemen crawl edilebilir kalır.
