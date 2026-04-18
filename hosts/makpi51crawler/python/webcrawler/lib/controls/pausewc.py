# EN: This module is the interpreted "pause" control surface.
# TR: Bu modül yorumlanan "pause" kontrol yüzeyidir.
from __future__ import annotations

# EN: We import the shared runtime-control helper so only the action-specific
# EN: identity lives here.
# TR: Burada yalnızca aksiyona özgü kimlik yaşasın diye paylaşılan
# TR: runtime-control yardımcısını içe aktarıyoruz.
from ._runtime_control_common import apply_runtime_control


# EN: This callable requests durable pause state.
# TR: Bu çağrılabilir kalıcı pause durumunu ister.
def main() -> int:
    # EN: We delegate the real durable change into the shared helper.
    # TR: Gerçek kalıcı değişimi paylaşılan yardımcıya devrediyoruz.
    return apply_runtime_control(
        desired_state="pause",
        state_reason="pausewc requested durable pause state",
        requested_by="pausewc",
    )


# EN: This standard guard allows module execution with python -m.
# TR: Bu standart guard modülün python -m ile çalıştırılmasını sağlar.
if __name__ == "__main__":
    raise SystemExit(main())
