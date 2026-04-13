# Outbox Core Prerequisites

## Overview

Before applying the outbox-core split SQL surface to a database, the target database environment must satisfy a small but critical prerequisite set.

## Genel Bakış

Outbox-core split SQL yüzeyini bir veritabanına uygulamadan önce, hedef veritabanı ortamının küçük ama kritik bir önkoşul setini sağlaması gerekir.

## Required upstream schema assumptions

The current outbox-core split surface depends on these upstream relations already existing:

- `frontier.url`
- `parse.page_preranking_snapshot`
- `parse.page_workflow_status`

## Gerekli upstream şema varsayımları

Mevcut outbox-core split yüzeyi, şu upstream ilişkilerin önceden var olmasına bağlıdır:

- `frontier.url`
- `parse.page_preranking_snapshot`
- `parse.page_workflow_status`

## Required extension / type assumptions

The current outbox-core split surface also depends on:

- `jsonb`
- `now()`
- cross-schema foreign key resolution between `outbox`, `parse`, and `frontier`

## Gerekli extension / type varsayımları

Mevcut outbox-core split yüzeyi ayrıca şunlara dayanır:

- `jsonb`
- `now()`
- `outbox`, `parse` ve `frontier` arasındaki cross-schema foreign key çözümlemesi

## Execution model

The intended execution entry point will be:

- `900_apply_outbox_core_split_surface.psql.sql`

The intended safety model is:

1. run preflight first
2. confirm upstream prerequisites
3. only then run the apply bundle

## Çalıştırma modeli

Amaçlanan execution giriş noktası şu olacaktır:

- `900_apply_outbox_core_split_surface.psql.sql`

Amaçlanan güvenlik modeli şöyledir:

1. önce preflight çalıştır
2. upstream önkoşulları doğrula
3. ancak ondan sonra apply bundle’ı çalıştır
