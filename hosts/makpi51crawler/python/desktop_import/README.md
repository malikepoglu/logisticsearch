# Python Desktop Import Surface

## What this folder is

This folder is the current Python-side helper surface for the Desktop import flow in LogisticSearch.

It exists to support the path from imported Pi51 batch artifacts into the Desktop-side database intake surface.

At the current repository point, this folder is intentionally small.

It does **not** contain a full Python package, service, worker fleet, or general-purpose ingestion framework.

It currently contains one focused helper script and should be read that way.

## Bu klasör nedir

Bu klasör, LogisticSearch içindeki Desktop import akışının mevcut Python-tarafı yardımcı yüzeyidir.

Amacı, Pi51’den içe alınan batch artefact’larından Desktop-tarafı veritabanı intake yüzeyine giden yolu desteklemektir.

Mevcut repository noktasında bu klasör bilinçli olarak küçüktür.

Tam bir Python paketi, servis, worker filosu veya genel amaçlı ingestion framework içermez.

Şu anda tek bir odaklı yardımcı script içerir ve bu şekilde okunmalıdır.

## Current judgement

At the current repository point, this directory is a real repo surface and therefore deserves an explicit README.

However, its current scope is still narrow:

- one script
- one specific import path
- one clearly bounded purpose

This README must describe the current truth precisely and must not invent broader behavior that does not yet exist.

## Mevcut hüküm

Mevcut repository noktasında bu dizin gerçek bir repo yüzeyidir ve bu nedenle açık bir README’yi hak eder.

Ancak mevcut kapsamı hâlâ dardır:

- tek script
- tek belirli import yolu
- açıkça sınırlandırılmış tek amaç

Bu README mevcut gerçeği tam olarak anlatmalı ve henüz var olmayan daha geniş davranışlar uydurmamalıdır.

## Current file map

Current file map in this folder:

- `load_pi51_batch_into_postgres.py`

There is currently no second helper, package initializer, tests subfolder, or local README-independent execution framework in this directory.

## Mevcut dosya haritası

Bu klasördeki mevcut dosya haritası:

- `load_pi51_batch_into_postgres.py`

Bu dizinde şu anda ikinci bir yardımcı script, package initializer, test alt klasörü veya README’den bağımsız yerel execution framework’ü yoktur.

## Primary file today

The primary and only current working file is:

- `load_pi51_batch_into_postgres.py`

Despite the filename, the current script truth is important:

it does **not** directly open a PostgreSQL connection and push rows into PostgreSQL.

Instead, it reads a prepared import directory and materializes TSV files that are then suitable for the Desktop-side SQL intake flow.

That distinction matters and must remain documented clearly.

## Bugünkü ana dosya

Bugünkü ana ve tek çalışma dosyası şudur:

- `load_pi51_batch_into_postgres.py`

Dosya adına rağmen mevcut script gerçeği önemlidir:

script şu anda doğrudan PostgreSQL bağlantısı açıp satırları PostgreSQL’e basmaz.

Bunun yerine hazırlanmış bir import dizinini okur ve daha sonra Desktop-tarafı SQL intake akışına uygun TSV dosyaları üretir.

Bu ayrım önemlidir ve açık biçimde dokümante edilmiş olarak kalmalıdır.

## What the script currently does

At the current repository point, the script:

1. expects exactly one argument: an import directory
2. reads these JSON inputs from that directory:
   - `batch.json`
   - `manifest.json`
   - `PUSH_RECEIPT.json`
   - `IMPORT_RECEIPT.json`
3. normalizes batch item shape
4. extracts import metadata and item-level fields
5. writes these TSV outputs into the same import directory:
   - `_desktop_import_batch_intake.tsv`
   - `_desktop_import_page_export_raw.tsv`
6. prints summary lines such as:
   - `BATCH_KEY=...`
   - `ITEM_COUNT_EXPECTED=...`
   - `ITEM_COUNT_LOADED=...`
   - output TSV paths

This is the current truth of the script surface.

## Script şu anda ne yapıyor

Mevcut repository noktasında script şunları yapar:

1. tam olarak bir argüman bekler: bir import dizini
2. o dizinden şu JSON girdilerini okur:
   - `batch.json`
   - `manifest.json`
   - `PUSH_RECEIPT.json`
   - `IMPORT_RECEIPT.json`
3. batch item yapısını normalize eder
4. import metadata’sını ve item-seviyesi alanları çıkarır
5. aynı import dizini içine şu TSV çıktıları yazar:
   - `_desktop_import_batch_intake.tsv`
   - `_desktop_import_page_export_raw.tsv`
6. şu tür özet satırlarını basar:
   - `BATCH_KEY=...`
   - `ITEM_COUNT_EXPECTED=...`
   - `ITEM_COUNT_LOADED=...`
   - çıktı TSV yolları

Script yüzeyinin mevcut doğrusu budur.

## What this surface is for

This Python surface exists to bridge structured imported batch artifacts into a Desktop-side tabular form that can be consumed by the SQL intake surface.

In simpler terms:

- imported JSON-like batch artifacts come in
- deterministic TSV files come out
- those TSV files belong to the downstream Desktop SQL import path

This makes the Python surface a conversion/preparation layer, not the final DB-ingestion truth by itself.

## Bu yüzey ne içindir

Bu Python yüzeyi, yapılandırılmış içe alınmış batch artefact’larını Desktop-tarafında SQL intake yüzeyinin tüketebileceği tablo-biçimli bir forma köprülemek için vardır.

Daha sade söylersek:

- içe alınmış JSON-benzeri batch artefact’ları içeri girer
- deterministik TSV dosyaları dışarı çıkar
- bu TSV dosyaları aşağı akış Desktop SQL import yoluna aittir

Bu nedenle Python yüzeyi kendi başına nihai DB-ingestion doğrusu değil, bir dönüştürme/hazırlama katmanıdır.

## Relation to sql/desktop_import

This directory should be read together with:

- `hosts/makpi51crawler/sql/desktop_import/README.md`
- the `sql/desktop_import` execution and validation surface

Current relationship model:

- `python/desktop_import` prepares structured tabular artifacts
- `sql/desktop_import` defines the canonical SQL-side intake surface

So the Python helper is upstream preparation logic, while the SQL surface remains the authoritative database-application layer for Desktop import.

## sql/desktop_import ile ilişkisi

Bu dizin şu yüzeylerle birlikte okunmalıdır:

- `hosts/makpi51crawler/sql/desktop_import/README.md`
- `sql/desktop_import` execution ve validation yüzeyi

Mevcut ilişki modeli şöyledir:

- `python/desktop_import`, yapılandırılmış tablo artefact’larını hazırlar
- `sql/desktop_import`, kanonik SQL-tarafı intake yüzeyini tanımlar

Dolayısıyla Python helper yukarı-akış hazırlık mantığıdır; SQL yüzeyi ise Desktop import için yetkili veritabanı uygulama katmanı olarak kalır.

## Beginner-first reading path

If you are starting from zero, use this order:

1. `docs/README.md`
   Start from the docs hub to understand the repository reading map.

2. `docs/TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
   Read the numbering discipline so the repository surface makes structural sense.

3. `hosts/makpi51crawler/sql/desktop_import/README.md`
   Understand the SQL-side intake surface first.

4. `hosts/makpi51crawler/python/desktop_import/README.md`
   Then read this file to understand the Python preparation layer.

5. `hosts/makpi51crawler/python/desktop_import/load_pi51_batch_into_postgres.py`
   Only after the surrounding context is clear, read the actual script.

Do **not** start by guessing from the Python filename alone.

## Başlangıç seviyesi okuma yolu

Sıfırdan başlıyorsan şu sırayı kullan:

1. `docs/README.md`
   Repository okuma haritasını anlamak için docs hub’dan başla.

2. `docs/TOPIC_REPOSITORY_ARTIFACT_NUMBERING_STANDARD.md`
   Repository yüzeyinin yapısal olarak anlamlı olması için numaralandırma disiplinini oku.

3. `hosts/makpi51crawler/sql/desktop_import/README.md`
   Önce SQL-tarafı intake yüzeyini anla.

4. `hosts/makpi51crawler/python/desktop_import/README.md`
   Sonra Python hazırlık katmanını anlamak için bu dosyayı oku.

5. `hosts/makpi51crawler/python/desktop_import/load_pi51_batch_into_postgres.py`
   Yalnızca çevresel bağlam netleştikten sonra gerçek script’i oku.

Yalnızca Python dosya adından tahmin yürütüp başlamamalısın.

## Scope boundaries

Current in scope for this folder:

- the single current helper script
- its exact current input/output behavior
- its role in the Desktop import preparation chain
- its relationship to `sql/desktop_import`

Current out of scope for this folder:

- invented future Python architecture
- background workers that do not yet exist here
- packaging claims that are not yet true
- test coverage claims that are not yet true
- pretending that this folder is already a full ingestion subsystem

## Kapsam sınırları

Bu klasör için mevcut kapsam içi konular:

- mevcut tek yardımcı script
- script’in tam mevcut girdi/çıktı davranışı
- Desktop import hazırlık zincirindeki rolü
- `sql/desktop_import` ile ilişkisi

Bu klasör için mevcut kapsam dışı konular:

- uydurulmuş gelecek Python mimarisi
- burada henüz var olmayan background worker’lar
- henüz doğru olmayan packaging iddiaları
- henüz doğru olmayan test coverage iddiaları
- bu klasör zaten tam ingestion subsystem’miş gibi davranmak

## Update discipline

Whenever this folder changes, the maintainer should ask:

1. did the file map change
2. did the real script behavior change
3. did input expectations change
4. did output artifacts change
5. did the relationship to `sql/desktop_import` change
6. does this README still describe reality exactly

If the answer to any of those is yes, this README should be updated in the same work package.

## Güncelleme disiplini

Bu klasör her değiştiğinde bakımcı şu soruları sormalıdır:

1. dosya haritası değişti mi
2. script’in gerçek davranışı değişti mi
3. girdi beklentileri değişti mi
4. çıktı artefact’ları değişti mi
5. `sql/desktop_import` ile ilişki değişti mi
6. bu README hâlâ gerçeği tam olarak anlatıyor mu

Bu sorulardan herhangi birine cevap evetse, bu README aynı iş paketi içinde güncellenmelidir.

## Documentation hub

- `docs/README.md` — use this as the root reading map for the documentation set.

## Dokümantasyon merkezi

- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.
