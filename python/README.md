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

## Current Tracked Surface

At the moment, the tracked Python surface is intentionally very small. The active tracked implementation under this directory is the `python/desktop_import/` area, currently represented by `python/desktop_import/load_pi51_batch_into_postgres.py`. This means the Python surface is not yet a broad framework; it is a controlled support layer centered on desktop-side batch intake preparation for PostgreSQL loading.

## Güncel İzlenen Yüzey

Şu anda izlenen Python yüzeyi bilinçli olarak oldukça küçüktür. Bu dizin altındaki aktif izlenen uygulama `python/desktop_import/` alanıdır ve şu an `python/desktop_import/load_pi51_batch_into_postgres.py` ile temsil edilmektedir. Bu da Python yüzeyinin henüz geniş bir framework olmadığı; PostgreSQL yüklemesi öncesi desktop tarafı batch intake hazırlığına odaklanan kontrollü bir destek katmanı olduğu anlamına gelir.
