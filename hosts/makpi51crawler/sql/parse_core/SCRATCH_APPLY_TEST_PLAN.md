# Parse Core Scratch Apply Test Plan

## Overview

This document defines the controlled scratch-database validation step for the parse-core split SQL surface.

The purpose is not to mutate the live Pi51 crawler database.  
The purpose is to validate that the split parse-core surface can be applied cleanly after the required crawler-core upstream dependency is already present.

## Genel Bakış

Bu belge, parse-core split SQL yüzeyi için kontrollü scratch veritabanı doğrulama adımını tanımlar.

Amaç, canlı Pi51 crawler veritabanını değiştirmek değildir.  
Amaç, gerekli crawler-core upstream bağımlılığı zaten mevcutken split parse-core yüzeyinin temiz şekilde uygulanabildiğini doğrulamaktır.

## Scope

Validation target:
- parse-core split working surface

Validation dependency:
- crawler-core must already be applied in the target scratch database

Validation entry points:
- `901_preflight_parse_core_split_surface.psql.sql`
- `900_apply_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`

## Kapsam

Doğrulama hedefi:
- parse-core split çalışma yüzeyi

Doğrulama bağımlılığı:
- hedef scratch veritabanında crawler-core zaten uygulanmış olmalıdır

Doğrulama giriş noktaları:
- `901_preflight_parse_core_split_surface.psql.sql`
- `900_apply_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`

## Planned validation sequence

1. create a disposable scratch database
2. apply crawler-core validated split surface first
3. run parse-core preflight
4. run parse-core apply bundle
5. run parse-core presence audit
6. compare resulting object families against the imported live parse snapshot
7. keep or drop the scratch database depending on the current audit phase

## Planlanan doğrulama sırası

1. geçici bir scratch veritabanı oluştur
2. önce crawler-core doğrulanmış split yüzeyini uygula
3. parse-core preflight çalıştır
4. parse-core apply bundle çalıştır
5. parse-core presence audit çalıştır
6. ortaya çıkan nesne ailelerini ithal edilmiş canlı parse snapshot ile karşılaştır
7. mevcut audit fazına göre scratch veritabanını koru veya sil

## Success criteria

A scratch validation is successful when:
- crawler-core upstream dependency is present
- parse preflight passes
- parse apply bundle completes without SQL errors
- parse presence audit returns zero missing checks
- no unplanned structural drift is observed

## Başarı ölçütleri

Bir scratch doğrulaması şu koşullarda başarılı kabul edilir:
- crawler-core upstream bağımlılığı mevcuttur
- parse preflight geçer
- parse apply bundle SQL hatası olmadan tamamlanır
- parse presence audit sıfır missing check döner
- plansız yapısal sapma görülmez
