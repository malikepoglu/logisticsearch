# Desktop Import Working Style and Validation Discipline

## Overview

This document records the current working style and validation discipline for the `sql/desktop_import` surface.

Its purpose is to ensure that future evolution of the primary working surface remains:

- controlled
- auditable
- reproducible
- warning-free at execution time

## Genel Bakış

Bu belge, `sql/desktop_import` yüzeyi için mevcut çalışma stili ve doğrulama disiplinini kayda geçirir.

Amacı, ana çalışma yüzeyinin gelecekteki evriminin şu özellikleri korumasını sağlamaktır:

- kontrollü
- denetlenebilir
- yeniden üretilebilir
- çalıştırma anında warning'siz

## Current practical rule

For this surface, the normal operating rhythm is:

1. update the primary working surface
2. update execution/validation entry points if needed
3. rerun scratch validation
4. inspect presence-audit shape
5. document the result
6. only then commit and push

## Güncel pratik kural

Bu yüzey için normal işletim ritmi şöyledir:

1. ana çalışma yüzeyini güncelle
2. gerekiyorsa execution/validation giriş noktalarını güncelle
3. scratch doğrulamayı tekrar çalıştır
4. presence-audit şeklini incele
5. sonucu belgeye işle
6. ancak ondan sonra commit ve push yap

## Working surface rule

The primary structural evolution surface is:

- `001_pi51_batch_intake_contract.sql`

This means future meaningful SQL changes should begin there first.

## Çalışma yüzeyi kuralı

Ana yapısal evrim yüzeyi şudur:

- `001_pi51_batch_intake_contract.sql`

Bu, gelecekteki anlamlı SQL değişikliklerinin önce burada başlaması gerektiği anlamına gelir.

## Execution layer rule

The canonical execution/validation layer is:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

These files must stay aligned with the primary working surface.

## Execution katmanı kuralı

Kanonik execution/validation katmanı şudur:

- `900_apply_desktop_import_surface.psql.sql`
- `901_preflight_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

Bu dosyalar ana çalışma yüzeyi ile hizalı kalmalıdır.

## Validation rule

A structural change should not be treated as trusted until:

1. scratch database recreation succeeds
2. preflight succeeds
3. apply succeeds
4. presence audit succeeds
5. no execution-warning regression appears

## Doğrulama kuralı

Bir yapısal değişiklik şu koşullar oluşmadan güvenilir kabul edilmemelidir:

1. scratch veritabanının yeniden oluşturulması başarılı olmalı
2. preflight başarılı olmalı
3. apply başarılı olmalı
4. presence audit başarılı olmalı
5. execution-warning gerilemesi oluşmamalı

## Warning discipline

Execution warnings should be treated as real quality signals.

The recent transaction-wrapper cleanup established an important rule:

- do not wrap an already transaction-owning contract in a redundant outer transaction layer

## Warning disiplini

Execution warning'leri gerçek kalite sinyali olarak ele alınmalıdır.

Yakın zamanda yapılan transaction-wrapper temizliği şu önemli kuralı oluşturdu:

- transaction'ını zaten kendi yöneten bir contract'ı gereksiz dış transaction katmanı ile sarmalama

## Evidence preservation rule

The following files must remain preserved as live evidence:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

They are not the main editing surface, but they remain important audit evidence.

## Kanıt koruma kuralı

Şu dosyalar canlı kanıt olarak korunmalıdır:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Bunlar ana düzenleme yüzeyi değildir; ancak önemli denetim kanıtı olmaya devam ederler.

## Commit discipline

Commit messages should distinguish clearly between:

- live snapshot evidence
- role/chronology docs
- equivalence judgement
- primary working surface decisions
- execution-surface additions
- validation seals
- fixes

## Commit disiplini

Commit mesajları şu katmanları açıkça ayırmalıdır:

- canlı snapshot kanıtı
- rol/kronoloji belgeleri
- eşdeğerlik hükmü
- ana çalışma yüzeyi kararları
- execution-surface eklemeleri
- validation seal'leri
- düzeltmeler

## Next continuation point

The next normal work after this discipline document should be:

- final execution-surface audit
- then controlled commit/push of the execution-surface package

## Sonraki devam noktası

Bu disiplin belgesinden sonraki normal iş şu olmalıdır:

- final execution-surface audit
- ardından execution-surface paketinin kontrollü commit/push işlemi
