# Desktop Import SQL Surface

## Overview

This directory is the canonical repository surface for the current `desktop_import` PostgreSQL layer on Ubuntu Desktop.

Its purpose is to preserve the live observed schema snapshot, keep the current executable contract visible in the repository, and prepare the surface for controlled future evolution.

## Genel Bakış

Bu dizin, Ubuntu Desktop üzerindeki mevcut `desktop_import` PostgreSQL katmanı için kanonik repository yüzeyidir.

Amacı, canlı gözlenen şema snapshot'ını korumak, mevcut çalıştırılabilir contract yüzeyini repository içinde görünür tutmak ve yüzeyi kontrollü gelecekteki evrim için hazırlamaktır.

## Current file map

### Live evidence surface
- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

### Primary working surface
- `001_pi51_batch_intake_contract.sql`

### Execution and validation entry points
- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

### Interpretation / decision surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `NEXT_STEP.md`

## Güncel dosya haritası

### Canlı kanıt yüzeyi
- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

### Ana çalışma yüzeyi
- `001_pi51_batch_intake_contract.sql`

### Execution ve validation giriş noktaları
- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

### Yorum / karar yüzeyi
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `NEXT_STEP.md`

## Current observed scope

The current live snapshot scope is:

- schemas: 1
- enum types: 0
- tables: 2
- functions: 0
- indexes: 3 in the schema dump surface
- indexes: 6 in the audited live/apply reality, because constraints materialize supporting index objects

Observed schema family:

- `desktop_import`

Observed tables:

- `desktop_import.batch_intake`
- `desktop_import.page_export_raw`

## Mevcut gözlenen kapsam

Mevcut canlı snapshot kapsamı şudur:

- şema: 1
- enum type: 0
- tablo: 2
- fonksiyon: 0
- indeks: dump yüzeyinde 3
- indeks: canlı/apply denetim gerçekliğinde 6; çünkü constraint'ler destekleyici index nesneleri üretir

Gözlenen şema ailesi:

- `desktop_import`

Gözlenen tablolar:

- `desktop_import.batch_intake`
- `desktop_import.page_export_raw`

## Surface meaning

This surface is import-oriented, not crawler-runtime-oriented.

It exists on Ubuntu Desktop to receive, persist, and inspect downstream imported material that originated from Pi51 export flow.

## Yüzeyin anlamı

Bu yüzey crawler-runtime odaklı değil, import odaklıdır.

Pi51 export akışından gelen downstream içeriği Ubuntu Desktop üzerinde almak, kalıcılaştırmak ve incelemek için vardır.

## Current interpretation

At the current point, the repository preserves four related layers:

1. the live schema snapshot truth
2. the executable contract truth
3. the execution/validation entry-point truth
4. the interpretation/decision truth

These should not be confused.

The live snapshot is evidence of current observed reality.  
The contract file is the primary working SQL surface.  
The 900/901/902/910 files are execution and validation helpers around that surface.

## Güncel yorum

Mevcut noktada repository birbiriyle ilişkili dört katmanı korur:

1. canlı şema snapshot doğruluğu
2. çalıştırılabilir contract doğruluğu
3. execution/validation giriş noktası doğruluğu
4. yorum/karar doğruluğu

Bunlar birbirine karıştırılmamalıdır.

Canlı snapshot, gözlenen mevcut gerçekliğin kanıtıdır.  
Contract dosyası ana çalışma SQL yüzeyidir.  
900/901/902/910 dosyaları ise bu yüzey etrafındaki execution ve validation yardımcılarıdır.

## Numbering convention

The current numbering convention is:

- `001...` = primary SQL / contract surface
- `900...` = canonical apply / execution bundle
- `901...` = preflight surface
- `902...` = presence audit surface
- `910...` = reusable one-command validation runner

## Numaralandırma kuralı

Mevcut numaralandırma kuralı şudur:

- `001...` = ana SQL / contract yüzeyi
- `900...` = kanonik apply / execution bundle
- `901...` = preflight yüzeyi
- `902...` = presence audit yüzeyi
- `910...` = reusable tek-komut validation runner

## Current rule

For now:

- preserve the snapshot files as evidence
- preserve the contract file as the primary working surface
- preserve the 900/901/902/910 layer as execution-surface truth
- avoid redundant transaction wrappers around a contract that already manages its own transaction
- validate through scratch before meaningful structural changes are trusted

## Güncel kural

Şimdilik:

- snapshot dosyalarını kanıt olarak koru
- contract dosyasını ana çalışma yüzeyi olarak koru
- 900/901/902/910 katmanını execution-surface doğruluğu olarak koru
- transaction'ını zaten kendi yöneten contract etrafına gereksiz transaction sarmalı ekleme
- anlamlı yapısal değişikliklere güvenmeden önce scratch üzerinden doğrula

## Immediate next documentation work

The next normal repository-side document after warning-free validation should be one of these:

- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`
- a final execution-surface audit/seal document

## Anlık sonraki dokümantasyon işi

Warning'siz doğrulamadan sonra sıradaki normal repository-side belge şu alanlardan biri olmalıdır:

- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`
- final execution-surface audit/seal belgesi
