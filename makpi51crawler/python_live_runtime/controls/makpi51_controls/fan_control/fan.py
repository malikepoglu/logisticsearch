#!/usr/bin/env python3
# EN: This file is the safe read-only fan status control entry for Pi51.
# TR: Bu dosya Pi51 için güvenli salt-okunur fan durum kontrol girişidir.

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_text(command: list[str]) -> str:
    # EN: Run a diagnostic command without raising on non-zero exit.
    # TR: Tanı komutunu sıfır dışı çıkışta hata fırlatmadan çalıştır.
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return result.stdout.rstrip()


def read_text_or_missing(path: Path) -> str:
    # EN: Read a small status file and return "missing" if it is absent or unreadable.
    # TR: Küçük durum dosyasını oku; yoksa veya okunamazsa "missing" döndür.
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return "missing"


def print_temperatures() -> None:
    # EN: Print available hwmon temperatures without mutating the host.
    # TR: Host üzerinde değişiklik yapmadan mevcut hwmon sıcaklıklarını yazdır.
    print("== TEMPERATURES ==")
    for temp_path in sorted(Path("/sys/class/hwmon").glob("hwmon*/temp*_input")):
        try:
            raw_value = temp_path.read_text(encoding="utf-8").strip()
            name = (temp_path.parent / "name").read_text(encoding="utf-8").strip()
            celsius = int(raw_value) / 1000.0
        except (OSError, ValueError):
            continue
        print(f"{name}={celsius:.1f} C path={temp_path}")


def main(argv: list[str]) -> int:
    # EN: Keep this control intentionally narrow: only "status" is read-only and safe.
    # TR: Bu kontrolü bilinçli olarak dar tut: yalnızca "status" salt-okunur ve güvenlidir.
    if argv != ["status"]:
        print("usage: fan.py status", file=sys.stderr)
        return 2

    print(f"service={run_text(['systemctl', 'is-active', 'pi51c-gpio-fan-controller.service'])}")
    print(f"fan0={read_text_or_missing(Path('/etc/pi51c-fans/fan0.mode'))}")
    print(f"fan1={read_text_or_missing(Path('/etc/pi51c-fans/fan1.mode'))}")
    print(f"fan2={read_text_or_missing(Path('/etc/pi51c-fans/fan2.mode'))}")
    print()

    print_temperatures()
    print()

    print("== FAN0 COOLING DEVICE ==")
    print(run_text(["cat", "/sys/class/thermal/cooling_device0/type"]))
    print(f"cur_state={run_text(['cat', '/sys/class/thermal/cooling_device0/cur_state'])}")
    print(f"max_state={run_text(['cat', '/sys/class/thermal/cooling_device0/max_state'])}")
    print()

    print("== SERVICE LOG ==")
    print(run_text(["journalctl", "-u", "pi51c-gpio-fan-controller.service", "-n", "8", "--no-pager"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
