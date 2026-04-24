# Pi51c host-control runtime snapshot

## EN

This directory stores the Git-tracked, non-secret runtime snapshot for Pi51c host-control helpers.

Scope:

- thermal sensor routing
- `fan0`, `fan1`, `fan2` control helpers
- GPIO fan controller service payload
- Wi-Fi enable/disable helper scripts

This is host-control infrastructure for `makpi51crawler`; it is not crawler application logic.

Secret rule:

- Do not commit `/etc/netplan/60-wlan0.yaml`.
- Do not commit Wi-Fi SSID or PSK values.
- Only helper scripts and non-secret runtime logic belong here.

## TR

Bu dizin Pi51c host-control yardımcıları için Git altında izlenen, secret içermeyen runtime snapshot yüzeyidir.

Kapsam:

- sıcaklık sensörü yönlendirmesi
- `fan0`, `fan1`, `fan2` kontrol yardımcıları
- GPIO fan controller servis payload'u
- Wi-Fi açma/kapatma yardımcı scriptleri

Bu yüzey `makpi51crawler` için host-control altyapısıdır; crawler uygulama mantığı değildir.

Secret kuralı:

- `/etc/netplan/60-wlan0.yaml` commit edilmez.
- Wi-Fi SSID veya PSK değerleri commit edilmez.
- Buraya yalnızca yardımcı scriptler ve secret içermeyen runtime mantığı girer.
