# EN: This module is the interpreted "reboot preparation" control surface.
# EN: It intentionally performs only the safe internal durable stop phase.
# TR: Bu modül yorumlanan "reboot hazırlık" kontrol yüzeyidir.
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


# EN: This callable requests durable stop preparation for the later reboot phase.
# TR: Bu çağrılabilir sonraki reboot aşaması için kalıcı stop hazırlığını ister.
def main() -> int:
    # EN: We first perform the durable internal stop request.
    # TR: Önce kalıcı iç stop isteğini yürütüyoruz.
    rc = apply_runtime_control(
        desired_state="stop",
        state_reason="rebootwc requested internal durable stop state before later reboot phase",
        requested_by="rebootwc",
    )

    # EN: Any non-zero result is propagated immediately.
    # TR: Sıfır olmayan her sonuç hemen aynen yayılır.
    if rc != 0:
        return rc

    # EN: Real reboot is intentionally not implemented here yet.
    # TR: Gerçek reboot burada henüz bilinçli olarak uygulanmamıştır.
    print(
        "INFO: rebootwc currently performs only the safe internal stop-preparation phase.",
        file=sys.stderr,
    )
    print(
        "INFO: real reboot phase is intentionally not implemented in this step.",
        file=sys.stderr,
    )
    return 0


# EN: This standard guard allows module execution with python -m.
# TR: Bu standart guard modülün python -m ile çalıştırılmasını sağlar.
if __name__ == "__main__":
    raise SystemExit(main())
