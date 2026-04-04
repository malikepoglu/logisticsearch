# Crawler Core SQL Surface

## EN

This directory is the canonical repository surface for the real crawler-core SQL layer of LogisticSearch. Its purpose is to bring the live PostgreSQL crawler contract into the GitHub-centered repository in a disciplined way, starting from the currently verified Pi51 state rather than from reconstructed or guessed definitions.

The first import in this directory is intentionally live-sourced from Pi51. This keeps the repository aligned with the already validated crawler chronology instead of inventing a parallel SQL history on Ubuntu Desktop.

### Current import scope

The current live snapshot covers the core crawler database schemas that have already been developed on Pi51:

- `seed`
- `frontier`
- `http_fetch`

This surface is expected to contain the structural backbone for:
- source and seed definitions
- frontier host/url persistence
- lease and fetch state transitions
- politeness and freshness helpers
- robots cache and enforcement helpers

### Policy

This directory should contain repository-worthy crawler SQL only.  
The initial live snapshot is not a random dump; it is a controlled canonicalization step.

The immediate goal is:
1. bring the live verified crawler-core SQL into the repository
2. review it under version control
3. later normalize/split it into chronology-friendly files without losing truth

---

## TR

Bu dizin, LogisticSearch’in gerçek crawler-core SQL katmanı için kanonik repository yüzeyidir. Amacı, canlı PostgreSQL crawler kontratını tahmin veya yeniden kurgu üzerinden değil, şu anda Pi51 üzerinde doğrulanmış durumdan başlayarak disiplinli biçimde GitHub merkezli repository içine taşımaktır.

Bu dizindeki ilk import bilinçli olarak Pi51 canlı doğrusu üzerinden alınmaktadır. Böylece Ubuntu Desktop üzerinde paralel ve uydurma bir SQL tarihi üretmek yerine, zaten doğrulanmış crawler chronology ile repository hizalanmış olur.

### Mevcut import kapsamı

Mevcut canlı snapshot, Pi51 üzerinde geliştirilmiş olan çekirdek crawler veritabanı şemalarını kapsar:

- `seed`
- `frontier`
- `http_fetch`

Bu yüzeyin şu omurgayı içermesi beklenir:
- source ve seed tanımları
- frontier host/url kalıcılığı
- lease ve fetch durum geçişleri
- politeness ve freshness yardımcıları
- robots cache ve enforcement yardımcıları

### Politika

Bu dizin yalnızca repository’ye girmeye değer crawler SQL içermelidir.  
İlk canlı snapshot rastgele bir dump değildir; kontrollü bir canonicalization adımıdır.

Yakın hedef şudur:
1. canlı doğrulanmış crawler-core SQL’i repository içine almak
2. bunu version control altında gözden geçirmek
3. daha sonra doğruluğu kaybetmeden chronology uyumlu dosyalara ayırmak / normalize etmek
