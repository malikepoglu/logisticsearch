# Outbox Core Scratch Apply Validation Seal

## Overview

This document records the successful scratch-database validation of the outbox-core split SQL surface.

The validation was performed on Ubuntu Desktop against a disposable local PostgreSQL scratch database.  
It was not applied to the live Pi51 crawler database.

## Genel Bakış

Bu belge, outbox-core split SQL yüzeyinin scratch veritabanı üzerindeki başarılı doğrulamasını kayda geçirir.

Doğrulama, Ubuntu Desktop üzerinde geçici yerel PostgreSQL scratch veritabanına karşı yapılmıştır.  
Canlı Pi51 crawler veritabanına uygulanmamıştır.

## Validated database

- scratch database name: `logisticsearch_outbox_core_split_scratch`

## Doğrulanan veritabanı

- scratch veritabanı adı: `logisticsearch_outbox_core_split_scratch`

## Validated execution path

The validated execution path was:

1. prepare crawler-core upstream on the scratch database
2. prepare parse-core upstream on the scratch database
3. run `901_preflight_outbox_core_split_surface.psql.sql`
4. run `900_apply_outbox_core_split_surface.psql.sql`
5. inspect object presence with `902_presence_audit_outbox_core_split_surface.psql.sql`

## Doğrulanan çalıştırma yolu

Doğrulanan çalıştırma yolu şuydu:

1. scratch veritabanında crawler-core upstream katmanını hazırla
2. scratch veritabanında parse-core upstream katmanını hazırla
3. `901_preflight_outbox_core_split_surface.psql.sql` çalıştır
4. `900_apply_outbox_core_split_surface.psql.sql` çalıştır
5. `902_presence_audit_outbox_core_split_surface.psql.sql` ile nesne varlığını incele

## Validation result

The outbox-core split surface passed scratch validation successfully.

Validated presence result:
- required upstream dependency checks: OK
- schemas: 1 / 1
- enum types: 2 / 2
- tables: 3 / 3
- functions: 7 / 7
- indexes: 10 / 10
- missing check count: 0

## Doğrulama sonucu

Outbox-core split yüzey scratch doğrulamasını başarıyla geçti.

Doğrulanan varlık sonucu:
- gerekli upstream bağımlılık kontrolleri: OK
- şemalar: 1 / 1
- enum type'lar: 2 / 2
- tablolar: 3 / 3
- fonksiyonlar: 7 / 7
- index'ler: 10 / 10
- missing check count: 0

## Current technical judgement

The outbox-core split SQL surface is now:

- coverage-complete for the imported outbox-core scope
- executable in the intended apply order
- validated on a disposable scratch PostgreSQL database with required upstream layers
- ready for future controlled evolution from the split working surface

## Güncel teknik hüküm

Outbox-core split SQL yüzeyi artık:

- ithal edilmiş outbox-core kapsamı için coverage-complete durumdadır
- hedeflenen apply sırası ile çalıştırılabilirdir
- gerekli upstream katmanlarla birlikte geçici scratch PostgreSQL veritabanında doğrulanmıştır
- split çalışma yüzeyi üzerinden gelecekteki kontrollü evrim için hazırdır

## Safety note

This validation phase did not mutate the live Pi51 crawler database.  
Pi51 remained the source of imported truth; Ubuntu Desktop remained the execution and validation surface.

## Güvenlik notu

Bu doğrulama fazı canlı Pi51 crawler veritabanını değiştirmemiştir.  
Pi51, ithal edilen doğrunun kaynağı olarak kalmış; Ubuntu Desktop ise çalıştırma ve doğrulama yüzeyi olmuştur.
