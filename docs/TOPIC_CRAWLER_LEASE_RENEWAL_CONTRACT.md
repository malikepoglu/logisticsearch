# Crawler Lease Renewal Contract

## Overview

This document defines the proposed canonical lease-renewal / heartbeat contract for the LogisticSearch crawler.

Its purpose is to close the most visible lifecycle gap identified in the crawler-core surface: long-running fetch work currently has lease acquisition, lease finalization, and expired-lease recovery, but does not yet have an explicit lease-renewal surface.

## Genel Bakış

Bu belge, LogisticSearch crawler için önerilen kanonik lease-renewal / heartbeat sözleşmesini tanımlar.

Amacı, crawler-core yüzeyinde tespit edilen en görünür yaşam döngüsü boşluğunu kapatmaktır: uzun süren fetch işlerinde şu anda lease alma, lease finalization ve expired-lease recovery vardır; ancak açık bir lease-renewal yüzeyi henüz yoktur.

## Problem statement

Current crawler-core behavior already provides:

- claim-time lease acquisition
- finish-time lease release
- expired-lease recovery back to `queued`

However, a long-running fetch may still outlive its original lease.

This creates duplicate-claim risk if:

1. worker A is still genuinely working
2. its lease expires
3. worker B later reaps and reclaims the same URL

## Problem tanımı

Mevcut crawler-core davranışı şimdiden şunları sağlar:

- claim anında lease alma
- finish anında lease bırakma
- expired-lease recovery ile tekrar `queued` durumuna dönüş

Ancak uzun süren bir fetch yine de ilk lease süresini aşabilir.

Bu da şu durumda duplicate-claim riski oluşturur:

1. worker A hâlâ gerçekten çalışıyordur
2. lease süresi dolar
3. worker B aynı URL'yi reap edip tekrar claim eder

## Proposed canonical function

Proposed function name:

- `frontier.renew_url_lease(...)`

This function should do one thing only:

- extend the lease of a currently valid leased URL that is still owned by the same worker

## Önerilen kanonik fonksiyon

Önerilen fonksiyon adı:

- `frontier.renew_url_lease(...)`

Bu fonksiyon yalnızca tek bir iş yapmalıdır:

- hâlâ aynı worker tarafından sahip olunan geçerli bir leased URL'nin lease süresini uzatmak

## Proposed inputs

Recommended input shape:

- `p_url_id bigint`
- `p_lease_token uuid`
- `p_worker_id text`
- `p_now timestamptz default now()`
- `p_extend_by interval`
- `p_touch_host boolean default false`

## Önerilen girdiler

Önerilen girdi şekli:

- `p_url_id bigint`
- `p_lease_token uuid`
- `p_worker_id text`
- `p_now timestamptz default now()`
- `p_extend_by interval`
- `p_touch_host boolean default false`

## Proposed validation rules

The renewal should succeed only if all of these remain true:

1. `p_url_id` is not null
2. `p_lease_token` is not null
3. `p_worker_id` is non-empty
4. `p_extend_by > interval '0 seconds'`
5. target URL currently exists
6. target URL is still in state `leased`
7. target URL still has the same `lease_token`
8. target URL still has the same `lease_owner`
9. renewal is being attempted before the worker has effectively lost ownership

## Önerilen doğrulama kuralları

Yenileme yalnızca aşağıdakilerin hepsi doğruysa başarılı olmalıdır:

1. `p_url_id` null olmamalıdır
2. `p_lease_token` null olmamalıdır
3. `p_worker_id` boş olmamalıdır
4. `p_extend_by > interval '0 seconds'`
5. hedef URL hâlâ mevcut olmalıdır
6. hedef URL hâlâ `leased` durumda olmalıdır
7. hedef URL hâlâ aynı `lease_token` değerine sahip olmalıdır
8. hedef URL hâlâ aynı `lease_owner` değerine sahip olmalıdır
9. yenileme, worker sahipliği fiilen kaybetmeden önce deneniyor olmalıdır

## Proposed effect

If renewal succeeds, the function should:

- keep state as `leased`
- keep the same `lease_token`
- keep the same `lease_owner`
- extend `lease_expires_at` to `p_now + p_extend_by`
- update `updated_at`
- optionally touch host/activity metadata only if there is a clear need

## Önerilen etki

Yenileme başarılı olursa fonksiyon şunları yapmalıdır:

- state'i `leased` olarak korumalıdır
- aynı `lease_token` değerini korumalıdır
- aynı `lease_owner` değerini korumalıdır
- `lease_expires_at` değerini `p_now + p_extend_by` olarak uzatmalıdır
- `updated_at` alanını güncellemelidir
- host/activity metadata'sına yalnızca açık ihtiyaç varsa dokunmalıdır

## Proposed non-goals

The renewal function should **not**:

- perform a new claim
- change the URL lifecycle outcome
- compute retry policy
- compute revisit policy
- decide robots allow/block
- transfer ownership to another worker
- silently recover expired leases
- act as a finish function

## Önerilen non-goal'ler

Yenileme fonksiyonu şunları **yapmamalıdır**:

- yeni claim yapmak
- URL yaşam döngüsü sonucunu değiştirmek
- retry politikası hesaplamak
- revisit politikası hesaplamak
- robots allow/block kararı vermek
- sahipliği başka worker'a aktarmak
- expired lease'leri sessizce toparlamak
- finish fonksiyonu gibi davranmak

## Proposed return shape

Recommended return fields:

- `url_id`
- `host_id`
- `lease_owner`
- `previous_lease_expires_at`
- `new_lease_expires_at`
- `renewed boolean`

The goal is operational clarity rather than minimalist silence.

## Önerilen dönüş şekli

Önerilen dönüş alanları:

- `url_id`
- `host_id`
- `lease_owner`
- `previous_lease_expires_at`
- `new_lease_expires_at`
- `renewed boolean`

Amaç minimal sessizlik değil, operasyonel açıklıktır.

## Recommended worker-side operational rule

Recommended future worker discipline:

- fetch timeout must be shorter than lease duration
- heartbeat interval must be shorter than lease duration
- heartbeat should happen comfortably before expiry, not at the last second

Practical ordering rule:

- `fetch timeout < heartbeat interval < lease duration`

## Önerilen worker-tarafı operasyon kuralı

Önerilen gelecekteki worker disiplini:

- fetch timeout, lease süresinden kısa olmalıdır
- heartbeat aralığı, lease süresinden kısa olmalıdır
- heartbeat son saniyede değil, rahat güvenlik payıyla yapılmalıdır

Pratik sıralama kuralı:

- `fetch timeout < heartbeat interval < lease duration`

## Relation to current crawler-core files

This proposed function belongs conceptually next to:

- `002_frontier_claim_and_lease.sql`

because it extends the ownership lifecycle rather than finalizing it.

It should not be mixed into finalization logic in `003`.

## Mevcut crawler-core dosyalarıyla ilişkisi

Bu önerilen fonksiyon kavramsal olarak şu dosyanın yanına aittir:

- `002_frontier_claim_and_lease.sql`

çünkü finalization yapmaz, ownership yaşam döngüsünü uzatır.

`003` içindeki finalization mantığıyla karıştırılmamalıdır.

## Current design position

Current recommended design position:

1. seal this contract first
2. add the SQL function second
3. validate the SQL behavior on scratch database third
4. only then treat Python worker heartbeat logic as a real implementation target

## Güncel tasarım pozisyonu

Güncel önerilen tasarım pozisyonu şudur:

1. önce bu sözleşmeyi mühürle
2. sonra SQL fonksiyonunu ekle
3. sonra SQL davranışını scratch veritabanında doğrula
4. ancak bundan sonra Python worker heartbeat mantığını gerçek implementasyon hedefi olarak ele al

## Immediate next design consequence

The next technical step after this document should be:

**design and add a narrow, explicit, non-magical lease-renewal SQL surface.**

## Anlık sonraki tasarım sonucu

Bu belgeden sonraki teknik adım şu olmalıdır:

**dar, açık ve sihir yapmayan bir lease-renewal SQL yüzeyi tasarlayıp eklemek.**
