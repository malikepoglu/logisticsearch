# Crawler Core Primary Working Surface Seal

Current sealed position:

- the live Pi51 crawler-core snapshot remains preserved as evidence
- the split crawler-core SQL files are now the primary working surface
- the psql apply bundle is the canonical execution entry point for the split surface
- this phase used Pi51 as a read-only truth source, not as the main editing surface

# Crawler Core Birincil Çalışma Yüzeyi Mührü

Mevcut mühürlü konum:

- canlı Pi51 crawler-core snapshot'ı kanıt olarak korunur
- split crawler-core SQL dosyaları artık ana çalışma yüzeyidir
- psql apply bundle, split yüzey için kanonik execution giriş noktasıdır
- bu fazda Pi51 ana düzenleme yüzeyi değil, read-only doğru kaynağı olarak kullanılmıştır

## Primary working surface

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

## Ana çalışma yüzeyi

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`
- `900_apply_crawler_core_split_surface.psql.sql`

## Evidence surface

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Kanıt yüzeyi

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Rule

From this point forward, normal crawler-core SQL evolution should target the split surface first. The live snapshot remains preserved as imported evidence and comparison truth.

## Kural

Bu noktadan sonra normal crawler-core SQL evrimi önce split yüzeyi hedeflemelidir. Canlı snapshot, ithal kanıt ve karşılaştırma doğrusu olarak korunur.
