# Crawler Core Chronology Split Plan

## EN

This document maps the live Pi51 crawler-core schema snapshot to the next intended chronology-aligned SQL file layout. The source of truth for structure is currently:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`

The purpose of this plan is not to replace the live snapshot immediately, but to define a disciplined decomposition path without losing the verified live contract.

## Current live snapshot contents

### Types
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
- `frontier.host`
- `frontier.url`
- `http_fetch.fetch_attempt`
- `http_fetch.robots_txt_cache`
- `seed.seed_url`
- `seed.source`

### Functions
- `frontier.claim_next_url`
- `frontier.compute_retry_backoff`
- `frontier.compute_success_next_fetch_at`
- `frontier.finish_fetch_permanent_error`
- `frontier.finish_fetch_retryable_error`
- `frontier.finish_fetch_success`
- `frontier.reap_expired_leases`
- `http_fetch.compute_robots_allow_decision`
- `http_fetch.compute_robots_refresh_decision`
- `http_fetch.upsert_robots_txt_cache`

### Indexes
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

## Intended chronology-aligned target layout

### 001_seed_frontier_http_fetch_base.sql
Contains:
- schema creation
- all enum types
- base tables
- base constraints
- base indexes that belong directly to core table access paths

Expected object families:
- all 10 enum types
- all 6 tables
- baseline indexes

### 002_frontier_claim_and_lease.sql
Contains:
- `frontier.claim_next_url`
- `frontier.renew_url_lease`
- `frontier.reap_expired_leases`

Purpose:
- queue claiming
- lease lifecycle entry
- lease lifecycle renewal
- lease lifecycle recovery

Post-import controlled extension note:
- `frontier.renew_url_lease` was not part of the imported live Pi51 snapshot
- it is now a deliberate split-surface extension added after explicit contract design and targeted scratch smoke validation

### 003_frontier_finish_transitions.sql
Contains:
- `frontier.finish_fetch_success`
- `frontier.finish_fetch_retryable_error`
- `frontier.finish_fetch_permanent_error`

Purpose:
- leased fetch finalization
- state transitions after fetch completion

### 004_frontier_politeness_and_freshness.sql
Contains:
- `frontier.compute_retry_backoff`
- `frontier.compute_success_next_fetch_at`

Purpose:
- retry delay policy
- freshness / revisit timing

### 005_http_fetch_robots_cache_and_enforcement.sql
Contains:
- `http_fetch.upsert_robots_txt_cache`
- `http_fetch.compute_robots_refresh_decision`
- `http_fetch.compute_robots_allow_decision`

Purpose:
- robots cache persistence
- refresh decision
- allow/block decision

## Rules for the split phase

1. The live snapshot remains preserved as the canonical imported evidence.
2. Split files must not silently change semantics.
3. Object order must preserve dependency correctness.
4. Any normalization beyond pure decomposition must be explicit and reviewable.
5. The split phase should be done only on Ubuntu Desktop and then pushed through GitHub.

---

## TR

Bu belge, canlı Pi51 crawler-core şema snapshot’ını bir sonraki chronology uyumlu SQL dosya düzenine eşler. Yapısal doğruluk için mevcut kaynak dosya şudur:

- `001_pi51_live_seed_frontier_http_fetch_schema.sql`

Bu planın amacı canlı snapshot’ı hemen değiştirmek değil; doğrulanmış canlı kontratı kaybetmeden disiplinli bir parçalama yolu tanımlamaktır.

## Mevcut canlı snapshot içeriği

### Type'lar
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

### Tablolar
- `frontier.host`
- `frontier.url`
- `http_fetch.fetch_attempt`
- `http_fetch.robots_txt_cache`
- `seed.seed_url`
- `seed.source`

### Fonksiyonlar
- `frontier.claim_next_url`
- `frontier.compute_retry_backoff`
- `frontier.compute_success_next_fetch_at`
- `frontier.finish_fetch_permanent_error`
- `frontier.finish_fetch_retryable_error`
- `frontier.finish_fetch_success`
- `frontier.reap_expired_leases`
- `http_fetch.compute_robots_allow_decision`
- `http_fetch.compute_robots_refresh_decision`
- `http_fetch.upsert_robots_txt_cache`

### Index'ler
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

## Hedef chronology uyumlu dosya düzeni

### 001_seed_frontier_http_fetch_base.sql
Şunları içerir:
- şema oluşturma
- tüm enum type'lar
- temel tablolar
- temel constraint'ler
- çekirdek tablo erişim yollarına ait temel index'ler

Beklenen nesne aileleri:
- tüm 10 enum type
- tüm 6 tablo
- temel index'ler

### 002_frontier_claim_and_lease.sql
Şunları içerir:
- `frontier.claim_next_url`
- `frontier.renew_url_lease`
- `frontier.reap_expired_leases`

Amaç:
- kuyruktan claim etme
- lease yaşam döngüsüne giriş
- lease yaşam döngüsünü yenileme
- lease yaşam döngüsünü toparlama


İthal-sonrası kontrollü genişletme notu:
- `frontier.renew_url_lease`, ithal edilmiş canlı Pi51 snapshot'ının parçası değildi
- şimdi açık kontrat tasarımı ve hedefli scratch smoke validation sonrasında eklenmiş bilinçli bir split-surface genişletmesidir

### 003_frontier_finish_transitions.sql
Şunları içerir:
- `frontier.finish_fetch_success`
- `frontier.finish_fetch_retryable_error`
- `frontier.finish_fetch_permanent_error`

Amaç:
- leased fetch finalization
- fetch sonrası durum geçişleri

### 004_frontier_politeness_and_freshness.sql
Şunları içerir:
- `frontier.compute_retry_backoff`
- `frontier.compute_success_next_fetch_at`

Amaç:
- retry delay politikası
- freshness / yeniden ziyaret zamanlaması

### 005_http_fetch_robots_cache_and_enforcement.sql
Şunları içerir:
- `http_fetch.upsert_robots_txt_cache`
- `http_fetch.compute_robots_refresh_decision`
- `http_fetch.compute_robots_allow_decision`

Amaç:
- robots cache kalıcılığı
- refresh kararı
- allow/block kararı

## Parçalama fazı kuralları

1. Canlı snapshot, kanonik ithal kanıt olarak korunur.
2. Split dosyaları semantiği sessizce değiştirmemelidir.
3. Nesne sırası dependency doğruluğunu korumalıdır.
4. Saf parçalama dışındaki her normalizasyon açık ve gözden geçirilebilir olmalıdır.
5. Split fazı yalnızca Ubuntu Desktop üzerinde yapılmalı ve sonra GitHub üzerinden taşınmalıdır.
