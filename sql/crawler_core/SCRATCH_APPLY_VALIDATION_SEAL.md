# Crawler Core Scratch Apply Validation Seal

## Overview

This document records the successful scratch-database validation of the crawler-core split SQL surface.

The validation was performed on Ubuntu Desktop against a disposable local PostgreSQL scratch database.  
It was not applied to the live Pi51 crawler database.

## Genel Bakış

Bu belge, crawler-core split SQL yüzeyinin scratch veritabanı üzerindeki başarılı doğrulamasını kayda geçirir.

Doğrulama, Ubuntu Desktop üzerinde geçici yerel PostgreSQL scratch veritabanına karşı yapılmıştır.  
Canlı Pi51 crawler veritabanına uygulanmamıştır.

## Validated database

- scratch database name: `logisticsearch_crawler_split_scratch`

## Doğrulanan veritabanı

- scratch veritabanı adı: `logisticsearch_crawler_split_scratch`

## Validated execution path

The validated execution path was:

1. ensure `pgcrypto`
2. run `901_preflight_crawler_core_split_surface.psql.sql`
3. run `900_apply_crawler_core_split_surface.psql.sql`
4. inspect object presence in the scratch database

## Doğrulanan çalıştırma yolu

Doğrulanan çalıştırma yolu şuydu:

1. `pgcrypto` hazırla
2. `901_preflight_crawler_core_split_surface.psql.sql` çalıştır
3. `900_apply_crawler_core_split_surface.psql.sql` çalıştır
4. scratch veritabanında nesne varlığını incele

## Validation result

The split surface passed scratch validation successfully.

Validated presence result:
- prerequisite checks: OK
- schemas: 3 / 3
- enum types: 10 / 10
- tables: 6 / 6
- functions: 10 / 10
- indexes: 12 / 12
- missing check count: 0

## Doğrulama sonucu

Split yüzey scratch doğrulamasını başarıyla geçti.

Doğrulanan varlık sonucu:
- önkoşul kontrolleri: OK
- şemalar: 3 / 3
- enum type'lar: 10 / 10
- tablolar: 6 / 6
- fonksiyonlar: 10 / 10
- index'ler: 12 / 12
- missing check count: 0

## Current technical judgement

The crawler-core split SQL surface is now:

- coverage-complete for the imported crawler-core scope
- executable in the intended apply order
- validated on a disposable scratch PostgreSQL database
- ready for future controlled evolution from the split working surface

## Güncel teknik hüküm

Crawler-core split SQL yüzeyi artık:

- ithal edilmiş crawler-core kapsamı için coverage-complete durumdadır
- hedeflenen apply sırası ile çalıştırılabilirdir
- geçici scratch PostgreSQL veritabanında doğrulanmıştır
- split çalışma yüzeyi üzerinden gelecekteki kontrollü evrim için hazırdır

## Safety note

This validation phase did not mutate the live Pi51 crawler database.  
Pi51 remained the source of imported truth; Ubuntu Desktop remained the execution and validation surface.

## Güvenlik notu

Bu doğrulama fazı canlı Pi51 crawler veritabanını değiştirmemiştir.  
Pi51, ithal edilen doğrunun kaynağı olarak kalmış; Ubuntu Desktop ise çalıştırma ve doğrulama yüzeyi olmuştur.
