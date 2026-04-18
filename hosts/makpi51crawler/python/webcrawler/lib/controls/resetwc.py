# EN: This module is the interpreted "reset preparation" control surface.
# EN: It intentionally performs only the safe internal durable stop phase.
# TR: Bu modül yorumlanan "reset hazırlık" kontrol yüzeyidir.
# TR: Bilinçli olarak yalnızca güvenli iç kalıcı stop aşamasını yürütür.
from __future__ import annotations

# EN: We import sys because informational follow-up lines should go to stderr.
# TR: Bilgilendirici takip satırları stderr'e gitmelidir; bu yüzden sys içe
# TR: aktarıyoruz.
import sys

# EN: We import the shared runtime-control helper so DB logic stays centralized.
# TR: DB mantığı merkezde kalsın diye paylaşılan runtime-control yardımcısını içe
# TR: aktarıyoruz.
from ._runtime_control_common import apply_runtime_control


# EN: This callable requests durable stop preparation for the later reset phase.
# TR: Bu çağrılabilir sonraki reset aşaması için kalıcı stop hazırlığını ister.
def main() -> int:
    # EN: We first perform the durable internal stop request.
    # TR: Önce kalıcı iç stop isteğini yürütüyoruz.
    rc = apply_runtime_control(
        desired_state="stop",
        state_reason="resetwc requested internal durable stop state before later reset phase",
        requested_by="resetwc",
    )

    # EN: Any non-zero result is propagated immediately.
    # TR: Sıfır olmayan her sonuç hemen aynen yayılır.
    if rc != 0:
        return rc

    # EN: Real reset is intentionally not implemented here yet.
    # TR: Gerçek reset burada henüz bilinçli olarak uygulanmamıştır.
    print(
        "INFO: resetwc currently performs only the safe internal stop-preparation phase.",
        file=sys.stderr,
    )
    print(
        "INFO: explicit reset body is intentionally not implemented in this step.",
        file=sys.stderr,
    )
    return 0


# EN: This standard guard allows module execution with python -m.
# TR: Bu standart guard modülün python -m ile çalıştırılmasını sağlar.
if __name__ == "__main__":
    raise SystemExit(main())
