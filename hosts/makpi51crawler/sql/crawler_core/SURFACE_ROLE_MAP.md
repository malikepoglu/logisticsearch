# Crawler Core Surface Role Map

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

Current role model inside `hosts/makpi51crawler/sql/crawler_core`:

# Crawler Core Yüzey Rol Haritası

`hosts/makpi51crawler/sql/crawler_core` içindeki mevcut rol modeli:

## Live evidence surface

These files preserve the live Pi51-derived crawler-core truth as imported evidence:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Canlı kanıt yüzeyi

Bu dosyalar Pi51'den alınmış canlı crawler-core doğrusunu ithal kanıt olarak korur:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

## Planning surface

These files define how the live snapshot is decomposed into chronology-aligned units:

- `CHRONOLOGY_SPLIT_PLAN.md`

## Planlama yüzeyi

Bu dosyalar canlı snapshot'ın chronology uyumlu parçalara nasıl ayrıldığını tanımlar:

- `CHRONOLOGY_SPLIT_PLAN.md`

## Execution-oriented split surface

These files are the practical chronology-aligned SQL surface for future controlled work:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

## Execution-oriented split yüzeyi

Bu dosyalar, gelecekteki kontrollü işler için pratik chronology uyumlu SQL yüzeyidir:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

## Current policy

- live snapshot stays preserved
- split files are the working surface for future crawler-core SQL evolution
- snapshot is evidence, split files are the main editable structure

## Mevcut politika

- canlı snapshot korunur
- split dosyaları gelecekteki crawler-core SQL evriminin çalışma yüzeyidir
- snapshot kanıttır, split dosyaları ana düzenlenebilir yapıdır
