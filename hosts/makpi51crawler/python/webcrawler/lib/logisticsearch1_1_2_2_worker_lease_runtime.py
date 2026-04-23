"""
EN:
This file is the worker-lease child of the worker-runtime family.

EN:
Why this file exists:
- because lease-specific runtime truth should live in one explicit child instead of being hidden inside the main worker hub
- because lease ownership, renewal timing, and lease-failure visibility are central worker concepts
- because a beginner should be able to find lease logic without digging through unrelated runtime phases

EN:
What this file DOES:
- expose worker-lease-oriented runtime helper boundaries
- preserve visible renewal, ownership, timeout, and degraded branch meaning
- keep lease-specific semantics separate from broader worker orchestration

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not own all robots logic
- it does not own all acquisition logic
- it does not own all parse/finalize logic

EN:
Topological role:
- the main worker runtime hub sits above this file
- this file owns narrow lease-side runtime semantics
- sibling worker submodules own other focused contracts such as robots, acquisition, parse, finalize, and storage

EN:
Important visible values and shapes:
- lease token => explicit proof of current lease ownership
- lease_seconds => requested or active lease duration
- renewal result payload => whether lease renewal succeeded, degraded, or failed
- phase labels and branch markers => readable lease-side visibility for operators and future readers

EN:
Accepted architectural identity:
- worker lease runtime child
- narrow lease contract layer
- readable lease-renewal boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague timing utility dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya worker-runtime ailesinin worker-lease child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü leasee özgü runtime doğrusu ana worker hubının içinde gizlenmek yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü lease sahipliği, renewal zamanlaması ve lease-failure görünürlüğü worker için merkezi kavramlardır
- çünkü yeni başlayan biri lease mantığını ilgisiz runtime fazları arasında kaybolmadan bulabilmelidir

TR:
Bu dosya NE yapar:
- worker-lease odaklı runtime yardımcı sınırlarını açığa çıkarır
- renewal, sahiplik, timeout ve degraded dal anlamını görünür tutar
- leasee özgü semantiklerini daha geniş worker orkestrasyonundan ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tüm robots mantığının sahibi değildir
- tüm acquisition mantığının sahibi değildir
- tüm parse/finalize mantığının sahibi değildir

TR:
Topolojik rol:
- ana worker runtime hubı bu dosyanın üstündedir
- bu dosya dar lease tarafı runtime semantiklerini taşır
- kardeş worker altmodülleri robots, acquisition, parse, finalize ve storage gibi diğer odaklı sözleşmeleri taşır

TR:
Önemli görünür değerler ve şekiller:
- lease token => mevcut lease sahipliğinin açık ispatı
- lease_seconds => istenen veya aktif lease süresi
- renewal result payloadı => lease renewalın başarılı, degraded veya başarısız olup olmadığı
- phase labeları ve dal işaretleri => operatörler ve gelecekteki okuyucular için okunabilir lease tarafı görünürlüğü

TR:
Kabul edilen mimari kimlik:
- worker lease runtime child
- dar lease sözleşme katmanı
- okunabilir lease-renewal sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz zamanlama utility çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module owns the explicit lease-renewal helper that the worker calls
# EN: at clear durable phase boundaries.
# TR: Bu modül worker’ın net durable aşama sınırlarında çağırdığı açık lease
# TR: yenileme yardımcısını sahiplenir.

# EN: WORKER LEASE RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow lease corner of the worker corridor.
# EN: Beginner mental model:
# EN: - the main worker runtime file is the main room
# EN: - this file is the labeled lease desk inside that larger runtime building
# EN: - it exists so lease ownership and renewal meaning do not become vague
# EN:
# EN: Accepted architectural meaning:
# EN: - named lease-runtime child
# EN: - focused renewal/ownership helper surface
# EN: - readable branch boundary for lease-side outcomes
# EN:
# EN: Undesired architectural meaning:
# EN: - random timing helper pile
# EN: - hidden second orchestrator
# EN: - place where lease failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - lease tokens should stay explicit
# EN: - renewal results should stay structured and readable
# EN: - degraded lease branches must remain visible
# TR: WORKER LEASE RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar lease köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - ana worker runtime dosyası ana odadır
# TR: - bu dosya o daha büyük runtime binası içindeki etiketli lease masasıdır
# TR: - lease sahipliği ve renewal anlamı belirsizleşmesin diye vardır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli lease-runtime child
# TR: - odaklı renewal/sahiplik yardımcı yüzeyi
# TR: - lease tarafı sonuçlar için okunabilir dal sınırı
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele zamanlama helper yığını
# TR: - gizli ikinci orchestrator
# TR: - lease hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - lease tokenları açık kalmalıdır
# TR: - renewal sonuçları yapılı ve okunabilir kalmalıdır
# TR: - degraded lease dalları görünür kalmalıdır

from __future__ import annotations

# EN: We import canonical claimed-url field access from the stable acquisition
# EN: family surface.
# TR: Kanonik claimed-url alan erişimini kararlı acquisition ailesi yüzeyinden
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    get_claimed_url_value,
)

# EN: We import the canonical DB gateway renewal wrapper because lease truth
# EN: belongs to crawler-core SQL, not to ad hoc Python state.
# TR: Lease doğrusu crawler-core SQL tarafına ait olduğu için kanonik DB gateway
# TR: renewal wrapper’ını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    renew_url_lease,
)


# EN: This helper converts lease-phase renewal drift into an operator-visible
# EN: degraded payload so the parent worker can stop cleanly instead of crashing.
# TR: Bu yardımcı lease-phase renewal drift'ini operatörün görebileceği degrade
# TR: payload'a çevirir; böylece parent worker çökmeden temiz biçimde durabilir.
# EN: WORKER LEASE FUNCTION PURPOSE MEMORY BLOCK V6 / build_lease_phase_degraded_payload
# EN:
# EN: Why this function exists:
# EN: - because worker-lease truth for 'build_lease_phase_degraded_payload' should be exposed through one named top-level helper boundary
# EN: - because lease-side runtime semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: phase_label, claimed_url, config, renew_result, error_class, error_message, degraded_reason
# EN: - values should match the current Python signature and the lease contract below
# EN:
# EN: Accepted output:
# EN: - a worker-lease-oriented result shape defined by the current function body
# EN: - this may be a structured renewal payload, a lease-status shape, or another explicit lease-side branch result
# EN:
# EN: Common lease meaning hints:
# EN: - this helper likely deals with lease ownership, renewal timing, or lease-result visibility
# EN: - explicit lease token handling and degraded renewal meaning may matter here
# EN: - these helpers often protect restart/resume safety
# EN:
# EN: Important beginner reminder:
# EN: - this function is lease-side support logic, not the whole worker corridor
# EN: - lease results must stay explicit so failure, degradation, and recovery meaning are easy to understand
# EN:
# EN: Undesired behavior:
# EN: - silent ownership mutation
# EN: - vague renewal results that hide branch meaning
# TR: WORKER LEASE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_lease_phase_degraded_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_lease_phase_degraded_payload' için worker-lease doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü lease tarafı runtime semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: phase_label, claimed_url, config, renew_result, error_class, error_message, degraded_reason
# TR: - değerler aşağıdaki mevcut Python imzası ve lease sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-lease odaklı sonuç şekli
# TR: - bu; yapılı renewal payloadı, lease-status şekli veya başka açık lease tarafı dal sonucu olabilir
# TR:
# TR: Ortak lease anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease sahipliği, renewal zamanlaması veya lease-sonucu görünürlüğü ile ilgilenir
# TR: - açık lease token işleme ve degraded renewal anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman restart/resume güvenliğini korur
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon lease tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - lease sonuçları açık kalmalıdır ki başarısızlık, degraded durum ve recovery anlamı kolay anlaşılsın
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz sahiplik değişimi
# TR: - dal anlamını gizleyen belirsiz renewal sonuçları

# EN: WORKER LEASE RUNTIME DENSITY LIFT MEMORY BLOCK V7
# EN:
# EN: Why one more density block is justified here:
# EN: - lease code looks smaller than the full worker hub, but lease mistakes can break restart, resume, and ownership safety
# EN: - therefore this file needs extra explanation density even when the code surface looks compact
# EN: - the goal is that a beginner can understand why lease renewal is its own child surface
# EN:
# EN: For-dummies mental picture:
# EN: - imagine the worker as a courier temporarily holding a delivery token
# EN: - this file explains how that token is kept alive, checked, renewed, or visibly lost
# EN: - if that token logic becomes vague, the whole crawler can forget who currently owns work
# EN:
# EN: Accepted reading model:
# EN: - expect focused lease ownership helpers here
# EN: - expect renewal and degraded branches to stay explicit
# EN: - expect readable contract meaning rather than clever compactness
# EN:
# EN: Undesired reading model:
# EN: - treating lease logic as just a tiny timing detail
# EN: - assuming lease helpers need less contract clarity than fetch or parse helpers
# TR: WORKER LEASE RUNTIME YOĞUNLUK TAKVİYE HAFIZA BLOĞU V7
# TR:
# TR: Burada bir ek yoğunluk bloğu neden haklıdır:
# TR: - lease kodu tam worker hubından küçük görünür, ama lease hataları restart, resume ve sahiplik güvenliğini bozabilir
# TR: - bu yüzden kod yüzeyi kompakt görünse bile bu dosya ek açıklama yoğunluğu ister
# TR: - amaç yeni başlayan birinin lease renewalın neden ayrı child yüzey olduğunu anlayabilmesidir
# TR:
# TR: For-dummies zihinsel resmi:
# TR: - workerı geçici teslimat tokenı taşıyan bir kurye gibi düşün
# TR: - bu dosya o tokenın nasıl canlı tutulduğunu, kontrol edildiğini, yenilendiğini veya görünür biçimde kaybedildiğini açıklar
# TR: - o token mantığı belirsizleşirse tüm crawler şu anda işin kimde olduğunu unutabilir
# TR:
# TR: Kabul edilen okuma modeli:
# TR: - burada odaklı lease sahipliği yardımcıları bekle
# TR: - renewal ve degraded dallarının açık kalmasını bekle
# TR: - akıllı kısalık yerine okunabilir sözleşme anlamı bekle
# TR:
# TR: İstenmeyen okuma modeli:
# TR: - lease mantığını sadece küçük zamanlama detayı sanmak
# TR: - lease yardımcılarının fetch veya parse yardımcılarından daha az sözleşme açıklığı istediğini sanmak

# EN: WORKER LEASE FUNCTION REINFORCEMENT BLOCK V7 / build_lease_phase_degraded_payload
# EN:
# EN: Extra clarity layer:
# EN: - lease helpers may look small but they carry ownership safety meaning
# EN: - that is why this function gets one more explicit reminder block
# EN:
# EN: Input reminder:
# EN: - current explicit parameters: phase_label, claimed_url, config, renew_result, error_class, error_message, degraded_reason
# EN: - callers should pass values that keep lease ownership and branch meaning explicit
# EN:
# EN: Output reminder:
# EN: - results should stay structured and readable
# EN: - degraded, expired, failed, or renewed branches should remain visible
# EN:
# EN: Common lease meaning hints:
# EN: - this helper likely deals with lease ownership, renewal timing, or lease-result visibility
# EN: - explicit lease token handling and degraded renewal meaning may matter here
# EN: - these helpers often protect restart/resume safety
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Beginner warning:
# EN: - lease helpers are exactly where silent mistakes can make the crawler think it still owns work when it does not
# EN: - this block exists to resist that kind of ambiguity
# TR: WORKER LEASE FUNCTION PEKİŞTİRME BLOĞU V7 / build_lease_phase_degraded_payload
# TR:
# TR: Ek açıklık katmanı:
# TR: - lease yardımcıları küçük görünebilir ama sahiplik güvenliği anlamı taşır
# TR: - bu yüzden bu fonksiyon bir ek açık hatırlatma bloğu alır
# TR:
# TR: Girdi hatırlatması:
# TR: - mevcut açık parametreler: phase_label, claimed_url, config, renew_result, error_class, error_message, degraded_reason
# TR: - çağıranlar lease sahipliğini ve dal anlamını açık tutan değerler geçmelidir
# TR:
# TR: Çıktı hatırlatması:
# TR: - sonuçlar yapılı ve okunabilir kalmalıdır
# TR: - degraded, expired, failed veya renewed dalları görünür kalmalıdır
# TR:
# TR: Ortak lease anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease sahipliği, renewal zamanlaması veya lease-sonucu görünürlüğü ile ilgilenir
# TR: - açık lease token işleme ve degraded renewal anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman restart/resume güvenliğini korur
# TR: - görünür başarı vs başarısızlık ayrımı burada özellikle önemlidir
# TR:
# TR: Başlangıç seviyesi uyarı:
# TR: - lease yardımcıları tam da sessiz hataların crawlerın hâlâ işe sahip olduğunu sanmasına yol açabildiği yerdir
# TR: - bu blok o tür belirsizliğe direnmek için vardır

# EN: This function builds the explicit degraded lease-phase payload instead of hiding renewal trouble.
# EN: `phase_label` names the durable worker phase that was being protected by lease handling.
# EN: `claimed_url` carries the currently claimed work item whose lease context is being described.
# EN: `config` carries lease-runtime configuration values used while shaping the degraded result.
# EN: `renew_result` carries any partial renewal result already produced before degradation handling.
# EN: `error_class` records the failure class or exception type for operator-readable diagnostics.
# EN: `error_message` records the human-readable failure text that explains the degraded branch.
# EN: `degraded_reason` records the normalized machine-friendly degraded reason returned downstream.
# TR: Bu fonksiyon lease yenileme sorununu gizlemek yerine açık degraded lease-phase payload'ını kurar.
# TR: `phase_label` lease yönetimiyle korunmaya çalışılan durable worker fazını adlandırır.
# TR: `claimed_url` lease bağlamı anlatılan şu anda claim edilmiş iş öğesini taşır.
# TR: `config` degraded sonucu şekillendirirken kullanılan lease-runtime yapılandırma değerlerini taşır.
# TR: `renew_result` degraded işlenmeden önce üretilmiş olabilecek kısmi renewal sonucunu taşır.
# TR: `error_class` operatör-okunur tanı için hata sınıfını veya exception tipini kaydeder.
# TR: `error_message` degraded dalı açıklayan insan-okunur hata metnini kaydeder.
# TR: `degraded_reason` aşağı akışa dönen normalize makine-okunur degraded nedenini kaydeder.
def build_lease_phase_degraded_payload(
    *,
    phase_label: str,
    claimed_url: object,
    config: object,
    renew_result: dict[str, object] | None,
    error_class: str,
    error_message: str,
    degraded_reason: str,
) -> dict[str, object]:
    # EN: We keep one normalized degraded payload shape across durable phase
    # EN: boundaries so operator-visible lease truth stays explicit and consistent.
    # TR: Operatörün gördüğü lease doğrusu açık ve tutarlı kalsın diye durable
    # TR: phase sınırlarında tek ve normalize bir degrade payload şekli tutuyoruz.
    return {
        "url_id": int(get_claimed_url_value(claimed_url, "url_id")),
        "lease_token": str(get_claimed_url_value(claimed_url, "lease_token")),
        "worker_id": str(getattr(config, "worker_id")),
        "extend_seconds": int(getattr(config, "lease_seconds")),
        "phase_label": phase_label,
        "renewed": None if renew_result is None else renew_result.get("renewed"),
        "new_lease_expires_at": (
            None if renew_result is None else renew_result.get("new_lease_expires_at")
        ),
        "gateway_lease_degraded_reason": (
            None if renew_result is None else renew_result.get("lease_degraded_reason")
        ),
        "lease_degraded": True,
        "lease_degraded_reason": degraded_reason,
        "lease_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }


# EN: This helper renews the currently owned lease right before the worker enters
# EN: a durable phase that may take non-trivial time.
# TR: Bu yardımcı worker kayda değer süre alabilecek bir durable aşamaya girmeden
# TR: hemen önce mevcut lease’i yeniler.
# EN: WORKER LEASE FUNCTION PURPOSE MEMORY BLOCK V6 / renew_claimed_lease_before_durable_phase
# EN:
# EN: Why this function exists:
# EN: - because worker-lease truth for 'renew_claimed_lease_before_durable_phase' should be exposed through one named top-level helper boundary
# EN: - because lease-side runtime semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, config, phase_label
# EN: - values should match the current Python signature and the lease contract below
# EN:
# EN: Accepted output:
# EN: - a worker-lease-oriented result shape defined by the current function body
# EN: - this may be a structured renewal payload, a lease-status shape, or another explicit lease-side branch result
# EN:
# EN: Common lease meaning hints:
# EN: - this helper likely deals with lease ownership, renewal timing, or lease-result visibility
# EN: - explicit lease token handling and degraded renewal meaning may matter here
# EN: - these helpers often protect restart/resume safety
# EN:
# EN: Important beginner reminder:
# EN: - this function is lease-side support logic, not the whole worker corridor
# EN: - lease results must stay explicit so failure, degradation, and recovery meaning are easy to understand
# EN:
# EN: Undesired behavior:
# EN: - silent ownership mutation
# EN: - vague renewal results that hide branch meaning
# TR: WORKER LEASE FUNCTION AMAÇ HAFIZA BLOĞU V6 / renew_claimed_lease_before_durable_phase
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'renew_claimed_lease_before_durable_phase' için worker-lease doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü lease tarafı runtime semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, config, phase_label
# TR: - değerler aşağıdaki mevcut Python imzası ve lease sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-lease odaklı sonuç şekli
# TR: - bu; yapılı renewal payloadı, lease-status şekli veya başka açık lease tarafı dal sonucu olabilir
# TR:
# TR: Ortak lease anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease sahipliği, renewal zamanlaması veya lease-sonucu görünürlüğü ile ilgilenir
# TR: - açık lease token işleme ve degraded renewal anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman restart/resume güvenliğini korur
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon lease tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - lease sonuçları açık kalmalıdır ki başarısızlık, degraded durum ve recovery anlamı kolay anlaşılsın
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz sahiplik değişimi
# TR: - dal anlamını gizleyen belirsiz renewal sonuçları

# EN: WORKER LEASE FUNCTION REINFORCEMENT BLOCK V7 / renew_claimed_lease_before_durable_phase
# EN:
# EN: Extra clarity layer:
# EN: - lease helpers may look small but they carry ownership safety meaning
# EN: - that is why this function gets one more explicit reminder block
# EN:
# EN: Input reminder:
# EN: - current explicit parameters: conn, claimed_url, config, phase_label
# EN: - callers should pass values that keep lease ownership and branch meaning explicit
# EN:
# EN: Output reminder:
# EN: - results should stay structured and readable
# EN: - degraded, expired, failed, or renewed branches should remain visible
# EN:
# EN: Common lease meaning hints:
# EN: - this helper likely deals with lease ownership, renewal timing, or lease-result visibility
# EN: - explicit lease token handling and degraded renewal meaning may matter here
# EN: - these helpers often protect restart/resume safety
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Beginner warning:
# EN: - lease helpers are exactly where silent mistakes can make the crawler think it still owns work when it does not
# EN: - this block exists to resist that kind of ambiguity
# TR: WORKER LEASE FUNCTION PEKİŞTİRME BLOĞU V7 / renew_claimed_lease_before_durable_phase
# TR:
# TR: Ek açıklık katmanı:
# TR: - lease yardımcıları küçük görünebilir ama sahiplik güvenliği anlamı taşır
# TR: - bu yüzden bu fonksiyon bir ek açık hatırlatma bloğu alır
# TR:
# TR: Girdi hatırlatması:
# TR: - mevcut açık parametreler: conn, claimed_url, config, phase_label
# TR: - çağıranlar lease sahipliğini ve dal anlamını açık tutan değerler geçmelidir
# TR:
# TR: Çıktı hatırlatması:
# TR: - sonuçlar yapılı ve okunabilir kalmalıdır
# TR: - degraded, expired, failed veya renewed dalları görünür kalmalıdır
# TR:
# TR: Ortak lease anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease sahipliği, renewal zamanlaması veya lease-sonucu görünürlüğü ile ilgilenir
# TR: - açık lease token işleme ve degraded renewal anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman restart/resume güvenliğini korur
# TR: - görünür başarı vs başarısızlık ayrımı burada özellikle önemlidir
# TR:
# TR: Başlangıç seviyesi uyarı:
# TR: - lease yardımcıları tam da sessiz hataların crawlerın hâlâ işe sahip olduğunu sanmasına yol açabildiği yerdir
# TR: - bu blok o tür belirsizliğe direnmek için vardır

# EN: This function attempts lease renewal before a durable worker phase so ownership does not silently expire.
# EN: `conn` is the live database connection used to call the lease-renewal boundary.
# EN: `claimed_url` is the claimed work item whose current lease token and identifiers must remain valid.
# EN: `config` provides lease-related runtime settings such as renewal timing or duration defaults.
# EN: `phase_label` names which durable phase is about to run so logs and degraded payloads stay readable.
# TR: Bu fonksiyon sahiplik sessizce sona ermesin diye durable worker fazından önce lease renewal dener.
# TR: `conn` lease-renewal sınırını çağırmak için kullanılan canlı veritabanı bağlantısıdır.
# TR: `claimed_url` mevcut lease tokenı ve kimlikleri geçerli kalması gereken claim edilmiş iş öğesidir.
# TR: `config` renewal zamanlaması veya süre varsayılanları gibi lease ile ilgili runtime ayarlarını sağlar.
# TR: `phase_label` hangi durable fazın başlamak üzere olduğunu adlandırır; böylece loglar ve degraded payload'lar okunabilir kalır.
def renew_claimed_lease_before_durable_phase(
    conn,
    *,
    claimed_url: object,
    config: object,
    phase_label: str,
) -> dict[str, object]:
    # EN: We call the canonical DB wrapper using the currently owned lease
    # EN: identity plus the worker/config contract values.
    # TR: Kanonik DB wrapper’ını mevcut lease kimliği ve worker/config sözleşme
    # TR: değerleri ile çağırıyoruz.
# EN: `renew_result` stores the raw lease-renewal answer before success/degraded interpretation happens.
# TR: `renew_result` başarı/degraded yorumlaması yapılmadan önce ham lease-renewal cevabını tutar.
    renew_result = renew_url_lease(
        conn=conn,
        url_id=int(get_claimed_url_value(claimed_url, "url_id")),
        lease_token=str(get_claimed_url_value(claimed_url, "lease_token")),
        worker_id=str(getattr(config, "worker_id")),
        extend_seconds=int(getattr(config, "lease_seconds")),
    )

    # EN: Missing output or a gateway-level degraded payload means renewal truth
    # EN: could not be confirmed for this durable phase boundary.
    # TR: Çıktı eksikse veya gateway-seviyesi degrade payload geldiyse bu durable
    # TR: phase sınırında renewal doğrusu teyit edilememiş demektir.
    if renew_result is None or bool(renew_result.get("lease_degraded")):
        return build_lease_phase_degraded_payload(
            phase_label=phase_label,
            claimed_url=claimed_url,
            config=config,
            renew_result=renew_result,
            error_class="lease_renewal_no_row_before_durable_phase",
            error_message=f"renew_url_lease(...) returned no row before durable phase: {phase_label}",
            degraded_reason="renew_url_lease_returned_no_row_before_durable_phase",
        )

    # EN: The canonical SQL surface returns renewed=true on success, so we verify
    # EN: that explicit signal instead of assuming success silently.
    # TR: Kanonik SQL yüzeyi başarıda renewed=true döndürdüğü için başarıyı sessizce
    # TR: varsaymak yerine bu açık sinyali doğruluyoruz.
    if renew_result.get("renewed") is not True:
        return build_lease_phase_degraded_payload(
            phase_label=phase_label,
            claimed_url=claimed_url,
            config=config,
            renew_result=renew_result,
            error_class="lease_renewal_not_confirmed_before_durable_phase",
            error_message=f"renew_url_lease(...) did not confirm renewal before durable phase: {phase_label}",
            degraded_reason="renew_url_lease_not_confirmed_before_durable_phase",
        )

    # EN: We refresh the in-memory lease expiry view so later phases see the
    # EN: newest DB-backed lease horizon.
    # TR: Sonraki aşamalar en güncel DB-backed lease ufkunu görsün diye bellek içi
    # TR: lease expiry görünümünü yeniliyoruz.
    if isinstance(claimed_url, dict):
        claimed_url["lease_expires_at"] = renew_result["new_lease_expires_at"]
    elif hasattr(claimed_url, "lease_expires_at"):
        setattr(claimed_url, "lease_expires_at", renew_result["new_lease_expires_at"])

    # EN: We return the explicit renewal payload for later inspection when needed.
    # TR: Gerekirse daha sonra incelenebilsin diye açık renewal payload’ını
    # TR: döndürüyoruz.
    return renew_result


# EN: This explicit export list documents the public lease child surface.
# TR: Bu açık export listesi public lease alt yüzeyini belgelendirir.
__all__ = [
    "renew_claimed_lease_before_durable_phase",
]
