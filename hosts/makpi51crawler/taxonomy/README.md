# LogisticSearch Taxonomy Canonical JSON Source

## EN

This directory is the canonical source surface for LogisticSearch taxonomy language data.

PostgreSQL remains the runtime database. The JSON files here are the source of truth for language-specific taxonomy titles and searchable terms.

The intended flow is:

1. Edit canonical JSON.
2. Validate JSON schema and deterministic rules.
3. Import JSON into a PostgreSQL scratch database.
4. Rebuild runtime taxonomy/search-document tables.
5. Export deterministic hashes and guard metrics.
6. Compare Desktop and pi51c scratch output.
7. Promote to live only by controlled scratch -> audit -> live swap.

Repair/patch SQL files are historical migration records. They are not the future canonical data model.

Ranking is intentionally not stored here. Ranking will later reference stable taxonomy node IDs and term IDs.

## TR

Bu dizin LogisticSearch taxonomy dil verilerinin kanonik JSON kaynak yüzeyidir.

PostgreSQL runtime veritabanı olarak kalır. Buradaki JSON dosyaları dil bazlı taxonomy başlıkları ve aranabilir terimler için ana doğruluk kaynağıdır.

Hedef akış:

1. Kanonik JSON düzenlenir.
2. JSON schema ve deterministik kurallar doğrulanır.
3. JSON PostgreSQL scratch veritabanına import edilir.
4. Runtime taxonomy/search-document tabloları yeniden üretilir.
5. Deterministik hash ve guard metrics export alınır.
6. Desktop ve pi51c scratch çıktıları karşılaştırılır.
7. Canlı DB’ye geçiş sadece kontrollü scratch -> audit -> live swap disipliniyle yapılır.

Repair/patch SQL dosyaları geçmiş migration kayıtlarıdır. Gelecekteki kanonik veri modeli değildir.

Ranking bilgisi bilinçli olarak burada tutulmaz. Ranking daha sonra stable taxonomy node ID ve term ID değerlerini referans alacaktır.
