# Desktop Import Chronology Split Plan

## Overview

This document defines the current chronology interpretation for the `sql/desktop_import` surface.

Unlike crawler-core, parse-core, or outbox-core, this surface did not begin as a fully split primary-working-surface package.

Its maturity was reached step by step through:

- live observed schema capture
- repository-side executable contract preservation
- interpretation and role separation
- structural equivalence audit
- primary working surface decision
- execution-surface entry point creation

## Genel Bakış

Bu belge, `sql/desktop_import` yüzeyi için mevcut kronoloji yorumunu tanımlar.

Crawler-core, parse-core veya outbox-core'dan farklı olarak bu yüzey işe tam split edilmiş bir ana çalışma yüzeyi paketi olarak başlamamıştır.

Olgunluğu şu adımlar üzerinden adım adım oluşmuştur:

- canlı gözlenen şema yakalama
- repository-side çalıştırılabilir contract'ın korunması
- yorum ve rol ayrımı
- yapısal eşdeğerlik denetimi
- ana çalışma yüzeyi kararı
- execution-surface giriş noktalarının oluşturulması

## Current chronology reading

The chronology should now be read in this order:

### Stage 0 — Live reality capture
The following files preserve observed current desktop reality:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

### Stage 1 — Executable contract preservation
The following file preserves the repository-side executable intake contract:

- `001_pi51_batch_intake_contract.sql`

### Stage 2 — Interpretation and role separation
This interpretation layer is documented through:

- `README.md`
- `SURFACE_ROLE_MAP.md`

### Stage 3 — Equivalence judgement
This layer records whether live observed reality and executable contract truth match:

- `COVERAGE_OR_EQUIVALENCE_NOTE.md`

Recorded result:
- structural equivalence verified at the audited layer

### Stage 4 — Primary working surface decision
This layer records which file should be treated as the primary working surface:

- `PRIMARY_WORKING_SURFACE_SEAL.md`

Recorded result:
- `001_pi51_batch_intake_contract.sql` is now the primary working surface

### Stage 5 — Execution-surface maturity start
This layer records the first reusable execution and validation entry points:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

Recorded result:
- execution/validation surface now exists and can be used to validate the primary working surface on scratch databases

## Güncel kronoloji okuması

Kronoloji artık şu sırayla okunmalıdır:

### Aşama 0 — Canlı gerçekliğin yakalanması
Şu dosyalar gözlenen güncel desktop gerçekliğini korur:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

### Aşama 1 — Çalıştırılabilir contract'ın korunması
Şu dosya repository-side çalıştırılabilir intake contract'ını korur:

- `001_pi51_batch_intake_contract.sql`

### Aşama 2 — Yorum ve rol ayrımı
Bu yorum katmanı şu belgelerle işlenmiştir:

- `README.md`
- `SURFACE_ROLE_MAP.md`

### Aşama 3 — Eşdeğerlik hükmü
Bu katman, canlı gözlenen gerçeklik ile çalıştırılabilir contract doğruluğunun eşleşip eşleşmediğini kayda geçirir:

- `COVERAGE_OR_EQUIVALENCE_NOTE.md`

Kayda geçen sonuç:
- denetlenen katmanda yapısal eşdeğerlik doğrulandı

### Aşama 4 — Ana çalışma yüzeyi kararı
Bu katman, hangi dosyanın ana çalışma yüzeyi olarak ele alınacağını kayda geçirir:

- `PRIMARY_WORKING_SURFACE_SEAL.md`

Kayda geçen sonuç:
- `001_pi51_batch_intake_contract.sql` artık ana çalışma yüzeyidir

### Aşama 5 — Execution-surface olgunlaşmasının başlangıcı
Bu katman ilk reusable execution ve validation giriş noktalarını kayda geçirir:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

Kayda geçen sonuç:
- execution/validation yüzeyi artık vardır ve ana çalışma yüzeyini scratch veritabanlarında doğrulamak için kullanılabilir

## Important distinction from outbox-core

Outbox-core had already reached a mature split working model when its documentation hardening intensified.

Desktop_import reached clarity in a different order:

1. live snapshot first
2. executable contract preserved in repository
3. interpretation documents added
4. equivalence verified
5. primary working surface sealed
6. execution entry points added around that surface

So the key point is not to pretend it started mature, but to preserve the true chronology of how maturity was reached.

## Outbox-core'dan önemli fark

Outbox-core, dokümantasyon sertleştirmesi yoğunlaşmadan önce zaten olgun bir split çalışma modeline ulaşmıştı.

Desktop_import ise açıklığa farklı bir sırayla ulaştı:

1. önce canlı snapshot
2. repository içinde çalıştırılabilir contract'ın korunması
3. yorum belgelerinin eklenmesi
4. eşdeğerliğin doğrulanması
5. ana çalışma yüzeyinin mühürlenmesi
6. bu yüzey etrafına execution giriş noktalarının eklenmesi

Dolayısıyla kritik nokta, işe olgun başlamış gibi davranmak değil; olgunluğa nasıl ulaşıldığının gerçek kronolojisini korumaktır.

## Immediate next work after this plan

The next normal repository-side work should now move toward warning-free validation sealing and execution-surface closure, such as:

1. warning-free scratch validation rerun
2. scratch validation seal
3. working-style / validation-discipline document
4. final execution-surface audit

## Bu plandan sonraki anlık iş

Bu plandan sonraki normal repository-side iş artık warning'siz validation mühürlemesine ve execution-surface kapanışına gitmelidir; örneğin:

1. warning'siz scratch validation tekrar koşusu
2. scratch validation seal
3. working-style / validation-discipline belgesi
4. final execution-surface audit

## Current rule

The chronology rule is now:

- snapshot truth preserved as evidence
- contract truth preserved as executable surface
- structural equivalence already verified
- primary working surface already decided
- execution helpers already added
- future evolution should proceed deliberately from the contract file and be validated through the execution layer

## Güncel kural

Kronoloji kuralı artık şudur:

- snapshot doğruluğu kanıt olarak korunur
- contract doğruluğu çalıştırılabilir yüzey olarak korunur
- yapısal eşdeğerlik zaten doğrulanmıştır
- ana çalışma yüzeyi zaten kararlaştırılmıştır
- execution yardımcıları zaten eklenmiştir
- gelecekteki evrim contract dosyasından bilinçli şekilde ilerlemeli ve execution katmanı üzerinden doğrulanmalıdır
