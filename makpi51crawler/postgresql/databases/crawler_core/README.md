# crawler_core PostgreSQL JSON database key / crawler_core PostgreSQL JSON database anahtarı

## 1. Short answer / Kısa cevap

EN: This folder is named `crawler_core` because it documents the crawler_core runtime contract.

TR: Bu klasör `crawler_core` adını taşır çünkü crawler_core runtime sözleşmesini belgeler.

EN: This folder is not the live PostgreSQL database.

TR: Bu klasör canlı PostgreSQL database değildir.

EN: The live PostgreSQL logical database name is `logisticsearch_crawler`.

TR: Canlı PostgreSQL mantıksal database adı `logisticsearch_crawler` değeridir.

EN: `logisticsearch_crawler` is not a file and has no extension.

TR: `logisticsearch_crawler` bir dosya değildir ve uzantısı yoktur.

## 2. Two names, two jobs / İki isim, iki görev

EN: `logisticsearch_crawler` is the runtime database name used by PostgreSQL.

TR: `logisticsearch_crawler`, PostgreSQL tarafından kullanılan runtime database adıdır.

EN: `crawler_core` is the repository design key for the crawler_core layer.

TR: `crawler_core`, crawler_core katmanı için repository tasarım anahtarıdır.

EN: The repo path uses the design key because it should be easy to understand what part of the system is being documented.

TR: Repo path tasarım anahtarını kullanır çünkü sistemin hangi bölümünün belgelendiği kolay anlaşılmalıdır.

## 3. Current topology / Mevcut topoloji

EN:

    makpi51crawler/postgresql/databases/crawler_core/
      README.md
      raw_fetch/
        README.md
        frontier_queue.v1.json
        http_raw_capture.v1.json

TR:

    makpi51crawler/postgresql/databases/crawler_core/
      README.md
      raw_fetch/
        README.md
        frontier_queue.v1.json
        http_raw_capture.v1.json

EN: `raw_fetch/` is first because crawler_core first proves raw HTTP fetch, raw body storage, minimal parse, and discovery.

TR: `raw_fetch/` önce gelir çünkü crawler_core ilk olarak ham HTTP fetch, ham body storage, minimal parse ve discovery akışını kanıtlar.

## 4. What belongs here? / Buraya ne konur?

EN: This folder contains source-controlled PostgreSQL plus JSON/JSONB representation files.

TR: Bu klasör source-controlled PostgreSQL plus JSON/JSONB temsil dosyalarını içerir.

EN: These files explain what crawler_core expects from the live PostgreSQL runtime.

TR: Bu dosyalar crawler_core'un canlı PostgreSQL runtime yüzeyinden ne beklediğini açıklar.

EN: They do not replace PostgreSQL.

TR: PostgreSQL'in yerine geçmezler.

EN: They do not store live PostgreSQL physical files.

TR: Canlı PostgreSQL fiziksel dosyalarını saklamazlar.

EN: They do not store raw HTTP body bytes.

TR: Ham HTTP body byte'larını saklamazlar.

## 5. Database name versus manifest file / Database adı ve manifest dosyası farkı

EN: Database name:

    logisticsearch_crawler

TR: Database adı:

    logisticsearch_crawler

EN: Manifest files:

    raw_fetch/frontier_queue.v1.json
    raw_fetch/http_raw_capture.v1.json

TR: Manifest dosyaları:

    raw_fetch/frontier_queue.v1.json
    raw_fetch/http_raw_capture.v1.json

EN: The database name has no `.json` extension because it is not a JSON file.

TR: Database adında `.json` uzantısı yoktur çünkü JSON dosyası değildir.

EN: The `.json` files are human-readable runtime-shape contracts.

TR: `.json` dosyaları insan tarafından okunabilir runtime-şekil sözleşmeleridir.

## 6. Runtime storage paths / Runtime storage pathleri

EN: Raw HTTP body files belong under:

    /srv/webcrawler/raw_fetch

TR: Ham HTTP body dosyaları şu path altında durur:

    /srv/webcrawler/raw_fetch

EN: Processed output belongs under:

    /srv/data

TR: İşlenmiş çıktı şu path altında durur:

    /srv/data

EN: PostgreSQL internal cluster folders are not crawler application paths.

TR: PostgreSQL iç cluster klasörleri crawler uygulama path'i değildir.

## 7. What PostgreSQL stores / PostgreSQL ne saklar?

EN: PostgreSQL stores durable runtime metadata: URL state, queue state, claim/lease state, retry timing, revisit timing, fetch attempt metadata, raw body path, body hash, and workflow state.

TR: PostgreSQL kalıcı runtime metadata saklar: URL durumu, kuyruk durumu, claim/lease durumu, retry zamanı, revisit zamanı, fetch attempt metadata, ham body path, body hash ve workflow state.

EN: PostgreSQL may also use JSONB columns later for structured runtime metadata.

TR: PostgreSQL ileride yapılı runtime metadata için JSONB kolonları da kullanabilir.

## 8. What runtime files store / Runtime dosyaları ne saklar?

EN: Large raw HTTP response body bytes are stored as artefact files under `/srv/webcrawler/raw_fetch`.

TR: Büyük ham HTTP response body byte'ları `/srv/webcrawler/raw_fetch` altında artefact dosyaları olarak saklanır.

EN: PostgreSQL stores the path and integrity metadata for those artefacts.

TR: PostgreSQL bu artefactlar için path ve bütünlük metadata değerlerini saklar.

## 9. Forbidden topology drift / Yasak topoloji sapması

EN: Do not create these paths here:

    runtime_changes/
    frontier/
    patch_manifests/
    loose SQL folders

TR: Burada şu pathleri oluşturma:

    runtime_changes/
    frontier/
    patch_manifests/
    gevşek SQL klasörleri

EN: If a new PostgreSQL runtime representation is needed, first decide the topology explicitly.

TR: Yeni bir PostgreSQL runtime temsili gerekirse önce topolojiyi açıkça kararlaştır.

## 10. Current design status / Mevcut tasarım durumu

EN: Current scope is crawler_core raw fetch representation only.

TR: Mevcut kapsam yalnızca crawler_core raw fetch temsilidir.

EN: Taxonomy, ranking, runtime change systems, and long crawler loop readiness are separate later lines.

TR: Taxonomy, ranking, runtime change sistemleri ve uzun crawler loop hazır oluşu ayrı sonraki hatlardır.
