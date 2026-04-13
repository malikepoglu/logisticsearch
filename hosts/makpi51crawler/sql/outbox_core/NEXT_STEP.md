# Outbox Core Next Step

## Overview

The outbox-core split SQL surface has now been:

- imported from live Pi51 truth
- decomposed into chronology-aligned working files
- checked for upstream dependency assumptions
- validated successfully on a local scratch PostgreSQL database with required upstream layers
- equipped with reusable execution and validation entry points
- aligned with README / seal / audit documentation

The next work should no longer start from the imported live snapshot as the primary editing surface.

## Genel Bakış

Outbox-core split SQL yüzeyi artık:

- canlı Pi51 doğrusundan ithal edilmiş
- chronology uyumlu çalışma dosyalarına parçalanmış
- upstream bağımlılık varsayımları açısından kontrol edilmiş
- gerekli upstream katmanlarla yerel scratch PostgreSQL veritabanında başarıyla doğrulanmış
- reusable execution ve validation giriş noktalarıyla donatılmış
- README / seal / audit dokümantasyonu ile hizalanmış durumdadır

Bundan sonraki iş artık ana düzenleme yüzeyi olarak ithal edilmiş canlı snapshot'tan başlamamalıdır.

## Primary working files from now on

Future outbox-core SQL evolution should start from:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

Execution entry points:

- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`
- `910_validate_outbox_core_split_surface.sh`

## Bundan sonra ana çalışma dosyaları

Gelecekteki outbox-core SQL evrimi şu dosyalardan başlamalıdır:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

Execution giriş noktaları:

- `900_apply_outbox_core_split_surface.psql.sql`
- `901_preflight_outbox_core_split_surface.psql.sql`
- `902_presence_audit_outbox_core_split_surface.psql.sql`
- `910_validate_outbox_core_split_surface.sh`

## Preserved comparison surfaces

These remain important, but they are comparison/evidence surfaces rather than the main editing layer:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Korunan karşılaştırma yüzeyleri

Bunlar önemini korur; ancak ana düzenleme katmanı değil, karşılaştırma/kanıt yüzeyidir:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Immediate practical continuation

The next practical continuation should be one of these:

1. controlled semantic evolution of one split SQL file
2. addition of a new chronology-aligned outbox-core package if the surface grows
3. fresh scratch re-validation after any meaningful SQL change
4. dependency-aware verification whenever upstream crawler-core or parse-core contracts change

## Anlık pratik devam yolu

Bir sonraki pratik devam adımı şunlardan biri olmalıdır:

1. split SQL dosyalarından birinde kontrollü semantik evrim
2. yüzey büyürse chronology uyumlu yeni bir outbox-core paketinin eklenmesi
3. anlamlı her SQL değişikliğinden sonra yeni bir scratch tekrar doğrulaması
4. upstream crawler-core veya parse-core contract'ları değiştiğinde bağımlılık farkındalıklı tekrar doğrulama
