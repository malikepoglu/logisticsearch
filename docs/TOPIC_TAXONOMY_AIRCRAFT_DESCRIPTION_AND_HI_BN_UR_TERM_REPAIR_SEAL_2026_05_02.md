# Taxonomy Aircraft Description and hi/bn/ur Term Repair Seal - 2026-05-02

[EN] This document seals the completed LogisticSearch taxonomy JSON repair cycle for aircraft-related description drift and Hindi/Bengali/Urdu term alignment.

[TR] Bu belge, LogisticSearch taxonomy JSON yapısında aircraft alanındaki description kayması ve Hindi/Bengali/Urdu term hizalama onarım döngüsünün tamamlandığını mühürler.

## Final sealed commit

- Commit: `5ec833d937059a15dafe9f161861f939b2e38737`
- Commit message: `feat(taxonomy): repair aircraft taxonomy descriptions and terms`
- Machine: Ubuntu Desktop
- Pi51c: not touched
- DB/SQL/runtime/systemd: not touched
- Bulk crawler data: not involved

## Scope

[EN] The repair changed exactly the canonical taxonomy language JSON surface under `makpi51crawler/taxonomy/languages/`.

[TR] Onarım yalnızca `makpi51crawler/taxonomy/languages/` altındaki canonical taxonomy language JSON yüzeyini değiştirdi.

Changed surface:

- 25 taxonomy language JSON files
- 8,375 total records
- 25 languages x 335 records
- 450 description guard rows sealed
- 54 exact hi/bn/ur term guard rows sealed

## What was repaired

### 1. Aircraft and railway/tramway description drift

[EN] 18 stable ordinals had description template drift. The descriptions incorrectly described aircraft rows as marine/waterway concepts, and the railway/tramway equipment row as aircraft/aviation. The repair replaced these descriptions with sector-correct EN/TR admin-control descriptions.

[TR] 18 sabit ordinal satırında description template kayması vardı. Aircraft satırları yanlış şekilde marine/waterway kavramı gibi, railway/tramway equipment satırı ise aircraft/aviation gibi açıklanıyordu. Onarım bu açıklamaları sector-correct EN/TR admin-control açıklamalarıyla değiştirdi.

Patched ordinals:

`272,273,274,275,276,278,279,280,281,282,283,284,285,286,287,288,290,291`

### 2. hi/bn/ur term alignment repair

[EN] Hindi, Bengali, and Urdu had shifted terms for the same 18 ordinals. These terms pointed to road/rental/container/public-transport concepts while the stable identity fields pointed to rail equipment or aircraft concepts. The repair changed only the `term` field for those exact rows.

[TR] Hindi, Bengali ve Urdu dosyalarında aynı 18 ordinal için term kayması vardı. Bu term değerleri road/rental/container/public-transport kavramlarına işaret ederken stable identity alanları rail equipment veya aircraft kavramlarına işaret ediyordu. Onarım sadece bu exact satırlarda `term` alanını değiştirdi.

Patched language/row count:

- `hi`: 18 term rows
- `bn`: 18 term rows
- `ur`: 18 term rows
- Total: 54 term rows

## Explicitly not changed

- No new taxonomy nodes were created.
- No hierarchy expansion was performed.
- No UNSPSC remapping was performed.
- No `concept_id` changes were made.
- No `hierarchy_id` changes were made.
- No `unspsc_code` changes were made.
- No `role` changes were made.
- No `is_searchable` changes were made.
- No `attributes` changes were made.
- No term_id padding normalization was performed.
- No Pi51c runtime or database surface was touched.

## Final R11 evidence

R11 post-push final seal evidence root:

`/tmp/logisticsearch_taxonomy_all25_r11_post_push_final_seal_2026-05-02_00-35-49`

Final R11 metrics:

- `final_verdict=PASS`
- `commit_head=5ec833d937059a15dafe9f161861f939b2e38737`
- `four_pass_stable=True`
- `language_count_loaded=25`
- `total_record_count=8375`
- `hard_error_count=0`
- `duplicate_normalized_term_group_count=0`
- `wrong_script_count=0`
- `patched_description_guard_rows=450`
- `patched_description_guard_fail_count=0`
- `hi_bn_ur_term_guard_rows=54`
- `hi_bn_ur_term_guard_fail_count=0`
- `old_shifted_term_hit_count=0`
- `term_id_policy_fail_count=0`

Stable fingerprint:

`2432c4a5ae13885e86d67044f0f7b2489885372b411309a9f5412b1f2cd260eb`

## Next recommended work

[EN] After this seal, the next strict path should be either taxonomy JSON-first runtime bridge / scratch DB import continuation, or a separate English-first taxonomy expansion planning cycle. Expansion must be handled as a new controlled design cycle and must not be mixed with this repair patch.

[TR] Bu mühürden sonra en doğru devam yolu taxonomy JSON-first runtime bridge / scratch DB import hattına dönmek veya ayrı bir English-first taxonomy expansion planlama döngüsü başlatmaktır. Expansion ayrı kontrollü tasarım döngüsü olarak ele alınmalı ve bu repair patch ile karıştırılmamalıdır.
