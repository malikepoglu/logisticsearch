# Webcrawler Python Worker Surface

This is the first real Python-side worker surface for LogisticSearch.

# Webcrawler Python Worker Yüzeyi

Bu, LogisticSearch için ilk gerçek Python-tarafı worker yüzeyidir.

## Purpose

This directory provides the first controlled Python implementation surface for the LogisticSearch webcrawler.

Its job is intentionally narrow:
it proves that Python can call the current crawler-core SQL claim path honestly, observe the current robots allow-decision surface, and then roll the transaction back safely.

It is not a full crawler runtime.

## Amaç

Bu dizin, LogisticSearch webcrawler için ilk kontrollü Python implementasyon yüzeyini sağlar.

Görevi bilinçli olarak dardır:
Python tarafının mevcut crawler-core SQL claim yolunu dürüst biçimde çağırabildiğini, mevcut robots allow-decision yüzeyini gözlemleyebildiğini ve ardından transaction'ı güvenli biçimde rollback edebildiğini kanıtlar.

Bu dizin tam bir crawler runtime değildir.

## Current truth boundary

This directory is the first real Python-side worker surface for the LogisticSearch webcrawler.

Its current scope is intentionally narrow and controlled.

It does not yet provide a real HTTP fetch runtime.

It does not yet provide robots cache refresh fetching.

It does not yet provide success / retryable-error / permanent-error finalize execution.

It does not yet provide parse/runtime continuation.

It does not yet provide service-layer runtime orchestration.

It does not yet provide shutdown helper or power helper behavior.

The current proved truth is narrower:
a probe-only worker can claim one URL through the real SQL surface, inspect the current robots allow-decision output, emit structured JSON, and leave the scratch database lease-clean by rollback.

## Güncel gerçeklik sınırı

Bu dizin, LogisticSearch webcrawler için ilk gerçek Python-tarafı worker yüzeyidir.

Güncel kapsamı bilinçli olarak dar ve kontrollüdür.

Henüz gerçek bir HTTP fetch runtime'ı sağlamaz.

Henüz robots cache refresh fetch akışını sağlamaz.

Henüz success / retryable-error / permanent-error finalize çalıştırmasını sağlamaz.

Henüz parse/runtime devam akışını sağlamaz.

Henüz service-layer runtime orkestrasyonu sağlamaz.

Henüz shutdown helper veya power helper davranışı sağlamaz.

Kanıtlanmış güncel gerçek daha dardır:
probe-only bir worker, gerçek SQL yüzeyi üzerinden bir URL claim edebilir, mevcut robots allow-decision çıktısını inceleyebilir, yapılı JSON üretebilir ve scratch veritabanını rollback ile lease-clean bırakabilir.

## Files

Current controlled files in this directory:

- `worker_claim_loop.py`  
  CLI entry surface for the first probe-only worker run.

- `lib/db.py`  
  Narrow database access helpers for claim, lease-renewal access, robots allow-decision access, transaction close, and rollback.

- `lib/worker_runtime.py`  
  Probe-only worker runtime logic that keeps the first implementation honest.

- `requirements.txt`  
  The tracked dependency surface for this directory.

## Dosyalar

Bu dizindeki güncel kontrollü dosyalar:

- `worker_claim_loop.py`  
  İlk probe-only worker çalıştırması için CLI giriş yüzeyi.

- `lib/db.py`  
  Claim, lease-renewal erişimi, robots allow-decision erişimi, transaction kapatma ve rollback için dar veritabanı yardımcıları.

- `lib/worker_runtime.py`  
  İlk implementasyonu dürüst tutan probe-only worker runtime mantığı.

- `requirements.txt`  
  Bu dizin için izlenen bağımlılık yüzeyi.

## Authoritative basis

This directory must be read and evolved against the current GitHub-tracked project contracts first.

The most important current authority surfaces for this worker directory are:

- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `docs/SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
- `sql/crawler_core/README.md`
- `sql/crawler_core/906_seed_frontier_entrypoint_bootstrap.psql.sql`

Code here must follow those documents.
Code here must not silently outrun those documents.

## Otoritatif temel

Bu dizin, önce GitHub üzerinde izlenen güncel proje sözleşmelerine göre okunmalı ve geliştirilmelidir.

Bu worker dizini için en önemli güncel otorite yüzeyleri şunlardır:

- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `docs/SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
- `sql/crawler_core/README.md`
- `sql/crawler_core/906_seed_frontier_entrypoint_bootstrap.psql.sql`

Buradaki kod bu dokümanları izlemelidir.
Buradaki kod bu dokümanların sessizce önüne geçmemelidir.

## Working rule

Every future coding step in this directory must be doc-driven.

That means:

- check the relevant GitHub-tracked docs/contracts first
- implement only what the current contracts honestly allow
- keep narrow truth explicit
- do not imply production-grade completeness before proof exists
- expand in controlled layers, not by hidden jumps

## Çalışma kuralı

Bu dizindeki her gelecekteki kodlama adımı doküman güdümlü olmalıdır.

Bunun anlamı şudur:

- önce ilgili GitHub-tracked dokümanları/sözleşmeleri kontrol et
- yalnızca mevcut sözleşmelerin dürüstçe izin verdiği şeyi implemente et
- dar güncel gerçeği açık tut
- kanıt oluşmadan production-grade tamlık ima etme
- gizli sıçramalarla değil, kontrollü katmanlarla genişlet

## Controlled dependency surface

This directory now has one tracked dependency surface: `requirements.txt`.

Current controlled dependency rule:

- use `psycopg[binary]==3.3.3`
- do not add broader crawler dependencies yet
- do not add HTTP client packages yet
- do not add parser stacks yet
- do not add orchestration/runtime packages yet unless a later doc-driven patch proves they are needed

A local virtual environment may be created for execution, but the tracked dependency truth for the repository must remain the committed `requirements.txt` file.

## Kontrollü bağımlılık yüzeyi

Bu dizinin artık bir izlenen bağımlılık yüzeyi vardır: `requirements.txt`.

Güncel kontrollü bağımlılık kuralı şudur:

- `psycopg[binary]==3.3.3` kullan
- henüz daha geniş crawler bağımlılıkları ekleme
- henüz HTTP client paketleri ekleme
- henüz parser stack'leri ekleme
- daha sonraki doküman-güdümlü bir patch gerçekten gerektiğini kanıtlamadıkça orkestrasyon/runtime paketleri ekleme

Çalıştırma için yerel bir virtual environment oluşturulabilir; ancak repository için izlenen bağımlılık doğrusu committed `requirements.txt` dosyası olarak kalmalıdır.

## Minimal processed-output storage routing

This directory now also includes `python/webcrawler/lib/storage_routing.py`.

Current minimal canonical storage rule:

- raw and working crawler accumulation stays under `/srv`
- processed output goes to `/srv/data` when `/srv/data` is usable
- if `/srv/data` is not usable, processed output goes to `/srv/buffer`
- if `/srv/data` becomes usable again while `/srv/buffer` contains buffered backlog, crawler must pause and stay paused until buffered processed output is fully drained into `/srv/data`
- if neither `/srv/data` nor `/srv/buffer` is usable, crawler must pause and surface an explicit error

This surface is intentionally minimal.
It defines the current processed-output path choice truth, but it does not yet implement the real drain execution or worker-loop integration.

## Minimal işlenmiş-çıktı storage routing

Bu dizin artık `python/webcrawler/lib/storage_routing.py` dosyasını da içerir.

Güncel minimal kanonik storage kuralı şudur:

- ham ve çalışma crawler birikimi `/srv` altında kalır
- işlenmiş çıktı, `/srv/data` kullanılabiliyorsa `/srv/data` yoluna gider
- `/srv/data` kullanılamıyorsa işlenmiş çıktı `/srv/buffer` yoluna gider
- `/srv/data` yeniden kullanılabilir hale gelirken `/srv/buffer` içinde buffer backlog varsa crawler pause olmalı ve buffer işlenmiş çıktı tamamen `/srv/data` yoluna boşaltılana kadar paused kalmalıdır
- ne `/srv/data` ne de `/srv/buffer` kullanılabiliyorsa crawler pause olmalı ve açık bir hata üretmelidir

Bu yüzey bilinçli olarak minimal tutulmuştur.
Mevcut işlenmiş-çıktı path seçimi doğrusunu tanımlar; ancak gerçek drain execution'ını veya worker-loop entegrasyonunu henüz uygulamaz.

