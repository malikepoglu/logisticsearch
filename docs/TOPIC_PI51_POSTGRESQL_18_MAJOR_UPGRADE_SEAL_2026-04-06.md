# Pi51 PostgreSQL 18 Major Upgrade Seal - 2026-04-06

## Overview

This document records the sealed final state of the Pi51 PostgreSQL major-version upgrade from PostgreSQL 16 to PostgreSQL 18.

The upgrade was completed in a controlled manner on Pi51 and then final-audited from Ubuntu Desktop.

## Genel Bakış

Bu belge, Pi51 üzerinde PostgreSQL 16'dan PostgreSQL 18'e yapılan major sürüm yükseltmesinin mühürlü nihai durumunu kayda geçirir.

Yükseltme Pi51 üzerinde kontrollü şekilde tamamlanmış, ardından Ubuntu Desktop üzerinden final audit ile doğrulanmıştır.

## Sealed final state

At the sealed point:

- only `18/main` remains registered
- active PostgreSQL port is `5432`
- live cluster state is `online`
- active data directory is `/srv/postgresql/18/main`
- canonical cluster log target is `/var/log/postgresql/postgresql-18-main.log`

## Mühürlü nihai durum

Mühürlü noktada:

- yalnızca `18/main` kayıtlıdır
- aktif PostgreSQL portu `5432`'dir
- canlı cluster durumu `online`'dır
- aktif data directory `/srv/postgresql/18/main` yoludur
- kanonik cluster log hedefi `/var/log/postgresql/postgresql-18-main.log` yoludur

## Upgrade path summary

The upgrade path that was completed was:

1. audit current PG16 reality
2. onboard PGDG source on Pi51
3. install PostgreSQL 18 and PostgreSQL 18 PostGIS packages without auto-cluster creation
4. prepare controlled pre-upgrade backup/export package
5. run controlled `pg_upgradecluster` upgrade from `16/main` to `18/main`
6. verify live database state on PostgreSQL 18
7. remove old PostgreSQL 16 runtime traces and packages
8. normalize the PostgreSQL 18 cluster log target
9. run final seal audit

## Yükseltme yolu özeti

Tamamlanan yükseltme yolu şuydu:

1. mevcut PG16 gerçekliğini denetle
2. Pi51 üzerinde PGDG kaynağını onboard et
3. otomatik cluster oluşturmadan PostgreSQL 18 ve PostgreSQL 18 PostGIS paketlerini kur
4. kontrollü pre-upgrade backup/export paketi hazırla
5. `16/main` → `18/main` kontrollü `pg_upgradecluster` yükseltmesini çalıştır
6. PostgreSQL 18 üzerindeki canlı veritabanı durumunu doğrula
7. eski PostgreSQL 16 runtime izlerini ve paketlerini kaldır
8. PostgreSQL 18 cluster log hedefini normalize et
9. final seal audit çalıştır

## Final verified runtime facts

Verified final facts:

- cluster surface: `18/main` only
- service: `postgresql@18-main = active`
- loopback listener: `127.0.0.1:5432`
- live server version: `PostgreSQL 18.3`
- crawler database reachable: `logisticsearch_crawler`
- old PG16 package family absent
- old PG16 path family absent
- old PG16 mount/fstab trace absent

## Nihai doğrulanmış çalışma gerçekleri

Doğrulanan nihai gerçekler:

- cluster yüzeyi: yalnızca `18/main`
- servis: `postgresql@18-main = active`
- loopback listener: `127.0.0.1:5432`
- canlı sunucu sürümü: `PostgreSQL 18.3`
- crawler veritabanı erişilebilir: `logisticsearch_crawler`
- eski PG16 paket ailesi yok
- eski PG16 path ailesi yok
- eski PG16 mount/fstab izi yok

## Extension state after upgrade

Verified extension state:

### logisticsearch_crawler
- `pgcrypto = 1.4`
- `postgis = 3.6.2`

### logisticsearch_geo
- `pgcrypto = 1.4`
- `postgis = 3.6.2`

### logisticsearch_taxonomy
- `pgcrypto = 1.4`

## Yükseltme sonrası extension durumu

Doğrulanan extension durumu:

### logisticsearch_crawler
- `pgcrypto = 1.4`
- `postgis = 3.6.2`

### logisticsearch_geo
- `pgcrypto = 1.4`
- `postgis = 3.6.2`

### logisticsearch_taxonomy
- `pgcrypto = 1.4`

## Safety / discipline notes

Important safety facts:

- the upgrade was not treated as a blind in-place mutation
- pre-upgrade backup/export artifacts were created first
- controlled read-only audits were run before and after mutation
- PG16 was only removed after PG18 runtime health was verified
- final seal audit passed after cleanup and log normalization

## Güvenlik / disiplin notları

Önemli güvenlik gerçekleri:

- yükseltme kör bir in-place mutasyon olarak ele alınmadı
- pre-upgrade backup/export artefact'ları önce oluşturuldu
- mutasyon öncesi ve sonrası kontrollü salt-okunur denetimler çalıştırıldı
- PG16 ancak PG18 runtime sağlığı doğrulandıktan sonra kaldırıldı
- cleanup ve log normalization sonrasında final seal audit başarıyla geçti

## Operational conclusion

Pi51 should now be treated as PostgreSQL-18-based operational truth for the crawler node.

Future PostgreSQL work on Pi51 should start from this assumption and should not refer back to PostgreSQL 16 as live runtime reality.

## Operasyonel sonuç

Pi51 artık crawler node için PostgreSQL-18-temelli operasyonel doğruluk olarak ele alınmalıdır.

Pi51 üzerindeki gelecekteki PostgreSQL işleri bu varsayımdan başlamalı; PostgreSQL 16'ya artık canlı runtime gerçeği olarak geri dönülmemelidir.

## Next continuation point

The next normal continuation should move away from PostgreSQL major-upgrade work and back into crawler application progress.

Practical next focus should be one of:

- Python crawler worker/app skeleton
- fetch/parse/outbox live workflow integration
- desktop_import / downstream import surface standardization
- crawler execution/service discipline

## Sonraki devam noktası

Bir sonraki normal devam, PostgreSQL major-upgrade işinden çıkıp yeniden crawler uygulama ilerleyişine dönmelidir.

Pratik sonraki odak şu alanlardan biri olmalıdır:

- Python crawler worker/app skeleton
- fetch/parse/outbox canlı workflow entegrasyonu
- desktop_import / downstream import yüzeyi standardizasyonu
- crawler execution/service disiplini
