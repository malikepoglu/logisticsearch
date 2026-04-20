# EN: This module owns worker-side terminal fetch-attempt logging plus durable
# EN: error finalization helpers after the controlled worker-runtime split.
# TR: Bu modül kontrollü worker-runtime split’inden sonra worker-tarafı terminal
# TR: fetch-attempt loglamasını ve kalıcı hata finalization yardımcılarını sahiplenir.

from __future__ import annotations

# EN: We import the stable acquisition-family public surface because finalize
# EN: helpers need claimed-url field access plus the fetched-page contract shape.
# TR: Finalize yardımcıları claimed-url alan erişimine ve fetched-page sözleşme
# TR: şekline ihtiyaç duyduğu için kararlı acquisition-aile public yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    FetchedPageResult,
    get_claimed_url_value,
)

# EN: We import the worker support helper that builds explicit metadata for
# EN: durable per-attempt logging.
# TR: Kalıcı deneme-bazlı loglama için açık metadata üreten worker destek
# TR: yardımcısını içe aktarıyoruz.
from .logisticsearch1_1_2_1_worker_runtime_support import (
    build_terminal_fetch_attempt_metadata,
)

# EN: We import the canonical DB gateway finalize/log wrappers because Python
# EN: must stay aligned with the sealed SQL contract.
# TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye kanonik DB
# TR: gateway finalize/log wrapper’larını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    log_fetch_attempt_terminal,
)


# EN: This helper writes one terminal fetch-attempt row using only the fields the
# EN: current worker surface honestly knows at log time.
# TR: Bu yardımcı log anında worker yüzeyinin dürüstçe bildiği alanları kullanarak
# TR: tek bir terminal fetch-attempt satırı yazar.
def log_fetch_attempt_terminal_from_worker(
    conn,
    *,
    claimed_url: object,
    worker_id: str,
    outcome: str,
    note: str,
    acquisition_method: str | None,
    fetched_page: FetchedPageResult | None = None,
    error_class: str | None = None,
    error_message: str | None = None,
) -> dict[str, object]:
    # EN: We extract the exact frontier identities so the durable log row stays
    # EN: anchored to the same leased work item.
    # TR: Kalıcı log satırı aynı leased iş öğesine bağlı kalsın diye tam frontier
    # TR: kimliklerini çıkarıyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    host_id = int(get_claimed_url_value(claimed_url, "host_id"))
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))
    request_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We start with the minimum field set always visible in the worker.
    # TR: Worker’da her zaman görünür olan asgari alan kümesiyle başlıyoruz.
    payload = {
        "url_id": url_id,
        "host_id": host_id,
        "worker_id": worker_id,
        "request_url": request_url,
        "outcome": outcome,
        "fetch_kind": "page",
        "lease_token": lease_token,
        "request_method": "GET",
        "final_url": request_url,
        "http_status": None,
        "content_type": None,
        "content_length": None,
        "body_storage_path": None,
        "body_sha256": None,
        "body_bytes": None,
        "etag": None,
        "last_modified": None,
        "error_class": error_class,
        "error_message": error_message,
        "fetch_metadata": build_terminal_fetch_attempt_metadata(
            claimed_url=claimed_url,
            acquisition_method=acquisition_method,
            note=note,
        ),
    }

    # EN: When a real fetched-page artefact exists, we enrich the payload with
    # EN: honest response/storage fields.
    # TR: Gerçek bir fetched-page artefact’ı varsa payload’ı dürüst response ve
    # TR: storage alanlarıyla zenginleştiriyoruz.
    if fetched_page is not None:
        payload.update(
            {
                "final_url": fetched_page.final_url,
                "http_status": fetched_page.http_status,
                "content_type": fetched_page.content_type,
                "content_length": fetched_page.body_bytes,
                "body_storage_path": fetched_page.raw_storage_path,
                "body_sha256": fetched_page.raw_sha256,
                "body_bytes": fetched_page.body_bytes,
                "etag": fetched_page.etag,
                "last_modified": fetched_page.last_modified,
            }
        )

    # EN: We delegate the durable insert to the canonical DB gateway helper.
    # TR: Kalıcı insert işlemini kanonik DB gateway yardımcısına devrediyoruz.
    return log_fetch_attempt_terminal(
        conn,
        **payload,
    )


# EN: This helper classifies HTTP status failures into the minimal retryable vs
# EN: permanent buckets currently used by the worker.
# TR: Bu yardımcı HTTP durum hatalarını worker’ın şu anda kullandığı minimal
# TR: retryable ve permanent kovalarına ayırır.
def classify_http_status_failure(http_status: int) -> tuple[str, bool]:
    # EN: These status codes are usually transient overload/timeout/upstream
    # EN: failures, so the minimal layer treats them as retryable.
    # TR: Bu durum kodları genelde geçici aşırı yük/timeout/upstream hatalarıdır;
    # TR: bu yüzden minimal katman onları retryable kabul eder.
    if http_status in {408, 425, 429, 500, 502, 503, 504}:
        return ("http_retryable_status", True)

    # EN: All remaining HTTP failures are treated as permanent by this first
    # EN: narrow worker layer.
    # TR: Kalan tüm HTTP hataları bu ilk dar worker katmanı tarafından permanent
    # TR: kabul edilir.
    return ("http_permanent_status", False)


# EN: This helper finalizes a robots-blocked claim as a permanent outcome.
# TR: Bu yardımcı robots tarafından engellenen bir claim’i permanent sonuç olarak
# TR: finalize eder.
def finalize_robots_block(
    conn,
    *,
    claimed_url: object,
    robots_allow_decision: dict | None,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We read the visible verdict so the stored error stays explicit.
    # TR: Saklanan hata açık kalsın diye görünür verdict’i okuyoruz.
    verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")
    error_message = f"robots verdict forbids fetch: {verdict}"

    # EN: We first persist one terminal per-attempt row for audit visibility.
    # TR: Audit görünürlüğü oluşsun diye önce tek bir terminal deneme satırı
    # TR: yazıyoruz.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="blocked_robots",
        note="worker runtime robots-blocked finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="robots_blocked",
        error_message=error_message,
    )

    # EN: We then finalize the frontier row through the permanent wrapper.
    # TR: Ardından frontier satırını permanent wrapper üzerinden finalize ediyoruz.
    finalize_result = finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="robots_blocked",
        error_message=error_message,
    )

    # EN: We merge durable fetch-attempt evidence into the returned payload.
    # TR: Kalıcı fetch-attempt kanıtını dönen payload’a birleştiriyoruz.
    return {
        **dict(finalize_result),
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This helper finalizes an HTTP error according to the current minimal
# EN: retryable/permanent rule.
# TR: Bu yardımcı bir HTTP hatasını mevcut minimal retryable/permanent kuralına
# TR: göre finalize eder.
def finalize_http_error(
    conn,
    *,
    claimed_url: object,
    http_status: int,
    error_message: str,
    worker_id: str,
) -> dict[str, object]:
    # EN: We classify the HTTP status first so the branch stays explicit.
    # TR: Branch açık kalsın diye önce HTTP durumunu sınıflandırıyoruz.
    error_class, is_retryable = classify_http_status_failure(http_status)

    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We persist one terminal fetch-attempt row before frontier finalization.
    # TR: Frontier finalization’dan önce tek bir terminal fetch-attempt satırı
    # TR: yazıyoruz.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="retryable_error" if is_retryable else "permanent_error",
        note="worker runtime HTTPError finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class=error_class,
        error_message=error_message,
    )

    # EN: Retryable statuses go through the retryable finalize wrapper.
    # TR: Retryable durumlar retryable finalize wrapper üzerinden gider.
    if is_retryable:
        finalize_result = finish_fetch_retryable_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=error_class,
            error_message=error_message,
            retry_delay=None,
        )
    else:
        # EN: All remaining HTTP failure statuses go through the permanent wrapper.
        # TR: Kalan tüm HTTP hata durumları permanent wrapper üzerinden gider.
        finalize_result = finish_fetch_permanent_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=error_class,
            error_message=error_message,
        )

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **dict(finalize_result),
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This helper finalizes a transport-layer failure as retryable.
# TR: Bu yardımcı bir taşıma-katmanı hatasını retryable olarak finalize eder.
def finalize_transport_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We separate timeout-like text from broader network failure text so the
    # EN: durable fetch-attempt row stays more informative.
    # TR: Kalıcı fetch-attempt satırı daha bilgilendirici kalsın diye timeout-benzeri
    # TR: metni daha genel ağ hatasından ayırıyoruz.
    normalized_error_message = error_message.lower()
    transport_outcome = "timeout" if "timeout" in normalized_error_message else "network_error"

    # EN: We persist one terminal per-attempt row before frontier finalization.
    # TR: Frontier finalization’dan önce tek bir terminal deneme satırı yazıyoruz.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome=transport_outcome,
        note="worker runtime transport-error finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="transport_retryable_error",
        error_message=error_message,
    )

    # EN: Transport failures are treated as retryable in this minimal layer.
    # TR: Taşıma hataları bu minimal katmanda retryable kabul edilir.
    finalize_result = finish_fetch_retryable_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="transport_retryable_error",
        error_message=error_message,
        retry_delay=None,
    )

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **dict(finalize_result),
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This helper finalizes an unexpected runtime failure as permanent.
# TR: Bu yardımcı beklenmeyen bir runtime hatasını permanent olarak finalize eder.
def finalize_unexpected_runtime_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We first persist one terminal fetch-attempt row.
    # TR: Önce tek bir terminal fetch-attempt satırı yazıyoruz.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="permanent_error",
        note="worker runtime unexpected-error finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="unexpected_fetch_runtime_error",
        error_message=error_message,
    )

    # EN: Unknown runtime failures are treated as permanent so the minimal layer
    # EN: fails loudly instead of hiding drift.
    # TR: Minimal katman drift’i gizlemek yerine yüksek sesle hata versin diye
    # TR: bilinmeyen runtime hataları permanent kabul edilir.
    try:
        finalize_result = finish_fetch_permanent_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="unexpected_fetch_runtime_error",
            error_message=error_message,
        )
        finalize_result_payload = dict(finalize_result)

    # EN: A no-row finalize result must not crash the worker again. We degrade the
    # EN: payload into an operator-visible unresolved state and keep the fetch-attempt
    # EN: evidence that was already written in this transaction.
    # TR: Finalize fonksiyonunun satır döndürmemesi worker’ı yeniden çökertmemelidir.
    # TR: Payload’ı operatör-görünür çözülmemiş duruma düşürüyor ve bu transaction içinde
    # TR: zaten yazılmış fetch-attempt kanıtını koruyoruz.
    except RuntimeError as exc:
        if "frontier.finish_fetch_permanent_error(...) returned no row" not in str(exc):
            raise

        finalize_result_payload = {
            "url_id": url_id,
            "lease_token": lease_token,
            "http_status": None,
            "error_class": "unexpected_fetch_runtime_error_finalize_no_row",
            "error_message": f"{error_message} | finalize_no_row: {exc}",
            "finalize_degraded": True,
            "finalize_degraded_reason": "frontier_finish_fetch_permanent_error_returned_no_row",
            "finalize_completed": False,
        }

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **finalize_result_payload,
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This explicit export list documents the public finalize child surface.
# TR: Bu açık export listesi public finalize alt yüzeyini belgelendirir.
__all__ = [
    "log_fetch_attempt_terminal_from_worker",
    "classify_http_status_failure",
    "finalize_robots_block",
    "finalize_http_error",
    "finalize_transport_error",
    "finalize_unexpected_runtime_error",
]
