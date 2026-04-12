from __future__ import annotations

# EN: We import dataclass helpers because this first canonical browser-acquisition
# EN: surface must return explicit, structured, machine-readable evidence instead
# EN: of loose ad hoc dictionaries scattered across the codebase.
# TR: İlk kanonik browser-acquisition yüzeyi gevşek ve dağınık sözlükler yerine
# TR: açık, yapılı ve makine-okunur kanıt döndürmelidir; bu yüzden dataclass
# TR: yardımcılarını içe aktarıyoruz.
from dataclasses import asdict, dataclass, field

# EN: We use Path because evidence files such as rendered HTML, screenshot, and
# EN: JSON output must be written in a filesystem-safe and explicit manner.
# TR: Rendered HTML, screenshot ve JSON çıktısı gibi kanıt dosyalarının dosya
# TR: sistemine güvenli ve açık biçimde yazılması gerektiği için Path kullanıyoruz.
from pathlib import Path

# EN: We import Any only for explicit result serialization typing.
# TR: Any tipini yalnızca açık sonuç serileştirme tipi için içe aktarıyoruz.
from typing import Any

# EN: This first real browser-acquisition surface uses Playwright's sync API
# EN: because the current crawler runtime is still operationally narrower and a
# EN: synchronous first implementation is easier to inspect, smoke-test, and audit.
# TR: Bu ilk gerçek browser-acquisition yüzeyi Playwright'ın sync API'sini
# TR: kullanır; çünkü mevcut crawler runtime hâlâ operasyonel olarak daha dardır
# TR: ve senkron ilk implementasyon denetlemek, smoke-test etmek ve audit etmek
# TR: açısından daha kolaydır.
from playwright.sync_api import Page, Response, sync_playwright


# EN: This dataclass stores one observed public browser-network response in a
# EN: narrow, serializable form. We keep it intentionally small in the first step.
# TR: Bu dataclass gözlenen bir public browser-network response'unu dar ve
# TR: serileştirilebilir biçimde saklar. İlk adımda bunu bilinçli olarak küçük tutuyoruz.
@dataclass(slots=True)
class BrowserNetworkRecord:
    # EN: The concrete response URL observed by the browser.
    # TR: Tarayıcı tarafından gözlenen somut response URL'si.
    url: str

    # EN: The HTTP status, if Playwright exposed one.
    # TR: Playwright sağladıysa HTTP durum kodu.
    status: int | None

    # EN: The resource type that triggered the response, such as document,
    # EN: stylesheet, script, image, xhr, or fetch.
    # TR: document, stylesheet, script, image, xhr veya fetch gibi response'u
    # TR: tetikleyen resource türü.
    resource_type: str

    # EN: Whether Playwright considers this response successful.
    # TR: Playwright'ın bu response'u başarılı kabul edip etmediği bilgisi.
    ok: bool | None


# EN: This dataclass is the first canonical repo-visible evidence package for
# EN: browser-based public acquisition.
# TR: Bu dataclass, browser tabanlı public acquisition için repo içinde görünür
# TR: ilk kanonik kanıt paketidir.
@dataclass(slots=True)
class BrowserAcquisitionResult:
    # EN: The target URL requested by the caller.
    # TR: Çağıran tarafından istenen hedef URL.
    target_url: str

    # EN: The final URL after navigation and redirects.
    # TR: Navigasyon ve yönlendirmeler sonrasındaki nihai URL.
    final_url: str | None

    # EN: The document title observed after page load.
    # TR: Sayfa yüklendikten sonra gözlenen doküman başlığı.
    title: str | None

    # EN: The byte length of the rendered DOM snapshot written to disk.
    # TR: Diske yazılan rendered DOM snapshot'ının bayt uzunluğu.
    rendered_html_bytes: int

    # EN: Absolute path of the HTML evidence file.
    # TR: HTML kanıt dosyasının mutlak yolu.
    html_path: str

    # EN: Absolute path of the screenshot evidence file.
    # TR: Screenshot kanıt dosyasının mutlak yolu.
    screenshot_path: str

    # EN: Whether browser launch completed successfully.
    # TR: Browser başlatmasının başarılı tamamlanıp tamamlanmadığı.
    launched: bool

    # EN: Whether the main navigation succeeded.
    # TR: Ana navigasyonun başarılı olup olmadığı.
    goto_ok: bool

    # EN: The Playwright wait mode used during navigation.
    # TR: Navigasyon sırasında kullanılan Playwright wait modu.
    wait_until: str

    # EN: Whether the browser was launched headless.
    # TR: Browser'ın headless olarak başlatılıp başlatılmadığı.
    headless: bool

    # EN: The browser engine identifier used by this first implementation.
    # TR: Bu ilk implementasyonda kullanılan browser engine kimliği.
    browser_engine: str

    # EN: A narrow collection of observed browser network responses.
    # TR: Gözlenen browser network response'larının dar bir koleksiyonu.
    network_records: list[BrowserNetworkRecord] = field(default_factory=list)

    # EN: This helper converts the dataclass into a plain JSON-serializable dict.
    # TR: Bu yardımcı, dataclass nesnesini sade JSON-serileştirilebilir sözlüğe çevirir.
    def to_dict(self) -> dict[str, Any]:
        # EN: asdict already recursively serializes nested dataclasses.
        # TR: asdict iç içe dataclass'ları zaten özyineli biçimde serileştirir.
        return asdict(self)


# EN: This helper ensures parent directories exist before writing evidence files.
# TR: Bu yardımcı, kanıt dosyaları yazılmadan önce üst dizinlerin var olmasını sağlar.
def ensure_parent_dir(path: Path) -> None:
    # EN: parents=True allows deeper directory trees to be created in one step.
    # TR: parents=True, daha derin dizin ağaçlarının tek adımda oluşturulmasını sağlar.
    path.parent.mkdir(parents=True, exist_ok=True)


# EN: This helper writes rendered HTML text using UTF-8.
# TR: Bu yardımcı rendered HTML metnini UTF-8 ile yazar.
def write_text_file(path: Path, content: str) -> None:
    ensure_parent_dir(path)
    path.write_text(content, encoding="utf-8")


# EN: This helper writes a browser screenshot to disk.
# TR: Bu yardımcı browser screenshot'ını diske yazar.
def write_screenshot(page: Page, path: Path) -> None:
    ensure_parent_dir(path)
    # EN: We route screenshot persistence through the canonical helper so the
    # EN: repo-visible browser-acquisition path stays structurally explicit and auditable.
    # TR: Screenshot kalıcılığını kanonik helper üzerinden yönlendiriyoruz; böylece
    # TR: repo-görünür browser-acquisition yolu yapısal olarak açık ve denetlenebilir kalır.
    take_full_page_screenshot(
        page=page,
        path=path,
    )


# EN: This is the first canonical browser-acquisition function. Its job is:
# EN: 1) launch a real browser,
# EN: 2) visit a public page,
# EN: 3) capture rendered HTML,
# EN: 4) capture a screenshot,
# EN: 5) capture a narrow set of browser-network evidence,
# EN: 6) return a structured result object.
# TR: Bu ilk kanonik browser-acquisition fonksiyonunun görevi şudur:
# TR: 1) gerçek bir browser başlatmak,
# TR: 2) public bir sayfayı ziyaret etmek,
# TR: 3) rendered HTML yakalamak,
# TR: 4) screenshot yakalamak,
# TR: 5) dar bir browser-network kanıt seti yakalamak,
# TR: 6) yapılı bir sonuç nesnesi döndürmek.

# EN: This helper writes the full-page screenshot evidence for the current browser run.
# EN: We keep it as a dedicated function so screenshot persistence becomes a visible,
# EN: named, reusable, and audit-friendly surface rather than an inline side effect.
# TR: Bu yardımcı, mevcut browser çalışmasının tam-sayfa screenshot kanıtını yazar.
# TR: Bunu ayrı bir fonksiyon olarak tutuyoruz; böylece screenshot kalıcılığı satır
# TR: içi yan-etki yerine görünür, isimli, yeniden kullanılabilir ve audit-dostu bir yüzey olur.
def take_full_page_screenshot(page: Page, path: Path) -> None:
    # EN: We first ensure the parent directory exists, because evidence writing
    # EN: must fail less often for avoidable filesystem-shape reasons.
    # TR: Önce üst dizinin varlığını garanti ediyoruz; çünkü kanıt yazımı,
    # TR: önlenebilir dosya-sistemi şekli hataları yüzünden gereksiz yere patlamamalıdır.
    ensure_parent_dir(path)

    # EN: We then ask Playwright to persist one full-page screenshot so operators
    # EN: can later inspect what the browser actually rendered.
    # TR: Ardından Playwright'tan tek bir tam-sayfa screenshot kalıcılığı istiyoruz;
    # TR: böylece operatör daha sonra browser'ın gerçekten ne render ettiğini inceleyebilir.
    page.screenshot(path=str(path), full_page=True)


def acquire_public_page_with_browser(
    *,
    target_url: str,
    html_output_path: Path,
    screenshot_output_path: Path,
    headless: bool = True,
    wait_until: str = "networkidle",
    timeout_ms: int = 30000,
    max_network_records: int = 200,
) -> BrowserAcquisitionResult:
    # EN: We prepare mutable evidence state before browser launch so failures can
    # EN: still be described explicitly and honestly.
    # TR: Browser başlatılmadan önce değişebilir kanıt durumunu hazırlıyoruz ki
    # TR: hata durumları da açık ve dürüst biçimde ifade edilebilsin.
    launched = False
    goto_ok = False
    final_url: str | None = None
    title: str | None = None
    rendered_html = ""
    network_records: list[BrowserNetworkRecord] = []

    # EN: This nested callback captures each visible browser response in a narrow
    # EN: serializable format.
    # TR: Bu iç callback, görünen her browser response'unu dar ve serileştirilebilir
    # TR: biçimde yakalar.
    def on_response(response: Response) -> None:
        # EN: We intentionally stop collecting after the configured cap so the
        # EN: first implementation does not grow evidence without bound.
        # TR: İlk implementasyonun sınırsız büyümemesi için yapılandırılmış üst sınıra
        # TR: ulaşıldığında bilinçli olarak toplamayı durduruyoruz.
        if len(network_records) >= max_network_records:
            return

        # EN: We only keep http/https traffic because this surface is about public
        # EN: acquisition evidence, not internal browser pseudo-schemes.
        # TR: Bu yüzey public acquisition kanıtı ile ilgili olduğu için yalnızca
        # TR: http/https trafiğini tutuyoruz; tarayıcı içi sözde şemaları değil.
        if not response.url.startswith(("http://", "https://")):
            return

        # EN: We derive a compact record from Playwright's response object.
        # TR: Playwright response nesnesinden kompakt bir kayıt türetiyoruz.
        network_records.append(
            BrowserNetworkRecord(
                url=response.url,
                status=response.status,
                resource_type=response.request.resource_type,
                ok=response.ok,
            )
        )

    # EN: sync_playwright manages browser-driver lifecycle cleanly.
    # TR: sync_playwright browser-driver yaşam döngüsünü temiz biçimde yönetir.
    with sync_playwright() as playwright:
        # EN: We intentionally use Playwright's Chromium runtime because that is
        # EN: the browser runtime we installed and verified on Pi51c.
        # TR: Bilinçli olarak Playwright Chromium runtime'ını kullanıyoruz; çünkü
        # TR: Pi51c üzerinde kurup doğruladığımız browser runtime budur.
        browser = playwright.chromium.launch(headless=headless)
        launched = True

        # EN: A fresh context keeps the smoke deterministic and isolated.
        # TR: Taze bir context smoke'un deterministik ve izole kalmasını sağlar.
        context = browser.new_context()

        try:
            # EN: We create a page and attach the network callback before navigation
            # EN: so we do not miss early responses.
            # TR: Erken response'ları kaçırmamak için sayfayı oluşturup network
            # TR: callback'ini navigasyondan önce bağlıyoruz.
            page = context.new_page()
            page.on("response", on_response)

            # EN: page.goto performs the real navigation through a browser engine.
            # TR: page.goto gerçek navigasyonu browser motoru üzerinden yapar.
            page.goto(target_url, wait_until=wait_until, timeout=timeout_ms)
            goto_ok = True

            # EN: After navigation we read browser-observed final URL and title.
            # TR: Navigasyon sonrasında browser tarafından gözlenen final URL ve
            # TR: title bilgisini okuyoruz.
            final_url = page.url
            title = page.title()

            # EN: page.content returns the rendered DOM snapshot, not merely the
            # EN: original raw HTTP body.
            # TR: page.content yalnızca ilk ham HTTP body'yi değil, rendered DOM
            # TR: snapshot'ını döndürür.
            rendered_html = page.content()

            # EN: We now persist both rendered HTML evidence and screenshot evidence.
            # TR: Artık hem rendered HTML kanıtını hem de screenshot kanıtını kalıcı yazıyoruz.
            write_text_file(html_output_path, rendered_html)
            write_screenshot(page, screenshot_output_path)
        finally:
            # EN: Even on failure we close context and browser explicitly.
            # TR: Hata olsa bile context ve browser'ı açıkça kapatıyoruz.
            context.close()
            browser.close()

    # EN: We return a structured result package that later caller layers can
    # EN: serialize, store, or compare.
    # TR: Daha sonraki çağıran katmanların serileştirebileceği, saklayabileceği
    # TR: veya karşılaştırabileceği yapılı bir sonuç paketi döndürüyoruz.
    return BrowserAcquisitionResult(
        target_url=target_url,
        final_url=final_url,
        title=title,
        rendered_html_bytes=len(rendered_html.encode("utf-8")),
        html_path=str(html_output_path),
        screenshot_path=str(screenshot_output_path),
        launched=launched,
        goto_ok=goto_ok,
        wait_until=wait_until,
        headless=headless,
        browser_engine="playwright.chromium",
        network_records=network_records,
    )
