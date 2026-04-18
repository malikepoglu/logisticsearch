# EN: This module is the browser-backed page-acquisition child surface.
# EN: It adapts the deeper browser runtime into the same stable FetchedPageResult
# EN: contract already used by the rest of crawler_core.
# TR: Bu modül browser-backed page-acquisition alt yüzeyidir.
# TR: Daha derindeki browser runtime yüzeyini crawler_core'un geri kalanının zaten
# TR: kullandığı aynı kararlı FetchedPageResult sözleşmesine uyarlar.

from __future__ import annotations

# EN: We import Path because the child surface exposes a configurable raw_root
# EN: path in its explicit function signature.
# TR: Bu alt yüzey açık fonksiyon imzasında yapılandırılabilir raw_root yolu
# TR: sunduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import the shared acquisition support surface so this child reuses the
# EN: same stable artefact/result contract as the rest of the acquisition family.
# TR: Bu alt yüzey acquisition ailesinin geri kalanıyla aynı kararlı artefact/sonuç
# TR: sözleşmesini yeniden kullansın diye paylaşılan acquisition destek yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedPageResult,
    build_browser_rendered_storage_path,
    build_browser_screenshot_storage_path,
    ensure_parent_directory,
    get_claimed_url_value,
    sha256_hex,
    utc_now,
)


# EN: This helper extracts the most relevant document-level HTTP status from the
# EN: browser network evidence collected by the canonical browser runtime.
# EN: We intentionally keep the rule narrow: first successful document-style record wins.
# TR: Bu yardımcı, kanonik browser runtime tarafından toplanan browser network evidence
# TR: içinden en anlamlı document-seviyesi HTTP durumunu çıkarır.
# TR: Kuralı bilinçli olarak dar tutuyoruz: ilk uygun document-türü kayıt kazanır.
def infer_browser_document_status(browser_result: object) -> int:
    # EN: We read network_records tolerantly because the browser runtime returns dataclass-like
    # EN: structures that are later serialized, and we only need a small stable subset here.
    # TR: Yalnızca küçük ve kararlı bir alt kümeye ihtiyaç duyduğumuz için network_records alanını
    # TR: toleranslı biçimde okuyoruz; browser runtime dataclass-benzeri yapılar döndürüyor olabilir.
    network_records = getattr(browser_result, "network_records", []) or []

    # EN: We scan records in observed order and prefer a document resource with an integer status.
    # TR: Kayıtları gözlenme sırasıyla tarıyor ve integer status taşıyan bir document resource'u tercih ediyoruz.
    for record in network_records:
        resource_type = getattr(record, "resource_type", None)
        status = getattr(record, "status", None)
        if resource_type == "document" and isinstance(status, int):
            return status

    # EN: If browser navigation succeeded but no explicit document status was surfaced,
    # EN: we conservatively fall back to 200 because we do have a rendered HTML result.
    # TR: Browser navigasyonu başarılı olduğu halde açık bir document status yüzeye çıkmadıysa,
    # TR: elimizde rendered HTML sonucu bulunduğu için muhafazakâr biçimde 200'e düşüyoruz.
    return 200

# EN: This function performs one browser-backed public page fetch and persists the
# EN: rendered HTML under the same raw acquisition tree used by the direct HTTP path.
# EN: The whole point is not to replace the browser runtime surface, but to let the
# EN: fetch layer expose a browser-backed acquisition result in the same FetchedPageResult
# EN: contract shape already understood by the rest of crawler_core.
# TR: Bu fonksiyon tek bir browser-backed public page fetch işlemi yapar ve rendered HTML'i
# TR: direct HTTP yolunun kullandığı aynı raw acquisition ağacı altında kalıcılaştırır.
# TR: Amaç browser runtime yüzeyini ortadan kaldırmak değil, fetch katmanının crawler_core'un
# TR: geri kalanı tarafından zaten anlaşılan aynı FetchedPageResult sözleşme şekli içinde
# TR: browser-backed acquisition sonucu döndürebilmesini sağlamaktır.
def fetch_page_with_browser_to_raw_storage(
    claimed_url: object,
    *,
    timeout_ms: int = 30000,
    wait_until: str = "networkidle",
    raw_root: Path = RAW_FETCH_ROOT,
    headless: bool = True,
) -> FetchedPageResult:
    # EN: We import the canonical browser acquisition function locally so this narrow adapter
    # EN: does not force a broader import rewrite at the top of the file.
    # TR: Bu dar adapter, dosyanın üst tarafında daha geniş bir import yeniden düzenlemesi
    # TR: zorlamasın diye kanonik browser acquisition fonksiyonunu burada lokal içe aktarıyoruz.
    from .logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime import acquire_public_page_with_browser

    # EN: We read the claimed frontier url id because the rendered artefacts must stay
    # EN: directly traceable to one frontier work item.
    # TR: Rendered artefact'lar tek bir frontier iş öğesine doğrudan izlenebilir kalsın diye
    # TR: claim edilmiş frontier url kimliğini okuyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))

    # EN: We read the requested canonical URL because it is the real browser target.
    # TR: Gerçek browser hedefi olduğu için istenen canonical URL'yi okuyoruz.
    requested_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We capture the current UTC fetch time before browser work starts so all generated
    # EN: artefacts share the same deterministic timestamp stem.
    # TR: Üretilen tüm artefact'lar aynı deterministik zaman damgası kökünü paylaşsın diye
    # TR: browser işi başlamadan önce mevcut UTC fetch zamanını yakalıyoruz.
    fetched_at = utc_now()

    # EN: We compute the rendered HTML evidence path now so the browser runtime writes
    # EN: directly into the controlled raw acquisition tree.
    # TR: Browser runtime doğrudan kontrollü raw acquisition ağacına yazsın diye rendered HTML
    # TR: kanıt yolunu şimdi hesaplıyoruz.
    html_output_path = build_browser_rendered_storage_path(
        url_id=url_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )

    # EN: We compute the screenshot sibling path now so the browser evidence set stays complete.
    # TR: Browser kanıt seti tam kalsın diye screenshot kardeş yolunu da şimdi hesaplıyoruz.
    screenshot_output_path = build_browser_screenshot_storage_path(
        url_id=url_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )

    # EN: We make sure both parent directories exist before handing them to the browser runtime.
    # TR: Bu yolları browser runtime'a vermeden önce her iki parent dizinin de var olduğundan emin oluyoruz.
    ensure_parent_directory(html_output_path)
    ensure_parent_directory(screenshot_output_path)

    # EN: We execute the canonical browser acquisition surface and ask it to persist both
    # EN: rendered HTML and screenshot evidence.
    # TR: Kanonik browser acquisition yüzeyini çalıştırıyor ve hem rendered HTML hem de
    # TR: screenshot kanıtını kalıcılaştırmasını istiyoruz.
    browser_result = acquire_public_page_with_browser(
        target_url=requested_url,
        html_output_path=html_output_path,
        screenshot_output_path=screenshot_output_path,
        headless=headless,
        wait_until=wait_until,
        timeout_ms=timeout_ms,
    )

    # EN: We read back the persisted rendered HTML bytes from disk because the final
    # EN: contract should be based on the actual artefact we stored, not on a separate guess.
    # TR: Nihai sözleşme ayrı bir tahmine değil, gerçekten sakladığımız artefact'a dayansın diye
    # TR: kalıcılaştırılmış rendered HTML byte'larını diskten tekrar okuyoruz.
    rendered_html_bytes = html_output_path.read_bytes()

    # EN: We compute a deterministic fingerprint of the rendered HTML artefact.
    # TR: Rendered HTML artefact'ının deterministik parmak izini hesaplıyoruz.
    rendered_html_sha256 = sha256_hex(rendered_html_bytes)

    # EN: We infer one document-level status code from browser network evidence.
    # TR: Browser network evidence içinden tek bir document-seviyesi durum kodu çıkarıyoruz.
    inferred_http_status = infer_browser_document_status(browser_result)

    # EN: We return the same FetchedPageResult contract shape already used by the
    # EN: direct HTTP path so later layers can stay narrow.
    # TR: Sonraki katmanlar dar kalabilsin diye, direct HTTP yolunun zaten kullandığı
    # TR: aynı FetchedPageResult sözleşme şeklini döndürüyoruz.
    return FetchedPageResult(
        url_id=url_id,
        requested_url=requested_url,
        final_url=str(getattr(browser_result, "final_url", requested_url) or requested_url),
        http_status=inferred_http_status,
        content_type="text/html; charset=utf-8",
        etag=None,
        last_modified=None,
        body_bytes=len(rendered_html_bytes),
        raw_storage_path=str(html_output_path),
        raw_sha256=rendered_html_sha256,
        fetched_at=fetched_at.isoformat(),
    )

# EN: This export list keeps the browser-backed child surface explicit.
# TR: Bu export listesi browser-backed alt yüzeyi açık tutar.
__all__ = [
    "infer_browser_document_status",
    "fetch_page_with_browser_to_raw_storage",
]
