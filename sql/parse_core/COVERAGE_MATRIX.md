# Parse Core Coverage Matrix

## Overview

This document records the coverage relationship between the imported live Pi51 parse snapshot and the split primary working surface.

## Genel Bakış

Bu belge, ithal edilmiş canlı Pi51 parse snapshot’ı ile split ana çalışma yüzeyi arasındaki kapsama ilişkisini kayda geçirir.

## Evidence source

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`

## Kanıt kaynağı

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`

## Primary working surface

- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

## Ana çalışma yüzeyi

- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

## Coverage summary

### Schemas
Covered in:
- `001_parse_base.sql`

Objects:
- `parse`

### Types
Covered in:
- `001_parse_base.sql`

Objects:
- `parse.workflow_state_enum`

### Tables
Covered in:
- `001_parse_base.sql`

Objects:
- `parse.page_evidence_snapshot`
- `parse.page_preranking_snapshot`
- `parse.page_taxonomy_candidate`
- `parse.page_workflow_status`

### Functions
Covered in:
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

Objects:
- `parse.upsert_page_evidence_snapshot` -> `002_parse_evidence_and_candidate_upserts.sql`
- `parse.upsert_page_taxonomy_candidate` -> `002_parse_evidence_and_candidate_upserts.sql`
- `parse.persist_page_preranking_snapshot` -> `003_parse_preranking_persistence.sql`
- `parse.persist_page_taxonomy_candidates` -> `003_parse_preranking_persistence.sql`
- `parse.persist_page_taxonomy_preranking` -> `003_parse_preranking_persistence.sql`
- `parse.persist_taxonomy_preranking_payload` -> `004_parse_workflow_state_and_payload.sql`
- `parse.upsert_page_workflow_status` -> `004_parse_workflow_state_and_payload.sql`

### Inventory-visible indexes
Covered by validated split apply result:
- total index count: 17 / 17

## Kapsama özeti

### Şemalar
Şurada kapsanır:
- `001_parse_base.sql`

Nesneler:
- `parse`

### Type'lar
Şurada kapsanır:
- `001_parse_base.sql`

Nesneler:
- `parse.workflow_state_enum`

### Tablolar
Şurada kapsanır:
- `001_parse_base.sql`

Nesneler:
- `parse.page_evidence_snapshot`
- `parse.page_preranking_snapshot`
- `parse.page_taxonomy_candidate`
- `parse.page_workflow_status`

### Fonksiyonlar
Şurada kapsanır:
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

Nesneler:
- `parse.upsert_page_evidence_snapshot` -> `002_parse_evidence_and_candidate_upserts.sql`
- `parse.upsert_page_taxonomy_candidate` -> `002_parse_evidence_and_candidate_upserts.sql`
- `parse.persist_page_preranking_snapshot` -> `003_parse_preranking_persistence.sql`
- `parse.persist_page_taxonomy_candidates` -> `003_parse_preranking_persistence.sql`
- `parse.persist_page_taxonomy_preranking` -> `003_parse_preranking_persistence.sql`
- `parse.persist_taxonomy_preranking_payload` -> `004_parse_workflow_state_and_payload.sql`
- `parse.upsert_page_workflow_status` -> `004_parse_workflow_state_and_payload.sql`

### Inventory'de görünen index'ler
Doğrulanmış split apply sonucu ile kapsanır:
- toplam index sayısı: 17 / 17
