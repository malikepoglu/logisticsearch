# EN: This module is the small worker-runtime support child created by the
# EN: controlled split. It keeps tiny generic helpers out of the parent
# EN: orchestrator so the parent can focus on branch flow only.
# TR: Bu modül kontrollü split ile oluşturulan küçük worker-runtime destek
# TR: alt yüzeyidir. Küçük genel yardımcıları parent orchestrator dışına taşır;
# TR: böylece parent yalnızca branch akışına odaklanabilir.

from __future__ import annotations

# EN: We import datetime and timezone so the support child can produce explicit
# EN: UTC timestamps without depending on parent-level helpers.
# TR: Destek alt yüzeyi parent-seviyesi yardımcılara bağlı kalmadan açık UTC
# TR: zaman damgaları üretebilsin diye datetime ve timezone içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import uuid4 so each worker execution can still receive a unique run id.
# TR: Her worker çalıştırması benzersiz bir run id alabilsin diye uuid4 içe
# TR: aktarıyoruz.
from uuid import uuid4

# EN: We import the canonical claimed-url field reader directly from the
# EN: acquisition-support child instead of the acquisition hub. This avoids a
# EN: circular import while still unifying field access in one canonical place.
# TR: Kanonik claimed-url alan okuyucusunu acquisition hub yerine doğrudan
# TR: acquisition-support alt yüzeyinden içe aktarıyoruz. Bu yaklaşım circular
# TR: import riskini önlerken alan erişimini yine tek kanonik yerde birleştirir.
from .logisticsearch1_1_2_4_1_acquisition_support import get_claimed_url_value


# EN: This helper creates a unique runtime execution id.
# TR: Bu yardımcı benzersiz bir runtime çalıştırma kimliği üretir.
def new_run_id() -> str:
    # EN: We convert uuid4() to text because text ids are easy to print, audit,
    # EN: serialize, and carry through structured result payloads.
    # TR: uuid4() sonucunu metne çeviriyoruz; çünkü metinsel kimlikler yapılı
    # TR: sonuç payload’larında yazdırmak, denetlemek, serileştirmek ve taşımak
    # TR: için kolaydır.
    return str(uuid4())


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı ISO-8601 biçiminde UTC zaman damgası metni döndürür.
def utc_now_iso() -> str:
    # EN: We explicitly use timezone.utc so no machine-local timezone ambiguity
    # EN: can leak into worker-runtime evidence.
    # TR: Worker-runtime kanıtına makineye özgü saat dilimi belirsizliği sızmasın
    # TR: diye açıkça timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc).isoformat()


# EN: This helper builds a small explicit terminal fetch-attempt metadata payload.
# EN: The goal is to keep durable per-attempt evidence easy to interpret later.
# TR: Bu yardımcı küçük ve açık bir terminal fetch-attempt metadata payload’ı
# TR: kurar. Amaç kalıcı deneme-bazlı kanıtın daha sonra kolay yorumlanmasıdır.
def build_terminal_fetch_attempt_metadata(
    *,
    claimed_url: object,
    acquisition_method: str | None,
    note: str,
) -> dict[str, object]:
    # EN: We keep the metadata shape narrow and explicit so later audits can see
    # EN: exactly which runtime path created the durable row.
    # TR: Daha sonraki audit’ler kalıcı satırı hangi runtime yolunun ürettiğini
    # TR: açıkça görebilsin diye metadata şeklini dar ve açık tutuyoruz.
    return {
        "runtime_surface": "worker_runtime",
        "note": note,
        "acquisition_method": acquisition_method,
        "canonical_url": str(get_claimed_url_value(claimed_url, "canonical_url")),
        "authority_key": str(get_claimed_url_value(claimed_url, "authority_key")),
        "scheme": str(get_claimed_url_value(claimed_url, "scheme")),
        "host": str(get_claimed_url_value(claimed_url, "host")),
    }


# EN: This explicit export list keeps the public surface of the support child
# EN: stable and readable.
# TR: Bu açık export listesi destek alt yüzeyinin public yüzeyini stabil ve
# TR: okunabilir tutar.
__all__ = [
    "new_run_id",
    "utc_now_iso",
    "build_terminal_fetch_attempt_metadata",
]
