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

### Current executable contract surface
- `001_pi51_batch_intake_contract.sql`

### Interpretation / decision surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

## Güncel dosya haritası

### Canlı kanıt yüzeyi
- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

### Mevcut çalıştırılabilir contract yüzeyi
- `001_pi51_batch_intake_contract.sql`

## Current observed scope

The current live snapshot scope is:

- schemas: 1
- enum types: 0
- tables: 2
- functions: 0
- indexes: 3

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
- indeks: 3

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

At the current point, the repository preserves two different but related truths:

1. the live schema snapshot truth
2. the executable repository contract truth

These should not be confused.

The live snapshot is evidence of current observed reality.  
The contract file is the executable repository-side surface.

After the structural equivalence audit and primary-working-surface seal, the contract file is now also the confirmed primary working surface.

## Güncel yorum

Mevcut noktada repository birbiriyle ilişkili fakat farklı iki doğruluk katmanını korur:

1. canlı şema snapshot doğruluğu
2. çalıştırılabilir repository contract doğruluğu

Bunlar birbirine karıştırılmamalıdır.

Canlı snapshot, gözlenen mevcut gerçekliğin kanıtıdır.  
Contract dosyası ise çalıştırılabilir repository-side yüzeydir.

Yapısal eşdeğerlik denetimi ve ana çalışma yüzeyi mühründen sonra contract dosyası artık doğrulanmış ana çalışma yüzeyi haline gelmiştir.

## Current sealed interpretation result

The current documented result is now:

- chronology interpretation defined
- surface role separation defined
- structural equivalence between live snapshot and executable contract verified
- primary working surface decision sealed

## Güncel mühürlü yorum sonucu

Mevcut belgelenmiş sonuç artık şudur:

- kronoloji yorumu tanımlandı
- yüzey rol ayrımı tanımlandı
- canlı snapshot ile çalıştırılabilir contract arasındaki yapısal eşdeğerlik doğrulandı
- ana çalışma yüzeyi kararı mühürlendi

## Current rule

For now:

- preserve the snapshot files as evidence
- preserve the contract file as executable truth
- treat `001_pi51_batch_intake_contract.sql` as the primary working surface
- make future structural evolution there first
- re-audit when meaningful structural change happens

## Güncel kural

Şimdilik:

- snapshot dosyalarını kanıt olarak koru
- contract dosyasını çalıştırılabilir doğruluk olarak koru
- `001_pi51_batch_intake_contract.sql` dosyasını ana çalışma yüzeyi olarak ele al
- gelecekteki yapısal evrimi önce burada yap
- anlamlı yapısal değişiklik olduğunda yeniden denetle
