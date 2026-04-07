# Crawler Lease Renewal Contract

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document defines the current canonical lease-renewal / heartbeat SQL contract for the LogisticSearch crawler.

Its purpose is to record and standardize the lease-renewal SQL surface that now exists in crawler-core, and to make clear that the remaining gap has shifted from SQL absence to worker-side heartbeat discipline.

Current status note:
- `frontier.renew_url_lease(...)` has now been added to `sql/crawler_core/002_frontier_claim_and_lease.sql`
- targeted scratch smoke validation has passed on `logisticsearch_crawler_lease_renew_scratch`
- the remaining design problem is now operational worker usage, not absence of SQL surface
- the canonical worker-side usage rule is documented in `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- the canonical drain/graceful-shutdown rule is documented in `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

## Genel Bakış

Bu belge, LogisticSearch crawler için mevcut kanonik lease-renewal / heartbeat SQL sözleşmesini tanımlar.

Amacı, crawler-core içinde artık mevcut olan lease-renewal SQL yüzeyini kayda geçirip standardize etmek ve kalan boşluğun artık SQL yokluğundan worker-tarafı heartbeat disiplinine kaydığını açık hale getirmektir.

Mevcut durum notu:
- `frontier.renew_url_lease(...)` artık `sql/crawler_core/002_frontier_claim_and_lease.sql` içine eklenmiştir
- hedefli scratch smoke validation `logisticsearch_crawler_lease_renew_scratch` üzerinde geçmiştir
- artık kalan tasarım problemi SQL yüzeyinin yokluğu değil, worker-tarafı operasyon kullanımıdır
- kanonik worker-tarafı kullanım kuralı `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md` içinde dokümante edilmiştir
- kanonik drain/graceful-shutdown kuralı `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md` içinde dokümante edilmiştir

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

## Current canonical function

Proposed function name:

- `frontier.renew_url_lease(...)`

This function should do one thing only:

- extend the lease of a currently valid leased URL that is still owned by the same worker

## Mevcut kanonik fonksiyon

Önerilen fonksiyon adı:

- `frontier.renew_url_lease(...)`

Bu fonksiyon yalnızca tek bir iş yapmalıdır:

- hâlâ aynı worker tarafından sahip olunan geçerli bir leased URL'nin lease süresini uzatmak

## Current input shape

Recommended input shape:

- `p_url_id bigint`
- `p_lease_token uuid`
- `p_worker_id text`
- `p_now timestamptz default now()`
- `p_extend_by interval`
- `p_touch_host boolean default false`

## Mevcut girdi şekli

Önerilen girdi şekli:

- `p_url_id bigint`
- `p_lease_token uuid`
- `p_worker_id text`
- `p_now timestamptz default now()`
- `p_extend_by interval`
- `p_touch_host boolean default false`

## Current validation rules

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

## Mevcut doğrulama kuralları

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

## Current effect

If renewal succeeds, the function should:

- keep state as `leased`
- keep the same `lease_token`
- keep the same `lease_owner`
- extend `lease_expires_at` to `p_now + p_extend_by`
- update `updated_at`
- optionally touch host/activity metadata only if there is a clear need

## Mevcut etki

Yenileme başarılı olursa fonksiyon şunları yapmalıdır:

- state'i `leased` olarak korumalıdır
- aynı `lease_token` değerini korumalıdır
- aynı `lease_owner` değerini korumalıdır
- `lease_expires_at` değerini `p_now + p_extend_by` olarak uzatmalıdır
- `updated_at` alanını güncellemelidir
- host/activity metadata'sına yalnızca açık ihtiyaç varsa dokunmalıdır

## Current non-goals

The renewal function should **not**:

- perform a new claim
- change the URL lifecycle outcome
- compute retry policy
- compute revisit policy
- decide robots allow/block
- transfer ownership to another worker
- silently recover expired leases
- act as a finish function

## Mevcut non-goal'ler

Yenileme fonksiyonu şunları **yapmamalıdır**:

- yeni claim yapmak
- URL yaşam döngüsü sonucunu değiştirmek
- retry politikası hesaplamak
- revisit politikası hesaplamak
- robots allow/block kararı vermek
- sahipliği başka worker'a aktarmak
- expired lease'leri sessizce toparlamak
- finish fonksiyonu gibi davranmak

## Current return shape

Recommended return fields:

- `url_id`
- `host_id`
- `lease_owner`
- `previous_lease_expires_at`
- `new_lease_expires_at`
- `renewed boolean`

The goal is operational clarity rather than minimalist silence.

## Mevcut dönüş şekli

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

Current design position:

1. the contract is documented
2. the SQL function now exists in `002_frontier_claim_and_lease.sql`
3. targeted scratch smoke validation has passed
4. the next remaining work is worker-side heartbeat usage discipline rather than SQL existence
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

**seal the worker-side heartbeat operating rule around the existing narrow, explicit, non-magical lease-renewal SQL surface.**

## Anlık sonraki tasarım sonucu

Bu belgeden sonraki teknik adım şu olmalıdır:

**mevcut dar, açık ve sihir yapmayan lease-renewal SQL yüzeyi etrafında worker-tarafı heartbeat işletim kuralını mühürlemek.**
