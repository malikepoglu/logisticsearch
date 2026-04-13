# Parse Core SQL Surface

## Overview

This directory is the canonical repository surface for the real parse-core SQL layer of LogisticSearch. It preserves the imported live Pi51 parse PostgreSQL truth as evidence, while also providing the split, executable, and validated working SQL surface used for controlled evolution.

## Genel Bakış

Bu dizin, LogisticSearch'in gerçek parse-core SQL katmanı için kanonik repository yüzeyidir. İthal edilmiş canlı Pi51 parse PostgreSQL doğrusunu kanıt olarak korurken, kontrollü evrim için kullanılan split, çalıştırılabilir ve doğrulanmış çalışma SQL yüzeyini de sağlar.

## Purpose

This surface exists so that parse-core database logic is no longer trapped only inside the live Pi51 database. It gives the project a versioned, reviewable, auditable, executable, and evolvable SQL working layer centered on GitHub canonical main and Ubuntu Desktop execution discipline.

## Amaç

Bu yüzey, parse-core veritabanı mantığının artık yalnızca canlı Pi51 veritabanı içinde kapalı kalmaması için vardır. Projeye GitHub canonical main ve Ubuntu Desktop çalışma disiplini merkezli, versiyonlu, gözden geçirilebilir, denetlenebilir, çalıştırılabilir ve evrilebilir bir SQL çalışma katmanı kazandırır.

## Current File Map

### Live evidence surface
- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

### Primary working surface
- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

### Execution and validation entry points
- `900_apply_parse_core_split_surface.psql.sql`
- `901_preflight_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`
- `910_validate_parse_core_split_surface.sh`

### Planning, policy, and seal surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`

## Güncel Dosya Haritası

### Canlı kanıt yüzeyi
- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

### Ana çalışma yüzeyi
- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

### Execution ve validation giriş noktaları
- `900_apply_parse_core_split_surface.psql.sql`
- `901_preflight_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`
- `910_validate_parse_core_split_surface.sh`

### Planlama, politika ve mühür yüzeyi
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`

## Current Scope

The imported and split parse-core surface currently covers:

- schemas: 1
- enum types: 1
- tables: 4
- functions: 7
- inventory-visible indexes: 17

## Mevcut Kapsam

İthal edilmiş ve split edilmiş parse-core yüzeyi şu anda şunları kapsar:

- şema: 1
- enum type: 1
- tablo: 4
- fonksiyon: 7
- inventory'de görünen index: 17

## Current Validation Status

The split parse-core SQL surface has been validated successfully on Ubuntu Desktop against the local scratch PostgreSQL database:

- `logisticsearch_parse_core_split_scratch`

Validated result:
- crawler-core upstream dependency: passed
- parse preflight: passed
- parse apply bundle: passed
- parse presence audit: passed
- missing check count: 0

The live Pi51 crawler database was not mutated during this validation phase.

## Güncel Doğrulama Durumu

Split parse-core SQL yüzeyi, Ubuntu Desktop üzerinde yerel scratch PostgreSQL veritabanına karşı başarıyla doğrulanmıştır:

- `logisticsearch_parse_core_split_scratch`

Doğrulanan sonuç:
- crawler-core upstream bağımlılığı: geçti
- parse preflight: geçti
- parse apply bundle: geçti
- parse presence audit: geçti
- missing check count: 0

Bu doğrulama fazı sırasında canlı Pi51 crawler veritabanı değiştirilmemiştir.

## Working Model

The current working model is:

1. preserve the imported live snapshot as evidence
2. evolve the split SQL files as the primary working layer
3. satisfy crawler-core upstream dependency before clean parse apply
4. use `901` before parse apply
5. use `900` as the canonical parse split execution bundle
6. use `902` as the canonical reusable parse presence audit
7. use `910` as the reusable one-command parse scratch validation runner
8. re-run scratch validation after meaningful SQL changes

## Çalışma Modeli

Mevcut çalışma modeli şöyledir:

1. ithal edilmiş canlı snapshot'ı kanıt olarak koru
2. split SQL dosyalarını ana çalışma katmanı olarak evrimleştir
3. temiz parse apply öncesinde crawler-core upstream bağımlılığını sağla
4. parse apply öncesinde `901` kullan
5. kanonik parse split execution bundle olarak `900` kullan
6. kanonik reusable parse presence audit olarak `902` kullan
7. reusable tek-komut parse scratch validation runner olarak `910` kullan
8. anlamlı SQL değişikliklerinden sonra scratch doğrulamayı tekrar çalıştır

## Policy

The live snapshot remains comparison truth, but it is no longer the primary editing surface. Normal parse-core SQL evolution should start from the split working files on Ubuntu Desktop and then be versioned through GitHub canonical main.

## Politika

Canlı snapshot karşılaştırma doğrusu olarak önemini korur, ancak artık ana düzenleme yüzeyi değildir. Normal parse-core SQL evrimi Ubuntu Desktop üzerindeki split çalışma dosyalarından başlamalı ve sonra GitHub canonical main üzerinden versiyonlanmalıdır.
