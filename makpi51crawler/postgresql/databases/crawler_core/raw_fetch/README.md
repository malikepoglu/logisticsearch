# raw_fetch PostgreSQL JSON manifests / raw_fetch PostgreSQL JSON manifestleri

## 1. Short answer / Kısa cevap

EN: `raw_fetch/` documents the first raw data boundary of crawler_core.

TR: `raw_fetch/`, crawler_core'un ilk ham veri sınırını belgeler.

EN: This folder does not store real raw HTTP body bytes.

TR: Bu klasör gerçek ham HTTP body byte'larını saklamaz.

EN: Real raw HTTP body files are stored at runtime under `/srv/webcrawler/raw_fetch`.

TR: Gerçek ham HTTP body dosyaları runtime sırasında `/srv/webcrawler/raw_fetch` altında saklanır.

EN: PostgreSQL stores durable metadata and points to those raw body files.

TR: PostgreSQL kalıcı metadata saklar ve bu ham body dosyalarına işaret eder.

## 2. Current files / Mevcut dosyalar

EN:

    raw_fetch/
      README.md
      frontier_queue.v1.json
      http_raw_capture.v1.json

TR:

    raw_fetch/
      README.md
      frontier_queue.v1.json
      http_raw_capture.v1.json

EN: `frontier_queue.v1.json` explains the URL queue and scheduling intent.

TR: `frontier_queue.v1.json`, URL kuyruğu ve zamanlama niyetini açıklar.

EN: `http_raw_capture.v1.json` explains the raw HTTP capture metadata shape.

TR: `http_raw_capture.v1.json`, ham HTTP capture metadata şeklini açıklar.

## 3. What is frontier_queue.v1.json? / frontier_queue.v1.json nedir?

EN: `frontier_queue.v1.json` is a manifest for queue intent.

TR: `frontier_queue.v1.json`, kuyruk niyeti için bir manifesttir.

EN: It describes how crawler_core thinks about URLs before fetch.

TR: crawler_core'un fetch öncesinde URL'leri nasıl düşündüğünü açıklar.

EN: It covers concepts such as canonical URL, queued state, claim, lease, priority, depth, parent URL, discovery type, retry timing, and revisit timing.

TR: canonical URL, queued state, claim, lease, priority, depth, parent URL, discovery type, retry timing ve revisit timing gibi kavramları kapsar.

EN: It is not the live queue table itself.

TR: Canlı kuyruk tablosunun kendisi değildir.

EN: PostgreSQL remains the runtime authority.

TR: Runtime otoritesi PostgreSQL olarak kalır.

## 4. What is http_raw_capture.v1.json? / http_raw_capture.v1.json nedir?

EN: `http_raw_capture.v1.json` is the manifest for the first raw HTTP data captured by crawler_core.

TR: `http_raw_capture.v1.json`, crawler_core tarafından yakalanan ilk ham HTTP verisinin manifestidir.

EN: It is not a database name.

TR: Database adı değildir.

EN: It is not the raw body file.

TR: Ham body dosyasının kendisi değildir.

EN: It describes the metadata that links PostgreSQL, the fetched URL, the fetch attempt, and the raw body artefact.

TR: PostgreSQL, fetch edilen URL, fetch attempt ve ham body artefact arasındaki metadata bağlantısını açıklar.

## 5. Runtime path difference / Runtime path farkı

EN: Repo manifest path:

    makpi51crawler/postgresql/databases/crawler_core/raw_fetch/http_raw_capture.v1.json

TR: Repo manifest path'i:

    makpi51crawler/postgresql/databases/crawler_core/raw_fetch/http_raw_capture.v1.json

EN: Runtime raw body root:

    /srv/webcrawler/raw_fetch

TR: Runtime ham body kökü:

    /srv/webcrawler/raw_fetch

EN: Live PostgreSQL logical database name:

    logisticsearch_crawler

TR: Canlı PostgreSQL mantıksal database adı:

    logisticsearch_crawler

EN: These are three different things: manifest path, raw body storage root, and live database name.

TR: Bunlar üç farklı şeydir: manifest path, ham body storage kökü ve canlı database adı.

## 6. First crawler_core raw fetch flow / İlk crawler_core raw fetch akışı

EN: Step 1: crawler_core claims a URL from PostgreSQL.

TR: Adım 1: crawler_core PostgreSQL üzerinden bir URL claim eder.

EN: Step 2: crawler_core performs an HTTP request.

TR: Adım 2: crawler_core HTTP isteği yapar.

EN: Step 3: crawler_core writes the raw response body to `/srv/webcrawler/raw_fetch`.

TR: Adım 3: crawler_core ham response body içeriğini `/srv/webcrawler/raw_fetch` altına yazar.

EN: Step 4: crawler_core records metadata in PostgreSQL.

TR: Adım 4: crawler_core metadata bilgisini PostgreSQL içine kaydeder.

EN: Step 5: parse/runtime code later reads the raw body through the recorded path.

TR: Adım 5: parse/runtime kodu daha sonra kayıtlı path üzerinden ham body içeriğini okur.

## 7. Expected HTTP raw capture metadata / Beklenen HTTP raw capture metadata

EN: `http_raw_capture.v1.json` should describe fields such as:

    fetch_attempt_id
    url_id
    canonical_url
    requested_url
    final_url
    http_status
    content_type
    body_bytes
    body_sha256
    raw_storage_path
    started_at
    finished_at
    outcome
    error_class
    error_message

TR: `http_raw_capture.v1.json` şu gibi alanları açıklamalıdır:

    fetch_attempt_id
    url_id
    canonical_url
    requested_url
    final_url
    http_status
    content_type
    body_bytes
    body_sha256
    raw_storage_path
    started_at
    finished_at
    outcome
    error_class
    error_message

## 8. Expected frontier queue metadata / Beklenen frontier queue metadata

EN: `frontier_queue.v1.json` should describe fields such as:

    url_id
    canonical_url
    canonical_url_sha256
    state
    priority
    depth
    parent_url_id
    discovery_type
    last_seen_at
    last_enqueued_at
    last_success_at
    next_fetch_at
    lease_token
    lease_expires_at

TR: `frontier_queue.v1.json` şu gibi alanları açıklamalıdır:

    url_id
    canonical_url
    canonical_url_sha256
    state
    priority
    depth
    parent_url_id
    discovery_type
    last_seen_at
    last_enqueued_at
    last_success_at
    next_fetch_at
    lease_token
    lease_expires_at

## 9. Important R114 rule / Önemli R114 kuralı

EN: Rediscovery may update visibility metadata, but it must not blindly reset a successful URL's future `next_fetch_at` back to now.

TR: Rediscovery görünürlük metadata değerlerini güncelleyebilir; fakat başarılı olmuş bir URL'nin gelecekteki `next_fetch_at` değerini kör şekilde tekrar now değerine çekmemelidir.

EN: This rule belongs to crawler_core queue/revisit safety.

TR: Bu kural crawler_core queue/revisit güvenliğine aittir.

## 10. Forbidden misunderstandings / Yasak yanlış anlamalar

EN: Do not call `http_raw_capture.v1.json` the database name.

TR: `http_raw_capture.v1.json` dosyasına database adı deme.

EN: Do not call `frontier_queue.v1.json` the queue table itself.

TR: `frontier_queue.v1.json` dosyasına kuyruk tablosunun kendisi deme.

EN: Do not store raw body bytes inside GitHub.

TR: Ham body byte'larını GitHub içinde saklama.

EN: Do not use PostgreSQL internal engine folders as crawler application paths.

TR: PostgreSQL iç motor klasörlerini crawler uygulama path'i olarak kullanma.

EN: Do not recreate `runtime_changes/`, `frontier/`, `patch_manifests/`, or loose SQL folders under this topology.

TR: Bu topoloji altında `runtime_changes/`, `frontier/`, `patch_manifests/` veya gevşek SQL klasörleri oluşturma.
