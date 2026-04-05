# Crawler Core SQL Surface

## Overview

This directory is the canonical repository surface for the real crawler-core SQL layer of LogisticSearch. It brings the live Pi51 crawler-core PostgreSQL truth into the GitHub-centered repository and then reorganizes that truth into chronology-aligned working files.

## Genel Bakış

Bu dizin, LogisticSearch’in gerçek crawler-core SQL katmanı için kanonik repository yüzeyidir. Canlı Pi51 crawler-core PostgreSQL doğrusunu GitHub merkezli repository içine alır ve ardından bu doğruyu chronology uyumlu çalışma dosyalarına dönüştürür.

## Purpose

This surface exists so that crawler-core database logic is no longer trapped only inside the live Pi51 database. It gives the project a versioned, reviewable, auditable, and editable SQL working layer.

## Amaç

Bu yüzey, crawler-core veritabanı mantığının yalnızca canlı Pi51 veritabanı içinde kapalı kalmaması için vardır. Projeye versiyonlu, gözden geçirilebilir, denetlenebilir ve düzenlenebilir bir SQL çalışma katmanı kazandırır.

## Current File Map

### Live evidence surface
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Planning and control surface
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `COVERAGE_MATRIX.md`

### Primary working surface
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Apply entry point
- `900_apply_crawler_core_split_surface.psql.sql`

## Güncel Dosya Haritası

### Canlı kanıt yüzeyi
- `001_pi51_live_seed_frontier_http_fetch_schema.sql`
- `001_pi51_live_seed_frontier_http_fetch_inventory.txt`
- `001_pi51_live_seed_frontier_http_fetch_schema.sha256`

### Planlama ve kontrol yüzeyi
- `CHRONOLOGY_SPLIT_PLAN.md`
- `SURFACE_ROLE_MAP.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`
- `COVERAGE_MATRIX.md`

### Ana çalışma yüzeyi
- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

### Apply giriş noktası
- `900_apply_crawler_core_split_surface.psql.sql`

## Current Scope

The imported and split crawler-core surface currently covers three schemas:

- `seed`
- `frontier`
- `http_fetch`

At the current sealed point, the covered live object counts are:

- schemas: 3
- types: 10
- tables: 6
- functions: 10
- indexes: 12

## Mevcut Kapsam

İthal edilmiş ve split edilmiş crawler-core yüzeyi şu anda üç şemayı kapsar:

- `seed`
- `frontier`
- `http_fetch`

Mevcut mühürlü noktada kapsanan canlı nesne sayıları şunlardır:

- şema: 3
- type: 10
- tablo: 6
- fonksiyon: 10
- index: 12

## Working Model

The current working model is:

1. live Pi51 snapshot is preserved as evidence
2. split SQL files are the primary working surface
3. the apply bundle is the canonical execution entry point
4. future crawler-core SQL evolution should target the split surface first

## Çalışma Modeli

Mevcut çalışma modeli şöyledir:

1. canlı Pi51 snapshot’ı kanıt olarak korunur
2. split SQL dosyaları ana çalışma yüzeyidir
3. apply bundle kanonik execution giriş noktasıdır
4. gelecekteki crawler-core SQL evrimi önce split yüzeyi hedeflemelidir

## Policy

The live snapshot remains important, but it is not the main editing surface anymore. The main editable structure is now the split crawler-core SQL surface on Ubuntu Desktop, versioned in GitHub canonical main.

## Politika

Canlı snapshot önemini korur, ancak artık ana düzenleme yüzeyi değildir. Ana düzenlenebilir yapı artık Ubuntu Desktop üzerindeki split crawler-core SQL yüzeyidir ve GitHub canonical main içinde versiyonlanmaktadır.
