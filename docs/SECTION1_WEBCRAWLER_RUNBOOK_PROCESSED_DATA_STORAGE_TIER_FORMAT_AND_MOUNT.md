# SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT

Documentation hub:

* `docs/README.md` — documentation hub
* `README.md` — repository root surface

Dokümantasyon merkezi:

* `docs/README.md` — dokümantasyon merkezi
* `README.md` — repository kök yüzeyi

## Purpose

This runbook records the real controlled Pi51 work used to lock removable disk identity, format the processed-data storage tiers, mount them, verify them, and repair `/etc/fstab` after the accidental second destructive rerun changed filesystem UUIDs.

This runbook is the action-layer companion to:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`

## Amaç

Bu runbook, çıkarılabilir disk kimliğini kilitlemek, işlenmiş-veri depolama katmanlarını formatlamak, mount etmek, doğrulamak ve kazara yapılan ikinci yıkıcı yeniden çalıştırmanın filesystem UUID'lerini değiştirmesinden sonra `/etc/fstab` dosyasını onarmak için yapılan gerçek kontrollü Pi51 işini kaydeder.

Bu runbook, şu belgenin action-layer eşidir:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`

## Scope

This runbook covers only completed and validated work:

- target disk identity lock
- destructive GPT + ext4 format
- `/srv/data` and `/srv/buffer` mount preparation
- `/etc/fstab` integration
- live mount verification
- `/etc/fstab` UUID repair

It does not yet cover:

- automatic `/srv/data` versus `/srv/buffer` selection logic
- automatic buffer drain behavior
- crawler pause integration during drain
- Python write-path integration

## Kapsam

Bu runbook yalnızca tamamlanmış ve doğrulanmış işi kapsar:

- hedef disk kimlik kilidi
- yıkıcı GPT + ext4 format
- `/srv/data` ve `/srv/buffer` mount hazırlığı
- `/etc/fstab` entegrasyonu
- canlı mount doğrulaması
- `/etc/fstab` UUID onarımı

Henüz şunları kapsamaz:

- otomatik `/srv/data` ve `/srv/buffer` seçim mantığı
- otomatik buffer drain davranışı
- drain sırasında crawler pause entegrasyonu
- Python write-path entegrasyonu

## Machine and path context

Execution context:

- control machine: `Desktop-Ubuntu`
- target machine: `Pi51`
- target hostname: `makpi51crawler`

Canonical paths:

- `/srv` = existing internal NVMe service/data surface
- `/srv/data` = primary removable processed-data target
- `/srv/buffer` = temporary removable fallback target

## Makine ve path bağlamı

Execution bağlamı:

- kontrol makinesi: `Desktop-Ubuntu`
- hedef makine: `Pi51`
- hedef hostname: `makpi51crawler`

Kanonik path'ler:

- `/srv` = mevcut iç NVMe service/data yüzeyi
- `/srv/data` = birincil çıkarılabilir işlenmiş-veri hedefi
- `/srv/buffer` = geçici çıkarılabilir fallback hedefi

## Locked removable targets

Final locked removable targets:

- `/srv/data`
  - by-id: `/dev/disk/by-id/usb-SABRENT_SABRENT_DB9876543214E-0:0`
  - device: `/dev/sdb`
  - live partition: `/dev/sdb1`

- `/srv/buffer`
  - by-id: `/dev/disk/by-id/usb-USB_SanDisk_3.2Gen1_03002915121125143535-0:0`
  - device: `/dev/sda`
  - live partition: `/dev/sda1`

Internal system disk excluded from destructive work:

- `/dev/nvme0n1`
- existing `/srv` partition: `/dev/nvme0n1p3`

## Kilitlenen çıkarılabilir hedefler

Nihai kilitlenen çıkarılabilir hedefler:

- `/srv/data`
  - by-id: `/dev/disk/by-id/usb-SABRENT_SABRENT_DB9876543214E-0:0`
  - aygıt: `/dev/sdb`
  - canlı partition: `/dev/sdb1`

- `/srv/buffer`
  - by-id: `/dev/disk/by-id/usb-USB_SanDisk_3.2Gen1_03002915121125143535-0:0`
  - aygıt: `/dev/sda`
  - canlı partition: `/dev/sda1`

Yıkıcı işten hariç tutulan iç sistem diski:

- `/dev/nvme0n1`
- mevcut `/srv` partition'ı: `/dev/nvme0n1p3`

## Real execution order

The real execution order was:

1. `STEP156-AE-R10` disk discovery identity audit
2. `STEP156-AE-R11` focused target disk lock audit
3. `STEP156-AE-R12` destructive format + mount storage tiers
4. accidental second destructive rerun changed UUID truth
5. `STEP156-AE-R12-R2` repaired `/etc/fstab` to current live UUID truth

## Gerçek execution sırası

Gerçek execution sırası şuydu:

1. `STEP156-AE-R10` disk discovery identity audit
2. `STEP156-AE-R11` focused target disk lock audit
3. `STEP156-AE-R12` yıkıcı format + mount storage tiers
4. kazara ikinci yıkıcı yeniden çalıştırma UUID doğrusunu değiştirdi
5. `STEP156-AE-R12-R2` `/etc/fstab` dosyasını mevcut canlı UUID doğrusu ile onardı

## Current live filesystem truth

The final current live truth is:

- `/srv/data`
  - label: `ls_proc_data`
  - UUID: `fd8bd0a5-40aa-4123-860a-707c647660f4`

- `/srv/buffer`
  - label: `ls_proc_buffer`
  - UUID: `9dad5ea0-49ad-425f-9798-83cbc75809d8`

Current relevant `/etc/fstab` lines:

- `UUID=fd8bd0a5-40aa-4123-860a-707c647660f4  /srv/data    ext4  noauto,x-systemd.automount,nofail,noatime,x-systemd.device-timeout=10s  0  2`
- `UUID=9dad5ea0-49ad-425f-9798-83cbc75809d8  /srv/buffer  ext4  noauto,x-systemd.automount,nofail,noatime,x-systemd.device-timeout=10s  0  2`

## Mevcut canlı filesystem doğrusu

Nihai mevcut canlı doğru şudur:

- `/srv/data`
  - label: `ls_proc_data`
  - UUID: `fd8bd0a5-40aa-4123-860a-707c647660f4`

- `/srv/buffer`
  - label: `ls_proc_buffer`
  - UUID: `9dad5ea0-49ad-425f-9798-83cbc75809d8`

Güncel ilgili `/etc/fstab` satırları:

- `UUID=fd8bd0a5-40aa-4123-860a-707c647660f4  /srv/data    ext4  noauto,x-systemd.automount,nofail,noatime,x-systemd.device-timeout=10s  0  2`
- `UUID=9dad5ea0-49ad-425f-9798-83cbc75809d8  /srv/buffer  ext4  noauto,x-systemd.automount,nofail,noatime,x-systemd.device-timeout=10s  0  2`

## Validation truth

Final live verification confirmed:

- `/srv/data` mounts from `/dev/sdb1`
- `/srv/buffer` mounts from `/dev/sda1`
- both filesystems are writable
- `/srv/data` is larger than `/srv/buffer`
- `/etc/fstab` matches the current live UUID truth

Observed capacity:

- `/srv/data` available bytes: `955752202240`
- `/srv/buffer` available bytes: `460548956160`

## Doğrulama doğrusu

Nihai canlı doğrulama şunları teyit etti:

- `/srv/data`, `/dev/sdb1` üzerinden mount olmaktadır
- `/srv/buffer`, `/dev/sda1` üzerinden mount olmaktadır
- her iki filesystem yazılabilirdir
- `/srv/data`, `/srv/buffer` katmanından daha büyüktür
- `/etc/fstab`, mevcut canlı UUID doğrusu ile eşleşmektedir

Gözlenen kapasite:

- `/srv/data` kullanılabilir byte: `955752202240`
- `/srv/buffer` kullanılabilir byte: `460548956160`

## Failure handling

Minimum recovery direction if this surface breaks later:

1. inspect the newest `/etc/fstab.bak.*`
2. restore the correct prior file if needed
3. reload systemd
4. read current live UUIDs again
5. repair only the `/srv/data` and `/srv/buffer` lines
6. verify mount and capacity again

If a later accidental rerun changes UUIDs again, runbook truth must follow the newest validated live filesystem truth.

## Hata yönetimi

Bu yüzey daha sonra bozulursa asgari recovery yönü şudur:

1. en yeni `/etc/fstab.bak.*` dosyasını incele
2. gerekirse doğru önceki dosyayı geri yükle
3. systemd'yi yeniden yükle
4. mevcut canlı UUID'leri yeniden oku
5. yalnızca `/srv/data` ve `/srv/buffer` satırlarını onar
6. mount ve kapasiteyi yeniden doğrula

Daha sonraki kazara bir yeniden çalıştırma UUID'leri tekrar değiştirirse, runbook doğrusu en yeni doğrulanmış canlı filesystem doğrusunu izlemelidir.

## Completion criteria

This runbook is complete only if all of the following are true:

- by-id identities are locked correctly
- wrong-device risk is ruled out
- both removable targets are formatted successfully
- both mountpoints mount successfully
- both filesystems pass write verification
- `/etc/fstab` matches current live UUID truth
- final capacity verification passes

## Tamamlanma kriterleri

Bu runbook ancak aşağıdakilerin tümü doğruysa tamamdır:

- by-id kimlikleri doğru kilitlenmiştir
- yanlış aygıt riski dışlanmıştır
- her iki çıkarılabilir hedef başarıyla formatlanmıştır
- her iki mountpoint başarıyla mount olmaktadır
- her iki filesystem write doğrulamasını geçmektedir
- `/etc/fstab` mevcut canlı UUID doğrusu ile eşleşmektedir
- son kapasite doğrulaması geçmektedir

## Deliberately deferred next work

Still separate next work:

- automatic `/srv/data` versus `/srv/buffer` selection logic
- automatic buffer-drain behavior
- crawler short pause during drain
- Python-side processed-data write-path integration

## Bilinçli olarak ertelenen sonraki iş

Ayrı kalan sonraki iş:

- otomatik `/srv/data` ve `/srv/buffer` seçim mantığı
- otomatik buffer-drain davranışı
- drain sırasında crawler kısa pause davranışı
- Python tarafı işlenmiş-veri write-path entegrasyonu
