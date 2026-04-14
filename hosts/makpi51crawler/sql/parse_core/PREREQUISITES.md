# Parse Core Prerequisites

## Overview

Before applying the parse-core split SQL surface to a database, the target environment must already satisfy the required upstream dependency contract.

## Genel Bakış

Parse-core split SQL yüzeyini bir veritabanına uygulamadan önce, hedef ortam gerekli upstream bağımlılık kontratını zaten sağlamış olmalıdır.

## Required upstream dependency

The current parse-core split surface is not standalone.

It depends on:
- schema `frontier`
- table `frontier.url`

This dependency exists because parse tables reference `frontier.url(url_id)` through foreign keys.

## Gerekli upstream bağımlılık

Mevcut parse-core split yüzeyi standalone değildir.

Şunlara bağlıdır:
- `frontier` şeması
- `frontier.url` tablosu

Bu bağımlılık, parse tablolarının foreign key üzerinden `frontier.url(url_id)` referanslamasından kaynaklanır.

## Execution order

The intended clean apply order is:

1. satisfy upstream crawler-core dependency first
2. run `901_preflight_parse_core_split_surface.psql.sql`
3. run `900_apply_parse_core_split_surface.psql.sql`
4. run `902_presence_audit_parse_core_split_surface.psql.sql`

## Çalıştırma sırası

Amaçlanan temiz apply sırası şudur:

1. önce upstream crawler-core bağımlılığını sağla
2. `901_preflight_parse_core_split_surface.psql.sql` çalıştır
3. `900_apply_parse_core_split_surface.psql.sql` çalıştır
4. `902_presence_audit_parse_core_split_surface.psql.sql` çalıştır

## Rule

Normal parse-core SQL evrimi split çalışma dosyalarından yürütülmelidir, ancak validation ve clean apply akışı crawler-core bağımlılığını açıkça hesaba katmalıdır.

## Kural

Normal parse-core SQL evrimi split çalışma dosyalarından yürütülmelidir; ancak validation ve clean apply akışı crawler-core bağımlılığını açıkça hesaba katmalıdır.
