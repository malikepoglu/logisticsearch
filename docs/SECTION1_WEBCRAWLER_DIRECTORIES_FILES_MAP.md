# Section1: Webcrawler Directories Files Map
# Bölüm1: Webcrawler Dizin Dosya Haritası

## Purpose
## Amaç

This document defines the strict canonical directory and file placement model for the LogisticSearch webcrawler system across Pi51c, GitHub, and Ubuntu Desktop.

Bu belge, LogisticSearch webcrawler sistemi için Pi51c, GitHub ve Ubuntu Desktop boyunca geçerli olacak sıkı kanonik dizin ve dosya yerleşim modelini tanımlar.

## Hard Rules
## Sert Kurallar

1. `/srv/` is a data area only.
2. Runtime code must not live under `/srv/`.
3. `/logisticsearch/` is the canonical root for runtime, controls, config, and repository placement.
4. No `/opt/` surface is introduced for this model.
5. The command set is `playwc`, `stopwc`, `resumewc`, `resetwc`, `poweroffwc`, and `rebootwc`.
6. No separate `pausewc` command exists in the canonical model.
7. `stopwc` is the durable stop command and behaves like a resumable pause.
8. `resetwc` must stop first and then intentionally reset crawler state.
9. The long repository path `/srv/crawler/logisticsearch/repo/` is not the target steady-state repository location.
10. The target canonical repository path is `/logisticsearch/repo/`.
11. The stray `/srv/crawler/logisticsearch/repo/python/` surface is not part of the canonical target model and must be removed during controlled migration.
12. Runtime and data surfaces must not be mixed.

1. `/srv/` yalnızca veri alanıdır.
2. Runtime kodu `/srv/` altında yaşamamalıdır.
3. `/logisticsearch/`, runtime, kontroller, config ve repository yerleşimi için kanonik köktür.
4. Bu model için `/opt/` yüzeyi kullanılmaz.
5. Komut seti `playwc`, `stopwc`, `resumewc`, `resetwc`, `poweroffwc` ve `rebootwc` komutlarından oluşur.
6. Kanonik modelde ayrı bir `pausewc` komutu yoktur.
7. `stopwc`, kalıcı stop komutudur ve resume edilebilir pause gibi davranır.
8. `resetwc`, önce stop etmeli, sonra crawler durumunu bilinçli olarak sıfırlamalıdır.
9. Uzun repository yolu `/srv/crawler/logisticsearch/repo/`, hedef kalıcı repository konumu değildir.
10. Hedef kanonik repository yolu `/logisticsearch/repo/` yoludur.
11. Dağınık `/srv/crawler/logisticsearch/repo/python/` yüzeyi kanonik hedef modelin parçası değildir ve kontrollü migrasyon sırasında kaldırılmalıdır.
12. Runtime ve veri yüzeyleri birbirine karıştırılmamalıdır.

## Canonical Data Surface
## Kanonik Veri Yüzeyi

The canonical data surface is:

    /srv/
    /srv/webcrawler/raw_fetch/
    /srv/data/
    /srv/buffer/
    /srv/webcrawler/exports/

Kanonik veri yüzeyi şudur:

    /srv/
    /srv/webcrawler/raw_fetch/
    /srv/data/
    /srv/buffer/
    /srv/webcrawler/exports/

### Data Placement Rules
### Veri Yerleşim Kuralları

`/srv/webcrawler/raw_fetch/` stores raw fetched page bodies and raw fetch artefacts.
`/srv/data/` stores durable processed output.
`/srv/buffer/` stores temporary or overflow processed output only when explicitly needed by policy.
`/srv/webcrawler/exports/` stores crawler export surfaces.

`/srv/webcrawler/raw_fetch/`, ham çekilmiş sayfa gövdelerini ve ham fetch artefact'larını tutar.
`/srv/data/`, kalıcı işlenmiş çıktıyı tutar.
`/srv/buffer/`, yalnızca politika gereği açıkça gerektiğinde geçici veya taşma işlenmiş çıktıyı tutar.
`/srv/webcrawler/exports/`, crawler export yüzeylerini tutar.

## Canonical Runtime Code Surface
## Kanonik Runtime Kod Yüzeyi

The canonical runtime and code surface is:

    /logisticsearch/webcrawler/
    /logisticsearch/webcrawler/lib/
    /logisticsearch/webcrawler/.venv/

Kanonik runtime ve kod yüzeyi şudur:

    /logisticsearch/webcrawler/
    /logisticsearch/webcrawler/lib/
    /logisticsearch/webcrawler/.venv/

### Runtime Placement Rules
### Runtime Yerleşim Kuralları

`/logisticsearch/webcrawler/` is the runtime root.
`/logisticsearch/webcrawler/lib/` contains the runtime Python implementation.
`/logisticsearch/webcrawler/.venv/` contains the runtime virtual environment.

`/logisticsearch/webcrawler/`, runtime köküdür.
`/logisticsearch/webcrawler/lib/`, runtime Python implementasyonunu içerir.
`/logisticsearch/webcrawler/.venv/`, runtime sanal ortamını içerir.

## Canonical Controls Surface
## Kanonik Kontrol Yüzeyi

The canonical controls surface is:

    /logisticsearch/webcrawler/controls/playwc
    /logisticsearch/webcrawler/controls/stopwc
    /logisticsearch/webcrawler/controls/resumewc
    /logisticsearch/webcrawler/controls/resetwc
    /logisticsearch/webcrawler/controls/poweroffwc
    /logisticsearch/webcrawler/controls/rebootwc

Kanonik kontrol yüzeyi şudur:

    /logisticsearch/webcrawler/controls/playwc
    /logisticsearch/webcrawler/controls/stopwc
    /logisticsearch/webcrawler/controls/resumewc
    /logisticsearch/webcrawler/controls/resetwc
    /logisticsearch/webcrawler/controls/poweroffwc
    /logisticsearch/webcrawler/controls/rebootwc

### Control Semantics
### Kontrol Semantiği

`playwc` starts normal crawler loop execution from an allowed runnable state.
`stopwc` is the canonical durable stop command and behaves like a resumable pause instead of a destructive reset.
`resumewc` resumes from the preserved durable state left by `stopwc`.
`resetwc` performs an intentional stop-first then reset flow.
`poweroffwc` and `rebootwc` are explicit host-level wrappers and must not silently destroy crawler state.
No separate `pausewc` command exists in the canonical model.

`playwc`, izin verilen çalışabilir durumdan normal crawler loop çalıştırmasını başlatır.
`stopwc`, kanonik kalıcı stop komutudur ve yıkıcı reset yerine resume edilebilir pause gibi davranır.
`resumewc`, `stopwc` tarafından bırakılan korunmuş kalıcı durumdan devam eder.
`resetwc`, bilinçli bir önce-stop-sonra-reset akışı uygular.
`poweroffwc` ve `rebootwc`, açık host-seviyesi sarmalayıcılardır ve crawler durumunu sessizce yok etmemelidir.
Kanonik modelde ayrı bir `pausewc` komutu yoktur.

## Canonical Config Surface
## Kanonik Config Yüzeyi

The canonical config file is:

    /logisticsearch/webcrawler/config/webcrawler.env

Kanonik config dosyası şudur:

    /logisticsearch/webcrawler/config/webcrawler.env

### Config Rule
### Config Kuralı

The crawler runtime must read its environment configuration from this canonical config surface.

Crawler runtime, environment konfigürasyonunu bu kanonik config yüzeyinden okumalıdır.

## Canonical Repository Surface
## Kanonik Repository Yüzeyi

The canonical repository root is:

    /logisticsearch/repo/

Kanonik repository kökü şudur:

    /logisticsearch/repo/

### Repository Rule
### Repository Kuralı

The content currently living under `/srv/crawler/logisticsearch/repo/` is intended to move into `/logisticsearch/repo/` in a controlled migration.
Git synchronization should then operate against `/logisticsearch/repo/`.
The old long path is not the target steady-state repository location.

Şu anda `/srv/crawler/logisticsearch/repo/` altında yaşayan içerik, kontrollü migrasyonla `/logisticsearch/repo/` altına taşınmak üzere hedeflenmiştir.
Git senkronizasyonu daha sonra `/logisticsearch/repo/` üzerinden çalışmalıdır.
Eski uzun yol, hedef kalıcı repository konumu değildir.

## Explicit Non Canonical Surfaces
## Açık Kanonik Dışı Yüzeyler

The following are not canonical target surfaces for the agreed model:

* runtime code under `/srv/`
* a separate `pausewc` wrapper
* an `/opt/` placement for this crawler model
* keeping the repository root as `/srv/crawler/logisticsearch/repo/`
* keeping a stray repository-side Python surface at `/srv/crawler/logisticsearch/repo/python/`

Aşağıdakiler, üzerinde anlaşılan model için kanonik hedef yüzeyler değildir:

* `/srv/` altında runtime kodu
* ayrı bir `pausewc` sarmalayıcısı
* bu crawler modeli için `/opt/` yerleşimi
* repository kökünü `/srv/crawler/logisticsearch/repo/` olarak tutmak
* `/srv/crawler/logisticsearch/repo/python/` yolundaki dağınık repository-yanı Python yüzeyini korumak

## Migration Direction Rule
## Migrasyon Yönü Kuralı

The migration direction is strict:

1. document the target layout
2. align repository location
3. align runtime code location
4. align controls and config location
5. align data paths under `/srv/`
6. remove retired or stray legacy surfaces only after the new canonical surface is ready

Migrasyon yönü sıkıdır:

1. hedef yerleşimi dokümante et
2. repository konumunu hizala
3. runtime kod konumunu hizala
4. controls ve config konumunu hizala
5. `/srv/` altındaki veri yollarını hizala
6. yeni kanonik yüzey hazır olduktan sonra emekli veya dağınık legacy yüzeyleri kaldır

## Current Decision Status
## Güncel Karar Durumu

This document records the agreed target layout as the canonical direction for Pi51c, GitHub, and Ubuntu Desktop coordination.

Bu belge, Pi51c, GitHub ve Ubuntu Desktop koordinasyonu için üzerinde anlaşılmış hedef yerleşimi kanonik yön olarak kaydeder.
