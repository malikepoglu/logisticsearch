# Parse Core Chronology Split Plan

## Overview

This document maps the imported live Pi51 parse schema snapshot to the next intended chronology-aligned SQL file layout.

Current structure source of truth:
- `001_pi51_live_parse_schema.sql`

Its purpose is to define a disciplined decomposition path without losing the verified live contract.

## Genel Bakış

Bu belge, ithal edilmiş canlı Pi51 parse şema snapshot’ını bir sonraki chronology uyumlu SQL dosya düzenine eşler.

Mevcut yapısal doğruluk kaynağı:
- `001_pi51_live_parse_schema.sql`

Amacı, doğrulanmış canlı kontratı kaybetmeden disiplinli bir parçalama yolu tanımlamaktır.

## Current live snapshot contents

### Types
- `parse.workflow_state_enum`

### Tables
- `parse.page_evidence_snapshot`
- `parse.page_preranking_snapshot`
- `parse.page_taxonomy_candidate`
- `parse.page_workflow_status`

### Functions
- `parse.persist_page_preranking_snapshot`
- `parse.persist_page_taxonomy_candidates`
- `parse.persist_page_taxonomy_preranking`
- `parse.persist_taxonomy_preranking_payload`
- `parse.upsert_page_evidence_snapshot`
- `parse.upsert_page_taxonomy_candidate`
- `parse.upsert_page_workflow_status`

### Indexes
- all parse indexes currently present in the imported live snapshot inventory

## Mevcut canlı snapshot içeriği

### Type'lar
- `parse.workflow_state_enum`

### Tablolar
- `parse.page_evidence_snapshot`
- `parse.page_preranking_snapshot`
- `parse.page_taxonomy_candidate`
- `parse.page_workflow_status`

### Fonksiyonlar
- `parse.persist_page_preranking_snapshot`
- `parse.persist_page_taxonomy_candidates`
- `parse.persist_page_taxonomy_preranking`
- `parse.persist_taxonomy_preranking_payload`
- `parse.upsert_page_evidence_snapshot`
- `parse.upsert_page_taxonomy_candidate`
- `parse.upsert_page_workflow_status`

### Index'ler
- ithal edilmiş canlı snapshot inventory içinde görülen tüm parse index'leri

## Intended chronology-aligned target layout

### 001_parse_base.sql
Contains:
- schema creation
- enum types
- base tables
- sequences
- constraints
- indexes

### 002_parse_evidence_and_candidate_upserts.sql
Contains:
- `parse.upsert_page_evidence_snapshot`
- `parse.upsert_page_taxonomy_candidate`

### 003_parse_preranking_persistence.sql
Contains:
- `parse.persist_page_preranking_snapshot`
- `parse.persist_page_taxonomy_candidates`
- `parse.persist_page_taxonomy_preranking`

### 004_parse_workflow_state_and_payload.sql
Contains:
- `parse.persist_taxonomy_preranking_payload`
- `parse.upsert_page_workflow_status`

## Hedef chronology uyumlu dosya düzeni

### 001_parse_base.sql
Şunları içerir:
- şema oluşturma
- enum type'lar
- temel tablolar
- sequence'ler
- constraint'ler
- index'ler

### 002_parse_evidence_and_candidate_upserts.sql
Şunları içerir:
- `parse.upsert_page_evidence_snapshot`
- `parse.upsert_page_taxonomy_candidate`

### 003_parse_preranking_persistence.sql
Şunları içerir:
- `parse.persist_page_preranking_snapshot`
- `parse.persist_page_taxonomy_candidates`
- `parse.persist_page_taxonomy_preranking`

### 004_parse_workflow_state_and_payload.sql
Şunları içerir:
- `parse.persist_taxonomy_preranking_payload`
- `parse.upsert_page_workflow_status`

## Rules

1. The imported live snapshot remains preserved as evidence.
2. Split files must not silently change semantics.
3. Dependency order must remain explicit and correct.
4. Any normalization beyond decomposition must be explicit and reviewable.

## Kurallar

1. İthal edilmiş canlı snapshot kanıt olarak korunur.
2. Split dosyaları semantiği sessizce değiştirmemelidir.
3. Bağımlılık sırası açık ve doğru kalmalıdır.
4. Parçalama dışındaki her normalizasyon açık ve gözden geçirilebilir olmalıdır.
