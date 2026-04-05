# Outbox Core Scratch Apply Test Plan

## Overview

This document defines the next controlled validation step for the outbox-core split SQL surface.

The purpose is not to change the live Pi51 crawler database directly.  
The purpose is to validate that the split surface can be applied cleanly, in order, against a scratch PostgreSQL database after upstream prerequisites are satisfied.

## Genel Bakış

Bu belge, outbox-core split SQL yüzeyi için bir sonraki kontrollü doğrulama adımını tanımlar.

Amaç, canlı Pi51 crawler veritabanını doğrudan değiştirmek değildir.  
Amaç, upstream önkoşullar sağlandıktan sonra split yüzeyin scratch bir PostgreSQL veritabanına sıralı ve temiz şekilde uygulanabildiğini doğrulamaktır.

## Scope

Validation target:
- split working surface only

Validation source of truth:
- imported live snapshot remains the comparison truth

Expected upstream dependency base:
- crawler-core split surface applied
- parse-core split surface applied

## Kapsam

Doğrulama hedefi:
- yalnızca split çalışma yüzeyi

Doğrulama karşılaştırma doğrusu:
- ithal edilmiş canlı snapshot karşılaştırma doğrusu olarak korunur

Beklenen upstream bağımlılık tabanı:
- crawler-core split yüzeyi uygulanmış olmalı
- parse-core split yüzeyi uygulanmış olmalı

## Planned validation sequence

1. create a disposable scratch database
2. apply crawler-core validated surface
3. apply parse-core validated surface
4. confirm outbox prerequisites
5. run outbox preflight
6. run outbox apply bundle
7. inspect resulting schemas, types, tables, functions, and indexes
8. compare object-family counts with the imported live snapshot
9. drop the scratch database after validation unless intentionally preserved for further audit

## Planlanan doğrulama sırası

1. geçici bir scratch veritabanı oluştur
2. crawler-core doğrulanmış yüzeyini uygula
3. parse-core doğrulanmış yüzeyini uygula
4. outbox önkoşullarını doğrula
5. outbox preflight çalıştır
6. outbox apply bundle’ı çalıştır
7. ortaya çıkan şema, type, tablo, fonksiyon ve index’leri incele
8. nesne ailesi sayılarını ithal edilmiş canlı snapshot ile karşılaştır
9. daha ileri audit için özellikle korunmayacaksa scratch veritabanını sil

## Success criteria

A scratch apply test is considered successful when:

- upstream prerequisites are present
- preflight passes
- apply bundle completes without SQL errors
- the expected object-family counts are present
- no unplanned semantic drift is observed relative to the imported live snapshot

## Başarı ölçütleri

Bir scratch apply testi şu koşullarda başarılı kabul edilir:

- upstream önkoşullar mevcuttur
- preflight geçer
- apply bundle SQL hatası olmadan tamamlanır
- beklenen nesne ailesi sayıları oluşur
- ithal edilmiş canlı snapshot’a göre plansız semantik sapma görülmez
