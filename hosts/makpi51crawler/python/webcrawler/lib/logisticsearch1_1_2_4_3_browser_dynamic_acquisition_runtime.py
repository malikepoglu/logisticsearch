"""
EN:
This file is the dynamic-browser acquisition child inside the broader acquisition family.

EN:
Why this file exists:
- because some pages cannot be understood by plain HTTP alone and need a browser-driven dynamic corridor
- because browser startup, navigation, rendering, dynamic DOM state, browser-side timeout handling, and rendered-page shaping must remain readable in one narrow child
- because a beginner should be able to answer where the crawler handles JavaScript-rendered or browser-required acquisition work

EN:
What this file DOES:
- expose the browser-dynamic acquisition boundaries
- keep browser-driven request/navigation/render semantics readable
- shape dynamic acquisition outputs into explicit downstream-friendly results
- keep degraded dynamic-browser outcomes visible instead of hiding them

EN:
What this file DOES NOT do:
- it does not become the whole acquisition parent
- it does not replace the plain direct-http child
- it does not become parse or storage logic
- it does not turn browser failure into fake success

EN:
Topological role:
- acquisition parent can delegate here when dynamic browser execution is required
- this child owns browser-driven render/navigation style work that is narrower than the full parent but broader than plain support utilities
- later layers consume shaped dynamic results, fetched-page style payloads, or explicit degraded outcomes produced here

EN:
Important visible values and shapes:
- browser-execution helper values => visible indicators that a browser-style corridor ran
- rendered page or browser result payloads => dynamic acquisition outputs prepared for later validation or parse use
- timeout/error/degraded branches => explicit non-happy browser outcomes that must remain readable
- acquisition_method-related meaning => browser-oriented selection signals, often feeding later browser-page style downstream logic

EN:
Accepted architectural identity:
- dynamic-browser acquisition child
- narrow rendered-page execution contract layer
- readable browser-required acquisition boundary

EN:
Undesired architectural identity:
- vague browser utility dump
- hidden second acquisition parent
- hidden parse layer
- hidden side-effect maze

TR:
Bu dosya daha geniş acquisition ailesinin içindeki dynamic-browser acquisition child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü bazı sayfalar yalnızca plain HTTP ile anlaşılamaz ve browser güdümlü dynamic koridora ihtiyaç duyar
- çünkü browser başlatma, navigation, rendering, dynamic DOM durumu, browser tarafı timeout işleme ve render edilmiş sayfa şekillendirme tek bir dar child yüzeyde okunabilir kalmalıdır
- çünkü yeni başlayan biri crawlerın JavaScript-rendered veya browser-gerekli acquisition işini tam olarak nerede yaptığını anlayabilmelidir

TR:
Bu dosya NE yapar:
- browser-dynamic acquisition sınırlarını açığa çıkarır
- browser güdümlü request/navigation/render semantiklerini okunabilir tutar
- dynamic acquisition çıktıları için downstream tarafın anlayacağı açık sonuçlar şekillendirir
- degraded dynamic-browser sonuçlarını gizlemek yerine görünür tutar

TR:
Bu dosya NE yapmaz:
- acquisition parent yüzeyinin tamamı olmaz
- plain direct-http child yüzeyinin yerine geçmez
- parse veya storage mantığı olmaz
- browser başarısızlığını sahte başarıya çevirmez

TR:
Topolojik rol:
- dynamic browser çalıştırması gerektiğinde acquisition parent bu child yüzeye delegasyon yapabilir
- bu child parent yüzeyden daha dar, plain support utility yüzeylerinden daha geniş browser güdümlü render/navigation işini taşır
- sonraki katmanlar burada üretilen şekillendirilmiş dynamic sonuçları, fetched-page benzeri payloadları veya açık degraded sonuçları tüketir

TR:
Önemli görünür değerler ve şekiller:
- browser-execution yardımcı değerleri => browser tarzı koridorun çalıştığını gösteren görünür işaretler
- render edilmiş sayfa veya browser sonuç payloadları => sonraki validation veya parse kullanımına hazırlanan dynamic acquisition çıktıları
- timeout/error/degraded dallar => okunabilir kalması gereken mutlu-yol-dışı browser sonuçları
- acquisition_method ile ilgili anlam => sonraki browser-page tarzı downstream mantığına besleme yapan browser-yönelimli seçim işaretleri

TR:
Kabul edilen mimari kimlik:
- dynamic-browser acquisition child
- dar render edilmiş sayfa execution sözleşme katmanı
- okunabilir browser-gerekli acquisition sınırı

TR:
İstenmeyen mimari kimlik:
- belirsiz browser utility çöplüğü
- gizli ikinci acquisition parent
- gizli parse katmanı
- gizli yan-etki labirenti
"""

# EN: BROWSER DYNAMIC ACQUISITION IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the browser-required dynamic child inside the acquisition family.
# EN: Beginner mental model:
# EN: - the acquisition parent decides that plain HTTP is not enough
# EN: - this child runs browser-driven dynamic work
# EN: - it exists so the crawler can later answer which rendered-page corridor ran, what browser-driven result came back, and how that result was shaped
# EN:
# EN: Accepted architectural meaning:
# EN: - named dynamic-browser acquisition child
# EN: - focused rendered-page and browser-execution surface
# EN: - readable JavaScript-required acquisition boundary
# EN:
# EN: Undesired architectural meaning:
# EN: - random browser helper pile
# EN: - hidden second acquisition parent
# EN: - place where dynamic browser failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - browser-driven outputs should stay explicit
# EN: - rendered-page or fetched-page style payloads should stay structured
# EN: - degraded browser branches must remain visible
# TR: BROWSER DYNAMIC ACQUISITION KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya acquisition ailesinin içindeki browser-gerekli dynamic child gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition parent plain HTTPnin yeterli olmadığına karar verir
# TR: - bu child browser güdümlü dynamic işi çalıştırır
# TR: - crawlerın daha sonra hangi render edilmiş sayfa koridorunun çalıştığını, hangi browser sonucunun geldiğini ve bu sonucun nasıl şekillendiğini cevaplayabilmesi için vardır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli dynamic-browser acquisition child
# TR: - odaklı render edilmiş sayfa ve browser-execution yüzeyi
# TR: - okunabilir JavaScript-gerekli acquisition sınırı
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele browser helper yığını
# TR: - gizli ikinci acquisition parent
# TR: - dynamic browser hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - browser güdümlü çıktılar açık kalmalıdır
# TR: - render edilmiş sayfa veya fetched-page benzeri payloadlar yapılı kalmalıdır
# TR: - degraded browser dalları görünür kalmalıdır

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
# EN: REAL-RULE AST REPAIR / CLASS BrowserNetworkRecord
# EN: BrowserNetworkRecord is an explicit browser-dynamic acquisition runtime data shape.
# TR: REAL-RULE AST REPAIR / SINIF BrowserNetworkRecord
# TR: BrowserNetworkRecord acik bir browser-dynamic acquisition runtime veri seklidir.
@dataclass(slots=True)
# EN: BROWSER DYNAMIC CLASS PURPOSE MEMORY BLOCK V6 / BrowserNetworkRecord
# EN:
# EN: Why this class exists:
# EN: - because browser-dynamic acquisition truth for 'BrowserNetworkRecord' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should inspect field names and understand rendered/browser-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named browser result payload, rendered-page structure, session-like helper carrier, or structured browser-side result container
# EN: - visible field set currently detected here: url, status, resource_type, ok
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface likely performs browser startup, navigation, render waiting, rendered-content shaping, or browser result packaging
# EN: - explicit timeout/error/degraded browser visibility is important here
# EN: - later layers depend on this child to keep dynamic rendered results honest and readable
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no browser-dynamic contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: BROWSER DYNAMIC CLASS AMAÇ HAFIZA BLOĞU V6 / BrowserNetworkRecord
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'BrowserNetworkRecord' için browser-dynamic acquisition doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerine bakıp render/browser tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli browser sonuç payloadı, render edilmiş sayfa yapısı, session-benzeri helper taşıyıcısı veya yapılı browser tarafı sonuç kabı
# TR: - burada şu an tespit edilen görünür alan kümesi: url, status, resource_type, ok
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser başlatma, navigation, render bekleme, render edilmiş içerik şekillendirme veya browser sonucu paketleme işini yapar
# TR: - açık timeout/error/degraded browser görünürlüğü burada önemlidir
# TR: - sonraki katmanlar dynamic render sonuçlarının dürüst ve okunabilir kalması için bu child yüzeye bağımlıdır
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı browser-dynamic sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

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
# EN: REAL-RULE AST REPAIR / CLASS BrowserAcquisitionResult
# EN: BrowserAcquisitionResult is an explicit browser-dynamic acquisition runtime data shape.
# TR: REAL-RULE AST REPAIR / SINIF BrowserAcquisitionResult
# TR: BrowserAcquisitionResult acik bir browser-dynamic acquisition runtime veri seklidir.
@dataclass(slots=True)
# EN: BROWSER DYNAMIC CLASS PURPOSE MEMORY BLOCK V6 / BrowserAcquisitionResult
# EN:
# EN: Why this class exists:
# EN: - because browser-dynamic acquisition truth for 'BrowserAcquisitionResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should inspect field names and understand rendered/browser-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named browser result payload, rendered-page structure, session-like helper carrier, or structured browser-side result container
# EN: - visible field set currently detected here: target_url, final_url, title, rendered_html_bytes, html_path, screenshot_path, launched, goto_ok, wait_until, headless, browser_engine, network_records
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface likely performs browser startup, navigation, render waiting, rendered-content shaping, or browser result packaging
# EN: - explicit timeout/error/degraded browser visibility is important here
# EN: - later layers depend on this child to keep dynamic rendered results honest and readable
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no browser-dynamic contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: BROWSER DYNAMIC CLASS AMAÇ HAFIZA BLOĞU V6 / BrowserAcquisitionResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'BrowserAcquisitionResult' için browser-dynamic acquisition doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerine bakıp render/browser tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli browser sonuç payloadı, render edilmiş sayfa yapısı, session-benzeri helper taşıyıcısı veya yapılı browser tarafı sonuç kabı
# TR: - burada şu an tespit edilen görünür alan kümesi: target_url, final_url, title, rendered_html_bytes, html_path, screenshot_path, launched, goto_ok, wait_until, headless, browser_engine, network_records
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser başlatma, navigation, render bekleme, render edilmiş içerik şekillendirme veya browser sonucu paketleme işini yapar
# TR: - açık timeout/error/degraded browser görünürlüğü burada önemlidir
# TR: - sonraki katmanlar dynamic render sonuçlarının dürüst ve okunabilir kalması için bu child yüzeye bağımlıdır
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı browser-dynamic sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

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
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / to_dict
# EN:
# EN: This nested function exists so the browser-dynamic corridor keeps one named and auditable step for 'to_dict'.
# EN: Why this function exists:
# EN: - to keep browser-driven render/navigation/result semantics visible
# EN: - to keep dynamic branches readable for someone tracing browser-required acquisition from top to bottom
# EN: Accepted input:
# EN: - explicit parameters currently visible here: self
# EN: Accepted output:
# EN: - a result shape defined by the live body below; this may be a rendered-page payload, browser callback effect, response-side mutation, or explicit degraded branch
# EN: Undesired behavior:
# EN: - hidden browser-side mutation
# EN: - unlabeled branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / to_dict
# TR:
# TR: Bu nested fonksiyon, browser-dynamic koridorunun 'to_dict' için tek, isimli ve denetlenebilir bir adım taşıması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - browser güdümlü render/navigation/sonuç semantiklerini görünür tutmak için
# TR: - browser-gerekli acquisition izini yukarıdan aşağı takip eden birinin dynamic dalları okuyabilmesi için
# TR: Kabul edilen girdi:
# TR: - burada şu an görülen açık parametreler: self
# TR: Kabul edilen çıktı:
# TR: - aşağıdaki canlı gövdenin tanımladığı sonuç şekli; bu render edilmiş sayfa payloadı, browser callback etkisi, response tarafı mutasyonu veya açık degraded dal olabilir
# TR: İstenmeyen davranış:
# TR: - gizli browser tarafı mutasyonu
# TR: - etiketsiz dal anlamı

    # EN: REAL-RULE AST REPAIR / DEF to_dict
    # EN: to_dict is an explicit browser-dynamic acquisition runtime/helper contract.
    # EN: Parameters kept explicit here: self.
    # TR: REAL-RULE AST REPAIR / FONKSIYON to_dict
    # TR: to_dict acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
    # TR: Burada acik tutulan parametreler: self.
    def to_dict(self) -> dict[str, Any]:
        # EN: asdict already recursively serializes nested dataclasses.
        # TR: asdict iç içe dataclass'ları zaten özyineli biçimde serileştirir.
        return asdict(self)


# EN: This helper ensures parent directories exist before writing evidence files.
# TR: Bu yardımcı, kanıt dosyaları yazılmadan önce üst dizinlerin var olmasını sağlar.
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / ensure_parent_dir
# EN:
# EN: Why this function exists:
# EN: - because browser-dynamic acquisition truth for 'ensure_parent_dir' should be exposed through one named top-level boundary
# EN: - because rendered-page and browser-driven semantics should remain readable instead of being hidden in broader acquisition layers
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: path
# EN: - values should match the current Python signature and the browser-dynamic acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a browser-dynamic acquisition result shape defined by the current function body
# EN: - this may be a rendered-page payload, browser execution result, fetched_page-style package, or another explicit browser branch result
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface exposes one named browser-required acquisition boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is browser-dynamic acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand rendered success, timeout, browser_error, degraded branches, and downstream payload meaning
# EN:
# EN: Undesired behavior:
# EN: - silent browser result mutation
# EN: - vague outputs that hide branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / ensure_parent_dir
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'ensure_parent_dir' için browser-dynamic acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü render edilmiş sayfa ve browser güdümlü semantiklerin daha geniş acquisition katmanlarında gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: path
# TR: - değerler aşağıdaki mevcut Python imzası ve browser-dynamic acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen browser-dynamic acquisition sonuç şekli
# TR: - bu; render edilmiş sayfa payloadı, browser execution sonucu, fetched_page benzeri paket veya başka açık browser dal sonucu olabilir
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey isimli bir browser-gerekli acquisition sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon browser-dynamic acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler render success, timeout, browser_error, degraded dallar ve downstream payload anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz browser sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: REAL-RULE AST REPAIR / DEF ensure_parent_dir
# EN: ensure_parent_dir is an explicit browser-dynamic acquisition runtime/helper contract.
# EN: Parameters kept explicit here: path.
# TR: REAL-RULE AST REPAIR / FONKSIYON ensure_parent_dir
# TR: ensure_parent_dir acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: path.
def ensure_parent_dir(path: Path) -> None:
    # EN: parents=True allows deeper directory trees to be created in one step.
    # TR: parents=True, daha derin dizin ağaçlarının tek adımda oluşturulmasını sağlar.
    path.parent.mkdir(parents=True, exist_ok=True)


# EN: This helper writes rendered HTML text using UTF-8.
# TR: Bu yardımcı rendered HTML metnini UTF-8 ile yazar.
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / write_text_file
# EN:
# EN: Why this function exists:
# EN: - because browser-dynamic acquisition truth for 'write_text_file' should be exposed through one named top-level boundary
# EN: - because rendered-page and browser-driven semantics should remain readable instead of being hidden in broader acquisition layers
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: path, content
# EN: - values should match the current Python signature and the browser-dynamic acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a browser-dynamic acquisition result shape defined by the current function body
# EN: - this may be a rendered-page payload, browser execution result, fetched_page-style package, or another explicit browser branch result
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface exposes one named browser-required acquisition boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is browser-dynamic acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand rendered success, timeout, browser_error, degraded branches, and downstream payload meaning
# EN:
# EN: Undesired behavior:
# EN: - silent browser result mutation
# EN: - vague outputs that hide branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / write_text_file
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'write_text_file' için browser-dynamic acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü render edilmiş sayfa ve browser güdümlü semantiklerin daha geniş acquisition katmanlarında gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: path, content
# TR: - değerler aşağıdaki mevcut Python imzası ve browser-dynamic acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen browser-dynamic acquisition sonuç şekli
# TR: - bu; render edilmiş sayfa payloadı, browser execution sonucu, fetched_page benzeri paket veya başka açık browser dal sonucu olabilir
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey isimli bir browser-gerekli acquisition sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon browser-dynamic acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler render success, timeout, browser_error, degraded dallar ve downstream payload anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz browser sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: REAL-RULE AST REPAIR / DEF write_text_file
# EN: write_text_file is an explicit browser-dynamic acquisition runtime/helper contract.
# EN: Parameters kept explicit here: path, content.
# TR: REAL-RULE AST REPAIR / FONKSIYON write_text_file
# TR: write_text_file acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: path, content.
def write_text_file(path: Path, content: str) -> None:
    ensure_parent_dir(path)
    path.write_text(content, encoding="utf-8")


# EN: This helper writes a browser screenshot to disk.
# TR: Bu yardımcı browser screenshot'ını diske yazar.
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / write_screenshot
# EN:
# EN: Why this function exists:
# EN: - because browser-dynamic acquisition truth for 'write_screenshot' should be exposed through one named top-level boundary
# EN: - because rendered-page and browser-driven semantics should remain readable instead of being hidden in broader acquisition layers
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: page, path
# EN: - values should match the current Python signature and the browser-dynamic acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a browser-dynamic acquisition result shape defined by the current function body
# EN: - this may be a rendered-page payload, browser execution result, fetched_page-style package, or another explicit browser branch result
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface exposes one named browser-required acquisition boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is browser-dynamic acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand rendered success, timeout, browser_error, degraded branches, and downstream payload meaning
# EN:
# EN: Undesired behavior:
# EN: - silent browser result mutation
# EN: - vague outputs that hide branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / write_screenshot
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'write_screenshot' için browser-dynamic acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü render edilmiş sayfa ve browser güdümlü semantiklerin daha geniş acquisition katmanlarında gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: page, path
# TR: - değerler aşağıdaki mevcut Python imzası ve browser-dynamic acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen browser-dynamic acquisition sonuç şekli
# TR: - bu; render edilmiş sayfa payloadı, browser execution sonucu, fetched_page benzeri paket veya başka açık browser dal sonucu olabilir
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey isimli bir browser-gerekli acquisition sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon browser-dynamic acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler render success, timeout, browser_error, degraded dallar ve downstream payload anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz browser sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: REAL-RULE AST REPAIR / DEF write_screenshot
# EN: write_screenshot is an explicit browser-dynamic acquisition runtime/helper contract.
# EN: Parameters kept explicit here: page, path.
# TR: REAL-RULE AST REPAIR / FONKSIYON write_screenshot
# TR: write_screenshot acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: page, path.
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
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / take_full_page_screenshot
# EN:
# EN: Why this function exists:
# EN: - because browser-dynamic acquisition truth for 'take_full_page_screenshot' should be exposed through one named top-level boundary
# EN: - because rendered-page and browser-driven semantics should remain readable instead of being hidden in broader acquisition layers
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: page, path
# EN: - values should match the current Python signature and the browser-dynamic acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a browser-dynamic acquisition result shape defined by the current function body
# EN: - this may be a rendered-page payload, browser execution result, fetched_page-style package, or another explicit browser branch result
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface likely performs browser startup, navigation, render waiting, rendered-content shaping, or browser result packaging
# EN: - explicit timeout/error/degraded browser visibility is important here
# EN: - later layers depend on this child to keep dynamic rendered results honest and readable
# EN:
# EN: Important beginner reminder:
# EN: - this function is browser-dynamic acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand rendered success, timeout, browser_error, degraded branches, and downstream payload meaning
# EN:
# EN: Undesired behavior:
# EN: - silent browser result mutation
# EN: - vague outputs that hide branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / take_full_page_screenshot
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'take_full_page_screenshot' için browser-dynamic acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü render edilmiş sayfa ve browser güdümlü semantiklerin daha geniş acquisition katmanlarında gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: page, path
# TR: - değerler aşağıdaki mevcut Python imzası ve browser-dynamic acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen browser-dynamic acquisition sonuç şekli
# TR: - bu; render edilmiş sayfa payloadı, browser execution sonucu, fetched_page benzeri paket veya başka açık browser dal sonucu olabilir
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser başlatma, navigation, render bekleme, render edilmiş içerik şekillendirme veya browser sonucu paketleme işini yapar
# TR: - açık timeout/error/degraded browser görünürlüğü burada önemlidir
# TR: - sonraki katmanlar dynamic render sonuçlarının dürüst ve okunabilir kalması için bu child yüzeye bağımlıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon browser-dynamic acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler render success, timeout, browser_error, degraded dallar ve downstream payload anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz browser sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: REAL-RULE AST REPAIR / DEF take_full_page_screenshot
# EN: take_full_page_screenshot is an explicit browser-dynamic acquisition runtime/helper contract.
# EN: Parameters kept explicit here: page, path.
# TR: REAL-RULE AST REPAIR / FONKSIYON take_full_page_screenshot
# TR: take_full_page_screenshot acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: page, path.
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


# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / acquire_public_page_with_browser
# EN:
# EN: Why this function exists:
# EN: - because browser-dynamic acquisition truth for 'acquire_public_page_with_browser' should be exposed through one named top-level boundary
# EN: - because rendered-page and browser-driven semantics should remain readable instead of being hidden in broader acquisition layers
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: target_url, html_output_path, screenshot_output_path, headless, wait_until, timeout_ms, max_network_records
# EN: - values should match the current Python signature and the browser-dynamic acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a browser-dynamic acquisition result shape defined by the current function body
# EN: - this may be a rendered-page payload, browser execution result, fetched_page-style package, or another explicit browser branch result
# EN:
# EN: Common browser-dynamic meaning hints:
# EN: - this surface likely performs browser startup, navigation, render waiting, rendered-content shaping, or browser result packaging
# EN: - explicit timeout/error/degraded browser visibility is important here
# EN: - later layers depend on this child to keep dynamic rendered results honest and readable
# EN:
# EN: Important beginner reminder:
# EN: - this function is browser-dynamic acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand rendered success, timeout, browser_error, degraded branches, and downstream payload meaning
# EN:
# EN: Undesired behavior:
# EN: - silent browser result mutation
# EN: - vague outputs that hide branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / acquire_public_page_with_browser
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'acquire_public_page_with_browser' için browser-dynamic acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü render edilmiş sayfa ve browser güdümlü semantiklerin daha geniş acquisition katmanlarında gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: target_url, html_output_path, screenshot_output_path, headless, wait_until, timeout_ms, max_network_records
# TR: - değerler aşağıdaki mevcut Python imzası ve browser-dynamic acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen browser-dynamic acquisition sonuç şekli
# TR: - bu; render edilmiş sayfa payloadı, browser execution sonucu, fetched_page benzeri paket veya başka açık browser dal sonucu olabilir
# TR:
# TR: Ortak browser-dynamic anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser başlatma, navigation, render bekleme, render edilmiş içerik şekillendirme veya browser sonucu paketleme işini yapar
# TR: - açık timeout/error/degraded browser görünürlüğü burada önemlidir
# TR: - sonraki katmanlar dynamic render sonuçlarının dürüst ve okunabilir kalması için bu child yüzeye bağımlıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon browser-dynamic acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler render success, timeout, browser_error, degraded dallar ve downstream payload anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz browser sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: REAL-RULE AST REPAIR / DEF acquire_public_page_with_browser
# EN: acquire_public_page_with_browser is an explicit browser-dynamic acquisition runtime/helper contract.
# EN: Parameters kept explicit here: target_url, html_output_path, screenshot_output_path, headless, wait_until, timeout_ms, max_network_records.
# TR: REAL-RULE AST REPAIR / FONKSIYON acquire_public_page_with_browser
# TR: acquire_public_page_with_browser acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: target_url, html_output_path, screenshot_output_path, headless, wait_until, timeout_ms, max_network_records.
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
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / launched
    # EN: launched are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / launched
    # TR: launched burada acik ara dal degerleri olarak atanir.
    launched = False
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / goto_ok
    # EN: goto_ok are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / goto_ok
    # TR: goto_ok burada acik ara dal degerleri olarak atanir.
    goto_ok = False
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / final_url
    # EN: final_url are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / final_url
    # TR: final_url burada acik ara dal degerleri olarak atanir.
    final_url: str | None = None
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / title
    # EN: title are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / title
    # TR: title burada acik ara dal degerleri olarak atanir.
    title: str | None = None
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / rendered_html
    # EN: rendered_html are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / rendered_html
    # TR: rendered_html burada acik ara dal degerleri olarak atanir.
    rendered_html = ""
    # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / network_records
    # EN: network_records are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / network_records
    # TR: network_records burada acik ara dal degerleri olarak atanir.
    network_records: list[BrowserNetworkRecord] = []

    # EN: This nested callback captures each visible browser response in a narrow
    # EN: serializable format.
    # TR: Bu iç callback, görünen her browser response'unu dar ve serileştirilebilir
    # TR: biçimde yakalar.
# EN: BROWSER DYNAMIC FUNCTION PURPOSE MEMORY BLOCK V6 / on_response
# EN:
# EN: This nested function exists so the browser-dynamic corridor keeps one named and auditable step for 'on_response'.
# EN: Why this function exists:
# EN: - to keep browser-driven render/navigation/result semantics visible
# EN: - to keep dynamic branches readable for someone tracing browser-required acquisition from top to bottom
# EN: Accepted input:
# EN: - explicit parameters currently visible here: response
# EN: Accepted output:
# EN: - a result shape defined by the live body below; this may be a rendered-page payload, browser callback effect, response-side mutation, or explicit degraded branch
# EN: Undesired behavior:
# EN: - hidden browser-side mutation
# EN: - unlabeled branch meaning
# TR: BROWSER DYNAMIC FUNCTION AMAÇ HAFIZA BLOĞU V6 / on_response
# TR:
# TR: Bu nested fonksiyon, browser-dynamic koridorunun 'on_response' için tek, isimli ve denetlenebilir bir adım taşıması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - browser güdümlü render/navigation/sonuç semantiklerini görünür tutmak için
# TR: - browser-gerekli acquisition izini yukarıdan aşağı takip eden birinin dynamic dalları okuyabilmesi için
# TR: Kabul edilen girdi:
# TR: - burada şu an görülen açık parametreler: response
# TR: Kabul edilen çıktı:
# TR: - aşağıdaki canlı gövdenin tanımladığı sonuç şekli; bu render edilmiş sayfa payloadı, browser callback etkisi, response tarafı mutasyonu veya açık degraded dal olabilir
# TR: İstenmeyen davranış:
# TR: - gizli browser tarafı mutasyonu
# TR: - etiketsiz dal anlamı

    # EN: REAL-RULE AST REPAIR / DEF on_response
    # EN: on_response is an explicit browser-dynamic acquisition runtime/helper contract.
    # EN: Parameters kept explicit here: response.
    # TR: REAL-RULE AST REPAIR / FONKSIYON on_response
    # TR: on_response acik bir browser-dynamic acquisition runtime/helper sozlesmesidir.
    # TR: Burada acik tutulan parametreler: response.
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
        # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / launched
        # EN: launched are assigned here as explicit intermediate branch values.
        # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / launched
        # TR: launched burada acik ara dal degerleri olarak atanir.
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
            # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / goto_ok
            # EN: goto_ok are assigned here as explicit intermediate branch values.
            # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / goto_ok
            # TR: goto_ok burada acik ara dal degerleri olarak atanir.
            goto_ok = True

            # EN: After navigation we read browser-observed final URL and title.
            # TR: Navigasyon sonrasında browser tarafından gözlenen final URL ve
            # TR: title bilgisini okuyoruz.
            # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / final_url
            # EN: final_url are assigned here as explicit intermediate branch values.
            # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / final_url
            # TR: final_url burada acik ara dal degerleri olarak atanir.
            final_url = page.url
            # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / title
            # EN: title are assigned here as explicit intermediate branch values.
            # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / title
            # TR: title burada acik ara dal degerleri olarak atanir.
            title = page.title()

            # EN: page.content returns the rendered DOM snapshot, not merely the
            # EN: original raw HTTP body.
            # TR: page.content yalnızca ilk ham HTTP body'yi değil, rendered DOM
            # TR: snapshot'ını döndürür.
            # EN: REAL-RULE AST REPAIR / LOCAL acquire_public_page_with_browser / rendered_html
            # EN: rendered_html are assigned here as explicit intermediate branch values.
            # TR: REAL-RULE AST REPAIR / YEREL acquire_public_page_with_browser / rendered_html
            # TR: rendered_html burada acik ara dal degerleri olarak atanir.
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
