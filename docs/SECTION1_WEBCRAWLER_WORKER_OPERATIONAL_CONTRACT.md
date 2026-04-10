# Crawler Worker Operational Contract

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document defines the current canonical operational contract for a LogisticSearch crawler worker.

It is written as an implementation-facing guide, not as marketing text.

Its purpose is to make the future worker behavior explicit before large Python crawler implementation begins.

This document therefore separates:

1. what a worker may safely assume today
2. what a worker must do today
3. what a worker must **not** assume yet
4. which behaviors still require future SQL and/or service-layer design

## Genel Bakış

Bu belge, bir LogisticSearch crawler worker için mevcut kanonik operasyon sözleşmesini tanımlar.

Pazarlama metni olarak değil, implementasyon odaklı rehber olarak yazılmıştır.

Amacı, büyük Python crawler implementasyonu başlamadan önce gelecekteki worker davranışını açık hale getirmektir.

Bu nedenle şu ayrımı yapar:

1. worker'ın bugün güvenle neyi varsayabileceği
2. worker'ın bugün ne yapması gerektiği
3. worker'ın henüz neyi varsaymaması gerektiği
4. hangi davranışların hâlâ gelecek SQL ve/veya service-layer tasarımı gerektirdiği

## Current worker mission

A crawler worker is expected to do one practical job repeatedly:

1. acquire exactly one eligible URL
2. decide whether robots information must be refreshed
3. decide whether the target path is allowed
4. perform the fetch if allowed
5. finalize the URL with the correct lifecycle outcome
6. repeat under policy limits

## Mevcut worker görevi

Bir crawler worker'ın tekrar tekrar yaptığı pratik iş şudur:

1. tam bir uygun URL almak
2. robots bilgisinin refresh edilmesi gerekip gerekmediğine karar vermek
3. hedef path'in allowed olup olmadığına karar vermek
4. allowed ise fetch yapmak
5. URL'yi doğru yaşam döngüsü sonucuyla finalize etmek
6. politika limitleri altında bu döngüyü tekrarlamak

## Current canonical SQL entry points a worker must respect

### Claim and lease

- `frontier.claim_next_url(...)`
- `frontier.renew_url_lease(...)`
- `frontier.reap_expired_leases(...)`

### Finish transitions

- `frontier.finish_fetch_success(...)`
- `frontier.finish_fetch_retryable_error(...)`
- `frontier.finish_fetch_permanent_error(...)`

### Timing policy support

- `frontier.compute_retry_backoff(...)`
- `frontier.compute_success_next_fetch_at(...)`

### Robots support

- `http_fetch.compute_robots_refresh_decision(...)`
- `http_fetch.compute_robots_allow_decision(...)`
- `http_fetch.upsert_robots_txt_cache(...)`

## Worker'ın uyması gereken mevcut kanonik SQL giriş noktaları

### Claim ve lease

- `frontier.claim_next_url(...)`
- `frontier.renew_url_lease(...)`
- `frontier.reap_expired_leases(...)`

### Finish transition'lar

- `frontier.finish_fetch_success(...)`
- `frontier.finish_fetch_retryable_error(...)`
- `frontier.finish_fetch_permanent_error(...)`

### Zaman-politikası desteği

- `frontier.compute_retry_backoff(...)`
- `frontier.compute_success_next_fetch_at(...)`

### Robots desteği

- `http_fetch.compute_robots_refresh_decision(...)`
- `http_fetch.compute_robots_allow_decision(...)`
- `http_fetch.upsert_robots_txt_cache(...)`

## Current safe worker assumptions

A worker may safely assume the following today:

### 1. Database state is the source of truth

The worker must treat PostgreSQL state, not process memory, as the durable truth of:

- claim ownership
- retry waiting
- parse handoff
- dead/permanent failure
- host backoff state
- host next eligible time

### 2. Claim eligibility is centrally enforced

The worker does not need to re-implement host concurrency or host due-time selection logic in Python before claim. The database already gates:

- `queued` / `retry_wait`
- `next_fetch_at`
- `revisit_not_before`
- `pause_until`
- `backoff_until`
- `next_eligible_at`
- `max_concurrency`

### 3. Expired-lease recovery exists

If a worker disappears entirely, the crawler-core SQL layer has a real reaping path for expired leases.

### 4. Success and retry timing are policy-driven

The worker does not need to invent revisit timing or retry timing from scratch. Current SQL policy surfaces already compute them.

## Mevcut güvenli worker varsayımları

Bir worker bugün şu varsayımları güvenle yapabilir:

### 1. Veritabanı durumu tek doğruluk kaynağıdır

Worker, aşağıdaki konuların kalıcı doğrusu olarak process belleğini değil PostgreSQL durumunu görmelidir:

- claim sahipliği
- retry waiting
- parse handoff
- dead/permanent failure
- host backoff durumu
- host next eligible zamanı

### 2. Claim eligibility merkezi olarak uygulanır

Worker, claim öncesinde Python içinde host concurrency veya host due-time seçim mantığını yeniden implement etmek zorunda değildir. Veritabanı şimdiden şu gate'leri uygular:

- `queued` / `retry_wait`
- `next_fetch_at`
- `revisit_not_before`
- `pause_until`
- `backoff_until`
- `next_eligible_at`
- `max_concurrency`

### 3. Expired-lease recovery vardır

Bir worker tamamen kaybolursa crawler-core SQL katmanında expired lease'ler için gerçek bir geri alma yolu vardır.

### 4. Success ve retry zamanlaması politika tabanlıdır

Worker revisit timing veya retry timing'i sıfırdan icat etmek zorunda değildir. Mevcut SQL politika yüzeyleri bunları zaten hesaplar.

## Current mandatory worker behavior

The worker should follow this practical high-level loop.

This operational contract now sits together with the stricter heartbeat discipline and the drain-mode / graceful-shutdown rule defined in:

- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

### Step 1 — claim

Call `frontier.claim_next_url(...)`.

If no row is returned, the worker has no eligible job at that moment and should sleep according to operational policy rather than spin aggressively.

### Step 1B — renew the lease during genuinely long work

If the worker is still legitimately processing the same URL and lease expiry is approaching, it should renew the lease with `frontier.renew_url_lease(...)` before expiry rather than relying on luck.

### Step 2 — inspect robots refresh need

Use `http_fetch.compute_robots_refresh_decision(...)`.

If refresh is needed, the worker should fetch and update robots cache truth before trusting a stale or missing robots view.

### Step 3 — inspect allow/block decision

Use `http_fetch.compute_robots_allow_decision(...)`.

The worker must not silently ignore robots when the host is in respect mode.

### Step 4 — perform fetch or skip for robots reasons

If allowed, perform page fetch.

If not allowed, do **not** pretend that success/retry/permanent finalization fully covers the robots-blocked path. This area still requires explicit lifecycle design completion.

### Step 5 — finalize exactly once

When a fetch concludes, the worker must finalize with the correct canonical function:

- success -> `frontier.finish_fetch_success(...)`
- retryable failure -> `frontier.finish_fetch_retryable_error(...)`
- permanent failure -> `frontier.finish_fetch_permanent_error(...)`

### Step 6 — forget the lease locally after finalization

Once finalization succeeds, the worker must treat the lease as closed and must not continue operating on the URL as if it still owns it.

## Mevcut zorunlu worker davranışı

Worker şu pratik üst seviye döngüyü izlemelidir.

Bu operasyon sözleşmesi artık şu daha katı heartbeat disiplini dokümanıyla birlikte düşünülmelidir:

- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

### Adım 1 — claim

`frontier.claim_next_url(...)` çağır.

### Adım 1B — gerçekten uzun süren işte lease'i yenile

Worker hâlâ aynı URL üzerinde meşru şekilde çalışıyorsa ve lease bitişi yaklaşıyorsa, şansa güvenmek yerine bitişten önce `frontier.renew_url_lease(...)` ile lease yenilemelidir.

Satır dönmezse worker'ın o anda uygun işi yoktur; agresif şekilde spin etmek yerine operasyon politikasına göre uyumalıdır.

### Adım 2 — robots refresh ihtiyacını incele

`http_fetch.compute_robots_refresh_decision(...)` kullan.

Refresh gerekiyorsa worker bayat veya eksik robots görünümüne güvenmeden önce robots cache doğrusunu fetch edip güncellemelidir.

### Adım 3 — allow/block kararını incele

`http_fetch.compute_robots_allow_decision(...)` kullan.

Host respect modundaysa worker robots'ı sessizce görmezden gelmemelidir.

### Adım 4 — fetch yap veya robots nedeniyle atla

Allowed ise page fetch yap.

Allowed değilse success/retry/permanent finalization'ın robots-blocked yolu tam kapsadığını varsayma. Bu alan hâlâ açık yaşam döngüsü tasarımı tamamlaması gerektirir.

### Adım 5 — tam bir kez finalize et

Bir fetch bittiğinde worker doğru kanonik fonksiyonla finalize etmelidir:

- success -> `frontier.finish_fetch_success(...)`
- retryable failure -> `frontier.finish_fetch_retryable_error(...)`
- permanent failure -> `frontier.finish_fetch_permanent_error(...)`

### Adım 6 — finalization sonrası lease'i yerelde unut

Finalization başarılı olduktan sonra worker lease'i kapanmış kabul etmeli ve URL üzerinde hâlâ sahiplik varmış gibi işlem yapmamalıdır.

## Boundary against map presentation-library choice

This worker contract governs crawler-side acquisition, robots handling, fetch behavior, parse continuation, and geospatial-input truth.

It does **not** decide application-side map presentation-library choice.

If the crawler later acquires OSM-derived coordinates or other geospatial fields, that belongs here as data/enrichment truth. But live tracking screens, technical map-analysis screens, and UI-library choice belong to the separate topic document:

- `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`

## Harita gösterim-kütüphanesi seçimine karşı sınır

Bu worker sözleşmesi crawler tarafındaki veri edinimi, robots işleme, fetch davranışı, parse devamı ve coğrafi girdi doğrusunu yönetir.

Uygulama tarafı harita gösterim-kütüphanesi seçimini **belirlemez**.

Crawler ileride OSM-türevli koordinatlar veya başka coğrafi alanlar toplarsa, bu burada veri/zenginleştirme doğrusu olarak yer alır. Ancak canlı takip ekranları, teknik harita-analiz ekranları ve UI-kütüphanesi seçimi ayrı topic dokümana aittir:

- `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`

## Current unsafe assumptions the worker must not make

The worker must **not** assume the following yet.

### Unsafe assumption A — long fetches are automatically lease-safe

The SQL surface is now better than before because `frontier.renew_url_lease(...)` exists. But a worker is **not** automatically lease-safe unless it actually renews before expiry under an explicit operational cadence.

That cadence is now part of the worker-side heartbeat discipline and operating rule, not an optional coding style preference.

This is not yet guaranteed.

An explicit lease-renewal SQL function is now visible in crawler-core: `frontier.renew_url_lease(...)`.

### Unsafe assumption B — graceful global shutdown is already solved

This is not yet guaranteed.

Host-level pause/backoff fields exist, but a global drain contract is not yet sealed.

### Unsafe assumption C — robots-blocked lifecycle finalization is fully integrated

This is not yet guaranteed.

Robots decision support exists, but a dedicated canonical robots-blocked finalize path is not yet visible in the split working SQL surface.

### Unsafe assumption D — process memory is enough for resume

This is false.

Resume safety must always come from database truth rather than from local in-process memory.

## Worker'ın yapmaması gereken mevcut güvensiz varsayımlar

Worker henüz şu varsayımları **yapmamalıdır**.

### Güvensiz varsayım A — uzun fetch'ler otomatik olarak lease-safe'dir

SQL yüzeyi artık eskisine göre daha iyidir; çünkü `frontier.renew_url_lease(...)` vardır. Ancak worker, açık bir operasyon ritmiyle bitişten önce gerçekten yenileme yapmadıkça **otomatik olarak** lease-safe değildir.

Bu henüz garanti edilmemiştir.

Crawler-core içinde artık açık bir lease-renewal SQL fonksiyonu görünmektedir: `frontier.renew_url_lease(...)`.

### Güvensiz varsayım B — graceful global shutdown zaten çözülmüştür

Bu henüz garanti edilmemiştir.

Host düzeyi pause/backoff alanları var, ancak global drain sözleşmesi henüz mühürlü değildir.

### Güvensiz varsayım C — robots-blocked yaşam döngüsü finalization'ı tam entegredir

Bu henüz garanti edilmemiştir.

Robots karar desteği vardır; ancak split çalışma SQL yüzeyinde dedicated kanonik robots-blocked finalize yolu henüz görünmemektedir.

### Güvensiz varsayım D — resume için process belleği yeterlidir

Bu yanlıştır.

Resume güvenliği her zaman yerel process belleğinden değil veritabanı doğrusundan gelmelidir.

## Current power-loss and crash interpretation

### What is already true

If a worker crashes or the machine loses power, the current design still has one strong recovery building block:

- expired leased rows can be reaped back to `queued`

### What is not yet fully true

The project should not yet claim that:

- every in-progress long-running fetch is duplicate-safe
- graceful stop is already coordinated
- every shutdown path is operationally sealed

## Mevcut power-loss ve crash yorumu

### Şimdiden doğru olan

Bir worker çökerse veya makine elektriği kaybederse mevcut tasarımın hâlâ güçlü bir recovery yapı taşı vardır:

- süresi dolmuş leased satırlar tekrar `queued` durumuna alınabilir

### Henüz tam doğru olmayan

Proje henüz şu iddialarda bulunmamalıdır:

- her uzun süren in-progress fetch'in duplicate-safe olduğu
- graceful stop'un şimdiden koordine edildiği
- her shutdown yolunun operasyonel olarak mühürlü olduğu

## Current controlled-stop interpretation

At the current stage, the safest truthful interpretation is:

- a worker may stop between jobs safely
- a worker may crash and later rely on expired-lease recovery
- a worker must not assume that global controlled draining is already fully modeled

## Mevcut kontrollü-stop yorumu

Mevcut aşamada en güvenli ve doğru yorum şudur:

- worker işler arasında güvenli şekilde durabilir
- worker çökebilir ve daha sonra expired-lease recovery'ye dayanabilir
- worker global controlled draining'in şimdiden tam modellenmiş olduğunu varsaymamalıdır

## What future worker implementation should receive before production-grade status

Before the crawler worker is treated as production-grade, the project should strongly consider adding and sealing at least these items:

1. worker-side lease renewal / heartbeat operational adoption using `frontier.renew_url_lease(...)`
2. explicit worker drain / graceful-stop contract
3. explicit robots-blocked finalization path
4. explicit operational runbook for service stop / restart / reboot / poweroff behavior

## Gelecekteki worker implementasyonunun production-grade sayılmadan önce alması gerekenler

Crawler worker production-grade kabul edilmeden önce proje en az şu unsurları eklemeyi ve mühürlemeyi güçlü şekilde değerlendirmelidir:

1. `frontier.renew_url_lease(...)` kullanarak worker-tarafı lease renewal / heartbeat operasyonel benimsenmesi
2. açık worker drain / graceful-stop sözleşmesi
3. açık robots-blocked finalization yolu
4. service stop / restart / reboot / poweroff davranışı için açık operasyon rehberi

## Immediate next design priority

The immediate next design priority is:

**seal the lease-lifecycle gap before large Python crawler implementation begins.**

## Anlık sonraki tasarım önceliği

Anlık sonraki tasarım önceliği şudur:

**büyük Python crawler implementasyonu başlamadan önce lease-lifecycle boşluğunu mühürlemek.**
