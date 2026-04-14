# Crawler Core Primary Working Surface Seal

Documentation hub:

* `hosts/makpi51crawler/sql/README.md` — host-scoped SQL hub
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core surface hub
* `hosts/makpi51crawler/README.md` — host root for makpi51crawler
* `hosts/README.md` — host family root
* `README.md` — repository root surface
* `docs/README.md` — documentation hub

Dokümantasyon merkezi:

* `hosts/makpi51crawler/sql/README.md` — host-kapsamlı SQL merkezi
* `hosts/makpi51crawler/sql/crawler_core/README.md` — crawler_core yüzey merkezi
* `hosts/makpi51crawler/README.md` — makpi51crawler host kökü
* `hosts/README.md` — host aile kökü
* `README.md` — repository kök yüzeyi
* `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This document supports the current `crawler_core` working surface under `hosts/makpi51crawler/sql/crawler_core/` and should be read as part of the controlled SECTION1 crawler_core line.

Bu belge, `hosts/makpi51crawler/sql/crawler_core/` altındaki mevcut `crawler_core` çalışma yüzeyini destekler ve kontrollü SECTION1 crawler_core hattının bir parçası olarak okunmalıdır.

## Current host-scoped path
## Güncel host-kapsamlı yol

At the current repository point, this surface lives under `hosts/makpi51crawler/sql/crawler_core/`.

Mevcut repository noktasında bu yüzey `hosts/makpi51crawler/sql/crawler_core/` altında yaşar.

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
