# LogisticSearch Taxonomy Canonical JSON Source

## EN

This directory is the canonical source surface for LogisticSearch taxonomy language data.

PostgreSQL remains the runtime database. The JSON files here are the source of truth for language-specific taxonomy titles, searchable terms, and term-level metadata.

The current taxonomy JSON model is term-record-centric. Each record represents one real taxonomy term or phrase surface, not a nested node object. The core shared fields are `term_id`, `concept_id`, `hierarchy_id`, `unspsc_code`, `language`, `term`, `description`, `role`, `synonyms`, `is_searchable`, and `attributes`.

`hierarchy_id` is the canonical JSON field that replaces the older `node_code` name. Existing SQL/runtime history may still contain older terminology, but new canonical JSON language data must use `hierarchy_id`.

`concept_id` is the stable language-independent concept reference. It is shared across languages for the same taxonomy meaning.

`term_id` is the stable language-specific term record reference. It is unique per language/term surface and is the correct reference target for synonym arrays.

`synonyms` stores `term_id` references only. It must not embed free-text synonym strings directly.

### Current repository state

As of commit `831d5c0` (`feat(taxonomy): normalize canonical JSON model`), this taxonomy JSON surface intentionally contains 25 language JSON files under `hosts/makpi51crawler/taxonomy/languages/`.

Four language files are populated canonical JSON files:

1. `ar` Arabic
2. `de` German
3. `en` English
4. `tr` Turkish

Each populated language file currently contains 335 term records. Together, these four populated files contain 1,340 populated `term_id` records.

The remaining 21 language files are intentional controlled placeholders represented as empty JSON arrays (`[]`):

`bg`, `bn`, `cs`, `el`, `es`, `fr`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `ko`, `nl`, `pt`, `ro`, `ru`, `uk`, `ur`, `vi`, `zh`.

These placeholder files are not missing data, corrupt files, failed exports, or runtime-ready language datasets. They are explicit backlog placeholders kept so the repository already has the complete 25-language file surface and can be filled language by language under the same audited process.

### Runtime boundary

The JSON files are the canonical source surface, but PostgreSQL remains the runtime database for crawler/search execution.

The intended flow is:

1. Edit canonical JSON.
2. Validate JSON schema and deterministic rules.
3. Import JSON into a PostgreSQL scratch database.
4. Rebuild runtime taxonomy/search-document tables.
5. Export deterministic hashes and guard metrics.
6. Compare Desktop and pi51c scratch output.
7. Promote to live only by controlled scratch -> audit -> live swap.

The crawler/runtime code must not treat a placeholder language file as a populated runtime language. Placeholder files must be detected as controlled backlog state until they are filled and sealed.

### SQL boundary

Repair/patch SQL files are historical migration records. They are not the future canonical data model for language terms.

Future language-term data corrections should happen in canonical JSON first, then flow through validation, scratch import, deterministic audit, and controlled live promotion. SQL should be used for runtime schema, import/export machinery, deterministic audits, migrations, and controlled database operations, not as the primary long-term language-term editing surface.

### Ranking boundary

Ranking is intentionally not stored here yet.

Ranking will be a separate large design surface. It may later reference stable `concept_id`, `hierarchy_id`, and `term_id` values, but ranking weights, popularity scores, crawler-derived signals, and search scoring rules must not be mixed into this canonical taxonomy language-data README prematurely.

## TR

Bu dizin LogisticSearch taxonomy dil verilerinin kanonik JSON kaynak yüzeyidir.

PostgreSQL runtime veritabanı olarak kalır. Buradaki JSON dosyaları dil bazlı taxonomy başlıkları, aranabilir terimler ve terim-seviyesi metadata için ana doğruluk kaynağıdır.

Mevcut taxonomy JSON modeli term-record merkezlidir. Her kayıt bir gerçek taxonomy terimini veya ifade yüzeyini temsil eder; nested node objesi değildir. Ana ortak alanlar `term_id`, `concept_id`, `hierarchy_id`, `unspsc_code`, `language`, `term`, `description`, `role`, `synonyms`, `is_searchable` ve `attributes` alanlarıdır.

`hierarchy_id`, eski `node_code` adının yerine geçen kanonik JSON alanıdır. Mevcut SQL/runtime geçmişinde eski isimlendirme görülebilir, fakat yeni kanonik JSON dil verilerinde `hierarchy_id` kullanılmalıdır.

`concept_id`, dil bağımsız stabil anlam referansıdır. Aynı taxonomy anlamı için diller arasında ortak kalır.

`term_id`, dil bazlı stabil terim kayıt referansıdır. Her dil/terim yüzeyi için benzersizdir ve synonym array içinde referans verilmesi gereken doğru hedeftir.

`synonyms` yalnızca `term_id` referansları saklar. Doğrudan serbest metin eşanlamlı string gömülmemelidir.

### Mevcut repo durumu

`831d5c0` (`feat(taxonomy): normalize canonical JSON model`) commit'i itibarıyla bu taxonomy JSON yüzeyi bilinçli olarak `hosts/makpi51crawler/taxonomy/languages/` altında 25 dil JSON dosyası içerir.

Dört dil dosyası dolu kanonik JSON dosyasıdır:

1. `ar` Arapça
2. `de` Almanca
3. `en` İngilizce
4. `tr` Türkçe

Her dolu dil dosyasında şu anda 335 term kaydı vardır. Bu dört dolu dosyada toplam 1.340 dolu `term_id` kaydı vardır.

Kalan 21 dil dosyası bilinçli kontrollü placeholder dosyalarıdır ve boş JSON array (`[]`) olarak tutulur:

`bg`, `bn`, `cs`, `el`, `es`, `fr`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `ko`, `nl`, `pt`, `ro`, `ru`, `uk`, `ur`, `vi`, `zh`.

Bu placeholder dosyalar eksik veri, bozuk dosya, başarısız export veya runtime'a hazır dil dataset'i değildir. Bunlar 25 dilli dosya yüzeyinin repo içinde şimdiden tam görünmesi ve dillerin aynı denetimli süreçle tek tek doldurulması için tutulmuş açık backlog placeholder dosyalarıdır.

### Runtime sınırı

JSON dosyaları kanonik kaynak yüzeyidir, fakat crawler/search çalışması için PostgreSQL runtime veritabanı olarak kalır.

Hedef akış:

1. Kanonik JSON düzenlenir.
2. JSON schema ve deterministik kurallar doğrulanır.
3. JSON PostgreSQL scratch veritabanına import edilir.
4. Runtime taxonomy/search-document tabloları yeniden üretilir.
5. Deterministik hash ve guard metrics export alınır.
6. Desktop ve pi51c scratch çıktıları karşılaştırılır.
7. Canlı DB’ye geçiş sadece kontrollü scratch -> audit -> live swap disipliniyle yapılır.

Crawler/runtime kodu placeholder dil dosyasını dolu runtime dili gibi ele almamalıdır. Placeholder dosyalar doldurulup seal edilene kadar kontrollü backlog durumu olarak algılanmalıdır.

### SQL sınırı

Repair/patch SQL dosyaları geçmiş migration kayıtlarıdır. Dil terimleri için gelecekteki kanonik veri modeli değildir.

Gelecekteki dil-terim veri düzeltmeleri önce kanonik JSON içinde yapılmalı, sonra validation, scratch import, deterministic audit ve kontrollü live promotion akışından geçmelidir. SQL; runtime schema, import/export mekanizması, deterministik audit, migration ve kontrollü database operasyonları için kullanılmalıdır. Uzun vadeli ana dil-terim düzenleme yüzeyi SQL olmamalıdır.

### Ranking sınırı

Ranking bilgisi bilinçli olarak burada tutulmaz.

Ranking daha sonra ayrıca büyük bir tasarım yüzeyi olacaktır. İleride stabil `concept_id`, `hierarchy_id` ve `term_id` değerlerini referans alabilir; fakat ranking ağırlıkları, popülerlik puanları, crawler kaynaklı sinyaller ve search scoring kuralları bu kanonik taxonomy dil-verisi README içine erken karıştırılmamalıdır.
