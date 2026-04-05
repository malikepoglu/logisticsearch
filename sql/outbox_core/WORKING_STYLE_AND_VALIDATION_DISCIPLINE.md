# Outbox Core Working Style and Validation Discipline

## Overview

This document records the working style and validation discipline currently used for the outbox-core SQL surface.

Its purpose is to standardize not only what files exist, but also how changes are made, checked, and sealed.

## Genel Bakış

Bu belge, outbox-core SQL yüzeyi için şu anda kullanılan çalışma stilini ve doğrulama disiplinini kayda geçirir.

Amacı, yalnızca hangi dosyaların bulunduğunu değil, değişikliklerin nasıl yapıldığını, kontrol edildiğini ve mühürlendiğini de standartlaştırmaktır.

## Core working style

The current working style is:

1. work from Ubuntu Desktop as the write authority
2. treat GitHub canonical main as the repository truth
3. treat imported live Pi51 snapshot files as comparison/evidence surfaces
4. treat split SQL files as the main editable working surface
5. keep commands explicit, reproducible, and machine-scoped

## Temel çalışma stili

Mevcut çalışma stili şöyledir:

1. yazma otoritesi olarak Ubuntu Desktop üzerinden çalış
2. GitHub canonical main'i repository doğrusu olarak kabul et
3. ithal edilmiş canlı Pi51 snapshot dosyalarını karşılaştırma/kanıt yüzeyi olarak ele al
4. split SQL dosyalarını ana düzenlenebilir çalışma yüzeyi olarak ele al
5. komutları açık, yeniden üretilebilir ve makineye göre belirlenmiş tut

## Command discipline

The current command discipline is:

1. give exactly one command block at a time
2. run the command
3. inspect the result
4. only then decide the next command
5. avoid bundling unrelated operations into one opaque step

## Komut disiplini

Mevcut komut disiplini şöyledir:

1. her seferinde tam olarak bir komut bloğu ver
2. komutu çalıştır
3. sonucu incele
4. ancak ondan sonra bir sonraki komuta karar ver
5. ilgisiz işlemleri tek ve opak bir adımda birleştirme

## Change discipline

The current change discipline is:

1. first derive or write the target file locally
2. preview the content
3. run a focused audit or validation
4. commit only after the result is understood
5. push only after the local state is coherent

## Değişiklik disiplini

Mevcut değişiklik disiplini şöyledir:

1. önce hedef dosyayı yerelde üret veya yaz
2. içeriği önizle
3. odaklı bir audit veya doğrulama çalıştır
4. sonucu anlamadan commit yapma
5. yerel durum tutarlı olmadan push yapma

## Validation discipline

The current validation discipline is:

1. preserve imported live truth
2. derive split working files
3. add execution entry points
4. validate against a scratch database
5. record the result in seal documents
6. add or validate a reusable runner when the surface is stable

## Doğrulama disiplini

Mevcut doğrulama disiplini şöyledir:

1. ithal edilmiş canlı doğruluğu koru
2. split çalışma dosyalarını türet
3. execution giriş noktalarını ekle
4. scratch veritabanına karşı doğrula
5. sonucu seal belgelerine işle
6. yüzey istikrarlı hale geldiğinde reusable runner ekle veya doğrula

## Safety discipline

The current safety discipline is:

1. do not mutate live Pi51 crawler database during repository-side structure work
2. prefer scratch validation before any live mutation discussion
3. make upstream dependencies explicit
4. make sequencing explicit
5. keep rollback thinking present even when not executing rollback steps

## Güvenlik disiplini

Mevcut güvenlik disiplini şöyledir:

1. repository taraflı yapı çalışmasında canlı Pi51 crawler veritabanını değiştirme
2. canlı mutasyon tartışmasından önce scratch doğrulamayı tercih et
3. upstream bağımlılıkları açıkça belirt
4. sıralamayı açıkça belirt
5. rollback adımları uygulanmasa bile rollback düşüncesini canlı tut

## Documentation discipline

The current documentation discipline is:

1. document structural truth
2. document execution truth
3. document validation truth
4. document the next continuation point
5. keep the interpretation layer bilingual when the surface is being sealed

## Dökümantasyon disiplini

Mevcut dökümantasyon disiplini şöyledir:

1. yapısal doğruluğu belgeye işle
2. execution doğruluğunu belgeye işle
3. validation doğruluğunu belgeye işle
4. bir sonraki devam noktasını belgeye işle
5. yüzey mühürlenirken yorum katmanını çift dilli tut

## Current practical rule

For this surface, the normal operating rhythm is:

1. write or derive
2. preview
3. audit
4. commit
5. push
6. validate
7. seal
8. continue from the documented next step

## Güncel pratik kural

Bu yüzey için normal işletim ritmi şöyledir:

1. yaz veya türet
2. önizle
3. audit yap
4. commit et
5. push et
6. doğrula
7. mühürle
8. belgelenmiş sonraki adımdan devam et
