# Parse Core Primary Working Surface Seal

## Overview

Current sealed position:

- the imported live Pi51 parse snapshot remains preserved as evidence
- the split parse-core SQL files are now the primary working surface
- the apply/preflight/audit entry points define the controlled execution path
- this phase used Pi51 as a read-only truth source, not as the main editing surface

## Genel Bakış

Mevcut mühürlü konum:

- ithal edilmiş canlı Pi51 parse snapshot'ı kanıt olarak korunur
- split parse-core SQL dosyaları artık ana çalışma yüzeyidir
- apply/preflight/audit giriş noktaları kontrollü çalıştırma yolunu tanımlar
- bu fazda Pi51 ana düzenleme yüzeyi değil, read-only doğru kaynağı olarak kullanılmıştır

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

## Evidence surface

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

## Kanıt yüzeyi

- `001_pi51_live_parse_schema.sql`
- `001_pi51_live_parse_inventory.txt`
- `001_pi51_live_parse_schema.sha256`

## Rule

From this point forward, normal parse-core SQL evolution should target the split surface first. The imported live snapshot remains preserved as evidence and comparison truth.

## Kural

Bu noktadan sonra normal parse-core SQL evrimi önce split yüzeyi hedeflemelidir. İthal edilmiş canlı snapshot, kanıt ve karşılaştırma doğrusu olarak korunur.
