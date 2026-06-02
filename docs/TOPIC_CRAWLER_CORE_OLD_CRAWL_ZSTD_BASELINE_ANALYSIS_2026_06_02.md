# Crawler Core Old ZSTD Baseline Analysis / Crawler Core Eski ZSTD Baseline Analizi

Marker: `KOD_BLOGU_104_OLD_CRAWL_ZSTD_BASELINE_DECISION_DOC`

Date: 2026-06-02  
Source gate: `KOD_BLOGU_103 / OLD_CRAWL_ZSTD_BASELINE_ANALYSIS_READONLY_R1`  
Canonical head: `b474f39e39b200bd7c78d62c573822796eadf3eb`  
Commit subject: `fix(crawler-core): disable zstd sidecar hot path`

---

## 1. Purpose / Amaç

### English

This document records the old crawler_core test baseline where crawler_core still produced `.fetch.json.zst` sidecar artefacts.

This baseline is intentionally captured before:

1. deleting old raw artefacts,
2. resetting crawler DB tables/counters,
3. running the new body-family-only crawler_core test,
4. comparing old ZSTD-sidecar behaviour against the new disabled-sidecar behaviour.

No runtime change is made by this document.

### Türkçe

Bu doküman, crawler_core katmanının hâlâ `.fetch.json.zst` sidecar artefact ürettiği eski crawler_core test baseline sonucunu kaydeder.

Bu baseline özellikle şu işlemlerden önce yazılı hale getirilmiştir:

1. eski raw artefact dosyalarını silmeden önce,
2. crawler DB tablo/sayaç resetinden önce,
3. yeni body-family-only crawler_core testinden önce,
4. eski ZSTD-sidecar davranışı ile yeni disabled-sidecar davranışı karşılaştırılmadan önce.

Bu doküman runtime değişikliği yapmaz.

---

## 2. Hard boundary / Sert sınır

### English

This document is evidence only.

It does not authorize:

- DB mutation,
- raw file deletion,
- crawler start,
- crawler stop,
- systemd mutation,
- live runtime copy,
- source URL fetch,
- compression_worker creation.

### Türkçe

Bu doküman yalnızca kanıt/evidence dokümanıdır.

Şunlara izin vermez:

- DB mutation,
- raw file deletion,
- crawler start,
- crawler stop,
- systemd mutation,
- live runtime copy,
- source URL fetch,
- compression_worker creation.

---

## 3. Runtime and safety status / Runtime ve güvenlik durumu

| Field | Value |
|---|---|
| Desktop HEAD | `b474f39e39b200bd7c78d62c573822796eadf3eb` |
| pi51c repo HEAD | `b474f39e39b200bd7c78d62c573822796eadf3eb` |
| pi51c repo status | clean |
| Live ZSTD-disable support SHA | `4c7fe9696b216a98d61db33482f382f5017a77273d837dcf0de2c0b817e3307f` |
| Live HTTP acquisition SHA | `d44788ada7312c2f5544eabe22ea5de898119aa001da04446b7bb7f60c2e6259` |
| Live browser page acquisition SHA | `e2f1302069bbdd12c51f6d9f6dcf8e55b6144d1ff21e9a6f0ecf66ac82eee8ef` |
| Live `__pycache__` count | `0` |
| Matching service active count | `0` |
| Matching service enabled count | `0` |
| Crawler process count | `0` |
| Browser process count | `0` |

---

## 4. Raw artefact root / Raw artefact kök dizini

| Field | Value |
|---|---|
| Raw root | `/srv/webcrawler/raw_fetch` |
| Raw root type | directory |
| Raw root mode | `2775` |
| Raw root owner | `makpi51` |
| Raw root group | `makpi51` |
| Baseline day bucket | `2026-05-31` |

### English

All old raw artefacts from this baseline are under:

`/srv/webcrawler/raw_fetch/2026/05/31/`

### Türkçe

Bu baseline içindeki tüm eski raw artefact dosyaları şu dizin altındadır:

`/srv/webcrawler/raw_fetch/2026/05/31/`

---

## 5. Raw artefact inventory / Raw artefact envanteri

| Artefact class | Count | Bytes | Min bytes | Max bytes | Average bytes |
|---|---:|---:|---:|---:|---:|
| `.body.bin` | `4505` | `501647936` | `0` | `12823930` | `111353.59` |
| `.fetch.json.zst` | `1928` | `112971063` | `1129` | `9980650` | `58594.95` |
| `.body.bin.zst` | `0` | `0` | `0` | `0` | `0.00` |
| `.fetch.json` | `0` | `0` | `0` | `0` | `0.00` |
| `.rendered.html` | `1` | `192031` | `192031` | `192031` | `192031.00` |
| `.raw_response_body.bin.zst` | `0` | `0` | `0` | `0` | `0.00` |
| other files | `1` | `266885` | n/a | n/a | n/a |
| total files | `6435` | `615077915` | n/a | n/a | n/a |

### English

Important interpretation:

- `.body.bin` is the hot raw body evidence family.
- `.fetch.json.zst` was produced by the old crawler_core sidecar behaviour.
- `.body.bin.zst` did not exist in the old run.
- plain `.fetch.json` did not exist in the old run.
- one rendered HTML file existed.
- one other file existed; observed evidence indicates a screenshot PNG artefact.

### Türkçe

Önemli yorum:

- `.body.bin`, sıcak raw body evidence ailesidir.
- `.fetch.json.zst`, eski crawler_core sidecar davranışı tarafından üretilmiştir.
- Eski koşuda `.body.bin.zst` yoktur.
- Eski koşuda plain `.fetch.json` yoktur.
- Bir adet rendered HTML dosyası vardır.
- Bir adet other dosya vardır; görülen evidence screenshot PNG artefact olduğunu göstermektedir.

---

## 6. Raw body family split / Raw body ailesi ayrımı

| Raw body family member | Count | Bytes | Average bytes | Median bytes | Purpose |
|---|---:|---:|---:|---:|---|
| URL `.body.bin` | `1927` | `473928373` | `245941.03` | `104260.00` | Main fetched page/API/file response body |
| Host robots `.body.bin` | `2578` | `27719563` | `10752.35` | `489.00` | Host-scoped robots policy evidence |
| Rendered HTML | `1` | `192031` | `192031.00` | `192031.00` | Browser-rendered DOM/HTML evidence |

### English

The old raw body family already proves that `BODY_BIN_ONLY` must not be interpreted as a single output file.

Correct interpretation:

- URL fetch may create `url_<url_id>_<timestamp>.body.bin`.
- robots fetch may create `host_<host_id>_robots_<timestamp>.body.bin`.
- browser-rendered acquisition may create `url_<url_id>_<timestamp>.rendered.html`.

### Türkçe

Eski raw body ailesi şunu açıkça gösterir: `BODY_BIN_ONLY`, tek output dosyası anlamına gelmez.

Doğru yorum:

- URL fetch `url_<url_id>_<timestamp>.body.bin` oluşturabilir.
- robots fetch `host_<host_id>_robots_<timestamp>.body.bin` oluşturabilir.
- browser-rendered acquisition `url_<url_id>_<timestamp>.rendered.html` oluşturabilir.

---

## 7. Time window / Zaman aralığı

| Source | First timestamp | Last timestamp |
|---|---|---|
| Raw file mtime range | `2026-05-31T06:42:38` | `2026-05-31T13:23:51` |
| DB `http_fetch.fetch_attempt.started_at` | `2026-05-31 06:42:37+02` | `2026-05-31 13:23:57+02` |
| DB `http_fetch.fetch_attempt.ended_at` | `2026-05-31 06:42:37+02` | `2026-05-31 13:23:57+02` |

### English

The old baseline run spans roughly 6 hours and 41 minutes by DB attempt timestamps.

### Türkçe

Eski baseline koşusu DB attempt timestamp değerlerine göre yaklaşık 6 saat 41 dakika sürmüştür.

---

## 8. Largest raw artefacts / En büyük raw artefact dosyaları

| Rank | Bytes | Artefact |
|---:|---:|---|
| 1 | `12823930` | `/srv/webcrawler/raw_fetch/2026/05/31/url_610_20260531T062611Z.body.bin` |
| 2 | `9980650` | `/srv/webcrawler/raw_fetch/2026/05/31/url_610_20260531T062611Z.fetch.json.zst` |
| 3 | `9251355` | `/srv/webcrawler/raw_fetch/2026/05/31/url_1314_20260531T074717Z.body.bin` |
| 4 | `8983074` | `/srv/webcrawler/raw_fetch/2026/05/31/url_89_20260531T052501Z.body.bin` |
| 5 | `8489698` | `/srv/webcrawler/raw_fetch/2026/05/31/url_1314_20260531T074717Z.fetch.json.zst` |
| 6 | `7926984` | `/srv/webcrawler/raw_fetch/2026/05/31/url_2110_20260531T091908Z.body.bin` |
| 7 | `6597091` | `/srv/webcrawler/raw_fetch/2026/05/31/url_2112_20260531T091837Z.body.bin` |
| 8 | `5841369` | `/srv/webcrawler/raw_fetch/2026/05/31/url_2808_20260531T103946Z.body.bin` |
| 9 | `5338604` | `/srv/webcrawler/raw_fetch/2026/05/31/url_1323_20260531T074857Z.body.bin` |
| 10 | `5331822` | repeated large URL/robots body artefacts observed around host/url `731`, `1015`, `1837`, `1838` |

---

## 9. ZSTD envelope readability / ZSTD envelope okunabilirliği

### English

The `.fetch.json.zst` samples were readable with `/usr/bin/zstd`.

Sample JSON heads showed fields such as:

- `body_bytes`,
- `body_sha256`,
- `canonical_url`,
- `compression`,
- `content_encoding`,
- `content_type`.

This confirms the sidecar is a structured compressed JSON envelope, but this baseline did not run a full payload-schema diff for every envelope.

### Türkçe

`.fetch.json.zst` örnekleri `/usr/bin/zstd` ile okunabilmiştir.

Örnek JSON başlangıçlarında şu alanlar görülmüştür:

- `body_bytes`,
- `body_sha256`,
- `canonical_url`,
- `compression`,
- `content_encoding`,
- `content_type`.

Bu durum sidecar dosyasının structured compressed JSON envelope olduğunu doğrular; fakat bu baseline her envelope için tam payload-schema diff yapmamıştır.

---

## 10. DB table inventory / DB tablo envanteri

| Table | Count |
|---|---:|
| `frontier.url` | `3047` |
| `frontier.host` | `1402` |
| `http_fetch.fetch_attempt` | `3056` |
| `seed.seed_url` | `3092` |
| `seed.source` | `1955` |
| `ops.webcrawler_runtime_control` | `1` |

---

## 11. Frontier and fetch outcomes / Frontier ve fetch sonuçları

### `frontier.url.state`

| State | Count |
|---|---:|
| `queued` | `1927` |
| `retry_wait` | `935` |
| `dead` | `185` |
| total | `3047` |
| touched candidates | `1120` |

### `http_fetch.fetch_attempt.outcome`

| Outcome | Count |
|---|---:|
| `success` | `1927` |
| `retryable_error` | `940` |
| `blocked_robots` | `184` |
| `network_error` | `4` |
| `permanent_error` | `1` |
| total | `3056` |

### English

The old baseline is not a clean “all-success” crawl. It contains a meaningful retry/blocked/dead distribution that must be preserved before reset.

### Türkçe

Eski baseline temiz “all-success” crawl değildir. Reset öncesinde korunması gereken anlamlı retry/blocked/dead dağılımı vardır.

---

## 12. DB path-column interpretation / DB path-column yorumu

| DB path surface | Count | Non-null | `.fetch.json.zst` refs | `.body.bin` refs |
|---|---:|---:|---:|---:|
| `http_fetch.fetch_attempt.body_storage_path` | `3056` | `1928` | `0` | `1927` |
| `http_fetch.robots_txt_cache.raw_storage_path` | `1402` | `1004` | `0` | `1004` |

### English

The DB path-column audit did not show `.fetch.json.zst` references in the checked DB path columns. The sidecar files existed on disk as raw evidence artefacts, while the DB body path references primarily pointed to `.body.bin`.

The one-count difference between non-null `body_storage_path=1928` and `.body.bin` references `1927` must be preserved for later targeted audit. It likely relates to browser-rendered/screenshot evidence, but this document does not make that conclusion final.

### Türkçe

DB path-column audit kontrol edilen DB path kolonlarında `.fetch.json.zst` referansı göstermemiştir. Sidecar dosyaları diskte raw evidence artefact olarak vardır; DB body path referansları esas olarak `.body.bin` dosyalarına işaret etmiştir.

`body_storage_path=1928` non-null değeri ile `.body.bin` referansı `1927` arasındaki bir adet fark daha sonra targeted audit için korunmalıdır. Bu fark browser-rendered/screenshot evidence ile ilişkili olabilir; fakat bu doküman bunu kesin hüküm olarak mühürlemez.

---

## 13. Journal signal summary / Journal sinyal özeti

| Signal | Count |
|---|---:|
| `Traceback` | `1` |
| `Exception ignored` | `1` |
| `fatal` | `0` |
| `critical` | `0` |
| `storage_pause` | `0` |
| `write_raw_fetch_json_zstd` | `0` |
| `.fetch.json.zst` | `0` |
| `runtime_exception_retry_wait` | `1212` |
| `robots_blocked` | `216` |
| `http_404` | `153` |
| `http_403` | `26` |
| `http_500` | `16` |
| `http_503` | `7` |

### English

Important interpretation:

- There were no `fatal` or `critical` journal signals.
- There were no `storage_pause` journal signals.
- There was one `Traceback` and one `Exception ignored`; these must be inspected before final performance conclusions.
- The high `runtime_exception_retry_wait` count must be compared against the new run.
- Journal did not directly show `.fetch.json.zst` text, even though disk inventory found `.fetch.json.zst` artefacts.

### Türkçe

Önemli yorum:

- Journal içinde `fatal` veya `critical` sinyali yoktur.
- Journal içinde `storage_pause` sinyali yoktur.
- Bir adet `Traceback` ve bir adet `Exception ignored` vardır; final performans yorumu öncesinde incelenmelidir.
- Yüksek `runtime_exception_retry_wait` sayısı yeni koşu ile karşılaştırılmalıdır.
- Journal doğrudan `.fetch.json.zst` metni göstermemiştir; buna rağmen disk envanteri `.fetch.json.zst` artefact dosyalarını bulmuştur.

---

## 14. Old baseline conclusions / Eski baseline sonuçları

### English

The old run proves these points:

1. Old crawler_core produced `.fetch.json.zst` sidecars.
2. Old crawler_core did not produce `.body.bin.zst`.
3. Old crawler_core did not produce plain `.fetch.json`.
4. The main storage consumer was `.body.bin`, not `.fetch.json.zst`.
5. `.fetch.json.zst` still had meaningful storage cost: `112971063` bytes.
6. URL raw body and robots raw body are separate raw body family members.
7. A browser-rendered/screenshot path existed in the old evidence set.
8. DB path columns mostly pointed to `.body.bin`; `.fetch.json.zst` existed as disk-side evidence.
9. The next test must compare old sidecar-on behaviour against new sidecar-disabled behaviour using the same reset-before-test discipline.

### Türkçe

Eski koşu şu noktaları kanıtlar:

1. Eski crawler_core `.fetch.json.zst` sidecar üretmiştir.
2. Eski crawler_core `.body.bin.zst` üretmemiştir.
3. Eski crawler_core plain `.fetch.json` üretmemiştir.
4. Ana storage tüketicisi `.body.bin` dosyalarıdır; `.fetch.json.zst` değildir.
5. Buna rağmen `.fetch.json.zst` anlamlı storage maliyetine sahiptir: `112971063` byte.
6. URL raw body ve robots raw body ayrı raw body family üyeleridir.
7. Eski evidence set içinde browser-rendered/screenshot path vardır.
8. DB path kolonları çoğunlukla `.body.bin` dosyalarına işaret etmiştir; `.fetch.json.zst` disk-side evidence olarak vardır.
9. Yeni testte eski sidecar-on davranış ile yeni sidecar-disabled davranış aynı reset-before-test disipliniyle karşılaştırılmalıdır.

---

## 15. Next gate plan / Sonraki gate planı

### English

After this document is audited and committed:

1. Run a read-only audit of this document.
2. Commit/push this baseline document.
3. Sync pi51c repo.
4. Prepare cleanup/reset plan.
5. Reset old raw artefacts and crawler DB counters in one controlled cleanup gate.
6. Run the new crawler_core test with `.fetch.json.zst` disabled.
7. Compare old and new:
   - file counts,
   - bytes,
   - duration,
   - success/retry/error distribution,
   - journal signals,
   - DB state distribution,
   - raw evidence shape.

### Türkçe

Bu doküman audit edilip commit edildikten sonra:

1. Bu dokümanın read-only audit’i çalıştırılacak.
2. Baseline dokümanı commit/push yapılacak.
3. pi51c repo senkronlanacak.
4. Cleanup/reset plan hazırlanacak.
5. Eski raw artefact dosyaları ve crawler DB sayaçları tek kontrollü cleanup gate ile resetlenecek.
6. `.fetch.json.zst` disabled yeni crawler_core testi çalıştırılacak.
7. Eski ve yeni koşu karşılaştırılacak:
   - dosya sayıları,
   - byte miktarları,
   - süre,
   - success/retry/error dağılımı,
   - journal sinyalleri,
   - DB state dağılımı,
   - raw evidence şekli.

---

## 16. Current next gate / Güncel sonraki gate

`KOD_BLOGU_105 / OLD_CRAWL_ZSTD_BASELINE_DECISION_DOC_AUDIT_READONLY_R1`
---

## 17. Exact baseline duration and comparison rule / Exact baseline süresi ve karşılaştırma kuralı

Marker: `KOD_BLOGU_104B_EXACT_DURATION_AND_PARALLEL_WORK_TRUTH`

### English

The old `.fetch.json.zst` sidecar-on crawler_core baseline duration must be recorded exactly because the next crawler_core test will run with `.fetch.json.zst` disabled and the two runs will be compared.

Primary comparison duration:

| Metric | Start | End | Exact duration |
|---|---|---|---|
| DB attempt window | `2026-05-31 06:42:37.875549+02` | `2026-05-31 13:23:57.270254+02` | `6h 41m 19.395s` |

Supporting artefact duration:

| Metric | Start | End | Exact duration |
|---|---|---|---|
| Raw file mtime window | `2026-05-31T06:42:38.0792413130` | `2026-05-31T13:23:51.4040021720` | `6h 41m 13.325s` |

Interpretation:

- The primary old-run duration for performance comparison is `6h 41m 19.395s`.
- The raw-file mtime duration is supporting evidence only.
- The next sidecar-disabled run must record the same two duration classes.
- Final comparison must include:
  - duration,
  - raw file count,
  - raw total bytes,
  - `.body.bin` bytes,
  - `.fetch.json.zst` count and bytes,
  - success/retry/blocked/dead distributions,
  - journal signals,
  - DB state/outcome distribution.

### Türkçe

Eski `.fetch.json.zst` sidecar-on crawler_core baseline süresi exact olarak kaydedilmelidir; çünkü bir sonraki crawler_core testi `.fetch.json.zst` disabled halde çalışacak ve iki koşu karşılaştırılacaktır.

Ana karşılaştırma süresi:

| Metrik | Başlangıç | Bitiş | Exact süre |
|---|---|---|---|
| DB attempt window | `2026-05-31 06:42:37.875549+02` | `2026-05-31 13:23:57.270254+02` | `6 saat 41 dakika 19.395 saniye` |

Destekleyici artefact süresi:

| Metrik | Başlangıç | Bitiş | Exact süre |
|---|---|---|---|
| Raw file mtime window | `2026-05-31T06:42:38.0792413130` | `2026-05-31T13:23:51.4040021720` | `6 saat 41 dakika 13.325 saniye` |

Yorum:

- Performans karşılaştırması için ana eski-koşu süresi `6 saat 41 dakika 19.395 saniye` olarak alınacaktır.
- Raw-file mtime süresi yalnızca destekleyici evidence değeridir.
- Sonraki sidecar-disabled koşu aynı iki süre sınıfını kaydetmelidir.
- Final karşılaştırma şunları içermelidir:
  - süre,
  - raw dosya sayısı,
  - raw toplam byte,
  - `.body.bin` byte,
  - `.fetch.json.zst` sayı ve byte,
  - success/retry/blocked/dead dağılımları,
  - journal sinyalleri,
  - DB state/outcome dağılımı.

---



### Turkish duration wording clarity / Türkçe süre yazımı netliği

Marker: `KOD_BLOGU_104C_TURKISH_DURATION_CLARITY_TRUTH`

The Turkish duration wording intentionally uses full words instead of compact abbreviations.

Türkçe süre yazımı özellikle kısaltma yerine açık kelimelerle yapılır:

- `6 saat 41 dakika 19.395 saniye`
- `6 saat 41 dakika 13.325 saniye`

This avoids ambiguity before the sidecar-disabled performance comparison.

Bu tercih, sidecar-disabled performans karşılaştırması öncesinde süre bilgisinin yanlış yorumlanmasını engeller.

---

## 18. Parallel work rule while pi51c test runs / pi51c testi çalışırken paralel çalışma kuralı

### English

During the next long crawler_core test:

- pi51c may continue the crawler_core test independently.
- Ubuntu Desktop and GitHub work may continue in parallel.
- pi51c is excluded from repo/live sync during the active test.
- No live runtime copy to pi51c is allowed during the active test.
- No pi51c repo reset is allowed during the active test.
- No DB/raw reset is allowed during the active test.
- After the test ends, all four surfaces will be reconciled and synchronized deliberately:
  - Ubuntu Desktop,
  - GitHub,
  - pi51c repo,
  - pi51c live runtime.

### Türkçe

Bir sonraki uzun crawler_core testi sırasında:

- pi51c crawler_core testini bağımsız olarak sürdürebilir.
- Ubuntu Desktop ve GitHub üzerinde paralel çalışma devam edebilir.
- Aktif test sırasında pi51c repo/live sync dışında tutulur.
- Aktif test sırasında pi51c live runtime kopyası yapılmaz.
- Aktif test sırasında pi51c repo reset yapılmaz.
- Aktif test sırasında DB/raw reset yapılmaz.
- Test bittikten sonra dört yüzey bilinçli ve kontrollü şekilde tekrar uzlaştırılıp senkronlanır:
  - Ubuntu Desktop,
  - GitHub,
  - pi51c repo,
  - pi51c live runtime.

