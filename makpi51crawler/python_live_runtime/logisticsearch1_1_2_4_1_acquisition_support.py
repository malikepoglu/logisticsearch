"""
EN:
This file is the shared acquisition-support child beneath the broader acquisition-runtime parent.

EN:
Why this file exists:
- because shared acquisition helper truth should live in one explicit support child instead of being duplicated across http, browser, robots, or parent acquisition surfaces
- because acquisition_method helper values, page/request/response support payloads, browser/http shared normalization, and fetched-page shaping helpers must remain readable
- because a beginner should be able to find where reusable acquisition pieces live before entering narrower http-page, browser-page, or robots-txt children

EN:
What this file DOES:
- expose shared acquisition helper, class, and payload boundaries
- preserve visible normalization, preparation, helper-shaping, and degraded branch meaning used by multiple acquisition corridors
- keep shared acquisition support semantics separate from the acquisition parent controller and from narrower single-method children

EN:
What this file DOES NOT do:
- it does not become the full acquisition orchestrator
- it does not become only the browser implementation
- it does not become only the http implementation
- it does not become the parse or storage layer

EN:
Topological role:
- the broader acquisition parent can depend on helpers defined here
- narrower acquisition children can reuse the same shared helper structures and normalization logic from this file
- later layers consume fetched-page or related support outputs that were shaped using these shared definitions

EN:
Important visible values and shapes:
- acquisition_method helper values => explicit strings such as http_page, browser_page, robots_txt, or None in non-selected branches
- fetched_page helper shapes => structured acquisition result material passed toward later validation and parse steps
- request/response or browser/http support payloads => reusable shared structures used by multiple acquisition paths
- degraded support payloads => explicit non-happy helper outcomes that must remain readable

EN:
Accepted architectural identity:
- shared acquisition-support child
- narrow reusable acquisition contract layer
- readable helper boundary for all acquisition children

EN:
Undesired architectural identity:
- hidden second acquisition parent
- vague utility dump
- hidden operator CLI surface
- hidden side-effect maze

TR:
Bu dosya daha geniş acquisition-runtime parent yüzeyinin altındaki ortak acquisition-support child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü ortak acquisition yardımcı doğrusu http, browser, robots veya acquisition parent yüzeylerine kopyalanmak yerine tek ve açık support child içinde yaşamalıdır
- çünkü acquisition_method yardımcı değerleri, page/request/response support payloadları, browser/http ortak normalization ve fetched-page shaping yardımcıları okunabilir kalmalıdır
- çünkü yeni başlayan biri daha dar http-page, browser-page veya robots-txt child yüzeylerine girmeden önce tekrar kullanılan acquisition parçalarının nerede yaşadığını bulabilmelidir

TR:
Bu dosya NE yapar:
- ortak acquisition helper, class ve payload sınırlarını açığa çıkarır
- birden çok acquisition koridorunun kullandığı normalization, preparation, helper-shaping ve degraded dal anlamını görünür tutar
- ortak acquisition support semantiklerini acquisition parent controller yüzeyinden ve daha dar tek-method child yüzeylerinden ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam acquisition orchestratorun kendisi olmaz
- yalnızca browser implementasyonu olmaz
- yalnızca http implementasyonu olmaz
- parse veya storage katmanının kendisi olmaz

TR:
Topolojik rol:
- daha geniş acquisition parent burada tanımlanan yardımcı parçalara bağımlı olabilir
- daha dar acquisition child yüzeyleri bu dosyadaki ortak helper yapıları ve normalization mantığını tekrar kullanabilir
- sonraki katmanlar burada şekillenen ortak tanımlar kullanılarak hazırlanmış fetched-page veya ilgili support çıktıları tüketir

TR:
Önemli görünür değerler ve şekiller:
- acquisition_method yardımcı değerleri => http_page, browser_page, robots_txt veya seçilmeyen dallarda None gibi açık stringler
- fetched_page yardımcı şekilleri => sonraki validation ve parse adımlarına giden yapılı acquisition sonuç malzemesi
- request/response veya browser/http support payloadları => birden çok acquisition yolunun kullandığı tekrar kullanılabilir ortak yapılar
- degraded support payloadları => okunabilir kalması gereken mutlu-yol-dışı helper sonuçları

TR:
Kabul edilen mimari kimlik:
- ortak acquisition-support child
- dar tekrar kullanılabilir acquisition sözleşme katmanı
- tüm acquisition child yüzeyleri için okunabilir helper sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci acquisition parent
- belirsiz utility çöplüğü
- gizli operatör CLI yüzeyi
- gizli yan-etki labirenti
"""

# EN: This module is the shared support surface for the acquisition family.
# EN: It holds only stable result types and generic acquisition helpers that are
# EN: reused by direct HTTP fetch, robots fetch, and browser-backed fetch paths.
# TR: Bu modül acquisition ailesi için paylaşılan destek yüzeyidir.
# TR: Doğrudan HTTP fetch, robots fetch ve browser-backed fetch yolları tarafından
# TR: yeniden kullanılan yalnızca kararlı sonuç tiplerini ve genel acquisition
# TR: yardımcılarını tutar.

# EN: ACQUISITION SUPPORT IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the shared helper toolbox for acquisition children.
# EN: Beginner mental model:
# EN: - the acquisition parent decides the broader route
# EN: - narrower children perform concrete method-specific work
# EN: - this support child holds reusable helper pieces so the same meaning does not get reimplemented everywhere
# EN: - it exists so the crawler can later answer: which shared acquisition shapes, helper contracts, and fetched-page support pieces were reused
# EN:
# EN: Accepted architectural meaning:
# EN: - named acquisition-support child
# EN: - focused shared helper and payload-shaping surface
# EN: - readable reusable boundary for acquisition children
# EN:
# EN: Undesired architectural meaning:
# EN: - random utility pile
# EN: - hidden second acquisition parent
# EN: - place where shared helper failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - acquisition support payloads should stay explicit
# EN: - fetched_page helper shapes should stay structured and readable
# EN: - degraded support branches must remain visible
# TR: ACQUISITION SUPPORT KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya acquisition child yüzeyleri için ortak yardımcı alet kutusu gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition parent daha geniş yolu seçer
# TR: - daha dar child yüzeyler somut method-özel işi yapar
# TR: - bu support child aynı anlamın her yerde yeniden yazılmaması için tekrar kullanılabilir helper parçalarını tutar
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: hangi ortak acquisition şekilleri, helper sözleşmeleri ve fetched-page support parçaları tekrar kullanıldı
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli acquisition-support child
# TR: - odaklı ortak helper ve payload-shaping yüzeyi
# TR: - acquisition child yüzeyleri için okunabilir tekrar kullanılabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele utility yığını
# TR: - gizli ikinci acquisition parent
# TR: - ortak helper hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - acquisition support payloadları açık kalmalıdır
# TR: - fetched_page helper şekilleri yapılı ve okunabilir kalmalıdır
# TR: - degraded support dalları görünür kalmalıdır

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
import json
import subprocess

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
# EN: ACQUISITION SUPPORT CLASS PURPOSE MEMORY BLOCK V6 / FetchedPageResult
# EN:
# EN: Why this class exists:
# EN: - because shared acquisition-support truth for 'FetchedPageResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand support-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named support payload, normalized helper shape, request/response structure, or structured result carrier
# EN: - visible field set currently detected here: url_id, requested_url, final_url, http_status, content_type, etag, last_modified, body_bytes, raw_storage_path, raw_sha256, fetched_at
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely shapes fetched-page, request, response, or page-support payloads
# EN: - explicit support payload structure is often important for audits and later parse layers
# EN: - visible success vs degraded helper meaning may matter here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no acquisition-support contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: ACQUISITION SUPPORT CLASS AMAÇ HAFIZA BLOĞU V6 / FetchedPageResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'FetchedPageResult' için ortak acquisition-support doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip support tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli support payloadı, normalize helper şekli, request/response yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: url_id, requested_url, final_url, http_status, content_type, etag, last_modified, body_bytes, raw_storage_path, raw_sha256, fetched_at
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle fetched-page, request, response veya page-support payloadlarını şekillendirir
# TR: - açık support payload yapısı çoğu zaman denetimler ve sonraki parse katmanları için önemlidir
# TR: - görünür success vs degraded helper anlamı burada önemli olabilir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı acquisition-support sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: ACQUISITION SUPPORT CLASS PURPOSE MEMORY BLOCK V7 / FetchedPageResult
# EN:
# EN: Why this class exists:
# EN: - because this support layer should move one reusable acquisition result as a named contract instead of an anonymous dict
# EN: - because later validation, parse, storage, and audit steps need stable field names and readable branch meaning
# EN:
# EN: Accepted role:
# EN: - shared page acquisition result package
# EN:
# EN: Important contract reminders:
# EN: - url_id anchors the frontier.url identity of the fetched page
# EN: - requested_url records the original canonical URL that was requested
# EN: - final_url records the terminal URL after redirects or browser navigation
# EN: - raw_storage_path points to the persisted raw artefact on disk
# EN: - raw_sha256 records the expected persisted body fingerprint
# EN: - fetched_at records when the acquisition result was produced
# TR: ACQUISITION SUPPORT CLASS AMAÇ HAFIZA BLOĞU V7 / FetchedPageResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü bu support katmanı tekrar kullanılabilir acquisition sonucunu anonim dict yerine isimli sözleşme olarak taşımalıdır
# TR: - çünkü sonraki validation, parse, storage ve denetim adımları kararlı alan isimlerine ve okunabilir dal anlamına ihtiyaç duyar
# TR:
# TR: Kabul edilen rol:
# TR: - shared page acquisition result package
# TR:
# TR: Önemli sözleşme hatırlatmaları:
# TR: - url_id anchors the frontier.url identity of the fetched page
# TR: - requested_url records the original canonical URL that was requested
# TR: - final_url records the terminal URL after redirects or browser navigation
# TR: - raw_storage_path points to the persisted raw artefact on disk
# TR: - raw_sha256 records the expected persisted body fingerprint
# TR: - fetched_at records when the acquisition result was produced
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
# EN: ACQUISITION SUPPORT CLASS PURPOSE MEMORY BLOCK V6 / FetchedRobotsTxtResult
# EN:
# EN: Why this class exists:
# EN: - because shared acquisition-support truth for 'FetchedRobotsTxtResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand support-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named support payload, normalized helper shape, request/response structure, or structured result carrier
# EN: - visible field set currently detected here: host_id, robots_url, final_url, http_status, content_type, etag, last_modified, body_bytes, raw_storage_path, raw_sha256, fetched_at, fetch_error_class, fetch_error_message
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely shapes fetched-page, request, response, or page-support payloads
# EN: - explicit support payload structure is often important for audits and later parse layers
# EN: - visible success vs degraded helper meaning may matter here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no acquisition-support contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: ACQUISITION SUPPORT CLASS AMAÇ HAFIZA BLOĞU V6 / FetchedRobotsTxtResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'FetchedRobotsTxtResult' için ortak acquisition-support doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip support tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli support payloadı, normalize helper şekli, request/response yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: host_id, robots_url, final_url, http_status, content_type, etag, last_modified, body_bytes, raw_storage_path, raw_sha256, fetched_at, fetch_error_class, fetch_error_message
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle fetched-page, request, response veya page-support payloadlarını şekillendirir
# TR: - açık support payload yapısı çoğu zaman denetimler ve sonraki parse katmanları için önemlidir
# TR: - görünür success vs degraded helper anlamı burada önemli olabilir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı acquisition-support sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: ACQUISITION SUPPORT CLASS PURPOSE MEMORY BLOCK V7 / FetchedRobotsTxtResult
# EN:
# EN: Why this class exists:
# EN: - because this support layer should move one reusable acquisition result as a named contract instead of an anonymous dict
# EN: - because later validation, parse, storage, and audit steps need stable field names and readable branch meaning
# EN:
# EN: Accepted role:
# EN: - shared robots.txt acquisition result package
# EN:
# EN: Important contract reminders:
# EN: - host_id anchors the frontier.host identity whose robots contract was fetched
# EN: - robots_url records the explicit robots.txt URL that was requested
# EN: - final_url records the terminal robots URL after transport handling
# EN: - raw_storage_path is used only for body-present persisted robots results
# EN: - raw_sha256 records the expected persisted robots body fingerprint when a body exists
# EN: - fetched_at records when the robots acquisition result was produced
# TR: ACQUISITION SUPPORT CLASS AMAÇ HAFIZA BLOĞU V7 / FetchedRobotsTxtResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü bu support katmanı tekrar kullanılabilir acquisition sonucunu anonim dict yerine isimli sözleşme olarak taşımalıdır
# TR: - çünkü sonraki validation, parse, storage ve denetim adımları kararlı alan isimlerine ve okunabilir dal anlamına ihtiyaç duyar
# TR:
# TR: Kabul edilen rol:
# TR: - shared robots.txt acquisition result package
# TR:
# TR: Önemli sözleşme hatırlatmaları:
# TR: - host_id anchors the frontier.host identity whose robots contract was fetched
# TR: - robots_url records the explicit robots.txt URL that was requested
# TR: - final_url records the terminal robots URL after transport handling
# TR: - raw_storage_path is used only for body-present persisted robots results
# TR: - raw_sha256 records the expected persisted robots body fingerprint when a body exists
# TR: - fetched_at records when the robots acquisition result was produced
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_acquisition_contract_degraded_payload
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'build_acquisition_contract_degraded_payload' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: action, target_kind, target_id, requested_url, final_url, content_type, body_bytes, raw_storage_path, raw_sha256, fetched_at, error_class, error_message
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_acquisition_contract_degraded_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_acquisition_contract_degraded_payload' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: action, target_kind, target_id, requested_url, final_url, content_type, body_bytes, raw_storage_path, raw_sha256, fetched_at, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / build_acquisition_contract_degraded_payload
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - shared degraded acquisition contract builder
# EN:
# EN: Parameter contract:
# EN: - action => short helper-action label that says which acquisition-support step degraded
# EN: - target_kind => target family such as page or robots
# EN: - target_id => numeric identity of the affected target row
# EN: - requested_url => original requested URL text when available
# EN: - final_url => terminal URL text when available
# EN: - content_type => observed content type when available
# EN: - body_bytes => expected or observed body size when available
# EN: - raw_storage_path => persisted raw artefact path when available
# EN: - raw_sha256 => expected raw artefact SHA256 when available
# EN: - fetched_at => fetch timestamp text when available
# EN: - error_class => stable machine-readable error label
# EN: - error_message => human-readable failure explanation
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_acquisition_contract_degraded_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - shared degraded acquisition contract builder
# TR:
# TR: Parametre sözleşmesi:
# TR: - action => short helper-action label that says which acquisition-support step degraded
# TR: - target_kind => target family such as page or robots
# TR: - target_id => numeric identity of the affected target row
# TR: - requested_url => original requested URL text when available
# TR: - final_url => terminal URL text when available
# TR: - content_type => observed content type when available
# TR: - body_bytes => expected or observed body size when available
# TR: - raw_storage_path => persisted raw artefact path when available
# TR: - raw_sha256 => expected raw artefact SHA256 when available
# TR: - fetched_at => fetch timestamp text when available
# TR: - error_class => stable machine-readable error label
# TR: - error_message => human-readable failure explanation
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / read_controlled_raw_artefact_bytes
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'read_controlled_raw_artefact_bytes' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: action, target_kind, target_id, requested_url, final_url, content_type, body_bytes, raw_storage_path, raw_sha256, fetched_at
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / read_controlled_raw_artefact_bytes
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'read_controlled_raw_artefact_bytes' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: action, target_kind, target_id, requested_url, final_url, content_type, body_bytes, raw_storage_path, raw_sha256, fetched_at
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / read_controlled_raw_artefact_bytes
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - controlled raw artefact reader with path-safety and degradation handling
# EN:
# EN: Parameter contract:
# EN: - action => short helper-action label used if reading degrades
# EN: - target_kind => target family such as page or robots
# EN: - target_id => numeric identity of the affected target row
# EN: - requested_url => original requested URL text when available
# EN: - final_url => terminal URL text when available
# EN: - content_type => observed content type when available
# EN: - body_bytes => expected body size when available
# EN: - raw_storage_path => persisted raw artefact path that should be read
# EN: - raw_sha256 => expected raw artefact SHA256 when available
# EN: - fetched_at => fetch timestamp text when available
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / read_controlled_raw_artefact_bytes
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - controlled raw artefact reader with path-safety and degradation handling
# TR:
# TR: Parametre sözleşmesi:
# TR: - action => short helper-action label used if reading degrades
# TR: - target_kind => target family such as page or robots
# TR: - target_id => numeric identity of the affected target row
# TR: - requested_url => original requested URL text when available
# TR: - final_url => terminal URL text when available
# TR: - content_type => observed content type when available
# TR: - body_bytes => expected body size when available
# TR: - raw_storage_path => persisted raw artefact path that should be read
# TR: - raw_sha256 => expected raw artefact SHA256 when available
# TR: - fetched_at => fetch timestamp text when available
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
    # EN: controlled_root is the resolved trusted raw root used as the containment anchor for later safety checks.
    # TR: controlled_root, sonraki güvenlik kontrolleri için kapsama çapası olarak kullanılan resolve edilmiş güvenilir raw köktür.
    controlled_root = RAW_FETCH_ROOT.resolve()

    # EN: We resolve the target artefact path without requiring existence first,
    # EN: because we want to distinguish path-shape problems from missing-file problems.
    # TR: Hedef artefact yolunu önce varlık zorunluluğu olmadan resolve ediyoruz;
    # TR: çünkü yol-şekli sorunlarını eksik-dosya sorunlarından ayırmak istiyoruz.
    try:
# EN: resolved_path is the normalized filesystem path derived from raw_storage_path.
# EN: We compute it before existence checks so path-shape failures and missing-file failures stay distinguishable.
# TR: resolved_path, raw_storage_path değerinden türetilen normalize edilmiş dosya sistemi yoludur.
# TR: Bunu varlık kontrollerinden önce hesaplıyoruz; böylece yol-şekli hataları ile eksik-dosya hataları birbirinden ayrılabilir kalır.
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
# EN: raw_bytes is the actual persisted artefact content read from disk.
# EN: Later body-size and SHA256 validation must compare against these exact bytes.
# TR: raw_bytes diskten okunan gerçek saklanmış artefact içeriğidir.
# TR: Sonraki body-size ve SHA256 doğrulaması tam olarak bu byte'lar üzerinden yapılmalıdır.
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / validate_fetched_page_result_contract
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'validate_fetched_page_result_contract' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: fetched_page
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely shapes fetched-page, request, response, or page-support payloads
# EN: - explicit support payload structure is often important for audits and later parse layers
# EN: - visible success vs degraded helper meaning may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / validate_fetched_page_result_contract
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'validate_fetched_page_result_contract' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: fetched_page
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle fetched-page, request, response veya page-support payloadlarını şekillendirir
# TR: - açık support payload yapısı çoğu zaman denetimler ve sonraki parse katmanları için önemlidir
# TR: - görünür success vs degraded helper anlamı burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / validate_fetched_page_result_contract
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - page-result contract validator for persisted raw fetch artefacts
# EN:
# EN: Parameter contract:
# EN: - fetched_page => named fetched page contract object that must match persisted disk truth
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / validate_fetched_page_result_contract
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - page-result contract validator for persisted raw fetch artefacts
# TR:
# TR: Parametre sözleşmesi:
# TR: - fetched_page => named fetched page contract object that must match persisted disk truth
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
# EN: raw_storage_path is the normalized string form of path used in later degraded payloads and mismatch messages.
# TR: raw_storage_path, sonraki degrade payload'larda ve uyuşmazlık mesajlarında kullanılacak normalize string yol biçimidir.
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

# EN: controlled_read_result is the guarded read outcome returned by the controlled raw-artefact reader.
# EN: It may be a degraded payload dict or a successful tuple carrying persisted artefact data.
# TR: controlled_read_result, kontrollü ham artefact okuyucusundan dönen korumalı okuma sonucudur.
# TR: Bu değer degrade payload dict'i de olabilir, saklanmış artefact verisini taşıyan başarılı bir tuple da olabilir.
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

# EN: path is the persisted artefact path returned by the controlled reader.
# EN: raw_bytes is the exact persisted file content returned together with path.
# TR: path, kontrollü okuyucunun döndürdüğü saklanmış artefact yoludur.
# TR: raw_bytes ise path ile birlikte dönen tam saklanmış dosya içeriğidir.
    path, raw_bytes = controlled_read_result
# EN: raw_storage_path is the normalized string form of path used in later degraded payloads and mismatch messages.
# TR: raw_storage_path, sonraki degrade payload'larda ve uyuşmazlık mesajlarında kullanılacak normalize string yol biçimidir.
    raw_storage_path = str(path)

    # EN: raw_sha256 must look like a full SHA256 hex digest.
    # TR: raw_sha256 tam bir SHA256 hex özeti gibi görünmelidir.
    # EN: raw_sha256 is the normalized declared digest string that we compare against the persisted raw bytes.
    # TR: raw_sha256, saklanan ham byte'larla karşılaştırdığımız normalize edilmiş beyan edilen özet metnidir.
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
    # EN: actual_body_bytes is the true byte length of the persisted artefact that was read back from disk.
    # TR: actual_body_bytes, diskten geri okunan saklanmış artefact'ın gerçek byte uzunluğudur.
    actual_body_bytes = len(raw_bytes)
# EN: expected_body_bytes is the declared body size from fetched_page metadata.
# EN: We keep it separately so declared size and actual persisted size can be compared explicitly.
# TR: expected_body_bytes, fetched_page metadata'sındaki beyan edilmiş body boyutudur.
# TR: Bunu ayrı tutuyoruz; böylece beyan edilen boyut ile gerçek saklanmış boyut açık biçimde karşılaştırılabilir.
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

# EN: actual_sha256 is the real SHA256 fingerprint computed from persisted raw_bytes.
# EN: It must match the declared raw_sha256 or the page-result contract has drifted.
# TR: actual_sha256, saklanmış raw_bytes üzerinden hesaplanan gerçek SHA256 parmak izidir.
# TR: Bu değer beyan edilen raw_sha256 ile eşleşmelidir; aksi halde page-result sözleşmesi drift etmiştir.
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / validate_fetched_robots_result_contract
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'validate_fetched_robots_result_contract' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: robots_fetch
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely shapes fetched-page, request, response, or page-support payloads
# EN: - explicit support payload structure is often important for audits and later parse layers
# EN: - visible success vs degraded helper meaning may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / validate_fetched_robots_result_contract
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'validate_fetched_robots_result_contract' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: robots_fetch
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle fetched-page, request, response veya page-support payloadlarını şekillendirir
# TR: - açık support payload yapısı çoğu zaman denetimler ve sonraki parse katmanları için önemlidir
# TR: - görünür success vs degraded helper anlamı burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / validate_fetched_robots_result_contract
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - robots-result contract validator for persisted raw robots artefacts
# EN:
# EN: Parameter contract:
# EN: - robots_fetch => named fetched robots contract object that must match persisted disk truth
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / validate_fetched_robots_result_contract
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - robots-result contract validator for persisted raw robots artefacts
# TR:
# TR: Parametre sözleşmesi:
# TR: - robots_fetch => named fetched robots contract object that must match persisted disk truth
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
# EN: raw_storage_path is the normalized string form of path reused in later contract-mismatch messages.
# TR: raw_storage_path, sonraki sözleşme-uyuşmazlığı mesajlarında yeniden kullanılacak normalize string yol biçimidir.
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

# EN: controlled_read_result is the guarded read outcome for the persisted robots artefact.
# EN: It may degrade into a payload dict or succeed with the persisted path-and-bytes tuple.
# TR: controlled_read_result, saklanmış robots artefact'ı için korumalı okuma sonucudur.
# TR: Bu değer payload dict'e degrade olabilir veya saklanmış yol-ve-byte tuple'ı ile başarılı dönebilir.
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

# EN: path is the persisted robots artefact path returned by the controlled reader.
# EN: raw_bytes is the exact persisted robots body returned together with path.
# TR: path, kontrollü okuyucunun döndürdüğü saklanmış robots artefact yoludur.
# TR: raw_bytes ise path ile birlikte dönen tam saklanmış robots body içeriğidir.
    path, raw_bytes = controlled_read_result
# EN: raw_storage_path is the normalized string form of path reused in later contract-mismatch messages.
# TR: raw_storage_path, sonraki sözleşme-uyuşmazlığı mesajlarında yeniden kullanılacak normalize string yol biçimidir.
    raw_storage_path = str(path)

# EN: raw_sha256 is the declared robots artefact fingerprint normalized to lowercase text.
# EN: We isolate it before validation so malformed or missing fingerprints degrade explicitly.
# TR: raw_sha256, küçük harfe normalize edilmiş beyan edilmiş robots artefact parmak izidir.
# TR: Bunu doğrulamadan önce ayırıyoruz; böylece bozuk veya eksik parmak izleri açık biçimde degrade olur.
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

# EN: actual_body_bytes is the real persisted robots body size measured from raw_bytes.
# TR: actual_body_bytes, raw_bytes üzerinden ölçülen gerçek saklanmış robots body boyutudur.
    actual_body_bytes = len(raw_bytes)
# EN: expected_body_bytes is the declared robots body size from robots_fetch metadata.
# TR: expected_body_bytes, robots_fetch metadata'sındaki beyan edilmiş robots body boyutudur.
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

# EN: actual_sha256 is the real SHA256 fingerprint computed from persisted robots raw_bytes.
# TR: actual_sha256, saklanmış robots raw_bytes üzerinden hesaplanan gerçek SHA256 parmak izidir.
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / utc_now
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'utc_now' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / utc_now
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'utc_now' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / utc_now
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - UTC current-time helper used by shared acquisition support code
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / utc_now
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - UTC current-time helper used by shared acquisition support code
def utc_now() -> datetime:
    # EN: We explicitly use timezone.utc so no local-machine timezone ambiguity leaks in.
    # TR: Yerel makine saat dilimi belirsizliği sızmasın diye açıkça timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc)

# EN: This helper formats a UTC timestamp as an ISO-8601 string.
# TR: Bu yardımcı UTC zaman damgasını ISO-8601 metni olarak biçimlendirir.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / utc_now_iso
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'utc_now_iso' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / utc_now_iso
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'utc_now_iso' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / utc_now_iso
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - UTC current-time formatter that returns ISO-8601 text
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / utc_now_iso
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - UTC current-time formatter that returns ISO-8601 text
def utc_now_iso() -> str:
    # EN: We delegate to utc_now() so all current-time generation stays consistent.
    # TR: Tüm mevcut-zaman üretimi tutarlı kalsın diye utc_now() yardımcısını kullanıyoruz.
    return utc_now().isoformat()

# EN: This helper turns a datetime into a compact filesystem-safe UTC timestamp.
# TR: Bu yardımcı bir datetime değerini filesystem için güvenli, kompakt bir UTC
# TR: zaman damgasına dönüştürür.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / utc_path_stamp
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'utc_path_stamp' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: moment
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / utc_path_stamp
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'utc_path_stamp' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: moment
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / utc_path_stamp
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - filesystem-safe UTC timestamp formatter
# EN:
# EN: Parameter contract:
# EN: - moment => datetime value that will be rendered as a compact UTC path stamp
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / utc_path_stamp
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - filesystem-safe UTC timestamp formatter
# TR:
# TR: Parametre sözleşmesi:
# TR: - moment => datetime value that will be rendered as a compact UTC path stamp
def utc_path_stamp(moment: datetime) -> str:
    # EN: We use a compact YYYYMMDDTHHMMSSZ shape because it is easy to sort lexically.
    # TR: Leksik olarak kolay sıralandığı için kompakt YYYYMMDDTHHMMSSZ biçimini kullanıyoruz.
    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# EN: This helper reads one field from a claimed_url object in a tolerant way.
# EN: The current worker surfaces may hand us either an attribute-style object or a dict-like object.
# TR: Bu yardımcı claimed_url nesnesinden bir alanı toleranslı biçimde okur.
# TR: Güncel worker yüzeyleri bize attribute-stili bir nesne veya dict-benzeri bir nesne verebilir.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / get_claimed_url_value
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'get_claimed_url_value' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, field_name
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / get_claimed_url_value
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'get_claimed_url_value' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, field_name
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / get_claimed_url_value
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - tolerant claimed_url field reader across dict-like and attribute-style inputs
# EN:
# EN: Parameter contract:
# EN: - claimed_url => claimed work-item object or dict-like payload
# EN: - field_name => field name that must be extracted from claimed_url
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / get_claimed_url_value
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - tolerant claimed_url field reader across dict-like and attribute-style inputs
# TR:
# TR: Parametre sözleşmesi:
# TR: - claimed_url => claimed work-item object or dict-like payload
# TR: - field_name => field name that must be extracted from claimed_url
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_raw_fetch_storage_path
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'build_raw_fetch_storage_path' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, fetched_at, raw_root
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely shapes fetched-page, request, response, or page-support payloads
# EN: - explicit support payload structure is often important for audits and later parse layers
# EN: - visible success vs degraded helper meaning may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_raw_fetch_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_raw_fetch_storage_path' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, fetched_at, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle fetched-page, request, response veya page-support payloadlarını şekillendirir
# TR: - açık support payload yapısı çoğu zaman denetimler ve sonraki parse katmanları için önemlidir
# TR: - görünür success vs degraded helper anlamı burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / build_raw_fetch_storage_path
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - raw direct-fetch artefact path builder
# EN:
# EN: Parameter contract:
# EN: - url_id => frontier.url identity used in the filename
# EN: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# EN: - raw_root => root directory under which raw fetch artefacts are stored
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_raw_fetch_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - raw direct-fetch artefact path builder
# TR:
# TR: Parametre sözleşmesi:
# TR: - url_id => frontier.url identity used in the filename
# TR: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# TR: - raw_root => root directory under which raw fetch artefacts are stored
def build_raw_fetch_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    # EN: day_root is the UTC year/month/day directory that groups this raw fetch artefact under one inspectable daily partition.
    # TR: day_root, bu ham fetch artefact'ını tek bir incelenebilir günlük bölüm altında toplayan UTC year/month/day dizinidir.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: We create one deterministic filename that includes the frontier url id
    # EN: and the UTC fetch timestamp.
    # TR: Frontier url id'sini ve UTC fetch zaman damgasını içeren deterministik
    # TR: tek bir dosya adı oluşturuyoruz.
    # EN: filename is the deterministic body artefact file name for this direct raw page fetch.
    # TR: filename, bu doğrudan ham sayfa fetch'i için deterministik body artefact dosya adıdır.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.body.bin"

    # EN: We return the final full path object.
    # TR: Nihai tam path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper builds the deterministic raw-storage path for one robots.txt body.
# TR: Bu yardımcı tek bir robots.txt body için deterministik ham-saklama yolunu kurar.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_raw_robots_storage_path
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'build_raw_robots_storage_path' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: host_id, fetched_at, raw_root
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_raw_robots_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_raw_robots_storage_path' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: host_id, fetched_at, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / build_raw_robots_storage_path
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - raw robots artefact path builder
# EN:
# EN: Parameter contract:
# EN: - host_id => frontier.host identity used in the filename
# EN: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# EN: - raw_root => root directory under which raw robots artefacts are stored
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_raw_robots_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - raw robots artefact path builder
# TR:
# TR: Parametre sözleşmesi:
# TR: - host_id => frontier.host identity used in the filename
# TR: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# TR: - raw_root => root directory under which raw robots artefacts are stored
def build_raw_robots_storage_path(
    *,
    host_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    # EN: day_root is the UTC year/month/day directory that groups this robots artefact under one inspectable daily partition.
    # TR: day_root, bu robots artefact'ını tek bir incelenebilir günlük bölüm altında gruplayan UTC year/month/day dizinidir.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename carries host identity plus UTC timestamp so later audits can
    # EN: connect the artefact back to the exact host-level robots refresh.
    # TR: Dosya adı host kimliğini ve UTC zaman damgasını taşır; böylece sonraki
    # TR: audit'ler artefact'ı tam host-seviyesi robots refresh işlemine bağlayabilir.
    # EN: filename is the deterministic raw robots.txt artefact file name for this host-level refresh event.
    # TR: filename, bu host-seviyesi refresh olayı için deterministik ham robots.txt artefact dosya adıdır.
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
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_browser_rendered_storage_path
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'build_browser_rendered_storage_path' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, fetched_at, raw_root
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely helps browser/http shared normalization or acquisition-method helper meaning
# EN: - explicit shared helper semantics are important because multiple acquisition children may reuse them
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_browser_rendered_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_browser_rendered_storage_path' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, fetched_at, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser/http ortak normalization veya acquisition-method helper anlamına yardım eder
# TR: - açık ortak helper semantiği önemlidir çünkü birden çok acquisition child yüzeyi bunları tekrar kullanabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / build_browser_rendered_storage_path
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - browser-rendered HTML artefact path builder
# EN:
# EN: Parameter contract:
# EN: - url_id => frontier.url identity used in the filename
# EN: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# EN: - raw_root => root directory under which browser-rendered artefacts are stored
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_browser_rendered_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - browser-rendered HTML artefact path builder
# TR:
# TR: Parametre sözleşmesi:
# TR: - url_id => frontier.url identity used in the filename
# TR: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# TR: - raw_root => root directory under which browser-rendered artefacts are stored
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
    # EN: day_root is the UTC year/month/day directory that groups this browser-rendered artefact beside related raw captures.
    # TR: day_root, bu browser-rendered artefact'ı ilgili ham kayıtların yanında gruplayan UTC year/month/day dizinidir.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename explicitly says this is a rendered HTML body, not the original wire body.
    # TR: Dosya adı bunun orijinal wire body değil, rendered HTML body olduğunu açıkça söyler.
    # EN: filename is the deterministic rendered-HTML artefact file name for this browser-backed page capture.
    # TR: filename, bu browser-backed sayfa kaydı için deterministik rendered-HTML artefact dosya adıdır.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.rendered.html"

    # EN: We return the final full Path object.
    # TR: Nihai tam Path nesnesini döndürüyoruz.
    return day_root / filename


RAW_FETCH_JSON_ZSTD_SCHEMA_VERSION = "logisticsearch.raw_fetch.envelope.v1"
RAW_FETCH_JSON_ZSTD_EXTENSION = ".fetch.json.zst"
RAW_FETCH_JSON_ZSTD_CLI = Path("/usr/bin/zstd")


def build_raw_fetch_json_zstd_sidecar_path(raw_body_path: Path | str) -> Path:
    # EN: This helper derives the compressed JSON sidecar path from the existing
    # EN: raw body evidence path without changing the original evidence file.
    # TR: Bu helper mevcut ham body kanıt dosyasını değiştirmeden sıkıştırılmış
    # TR: JSON sidecar yolunu türetir.
    path = Path(raw_body_path)
    name = path.name
    for raw_suffix in (".body.bin", ".rendered.html"):
        if name.endswith(raw_suffix):
            return path.with_name(name[: -len(raw_suffix)] + RAW_FETCH_JSON_ZSTD_EXTENSION)
    return path.with_name(name + RAW_FETCH_JSON_ZSTD_EXTENSION)


def decode_raw_fetch_body_as_html_text(
    raw_body_bytes: bytes,
    *,
    content_type: str | None,
) -> tuple[str, str]:
    # EN: We prefer the declared charset when present, then fall back safely to
    # EN: UTF-8 replacement decoding so the JSON envelope remains inspectable.
    # TR: Varsa bildirilen charset'i tercih ediyoruz; yoksa JSON zarfı
    # TR: incelenebilir kalsın diye güvenli UTF-8 replacement decode kullanıyoruz.
    declared_encoding = "utf-8"
    if content_type:
        for content_type_part in str(content_type).split(";"):
            if "charset" in content_type_part.lower() and "=" in content_type_part:
                declared_encoding = content_type_part.split("=", 1)[1].strip().strip("\"'") or "utf-8"
                break

    try:
        return raw_body_bytes.decode(declared_encoding), f"declared_charset:{declared_encoding}"
    except (LookupError, UnicodeDecodeError):
        return raw_body_bytes.decode("utf-8", errors="replace"), f"utf8_replace_after_failed:{declared_encoding}"


def build_raw_fetch_json_zstd_envelope(
    *,
    url_id: int,
    host_id: int | None,
    requested_url: str,
    final_url: str,
    http_status: int | None,
    content_type: str | None,
    content_encoding: str | None,
    raw_body_path: Path | str,
    raw_body_bytes: bytes,
    raw_sha256: str,
    fetched_at: str,
    acquisition_method: str,
) -> tuple[dict[str, object], bytes]:
    # EN: The envelope keeps decoded HTML with tags for inspection while the raw
    # EN: body artefact remains the durable byte-for-byte source of truth.
    # TR: Zarf inceleme için tag'leriyle decode edilmiş HTML tutar; ham body
    # TR: artefact'ı byte-for-byte kalıcı doğruluk kaynağı olarak kalır.
    computed_sha256 = sha256_hex(raw_body_bytes)
    if computed_sha256 != raw_sha256:
        raise RuntimeError(
            "raw fetch JSON envelope SHA mismatch: "
            f"expected={raw_sha256} actual={computed_sha256}"
        )

    html_text, html_decode_strategy = decode_raw_fetch_body_as_html_text(
        raw_body_bytes,
        content_type=content_type,
    )

    envelope: dict[str, object] = {
        "schema_version": RAW_FETCH_JSON_ZSTD_SCHEMA_VERSION,
        "compression": "zstd",
        "url_id": int(url_id),
        "host_id": None if host_id is None else int(host_id),
        "requested_url": str(requested_url),
        "final_url": str(final_url),
        "http_status": http_status,
        "content_type": content_type,
        "content_encoding": content_encoding,
        "body_bytes": len(raw_body_bytes),
        "body_sha256": raw_sha256,
        "raw_body_path": str(raw_body_path),
        "raw_json_uncompressed_bytes": None,
        "fetched_at": str(fetched_at),
        "html": html_text,
        "html_decode_strategy": html_decode_strategy,
        "storage_policy": {
            "raw_fetch_root": str(RAW_FETCH_ROOT),
            "parse_core_primary": "/srv/data",
            "parse_core_fallback": "/srv/buffer",
            "pause_rule": (
                "pause_if_raw_fetch_unusable_or_full_or_both_data_and_buffer_unusable_or_full"
            ),
        },
        "crawler_metadata": {
            "runtime_surface": "crawler_core",
            "acquisition_method": acquisition_method,
            "secrets_redacted": True,
            "contains_lease_token": False,
            "contains_user_agent_token": False,
            "contains_dsn": False,
        },
    }

    raw_json_bytes = json.dumps(
        envelope,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    envelope["raw_json_uncompressed_bytes"] = len(raw_json_bytes)
    raw_json_bytes = json.dumps(
        envelope,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return envelope, raw_json_bytes


def _write_raw_fetch_json_zstd_envelope_compressed_only_v1(
    *,
    url_id: int,
    host_id: int | None,
    requested_url: str,
    final_url: str,
    http_status: int | None,
    content_type: str | None,
    content_encoding: str | None = None,
    raw_body_path: Path | str,
    raw_body_bytes: bytes,
    raw_sha256: str,
    fetched_at: str,
    acquisition_method: str,
) -> str:
    # EN: This function writes a compressed JSON sidecar beside the existing raw
    # EN: evidence file. The original raw evidence path remains unchanged.
    # TR: Bu fonksiyon mevcut ham kanıt dosyasının yanına sıkıştırılmış JSON
    # TR: sidecar yazar. Özgün ham kanıt yolu değişmeden kalır.
    if not RAW_FETCH_JSON_ZSTD_CLI.is_file():
        raise RuntimeError(f"zstd CLI is missing: {RAW_FETCH_JSON_ZSTD_CLI}")

    sidecar_path = build_raw_fetch_json_zstd_sidecar_path(raw_body_path)
    sidecar_path.parent.mkdir(parents=True, exist_ok=True)

    _, raw_json_bytes = build_raw_fetch_json_zstd_envelope(
        url_id=url_id,
        host_id=host_id,
        requested_url=requested_url,
        final_url=final_url,
        http_status=http_status,
        content_type=content_type,
        content_encoding=content_encoding,
        raw_body_path=raw_body_path,
        raw_body_bytes=raw_body_bytes,
        raw_sha256=raw_sha256,
        fetched_at=fetched_at,
        acquisition_method=acquisition_method,
    )

    temp_sidecar_path = sidecar_path.with_name(sidecar_path.name + ".tmp")
    completed_process = subprocess.run(
        [
            str(RAW_FETCH_JSON_ZSTD_CLI),
            "-q",
            "-f",
            "-o",
            str(temp_sidecar_path),
            "-",
        ],
        input=raw_json_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed_process.returncode != 0:
        stderr_text = completed_process.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(
            "zstd JSON envelope compression failed: "
            f"rc={completed_process.returncode} stderr={stderr_text}"
        )

    temp_sidecar_path.replace(sidecar_path)
    return str(sidecar_path)


# EN: This helper builds the screenshot evidence path that belongs to the same browser fetch.
# EN: We keep screenshot and rendered HTML as sibling artefacts with the same timestamp stem.
# TR: Bu yardımcı, aynı browser fetch'e ait screenshot kanıt yolunu üretir.
# TR: Screenshot ve rendered HTML'i aynı zaman damgalı köke sahip kardeş artefact'lar olarak tutuyoruz.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_browser_screenshot_storage_path
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'build_browser_screenshot_storage_path' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, fetched_at, raw_root
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface likely helps browser/http shared normalization or acquisition-method helper meaning
# EN: - explicit shared helper semantics are important because multiple acquisition children may reuse them
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_browser_screenshot_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_browser_screenshot_storage_path' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, fetched_at, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle browser/http ortak normalization veya acquisition-method helper anlamına yardım eder
# TR: - açık ortak helper semantiği önemlidir çünkü birden çok acquisition child yüzeyi bunları tekrar kullanabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / build_browser_screenshot_storage_path
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - browser screenshot artefact path builder
# EN:
# EN: Parameter contract:
# EN: - url_id => frontier.url identity used in the filename
# EN: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# EN: - raw_root => root directory under which browser screenshot artefacts are stored
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_browser_screenshot_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - browser screenshot artefact path builder
# TR:
# TR: Parametre sözleşmesi:
# TR: - url_id => frontier.url identity used in the filename
# TR: - fetched_at => fetch timestamp used for UTC date partitioning and stamp text
# TR: - raw_root => root directory under which browser screenshot artefacts are stored
def build_browser_screenshot_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We use the same UTC day partitioning as every other raw acquisition artefact.
    # TR: Diğer tüm ham acquisition artefact'larıyla aynı UTC gün bölmesini kullanıyoruz.
    # EN: day_root is the UTC year/month/day directory that holds this screenshot artefact together with sibling acquisition outputs.
    # TR: day_root, bu screenshot artefact'ını kardeş acquisition çıktılarıyla birlikte tutan UTC year/month/day dizinidir.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename explicitly marks this sibling artefact as a screenshot.
    # TR: Dosya adı bu kardeş artefact'ın screenshot olduğunu açıkça işaretler.
    # EN: filename is the deterministic screenshot artefact file name paired with the same browser fetch event.
    # TR: filename, aynı browser fetch olayıyla eşlenen deterministik screenshot artefact dosya adıdır.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.screenshot.png"

    # EN: We return the final full Path object.
    # TR: Nihai tam Path nesnesini döndürüyoruz.
    return day_root / filename

# EN: This helper ensures the parent directory of a target file exists.
# TR: Bu yardımcı hedef dosyanın parent dizininin var olduğundan emin olur.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / ensure_parent_directory
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'ensure_parent_directory' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: path
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / ensure_parent_directory
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'ensure_parent_directory' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: path
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / ensure_parent_directory
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - filesystem parent-directory creator for acquisition artefacts
# EN:
# EN: Parameter contract:
# EN: - path => target path whose parent directory must exist before writing
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / ensure_parent_directory
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - filesystem parent-directory creator for acquisition artefacts
# TR:
# TR: Parametre sözleşmesi:
# TR: - path => target path whose parent directory must exist before writing
def ensure_parent_directory(path: Path) -> None:
    # EN: parents=True lets deeper missing directories be created in one step.
    # TR: parents=True daha derindeki eksik dizinlerin tek adımda oluşturulmasını sağlar.
    path.parent.mkdir(parents=True, exist_ok=True)

# EN: This helper computes the SHA256 hex digest of raw bytes.
# TR: Bu yardımcı ham byte'ların SHA256 hex özetini hesaplar.
# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / sha256_hex
# EN:
# EN: Why this function exists:
# EN: - because shared acquisition helper truth for 'sha256_hex' should be exposed through one named top-level boundary
# EN: - because support semantics should remain readable instead of being copied into many acquisition children
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: data
# EN: - values should match the current Python signature and the shared acquisition-support contract below
# EN:
# EN: Accepted output:
# EN: - a shared acquisition-support result shape defined by the current function body
# EN: - this may be a helper payload, normalized page/request/response shape, method-related value, or another explicit support-side branch result
# EN:
# EN: Common acquisition-support meaning hints:
# EN: - this surface exposes one named shared acquisition support boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is shared acquisition-support logic, not the whole acquisition corridor
# EN: - support results must stay explicit so audits can understand reusable helper meaning and downstream fetched-page shaping
# EN:
# EN: Undesired behavior:
# EN: - silent helper mutation
# EN: - vague support results that hide branch meaning
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / sha256_hex
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'sha256_hex' için ortak acquisition yardımcı doğrusu tek ve isimli top-level sınır üzerinden açığa çıkmalıdır
# TR: - çünkü support semantiklerinin birçok acquisition child yüzeyine kopyalanarak dağılmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: data
# TR: - değerler aşağıdaki mevcut Python imzası ve ortak acquisition-support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen ortak acquisition-support sonuç şekli
# TR: - bu; helper payloadı, normalize page/request/response şekli, method ile ilgili değer veya başka açık support tarafı dal sonucu olabilir
# TR:
# TR: Ortak acquisition-support anlam ipuçları:
# TR: - bu yüzey isimli bir ortak acquisition support sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon ortak acquisition-support mantığıdır, acquisition koridorunun tamamı değildir
# TR: - support sonuçları açık kalmalıdır ki denetimler tekrar kullanılabilir helper anlamını ve downstream fetched-page shaping anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz helper değişimi
# TR: - dal anlamını gizleyen belirsiz support sonuçları

# EN: ACQUISITION SUPPORT FUNCTION PURPOSE MEMORY BLOCK V7 / sha256_hex
# EN:
# EN: Why this function exists:
# EN: - because this support layer needs one explicit reusable helper boundary
# EN: - because helper meaning should stay readable instead of leaking into silent inline drift
# EN:
# EN: Accepted role:
# EN: - SHA256 hex digest helper for raw bytes
# EN:
# EN: Parameter contract:
# EN: - data => raw bytes whose deterministic SHA256 hex digest will be returned
# TR: ACQUISITION SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V7 / sha256_hex
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü bu support katmanının açık ve tekrar kullanılabilir bir helper sınırına ihtiyacı vardır
# TR: - çünkü helper anlamı sessiz inline dağılma yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen rol:
# TR: - SHA256 hex digest helper for raw bytes
# TR:
# TR: Parametre sözleşmesi:
# TR: - data => raw bytes whose deterministic SHA256 hex digest will be returned
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


# EN: This helper controls whether the crawler also writes a plain JSON sidecar
# EN: beside the compressed .fetch.json.zst envelope.
# EN: The default is enabled for the short 15-minute validation test so we can
# EN: compare plain JSON size/content against Zstandard-compressed JSON.
# EN: For the future 24-hour system-limit test, set
# EN: LOGISTICSEARCH_RAW_FETCH_PLAIN_JSON_COMPARE_MODE=0 so only .fetch.json.zst
# EN: is kept as raw evidence.
# TR: Bu helper, sıkıştırılmış .fetch.json.zst envelope yanında plain JSON
# TR: sidecar yazılıp yazılmayacağını kontrol eder.
# TR: Varsayılan açık tutulur; çünkü 15 dakikalık doğrulama testinde plain JSON
# TR: boyutu/içeriği ile Zstandard sıkıştırılmış JSON karşılaştırılacaktır.
# TR: Gelecekteki 24 saatlik sistem-limit testinde yalnız .fetch.json.zst
# TR: tutulması için LOGISTICSEARCH_RAW_FETCH_PLAIN_JSON_COMPARE_MODE=0 verilir.
def raw_fetch_plain_json_compare_mode_enabled() -> bool:
    import os as _os

    value = _os.environ.get(
        "LOGISTICSEARCH_RAW_FETCH_PLAIN_JSON_COMPARE_MODE",
        "1",
    ).strip().lower()
    return value not in {"0", "false", "no", "off"}


# EN: This helper maps a compressed JSON envelope path to its plain comparison
# EN: JSON path by removing the final .zst suffix.
# TR: Bu helper, sıkıştırılmış JSON envelope yolunu, son .zst uzantısını
# TR: kaldırarak plain karşılaştırma JSON yoluna çevirir.
def build_raw_fetch_plain_json_compare_path_from_zstd_path(json_zstd_path):
    from pathlib import Path as _Path

    zstd_path = _Path(json_zstd_path)
    if zstd_path.name.endswith(".zst"):
        return zstd_path.with_name(zstd_path.name[:-4])
    return zstd_path.with_suffix(zstd_path.suffix + ".plain.json")


# EN: This helper infers the .fetch.json.zst path produced by the compressed
# EN: writer, without changing the writer's return contract.
# TR: Bu helper, compressed writer'ın dönüş sözleşmesini değiştirmeden üretilen
# TR: .fetch.json.zst yolunu çıkarır.
def infer_raw_fetch_json_zstd_path_from_writer_result(
    writer_result,
    bound_arguments: dict,
):
    from pathlib import Path as _Path

    if isinstance(writer_result, _Path):
        return writer_result

    if isinstance(writer_result, str):
        return _Path(writer_result)

    if isinstance(writer_result, dict):
        for key in (
            "json_zstd_path",
            "json_zst_path",
            "zstd_path",
            "compressed_json_path",
            "raw_fetch_json_zstd_path",
            "sidecar_path",
        ):
            value = writer_result.get(key)
            if value:
                return _Path(str(value))

    for key in (
        "raw_storage_path",
        "raw_body_path",
        "body_storage_path",
    ):
        value = bound_arguments.get(key)
        if value:
            return build_raw_fetch_json_zstd_sidecar_path(value)

    return None


# EN: This wrapper preserves the existing compressed JSON writer but adds the
# EN: short-test comparison behavior: when enabled, it decompresses the just-written
# EN: .fetch.json.zst into a sibling .fetch.json file.
# EN: The canonical runtime JSONL log remains unchanged.
# EN: No HTML is printed to the terminal.
# TR: Bu wrapper mevcut compressed JSON writer'ı korur fakat kısa-test
# TR: karşılaştırma davranışını ekler: açık olduğunda yeni yazılan
# TR: .fetch.json.zst dosyasını kardeş .fetch.json dosyasına açar.
# TR: Kanonik runtime JSONL log değişmeden kalır.
# TR: Terminale HTML basılmaz.
def write_raw_fetch_json_zstd_envelope(*args, **kwargs):
    import inspect as _inspect
    import subprocess as _subprocess

    compressed_result = _write_raw_fetch_json_zstd_envelope_compressed_only_v1(
        *args,
        **kwargs,
    )

    if not raw_fetch_plain_json_compare_mode_enabled():
        return compressed_result

    signature = _inspect.signature(
        _write_raw_fetch_json_zstd_envelope_compressed_only_v1
    )
    bound = signature.bind_partial(*args, **kwargs)
    bound_arguments = dict(bound.arguments)

    json_zstd_path = infer_raw_fetch_json_zstd_path_from_writer_result(
        compressed_result,
        bound_arguments,
    )

    if json_zstd_path is None:
        raise RuntimeError(
            "raw_fetch_json_zstd_plain_compare_path_unresolved"
        )

    json_zstd_path = Path(json_zstd_path)
    if not json_zstd_path.is_file():
        raise RuntimeError(
            f"raw_fetch_json_zstd_missing_for_plain_compare: {json_zstd_path}"
        )

    plain_json_path = build_raw_fetch_plain_json_compare_path_from_zstd_path(
        json_zstd_path
    )
    plain_json_tmp_path = plain_json_path.with_name(
        plain_json_path.name + ".tmp"
    )

    completed = _subprocess.run(
        [
            str(RAW_FETCH_JSON_ZSTD_CLI),
            "-d",
            "-c",
            str(json_zstd_path),
        ],
        check=True,
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
    )

    plain_json_tmp_path.write_bytes(completed.stdout)
    plain_json_tmp_path.replace(plain_json_path)

    return compressed_result
