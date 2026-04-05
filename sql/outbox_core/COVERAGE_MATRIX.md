# Outbox Core Coverage Matrix

## Overview

This document records the current coverage relationship between:

- the imported live Pi51 outbox snapshot
- the split working SQL surface
- the validated execution surface

## Genel Bakış

Bu belge, şu katmanlar arasındaki mevcut kapsama ilişkisini kayda geçirir:

- ithal edilmiş canlı Pi51 outbox snapshot'ı
- split çalışma SQL yüzeyi
- doğrulanmış execution yüzeyi

## Current scope summary

Current outbox-core scope at the sealed point:

- schemas: 1
- enum types: 2
- tables: 3
- functions: 7
- indexes: 10

## Güncel kapsam özeti

Mühürlü noktadaki mevcut outbox-core kapsamı:

- şema: 1
- enum type: 2
- tablo: 3
- fonksiyon: 7
- indeks: 10

## Coverage matrix

| Object family | Live snapshot count | Split surface count | Scratch-validated count | Status |
|---|---:|---:|---:|---|
| Schema | 1 | 1 | 1 | Covered |
| Enum type | 2 | 2 | 2 | Covered |
| Table | 3 | 3 | 3 | Covered |
| Function | 7 | 7 | 7 | Covered |
| Index | 10 | 10 | 10 | Covered |

## Kapsama matrisi

| Nesne ailesi | Canlı snapshot sayısı | Split yüzey sayısı | Scratch-doğrulanmış sayı | Durum |
|---|---:|---:|---:|---|
| Şema | 1 | 1 | 1 | Kapsanmış |
| Enum type | 2 | 2 | 2 | Kapsanmış |
| Tablo | 3 | 3 | 3 | Kapsanmış |
| Fonksiyon | 7 | 7 | 7 | Kapsanmış |
| İndeks | 10 | 10 | 10 | Kapsanmış |

## Split surface file mapping

### 001_outbox_base.sql
Covers:
- schema creation
- enum types
- tables
- sequences
- defaults
- primary key / unique constraints
- foreign keys
- indexes

### 002_outbox_enqueue_and_batch_creation.sql
Covers:
- `outbox.create_export_batch`
- `outbox.enqueue_page_export_item`

### 003_outbox_batch_attachment_and_state_transitions.sql
Covers:
- `outbox.attach_export_item_to_batch`
- `outbox.mark_export_batch_failed`
- `outbox.mark_export_batch_pushed`
- `outbox.mark_export_items_pushed_by_batch`
- `outbox.requeue_export_items_by_batch`

## Split yüzey dosya eşlemesi

### 001_outbox_base.sql
Şunları kapsar:
- şema oluşturma
- enum type'lar
- tablolar
- sequence'ler
- default'lar
- primary key / unique constraint'ler
- foreign key'ler
- indeksler

### 002_outbox_enqueue_and_batch_creation.sql
Şunları kapsar:
- `outbox.create_export_batch`
- `outbox.enqueue_page_export_item`

### 003_outbox_batch_attachment_and_state_transitions.sql
Şunları kapsar:
- `outbox.attach_export_item_to_batch`
- `outbox.mark_export_batch_failed`
- `outbox.mark_export_batch_pushed`
- `outbox.mark_export_items_pushed_by_batch`
- `outbox.requeue_export_items_by_batch`

## Validation interpretation

The current interpretation is:

1. the imported live snapshot remains the comparison truth
2. the split working surface fully covers the imported outbox-core scope
3. the split execution surface has been validated successfully on scratch
4. there is currently no known uncovered object family inside the imported outbox-core scope

## Doğrulama yorumu

Mevcut yorum şudur:

1. ithal edilmiş canlı snapshot karşılaştırma doğrusu olarak korunur
2. split çalışma yüzeyi, ithal edilmiş outbox-core kapsamını tam kapsar
3. split execution yüzeyi scratch üzerinde başarıyla doğrulanmıştır
4. şu anda ithal edilmiş outbox-core kapsamı içinde bilinen kapsanmamış nesne ailesi yoktur
