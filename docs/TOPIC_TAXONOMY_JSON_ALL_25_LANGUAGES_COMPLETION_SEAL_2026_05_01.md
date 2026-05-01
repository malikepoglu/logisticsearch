# Taxonomy JSON all-25-language completion seal — 2026-05-01

## English

This document seals the completion of the canonical JSON-first taxonomy language set.

The canonical language JSON surface is complete:

- Language JSON files: **25**
- Populated languages: **25**
- Placeholder languages: **0**
- Records per language: **335**
- Total populated records: **8375**
- Final repository head: `b9e75a3be0c6da134a0c362b6dd2b85f9e751f6c`

The final corrected rollup audit passed with:

- `error_count = 0`
- `duplicate_term_group_count = 0`
- `blank_or_invalid_field_count = 0`
- `description_marker_issue_count = 0`
- `stable_identity_mismatch_count = 0`
- No SQL, database, scratch database, runtime, pi51c, or systemd surface touched.

### Corrected rollup policy

The R2 rollup corrected the overly strict R1 assumptions:

1. `term_id` is valid when it uses the correct language prefix and numeric ordinal, whether the numeric part is unpadded (`xx-1`) or zero-padded (`xx-001`).
2. `attributes.is_compound` and `attributes.morphology` are language-surface-specific attributes. They are type-checked, but they are not cross-language identity fields.
3. Stable cross-language identity fields are:
   - `concept_id`
   - `hierarchy_id`
   - `unspsc_code`
   - `description`
   - `role`
   - `is_searchable`
   - `attributes.priority`
   - `attributes.industry_standards`

### Completed languages

`ar, bg, cs, de, el, en, es, fr, hu, it, ja, ko, nl, pt, ro, ru, tr, zh, hi, bn, ur, uk, id, vi, he`

### Term ID policy observed

Unpadded first-99 policy languages:

`ar, bg, cs, de, el, en, es, fr, hu, it, ja, tr`

Zero-padded first-99 policy languages:

`ko, nl, pt, ro, ru, zh, hi, bn, ur, uk, id, vi, he`

### Evidence

Primary R2 summary:

`_build/taxonomy_json_language_completion_audit/2026-05-01_21-38-26_taxonomy_json_all_25_languages_final_rollup_seal_r2_readonly/taxonomy_json_all_25_languages_final_rollup_r2_summary.json`

R1_R1 local-only documentation evidence:

`_build/taxonomy_json_language_completion_audit/2026-05-01_21-51-40_taxonomy_json_all_25_languages_completion_doc_seal_r1_r1_fix_export_local_only`

## Türkçe

Bu belge, canonical JSON-first taxonomy dil setinin tamamlandığını mühürler.

Canonical language JSON yüzeyi tamamlanmıştır:

- Language JSON dosyası: **25**
- Dolu/populated dil: **25**
- Placeholder dil: **0**
- Dil başına kayıt: **335**
- Toplam populated kayıt: **8375**
- Final repository head: `b9e75a3be0c6da134a0c362b6dd2b85f9e751f6c`

Final düzeltilmiş rollup audit sonucu:

- `error_count = 0`
- `duplicate_term_group_count = 0`
- `blank_or_invalid_field_count = 0`
- `description_marker_issue_count = 0`
- `stable_identity_mismatch_count = 0`
- SQL, database, scratch database, runtime, pi51c veya systemd yüzeyine dokunulmadı.

### Düzeltilmiş rollup politikası

R2 rollup, R1 içindeki fazla dar varsayımları düzeltti:

1. `term_id`, doğru language prefix ve numeric ordinal taşıdığı sürece geçerlidir. Numeric bölüm unpadded (`xx-1`) veya zero-padded (`xx-001`) olabilir.
2. `attributes.is_compound` ve `attributes.morphology` dil/yüzey bağımlı alanlardır. Type kontrolü yapılır, fakat cross-language identity alanı olarak karşılaştırılmaz.
3. Stable cross-language identity alanları:
   - `concept_id`
   - `hierarchy_id`
   - `unspsc_code`
   - `description`
   - `role`
   - `is_searchable`
   - `attributes.priority`
   - `attributes.industry_standards`

### Tamamlanan diller

`ar, bg, cs, de, el, en, es, fr, hu, it, ja, ko, nl, pt, ro, ru, tr, zh, hi, bn, ur, uk, id, vi, he`

### Gözlenen term ID politikası

İlk 99 kayıtta unpadded policy kullanan diller:

`ar, bg, cs, de, el, en, es, fr, hu, it, ja, tr`

İlk 99 kayıtta zero-padded policy kullanan diller:

`ko, nl, pt, ro, ru, zh, hi, bn, ur, uk, id, vi, he`

### Kanıt

Ana R2 summary:

`_build/taxonomy_json_language_completion_audit/2026-05-01_21-38-26_taxonomy_json_all_25_languages_final_rollup_seal_r2_readonly/taxonomy_json_all_25_languages_final_rollup_r2_summary.json`

R1_R1 local-only dokümantasyon evidence:

`_build/taxonomy_json_language_completion_audit/2026-05-01_21-51-40_taxonomy_json_all_25_languages_completion_doc_seal_r1_r1_fix_export_local_only`

## Decision / Karar

EN: The taxonomy data completion stage is sealed. The next architectural decision is whether to document the completion package first or move into the JSON-to-runtime bridge/import decision surface.

TR: Taxonomy data completion aşaması mühürlenmiştir. Sıradaki mimari karar, önce completion package dokümantasyonunu genişletmek mi yoksa JSON-to-runtime bridge/import decision yüzeyine geçmek mi olacağıdır.
