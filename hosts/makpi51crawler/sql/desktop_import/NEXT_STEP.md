# Desktop Import Next Step

## Overview

The `desktop_import` repository surface has now been:

- captured from live Ubuntu Desktop truth
- represented with a preserved live evidence snapshot
- given an explicit primary working SQL surface
- surrounded with reusable execution and validation entry points
- post-push repaired and re-audited successfully

The next work should no longer start from the live snapshot dump as the primary editing surface.

## Genel Bakış

`desktop_import` repository yüzeyi artık:

- canlı Ubuntu Desktop doğrusundan alınmış
- korunmuş bir canlı kanıt snapshot'ı ile temsil edilmiş
- açık bir ana çalışma SQL yüzeyi kazanmış
- reusable execution ve validation giriş noktaları ile çevrelenmiş
- post-push onarım ve tekrar denetimden başarıyla geçmiş durumdadır

Bundan sonraki iş artık ana düzenleme yüzeyi olarak canlı snapshot dump'ından başlamamalıdır.

## Primary working file from now on

Future `desktop_import` SQL evolution should start from:

- `001_pi51_batch_intake_contract.sql`

Execution and validation entry points:

- `901_preflight_desktop_import_surface.psql.sql`
- `900_apply_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

## Bundan sonra ana çalışma dosyası

Gelecekteki `desktop_import` SQL evrimi şu dosyadan başlamalıdır:

- `001_pi51_batch_intake_contract.sql`

Execution ve validation giriş noktaları:

- `901_preflight_desktop_import_surface.psql.sql`
- `900_apply_desktop_import_surface.psql.sql`
- `902_presence_audit_desktop_import_surface.psql.sql`
- `910_validate_desktop_import_surface.sh`

## Preserved comparison surfaces

These remain important, but they are comparison/evidence surfaces rather than the main editing layer:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`
- `001_live_desktop_import_sha256.txt`

## Korunan karşılaştırma yüzeyleri

Bunlar önemini korur; ancak ana düzenleme katmanı değil, karşılaştırma/kanıt yüzeyidir:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`
- `001_live_desktop_import_sha256.txt`

## Immediate practical continuation

The next practical continuation should be one of these:

1. controlled semantic evolution of `001_pi51_batch_intake_contract.sql`
2. addition of a new `desktop_import` SQL package only if the surface genuinely grows beyond the current contract scope
3. fresh execution/validation re-check after any meaningful SQL change
4. continued README / seal / chronology alignment if the surface meaning changes

## Anlık pratik devam yolu

Bir sonraki pratik devam adımı şunlardan biri olmalıdır:

1. `001_pi51_batch_intake_contract.sql` üzerinde kontrollü semantik evrim
2. yüzey gerçekten mevcut contract kapsamını aşarsa yeni bir `desktop_import` SQL paketinin eklenmesi
3. anlamlı her SQL değişikliğinden sonra execution/validation tekrar kontrolü
4. yüzeyin anlamı değişirse README / seal / chronology hizasının sürdürülmesi
