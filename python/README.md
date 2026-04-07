# Python Surface

## Overview

This directory is intended for tracked Python code that belongs in the canonical LogisticSearch repository. Its purpose is to hold durable support code such as import/export helpers, crawler-side or desktop-side utilities, validation tools, and other project-level Python assets that should be versioned, reviewed, and kept reproducible.

## Genel Bakış

Bu dizin, kanonik LogisticSearch repository’sinde izlenmesi gereken Python kodları için ayrılmıştır. Amacı; import/export yardımcıları, crawler veya desktop tarafı araçları, doğrulama araçları ve versiyonlanması, gözden geçirilmesi ve tekrar üretilebilir kalması gereken diğer proje düzeyi Python varlıklarını barındırmaktır.
## Policy

Only durable and repository-worthy Python content should live here. Machine-local virtual environments, cache folders, quick one-off scraps, and other disposable artifacts must stay outside Git or remain ignored. The directory should gradually evolve into a clean and intentional Python support surface rather than an uncontrolled dump area.

## Politika

Burada yalnızca kalıcı ve repository’ye girmeye değer Python içerikleri yer almalıdır. Makineye özel sanal ortamlar, cache klasörleri, tek kullanımlık geçici denemeler ve diğer atıl çıktılar Git dışında kalmalı veya ignore edilmelidir. Bu dizin zamanla kontrolsüz bir döküm alanına değil, temiz ve bilinçli bir Python destek yüzeyine dönüşmelidir.
## Expected Direction

The likely long-term role of this directory includes import helpers, export validators, structured tools, command-line utilities, and operational scripts that support the LogisticSearch data flow.

## Beklenen Yön

Bu dizinin muhtemel uzun vadeli rolü; LogisticSearch veri akışını destekleyen import yardımcıları, export doğrulayıcıları, yapısal araçlar, komut satırı yardımcıları ve operasyon script’lerini içermektir.

## Documentation hub

Use these surfaces as the current hub / reading map around the Python area:

- `README.md` — root repository entry surface
- `docs/README.md` — documentation hub and safest beginner reading map
- `python/desktop_import/README.md` — current real Python sub-surface with explicit current behavior

This file should be read as the Python-area hub, not as a standalone isolated note.

## Dokümantasyon merkezi

Python alanı etrafındaki mevcut merkez / okuma haritası olarak şu yüzeyleri kullan:

- `README.md` — repository kök giriş yüzeyi
- `docs/README.md` — dokümantasyon merkezi ve başlangıç için en güvenli okuma haritası
- `python/desktop_import/README.md` — açık mevcut davranışı anlatan güncel gerçek Python alt yüzeyi

Bu dosya, tek başına izole bir not olarak değil, Python alanının hub yüzeyi olarak okunmalıdır.

## Beginner-first reading path

If you are starting from zero, do **not** guess the Python surface from filenames alone.

Use this order:

1. `README.md` — understand the repository-level direction first
2. `docs/README.md` — understand the documentation hub and reading model
3. `python/README.md` — understand what the Python surface is and is not
4. `python/desktop_import/README.md` — understand the current real tracked Python sub-surface
5. `python/desktop_import/load_pi51_batch_into_postgres.py` — only then read the actual script

## Başlangıç seviyesi okuma yolu

Sıfırdan başlıyorsan Python yüzeyini yalnızca dosya adlarına bakarak tahmin etme.

Şu sırayı kullan:

1. `README.md` — önce repository seviyesindeki yönü anla
2. `docs/README.md` — dokümantasyon merkezini ve okuma modelini anla
3. `python/README.md` — Python yüzeyinin ne olduğunu ve ne olmadığını anla
4. `python/desktop_import/README.md` — mevcut gerçek izlenen Python alt yüzeyini anla
5. `python/desktop_import/load_pi51_batch_into_postgres.py` — ancak bundan sonra gerçek script'i oku

## Current Tracked Surface

At the moment, the tracked Python surface is intentionally very small. The active tracked implementation under this directory is the `python/desktop_import/` area, currently represented by `python/desktop_import/load_pi51_batch_into_postgres.py`. This means the Python surface is not yet a broad framework; it is a controlled support layer centered on desktop-side batch intake preparation for PostgreSQL loading.

## Güncel İzlenen Yüzey

Şu anda izlenen Python yüzeyi bilinçli olarak oldukça küçüktür. Bu dizin altındaki aktif izlenen uygulama `python/desktop_import/` alanıdır ve şu an `python/desktop_import/load_pi51_batch_into_postgres.py` ile temsil edilmektedir. Bu da Python yüzeyinin henüz geniş bir framework olmadığı; PostgreSQL yüklemesi öncesi desktop tarafı batch intake hazırlığına odaklanan kontrollü bir destek katmanı olduğu anlamına gelir.
