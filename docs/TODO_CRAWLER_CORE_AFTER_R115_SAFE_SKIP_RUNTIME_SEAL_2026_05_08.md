# TODO After R115 Safe-Skip Runtime Seal / R115 Safe-Skip Runtime Mührü Sonrası TODO

## 1. Sealed / Mühürlendi

R115 metadata parent-conflict safe-skip runtime line is sealed by evidence.

Confirmed:

- Commit `f9ce0b882674f37b86bda402719bb652a9c70a7a`
- Safe-skip patch exists in pi51c live runtime.
- URL75 direct helper metadata write works.
- URL76 controlled runtime smoke passed.
- URL77 controlled runtime smoke passed.
- `metadata_degraded_count=0` in both real runtime smokes.
- `metadata_skipped_count=16` in both real runtime smokes.
- Service remained disabled/inactive.
- Exact crawler process count remained 0.
- No SQL file was added.
- No DB schema change was required.

## 2. Immediate Next Work / Hemen Sonraki İş

Preferred next sequence:

1. Validate this docs patch locally.
2. Stage and commit only the documentation files.
3. Push to GitHub.
4. Optionally sync pi51c repo for documentation parity.
5. Continue crawler_core with another controlled one-shot run only if needed.

## 3. Do Not Do Yet / Henüz Yapma

Do not enable long-running systemd loop yet.

Do not start broad crawling yet.

Do not remove the metadata parent guard.

Do not move heavy ranking, enrichment, or geocoding into Crawler_Core.

Do not introduce Pydantic dependency into runtime before a documented dependency/version/runtime-cost evaluation.

## 4. Architecture Follow-Up / Mimari Takip

Create a separate design note for the staged data model:

- Crawler_Core on Pi 5:
  - raw extraction
  - raw HTML/JSON/body storage
  - fetch metadata
  - robots/fetch/parse/discovery evidence
  - lightweight metadata
  - raw OSM/location clues and coordinates when already visible in source data

- Parse_Core on Pi 5:
  - filtering
  - pre-ranking
  - taxonomy keyword mapping
  - light structured validation
  - use raw location clues collected by Crawler_Core

- Desktop_Import on Ubuntu Desktop:
  - master data
  - enrichment
  - stricter validation
  - OSM geocoding and location normalization
  - search-ready output

Track processing stages:

- `STAGE_RAW`
- `STAGE_PARSED`
- `STAGE_IMPORTED`
- `STAGE_READY`

## 5. Current Crawler_Core Runtime Continuation / Mevcut Crawler_Core Devamı

Current due queue remains available.

Known recent successful runtime rows:

- URL64: `https://fiata.org/directory/`
- URL75: `https://fiata.org/directory/ao/`
- URL76: `https://fiata.org/directory/al/`
- URL77: `https://fiata.org/directory/ae/`

Next controlled runtime candidate should be selected by read-only preflight, not assumed manually.

## R29A validation terminology bridge / R29A doğrulama terim köprüsü

EN: `SAFE_SKIP_PATCH_RUNTIME_STABILITY` is the short machine-readable seal label for the R115/R26 safe-skip runtime line after two controlled one-shot crawler_core runs.
TR: `SAFE_SKIP_PATCH_RUNTIME_STABILITY`, iki kontrollü tek-seferlik crawler_core çalışması sonrası R115/R26 safe-skip runtime hattının kısa makine-okunur mühür etiketidir.

EN: OSM/location clues may be collected during raw crawling for later Parse_Core use, but heavy geocoding and location normalization must stay in Desktop_Import.
TR: OSM/location clues ham crawl sırasında Parse_Core'un daha sonra kullanması için toplanabilir; heavy geocoding ve lokasyon normalizasyonu Desktop_Import tarafında kalmalıdır.
