# EN: This module owns the explicit lease-renewal helper that the worker calls
# EN: at clear durable phase boundaries.
# TR: Bu modül worker’ın net durable aşama sınırlarında çağırdığı açık lease
# TR: yenileme yardımcısını sahiplenir.

from __future__ import annotations

# EN: We import canonical claimed-url field access from the stable acquisition
# EN: family surface.
# TR: Kanonik claimed-url alan erişimini kararlı acquisition ailesi yüzeyinden
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_2_acquisition_runtime import (
    get_claimed_url_value,
)

# EN: We import the canonical DB gateway renewal wrapper because lease truth
# EN: belongs to crawler-core SQL, not to ad hoc Python state.
# TR: Lease doğrusu crawler-core SQL tarafına ait olduğu için kanonik DB gateway
# TR: renewal wrapper’ını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    renew_url_lease,
)


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

    # EN: Missing output means the worker no longer holds the lease the way the
    # EN: current runtime expects.
    # TR: Çıktı yoksa worker lease’i mevcut runtime’ın beklediği biçimde artık
    # TR: tutmuyor demektir.
    if renew_result is None:
        raise RuntimeError(
            f"renew_url_lease(...) returned no row before durable phase: {phase_label}"
        )

    # EN: The canonical SQL surface returns renewed=true on success, so we verify
    # EN: that explicit signal instead of assuming success silently.
    # TR: Kanonik SQL yüzeyi başarıda renewed=true döndürdüğü için başarıyı sessizce
    # TR: varsaymak yerine bu açık sinyali doğruluyoruz.
    if renew_result.get("renewed") is not True:
        raise RuntimeError(
            f"renew_url_lease(...) did not confirm renewal before durable phase: {phase_label}"
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
