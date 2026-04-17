# Crawler Core SQL Surface

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

## Current host-scoped path
## Güncel host-kapsamlı yol

At the current repository point, this surface lives under `hosts/makpi51crawler/sql/crawler_core/`.

Mevcut repository noktasında bu yüzey `hosts/makpi51crawler/sql/crawler_core/` altında yaşar.

## Overview

This directory is the canonical repository surface for the real crawler-core SQL layer of LogisticSearch. It preserves the imported live Pi51 crawler-core PostgreSQL truth as evidence, while also providing the split, executable, and validated working SQL surface that is now used for controlled evolution.

## Genel Bakış

Bu dizin, LogisticSearch’in gerçek crawler-core SQL katmanı için kanonik repository yüzeyidir. İthal edilmiş canlı Pi51 crawler-core PostgreSQL doğrusunu kanıt olarak korurken, artık kontrollü evrim için kullanılan split, çalıştırılabilir ve doğrulanmış çalışma SQL yüzeyini de sağlar.

## Purpose

This surface exists so that crawler-core database logic is no longer trapped only inside the live Pi51 database. It gives the project a versioned, reviewable, auditable, executable, and evolvable SQL working layer centered on GitHub canonical main and Ubuntu Desktop execution discipline.

## Amaç

Bu yüzey, crawler-core veritabanı mantığının artık yalnızca canlı Pi51 veritabanı içinde kapalı kalmaması için vardır. Projeye GitHub canonical main ve Ubuntu Desktop çalışma disiplini merkezli, versiyonlu, gözden geçirilebilir, denetlenebilir, çalıştırılabilir ve evrilebilir bir SQL çalışma katmanı kazandırır.

## Current File Map

### Live evidence surface
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Primary working surface
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Execution and validation entry points
- `900_apply_crawler_core_split_surface.psql.sql`
- `901_preflight_crawler_core_split_surface.psql.sql`
- `902_presence_audit_crawler_core_split_surface.psql.sql`
- `910_validate_crawler_core_split_surface.sh`

### Planning, policy, and seal surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`
- `RUNBOOK_CONTROLLED_APPLY_AND_VALIDATION.md`
- `RUNBOOK_CONTROLLED_EXIT_PATH_VALIDATION.md`

## Güncel Dosya Haritası

### Canlı kanıt yüzeyi
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Ana çalışma yüzeyi
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql` — `frontier.claim_next_url`, `frontier.renew_url_lease`, `frontier.reap_expired_leases`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Execution ve validation giriş noktaları
- `900_apply_crawler_core_split_surface.psql.sql`
- `901_preflight_crawler_core_split_surface.psql.sql`
- `902_presence_audit_crawler_core_split_surface.psql.sql`
- `910_validate_crawler_core_split_surface.sh`

### Planlama, politika ve mühür yüzeyi
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `COVERAGE_MATRIX.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `PREREQUISITES.md`
- `SCRATCH_APPLY_TEST_PLAN.md`
- `SCRATCH_APPLY_VALIDATION_SEAL.md`
- `NEXT_STEP.md`
- `RUNBOOK_CONTROLLED_APPLY_AND_VALIDATION.md`
- `RUNBOOK_CONTROLLED_EXIT_PATH_VALIDATION.md`

## Current Scope

The imported and split crawler-core surface currently covers three schemas:

- `seed`
- `frontier`
- `http_fetch`

At the current sealed point, the covered object counts are:

- schemas: 3
- enum types: 10
- tables: 6
- functions from imported live scope: 10
- post-import controlled extension functions: 1
- indexes: 12

Current post-import controlled extension now present in the split working surface:

- `frontier.renew_url_lease` in `002_frontier_claim_and_lease.sql`

## Mevcut Kapsam

İthal edilmiş ve split edilmiş crawler-core yüzeyi şu anda üç şemayı kapsar:

- `seed`
- `frontier`
- `http_fetch`

Mevcut mühürlü noktada kapsanan nesne sayıları şunlardır:

- şema: 3
- enum type: 10
- tablo: 6
- ithal edilmiş canlı kapsamdan gelen fonksiyon: 10
- ithal-sonrası kontrollü genişletme fonksiyonu: 1
- index: 12

Split çalışma yüzeyinde artık mevcut olan ithal-sonrası kontrollü genişletme şudur:

- `frontier.renew_url_lease` `002_frontier_claim_and_lease.sql` içinde

## Current Validation Status

The split crawler-core SQL surface has been validated successfully on Ubuntu Desktop against the local scratch PostgreSQL database:

- `logisticsearch_crawler_split_scratch`

Validated result:

- preflight: passed
- apply bundle: passed
- reusable presence audit: passed
- reusable validation runner: passed
- missing check count: 0

The live Pi51 crawler database was not mutated during this validation phase.

Additional note:
- `frontier.renew_url_lease` was added as a deliberate post-import extension and has passed targeted scratch smoke validation on `logisticsearch_crawler_lease_renew_scratch`.

## Güncel Doğrulama Durumu

Split crawler-core SQL yüzeyi, Ubuntu Desktop üzerinde yerel scratch PostgreSQL veritabanına karşı başarıyla doğrulanmıştır:

- `logisticsearch_crawler_split_scratch`

Doğrulanan sonuç:

- preflight: geçti
- apply bundle: geçti
- reusable presence audit: geçti
- reusable validation runner: geçti
- missing check count: 0

Bu doğrulama fazı sırasında canlı Pi51 crawler veritabanı değiştirilmemiştir.

Ek not:
- `frontier.renew_url_lease`, bilinçli bir ithal-sonrası genişletme olarak eklenmiştir ve `logisticsearch_crawler_lease_renew_scratch` üzerinde hedefli scratch smoke validation'dan geçmiştir.

## Working Model

The current working model is:

1. preserve the imported live snapshot as evidence
2. evolve the split SQL files as the primary working layer
3. use `901` before apply when validating a target database
4. use `900` as the canonical split execution bundle
5. use `902` as the canonical reusable presence audit
6. use `910` as the canonical one-command scratch validation runner
7. re-run scratch validation after meaningful SQL changes

## Çalışma Modeli

Mevcut çalışma modeli şöyledir:

1. ithal edilmiş canlı snapshot’ı kanıt olarak koru
2. split SQL dosyalarını ana çalışma katmanı olarak evrimleştir
3. bir hedef veritabanını doğrularken apply öncesinde `901` kullan
4. kanonik split execution bundle olarak `900` kullan
5. kanonik reusable presence audit olarak `902` kullan
6. kanonik tek-komut scratch validation runner olarak `910` kullan
7. anlamlı SQL değişikliklerinden sonra scratch doğrulamayı tekrar çalıştır

## Policy

The live snapshot remains comparison truth, but it is no longer the primary editing surface. Normal crawler-core SQL evolution should start from the split working files on Ubuntu Desktop and then be versioned through GitHub canonical main.

## Politika

Canlı snapshot karşılaştırma doğrusu olarak önemini korur, ancak artık ana düzenleme yüzeyi değildir. Normal crawler-core SQL evrimi Ubuntu Desktop üzerindeki split çalışma dosyalarından başlamalı ve sonra GitHub canonical main üzerinden versiyonlanmalıdır.
