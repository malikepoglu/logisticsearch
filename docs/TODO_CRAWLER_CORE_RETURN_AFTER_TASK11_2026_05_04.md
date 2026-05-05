# TODO - Crawler Core Return After Task11

Status: ACTIVE TODO  
Created: 2026-05-05  
Canonical basis: Task11 R100/R101B/R102  
Current canonical head before this TODO seal: `c178afbd26492a98d3007f0df24a88d129b93201`

---

## 1. EN - Non-negotiable operating rules

1. Start every step from Ubuntu Desktop canonical repo: `/home/mak/dev/logisticsearch`.
2. Verify local `main`, `origin/main`, and GitHub remote head before mutation.
3. Use one narrow command block per step.
4. Print PASS/FAIL evidence.
5. Never print DSN/password/token/secret values.
6. Do not move DSN values into tracked Python.
7. Do not recreate retired surfaces:
   - retired top-level wrapper directory
   - retired backup directory
   - retired legacy runtime root
   - retired live config directory
8. Do not start crawler unless the step explicitly says crawler start/run is allowed.
9. Do not mutate DB unless the step explicitly says DB mutation is allowed.
10. After every successful tracked change: commit, push, then sync pi51c repo/live if relevant.
11. Update canonical docs/runbook/TODO after every sealed successful phase.

## 2. TR - Vazgeçilmez operasyon kuralları

1. Her adım Ubuntu Desktop canonical repo üzerinden başlar: `/home/mak/dev/logisticsearch`.
2. Mutation öncesi local `main`, `origin/main` ve GitHub remote head doğrulanır.
3. Her adım tek ve dar kapsamlı komut bloğu ile yapılır.
4. PASS/FAIL kanıtı yazdırılır.
5. DSN/password/token/secret değerleri asla yazdırılmaz.
6. DSN değerleri tracked Python içine taşınmaz.
7. Emekli yüzeyler yeniden oluşturulmaz:
   - emekli top-level wrapper dizini
   - emekli backup dizini
   - emekli legacy runtime root
   - emekli live config dizini
8. Adım açıkça crawler start/run izni vermedikçe crawler başlatılmaz.
9. Adım açıkça DB mutation izni vermedikçe DB mutation yapılmaz.
10. Her başarılı tracked değişiklikten sonra commit, push, sonra gerekirse pi51c repo/live sync yapılır.
11. Her mühürlenmiş başarılı fazdan sonra canonical docs/runbook/TODO güncellenir.

---

## 3. EN - Immediate next steps

### R102B - Corrected package-context entrypoint baseline, read-only

Goal:

- Re-run the crawler_core return baseline without the top-level module invocation bug.
- Use package-context invocation.
- Confirm help works without starting crawler.

Expected safe invocation shape:

    PYTHONPATH=/logisticsearch/makpi51crawler \
      /logisticsearch/makpi51crawler/.venv/bin/python \
      -m python_live_runtime.logisticsearch1_main_entry \
      --help

Forbidden:

- crawler start
- DB mutation
- service start/restart
- printing DSN values

### R102C - Secure env and DB connectivity audit, read-only

Goal:

- Confirm secure env file exists at `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`.
- Confirm it has the two expected key names.
- Source/use values without printing them.
- Test crawler DB and taxonomy DB with read-only transaction only.

Forbidden:

- writing to DB
- schema changes
- printing DSN values
- starting crawler

### R102D - Runtime control state audit, read-only

Goal:

- Inspect control files under `python_live_runtime/controls`.
- Verify pause/play/reset/poweroff/reboot command contracts without invoking side effects.
- Confirm default runtime control state before any crawler loop test.

Forbidden:

- side-effect controls
- systemd mutation
- crawler run

### R102E - Startpoint catalog projection audit, read-only

Goal:

- Load English startpoint catalog.
- Confirm current projection count remains 27 source families and 43 seed URLs.
- Verify no accidental mutation.

### R102F - Seed/frontier bridge dry-run

Goal:

- Exercise seed/frontier bridge logic in dry-run or rollback-only mode.
- Confirm which rows would be written before any actual DB mutation.

### R102G - Controlled seed/frontier apply gate

Goal:

- Only after R102F passes, perform explicit DB mutation gate for seed/frontier.
- Must include backup/snapshot strategy and rollback path.

### R102H - Main while-loop readiness audit

Goal:

- Audit main loop behavior without running infinite crawl.
- Confirm pause/stop/durable claim/lease behavior.
- Prepare a tiny one-iteration test only after explicit approval.

---

## 4. TR - Sıradaki acil adımlar

### R102B - Düzeltilmiş package-context entrypoint baseline, read-only

Amaç:

- Top-level module invocation hatasına düşmeden crawler_core return baseline tekrar almak.
- Package-context invocation kullanmak.
- Crawler başlatmadan help çıktısının çalıştığını doğrulamak.

Beklenen güvenli invocation şekli:

    PYTHONPATH=/logisticsearch/makpi51crawler \
      /logisticsearch/makpi51crawler/.venv/bin/python \
      -m python_live_runtime.logisticsearch1_main_entry \
      --help

Yasak:

- crawler start
- DB mutation
- service start/restart
- DSN değerlerini yazdırmak

### R102C - Secure env ve DB bağlantı audit, read-only

Amaç:

- Secure env dosyasının `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env` konumunda olduğunu doğrulamak.
- İçinde beklenen iki key adının olduğunu doğrulamak.
- Değerleri yazdırmadan source/use etmek.
- Crawler DB ve taxonomy DB bağlantısını sadece read-only transaction ile test etmek.

Yasak:

- DB yazma
- schema değişikliği
- DSN değerlerini yazdırma
- crawler başlatma

### R102D - Runtime control state audit, read-only

Amaç:

- `python_live_runtime/controls` altındaki kontrol dosyalarını incelemek.
- pause/play/reset/poweroff/reboot command contractlarını yan etki oluşturmadan doğrulamak.
- Herhangi bir crawler loop testinden önce default runtime control state durumunu doğrulamak.

Yasak:

- side-effect controls
- systemd mutation
- crawler run

### R102E - Startpoint catalog projection audit, read-only

Amaç:

- English startpoint catalog dosyasını yüklemek.
- Projection sayısının 27 source family ve 43 seed URL olarak kaldığını doğrulamak.
- Kazara mutation olmadığını doğrulamak.

### R102F - Seed/frontier bridge dry-run

Amaç:

- Seed/frontier bridge mantığını dry-run veya rollback-only modda çalıştırmak.
- Gerçek DB mutation öncesi hangi row'ların yazılacağını doğrulamak.

### R102G - Kontrollü seed/frontier apply gate

Amaç:

- Sadece R102F geçtikten sonra seed/frontier için açık DB mutation gate yapmak.
- Backup/snapshot stratejisi ve rollback yolu içermek zorundadır.

### R102H - Main while-loop readiness audit

Amaç:

- Main loop davranışını infinite crawl başlatmadan audit etmek.
- pause/stop/durable claim/lease davranışını doğrulamak.
- Sadece açık onaydan sonra tiny one-iteration test hazırlamak.

---

## 5. EN - New chat copy block

~~~text
We are continuing LogisticSearch crawler_core work after Task11 cleanup.

Canonical repo:
- GitHub: https://github.com/malikepoglu/logisticsearch
- Ubuntu Desktop repo: /home/mak/dev/logisticsearch
- pi51c repo mirror: /logisticsearch/repo
- pi51c live runtime: /logisticsearch/makpi51crawler

Current sealed state:
- Canonical head after Task11 config migration: c178afbd26492a98d3007f0df24a88d129b93201
- /logisticsearch/bin is absent.
- /logisticsearch/backups is absent.
- legacy /logisticsearch/webcrawler is absent.
- /logisticsearch/makpi51crawler/config is absent.
- Secure user-env file is: /home/makpi51/.config/logisticsearch/secrets/webcrawler.env
- Secure env contains LOGISTICSEARCH_CRAWLER_DSN and LOGISTICSEARCH_TAXONOMY_DSN; values must never be printed or committed.
- Direct sync command on pi51c is:
  /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py
- Crawler service is disabled/inactive.
- Crawler has not been started during Task11 cleanup.
- DB mutation was not performed during Task11 cleanup.

Boot/shutdown decision:
- Previous slow shutdown was caused by stale session-45.scope with a lingering sudo process, not LogisticSearch runtime.
- Current policy: close active SSH/SFTP sessions and ensure no sudo process remains before poweroff.
- fwupd/cloud-init/apt/snapd are optional OS tuning topics, not crawler_core blockers.
- PostgreSQL stays enabled for crawler DB for now.

R102 finding:
- Top-level python -m logisticsearch1_main_entry failed with relative import context error.
- Next corrected check should use package context:
  PYTHONPATH=/logisticsearch/makpi51crawler /logisticsearch/makpi51crawler/.venv/bin/python -m python_live_runtime.logisticsearch1_main_entry --help

Next work:
- Start with R102B corrected package-context entrypoint/help audit, read-only.
- Then secure env + DB read-only connectivity audit.
- Then runtime control state audit.
- Then startpoint catalog projection audit.
- Then seed/frontier bridge dry-run.
- Only after strict gates, move toward controlled seed/frontier apply and main while-loop crawling.
- Every successful step must be documented, committed to GitHub, and synced to pi51c where appropriate.
~~~

## 6. TR - Yeni sohbet copy block

~~~text
LogisticSearch crawler_core çalışmasına Task11 cleanup sonrası devam ediyoruz.

Canonical repo:
- GitHub: https://github.com/malikepoglu/logisticsearch
- Ubuntu Desktop repo: /home/mak/dev/logisticsearch
- pi51c repo mirror: /logisticsearch/repo
- pi51c live runtime: /logisticsearch/makpi51crawler

Mühürlenmiş mevcut durum:
- Task11 config migration sonrası canonical head: c178afbd26492a98d3007f0df24a88d129b93201
- /logisticsearch/bin yok.
- /logisticsearch/backups yok.
- legacy /logisticsearch/webcrawler yok.
- /logisticsearch/makpi51crawler/config yok.
- Secure user-env dosyası: /home/makpi51/.config/logisticsearch/secrets/webcrawler.env
- Secure env içinde LOGISTICSEARCH_CRAWLER_DSN ve LOGISTICSEARCH_TAXONOMY_DSN var; değerleri asla yazdırılmamalı ve commit edilmemeli.
- pi51c direct sync komutu:
  /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py
- Crawler service disabled/inactive.
- Task11 cleanup sırasında crawler başlatılmadı.
- Task11 cleanup sırasında DB mutation yapılmadı.

Boot/shutdown kararı:
- Önceki yavaş kapanışın sebebi LogisticSearch runtime değil; session-45.scope içinde kalmış lingering sudo process idi.
- Güncel politika: poweroff öncesi aktif SSH/SFTP oturumlarını kapat ve sudo process kalmadığını doğrula.
- fwupd/cloud-init/apt/snapd opsiyonel OS tuning konularıdır, crawler_core blocker değildir.
- PostgreSQL crawler DB için şimdilik enabled kalacak.

R102 bulgusu:
- Top-level python -m logisticsearch1_main_entry relative import context hatası verdi.
- Sıradaki düzeltilmiş kontrol package context ile yapılmalı:
  PYTHONPATH=/logisticsearch/makpi51crawler /logisticsearch/makpi51crawler/.venv/bin/python -m python_live_runtime.logisticsearch1_main_entry --help

Sıradaki iş:
- R102B corrected package-context entrypoint/help audit ile read-only başla.
- Sonra secure env + DB read-only connectivity audit.
- Sonra runtime control state audit.
- Sonra startpoint catalog projection audit.
- Sonra seed/frontier bridge dry-run.
- Sadece strict gate sonrası kontrollü seed/frontier apply ve main while-loop crawling aşamasına geç.
- Her başarılı adım dokümante edilmeli, GitHub'a commit edilmeli ve uygun olduğunda pi51c'ye sync edilmeli.
~~~

## R104B EntryPoint Invocation Contract Link

- Contract doc: `docs/TOPIC_CRAWLER_CORE_ENTRYPOINT_INVOCATION_CONTRACT_2026_05_05.md`
- Status: created locally after R103B; commit/push/sync still pending.
- Safety boundary: no crawler start, no DB mutation, no systemd mutation, no pi51c sync under STEP1/STEP2.
- Next gate after local validation: commit/push only after dirty scope and secret guards pass.

## R106/R106B Service Invocation Patch Seal

- R106 patched the pi51c user service invocation from top-level corridor to package-context corridor.
- Correct service contract: `PYTHONPATH=/logisticsearch/makpi51crawler` and `-m python_live_runtime.logisticsearch1_main_entry`.
- R106B read-only final seal passed: service remained inactive/disabled, crawler process count stayed 0, help smoke passed, no DB mutation occurred.
- Documentation file: `docs/TOPIC_CRAWLER_CORE_SYSTEMD_SERVICE_INVOCATION_PATCH_SEAL_2026_05_05.md`.
- Next safe technical path: controls safety review, then main-loop state-machine read-only trace.
