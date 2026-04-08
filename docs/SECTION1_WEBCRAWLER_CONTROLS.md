# Webcrawler Controls

# Webcrawler Kontrolleri

## Purpose

## Amaç

This document defines the canonical operator-facing top-level control family for the LogisticSearch webcrawler.

Bu belge, LogisticSearch webcrawler için kanonik operatör-yüzlü üst-seviye kontrol ailesini tanımlar.

It exists so the project has one explicit documentation home for all top-level webcrawler control names.

Projenin tüm üst-seviye webcrawler kontrol adları için tek açık dokümantasyon evi olması için vardır.

It does **not** prove that live helper commands already exist.

Bu belge, canlı yardımcı komutların şimdiden var olduğunu **kanıtlamaz**.

## Current truth boundary

## Güncel doğruluk sınırı

Current truth:

- crawler_core SQL/data-model foundation exists
- controlled seed+frontier bootstrap proof now exists on Ubuntu Desktop scratch
- control-command names are standardized
- but command-name standardization alone does **not** prove a live worker/runtime/service implementation

Güncel doğruluk:

- crawler_core SQL/veri-modeli temeli vardır
- Ubuntu Desktop scratch üzerinde kontrollü seed+frontier bootstrap kanıtı artık vardır
- kontrol-komut adları standardize edilmiştir
- ancak yalnızca komut adı standardizasyonu, canlı bir worker/runtime/service implementasyonu olduğunu **kanıtlamaz**

## Canonical control family

## Kanonik kontrol ailesi

The canonical top-level control family is:

- `playwc`
- `resumewc`
- `stopwc`
- `resetwc`
- `poweroffwc`
- `rebootwc`

Kanonik üst-seviye kontrol ailesi şudur:

- `playwc`
- `resumewc`
- `stopwc`
- `resetwc`
- `poweroffwc`
- `rebootwc`

## Canonical meaning of each name

## Her adın kanonik anlamı

### EN

- `playwc` should start the future crawler runtime only after a real worker/service surface exists.
- `resumewc` must resume only through durable database truth and the normal claim path; it must not pretend to restore hidden in-memory crawler position.
- `stopwc` is the deliberate controlled-stop command.
- `resetwc` is the canonical short reset helper name for repeated test cycles, but it must remain explicit-scope only unless a stricter later design seals broader behavior.
- `poweroffwc` belongs to both the general control family and the shutdown-class subset.
- `rebootwc` belongs to both the general control family and the shutdown-class subset.

### TR

- `playwc`, ancak gerçek bir worker/service yüzeyi var olduktan sonra gelecekteki crawler runtime’ını başlatmalıdır.
- `resumewc`, yalnızca kalıcı veritabanı doğrusu ve normal claim yolu üzerinden devam etmelidir; gizli process/RAM durumundan crawler pozisyonu geri geliyormuş gibi davranmamalıdır.
- `stopwc`, bilinçli kontrollü-durdurma komutudur.
- `resetwc`, tekrar eden test döngüleri için kanonik kısa reset yardımcı adıdır; ancak daha katı bir sonraki tasarım daha geniş davranışı mühürlemedikçe açık-kapsamlı kalmalıdır.
- `poweroffwc`, hem genel kontrol ailesine hem de shutdown-sınıfı alt kümeye aittir.
- `rebootwc`, hem genel kontrol ailesine hem de shutdown-sınıfı alt kümeye aittir.

## Relationship to shutdown-class controls

## Shutdown-sınıfı kontroller ile ilişki

The shutdown-class subset is documented in:

- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

Shutdown-sınıfı alt küme şu dokümanda tanımlanır:

- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`

Intentional overlap is allowed for these names:

- `stopwc`
- `poweroffwc`
- `rebootwc`

Şu adlar için bilinçli çift-görünüm izinlidir:

- `stopwc`
- `poweroffwc`
- `rebootwc`

Conditional overlap rule for `resetwc`:

- `resetwc` currently belongs to the general control family
- `resetwc` is **not yet** part of the shutdown-class subset
- if a future sealed design makes `resetwc` perform reboot, poweroff, or another shutdown-class system transition, then it must also appear under the shutdown-class subset
- in that case, `resetwc` must first execute the same controlled stop/drain semantics as `stopwc`

`resetwc` için koşullu çift-görünüm kuralı:

- `resetwc`, şu anda genel kontrol ailesine aittir
- `resetwc`, henüz shutdown-sınıfı alt kümenin parçası değildir
- eğer gelecekte mühürlü bir tasarım `resetwc` komutuna reboot, poweroff veya başka bir shutdown-sınıfı sistem geçişi yüklerse, shutdown-sınıfı alt kümede de görünmelidir
- böyle bir durumda `resetwc`, önce `stopwc` ile aynı kontrollü stop/drain semantiğini işletmelidir

## Safety boundary

## Güvenlik sınırı

- do **not** shadow native system commands `poweroff` or `reboot`
- do **not** imply that live helper implementations already exist
- do **not** imply magical RAM-based resume after crash/power loss
- do **not** blur scratch/test reset with future live-runtime reset
- keep pause semantics separate from drain semantics unless later sealed explicitly

- yerleşik sistem komutları `poweroff` veya `reboot` gölgelenmemelidir
- canlı yardımcı implementasyonlar şimdiden varmış gibi davranılmamalıdır
- crash/elektrik kesintisi sonrası sihirli RAM-tabanlı resume varsayılmamalıdır
- scratch/test reset ile gelecekteki live-runtime reset birbirine karıştırılmamalıdır
- daha sonra açıkça mühürlenmedikçe pause semantiği ile drain semantiği birleştirilmemelidir

## Canonical ownership rule

## Kanonik sahiplik kuralı

This document is the canonical documentation home for:

- the general webcrawler control family
- non-shutdown top-level naming semantics
- control-family classification boundaries

Bu belge şu konular için kanonik dokümantasyon evidir:

- genel webcrawler kontrol ailesi
- shutdown-dışı üst-seviye adlandırma semantikliği
- kontrol-ailesi sınıflandırma sınırları

The shutdown/drain document remains the canonical home for shutdown-class stop, poweroff, reboot, and drain semantics.

Shutdown/drain dokümanı, shutdown-sınıfı stop, poweroff, reboot ve drain semantiklerinin kanonik evi olarak kalır.
