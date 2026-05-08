# R115 Metadata Safe-Skip Runtime Seal / R115 Metadata Safe-Skip Runtime Mührü

## 1. Summary / Özet

EN: This document seals the R115 crawler_core metadata safe-skip runtime line.

TR: Bu belge R115 crawler_core metadata safe-skip runtime hattını mühürler.

The safe-skip patch was committed as:

- Commit: `f9ce0b882674f37b86bda402719bb652a9c70a7a`
- Subject: `fix(crawler-core): classify metadata parent conflicts as skips`
- Parent: `4bac283a37c641c54987c31e879b97b89c966214`

The patch changed exactly two Python runtime files:

1. `makpi51crawler/python_live_runtime/logisticsearch1_1_1_3_frontier_gateway.py`
2. `makpi51crawler/python_live_runtime/logisticsearch1_1_2_6_parse_runtime.py`

No SQL file was added. No DB schema change was required. The parent guard was not removed.

## 2. Problem / Problem

EN: Before this patch, rediscovered existing URL rows could be classified as `metadata_degraded` when the `crawl_map` parent guard intentionally blocked metadata writes.

TR: Bu patch öncesinde, yeniden keşfedilen mevcut URL satırları için `crawl_map` parent guard metadata yazımını bilerek engellediğinde sonuç `metadata_degraded` gibi görünebiliyordu.

That was misleading because the helper itself was not broken. The guard was protecting against writing wrong crawl context onto unrelated or pre-existing rows.

## 3. Decision / Karar

EN: Parent-conflict guard failures are safe skips.

TR: Parent-conflict guard başarısızlıkları güvenli skip olarak sınıflandırılır.

Accepted behavior:

- `metadata_updated=false`
- `metadata_degraded=false`
- `metadata_skipped=true`
- `skip_class=parent_conflict_guard_skipped`

Rejected behavior:

- Removing the parent guard blindly.
- Writing misleading `crawl_map` context onto unrelated existing rows.
- Copying durable PostgreSQL truth columns into `url_metadata`.

True degraded cases remain degraded:

- Empty metadata patch.
- Target URL row missing.
- No row returned after the parent guard precheck has already passed.

## 4. Runtime Evidence / Runtime Kanıtı

### 4.1 Direct helper smoke / Doğrudan helper smoke

URL75 direct helper smoke confirmed the helper can write metadata when the safe parent context is used.

- URL: `https://fiata.org/directory/ao/`
- URL ID: `75`
- Parent/root URL ID: `64`
- Result: metadata update succeeded.
- `schema_version`: `crawler_url_metadata.v1`
- `crawl_map.root_url_id`: `64`
- `crawl_map.branch_role`: `controlled_direct_helper_smoke`
- `crawl_map.branch_label`: `html_link`
- `crawl_map.crawl_path_hint`: `r115_r26g_direct_helper_smoke_url75_parent64`

### 4.2 First controlled runtime smoke / İlk kontrollü runtime smoke

R26U confirmed the safe-skip behavior in real runtime flow.

- Claimed URL ID: `76`
- URL: `https://fiata.org/directory/al/`
- HTTP status: `200`
- `metadata_updated_count=0`
- `metadata_degraded_count=0`
- `metadata_skipped_count=16`
- Storage pause: `false`
- Processed output root: `/srv/data`

### 4.3 Second controlled runtime smoke / İkinci kontrollü runtime smoke

R26Y confirmed stable repeat behavior.

- Claimed URL ID: `77`
- URL: `https://fiata.org/directory/ae/`
- HTTP status: `200`
- `metadata_updated_count=0`
- `metadata_degraded_count=0`
- `metadata_skipped_count=16`
- Storage pause: `false`
- Processed output root: `/srv/data`

## 5. Synchronization Seal / Senkron Mührü

The patch was synchronized through:

1. Ubuntu Desktop canonical repo.
2. GitHub `origin/main`.
3. pi51c `/logisticsearch/repo`.
4. pi51c live runtime `/logisticsearch/makpi51crawler`.

Final expected runtime state:

- Ubuntu Desktop HEAD: `f9ce0b882674f37b86bda402719bb652a9c70a7a`
- GitHub origin/main: `f9ce0b882674f37b86bda402719bb652a9c70a7a`
- pi51c repo HEAD: `f9ce0b882674f37b86bda402719bb652a9c70a7a`
- pi51c live runtime aligned with repo Python runtime.
- Service state: disabled/inactive.
- Exact crawler process count: 0.
- Live `__pycache__` and `.pyc` count: 0.

## 6. Current Queue State / Mevcut Queue Durumu

As of the R27 decision pack:

- Total URL rows: 45
- Queued rows: 45
- Due queued rows: 32
- Successful due rows: 0
- Successful future rows: 13
- Leased rows: 0
- Parse pending rows: 0
- Metadata v1 rows: 1
- Crawl map rows: 1
- Unexpected metadata rows: 0

Known successful evidence rows:

- URL64: `https://fiata.org/directory/`, success count 2, HTTP 200
- URL75: `https://fiata.org/directory/ao/`, success count 1, HTTP 200, direct metadata evidence present
- URL76: `https://fiata.org/directory/al/`, success count 1, HTTP 200
- URL77: `https://fiata.org/directory/ae/`, success count 1, HTTP 200

## 7. Design Boundary / Tasarım Sınırı

EN: Crawler_Core remains focused on raw fetch, crawl evidence, runtime safety, and lightweight metadata.

TR: Crawler_Core ham fetch, crawl kanıtı, runtime güvenliği ve hafif metadata toplamaya odaklı kalır.

This line does not move into ranking, heavy enrichment, or Desktop_Import work.

Future architecture notes to track separately:

1. Crawler_Core on Pi 5 should collect raw content and lightweight metadata.
2. Raw crawling should preserve OSM/location clues and coordinates when they are already available in page content or metadata.
3. Heavy geocoding, address normalization, OSM enrichment, and master-data construction should stay on Ubuntu Desktop.
4. Parse_Core can use collected raw location clues later.
5. Pydantic should be evaluated as a lightweight validation helper, not as the durable source of truth.
6. PostgreSQL and JSON/JSONB remain durable runtime truth.
7. Processing stages should be considered explicitly:
   - `STAGE_RAW`
   - `STAGE_PARSED`
   - `STAGE_IMPORTED`
   - `STAGE_READY`

## 8. Next Safe Direction / Sonraki Güvenli Yön

Recommended next action after this seal:

1. Commit and push this documentation seal.
2. Sync pi51c repo if documentation sync is desired.
3. Continue crawler_core with controlled one-shot confidence, not systemd loop yet.
4. Keep systemd loop disabled until more one-shot runtime evidence is collected and documented.
5. Track Pydantic, OSM raw clues, and processing-stage model as a separate architecture/design note.
