# TOPIC_TAXONOMY_JSON_FIRST_RUNTIME_BRIDGE_CONTRACT

## EN

### Purpose

This document records the LogisticSearch taxonomy JSON-first runtime bridge contract.

It exists so the project can move from SQL-authored taxonomy language-term data toward canonical JSON-authored taxonomy language-term data without destabilizing the crawler runtime.

### Core decision

Canonical taxonomy language-term data lives in repository-tracked JSON files.

PostgreSQL remains the runtime database for crawler/search execution.

The crawler worker loop must not read canonical taxonomy JSON language files directly during normal runtime execution.

### Why runtime must not read JSON directly

Direct runtime reads from canonical JSON files would mix authoring truth with execution truth.

That would create several risks:

1. placeholder language files could be treated as live runtime languages;
2. schema-valid but not yet imported data could affect crawler behavior before scratch audit;
3. runtime behavior could differ between Ubuntu Desktop, GitHub, and pi51c depending on file sync timing;
4. crawler performance and error handling would become dependent on repository file parsing;
5. deterministic database audit and controlled live-swap discipline would be weakened.

Therefore JSON is the canonical authoring and source-of-truth surface, but PostgreSQL is the runtime execution surface.

### Current repository state

At the current sealed point, the taxonomy JSON language surface has 25 files.

The populated canonical JSON language files are:

1. `ar`
2. `de`
3. `en`
4. `tr`

Each populated file contains 335 term records.

The remaining 21 language files are controlled placeholder files represented as empty JSON arrays.

A placeholder language file is not a runtime-ready language dataset.

### Required execution flow

The correct taxonomy data flow is:

1. edit canonical JSON;
2. validate JSON schema;
3. validate deterministic invariants;
4. import JSON into a PostgreSQL scratch/staging surface;
5. build PostgreSQL runtime tables or runtime views;
6. run deterministic counts, hashes, semantic probes, and guard checks;
7. compare Desktop and pi51c scratch results when required;
8. promote to live only through controlled scratch -> audit -> live swap;
9. let Python runtime query the live PostgreSQL runtime seam.

### Minimal runtime bridge target

The JSON-first PostgreSQL runtime bridge must expose these canonical identity fields:

1. `concept_id`
2. `hierarchy_id`
3. `term_id`
4. `language`
5. `term`
6. `description`
7. `role`
8. `synonyms`
9. `is_searchable`
10. `attributes`
11. `unspsc_code`

The bridge may temporarily expose compatibility fields while migration is unfinished:

1. `node_id`
2. `node_code`
3. `matched_surface`
4. `matched_text`
5. `match_score`
6. `lang_priority`

`node_code` is compatibility terminology only during transition. New canonical JSON language data must use `hierarchy_id`.

### SQL boundary

SQL remains necessary for:

1. runtime schema;
2. JSON import/staging;
3. deterministic validation;
4. runtime search views;
5. migrations;
6. controlled scratch/live operations.

SQL should not remain the long-term primary editing surface for language-term data.

Historical SQL repair/patch files must not be deleted until the JSON-first import/runtime bridge is sealed and the archival policy is documented.

### Python runtime boundary

`logisticsearch1_1_2_6_1_taxonomy_runtime.py` should eventually query one clear PostgreSQL runtime seam derived from canonical JSON import.

It should not query scattered legacy tables as the final design.

During migration it may preserve compatibility output so downstream parse/runtime code does not break suddenly.

### Parse runtime boundary

`logisticsearch1_1_2_6_parse_runtime.py` consumes taxonomy runtime helpers.

It must not treat placeholder languages as populated runtime languages.

It should receive explicit taxonomy match payloads where canonical identity fields are visible or recoverable.

### Safe migration order

The safe technical order is:

1. create this tracked contract document;
2. add JSON-first SQL bridge skeleton;
3. update SQL apply/preflight/presence audit surfaces;
4. run Desktop scratch-only validation;
5. update Python taxonomy runtime to query the new runtime seam;
6. update parse integration only after taxonomy runtime seam is proven;
7. commit and push sealed repo state;
8. sync pi51c repo;
9. perform controlled runtime DB promotion only after scratch audit passes.

### Explicit non-goals for this stage

This stage does not design final ranking.

This stage does not delete legacy runtime tables.

This stage does not delete historical SQL patch files.

This stage does not move runtime execution out of PostgreSQL.

This stage does not make crawler workers read JSON files directly.

## TR

### Amaç

Bu doküman LogisticSearch taxonomy JSON-first runtime bridge sözleşmesini kaydeder.

Projenin SQL içinde düzenlenen taxonomy dil-terim verisinden kanonik JSON içinde düzenlenen taxonomy dil-terim verisine geçmesini, crawler runtime'ı bozmadan yönetmek için vardır.

### Ana karar

Kanonik taxonomy dil-terim verisi repository içinde izlenen JSON dosyalarında yaşar.

PostgreSQL crawler/search çalışması için runtime veritabanı olarak kalır.

Crawler worker loop normal runtime çalışması sırasında kanonik taxonomy JSON dil dosyalarını doğrudan okumamalıdır.

### Runtime neden JSON'u doğrudan okumamalı

Runtime'ın kanonik JSON dosyalarını doğrudan okuması authoring truth ile execution truth alanlarını karıştırır.

Bu birkaç risk üretir:

1. placeholder dil dosyaları canlı runtime dili gibi algılanabilir;
2. schema-valid fakat henüz import/audit edilmemiş veri crawler davranışını etkileyebilir;
3. Ubuntu Desktop, GitHub ve pi51c arasında file sync zamanına bağlı runtime farkları oluşabilir;
4. crawler performansı ve hata yönetimi repository dosya parse işlemine bağımlı hale gelir;
5. deterministik database audit ve kontrollü live-swap disiplini zayıflar.

Bu yüzden JSON kanonik authoring ve source-of-truth yüzeyidir; PostgreSQL ise runtime execution yüzeyidir.

### Mevcut repo durumu

Mevcut sealed noktada taxonomy JSON dil yüzeyinde 25 dosya vardır.

Dolu kanonik JSON dil dosyaları şunlardır:

1. `ar`
2. `de`
3. `en`
4. `tr`

Her dolu dosyada 335 term kaydı vardır.

Kalan 21 dil dosyası boş JSON array olarak tutulan kontrollü placeholder dosyalarıdır.

Placeholder dil dosyası runtime'a hazır dil dataset'i değildir.

### Zorunlu çalışma akışı

Doğru taxonomy veri akışı şudur:

1. kanonik JSON düzenlenir;
2. JSON schema doğrulanır;
3. deterministik invariant'lar doğrulanır;
4. JSON PostgreSQL scratch/staging yüzeyine import edilir;
5. PostgreSQL runtime tabloları veya runtime view'ları üretilir;
6. deterministik count, hash, semantic probe ve guard kontrolleri çalıştırılır;
7. gerektiğinde Desktop ve pi51c scratch sonuçları karşılaştırılır;
8. live'a geçiş sadece kontrollü scratch -> audit -> live swap ile yapılır;
9. Python runtime canlı PostgreSQL runtime seam'ini sorgular.

### Minimal runtime bridge hedefi

JSON-first PostgreSQL runtime bridge şu kanonik identity alanlarını açığa çıkarmalıdır:

1. `concept_id`
2. `hierarchy_id`
3. `term_id`
4. `language`
5. `term`
6. `description`
7. `role`
8. `synonyms`
9. `is_searchable`
10. `attributes`
11. `unspsc_code`

Bridge geçiş tamamlanana kadar uyumluluk alanlarını geçici olarak açığa çıkarabilir:

1. `node_id`
2. `node_code`
3. `matched_surface`
4. `matched_text`
5. `match_score`
6. `lang_priority`

`node_code` geçiş sırasında yalnızca uyumluluk terminolojisidir. Yeni kanonik JSON dil verisinde `hierarchy_id` kullanılmalıdır.

### SQL sınırı

SQL şu işler için gerekli kalır:

1. runtime schema;
2. JSON import/staging;
3. deterministik validation;
4. runtime search view'ları;
5. migration;
6. kontrollü scratch/live operasyonları.

SQL uzun vadede dil-terim verisi için ana düzenleme yüzeyi olarak kalmamalıdır.

Tarihsel SQL repair/patch dosyaları JSON-first import/runtime bridge seal edilmeden ve archival policy dokümante edilmeden silinmemelidir.

### Python runtime sınırı

`logisticsearch1_1_2_6_1_taxonomy_runtime.py` ileride kanonik JSON importundan türetilmiş tek açık PostgreSQL runtime seam'ini sorgulamalıdır.

Final tasarımda dağınık legacy tabloları doğrudan sorgulamamalıdır.

Migration sırasında downstream parse/runtime kodu bir anda bozulmasın diye compatibility output korunabilir.

### Parse runtime sınırı

`logisticsearch1_1_2_6_parse_runtime.py` taxonomy runtime helper'larını tüketir.

Placeholder dilleri populated runtime dili gibi ele almamalıdır.

Kanonik identity alanlarının görünür veya geri kazanılabilir olduğu açık taxonomy match payload'ları almalıdır.

### Güvenli migration sırası

Güvenli teknik sıra şudur:

1. bu tracked contract dokümanını oluştur;
2. JSON-first SQL bridge skeleton ekle;
3. SQL apply/preflight/presence audit yüzeylerini güncelle;
4. Desktop scratch-only validation çalıştır;
5. Python taxonomy runtime'ı yeni runtime seam'i sorgulayacak şekilde güncelle;
6. taxonomy runtime seam kanıtlandıktan sonra parse integration güncelle;
7. sealed repo state'i commit/push yap;
8. pi51c repo sync yap;
9. runtime DB promotion sadece scratch audit geçtikten sonra kontrollü yapılır.

### Bu aşamanın açık non-goal maddeleri

Bu aşama final ranking tasarlamaz.

Bu aşama legacy runtime tablolarını silmez.

Bu aşama tarihsel SQL patch dosyalarını silmez.

Bu aşama runtime execution'ı PostgreSQL dışına taşımaz.

Bu aşama crawler worker'ların JSON dosyalarını doğrudan okumasını sağlamaz.
