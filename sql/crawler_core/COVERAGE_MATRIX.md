# Crawler Core Coverage Matrix

This document records the current coverage relationship between the imported live Pi51 crawler-core snapshot and the split primary working surface.

# Crawler Core Kapsama Matrisi

Bu belge, ithal edilmiş canlı Pi51 crawler-core snapshot'ı ile split ana çalışma yüzeyi arasındaki mevcut kapsama ilişkisini kayda geçirir.

## Evidence source

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`

## Kanıt kaynağı

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`

## Primary working surface

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

## Ana çalışma yüzeyi

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

## Coverage summary

This section maps which object families are covered by the current split working surface and where that coverage lives.

## Kapsama özeti

Bu bölüm, hangi nesne ailelerinin mevcut split çalışma yüzeyi tarafından kapsandığını ve bu kapsamanın nerede yaşadığını eşler.

### Schemas

Covered in:

- `001_seed_frontier_http_fetch_base.sql`

Objects:

- `frontier`
- `http_fetch`
- `seed`

### Şemalar

Şurada kapsanır:

- `001_seed_frontier_http_fetch_base.sql`

Nesneler:

- `frontier`
- `http_fetch`
- `seed`

### Types

Covered in:

- `001_seed_frontier_http_fetch_base.sql`

Objects:

- `frontier.discovery_type_enum`
- `frontier.host_status_enum`
- `frontier.robots_mode_enum`
- `frontier.url_state_enum`
- `http_fetch.fetch_kind_enum`
- `http_fetch.fetch_outcome_enum`
- `http_fetch.robots_cache_state_enum`
- `http_fetch.robots_verdict_enum`
- `seed.seed_type_enum`
- `seed.source_status_enum`

### Type'lar

Şurada kapsanır:

- `001_seed_frontier_http_fetch_base.sql`

Nesneler:

- `frontier.discovery_type_enum`
- `frontier.host_status_enum`
- `frontier.robots_mode_enum`
- `frontier.url_state_enum`
- `http_fetch.fetch_kind_enum`
- `http_fetch.fetch_outcome_enum`
- `http_fetch.robots_cache_state_enum`
- `http_fetch.robots_verdict_enum`
- `seed.seed_type_enum`
- `seed.source_status_enum`

### Tables

Covered in:

- `001_seed_frontier_http_fetch_base.sql`

Objects:

- `frontier.host`
- `frontier.url`
- `http_fetch.fetch_attempt`
- `http_fetch.robots_txt_cache`
- `seed.seed_url`
- `seed.source`

### Tablolar

Şurada kapsanır:

- `001_seed_frontier_http_fetch_base.sql`

Nesneler:

- `frontier.host`
- `frontier.url`
- `http_fetch.fetch_attempt`
- `http_fetch.robots_txt_cache`
- `seed.seed_url`
- `seed.source`

### Indexes

Covered in:

- `001_seed_frontier_http_fetch_base.sql`

Objects:

- `frontier_host_pause_idx`
- `frontier_host_sched_idx`
- `frontier_url_due_idx`
- `frontier_url_host_due_idx`
- `frontier_url_lease_expiry_idx`
- `frontier_url_parent_idx`
- `frontier_url_parse_pending_idx`
- `fetch_attempt_host_time_idx`
- `fetch_attempt_open_idx`
- `fetch_attempt_url_time_idx`
- `robots_cache_expiry_idx`
- `seed_seed_url_due_idx`

### Index'ler

Şurada kapsanır:

- `001_seed_frontier_http_fetch_base.sql`

Nesneler:

- `frontier_host_pause_idx`
- `frontier_host_sched_idx`
- `frontier_url_due_idx`
- `frontier_url_host_due_idx`
- `frontier_url_lease_expiry_idx`
- `frontier_url_parent_idx`
- `frontier_url_parse_pending_idx`
- `fetch_attempt_host_time_idx`
- `fetch_attempt_open_idx`
- `fetch_attempt_url_time_idx`
- `robots_cache_expiry_idx`
- `seed_seed_url_due_idx`

### Functions

Covered in:

- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Objects:

- `frontier.claim_next_url` -> `002_frontier_claim_and_lease.sql`
- `frontier.renew_url_lease` -> `002_frontier_claim_and_lease.sql` (post-import controlled extension)
- `frontier.reap_expired_leases` -> `002_frontier_claim_and_lease.sql`
- `frontier.finish_fetch_success` -> `003_frontier_finish_transitions.sql`
- `frontier.finish_fetch_retryable_error` -> `003_frontier_finish_transitions.sql`
- `frontier.finish_fetch_permanent_error` -> `003_frontier_finish_transitions.sql`
- `frontier.compute_retry_backoff` -> `004_frontier_politeness_and_freshness.sql`
- `frontier.compute_success_next_fetch_at` -> `004_frontier_politeness_and_freshness.sql`
- `http_fetch.upsert_robots_txt_cache` -> `005_http_fetch_robots_cache_and_enforcement.sql`
- `http_fetch.compute_robots_refresh_decision` -> `005_http_fetch_robots_cache_and_enforcement.sql`
- `http_fetch.compute_robots_allow_decision` -> `005_http_fetch_robots_cache_and_enforcement.sql`

### Fonksiyonlar

Şurada kapsanır:

- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Nesneler:

- `frontier.claim_next_url` -> `002_frontier_claim_and_lease.sql`
- `frontier.renew_url_lease` -> `002_frontier_claim_and_lease.sql` (ithal sonrası kontrollü genişletme)
- `frontier.reap_expired_leases` -> `002_frontier_claim_and_lease.sql`
- `frontier.finish_fetch_success` -> `003_frontier_finish_transitions.sql`
- `frontier.finish_fetch_retryable_error` -> `003_frontier_finish_transitions.sql`
- `frontier.finish_fetch_permanent_error` -> `003_frontier_finish_transitions.sql`
- `frontier.compute_retry_backoff` -> `004_frontier_politeness_and_freshness.sql`
- `frontier.compute_success_next_fetch_at` -> `004_frontier_politeness_and_freshness.sql`
- `http_fetch.upsert_robots_txt_cache` -> `005_http_fetch_robots_cache_and_enforcement.sql`
- `http_fetch.compute_robots_refresh_decision` -> `005_http_fetch_robots_cache_and_enforcement.sql`
- `http_fetch.compute_robots_allow_decision` -> `005_http_fetch_robots_cache_and_enforcement.sql`

## Post-import controlled extension

Current split surface now also contains one deliberate function beyond the imported live snapshot:

- `frontier.renew_url_lease` -> `002_frontier_claim_and_lease.sql`

This does not change the fact that live-snapshot coverage remains complete.

It means the split working surface now consists of:

1. full coverage of the imported live crawler-core truth
2. one explicit post-import lease-renewal extension

## İthal sonrası kontrollü genişletme

Mevcut split yüzey, ithal edilmiş canlı snapshot'ın ötesinde artık bilinçli bir ek fonksiyon da içerir:

- `frontier.renew_url_lease` -> `002_frontier_claim_and_lease.sql`

Bu durum canlı snapshot kapsamasının tam olduğu gerçeğini değiştirmez.

Anlamı şudur: split çalışma yüzeyi artık şunlardan oluşur:

1. ithal edilmiş canlı crawler-core doğrusunun tam kapsamı
2. açık bir ithal-sonrası lease-renewal genişletmesi

## Current result

The split working surface currently covers the live snapshot object families at the following counts:

- schemas: 3 / 3
- types: 10 / 10
- tables: 6 / 6
- functions from imported live snapshot: 10 / 10
- post-import controlled extension functions: 1 / 1
- indexes: 12 / 12

Current judgement:

- live snapshot remains preserved as evidence
- split surface is structurally coverage-complete for the imported crawler-core scope
- future crawler-core SQL evolution should target the split surface first
- explicit post-import extensions must be documented as extensions rather than silently merged into live-snapshot coverage language

## Mevcut sonuç

Split çalışma yüzeyi şu anda canlı snapshot nesne ailelerini aşağıdaki sayımlarla kapsar:

- şemalar: 3 / 3
- type'lar: 10 / 10
- tablolar: 6 / 6
- ithal edilmiş canlı snapshot fonksiyonları: 10 / 10
- ithal sonrası kontrollü genişletme fonksiyonları: 1 / 1
- index'ler: 12 / 12

Güncel hüküm:

- canlı snapshot kanıt olarak korunmaktadır
- split yüzey, ithal edilmiş crawler-core kapsamı için yapısal olarak kapsama-tam durumdadır
- gelecekteki crawler-core SQL evrimi önce split yüzeyi hedeflemelidir
- açık ithal-sonrası genişletmeler, canlı-snapshot kapsama diline sessizce yedirilmek yerine genişletme olarak dokümante edilmelidir
