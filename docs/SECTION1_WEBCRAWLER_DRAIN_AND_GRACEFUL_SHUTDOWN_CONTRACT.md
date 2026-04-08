# Crawler Drain and Graceful Shutdown Contract

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document defines the current canonical drain and graceful-shutdown contract for the LogisticSearch crawler.

Its purpose is to close the next major operational gap after lease renewal and worker heartbeat discipline were defined.

The crawler now already has:

- explicit claim entry
- explicit lease renewal
- explicit finish transitions
- expired-lease recovery
- explicit worker heartbeat operating rule

What still must be made strict is the controlled behavior when the crawler is intentionally being stopped.

## Genel Bakış

Bu belge, LogisticSearch crawler için mevcut kanonik drain ve graceful-shutdown sözleşmesini tanımlar.

Amacı, lease renewal ve worker heartbeat disiplini tanımlandıktan sonra kalan bir sonraki büyük operasyon boşluğunu kapatmaktır.

Crawler artık şunlara sahiptir:

- açık claim girişi
- açık lease renewal
- açık finish transition’ları
- expired-lease recovery
- açık worker heartbeat işletim kuralı

Şimdi katı hale getirilmesi gereken şey, crawler bilinçli olarak durdurulurken göstereceği kontrollü davranıştır.

## Current prerequisite truth

The current crawler-core and top-level contract surface already provide:

- `frontier.claim_next_url(...)`
- `frontier.renew_url_lease(...)`
- `frontier.finish_fetch_success(...)`
- `frontier.finish_fetch_retryable_error(...)`
- `frontier.finish_fetch_permanent_error(...)`
- `frontier.reap_expired_leases(...)`
- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`

Therefore the drain problem is no longer about missing ownership mechanics.

The remaining problem is coordinated stop behavior.

## Mevcut önkoşul doğrusu

Mevcut crawler-core ve üst seviye sözleşme yüzeyi artık şunları sağlar:

- `frontier.claim_next_url(...)`
- `frontier.renew_url_lease(...)`
- `frontier.finish_fetch_success(...)`
- `frontier.finish_fetch_retryable_error(...)`
- `frontier.finish_fetch_permanent_error(...)`
- `frontier.reap_expired_leases(...)`
- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`

Dolayısıyla drain problemi artık sahiplik mekaniklerinin eksikliği değildir.

Kalan problem, koordineli durdurma davranışıdır.

## Problem statement

Without a strict drain rule, a crawler stop request can become ambiguous:

1. a worker may keep claiming new work too late
2. a worker may keep renewing leases without real shutdown intent
3. a service stop may behave differently from a manual stop
4. a helper script may pretend to be graceful while actually being abrupt
5. operators may falsely believe that process memory is enough to preserve exact position

That ambiguity is not acceptable.

The crawler must have a deterministic stop contract.

## Problem tanımı

Katı bir drain kuralı olmadan crawler stop isteği belirsiz hale gelebilir:

1. worker çok geç zamanda yeni iş claim etmeye devam edebilir
2. worker gerçek shutdown niyeti olmadan lease yenilemeye devam edebilir
3. service stop ile manuel stop farklı davranabilir
4. yardımcı script graceful görünürken gerçekte ani olabilir
5. operatörler process belleğinin tam pozisyonu korumaya yeteceğini sanabilir

Bu belirsizlik kabul edilemez.

Crawler’ın deterministik bir stop sözleşmesi olmalıdır.

## Core contract

When a crawler instance enters deliberate shutdown intent, it must enter **drain mode**.

Drain mode means:

1. stop accepting new work
2. stop claiming new URLs
3. do not widen scope
4. only deal with already-owned in-flight work
5. exit in a bounded way

Drain mode is not optional style.
It is required operational behavior.

## Temel sözleşme

Bir crawler instance bilinçli shutdown niyetine girdiğinde **drain mode**’a girmelidir.

Drain mode şu anlama gelir:

1. yeni iş kabul etmeyi bırak
2. yeni URL claim etmeyi bırak
3. kapsamı genişletme
4. yalnızca hâlihazırda sahip olunan in-flight işle ilgilen
5. bounded biçimde çık

Drain mode isteğe bağlı bir stil değildir.
Zorunlu operasyon davranışıdır.

## Admission-close rule

The first action of deliberate stop must be admission close.

Admission close means:

- no new worker loop may call `frontier.claim_next_url(...)`
- no restarted inner sub-loop may sneak in one last new claim
- stop intent must dominate over throughput desire

A crawler that still claims new work after stop intent has already violated the shutdown contract.

## İş kabulünü kapatma kuralı

Bilinçli stop’un ilk aksiyonu iş kabulünü kapatmak olmalıdır.

İş kabulünü kapatmak şu anlama gelir:

- hiçbir yeni worker döngüsü `frontier.claim_next_url(...)` çağırmamalıdır
- yeniden başlayan iç alt döngü “son bir claim daha” kaçırmamalıdır
- stop niyeti throughput arzusundan baskın olmalıdır

Stop niyeti geldikten sonra hâlâ yeni iş claim eden bir crawler shutdown sözleşmesini ihlal etmiş olur.

## In-flight work decision rule

After admission close, the worker must decide only among bounded in-flight outcomes.

Allowed choices are:

1. finish the current URL cleanly within the remaining lease window
2. perform a bounded lease renewal only if it is genuinely needed for clean completion
3. stop work and allow lease expiry + later reap recovery

Forbidden choices are:

- claiming another URL first
- renewing repeatedly without shutdown budget discipline
- pretending unfinished work is successful
- hanging indefinitely just because stop was requested

## In-flight iş karar kuralı

Admission close’dan sonra worker yalnızca bounded in-flight sonuçlar arasında karar vermelidir.

İzin verilen seçenekler şunlardır:

1. mevcut URL’yi kalan lease penceresi içinde temiz biçimde bitirmek
2. yalnızca temiz bitiriş için gerçekten gerekiyorsa bounded lease renewal yapmak
3. işi bırakıp lease expiry + daha sonra reap recovery’ye izin vermek

Yasak seçenekler şunlardır:

- önce başka bir URL claim etmek
- shutdown bütçesi disiplini olmadan tekrar tekrar renewal yapmak
- bitmemiş işi başarılıymış gibi göstermek
- stop istendi diye süresiz asılı kalmak

## Bounded-renewal rule during shutdown

Drain mode does **not** mean “renew forever until convenient”.

A renewal during shutdown is allowed only if all of the following are true:

1. the worker still owns the current lease
2. the current work is near legitimate completion
3. one bounded renewal materially improves clean completion probability
4. the shutdown budget still allows that bounded completion
5. renewal is not being used to postpone exit indefinitely

If those conditions are not true, the worker must not renew during shutdown.

Strict shutdown rule:

- do not renew during shutdown unless the bounded completion conditions are genuinely met

## Shutdown sırasında bounded-renewal kuralı

Drain mode, “uygun olana kadar sonsuza dek renew et” demek **değildir**.

Shutdown sırasında renewal ancak aşağıdakilerin hepsi doğruysa izinlidir:

1. worker mevcut lease’in sahibidir
2. mevcut iş meşru biçimde tamamlanmaya yakındır
3. tek bir bounded renewal temiz bitiriş olasılığını anlamlı biçimde artırır
4. shutdown bütçesi bu bounded bitirişi hâlâ izinli kılar
5. renewal çıkışı süresiz ertelemek için kullanılmıyordur

Bu şartlar doğru değilse worker shutdown sırasında renewal yapmamalıdır.

Katı shutdown kuralı:

- bounded completion koşulları gerçekten sağlanmıyorsa shutdown sırasında renewal yapma

## Shutdown budget rule

A graceful shutdown must have a bounded budget.

That means:

- there is a maximum allowed time for graceful stop
- after that bound, the crawler must exit even if work was not perfectly completed
- incompletely owned work must fall back to lease expiry + reaping recovery

Graceful does not mean unbounded.

## Shutdown bütçesi kuralı

Graceful shutdown bounded bir bütçeye sahip olmalıdır.

Bu şu anlama gelir:

- graceful stop için izin verilen azami bir süre vardır
- bu sınırdan sonra iş kusursuz tamamlanmamış olsa bile crawler çıkmalıdır
- tamamlanmamış sahip olunan iş lease expiry + reap recovery’ye geri düşmelidir

Graceful olmak sınırsız olmak demek değildir.

## Service-layer stop rule

A future systemd service, wrapper, or helper script must follow this order:

1. signal stop intent
2. close admission for new work
3. allow bounded drain for current in-flight work
4. exit cleanly if possible
5. otherwise terminate and rely on bounded recovery

This ordering must be the same whether stop is triggered by:

- manual operator action
- service manager action
- helper script
- future UI/panel control
- controlled poweroff helper

## Service-layer stop kuralı

Gelecekteki systemd servisi, sarmalayıcı veya yardımcı script şu sırayı izlemelidir:

1. stop intent sinyali ver
2. yeni iş için admission’ı kapat
3. mevcut in-flight iş için bounded drain’e izin ver
4. mümkünse temiz çık
5. değilse sonlandır ve bounded recovery’ye güven

Bu sıralama stop şu kaynaklardan hangisiyle tetiklenirse tetiklensin aynı olmalıdır:

- manuel operatör aksiyonu
- service manager aksiyonu
- yardımcı script
- gelecekteki UI/panel kontrolü
- kontrollü poweroff helper

## Relationship to sudo-less poweroff helper

A future sudo-less shutdown helper may later exist.

If such a helper is introduced, its canonical behavior should be:

1. request crawler drain first
2. wait only for the bounded graceful-stop budget
3. avoid new work during that window
4. then continue to system shutdown

A shutdown helper must never create the illusion that crawler position is preserved by magic.

Durable truth remains PostgreSQL state plus bounded lease recovery.

## Sudo’suz poweroff helper ile ilişkisi

Gelecekte sudo’suz bir shutdown helper var olabilir.

Böyle bir helper eklenirse kanonik davranışı şu olmalıdır:

1. önce crawler drain iste
2. yalnızca bounded graceful-stop bütçesi kadar bekle
3. bu pencere boyunca yeni işi engelle
4. sonra sistem shutdown’a devam et

Shutdown helper, crawler pozisyonunun sihirle korunduğu yanılsamasını asla oluşturmamalıdır.

Kalıcı doğruluk yine PostgreSQL durumu ile bounded lease recovery’dir.

## Crash and sudden power-loss rule

Sudden death is a different class from graceful stop.

If power is cut unexpectedly:

- no graceful drain may happen
- no final renewal may happen
- no final finish transition may happen

Therefore the system must remain safe even without graceful behavior.

That safety comes from:

- bounded lease duration
- explicit lease renewal rather than silent ownership
- expired-lease recovery
- later re-claim from database truth

## Crash ve ani elektrik kesintisi kuralı

Ani ölüm graceful stop’tan farklı bir sınıftır.

Elektrik beklenmedik şekilde giderse:

- graceful drain gerçekleşmeyebilir
- son renewal gerçekleşmeyebilir
- son finish transition gerçekleşmeyebilir

Dolayısıyla sistem graceful davranış olmadan da güvenli kalmalıdır.

Bu güvenlik şuralardan gelir:

- bounded lease süresi
- sessiz sahiplik yerine açık lease renewal
- expired-lease recovery
- daha sonra veritabanı doğrusundan yeniden claim etme

## Resume rule after restart

After restart, the crawler must not pretend it remembers exact in-flight control state from RAM.

Instead it must:

1. trust PostgreSQL as durable ownership truth
2. allow expired leases to become reclaimable
3. resume by the normal claim path
4. avoid special hidden resume shortcuts

## Yeniden başlatma sonrası resume kuralı

Restart sonrasında crawler RAM’deki exact in-flight kontrol durumunu hatırlıyormuş gibi davranmamalıdır.

Bunun yerine şunları yapmalıdır:

1. kalıcı sahiplik doğrusu olarak PostgreSQL’e güven
2. süresi dolmuş lease’lerin yeniden claim edilebilir hale gelmesine izin ver
3. normal claim yolu üzerinden resume et
4. özel gizli resume kestirmelerinden kaçın

## Non-goals

This contract does **not** yet define:

- final numeric shutdown timeout values
- final numeric drain budget values
- final systemd unit syntax
- final helper script names
- final UI/panel stop buttons
- pause-mode semantics separate from drain mode

Those may be added later.
The contract here defines the mandatory behavior model first.

## Non-goal'ler

Bu sözleşme henüz şunları tanımlamaz:

- nihai sayısal shutdown timeout değerleri
- nihai sayısal drain budget değerleri
- nihai systemd unit sözdizimi
- nihai helper script adları
- nihai UI/panel stop düğmeleri
- drain mode’dan ayrı pause-mode semantiği

Bunlar daha sonra eklenebilir.
Buradaki sözleşme önce zorunlu davranış modelini tanımlar.

## Immediate next design consequence

The next practical continuation after this document should be:

1. cross-align the crawler top-level docs with this drain contract
2. decide whether drain mode needs an explicit future SQL/control surface or can remain service-layer behavior
3. only then design helper/service stop mechanics
4. only after that, decide exact stop / restart / poweroff orchestration details

## Anlık bir sonraki tasarım sonucu

Bu belgeden sonraki pratik devam adımı şu olmalıdır:

1. crawler üst seviye dokümanlarını bu drain sözleşmesiyle çapraz hizalamak
2. drain mode’un açık bir gelecek SQL/control yüzeyine ihtiyaç duyup duymadığını ya da service-layer davranışı olarak kalıp kalamayacağını kararlaştırmak
3. ancak bundan sonra helper/service stop mekaniklerini tasarlamak
4. ve ancak ondan sonra exact stop / restart / poweroff orkestrasyon ayrıntılarını belirlemek


<!-- BEGIN SECTION1_WEBCRAWLER_CONTROL_COMMAND_SPEC -->


## Future Shutdown-Class Webcrawler Controls

This document remains the canonical home for shutdown-class subset semantics and for drain/graceful-shutdown behavior.

## Gelecekteki Shutdown-Sınıfı Webcrawler Kontrolleri

Bu doküman, shutdown-sınıfı alt küme semantiklerinin ve drain/graceful-shutdown davranışının kanonik evi olarak kalır.

## Current shutdown-class subset

The current shutdown-class subset is:

- `stopwc`
- `poweroffwc`
- `rebootwc`

`playwc` is a control command, but it is **not** a shutdown-class command.

`resumewc` is a control command, but it is **not** a shutdown-class command.

`poweroffwc` and `rebootwc` belong to both the general control family and the shutdown-class subset.

`resetwc` currently belongs to the general control family, but is **not yet** part of the shutdown-class subset.

## Güncel shutdown-sınıfı alt küme

Güncel shutdown-sınıfı alt küme şudur:

- `stopwc`
- `poweroffwc`
- `rebootwc`

`playwc` bir kontrol komutudur; ancak **shutdown-sınıfı** bir komut değildir.

`resumewc` bir kontrol komutudur; ancak **shutdown-sınıfı** bir komut değildir.

`poweroffwc` ve `rebootwc`, hem genel kontrol ailesine hem de shutdown-sınıfı alt kümeye aittir.

`resetwc`, şu anda genel kontrol ailesine aittir; ancak henüz shutdown-sınıfı alt kümenin parçası değildir.

## Canonical shutdown-class meaning

- `stopwc` must first request crawler drain, stop new claims first, allow only bounded graceful-stop behavior for in-flight work, and then stop the service/worker layer.
- `poweroffwc` must execute `stopwc` semantics first and only then continue to `sudo poweroff`.
- `rebootwc` must execute `stopwc` semantics first and only then continue to `sudo reboot`.

## Kanonik shutdown-sınıfı anlamı

- `stopwc`, önce crawler drain istemeli, yeni claim’leri önce kapatmalı, in-flight iş için yalnızca bounded graceful-stop davranışına izin vermeli ve ancak ondan sonra service/worker katmanını durdurmalıdır.
- `poweroffwc`, önce `stopwc` semantiğini işletmeli, ancak ondan sonra `sudo poweroff` tarafına devam etmelidir.
- `rebootwc`, önce `stopwc` semantiğini işletmeli, ancak ondan sonra `sudo reboot` tarafına devam etmelidir.

## Conditional reset overlap rule

- if a future sealed reset design makes `resetwc` perform machine reboot, machine poweroff, or another shutdown-class system transition, then `resetwc` must also be classified under the shutdown-class subset
- in that case, `resetwc` must first execute the same controlled stop/drain semantics as `stopwc` before continuing into reboot/poweroff behavior

## Koşullu reset örtüşme kuralı

- eğer gelecekte mühürlü bir reset tasarımı `resetwc` komutuna makine reboot’u, makine poweroff’u veya başka bir shutdown-sınıfı sistem geçişi yüklerse, `resetwc` shutdown-sınıfı alt kümeye de alınmalıdır
- böyle bir durumda `resetwc`, reboot/poweroff davranışına geçmeden önce `stopwc` ile aynı kontrollü stop/drain semantiğini işletmelidir

## Cross-reference to the general control family

The general top-level control-family naming semantics are documented in:

- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`

## Genel kontrol ailesine çapraz referans

Genel üst-seviye kontrol-ailesi adlandırma semantiği şu dokümanda yer alır:

- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
