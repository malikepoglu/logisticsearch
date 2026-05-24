# Global directories source-seed URL decision / Küresel dizin startpoint URL kararı

<!-- GLOBAL_DIR_R2A34_DOCS_INDEX_PATCH_LOCAL_ONLY:DECISION -->

## 1. Purpose / Amaç

TR: Bu karar dokümanı, LogisticSearch crawler_core için global dizin kaynaklarının nasıl modellenip canonical JSON'a dönüştürüldüğünü açıklar. Bu katalog, 25 ayrı dil kataloğuna ek olarak çalışan `global` kaynak katmanıdır.

EN: This decision document records how the global directory source-seed set was cleaned, deduplicated, canonicalized, and converted into a candidate-only JSON catalog for LogisticSearch crawler_core.

Canonical JSON:

`makpi51crawler/catalog/startpoints/global/global_directories_source_families_v2.json`

## 2. Final sealed result / Son mühürlü sonuç

| Metric | Value |
| --- | ---: |
| Raw rows reviewed | 1072 |
| Canonical source families | 696 |
| Seed surfaces | 696 |
| Seed URLs | 696 |
| Unique normalized hosts | 696 |
| Duplicate root-domain groups | 204 |
| Duplicate raw records inside duplicate groups | 580 |
| Merge-excess raw records | 376 |
| Exact URL exception rows | 1 |
| HOLD_VERIFY rows | 1 |
| HTTP canonical URLs | 6 |
| HTTPS canonical URLs | 690 |
| JSON SHA256 | `2b158159e0746e014a8176f31c8fb910d868fee219e542ec764a1bc1c24b55c1` |

## 3. Safety state / Güvenlik durumu

The catalog is intentionally not live.

- `candidate_manifest=true`
- `enabled=false`
- `is_live=false`
- `needs_live_check=true`
- `safety_state=candidate_only_not_live`
- `review_state=needs_live_check`
- `runtime_activation_policy=pi51c_live_probe_required_before_db_or_frontier_insert`

No DB insert, no frontier activation, no crawler start, no systemd mutation, no pi51c sync, and no public source URL probe occurred during this phase.

## 4. Canonicalization decision / Canonical karar

TR: Ham listede aynı root domain çok sayıda tekrar ediyordu. Bunlar silinmedi; tek canonical source_family altında metadata olarak birleştirildi.

EN: Repeated raw rows were not silently discarded. They were merged into canonical source families by normalized root host, while preserving raw references, aliases, categories, language scopes, and Turkish descriptions.

Final model:

`1072 raw refs -> 696 canonical source families`

## 5. High-priority prepend sources / Yüksek öncelikli kaynaklar

The initial priority sources were kept at the beginning of the canonical ordering when possible:

1. UNCTAD
2. World Bank Logistics Performance Index
3. TRACECA
4. CONFETRA
5. Cool Chain Association
6. Dangerous Goods Advisory Council
7. FNTR
8. ASTIC
9. ASLOG Morocco candidate

ASLOG remains `HOLD_VERIFY` because the official Morocco domain requires verification.

## 6. Kompass and Europages decision

TR: Kompass ve Europages çok geniş B2B dizinleri olduğu için silinmedi veya dar path ile sınırlandırılmadı. Root-domain source family olarak tutuldu. İlk lojistik filtreleme crawler_core aşamasında değil, parse_core/taxonomy aşamasında yapılacaktır.

EN: Kompass and Europages are broad but strategically important global B2B directories. They remain as root-domain source families. Logistics-specific filtering is deferred to parse_core using taxonomy/language filters after fetch.

Current canonical roots:

- `https://kompass.com`
- `https://europages.com`

## 7. Exact URL exception

Wikipedia logistics search is the only exact URL exception:

`https://en.wikipedia.org/w/index.php?search=logistics&title=Special%3ASearch&profile=advanced&fulltext=1&ns0=1`

It remains `url_type=exact_url` rather than root-domain.

## 8. HTTP handling

Raw staging had 7 HTTP rows. Canonical JSON has 6 HTTP URLs because `portshanghai.com.cn` appeared twice and collapsed into one canonical URL. This is expected and accepted.

Future live probe gates may verify HTTPS upgrades, but R2A catalog creation did not probe public URLs.

## 9. Future gates / Sonraki kapılar

Required next documentation gates:

- `GLOBAL_DIR_R2A35_DOCS_INDEX_AUDIT_READONLY`
- `GLOBAL_DIR_R2A36_DOCS_INDEX_COMMIT_PUSH_GATE`
- `GLOBAL_DIR_R2A37_DOCS_INDEX_POST_PUSH_SEAL_READONLY`

Future operational gates before activation:

- pi51c repo sync preflight
- pi51c repo sync
- live runtime sync
- source-by-source live probe
- robots/rate budget verification
- candidate frontier promotion only after explicit approval

## 10. Non-touch assertions

This decision did not:

- start crawler
- mutate DB/frontier
- mutate systemd
- sync pi51c
- run public URL probes
- promote global sources to live queue
<!-- GLOBAL_DIR_R2A34B2_DOCS_NEEDLE_FIX_LOCAL_ONLY_ROBUST:DECISION -->

## Exact catalog identity needle / Kesin katalog kimliği

This decision document intentionally keeps the exact identity literal for audits:

- `language_code=global`
- `global_directories_source_families_v2.json`
- Global directories
- `candidate_only_not_live`
- `pi51c_live_probe_required_before_db_or_frontier_insert`
<!-- GLOBAL_DIR_R2A35B_DECISION_DOC_EXACT_NEEDLE_FIX_LOCAL_ONLY -->

## Exact non-touch safety literals / Kesin dokunmama güvenlik ifadeleri

This section intentionally keeps the exact audit literals required by the documentation gate.

- No DB insert
- No frontier activation
- No crawler start
- No public source URL probe
- No systemd mutation
- No pi51c sync

<!-- GLOBAL_DIR_R2A72_RUNTIME_SCHEMA_FINAL_SEAL_BEGIN -->
## Runtime schema alignment and four-layer final seal / Runtime schema hizalaması ve dört katman final mührü

EN: This section was added after `GLOBAL_DIR_R2A71_FOUR_LAYER_SEAL_READONLY`. The original canonical JSON identity remains preserved above as the first deduplicated decision identity. The current runtime-schema-aligned catalog identity is now:

- `HEAD=934a9b4628127e96c61324cd236ee3e33708d84d`
- `SUBJECT=fix(source-seed): align global directories runtime schema`
- `global_directories_source_families_v2.json`
- `SHA256=d58b7e2cbdbeee71e170c2636c199421c60951b5570b32f1f4329c407bfe0363`
- `LINES=122178`
- `BYTES=5272821`
- `source_families=696`
- `seed_surfaces=696`
- `seed_urls=696`
- `raw_refs=1072`
- `merge_excess_raw_records=376`
- `duplicate_root_domain_groups=204`
- `runtime_validator=OK`
- `projection_return_type=dict`
- `projection_top_level_key_count=2`
- `projection_top_level_keys=projected_sources,projected_seed_urls`
- `projected_sources=696`
- `projected_seed_urls=696`

TR: Bu bölüm `GLOBAL_DIR_R2A71_FOUR_LAYER_SEAL_READONLY` sonrasında eklenmiştir. Yukarıdaki ilk canonical JSON kimliği, ilk deduplication karar kimliği olarak korunur. Güncel runtime-schema-aligned catalog kimliği artık şudur:

- `HEAD=934a9b4628127e96c61324cd236ee3e33708d84d`
- `SUBJECT=fix(source-seed): align global directories runtime schema`
- `global_directories_source_families_v2.json`
- `SHA256=d58b7e2cbdbeee71e170c2636c199421c60951b5570b32f1f4329c407bfe0363`
- `LINES=122178`
- `BYTES=5272821`
- `source_families=696`
- `seed_surfaces=696`
- `seed_urls=696`
- `raw_refs=1072`
- `merge_excess_raw_records=376`
- `duplicate_root_domain_groups=204`
- `runtime_validator=OK`
- `projection_return_type=dict`
- `projection_top_level_key_count=2`
- `projection_top_level_keys=projected_sources,projected_seed_urls`
- `projected_sources=696`
- `projected_seed_urls=696`

EN: Four-layer synchronization was sealed across Ubuntu Desktop, GitHub, pi51c `/logisticsearch/repo`, and pi51c live runtime `/logisticsearch/makpi51crawler`. The catalog is still candidate-only and not live. No DB insert, no frontier activation, no crawler start, no systemd mutation, and no public source URL probe occurred.

TR: Dört katman senkronizasyonu Ubuntu Desktop, GitHub, pi51c `/logisticsearch/repo` ve pi51c live runtime `/logisticsearch/makpi51crawler` üzerinde mühürlendi. Katalog hâlâ candidate-only ve live değildir. DB insert, frontier activation, crawler start, systemd mutation ve public source URL probe yapılmadı.

Detailed final seal document: `docs/TOPIC_CRAWLER_CORE_GLOBAL_DIRECTORIES_RUNTIME_SCHEMA_AND_FOUR_LAYER_SEAL_2026_05_23.md`.
<!-- GLOBAL_DIR_R2A72_RUNTIME_SCHEMA_FINAL_SEAL_END -->

<!-- GLOBAL_DIR_R2A81B_PROJECTION_RETURN_SHAPE_CORRECTION_BEGIN -->
EN: Earlier documentation used the shorthand `projected_rows` value `2`, but R2A80B proved that this was Python `len(...)` on a dictionary with two top-level row groups. The runtime projection return object is `dict`; its top-level keys are `projected_sources` and `projected_seed_urls`; each list contains 696 rows.

TR: Önceki dokümantasyonda `projected_rows` değeri `2` şeklinde kısaltma kullanılmıştı; R2A80B bunun iki top-level row group içeren dictionary üzerinde Python `len(...)` sonucu olduğunu kanıtladı. Runtime projection return object `dict`; top-level key’ler `projected_sources` ve `projected_seed_urls`; her iki liste de 696 satır içerir.
<!-- GLOBAL_DIR_R2A81B_PROJECTION_RETURN_SHAPE_CORRECTION_END -->
