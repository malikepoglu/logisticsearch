# Outbox Core SQL Surface

## Overview

This directory is the canonical repository surface for the real outbox-core SQL layer of LogisticSearch. It preserves the imported live Pi51 outbox-core PostgreSQL truth as evidence, while also providing the split, executable, and validated working SQL surface that is now used for controlled evolution.

## Genel Bakış

Bu dizin, LogisticSearch’in gerçek outbox-core SQL katmanı için kanonik repository yüzeyidir. İthal edilmiş canlı Pi51 outbox-core PostgreSQL doğrusunu kanıt olarak korurken, artık kontrollü evrim için kullanılan split, çalıştırılabilir ve doğrulanmış çalışma SQL yüzeyini de sağlar.

## Purpose

This surface exists so that outbox-core database logic is no longer trapped only inside the live Pi51 database. It gives the project a versioned, reviewable, auditable, executable, and evolvable SQL working layer centered on GitHub canonical main and Ubuntu Desktop execution discipline.

## Amaç

Bu yüzey, outbox-core veritabanı mantığının artık yalnızca canlı Pi51 veritabanı içinde kapalı kalmaması için vardır. Projeye GitHub canonical main ve Ubuntu Desktop çalışma disiplini merkezli, versiyonlu, gözden geçirilebilir, denetlenebilir, çalıştırılabilir ve evrilebilir bir SQL çalışma katmanı kazandırır.

## Current File Map

### Live evidence surface
- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

### Primary working surface
- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

### Execution and validation entry points
- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`
- `910_validate_outbox_core_split_surface.sh`

### Planning, policy, and seal surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`
- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`
- `FINAL_SURFACE_AUDIT_SEAL.md`
- `LIVE_OPERATIONAL_REALITY_AUDIT_2026-04-05.md`

## Güncel Dosya Haritası

### Canlı kanıt yüzeyi
- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

### Ana çalışma yüzeyi
- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

### Execution ve validation giriş noktaları
- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`
- `910_validate_outbox_core_split_surface.sh`

### Planlama, politika ve mühür yüzeyi
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`
- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`
- `FINAL_SURFACE_AUDIT_SEAL.md`
- `LIVE_OPERATIONAL_REALITY_AUDIT_2026-04-05.md`

## Current Scope

The imported and split outbox-core surface currently covers one schema:

- `outbox`

At the current sealed point, the covered object counts are:

- schemas: 1
- enum types: 2
- tables: 3
- functions: 7
- indexes: 10

## Mevcut Kapsam

İthal edilmiş ve split edilmiş outbox-core yüzeyi şu anda tek bir şemayı kapsar:

- `outbox`

Mevcut mühürlü noktada kapsanan nesne sayıları şunlardır:

- şema: 1
- enum type: 2
- tablo: 3
- fonksiyon: 7
- indeks: 10

## Upstream Dependency Model

The current outbox-core split surface is not standalone. It depends on these upstream relations already existing:

- `frontier.url`
- `parse.page_preranking_snapshot`
- `parse.page_workflow_status`

Validated scratch execution therefore requires:

1. crawler-core upstream prepared first
2. parse-core upstream prepared second
3. outbox-core preflight/apply/audit executed third

## Upstream Bağımlılık Modeli

Mevcut outbox-core split yüzeyi tek başına bağımsız değildir. Şu upstream ilişkilerin önceden var olmasına dayanır:

- `frontier.url`
- `parse.page_preranking_snapshot`
- `parse.page_workflow_status`

Bu nedenle doğrulanmış scratch çalıştırma sırası şöyledir:

1. önce crawler-core upstream hazırlanır
2. sonra parse-core upstream hazırlanır
3. ardından outbox-core preflight/apply/audit yürütülür

## Current Validation Status

The split outbox-core SQL surface has been validated successfully on Ubuntu Desktop against the local scratch PostgreSQL database:

- `logisticsearch_outbox_core_split_scratch`

Validated result:

- upstream dependency checks: passed
- preflight: passed
- apply bundle: passed
- reusable presence audit: passed
- reusable validation runner: passed
- missing check count: 0
- final repository-side surface audit: sealed
- live operational reality audit: documented

The live Pi51 crawler database was not mutated during this validation phase.

## Güncel Doğrulama Durumu

Split outbox-core SQL yüzeyi, Ubuntu Desktop üzerinde yerel scratch PostgreSQL veritabanına karşı başarıyla doğrulanmıştır:

- `logisticsearch_outbox_core_split_scratch`

Doğrulanan sonuç:

- upstream bağımlılık kontrolleri: geçti
- preflight: geçti
- apply bundle: geçti
- reusable presence audit: geçti
- reusable validation runner: geçti
- missing check count: 0
- final repository-side surface audit: mühürlendi
- canlı operasyonel gerçeklik denetimi: belgelendi

Bu doğrulama fazı sırasında canlı Pi51 crawler veritabanı değiştirilmemiştir.

## Working Model

The current working model is:

1. preserve the imported live snapshot as evidence
2. evolve the split SQL files as the primary working layer
3. use `901` before apply when validating a target database
4. use `900` as the canonical split execution bundle
5. use `902` as the canonical reusable presence audit
6. use `910` as the canonical one-command scratch validation runner
7. re-run scratch validation after meaningful SQL changes

## Çalışma Modeli

Mevcut çalışma modeli şöyledir:

1. ithal edilmiş canlı snapshot’ı kanıt olarak koru
2. split SQL dosyalarını ana çalışma katmanı olarak evrimleştir
3. bir hedef veritabanını doğrularken apply öncesinde `901` kullan
4. kanonik split execution bundle olarak `900` kullan
5. kanonik reusable presence audit olarak `902` kullan
6. kanonik tek-komut scratch validation runner olarak `910` kullan
7. anlamlı SQL değişikliklerinden sonra scratch doğrulamayı tekrar çalıştır

## Policy

The live snapshot remains comparison truth, but it is no longer the primary editing surface. Normal outbox-core SQL evolution should start from the split working files on Ubuntu Desktop and then be versioned through GitHub canonical main.

## Politika

Canlı snapshot karşılaştırma doğrusu olarak önemini korur, ancak artık ana düzenleme yüzeyi değildir. Normal outbox-core SQL evrimi Ubuntu Desktop üzerindeki split çalışma dosyalarından başlamalı ve sonra GitHub canonical main üzerinden versiyonlanmalıdır.
