# Outbox Core Chronology Split Plan

## Overview

This document maps the imported live Pi51 outbox schema snapshot to the next intended chronology-aligned SQL file layout.

Current structure source of truth:
- `001_pi51_live_outbox_schema.sql`

Its purpose is to define a disciplined decomposition path without losing the verified live contract.

## Genel Bakış

Bu belge, ithal edilmiş canlı Pi51 outbox şema snapshot’ını bir sonraki chronology uyumlu SQL dosya düzenine eşler.

Mevcut yapısal doğruluk kaynağı:
- `001_pi51_live_outbox_schema.sql`

Amacı, doğrulanmış canlı kontratı kaybetmeden disiplinli bir parçalama yolu tanımlamaktır.

## Current live snapshot contents

### Types
- `outbox.batch_state_enum`
- `outbox.export_state_enum`

### Tables
- `outbox.export_batch`
- `outbox.export_batch_item`
- `outbox.page_export_item`

### Functions
- `outbox.attach_export_item_to_batch`
- `outbox.create_export_batch`
- `outbox.enqueue_page_export_item`
- `outbox.mark_export_batch_failed`
- `outbox.mark_export_batch_pushed`
- `outbox.mark_export_items_pushed_by_batch`
- `outbox.requeue_export_items_by_batch`

### Indexes
- all outbox indexes currently present in the imported live snapshot inventory

## Mevcut canlı snapshot içeriği

### Enum Type'lar
- `outbox.batch_state_enum`
- `outbox.export_state_enum`

### Tablolar
- `outbox.export_batch`
- `outbox.export_batch_item`
- `outbox.page_export_item`

### Fonksiyonlar
- `outbox.attach_export_item_to_batch`
- `outbox.create_export_batch`
- `outbox.enqueue_page_export_item`
- `outbox.mark_export_batch_failed`
- `outbox.mark_export_batch_pushed`
- `outbox.mark_export_items_pushed_by_batch`
- `outbox.requeue_export_items_by_batch`

### İndeksler
- ithal edilmiş canlı snapshot inventory içinde görülen tüm outbox indeksleri

## Intended chronology-aligned target layout

### 001_outbox_base.sql
Contains:
- schema creation
- enum types
- base tables
- sequences
- defaults
- primary key / unique constraints
- foreign keys
- indexes

### 002_outbox_enqueue_and_batch_creation.sql
Contains:
- `outbox.create_export_batch`
- `outbox.enqueue_page_export_item`

### 003_outbox_batch_attachment_and_state_transitions.sql
Contains:
- `outbox.attach_export_item_to_batch`
- `outbox.mark_export_batch_failed`
- `outbox.mark_export_batch_pushed`
- `outbox.mark_export_items_pushed_by_batch`
- `outbox.requeue_export_items_by_batch`

## Rules

1. The imported live snapshot remains preserved as evidence.
2. Split files must not silently change semantics.
3. `001_outbox_base.sql` must be derived from the live structural truth, not from partial grep output.
4. Dependency order must remain explicit and correct.
5. Any normalization beyond decomposition must be explicit and reviewable.

## Kurallar

1. İthal edilmiş canlı snapshot kanıt olarak korunur.
2. Split dosyaları semantiği sessizce değiştirmemelidir.
3. `001_outbox_base.sql`, kısmi grep çıktısından değil, canlı yapısal doğruluk kaynağından türetilmelidir.
4. Bağımlılık sırası açık ve doğru kalmalıdır.
5. Parçalama dışındaki her normalizasyon açık ve gözden geçirilebilir olmalıdır.
