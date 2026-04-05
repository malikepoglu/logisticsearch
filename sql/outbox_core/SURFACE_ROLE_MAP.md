# Outbox Core Surface Role Map

## Overview

This document defines the role of each important file family inside the `sql/outbox_core` surface.

Its purpose is to prevent confusion between:

- imported live evidence
- split working SQL
- execution entry points
- validation / seal documents

## Genel Bakış

Bu belge, `sql/outbox_core` yüzeyi içindeki önemli dosya ailelerinin rolünü tanımlar.

Amacı, şu katmanlar arasındaki karışıklığı önlemektir:

- ithal edilmiş canlı kanıt
- split çalışma SQL'i
- execution giriş noktaları
- validation / seal belgeleri

## 1) Imported live evidence surface

These files preserve the imported live Pi51 outbox-core truth and must remain available for comparison:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

Role:

- evidence
- comparison baseline
- live contract reference

These files are not the primary editing surface.

## 1) İthal edilmiş canlı kanıt yüzeyi

Bu dosyalar, ithal edilmiş canlı Pi51 outbox-core doğrusunu korur ve karşılaştırma için elde tutulmalıdır:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

Rol:

- kanıt
- karşılaştırma tabanı
- canlı kontrat referansı

Bu dosyalar ana düzenleme yüzeyi değildir.

## 2) Primary split working surface

These files are the current primary SQL working layer for outbox-core evolution:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

Role:

- main editing surface
- controlled SQL evolution surface
- split chronology-aligned implementation surface

Future outbox-core SQL changes should start here, not from the imported live snapshot.

## 2) Ana split çalışma yüzeyi

Bu dosyalar, outbox-core evrimi için mevcut ana SQL çalışma katmanıdır:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

Rol:

- ana düzenleme yüzeyi
- kontrollü SQL evrim yüzeyi
- split chronology uyumlu uygulama yüzeyi

Gelecekteki outbox-core SQL değişiklikleri ithal edilmiş canlı snapshot’tan değil, buradan başlamalıdır.

## 3) Execution and validation entry surface

These files define how the split working surface is executed and validated:

- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`

Role:

- canonical apply entry point
- prerequisite verification entry point
- reusable presence verification entry point

These files make the split working surface executable and testable as a package.

## 3) Execution ve validation giriş yüzeyi

Bu dosyalar, split çalışma yüzeyinin nasıl çalıştırıldığını ve doğrulandığını tanımlar:

- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`

Rol:

- kanonik apply giriş noktası
- önkoşul doğrulama giriş noktası
- reusable varlık doğrulama giriş noktası

Bu dosyalar, split çalışma yüzeyini paket olarak çalıştırılabilir ve test edilebilir hale getirir.

## 4) Planning and interpretation surface

These files explain structure, sequencing, and meaning:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `NEXT_STEP.md`

Role:

- navigation
- planning
- interpretation
- future continuation guidance

These files explain the surface; they do not themselves define the executable SQL contract.

## 4) Planlama ve yorumlama yüzeyi

Bu dosyalar yapı, sıra ve anlam katmanını açıklar:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `NEXT_STEP.md`

Rol:

- gezinme
- planlama
- yorumlama
- gelecek devam rehberi

Bu dosyalar yüzeyi açıklar; yürütülebilir SQL kontratını doğrudan tanımlamaz.

## 5) Validation seal surface

These files record validated state:

- `SCRATCH_APPLY_VALIDATION_SEAL.md`

Role:

- successful validation record
- sealed checkpoint
- continuity anchor for future work

## 5) Validation seal yüzeyi

Bu dosyalar doğrulanmış durumu kayda geçirir:

- `SCRATCH_APPLY_VALIDATION_SEAL.md`

Rol:

- başarılı doğrulama kaydı
- mühürlü kontrol noktası
- gelecekteki iş için continuity dayanağı

## Current rule

For normal evolution work:

1. compare against imported live evidence when needed
2. edit the split working surface
3. validate through `900 / 901 / 902`
4. record the result in seal / guidance documents

## Güncel kural

Normal evrim çalışması için:

1. gerektiğinde ithal edilmiş canlı kanıt ile karşılaştır
2. split çalışma yüzeyini düzenle
3. `900 / 901 / 902` üzerinden doğrula
4. sonucu seal / rehber belgelerine işle
