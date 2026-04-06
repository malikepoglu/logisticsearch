# Crawler Core Next Step

## Overview

The crawler-core split SQL surface has now been:

- imported from live Pi51 truth
- decomposed into chronology-aligned working files
- checked for dependency assumptions
- validated successfully on a local scratch PostgreSQL database

The next work should no longer start from the imported live snapshot as the primary editing surface.

## Genel Bakış

Crawler-core split SQL yüzeyi artık:

- canlı Pi51 doğrusundan ithal edilmiş
- chronology uyumlu çalışma dosyalarına parçalanmış
- bağımlılık varsayımları açısından kontrol edilmiş
- yerel scratch PostgreSQL veritabanında başarıyla doğrulanmıştır

Bundan sonraki iş artık ana düzenleme yüzeyi olarak ithal edilmiş canlı snapshot’tan başlamamalıdır.

## Primary working files from now on

Future crawler-core SQL evolution should start from:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Execution entry points:

- `901_preflight_crawler_core_split_surface.psql.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

Current ownership-lifecycle function family inside `002_frontier_claim_and_lease.sql` is now:

- `frontier.claim_next_url`
- `frontier.renew_url_lease`
- `frontier.reap_expired_leases`

## Bundan sonra ana çalışma dosyaları

Gelecekteki crawler-core SQL evrimi şu dosyalardan başlamalıdır:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Execution giriş noktaları:

- `901_preflight_crawler_core_split_surface.psql.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

`002_frontier_claim_and_lease.sql` içindeki mevcut ownership-lifecycle fonksiyon ailesi artık şudur:

- `frontier.claim_next_url`
- `frontier.renew_url_lease`
- `frontier.reap_expired_leases`

## Preserved comparison surfaces

These remain important, but they are comparison/evidence surfaces rather than the main editing layer:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Korunan karşılaştırma yüzeyleri

Bunlar önemini korur; ancak ana düzenleme katmanı değil, karşılaştırma/kanıt yüzeyidir:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Immediate practical continuation

The next practical continuation should be one of these:

1. controlled semantic evolution of one split SQL file, including claim / renew / reap ownership consistency inside `002_frontier_claim_and_lease.sql`
2. a new crawler-core package added in chronology order
3. a fresh scratch re-validation after any meaningful SQL change

## Anlık pratik devam yolu

Bir sonraki pratik devam adımı şunlardan biri olmalıdır:

1. `002_frontier_claim_and_lease.sql` içindeki claim / renew / reap ownership tutarlılığı dahil olmak üzere split SQL dosyalarından birinde kontrollü semantik evrim
2. chronology sırasına uygun yeni bir crawler-core paketinin eklenmesi
3. anlamlı her SQL değişikliğinden sonra yeni bir scratch tekrar doğrulaması

## Current preserved scratch database

Current preserved local scratch database:

- `logisticsearch_crawler_split_scratch`

This database may be retained temporarily for inspection, then dropped in a later cleanup step.

## Mevcut korunan scratch veritabanı

Mevcut korunan yerel scratch veritabanı:

- `logisticsearch_crawler_split_scratch`

Bu veritabanı inceleme için geçici olarak tutulabilir, daha sonra ayrı bir cleanup adımında silinebilir.
