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
