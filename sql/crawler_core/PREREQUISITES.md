# Crawler Core Prerequisites

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
