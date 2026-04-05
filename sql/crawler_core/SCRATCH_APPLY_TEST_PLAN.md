# Crawler Core Scratch Apply Test Plan

## Overview

This document defines the next controlled validation step for the crawler-core split SQL surface.

The purpose is not to change the live Pi51 crawler database directly.  
The purpose is to validate that the split surface can be applied cleanly, in order, against a scratch PostgreSQL database after preflight succeeds.

## Genel Bakış

Bu belge, crawler-core split SQL yüzeyi için bir sonraki kontrollü doğrulama adımını tanımlar.

Amaç, canlı Pi51 crawler veritabanını doğrudan değiştirmek değildir.  
Amaç, preflight başarıyla geçtikten sonra split yüzeyin scratch bir PostgreSQL veritabanına sıralı ve temiz şekilde uygulanabildiğini doğrulamaktır.

## Scope

Validation target:
- split working surface only

Validation entry points:
- `901_preflight_crawler_core_split_surface.psql.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

Validation source of truth:
- imported live snapshot remains the comparison truth

## Kapsam

Doğrulama hedefi:
- yalnızca split çalışma yüzeyi

Doğrulama giriş noktaları:
- `901_preflight_crawler_core_split_surface.psql.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

Doğrulama karşılaştırma doğrusu:
- ithal edilmiş canlı snapshot karşılaştırma doğrusu olarak korunur

## Planned validation sequence

1. create a disposable scratch database
2. ensure required extension assumptions are satisfied
3. run preflight
4. run split apply bundle
5. inspect resulting schemas, types, tables, functions, and indexes
6. compare object-family counts with the imported live snapshot
7. drop the scratch database after validation unless intentionally preserved for further audit

## Planlanan doğrulama sırası

1. geçici bir scratch veritabanı oluştur
2. gerekli extension varsayımlarının sağlandığını doğrula
3. preflight çalıştır
4. split apply bundle’ı çalıştır
5. ortaya çıkan şema, type, tablo, fonksiyon ve index’leri incele
6. nesne ailesi sayılarını ithal edilmiş canlı snapshot ile karşılaştır
7. daha ileri audit için özellikle korunmayacaksa scratch veritabanını sil

## Safety model

- do not target the live Pi51 crawler database
- do not mutate the imported evidence files
- use the split working surface as the executable layer
- keep the operation reversible and disposable

## Güvenlik modeli

- canlı Pi51 crawler veritabanını hedefleme
- ithal edilmiş kanıt dosyalarını değiştirme
- çalıştırılabilir katman olarak split çalışma yüzeyini kullan
- işlemi geri alınabilir ve geçici tut

## Success criteria

A scratch apply test is considered successful when:
- preflight passes
- apply bundle completes without SQL errors
- the expected object-family counts are present
- dependency assumptions are satisfied
- no unplanned semantic drift is observed relative to the imported live snapshot

## Başarı ölçütleri

Bir scratch apply testi şu koşullarda başarılı kabul edilir:
- preflight geçer
- apply bundle SQL hatası olmadan tamamlanır
- beklenen nesne ailesi sayıları oluşur
- bağımlılık varsayımları sağlanır
- ithal edilmiş canlı snapshot’a göre plansız semantik sapma görülmez
