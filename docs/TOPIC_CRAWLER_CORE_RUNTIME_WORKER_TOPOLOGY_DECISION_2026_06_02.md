# Crawler Core Runtime Worker Topology Decision / Crawler Core Runtime Worker Topoloji Kararı

Marker: `KOD_BLOGU_120_WORKER_TOPOLOGY_DECISION_DOC`

Created: `2026-06-02T20:33:56.499398+00:00`
Canonical head: `d0de6ffd7dd317122e7711b95ff697e093548d18`
Canonical subject: `fix(crawler-core): harden reset cleanup contract`

## 1. Purpose / Amaç

EN: This document freezes the next safe topology direction while the 26 JSON cascade crawler test continues on pi51c. It does not move files, create directories, change DB state, touch raw data, start/stop services, or sync pi51c.

TR: Bu doküman, pi51c üzerinde 26 JSON cascade crawler testi devam ederken bir sonraki güvenli topoloji yönünü mühürler. Dosya taşımaz, dizin oluşturmaz, DB durumunu değiştirmez, raw veriye dokunmaz, servis başlatmaz/durdurmaz ve pi51c senkronu yapmaz.

## 2. Hard decisions / Sert kararlar

1. EN: Python remains the orchestration/runtime-control/DB/queue/verification surface.
   TR: Python; orkestrasyon, runtime-control, DB, queue ve verification yüzeyi olarak kalır.
2. EN: C and C++ runtime surfaces remain separate.
   TR: C ve C++ runtime yüzeyleri ayrı kalır.
3. EN: No `native_live_runtime/` and no `c_cpp_live_runtime/`.
   TR: `native_live_runtime/` ve `c_cpp_live_runtime/` yoktur.
4. EN: Worker directory names use the `_worker` suffix.
   TR: Worker dizin adları `_worker` ekiyle kullanılır.
5. EN: Controls are immovable: `makpi51crawler/python_live_runtime/controls/` must not be moved, deleted, renamed, or folded into worker directories.
   TR: Controls taşınamaz: `makpi51crawler/python_live_runtime/controls/` taşınamaz, silinemez, yeniden adlandırılamaz veya worker dizinlerinin içine katılamaz.
6. EN: No empty placeholder worker directories will be created.
   TR: Boş placeholder worker dizinleri oluşturulmaz.
7. EN: Only language/runtime surfaces that actually receive code should get worker directories.
   TR: Sadece gerçekten kod alan dil/runtime yüzeylerinde worker dizini açılır.
8. EN: crawler_core zstd sidecar infrastructure is disabled, not deleted.
   TR: crawler_core zstd sidecar altyapısı silinmedi, deaktif edildi.
9. EN: Hot crawler_core path must not produce `.fetch.json.zst`, `.fetch.json`, or `.body.bin.zst`.
   TR: Sıcak crawler_core hattı `.fetch.json.zst`, `.fetch.json` veya `.body.bin.zst` üretmemelidir.
10. EN: Compression is deferred until parse_core has completed and desktop_import gives the compression directive.
   TR: Sıkıştırma, parse_core tamamlandıktan ve desktop_import sıkıştırma talimatı verdikten sonraya ertelenmiştir.

## 3. Canonical worker names / Kanonik worker adları

| Worker | Python surface | C surface | C++ surface | Current action |
|---|---|---|---|---|
| `crawler_core_worker` | planned under `python_live_runtime/` | no directory now | no directory now | document first, move later with explicit allowlist |
| `compression_worker` | no Python directory now | no directory now | planned later if C++ zstd work starts | do not create empty directory yet |
| `parse_core_worker` | planned later | no directory now | no directory now | document first |
| `ai_ranking_worker` | planned later | no directory now | no directory now | document first |
| `desktop_import_worker` | planned later | no directory now | no directory now | document first |

TR: Yukarıdaki tabloda `planned` ifadesi hemen dizin oluşturulacağı anlamına gelmez. Sadece yön kararını gösterir. Boş dizin yok.

## 4. Current audit snapshot / Güncel audit özeti

- Top-level Python files under `python_live_runtime/`: `32`
- Control Python files under `python_live_runtime/controls/`: `24`
- C runtime files under `c_live_runtime/`: `16`
- C++ runtime files under `cpp_live_runtime/`: `16`
- Forbidden mixed surfaces absent in KOD_BLOGU_119: `makpi51crawler/native_live_runtime`, `makpi51crawler/c_cpp_live_runtime`.
- Import graph parse failures in KOD_BLOGU_119: `0`.

## 5. First relocation target: crawler_core_worker / İlk taşıma hedefi

EN: The first real movement gate should focus only on crawler_core-related top-level Python files. It must use an explicit allowlist, not blind pattern matching.

TR: İlk gerçek taşıma gate’i sadece crawler_core ilişkili top-level Python dosyalarına odaklanmalıdır. Kör pattern matching değil, açık allowlist kullanılmalıdır.

### 5.1 Proposed crawler_core allowlist / Önerilen crawler_core allowlist

- `__init__.py` — `present` — sha256 `13d90a7e60dadc194fa059c5fea2a43e3e1e2c99439022ebba7319038bf18f04`
- `logisticsearch1_1_0_1_startpoint_catalog_runtime.py` — `present` — sha256 `3ed0c3fe60455fd5075b01dbb66ba34a3e0e6557a47912ffb4b5db66683fcc8e`
- `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` — `present` — sha256 `e0fed05dcc0d54d41920e2536e82a32ae714dc3d38479446b0cdff93288a51f0`
- `logisticsearch1_1_0_3_visit_policy_runtime.py` — `present` — sha256 `fb5839fc56d593d0474cc7b7c8c0651b59f522ce6aa17fae7b699664c6d3c2f6`
- `logisticsearch1_1_0_seed_frontier_bridge_runtime.py` — `present` — sha256 `65db8b907e0d704e6fe019d7bafa3afea3eaf0af062aa91ac57687e74dead68c`
- `logisticsearch1_1_1_1_gateway_support.py` — `present` — sha256 `07b48e33ce78971c28def1fca5c3c006f84399f1254a33d81da819ee59e52465`
- `logisticsearch1_1_1_2_runtime_control_gateway.py` — `present` — sha256 `5e184192d97e51e8d17b5636cb4d58c3b1b875e29765f33d0762530c9e0f7913`
- `logisticsearch1_1_1_3_frontier_gateway.py` — `present` — sha256 `88eed768687025d86275fbb37e8e46d891fb478790cdde95d077b6d5432481be`
- `logisticsearch1_1_1_4_robots_gateway.py` — `present` — sha256 `3aac486a49a510a2e1232edc9d30baaaedc98b15e4b1f84d794f633f007d167a`
- `logisticsearch1_1_1_5_fetch_attempt_gateway.py` — `present` — sha256 `162a2931045b5b1ff909575d81492c8b2be4c82560bd3ce149c37d372b76a6a2`
- `logisticsearch1_1_1_6_preranking_gateway.py` — `present` — sha256 `adc7be6988c0dab61f1e9e80b98221147e8a447723fb521e3da2838cc5b56d0c`
- `logisticsearch1_1_1_7_discovery_gateway.py` — `present` — sha256 `4b6b2ac39e13517ec37aef6be59d86535ef92bbb1d7750b8b09f4d746d1afd4e`
- `logisticsearch1_1_1_state_db_gateway.py` — `present` — sha256 `541c1090f20ca84e845de447d2585ec1cd4b1892115a72273ba3072b608b16f8`
- `logisticsearch1_1_2_1_worker_runtime_support.py` — `present` — sha256 `b2108b0a045abb8b6be648d8b73a774a66e5bec845cf5263f173c94834cf2ecc`
- `logisticsearch1_1_2_2_worker_lease_runtime.py` — `present` — sha256 `d4d3ab2f572500edb77b6a1f694ed170ded2b3f2dc7ff504920674169d5b5f3e`
- `logisticsearch1_1_2_3_worker_robots_runtime.py` — `present` — sha256 `dafb76e743a7bbbd5a43563631e50abf41240e0d2cecb96d1374e2b92346959e`
- `logisticsearch1_1_2_4_1_acquisition_support.py` — `present` — sha256 `4c7fe9696b216a98d61db33482f382f5017a77273d837dcf0de2c0b817e3307f`
- `logisticsearch1_1_2_4_2_http_page_acquisition_runtime.py` — `present` — sha256 `d44788ada7312c2f5544eabe22ea5de898119aa001da04446b7bb7f60c2e6259`
- `logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime.py` — `present` — sha256 `dfb8a0188b8f8f71deb648597b3a9c187e8a362311632a3e5f264de19d2ae552`
- `logisticsearch1_1_2_4_4_browser_page_acquisition_runtime.py` — `present` — sha256 `e2f1302069bbdd12c51f6d9f6dcf8e55b6144d1ff21e9a6f0ecf66ac82eee8ef`
- `logisticsearch1_1_2_4_5_robots_txt_acquisition_runtime.py` — `present` — sha256 `75d7ff0f6c0e685dcce96aac3c2cf28fbd4f6e3037da3c0b706fcb6d292cc459`
- `logisticsearch1_1_2_4_acquisition_runtime.py` — `present` — sha256 `ceeeaccd8a98342984e338a3b26d92825cf73171be593299d43495a84b8f38f5`
- `logisticsearch1_1_2_5_fetch_finalize_runtime.py` — `present` — sha256 `ab3102e6d269012d0bb0ff22ff6ff468444d996054d8f25e34d1e3135e0bb99f`
- `logisticsearch1_1_2_6_1_taxonomy_runtime.py` — `present` — sha256 `1248a8254ca042bafdac154d519b0b7fefe6dae64804abff1e5e5765cc28ed03`
- `logisticsearch1_1_2_6_parse_runtime.py` — `present` — sha256 `78621e8c28c0a1cfad556278f402dac1ca4f4a61b012cefe6315572a0230f179`
- `logisticsearch1_1_2_6_worker_frontier_policy_adapter.py` — `present` — sha256 `1e8d1ab4257f0f85d503aa889affd43cc94e34d83069825226edb9b5428e03c3`
- `logisticsearch1_1_2_7_storage_routing.py` — `present` — sha256 `f3124b85af891ad58605db8da324e83a4e87aebb74e429005f6965a2a6f9142b`
- `logisticsearch1_1_2_worker_runtime.py` — `present` — sha256 `071e925e0abdd3d044d6e3a0ce789838f92d1e367e91e332aa0746405470bd6f`
- `logisticsearch1_1_main_loop.py` — `present` — sha256 `c0bcfafa0b823238b49b0fe109c15d39bc8d7626d44de7056dadf728fa6ffbf8`
- `logisticsearch1_main_entry.py` — `present` — sha256 `ada962ab9cb10436a4d4144c1653057010c12b781f561e8e43a2571e9bf98379`
- `logisticsearch2_diag_browser_acquisition_smoke.py` — `present` — sha256 `e2f4b43b728ceaadf1dfce26b2609d6b53cba00be5d269192e0c367af2ccc6c0`

### 5.2 Desktop import candidate / Desktop import adayı

- `logisticsearch1_1_2_6_2_taxonomy_json_bridge_importer.py` — `present` — sha256 `1633954e82e386740d54a41987f1ede3b4fddccc20594525b63cdcc1fc7a5025`

### 5.3 Manual review / Elle inceleme

- No manual review files after proposed grouping.

## 6. Controls immovable seal / Controls taşınamaz mühür

EN: The following directory is out of scope for worker movement:

- `makpi51crawler/python_live_runtime/controls/`

TR: Aşağıdaki dizin worker taşıma kapsamı dışındadır:

- `makpi51crawler/python_live_runtime/controls/`

EN: Control scripts may call runtime modules, but they are operational controls and must stay stable while crawler tests run.

TR: Kontrol scriptleri runtime modüllerini çağırabilir, ancak bunlar operasyon kontrol yüzeyidir ve crawler testleri çalışırken stabil kalmalıdır.

## 7. ZSTD and compression decision / ZSTD ve sıkıştırma kararı

EN: crawler_core hot path currently writes `.body.bin` payloads and may write browser fallback artifacts such as `.rendered.html` and screenshots. It must not write `.fetch.json.zst`, `.fetch.json`, or `.body.bin.zst` during the hot crawler_core test.

TR: crawler_core sıcak hattı şu anda `.body.bin` payload dosyaları yazar ve gerekirse `.rendered.html` ile screenshot gibi browser fallback artifact’leri üretebilir. Sıcak crawler_core testinde `.fetch.json.zst`, `.fetch.json` veya `.body.bin.zst` yazmamalıdır.

EN: Later, after parse_core completes and desktop_import gives the directive, compression_worker will compress the raw body and fetch envelope separately, exactly once.

TR: Daha sonra parse_core tamamlandıktan ve desktop_import talimat verdikten sonra compression_worker ham body ve fetch envelope bilgisini ayrı ayrı, sadece bir kere sıkıştıracaktır.

## 8. Next gates / Sonraki gate’ler

1. `KOD_BLOGU_121_WORKER_TOPOLOGY_DECISION_DOC_AUDIT_READONLY_R1`
2. `KOD_BLOGU_122_WORKER_TOPOLOGY_DECISION_DOC_COMMIT_PUSH_GATE_R1`
3. `KOD_BLOGU_123_CRAWLER_CORE_WORKER_MOVE_PLAN_READONLY_R1`
4. After pi51c test ends: evaluate test and only then plan pi51c sync.

## 9. Forbidden next actions / Yasak sonraki eylemler

- EN: Do not touch pi51c while the test is running.
- EN: Do not move `controls/`.
- EN: Do not create empty C/C++ worker directories.
- EN: Do not enable zstd in crawler_core hot path.
- EN: Do not sync pi51c until the running test has been stopped/evaluated.
- EN: Do not use blind automated relocation without explicit file allowlist.

- TR: Test çalışırken pi51c’ye dokunma.
- TR: `controls/` dizinini taşıma.
- TR: Boş C/C++ worker dizinleri oluşturma.
- TR: crawler_core hot path içinde zstd’yi etkinleştirme.
- TR: Çalışan test durdurulup değerlendirilmeden pi51c senkronlama yapma.
- TR: Açık dosya allowlist’i olmadan kör otomatik taşıma yapma.

## 10. Final seal / Son mühür

EN: This document is a planning/decision artifact only. It intentionally performs no code movement.

TR: Bu doküman yalnızca plan/karar artifact’idir. Bilinçli olarak hiçbir kod taşıma işlemi yapmaz.

<!-- KOD_BLOGU_145_TOPOLOGY_NAMING_SUPERSESSION_BEGIN -->
## Naming supersession note / İsim standardı güncelleme notu

This topology document used the transitional name `crawler_core_worker` and listed older planned names such as `parse_core_worker`, `ai_ranking_worker`, and `desktop_import_worker`.

The canonical naming standard after KOD_BLOGU_145 is:

| Old / transitional name | Canonical future name |
|---|---|
| `crawler_core_worker` | `crawler_worker` |
| `parse_core_worker` | `process_worker` |
| `ai_ranking_worker` | `ai_rank_worker` |
| `desktop_import_worker` | `port_worker` |
| `compression_worker` | `compression_worker` |

This note does not move files. `crawler_core_worker` remains the current active directory until a separate gated rename patch.

Canonical naming doc:

- `docs/TOPIC_RUNTIME_SERVICE_PIPELINE_LAYER_NAMING_STANDARD_2026_06_03.md`
<!-- KOD_BLOGU_145_TOPOLOGY_NAMING_SUPERSESSION_END -->

<!-- KOD_BLOGU_149_TOPOLOGY_FOUR_SURFACE_NAMING_BEGIN -->
## Four-surface topology enforcement / Dört yüzey topoloji zorunluluğu

This topology is valid only when checked across:

- Ubuntu Desktop local repo: `/home/mak/dev/logisticsearch`
- GitHub main
- pi51c repo mirror: `/logisticsearch/repo`
- pi51c live runtime: `/logisticsearch/makpi51crawler`
- pi51c service unit surface

`crawler_core_worker` remains an active transitional directory until a later explicit `crawler_worker` rename gate. The service surface remains `logisticsearch-webcrawler.service` until a later explicit service rename gate.

No naming migration is complete until Ubuntu Desktop, GitHub main, pi51c repo, pi51c live, and service units are sealed.
<!-- KOD_BLOGU_149_TOPOLOGY_FOUR_SURFACE_NAMING_END -->
