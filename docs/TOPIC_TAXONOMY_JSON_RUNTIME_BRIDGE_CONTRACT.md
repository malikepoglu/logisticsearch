# Taxonomy JSON Runtime Bridge Contract

## English

### Purpose

This contract defines how LogisticSearch crawler_core/webcrawler will use the 25-language canonical taxonomy JSON without making SQL the taxonomy authoring source.

### Core decisions

- Canonical taxonomy content source of truth: JSON_FIRST_JSON_ONLY
- PostgreSQL role: RUNTIME_CACHE_QUERY_SEAM_ONLY
- Crawler hot loop policy: NO_DIRECT_JSON_READ_IN_HOT_LOOP
- Live runtime change policy: NO_LIVE_RUNTIME_SWITCH_BEFORE_SCRATCH_VALIDATION
- All-language coherence rule: ALL25_INVARIANT_REQUIRED_FOR_NODE_ADDITIONS

### Runtime bridge flow

canonical JSON
  -> controlled importer
  -> staging tables
  -> validation
  -> runtime lookup table or materialized view
  -> Python taxonomy lookup API
  -> parse pipeline classification/enrichment

### Canonical JSON surface

makpi51crawler/taxonomy/languages/*.json

SQL, staging rows, runtime lookup rows, crawler output, parser output, and import evidence are not taxonomy authoring surfaces.

### PostgreSQL boundary

PostgreSQL may be used only as a runtime cache/query seam rebuilt from validated canonical JSON imports. Manual runtime taxonomy edits are forbidden.

### Python lookup API boundary

The crawler/parser should use a stable lookup function such as search_runtime_taxonomy(...).

The API should return immutable result mappings with:

- term_id
- concept_id
- hierarchy_id
- unspsc_code
- language
- term
- matched_text
- matched_surface
- match_score
- match_reason

If lookup is unavailable, the caller must receive a controlled empty result or taxonomy-unavailable status. Crawler state must not be corrupted.

### Failure policy

Invalid JSON, schema drift, incomplete all-language coverage, staging write errors, runtime materialization mismatches, and lookup unavailability must stop safely with evidence.

No failure path may silently create live DB objects, touch Pi51crawler runtime, or modify canonical taxonomy files.

## Türkçe

### Amaç

Bu contract, LogisticSearch crawler_core/webcrawler katmanının 25 dilli canonical taxonomy JSON verisini nasıl kullanacağını tanımlar. SQL taxonomy yazım kaynağı olmayacaktır.

### Temel kararlar

- Canonical taxonomy içerik kaynağı: JSON_FIRST_JSON_ONLY
- PostgreSQL rolü: RUNTIME_CACHE_QUERY_SEAM_ONLY
- Crawler hot loop kuralı: NO_DIRECT_JSON_READ_IN_HOT_LOOP
- Live runtime kuralı: NO_LIVE_RUNTIME_SWITCH_BEFORE_SCRATCH_VALIDATION
- 25 dil tutarlılık kuralı: ALL25_INVARIANT_REQUIRED_FOR_NODE_ADDITIONS

### Runtime bridge akışı

canonical JSON
  -> controlled importer
  -> staging tables
  -> validation
  -> runtime lookup table or materialized view
  -> Python taxonomy lookup API
  -> parse pipeline classification/enrichment

### Canonical JSON yüzeyi

makpi51crawler/taxonomy/languages/*.json

SQL, staging kayıtları, runtime lookup kayıtları, crawler çıktısı, parser çıktısı ve import kanıtları taxonomy yazım kaynağı değildir.

### PostgreSQL sınırı

PostgreSQL sadece doğrulanmış canonical JSON importundan yeniden üretilen runtime cache/query seam olabilir. Elle runtime taxonomy düzenlemek yasaktır.

### Python lookup API sınırı

Crawler/parser sabit bir lookup fonksiyonu kullanmalıdır. Örneğin search_runtime_taxonomy(...).

API şu alanları döndürmelidir:

- term_id
- concept_id
- hierarchy_id
- unspsc_code
- language
- term
- matched_text
- matched_surface
- match_score
- match_reason

Lookup erişilemezse caller kontrollü boş sonuç veya taxonomy-unavailable status almalıdır. Crawler state bozulmamalıdır.

### Failure policy

Geçersiz JSON, schema drift, eksik 25 dil coverage, staging write hataları, runtime materialization mismatch ve lookup unavailable durumları evidence ile güvenli durmalıdır.

Hiçbir hata yolu sessizce live DB object yaratamaz, Pi51crawler runtime'a dokunamaz veya canonical taxonomy dosyalarını değiştiremez.
