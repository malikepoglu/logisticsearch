# Desktop Import Surface Role Map

## Overview

This document defines the role of each important file family inside the `sql/desktop_import` surface.

Its purpose is to prevent confusion between:

- live observed schema evidence
- repository-side executable contract
- execution/validation entry points
- interpretation documents
- future evolution decisions

## Genel Bakış

Bu belge, `sql/desktop_import` yüzeyi içindeki önemli dosya ailelerinin rolünü tanımlar.

Amacı, şu katmanlar arasındaki karışıklığı önlemektir:

- canlı gözlenen şema kanıtı
- repository-side çalıştırılabilir contract
- execution/validation giriş noktaları
- yorum belgeleri
- gelecekteki evrim kararları

## 1) Live observed evidence surface

These files preserve the currently observed desktop_import schema reality from Ubuntu Desktop PostgreSQL:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Role:

- evidence
- comparison baseline
- observed live-state reference

These files are not automatically the main editable working surface.

## 1) Canlı gözlenen kanıt yüzeyi

Bu dosyalar, Ubuntu Desktop PostgreSQL üzerindeki şu anda gözlenen desktop_import şema gerçekliğini korur:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Rol:

- kanıt
- karşılaştırma tabanı
- gözlenen canlı durum referansı

Bu dosyalar otomatik olarak ana düzenlenebilir çalışma yüzeyi değildir.

## 2) Primary working surface

This file preserves the current repository-side executable intake contract:

- `001_pi51_batch_intake_contract.sql`

Role:

- primary working SQL surface
- executable repository contract
- hand-maintained structural contract

This file is now the main place for deliberate future structural evolution.

## 2) Ana çalışma yüzeyi

Bu dosya mevcut repository-side çalıştırılabilir intake contract'ını korur:

- `001_pi51_batch_intake_contract.sql`

Rol:

- ana çalışma SQL yüzeyi
- çalıştırılabilir repository contract'ı
- elde sürdürülen yapısal contract

Bu dosya artık bilinçli gelecekteki yapısal evrimin ana yeridir.

## 3) Execution and validation entry-point surface

These files wrap the primary working surface with reusable execution discipline:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

Role:

- execution bundle
- preflight inspection
- presence audit
- scratch validation automation

These files are not the primary structural truth themselves; they are controlled runners around that truth.

## 3) Execution ve validation giriş noktası yüzeyi

Bu dosyalar ana çalışma yüzeyini reusable execution disiplini ile sarar:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

Rol:

- execution bundle
- preflight incelemesi
- presence audit
- scratch validation otomasyonu

Bu dosyalar kendi başlarına ana yapısal doğruluk değildir; o doğruluğun etrafındaki kontrollü koşturuculardır.

## 4) Interpretation and decision surface

These files explain how the surface should currently be read:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`
- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Role:

- navigation
- chronology interpretation
- equivalence judgement
- primary-surface decision memory

These files explain the surface and record decisions, but they do not directly define executable database structure by themselves.

## 4) Yorum ve karar yüzeyi

Bu dosyalar yüzeyin şu anda nasıl okunması gerektiğini açıklar:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`
- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Rol:

- gezinme
- kronoloji yorumu
- eşdeğerlik hükmü
- ana yüzey karar hafızası

Bu dosyalar yüzeyi açıklar ve kararları kayda geçirir; fakat tek başlarına yürütülebilir veritabanı yapısını tanımlamazlar.

## Current rule

For now:

1. treat the snapshot files as observed live evidence
2. treat the contract file as the primary working repository surface
3. treat the 900/901/902/910 layer as the execution/validation layer
4. treat the interpretation docs as sealed reading guidance
5. avoid mixing these roles together

## Güncel kural

Şimdilik:

1. snapshot dosyalarını gözlenen canlı kanıt olarak ele al
2. contract dosyasını ana çalışma repository yüzeyi olarak ele al
3. 900/901/902/910 katmanını execution/validation katmanı olarak ele al
4. yorum belgelerini mühürlü okuma rehberi olarak ele al
5. bu rolleri birbirine karıştırma
