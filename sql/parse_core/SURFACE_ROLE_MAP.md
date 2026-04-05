# Parse Core Surface Role Map

## Overview

This document defines the role of each major file family inside `sql/parse_core`.

## Genel Bakış

Bu belge, `sql/parse_core` içindeki ana dosya ailelerinin rolünü tanımlar.

## Live evidence surface

These files preserve imported live Pi51 parse truth as evidence:

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

## Canlı kanıt yüzeyi

Bu dosyalar ithal edilmiş canlı Pi51 parse doğrusunu kanıt olarak korur:

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

## Planning surface

These files define how the imported live snapshot is decomposed and governed:

- `CHRONOLOGY_SPLIT_PLAN.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`

## Planlama yüzeyi

Bu dosyalar, ithal edilmiş canlı snapshot’ın nasıl parçalandığını ve yönetildiğini tanımlar:

- `CHRONOLOGY_SPLIT_PLAN.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`

## Primary working surface

These are the main editable split SQL files for future controlled evolution:

- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

## Ana çalışma yüzeyi

Bunlar gelecekteki kontrollü evrim için ana düzenlenebilir split SQL dosyalarıdır:

- `001_parse_base.sql`
- `002_parse_evidence_and_candidate_upserts.sql`
- `003_parse_preranking_persistence.sql`
- `004_parse_workflow_state_and_payload.sql`

## Execution and validation surface

These files are the execution and validation entry points:

- `900_apply_parse_core_split_surface.psql.sql`
- `901_preflight_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`
- `910_validate_parse_core_split_surface.sh`

## Çalıştırma ve doğrulama yüzeyi

Bu dosyalar çalıştırma ve doğrulama giriş noktalarıdır:

- `900_apply_parse_core_split_surface.psql.sql`
- `901_preflight_parse_core_split_surface.psql.sql`
- `902_presence_audit_parse_core_split_surface.psql.sql`
- `910_validate_parse_core_split_surface.sh`

## Seal and navigation surface

These files record validated position, coverage, and next continuation direction:

- `README.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`

## Mühür ve navigasyon yüzeyi

Bu dosyalar doğrulanmış konumu, kapsamı ve sonraki devam yönünü kayda geçirir:

- `README.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`
