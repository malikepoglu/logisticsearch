# EN: This module is the shared support surface for the acquisition family.
# EN: It holds only stable result types and generic acquisition helpers that are
# EN: reused by direct HTTP fetch, robots fetch, and browser-backed fetch paths.
# TR: Bu modül acquisition ailesi için paylaşılan destek yüzeyidir.
# TR: Doğrudan HTTP fetch, robots fetch ve browser-backed fetch yolları tarafından
# TR: yeniden kullanılan yalnızca kararlı sonuç tiplerini ve genel acquisition
# TR: yardımcılarını tutar.

from __future__ import annotations

# EN: We import dataclass because shared acquisition result objects should stay
# EN: explicit, named, and beginner-readable.
# TR: Paylaşılan acquisition sonuç nesneleri açık, isimli ve beginner-okunur
# TR: kalsın diye dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone because shared acquisition timestamps must
# EN: stay explicit and UTC-based across the whole acquisition family.
# TR: Paylaşılan acquisition zaman damgaları tüm acquisition ailesinde açık ve
# TR: UTC tabanlı kalsın diye datetime ve timezone içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import hashlib because raw artefacts need deterministic SHA256
# EN: fingerprints across all acquisition branches.
# TR: Ham artefact'ların tüm acquisition dallarında deterministik SHA256 parmak
# TR: izine ihtiyacı olduğu için hashlib içe aktarıyoruz.
import hashlib

# EN: We import Path because filesystem path work is clearer and safer with
# EN: pathlib objects than with loose raw strings.
# TR: Filesystem path işi pathlib nesneleriyle gevşek ham metinlere göre daha
# TR: açık ve güvenli olduğu için Path içe aktarıyoruz.
from pathlib import Path


# EN: This constant defines the minimal controlled raw-fetch root under /srv.
# EN: Raw and working crawler accumulation must stay under /srv according to the
# EN: current simplified storage truth requested by the user.
# TR: Bu sabit /srv altındaki asgari kontrollü raw-fetch kökünü tanımlar.
# TR: Kullanıcının istediği güncel sade depolama doğrusuna göre ham ve çalışma
# TR: crawler birikimi /srv altında kalmalıdır.
RAW_FETCH_ROOT = Path("/srv/webcrawler/raw_fetch")

@dataclass
class FetchedPageResult:
    # EN: url_id is the claimed frontier url id that produced this fetch result.
    # TR: url_id bu fetch sonucunu üreten claim edilmiş frontier url kimliğidir.
    url_id: int

    # EN: requested_url is the original canonical URL that the worker tried to fetch.
    # TR: requested_url worker'ın fetch etmeye çalıştığı özgün canonical URL'dir.
    requested_url: str

    # EN: final_url is the final URL reported by the HTTP client after redirects.
    # TR: final_url redirect'lerden sonra HTTP istemcisinin bildirdiği son URL'dir.
    final_url: str

    # EN: http_status is the numeric HTTP response status code.
    # TR: http_status sayısal HTTP yanıt durum kodudur.
    http_status: int

    # EN: content_type is the visible Content-Type response header when present.
    # TR: content_type varsa görünür Content-Type yanıt başlığıdır.
    content_type: str | None

    # EN: etag is the visible ETag response header when present.
    # TR: etag varsa görünür ETag yanıt başlığıdır.
    etag: str | None

    # EN: last_modified is the visible Last-Modified response header when present.
    # TR: last_modified varsa görünür Last-Modified yanıt başlığıdır.
    last_modified: str | None

    # EN: body_bytes is the exact number of raw response bytes that were written.
    # TR: body_bytes yazılmış ham yanıt byte'larının tam sayısıdır.
    body_bytes: int

    # EN: raw_storage_path is the full on-disk path of the raw body artefact.
    # TR: raw_storage_path ham body artefact'ının disk üzerindeki tam yoludur.
    raw_storage_path: str

    # EN: raw_sha256 is the SHA256 fingerprint of the raw body bytes.
    # TR: raw_sha256 ham body byte'larının SHA256 parmak izidir.
    raw_sha256: str

    # EN: fetched_at records when the fetch result was produced.
    # TR: fetched_at fetch sonucunun ne zaman üretildiğini kaydeder.
    fetched_at: str

@dataclass
class FetchedRobotsTxtResult:
    # EN: host_id is the frontier.host identity whose robots URL we fetched.
    # TR: host_id robots URL'sini fetch ettiğimiz frontier.host kimliğidir.
    host_id: int

    # EN: robots_url is the explicit robots.txt URL we attempted to fetch.
    # TR: robots_url fetch etmeyi denediğimiz açık robots.txt URL'sidir.
    robots_url: str

    # EN: final_url is the final visible URL after redirects, when available.
    # TR: final_url varsa redirect sonrası görünen son URL'dir.
    final_url: str

    # EN: http_status is the visible HTTP status code when an HTTP response existed.
    # TR: http_status bir HTTP yanıtı mevcutsa görünen HTTP durum kodudur.
    http_status: int | None

    # EN: content_type is the visible Content-Type header when present.
    # TR: content_type varsa görünen Content-Type başlığıdır.
    content_type: str | None

    # EN: etag is the visible ETag header when present.
    # TR: etag varsa görünen ETag başlığıdır.
    etag: str | None

    # EN: last_modified is the visible Last-Modified header when present.
    # TR: last_modified varsa görünen Last-Modified başlığıdır.
    last_modified: str | None

    # EN: body_bytes is the exact raw byte count that was persisted or observed.
    # TR: body_bytes saklanan veya gözlenen ham byte sayısının tam değeridir.
    body_bytes: int

    # EN: raw_storage_path is the persisted raw body path when a body was captured.
    # TR: raw_storage_path bir body yakalandıysa saklanan ham body yoludur.
    raw_storage_path: str | None

    # EN: raw_sha256 is the SHA256 fingerprint of the persisted raw body when present.
    # TR: raw_sha256 varsa saklanan ham body'nin SHA256 parmak izidir.
    raw_sha256: str | None

    # EN: fetched_at records the UTC timestamp of this robots fetch attempt.
    # TR: fetched_at bu robots fetch denemesinin UTC zaman damgasını kaydeder.
    fetched_at: str

    # EN: fetch_error_class stores a transport-class error name when no HTTP response existed.
    # TR: fetch_error_class HTTP yanıtı yoksa taşıma-sınıfı hata adını tutar.
    fetch_error_class: str | None

    # EN: fetch_error_message stores the visible transport error message when present.
    # TR: fetch_error_message varsa görünen taşıma hata mesajını tutar.
    fetch_error_message: str | None

# EN: This helper builds one normalized degraded payload for acquisition
# EN: contract drift so upper layers can stop cleanly with explicit evidence.
# TR: Bu yardımcı acquisition contract drift'i için tek ve normalize bir degrade
# TR: payload üretir; böylece üst katmanlar açık kanıtla temiz biçimde durabilir.
def build_acquisition_contract_degraded_payload(
    *,
    action: str,
    target_kind: str,
    target_id: int,
    requested_url: str | None = None,
    final_url: str | None = None,
    content_type: str | None = None,
    body_bytes: int | None = None,
    raw_storage_path: str | None = None,
    raw_sha256: str | None = None,
    fetched_at: str | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, object]:
    # EN: We keep one normalized degraded payload shape across fetched-page and
    # EN: fetched-robots validation paths so caller-visible truth stays explicit.
    # TR: Çağıranın gördüğü doğruluk açık kalsın diye fetched-page ve fetched-robots
    # TR: doğrulama yolları arasında tek normalize degrade payload şekli tutuyoruz.
    return {
        "target_kind": target_kind,
        "target_id": target_id,
        "requested_url": requested_url,
        "final_url": final_url,
        "content_type": content_type,
        "body_bytes": body_bytes,
        "raw_storage_path": raw_storage_path,
        "raw_sha256": raw_sha256,
        "fetched_at": fetched_at,
        "acquisition_action": action,
        "acquisition_degraded": True,
        "acquisition_degraded_reason": f"{action}_contract_invalid",
        "acquisition_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }


# EN: This helper reads one persisted raw artefact only after confirming that
# EN: the path stays under the controlled raw root and is actually readable.
# TR: Bu yardımcı tek bir saklanmış ham artefact'ı ancak yol kontrollü raw root
# TR: altında kalıyorsa ve gerçekten okunabiliyorsa okur.
def read_controlled_raw_artefact_bytes(
    *,
    action: str,
    target_kind: str,
    target_id: int,
    requested_url: str | None,
    final_url: str | None,
    content_type: str | None,
    body_bytes: int | None,
    raw_storage_path: str,
    raw_sha256: str | None,
    fetched_at: str | None,
) -> tuple[Path, bytes] | dict[str, object]:
    # EN: We resolve the controlled raw root once so containment checks stay
    # EN: explicit and path-normalized.
    # TR: Kapsama kontrolleri açık ve path-normalize kalsın diye kontrollü raw
    # TR: root'u bir kez resolve ediyoruz.
    controlled_root = RAW_FETCH_ROOT.resolve()

    # EN: We resolve the target artefact path without requiring existence first,
    # EN: because we want to distinguish path-shape problems from missing-file problems.
    # TR: Hedef artefact yolunu önce varlık zorunluluğu olmadan resolve ediyoruz;
    # TR: çünkü yol-şekli sorunlarını eksik-dosya sorunlarından ayırmak istiyoruz.
    try:
        resolved_path = Path(raw_storage_path).expanduser().resolve(strict=False)
    except Exception as exc:
        return build_acquisition_contract_degraded_payload(
            action=action,
            target_kind=target_kind,
            target_id=target_id,
            requested_url=requested_url,
            final_url=final_url,
            content_type=content_type,
            body_bytes=body_bytes,
            raw_storage_path=raw_storage_path,
            raw_sha256=raw_sha256,
            fetched_at=fetched_at,
            error_class=f"{target_kind}_raw_storage_path_unresolvable",
            error_message=f"Raw artefact path could not be resolved: {exc}",
        )

    # EN: The artefact must stay under the controlled raw root. Anything outside
    # EN: that boundary is operationally unsafe and must be rejected.
    # TR: Artefact kontrollü raw root altında kalmalıdır. Bu sınırın dışındaki
    # TR: her şey operasyonel olarak güvensizdir ve reddedilmelidir.
    try:
        resolved_path.relative_to(controlled_root)
    except ValueError:
        return build_acquisition_contract_degraded_payload(
            action=action,
            target_kind=target_kind,
            target_id=target_id,
            requested_url=requested_url,
            final_url=final_url,
            content_type=content_type,
            body_bytes=body_bytes,
            raw_storage_path=str(resolved_path),
            raw_sha256=raw_sha256,
            fetched_at=fetched_at,
            error_class=f"{target_kind}_raw_artefact_outside_controlled_root",
            error_message=(
                "Raw artefact path is outside controlled raw root: "
                f"path={resolved_path} root={controlled_root}"
            ),
        )

    # EN: After containment is confirmed, the artefact must exist as a real file.
    # TR: Kapsama doğrulandıktan sonra artefact gerçek bir dosya olarak var olmalıdır.
    if not resolved_path.is_file():
        return build_acquisition_contract_degraded_payload(
            action=action,
            target_kind=target_kind,
            target_id=target_id,
            requested_url=requested_url,
            final_url=final_url,
            content_type=content_type,
            body_bytes=body_bytes,
            raw_storage_path=str(resolved_path),
            raw_sha256=raw_sha256,
            fetched_at=fetched_at,
            error_class=f"{target_kind}_raw_artefact_missing",
            error_message=f"Raw artefact is missing on disk: {resolved_path}",
        )

    # EN: We read the bytes inside an explicit OSError guard so permission or I/O
    # EN: failures degrade cleanly instead of crashing the validator.
    # TR: Permission veya I/O hataları validator'ı çökertmek yerine temiz biçimde
    # TR: degrade olsun diye byte'ları açık OSError koruması içinde okuyoruz.
    try:
        raw_bytes = resolved_path.read_bytes()
    except OSError as exc:
        return build_acquisition_contract_degraded_payload(
            action=action,
            target_kind=target_kind,
            target_id=target_id,
            requested_url=requested_url,
            final_url=final_url,
            content_type=content_type,
            body_bytes=body_bytes,
            raw_storage_path=str(resolved_path),
            raw_sha256=raw_sha256,
            fetched_at=fetched_at,
            error_class=f"{target_kind}_raw_artefact_unreadable",
            error_message=f"Raw artefact could not be read: {exc}",
        )

    # EN: Successful validation of the raw-file boundary returns the normalized
    # EN: resolved path plus exact bytes.
    # TR: Ham dosya sınırının başarılı doğrulaması normalize edilmiş resolve path
    # TR: ile tam byte içeriğini döndürür.
    return (resolved_path, raw_bytes)


# EN: This helper validates one fetched-page result against the persisted raw
# EN: artefact so later worker stages do not trust corrupted metadata blindly.
# TR: Bu yardımcı tek bir fetched-page sonucunu saklanan ham artefact ile
# TR: doğrular; böylece sonraki worker aşamaları bozuk metadata'ya körü körüne güvenmez.
def validate_fetched_page_result_contract(
    fetched_page: FetchedPageResult,
) -> dict[str, object] | None:
    # EN: requested_url must stay non-empty because it anchors later evidence.
    # TR: requested_url daha sonraki kanıtı sabitlediği için boş kalmamalıdır.
    if not str(fetched_page.requested_url).strip():
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=int(fetched_page.body_bytes),
            raw_storage_path=str(fetched_page.raw_storage_path),
            raw_sha256=str(fetched_page.raw_sha256),
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_requested_url_empty",
            error_message="FetchedPageResult.requested_url is empty",
        )

    # EN: final_url must stay visible and non-empty after acquisition.
    # TR: final_url acquisition sonrasında görünür ve boş olmayan bir değer olmalıdır.
    if not str(fetched_page.final_url).strip():
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=int(fetched_page.body_bytes),
            raw_storage_path=str(fetched_page.raw_storage_path),
            raw_sha256=str(fetched_page.raw_sha256),
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_final_url_empty",
            error_message="FetchedPageResult.final_url is empty",
        )

    # EN: fetched_at must stay ISO-parseable because later DB layers and audits
    # EN: depend on this timestamp.
    # TR: fetched_at ISO olarak parse edilebilir kalmalıdır; çünkü sonraki DB
    # TR: katmanları ve audit'ler bu zaman damgasına dayanır.
    try:
        datetime.fromisoformat(str(fetched_page.fetched_at))
    except Exception as exc:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=int(fetched_page.body_bytes),
            raw_storage_path=str(fetched_page.raw_storage_path),
            raw_sha256=str(fetched_page.raw_sha256),
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_fetched_at_invalid",
            error_message=f"FetchedPageResult.fetched_at is not ISO-parseable: {exc}",
        )

    # EN: raw_storage_path must point to a real persisted file.
    # TR: raw_storage_path gerçek bir saklanmış dosyayı göstermelidir.
    raw_storage_path = str(fetched_page.raw_storage_path).strip()
    if not raw_storage_path:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=int(fetched_page.body_bytes),
            raw_storage_path=str(fetched_page.raw_storage_path),
            raw_sha256=str(fetched_page.raw_sha256),
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_raw_storage_path_empty",
            error_message="FetchedPageResult.raw_storage_path is empty",
        )

    controlled_read_result = read_controlled_raw_artefact_bytes(
        action="validate_fetched_page_result_contract",
        target_kind="page",
        target_id=int(fetched_page.url_id),
        requested_url=str(fetched_page.requested_url),
        final_url=str(fetched_page.final_url),
        content_type=fetched_page.content_type,
        body_bytes=int(fetched_page.body_bytes),
        raw_storage_path=raw_storage_path,
        raw_sha256=str(fetched_page.raw_sha256),
        fetched_at=str(fetched_page.fetched_at),
    )
    if isinstance(controlled_read_result, dict):
        return controlled_read_result

    path, raw_bytes = controlled_read_result
    raw_storage_path = str(path)

    # EN: raw_sha256 must look like a full SHA256 hex digest.
    # TR: raw_sha256 tam bir SHA256 hex özeti gibi görünmelidir.
    raw_sha256 = str(fetched_page.raw_sha256).strip().lower()
    if len(raw_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in raw_sha256):
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=int(fetched_page.body_bytes),
            raw_storage_path=raw_storage_path,
            raw_sha256=str(fetched_page.raw_sha256),
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_raw_sha256_invalid",
            error_message="FetchedPageResult.raw_sha256 is empty or malformed",
        )

    # EN: We verify the persisted bytes directly so metadata cannot drift away from
    # EN: the real file on disk.
    # TR: Metadata diskteki gerçek dosyadan kopamasın diye saklanan byte'ları
    # TR: doğrudan doğruluyoruz.
    actual_body_bytes = len(raw_bytes)
    expected_body_bytes = int(fetched_page.body_bytes)

    if actual_body_bytes != expected_body_bytes:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=expected_body_bytes,
            raw_storage_path=raw_storage_path,
            raw_sha256=raw_sha256,
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_body_bytes_mismatch",
            error_message=(
                "FetchedPageResult.body_bytes does not match persisted file size: "
                f"expected={expected_body_bytes} actual={actual_body_bytes}"
            ),
        )

    actual_sha256 = sha256_hex(raw_bytes)
    if actual_sha256 != raw_sha256:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_page_result_contract",
            target_kind="page",
            target_id=int(fetched_page.url_id),
            requested_url=str(fetched_page.requested_url),
            final_url=str(fetched_page.final_url),
            content_type=fetched_page.content_type,
            body_bytes=expected_body_bytes,
            raw_storage_path=raw_storage_path,
            raw_sha256=raw_sha256,
            fetched_at=str(fetched_page.fetched_at),
            error_class="fetched_page_raw_sha256_mismatch",
            error_message=(
                "FetchedPageResult.raw_sha256 does not match persisted file digest: "
                f"expected={raw_sha256} actual={actual_sha256}"
            ),
        )

    # EN: No payload means the page contract is currently valid.
    # TR: Payload dönmemesi page contract'ının şu anda geçerli olduğu anlamına gelir.
    return None


# EN: This helper validates one fetched-robots result against the persisted raw
# EN: artefact or against the transport-failure contract when no body exists.
# TR: Bu yardımcı tek bir fetched-robots sonucunu saklanan ham artefact ile ya da
# TR: body yoksa transport-failure sözleşmesi ile doğrular.
def validate_fetched_robots_result_contract(
    robots_fetch: FetchedRobotsTxtResult,
) -> dict[str, object] | None:
    # EN: robots_url must stay non-empty because it is the durable cache target.
    # TR: robots_url kalıcı cache hedefi olduğu için boş kalmamalıdır.
    if not str(robots_fetch.robots_url).strip():
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=int(robots_fetch.body_bytes),
            raw_storage_path=None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path),
            raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_url_empty",
            error_message="FetchedRobotsTxtResult.robots_url is empty",
        )

    # EN: final_url must stay visible even on HTTP error responses.
    # TR: final_url HTTP hata yanıtlarında bile görünür kalmalıdır.
    if not str(robots_fetch.final_url).strip():
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=int(robots_fetch.body_bytes),
            raw_storage_path=None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path),
            raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_final_url_empty",
            error_message="FetchedRobotsTxtResult.final_url is empty",
        )

    # EN: fetched_at must stay ISO-parseable.
    # TR: fetched_at ISO olarak parse edilebilir kalmalıdır.
    try:
        datetime.fromisoformat(str(robots_fetch.fetched_at))
    except Exception as exc:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=int(robots_fetch.body_bytes),
            raw_storage_path=None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path),
            raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_fetched_at_invalid",
            error_message=f"FetchedRobotsTxtResult.fetched_at is not ISO-parseable: {exc}",
        )

    # EN: Transport failures are valid only when no body artefact exists and byte
    # EN: count stays zero.
    # TR: Transport hataları yalnızca body artefact'ı yoksa ve byte sayısı sıfırsa
    # TR: geçerli kabul edilir.
    if robots_fetch.fetch_error_class is not None:
        if (
            robots_fetch.raw_storage_path is not None
            or robots_fetch.raw_sha256 is not None
            or int(robots_fetch.body_bytes) != 0
        ):
            return build_acquisition_contract_degraded_payload(
                action="validate_fetched_robots_result_contract",
                target_kind="robots",
                target_id=int(robots_fetch.host_id),
                requested_url=str(robots_fetch.robots_url),
                final_url=str(robots_fetch.final_url),
                content_type=robots_fetch.content_type,
                body_bytes=int(robots_fetch.body_bytes),
                raw_storage_path=None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path),
                raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
                fetched_at=str(robots_fetch.fetched_at),
                error_class="fetched_robots_transport_contract_invalid",
                error_message=(
                    "FetchedRobotsTxtResult transport-failure contract is inconsistent "
                    "(body/path/hash should be empty)"
                ),
            )
        return None

    # EN: Body-present robots results must have a persisted raw file and a valid digest.
    # TR: Body içeren robots sonuçlarında saklanan ham dosya ve geçerli digest olmalıdır.
    raw_storage_path = None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path).strip()
    if not raw_storage_path:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=int(robots_fetch.body_bytes),
            raw_storage_path=None if robots_fetch.raw_storage_path is None else str(robots_fetch.raw_storage_path),
            raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_raw_storage_path_empty",
            error_message="FetchedRobotsTxtResult.raw_storage_path is empty for body-present result",
        )

    controlled_read_result = read_controlled_raw_artefact_bytes(
        action="validate_fetched_robots_result_contract",
        target_kind="robots",
        target_id=int(robots_fetch.host_id),
        requested_url=str(robots_fetch.robots_url),
        final_url=str(robots_fetch.final_url),
        content_type=robots_fetch.content_type,
        body_bytes=int(robots_fetch.body_bytes),
        raw_storage_path=raw_storage_path,
        raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
        fetched_at=str(robots_fetch.fetched_at),
    )
    if isinstance(controlled_read_result, dict):
        return controlled_read_result

    path, raw_bytes = controlled_read_result
    raw_storage_path = str(path)

    raw_sha256 = None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256).strip().lower()
    if raw_sha256 is None or len(raw_sha256) != 64 or any(ch not in "0123456789abcdef" for ch in raw_sha256):
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=int(robots_fetch.body_bytes),
            raw_storage_path=raw_storage_path,
            raw_sha256=None if robots_fetch.raw_sha256 is None else str(robots_fetch.raw_sha256),
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_raw_sha256_invalid",
            error_message="FetchedRobotsTxtResult.raw_sha256 is empty or malformed",
        )

    actual_body_bytes = len(raw_bytes)
    expected_body_bytes = int(robots_fetch.body_bytes)

    if actual_body_bytes != expected_body_bytes:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=expected_body_bytes,
            raw_storage_path=raw_storage_path,
            raw_sha256=raw_sha256,
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_body_bytes_mismatch",
            error_message=(
                "FetchedRobotsTxtResult.body_bytes does not match persisted file size: "
                f"expected={expected_body_bytes} actual={actual_body_bytes}"
            ),
        )

    actual_sha256 = sha256_hex(raw_bytes)
    if actual_sha256 != raw_sha256:
        return build_acquisition_contract_degraded_payload(
            action="validate_fetched_robots_result_contract",
            target_kind="robots",
            target_id=int(robots_fetch.host_id),
            requested_url=str(robots_fetch.robots_url),
            final_url=str(robots_fetch.final_url),
            content_type=robots_fetch.content_type,
            body_bytes=expected_body_bytes,
            raw_storage_path=raw_storage_path,
            raw_sha256=raw_sha256,
            fetched_at=str(robots_fetch.fetched_at),
            error_class="fetched_robots_raw_sha256_mismatch",
            error_message=(
                "FetchedRobotsTxtResult.raw_sha256 does not match persisted file digest: "
                f"expected={raw_sha256} actual={actual_sha256}"
            ),
        )

    # EN: No payload means the robots fetch contract is currently valid.
    # TR: Payload dönmemesi robots fetch contract'ının şu anda geçerli olduğu anlamına gelir.
    return None


# EN: This helper returns the current UTC time as a real datetime object.
# TR: Bu yardımcı mevcut UTC zamanını gerçek bir datetime nesnesi olarak döndürür.
def utc_now() -> datetime:
    # EN: We explicitly use timezone.utc so no local-machine timezone ambiguity leaks in.
    # TR: Yerel makine saat dilimi belirsizliği sızmasın diye açıkça timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc)

# EN: This helper formats a UTC timestamp as an ISO-8601 string.
# TR: Bu yardımcı UTC zaman damgasını ISO-8601 metni olarak biçimlendirir.
def utc_now_iso() -> str:
    # EN: We delegate to utc_now() so all current-time generation stays consistent.
    # TR: Tüm mevcut-zaman üretimi tutarlı kalsın diye utc_now() yardımcısını kullanıyoruz.
    return utc_now().isoformat()

# EN: This helper turns a datetime into a compact filesystem-safe UTC timestamp.
# TR: Bu yardımcı bir datetime değerini filesystem için güvenli, kompakt bir UTC
# TR: zaman damgasına dönüştürür.
def utc_path_stamp(moment: datetime) -> str:
    # EN: We use a compact YYYYMMDDTHHMMSSZ shape because it is easy to sort lexically.
    # TR: Leksik olarak kolay sıralandığı için kompakt YYYYMMDDTHHMMSSZ biçimini kullanıyoruz.
    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# EN: This helper reads one field from a claimed_url object in a tolerant way.
# EN: The current worker surfaces may hand us either an attribute-style object or a dict-like object.
# TR: Bu yardımcı claimed_url nesnesinden bir alanı toleranslı biçimde okur.
# TR: Güncel worker yüzeyleri bize attribute-stili bir nesne veya dict-benzeri bir nesne verebilir.
def get_claimed_url_value(claimed_url: object, field_name: str) -> object:
    # EN: If claimed_url is a dict, we read the key directly.
    # TR: claimed_url bir dict ise anahtarı doğrudan okuyoruz.
    if isinstance(claimed_url, dict):
        if field_name not in claimed_url:
            raise KeyError(f"claimed_url is missing key: {field_name}")
        return claimed_url[field_name]

    # EN: Otherwise we try attribute access because current DB helper surfaces may
    # EN: return row-like objects with named attributes.
    # TR: Aksi durumda attribute erişimini deniyoruz; çünkü güncel DB yardımcı
    # TR: yüzeyleri isimli alanları olan row-benzeri nesneler döndürebilir.
    if not hasattr(claimed_url, field_name):
        raise AttributeError(f"claimed_url is missing attribute: {field_name}")

    # EN: We return the discovered attribute value.
    # TR: Bulunan attribute değerini döndürüyoruz.
    return getattr(claimed_url, field_name)

# EN: This helper creates the raw fetch storage path for one fetched page body.
# TR: Bu yardımcı tek bir fetch edilmiş page body için raw fetch storage yolunu oluşturur.
def build_raw_fetch_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: We create one deterministic filename that includes the frontier url id
    # EN: and the UTC fetch timestamp.
    # TR: Frontier url id'sini ve UTC fetch zaman damgasını içeren deterministik
    # TR: tek bir dosya adı oluşturuyoruz.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.body.bin"

    # EN: We return the final full path object.
    # TR: Nihai tam path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper builds the deterministic raw-storage path for one robots.txt body.
# TR: Bu yardımcı tek bir robots.txt body için deterministik ham-saklama yolunu kurar.
def build_raw_robots_storage_path(
    *,
    host_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename carries host identity plus UTC timestamp so later audits can
    # EN: connect the artefact back to the exact host-level robots refresh.
    # TR: Dosya adı host kimliğini ve UTC zaman damgasını taşır; böylece sonraki
    # TR: audit'ler artefact'ı tam host-seviyesi robots refresh işlemine bağlayabilir.
    filename = f"host_{host_id}_robots_{utc_path_stamp(fetched_at)}.body.bin"

    # EN: We return the final full path object.
    # TR: Nihai tam path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper builds the raw HTML storage path for one browser-rendered page fetch.
# EN: We keep it next to the direct-HTTP raw artefacts so the acquisition family stays
# EN: physically inspectable under the same controlled raw root.
# TR: Bu yardımcı, tek bir browser-rendered page fetch işlemi için ham HTML saklama
# TR: yolunu üretir. Acquisition ailesi aynı kontrollü raw root altında fiziksel olarak
# TR: incelenebilir kalsın diye bunu direct-HTTP ham artefact'larının yanında tutuyoruz.
def build_browser_rendered_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We reuse the same UTC year/month/day partitioning strategy so browser-backed
    # EN: artefacts stay sortable and operationally consistent with direct fetch artefacts.
    # TR: Browser-backed artefact'lar direct fetch artefact'larıyla sıralanabilir ve
    # TR: operasyonel olarak tutarlı kalsın diye aynı UTC year/month/day bölme stratejisini kullanıyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename explicitly says this is a rendered HTML body, not the original wire body.
    # TR: Dosya adı bunun orijinal wire body değil, rendered HTML body olduğunu açıkça söyler.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.rendered.html"

    # EN: We return the final full Path object.
    # TR: Nihai tam Path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper builds the screenshot evidence path that belongs to the same browser fetch.
# EN: We keep screenshot and rendered HTML as sibling artefacts with the same timestamp stem.
# TR: Bu yardımcı, aynı browser fetch'e ait screenshot kanıt yolunu üretir.
# TR: Screenshot ve rendered HTML'i aynı zaman damgalı köke sahip kardeş artefact'lar olarak tutuyoruz.
def build_browser_screenshot_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We use the same UTC day partitioning as every other raw acquisition artefact.
    # TR: Diğer tüm ham acquisition artefact'larıyla aynı UTC gün bölmesini kullanıyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename explicitly marks this sibling artefact as a screenshot.
    # TR: Dosya adı bu kardeş artefact'ın screenshot olduğunu açıkça işaretler.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.screenshot.png"

    # EN: We return the final full Path object.
    # TR: Nihai tam Path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper ensures the parent directory of a target file exists.
# TR: Bu yardımcı hedef dosyanın parent dizininin var olduğundan emin olur.
def ensure_parent_directory(path: Path) -> None:
    # EN: parents=True lets deeper missing directories be created in one step.
    # TR: parents=True daha derindeki eksik dizinlerin tek adımda oluşturulmasını sağlar.
    path.parent.mkdir(parents=True, exist_ok=True)

# EN: This helper computes the SHA256 hex digest of raw bytes.
# TR: Bu yardımcı ham byte'ların SHA256 hex özetini hesaplar.
def sha256_hex(data: bytes) -> str:
    # EN: We use hashlib.sha256 because later pipeline layers need a stable body fingerprint.
    # TR: Sonraki pipeline katmanları kararlı bir body parmak izine ihtiyaç duyduğu için hashlib.sha256 kullanıyoruz.
    return hashlib.sha256(data).hexdigest()

# EN: This export list keeps the shared support surface explicit.
# TR: Bu export listesi paylaşılan destek yüzeyini açık tutar.
__all__ = [
    "RAW_FETCH_ROOT",
    "FetchedPageResult",
    "FetchedRobotsTxtResult",
    "utc_now",
    "utc_now_iso",
    "utc_path_stamp",
    "get_claimed_url_value",
    "build_raw_fetch_storage_path",
    "build_raw_robots_storage_path",
    "build_browser_rendered_storage_path",
    "build_browser_screenshot_storage_path",
    "ensure_parent_directory",
    "sha256_hex",
]
