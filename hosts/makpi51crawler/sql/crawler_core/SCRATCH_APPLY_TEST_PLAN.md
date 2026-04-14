# Crawler Core Scratch Apply Test Plan

Documentation hub:

* `hosts/makpi51crawler/sql/README.md` — host-scoped SQL hub
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core surface hub
* `hosts/makpi51crawler/README.md` — host root for makpi51crawler
* `hosts/README.md` — host family root
* `README.md` — repository root surface
* `docs/README.md` — documentation hub

Dokümantasyon merkezi:

* `hosts/makpi51crawler/sql/README.md` — host-kapsamlı SQL merkezi
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core yüzey merkezi
* `hosts/makpi51crawler/README.md` — makpi51crawler host kökü
* `hosts/README.md` — host aile kökü
* `README.md` — repository kök yüzeyi
* `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This document supports the current `crawler_core` working surface under `hosts/makpi51crawler/sql/crawler_core/` and should be read as part of the controlled SECTION1 crawler_core line.

Bu belge, `hosts/makpi51crawler/sql/crawler_core/` altındaki mevcut `crawler_core` çalışma yüzeyini destekler ve kontrollü SECTION1 crawler_core hattının bir parçası olarak okunmalıdır.

## Current host-scoped path
## Güncel host-kapsamlı yol

At the current repository point, this surface lives under `hosts/makpi51crawler/sql/crawler_core/`.

Mevcut repository noktasında bu yüzey `hosts/makpi51crawler/sql/crawler_core/` altında yaşar.

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
