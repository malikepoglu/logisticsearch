# Runbook: Sync Pi51 Repo and Live Runtime

<!-- TASK11_SYNC_COMMAND_LAYER_ANTI_DRIFT_BEGIN -->
## Current sync command layer and anti-drift rule

EN:
The current canonical synchronization direction is:

    Ubuntu Desktop /home/mak/dev/logisticsearch
      -> GitHub origin/main
      -> pi51c /logisticsearch/repo
      -> pi51c /logisticsearch/makpi51crawler

Ubuntu Desktop is the guide workspace. Do not invert this direction when deciding repository truth.

The current explicit pi51c sync command layer is:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo --help
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime --help
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py makpi51crawler --help

The project wrapper lives at /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py, but bare sync must still resolve to /usr/bin/sync unless a separate PATH policy is explicitly approved later.

The project wrapper delegates to the live tracked dispatcher:

    /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py

Unknown, empty, or coreutils-style calls are passed through by the Python dispatcher to /usr/bin/sync.

Side-effect controls are not part of sync smoke tests. Fan, Wi-Fi, play, pause, poweroff, reboot, reset, systemd mutation, DB mutation, crawler execution, and cleanup require separate small runbooks before live execution.

Cleanup is still blocked. Do not delete legacy /logisticsearch/webcrawler, legacy legacy live-only sync-repo wrapper, legacy legacy live-only sync-runtime wrapper, or backups from this sync-command line.

TR:
Güncel kanonik senkronizasyon yönü şudur:

    Ubuntu Desktop /home/mak/dev/logisticsearch
      -> GitHub origin/main
      -> pi51c /logisticsearch/repo
      -> pi51c /logisticsearch/makpi51crawler

Ubuntu Desktop kılavuz çalışma alanıdır. Repository doğrusu belirlenirken bu yön tersine çevrilmemelidir.

Güncel açık pi51c sync komut katmanı şudur:

    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo --help
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime --help
    /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py makpi51crawler --help

Proje wrapper dosyası /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py konumundadır; fakat ayrı bir PATH politikası açıkça onaylanmadıkça yalın sync komutu hâlâ /usr/bin/sync olarak kalmalıdır.

Proje wrapper'ı canlı tracked dispatcher'a delege eder:

    /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py

Bilinmeyen, boş veya coreutils tarzı çağrılar Python dispatcher tarafından /usr/bin/sync komutuna aktarılır.

Yan etkili kontroller sync smoke testlerinin parçası değildir. Fan, Wi-Fi, play, pause, poweroff, reboot, reset, systemd mutation, DB mutation, crawler çalıştırma ve cleanup işlemleri canlı çalıştırılmadan önce ayrı küçük runbook ister.

Cleanup hâlâ blokludur. Bu sync-command hattından legacy /logisticsearch/webcrawler, legacy legacy live-only sync-repo wrapper, legacy legacy live-only sync-runtime wrapper veya backup dosyaları silinmemelidir.
<!-- TASK11_SYNC_COMMAND_LAYER_ANTI_DRIFT_END -->



## What this runbook is

This runbook gives the single controlled operator path for synchronizing:

1. GitHub tracked repository truth into the Pi51 tracked repository checkout
2. the Pi51 tracked repository Python runtime surface into the Pi51 live crawler runtime surface

This is the action-layer companion to:

- `docs/TOPIC_PI51_SYNC_REPO_AND_RUNTIME_MODEL.md`

## Bu runbook nedir

Bu runbook şu iki senkronizasyon için tek kontrollü operatör yolunu verir:

1. GitHub tracked repository doğrusunu Pi51 tracked repository checkout yüzeyine taşımak
2. Pi51 tracked repository Python runtime yüzeyini Pi51 canlı crawler runtime yüzeyine taşımak

Bu belge şu dokümanın action-layer eşidir:

- `docs/TOPIC_PI51_SYNC_REPO_AND_RUNTIME_MODEL.md`

## Current operational boundary

This runbook currently covers only:

- `sync-repo` on Pi51
- `sync-runtime` on Pi51
- the current Python `python_live_runtime/` live-runtime sync surface
- the current verification chain for that Python surface

It does not cover Ubuntu Desktop to GitHub push discipline.
It does not cover future broader runtime families yet.

## Güncel operasyon sınırı

Bu runbook şu anda yalnızca şunları kapsar:

- Pi51 üzerindeki `sync-repo`
- Pi51 üzerindeki `sync-runtime`
- güncel Python `python_live_runtime/` canlı-runtime sync yüzeyi
- bu Python yüzeyi için güncel doğrulama zinciri

Ubuntu Desktop -> GitHub push disiplinini kapsamaz.
Gelecekteki daha geniş runtime ailelerini henüz kapsamaz.

## Execution target / machine context

- machine: `pi51c`
- tracked repository root: `/logisticsearch/repo`
- live runtime root: `/logisticsearch/makpi51crawler`
- live runtime Python surface: `/logisticsearch/makpi51crawler/python_live_runtime`
- live runtime environment file: `/logisticsearch/makpi51crawler/config/webcrawler.env`
- sync commands:
  - `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo`
  - `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime`

## Yürütme hedefi / makine bağlamı

- makine: `pi51c`
- tracked repository kökü: `/logisticsearch/repo`
- canlı runtime kökü: `/logisticsearch/makpi51crawler`
- canlı runtime Python yüzeyi: `/logisticsearch/makpi51crawler/python_live_runtime`
- canlı runtime environment dosyası: `/logisticsearch/makpi51crawler/config/webcrawler.env`
- sync komutları:
  - `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo`
  - `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime`

## Preconditions

Before running this runbook, confirm all of the following:

1. you are on `pi51c`
2. `/logisticsearch/repo` exists and is a Git checkout
3. `/logisticsearch/makpi51crawler/.venv/bin/python` exists
4. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py` exists
5. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo --help` and `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime --help` pass
6. the crawler runtime is quiesced
7. you understand that `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo` can discard local repo drift under `/logisticsearch/repo`
8. you understand that `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime` updates the live Python runtime surface from tracked repository truth

## Önkoşullar

Bu runbook çalıştırılmadan önce şunları doğrula:

1. `pi51c` üzerindesin
2. `/logisticsearch/repo` mevcut ve bir Git checkout yüzeyi
3. `/logisticsearch/makpi51crawler/.venv/bin/python` mevcut
4. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py` mevcut
5. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo --help` ve `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime --help` geçer
6. crawler runtime quiesced durumda
7. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo` komutunun `/logisticsearch/repo` altındaki drift içeriği silebileceğini anlıyorsun
8. `/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime` komutunun canlı Python runtime yüzeyini tracked repository doğrusundan güncellediğini anlıyorsun

## Step-by-step operator path

### Step 1 — verify command presence

```bash
# Makine: pi51c
cd /home/makpi51 && /usr/bin/env bash <<'BASH'
set -Eeuo pipefail

ls -l /logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py
ls -l /logisticsearch/makpi51crawler/.venv/bin/python
/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo --help >/dev/null
/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime --help >/dev/null
BASH
```

### Step 2 — verify runtime is quiesced

```bash
# Makine: pi51c
cd /home/makpi51 && /usr/bin/env bash <<'BASH'
set -Eeuo pipefail

systemctl --user status logisticsearch-webcrawler.service --no-pager || true
pgrep -af '/logisticsearch/makpi51crawler' || true
BASH
```

### Step 3 — sync tracked repo from GitHub into Pi51 repo checkout

```bash
# Makine: pi51c
cd /home/makpi51 && /usr/bin/env bash <<'BASH'
set -Eeuo pipefail

/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py repo
BASH
```

### Step 4 — sync tracked Python runtime surface into live runtime

```bash
# Makine: pi51c
cd /home/makpi51 && /usr/bin/env bash <<'BASH'
set -Eeuo pipefail

/logisticsearch/makpi51crawler/.venv/bin/python /logisticsearch/makpi51crawler/python_live_runtime/controls/sync_data/sync.py runtime
BASH
```

### Step 5 — independent post-sync verification

```bash
# Makine: pi51c
cd /home/makpi51 && /usr/bin/env bash <<'BASH'
set -Eeuo pipefail

git -C /logisticsearch/repo rev-parse HEAD
git -C /logisticsearch/repo rev-parse origin/main
git -C /logisticsearch/repo status -sb

find /logisticsearch/repo/makpi51crawler/python_live_runtime -type f -name '*.py' | LC_ALL=C sort | sed 's#^/logisticsearch/repo/makpi51crawler/python_live_runtime/##' > /tmp/pi51_repo_py_rel.txt
find /logisticsearch/makpi51crawler/python_live_runtime -type f -name '*.py' | LC_ALL=C sort | sed 's#^/logisticsearch/makpi51crawler/python_live_runtime/##' > /tmp/pi51_live_py_rel.txt

diff -u /tmp/pi51_repo_py_rel.txt /tmp/pi51_live_py_rel.txt
/logisticsearch/makpi51crawler/.venv/bin/python -m py_compile $(find /logisticsearch/makpi51crawler/python_live_runtime -type f -name '*.py' | LC_ALL=C sort)
BASH
```

## Success criteria

- `/logisticsearch/repo` is aligned with GitHub `main`
- `/logisticsearch/makpi51crawler/python_live_runtime` reflects the tracked repository Python runtime surface
- relative repo/live Python file lists match
- live `py_compile` passes
- runtime remains quiesced unless intentionally started later

## Başarı ölçütleri

- `/logisticsearch/repo`, GitHub `main` ile hizalıdır
- `/logisticsearch/makpi51crawler/python_live_runtime`, tracked repository Python runtime yüzeyini yansıtır
- relative repo/live Python dosya listeleri eşleşir
- canlı `py_compile` geçer
- daha sonra bilinçli olarak başlatılmadıkça runtime quiesced durumda kalır

## Stop conditions

Stop immediately if any of the following occur:

- `sync-repo` fails
- `sync-runtime` fails
- repo `HEAD` does not equal `origin/main`
- relative file-list equality fails
- live `py_compile` fails
- runtime is not quiesced when this runbook requires quiesced execution

## Durma koşulları

Aşağıdakilerden biri olursa hemen dur:

- `sync-repo` başarısız olursa
- `sync-runtime` başarısız olursa
- repo `HEAD`, `origin/main` ile eşit değilse
- relative dosya listesi eşitliği bozulursa
- canlı `py_compile` başarısız olursa
- bu runbook quiesced çalışma gerektirirken runtime quiesced değilse

## Scope boundary

This runbook does not cover:

- Ubuntu Desktop -> GitHub push discipline
- future broader runtime asset families beyond the current Python `lib/` surface
- service start / restart actions
- database schema apply or validation work

## Kapsam sınırı

Bu runbook şunları kapsamaz:

- Ubuntu Desktop -> GitHub push disiplini
- mevcut Python `lib/` yüzeyinin ötesindeki gelecekteki daha geniş runtime asset aileleri
- service start / restart aksiyonları
- veritabanı şema apply veya validation işleri
