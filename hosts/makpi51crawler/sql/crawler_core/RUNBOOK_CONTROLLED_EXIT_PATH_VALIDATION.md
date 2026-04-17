# RUNBOOK_CONTROLLED_EXIT_PATH_VALIDATION

## Purpose

This runbook defines the controlled validation flow for the currently implemented crawler-core exit paths on `makpi51crawler`.

It exists to prove, in a disciplined and repeatable way, that the live crawler runtime and the live crawler database agree on the currently implemented frontier exit boundaries:

- success -> transient `parse_pending` -> release back to `queued`
- retryable error -> `retry_wait`
- permanent error -> `dead`
- robots-blocked decision -> `dead` with `last_error_class = 'robots_blocked'`

This runbook is not the schema-apply runbook.  
This runbook is the operational validation runbook for exit-path behavior after the relevant SQL and runtime surfaces already exist.

## Amaç

Bu runbook, `makpi51crawler` üzerindeki şu anda uygulanmış crawler-core çıkış yolları için kontrollü doğrulama akışını tanımlar.

Bu runbook'un amacı, disiplinli ve tekrar edilebilir bir şekilde canlı crawler runtime ile canlı crawler veritabanının şu anda uygulanmış frontier çıkış sınırlarında aynı gerçeği taşıdığını kanıtlamaktır:

- başarı -> geçici `parse_pending` -> tekrar `queued`
- retryable error -> `retry_wait`
- permanent error -> `dead`
- robots tarafından engellenen karar -> `dead` ve `last_error_class = 'robots_blocked'`

Bu runbook schema-apply runbook'u değildir.  
Bu runbook, ilgili SQL ve runtime yüzeyleri zaten var olduktan sonra exit-path davranışını doğrulayan operasyonel runbook'tur.

---

## Scope

This runbook currently covers only the crawler-core exit-path validation package rooted in these surfaces:

- `hosts/makpi51crawler/sql/crawler_core/003_frontier_finish_transitions.sql`
- `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_1_state_db_gateway.py`
- `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_2_worker_runtime.py`
- `docs/SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`

It does not define parse ranking policy, outbox business decisions, or broad service orchestration.

## Kapsam

Bu runbook şu anda yalnızca aşağıdaki yüzeylere köklenen crawler-core exit-path validation paketini kapsar:

- `hosts/makpi51crawler/sql/crawler_core/003_frontier_finish_transitions.sql`
- `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_1_state_db_gateway.py`
- `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_2_worker_runtime.py`
- `docs/SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`

Bu runbook parse ranking politikasını, outbox iş kararlarını veya geniş service orkestrasyonunu tanımlamaz.

---

## Preconditions

Before executing this runbook, the operator must confirm all of the following:

1. Ubuntu Desktop repo is clean and `HEAD == origin/main`.
2. Pi51 repo can fast-forward cleanly to the expected commit.
3. Live runtime and live DB are already provisioned on Pi51.
4. The user service `logisticsearch-webcrawler.service` exists in user scope.
5. The validation target URL is explicitly chosen and understood.
6. Retryable / permanent / robots-blocked smoke proofs must be rollback-based unless a separate explicit live mutation decision is made.
7. Evidence must be written to timestamped output files.

## Önkoşullar

Bu runbook çalıştırılmadan önce operatör aşağıdakilerin tamamını doğrulamalıdır:

1. Ubuntu Desktop repo temiz olmalıdır ve `HEAD == origin/main` olmalıdır.
2. Pi51 repo beklenen commit'e clean fast-forward yapabilmelidir.
3. Canlı runtime ve canlı veritabanı Pi51 üzerinde zaten kurulmuş olmalıdır.
4. `logisticsearch-webcrawler.service` user scope altında mevcut olmalıdır.
5. Doğrulama hedef URL'si açıkça seçilmiş ve anlaşılmış olmalıdır.
6. Retryable / permanent / robots-blocked smoke kanıtları, ayrı bir açık canlı mutasyon kararı verilmedikçe rollback tabanlı olmalıdır.
7. Kanıtlar timestamp'li çıktı dosyalarına yazılmalıdır.

---

## Safety Boundary

The validation flow is intentionally split into two categories:

### Live-changing validation
Used only where the project explicitly accepts a real state transition on the live row.

Current example:
- proving the success path all the way through `parse_pending` release back to `queued`

### Rollback-only validation
Used where behavior must be proven without leaving durable damage in the live row.

Current examples:
- retryable exit path
- permanent exit path
- robots-blocked exit path

## Güvenlik Sınırı

Doğrulama akışı bilinçli olarak iki kategoriye ayrılmıştır:

### Canlı durumu değiştiren doğrulama
Yalnızca proje canlı satır üzerinde gerçek state transition'ı açıkça kabul ettiğinde kullanılır.

Güncel örnek:
- success yolunu `parse_pending` üzerinden tekrar `queued` durumuna bırakılana kadar kanıtlamak

### Yalnızca rollback tabanlı doğrulama
Davranışın canlı satırda kalıcı zarar bırakmadan kanıtlanması gerektiğinde kullanılır.

Güncel örnekler:
- retryable çıkış yolu
- permanent çıkış yolu
- robots-blocked çıkış yolu

---

## Required Evidence

A complete validation package should leave evidence for these categories:

1. pre-deploy drift audit
2. real deploy binding audit
3. runtime and DB sync/apply evidence
4. success-path proof
5. retryable rollback proof
6. permanent rollback proof
7. robots-blocked rollback proof
8. post-sync / post-push / final closure seal

## Gerekli Kanıtlar

Tam bir doğrulama paketi şu kategoriler için kanıt bırakmalıdır:

1. pre-deploy drift audit
2. real deploy binding audit
3. runtime ve DB sync/apply kanıtı
4. success-path kanıtı
5. retryable rollback kanıtı
6. permanent rollback kanıtı
7. robots-blocked rollback kanıtı
8. post-sync / post-push / final closure seal

---

## Controlled Execution Order

### A. Pre-change and drift discovery
Use read-only audits first.

Minimum intent:
- confirm repo truth
- confirm runtime/service binding truth
- detect repo/runtime drift
- detect missing DB function surfaces
- detect stranded `parse_pending` rows if any

### B. Live sync and repair only when justified
Apply runtime sync and SQL surface only when the read-only evidence proves drift or missing live capability.

Minimum intent:
- stop service in controlled manner
- sync runtime code from repo to live runtime
- clean stale runtime bytecode where required
- apply relevant SQL surface
- repair already-stranded `parse_pending` rows only when explicitly justified

### C. Success-path live proof
Prove that success currently lands on transient `parse_pending` and is then released back to `queued`.

Minimum intent:
- controlled one-shot run
- confirm claimed row
- confirm success fetch
- confirm finalize result reaches `parse_pending`
- confirm runtime release result reaches `queued`
- confirm parse-side continuation does not strand frontier state

### D. Retryable rollback proof
Prove inside a rollback-scoped transaction that the retryable boundary reaches `retry_wait` with the expected retryable metadata, while preserving live truth after rollback.

### E. Permanent rollback proof
Prove inside a rollback-scoped transaction that the permanent boundary reaches `dead` with permanent-error metadata, while preserving live truth after rollback.

### F. Robots-blocked rollback proof
Prove inside a rollback-scoped transaction that a robots-blocked decision currently uses the permanent boundary, reaches `dead`, and persists `last_error_class = 'robots_blocked'`, while preserving live truth after rollback.

### G. Documentation seal
After live truth is proven, seal the corresponding lifecycle and worker-contract documentation so the repo explains the exact validated behavior.

### H. Sync and closure seal
Fast-forward Pi51 repo to the sealed commit if needed, then close with read-only final audits on both Ubuntu Desktop and Pi51.

## Kontrollü Uygulama Sırası

### A. Değişiklik öncesi ve drift keşfi
Önce read-only audit'ler kullanılmalıdır.

Asgari amaç:
- repo gerçeğini doğrulamak
- runtime/service binding gerçeğini doğrulamak
- repo/runtime drift tespit etmek
- eksik DB function yüzeylerini tespit etmek
- varsa mahsur kalmış `parse_pending` satırlarını tespit etmek

### B. Yalnızca gerekçelendirilmişse canlı sync ve repair
Runtime sync ve SQL surface yalnızca read-only kanıt drift'i veya eksik canlı kabiliyeti ispat ediyorsa uygulanmalıdır.

Asgari amaç:
- servisi kontrollü biçimde durdurmak
- runtime kodunu repo'dan canlı runtime'a senkronlamak
- gerekiyorsa eski runtime bytecode kalıntılarını temizlemek
- ilgili SQL yüzeyini uygulamak
- yalnızca açıkça gerekçelendirilmişse daha önce mahsur kalmış `parse_pending` satırlarını onarmak

### C. Success-path canlı kanıtı
Success'in şu anda geçici `parse_pending` durumuna indiğini ve ardından tekrar `queued` durumuna bırakıldığını kanıtlamak.

Asgari amaç:
- kontrollü one-shot çalışma
- claim edilen satırı doğrulamak
- başarılı fetch'i doğrulamak
- finalize sonucunun `parse_pending` durumuna ulaştığını doğrulamak
- runtime release sonucunun `queued` durumuna ulaştığını doğrulamak
- parse-tarafı continuation'ın frontier state'i mahsur bırakmadığını doğrulamak

### D. Retryable rollback kanıtı
Rollback kapsamlı transaction içinde, retryable sınırının beklenen retryable metadata ile `retry_wait` durumuna ulaştığını ve rollback sonrası canlı gerçeğin korunduğunu kanıtlamak.

### E. Permanent rollback kanıtı
Rollback kapsamlı transaction içinde, permanent sınırının permanent-error metadata ile `dead` durumuna ulaştığını ve rollback sonrası canlı gerçeğin korunduğunu kanıtlamak.

### F. Robots-blocked rollback kanıtı
Rollback kapsamlı transaction içinde, robots-blocked kararının şu anda permanent sınırı kullandığını, `dead` durumuna ulaştığını ve `last_error_class = 'robots_blocked'` bilgisini kalıcılaştırdığını; rollback sonrası da canlı gerçeğin korunduğunu kanıtlamak.

### G. Dokümantasyon mührü
Canlı gerçek kanıtlandıktan sonra, repo'nun doğrulanmış davranışı açıkça anlatması için ilgili lifecycle ve worker-contract dokümantasyonu mühürlenmelidir.

### H. Sync ve closure mührü
Gerekliyse Pi51 repo mühürlenmiş commit'e fast-forward edilmelidir; ardından Ubuntu Desktop ve Pi51 üzerinde read-only final audit'lerle kapanış yapılmalıdır.

---

## Current Known Validation Chain

As of the currently sealed truth, the controlled validation chain that this runbook generalizes is:

- pre-deploy runtime/service/DB divergence audit
- real deploy binding and runtime drift audit
- runtime+DB sync and stranded parse_pending repair
- one-shot success -> parse_pending -> queued proof
- final live seal for release behavior
- rollback smoke for retryable path
- rollback smoke for permanent path
- rollback smoke for robots-blocked path
- lifecycle/worker contract clarification package
- Ubuntu push + Pi51 fast-forward + dual-side closure seals

This chain is useful as the current reference shape, but future executions must still rely on fresh evidence instead of blindly trusting earlier outputs.

## Güncel Bilinen Doğrulama Zinciri

Şu anda mühürlenmiş gerçeğe göre, bu runbook'un genelleştirdiği kontrollü doğrulama zinciri şudur:

- pre-deploy runtime/service/DB divergence audit
- real deploy binding and runtime drift audit
- runtime+DB sync ve mahsur kalmış parse_pending onarımı
- one-shot success -> parse_pending -> queued kanıtı
- release davranışı için final live seal
- retryable yol için rollback smoke
- permanent yol için rollback smoke
- robots-blocked yol için rollback smoke
- lifecycle/worker contract clarification paketi
- Ubuntu push + Pi51 fast-forward + iki taraflı closure seal'ler

Bu zincir güncel referans şekli olarak faydalıdır; ancak gelecekteki çalıştırmalar yine de eski çıktılara körü körüne güvenmek yerine taze kanıta dayanmalıdır.

---

## Non-goals

This runbook does not:

- redesign crawler-core state machine semantics
- decide parse ranking or outbox business policy
- replace schema-apply validation
- authorize uncontrolled live-row mutation
- authorize broad production experimentation

## Kapsam Dışı Olanlar

Bu runbook şunları yapmaz:

- crawler-core state machine semantiğini yeniden tasarlamaz
- parse ranking veya outbox iş politikasını kararlaştırmaz
- schema-apply validation'ın yerine geçmez
- kontrolsüz canlı satır mutasyonuna izin vermez
- geniş üretim denemelerine izin vermez

---

## Result Expectation

A successful execution of this runbook should leave the project with:

- sealed evidence that all currently implemented exit paths are operationally real
- sealed evidence that rollback proofs do not damage live frontier truth
- sealed documentation that matches the validated runtime behavior
- a clean and synchronized repo state after closure

## Beklenen Sonuç

Bu runbook'un başarılı uygulanması sonunda proje şunlara sahip olmalıdır:

- şu anda uygulanmış tüm exit path'lerin operasyonel olarak gerçek olduğunu gösteren mühürlü kanıt
- rollback kanıtlarının canlı frontier gerçeğine zarar vermediğini gösteren mühürlü kanıt
- doğrulanmış runtime davranışıyla uyumlu mühürlü dokümantasyon
- kapanış sonrası temiz ve senkronize repo durumu
