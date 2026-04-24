# RUNBOOK: Pi51c thermal, fan, and Wi-Fi control

## EN

### 1. Runbook purpose

This runbook defines the controlled operational procedure for inspecting, repairing, installing, and validating the Pi51c thermal, fan, GPIO, and Wi-Fi host-control layer.

Use this runbook when:

- checking fan status
- changing `fan0`, `fan1`, or `fan2` modes
- validating GPIO12/GPIO13 fan wiring
- validating temperature source mapping
- reinstalling the Git-tracked runtime snapshot onto Pi51c
- validating Ethernet-to-Wi-Fi failover
- recovering the current known-good host-control state from GitHub

### 2. Strict safety rules

Do not commit secrets.

Never copy these files or values into Git:

- `/etc/netplan/60-wlan0.yaml`
- Wi-Fi SSID values
- Wi-Fi PSK or password values
- screenshots or logs containing Wi-Fi credentials

Do not assume GPIO12/GPIO13 are on `gpiochip0`.

Validated Pi51c GPIO mapping:

- GPIO12 -> physical pin 32 -> `gpiochip4 line 12` -> `fan1`
- GPIO13 -> physical pin 33 -> `gpiochip4 line 13` -> `fan2`

Do not assume Ubuntu login banner `Temperature:` means CPU temperature.

Validated Pi51c temperature mapping:

- `fan0` follows `cpu_thermal`
- `fan1` follows `rp1_adc`
- `fan2` follows `nvme`
- login banner `Temperature:` follows `rp1_adc` on this host

### 3. Fast status check

Run on Pi51c:

```bash
# Makine: pi51c
fan status
systemctl is-active pi51c-gpio-fan-controller.service
systemctl is-enabled pi51c-gpio-fan-controller.service
```

Expected:

- service is `active`
- service is `enabled`
- fan mode files are printed
- temperature sources are printed
- last service log lines are printed

### 4. Temperature source audit

Run on Pi51c:

```bash
# Makine: pi51c
for f in /sys/class/hwmon/hwmon*/temp*_input; do
  [ -f "$f" ] || continue
  name="$(cat "$(dirname "$f")/name" 2>/dev/null || echo unknown)"
  raw="$(cat "$f")"
  c="$(awk "BEGIN { printf \"%.1f\", $raw/1000 }")"
  echo "$name=$c C path=$f"
done

landscape-sysinfo | grep Temperature || true
```

Expected interpretation:

- `cpu_thermal` is CPU or SoC temperature
- `rp1_adc` is RP1 I/O controller ADC temperature and matches login banner temperature on this host
- `nvme` is NVMe composite temperature

### 5. Fan command usage

Current command contract:

```bash
# Makine: pi51c
fan0 auto
fan0 255
fan1 auto
fan1 128
fan2 0
fan status
```

Meaning:

- `fan0 auto` returns the Pi 5 built-in fan connector to CPU-temperature-based automatic control
- `fan0 255` requests full manual speed for the Pi 5 built-in fan connector
- `fan1 auto` keeps the Noctua GPIO fan on RP1 temperature control
- `fan1 0..255` manually controls the Noctua GPIO fan
- `fan2 auto` returns the SEENGREAT fan to NVMe temperature control
- `fan2 0` keeps the noisy SEENGREAT fan off until replacement

Invalid input test:

```bash
# Makine: pi51c
fan2 300
fan status
```

Expected:

- command prints an invalid-input message
- existing `fan2` mode is preserved

### 6. External GPIO fan wiring validation

Use only when Pi51c is physically accessible and the fan wiring is being inspected.

Stop the controller:

```bash
# Makine: pi51c
sudo systemctl stop pi51c-gpio-fan-controller.service
```

Force both GPIO fan PWM lines HIGH for 10 seconds:

```bash
# Makine: pi51c
sudo gpioset -m time -s 10 gpiochip4 12=1 13=1
```

Expected:

- `fan1` runs.
- `fan2` runs.

Force both GPIO fan PWM lines LOW for 10 seconds:

```bash
# Makine: pi51c
sudo gpioset -m time -s 10 gpiochip4 12=0 13=0
```

Expected:

- `fan1` stops.
- `fan2` stops.

Restart the controller:

```bash
# Makine: pi51c
sudo systemctl restart pi51c-gpio-fan-controller.service
fan status
```

### 7. Built-in Raspberry Pi 5 fan connector validation

Run on Pi51c:

```bash
# Makine: pi51c
cat /sys/class/thermal/cooling_device0/type
cat /sys/class/thermal/cooling_device0/cur_state
cat /sys/class/thermal/cooling_device0/max_state
```

Expected:

- type: `pwm-fan`
- max_state: `4`

Manual full-speed request:

```bash
# Makine: pi51c
fan0 255
sleep 5
fan status
```

Expected:

- `fan0=manual 255`
- the runtime controller should request the highest available cooling state
- if `cur_state` does not move to the highest state, do not treat `fan0` manual control as sealed until the kernel cooling-device behavior is rechecked

Return to automatic mode:

```bash
# Makine: pi51c
fan0 auto
fan status
```

### 8. Wi-Fi failover validation

Ethernet connected state:

```bash
# Makine: pi51c
ip -br a | grep -E "^(eth0|wlan0)"
ip route
```

Expected:

- `eth0` normally has metric `100`.
- `wlan0` normally has metric `600`.
- Ethernet is preferred while the cable is connected.

Wi-Fi-only validation from Ubuntu Desktop:

```bash
# Makine: Ubuntu Desktop
ssh makpi51@192.168.0.98 hostnamectl --static
ssh makpi51@192.168.0.98 ip -br a
ssh makpi51@192.168.0.98 ip route
```

Expected after Ethernet cable removal:

- SSH still works over Wi-Fi.
- `eth0` is down or has no active IPv4 route.
- `wlan0` has `192.168.0.98`.
- default route uses `wlan0`.

### 9. Reinstall runtime from Git-tracked source snapshot

Run on Pi51c after `/logisticsearch/repo` is synced:

```bash
# Makine: pi51c
SRC="/logisticsearch/repo/hosts/makpi51crawler/python/host_control/pi51c_fan_control/live_runtime"

sudo install -m 0755 "$SRC/pi51c_gpio_fan_controller.py" /usr/local/sbin/pi51c_gpio_fan_controller.py
sudo install -m 0755 "$SRC/fan" /usr/local/bin/fan
sudo install -m 0755 "$SRC/fan0" /usr/local/bin/fan0
sudo install -m 0755 "$SRC/fan1" /usr/local/bin/fan1
sudo install -m 0755 "$SRC/fan2" /usr/local/bin/fan2
sudo install -m 0755 "$SRC/wifion" /usr/local/bin/wifion
sudo install -m 0755 "$SRC/wifioff" /usr/local/bin/wifioff
sudo ln -sfn /usr/local/bin/wifion /usr/local/sbin/wifion
sudo ln -sfn /usr/local/bin/wifioff /usr/local/sbin/wifioff

sudo python3 -m py_compile /usr/local/sbin/pi51c_gpio_fan_controller.py
sudo systemctl restart pi51c-gpio-fan-controller.service
sleep 3
fan status
```

### 10. Current preferred operating mode

Quiet/noisy-fan-avoidance mode:

```bash
# Makine: pi51c
fan0 auto
fan1 auto
fan2 0
fan status
```

Manual full-speed built-in fan mode:

```bash
# Makine: pi51c
fan0 255
fan1 auto
fan2 0
fan status
```

## TR

### 1. Runbook amacı

Bu runbook, Pi51c termal, fan, GPIO ve Wi-Fi host-control katmanını incelemek, onarmak, kurmak ve doğrulamak için kontrollü operasyon prosedürünü tanımlar.

Bu runbook şu durumlarda kullanılmalıdır:

- fan durumunu kontrol ederken
- `fan0`, `fan1` veya `fan2` modlarını değiştirirken
- GPIO12/GPIO13 fan kablolamasını doğrularken
- sıcaklık kaynağı eşleşmesini doğrularken
- Git altında izlenen runtime snapshot Pi51c üzerine yeniden kurulurken
- Ethernetten Wi-Fi failover doğrulanırken
- GitHub üzerinden bilinen sağlam host-control durumu geri kurulurken

### 2. Sert güvenlik kuralları

Secret commit edilmez.

Şu dosyalar veya değerler asla Git içine kopyalanmaz:

- `/etc/netplan/60-wlan0.yaml`
- Wi-Fi SSID değerleri
- Wi-Fi PSK veya password değerleri
- Wi-Fi credential içeren ekran görüntüleri veya loglar

GPIO12/GPIO13 için `gpiochip0` varsayımı yapılmaz.

Doğrulanmış Pi51c GPIO eşleşmesi:

- GPIO12 -> fiziksel pin 32 -> `gpiochip4 line 12` -> `fan1`
- GPIO13 -> fiziksel pin 33 -> `gpiochip4 line 13` -> `fan2`

Ubuntu login banner `Temperature:` değerinin CPU sıcaklığı olduğu varsayılmaz.

Doğrulanmış Pi51c sıcaklık eşleşmesi:

- `fan0`, `cpu_thermal` izler
- `fan1`, `rp1_adc` izler
- `fan2`, `nvme` izler
- bu host üzerinde login banner `Temperature:` değeri `rp1_adc` izler

### 3. Hızlı durum kontrolü

Pi51c üzerinde çalıştır:

```bash
# Makine: pi51c
fan status
systemctl is-active pi51c-gpio-fan-controller.service
systemctl is-enabled pi51c-gpio-fan-controller.service
```

Beklenen:

- servis `active` olmalıdır
- servis `enabled` olmalıdır
- fan mode dosyaları yazdırılmalıdır
- sıcaklık kaynakları yazdırılmalıdır
- son servis log satırları yazdırılmalıdır

### 4. Sıcaklık kaynağı denetimi

Pi51c üzerinde çalıştır:

```bash
# Makine: pi51c
for f in /sys/class/hwmon/hwmon*/temp*_input; do
  [ -f "$f" ] || continue
  name="$(cat "$(dirname "$f")/name" 2>/dev/null || echo unknown)"
  raw="$(cat "$f")"
  c="$(awk "BEGIN { printf \"%.1f\", $raw/1000 }")"
  echo "$name=$c C path=$f"
done

landscape-sysinfo | grep Temperature || true
```

Beklenen yorum:

- `cpu_thermal`, CPU veya SoC sıcaklığıdır
- `rp1_adc`, RP1 I/O controller ADC sıcaklığıdır ve bu host üzerinde login banner sıcaklığıyla eşleşir
- `nvme`, NVMe composite sıcaklığıdır

### 5. Fan komut kullanımı

Mevcut komut sözleşmesi:

```bash
# Makine: pi51c
fan0 auto
fan0 255
fan1 auto
fan1 128
fan2 0
fan status
```

Anlamı:

- `fan0 auto`, Pi 5 dahili fan soketini CPU sıcaklığına bağlı otomatik kontrole döndürür
- `fan0 255`, Pi 5 dahili fan soketi için manuel tam hız isteğidir
- `fan1 auto`, Noctua GPIO fanı RP1 sıcaklık kontrolünde tutar
- `fan1 0..255`, Noctua GPIO fanı manuel kontrol eder
- `fan2 auto`, SEENGREAT fanı NVMe sıcaklık kontrolüne döndürür
- `fan2 0`, gürültülü SEENGREAT fan değiştirilene kadar kapalı tutar

Geçersiz giriş testi:

```bash
# Makine: pi51c
fan2 300
fan status
```

Beklenen:

- komut invalid-input mesajı yazmalıdır
- mevcut `fan2` modu korunmalıdır

### 6. Harici GPIO fan kablolama doğrulaması

Yalnızca Pi51c fiziksel olarak erişilebilirken ve fan kablolaması incelenirken kullanılır.

Controller servisini durdur:

```bash
# Makine: pi51c
sudo systemctl stop pi51c-gpio-fan-controller.service
```

İki GPIO fan PWM hattını 10 saniye HIGH yap:

```bash
# Makine: pi51c
sudo gpioset -m time -s 10 gpiochip4 12=1 13=1
```

Beklenen:

- `fan1` çalışır.
- `fan2` çalışır.

İki GPIO fan PWM hattını 10 saniye LOW yap:

```bash
# Makine: pi51c
sudo gpioset -m time -s 10 gpiochip4 12=0 13=0
```

Beklenen:

- `fan1` durur.
- `fan2` durur.

Controller servisini yeniden başlat:

```bash
# Makine: pi51c
sudo systemctl restart pi51c-gpio-fan-controller.service
fan status
```

### 7. Raspberry Pi 5 dahili fan soketi doğrulaması

Pi51c üzerinde çalıştır:

```bash
# Makine: pi51c
cat /sys/class/thermal/cooling_device0/type
cat /sys/class/thermal/cooling_device0/cur_state
cat /sys/class/thermal/cooling_device0/max_state
```

Beklenen:

- type: `pwm-fan`
- max_state: `4`

Manuel tam hız isteği:

```bash
# Makine: pi51c
fan0 255
sleep 5
fan status
```

Beklenen:

- `fan0=manual 255`
- runtime controller en yüksek uygun cooling state değerini istemelidir
- `cur_state` en yüksek state değerine çıkmazsa, kernel cooling-device davranışı tekrar kontrol edilmeden `fan0` manuel kontrolü sealed kabul edilmemelidir

Otomatik moda dönüş:

```bash
# Makine: pi51c
fan0 auto
fan status
```

### 8. Wi-Fi failover doğrulaması

Ethernet bağlı durum:

```bash
# Makine: pi51c
ip -br a | grep -E "^(eth0|wlan0)"
ip route
```

Beklenen:

- `eth0` normalde metric `100` taşır.
- `wlan0` normalde metric `600` taşır.
- kablo bağlıyken Ethernet önceliklidir.

Ubuntu Desktop üzerinden Wi-Fi-only doğrulaması:

```bash
# Makine: Ubuntu Desktop
ssh makpi51@192.168.0.98 hostnamectl --static
ssh makpi51@192.168.0.98 ip -br a
ssh makpi51@192.168.0.98 ip route
```

Ethernet kablosu çıkarıldıktan sonra beklenen:

- SSH Wi-Fi üzerinden çalışmaya devam eder.
- `eth0` down olur veya aktif IPv4 route taşımaz.
- `wlan0`, `192.168.0.98` taşır.
- default route `wlan0` kullanır.

### 9. Git-tracked source snapshot üzerinden runtime yeniden kurulum

`/logisticsearch/repo` senkronlandıktan sonra Pi51c üzerinde çalıştır:

```bash
# Makine: pi51c
SRC="/logisticsearch/repo/hosts/makpi51crawler/python/host_control/pi51c_fan_control/live_runtime"

sudo install -m 0755 "$SRC/pi51c_gpio_fan_controller.py" /usr/local/sbin/pi51c_gpio_fan_controller.py
sudo install -m 0755 "$SRC/fan" /usr/local/bin/fan
sudo install -m 0755 "$SRC/fan0" /usr/local/bin/fan0
sudo install -m 0755 "$SRC/fan1" /usr/local/bin/fan1
sudo install -m 0755 "$SRC/fan2" /usr/local/bin/fan2
sudo install -m 0755 "$SRC/wifion" /usr/local/bin/wifion
sudo install -m 0755 "$SRC/wifioff" /usr/local/bin/wifioff
sudo ln -sfn /usr/local/bin/wifion /usr/local/sbin/wifion
sudo ln -sfn /usr/local/bin/wifioff /usr/local/sbin/wifioff

sudo python3 -m py_compile /usr/local/sbin/pi51c_gpio_fan_controller.py
sudo systemctl restart pi51c-gpio-fan-controller.service
sleep 3
fan status
```

### 10. Mevcut tercih edilen operasyon modu

Sessiz/gürültülü fanı devre dışı bırakma modu:

```bash
# Makine: pi51c
fan0 auto
fan1 auto
fan2 0
fan status
```

Dahili fan soketi manuel tam hız modu:

```bash
# Makine: pi51c
fan0 255
fan1 auto
fan2 0
fan status
```
