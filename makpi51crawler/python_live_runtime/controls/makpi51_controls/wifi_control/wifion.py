#!/usr/bin/env python3
# EN: This file enables Pi51 wlan0 netplan config in a controlled operator path.
# TR: Bu dosya Pi51 wlan0 netplan yapılandırmasını kontrollü operatör yolu ile açar.

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


WIFI_DISABLED = Path("/etc/netplan/60-wlan0.yaml.disabled")
WIFI_ENABLED = Path("/etc/netplan/60-wlan0.yaml")


def run(command: list[str]) -> None:
    # EN: Run host-network commands explicitly so failures stay visible.
    # TR: Host-network komutlarını açık çalıştır; hatalar görünür kalsın.
    subprocess.run(command, check=True)


def print_best_effort(command: list[str]) -> None:
    # EN: Print diagnostic output without failing the completed network operation.
    # TR: Tamamlanan ağ işleminden sonra tanı çıktısını hata saymadan yazdır.
    subprocess.run(command, check=False)


def main() -> int:
    # EN: Netplan mutation requires root; re-execute through sudo when needed.
    # TR: Netplan değişikliği root ister; gerekirse sudo ile yeniden çalıştır.
    if os.geteuid() != 0:
        os.execvp("sudo", ["sudo", sys.executable, __file__])

    if WIFI_ENABLED.exists():
        print("Wi-Fi config already enabled.")
    else:
        if not WIFI_DISABLED.exists():
            print(f"ERROR: {WIFI_DISABLED} not found", file=sys.stderr)
            return 1
        shutil.move(str(WIFI_DISABLED), str(WIFI_ENABLED))

    run(["netplan", "generate"])
    run(["netplan", "apply"])

    print("WIFI_ON_APPLY_DONE")
    print_best_effort(["ip", "-br", "a"])
    print_best_effort(["ip", "route"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
