# EN: This module is the real acquisition-family orchestration hub.
# EN: Its new job is not only to re-export child surfaces, but also to choose
# EN: the first acquisition path for one claimed URL in a narrow, explicit,
# EN: auditable way.
# TR: Bu modül acquisition ailesinin gerçek orkestrasyon merkezidir.
# TR: Yeni görevi yalnızca alt yüzeyleri yeniden dışa aktarmak değil; aynı
# TR: zamanda tek bir claimed URL için ilk acquisition yolunu dar, açık ve
# TR: denetlenebilir biçimde seçmektir.

from __future__ import annotations

# EN: We import dataclass because selection and execution results should stay
# EN: explicit, named, and beginner-readable instead of being loose dicts.
# TR: Seçim ve yürütme sonuçları gevşek dict yapıları yerine açık, isimli ve
# TR: beginner-okunur kalsın diye dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import Path because the public orchestration function keeps raw_root
# EN: configurable and explicit in its signature.
# TR: Public orkestrasyon fonksiyonu raw_root değerini imzada yapılandırılabilir
# TR: ve açık tuttuğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import urlparse because lightweight URL-shape inspection is enough for
# EN: the first selection policy we are introducing here.
# TR: Burada tanıttığımız ilk seçim politikası için hafif URL şekli incelemesi
# TR: yeterli olduğu için urlparse içe aktarıyoruz.
from urllib.parse import urlparse

# EN: We re-export the shared support surface so upstream callers can keep using
# EN: the stable acquisition-family contract without knowing the split layout.
# TR: Yukarı akış çağıranlar split yerleşimi bilmeden acquisition-aile
# TR: sözleşmesini kullanmaya devam etsin diye paylaşılan destek yüzeyini yeniden
# TR: dışa aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedPageResult,
    FetchedRobotsTxtResult,
    build_browser_rendered_storage_path,
    build_browser_screenshot_storage_path,
    build_raw_fetch_storage_path,
    build_raw_robots_storage_path,
    ensure_parent_directory,
    get_claimed_url_value,
    sha256_hex,
    utc_now,
    utc_now_iso,
    utc_path_stamp,
)

# EN: We re-export the direct HTTP page-acquisition child because upstream code
# EN: may still need the narrow child surface directly.
# TR: Yukarı akış kodu hâlâ dar alt yüzeye doğrudan ihtiyaç duyabilir diye
# TR: doğrudan HTTP page-acquisition alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_2_4_2_http_page_acquisition_runtime import (
    fetch_page_to_raw_storage,
)

# EN: We re-export the robots acquisition child because the acquisition family
# EN: still includes robots work in the same stable public surface.
# TR: Acquisition ailesi aynı kararlı public yüzey içinde robots işini de
# TR: taşımaya devam ettiği için robots acquisition alt yüzeyini yeniden dışa
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_5_robots_txt_acquisition_runtime import (
    decode_robots_body,
    fetch_robots_txt_to_raw_storage,
    parse_robots_txt_text,
)

# EN: We re-export the browser-backed page-acquisition child because some callers
# EN: still need the direct browser adapter explicitly.
# TR: Bazı çağıranlar doğrudan browser adapter'ına açık biçimde ihtiyaç duymaya
# TR: devam ettiği için browser-backed page-acquisition alt yüzeyini yeniden dışa
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_4_browser_page_acquisition_runtime import (
    fetch_page_with_browser_to_raw_storage,
    infer_browser_document_status,
)

# EN: These suffixes mark URL targets that are better treated as direct-download
# EN: or direct-fetch surfaces instead of browser-first HTML pages.
# TR: Bu sonekler, URL hedeflerinin browser-first HTML sayfaları yerine doğrudan
# TR: indirme veya doğrudan fetch yüzeyi gibi ele alınmasının daha doğru olduğunu
# TR: işaretler.
DIRECT_HTTP_FILE_SUFFIXES = (
    ".pdf",
    ".xml",
    ".json",
    ".txt",
    ".csv",
    ".zip",
    ".gz",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".svg",
)

# EN: This dataclass records the narrow policy decision made before acquisition.
# TR: Bu dataclass acquisition başlamadan önce verilen dar politika kararını kaydeder.
@dataclass
class AcquisitionSelectionPlan:
    # EN: target_url is the canonical public URL we are deciding on.
    # TR: target_url karar verdiğimiz kanonik public URL'dir.
    target_url: str

    # EN: strategy is the selected initial method family.
    # TR: strategy seçilmiş ilk yöntem ailesidir.
    strategy: str

    # EN: url_kind is the coarse URL-type classification used by the selector.
    # TR: url_kind selector tarafından kullanılan kaba URL-tipi sınıflandırmasıdır.
    url_kind: str

    # EN: reason is the human-readable explanation of why this plan was chosen.
    # TR: reason bu planın neden seçildiğini açıklayan insan-okunur metindir.
    reason: str

    # EN: browser_fallback_allowed tells the executor whether an HTTP exception
    # EN: may escalate into a browser-backed retry.
    # TR: browser_fallback_allowed, yürütücünün bir HTTP istisnasını browser-backed
    # TR: yeniden denemeye yükseltip yükseltemeyeceğini söyler.
    browser_fallback_allowed: bool

    # EN: browser_required records whether the plan intentionally starts with browser.
    # TR: browser_required planın bilinçli olarak browser ile başlayıp başlamadığını kaydeder.
    browser_required: bool


# EN: This dataclass records the actual executed method and the normalized fetch result.
# TR: Bu dataclass fiilen kullanılan yöntemi ve normalize edilmiş fetch sonucunu kaydeder.
@dataclass
class AcquisitionExecutionResult:
    # EN: selection_plan stores the selector output that drove execution.
    # TR: selection_plan yürütmeyi yönlendiren selector çıktısını taşır.
    selection_plan: AcquisitionSelectionPlan

    # EN: method_used is the concrete method that produced the fetch result.
    # TR: method_used fetch sonucunu üreten somut yöntemdir.
    method_used: str

    # EN: fallback_used tells whether execution had to switch away from the first plan.
    # TR: fallback_used yürütmenin ilk plandan ayrılmak zorunda kalıp kalmadığını söyler.
    fallback_used: bool

    # EN: fetch_result is the stable crawler-core fetch result contract.
    # TR: fetch_result kararlı crawler-core fetch sonucu sözleşmesidir.
    fetch_result: FetchedPageResult

    # EN: http_error_class stores the first HTTP-side exception class when fallback occurred.
    # TR: http_error_class fallback olduysa ilk HTTP-tarafı istisna sınıfını tutar.
    http_error_class: str | None

    # EN: http_error_message stores the first HTTP-side exception message when fallback occurred.
    # TR: http_error_message fallback olduysa ilk HTTP-tarafı istisna mesajını tutar.
    http_error_message: str | None


# EN: This helper reads the first available claimed_url field from a list of names.
# EN: It lets us keep the first selector tolerant while the broader worker contract
# EN: is still being tightened.
# TR: Bu yardımcı bir alan adı listesi içinden mevcut olan ilk claimed_url alanını okur.
# TR: Böylece daha geniş worker sözleşmesi henüz sıkılaştırılırken ilk selector'ü
# TR: toleranslı tutabiliriz.
def _read_optional_claimed_url_value(claimed_url: object, field_names: tuple[str, ...]) -> object | None:
    # EN: We scan candidate names in order because current surfaces may still carry
    # EN: small naming drift.
    # TR: Aday alan adlarını sırayla tarıyoruz; çünkü mevcut yüzeylerde küçük isim
    # TR: kaymaları hâlâ bulunabilir.
    for field_name in field_names:
        try:
            return get_claimed_url_value(claimed_url, field_name)
        except (KeyError, AttributeError):
            continue

    # EN: If none of the candidate names exists, we return None so the caller can
    # EN: decide on a safe default explicitly.
    # TR: Aday isimlerden hiçbiri yoksa None döndürüyoruz; böylece çağıran güvenli
    # TR: varsayılanı açık biçimde kendisi seçebilir.
    return None


# EN: This helper converts a tolerant claimed_url field into a strict boolean.
# TR: Bu yardımcı toleranslı claimed_url alanını katı bir boole değerine dönüştürür.
def _read_optional_bool_flag(claimed_url: object, field_names: tuple[str, ...]) -> bool:
    # EN: raw_value stores the first matching candidate field when one exists.
    # TR: raw_value mevcutsa eşleşen ilk aday alanı tutar.
    raw_value = _read_optional_claimed_url_value(claimed_url, field_names)

    # EN: Missing values mean the flag is not actively requested.
    # TR: Eksik değerler bu bayrağın aktif olarak istenmediği anlamına gelir.
    if raw_value is None:
        return False

    # EN: Real bool values can be returned directly.
    # TR: Gerçek bool değerler doğrudan döndürülebilir.
    if isinstance(raw_value, bool):
        return raw_value

    # EN: Integer flags are treated conservatively as truthy/non-truthy.
    # TR: Integer bayraklar muhafazakâr biçimde truthy/non-truthy olarak ele alınır.
    if isinstance(raw_value, int):
        return raw_value != 0

    # EN: String flags are normalized into a small explicit truthy vocabulary.
    # TR: Metin bayrakları küçük ve açık bir truthy sözlüğüne normalize edilir.
    normalized_text = str(raw_value).strip().lower()
    return normalized_text in {"1", "true", "yes", "y", "on", "browser", "required"}


# EN: This helper classifies the target URL into a coarse operational kind.
# EN: We intentionally keep the classification narrow because the first goal is
# EN: to enable safe orchestration, not to overfit site behavior too early.
# TR: Bu yardımcı hedef URL'yi kaba bir operasyonel türe sınıflandırır.
# TR: Sınıflandırmayı bilinçli olarak dar tutuyoruz; çünkü ilk hedef site
# TR: davranışını erken aşırı uyarlamak değil, güvenli orkestrasyon sağlamaktır.
def infer_target_url_kind(target_url: str) -> str:
    # EN: parsed_url stores the structured URL parts for lightweight inspection.
    # TR: parsed_url hafif inceleme için yapılandırılmış URL parçalarını tutar.
    parsed_url = urlparse(target_url)

    # EN: normalized_path is the lowercase path used for suffix checks.
    # TR: normalized_path sonek kontrolleri için kullanılan küçük harfli path değeridir.
    normalized_path = parsed_url.path.lower()

    # EN: File-like download targets stay on the direct HTTP path.
    # TR: Dosya-benzeri indirme hedefleri doğrudan HTTP yolunda kalır.
    if normalized_path.endswith(DIRECT_HTTP_FILE_SUFFIXES):
        return "direct_http_asset"

    # EN: Fragment-driven targets are browser-oriented because the visible document
    # EN: often depends on client-side routing.
    # TR: Fragment-tabanlı hedefler browser odaklıdır; çünkü görünür belge çoğu zaman
    # TR: istemci-tarafı yönlendirmeye bağlıdır.
    if parsed_url.fragment:
        return "browser_oriented_html"

    # EN: Everything else is treated as a normal HTML-like page candidate first.
    # TR: Geri kalan her şey önce normal HTML-benzeri sayfa adayı kabul edilir.
    return "html_like_page"


# EN: This function decides the first acquisition strategy for one claimed URL.
# EN: The first selector intentionally follows a simple policy:
# EN: 1) explicit browser flags win,
# EN: 2) obvious non-HTML assets stay on direct HTTP,
# EN: 3) normal page-like URLs start with HTTP and may fall back to browser on transport failure.
# TR: Bu fonksiyon tek bir claimed URL için ilk acquisition stratejisini belirler.
# TR: İlk selector bilinçli olarak basit bir politika izler:
# TR: 1) açık browser bayrakları kazanır,
# TR: 2) belirgin HTML-dışı varlıklar doğrudan HTTP'de kalır,
# TR: 3) normal sayfa-benzeri URL'ler HTTP ile başlar ve taşıma hatasında browser'a düşebilir.
def select_page_acquisition_plan(claimed_url: object) -> AcquisitionSelectionPlan:
    # EN: target_url is the canonical fetch target used by both HTTP and browser paths.
    # TR: target_url hem HTTP hem browser yollarının kullandığı kanonik fetch hedefidir.
    target_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: force_browser records the strongest explicit browser request.
    # TR: force_browser en güçlü açık browser isteğini kaydeder.
    force_browser = _read_optional_bool_flag(
        claimed_url,
        (
            "force_browser",
            "browser_required",
            "requires_browser",
            "use_browser",
        ),
    )

    # EN: prefer_browser records a softer browser preference that still deserves
    # EN: browser-first execution in this early implementation.
    # TR: prefer_browser daha yumuşak bir browser tercihidir; ancak bu erken
    # TR: implementasyonda yine de browser-first yürütmeyi hak eder.
    prefer_browser = _read_optional_bool_flag(
        claimed_url,
        (
            "prefer_browser",
            "browser_preferred",
        ),
    )

    # EN: force_http_only prevents escalation when the caller explicitly wants a
    # EN: direct wire-level fetch only.
    # TR: force_http_only, çağıran açıkça yalnızca doğrudan wire-seviyesi fetch
    # TR: istediğinde yükseltmeyi engeller.
    force_http_only = _read_optional_bool_flag(
        claimed_url,
        (
            "force_http_only",
            "http_only",
            "direct_http_only",
        ),
    )

    # EN: url_kind is the coarse URL classification used by the selector.
    # TR: url_kind selector tarafından kullanılan kaba URL sınıflandırmasıdır.
    url_kind = infer_target_url_kind(target_url)

    # EN: Explicit browser demand wins unless the caller also explicitly demanded
    # EN: HTTP-only, which is a contradictory contract that should fail loudly.
    # TR: Açık browser talebi, çağıran aynı anda açıkça HTTP-only de istemediyse
    # TR: kazanır; bu çelişkili sözleşme yüksek sesle hata vermelidir.
    if (force_browser or prefer_browser) and force_http_only:
        raise ValueError(
            "claimed_url requests both browser execution and HTTP-only execution"
        )

    # EN: Browser-first selection is used when the caller explicitly says so.
    # TR: Çağıran açıkça istediğinde browser-first seçim kullanılır.
    if force_browser or prefer_browser:
        return AcquisitionSelectionPlan(
            target_url=target_url,
            strategy="browser",
            url_kind=url_kind,
            reason="explicit browser flag requested browser-backed acquisition",
            browser_fallback_allowed=False,
            browser_required=True,
        )

    # EN: Direct asset/document URLs stay on the direct HTTP path because browser
    # EN: rendering adds cost without helping the first fetch layer.
    # TR: Doğrudan asset/document URL'leri doğrudan HTTP yolunda kalır; çünkü
    # TR: browser render maliyet ekler ama ilk fetch katmanına fayda sağlamaz.
    if url_kind == "direct_http_asset":
        return AcquisitionSelectionPlan(
            target_url=target_url,
            strategy="http",
            url_kind=url_kind,
            reason="direct asset/document URL should use direct HTTP acquisition",
            browser_fallback_allowed=False,
            browser_required=False,
        )

    # EN: The default page-like strategy starts with HTTP but keeps browser fallback
    # EN: open for future real-world escalation on transport failure.
    # TR: Varsayılan sayfa-benzeri strateji HTTP ile başlar; ancak gelecekteki gerçek
    # TR: dünya yükseltmesi için taşıma hatasında browser fallback kapısını açık tutar.
    return AcquisitionSelectionPlan(
        target_url=target_url,
        strategy="http_then_browser",
        url_kind=url_kind,
        reason="page-like URL should start with HTTP and keep browser fallback available",
        browser_fallback_allowed=not force_http_only,
        browser_required=False,
    )


# EN: This function executes the selected acquisition plan and normalizes the
# EN: result into one explicit orchestration record.
# TR: Bu fonksiyon seçilen acquisition planını yürütür ve sonucu tek bir açık
# TR: orkestrasyon kaydına normalize eder.
def fetch_page_via_selection_to_raw_storage(
    claimed_url: object,
    *,
    http_timeout_seconds: int = 30,
    browser_timeout_ms: int = 30000,
    browser_wait_until: str = "networkidle",
    raw_root: Path | str = RAW_FETCH_ROOT,
    headless: bool = True,
) -> AcquisitionExecutionResult:
    # EN: normalized_raw_root converts caller input into a real Path object before
    # EN: we pass it to lower acquisition children, because some controlled callers
    # EN: may still provide raw_root through environment-derived strings.
    # TR: normalized_raw_root, alt acquisition çocuklarına vermeden önce çağıran
    # TR: girdisini gerçek bir Path nesnesine dönüştürür; çünkü bazı kontrollü
    # TR: çağıranlar raw_root değerini hâlâ environment-kaynaklı string olarak verebilir.
    normalized_raw_root = Path(raw_root)

    # EN: selection_plan stores the explicit pre-fetch strategy decision.
    # TR: selection_plan açık pre-fetch strateji kararını tutar.
    selection_plan = select_page_acquisition_plan(claimed_url)

    # EN: Browser-first plans execute immediately through the browser-backed child.
    # TR: Browser-first planlar doğrudan browser-backed alt yüzey üzerinden yürütülür.
    if selection_plan.strategy == "browser":
        # EN: browser_fetch_result stores the normalized browser-backed fetch contract.
        # TR: browser_fetch_result normalize edilmiş browser-backed fetch sözleşmesini tutar.
        browser_fetch_result = fetch_page_with_browser_to_raw_storage(
            claimed_url,
            timeout_ms=browser_timeout_ms,
            wait_until=browser_wait_until,
            raw_root=normalized_raw_root,
            headless=headless,
        )
        return AcquisitionExecutionResult(
            selection_plan=selection_plan,
            method_used="browser",
            fallback_used=False,
            fetch_result=browser_fetch_result,
            http_error_class=None,
            http_error_message=None,
        )

    # EN: We first attempt the direct HTTP child because the remaining strategies
    # EN: all begin with wire-level fetch.
    # TR: Kalan stratejilerin tümü wire-seviyesi fetch ile başladığı için önce
    # TR: doğrudan HTTP alt yüzeyini deniyoruz.
    try:
        # EN: http_fetch_result stores the successful direct HTTP fetch outcome.
        # TR: http_fetch_result başarılı doğrudan HTTP fetch sonucunu tutar.
        http_fetch_result = fetch_page_to_raw_storage(
            claimed_url,
            timeout_seconds=http_timeout_seconds,
            raw_root=normalized_raw_root,
        )
        return AcquisitionExecutionResult(
            selection_plan=selection_plan,
            method_used="http",
            fallback_used=False,
            fetch_result=http_fetch_result,
            http_error_class=None,
            http_error_message=None,
        )
    except Exception as http_error:
        # EN: If fallback is not allowed, we re-raise the original HTTP exception so
        # EN: callers keep the true failure semantics.
        # TR: Fallback izinli değilse çağıranlar gerçek hata semantiğini korusun diye
        # TR: özgün HTTP istisnasını yeniden yükseltiyoruz.
        if not selection_plan.browser_fallback_allowed:
            raise

        # EN: browser_fetch_result stores the browser-backed recovery fetch outcome.
        # TR: browser_fetch_result browser-backed toparlama fetch sonucunu tutar.
        browser_fetch_result = fetch_page_with_browser_to_raw_storage(
            claimed_url,
            timeout_ms=browser_timeout_ms,
            wait_until=browser_wait_until,
            raw_root=normalized_raw_root,
            headless=headless,
        )
        return AcquisitionExecutionResult(
            selection_plan=selection_plan,
            method_used="browser",
            fallback_used=True,
            fetch_result=browser_fetch_result,
            http_error_class=type(http_error).__name__,
            http_error_message=str(http_error),
        )


# EN: This export list keeps the stable public acquisition-family surface explicit
# EN: while also exposing the new selection/orchestration layer.
# TR: Bu export listesi kararlı public acquisition-aile yüzeyini açık tutarken
# TR: yeni seçim/orkestrasyon katmanını da dışa açar.
__all__ = [
    "RAW_FETCH_ROOT",
    "FetchedPageResult",
    "FetchedRobotsTxtResult",
    "AcquisitionSelectionPlan",
    "AcquisitionExecutionResult",
    "build_browser_rendered_storage_path",
    "build_browser_screenshot_storage_path",
    "build_raw_fetch_storage_path",
    "build_raw_robots_storage_path",
    "ensure_parent_directory",
    "get_claimed_url_value",
    "sha256_hex",
    "utc_now",
    "utc_now_iso",
    "utc_path_stamp",
    "infer_target_url_kind",
    "select_page_acquisition_plan",
    "fetch_page_via_selection_to_raw_storage",
    "fetch_page_to_raw_storage",
    "decode_robots_body",
    "fetch_robots_txt_to_raw_storage",
    "parse_robots_txt_text",
    "fetch_page_with_browser_to_raw_storage",
    "infer_browser_document_status",
]
