# EN: This module owns the explicit lease-renewal helper that the worker calls
# EN: at clear durable phase boundaries.
# TR: Bu modül worker’ın net durable aşama sınırlarında çağırdığı açık lease
# TR: yenileme yardımcısını sahiplenir.

from __future__ import annotations

# EN: We import canonical claimed-url field access from the stable acquisition
# EN: family surface.
# TR: Kanonik claimed-url alan erişimini kararlı acquisition ailesi yüzeyinden
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    get_claimed_url_value,
)

# EN: We import the canonical DB gateway renewal wrapper because lease truth
# EN: belongs to crawler-core SQL, not to ad hoc Python state.
# TR: Lease doğrusu crawler-core SQL tarafına ait olduğu için kanonik DB gateway
# TR: renewal wrapper’ını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    renew_url_lease,
)


# EN: This helper converts lease-phase renewal drift into an operator-visible
# EN: degraded payload so the parent worker can stop cleanly instead of crashing.
# TR: Bu yardımcı lease-phase renewal drift'ini operatörün görebileceği degrade
# TR: payload'a çevirir; böylece parent worker çökmeden temiz biçimde durabilir.
def build_lease_phase_degraded_payload(
    *,
    phase_label: str,
    claimed_url: object,
    config: object,
    renew_result: dict[str, object] | None,
    error_class: str,
    error_message: str,
    degraded_reason: str,
) -> dict[str, object]:
    # EN: We keep one normalized degraded payload shape across durable phase
    # EN: boundaries so operator-visible lease truth stays explicit and consistent.
    # TR: Operatörün gördüğü lease doğrusu açık ve tutarlı kalsın diye durable
    # TR: phase sınırlarında tek ve normalize bir degrade payload şekli tutuyoruz.
    return {
        "url_id": int(get_claimed_url_value(claimed_url, "url_id")),
        "lease_token": str(get_claimed_url_value(claimed_url, "lease_token")),
        "worker_id": str(getattr(config, "worker_id")),
        "extend_seconds": int(getattr(config, "lease_seconds")),
        "phase_label": phase_label,
        "renewed": None if renew_result is None else renew_result.get("renewed"),
        "new_lease_expires_at": (
            None if renew_result is None else renew_result.get("new_lease_expires_at")
        ),
        "gateway_lease_degraded_reason": (
            None if renew_result is None else renew_result.get("lease_degraded_reason")
        ),
        "lease_degraded": True,
        "lease_degraded_reason": degraded_reason,
        "lease_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }


# EN: This helper renews the currently owned lease right before the worker enters
# EN: a durable phase that may take non-trivial time.
# TR: Bu yardımcı worker kayda değer süre alabilecek bir durable aşamaya girmeden
# TR: hemen önce mevcut lease’i yeniler.
def renew_claimed_lease_before_durable_phase(
    conn,
    *,
    claimed_url: object,
    config: object,
    phase_label: str,
) -> dict[str, object]:
    # EN: We call the canonical DB wrapper using the currently owned lease
    # EN: identity plus the worker/config contract values.
    # TR: Kanonik DB wrapper’ını mevcut lease kimliği ve worker/config sözleşme
    # TR: değerleri ile çağırıyoruz.
    renew_result = renew_url_lease(
        conn=conn,
        url_id=int(get_claimed_url_value(claimed_url, "url_id")),
        lease_token=str(get_claimed_url_value(claimed_url, "lease_token")),
        worker_id=str(getattr(config, "worker_id")),
        extend_seconds=int(getattr(config, "lease_seconds")),
    )

    # EN: Missing output or a gateway-level degraded payload means renewal truth
    # EN: could not be confirmed for this durable phase boundary.
    # TR: Çıktı eksikse veya gateway-seviyesi degrade payload geldiyse bu durable
    # TR: phase sınırında renewal doğrusu teyit edilememiş demektir.
    if renew_result is None or bool(renew_result.get("lease_degraded")):
        return build_lease_phase_degraded_payload(
            phase_label=phase_label,
            claimed_url=claimed_url,
            config=config,
            renew_result=renew_result,
            error_class="lease_renewal_no_row_before_durable_phase",
            error_message=f"renew_url_lease(...) returned no row before durable phase: {phase_label}",
            degraded_reason="renew_url_lease_returned_no_row_before_durable_phase",
        )

    # EN: The canonical SQL surface returns renewed=true on success, so we verify
    # EN: that explicit signal instead of assuming success silently.
    # TR: Kanonik SQL yüzeyi başarıda renewed=true döndürdüğü için başarıyı sessizce
    # TR: varsaymak yerine bu açık sinyali doğruluyoruz.
    if renew_result.get("renewed") is not True:
        return build_lease_phase_degraded_payload(
            phase_label=phase_label,
            claimed_url=claimed_url,
            config=config,
            renew_result=renew_result,
            error_class="lease_renewal_not_confirmed_before_durable_phase",
            error_message=f"renew_url_lease(...) did not confirm renewal before durable phase: {phase_label}",
            degraded_reason="renew_url_lease_not_confirmed_before_durable_phase",
        )

    # EN: We refresh the in-memory lease expiry view so later phases see the
    # EN: newest DB-backed lease horizon.
    # TR: Sonraki aşamalar en güncel DB-backed lease ufkunu görsün diye bellek içi
    # TR: lease expiry görünümünü yeniliyoruz.
    if isinstance(claimed_url, dict):
        claimed_url["lease_expires_at"] = renew_result["new_lease_expires_at"]
    elif hasattr(claimed_url, "lease_expires_at"):
        setattr(claimed_url, "lease_expires_at", renew_result["new_lease_expires_at"])

    # EN: We return the explicit renewal payload for later inspection when needed.
    # TR: Gerekirse daha sonra incelenebilsin diye açık renewal payload’ını
    # TR: döndürüyoruz.
    return renew_result


# EN: This explicit export list documents the public lease child surface.
# TR: Bu açık export listesi public lease alt yüzeyini belgelendirir.
__all__ = [
    "renew_claimed_lease_before_durable_phase",
]
