# Source Seed Planner / Worker Contract

## English

### Purpose

This document defines the canonical LogisticSearch contract for multilingual startpoint, source, and seed planning.

The main rule is simple: planning and execution must be separated.

The planner prepares, validates, and explains source seed work. The worker executes only approved source seed work after a separate runbook and safety gate.

### Canonical naming rule

All planned seed outputs and durable seed concepts should use the `source_seed_` naming pattern where appropriate.

Examples:

- `source_seed_plan`
- `source_seed_batch`
- `source_seed_matrix`
- `source_seed_candidate`
- `source_seed_language_coverage`
- `source_seed_source_family_coverage`

This naming keeps source discovery separate from generic URL discovery and makes crawler behaviour auditable.

### Python hierarchy rule

Webcrawler phase-1 Python modules must live under:

`hosts/makpi51crawler/python/webcrawler/lib/`

The current planned hierarchy is:

| Order | Module | Role |
|---:|---|---|
| 1 | `logisticsearch1_1_0_1_startpoint_catalog_runtime.py` | Reads and validates source-family startpoint catalog surfaces. |
| 2 | `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` | Plans multilingual `source_seed_` batches and dry-run evidence. |
| 3 | `logisticsearch1_1_0_3_multilingual_startpoint_seed_worker.py` | Executes approved `source_seed_` batches later. |

The worker must not be created or enabled before the planner contract, planner dry-run evidence, and execution runbook are sealed.

### Planner contract

The `_planner` module is responsible for:

- reading canonical startpoint catalogs,
- reading the 25-language taxonomy state when needed,
- building source/language/seed coverage matrices,
- detecting missing language coverage,
- detecting duplicate or unsafe seed candidates,
- producing dry-run evidence,
- producing reviewable `source_seed_` batches,
- refusing to mutate crawler runtime state.

The planner must default to read-only / dry-run behaviour.

The planner must not:

- claim URLs,
- fetch pages,
- write frontier rows,
- mutate runtime database state,
- touch Pi51c,
- start systemd services,
- bypass review evidence.

### Worker contract

The `_worker` module is responsible for executing approved planner output later.

The worker may only exist after:

1. the planner module is implemented,
2. the planner dry-run passes,
3. a source seed execution runbook exists,
4. the target runtime surface is explicitly approved.

The worker must not invent seed plans. It must consume approved planner output.

### 25-language source/startpoint strategy

The system will eventually support multilingual source discovery. This means the source/startpoint/seed model must handle:

- 25 languages,
- language-specific source surfaces,
- shared source families,
- country or language sections under the same host,
- cross-language coverage checks,
- no accidental duplicate top-level source families for the same host.

Important hierarchy rule:

A website with multiple country or language sections under one main host should remain one coherent source family unless there is a strong reason to split it.

Example:

`fiata.org` should be treated as one source family with language/country/section metadata beneath it, not as many unrelated top-level sources just because URL paths differ.

### Runtime safety

This contract does not authorize:

- DB creation,
- SQL execution,
- Pi51c touch,
- runtime copy,
- systemd action,
- crawler execution,
- source seed worker execution.

### Documentation and runbook rule

Canonical design decisions must be written to GitHub documentation first.

As implementation begins, each execution surface must receive a runbook before real runtime execution.

## Türkçe

### Amaç

Bu doküman, LogisticSearch için çok dilli startpoint, source ve seed planlamasının kanonik sözleşmesini tanımlar.

Ana kural yalındır: planlama ve çalıştırma ayrılmalıdır.

Planner, source seed işini hazırlar, doğrular ve açıklar. Worker ise sadece onaylanmış source seed işini ayrı runbook ve güvenlik kapısından sonra uygular.

### Kanonik isimlendirme kuralı

Planlanan seed çıktıları ve kalıcı seed kavramları uygun yerlerde `source_seed_` isimlendirmesini kullanmalıdır.

Örnekler:

- `source_seed_plan`
- `source_seed_batch`
- `source_seed_matrix`
- `source_seed_candidate`
- `source_seed_language_coverage`
- `source_seed_source_family_coverage`

Bu isimlendirme, source keşfini genel URL keşfinden ayırır ve crawler davranışını denetlenebilir yapar.

### Python hiyerarşi kuralı

Webcrawler faz-1 Python modülleri şu klasör altında olmalıdır:

`hosts/makpi51crawler/python/webcrawler/lib/`

Mevcut planlanan hiyerarşi:

| Sıra | Modül | Rol |
|---:|---|---|
| 1 | `logisticsearch1_1_0_1_startpoint_catalog_runtime.py` | Source-family startpoint catalog yüzeylerini okur ve doğrular. |
| 2 | `logisticsearch1_1_0_2_multilingual_startpoint_seed_planner.py` | Çok dilli `source_seed_` batch ve dry-run evidence üretir. |
| 3 | `logisticsearch1_1_0_3_multilingual_startpoint_seed_worker.py` | Onaylanmış `source_seed_` batchlerini daha sonra uygular. |

Worker; planner contract, planner dry-run evidence ve execution runbook mühürlenmeden oluşturulmamalı veya etkinleştirilmemelidir.

### Planner contract

`_planner` modülünün görevi şunlardır:

- canonical startpoint cataloglarını okumak,
- gerektiğinde 25 dilli taxonomy durumunu okumak,
- source/language/seed coverage matrix üretmek,
- eksik dil coverage durumlarını yakalamak,
- duplicate veya güvensiz seed adaylarını yakalamak,
- dry-run evidence üretmek,
- incelenebilir `source_seed_` batchleri üretmek,
- crawler runtime state değiştirmeyi reddetmek.

Planner varsayılan olarak read-only / dry-run çalışmalıdır.

Planner şunları yapmamalıdır:

- URL claim etmek,
- sayfa fetch etmek,
- frontier satırı yazmak,
- runtime database state değiştirmek,
- Pi51c’ye dokunmak,
- systemd servisi başlatmak,
- review evidence sürecini atlamak.

### Worker contract

`_worker` modülü ileride onaylanmış planner çıktısını çalıştırmak içindir.

Worker sadece şu koşullardan sonra var olmalıdır:

1. planner modülü uygulanmış olmalı,
2. planner dry-run PASS olmalı,
3. source seed execution runbook var olmalı,
4. hedef runtime yüzeyi açıkça onaylanmış olmalı.

Worker seed planı icat etmemelidir. Sadece onaylanmış planner çıktısını tüketmelidir.

### 25 dilli source/startpoint stratejisi

Sistem ileride çok dilli source keşfini destekleyecektir. Bu yüzden source/startpoint/seed modeli şunları taşımalıdır:

- 25 dil,
- dile özel source yüzeyleri,
- ortak source family yapısı,
- aynı host altındaki ülke veya dil bölümleri,
- cross-language coverage kontrolleri,
- aynı host için yanlışlıkla duplicate top-level source family üretmeme.

Önemli hiyerarşi kuralı:

Bir ana host altında birden çok ülke veya dil bölümü varsa, güçlü bir gerekçe olmadıkça bunlar tek coherent source family altında kalmalıdır.

Örnek:

`fiata.org`, URL path farklı diye birçok ilgisiz top-level source değil; dil/ülke/bölüm metadata’sı olan tek source family olarak ele alınmalıdır.

### Runtime güvenliği

Bu contract şunlara izin vermez:

- DB yaratma,
- SQL çalıştırma,
- Pi51c’ye dokunma,
- runtime copy,
- systemd action,
- crawler çalıştırma,
- source seed worker çalıştırma.

### Dokümantasyon ve runbook kuralı

Kanonik tasarım kararları önce GitHub dokümantasyonuna yazılmalıdır.

Implementation başladıkça, her execution yüzeyi gerçek runtime çalıştırma öncesi runbook almalıdır.


## Strict Python variable/comment standard / Katı Python değişken-yorum standardı

<!-- STRICT_PYTHON_VARIABLE_COMMENT_STANDARD_EN_TR -->

### English

Every LogisticSearch Python file must be written for a first-time reader.

For every important variable, function, parameter, dataclass field, path constant, mode flag, count, status value, and safety guard, the code must include detailed bilingual comments immediately above the relevant line or block.

Each comment must explain:

- what the variable/function/parameter is,
- why it exists,
- how it is used,
- which values are expected,
- which values are invalid or dangerous,
- which failure mode should happen for invalid values.

This rule is mandatory for source/startpoint/seed planner and worker code, crawler_core runtime code, taxonomy importer code, parse code, and future Python files.

A Python file that hides important variable meaning or safety assumptions is not ready for commit.

### Türkçe

Her LogisticSearch Python dosyası, ilk kez okuyacak bir kişinin anlayacağı şekilde yazılmalıdır.

Her önemli değişken, fonksiyon, parametre, dataclass alanı, path sabiti, mode flag, sayaç, status değeri ve güvenlik guard'ı için ilgili satırın veya bloğun hemen üstünde detaylı iki dilli yorum bulunmalıdır.

Her yorum şunları açıklamalıdır:

- değişkenin/fonksiyonun/parametrenin ne olduğu,
- neden var olduğu,
- nasıl kullanıldığı,
- hangi değerlerin beklendiği,
- hangi değerlerin hatalı veya tehlikeli olduğu,
- hatalı değerlerde hangi failure davranışının beklenmesi gerektiği.

Bu kural source/startpoint/seed planner ve worker kodları, crawler_core runtime kodları, taxonomy importer kodları, parse kodları ve gelecekteki Python dosyaları için zorunludur.

Önemli değişken anlamını veya güvenlik varsayımını gizleyen Python dosyası commit için hazır değildir.
