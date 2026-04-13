# Outbox Core Primary Working Surface Seal

## Overview

This document seals the current decision about which SQL surface is the primary working layer for outbox-core evolution.

## Genel Bakış

Bu belge, outbox-core evrimi için hangi SQL yüzeyinin ana çalışma katmanı olduğu konusundaki güncel kararı mühürler.

## Sealed decision

The primary working SQL surface for outbox-core is now:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

## Mühürlenen karar

Outbox-core için ana çalışma SQL yüzeyi artık şudur:

- `001_outbox_base.sql`
- `002_outbox_enqueue_and_batch_creation.sql`
- `003_outbox_batch_attachment_and_state_transitions.sql`

## What is no longer the primary editing surface

The imported live snapshot remains preserved and important, but it is no longer the primary editing layer:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Artık ana düzenleme yüzeyi olmayan katman

İthal edilmiş canlı snapshot korunur ve önemini sürdürür; ancak artık ana düzenleme katmanı değildir:

- `001_pi51_live_outbox_schema.sql`
- `001_pi51_live_outbox_inventory.txt`
- `001_pi51_live_outbox_schema.sha256`

## Why this decision is sealed

This decision is sealed because the split working surface has now been:

1. derived from imported live Pi51 truth
2. checked for coverage against the imported scope
3. execution-surfaced through `900 / 901 / 902`
4. validated successfully on a scratch PostgreSQL database with required upstream layers

## Bu karar neden mühürlendi

Bu karar şu nedenlerle mühürlenmiştir:

1. split çalışma yüzeyi, ithal edilmiş canlı Pi51 doğrusundan türetilmiştir
2. ithal edilmiş kapsamla kapsama açısından kontrol edilmiştir
3. `900 / 901 / 902` üzerinden execution surface haline getirilmiştir
4. gerekli upstream katmanlarla birlikte scratch PostgreSQL veritabanında başarıyla doğrulanmıştır

## Practical rule from now on

From this point forward:

- normal SQL evolution starts from the split working files
- comparison against live truth is done against the imported snapshot files
- validation is performed through the execution entry points
- meaningful changes should be followed by scratch re-validation

## Bundan sonraki pratik kural

Bu noktadan sonra:

- normal SQL evrimi split çalışma dosyalarından başlar
- canlı doğruluk ile karşılaştırma, ithal edilmiş snapshot dosyaları üzerinden yapılır
- doğrulama, execution giriş noktaları üzerinden yürütülür
- anlamlı değişikliklerden sonra scratch tekrar doğrulaması yapılmalıdır
