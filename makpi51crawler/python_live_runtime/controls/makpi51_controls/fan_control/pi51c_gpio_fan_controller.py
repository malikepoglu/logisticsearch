#!/usr/bin/env python3
import signal
import time
from pathlib import Path
import gpiod

RUN = True

MODE_DIR = Path("/etc/pi51c-fans")

GPIO_CHIP = "gpiochip4"
FAN1_LINE = 12
FAN2_LINE = 13

FAN0_COOLING_DEVICE = Path("/sys/class/thermal/cooling_device0")

CPU_SENSOR_NAME = "cpu_thermal"
FAN1_SENSOR_NAME = "rp1_adc"
FAN2_SENSOR_NAME = "nvme"

FAN_STEPS = [
    (35.0, 20),
    (40.0, 25),
    (50.0, 30),
    (60.0, 40),
    (65.0, 50),
    (70.0, 60),
    (75.0, 70),
    (80.0, 80),
    (85.0, 90),
    (90.0, 100),
]

CPU_FAN0_STEPS = [
    (40.0, 25),
    (45.0, 35),
    (50.0, 45),
    (55.0, 55),
    (60.0, 70),
    (65.0, 85),
    (70.0, 100),
]

HYST_C = 3.0
STEP_DOWN_DELAY_SEC = 10.0

GPIO_PWM_HZ = 25.0
GPIO_PERIOD_SEC = 1.0 / GPIO_PWM_HZ
KICKSTART_SEC = 1.0


def find_hwmon_temp_by_name(name):
    for name_path in Path("/sys/class/hwmon").glob("hwmon*/name"):
        try:
            current = name_path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if current == name:
            return name_path.parent / "temp1_input"
    raise RuntimeError(f"temperature sensor not found: {name}")


CPU_TEMP_PATH = find_hwmon_temp_by_name(CPU_SENSOR_NAME)
FAN1_TEMP_PATH = find_hwmon_temp_by_name(FAN1_SENSOR_NAME)
FAN2_TEMP_PATH = find_hwmon_temp_by_name(FAN2_SENSOR_NAME)


class Curve:
    def __init__(self, steps):
        self.steps = list(steps)
        self.current = 0
        self.down_since = None

    def raw(self, temp_c):
        duty = 0
        for threshold, percent in self.steps:
            if temp_c >= threshold:
                duty = percent
        return duty

    def entry_temp(self):
        for threshold, percent in self.steps:
            if percent == self.current:
                return threshold
        return None

    def update(self, temp_c):
        raw = self.raw(temp_c)

        if raw > self.current:
            old = self.current
            self.current = raw
            self.down_since = None
            return self.current, old == 0 and raw > 0

        if raw == self.current:
            self.down_since = None
            return self.current, False

        entry = self.entry_temp()
        if entry is None:
            self.current = raw
            self.down_since = None
            return self.current, False

        if temp_c <= entry - HYST_C:
            now = time.monotonic()
            if self.down_since is None:
                self.down_since = now
            elif now - self.down_since >= STEP_DOWN_DELAY_SEC:
                self.current = raw
                self.down_since = None
        else:
            self.down_since = None

        return self.current, False


def read_temp_c(path):
    return int(path.read_text(encoding="utf-8").strip()) / 1000.0


def read_mode(fan_name):
    text = (MODE_DIR / f"{fan_name}.mode").read_text(encoding="utf-8").strip()
    if text == "auto":
        return None
    if text.startswith("manual "):
        value = int(text.split()[1])
        value = max(0, min(255, value))
        return int(round(value * 100 / 255))
    return None


def percent_to_fan0_state(percent):
    if percent <= 0:
        return 0
    if percent >= 100:
        return 4
    if percent <= 25:
        return 1
    if percent <= 50:
        return 2
    if percent <= 75:
        return 3
    return 4


def set_fan0_percent(percent):
    state = percent_to_fan0_state(percent)
    (FAN0_COOLING_DEVICE / "cur_state").write_text(str(state), encoding="ascii")


def stop(signum, frame):
    global RUN
    RUN = False


def main():
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    chip = gpiod.Chip(GPIO_CHIP)
    fan1 = chip.get_line(FAN1_LINE)
    fan2 = chip.get_line(FAN2_LINE)

    fan1.request(consumer="pi51c-fan1", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
    fan2.request(consumer="pi51c-fan2", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)

    c0 = Curve(CPU_FAN0_STEPS)
    c1 = Curve(FAN_STEPS)
    c2 = Curve(FAN_STEPS)

    last = None

    while RUN:
        t0 = read_temp_c(CPU_TEMP_PATH)
        t1 = read_temp_c(FAN1_TEMP_PATH)
        t2 = read_temp_c(FAN2_TEMP_PATH)

        m0 = read_mode("fan0")
        m1 = read_mode("fan1")
        m2 = read_mode("fan2")

        auto0, _ = c0.update(t0)
        auto1, k1 = c1.update(t1)
        auto2, k2 = c2.update(t2)

        p0 = auto0 if m0 is None else m0
        p1 = auto1 if m1 is None else m1
        p2 = auto2 if m2 is None else m2

        set_fan0_percent(p0)

        mode0 = "auto" if m0 is None else "manual"
        mode1 = "auto" if m1 is None else "manual"
        mode2 = "auto" if m2 is None else "manual"

        report = (round(t0, 1), round(t1, 1), round(t2, 1), p0, p1, p2, mode0, mode1, mode2)
        if report != last:
            print(
                f"fan0_cpu={t0:.1f}C fan0={p0}%({mode0}) | "
                f"fan1_rp1_adc={t1:.1f}C fan1={p1}%({mode1}) | "
                f"fan2_nvme={t2:.1f}C fan2={p2}%({mode2})",
                flush=True,
            )
            last = report

        if (m1 is None and k1) or (m2 is None and k2):
            fan1.set_value(1 if p1 > 0 else 0)
            fan2.set_value(1 if p2 > 0 else 0)
            time.sleep(KICKSTART_SEC)

        if p1 == 0 and p2 == 0:
            fan1.set_value(0)
            fan2.set_value(0)
            time.sleep(2.0)
            continue

        end = time.monotonic() + 2.0
        on1 = GPIO_PERIOD_SEC * p1 / 100.0
        on2 = GPIO_PERIOD_SEC * p2 / 100.0

        while RUN and time.monotonic() < end:
            pos = time.monotonic() % GPIO_PERIOD_SEC
            fan1.set_value(1 if p1 >= 100 or (p1 > 0 and pos < on1) else 0)
            fan2.set_value(1 if p2 >= 100 or (p2 > 0 and pos < on2) else 0)
            time.sleep(0.001)

    fan1.set_value(0)
    fan2.set_value(0)


if __name__ == "__main__":
    main()
