# 0. Task11 Runtime Cleanup, Boot/Shutdown Decision, and Crawler Core Return Seal

## EN 0.1 Purpose

This document seals the final Task11 cleanup state and records the decision that the project is ready to return to crawler_core work.

Task11 completed the controlled runtime topology cleanup from Ubuntu Desktop to GitHub to pi51c. The live runtime no longer depends on retired top-level wrapper/config/trash surfaces. Runtime sync is now driven by the tracked Python sync dispatcher, and crawler secrets are kept outside Git and outside the live runtime tree.

No crawler run, no DB mutation, and no crawler service start was performed during this seal.

## EN 0.2 Final cleaned runtime state

The following retired surfaces are absent on pi51c:

- `/logisticsearch/bin`
- `/logisticsearch/backups`
- `/logisticsearch/webcrawler`
- `/logisticsearch/makpi51crawler/config`
- `/logisticsearch/makpi51crawler/bin`
- `/logisticsearch/makpi51crawler/lib`
- `/logisticsearch/makpi51crawler/webcrawler`
- `/logisticsearch/makpi51crawler/sql`
- `/logisticsearch/makpi51crawler/crawler_exports`

The live runtime is now expected to contain only the canonical tracked runtime surfaces plus preserved local runtime-only surfaces:

- tracked runtime: `/logisticsearch/makpi51crawler/python_live_runtime`
- tracked catalog: `/logisticsearch/makpi51crawler/catalog`
- tracked taxonomy: `/logisticsearch/makpi51crawler/taxonomy`
- preserved virtual environment: `/logisticsearch/makpi51crawler/.venv`
- secure untracked env file outside live root: `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`

The secure env file contains exactly two connection keys:

- `LOGISTICSEARCH_CRAWLER_DSN`
- `LOGISTICSEARCH_TAXONOMY_DSN`

The DSN values are never printed, never committed, and must not be moved into tracked Python source.

## EN 0.3 Canonical sync command

The old live-only `/logisticsearch/bin/sync` wrapper has been retired.

The canonical direct sync command on pi51c is:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py

Allowed subcommands:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py makpi51crawler

The bare shell command `sync` must continue to resolve to `/usr/bin/sync`.

## EN 0.4 R100 seven-task final seal summary

R100 completed the post-config-delete seven-task final seal.

Results:

1. Retired `/logisticsearch/bin`, `/logisticsearch/backups`, legacy `/logisticsearch/webcrawler`, and live config were absent.
2. Secure user env path was verified: `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`.
3. Ubuntu Desktop, GitHub, pi51c repo, and pi51c live runtime were aligned.
4. Controls under `python_live_runtime/controls` passed AST and read-only audit.
5. The user service was disabled/inactive and referenced the secure env file.
6. The 25 taxonomy JSON files were aligned across Desktop, GitHub, pi51c repo, and live runtime.
7. Trash inventory was clean.
8. Boot/shutdown diagnostics were collected without mutation.

Important R100 measured values:

- secure env mode: `600`
- secure env owner: `makpi51:makpi51`
- secure env key count: `2`
- taxonomy language files: `25`
- taxonomy total records: `8425`
- crawler process count: `0`
- service active state: `inactive`

## EN 0.5 R101B boot/shutdown decision

R101B classified the earlier shutdown delay.

The primary shutdown delay cause was not LogisticSearch runtime. The delay was caused by a stale `session-45.scope` that still contained a lingering `sudo` process. During shutdown, systemd waited for the session scope and eventually killed the stale process after timeout.

Decision summary:

- `SHUTDOWN_DECISION=CONFIRMED_PREVIOUS_DELAY_CAUSE_STALE_SESSION45_LINGERING_SUDO`
- `CURRENT_SUDO_DECISION=NO_CURRENT_SUDO_LEFT_RUNNING`
- `CURRENT_SESSION_DECISION=ACTIVE_SFTP_OR_SSH_SESSIONS_EXIST_CLOSE_CLIENTS_BEFORE_POWERDOWN`
- `FWUPD_DECISION=OPTIONAL_NOISE_TUNING_ONLY_NOT_PRIMARY_SHUTDOWN_CAUSE`
- `CLOUD_INIT_DECISION=OPTIONAL_SCHEMA_AUDIT_OR_DISABLE_LATER_IF_PI_NOT_CLOUD_PROVISIONED`
- `POSTGRESQL_DECISION=KEEP_ENABLED_FOR_CRAWLER_DB_FOR_NOW`
- `APT_SNAPD_DECISION=OPTIONAL_TIMER_POLICY_LATER_ONLY; NOT_A_BLOCKER_FOR_CRAWLER_CORE`
- `LOGISTICSEARCH_RUNTIME_DECISION=NOT_CAUSING_BOOT_SHUTDOWN_DELAY_IN_R100_R101_SCOPE`

Operational note:

Before powering off pi51c, close active SSH/SFTP sessions and ensure there is no lingering sudo process.

## EN 0.6 R102 crawler_core return finding

R102 attempted to run the runtime entrypoint help check from the live runtime in a top-level module context.

Finding:

    ImportError: attempted relative import with no known parent package

Classification:

This is an invocation/context issue, not a proof that crawler_core logic is broken. The file `logisticsearch1_main_entry.py` uses package-relative imports, so it must be invoked with package context.

The next corrected read-only entrypoint check should test package-context invocation, for example:

    PYTHONPATH=/logisticsearch/makpi51crawler \
      /logisticsearch/makpi51crawler/.venv/bin/python \
      -m python_live_runtime.logisticsearch1_main_entry \
      --help

No crawler loop should be started during that read-only correction.

## EN 0.7 Crawler core return decision

The default direction after Task11 is return to crawler_core.

Crawler_core work must continue from strict, small, auditable steps:

1. Correct package-context entrypoint/help audit.
2. Read-only DB connectivity validation using secure env values without printing them.
3. Runtime control state audit without starting the crawler.
4. Startpoint catalog projection audit.
5. Seed/frontier bridge dry-run.
6. Controlled seed/frontier apply only after explicit DB mutation gate.
7. Main while-loop behavior validation with crawler paused unless an explicit run gate is approved.
8. Robots, fetch, parse, taxonomy, and storage routing step-by-step validation.

Every successful step must be written into canonical docs/runbooks/TODO, committed to GitHub, and synchronized to pi51c when appropriate.

## TR 0.1 Amaç

Bu doküman Task11 temizlik durumunu mühürler ve projenin crawler_core çalışmasına dönmeye hazır olduğunu kayda geçirir.

Task11, Ubuntu Desktop → GitHub → pi51c hattındaki runtime topoloji temizliğini kontrollü şekilde tamamladı. Canlı runtime artık emekli edilmiş üst seviye wrapper/config/trash yüzeylerine bağlı değildir. Runtime senkronu tracked Python sync dispatcher ile yürür ve crawler secret değerleri Git dışında, live runtime ağacı dışında tutulur.

Bu mühür sırasında crawler çalıştırılmadı, DB mutation yapılmadı ve crawler service başlatılmadı.

---

## TR 0.2 Nihai temiz runtime durumu

pi51c üzerinde aşağıdaki emekli yüzeyler artık yoktur:

- `/logisticsearch/bin`
- `/logisticsearch/backups`
- `/logisticsearch/webcrawler`
- `/logisticsearch/makpi51crawler/config`
- `/logisticsearch/makpi51crawler/bin`
- `/logisticsearch/makpi51crawler/lib`
- `/logisticsearch/makpi51crawler/webcrawler`
- `/logisticsearch/makpi51crawler/sql`
- `/logisticsearch/makpi51crawler/crawler_exports`

Canlı runtime artık yalnızca canonical tracked runtime yüzeylerini ve korunması gereken local runtime-only yüzeyleri içermelidir:

- tracked runtime: `/logisticsearch/makpi51crawler/python_live_runtime`
- tracked catalog: `/logisticsearch/makpi51crawler/catalog`
- tracked taxonomy: `/logisticsearch/makpi51crawler/taxonomy`
- korunan virtual environment: `/logisticsearch/makpi51crawler/.venv`
- live root dışında secure untracked env dosyası: `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`

Secure env dosyasında yalnızca iki connection key bulunur:

- `LOGISTICSEARCH_CRAWLER_DSN`
- `LOGISTICSEARCH_TAXONOMY_DSN`

DSN değerleri asla yazdırılmaz, asla commit edilmez ve tracked Python source içine taşınmaz.

---

## TR 0.3 Canonical sync komutu

Eski live-only `/logisticsearch/bin/sync` wrapper emekli edilmiştir.

pi51c üzerindeki canonical direct sync komutu şudur:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py

İzinli alt komutlar:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py makpi51crawler

Yalın shell `sync` komutu hâlâ `/usr/bin/sync` olarak kalmalıdır.

---

## TR 0.4 R100 yedi görev final mühür özeti

R100, config silme sonrası yedi görev final mühür kontrolünü tamamladı.

Sonuçlar:

1. Emekli `/logisticsearch/bin`, `/logisticsearch/backups`, legacy `/logisticsearch/webcrawler` ve live config absent doğrulandı.
2. Secure user env path doğrulandı: `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`.
3. Ubuntu Desktop, GitHub, pi51c repo ve pi51c live runtime hizalıydı.
4. `python_live_runtime/controls` altındaki kontroller AST ve read-only audit geçti.
5. User service disabled/inactive durumdaydı ve secure env dosyasını referanslıyordu.
6. 25 taxonomy JSON dosyası Desktop, GitHub, pi51c repo ve live runtime arasında hizalıydı.
7. Trash inventory temizdi.
8. Boot/shutdown diagnostikleri mutation yapmadan toplandı.

Önemli R100 ölçümleri:

- secure env mode: `600`
- secure env owner: `makpi51:makpi51`
- secure env key count: `2`
- taxonomy language files: `25`
- taxonomy total records: `8425`
- crawler process count: `0`
- service active state: `inactive`

---

## TR 0.5 R101B boot/shutdown kararı

R101B önceki kapanış gecikmesini sınıflandırdı.

Ana kapanış gecikmesi LogisticSearch runtime kaynaklı değildi. Gecikmenin sebebi, içinde kapanmamış `sudo` process kalan stale `session-45.scope` idi. Shutdown sırasında systemd bu session scope'u bekledi ve timeout sonrası stale process'i öldürdü.

Karar özeti:

- `SHUTDOWN_DECISION=CONFIRMED_PREVIOUS_DELAY_CAUSE_STALE_SESSION45_LINGERING_SUDO`
- `CURRENT_SUDO_DECISION=NO_CURRENT_SUDO_LEFT_RUNNING`
- `CURRENT_SESSION_DECISION=ACTIVE_SFTP_OR_SSH_SESSIONS_EXIST_CLOSE_CLIENTS_BEFORE_POWERDOWN`
- `FWUPD_DECISION=OPTIONAL_NOISE_TUNING_ONLY_NOT_PRIMARY_SHUTDOWN_CAUSE`
- `CLOUD_INIT_DECISION=OPTIONAL_SCHEMA_AUDIT_OR_DISABLE_LATER_IF_PI_NOT_CLOUD_PROVISIONED`
- `POSTGRESQL_DECISION=KEEP_ENABLED_FOR_CRAWLER_DB_FOR_NOW`
- `APT_SNAPD_DECISION=OPTIONAL_TIMER_POLICY_LATER_ONLY; NOT_A_BLOCKER_FOR_CRAWLER_CORE`
- `LOGISTICSEARCH_RUNTIME_DECISION=NOT_CAUSING_BOOT_SHUTDOWN_DELAY_IN_R100_R101_SCOPE`

Operasyon notu:

pi51c kapatılmadan önce aktif SSH/SFTP oturumları kapatılmalı ve lingering sudo process kalmadığı doğrulanmalıdır.

---

## TR 0.6 R102 crawler_core dönüş bulgusu

R102, live runtime entrypoint help kontrolünü top-level module context içinde çalıştırmayı denedi.

Bulgu:

    ImportError: attempted relative import with no known parent package

Sınıflandırma:

Bu bir invocation/context problemidir; crawler_core mantığının bozuk olduğunu kanıtlamaz. `logisticsearch1_main_entry.py` package-relative import kullandığı için package context ile çağrılmalıdır.

Sıradaki düzeltilmiş read-only entrypoint kontrolü package-context invocation test etmelidir, örneğin:

    PYTHONPATH=/logisticsearch/makpi51crawler \
      /logisticsearch/makpi51crawler/.venv/bin/python \
      -m python_live_runtime.logisticsearch1_main_entry \
      --help

Bu read-only düzeltmede crawler loop başlatılmamalıdır.

---

## TR 0.7 Crawler core dönüş kararı

Task11 sonrası varsayılan yön crawler_core'a dönüştür.

Crawler_core çalışması küçük, sıkı ve audit edilebilir adımlarla devam etmelidir:

1. Package-context entrypoint/help audit düzeltmesi.
2. Secure env değerlerini yazdırmadan read-only DB bağlantı doğrulaması.
3. Crawler başlatmadan runtime control state audit.
4. Startpoint catalog projection audit.
5. Seed/frontier bridge dry-run.
6. Sadece açık DB mutation gate sonrası kontrollü seed/frontier apply.
7. Açık run gate onaylanmadan crawler paused kalacak şekilde main while-loop davranış doğrulaması.
8. Robots, fetch, parse, taxonomy ve storage routing adım adım doğrulaması.

Her başarılı adım canonical docs/runbook/TODO içine yazılmalı, GitHub'a commit edilmeli ve uygun olduğunda pi51c'ye senkronlanmalıdır.
