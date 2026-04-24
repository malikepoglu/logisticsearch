# TOPIC: Pi51c thermal, fan, and Wi-Fi control contract

## EN

### 1. Purpose

This document records the canonical operational truth for the Pi51c thermal, fan, GPIO, and Wi-Fi helper layer after the 2026-04-24 repair and validation work.

This document is host-specific.

Host identity:

- Hostname: `makpi51crawler`
- Normal SSH alias from Ubuntu Desktop: `pi51c`
- Role in LogisticSearch: crawler node
- Scope of this document: host-control support layer only
- Out of scope: crawler application logic, crawler database schema, parsing, ranking, export logic

The goal is to prevent repeated work, preserve the exact hardware/software mapping, and make the current state recoverable from GitHub even if chat history is lost.

### 2. Canonical controlled runtime surfaces

Current Pi51c runtime surfaces:

- `/usr/local/sbin/pi51c_gpio_fan_controller.py`
- `/etc/systemd/system/pi51c-gpio-fan-controller.service`
- `/etc/pi51c-fans/fan0.mode`
- `/etc/pi51c-fans/fan1.mode`
- `/etc/pi51c-fans/fan2.mode`
- `/usr/local/bin/fan`
- `/usr/local/bin/fan0`
- `/usr/local/bin/fan1`
- `/usr/local/bin/fan2`
- `/usr/local/bin/wifion`
- `/usr/local/bin/wifioff`

Git-tracked runtime snapshot:

- `hosts/makpi51crawler/python/host_control/pi51c_fan_control/live_runtime/`

This snapshot contains helper scripts only. It must not contain Wi-Fi credential files.

### 3. Fan naming contract

| Name | Physical component | Control surface | Temperature source | Purpose |
|---|---|---|---|---|
| `fan0` | Raspberry Pi 5 built-in fan connector | `/sys/class/thermal/cooling_device0` | `cpu_thermal` | CPU/SoC cooling |
| `fan1` | External Noctua 5V PWM fan | GPIO12 / physical pin 32 / `gpiochip4 line 12` | `rp1_adc` | RP1/I/O-side cooling |
| `fan2` | External SEENGREAT 5V PWM fan | GPIO13 / physical pin 33 / `gpiochip4 line 13` | `nvme` | NVMe-side cooling |

Current preferred operating mode:

- `fan0 auto`
- `fan1 auto`
- `fan2 0`

Alternative manual mode:

- `fan0 255` forces the Raspberry Pi 5 built-in fan connector to full speed.
- `fan0 auto` returns the built-in fan connector to CPU-temperature-based automatic control.

### 4. Temperature sensor contract

Validated temperature sources on this host:

| Sensor | Meaning | Used by |
|---|---|---|
| `cpu_thermal` | CPU/SoC temperature | `fan0` |
| `rp1_adc` | RP1 I/O controller ADC/temperature value | `fan1` |
| `nvme` | NVMe composite temperature | `fan2` |

Important correction:

- Ubuntu login banner `Temperature:` on this host matches `rp1_adc`.
- It does not match `cpu_thermal`.
- Therefore login-banner temperature is not treated as CPU temperature here.
- `fan0` intentionally follows `cpu_thermal`.
- `fan1` intentionally follows `rp1_adc`.
- `fan2` intentionally follows `nvme`.

Observed validation example:

- `cpu_thermal` around 30-31 C
- `nvme` around 32-33 C
- `rp1_adc` around 40-42 C
- login banner `Temperature:` around 40-42 C

### 5. GPIO mapping contract

Validated GPIO mapping:

| Fan | Physical pin | GPIO | Correct libgpiod surface | Validated behavior |
|---|---:|---:|---|---|
| `fan1` | 32 | GPIO12 | `gpiochip4 line 12` | HIGH runs fan, LOW stops fan |
| `fan2` | 33 | GPIO13 | `gpiochip4 line 13` | HIGH runs fan, LOW stops fan |

Important correction:

- GPIO12 and GPIO13 are not controlled through `gpiochip0` on this Pi51c runtime.
- The correct surface is `gpiochip4`.
- Earlier tests using `gpiochip0 line 12/13` were invalid for the physical fan pins.

Validated commands:

- `sudo gpioset -m time -s 10 gpiochip4 12=1 13=1`
- `sudo gpioset -m time -s 10 gpiochip4 12=0 13=0`

Expected behavior:

- HIGH: both GPIO fans run.
- LOW: both GPIO fans stop.

### 6. Physical wiring contract

Fan1 / Noctua:

- +5V -> physical pin 2
- GND -> physical pin 6
- PWM -> physical pin 32 / GPIO12
- tach -> physical pin 16 / GPIO23

Fan2 / SEENGREAT:

- +5V -> physical pin 4
- GND -> physical pin 14
- PWM -> physical pin 33 / GPIO13
- tach -> physical pin 18 / GPIO24

Validated physical facts:

- Both fans work with +5V and GND.
- With GPIO forced HIGH on the correct lines, both fans run.
- With GPIO forced LOW on the correct lines, both fans stop.
- The final problem was not fan failure; it was the earlier wrong GPIO or PWM surface assumption.

### 7. Command contract

Status command:

- `fan status`

Per-fan mode commands:

- `fan0 auto`
- `fan0 0`
- `fan0 255`
- `fan1 auto`
- `fan1 0`
- `fan1 255`
- `fan2 auto`
- `fan2 0`
- `fan2 255`

Manual values are accepted only in the inclusive range `0..255`.

Invalid input rule:

- invalid values must be ignored
- existing mode must be preserved
- example: `fan2 300` must not change `fan2.mode`

Mode files:

- `/etc/pi51c-fans/fan0.mode`
- `/etc/pi51c-fans/fan1.mode`
- `/etc/pi51c-fans/fan2.mode`

Valid mode file contents:

- `auto`
- `manual <0-255>`

### 8. Fan curve contract

Common external fan curve used for `fan1` and `fan2` automatic mode:

| Temperature | Fan percent |
|---:|---:|
| `< 35 C` | `0%` |
| `35-39 C` | `20%` |
| `40-49 C` | `25%` |
| `50-59 C` | `30%` |
| `60-64 C` | `40%` |
| `65-69 C` | `50%` |
| `70-74 C` | `60%` |
| `75-79 C` | `70%` |
| `80-84 C` | `80%` |
| `85-89 C` | `90%` |
| `>= 90 C` | `100%` |

Control policy:

- hysteresis: `3 C`
- step-down delay: `10 seconds`
- ramp-up: immediate
- positive transition from `0%` uses kickstart
- GPIO software PWM frequency: `25 Hz`

### 9. Built-in Raspberry Pi 5 fan connector contract

`fan0` uses the Pi 5 built-in `pwm-fan` cooling device.

Observed device:

- type: `pwm-fan`
- path: `/sys/class/thermal/cooling_device0`
- max state: `4`

Runtime mapping:

| Percent | cooling state |
|---:|---:|
| `0%` | `0` |
| `1-25%` | `1` |
| `26-50%` | `2` |
| `51-75%` | `3` |
| `76-100%` | `4` |

Full-speed command:

- `fan0 255`

Automatic command:

- `fan0 auto`

### 10. Wi-Fi failover contract

Validated interfaces:

- Ethernet: `eth0`
- Wi-Fi: `wlan0`

Validated routing policy:

- Ethernet metric: `100`
- Wi-Fi metric: `600`
- Ethernet is preferred when cable is connected.
- Wi-Fi is available as failover when Ethernet cable is removed.

Validated Wi-Fi-only SSH target:

- `192.168.0.98`

Secret rule:

- `/etc/netplan/60-wlan0.yaml` must never be committed.
- Wi-Fi SSID must not be committed.
- Wi-Fi PSK/password must not be committed.
- Documentation and runtime snapshots may reference the existence of the file, but not its secret content.

### 11. Current validated state

Validated current state after the session:

- `pi51c-gpio-fan-controller.service` is active.
- `fan status` works.
- `fan0`, `fan1`, and `fan2` mode commands work.
- `fan2 300` preserves current mode.
- `fan1` and `fan2` physical HIGH/LOW validation passed on `gpiochip4`.
- `fan1` currently follows `rp1_adc`.
- `fan2` can remain manual `0` until the noisy SEENGREAT fan is replaced.
- Wi-Fi failover works.
- Runtime snapshot exists under the Git-tracked host-control surface.

## TR

### 1. Amaç

Bu doküman, 2026-04-24 onarım ve doğrulama çalışmasından sonra Pi51c termal, fan, GPIO ve Wi-Fi yardımcı katmanının kanonik operasyon gerçeğini kaydeder.

Bu doküman host özeldir.

Host kimliği:

- Hostname: `makpi51crawler`
- Ubuntu Desktop üzerinden normal SSH alias: `pi51c`
- LogisticSearch rolü: crawler node
- Bu dokümanın kapsamı: yalnızca host-control destek katmanı
- Kapsam dışı: crawler uygulama mantığı, crawler veritabanı şeması, parse, ranking, export mantığı

Amaç aynı işin tekrar yapılmasını engellemek, kesin donanım/yazılım eşleşmesini korumak ve sohbet geçmişi kaybolsa bile mevcut durumu GitHub üzerinden tekrar kurulabilir hale getirmektir.

### 2. Kanonik kontrollü runtime yüzeyleri

Mevcut Pi51c runtime yüzeyleri:

- `/usr/local/sbin/pi51c_gpio_fan_controller.py`
- `/etc/systemd/system/pi51c-gpio-fan-controller.service`
- `/etc/pi51c-fans/fan0.mode`
- `/etc/pi51c-fans/fan1.mode`
- `/etc/pi51c-fans/fan2.mode`
- `/usr/local/bin/fan`
- `/usr/local/bin/fan0`
- `/usr/local/bin/fan1`
- `/usr/local/bin/fan2`
- `/usr/local/bin/wifion`
- `/usr/local/bin/wifioff`

Git altında izlenen runtime snapshot:

- `hosts/makpi51crawler/python/host_control/pi51c_fan_control/live_runtime/`

Bu snapshot yalnızca yardımcı scriptleri içerir. Wi-Fi credential dosyaları içeremez.

### 3. Fan isimlendirme sözleşmesi

| İsim | Fiziksel bileşen | Kontrol yüzeyi | Sıcaklık kaynağı | Amaç |
|---|---|---|---|---|
| `fan0` | Raspberry Pi 5 dahili fan soketi | `/sys/class/thermal/cooling_device0` | `cpu_thermal` | CPU/SoC soğutma |
| `fan1` | Harici Noctua 5V PWM fan | GPIO12 / fiziksel pin 32 / `gpiochip4 line 12` | `rp1_adc` | RP1/I/O tarafı soğutma |
| `fan2` | Harici SEENGREAT 5V PWM fan | GPIO13 / fiziksel pin 33 / `gpiochip4 line 13` | `nvme` | NVMe tarafı soğutma |

Mevcut kullanıcı tercihli mod:

- `fan0 auto`
- `fan1 auto`
- `fan2 0`

Alternatif sessiz/manuel mod:

- Kullanıcı Raspberry Pi 5 dahili fan soketini tam hıza zorlamak isterse `fan0 255`
- Kullanıcı tekrar CPU sıcaklığına bağlı otomatik moda dönmek isterse `fan0 auto`

### 4. Sıcaklık sensörü sözleşmesi

Bu host üzerinde doğrulanan sıcaklık kaynakları:

| Sensör | Anlam | Kullanan |
|---|---|---|
| `cpu_thermal` | CPU/SoC sıcaklığı | `fan0` |
| `rp1_adc` | RP1 I/O controller ADC/sıcaklık değeri | `fan1` |
| `nvme` | NVMe composite sıcaklığı | `fan2` |

Önemli düzeltme:

- Bu host üzerinde Ubuntu login banner `Temperature:` değeri `rp1_adc` ile eşleşir.
- Bu değer `cpu_thermal` ile eşleşmez.
- Bu nedenle login banner sıcaklığı burada CPU sıcaklığı olarak yorumlanmaz.
- `fan0` bilinçli olarak `cpu_thermal` izler.
- `fan1` bilinçli olarak `rp1_adc` izler.
- `fan2` bilinçli olarak `nvme` izler.

Gözlenen doğrulama örneği:

- `cpu_thermal` yaklaşık 30-31 C
- `nvme` yaklaşık 32-33 C
- `rp1_adc` yaklaşık 40-42 C
- login banner `Temperature:` yaklaşık 40-42 C

### 5. GPIO eşleşme sözleşmesi

Doğrulanan GPIO eşleşmesi:

| Fan | Fiziksel pin | GPIO | Doğru libgpiod yüzeyi | Doğrulanan davranış |
|---|---:|---:|---|---|
| `fan1` | 32 | GPIO12 | `gpiochip4 line 12` | HIGH fanı çalıştırır, LOW fanı durdurur |
| `fan2` | 33 | GPIO13 | `gpiochip4 line 13` | HIGH fanı çalıştırır, LOW fanı durdurur |

Önemli düzeltme:

- GPIO12 ve GPIO13 bu Pi51c runtime üzerinde `gpiochip0` üzerinden kontrol edilmez.
- Doğru yüzey `gpiochip4` yüzeyidir.
- `gpiochip0 line 12/13` ile yapılan önceki testler fiziksel fan pinleri için geçersizdi.

Doğrulanan komutlar:

- `sudo gpioset -m time -s 10 gpiochip4 12=1 13=1`
- `sudo gpioset -m time -s 10 gpiochip4 12=0 13=0`

Beklenen davranış:

- HIGH: iki GPIO fan çalışır.
- LOW: iki GPIO fan durur.

### 6. Fiziksel bağlantı sözleşmesi

Fan1 / Noctua:

- +5V -> fiziksel pin 2
- GND -> fiziksel pin 6
- PWM -> fiziksel pin 32 / GPIO12
- tach -> fiziksel pin 16 / GPIO23

Fan2 / SEENGREAT:

- +5V -> fiziksel pin 4
- GND -> fiziksel pin 14
- PWM -> fiziksel pin 33 / GPIO13
- tach -> fiziksel pin 18 / GPIO24

Doğrulanmış fiziksel gerçekler:

- İki fan da +5V ve GND ile çalışır.
- Doğru hatlarda GPIO HIGH yapılınca iki fan da çalışır.
- Doğru hatlarda GPIO LOW yapılınca iki fan da durur.
- Nihai sorun fan arızası değil, önceki yanlış GPIO veya PWM yüzeyi varsayımıydı.

### 7. Komut sözleşmesi

Durum komutu:

- `fan status`

Fan bazlı mod komutları:

- `fan0 auto`
- `fan0 0`
- `fan0 255`
- `fan1 auto`
- `fan1 0`
- `fan1 255`
- `fan2 auto`
- `fan2 0`
- `fan2 255`

Manuel değerler yalnızca `0..255` aralığında kabul edilir.

Geçersiz giriş kuralı:

- geçersiz değerler yok sayılır
- mevcut mode korunur
- örnek: `fan2 300`, `fan2.mode` değerini değiştirmemelidir

Mode dosyaları:

- `/etc/pi51c-fans/fan0.mode`
- `/etc/pi51c-fans/fan1.mode`
- `/etc/pi51c-fans/fan2.mode`

Geçerli mode dosyası içerikleri:

- `auto`
- `manual <0-255>`

### 8. Fan eğrisi sözleşmesi

`fan1` ve `fan2` otomatik modu için ortak harici fan eğrisi:

| Sıcaklık | Fan yüzdesi |
|---:|---:|
| `< 35 C` | `0%` |
| `35-39 C` | `20%` |
| `40-49 C` | `25%` |
| `50-59 C` | `30%` |
| `60-64 C` | `40%` |
| `65-69 C` | `50%` |
| `70-74 C` | `60%` |
| `75-79 C` | `70%` |
| `80-84 C` | `80%` |
| `85-89 C` | `90%` |
| `>= 90 C` | `100%` |

Kontrol politikası:

- histerezis: `3 C`
- step-down delay: `10 saniye`
- yukarı çıkış: anında
- `0%` değerinden pozitif değere geçişte kickstart kullanılır
- GPIO software PWM frekansı: `25 Hz`

### 9. Raspberry Pi 5 dahili fan soketi sözleşmesi

`fan0`, Pi 5 dahili `pwm-fan` cooling device yüzeyini kullanır.

Gözlenen cihaz:

- type: `pwm-fan`
- path: `/sys/class/thermal/cooling_device0`
- max state: `4`

Runtime eşleşmesi:

| Yüzde | cooling state |
|---:|---:|
| `0%` | `0` |
| `1-25%` | `1` |
| `26-50%` | `2` |
| `51-75%` | `3` |
| `76-100%` | `4` |

Tam hız komutu:

- `fan0 255`

Otomatik komut:

- `fan0 auto`

### 10. Wi-Fi failover sözleşmesi

Doğrulanan interface yüzeyleri:

- Ethernet: `eth0`
- Wi-Fi: `wlan0`

Doğrulanan route politikası:

- Ethernet metric: `100`
- Wi-Fi metric: `600`
- Ethernet kablosu bağlıyken Ethernet önceliklidir.
- Ethernet kablosu çıkarıldığında Wi-Fi failover çalışır.

Doğrulanan Wi-Fi-only SSH hedefi:

- `192.168.0.98`

Secret kuralı:

- `/etc/netplan/60-wlan0.yaml` asla commit edilmez.
- Wi-Fi SSID commit edilmez.
- Wi-Fi PSK/password commit edilmez.
- Dokümantasyon ve runtime snapshot dosyanın varlığını referans alabilir, fakat secret içeriğini içeremez.

### 11. Mevcut doğrulanmış durum

Oturum sonrası doğrulanan mevcut durum:

- `pi51c-gpio-fan-controller.service` aktif.
- `fan status` çalışıyor.
- `fan0`, `fan1`, `fan2` mode komutları çalışıyor.
- `fan2 300` mevcut mode değerini koruyor.
- `fan1` ve `fan2` fiziksel HIGH/LOW doğrulaması `gpiochip4` üzerinden geçti.
- `fan1` şu anda `rp1_adc` izliyor.
- `fan2`, gürültülü SEENGREAT fan değiştirilene kadar `manual 0` kalabiliyor.
- Wi-Fi failover çalışıyor.
- Runtime snapshot Git altında izlenen host-control yüzeyinde mevcut.
