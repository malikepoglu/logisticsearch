"""
EN:
This file is the narrow direct-http-page acquisition child beneath the broader acquisition family.

EN:
Why this file exists:
- because the crawler needs one exact place where the plain HTTP page corridor is explained without mixing it with browser-driven or robots-specific acquisition surfaces
- because acquisition_method=http_page, request execution, response handling, fetched_page shaping, and degraded HTTP outcomes must remain readable
- because a beginner should be able to answer: when the crawler does not need a browser, where exactly is the direct HTTP acquisition path implemented

EN:
What this file DOES:
- expose the direct HTTP page acquisition function boundary
- preserve visible request/response meaning, fetched_page shaping, and degraded HTTP branch meaning
- keep plain HTTP acquisition semantics separate from browser-page and browser-dynamic children

EN:
What this file DOES NOT do:
- it does not become the whole acquisition parent
- it does not become the browser implementation
- it does not become the parse or storage layer
- it does not hide HTTP failures behind vague success-looking payloads

EN:
Topological role:
- acquisition parent chooses or delegates into this child when the selected method is direct http_page
- this child performs the narrow plain-HTTP fetch corridor and shapes a fetched_page-compatible result
- later layers such as fetch_finalize, parse, taxonomy, and storage consume what this child returns

EN:
Important visible values and shapes:
- acquisition_method => commonly http_page in this child
- fetched_page => explicit direct-HTTP result payload sent downstream
- request/response helper values => visible indicators of what URL was requested and what came back
- degraded branch payloads => explicit timeout/network/error/non-happy HTTP outcomes that must stay readable

EN:
Accepted architectural identity:
- direct http-page acquisition child
- narrow plain-HTTP fetch contract layer
- readable non-browser fetch boundary

EN:
Undesired architectural identity:
- vague requests helper dump
- hidden second acquisition parent
- hidden browser fallback surface
- hidden side-effect maze

TR:
Bu dosya daha geniş acquisition ailesinin altındaki dar direct-http-page acquisition child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü crawler browser güdümlü veya robots-özel acquisition yüzeyleri ile karıştırmadan plain HTTP page koridorunu açıklayan tek ve tam bir yere ihtiyaç duyar
- çünkü acquisition_method=http_page, request çalıştırması, response işleme, fetched_page şekillendirme ve degraded HTTP sonuçları okunabilir kalmalıdır
- çünkü yeni başlayan biri şu soruya cevap verebilmelidir: crawler browser gerektirmediğinde direct HTTP acquisition yolu tam olarak nerede uygulanır

TR:
Bu dosya NE yapar:
- direct HTTP page acquisition fonksiyon sınırını açığa çıkarır
- request/response anlamını, fetched_page şekillendirmeyi ve degraded HTTP dal anlamını görünür tutar
- plain HTTP acquisition semantiklerini browser-page ve browser-dynamic child yüzeylerinden ayrı tutar

TR:
Bu dosya NE yapmaz:
- acquisition parent yüzeyinin tamamı olmaz
- browser implementasyonu olmaz
- parse veya storage katmanı olmaz
- HTTP hatalarını belirsiz başarıya benzeyen payloadların arkasına gizlemez

TR:
Topolojik rol:
- acquisition parent seçilen method direct http_page olduğunda bu child yüzeye delegasyon yapar
- bu child dar plain-HTTP fetch koridorunu çalıştırır ve fetched_page uyumlu sonuç şekillendirir
- fetch_finalize, parse, taxonomy ve storage gibi sonraki katmanlar bu child yüzeyin döndürdüğü sonucu tüketir

TR:
Önemli görünür değerler ve şekiller:
- acquisition_method => bu child yüzeyde çoğu zaman http_page
- fetched_page => aşağı katmanlara gönderilen açık direct-HTTP sonuç payloadı
- request/response yardımcı değerleri => hangi URLnin istendiğini ve ne döndüğünü anlatan görünür göstergeler
- degraded dal payloadları => okunabilir kalması gereken timeout/network/error/mutlu-yol-dışı HTTP sonuçları

TR:
Kabul edilen mimari kimlik:
- direct http-page acquisition child
- dar plain-HTTP fetch sözleşme katmanı
- okunabilir non-browser fetch sınırı

TR:
İstenmeyen mimari kimlik:
- belirsiz requests helper çöplüğü
- gizli ikinci acquisition parent
- gizli browser fallback yüzeyi
- gizli yan-etki labirenti
"""

# EN: This module is the direct HTTP page-acquisition child surface.
# EN: It should do only one thing: fetch one page through direct HTTP and persist
# EN: the raw body under the controlled raw acquisition tree.
# TR: Bu modül doğrudan HTTP page-acquisition alt yüzeyidir.
# TR: Yalnızca tek iş yapmalıdır: bir sayfayı doğrudan HTTP üzerinden fetch etmek
# TR: ve ham body'yi kontrollü raw acquisition ağacı altına yazmak.

# EN: HTTP PAGE ACQUISITION IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow direct-http child inside the acquisition family.
# EN: Beginner mental model:
# EN: - the acquisition parent decides that a browser is not needed
# EN: - this child then performs the plain HTTP corridor
# EN: - it exists so the crawler can later answer: which direct HTTP request path ran, what response came back, and how fetched_page was shaped
# EN:
# EN: Accepted architectural meaning:
# EN: - named direct-http acquisition child
# EN: - focused request/response and fetched_page shaping surface
# EN: - readable non-browser acquisition boundary
# EN:
# EN: Undesired architectural meaning:
# EN: - random requests helper pile
# EN: - hidden browser substitute
# EN: - place where direct HTTP failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - acquisition_method should stay explicit as http_page here
# EN: - fetched_page should stay structured and readable
# EN: - degraded HTTP branches must remain visible
# TR: HTTP PAGE ACQUISITION KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya acquisition ailesinin içindeki dar direct-http child gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition parent browser gerekmediğine karar verir
# TR: - ardından bu child plain HTTP koridorunu çalıştırır
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: hangi direct HTTP request yolu çalıştı, hangi response geldi ve fetched_page nasıl şekillendi
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli direct-http acquisition child
# TR: - odaklı request/response ve fetched_page shaping yüzeyi
# TR: - okunabilir non-browser acquisition sınırı
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele requests helper yığını
# TR: - gizli browser yerine geçen yüzey
# TR: - direct HTTP hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - acquisition_method burada açık biçimde http_page kalmalıdır
# TR: - fetched_page yapılı ve okunabilir kalmalıdır
# TR: - degraded HTTP dalları görünür kalmalıdır

# EN: HTTP PAGE ACQUISITION DENSITY LIFT MEMORY BLOCK V7
# EN:
# EN: This extra density block exists because the direct-http child must be readable even for someone who has never built a crawler before.
# EN: Very simple mental model:
# EN: - a worker already has a claimed work item
# EN: - the broader acquisition parent already chose the plain HTTP path instead of a browser path
# EN: - this child performs the actual non-browser fetch attempt
# EN: - it then shapes the result into a downstream-friendly fetched_page style payload
# EN:
# EN: Why this direct-http child matters so much:
# EN: - because direct HTTP is usually the cheapest acquisition corridor
# EN: - because it should stay clearly separate from browser-based corridors
# EN: - because later parse logic must know whether content came from a simple HTTP request or a more expensive browser run
# EN: - because operators must be able to inspect timeout, network_error, non-200, or malformed response outcomes without guessing
# EN:
# EN: Important beginner-first reminders:
# EN: - acquisition_method here should normally mean http_page
# EN: - if a browser is needed, that choice belongs in a different child surface
# EN: - fetched_page should remain explicit, structured, and honest
# EN: - degraded HTTP outcomes must not be made to look like successful pages
# EN:
# EN: Typical accepted values and meanings in this corridor:
# EN: - acquisition_method=http_page => plain HTTP path selected
# EN: - acquisition_method=None => no real HTTP acquisition method was chosen on that branch
# EN: - outcome-like values can later represent success, timeout, network_error, retryable_error, or permanent_error depending on wider contracts
# EN: - fetched_page commonly stays dict-shaped when successful and may stay missing/None-like on non-success branches depending on the current function contract
# EN:
# EN: Undesired meanings:
# EN: - hidden browser fallback
# EN: - unclear response semantics
# EN: - silent mutation of direct HTTP failure into fake success
# EN: - vague helper naming that hides whether we still have a request, a response, or a shaped page payload
# TR: HTTP PAGE ACQUISITION YOĞUNLUK ARTIRMA HAFIZA BLOĞU V7
# TR:
# TR: Bu ek yoğunluk bloğu, direct-http child yüzeyinin crawlerı hiç kurmamış biri için bile okunabilir kalması gerektiği için vardır.
# TR: Çok basit zihinsel model:
# TR: - bir worker zaten claim edilmiş bir iş öğesine sahiptir
# TR: - daha geniş acquisition parent yüzeyi plain HTTP yolunu browser yolu yerine çoktan seçmiştir
# TR: - bu child gerçek non-browser fetch denemesini çalıştırır
# TR: - sonra sonucu downstream tarafın okuyabileceği fetched_page benzeri payload şekline dönüştürür
# TR:
# TR: Bu direct-http child neden bu kadar önemlidir:
# TR: - çünkü direct HTTP çoğu zaman en ucuz acquisition koridorudur
# TR: - çünkü browser tabanlı koridorlardan açık biçimde ayrı kalmalıdır
# TR: - çünkü sonraki parse mantığı içeriğin basit HTTP isteğinden mi yoksa daha pahalı browser çalıştırmasından mı geldiğini bilmelidir
# TR: - çünkü operatörler timeout, network_error, non-200 veya bozuk response sonuçlarını tahmin etmeden inceleyebilmelidir
# TR:
# TR: Önemli başlangıç seviyesi hatırlatmalar:
# TR: - acquisition_method burada normalde http_page anlamına gelmelidir
# TR: - browser gerekiyorsa bu seçim başka bir child yüzeye aittir
# TR: - fetched_page açık, yapılı ve dürüst kalmalıdır
# TR: - degraded HTTP sonuçları başarılı sayfa gibi gösterilmemelidir
# TR:
# TR: Bu koridorda tipik kabul edilen değerler ve anlamları:
# TR: - acquisition_method=http_page => plain HTTP yolu seçildi
# TR: - acquisition_method=None => o dalda gerçek HTTP acquisition method seçilmedi
# TR: - outcome-benzeri değerler daha geniş sözleşmelere göre success, timeout, network_error, retryable_error veya permanent_error anlamı taşıyabilir
# TR: - fetched_page başarı dalında çoğu zaman dict şekilli kalır; başarısız dallarda mevcut fonksiyon sözleşmesine göre eksik/None-benzeri kalabilir
# TR:
# TR: İstenmeyen anlamlar:
# TR: - gizli browser fallback
# TR: - belirsiz response semantiği
# TR: - direct HTTP başarısızlığının sessizce sahte başarıya çevrilmesi
# TR: - hâlâ elimizde request mi, response mu, yoksa şekillendirilmiş sayfa payloadı mı olduğunu gizleyen muğlak helper isimlendirmesi

# EN: STAGE21-AUTO-COMMENT :: This import line declares HTTP acquisition runtime dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which request helpers, parsers, contracts, or normalization rules shape fetch behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether request semantics, timeout handling, or payload shaping changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak HTTP acquisition runtime bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi istek yardımcılarının, ayrıştırıcıların, sözleşmelerin veya normalizasyon kurallarının fetch davranışını şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse istek anlamının, zaman aşımı yönetiminin veya yük şekillendirmenin de değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil mimari ipucu olarak ele alır.
from __future__ import annotations

# EN: We import Path because the child surface exposes a configurable raw_root
# EN: path in its explicit function signature.
# TR: Bu alt yüzey açık fonksiyon imzasında yapılandırılabilir raw_root yolu
# TR: sunduğu için Path içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares HTTP acquisition runtime dependencies by bringing in pathlib -> Path.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which request helpers, parsers, contracts, or normalization rules shape fetch behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether request semantics, timeout handling, or payload shaping changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı pathlib -> Path ögelerini içeri alarak HTTP acquisition runtime bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi istek yardımcılarının, ayrıştırıcıların, sözleşmelerin veya normalizasyon kurallarının fetch davranışını şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse istek anlamının, zaman aşımı yönetiminin veya yük şekillendirmenin de değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil mimari ipucu olarak ele alır.
from pathlib import Path

# EN: We import Request and urlopen from the standard library so this direct HTTP
# EN: child stays dependency-light and fully explicit.
# TR: Bu doğrudan HTTP alt yüzeyi dependency açısından hafif ve tamamen açık
# TR: kalsın diye Request ve urlopen'u standart kütüphaneden içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares HTTP acquisition runtime dependencies by bringing in urllib.request -> Request, urlopen.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which request helpers, parsers, contracts, or normalization rules shape fetch behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether request semantics, timeout handling, or payload shaping changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı urllib.request -> Request, urlopen ögelerini içeri alarak HTTP acquisition runtime bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi istek yardımcılarının, ayrıştırıcıların, sözleşmelerin veya normalizasyon kurallarının fetch davranışını şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse istek anlamının, zaman aşımı yönetiminin veya yük şekillendirmenin de değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil mimari ipucu olarak ele alır.
from urllib.request import Request, urlopen

# EN: We import the shared acquisition support surface so this child reuses the
# EN: same stable artefact/result contract as the rest of the acquisition family.
# TR: Bu alt yüzey acquisition ailesinin geri kalanıyla aynı kararlı artefact/sonuç
# TR: sözleşmesini yeniden kullansın diye paylaşılan acquisition destek yüzeyini
# TR: içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares HTTP acquisition runtime dependencies by bringing in .logisticsearch1_1_2_4_1_acquisition_support -> RAW_FETCH_ROOT, FetchedPageResult, build_raw_fetch_storage_path, ensure_parent_directory, get_claimed_url_value, sha256_hex, utc_now.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which request helpers, parsers, contracts, or normalization rules shape fetch behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether request semantics, timeout handling, or payload shaping changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_2_4_1_acquisition_support -> RAW_FETCH_ROOT, FetchedPageResult, build_raw_fetch_storage_path, ensure_parent_directory, get_claimed_url_value, sha256_hex, utc_now ögelerini içeri alarak HTTP acquisition runtime bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi istek yardımcılarının, ayrıştırıcıların, sözleşmelerin veya normalizasyon kurallarının fetch davranışını şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse istek anlamının, zaman aşımı yönetiminin veya yük şekillendirmenin de değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil mimari ipucu olarak ele alır.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedPageResult,
    build_raw_fetch_storage_path,
    ensure_parent_directory,
    get_claimed_url_value,
    sha256_hex,
    utc_now,
)


# EN: This function performs one real HTTP fetch and writes the raw response body
# EN: under the controlled /srv raw-fetch subtree.
# TR: Bu fonksiyon tek bir gerçek HTTP fetch işlemi yapar ve ham yanıt body'sini
# TR: kontrollü /srv raw-fetch alt ağacına yazar.
# EN: HTTP PAGE FUNCTION PURPOSE MEMORY BLOCK V6 / fetch_page_to_raw_storage
# EN:
# EN: Why this function exists:
# EN: - because direct HTTP acquisition truth for 'fetch_page_to_raw_storage' should be exposed through one named top-level boundary
# EN: - because request/response semantics should remain readable instead of being hidden in the broader acquisition family
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, timeout_seconds, raw_root
# EN: - values should match the current Python signature and the direct-http acquisition contract below
# EN:
# EN: Accepted output:
# EN: - a direct-http acquisition result shape defined by the current function body
# EN: - this may be a fetched_page payload, request/response result, or another explicit direct-http branch result
# EN:
# EN: Common http-page acquisition meaning hints:
# EN: - this surface likely performs plain HTTP request/response work and shapes fetched_page payloads
# EN: - explicit timeout/network/error visibility is important here
# EN: - later layers depend on this child to keep direct HTTP results honest and readable
# EN:
# EN: Important beginner reminder:
# EN: - this function is narrow direct-http acquisition logic, not the whole acquisition family
# EN: - results must stay explicit so audits can understand success, timeout, network_error, and downstream fetched_page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent HTTP result mutation
# EN: - vague outputs that hide branch meaning
# TR: HTTP PAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / fetch_page_to_raw_storage
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'fetch_page_to_raw_storage' için direct HTTP acquisition doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü request/response semantiklerinin daha geniş acquisition ailesi içinde gizlenmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, timeout_seconds, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve direct-http acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen direct-http acquisition sonuç şekli
# TR: - bu; fetched_page payloadı, request/response sonucu veya başka açık direct-http dal sonucu olabilir
# TR:
# TR: Ortak http-page acquisition anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle plain HTTP request/response işini yapar ve fetched_page payloadlarını şekillendirir
# TR: - açık timeout/network/error görünürlüğü burada önemlidir
# TR: - sonraki katmanlar direct HTTP sonuçlarının dürüst ve okunabilir kalması için bu child yüzeye bağımlıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon dar direct-http acquisition mantığıdır, acquisition ailesinin tamamı değildir
# TR: - sonuçlar açık kalmalıdır ki denetimler success, timeout, network_error ve downstream fetched_page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz HTTP sonuç değişimi
# TR: - dal anlamını gizleyen belirsiz çıktılar

# EN: HTTP PAGE FUNCTION DENSITY LIFT MEMORY BLOCK V7 / fetch_page_to_raw_storage
# EN:
# EN: Beginner-first reading note:
# EN: - read this function as one exact step inside the plain HTTP corridor
# EN: - ask four questions while reading it:
# EN:   1) what input does it accept
# EN:   2) what part of the direct HTTP path does it perform
# EN:   3) what output shape does it return
# EN:   4) how does it behave on non-happy branches
# EN:
# EN: Direct-http contract reminders:
# EN: - accepted values should stay aligned with a plain HTTP page attempt
# EN: - response-like values should not be confused with browser-rendered outputs
# EN: - shaped fetched_page results should stay clearly distinguishable from raw transport results
# EN: - timeout/network/degraded meanings should remain explicit
# TR: HTTP PAGE FUNCTION YOĞUNLUK ARTIRMA HAFIZA BLOĞU V7 / {name}
# TR:
# TR: Başlangıç seviyesi okuma notu:
# TR: - bu fonksiyonu plain HTTP koridorunun içindeki tek ve açık adım gibi oku
# TR: - okurken dört soru sor:
# TR:   1) hangi girdiyi kabul ediyor
# TR:   2) direct HTTP yolunun hangi parçasını yapıyor
# TR:   3) hangi çıktı şeklini döndürüyor
# TR:   4) mutlu-yol-dışı dallarda nasıl davranıyor
# TR:
# TR: Direct-http sözleşme hatırlatmaları:
# TR: - kabul edilen değerler plain HTTP page denemesi ile uyumlu kalmalıdır
# TR: - response-benzeri değerler browser-rendered çıktılarla karıştırılmamalıdır
# TR: - şekillendirilmiş fetched_page sonuçları ham transport sonuçlarından açıkça ayrılmalıdır
# TR: - timeout/network/degraded anlamları görünür kalmalıdır

# EN: STAGE21-AUTO-COMMENT :: This HTTP acquisition function named fetch_page_to_raw_storage defines a runtime entry point for fetching a page through the non-browser path.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what fetch_page_to_raw_storage sends over the network, what it accepts back, and what normalized result it returns.
# EN: STAGE21-AUTO-COMMENT :: When editing fetch_page_to_raw_storage, confirm that request construction, response interpretation, and downstream contract shape stay aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker makes the beginning of fetch_page_to_raw_storage easy to find during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: fetch_page_to_raw_storage isimli bu HTTP acquisition fonksiyonu browser olmayan yol üzerinden sayfa çekmek için bir runtime giriş noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu fetch_page_to_raw_storage fonksiyonunun ağ üzerinden ne gönderdiğini, ne geri aldığını ve hangi normalize sonucu döndürdüğünü anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: fetch_page_to_raw_storage düzenlenirken istek kurulumu, yanıt yorumlama ve aşağı akış sözleşme biçiminin hizalı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch_page_to_raw_storage başlangıcını denetim ve olay incelemesi sırasında kolay bulunur hale getirir.
# EN: claimed_url is the claimed frontier work item object whose url_id and requested_url values drive the direct HTTP request and raw artefact naming.
# EN: timeout_seconds is the plain-HTTP timeout budget for this non-browser request path, and raw_root is the controlled filesystem root under which the raw response body will be persisted.
# TR: claimed_url, direct HTTP isteğini ve ham artefact adlandırmasını süren url_id ve requested_url değerlerini taşıyan claim edilmiş frontier iş öğesi nesnesidir.
# TR: timeout_seconds bu browser olmayan istek yolu için plain-HTTP timeout bütçesidir; raw_root ise ham response body'nin persist edileceği kontrollü filesystem köküdür.
def fetch_page_to_raw_storage(
    claimed_url: object,
    *,
    timeout_seconds: int = 30,
    raw_root: Path = RAW_FETCH_ROOT,
) -> FetchedPageResult:
    # EN: We read the claimed frontier url id because the raw artefact filename
    # EN: should stay directly traceable to the frontier work item.
    # TR: Ham artefact dosya adı frontier iş öğesine doğrudan izlenebilir kalsın
    # TR: diye claim edilmiş frontier url kimliğini okuyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates url_id as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama url_id değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))

    # EN: We read the requested canonical URL because it is the actual fetch target.
    # TR: Gerçek fetch hedefi olduğu için istenen canonical URL'yi okuyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates requested_url as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama requested_url değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    requested_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We read the user-agent token because crawler politeness and identity
    # EN: should be visible in the outgoing HTTP request.
    # TR: Crawler politeness ve kimliği giden HTTP isteğinde görünür olmalı diye
    # TR: user-agent token'ını okuyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates user_agent_token as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama user_agent_token değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    user_agent_token = str(get_claimed_url_value(claimed_url, "user_agent_token"))

    # EN: We capture the current UTC fetch time before network I/O so storage path
    # EN: and result metadata stay tied to one explicit moment.
    # TR: Storage yolu ve sonuç metadata'sı tek bir açık ana bağlı kalsın diye
    # TR: ağ I/O'sundan önce mevcut UTC fetch zamanını yakalıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates fetched_at as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama fetched_at değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    fetched_at = utc_now()

    # EN: We build a minimal HTTP request using only the current explicit crawler identity.
    # TR: Yalnızca mevcut açık crawler kimliğini kullanarak asgari bir HTTP isteği kuruyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates request as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama request değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    request = Request(
        requested_url,
        headers={
            "User-Agent": user_agent_token,
            "Accept": "*/*",
        },
    )

    # EN: We execute the real HTTP request with the caller-supplied timeout.
    # TR: Gerçek HTTP isteğini çağıran tarafından verilen timeout ile çalıştırıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible HTTP acquisition flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface affects large-scale crawl behavior.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intent and wider fetch meaning stay aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact runtime code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür HTTP acquisition akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey büyük ölçekli crawl davranışını etkiler.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş fetch anlamı hizalı kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık runtime kodunun sessiz anlam gizlemesini önler.
    with urlopen(request, timeout=timeout_seconds) as response:
        # EN: final_url captures the post-redirect visible final destination.
        # TR: final_url redirect sonrası görünen son hedefi yakalar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates final_url as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama final_url değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        final_url = str(response.geturl())

        # EN: http_status captures the numeric response code.
        # TR: http_status sayısal yanıt kodunu yakalar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates http_status as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama http_status değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        http_status = int(response.getcode())

        # EN: content_type captures the visible Content-Type header when present.
        # TR: content_type varsa görünür Content-Type başlığını yakalar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates content_type as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama content_type değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        content_type = response.headers.get("Content-Type")

        # EN: etag captures the visible ETag header when present.
        # TR: etag varsa görünür ETag başlığını yakalar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates etag as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama etag değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        etag = response.headers.get("ETag")

        # EN: last_modified captures the visible Last-Modified header when present.
        # TR: last_modified varsa görünür Last-Modified başlığını yakalar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates last_modified as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama last_modified değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        last_modified = response.headers.get("Last-Modified")

        # EN: body stores the full raw response bytes exactly as returned by the server.
        # TR: body sunucunun döndürdüğü tam ham yanıt byte'larını olduğu gibi tutar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates body as part of the HTTP page acquisition flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama body değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
        body = response.read()

    # EN: We compute the deterministic storage path only after fetch metadata is known.
    # TR: Deterministik storage yolunu ancak fetch metadata'sı bilindikten sonra hesaplıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates raw_storage_path as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama raw_storage_path değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    raw_storage_path = build_raw_fetch_storage_path(
        url_id=url_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )

    # EN: We ensure the target parent directory exists before writing bytes.
    # TR: Byte yazmadan önce hedef parent dizinin var olduğundan emin oluyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct runtime action, often a call that advances the HTTP fetch process toward a normalized result.
    # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because compact calls can hide meaningful network-side effects.
    # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in this runtime layer and still matches fetch policy.
    # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan bir runtime eylemi gerçekleştirir; çoğu zaman HTTP fetch sürecini normalize sonuca doğru ilerleten bir çağrıdır.
    # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık çağrılar anlamlı ağ yan etkilerini gizleyebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ bu runtime katmanına ait olduğu ve fetch politikasıyla eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etki gerçekleştiğini söyler.
    ensure_parent_directory(raw_storage_path)

    # EN: We write the raw bytes in binary mode because HTTP bodies are not guaranteed
    # EN: to be valid text.
    # TR: HTTP body'lerinin geçerli metin olması garanti olmadığı için ham byte'ları
    # TR: binary modda yazıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct runtime action, often a call that advances the HTTP fetch process toward a normalized result.
    # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because compact calls can hide meaningful network-side effects.
    # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in this runtime layer and still matches fetch policy.
    # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan bir runtime eylemi gerçekleştirir; çoğu zaman HTTP fetch sürecini normalize sonuca doğru ilerleten bir çağrıdır.
    # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık çağrılar anlamlı ağ yan etkilerini gizleyebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ bu runtime katmanına ait olduğu ve fetch politikasıyla eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etki gerçekleştiğini söyler.
    raw_storage_path.write_bytes(body)

    # EN: We compute the body fingerprint after the body bytes are finalized.
    # TR: Body byte'ları kesinleştikten sonra body parmak izini hesaplıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates raw_sha256 as part of the HTTP page acquisition flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama raw_sha256 değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
    raw_sha256 = sha256_hex(body)

    # EN: We return one explicit structured fetch result.
    # TR: Tek bir açık yapılı fetch sonucu döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete HTTP acquisition result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical contract that the rest of the crawler sees after a fetch attempt finishes.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected shape, semantics, and provenance details.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir HTTP acquisition sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları fetch denemesi tamamlandıktan sonra crawler'ın geri kalanının gördüğü pratik sözleşmeyi tanımlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, anlamı ve köken ayrıntılarını almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return FetchedPageResult(
        url_id=url_id,
        requested_url=requested_url,
        final_url=final_url,
        http_status=http_status,
        content_type=content_type,
        etag=etag,
        last_modified=last_modified,
        body_bytes=len(body),
        raw_storage_path=str(raw_storage_path),
        raw_sha256=raw_sha256,
        fetched_at=fetched_at.isoformat(),
    )

# EN: This export list keeps the direct HTTP child surface explicit.
# TR: Bu export listesi doğrudan HTTP alt yüzeyini açık tutar.
# EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates __all__ as part of the HTTP page acquisition flow.
# EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn raw network data into validated runtime state and should stay easy to audit.
# EN: STAGE21-AUTO-COMMENT :: When this value changes, verify that callers and downstream finalization logic still interpret it correctly.
# EN: STAGE21-AUTO-COMMENT :: This marker highlights where fetch state becomes concrete.
# TR: STAGE21-AUTO-COMMENT :: Bu atama __all__ değerlerini HTTP sayfa edinim akışının parçası olarak tanımlar veya günceller.
# TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham ağ verisini doğrulanmış runtime durumuna dönüştürür ve kolay denetlenebilir kalmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıranların ve aşağı akış finalize mantığının onu hâlâ doğru yorumladığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch durumunun somutlaştığı yeri vurgular.
__all__ = [
    "fetch_page_to_raw_storage",
]
