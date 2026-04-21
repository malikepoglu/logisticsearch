# Pi51 Sync Repo and Runtime Model

## Overview

This document defines the current canonical synchronization model between GitHub, the tracked Pi51 repository checkout, and the live Pi51 webcrawler runtime surface.

This is a model-and-boundary document.

It is not the action runbook.

The paired action-layer document for this surface is:

- `hosts/makpi51crawler/python/webcrawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`

## Genel Bakış

Bu belge; GitHub, Pi51 üzerindeki izlenen repository checkout yüzeyi ve canlı Pi51 webcrawler runtime yüzeyi arasındaki güncel kanonik senkronizasyon modelini tanımlar.

Bu bir model-ve-sınır belgesidir.

Bu belge action runbook değildir.

Bu yüzeyin eşlenik action-layer belgesi şudur:

- `hosts/makpi51crawler/python/webcrawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`

## Documentation hub

- `README.md`
- `docs/README.md`
- `hosts/README.md`
- `hosts/makpi51crawler/README.md`
- `hosts/makpi51crawler/python/README.md`
- `hosts/makpi51crawler/python/webcrawler/README.md`

## Dokümantasyon merkezi

- `README.md`
- `docs/README.md`
- `hosts/README.md`
- `hosts/makpi51crawler/README.md`
- `hosts/makpi51crawler/python/README.md`
- `hosts/makpi51crawler/python/webcrawler/README.md`

## Canonical machine-to-machine flow

The currently relevant code-and-runtime synchronization flow is:

1. Ubuntu Desktop tracked repository working tree  
   `/home/mak/dev/logisticsearch`

2. GitHub canonical repository  
   `git@github.com:malikepoglu/logisticsearch.git`

3. Pi51 tracked repository checkout  
   `/logisticsearch/repo`

4. Pi51 live crawler runtime root  
   `/logisticsearch/webcrawler`

5. Pi51 live runtime Python module surface  
   `/logisticsearch/webcrawler/lib`

## Kanonik makineden makineye akış

Şu anda ilgili olan kod-ve-runtime senkronizasyon akışı şudur:

1. Ubuntu Desktop izlenen repository çalışma ağacı  
   `/home/mak/dev/logisticsearch`

2. GitHub kanonik repository  
   `git@github.com:malikepoglu/logisticsearch.git`

3. Pi51 izlenen repository checkout yüzeyi  
   `/logisticsearch/repo`

4. Pi51 canlı crawler runtime kökü  
   `/logisticsearch/webcrawler`

5. Pi51 canlı runtime Python modül yüzeyi  
   `/logisticsearch/webcrawler/lib`

## What each layer means

### 1. Ubuntu Desktop working tree

This is the main development and authoring surface.

Code, docs, SQL, and tracked operational truth are prepared here before they are pushed to GitHub.

This layer is not covered by the current Pi51 sync commands.

### 2. GitHub repository

GitHub is the canonical shared tracked truth for repository-scoped code and documentation.

Pi51 does not invent new tracked truth in `/logisticsearch/repo`.
It receives tracked truth from GitHub.

### 3. Pi51 tracked repository checkout

`/logisticsearch/repo` is the controlled mirror-like checkout of the GitHub repository on Pi51.

Its job is to match GitHub `main` exactly after controlled sync.

It is not the live execution tree.

It is the tracked source surface on Pi51.

### 4. Pi51 live runtime root

`/logisticsearch/webcrawler` is the live runtime family used by the real crawler runtime.

This surface is intentionally separate from `/logisticsearch/repo`.

That separation is deliberate so repository truth and execution truth do not collapse into one uncontrolled mutable tree.

### 5. Pi51 live runtime Python module surface

`/logisticsearch/webcrawler/lib` is the current live runtime Python module surface.

At the current implementation point, `sync-runtime` populates this surface from the tracked repository Python runtime family.

## Her katman ne anlama gelir

### 1. Ubuntu Desktop çalışma ağacı

Bu ana geliştirme ve yazım yüzeyidir.

Kod, doküman, SQL ve izlenen operasyon doğrusu GitHub’a push edilmeden önce burada hazırlanır.

Bu katman mevcut Pi51 sync komutlarının kapsamı içinde değildir.

### 2. GitHub repository

GitHub, repository-kapsamlı kod ve dokümantasyon için paylaşılan kanonik izlenen doğrudur.

Pi51, `/logisticsearch/repo` içinde yeni tracked truth icat etmez.
Tracked truth’ü GitHub’dan alır.

### 3. Pi51 tracked repository checkout yüzeyi

`/logisticsearch/repo`, GitHub repository’sinin Pi51 üzerindeki kontrollü mirror-benzeri checkout yüzeyidir.

Görevi kontrollü sync sonrasında GitHub `main` ile tam eşleşmektir.

Bu canlı execution ağacı değildir.

Bu Pi51 üzerindeki tracked source yüzeyidir.

### 4. Pi51 canlı runtime kökü

`/logisticsearch/webcrawler`, gerçek crawler runtime tarafından kullanılan canlı runtime ailesidir.

Bu yüzey bilinçli olarak `/logisticsearch/repo`’dan ayrıdır.

Bu ayrım kasıtlıdır; böylece repository doğrusu ile execution doğrusu kontrolsüz biçimde tek mutable ağaç haline gelmez.

### 5. Pi51 canlı runtime Python modül yüzeyi

`/logisticsearch/webcrawler/lib`, güncel canlı runtime Python modül yüzeyidir.

Mevcut implementasyon noktasında `sync-runtime`, bu yüzeyi tracked repository Python runtime ailesinden doldurur.

## Current command model

The current semi-automatic command model on Pi51 is:

- `sync-repo`
- `sync-runtime`

The backward-compatible wrapper also currently exists:

- `/logisticsearch/bin/logisticsearch-sync-live-lib.sh`

## Güncel komut modeli

Pi51 üzerindeki güncel yarı otomatik komut modeli şudur:

- `sync-repo`
- `sync-runtime`

Geriye dönük uyumlu wrapper da şu anda mevcuttur:

- `/logisticsearch/bin/logisticsearch-sync-live-lib.sh`

## What sync-repo does

`sync-repo` is the controlled command for making `/logisticsearch/repo` match GitHub `main`.

Its current responsibilities are:

- verify expected remote URL
- verify current branch
- fetch from origin
- disable sparse-checkout if present
- hard-reset to `origin/main`
- run `git clean`
- verify `HEAD == origin/main`
- verify clean working tree

So the output contract is:

`/logisticsearch/repo` becomes a controlled exact tracked mirror of GitHub `main`.

## sync-repo ne yapar

`sync-repo`, `/logisticsearch/repo` yüzeyini GitHub `main` ile eşitleyen kontrollü komuttur.

Şu anki sorumlulukları şunlardır:

- beklenen remote URL’yi doğrulamak
- güncel branch’i doğrulamak
- origin’den fetch yapmak
- sparse-checkout varsa kapatmak
- `origin/main` üzerine hard-reset yapmak
- `git clean` çalıştırmak
- `HEAD == origin/main` doğrulamak
- çalışma ağacının temiz olduğunu doğrulamak

Dolayısıyla çıktı sözleşmesi şudur:

`/logisticsearch/repo`, GitHub `main`’in kontrollü tam tracked aynası haline gelir.

## What sync-runtime does now

`sync-runtime` is the controlled command for populating the current live runtime Python surface from the tracked repository surface.

Its current scope is intentionally narrow.

At the current implementation point it does all of the following:

- check that `/logisticsearch/repo` is aligned
- verify that the user runtime is quiesced
- remove Python caches before sync
- back up current live Python files
- rsync repository Python runtime files into live runtime `lib/`
- remove caches again after sync
- verify repo/live Python file list equality
- verify repo/live Python hash equality
- run live `py_compile` verification

## sync-runtime şu anda ne yapar

`sync-runtime`, güncel canlı runtime Python yüzeyini tracked repository yüzeyinden dolduran kontrollü komuttur.

Şu anki kapsamı bilinçli olarak dardır.

Mevcut implementasyon noktasında şunların tamamını yapar:

- `/logisticsearch/repo` hizalı mı kontrol eder
- user runtime’ın quiesced olduğunu doğrular
- senkron öncesi Python cache’lerini temizler
- canlı Python dosyalarının yedeğini alır
- repository Python runtime dosyalarını canlı runtime `lib/` içine rsync eder
- senkron sonrası cache’leri tekrar temizler
- repo/live Python dosya listesi eşitliğini doğrular
- repo/live Python hash eşitliğini doğrular
- canlı `py_compile` doğrulaması çalıştırır

## Important current scope boundary

At the current sealed point, `sync-runtime` is not a generic full runtime deploy engine.

It currently synchronizes the Python runtime module family into the live runtime `lib/` surface.

This is deliberate.

If future live runtime components become real and validated — for example additional runtime-side SQL, scripts, templates, config material, or other execution surfaces — the command may later grow in a controlled way.

But that future growth must be documented and revalidated explicitly.

## Önemli güncel kapsam sınırı

Mühürlenmiş güncel noktada `sync-runtime`, genel amaçlı tam runtime deploy motoru değildir.

Şu anda Python runtime modül ailesini canlı runtime `lib/` yüzeyine senkronize eder.

Bu kasıtlıdır.

İleride başka canlı runtime bileşenleri gerçek ve doğrulanmış hale gelirse — örneğin ek runtime-side SQL, script, template, config materyali veya başka execution yüzeyleri — komut daha sonra kontrollü biçimde büyüyebilir.

Ama bu gelecekteki büyüme açık biçimde dokümante edilmeli ve yeniden doğrulanmalıdır.

## Why the model is called semi-automatic

The model is called semi-automatic because the sync steps are automated inside controlled scripts, but the operator still decides when to run them and still verifies the outcome.

So:

- not fully manual
- not uncontrolled full automation
- operator-triggered, script-executed, verification-backed controlled sync

## Model neden yarı otomatik deniyor

Bu modele yarı otomatik denmesinin nedeni, sync adımlarının kontrollü script’ler içinde otomatikleştirilmiş olması; ama operatörün hâlâ ne zaman çalıştıracağına karar vermesi ve sonucu doğrulamasıdır.

Yani:

- tamamen manuel değil
- kontrolsüz tam otomasyon da değil
- operatör tetikli, script yürütmeli, doğrulama destekli kontrollü senkron

## Manual vs semi-automatic vs automatic

### Manual

Manual means the operator performs the file movement logic directly by hand.

Examples:

- direct `cp`
- direct `rsync`
- ad hoc path repair
- hand-written one-off copy sequences

This is acceptable during early exploration, but it is harder to repeat safely.

### Semi-automatic

Semi-automatic means the operator runs a named controlled command, and the command itself performs the repeated logic plus verification.

Examples now:

- `sync-repo`
- `sync-runtime`

This is the current canonical model.

### Fully automatic

Fully automatic would mean the system performs sync actions on its own without an explicit operator decision at run time.

That is **not** the current model.

No scheduled or self-triggered automatic deployment behavior is defined here.

## Manuel vs yarı otomatik vs otomatik

### Manuel

Manuel, dosya taşıma mantığının operatör tarafından doğrudan elle yapılması demektir.

Örnekler:

- doğrudan `cp`
- doğrudan `rsync`
- ad hoc path repair
- elle yazılmış tek seferlik kopyalama zincirleri

Bu erken keşif aşamasında kabul edilebilir; ama güvenli biçimde tekrar etmek daha zordur.

### Yarı otomatik

Yarı otomatik, operatörün isimli kontrollü bir komutu çalıştırması; komutun da tekrarlanan mantığı ve doğrulamayı kendisinin yapması demektir.

Şu anki örnekler:

- `sync-repo`
- `sync-runtime`

Bu güncel kanonik modeldir.

### Tam otomatik

Tam otomatik, sync işlemlerinin çalışma anında operatör açıkça karar vermeden sistem tarafından kendi başına yapılması demektir.

Bu **mevcut model değildir**.

Burada zamanlanmış veya self-triggered otomatik deploy davranışı tanımlı değildir.

## Current operator order

The current operator order on Pi51 is:

1. stop or confirm quiesced runtime
2. run `sync-repo`
3. run `sync-runtime`
4. verify repo truth
5. verify live runtime truth
6. only then continue into runtime tests or controlled execution

## Güncel operatör sırası

Pi51 üzerindeki güncel operatör sırası şudur:

1. runtime’ı durdur veya quiesced olduğunu doğrula
2. `sync-repo` çalıştır
3. `sync-runtime` çalıştır
4. repo doğrusu doğrula
5. canlı runtime doğrusunu doğrula
6. ancak bundan sonra runtime testleri veya kontrollü çalıştırmaya geç

## What this model does not cover

This document does not define:

- Ubuntu Desktop push discipline in detail
- service enable/disable policy in full
- automatic background deployment
- future live runtime growth beyond the currently validated Python `lib/` sync scope
- database content transfer
- removable-media processed-data transfer
- application-layer deploy behavior outside the crawler runtime family

## Bu modelin kapsamadıkları

Bu belge şunları tanımlamaz:

- Ubuntu Desktop push disiplinini ayrıntılı biçimde
- service enable/disable politikasını tam olarak
- otomatik arka plan deploy davranışını
- şu anda doğrulanmış Python `lib/` sync kapsamı dışındaki gelecekteki canlı runtime büyümesini
- veritabanı içerik transferini
- çıkarılabilir medya ile işlenmiş veri transferini
- crawler runtime ailesi dışındaki uygulama-katmanı deploy davranışını

## Current authoritative truth

At the current point:

- `sync-repo` exists on Pi51
- `sync-runtime` exists on Pi51
- controlled backup path exists under `/logisticsearch/backups/live_lib_sync`
- live runtime sync currently verifies repo/live file list equality and hash equality
- live runtime sync currently finishes with `py_compile` verification
- the wrapper `logisticsearch-sync-live-lib.sh` exists for backward compatibility

## Güncel yetkili doğruluk

Şu anki noktada:

- Pi51 üzerinde `sync-repo` vardır
- Pi51 üzerinde `sync-runtime` vardır
- kontrollü backup yolu `/logisticsearch/backups/live_lib_sync` altında vardır
- canlı runtime sync şu anda repo/live dosya listesi eşitliği ve hash eşitliği doğrular
- canlı runtime sync şu anda `py_compile` doğrulaması ile biter
- geri uyumluluk için `logisticsearch-sync-live-lib.sh` wrapper’ı vardır

## Paired runbook

The action-layer runbook for operating this model is:

- `hosts/makpi51crawler/python/webcrawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`

## Eşlenik runbook

Bu modeli işletmek için action-layer runbook şudur:

- `hosts/makpi51crawler/python/webcrawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`
