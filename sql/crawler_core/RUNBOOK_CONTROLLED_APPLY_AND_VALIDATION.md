# Crawler Core Controlled Apply And Validation Runbook

This runbook gives the single controlled operator path for applying and validating the current `sql/crawler_core` split working surface on Ubuntu Desktop.

# Crawler Core Kontrollü Uygulama ve Doğrulama Runbook'u

Bu runbook, mevcut `sql/crawler_core` split çalışma yüzeyini Ubuntu Desktop üzerinde uygulamak ve doğrulamak için tek kontrollü operatör yolunu verir.

## Purpose

It is action-first by design.

It does **not** replace these surfaces:

- `README.md`
- `PREREQUISITES.md`
- `NEXT_STEP.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Those files explain meaning, scope, prerequisites, and sealed status.

This runbook exists only to tell the operator exactly what to do.

## Amaç

Tasarım gereği action-first'tür.

Şu yüzeylerin yerine geçmez:

- `README.md`
- `PREREQUISITES.md`
- `NEXT_STEP.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Bu dosyalar anlamı, kapsamı, önkoşulları ve mühürlü durumu açıklar.

Bu runbook yalnızca operatöre tam olarak ne yapması gerektiğini söylemek için vardır.

## Current execution boundary

Current target is the `crawler_core` line only.

The real technical order remains:

`crawler_core` -> `parse_core` -> `desktop_import`

This runbook must not be used to jump ahead into `parse_core` or `desktop_import`.

## Güncel yürütme sınırı

Güncel hedef yalnızca `crawler_core` hattıdır.

Gerçek teknik sıra şu şekilde kalır:

`crawler_core` -> `parse_core` -> `desktop_import`

Bu runbook, `parse_core` veya `desktop_import` tarafına önden atlamak için kullanılmamalıdır.

## Machine and safety boundary

Machine:

- Ubuntu Desktop

Safety boundary:

- use a local scratch database
- do **not** mutate Pi51 live crawler PostgreSQL through this runbook
- do **not** treat this runbook as a production deploy guide

Default scratch database name:

- `logisticsearch_crawler_split_scratch`

## Makine ve güvenlik sınırı

Makine:

- Ubuntu Desktop

Güvenlik sınırı:

- yerel bir scratch veritabanı kullan
- bu runbook ile Pi51 canlı crawler PostgreSQL'ini **mutasyona uğratma**
- bu runbook'u production deploy rehberi gibi ele alma

Varsayılan scratch veritabanı adı:

- `logisticsearch_crawler_split_scratch`

## Required repository files

This runbook assumes these files exist and are current:

- `sql/crawler_core/001_seed_frontier_http_fetch_base.sql`
- `sql/crawler_core/002_frontier_claim_and_lease.sql`
- `sql/crawler_core/003_frontier_finish_transitions.sql`
- `sql/crawler_core/004_frontier_politeness_and_freshness.sql`
- `sql/crawler_core/005_http_fetch_robots_cache_and_enforcement.sql`
- `sql/crawler_core/900_apply_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/901_preflight_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/902_presence_audit_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/910_validate_crawler_core_split_surface.sh`

## Gerekli repository dosyaları

Bu runbook şu dosyaların mevcut ve güncel olduğunu varsayar:

- `sql/crawler_core/001_seed_frontier_http_fetch_base.sql`
- `sql/crawler_core/002_frontier_claim_and_lease.sql`
- `sql/crawler_core/003_frontier_finish_transitions.sql`
- `sql/crawler_core/004_frontier_politeness_and_freshness.sql`
- `sql/crawler_core/005_http_fetch_robots_cache_and_enforcement.sql`
- `sql/crawler_core/900_apply_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/901_preflight_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/902_presence_audit_crawler_core_split_surface.psql.sql`
- `sql/crawler_core/910_validate_crawler_core_split_surface.sh`

## Primary operator path

Run this from repository root on Ubuntu Desktop:

```bash
bash sql/crawler_core/910_validate_crawler_core_split_surface.sh
```

If you intentionally want a different scratch database name, pass it explicitly:

```bash
bash sql/crawler_core/910_validate_crawler_core_split_surface.sh my_custom_crawler_core_scratch
```

## Birincil operatör yolu

Ubuntu Desktop üzerinde repository kökünden şunu çalıştır:

```bash
bash sql/crawler_core/910_validate_crawler_core_split_surface.sh
```

Bilerek farklı bir scratch veritabanı adı kullanmak istiyorsan açıkça parametre ver:

```bash
bash sql/crawler_core/910_validate_crawler_core_split_surface.sh my_custom_crawler_core_scratch
```

## What the validation runner does

Current controlled behavior of the validation runner is:

- stage the required SQL files into a temporary directory
- verify that the `postgres` account can access the staged SQL bundle
- drop the scratch database if it already exists
- create the scratch database again
- ensure `pgcrypto` exists in `public`
- run `901_preflight_crawler_core_split_surface.psql.sql`
- run `900_apply_crawler_core_split_surface.psql.sql`
- run `902_presence_audit_crawler_core_split_surface.psql.sql`
- print `VALIDATION_RESULT=PASS` on success

## Validation runner ne yapar

Validation runner'ın güncel kontrollü davranışı şudur:

- gerekli SQL dosyalarını geçici bir dizine stage eder
- `postgres` hesabının staged SQL paketine erişebildiğini doğrular
- scratch veritabanı zaten varsa siler
- scratch veritabanını yeniden oluşturur
- `public` şeması içinde `pgcrypto` uzantısını garanti eder
- `901_preflight_crawler_core_split_surface.psql.sql` dosyasını çalıştırır
- `900_apply_crawler_core_split_surface.psql.sql` dosyasını çalıştırır
- `902_presence_audit_crawler_core_split_surface.psql.sql` dosyasını çalıştırır
- başarı halinde `VALIDATION_RESULT=PASS` çıktısını verir

## Pass criteria

Treat the run as successful only if all of these are true:

- the command exits with status `0`
- output contains `VALIDATION_RESULT=PASS`
- output contains `VALIDATED_DB=...`
- preflight does not fail
- apply bundle does not fail
- presence audit does not fail

## Geçiş kriterleri

Çalıştırmayı yalnızca şu koşulların tümü doğruysa başarılı say:

- komut `0` çıkış durumu ile biter
- çıktıda `VALIDATION_RESULT=PASS` bulunur
- çıktıda `VALIDATED_DB=...` bulunur
- preflight başarısız olmaz
- apply bundle başarısız olmaz
- presence audit başarısız olmaz

## Failure handling

If the run fails:

- do **not** patch SQL blindly
- do **not** move to `parse_core`
- capture the exact failing step
- preserve the terminal output
- repair the real failing cause first
- rerun this same runbook only after the cause is understood

## Hata durumu yönetimi

Çalıştırma başarısız olursa:

- SQL'i körlemesine patch'leme
- `parse_core` tarafına geçme
- tam olarak hangi adımın düştüğünü kaydet
- terminal çıktısını sakla
- önce gerçek hata nedenini düzelt
- neden anlaşıldıktan sonra aynı runbook'u tekrar çalıştır

## Prohibited shortcuts

Do not do these:

- do **not** source individual SQL files manually in random order
- do **not** skip preflight
- do **not** claim success from partial output
- do **not** treat scratch success as Pi51 live migration
- do **not** jump directly to `desktop_import`

## Yasak kısayollar

Şunları yapma:

- tekil SQL dosyalarını rastgele sırayla elle çalıştırma
- preflight adımını atlama
- kısmi çıktıyı başarı gibi yorumlama
- scratch başarısını Pi51 canlı geçişi gibi sunma
- doğrudan `desktop_import` tarafına atlama

## Completion handoff

After a clean successful run of this runbook, the next normal documentation/work line should move to:

- `parse_core`

It should not jump directly to `desktop_import`.

## Tamamlanma devri

Bu runbook temiz şekilde başarıyla tamamlandıktan sonra sıradaki normal dokümantasyon/iş hattı şu tarafa geçmelidir:

- `parse_core`

Doğrudan `desktop_import` tarafına atlamamalıdır.

## Maintenance rule

Update this runbook in the same work package if any of these change:

- validation runner behavior
- scratch database naming
- required prerequisite extension behavior
- apply / preflight / presence-audit entrypoints
- the real execution order between `crawler_core`, `parse_core`, and `desktop_import`

## Bakım kuralı

Şunlardan herhangi biri değişirse bu runbook aynı iş paketi içinde güncellenmelidir:

- validation runner davranışı
- scratch veritabanı adlandırması
- gerekli prerequisite extension davranışı
- apply / preflight / presence-audit giriş noktaları
- `crawler_core`, `parse_core` ve `desktop_import` arasındaki gerçek yürütme sırası
