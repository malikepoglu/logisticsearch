# Crawler Lifecycle Contract

## Purpose
## Amaç

This document makes one controlled SECTION1 webcrawler rule, contract, runbook, or boundary explicit in a beginner-readable way.

Bu belge, kontrollü bir SECTION1 webcrawler kuralını, sözleşmesini, runbook'unu veya sınırını başlangıç seviyesinde okunabilir biçimde açık hale getirir.

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document defines the current canonical lifecycle contract for the LogisticSearch crawler core.

Its purpose is to explain, in explicit operational language, how a crawler URL enters work, becomes leased, is finalized, is retried, is revisited, and is recovered after interruption.

This document is intentionally contract-oriented. It does not pretend that every desired feature already exists. It records:

1. what the current crawler-core SQL surface already guarantees
2. what the current crawler-core SQL surface does **not** yet guarantee
3. which later additions must be treated as explicit future work rather than silent assumptions

## Genel Bakış

Bu belge, LogisticSearch crawler core için mevcut kanonik yaşam döngüsü sözleşmesini tanımlar.

Amacı; bir crawler URL'sinin işe nasıl girdiğini, nasıl leased olduğunu, nasıl finalize edildiğini, nasıl retry edildiğini, nasıl revisit edildiğini ve kesinti sonrası nasıl toparlandığını açık operasyon diliyle açıklamaktır.

Bu belge bilinçli olarak sözleşme odaklıdır. Arzu edilen her özelliğin şimdiden mevcut olduğunu varsaymaz. Şunları kayda geçirir:

1. mevcut crawler-core SQL yüzeyinin halihazırda neyi garanti ettiği
2. mevcut crawler-core SQL yüzeyinin henüz neyi garanti etmediği
3. daha sonra eklenecek hangi unsurların sessiz varsayım değil, açık gelecek işi olarak ele alınması gerektiği

## Current canonical SQL surfaces

The current crawler lifecycle is distributed across these crawler-core surfaces:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Each file has a distinct responsibility. Lifecycle safety depends on their combined behavior rather than on any single file.

## Mevcut kanonik SQL yüzeyleri

Mevcut crawler yaşam döngüsü şu crawler-core yüzeylerine dağılmıştır:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`

Her dosyanın ayrı bir sorumluluğu vardır. Yaşam döngüsü güvenliği tek bir dosyaya değil, bunların birleşik davranışına dayanır.

## Responsibility map

### `001_seed_frontier_http_fetch_base.sql`

Base schema and state surface.

This file defines the durable shape of the crawler memory, including:

- host scheduling fields
- URL lifecycle state fields
- lease fields
- pause/backoff/eligibility fields
- retry counters
- parse handoff states
- robots-related base structures

### `002_frontier_claim_and_lease.sql`

Lease-entry and lease-recovery surface.

This file is responsible for:

- selecting exactly one eligible URL for work
- enforcing host eligibility gates at claim time
- enforcing host concurrency limits at claim time
- assigning `lease_token`, `lease_owner`, `lease_acquired_at`, `lease_expires_at`
- renewing an already-owned active lease via `frontier.renew_url_lease(...)`
- reaping expired leases back to `queued`

### `003_frontier_finish_transitions.sql`

Fetch-finalization surface.

This file is responsible for finalizing a leased URL into one of the currently implemented outcomes:

- success -> `parse_pending`
- retryable error -> `retry_wait`
- permanent error -> `dead`
- robots-blocked decision -> `dead`

It also clears lease fields and records outcome metadata.

### `004_frontier_politeness_and_freshness.sql`

Timing-policy surface.

This file is responsible for computing:

- retry backoff timing
- success revisit timing
- jittered success revisit timing
- timing values later written by finalization logic

### `005_http_fetch_robots_cache_and_enforcement.sql`

Robots-cache and robots-decision surface.

This file is responsible for:

- storing/updating robots cache truth
- deciding whether robots cache should be refreshed
- deciding whether a path is allowed or blocked by current robots cache

## Sorumluluk haritası

### `001_seed_frontier_http_fetch_base.sql`

Temel şema ve durum yüzeyi.

Bu dosya, crawler hafızasının kalıcı şeklini tanımlar. Buna şunlar dahildir:

- host scheduling alanları
- URL yaşam döngüsü state alanları
- lease alanları
- pause/backoff/eligibility alanları
- retry sayaçları
- parse handoff durumları
- robots ile ilişkili temel yapılar

### `002_frontier_claim_and_lease.sql`

Lease'e giriş ve lease toparlama yüzeyi.

Bu dosya şunlardan sorumludur:

- iş için tam bir uygun URL seçmek
- claim anında host eligibility gate'lerini uygulamak
- claim anında host concurrency limitlerini uygulamak
- `lease_token`, `lease_owner`, `lease_acquired_at`, `lease_expires_at` atamak
- hâlâ aynı worker'a ait aktif bir lease'i `frontier.renew_url_lease(...)` ile yenilemek
- süresi dolmuş lease'leri tekrar `queued` durumuna almak

### `003_frontier_finish_transitions.sql`

Fetch-finalization yüzeyi.

Bu dosya leased bir URL'yi şu anda uygulanmış sonuçlardan birine finalize etmekten sorumludur:

- başarı -> `parse_pending`
- retryable error -> `retry_wait`
- permanent error -> `dead`
- robots tarafından engellenen karar -> `dead`

Aynı zamanda lease alanlarını temizler ve sonuç metadata'sını kaydeder.

### `004_frontier_politeness_and_freshness.sql`

Zaman-politikası yüzeyi.

Bu dosya şunları hesaplamaktan sorumludur:

- retry backoff zamanlaması
- başarı sonrası revisit zamanlaması
- jitter uygulanmış başarı revisit zamanlaması
- daha sonra finalization mantığı tarafından yazılan zaman değerleri

### `005_http_fetch_robots_cache_and_enforcement.sql`

Robots-cache ve robots-karar yüzeyi.

Bu dosya şunlardan sorumludur:

- robots cache doğrusunu saklamak/güncellemek
- robots cache'in refresh edilip edilmeyeceğine karar vermek
- bir path'in mevcut robots cache'e göre allowed mı blocked mı olduğuna karar vermek

## Current URL lifecycle states visible in base truth

The current URL state family includes:

- `queued`
- `leased`
- `fetched`
- `parse_pending`
- `parsed`
- `retry_wait`
- `blocked_robots`
- `dead`
- `paused`

Important note:

The existence of a state in the enum does **not** automatically mean that every transition into and out of that state is already fully implemented in the split working SQL surface.

## Temel doğruda görünen mevcut URL yaşam döngüsü durumları

Mevcut URL state ailesi şunları içerir:

- `queued`
- `leased`
- `fetched`
- `parse_pending`
- `parsed`
- `retry_wait`
- `blocked_robots`
- `dead`
- `paused`

Önemli not:

Bir state'in enum içinde bulunması, split çalışma SQL yüzeyinde o state'e giriş ve çıkışların hepsinin şimdiden tam uygulanmış olduğu anlamına **gelmez**.

## Current guaranteed lifecycle behavior

### 1. Claim entry

A worker may claim only an eligible URL.

Current eligibility gate behavior includes:

- state must be `queued` or `retry_wait`
- `next_fetch_at <= now`
- `revisit_not_before` must not block the URL
- host must be `active`
- host must not be under `pause_until`
- host must not be under `backoff_until`
- host `next_eligible_at` must allow work
- host active lease count must remain below `max_concurrency`

### 2. Lease acquisition

On successful claim:

- URL becomes `leased`
- a new `lease_token` is created
- `lease_owner` is written
- `lease_acquired_at` is written
- `lease_expires_at` is written
- host `next_eligible_at` is advanced
- URL fetch-attempt counters are updated

### 3. Expired lease recovery

If a worker dies, disappears, or never finalizes the URL, the current crawler-core surface can recover the work by reaping expired leases.

This means:

- a stale `leased` row is not supposed to remain permanently lost
- expired leases can be pushed back to `queued`
- reboot/crash-safe resume has a real SQL foundation

### 4. Success finalization

A valid leased URL may be finalized as success.

Current guaranteed effects include:

- state becomes `parse_pending`
- lease fields are cleared
- success metadata is updated
- `consecutive_error_count` resets to zero
- `next_fetch_at` is written from explicit input or computed policy

Current runtime-side clarification:

- success finalization may happen only after optional same-lease durable success-side work has either completed or been deliberately skipped
- the current optional parse-side continuation is attempted only when fetched content is parse-suitable and the connected database exposes the `parse` schema
- crawler_core-only scratch databases may therefore reach a valid success finalization without parse persistence, because missing `parse` schema is treated as an explicit skip condition rather than as a fatal contradiction
- in the current runtime contract, `parse_pending` is a transient crawler-core handoff state rather than a long-lived scheduling home
- after optional parse-side durable work has completed or been deliberately skipped, the runtime must release the frontier row from `parse_pending` back to `queued` while preserving the already-computed revisit schedule in `next_fetch_at`
- parse-layer review/export decisions live in `parse` / `outbox` truth surfaces and must not leave `frontier.url` stranded permanently in `parse_pending`

Güncel runtime-tarafı açıklama:

- success finalization, ancak opsiyonel aynı-lease durable success-tarafı iş ya tamamlandıktan ya da bilinçli olarak atlandıktan sonra gerçekleşebilir
- güncel opsiyonel parse-tarafı continuation yalnızca fetch edilen içerik parse için uygunsa ve bağlı veritabanı `parse` şemasını sağlıyorsa denenir
- bu nedenle yalnızca crawler_core içeren scratch veritabanları, `parse` şeması yoksa bile geçerli bir success finalization sonucuna ulaşabilir; çünkü eksik `parse` şeması fatal bir çelişki değil, açık bir skip koşulu olarak ele alınır
- güncel runtime sözleşmesinde `parse_pending`, uzun ömürlü bir planlama yuvası değil, geçici bir crawler-core aktarım durumudur
- opsiyonel parse-tarafı kalıcı iş tamamlandıktan ya da bilinçli olarak atlandıktan sonra runtime, `frontier.url` satırını `parse_pending` durumundan tekrar `queued` durumuna bırakmalı ve önceden hesaplanmış `next_fetch_at` revisit planını korumalıdır
- parse-tarafı review/export kararları `parse` / `outbox` doğruluk yüzeylerinde yaşar; bu kararlar `frontier.url` satırını kalıcı biçimde `parse_pending` içinde mahsur bırakmamalıdır

### 5. Retryable-error finalization

A valid leased URL may be finalized as retryable error.

Current guaranteed effects include:

- state becomes `retry_wait`
- lease fields are cleared
- retryable counters are incremented
- `consecutive_error_count` increases
- URL `next_fetch_at` is advanced by retry policy
- host `backoff_until` is advanced by retry policy

### 6. Permanent-error finalization

A valid leased URL may be finalized as permanent error.

Current guaranteed effects include:

- state becomes `dead`
- robots-blocked decisions currently use the same permanent-error exit boundary and are persisted with `last_error_class = 'robots_blocked'`
- lease fields are cleared
- permanent-error counters are incremented
- host error metadata is updated

### 7. Success freshness policy

Current success freshness policy is computed by:

- `seed.seed_url.recrawl_interval`, else
- `seed.source.default_recrawl_interval`, else
- fallback `7 days`

and then jittered by host success jitter.

### 8. Retry backoff policy

Current retry backoff policy is computed from host policy fields:

- `retry_backoff_base_ms`
- `retry_backoff_cap_ms`

using exponential growth capped at host maximum.

### 9. Robots decision support

Current robots support can already answer:

- should robots cache be refreshed?
- is this URL path allowed, blocked, or only tentatively allowed because cache is missing or weak?

## Mevcut garanti edilen yaşam döngüsü davranışı

### 1. Claim girişi

Bir worker yalnızca uygun bir URL'yi claim edebilir.

Mevcut eligibility gate davranışı şunları içerir:

- state `queued` veya `retry_wait` olmalıdır
- `next_fetch_at <= now` olmalıdır
- `revisit_not_before` URL'yi bloklamamalıdır
- host `active` olmalıdır
- host `pause_until` altında olmamalıdır
- host `backoff_until` altında olmamalıdır
- host `next_eligible_at` çalışmaya izin vermelidir
- host aktif lease sayısı `max_concurrency` altında kalmalıdır

### 2. Lease alma

Başarılı claim sonrası:

- URL `leased` olur
- yeni bir `lease_token` üretilir
- `lease_owner` yazılır
- `lease_acquired_at` yazılır
- `lease_expires_at` yazılır
- host `next_eligible_at` ileri alınır
- URL fetch-attempt sayaçları güncellenir

### 3. Süresi dolmuş lease toparlama

Bir worker ölürse, kaybolursa veya URL'yi hiç finalize etmezse, mevcut crawler-core yüzeyi süresi dolmuş lease'leri geri alarak işi toparlayabilir.

Bu şu anlama gelir:

- bayat bir `leased` satırın sonsuza kadar kaybolması beklenmez
- süresi dolmuş lease'ler tekrar `queued` durumuna itilebilir
- reboot/crash-safe resume için gerçek bir SQL temeli vardır

### 4. Başarı finalization'ı

Geçerli leased bir URL başarı olarak finalize edilebilir.

Mevcut garanti edilen etkiler şunları içerir:

- state `parse_pending` olur
- lease alanları temizlenir
- success metadata güncellenir
- `consecutive_error_count` sıfırlanır
- `next_fetch_at`, açık girişten veya hesaplanmış politikadan yazılır

### 5. Retryable-error finalization'ı

Geçerli leased bir URL retryable error olarak finalize edilebilir.

Mevcut garanti edilen etkiler şunları içerir:

- state `retry_wait` olur
- lease alanları temizlenir
- retryable sayaçları artırılır
- `consecutive_error_count` artar
- URL `next_fetch_at` retry politikasına göre ileri alınır
- host `backoff_until` retry politikasına göre ileri alınır

### 6. Permanent-error finalization'ı

Geçerli leased bir URL permanent error olarak finalize edilebilir.

Mevcut garanti edilen etkiler şunları içerir:

- state `dead` olur
- robots tarafından engellenen kararlar şu anda aynı permanent-error çıkış sınırını kullanır ve `last_error_class = 'robots_blocked'` olarak kalıcılaştırılır
- lease alanları temizlenir
- permanent-error sayaçları artırılır
- host hata metadata'sı güncellenir

### 7. Başarı sonrası freshness politikası

Mevcut success freshness politikası şu sıradan hesaplanır:

- `seed.seed_url.recrawl_interval`, yoksa
- `seed.source.default_recrawl_interval`, yoksa
- fallback `7 days`

ve ardından host success jitter ile dağıtılır.

### 8. Retry backoff politikası

Mevcut retry backoff politikası host politika alanlarından hesaplanır:

- `retry_backoff_base_ms`
- `retry_backoff_cap_ms`

ve host üst sınırıyla sınırlanmış exponential büyüme kullanır.

### 9. Robots karar desteği

Mevcut robots desteği şimdiden şu soruları cevaplayabilir:

- robots cache refresh edilmeli mi?
- bu URL path allowed mı, blocked mı, yoksa cache eksik/zayıf olduğu için sadece temkinli şekilde mi allowed?

## Current known gaps

The following are important known gaps in the current crawler-core lifecycle contract.

### Gap A — explicit lease-renewal SQL surface now exists, but worker heartbeat discipline is not yet sealed

The current split crawler-core surface shows:

- lease acquisition
- lease release on finish
- expired-lease reap

It now shows an explicit lease-renewal SQL function: `frontier.renew_url_lease(...)` in `002_frontier_claim_and_lease.sql`.

Practical consequence:

A very long fetch may remain valid in worker memory but still outlive its lease in the database, creating duplicate-claim risk.

### Gap B — explicit drain / graceful-shutdown contract now exists, but full adoption is not yet sealed

The top-level drain/graceful-shutdown rule is now documented in:

- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

The remaining gap is no longer contract absence. The remaining gap is consistent worker/service/helper adoption.

The current crawler-core surface has host-level pause/backoff/eligibility controls, but it does **not** currently expose a clear global crawler drain / shutdown SQL contract.

Practical consequence:

Controlled stop behavior must not be silently assumed. It still requires explicit later design across SQL + worker + service layers.

### Gap C — explicit robots-blocked finalization path is not visible

The base state family contains `blocked_robots`, but the currently visible split finalization surface does not show a dedicated finalize function that moves a leased URL or a scheduled URL into a robots-blocked lifecycle outcome.

Practical consequence:

The project should not pretend that robots decision support is identical to fully integrated robots-blocked lifecycle finalization.

### Gap D — worker operational contract is documented, but lease-renewal worker usage is not yet sealed

The SQL surface provides strong building blocks, but a full canonical worker contract still needs to define:

- claim cadence
- fetch timeout relation to lease duration
- lease renewal expectation
- graceful drain behavior
- crash restart behavior
- shutdown/poweroff interaction

## Mevcut bilinen boşluklar

Aşağıdakiler mevcut crawler-core yaşam döngüsü sözleşmesindeki önemli bilinen boşluklardır.

### Boşluk A — açık lease-renewal SQL yüzeyi artık mevcut, ancak worker heartbeat disiplini henüz mühürlenmiş değil

Mevcut split crawler-core yüzeyi şunları gösteriyor:

- lease alma
- finish sırasında lease bırakma
- süresi dolmuş lease reap

Artık `002_frontier_claim_and_lease.sql` içinde açık bir lease-renewal SQL fonksiyonu görünmektedir: `frontier.renew_url_lease(...)`.

Pratik sonuç:

Çok uzun bir fetch worker belleğinde hâlâ geçerli olabilir ama veritabanındaki lease süresini aşabilir; bu da duplicate-claim riski doğurur.

### Boşluk B — açık drain / graceful-shutdown sözleşmesi artık mevcut, ancak tam benimsenme henüz mühürlenmiş değil

Üst seviye drain/graceful-shutdown kuralı artık burada dokümante edilmiştir:

- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

Kalan boşluk artık sözleşme yokluğu değildir. Kalan boşluk, worker/service/helper tarafında tutarlı benimsenmedir.

Mevcut crawler-core yüzeyinde host düzeyi pause/backoff/eligibility kontrolleri vardır; ancak ayrı ve kanonik bir global crawler drain / shutdown SQL sözleşmesi bu yüzeyde henüz standardize edilmemiştir.

Pratik sonuç:

Kontrollü stop davranışı sessizce varsayılmamalıdır. Bu konu hâlâ SQL + worker + service katmanları boyunca açık tasarım gerektirir.

### Boşluk C — açık robots-blocked finalization yolu görünmüyor

Temel state ailesi içinde `blocked_robots` var, ancak şu anda görünen split finalization yüzeyi leased veya scheduled bir URL'yi özel bir robots-blocked yaşam döngüsü sonucuna taşıyan ayrı bir finalize fonksiyonu göstermiyor.

Pratik sonuç:

Proje, robots karar desteğini tam entegre robots-blocked yaşam döngüsü finalization'ı ile aynı şeymiş gibi sunmamalıdır.

### Boşluk D — worker operasyon sözleşmesi henüz mühürlü değil

SQL yüzeyi güçlü yapı taşları sağlıyor, ancak tam kanonik worker sözleşmesi hâlâ şunları tanımlamalıdır:

- claim ritmi
- fetch timeout ile lease duration ilişkisi
- lease renewal beklentisi
- graceful drain davranışı
- crash restart davranışı
- shutdown/poweroff etkileşimi

## What is already safe to say

The current crawler-core surface is already strong enough to say the following safely:

1. crawler memory is database-backed, not process-memory-backed
2. crash recovery is partially real because expired leases can be reaped
3. anti-ban pacing is partially real because host eligibility and delay gates exist
4. retry and revisit timing are already policy-driven
5. robots refresh/allow decision support already exists

## Şimdiden güvenle söylenebilecekler

Mevcut crawler-core yüzeyi şunları güvenle söyleyecek kadar güçlüdür:

1. crawler hafızası process belleğine değil veritabanına dayanır
2. crash recovery kısmen gerçektir; çünkü expired lease'ler geri alınabilir
3. anti-ban pacing kısmen gerçektir; çünkü host eligibility ve delay gate'leri vardır
4. retry ve revisit zamanlaması şimdiden politika tabanlıdır
5. robots refresh/allow karar desteği şimdiden mevcuttur

## What must not be claimed yet

The project must **not** claim yet that:

- long-running fetches are fully duplicate-safe
- graceful shutdown is already completely designed
- robots-blocked finalization is already fully integrated
- every operational crawler edge case is already sealed

## Henüz iddia edilmemesi gerekenler

Proje henüz şu iddialarda **bulunmamalıdır**:

- uzun süren fetch'lerin tamamen duplicate-safe olduğu
- graceful shutdown'ın şimdiden tamamen tasarlanmış olduğu
- robots-blocked finalization'ın şimdiden tam entegre olduğu
- crawler operasyonundaki her edge case'in şimdiden mühürlendiği

## Immediate next design consequence

The next high-priority design question is:

**Should worker heartbeat behavior now be sealed around the explicit `frontier.renew_url_lease(...)` surface before Python implementation is treated as production-grade?**

Current answer:

**Yes, this is the most visible lifecycle gap and should be treated as a serious design priority.**

## Anlık sonraki tasarım sonucu

Bir sonraki yüksek öncelikli tasarım sorusu şudur:

**Python implementasyonu production-grade kabul edilmeden önce worker heartbeat davranışı artık açık `frontier.renew_url_lease(...)` yüzeyi etrafında mühürlenmeli mi?**

Mevcut cevap:

**Evet, bu en görünür yaşam döngüsü boşluğudur ve ciddi tasarım önceliği olarak ele alınmalıdır.**
