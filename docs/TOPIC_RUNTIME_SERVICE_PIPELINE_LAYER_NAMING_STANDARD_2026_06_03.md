
# Runtime Service Pipeline Layer Naming Standard / Runtime Service Pipeline Katman İsim Standardı

Date / Tarih: 2026-06-03

Source gate / Kaynak gate: `KOD_BLOGU_144 / PIPELINE_LAYER_NAMING_AND_DOC_STANDARD_AUDIT_READONLY_R1`

Canonical head / Kanonik head: `87913f44caba35d99b56506d32e9237370e2dbfe`

## 1. Purpose / Amaç

EN: This document freezes the canonical layer, worker, service, and pipeline naming standard for the next LogisticSearch runtime refactor. It does not move files, change service units, change database state, touch raw evidence, start crawlers, or sync pi51c.

TR: Bu belge LogisticSearch runtime refactor için kanonik katman, worker, service ve pipeline isim standardını mühürler. Dosya taşımaz, service unit değiştirmez, veritabanı durumunu değiştirmez, raw evidence’a dokunmaz, crawler başlatmaz ve pi51c senkronu yapmaz.

## 2. Core naming rule / Core isim kuralı

EN: `*_core` names describe architectural layers. `*_worker` names describe worker/service pipeline surfaces.

TR: `*_core` adları mimari katmanları tanımlar. `*_worker` adları worker/service pipeline yüzeylerini tanımlar.

EN: This is not a multi-thread naming model. The correct mental model is worker/service pipeline.

TR: Bu multi-thread isimlendirme modeli değildir. Doğru zihinsel model worker/service pipeline modelidir.

## 3. Canonical layer names / Kanonik katman adları

| Order | Canonical layer | Turkish meaning | English meaning | Status |
|---:|---|---|---|---|
| 1 | `preparation_core` | hazırlık katmanı | source/startpoint/seed preparation layer | canonical |
| 2 | `crawler_core` | crawler çekirdek katmanı | crawling, robots, fetch, raw evidence acquisition layer | canonical |
| 3 | `process_core` | işleme katmanı | content extraction and processing layer | canonical |
| 4 | `ai_rank_core` | AI sıralama katmanı | taxonomy, semantic, embedding, neural ranking, quality scoring layer | canonical |
| 5 | `port_core` | kontrollü veri taşıma/port katmanı | controlled data porting, handoff, packaging, queue-to-search/application transfer layer | canonical |
| 6 | `compression_core` | sıkıştırma katmanı | compression, decompression, checksum, verification layer | canonical |

## 4. Canonical worker/service names / Kanonik worker/service adları

| Order | Canonical worker/service | Primary layer | Role |
|---:|---|---|---|
| 1 | `preparation_worker` | `preparation_core` | prepares startpoints, source families, seed candidates, manifests, and future queue inputs |
| 2 | `crawler_worker` | `crawler_core` | claims URLs, applies robots policy, fetches URL/robots/browser fallback raw artefacts, and writes raw evidence |
| 3 | `process_worker` | `process_core` | processes raw payloads, extracts canonical text, entities, links, language signals, and parse/process evidence |
| 4 | `ai_rank_worker` | `ai_rank_core` | serves process/ranking needs: taxonomy match, semantic embedding, neural ranking, quality score, duplicate/entity resolution |
| 5 | `port_worker` | `port_core` | prepares and ports controlled clean data from crawler-side storage toward search/application-side storage |
| 6 | `compression_worker` | `compression_core` | compresses/decompresses/verifies raw artefacts and fetch envelopes after explicit downstream directive |

## 5. Pipeline dependency rule / Pipeline bağımlılık kuralı

EN:
- `ai_rank_worker` serves `process_worker`.
- `compression_worker` serves `port_worker`.
- `compression_worker` must not be part of the `crawler_worker` hot path.
- `crawler_worker` must not produce `.fetch.json.zst`, `.fetch.json`, or `.body.bin.zst` in the hot path.
- `process_worker` normally consumes raw hot payloads, not normal-path `.zst` artefacts.
- `port_worker` gives the controlled directive for later compression and search/application handoff.

TR:
- `ai_rank_worker`, `process_worker` hizmetinde çalışır.
- `compression_worker`, `port_worker` hizmetinde çalışır.
- `compression_worker`, `crawler_worker` sıcak hattının parçası olmamalıdır.
- `crawler_worker` sıcak hatta `.fetch.json.zst`, `.fetch.json` veya `.body.bin.zst` üretmemelidir.
- `process_worker` normalde sıcak ham payload ile çalışır, normal hatta `.zst` artefact tüketmez.
- `port_worker` daha sonraki sıkıştırma ve search/application handoff için kontrollü direktifi verir.

## 6. Directory naming standard / Dizin isim standardı

EN: Future worker/service directories should use canonical `*_worker` names. Existing active directories are not blindly renamed; each rename requires a separate gated patch, import audit, service audit, live sync, and short health test.

TR: Gelecekteki worker/service dizinleri kanonik `*_worker` adlarını kullanmalıdır. Mevcut aktif dizinler körlemesine yeniden adlandırılmaz; her yeniden adlandırma ayrı gated patch, import audit, service audit, live sync ve kısa health test gerektirir.

| Concept | Current / legacy name | Canonical future name | Rule |
|---|---|---|---|
| crawler runtime worker directory | `crawler_worker` | `crawler_worker` | rename later only after explicit import/service gate |
| parse worker directory | `parse_core_worker` | `process_worker` | `parse_core` name is deprecated in docs and future directory naming |
| AI ranking worker directory | `ai_ranking_worker` / `ranking_neural_worker` | `ai_rank_worker` | old names are deprecated |
| desktop import worker directory | `desktop_import_worker` | `port_worker` | old name is deprecated |
| compression worker directory | `compression_worker` | `compression_worker` | stays canonical |
| startpoint/source preparation directory | none / ad hoc source-seed docs | `preparation_worker` | create only when real code moves there |

## 7. Service naming standard / Service isim standardı

EN: Future service names should use worker names, not internal historical module names.

TR: Gelecekteki service adları worker adlarını kullanmalıdır; tarihsel internal modül adları kullanılmamalıdır.

| Worker | Future service name |
|---|---|
| `preparation_worker` | `logisticsearch-preparation-worker.service` |
| `crawler_worker` | `logisticsearch-crawler-worker.service` |
| `process_worker` | `logisticsearch-process-worker.service` |
| `ai_rank_worker` | `logisticsearch-ai-rank-worker.service` |
| `port_worker` | `logisticsearch-port-worker.service` |
| `compression_worker` | `logisticsearch-compression-worker.service` |

EN: Current `logisticsearch-webcrawler.service` remains an active historical service surface until an explicit service rename gate is executed.

TR: Mevcut `logisticsearch-webcrawler.service`, açık bir service rename gate uygulanana kadar aktif tarihsel service yüzeyi olarak kalır.

## 8. Deprecated names / Kullanımdan kaldırılan adlar

| Deprecated name | Replacement |
|---|---|
| `parse_core` | `process_core` |
| `parse_core_worker` | `process_worker` |
| `ai_ranking_worker` | `ai_rank_worker` |
| `ranking_neural_worker` | `ai_rank_worker` |
| `desktop_import` | `port_core` or `port_worker` depending on context |
| `desktop_import_worker` | `port_worker` |
| `crawler_worker` | `crawler_worker` later, after explicit migration gate |

EN: `port_core` means controlled data porting/handoff. It does not mean a network port, harbor, TCP port, UDP port, or socket listener.

TR: `port_core` kontrollü veri taşıma/handoff anlamındadır. Network port, liman, TCP port, UDP port veya socket listener anlamına gelmez.

## 9. Current active exception / Güncel aktif istisna

EN: The current live runtime still uses `python_live_runtime/crawler_worker/` because the last safe refactor isolated active crawler implementation there. This is a temporary active directory name, not the final canonical worker/service pipeline name.

TR: Güncel live runtime hâlâ `python_live_runtime/crawler_worker/` kullanır; çünkü son güvenli refactor aktif crawler implementation’ı oraya izole etti. Bu geçici aktif dizin adıdır; nihai kanonik worker/service pipeline adı değildir.

## 10. Current reachable boundary files / Güncel reachable sınır dosyaları

EN: The following files are conceptually outside pure crawler ownership but currently reachable from the active runtime graph, so they must not be moved blindly:

- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_2_6_parse_runtime.py`
- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_2_6_1_taxonomy_runtime.py`
- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_1_6_preranking_gateway.py`

TR: Aşağıdaki dosyalar kavramsal olarak saf crawler sahipliğinin dışında dursa da şu anda aktif runtime grafiğinden reachable durumdadır; bu yüzden körlemesine taşınmamalıdır:

- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_2_6_parse_runtime.py`
- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_2_6_1_taxonomy_runtime.py`
- `makpi51crawler/python_live_runtime/crawler_worker/logisticsearch1_1_1_6_preranking_gateway.py`

## 11. Runtime language surface rule / Runtime dil yüzeyi kuralı

EN:
- Python remains the orchestration, DB/state/queue/verification/control language.
- C++ is preferred for performance-heavy compression, inference, parsing, and byte-heavy operations when justified.
- C remains separate for low-level deterministic helpers and ABI-stable boundaries.
- `c_live_runtime/` and `cpp_live_runtime/` stay separate.
- `native_live_runtime/` and `c_cpp_live_runtime/` remain forbidden mixed surfaces.

TR:
- Python orkestrasyon, DB/state/queue/verification/control dili olarak kalır.
- C++, gerekli olduğunda performans ağırlıklı compression, inference, parsing ve byte-heavy işler için tercih edilir.
- C, low-level deterministic helper ve ABI-stable sınırlar için ayrı kalır.
- `c_live_runtime/` ve `cpp_live_runtime/` ayrı kalır.
- `native_live_runtime/` ve `c_cpp_live_runtime/` karışık yüzeyleri yasak kalır.

## 12. Next safe sequence / Sonraki güvenli sıra

1. Commit this documentation standard.
2. Update README indexes with this standard.
3. Plan worker directory rename gates separately.
4. Patch service names separately.
5. Run import/help/service read-only audit after every rename.
6. Sync pi51c only through explicit controlled sync gate.
7. Continue Python file filtering after naming standard is sealed.

## 13. Forbidden actions / Yasak eylemler

- no blind `mv`
- no blind deletion
- no code move in documentation gate
- no service rename without separate systemd gate
- no crawler start during naming documentation gate
- no DB mutation
- no raw evidence mutation
- no hidden pi51c sync
- no empty placeholder worker directories unless a real code or requirements surface is intentionally created

## 14. Final decision / Nihai karar

EN: The canonical service-pipeline vocabulary is now `preparation_core`, `crawler_core`, `process_core`, `ai_rank_core`, `port_core`, `compression_core` for layers and `preparation_worker`, `crawler_worker`, `process_worker`, `ai_rank_worker`, `port_worker`, `compression_worker` for worker/service surfaces.

TR: Kanonik service-pipeline sözlüğü artık katmanlar için `preparation_core`, `crawler_core`, `process_core`, `ai_rank_core`, `port_core`, `compression_core`; worker/service yüzeyleri için `preparation_worker`, `crawler_worker`, `process_worker`, `ai_rank_worker`, `port_worker`, `compression_worker` şeklindedir.

<!-- KOD_BLOGU_146_EXACT_AUDIT_NEEDLES_BEGIN -->
## Exact audit needles / Exact audit iğneleri

The following sentences are intentionally exact audit needles for future gates:

- port_core means controlled data porting/handoff.
- ai_rank_worker serves process_worker.
- compression_worker serves port_worker.
- parse_core is deprecated.
- desktop_import is deprecated.
- crawler_worker is an active transitional directory.

TR:

Aşağıdaki cümleler gelecek gate’ler için kasıtlı exact audit iğneleridir:

- port_core kontrollü veri portlama/handoff anlamındadır.
- ai_rank_worker process_worker hizmetindedir.
- compression_worker port_worker hizmetindedir.
- parse_core kullanımdan kaldırılmıştır.
- desktop_import kullanımdan kaldırılmıştır.
- crawler_worker aktif geçiş dizinidir.
<!-- KOD_BLOGU_146_EXACT_AUDIT_NEEDLES_END -->

<!-- KOD_BLOGU_149_FOUR_SURFACE_NAMING_ENFORCEMENT_BEGIN -->
## Four-surface naming enforcement / Dört yüzey isim standardı zorunluluğu

EN: The runtime service-pipeline naming migration is not complete until all of the following surfaces are aligned, audited, and sealed in order:

1. Ubuntu Desktop local repo: `/home/mak/dev/logisticsearch`
2. GitHub main: `https://github.com/malikepoglu/logisticsearch`
3. pi51c repo mirror: `/logisticsearch/repo`
4. pi51c live runtime: `/logisticsearch/makpi51crawler`
5. pi51c service unit surface: current `logisticsearch-webcrawler.service`, future `logisticsearch-crawler-worker.service`

TR: Runtime service-pipeline isim migration işi aşağıdaki yüzeylerin tamamı sırayla hizalanmadan, audit edilmeden ve mühürlenmeden bitmiş sayılmaz:

1. Ubuntu Desktop local repo: `/home/mak/dev/logisticsearch`
2. GitHub main: `https://github.com/malikepoglu/logisticsearch`
3. pi51c repo mirror: `/logisticsearch/repo`
4. pi51c live runtime: `/logisticsearch/makpi51crawler`
5. pi51c service unit yüzeyi: mevcut `logisticsearch-webcrawler.service`, gelecek `logisticsearch-crawler-worker.service`

### Mandatory sequence / Zorunlu sıra

1. Local-only documentation patch on Ubuntu Desktop.
2. Local read-only documentation audit.
3. Commit and push from Ubuntu Desktop to GitHub.
4. GitHub raw exact-head seal.
5. pi51c `/logisticsearch/repo` sync.
6. pi51c `/logisticsearch/repo` post-sync seal.
7. pi51c `/logisticsearch/makpi51crawler` live runtime sync.
8. pi51c live runtime post-sync seal.
9. Service unit rename/redirect gate.
10. Service unit read-only seal.
11. Short runtime health test before any long crawler run.

### Strict rule / Sert kural

No naming migration is complete until Ubuntu Desktop, GitHub main, pi51c repo, pi51c live, and service units are sealed.

TR: Ubuntu Desktop, GitHub main, pi51c repo, pi51c live ve service unit yüzeyi mühürlenmeden hiçbir isim migration işi tamamlanmış sayılmaz.

### Current active exception / Güncel aktif istisna

`python_live_runtime/crawler_worker/` and `logisticsearch-webcrawler.service` are active transitional surfaces. They must not be renamed by blind `mv`, blind `rsync`, blind `sed`, or hidden service edit. They require explicit import, service, live, DB-readonly, process-stillness, and short-health gates.

TR: `python_live_runtime/crawler_worker/` ve `logisticsearch-webcrawler.service` aktif geçiş yüzeyleridir. Kör `mv`, kör `rsync`, kör `sed` veya gizli service edit ile değiştirilmeyeceklerdir. Ayrı import, service, live, DB-readonly, process-stillness ve short-health gate isterler.
<!-- KOD_BLOGU_149_FOUR_SURFACE_NAMING_ENFORCEMENT_END -->
