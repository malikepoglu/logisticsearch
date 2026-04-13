# Parse Core Scratch Apply Validation Seal

## Overview

This document records the successful scratch-database validation of the parse-core split SQL surface.

The validation was performed on Ubuntu Desktop against a disposable local PostgreSQL scratch database after preparing the required crawler-core upstream dependency.  
It was not applied to the live Pi51 crawler database.

## Genel Bakış

Bu belge, parse-core split SQL yüzeyinin scratch veritabanı üzerindeki başarılı doğrulamasını kayda geçirir.

Doğrulama, gerekli crawler-core upstream bağımlılığı hazırlandıktan sonra Ubuntu Desktop üzerinde geçici yerel PostgreSQL scratch veritabanına karşı yapılmıştır.  
Canlı Pi51 crawler veritabanına uygulanmamıştır.

## Validated database

- scratch database name: `logisticsearch_parse_core_split_scratch`

## Doğrulanan veritabanı

- scratch veritabanı adı: `logisticsearch_parse_core_split_scratch`

## Validated execution path

1. prepare crawler-core upstream dependency in the scratch database
2. run `901_preflight_parse_core_split_surface.psql.sql`
3. run `900_apply_parse_core_split_surface.psql.sql`
4. run `902_presence_audit_parse_core_split_surface.psql.sql`

## Doğrulanan çalıştırma yolu

1. scratch veritabanında crawler-core upstream bağımlılığını hazırla
2. `901_preflight_parse_core_split_surface.psql.sql` çalıştır
3. `900_apply_parse_core_split_surface.psql.sql` çalıştır
4. `902_presence_audit_parse_core_split_surface.psql.sql` çalıştır

## Validation result

The split parse-core surface passed scratch validation successfully.

Validated presence result:
- upstream dependency: OK
- schemas: 1 / 1
- enum types: 1 / 1
- tables: 4 / 4
- functions: 7 / 7
- inventory-visible indexes: 17 / 17
- missing check count: 0

## Doğrulama sonucu

Split parse-core yüzeyi scratch doğrulamasını başarıyla geçti.

Doğrulanan varlık sonucu:
- upstream bağımlılık: OK
- şemalar: 1 / 1
- enum type'lar: 1 / 1
- tablolar: 4 / 4
- fonksiyonlar: 7 / 7
- inventory'de görünen index'ler: 17 / 17
- missing check count: 0

## Safety note

This validation phase did not mutate the live Pi51 crawler database.  
Pi51 remained the source of imported truth; Ubuntu Desktop remained the execution and validation surface.

## Güvenlik notu

Bu doğrulama fazı canlı Pi51 crawler veritabanını değiştirmemiştir.  
Pi51, ithal edilen doğrunun kaynağı olarak kalmış; Ubuntu Desktop ise çalıştırma ve doğrulama yüzeyi olmuştur.
