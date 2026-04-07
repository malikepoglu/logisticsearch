# SQL Surface

## Overview

This directory is intended for tracked SQL assets that belong in the canonical LogisticSearch repository. Its purpose is to hold durable database-side materials such as DDL, import logic, audit queries, validation queries, and other structured SQL content that should remain versioned, reviewable, and reusable.

## Genel Bakış

Bu dizin, kanonik LogisticSearch repository’sinde izlenmesi gereken SQL varlıkları için ayrılmıştır. Amacı; DDL, import mantığı, audit sorguları, doğrulama sorguları ve versiyonlu, gözden geçirilebilir ve yeniden kullanılabilir kalması gereken diğer yapısal SQL içeriklerini barındırmaktır.
## Policy

Only repository-worthy SQL should live here. Throwaway experiments, host-local scraps, temporary exports, and machine-specific runtime outputs should not accumulate inside this directory. The goal is to gradually shape this area into a clear and disciplined SQL surface.

## Politika

Burada yalnızca repository’ye girmeye değer SQL içerikleri yer almalıdır. Tek kullanımlık deneyler, host’a özel geçici parçalar, temporary export’lar ve makineye özgü runtime çıktıları bu dizinde birikmemelidir. Amaç bu alanı zamanla net ve disiplinli bir SQL yüzeyine dönüştürmektir.
## Documentation hub

Use these surfaces as the current hub / reading map around the SQL area:

- `README.md` — root repository entry surface
- `docs/README.md` — documentation hub and safest beginner reading map
- `sql/crawler_core/README.md` — crawler-core SQL working surface
- `sql/desktop_import/README.md` — desktop-import SQL intake surface
- `sql/outbox_core/README.md` — outbox-core SQL surface
- `sql/parse_core/README.md` — parse-core SQL surface

This file should be read as the SQL-area hub, not as a standalone isolated note.

## Dokümantasyon merkezi

SQL alanı etrafındaki mevcut merkez / okuma haritası olarak şu yüzeyleri kullan:

- `README.md` — repository kök giriş yüzeyi
- `docs/README.md` — dokümantasyon merkezi ve başlangıç için en güvenli okuma haritası
- `sql/crawler_core/README.md` — crawler-core SQL çalışma yüzeyi
- `sql/desktop_import/README.md` — desktop-import SQL intake yüzeyi
- `sql/outbox_core/README.md` — outbox-core SQL yüzeyi
- `sql/parse_core/README.md` — parse-core SQL yüzeyi

Bu dosya, tek başına izole bir not olarak değil, SQL alanının hub yüzeyi olarak okunmalıdır.

## Beginner-first reading path

If you are starting from zero, do **not** guess the SQL surface from filenames alone.

Use this order:

1. `README.md` — understand the repository-level direction first
2. `docs/README.md` — understand the documentation hub and reading model
3. `sql/README.md` — understand what the SQL surface is and is not
4. `sql/crawler_core/README.md` — understand the crawler-core SQL surface
5. `sql/desktop_import/README.md` — understand the desktop-import intake surface
6. `sql/outbox_core/README.md` — understand the outbox-core SQL surface
7. `sql/parse_core/README.md` — understand the parse-core SQL surface

## Başlangıç seviyesi okuma yolu

Sıfırdan başlıyorsan SQL yüzeyini yalnızca dosya adlarına bakarak tahmin etme.

Şu sırayı kullan:

1. `README.md` — önce repository seviyesindeki yönü anla
2. `docs/README.md` — dokümantasyon merkezini ve okuma modelini anla
3. `sql/README.md` — SQL yüzeyinin ne olduğunu ve ne olmadığını anla
4. `sql/crawler_core/README.md` — crawler-core SQL yüzeyini anla
5. `sql/desktop_import/README.md` — desktop-import intake yüzeyini anla
6. `sql/outbox_core/README.md` — outbox-core SQL yüzeyini anla
7. `sql/parse_core/README.md` — parse-core SQL yüzeyini anla

## Current tracked subsurfaces

At the current repository point, the main tracked SQL subsurfaces are:

- `sql/crawler_core/`
- `sql/desktop_import/`
- `sql/outbox_core/`
- `sql/parse_core/`

These are not interchangeable folders. Each one has its own bounded responsibility and should be read through its own README surface.

## Güncel izlenen alt yüzeyler

Mevcut repository noktasında ana izlenen SQL alt yüzeyleri şunlardır:

- `sql/crawler_core/`
- `sql/desktop_import/`
- `sql/outbox_core/`
- `sql/parse_core/`

Bunlar birbirinin yerine geçen klasörler değildir. Her birinin kendi sınırlı sorumluluğu vardır ve kendi README yüzeyi üzerinden okunmalıdır.

## Expected Direction

The likely long-term role of this directory includes schema definitions, import queries, audit checks, controlled transformations, and other database-side building blocks that support the LogisticSearch data pipeline.

## Beklenen Yön

Bu dizinin muhtemel uzun vadeli rolü; LogisticSearch veri hattını destekleyen şema tanımları, import sorguları, audit kontrolleri, kontrollü dönüşümler ve diğer veritabanı tarafı yapı taşlarını içermektir.
