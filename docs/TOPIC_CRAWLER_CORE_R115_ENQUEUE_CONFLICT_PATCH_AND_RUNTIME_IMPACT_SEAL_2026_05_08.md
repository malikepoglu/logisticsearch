# R115 enqueue conflict patch and runtime impact seal / R115 enqueue conflict patch ve runtime etki mührü

Patch time / Yama zamanı: 2026-05-08T03:01:53+02:00

## 1. EN: Scope

This document seals the R115 crawler_core enqueue conflict preservation work.

The live PostgreSQL function `frontier.enqueue_discovered_url` in logical database `logisticsearch_crawler` was patched and sealed.

The repository topology remains lean PostgreSQL + JSON/JSONB representation:

- no top-level `sql/`
- no `makpi51crawler/sql/`
- no `patch_manifests/`
- no `runtime_changes/`
- no raw body bytes in GitHub

## 1. TR: Kapsam

Bu belge R115 crawler_core enqueue conflict koruma çalışmasını mühürler.

Canlı PostgreSQL mantıksal veritabanı `logisticsearch_crawler` içindeki `frontier.enqueue_discovered_url` fonksiyonu yamalanmış ve mühürlenmiştir.

Repo topolojisi yalın PostgreSQL + JSON/JSONB temsil modelinde kalır:

- top-level `sql/` yok
- `makpi51crawler/sql/` yok
- `patch_manifests/` yok
- `runtime_changes/` yok
- GitHub içinde raw body byte yok

## 2. EN: DB function seal

Final live DB function:

- database: `logisticsearch_crawler`
- schema: `frontier`
- function: `enqueue_discovered_url`
- final md5: `1b629249c2182f5e2d499567f6a3539f`
- final chars: `6454`
- owner: `postgres`
- runtime execute role: `makpi51`
- `makpi51` EXECUTE privilege: preserved

Previous md5 before patch:

- `d6b028788dff6ebb1dc4b2cf5ec6a052`

## 2. TR: DB function mührü

Final canlı DB fonksiyonu:

- veritabanı: `logisticsearch_crawler`
- schema: `frontier`
- fonksiyon: `enqueue_discovered_url`
- final md5: `1b629249c2182f5e2d499567f6a3539f`
- final chars: `6454`
- owner: `postgres`
- runtime execute role: `makpi51`
- `makpi51` EXECUTE yetkisi: korundu

Yama öncesi md5:

- `d6b028788dff6ebb1dc4b2cf5ec6a052`

## 3. EN: Conflict preservation policy

The patched conflict branch preserves durable crawl scheduling truth.

Required invariant:

- Do not overwrite `next_fetch_at` for `leased` rows.
- Do not overwrite `next_fetch_at` for `parse_pending` rows.
- Do not overwrite retry_wait backoff `next_fetch_at` or collapse `retry_wait` to `queued`.
- Do not overwrite future `next_fetch_at` for successful queued rows.
- New URL inserts must remain immediately crawlable.
- Rediscovery may update `last_seen_at` as observation evidence.
- PostgreSQL columns remain durable truth.
- `url_metadata` remains lightweight context only.

## 3. TR: Conflict koruma politikası

Yamalanmış conflict branch dayanıklı crawl scheduling doğrusunu korur.

Zorunlu invariant:

- `leased` satırlarda `next_fetch_at` ezilmez.
- `parse_pending` satırlarda `next_fetch_at` ezilmez.
- `retry_wait` backoff `next_fetch_at` ezilmez ve `retry_wait` durumu `queued` durumuna çökertilmez.
- Başarılı `queued` satırlarda gelecekteki `next_fetch_at` ezilmez.
- Yeni URL insert satırları hemen crawl edilebilir kalır.
- Rediscovery `last_seen_at` değerini gözlem kanıtı olarak güncelleyebilir.
- PostgreSQL kolonları dayanıklı doğru olmaya devam eder.
- `url_metadata` yalnızca hafif bağlamdır.

## 4. EN: Runtime impact seal

R115_R7C sealed that the DB-only patch is runtime-signature compatible.

Runtime facts:

- correct Python helper surface: `makpi51crawler/python_live_runtime/logisticsearch1_1_1_7_discovery_gateway.py`
- not the old false-positive target: `logisticsearch1_1_1_3_frontier_gateway.py`
- parse runtime call surface: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_6_parse_runtime.py`
- DB function signature and return contract stayed compatible
- corrected AST audit including keyword-only arguments passed
- parse runtime has one AST enqueue call with all required keywords
- No immediate Python runtime patch is required for R6.

## 4. TR: Runtime etki mührü

R115_R7C, DB-only yamanın runtime signature ile uyumlu olduğunu mühürledi.

Runtime gerçekleri:

- doğru Python helper yüzeyi: `makpi51crawler/python_live_runtime/logisticsearch1_1_1_7_discovery_gateway.py`
- eski false-positive hedef değil: `logisticsearch1_1_1_3_frontier_gateway.py`
- parse runtime çağrı yüzeyi: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_6_parse_runtime.py`
- DB function signature ve return contract uyumlu kaldı
- keyword-only argümanları da kapsayan düzeltilmiş AST denetimi geçti
- parse runtime içinde gerekli tüm keywordleri taşıyan tek AST enqueue çağrısı var
- R6 için hemen Python runtime patch gerekmez

## 5. EN: Deferred work

`url_metadata` / `crawler_url_metadata.v1` runtime application has not started.

Current sealed state:

- Python code reference count for `url_metadata` / `crawler_url_metadata.v1` / `crawl_map`: 0
- DB `crawler_url_metadata.v1` row count: 0

Therefore, crawl-map runtime metadata application is separate R8-or-later work.

Existing successful-due queued rows are data repair scope, not R7 runtime patch scope.

## 5. TR: Ertelenen iş

`url_metadata` / `crawler_url_metadata.v1` runtime uygulaması başlamadı.

Güncel mühürlü durum:

- Python code reference count for `url_metadata` / `crawler_url_metadata.v1` / `crawl_map`: 0
- DB `crawler_url_metadata.v1` row count: 0

Bu yüzden crawl-map runtime metadata uygulaması ayrı bir R8-or-later işidir.

Mevcut successful-due queued satırlar data repair kapsamıdır; R7 runtime patch kapsamı değildir.

## 6. EN: Safety seal

During R6/R7:

- service stayed disabled/inactive
- crawler process count stayed 0
- no systemd mutation
- no crawler start
- no repo SQL resurrection
- no live filesystem mutation after the intended PostgreSQL subtree sync
- temporary DB backup/apply artifacts were cleaned after seal

## 6. TR: Güvenlik mührü

R6/R7 boyunca:

- service disabled/inactive kaldı
- crawler process count 0 kaldı
- systemd mutation yok
- crawler start yok
- repo SQL resurrection yok
- planlı PostgreSQL subtree sync sonrası live filesystem mutation yok
- geçici DB backup/apply artefactları mühür sonrası temizlendi

## 7. EN: Next decision point

Recommended next order:

1. R115_R8B validate this documentation seal.
2. R115_R8C commit/push documentation seal.
3. R115_R8D post-push seal.
4. Then choose the next controlled line:
   - data repair plan for existing successful-due queued rows, or
   - `crawler_url_metadata.v1` runtime application plan.

## 7. TR: Sonraki karar noktası

Önerilen sonraki sıra:

1. R115_R8B bu dokümantasyon mührünü doğrula.
2. R115_R8C dokümantasyon mührünü commit/push yap.
3. R115_R8D post-push seal yap.
4. Sonra sonraki kontrollü hattı seç:
   - mevcut successful-due queued satırlar için data repair plan, veya
   - `crawler_url_metadata.v1` runtime uygulama planı.
