# Webcrawler Python Worker Surface

This is the current controlled Python-side crawler runtime surface for LogisticSearch.

# Webcrawler Python Worker Yüzeyi

Bu, LogisticSearch için güncel kontrollü Python-tarafı crawler runtime yüzeyidir.

## Purpose

This directory provides the first controlled but real Python implementation surface for the LogisticSearch webcrawler.

Its scope is still intentionally narrow, but it is no longer limited to a probe-only claim demonstration.

It is not yet a broad production-grade crawler runtime.

## Amaç

Bu dizin, LogisticSearch webcrawler için ilk kontrollü ama gerçek Python implementasyon yüzeyini sağlar.

Kapsamı hâlâ bilinçli olarak dardır; ancak artık probe-only claim gösterimiyle sınırlı değildir.

Henüz geniş kapsamlı production-grade bir crawler runtime değildir.

## Current truth boundary

This directory is the first real Python-side worker surface for the LogisticSearch webcrawler.

Its current scope is still intentionally controlled.

It currently provides:

- storage-aware claim gating
- probe-only and durable claim modes
- a minimal real HTTP fetch flow
- raw response-body persistence under `/srv/crawler/logisticsearch/raw_fetch`
- success finalization back into crawler-core
- a minimal parse-entry flow that writes evidence
- workflow-status writing for the current narrow parse path
- a safe parse-link policy that refuses blind `linked_snapshot_id` reuse when snapshot mapping is ambiguous

It does not yet provide:

- robots cache refresh fetching
- a broader parser stack
- a sealed preranking-snapshot linkage model
- full production-grade orchestration/service supervision
- shutdown helper or power helper behavior

## Güncel gerçeklik sınırı

Bu dizin, LogisticSearch webcrawler için ilk gerçek Python-tarafı worker yüzeyidir.

Güncel kapsamı hâlâ bilinçli olarak kontrollüdür.

Şu anda şunları sağlar:

- storage-aware claim gating
- probe-only ve durable claim modları
- minimal gerçek HTTP fetch akışı
- ham response body'lerini `/srv/crawler/logisticsearch/raw_fetch` altında saklama
- crawler-core tarafına success finalize dönüşü
- evidence yazan minimal parse-entry akışı
- mevcut dar parse yolu için workflow-status yazımı
- snapshot eşlemesi belirsiz olduğunda kör `linked_snapshot_id` yeniden kullanımını reddeden güvenli parse-link politikası

Henüz şunları sağlamaz:

- robots cache refresh fetch akışı
- daha geniş bir parser stack
- mühürlenmiş bir preranking-snapshot linkage modeli
- tam production-grade orchestration/service supervision
- shutdown helper veya power helper davranışı

## Files

Current controlled files in this directory:

- `worker_claim_loop.py`  
  CLI entry surface for single-run worker execution in probe-only or durable-claim mode.

- `lib/db.py`  
  Database helpers for claim, finalize, parse persistence, workflow updates, and transaction control.

- `lib/storage_routing.py`  
  Minimal processed-output routing truth for `/srv`, `/srv/data`, and `/srv/buffer`.

- `lib/fetch_runtime.py`  
  Minimal real HTTP fetch layer that stores raw response bodies under `/srv/crawler/logisticsearch/raw_fetch`.

- `lib/parse_runtime.py`  
  Minimal parse-entry layer that extracts basic page evidence and enforces safe snapshot-link policy.

- `lib/worker_runtime.py`  
  Controlled worker runtime that spans storage-aware claim, minimal fetch, finalize, and minimal parse continuation.

- `requirements.txt`  
  The tracked dependency surface for this directory.

- `bootstrap_venv.sh`  
  Controlled local venv bootstrap helper for this Python surface.

## Dosyalar

Bu dizindeki güncel kontrollü dosyalar:

- `worker_claim_loop.py`  
  Probe-only veya durable-claim modunda tek çalıştırmalık worker yürütmesi için CLI giriş yüzeyi.

- `lib/db.py`  
  Claim, finalize, parse persistence, workflow update ve transaction control için veritabanı yardımcıları.

- `lib/storage_routing.py`  
  `/srv`, `/srv/data` ve `/srv/buffer` için minimal işlenmiş-çıktı yönlendirme doğrusu.

- `lib/fetch_runtime.py`  
  Ham response body'lerini `/srv/crawler/logisticsearch/raw_fetch` altına yazan minimal gerçek HTTP fetch katmanı.

- `lib/parse_runtime.py`  
  Temel sayfa evidence'ı çıkaran ve güvenli snapshot-link politikasını uygulayan minimal parse-entry katmanı.

- `lib/worker_runtime.py`  
  Storage-aware claim, minimal fetch, finalize ve minimal parse continuation kapsayan kontrollü worker runtime katmanı.

- `requirements.txt`  
  Bu dizin için izlenen bağımlılık yüzeyi.

- `bootstrap_venv.sh`  
  Bu Python yüzeyi için kontrollü local venv bootstrap yardımcısı.

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
- do not add broader parser stacks yet
- do not add orchestration/runtime packages yet unless a later doc-driven patch proves they are needed

A local virtual environment may be created for execution, but the tracked dependency truth for the repository must remain the committed `requirements.txt` file.

## Kontrollü bağımlılık yüzeyi

Bu dizinin artık bir izlenen bağımlılık yüzeyi vardır: `requirements.txt`.

Güncel kontrollü bağımlılık kuralı şudur:

- `psycopg[binary]==3.3.3` kullan
- henüz daha geniş crawler bağımlılıkları ekleme
- henüz daha geniş parser stack'leri ekleme
- daha sonraki doküman-güdümlü bir patch gerçekten gerektiğini kanıtlamadıkça orkestrasyon/runtime paketleri ekleme

Çalıştırma için yerel bir virtual environment oluşturulabilir; ancak repository için izlenen bağımlılık doğrusu committed `requirements.txt` dosyası olarak kalmalıdır.

## Minimal processed-output storage routing

This directory also includes `python/webcrawler/lib/storage_routing.py`.

Current minimal canonical storage rule:

- raw and working crawler accumulation stays under `/srv`
- processed output goes to `/srv/data` when `/srv/data` is usable
- if `/srv/data` is not usable, processed output goes to `/srv/buffer`
- if `/srv/data` becomes usable again while `/srv/buffer` contains buffered backlog, crawler must pause and stay paused until buffered processed output is fully drained into `/srv/data`
- if neither `/srv/data` nor `/srv/buffer` is usable, crawler must pause and surface an explicit error

This routing truth is intentionally narrow and explicit.

## Minimal işlenmiş-çıktı storage routing

Bu dizin ayrıca `python/webcrawler/lib/storage_routing.py` dosyasını da içerir.

Güncel minimal kanonik storage kuralı şudur:

- ham ve çalışma crawler birikimi `/srv` altında kalır
- işlenmiş çıktı, `/srv/data` kullanılabiliyorsa `/srv/data` yoluna gider
- `/srv/data` kullanılamıyorsa işlenmiş çıktı `/srv/buffer` yoluna gider
- `/srv/data` yeniden kullanılabilir hale gelirken `/srv/buffer` içinde buffer backlog varsa crawler pause olmalı ve buffer işlenmiş çıktı tamamen `/srv/data` yoluna boşaltılana kadar paused kalmalıdır
- ne `/srv/data` ne de `/srv/buffer` kullanılabiliyorsa crawler pause olmalı ve açık bir hata üretmelidir

Bu routing doğrusu bilinçli olarak dar ve açık tutulmuştur.
