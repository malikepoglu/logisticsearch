# PostgreSQL JSON Runtime Topology / PostgreSQL JSON Runtime Topolojisi

## 1. Very short answer / En kısa cevap

EN: `logisticsearch_crawler` is the live PostgreSQL logical database name.

TR: `logisticsearch_crawler` canlı PostgreSQL mantıksal database adıdır.

EN: It is not a file. Therefore it has no extension. It is not `logisticsearch_crawler.json`, not `logisticsearch_crawler.sql`, not `logisticsearch_crawler.db`.

TR: Bu bir dosya değildir. Bu yüzden uzantısı yoktur. `logisticsearch_crawler.json`, `logisticsearch_crawler.sql`, `logisticsearch_crawler.db` değildir.

EN: The JSON files in this repository are manifests. They describe the shape, meaning, and safety rules of runtime data. They are not the live database itself.

TR: Bu repository içindeki JSON dosyaları manifesttir. Runtime verisinin şeklini, anlamını ve güvenlik kurallarını açıklar. Canlı database'in kendisi değildir.

## 2. The three different layers / Üç farklı katman

EN: Layer 1 is PostgreSQL. PostgreSQL is the runtime authority.

TR: Katman 1 PostgreSQL'dir. PostgreSQL runtime otoritesidir.

EN: Layer 2 is JSON and JSONB. JSON in GitHub is the controlled representation. JSONB in PostgreSQL can later hold structured runtime metadata.

TR: Katman 2 JSON ve JSONB'dir. GitHub içindeki JSON kontrollü temsil katmanıdır. PostgreSQL içindeki JSONB ileride yapılı runtime metadata tutabilir.

EN: Layer 3 is runtime file storage. Raw HTTP body files are stored outside GitHub under a runtime directory.

TR: Katman 3 runtime dosya saklama alanıdır. Ham HTTP body dosyaları GitHub dışında runtime dizininde saklanır.

## 3. Canonical names / Kanonik isimler

EN:
  Live PostgreSQL logical database name:
    logisticsearch_crawler

TR:
  Canlı PostgreSQL mantıksal database adı:
    logisticsearch_crawler

EN:
  Repository database key:
    crawler_core

TR:
  Repository database anahtarı:
    crawler_core

EN:
  Raw HTTP body runtime root:
    /srv/webcrawler/raw_fetch

TR:
  Ham HTTP body runtime kökü:
    /srv/webcrawler/raw_fetch

EN:
  Processed output runtime root:
    /srv/data

TR:
  İşlenmiş çıktı runtime kökü:
    /srv/data

## 4. Why repo path says crawler_core / Repo path neden crawler_core diyor?

EN: The repository path uses `crawler_core` because this folder documents the crawler_core part of the system.

TR: Repository path `crawler_core` kullanır çünkü bu klasör sistemin crawler_core bölümünü belgeler.

EN: The live PostgreSQL database can still be named `logisticsearch_crawler`.

TR: Canlı PostgreSQL database adı yine `logisticsearch_crawler` olabilir.

EN: These two names serve different jobs. `logisticsearch_crawler` is the live database name. `crawler_core` is the repo design key for the crawler_core contract.

TR: Bu iki isim farklı işler yapar. `logisticsearch_crawler` canlı database adıdır. `crawler_core` crawler_core sözleşmesi için repo tasarım anahtarıdır.

## 5. Canonical repository topology / Kanonik repository topolojisi

EN: Current lean topology:

    makpi51crawler/postgresql/
      README.md
      schemas/
        postgresql_runtime_manifest.v1.schema.json
      databases/
        crawler_core/
          README.md
          raw_fetch/
            README.md
            frontier_queue.v1.json
            http_raw_capture.v1.json

TR: Mevcut yalın topoloji:

    makpi51crawler/postgresql/
      README.md
      schemas/
        postgresql_runtime_manifest.v1.schema.json
      databases/
        crawler_core/
          README.md
          raw_fetch/
            README.md
            frontier_queue.v1.json
            http_raw_capture.v1.json

## 6. What is frontier_queue.v1.json? / frontier_queue.v1.json nedir?

EN: `frontier_queue.v1.json` describes the durable URL queue intent.

TR: `frontier_queue.v1.json` kalıcı URL kuyruğu niyetini açıklar.

EN: It explains URL queue concepts such as queued URL, claim, lease, retry, revisit, priority, depth, parent URL, discovery type, and rediscovery safety.

TR: queued URL, claim, lease, retry, revisit, priority, depth, parent URL, discovery type ve rediscovery güvenliği gibi URL kuyruğu kavramlarını açıklar.

EN: It is not the queue table itself. PostgreSQL remains the runtime authority.

TR: Kuyruk tablosunun kendisi değildir. Runtime otoritesi PostgreSQL olarak kalır.

## 7. What is http_raw_capture.v1.json? / http_raw_capture.v1.json nedir?

EN: `http_raw_capture.v1.json` describes the first raw HTTP capture produced by crawler_core.

TR: `http_raw_capture.v1.json`, crawler_core tarafından üretilen ilk ham HTTP capture bilgisini açıklar.

EN: It is not a database name.

TR: Database adı değildir.

EN: It explains fields such as url_id, fetch_attempt_id, requested_url, final_url, http_status, content_type, body_bytes, body_sha256, raw body path, and fetched_at.

TR: url_id, fetch_attempt_id, requested_url, final_url, http_status, content_type, body_bytes, body_sha256, ham body path ve fetched_at gibi alanları açıklar.

EN: The actual raw body bytes are not stored in GitHub. They are stored under `/srv/webcrawler/raw_fetch` at runtime.

TR: Gerçek ham body byte'ları GitHub içinde saklanmaz. Runtime sırasında `/srv/webcrawler/raw_fetch` altında saklanır.

## 8. PostgreSQL internal storage warning / PostgreSQL iç storage uyarısı

EN: PostgreSQL may store its own physical engine files under a cluster directory such as `/srv/postgresql/...`.

TR: PostgreSQL kendi fiziksel motor dosyalarını `/srv/postgresql/...` gibi bir cluster dizini altında tutabilir.

EN: That is PostgreSQL internal storage. It is not a crawler application path. Do not design crawler file flow around PostgreSQL internal OID folders.

TR: Bu PostgreSQL iç storage alanıdır. Crawler uygulama path'i değildir. Crawler dosya akışını PostgreSQL iç OID klasörleri üzerine kurma.

EN: The crawler application paths are `/srv/webcrawler/raw_fetch` for raw body artefacts and `/srv/data` for processed output.

TR: Crawler uygulama pathleri ham body artefactları için `/srv/webcrawler/raw_fetch`, işlenmiş çıktı için `/srv/data` olmalıdır.

## 9. Forbidden retired surfaces / Yasak emekli yüzeyler

EN: Do not create or restore these paths:

    top-level sql/
    makpi51crawler/sql/
    makpi51crawler/postgresql/patch_manifests/
    makpi51crawler/postgresql/databases/logisticsearch_crawler/
    makpi51crawler/postgresql/databases/crawler_core/runtime_changes/

TR: Bu pathleri oluşturma veya geri getirme:

    top-level sql/
    makpi51crawler/sql/
    makpi51crawler/postgresql/patch_manifests/
    makpi51crawler/postgresql/databases/logisticsearch_crawler/
    makpi51crawler/postgresql/databases/crawler_core/runtime_changes/

## 10. Design rule / Tasarım kuralı

EN: Keep the system small, obvious, and PostgreSQL plus JSON/JSONB based.

TR: Sistemi küçük, açık ve PostgreSQL plus JSON/JSONB temelli tut.

EN: Add new folders only after an explicit topology decision.

TR: Yeni klasörleri sadece açık bir topoloji kararı sonrası ekle.
