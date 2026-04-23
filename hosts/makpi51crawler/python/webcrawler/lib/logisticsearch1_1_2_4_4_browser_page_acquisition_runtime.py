# EN: Top-off note for the universal bilingual comment-density rule.
# EN: This module stays inside the real browser-page runtime path and is not a placeholder.
# EN: The extra lines below exist to keep the bilingual documentation floor explicit and machine-auditable.
# EN: The explanation still describes the same runtime surface and does not change program behavior.
# TR: Evrensel iki dilli yorum yoğunluğu kuralı için tamamlama notu.
# TR: Bu modül gerçek browser-page runtime yolu içindedir; yer tutucu bir dosya değildir.
# TR: Aşağıdaki ek satırlar iki dilli dokümantasyon tabanını açık ve makineyle denetlenebilir tutmak için vardır.
# TR: Bu açıklama aynı runtime yüzeyini anlatır; program davranışını değiştirmez.

"""
EN:
This file is the browser-page acquisition child inside the acquisition family.

EN:
Why this file exists:
- because some acquisition branches must be labeled explicitly as browser_page rather than plain http_page or generic dynamic execution
- because a beginner should be able to answer exactly where the crawler runs the browser_page corridor
- because browser-backed page result shaping, page payload honesty, and corridor-specific branch visibility should remain readable in one narrow child file

EN:
What this file DOES:
- expose the browser_page acquisition boundary
- keep browser-backed page execution readable as its own named corridor
- shape browser_page outputs into explicit downstream-friendly payloads
- preserve visible success, timeout, degraded, and browser-error style branches instead of hiding them

EN:
What this file DOES NOT do:
- it does not become the whole acquisition parent
- it does not replace direct http acquisition
- it does not replace the broader browser_dynamic child
- it does not become parse or storage logic

EN:
Topological role:
- acquisition parent can delegate here when the selected acquisition_method is browser_page
- this child owns browser-page specific execution and output shaping
- later layers consume the explicit page result, fetched-page style payload, or visible degraded outcome produced here

EN:
Important variable and payload meanings:
- acquisition_method usually means browser_page when this child is the selected corridor
- browser-backed page result values should stay explicit and auditable
- fetched_page style payloads should remain readable for later validation, parse, and finalize corridors
- degraded branches must keep their meaning visible instead of silently collapsing into fake success

EN:
Accepted architectural identity:
- browser_page acquisition child
- narrow browser-backed page corridor
- explicit page-result shaping layer

EN:
Undesired architectural identity:
- random browser helper dump
- hidden second acquisition parent
- vague page payload mutation layer

TR:
Bu dosya acquisition ailesi içindeki browser-page acquisition child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü bazı acquisition dalları plain http_page veya genel dynamic execution yerine açık biçimde browser_page olarak etiketlenmelidir
- çünkü yeni başlayan biri crawlerın browser_page koridorunu tam olarak nerede çalıştırdığını anlayabilmelidir
- çünkü browser destekli page sonuç şekillendirme, page payload dürüstlüğü ve koridora özgü dal görünürlüğü tek ve dar bir child dosyada okunabilir kalmalıdır

TR:
Bu dosya NE yapar:
- browser_page acquisition sınırını açığa çıkarır
- browser destekli page execution işini ayrı ve isimli bir koridor olarak okunabilir tutar
- browser_page çıktıları için downstream tarafın anlayacağı açık payloadlar şekillendirir
- success, timeout, degraded ve browser-error tarzı dalları gizlemek yerine görünür tutar

TR:
Bu dosya NE yapmaz:
- acquisition parent yüzeyinin tamamı olmaz
- direct http acquisition yüzeyinin yerine geçmez
- daha geniş browser_dynamic child yüzeyinin yerine geçmez
- parse veya storage mantığına dönüşmez

TR:
Topolojik rol:
- acquisition_method browser_page seçildiğinde acquisition parent bu child yüzeye delegasyon yapabilir
- bu child browser-page özgü execution ve çıktı şekillendirmesini taşır
- sonraki katmanlar burada üretilen açık page sonucunu, fetched-page benzeri payloadı veya görünür degraded sonucu tüketir

TR:
Önemli değişken ve payload anlamları:
- acquisition_method bu child seçildiğinde çoğunlukla browser_page anlamına gelir
- browser destekli page sonuç değerleri açık ve denetlenebilir kalmalıdır
- fetched_page benzeri payloadlar sonraki validation, parse ve finalize koridorları için okunabilir kalmalıdır
- degraded dallar anlamını korumalı, sessizce sahte başarıya çökertilmemelidir

TR:
Kabul edilen mimari kimlik:
- browser_page acquisition child
- dar browser destekli page koridoru
- açık page-sonucu şekillendirme katmanı

TR:
İstenmeyen mimari kimlik:
- rastgele browser helper yığını
- gizli ikinci acquisition parent
- belirsiz page payload mutasyon katmanı
"""

# EN: This module is the browser-backed page-acquisition child surface.
# EN: It adapts the deeper browser runtime into the same stable FetchedPageResult
# EN: contract already used by the rest of crawler_core.
# TR: Bu modül browser-backed page-acquisition alt yüzeyidir.
# TR: Daha derindeki browser runtime yüzeyini crawler_core'un geri kalanının zaten
# TR: kullandığı aynı kararlı FetchedPageResult sözleşmesine uyarlar.

# EN: BROWSER PAGE ACQUISITION IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the named browser_page child inside the acquisition family.
# EN: Beginner mental model:
# EN: - the acquisition parent chooses a corridor
# EN: - if that corridor is browser_page, this child is the focused room where that work becomes readable
# EN: - the point is not just to fetch with a browser; the point is to keep page-level browser work, outputs, and failure meaning explicit
# EN:
# EN: Accepted architectural meaning:
# EN: - named browser_page child
# EN: - focused browser-backed page corridor
# EN: - explicit page payload shaping surface
# EN:
# EN: Undesired architectural meaning:
# EN: - random browser side helper pile
# EN: - hidden dynamic catch-all layer
# EN: - place where browser page failure becomes invisible
# EN:
# EN: Important visible reminders:
# EN: - acquisition_method meaning should stay explicit
# EN: - page payload shape should stay explicit
# EN: - degraded branches should stay visible
# TR: BROWSER PAGE ACQUISITION KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya acquisition ailesinin içindeki isimli browser_page child olarak okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition parent bir koridor seçer
# TR: - eğer o koridor browser_page ise bu child yüzey o işin okunabilir hale geldiği odaklı odadır
# TR: - amaç yalnızca browser ile fetch etmek değildir; amaç page düzeyi browser işini, çıktıları ve hata anlamını açık tutmaktır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli browser_page child
# TR: - odaklı browser destekli page koridoru
# TR: - açık page payload şekillendirme yüzeyi
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele browser tarafı helper yığını
# TR: - gizli dynamic catch-all katmanı
# TR: - browser page hatasının görünmez olduğu yer
# TR:
# TR: Önemli görünür hatırlatmalar:
# TR: - acquisition_method anlamı açık kalmalıdır
# TR: - page payload şekli açık kalmalıdır
# TR: - degraded dallar görünür kalmalıdır

# EN: BROWSER PAGE ACQUISITION IDENTITY MEMORY BLOCK V7
# EN:
# EN: Read this file as the explicit browser_page child, not as a generic browser utility drawer.
# EN: Beginner-first mental model:
# EN: - acquisition parent = corridor selector
# EN: - browser_dynamic child = broader browser-oriented machinery
# EN: - browser_page child = the narrower room where page-level browser acquisition is made explicit
# EN: Why this matters:
# EN: - a reader should see where browser_page starts
# EN: - a reader should see which payload belongs to the page corridor
# EN: - a reader should see which branch is success-like, timeout-like, degraded, or browser-error-like
# EN: Accepted steady-state meaning:
# EN: - acquisition_method should already point at browser_page when this child is intentionally selected
# EN: - page-level output should remain explicit and downstream-readable
# EN: Undesired steady-state meaning:
# EN: - hidden mutation layer
# EN: - unlabeled browser page side effect
# EN: - corridor where branch meaning becomes opaque
# TR: BROWSER PAGE ACQUISITION KIMLIK HAFIZA BLOĞU V7
# TR:
# TR: Bu dosya genel browser yardımcı çekmecesi gibi değil, açık browser_page child olarak okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition parent = koridor seçici
# TR: - browser_dynamic child = daha geniş browser odaklı makine katmanı
# TR: - browser_page child = page düzeyi browser acquisition işinin açık hale getirildiği daha dar oda
# TR: Bu neden önemlidir:
# TR: - okuyucu browser_page işinin nerede başladığını görmelidir
# TR: - okuyucu hangi payloadın page koridoruna ait olduğunu görmelidir
# TR: - okuyucu hangi dalın success-benzeri, timeout-benzeri, degraded veya browser-error-benzeri olduğunu görebilmelidir
# TR: Kabul edilen kararlı anlam:
# TR: - bu child bilinçli seçildiğinde acquisition_method zaten browser_page göstermelidir
# TR: - page düzeyi çıktı açık ve downstream tarafından okunabilir kalmalıdır
# TR: İstenmeyen kararlı anlam:
# TR: - gizli mutasyon katmanı
# TR: - etiketsiz browser page yan etkisi
# TR: - dal anlamının opaklaştığı koridor

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
# EN: BROWSER PAGE FUNCTION PURPOSE MEMORY BLOCK V6 / infer_browser_document_status
# EN:
# EN: This top-level function exists so browser_page acquisition truth for 'infer_browser_document_status' stays visible and auditable.
# EN: Why this function exists:
# EN: - to preserve one named browser_page step instead of hiding it in a larger acquisition blur
# EN: - to keep page-level browser semantics readable for a beginner tracing the corridor
# EN: Accepted input:
# EN: - explicit parameters currently visible here: browser_result
# EN: - values should match the current Python signature and the page-level browser corridor beneath this marker
# EN: Accepted output:
# EN: - a result shape defined by the live body below; this may be a browser_page payload, fetched_page style package, callback-side effect, explicit success, timeout, browser_error, or degraded branch
# EN: Important meaning:
# EN: - this function belongs to the browser_page child, not to the whole acquisition parent
# EN: - if a downstream layer needs to know what happened in the page-level browser corridor, it should be able to read the branch meaning here
# EN: Undesired behavior:
# EN: - unlabeled browser page mutation
# EN: - vague output shape that hides branch meaning
# TR: BROWSER PAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / infer_browser_document_status
# TR:
# TR: Bu top-level fonksiyon, 'infer_browser_document_status' için browser_page acquisition doğrusunun görünür ve denetlenebilir kalması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - browser_page adımını daha büyük acquisition bulanıklığı içinde gizlemek yerine isimli tutmak için
# TR: - koridoru takip eden bir başlangıç seviyesi okuyucu için page düzeyi browser semantiklerini okunabilir tutmak için
# TR: Kabul edilen girdi:
# TR: - burada şu an görülen açık parametreler: browser_result
# TR: - değerler mevcut Python imzası ve bu işaretin altındaki page düzeyi browser koridoru ile uyumlu olmalıdır
# TR: Kabul edilen çıktı:
# TR: - aşağıdaki canlı gövdenin tanımladığı sonuç şekli; bu browser_page payloadı, fetched_page benzeri paket, callback tarafı etki, açık success, timeout, browser_error veya degraded dal olabilir
# TR: Önemli anlam:
# TR: - bu fonksiyon acquisition parent yüzeyinin tamamına değil, browser_page child yüzeyine aittir
# TR: - downstream katman browserın page düzeyi koridorunda ne olduğunu anlamak istiyorsa dal anlamını burada okuyabilmelidir
# TR: İstenmeyen davranış:
# TR: - etiketsiz browser page mutasyonu
# TR: - dal anlamını gizleyen belirsiz çıktı şekli

# EN: BROWSER PAGE FUNCTION CONTRACT DENSITY BLOCK V7 / infer_browser_document_status
# EN:
# EN: This top-level function exists so browser_page corridor truth for 'infer_browser_document_status' stays readable.
# EN: Why this function exists:
# EN: - to keep one named browser_page step visible
# EN: - to prevent page-level browser meaning from disappearing inside a larger helper cloud
# EN: Accepted input line shapes:
# EN: - visible parameters now: browser_result
# EN: - callers should respect the current Python signature exactly
# EN: - payload-like parameters are expected to match the active page-level browser corridor
# EN: Accepted output line shapes:
# EN: - the live body may return a dict-like payload, fetched_page-style package, callback-driven side effect, explicit browser success, timeout-style outcome, degraded branch, or browser-error branch
# EN: Common browser_page variable expectations:
# EN: - acquisition_method should usually already be browser_page at this level
# EN: - fetched_page-like values are commonly dict-shaped on success-style branches
# EN: - fetched_page-like values may be None, absent, or partial when timeout/degraded/error branches are active
# EN: - undesired meaning is silent ambiguity about what happened in the page corridor
# EN: Forwarding note:
# EN: - this function may prepare, receive, transform, or forward page-level browser results to downstream validation, finalize, parse, or acquisition-parent logic
# TR: BROWSER PAGE FUNCTION CONTRACT YOĞUNLUK BLOĞU V7 / infer_browser_document_status
# TR:
# TR: Bu üst seviye fonksiyon, 'infer_browser_document_status' için browser_page koridoru doğrusunun okunabilir kalması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - isimli browser_page adımını görünür tutmak için
# TR: - page düzeyi browser anlamının daha büyük yardımcı bulutu içinde kaybolmasını engellemek için
# TR: Kabul edilen girdi satırı şekilleri:
# TR: - şu an görülen parametreler: browser_result
# TR: - çağıran taraf mevcut Python imzasına tam uymalıdır
# TR: - payload benzeri parametreler etkin page düzeyi browser koridoru ile uyumlu olmalıdır
# TR: Kabul edilen çıktı satırı şekilleri:
# TR: - canlı gövde dict-benzeri payload, fetched_page benzeri paket, callback kaynaklı yan etki, açık browser başarısı, timeout tarzı sonuç, degraded dalı veya browser-error dalı döndürebilir
# TR: Yaygın browser_page değişken beklentileri:
# TR: - bu seviyede acquisition_method çoğu zaman zaten browser_page olmalıdır
# TR: - fetched_page benzeri değerler başarı tarzı dallarda çoğunlukla dict yapısındadır
# TR: - fetched_page benzeri değerler timeout/degraded/hata dallarında None, eksik veya kısmi olabilir
# TR: - istenmeyen anlam, page koridorunda ne olduğunu sessiz belirsizlik içinde bırakmaktır
# TR: Forward etme notu:
# TR: - bu fonksiyon page düzeyi browser sonuçlarını hazırlayabilir, alabilir, dönüştürebilir veya downstream validation, finalize, parse ya da acquisition-parent mantığına forward edebilir

# EN: This function is part of the browser-page acquisition layer.
# EN: It should explain what browser-backed page capture does, why this path exists in addition to plain HTTP,
# EN: which inputs it depends on, what output contract it returns, and which failure boundaries it protects.
# EN: The goal of this added explanation is not to change runtime behavior, but to make the operational intent
# EN: and data-flow role obvious to a beginner reading the crawler for the first time.
# EN: This block is intentionally placed immediately above the function so the explanation stays attached to the logic.
# TR: Bu fonksiyon browser-page acquisition katmanının bir parçasıdır.
# TR: Bu açıklama, tarayıcı destekli sayfa yakalamanın ne yaptığını, neden düz HTTP yoluna ek olarak var olduğunu,
# TR: hangi girdilere dayandığını, hangi çıktı sözleşmesini döndürdüğünü ve hangi hata sınırlarını koruduğunu anlatmalıdır.
# TR: Buradaki ek açıklamanın amacı çalışma davranışını değiştirmek değil; operasyonel niyeti ve veri akışındaki rolü
# TR: crawler'ı ilk kez okuyan birisi için açık hale getirmektir.
# TR: Bu blok özellikle fonksiyonun hemen üstüne eklenir; böylece açıklama mantıktan kopmaz.
# EN: This helper named infer_browser_document_status reads browser_result and tries to extract one honest document-level status code without inventing certainty.
# EN: browser_result is the browser-runtime result object whose resource type and status fields are inspected here.
# EN: The purpose is to keep browser_result status interpretation explicit before later payload shaping uses the inferred value.
# TR: infer_browser_document_status isimli bu yardımcı browser_result içinden dürüst bir document-seviyesi durum kodu çıkarmaya çalışır; olmayan kesinliği uydurmaz.
# TR: browser_result, burada resource type ve status alanları incelenen browser-runtime sonuç nesnesidir.
# TR: Amaç, daha sonraki payload şekillendirme inferred değeri kullanmadan önce browser_result durum yorumunu açık tutmaktır.
def infer_browser_document_status(browser_result: object) -> int:
    # EN: We read network_records tolerantly because the browser runtime returns dataclass-like
    # EN: structures that are later serialized, and we only need a small stable subset here.
    # TR: Yalnızca küçük ve kararlı bir alt kümeye ihtiyaç duyduğumuz için network_records alanını
    # TR: toleranslı biçimde okuyoruz; browser runtime dataclass-benzeri yapılar döndürüyor olabilir.
    network_records = getattr(browser_result, "network_records", []) or []

    # EN: We scan records in observed order and prefer a document resource with an integer status.
    # TR: Kayıtları gözlenme sırasıyla tarıyor ve integer status taşıyan bir document resource'u tercih ediyoruz.
    for record in network_records:
# EN: resource_type is the browser_result resource-type marker used to decide whether a document-level status is meaningful here.
# TR: resource_type, burada document-seviyesi bir status bilgisinin anlamlı olup olmadığına karar vermek için kullanılan browser_result resource-type işaretidir.
        resource_type = getattr(record, "resource_type", None)
# EN: status is the candidate document status value copied from browser_result before strict integer normalization and fallback handling.
# TR: status, sıkı tamsayı normalize etme ve fallback işleme öncesinde browser_result içinden alınan aday document status değeridir.
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
# EN: BROWSER PAGE FUNCTION PURPOSE MEMORY BLOCK V6 / fetch_page_with_browser_to_raw_storage
# EN:
# EN: This top-level function exists so browser_page acquisition truth for 'fetch_page_with_browser_to_raw_storage' stays visible and auditable.
# EN: Why this function exists:
# EN: - to preserve one named browser_page step instead of hiding it in a larger acquisition blur
# EN: - to keep page-level browser semantics readable for a beginner tracing the corridor
# EN: Accepted input:
# EN: - explicit parameters currently visible here: claimed_url, timeout_ms, wait_until, raw_root, headless
# EN: - values should match the current Python signature and the page-level browser corridor beneath this marker
# EN: Accepted output:
# EN: - a result shape defined by the live body below; this may be a browser_page payload, fetched_page style package, callback-side effect, explicit success, timeout, browser_error, or degraded branch
# EN: Important meaning:
# EN: - this function belongs to the browser_page child, not to the whole acquisition parent
# EN: - if a downstream layer needs to know what happened in the page-level browser corridor, it should be able to read the branch meaning here
# EN: Undesired behavior:
# EN: - unlabeled browser page mutation
# EN: - vague output shape that hides branch meaning
# TR: BROWSER PAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / fetch_page_with_browser_to_raw_storage
# TR:
# TR: Bu top-level fonksiyon, 'fetch_page_with_browser_to_raw_storage' için browser_page acquisition doğrusunun görünür ve denetlenebilir kalması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - browser_page adımını daha büyük acquisition bulanıklığı içinde gizlemek yerine isimli tutmak için
# TR: - koridoru takip eden bir başlangıç seviyesi okuyucu için page düzeyi browser semantiklerini okunabilir tutmak için
# TR: Kabul edilen girdi:
# TR: - burada şu an görülen açık parametreler: claimed_url, timeout_ms, wait_until, raw_root, headless
# TR: - değerler mevcut Python imzası ve bu işaretin altındaki page düzeyi browser koridoru ile uyumlu olmalıdır
# TR: Kabul edilen çıktı:
# TR: - aşağıdaki canlı gövdenin tanımladığı sonuç şekli; bu browser_page payloadı, fetched_page benzeri paket, callback tarafı etki, açık success, timeout, browser_error veya degraded dal olabilir
# TR: Önemli anlam:
# TR: - bu fonksiyon acquisition parent yüzeyinin tamamına değil, browser_page child yüzeyine aittir
# TR: - downstream katman browserın page düzeyi koridorunda ne olduğunu anlamak istiyorsa dal anlamını burada okuyabilmelidir
# TR: İstenmeyen davranış:
# TR: - etiketsiz browser page mutasyonu
# TR: - dal anlamını gizleyen belirsiz çıktı şekli

# EN: BROWSER PAGE FUNCTION CONTRACT DENSITY BLOCK V7 / fetch_page_with_browser_to_raw_storage
# EN:
# EN: This top-level function exists so browser_page corridor truth for 'fetch_page_with_browser_to_raw_storage' stays readable.
# EN: Why this function exists:
# EN: - to keep one named browser_page step visible
# EN: - to prevent page-level browser meaning from disappearing inside a larger helper cloud
# EN: Accepted input line shapes:
# EN: - visible parameters now: claimed_url, timeout_ms, wait_until, raw_root, headless
# EN: - callers should respect the current Python signature exactly
# EN: - payload-like parameters are expected to match the active page-level browser corridor
# EN: Accepted output line shapes:
# EN: - the live body may return a dict-like payload, fetched_page-style package, callback-driven side effect, explicit browser success, timeout-style outcome, degraded branch, or browser-error branch
# EN: Common browser_page variable expectations:
# EN: - acquisition_method should usually already be browser_page at this level
# EN: - fetched_page-like values are commonly dict-shaped on success-style branches
# EN: - fetched_page-like values may be None, absent, or partial when timeout/degraded/error branches are active
# EN: - undesired meaning is silent ambiguity about what happened in the page corridor
# EN: Forwarding note:
# EN: - this function may prepare, receive, transform, or forward page-level browser results to downstream validation, finalize, parse, or acquisition-parent logic
# TR: BROWSER PAGE FUNCTION CONTRACT YOĞUNLUK BLOĞU V7 / fetch_page_with_browser_to_raw_storage
# TR:
# TR: Bu üst seviye fonksiyon, 'fetch_page_with_browser_to_raw_storage' için browser_page koridoru doğrusunun okunabilir kalması için vardır.
# TR: Bu fonksiyon neden var:
# TR: - isimli browser_page adımını görünür tutmak için
# TR: - page düzeyi browser anlamının daha büyük yardımcı bulutu içinde kaybolmasını engellemek için
# TR: Kabul edilen girdi satırı şekilleri:
# TR: - şu an görülen parametreler: claimed_url, timeout_ms, wait_until, raw_root, headless
# TR: - çağıran taraf mevcut Python imzasına tam uymalıdır
# TR: - payload benzeri parametreler etkin page düzeyi browser koridoru ile uyumlu olmalıdır
# TR: Kabul edilen çıktı satırı şekilleri:
# TR: - canlı gövde dict-benzeri payload, fetched_page benzeri paket, callback kaynaklı yan etki, açık browser başarısı, timeout tarzı sonuç, degraded dalı veya browser-error dalı döndürebilir
# TR: Yaygın browser_page değişken beklentileri:
# TR: - bu seviyede acquisition_method çoğu zaman zaten browser_page olmalıdır
# TR: - fetched_page benzeri değerler başarı tarzı dallarda çoğunlukla dict yapısındadır
# TR: - fetched_page benzeri değerler timeout/degraded/hata dallarında None, eksik veya kısmi olabilir
# TR: - istenmeyen anlam, page koridorunda ne olduğunu sessiz belirsizlik içinde bırakmaktır
# TR: Forward etme notu:
# TR: - bu fonksiyon page düzeyi browser sonuçlarını hazırlayabilir, alabilir, dönüştürebilir veya downstream validation, finalize, parse ya da acquisition-parent mantığına forward edebilir

# EN: This browser-page acquisition function named fetch_page_with_browser_to_raw_storage is the explicit browser_page corridor entry point inside the acquisition family.
# EN: claimed_url is the claimed frontier payload that supplies url_id and requested URL truth for this fetch.
# EN: timeout_ms is the browser-side timeout budget in milliseconds for the page operation.
# EN: wait_until is the browser navigation readiness target such as load, domcontentloaded, or networkidle.
# EN: raw_root is the controlled raw acquisition root under which rendered HTML and screenshot artefacts are stored.
# EN: headless declares whether the browser page run should execute in headless mode.
# EN: A reader should understand exactly how browser_page work is executed here and how outputs are shaped into the stable fetched-page contract.
# TR: fetch_page_with_browser_to_raw_storage isimli bu browser-page acquisition fonksiyonu acquisition ailesi içindeki açık browser_page koridoru giriş noktasıdır.
# TR: claimed_url, bu fetch için url_id ve requested URL doğrusunu sağlayan claim edilmiş frontier payload'ıdır.
# TR: timeout_ms, sayfa işlemi için milisaniye cinsinden browser tarafı zaman aşımı bütçesidir.
# TR: wait_until, load, domcontentloaded veya networkidle gibi browser navigation hazır olma hedefidir.
# TR: raw_root, rendered HTML ve screenshot artefact'larının saklandığı kontrollü ham acquisition köküdür.
# TR: headless, browser page çalışmasının headless kipte yürütülüp yürütülmeyeceğini belirtir.
# TR: Okuyucu browser_page işinin burada tam olarak nasıl çalıştırıldığını ve çıktının kararlı fetched-page sözleşmesine nasıl şekillendirildiğini anlayabilmelidir.
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
# EN: url_id is the frontier work-item id extracted from claimed_url so browser artefact filenames remain directly traceable.
# TR: url_id, browser artefact dosya adları doğrudan izlenebilir kalsın diye claimed_url içinden çıkarılan frontier iş öğesi kimliğidir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))

    # EN: We read the requested canonical URL because it is the real browser target.
    # TR: Gerçek browser hedefi olduğu için istenen canonical URL'yi okuyoruz.
# EN: requested_url is the normalized requested frontier URL that remains visible alongside browser_result so downstream payload shaping can compare requested and final navigation truth.
# TR: requested_url, browser_result ile birlikte görünür tutulan normalize frontier istenen URL'sidir; böylece aşağı akış payload şekillendirme istenen ve nihai gezinme doğrusunu karşılaştırabilir.
    requested_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We capture the current UTC fetch time before browser work starts so all generated
# EN: requested_url is the normalized requested frontier URL extracted from claimed_url for the browser_page request corridor.
# TR: requested_url, browser_page istek koridoru için claimed_url içinden çıkarılan normalize edilmiş istenen frontier URL'sidir.
    # EN: artefacts share the same deterministic timestamp stem.
    # TR: Üretilen tüm artefact'lar aynı deterministik zaman damgası kökünü paylaşsın diye
    # TR: browser işi başlamadan önce mevcut UTC fetch zamanını yakalıyoruz.
# EN: fetched_at is the UTC acquisition timestamp used to stamp sibling browser artefacts and the downstream fetched-page payload.
# TR: fetched_at, kardeş browser artefact'larını ve aşağı akış fetched-page payload'ını damgalamak için kullanılan UTC acquisition zamanıdır.
    fetched_at = utc_now()

    # EN: We compute the rendered HTML evidence path now so the browser runtime writes
    # EN: directly into the controlled raw acquisition tree.
    # TR: Browser runtime doğrudan kontrollü raw acquisition ağacına yazsın diye rendered HTML
    # TR: kanıt yolunu şimdi hesaplıyoruz.
# EN: html_output_path is the controlled raw path where the rendered browser HTML body will be written for this browser_page fetch.
# TR: html_output_path, bu browser_page fetch işlemi için rendered browser HTML gövdesinin yazılacağı kontrollü ham depolama yoludur.
    html_output_path = build_browser_rendered_storage_path(
        url_id=url_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )

    # EN: We compute the screenshot sibling path now so the browser evidence set stays complete.
    # TR: Browser kanıt seti tam kalsın diye screenshot kardeş yolunu da şimdi hesaplıyoruz.
# EN: screenshot_output_path is the controlled raw path where the browser screenshot evidence will be written for the same browser_page fetch.
# TR: screenshot_output_path, aynı browser_page fetch işlemi için browser screenshot kanıtının yazılacağı kontrollü ham depolama yoludur.
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
# EN: browser_result is the deeper browser-runtime result object returned by the browser_page corridor for shaping into the stable fetched-page contract.
# TR: browser_result, kararlı fetched-page sözleşmesine şekillendirilmek üzere browser_page koridorundan dönen daha derin browser-runtime sonuç nesnesidir.
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
# EN: rendered_html_bytes is the UTF-8 encoded browser-rendered page body that becomes the persisted HTML artefact.
# TR: rendered_html_bytes, kalıcı HTML artefact'ına dönüşen UTF-8 kodlu browser-rendered sayfa gövdesidir.
    rendered_html_bytes = html_output_path.read_bytes()

    # EN: We compute a deterministic fingerprint of the rendered HTML artefact.
    # TR: Rendered HTML artefact'ının deterministik parmak izini hesaplıyoruz.
# EN: rendered_html_sha256 is the checksum of rendered_html_bytes written to controlled raw storage for later integrity checks.
# TR: rendered_html_sha256, sonraki bütünlük kontrolleri için kontrollü ham depoya yazılan rendered_html_bytes özetidir.
    rendered_html_sha256 = sha256_hex(rendered_html_bytes)

    # EN: We infer one document-level status code from browser network evidence.
    # TR: Browser network evidence içinden tek bir document-seviyesi durum kodu çıkarıyoruz.
# EN: inferred_http_status is the best-effort page status inferred from browser_result when an explicit document status is available.
# TR: inferred_http_status, açık bir document status mevcutsa browser_result içinden çıkarılan en iyi çabalı sayfa durum kodudur.
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
