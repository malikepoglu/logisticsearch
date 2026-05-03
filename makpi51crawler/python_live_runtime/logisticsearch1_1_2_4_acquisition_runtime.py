"""
EN:
This file is the acquisition-runtime parent child of the worker-runtime family.

EN:
Why this file exists:
- because acquisition-specific runtime truth should live in one explicit parent child instead of being hidden inside the main worker hub
- because acquisition_method selection, acquisition_execution meaning, static vs dynamic path choice, browser vs http branching, and fetched-page production boundaries must remain readable
- because a beginner should be able to find where the crawler decides how a page will actually be acquired before parse and storage layers ever see the result

EN:
What this file DOES:
- expose acquisition-oriented runtime helper, class, and payload boundaries
- preserve visible acquisition_method, execution planning, route choice, static/dynamic branching, and degraded branch meaning
- keep acquisition semantics separate from broader worker orchestration, lease handling, robots policy, parse logic, and storage logic

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not become the entire browser implementation by itself
- it does not replace narrower acquisition support children
- it does not become the parse, taxonomy, or storage layer

EN:
Topological role:
- worker runtime can call into this acquisition parent when a claimed work item is ready to be fetched
- this file helps decide which acquisition corridor should run and how the resulting fetched-page contract is shaped
- later layers such as fetch-finalize, parse, taxonomy, and storage consume the outputs prepared here

EN:
Important visible values and shapes:
- acquisition_method => values such as http_page, browser_page, or None when no real acquisition method is chosen
- acquisition_execution => structured description of which acquisition path is about to run or already ran
- fetched_page => explicit acquisition result payload that later layers can validate and parse
- route/decision payloads => visible explanation of why one acquisition path was selected
- degraded branch payloads => explicit non-happy acquisition outcomes that must remain readable

EN:
Accepted architectural identity:
- acquisition runtime parent child
- narrow acquisition contract layer
- readable worker-to-fetch boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague browser/http helper dump
- hidden operator CLI surface
- hidden fetch side-effect maze

TR:
Bu dosya worker-runtime ailesinin acquisition-runtime parent child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü acquisitiona özgü runtime doğrusu ana worker hubının içinde gizlenmek yerine tek ve açık parent child yüzeyde yaşamalıdır
- çünkü acquisition_method seçimi, acquisition_execution anlamı, static vs dynamic yol tercihi, browser vs http dal seçimi ve fetched-page üretim sınırları okunabilir kalmalıdır
- çünkü yeni başlayan biri crawlerın parse ve storage katmanları sonucu görmeden önce bir sayfanın nasıl acquire edileceğine nerede karar verdiğini bulabilmelidir

TR:
Bu dosya NE yapar:
- acquisition odaklı runtime helper, class ve payload sınırlarını açığa çıkarır
- acquisition_method, execution planning, yol seçimi, static/dynamic dallanma ve degraded dal anlamını görünür tutar
- acquisition semantiklerini daha geniş worker orkestrasyonundan, lease yönetiminden, robots policy mantığından, parse mantığından ve storage mantığından ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- browser implementasyonunun tamamı tek başına olmaz
- daha dar acquisition support child yüzeylerinin yerini almaz
- parse, taxonomy veya storage katmanının kendisi olmaz

TR:
Topolojik rol:
- worker runtime claim edilmiş iş öğesi fetch edilmeye hazır olduğunda bu acquisition parent yüzeye çağrı yapabilir
- bu dosya hangi acquisition koridorunun çalışacağını ve ortaya çıkan fetched-page sözleşmesinin nasıl şekilleneceğini belirlemeye yardımcı olur
- fetch-finalize, parse, taxonomy ve storage gibi sonraki katmanlar burada hazırlanan çıktıları tüketir

TR:
Önemli görünür değerler ve şekiller:
- acquisition_method => http_page, browser_page veya gerçek acquisition method seçilmediğinde None gibi değerler
- acquisition_execution => hangi acquisition yolunun çalışacağına veya çalıştığına dair yapılı açıklama
- fetched_page => sonraki katmanların doğrulayıp parse edebileceği açık acquisition sonuç payloadı
- route/decision payloadları => neden belirli acquisition yolunun seçildiğini anlatan görünür açıklama
- degraded dal payloadları => okunabilir kalması gereken mutlu-yol-dışı acquisition sonuçları

TR:
Kabul edilen mimari kimlik:
- acquisition runtime parent child
- dar acquisition sözleşme katmanı
- okunabilir worker-to-fetch sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz browser/http helper çöplüğü
- gizli operatör CLI yüzeyi
- gizli fetch yan-etki labirenti
"""

# EN: This module is the real acquisition-family orchestration hub.
# EN: Its new job is not only to re-export child surfaces, but also to choose
# EN: the first acquisition path for one claimed URL in a narrow, explicit,
# EN: auditable way.
# TR: Bu modül acquisition ailesinin gerçek orkestrasyon merkezidir.
# TR: Yeni görevi yalnızca alt yüzeyleri yeniden dışa aktarmak değil; aynı
# TR: zamanda tek bir claimed URL için ilk acquisition yolunu dar, açık ve
# TR: denetlenebilir biçimde seçmektir.

# EN: ACQUISITION RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow acquisition parent of the worker corridor.
# EN: Beginner mental model:
# EN: - worker runtime decides that a claimed item should now be acquired
# EN: - this parent explains how the crawler chooses a real acquisition path
# EN: - it exists so the crawler can later answer: which acquisition method ran, why it was selected, and what fetched-page shaped result emerged
# EN:
# EN: Accepted architectural meaning:
# EN: - named acquisition-runtime parent child
# EN: - focused acquisition-method and execution-decision helper surface
# EN: - readable boundary for worker meaning becoming fetch/acquisition meaning
# EN:
# EN: Undesired architectural meaning:
# EN: - random browser/http helper pile
# EN: - hidden second worker orchestrator
# EN: - place where acquisition route failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - acquisition_method should stay explicit
# EN: - acquisition_execution and fetched_page should stay structured and readable
# EN: - degraded acquisition branches must remain visible
# TR: ACQUISITION RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar acquisition parent yüzeyi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - worker runtime claim edilmiş iş öğesinin artık acquire edilmesi gerektiğine karar verir
# TR: - bu parent crawlerın gerçek acquisition yolunu nasıl seçtiğini açıklar
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: hangi acquisition method çalıştı, neden seçildi ve hangi fetched-page şekilli sonuç ortaya çıktı
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli acquisition-runtime parent child
# TR: - odaklı acquisition-method ve execution-decision yardımcı yüzeyi
# TR: - worker anlamının fetch/acquisition anlamına dönüşmesi için okunabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele browser/http helper yığını
# TR: - gizli ikinci worker orchestrator
# TR: - acquisition route hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - acquisition_method açık kalmalıdır
# TR: - acquisition_execution ve fetched_page yapılı ve okunabilir kalmalıdır
# TR: - degraded acquisition dalları görünür kalmalıdır

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
# EN: This class 'AcquisitionSelectionPlan' is an explicit named acquisition-runtime structure.
# EN: AcquisitionSelectionPlan exists so acquisition-side meaning stays readable instead of drifting into anonymous payloads.
# TR: Bu 'AcquisitionSelectionPlan' sınıfı açık ve isimli bir acquisition-runtime yapısıdır.
# TR: AcquisitionSelectionPlan acquisition tarafı anlamı anonim payloadlara kaymasın diye vardır.
@dataclass
# EN: ACQUISITION CLASS PURPOSE MEMORY BLOCK V6 / AcquisitionSelectionPlan
# EN:
# EN: Why this class exists:
# EN: - because acquisition-layer truth for 'AcquisitionSelectionPlan' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand acquisition-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named acquisition payload, route shape, execution structure, or structured result carrier
# EN: - visible field set currently detected here: target_url, strategy, url_kind, reason, browser_fallback_allowed, browser_required
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
# EN: - explicit success vs degraded acquisition meaning may matter here
# EN: - these helpers often decide whether later layers receive usable fetched-page payloads
# EN: - visible http vs browser vs no-method distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no acquisition contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: ACQUISITION CLASS AMAÇ HAFIZA BLOĞU V6 / AcquisitionSelectionPlan
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'AcquisitionSelectionPlan' için acquisition katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip acquisition tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli acquisition payloadı, route şekli, execution yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: target_url, strategy, url_kind, reason, browser_fallback_allowed, browser_required
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
# TR: - açık success vs degraded acquisition anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir fetched-page payload alıp almayacağını belirler
# TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı acquisition sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

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
# EN: This class 'AcquisitionExecutionResult' is an explicit named acquisition-runtime structure.
# EN: AcquisitionExecutionResult exists so acquisition-side meaning stays readable instead of drifting into anonymous payloads.
# TR: Bu 'AcquisitionExecutionResult' sınıfı açık ve isimli bir acquisition-runtime yapısıdır.
# TR: AcquisitionExecutionResult acquisition tarafı anlamı anonim payloadlara kaymasın diye vardır.
@dataclass
# EN: ACQUISITION CLASS PURPOSE MEMORY BLOCK V6 / AcquisitionExecutionResult
# EN:
# EN: Why this class exists:
# EN: - because acquisition-layer truth for 'AcquisitionExecutionResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand acquisition-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named acquisition payload, route shape, execution structure, or structured result carrier
# EN: - visible field set currently detected here: selection_plan, method_used, fallback_used, fetch_result, http_error_class, http_error_message
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
# EN: - explicit success vs degraded acquisition meaning may matter here
# EN: - these helpers often decide whether later layers receive usable fetched-page payloads
# EN: - visible http vs browser vs no-method distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no acquisition contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: ACQUISITION CLASS AMAÇ HAFIZA BLOĞU V6 / AcquisitionExecutionResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'AcquisitionExecutionResult' için acquisition katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip acquisition tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli acquisition payloadı, route şekli, execution yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: selection_plan, method_used, fallback_used, fetch_result, http_error_class, http_error_message
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
# TR: - açık success vs degraded acquisition anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir fetched-page payload alıp almayacağını belirler
# TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı acquisition sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

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
# EN: ACQUISITION FUNCTION PURPOSE MEMORY BLOCK V6 / _read_optional_claimed_url_value
# EN:
# EN: Why this function exists:
# EN: - because acquisition truth for '_read_optional_claimed_url_value' should be exposed through one named top-level helper boundary
# EN: - because acquisition-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, field_names
# EN: - values should match the current Python signature and the acquisition contract below
# EN:
# EN: Accepted output:
# EN: - an acquisition-oriented result shape defined by the current function body
# EN: - this may be a route result, acquisition plan, fetched-page shape, execution payload, or another explicit acquisition-side branch result
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface exposes one named acquisition runtime contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is acquisition-side helper logic, not the whole worker corridor
# EN: - acquisition results must stay explicit so audits can understand success, degraded, no-method, and downstream fetched-page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague acquisition results that hide branch meaning
# TR: ACQUISITION FUNCTION AMAÇ HAFIZA BLOĞU V6 / _read_optional_claimed_url_value
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü '_read_optional_claimed_url_value' için acquisition doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü acquisition tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, field_names
# TR: - değerler aşağıdaki mevcut Python imzası ve acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen acquisition odaklı sonuç şekli
# TR: - bu; route sonucu, acquisition planı, fetched-page şekli, execution payloadı veya başka açık acquisition tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey isimli bir acquisition runtime sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon acquisition tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - acquisition sonuçları açık kalmalıdır ki denetimler success, degraded, no-method ve downstream fetched-page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz acquisition sonuçları

# EN: This function '_read_optional_claimed_url_value' is an explicit acquisition-runtime step.
# EN: _read_optional_claimed_url_value exists so this file keeps one narrow acquisition decision or execution step readable.
# TR: Bu '_read_optional_claimed_url_value' fonksiyonu açık bir acquisition-runtime adımıdır.
# TR: _read_optional_claimed_url_value bu dosyada dar acquisition kararının veya yürütme adımının okunabilir kalması için vardır.
# EN: claimed_url is the claimed frontier payload that this acquisition step reads.
# TR: claimed_url bu acquisition adımının okuduğu claim edilmiş frontier payloadıdır.
# EN: field_names is the ordered tuple of candidate field names searched by this helper.
# TR: field_names bu yardımcının aradığı aday alan adlarının sıralı tuple değeridir.
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
# EN: ACQUISITION FUNCTION PURPOSE MEMORY BLOCK V6 / _read_optional_bool_flag
# EN:
# EN: Why this function exists:
# EN: - because acquisition truth for '_read_optional_bool_flag' should be exposed through one named top-level helper boundary
# EN: - because acquisition-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, field_names
# EN: - values should match the current Python signature and the acquisition contract below
# EN:
# EN: Accepted output:
# EN: - an acquisition-oriented result shape defined by the current function body
# EN: - this may be a route result, acquisition plan, fetched-page shape, execution payload, or another explicit acquisition-side branch result
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface exposes one named acquisition runtime contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is acquisition-side helper logic, not the whole worker corridor
# EN: - acquisition results must stay explicit so audits can understand success, degraded, no-method, and downstream fetched-page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague acquisition results that hide branch meaning
# TR: ACQUISITION FUNCTION AMAÇ HAFIZA BLOĞU V6 / _read_optional_bool_flag
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü '_read_optional_bool_flag' için acquisition doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü acquisition tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, field_names
# TR: - değerler aşağıdaki mevcut Python imzası ve acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen acquisition odaklı sonuç şekli
# TR: - bu; route sonucu, acquisition planı, fetched-page şekli, execution payloadı veya başka açık acquisition tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey isimli bir acquisition runtime sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon acquisition tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - acquisition sonuçları açık kalmalıdır ki denetimler success, degraded, no-method ve downstream fetched-page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz acquisition sonuçları

# EN: This function '_read_optional_bool_flag' is an explicit acquisition-runtime step.
# EN: _read_optional_bool_flag exists so this file keeps one narrow acquisition decision or execution step readable.
# TR: Bu '_read_optional_bool_flag' fonksiyonu açık bir acquisition-runtime adımıdır.
# TR: _read_optional_bool_flag bu dosyada dar acquisition kararının veya yürütme adımının okunabilir kalması için vardır.
# EN: claimed_url is the claimed frontier payload that this acquisition step reads.
# TR: claimed_url bu acquisition adımının okuduğu claim edilmiş frontier payloadıdır.
# EN: field_names is the ordered tuple of candidate field names searched by this helper.
# TR: field_names bu yardımcının aradığı aday alan adlarının sıralı tuple değeridir.
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
# EN: normalized_text stores the stripped lowercase text form used for explicit boolean-flag normalization.
# TR: normalized_text açık boolean-bayrak normalizasyonu için kullanılan kırpılmış küçük-harfli metin biçimini tutar.
    normalized_text = str(raw_value).strip().lower()
    return normalized_text in {"1", "true", "yes", "y", "on", "browser", "required"}


# EN: This helper classifies the target URL into a coarse operational kind.
# EN: We intentionally keep the classification narrow because the first goal is
# EN: to enable safe orchestration, not to overfit site behavior too early.
# TR: Bu yardımcı hedef URL'yi kaba bir operasyonel türe sınıflandırır.
# TR: Sınıflandırmayı bilinçli olarak dar tutuyoruz; çünkü ilk hedef site
# TR: davranışını erken aşırı uyarlamak değil, güvenli orkestrasyon sağlamaktır.
# EN: ACQUISITION FUNCTION PURPOSE MEMORY BLOCK V6 / infer_target_url_kind
# EN:
# EN: Why this function exists:
# EN: - because acquisition truth for 'infer_target_url_kind' should be exposed through one named top-level helper boundary
# EN: - because acquisition-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: target_url
# EN: - values should match the current Python signature and the acquisition contract below
# EN:
# EN: Accepted output:
# EN: - an acquisition-oriented result shape defined by the current function body
# EN: - this may be a route result, acquisition plan, fetched-page shape, execution payload, or another explicit acquisition-side branch result
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface exposes one named acquisition runtime contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is acquisition-side helper logic, not the whole worker corridor
# EN: - acquisition results must stay explicit so audits can understand success, degraded, no-method, and downstream fetched-page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague acquisition results that hide branch meaning
# TR: ACQUISITION FUNCTION AMAÇ HAFIZA BLOĞU V6 / infer_target_url_kind
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'infer_target_url_kind' için acquisition doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü acquisition tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: target_url
# TR: - değerler aşağıdaki mevcut Python imzası ve acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen acquisition odaklı sonuç şekli
# TR: - bu; route sonucu, acquisition planı, fetched-page şekli, execution payloadı veya başka açık acquisition tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey isimli bir acquisition runtime sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon acquisition tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - acquisition sonuçları açık kalmalıdır ki denetimler success, degraded, no-method ve downstream fetched-page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz acquisition sonuçları

# EN: This function 'infer_target_url_kind' is an explicit acquisition-runtime step.
# EN: infer_target_url_kind exists so this file keeps one narrow acquisition decision or execution step readable.
# TR: Bu 'infer_target_url_kind' fonksiyonu açık bir acquisition-runtime adımıdır.
# TR: infer_target_url_kind bu dosyada dar acquisition kararının veya yürütme adımının okunabilir kalması için vardır.
# EN: target_url is the URL text being classified or planned for acquisition.
# TR: target_url acquisition için sınıflandırılan veya planlanan URL metnidir.
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
# EN: ACQUISITION FUNCTION PURPOSE MEMORY BLOCK V6 / select_page_acquisition_plan
# EN:
# EN: Why this function exists:
# EN: - because acquisition truth for 'select_page_acquisition_plan' should be exposed through one named top-level helper boundary
# EN: - because acquisition-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url
# EN: - values should match the current Python signature and the acquisition contract below
# EN:
# EN: Accepted output:
# EN: - an acquisition-oriented result shape defined by the current function body
# EN: - this may be a route result, acquisition plan, fetched-page shape, execution payload, or another explicit acquisition-side branch result
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
# EN: - explicit success vs degraded acquisition meaning may matter here
# EN: - these helpers often decide whether later layers receive usable fetched-page payloads
# EN: - visible http vs browser vs no-method distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is acquisition-side helper logic, not the whole worker corridor
# EN: - acquisition results must stay explicit so audits can understand success, degraded, no-method, and downstream fetched-page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague acquisition results that hide branch meaning
# TR: ACQUISITION FUNCTION AMAÇ HAFIZA BLOĞU V6 / select_page_acquisition_plan
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'select_page_acquisition_plan' için acquisition doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü acquisition tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url
# TR: - değerler aşağıdaki mevcut Python imzası ve acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen acquisition odaklı sonuç şekli
# TR: - bu; route sonucu, acquisition planı, fetched-page şekli, execution payloadı veya başka açık acquisition tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
# TR: - açık success vs degraded acquisition anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir fetched-page payload alıp almayacağını belirler
# TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon acquisition tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - acquisition sonuçları açık kalmalıdır ki denetimler success, degraded, no-method ve downstream fetched-page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz acquisition sonuçları

# EN: This function 'select_page_acquisition_plan' is an explicit acquisition-runtime step.
# EN: select_page_acquisition_plan exists so this file keeps one narrow acquisition decision or execution step readable.
# TR: Bu 'select_page_acquisition_plan' fonksiyonu açık bir acquisition-runtime adımıdır.
# TR: select_page_acquisition_plan bu dosyada dar acquisition kararının veya yürütme adımının okunabilir kalması için vardır.
# EN: claimed_url is the claimed frontier payload that this acquisition step reads.
# TR: claimed_url bu acquisition adımının okuduğu claim edilmiş frontier payloadıdır.
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
# EN: ACQUISITION FUNCTION PURPOSE MEMORY BLOCK V6 / fetch_page_via_selection_to_raw_storage
# EN:
# EN: Why this function exists:
# EN: - because acquisition truth for 'fetch_page_via_selection_to_raw_storage' should be exposed through one named top-level helper boundary
# EN: - because acquisition-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, http_timeout_seconds, browser_timeout_ms, browser_wait_until, raw_root, headless
# EN: - values should match the current Python signature and the acquisition contract below
# EN:
# EN: Accepted output:
# EN: - an acquisition-oriented result shape defined by the current function body
# EN: - this may be a route result, acquisition plan, fetched-page shape, execution payload, or another explicit acquisition-side branch result
# EN:
# EN: Common acquisition meaning hints:
# EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
# EN: - explicit success vs degraded acquisition meaning may matter here
# EN: - these helpers often decide whether later layers receive usable fetched-page payloads
# EN: - visible http vs browser vs no-method distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is acquisition-side helper logic, not the whole worker corridor
# EN: - acquisition results must stay explicit so audits can understand success, degraded, no-method, and downstream fetched-page meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague acquisition results that hide branch meaning
# TR: ACQUISITION FUNCTION AMAÇ HAFIZA BLOĞU V6 / fetch_page_via_selection_to_raw_storage
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'fetch_page_via_selection_to_raw_storage' için acquisition doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü acquisition tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, http_timeout_seconds, browser_timeout_ms, browser_wait_until, raw_root, headless
# TR: - değerler aşağıdaki mevcut Python imzası ve acquisition sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen acquisition odaklı sonuç şekli
# TR: - bu; route sonucu, acquisition planı, fetched-page şekli, execution payloadı veya başka açık acquisition tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
# TR: - açık success vs degraded acquisition anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir fetched-page payload alıp almayacağını belirler
# TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon acquisition tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - acquisition sonuçları açık kalmalıdır ki denetimler success, degraded, no-method ve downstream fetched-page anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz acquisition sonuçları

# EN: This function 'fetch_page_via_selection_to_raw_storage' is an explicit acquisition-runtime step.
# EN: fetch_page_via_selection_to_raw_storage exists so this file keeps one narrow acquisition decision or execution step readable.
# TR: Bu 'fetch_page_via_selection_to_raw_storage' fonksiyonu açık bir acquisition-runtime adımıdır.
# TR: fetch_page_via_selection_to_raw_storage bu dosyada dar acquisition kararının veya yürütme adımının okunabilir kalması için vardır.
# EN: claimed_url is the claimed frontier payload that this acquisition step reads.
# TR: claimed_url bu acquisition adımının okuduğu claim edilmiş frontier payloadıdır.
# EN: http_timeout_seconds is the HTTP-side timeout budget in seconds.
# TR: http_timeout_seconds HTTP tarafındaki timeout bütçesini saniye cinsinden belirtir.
# EN: browser_timeout_ms is the browser-side timeout budget in milliseconds.
# TR: browser_timeout_ms browser tarafındaki timeout bütçesini milisaniye cinsinden belirtir.
# EN: browser_wait_until is the browser readiness mode used before reading rendered output.
# TR: browser_wait_until render edilmiş çıktıyı okumadan önce kullanılan browser hazır-olma kipidir.
# EN: raw_root is the raw artefact root path used to persist acquisition output.
# TR: raw_root acquisition çıktısını kalıcılaştırmak için kullanılan ham artefact kök yoludur.
# EN: headless controls whether browser acquisition runs without a visible window.
# TR: headless browser acquisitionın görünür pencere olmadan çalışıp çalışmayacağını kontrol eder.
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
