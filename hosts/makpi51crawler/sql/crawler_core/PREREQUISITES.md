# Crawler Core Prerequisites

Documentation hub:

* `hosts/makpi51crawler/sql/README.md` — host-scoped SQL hub
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core surface hub
* `hosts/makpi51crawler/README.md` — host root for makpi51crawler
* `hosts/README.md` — host family root
* `README.md` — repository root surface
* `docs/README.md` — documentation hub

Dokümantasyon merkezi:

* `hosts/makpi51crawler/sql/README.md` — host-kapsamlı SQL merkezi
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core yüzey merkezi
* `hosts/makpi51crawler/README.md` — makpi51crawler host kökü
* `hosts/README.md` — host aile kökü
* `README.md` — repository kök yüzeyi
* `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This document supports the current `crawler_core` working surface under `hosts/makpi51crawler/sql/crawler_core/` and should be read as part of the controlled SECTION1 crawler_core line.

Bu belge, `hosts/makpi51crawler/sql/crawler_core/` altındaki mevcut `crawler_core` çalışma yüzeyini destekler ve kontrollü SECTION1 crawler_core hattının bir parçası olarak okunmalıdır.

## Current host-scoped path
## Güncel host-kapsamlı yol

At the current repository point, this surface lives under `hosts/makpi51crawler/sql/crawler_core/`.

Mevcut repository noktasında bu yüzey `hosts/makpi51crawler/sql/crawler_core/` altında yaşar.

## Overview

Before applying the crawler-core split SQL surface to a database, the target database environment must satisfy a small set of prerequisites.

## Genel Bakış

Crawler-core split SQL yüzeyini bir veritabanına uygulamadan önce, hedef veritabanı ortamının küçük ama kritik bir önkoşul setini sağlaması gerekir.

## Required extension and function assumptions

The current split surface depends on:
- `pgcrypto`
- `gen_random_uuid()`
- `public.digest(...)`

This means the target database must have the `pgcrypto` extension installed, and `digest` must be resolvable from the `public` schema exactly as used by the imported live crawler-core truth.

## Gerekli extension ve fonksiyon varsayımları

Mevcut split surface şunlara bağlıdır:
- `pgcrypto`
- `gen_random_uuid()`
- `public.digest(...)`

Bu da hedef veritabanında `pgcrypto` extension’ının kurulu olması ve `digest` fonksiyonunun, ithal edilen canlı crawler-core doğrusunda kullanıldığı şekliyle `public` şemasından çözümlenebilmesi gerektiği anlamına gelir.

## Current dependency highlights

The split surface also relies on:
- UUID columns and UUID-returning helper usage
- JSONB columns and JSONB helper usage
- cross-schema references among `seed`, `frontier`, and `http_fetch`
- ordered apply behavior through the psql bundle

## Mevcut bağımlılık öne çıkanları

Split surface ayrıca şunlara dayanır:
- UUID kolonları ve UUID döndüren yardımcı kullanım
- JSONB kolonları ve JSONB yardımcı kullanımı
- `seed`, `frontier` ve `http_fetch` arasındaki cross-schema referanslar
- psql bundle üzerinden sıralı apply davranışı

## Execution model

The intended execution entry point is:
- `900_apply_crawler_core_split_surface.psql.sql`

The intended safety model is:
1. run preflight first
2. confirm prerequisites
3. only then run the apply bundle

## Çalıştırma modeli

Amaçlanan execution giriş noktası şudur:
- `900_apply_crawler_core_split_surface.psql.sql`

Amaçlanan güvenlik modeli şudur:
1. önce preflight çalıştır
2. önkoşulları doğrula
3. ancak ondan sonra apply bundle’ı çalıştır
