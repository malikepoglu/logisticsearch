# Runbook Authoring and Execution Discipline

## Overview

This document defines the canonical discipline for writing, reading, maintaining, and validating runbooks in the LogisticSearch repository.

A runbook is not the same thing as a README.

A README explains:

- what a surface is
- why it exists
- how it fits into the repository
- how it should be read safely

A runbook explains:

- exactly what to do
- in what order to do it
- what must already exist
- what success looks like
- when to stop
- what to do if something fails
- what the next authoritative handoff surface is

Runbooks must be operational, explicit, conservative, disciplined, and current-truth only.

## Genel Bakış

Bu belge, LogisticSearch repository’sinde runbook yazımı, okunması, bakımı ve doğrulanması için kanonik disiplini tanımlar.

Bir runbook, README ile aynı şey değildir.

README şunları açıklar:

- bir yüzeyin ne olduğunu
- neden var olduğunu
- repository içindeki yerine nasıl oturduğunu
- güvenli biçimde nasıl okunması gerektiğini

Runbook ise şunları açıklar:

- tam olarak ne yapılacağını
- hangi sırayla yapılacağını
- önceden nelerin mevcut olması gerektiğini
- başarının neye benzediğini
- ne zaman durulacağını
- bir şey başarısız olursa ne yapılacağını
- sıradaki yetkili handoff yüzeyinin ne olduğunu

Runbook’lar operasyonel, açık, muhafazakâr, disiplinli ve yalnızca mevcut doğruya dayalı olmalıdır.

## Paired-document model

In this repository, explanation surfaces and runbooks must be treated as paired deliverables whenever a surface becomes operationally meaningful.

The pairing model is:

- README / topic document = explanation layer
- RUNBOOK = action layer

The explanation layer answers:

- what this surface is
- why it exists
- how it should be understood

The runbook layer answers:

- how to operate it now
- how to verify it now
- how to stop safely
- where the next handoff begins

A README must not pretend to be a runbook.
A runbook must not replace a README.

## Eşlenik belge modeli

Bu repository’de açıklama yüzeyleri ile runbook’lar, bir yüzey operasyonel olarak anlamlı hale geldiğinde eşlenik teslimatlar olarak ele alınmalıdır.

Eşleşme modeli şöyledir:

- README / topic belge = açıklama katmanı
- RUNBOOK = eylem katmanı

Açıklama katmanı şunları cevaplar:

- bu yüzey nedir
- neden vardır
- nasıl anlaşılmalıdır

Runbook katmanı ise şunları cevaplar:

- şu anda nasıl işletilir
- şu anda nasıl doğrulanır
- güvenli biçimde nasıl durulur
- sıradaki handoff nerede başlar

README, runbook gibi davranmamalıdır.
Runbook da README’nin yerine geçmemelidir.

## Mandatory runbook properties

Every real runbook should contain, when applicable:

1. what this runbook is
2. current judgement / current operational boundary
3. documentation hub
4. execution target / machine context
5. preconditions
6. exact step-by-step execution order
7. expected outputs or state transitions
8. verification steps
9. stop conditions
10. failure handling
11. scope boundaries
12. update discipline
13. next authoritative handoff surface

Not every runbook must be long.
Every real runbook must be complete for its real scope.

## Zorunlu runbook özellikleri

Her gerçek runbook, uygunsa şunları içermelidir:

1. bu runbook’un ne olduğu
2. mevcut hüküm / mevcut operasyon sınırı
3. dokümantasyon merkezi
4. yürütme hedefi / makine bağlamı
5. önkoşullar
6. tam adım adım uygulama sırası
7. beklenen çıktılar veya durum geçişleri
8. doğrulama adımları
9. durma koşulları
10. hata durumunda yapılacaklar
11. kapsam sınırları
12. güncelleme disiplini
13. sıradaki yetkili handoff yüzeyi

Her runbook uzun olmak zorunda değildir.
Her gerçek runbook, kendi gerçek kapsamı için tam olmalıdır.

## Bilingual structure rule

Runbooks must follow the repository bilingual discipline.

This means:

- explanatory sections must exist in both English and Turkish
- English and Turkish should be written under separate headings or clearly separated paired sections
- file names, paths, commands, identifiers, keys, and code-facing tokens remain in English
- Turkish must not silently omit safety-critical details that appear in English
- English must not silently omit operationally meaningful details that appear in Turkish
- translation quality matters; paired sections must remain semantically aligned

## Çift dilli yapı kuralı

Runbook’lar repository’nin çift dilli disiplinine uymalıdır.

Bu şu anlama gelir:

- açıklayıcı bölümler hem İngilizce hem Türkçe bulunmalıdır
- İngilizce ve Türkçe ayrı başlıklar altında veya açıkça ayrılmış eş bölümler halinde yazılmalıdır
- dosya adları, yollar, komutlar, kimlikler, anahtarlar ve kod-tarafı belirteçler İngilizce kalır
- Türkçe metin, İngilizce metindeki güvenlik açısından kritik ayrıntıları sessizce atlamamalıdır
- İngilizce metin de Türkçe metindeki operasyon açısından anlamlı ayrıntıları sessizce atlamamalıdır
- çeviri kalitesi önemlidir; eş bölümler anlamsal olarak hizalı kalmalıdır

## Command-writing rule

Runbooks must prefer exact commands over vague prose whenever command execution is part of the real surface.

A good runbook should explicitly tell the operator:

- which machine the command is for
- which directory to enter
- which variable must be set
- which command to run
- which files or states should appear afterward
- which quick verification proves success

A runbook must not rely on “you probably already know the rest”.

## Komut yazım kuralı

Runbook’lar, komut çalıştırma gerçek yüzeyin parçasıysa muğlak açıklama yerine tam komutları tercih etmelidir.

İyi bir runbook operatöre açıkça şunları söylemelidir:

- komutun hangi makine için olduğu
- hangi dizine girileceği
- hangi değişkenin ayarlanacağı
- hangi komutun çalıştırılacağı
- sonrasında hangi dosya veya durumların ortaya çıkmasının beklendiği
- başarının hangi hızlı doğrulamayla kanıtlanacağı

Bir runbook, “gerisini zaten biliyorsundur” varsayımına dayanamaz.

## Verification rule

A runbook is incomplete if it tells the operator how to run a step but not how to verify that step.

Verification should include, when applicable:

- file-existence checks
- quick content checks
- status checks
- count or shape sanity checks
- success criteria
- non-success criteria

## Doğrulama kuralı

Bir runbook, operatöre bir adımı nasıl çalıştıracağını söyleyip o adımı nasıl doğrulayacağını söylemiyorsa eksiktir.

Doğrulama, uygunsa şunları içermelidir:

- dosya varlığı kontrolleri
- hızlı içerik kontrolleri
- durum kontrolleri
- sayı veya şekil mantıklılık kontrolleri
- başarı kriterleri
- başarısızlık kriterleri

## Failure-handling rule

A real runbook must not stop at the happy path.

It should tell the operator what to do when:

- a required input is missing
- a command exits non-zero
- an expected output does not appear
- an output exists but looks suspicious
- the operator has not yet reached the next safe handoff condition

Failure handling should be conservative.
Prefer “stop and verify” over blind continuation.

## Hata yönetimi kuralı

Gerçek bir runbook yalnızca mutlu yol ile sınırlı kalmamalıdır.

Şu durumlarda operatöre ne yapacağını söylemelidir:

- gerekli bir girdi eksikse
- bir komut sıfır olmayan çıkış koduyla biterse
- beklenen bir çıktı oluşmazsa
- çıktı vardır ama şüpheli görünüyorsa
- operatör henüz sıradaki güvenli handoff koşuluna ulaşmadıysa

Hata yönetimi muhafazakâr olmalıdır.
Körlemesine devam etmek yerine “dur ve doğrula” yaklaşımı tercih edilmelidir.

## Scope-boundary rule

Every runbook must say where it stops.

This matters because many repository surfaces are preparation layers, transfer layers, validation layers, or apply layers rather than full end-to-end systems.

A runbook should clearly separate:

- what it covers
- what it does not cover
- where the next authoritative surface begins

## Kapsam sınırı kuralı

Her runbook nerede durduğunu söylemelidir.

Bu önemlidir; çünkü repository içindeki birçok yüzey uçtan uca tam sistem değil, hazırlık katmanı, taşıma katmanı, doğrulama katmanı veya apply katmanıdır.

Bir runbook şunları açıkça ayırmalıdır:

- neyi kapsadığını
- neyi kapsamadığını
- sıradaki yetkili yüzeyin nerede başladığını

## Anti-fiction rule

Runbooks must describe real current behavior only.

They must not:

- invent hidden automation that does not exist
- imply full pipeline behavior when only one real step exists
- silently upgrade a helper into a complete subsystem
- blur preparation steps with apply steps
- describe future intent as if it were current production truth

## Kurgu karşıtı kural

Runbook’lar yalnızca gerçek mevcut davranışı anlatmalıdır.

Şunları yapmamalıdır:

- var olmayan gizli otomasyonları uydurmak
- yalnızca tek gerçek adım varken tüm pipeline davranışını varmış gibi göstermek
- bir helper’ı sessizce tam bir alt sisteme yükseltmek
- hazırlık adımları ile apply adımlarını bulanıklaştırmak
- gelecek niyeti mevcut üretim gerçeği gibi anlatmak

## Naming rule

Runbook file names should be explicit and English.

Preferred pattern:

- `RUNBOOK_<SURFACE>_<ACTION>.md`

Examples:

- `RUNBOOK_DESKTOP_IMPORT_TSV_PREPARATION.md`
- `RUNBOOK_SQL_DESKTOP_IMPORT_APPLY.md`
- `RUNBOOK_GITHUB_BATCH_V1_INTAKE_VERIFICATION.md`

## Adlandırma kuralı

Runbook dosya adları açık ve İngilizce olmalıdır.

Tercih edilen desen:

- `RUNBOOK_<SURFACE>_<ACTION>.md`

Örnekler:

- `RUNBOOK_DESKTOP_IMPORT_TSV_PREPARATION.md`
- `RUNBOOK_SQL_DESKTOP_IMPORT_APPLY.md`
- `RUNBOOK_GITHUB_BATCH_V1_INTAKE_VERIFICATION.md`

## Review and audit rule

A runbook should normally pass through this order:

1. create draft
2. strict re-audit
3. commit and push
4. post-push final audit

Do not treat “written” as “finished”.
A runbook is not sealed until it has passed a strict audit path.

## İnceleme ve audit kuralı

Bir runbook normalde şu sıradan geçmelidir:

1. taslak oluşturma
2. katı re-audit
3. commit ve push
4. post-push final audit

“Yazıldı” durumunu “tamamlandı” ile eşitleme.
Bir runbook, katı audit yolundan geçmeden mühürlenmiş sayılmaz.

## Update discipline

Update a runbook when one of these changes:

- command contract
- input/output filenames
- verification logic
- handoff boundary
- machine context
- operational success criteria

Do not leave a stale runbook beside a corrected README.

## Güncelleme disiplini

Şunlardan biri değiştiğinde runbook’u güncelle:

- komut sözleşmesi
- girdi/çıktı dosya adları
- doğrulama mantığı
- handoff sınırı
- makine bağlamı
- operasyonel başarı kriterleri

Düzeltilmiş bir README’nin yanında bayat bir runbook bırakma.

## Current repository judgement

At the current repository point, the disciplined direction is:

- keep README and topic explanation surfaces coherent
- add action-first runbooks for real operational surfaces
- progress one controlled runbook at a time
- validate each runbook strictly before sealing it
- treat README and RUNBOOK as paired deliverables whenever a surface becomes truly operational

## Mevcut repository hükmü

Mevcut repository noktasında disiplinli yön şudur:

- README ve topic açıklama yüzeylerini tutarlı tut
- gerçek operasyon yüzeyleri için eylem-öncelikli runbook’lar ekle
- aynı anda çok sayıda değil, kontrollü biçimde bir runbook ilerlet
- her runbook’u mühürlemeden önce katı biçimde doğrula
- bir yüzey gerçekten operasyonel hale geldiğinde README ile RUNBOOK’u eşlenik teslimatlar olarak ele al
