# EN: This module is the interpreted "play" control surface.
# TR: Bu modül yorumlanan "play" kontrol yüzeyidir.
from __future__ import annotations

# EN: We import the shared runtime-control helper so this thin control module
# EN: contains only the action identity, not duplicated DB logic.
# TR: Bu ince kontrol modülü yinelenmiş DB mantığı değil yalnızca aksiyon
# TR: kimliği içersin diye paylaşılan runtime-control yardımcısını içe aktarıyoruz.
from ._runtime_control_common import apply_runtime_control


# EN: This callable requests durable run state.
# TR: Bu çağrılabilir kalıcı run durumunu ister.
def main() -> int:
    # EN: We delegate the real durable change into the shared helper.
    # TR: Gerçek kalıcı değişimi paylaşılan yardımcıya devrediyoruz.
    return apply_runtime_control(
        desired_state="run",
        state_reason="playwc requested durable run state",
        requested_by="playwc",
    )


# EN: This standard guard allows module execution with python -m.
# TR: Bu standart guard modülün python -m ile çalıştırılmasını sağlar.
if __name__ == "__main__":
    raise SystemExit(main())
