# Crawler Worker Heartbeat Operating Rule

## Overview

This document defines the current canonical worker-side heartbeat operating rule for the LogisticSearch crawler.

Its purpose is to close the remaining operational gap after the addition of the explicit SQL lease-renewal surface.

The SQL layer now contains `frontier.renew_url_lease(...)`.  
What still needs to be made explicit is **how a worker must behave around that function**.

This document is therefore not about adding another SQL feature.  
It is about turning the existing lease-renewal surface into a strict operational rule for future worker implementation.

## Genel Bakış

Bu belge, LogisticSearch crawler için mevcut kanonik worker-tarafı heartbeat işletim kuralını tanımlar.

Amacı, açık SQL lease-renewal yüzeyinin eklenmesinden sonra kalan operasyon boşluğunu kapatmaktır.

SQL katmanı artık `frontier.renew_url_lease(...)` fonksiyonunu içerir.  
Açık hale getirilmesi gereken şey artık **worker’ın bu fonksiyon etrafında nasıl davranması gerektiğidir**.

Bu nedenle bu belge yeni bir SQL özellik eklemekle ilgili değildir.  
Mevcut lease-renewal yüzeyini gelecekteki worker implementasyonu için katı bir işletim kuralına dönüştürmekle ilgilidir.

## Current prerequisite truth

The current crawler-core ownership lifecycle already has:

- claim entry via `frontier.claim_next_url(...)`
- explicit lease renewal via `frontier.renew_url_lease(...)`
- finish transitions via `frontier.finish_fetch_success(...)`, `frontier.finish_fetch_retryable_error(...)`, and `frontier.finish_fetch_permanent_error(...)`
- expired-lease recovery via `frontier.reap_expired_leases(...)`

Therefore the remaining discipline is no longer “SQL function missing”.

The remaining discipline is:

- when to renew
- when not to renew
- what to do during graceful stop
- what to do when renewal fails
- how to stay crash-safe without pretending that process memory is durable truth

## Mevcut önkoşul doğrusu

Mevcut crawler-core ownership yaşam döngüsünde artık şunlar vardır:

- `frontier.claim_next_url(...)` ile claim girişi
- `frontier.renew_url_lease(...)` ile açık lease yenileme
- `frontier.finish_fetch_success(...)`, `frontier.finish_fetch_retryable_error(...)` ve `frontier.finish_fetch_permanent_error(...)` ile finish transition’ları
- `frontier.reap_expired_leases(...)` ile expired-lease recovery

Dolayısıyla kalan disiplin artık “SQL fonksiyonu eksik” değildir.

Kalan disiplin şudur:

- ne zaman yenileme yapılacağı
- ne zaman yenileme yapılmayacağı
- graceful stop sırasında ne yapılacağı
- yenileme başarısız olursa ne yapılacağı
- process belleğini kalıcı doğruluk kaynağı sanmadan crash-safe kalmanın nasıl sağlanacağı

## Core operating rule

A worker may renew a lease only when all of the following are true:

1. it is still legitimately working on the same URL
2. it still owns the current lease
3. lease expiry is approaching within the configured safety window
4. the work is still expected to continue meaningfully
5. the worker has not entered stop/drain mode

If those conditions are not true, the worker must **not** renew.

The renewal mechanism is a safety tool, not a way to hide bad control flow.

## Temel işletim kuralı

Bir worker ancak aşağıdakilerin hepsi doğruysa lease yenileyebilir:

1. hâlâ gerçekten aynı URL üzerinde çalışıyordur
2. mevcut lease’in sahibi hâlâ kendisidir
3. lease bitişi, yapılandırılmış güvenlik penceresi içine girmiştir
4. yapılan iş hâlâ anlamlı şekilde devam edecektir
5. worker stop/drain moduna girmemiştir

Bu şartlar doğru değilse worker **lease yenilememelidir**.

Yenileme mekanizması kötü kontrol akışını gizleme yolu değil, güvenlik aracıdır.

## Renewal trigger rule

The worker must not wait for the last second.

Instead it should define an internal renewal threshold such as:

- renew when remaining lease time falls below a safety threshold
- that threshold must leave enough room for DB round-trip delay, temporary scheduler delay, and one retry margin

The exact numeric values may evolve later, but the operating rule is fixed:

- renew **before** expiry
- renew with safety margin
- never rely on “probably still enough time”

## Yenileme tetik kuralı

Worker son saniyeyi beklememelidir.

Bunun yerine içsel bir yenileme eşiği tanımlamalıdır:

- kalan lease süresi güvenlik eşiğinin altına düşünce yenile
- bu eşik; DB gidiş-dönüş gecikmesi, geçici scheduler gecikmesi ve tek retry marjı için yeterli boşluk bırakmalıdır

Kesin sayısal değerler ileride evrilebilir; ancak işletim kuralı sabittir:

- bitişten **önce** yenile
- güvenlik marjıyla yenile
- “muhtemelen daha zaman var” varsayımına güvenme

## Mandatory worker behavior around long-running work

### 1. Before starting actual fetch work

The worker should record locally:

- claimed `url_id`
- claimed `lease_token`
- claimed `worker_id`
- current lease expiry moment

This local memory is only runtime convenience.  
It must never be treated as stronger than database truth.

### 2. During genuinely long work

If the same URL is still in progress and the safety threshold is crossed, the worker must call:

- `frontier.renew_url_lease(...)`

If renewal succeeds, the worker may continue.

If renewal returns no row or otherwise fails ownership validation, the worker must immediately treat the lease as lost.

### 3. After lease loss

If the worker has lost the lease, it must stop acting as if it still owns the URL.

That means:

- do not keep fetching as normal
- do not write downstream success as if ownership still exists
- do not continue heartbeat attempts blindly
- move into safe abort / safe failure handling in the application layer

## Uzun süren işler etrafındaki zorunlu worker davranışı

### 1. Gerçek fetch işine başlamadan önce

Worker yerel olarak şunları kaydetmelidir:

- claim edilen `url_id`
- claim edilen `lease_token`
- claim edilen `worker_id`
- mevcut lease bitiş anı

Bu yerel hafıza yalnızca çalışma anı kolaylığıdır.  
Asla veritabanı doğrusundan daha güçlü görülmemelidir.

### 2. Gerçekten uzun süren iş sırasında

Aynı URL üzerindeki iş hâlâ sürüyorsa ve güvenlik eşiği geçilmişse worker şu çağrıyı yapmalıdır:

- `frontier.renew_url_lease(...)`

Yenileme başarılı olursa worker devam edebilir.

Yenileme satır döndürmezse veya sahiplik doğrulamasında başarısız olursa worker lease’i kaybetmiş kabul etmelidir.

### 3. Lease kaybından sonra

Worker lease’i kaybettiyse artık URL’nin sahibiymiş gibi davranmayı bırakmalıdır.

Bu şu anlama gelir:

- normal şekilde fetch’e devam etme
- sahiplik sürüyormuş gibi downstream success yazma
- kör şekilde heartbeat denemelerine devam etme
- uygulama katmanında güvenli abort / güvenli failure davranışına geçme

## Graceful stop / drain rule

When the worker enters a deliberate stop state, it must switch to **drain mode**.

Drain mode means:

1. do not claim new URLs
2. do not renew leases just to prolong work indefinitely
3. either finish the currently owned URL cleanly within the remaining lease window
4. or stop and allow bounded lease recovery to occur through expiry + reap

A graceful stop is therefore not “pretend nothing changed”.

It is a controlled transition from active ownership to no-new-work behavior.

## Graceful stop / drain kuralı

Worker bilinçli bir stop durumuna girdiğinde **drain mode**’a geçmelidir.

Drain mode şu anlama gelir:

1. yeni URL claim etme
2. işi süresiz uzatmak için lease yenileme yapma
3. ya mevcut sahip olunan URL’yi kalan lease penceresi içinde temiz biçimde bitir
4. ya da durup bounded lease recovery’nin expiry + reap ile gerçekleşmesine izin ver

Dolayısıyla graceful stop, “hiçbir şey değişmemiş gibi davran” demek değildir.

Aktif sahiplikten yeni iş almama davranışına kontrollü geçiştir.

## Power-loss and crash rule

Crash-safety must come from bounded lease duration plus expired-lease recovery, not from fantasy assumptions.

This means:

- the worker must assume sudden termination is possible
- active ownership must be reconstructible from PostgreSQL state
- lease duration must stay bounded
- renewal must be explicit and periodic, not hidden
- recovery after sudden death must rely on lease expiry and later reaping

A crash is not a special success path.  
It is an interruption that the system tolerates by design.

## Elektrik kesilmesi ve crash kuralı

Crash-safety hayali varsayımlardan değil, bounded lease süresi ile expired-lease recovery’den gelmelidir.

Bu şu anlama gelir:

- worker ani sonlanmanın mümkün olduğunu varsaymalıdır
- aktif sahiplik PostgreSQL durumundan yeniden kurulabilir olmalıdır
- lease süresi bounded kalmalıdır
- yenileme açık ve periyodik olmalıdır; gizli olmamalıdır
- ani ölüm sonrası toparlama lease expiry ve daha sonra reap üzerinden yürümelidir

Crash özel bir başarı yolu değildir.  
Sistem tasarımı tarafından tolere edilen bir kesintidir.

## Relationship to shutdown helpers

A future sudo-less or controlled shutdown helper may later be added at the OS/service layer.

But even if such a helper exists, the worker rule must remain the same:

- stop claiming new work first
- do not invent magical ownership persistence
- finish current work only if safely possible
- otherwise let bounded lease recovery do its job

## Shutdown yardımcılarıyla ilişki

İleride OS/service katmanında sudo’suz veya kontrollü bir shutdown helper eklenebilir.

Ancak böyle bir yardımcı eklense bile worker kuralı aynı kalmalıdır:

- önce yeni iş claim etmeyi bırak
- sihirli sahiplik kalıcılığı icat etme
- yalnızca güvenliyse mevcut işi bitir
- aksi halde bounded lease recovery’nin işini yapmasına izin ver

## Non-goals

This operating rule does **not** define:

- exact Python code shape
- exact thread model
- exact async model
- exact numeric heartbeat cadence
- exact systemd unit shape
- exact shutdown wrapper implementation

Those are later implementation topics.

What is being sealed here is the operating rule, not every final engineering detail.

## Non-goal’ler

Bu işletim kuralı şunları **tanımlamaz**:

- kesin Python kod şekli
- kesin thread modeli
- kesin async modeli
- kesin sayısal heartbeat ritmi
- kesin systemd unit şekli
- kesin shutdown wrapper implementasyonu

Bunlar daha sonraki implementasyon konularıdır.

Burada mühürlenen şey her son mühendislik ayrıntısı değil, işletim kuralıdır.

## Immediate next design consequence

The next disciplined step after this document should be:

- align the crawler top-level contract docs to treat SQL lease renewal as existing truth
- then design the future Python worker around this operating rule
- not the other way around

## Anlık sonraki tasarım sonucu

Bu belgeden sonraki disiplinli adım şu olmalıdır:

- crawler üst-seviye sözleşme dokümanlarını SQL lease renewal’ı artık mevcut doğruluk olarak hizalamak
- sonra gelecekteki Python worker’ı bu işletim kuralı etrafında tasarlamak
- tersi değil
