# Outbox Core SQL Surface

## Overview

This directory is the canonical repository surface for the live outbox SQL layer imported from Pi51. It preserves the live schema truth as evidence and prepares the surface for later controlled split and validation work.

## Genel Bakış

Bu dizin, Pi51 üzerinden ithal edilen canlı outbox SQL katmanı için kanonik repository yüzeyidir. Canlı şema doğrusunu kanıt olarak korur ve yüzeyi daha sonra yapılacak kontrollü split ve doğrulama çalışmasına hazırlar.

## Purpose

This surface exists so that outbox-layer database logic is no longer trapped only inside the live Pi51 database. It gives the project a versioned, reviewable, auditable import surface.

## Amaç

Bu yüzey, outbox katmanı veritabanı mantığının artık yalnızca canlı Pi51 veritabanı içinde kapalı kalmaması için vardır. Projeye versiyonlu, gözden geçirilebilir ve denetlenebilir bir ithal yüzeyi kazandırır.

## Current Imported Scope

Current imported source:
- live Pi51 `outbox` schema from database `logisticsearch_crawler`

Imported evidence files:
- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Mevcut İthal Kapsam

Mevcut ithal kaynağı:
- `logisticsearch_crawler` veritabanındaki canlı Pi51 `outbox` şeması

İthal kanıt dosyaları:
- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Policy

At this stage, this directory is an import/evidence surface first. Later steps may add chronology-aligned split working files, execution entry points, and validation runners.

## Politika

Bu aşamada bu dizin öncelikle bir ithal/kanıt yüzeyidir. Daha sonraki adımlarda chronology uyumlu split çalışma dosyaları, execution giriş noktaları ve validation runner’lar eklenebilir.
