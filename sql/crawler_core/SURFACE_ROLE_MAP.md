# Crawler Core Surface Role Map

## EN

Current role model inside `sql/crawler_core`:

### Live evidence surface
These files preserve the live Pi51-derived crawler-core truth as imported evidence:
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Planning surface
These files define how the live snapshot is decomposed into chronology-aligned units:
- `CHRONOLOGY_SPLIT_PLAN.md`

### Execution-oriented split surface
These files are the practical chronology-aligned SQL surface for future controlled work:
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Current policy
- live snapshot stays preserved
- split files are the working surface for future crawler-core SQL evolution
- snapshot is evidence, split files are the main editable structure

---

## TR

`sql/crawler_core` içindeki mevcut rol modeli:

### Canlı kanıt yüzeyi
Bu dosyalar Pi51’den alınmış canlı crawler-core doğrusunu ithal kanıt olarak korur:
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Planlama yüzeyi
Bu dosyalar canlı snapshot’ın chronology uyumlu parçalara nasıl ayrıldığını tanımlar:
- `CHRONOLOGY_SPLIT_PLAN.md`

### Execution-oriented split yüzeyi
Bu dosyalar, gelecekteki kontrollü işler için pratik chronology uyumlu SQL yüzeyidir:
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Mevcut politika
- canlı snapshot korunur
- split dosyaları gelecekteki crawler-core SQL evriminin çalışma yüzeyidir
- snapshot kanıttır, split dosyaları ana düzenlenebilir yapıdır
