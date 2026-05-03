#!/usr/bin/env python3
# EN: This file controls Pi51 fan1 mode through /etc/pi51c-fans/fan1.mode.
# TR: Bu dosya Pi51 fan1 modunu /etc/pi51c-fans/fan1.mode üzerinden yönetir.

from __future__ import annotations

import os
import sys
from pathlib import Path


MODE_PATH = Path("/etc/pi51c-fans/fan1.mode")


def show() -> None:
    # EN: Print current mode without failing when the mode file is absent.
    # TR: Mod dosyası yoksa hata vermeden mevcut modu yazdır.
    try:
        current = MODE_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        current = "missing"
    print(f"fan1: {current}")


def rerun_with_sudo(argv: list[str]) -> None:
    # EN: Re-execute through sudo when writing root-owned mode files is required.
    # TR: Root sahipli mod dosyası yazılacağı zaman sudo ile yeniden çalıştır.
    os.execvp("sudo", ["sudo", sys.executable, __file__, *argv])


def main(argv: list[str]) -> int:
    # EN: Accept only "auto" or an integer PWM value from 0 to 255.
    # TR: Yalnızca "auto" veya 0-255 arası tam sayı PWM değerini kabul et.
    if len(argv) != 1:
        print("usage: fan1.py auto|0-255", file=sys.stderr)
        show()
        return 2

    value = argv[0]

    if value == "auto":
        if os.geteuid() != 0:
            rerun_with_sudo(argv)
        MODE_PATH.write_text("auto\n", encoding="utf-8")
        print("fan1=auto")
        return 0

    if value.isdigit() and 0 <= int(value) <= 255:
        if os.geteuid() != 0:
            rerun_with_sudo(argv)
        MODE_PATH.write_text(f"manual {value}\n", encoding="utf-8")
        print(f"fan1=manual value={value}")
        return 0

    print(f"invalid input ignored: {value}", file=sys.stderr)
    show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
