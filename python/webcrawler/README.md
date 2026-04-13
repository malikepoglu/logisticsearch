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
  * storage-aware claim gating
  * probe-only and durable claim modes
  * a minimal real HTTP fetch flow
  * raw response-body persistence under `/srv/crawler/logisticsearch/raw_fetch`
  * canonical robots refresh-decision evaluation through crawler-core
  * controlled robots.txt fetching, raw-body persistence, narrow parsing, and cache upsert flow
  * success finalization back into crawler-core
  * a minimal parse-entry flow that writes evidence
  * workflow-status writing for the current narrow parse path
  * a safe parse-link policy that refuses blind `linked_snapshot_id` reuse when snapshot mapping is ambiguous
  * a committed narrow browser-render acquisition surface
  * a committed repo-local browser smoke entry that proves rendered HTML, screenshot, and JSON evidence generation on the real crawler machine

It does not yet provide:

  * worker-integrated browser-path selection inside the canonical fetch path
  * a broader parser stack
  * a sealed preranking-snapshot linkage model
  * full production-grade orchestration/service supervision
  * shutdown helper or power helper behavior

## Current runtime clarification for guarded parse continuation

The current worker surface now contains one explicit guarded-runtime rule that matters for scratch smoke interpretation.

A successful real page fetch does **not** automatically imply that narrow parse persistence will run.

The worker attempts that optional parse-side continuation only when:

- the fetched content is parse-suitable for the current narrow path
- the connected PostgreSQL database really exposes the `parse` schema

So crawler_core-only scratch databases can still be valid durable fetch/finalize smoke targets even when they do not expose the `parse` schema.

In that case, the worker skips optional parse persistence deliberately and still performs valid success finalization in the correct order.

## Guarded parse continuation için güncel runtime açıklaması

Güncel worker yüzeyi, scratch smoke yorumlaması için önemli olan açık bir guarded-runtime kuralı içerir.

Başarılı bir gerçek page fetch, dar parse persistence adımının otomatik olarak da çalışacağı anlamına **gelmez**.

Worker bu opsiyonel parse-tarafı continuation adımını yalnızca şu koşullarda dener:

- fetch edilen içerik mevcut dar yol için parse edilmeye uygundur
- bağlı PostgreSQL veritabanı gerçekten `parse` şemasını sağlar

Bu nedenle yalnızca crawler_core içeren scratch veritabanları, `parse` şemasını sağlamasalar bile hâlâ geçerli durable fetch/finalize smoke hedefleri olabilir.

Böyle bir durumda worker opsiyonel parse persistence adımını bilinçli olarak atlar ve yine doğru sırada geçerli success finalization yapar.

## Güncel gerçeklik sınırı

Bu dizin, LogisticSearch webcrawler için ilk gerçek Python-tarafı worker yüzeyidir.

Güncel kapsamı hâlâ bilinçli olarak kontrollüdür.

Şu anda şunları sağlar:
  * storage-aware claim gating
  * probe-only ve durable claim modları
  * minimal gerçek HTTP fetch akışı
  * ham response body'lerini `/srv/crawler/logisticsearch/raw_fetch` altında saklama
  * crawler-core üzerinden kanonik robots refresh-decision değerlendirmesi
  * kontrollü robots.txt fetch, ham body saklama, dar parse ve cache upsert akışı
  * crawler-core tarafına success finalize dönüşü
  * evidence yazan minimal parse-entry akışı
  * mevcut dar parse yolu için workflow-status yazımı
  * snapshot eşlemesi belirsiz olduğunda kör `linked_snapshot_id` yeniden kullanımını reddeden güvenli parse-link politikası
  * commit edilmiş dar browser-render acquisition yüzeyi
  * gerçek crawler makinesinde rendered HTML, screenshot ve JSON kanıtı üreten commit edilmiş repo-local browser smoke giriş yüzeyi

Henüz şunları sağlamaz:

  * kanonik fetch yolu içinde worker-entegre browser-path seçimi
  * daha geniş bir parser stack
  * mühürlenmiş bir preranking-snapshot linkage modeli
  * tam production-grade orchestration/service supervision
  * shutdown helper veya power helper davranışı

## Boundary against map-library choice

This directory is responsible for crawler/runtime-side geospatial data truth, not future application-screen library choice.

That means:

- collecting or enriching coordinates may belong here
- GeoJSON-ready or PostGIS-ready geospatial output truth may belong here
- OSM-facing acquisition constraints may belong here

But these decisions do **not** belong here:

- application-side map presentation-library choice
- live-tracking screen choice
- operator-facing analytical map-screen choice

Those belong to:

- `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`

## Harita-kütüphanesi seçimine karşı sınır

Bu dizin gelecekteki uygulama ekranı kütüphanesi seçimiyle değil, crawler/runtime tarafındaki coğrafi veri doğrusu ile ilgilidir.

Bunun anlamı şudur:

- koordinat toplama veya zenginleştirme burada yer alabilir
- GeoJSON-hazır veya PostGIS-hazır coğrafi çıktı doğrusu burada yer alabilir
- OSM'e bakan veri edinim kısıtları burada yer alabilir

Ama şu kararlar burada yer almaz:

- uygulama tarafı harita gösterim-kütüphanesi seçimi
- canlı takip ekranı tercihi
- operatör-yüzlü analitik harita ekranı tercihi

Bunlar şu dokümana aittir:

- `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`

## Files

Current controlled files in this directory:

  * `lib/logisticsearch2_worker_claim_loop.py`
CLI entry surface for single-run worker execution in probe-only or durable-claim mode.

  * `lib/db.py`
Database helpers for claim, finalize, parse persistence, workflow updates, and transaction control.

  * `lib/storage_routing.py`
Minimal processed-output routing truth for `/srv`, `/srv/data`, and `/srv/buffer`.

  * `lib/logisticsearch1_1_fetch_runtime.py`
Minimal acquisition layer. It currently carries the direct HTTP fetch path and should become the single narrow acquisition home for both direct HTTP and browser-backed page capture over time.

  * `lib/logisticsearch1_2_browser_acquisition_runtime.py`
Current narrow browser-render acquisition seam that captures rendered HTML, screenshot evidence, and browser-network observations.

  * `lib/parse_runtime.py`
Minimal parse-entry layer that extracts basic page evidence and enforces safe snapshot-link policy.

  * `lib/logisticsearch1_main_worker_runtime.py`
Controlled worker runtime that should remain the main continuous crawler runtime/service core rather than being split across multiple competing runtime centers.

  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
Repo-local browser smoke entry used to prove that the committed browser-acquisition seam can launch, navigate, and emit evidence on the real crawler machine.

  * `requirements.txt`
The tracked dependency surface for this directory.

  * `bootstrap_venv.sh`
Controlled local venv bootstrap helper for this Python surface.

The active Python runtime family now lives under `python/webcrawler/lib/`.

Aktif Python runtime ailesi artık `python/webcrawler/lib/` altında yaşamaktadır.

## Canonical lean runtime direction

The long-term runtime reading for this directory must remain lean and explicit.

That means:

  * `lib/logisticsearch1_main_worker_runtime.py` should remain the main continuous crawler runtime/service core
  * `lib/logisticsearch1_1_fetch_runtime.py` should remain the acquisition layer and absorb both direct HTTP and browser-backed fetch paths over time
  * `lib/logisticsearch1_2_browser_acquisition_runtime.py` is currently a narrow transitional seam and may later be folded into `lib/logisticsearch1_1_fetch_runtime.py` if that keeps the system simpler
  * `lib/parse_runtime.py` remains the post-fetch evidence and parsing layer
  * `lib/db.py` remains the database/state-transition helper layer
  * `lib/storage_routing.py` remains the storage-decision layer for `/srv/crawler/logisticsearch`, `/srv/data`, and `/srv/buffer`
  * `lib/logisticsearch2_worker_claim_loop.py` must remain a thin operator/CLI surface and must not grow into a second hidden runtime center

The crawler should therefore grow by strengthening a small number of clear files, not by scattering logic across many overlapping entrypoints.

## Dosyalar

Bu dizindeki güncel kontrollü dosyalar:

  * `lib/logisticsearch2_worker_claim_loop.py`
Probe-only veya durable-claim modunda tek çalıştırmalık worker yürütmesi için CLI giriş yüzeyi.

  * `lib/db.py`
Claim, finalize, parse persistence, workflow update ve transaction control için veritabanı yardımcıları.

  * `lib/storage_routing.py`
`/srv`, `/srv/data` ve `/srv/buffer` için minimal işlenmiş-çıktı yönlendirme doğrusu.

  * `lib/logisticsearch1_1_fetch_runtime.py`
Minimal acquisition katmanıdır. Şu anda direct HTTP fetch yolunu taşır; zamanla hem direct HTTP hem browser destekli sayfa yakalama için tek dar acquisition evi haline gelmelidir.

  * `lib/logisticsearch1_2_browser_acquisition_runtime.py`
Rendered HTML, screenshot kanıtı ve browser-network gözlemleri yakalayan güncel dar browser-render acquisition seam'idir.

  * `lib/parse_runtime.py`
Temel sayfa evidence'ı çıkaran ve güvenli snapshot-link politikasını uygulayan minimal parse-entry katmanıdır.

  * `lib/logisticsearch1_main_worker_runtime.py`
Birden fazla yarışan runtime merkezi arasında bölünmek yerine ana sürekli çalışan crawler runtime/service çekirdeği olarak kalması gereken kontrollü worker runtime katmanıdır.

  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
Commit edilmiş browser-acquisition seam'inin gerçek crawler makinesinde launch, navigation ve kanıt üretimi yapabildiğini kanıtlamak için kullanılan repo-local browser smoke giriş yüzeyidir.

  * `requirements.txt`
Bu dizin için izlenen bağımlılık yüzeyidir.

  * `bootstrap_venv.sh`
Bu Python yüzeyi için kontrollü local venv bootstrap yardımcısıdır.

## Kanonik yalın runtime yönü

Bu dizin için uzun vadeli runtime okuması yalın ve açık kalmalıdır.

Bunun anlamı şudur:

  * `lib/logisticsearch1_main_worker_runtime.py` ana sürekli çalışan crawler runtime/service çekirdeği olarak kalmalıdır
  * `lib/logisticsearch1_1_fetch_runtime.py` acquisition katmanı olarak kalmalı ve zamanla direct HTTP ile browser destekli fetch yollarını kendi içinde toplamalıdır
  * `lib/logisticsearch1_2_browser_acquisition_runtime.py` şu anda dar bir geçiş seam'idir; sistemi daha sade tutacaksa ileride `lib/logisticsearch1_1_fetch_runtime.py` içine katlanabilir
  * `lib/parse_runtime.py` fetch sonrası evidence ve parse katmanı olarak kalır
  * `lib/db.py` veritabanı/state-transition yardımcı katmanı olarak kalır
  * `lib/storage_routing.py` `/srv/crawler/logisticsearch`, `/srv/data` ve `/srv/buffer` için storage-karar katmanı olarak kalır
  * `lib/logisticsearch2_worker_claim_loop.py` ince bir operatör/CLI yüzeyi olarak kalmalı, ikinci gizli runtime merkezine dönüşmemelidir

Dolayısıyla crawler, birçok çakışan giriş noktasına saçılarak değil, az sayıdaki açık dosyanın güçlendirilmesiyle büyümelidir.

## Canonical runtime role map

The crawler runtime must remain intentionally lean and role-separated.

The corrected target file family is:

  * `logisticsearch1_main_worker_runtime.py`
  * `logisticsearch1_1_fetch_runtime.py`
  * `logisticsearch1_2_browser_acquisition_runtime.py`
  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
  * `logisticsearch1_3_parse_runtime.py`
  * `logisticsearch1_4_db.py`
  * `logisticsearch1_5_storage_routing.py`
  * `lib/logisticsearch2_worker_claim_loop.py`

Detailed reading of each file:

  * `logisticsearch1_main_worker_runtime.py`
    Main continuous crawler runtime/service core.
    This file should orchestrate claim -> robots -> acquisition -> parse continuation -> finalize order.
    It should not become a second acquisition implementation home.

  * `logisticsearch1_1_fetch_runtime.py`
    Acquisition home.
    Direct HTTP page fetch lives here.
    Robots fetch lives here.
    Over time this file should become the single narrow acquisition home for browser-backed fetch too.

  * `logisticsearch1_2_browser_acquisition_runtime.py`
    Narrow transitional browser-render seam.
    It exists to keep the first browser-based acquisition capability explicit, provable, and isolated
    before the browser-backed path is folded more tightly into the canonical fetch runtime.

  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
    Repo-local browser smoke tool.
    This is not the main runtime.
    It exists only to prove browser launch, public-page navigation, rendered HTML capture,
    screenshot evidence, and machine-readable JSON evidence.

  * `logisticsearch1_3_parse_runtime.py`
    Parse / evidence extraction layer.
    This file is responsible for narrow post-fetch evidence extraction and should gradually grow
    into controlled filtering, normalization, and future pre-ranking preparation.

  * `logisticsearch1_4_db.py`
    Database and state-transition helper layer.
    Claim/finalize/persistence/workflow helper behavior belongs here, not inside ad hoc runtime fragments.

  * `logisticsearch1_5_storage_routing.py`
    Storage decision layer.
    This file should remain responsible for `/srv/crawler/logisticsearch/`, `/srv/data/`, and `/srv/buffer`
    routing truth and should not become a fetch or parse file.

  * `lib/logisticsearch2_worker_claim_loop.py`
    Thin CLI/operator surface.
    This is related to the worker runtime but it is not a child implementation layer inside the same
    top-level runtime family. That is why it belongs under `2`, not under `1`.

Operational interpretation:

  * `1` family = main continuous runtime tree
  * `1_1 ... 1_5` = sublayers under the main runtime tree
  * `1_2_1` = smoke tool under the browser-acquisition seam
  * `2` family = separate thin operator/CLI surface

This keeps the system explicit, predictable, and lean.

## Kanonik runtime rol haritası

Crawler runtime bilinçli olarak yalın ve rol-ayrımlı kalmalıdır.

Düzeltilmiş hedef dosya ailesi şudur:

  * `logisticsearch1_main_worker_runtime.py`
  * `logisticsearch1_1_fetch_runtime.py`
  * `logisticsearch1_2_browser_acquisition_runtime.py`
  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
  * `logisticsearch1_3_parse_runtime.py`
  * `logisticsearch1_4_db.py`
  * `logisticsearch1_5_storage_routing.py`
  * `lib/logisticsearch2_worker_claim_loop.py`

Her dosyanın ayrıntılı okuması:

  * `logisticsearch1_main_worker_runtime.py`
    Ana sürekli çalışan crawler runtime/service çekirdeği.
    Bu dosya claim -> robots -> acquisition -> parse continuation -> finalize sırasını orkestre etmelidir.
    İkinci bir acquisition implementasyon evi haline gelmemelidir.

  * `logisticsearch1_1_fetch_runtime.py`
    Acquisition evidir.
    Direct HTTP page fetch burada yaşar.
    Robots fetch burada yaşar.
    Zamanla browser destekli fetch yolu da tek dar acquisition evi olarak burada toplanmalıdır.

  * `logisticsearch1_2_browser_acquisition_runtime.py`
    Dar geçiş browser-render seam'idir.
    Var olma sebebi, browser tabanlı ilk acquisition kabiliyetini kanonik fetch runtime içine daha sıkı katlanmadan önce
    açık, kanıtlanabilir ve izole halde tutmaktır.

  * `lib/logisticsearch1_2_1_browser_acquisition_smoke.py`
    Repo-local browser smoke aracıdır.
    Ana runtime değildir.
    Yalnızca browser launch, public page navigation, rendered HTML capture, screenshot kanıtı
    ve machine-readable JSON kanıtı üretimini doğrulamak için vardır.

  * `logisticsearch1_3_parse_runtime.py`
    Parse / evidence extraction katmanıdır.
    Bu dosya dar post-fetch evidence extraction işinden sorumludur ve zamanla kontrollü filtering,
    normalization ve gelecekteki pre-ranking hazırlığı yönünde büyümelidir.

  * `logisticsearch1_4_db.py`
    Veritabanı ve state-transition yardımcı katmanıdır.
    Claim/finalize/persistence/workflow yardımcı davranışı rastgele runtime parçalarında değil burada yaşamalıdır.

  * `logisticsearch1_5_storage_routing.py`
    Storage karar katmanıdır.
    Bu dosya `/srv/crawler/logisticsearch/`, `/srv/data/` ve `/srv/buffer` yönlendirme doğrusundan sorumlu kalmalı,
    fetch veya parse dosyasına dönüşmemelidir.

  * `lib/logisticsearch2_worker_claim_loop.py`
    İnce CLI/operatör yüzeyidir.
    Worker runtime ile ilişkilidir; ancak aynı üst runtime ailesi içinde hiyerarşik alt implementasyon katmanı değildir.
    Bu yüzden `1` altında değil, `2` altında yer almalıdır.

Operasyonel yorum:

  * `1` ailesi = ana sürekli çalışan runtime ağacı
  * `1_1 ... 1_5` = ana runtime ağacının alt katmanları
  * `1_2_1` = browser-acquisition seam'inin altındaki smoke aracı
  * `2` ailesi = ayrı ince operatör/CLI yüzeyi

Bu okuma sistemi açık, öngörülebilir ve yalın tutar.

## Canonical version metadata rule

Live source filenames should remain stable.

Version truth should be carried inside the file metadata in a human-readable form.

Canonical example:

  * `SURFACE_VERSION = "V1-13.04.2026-15.41.13"`

Why this format is preferred:

  * operators can read it immediately
  * runbooks can quote it without decoding
  * handoff and audit notes stay human-readable
  * the live source filename stays stable while the version truth still remains explicit

This version string belongs inside source metadata, README truth, runbook truth, and Git history.

It should not be used to rename the live source file on every change.

## Kanonik version metadata kuralı

Canlı source dosya adları stabil kalmalıdır.

Version doğrusu insan-okunur biçimde dosya içi metadata ile taşınmalıdır.

Kanonik örnek:

  * `SURFACE_VERSION = "V1-13.04.2026-15.41.13"`

Bu formatın tercih sebebi:

  * operatör bunu anında okuyabilir
  * runbook bunu şifresini çözmeden alıntılayabilir
  * handoff ve audit notları insan-okunur kalır
  * canlı source dosya adı stabil kalırken version doğrusu yine de açık biçimde taşınır

Bu version metni source metadata, README doğrusu, runbook doğrusu ve Git geçmişi içinde yer almalıdır.

Canlı source dosyası her değişiklikte bununla yeniden adlandırılmamalıdır.

## Current operational status snapshot

Current proven status:

  * direct HTTP acquisition exists
  * robots fetch/cache flow exists
  * raw fetch persistence exists
  * narrow parse continuation exists
  * committed browser-render acquisition seam exists
  * committed repo-local browser smoke exists and has been proven on the real crawler machine

Current missing integration truth:

  * the main worker runtime still does not select browser-backed acquisition inside the canonical fetch path
  * the browser seam is still separate from the main acquisition home
  * crawler_core must therefore remain open

## Güncel operasyonel durum özeti

Güncel kanıtlanmış durum:

  * direct HTTP acquisition mevcut
  * robots fetch/cache akışı mevcut
  * ham fetch persistence mevcut
  * dar parse continuation mevcut
  * commit edilmiş browser-render acquisition seam'i mevcut
  * commit edilmiş repo-local browser smoke mevcut ve gerçek crawler makinesinde kanıtlandı

Güncel eksik entegrasyon doğrusu:

  * ana worker runtime henüz kanonik fetch yolu içinde browser destekli acquisition seçimi yapmıyor
  * browser seam'i hâlâ ana acquisition evinden ayrı duruyor
  * bu nedenle crawler_core açık kalmalıdır

## Immediate next implementation order

The next coding order must remain narrow:

  1. first finish README truth and commit it
  2. then rename the Python surfaces in one controlled patch
  3. then repair imports and smoke references
  4. then re-prove syntax and browser smoke
  5. only then evolve the acquisition home
  6. only after that add one narrow selector seam into the main worker runtime

Do not spread acquisition logic across multiple competing runtime centers.

## Hemen sonraki implementation sırası

Sonraki kodlama sırası dar kalmalıdır:

  1. önce README doğrusunu tamamlayıp commit etmek
  2. sonra Python yüzeylerini tek bir kontrollü patch ile yeniden adlandırmak
  3. ardından import ve smoke referanslarını onarmak
  4. sonra sözdizimi ve browser smoke'u yeniden kanıtlamak
  5. ancak ondan sonra acquisition evini büyütmek
  6. ve ancak bunun ardından ana worker runtime içine tek bir dar selector seam'i eklemek

Acquisition mantığı birden fazla yarışan runtime merkezine saçılmamalıdır.

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

This directory also includes `python/webcrawler/lib/logisticsearch1_5_storage_routing.py`.

Current minimal canonical storage rule:

- raw and working crawler accumulation stays under `/srv`
- processed output goes to `/srv/data` when `/srv/data` is usable
- if `/srv/data` is not usable, processed output goes to `/srv/buffer`
- if `/srv/data` becomes usable again while `/srv/buffer` contains buffered backlog, crawler must pause and stay paused until buffered processed output is fully drained into `/srv/data`
- if neither `/srv/data` nor `/srv/buffer` is usable, crawler must pause and surface an explicit error

This routing truth is intentionally narrow and explicit.

## Minimal işlenmiş-çıktı storage routing

Bu dizin ayrıca `python/webcrawler/lib/logisticsearch1_5_storage_routing.py` dosyasını da içerir.

Güncel minimal kanonik storage kuralı şudur:

- ham ve çalışma crawler birikimi `/srv` altında kalır
- işlenmiş çıktı, `/srv/data` kullanılabiliyorsa `/srv/data` yoluna gider
- `/srv/data` kullanılamıyorsa işlenmiş çıktı `/srv/buffer` yoluna gider
- `/srv/data` yeniden kullanılabilir hale gelirken `/srv/buffer` içinde buffer backlog varsa crawler pause olmalı ve buffer işlenmiş çıktı tamamen `/srv/data` yoluna boşaltılana kadar paused kalmalıdır
- ne `/srv/data` ne de `/srv/buffer` kullanılabiliyorsa crawler pause olmalı ve açık bir hata üretmelidir

Bu routing doğrusu bilinçli olarak dar ve açık tutulmuştur.


## Current canonical layout direction

At the current repository point, the live Python runtime family is not yet grouped fully under `python/webcrawler/lib/`.

That is still a temporary truth.

The canonical target direction is:

- all live runtime Python files should sit under `python/webcrawler/lib/`
- the numbered hierarchy should be visible there in one place
- `lib/logisticsearch2_worker_claim_loop.py` now already lives in `lib/` as the thin operator/CLI surface
- `lib/logisticsearch1_2_1_browser_acquisition_smoke.py` now already lives in `lib/` as the repo-local browser smoke entry

Use these supporting surfaces:

- `python/webcrawler/lib/README.md`
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md`

## Güncel kanonik yerleşim yönü

Mevcut repository noktasında canlı Python runtime ailesi henüz tamamen `python/webcrawler/lib/` altında gruplanmış değildir.

Bu hâlâ geçici bir doğrudur.

Kanonik hedef yön şudur:

- tüm canlı runtime Python dosyaları `python/webcrawler/lib/` altında durmalıdır
- numaralı hiyerarşi orada tek yerde görünmelidir
- `lib/logisticsearch2_worker_claim_loop.py` artık ince operatör/CLI yüzeyi olarak zaten `lib/` içinde yaşamaktadır
- `lib/logisticsearch1_2_1_browser_acquisition_smoke.py` artık repo-local browser smoke girişi olarak zaten `lib/` içinde yaşamaktadır

Şu destek yüzeylerini kullan:

- `python/webcrawler/lib/README.md`
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md`
