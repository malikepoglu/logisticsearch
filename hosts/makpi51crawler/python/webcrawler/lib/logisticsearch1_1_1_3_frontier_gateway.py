"""
EN:
This file is the frontier child of the state DB gateway family.

EN:
Why this file exists:
- because frontier-specific DB truth should be exposed through one named gateway child
- because upper layers should read named Python helper boundaries instead of repeating raw frontier SQL semantics
- because claim, lease, release, and frontier-row visibility are core runtime ideas and should stay legible

EN:
What this file DOES:
- expose frontier-specific DB helper boundaries
- expose claim / lease / release style DB-truth helpers
- preserve readable frontier contract boundaries for upper runtime layers

EN:
What this file DOES NOT do:
- it does not own shared DB connection helpers
- it does not own runtime-control truth
- it does not parse HTML
- it does not classify taxonomy
- it does not act as an operator CLI surface

EN:
Topological role:
- gateway_support sits below this file for shared DB support
- this file sits in the middle for frontier-specific DB truth
- worker/controller layers above call these helpers instead of embedding raw frontier SQL ideas

EN:
Important visible values and shapes:
- conn => live DB connection object
- worker_id => claim identity text
- lease_seconds => requested lease duration
- lease_token => lease ownership proof text
- claimed_url or claim-result payload => one claimed work item or no-claim branch visibility
- frontier row identifiers => row-level DB truth
- no-work / no-claim branches => visible non-success branches that should not be hidden

EN:
Accepted architectural identity:
- frontier truth gateway
- claim/lease/release DB-adjacent helper layer
- readable frontier contract boundary

EN:
Undesired architectural identity:
- hidden crawler controller
- hidden fetch engine
- hidden parse engine
- hidden ranking engine

TR:
Bu dosya state DB gateway ailesinin frontier child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü frontier’e özgü DB doğrusu tek ve isimli bir gateway child yüzeyi üzerinden açığa çıkmalıdır
- çünkü üst katmanlar frontier SQL semantiğini her yere gömmek yerine isimli Python yardımcı sınırlarını okumalıdır
- çünkü claim, lease, release ve frontier satırı görünürlüğü temel runtime fikirleridir ve okunabilir kalmalıdır

TR:
Bu dosya NE yapar:
- frontier’e özgü DB yardımcı sınırlarını açığa çıkarır
- claim / lease / release tarzı DB-truth yardımcıları sunar
- üst runtime katmanları için okunabilir frontier sözleşme sınırlarını korur

TR:
Bu dosya NE yapmaz:
- ortak DB bağlantı yardımcılarının sahibi değildir
- runtime-control doğrusunun sahibi değildir
- HTML parse etmez
- taxonomy sınıflandırması yapmaz
- operatör CLI yüzeyi gibi davranmaz

TR:
Topolojik rol:
- ortak DB desteği için gateway_support bu dosyanın altındadır
- frontier’e özgü DB doğrusu için bu dosya ortadadır
- üstteki worker/controller katmanları ham frontier SQL fikrini gömmek yerine bu yardımcıları çağırır

TR:
Önemli görünür değerler ve şekiller:
- conn => canlı DB bağlantı nesnesi
- worker_id => claim kimlik metni
- lease_seconds => istenen lease süresi
- lease_token => lease sahiplik ispatı metni
- claimed_url veya claim-result payload => tek claim edilmiş iş öğesi ya da no-claim dal görünürlüğü
- frontier satır kimlikleri => satır-düzeyi DB doğrusu
- no-work / no-claim dalları => gizlenmemesi gereken görünür başarısız-olmayan dallar

TR:
Kabul edilen mimari kimlik:
- frontier truth gateway
- claim/lease/release DB-yanı yardımcı katmanı
- okunabilir frontier sözleşme sınırı

TR:
İstenmeyen mimari kimlik:
- gizli crawler controller
- gizli fetch motoru
- gizli parse motoru
- gizli ranking motoru
"""

# EN: This module is the frontier child of the state DB gateway family.
# EN: It owns only frontier claim, lease, success, retryable, permanent, and
# EN: release DB wrappers.
# TR: Bu modül state DB gateway ailesinin frontier alt yüzeyidir.
# TR: Yalnızca frontier claim, lease, success, retryable, permanent ve release
# TR: DB wrapper'larını taşır.

from __future__ import annotations

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
from typing import Any

# EN: We import psycopg because these functions are thin wrappers around SQL calls.
# TR: Bu fonksiyonlar SQL çağrılarının ince wrapper'ları olduğu için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
from psycopg.rows import dict_row

# EN: We import the shared ClaimedUrl shape and row-mapping helper from the
# EN: gateway-support child so frontier wrappers keep one canonical row contract.
# TR: Frontier wrapper'ları tek bir kanonik satır sözleşmesi kullansın diye
# TR: paylaşılan ClaimedUrl şeklini ve satır-eşleme yardımcısını gateway-support
# TR: alt yüzeyinden içe aktarıyoruz.
from .logisticsearch1_1_1_1_gateway_support import ClaimedUrl, _row_to_claimed_url




# EN: This function calls the canonical crawler-core claim entry point.
# TR: Bu fonksiyon, kanonik crawler-core claim giriş noktasını çağırır.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / claim_next_url
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'claim_next_url' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, worker_id, lease_seconds
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper likely participates in claimable-row selection or claimed work visibility
# EN: - worker identity, lease ownership, or no-claim branch visibility may matter here
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / claim_next_url
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'claim_next_url' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, worker_id, lease_seconds
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle claim edilebilir satır seçimi veya claim edilmiş iş görünürlüğüne katılır
# TR: - worker kimliği, lease sahipliği veya no-claim dal görünürlüğü burada önemli olabilir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / claim_next_url
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
# EN: - worker_id => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
# EN: - lease_seconds => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / claim_next_url
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - worker_id => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_seconds => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def claim_next_url(
    conn: psycopg.Connection,
    worker_id: str,
    lease_seconds: int,
) -> ClaimedUrl | None:
    # EN: We open a cursor from the existing connection so we can execute SQL
    # EN: statements inside the caller-controlled transaction scope.
    # TR: SQL ifadelerini çağıran tarafın kontrol ettiği transaction kapsamı
    # TR: içinde çalıştırabilmek için mevcut bağlantıdan bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We execute the canonical function instead of re-implementing
        # EN: scheduling rules in Python because the repository docs say the DB
        # EN: is the durable truth of claimability.
        # TR: Repository dokümanları claim edilebilirlik doğrusunun veritabanında
        # TR: olduğunu söylediği için zamanlama kurallarını Python'da yeniden yazmak
        # TR: yerine kanonik fonksiyonu çalıştırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM frontier.claim_next_url(
                p_worker_id => %(worker_id)s,
                p_lease_duration => make_interval(secs => %(lease_seconds)s)
            )
            """,
            {
                "worker_id": worker_id,
                "lease_seconds": lease_seconds,
            },
        )

        # EN: We fetch at most one row because crawler-core claim_next_url(...)
        # EN: is already designed to claim exactly one eligible URL.
        # TR: En fazla bir satır çekiyoruz; çünkü crawler-core claim_next_url(...)
        # TR: zaten tam olarak bir uygun URL claim edecek şekilde tasarlanmıştır.
        row = cur.fetchone()

    # EN: If no row exists, the worker currently has no claimable work.
    # TR: Hiç satır yoksa worker'ın şu anda claim edebileceği iş yok demektir.
    if row is None:
        # EN: We return None to make the no-work state explicit in Python.
        # TR: Python tarafında iş-yok durumunu açık hale getirmek için None döndürüyoruz.
        return None

    # EN: If a row exists, we convert it into our strongly-shaped Python object.
    # TR: Satır varsa onu şekli net Python nesnemize dönüştürüyoruz.
    return _row_to_claimed_url(row)



# EN: This helper converts a lease-renewal SQL wrapper no-row condition into an
# EN: operator-visible degraded payload so upper runtime layers can keep moving
# EN: with honest unresolved lease state instead of crashing again.
# TR: Bu yardımcı lease-renewal SQL wrapper no-row durumunu operatörün
# TR: görebileceği degrade payload'a çevirir; böylece üst runtime katmanları
# TR: yeniden çökmeden dürüst çözülmemiş lease durumu ile ilerleyebilir.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / build_lease_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'build_lease_no_row_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: action, url_id, lease_token, worker_id, extend_seconds, renewed, new_lease_expires_at, error_class, error_message
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper likely deals with lease duration, renewal, or lease ownership truth
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / build_lease_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'build_lease_no_row_payload' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: action, url_id, lease_token, worker_id, extend_seconds, renewed, new_lease_expires_at, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease süresi, yenileme veya lease sahiplik doğrusu ile ilgilidir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / build_lease_no_row_payload
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - action => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - worker_id => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - extend_seconds => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - renewed => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - new_lease_expires_at => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - error_class => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - error_message => explicit frontier-gateway input parameter of build_lease_no_row_payload; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_lease_no_row_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - action => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - worker_id => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - extend_seconds => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - renewed => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - new_lease_expires_at => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_class => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_message => build_lease_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def build_lease_no_row_payload(
    *,
    action: str,
    url_id: int,
    lease_token: str,
    worker_id: str,
    extend_seconds: int,
    renewed: bool | None = None,
    new_lease_expires_at: object | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, Any]:
    # EN: We keep one normalized degraded payload shape across lease-renewal
    # EN: wrappers so caller-visible results stay explicit and consistent.
    # TR: Lease-renewal wrapper'ları arasında tek ve normalize bir degrade payload
    # TR: şekli tutuyoruz; böylece çağıranın gördüğü sonuç açık ve tutarlı kalır.
    return {
        "url_id": url_id,
        "lease_token": lease_token,
        "worker_id": worker_id,
        "extend_seconds": extend_seconds,
        "renewed": renewed,
        "new_lease_expires_at": new_lease_expires_at,
        "lease_action": action,
        "lease_degraded": True,
        "lease_degraded_reason": f"{action}_returned_no_row",
        "lease_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }


# EN: This function tries to renew an already-owned lease.
# TR: Bu fonksiyon, halihazırda sahip olunan bir lease'i yenilemeyi dener.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / renew_url_lease
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'renew_url_lease' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, lease_token, worker_id, extend_seconds
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper likely deals with lease duration, renewal, or lease ownership truth
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / renew_url_lease
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'renew_url_lease' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, lease_token, worker_id, extend_seconds
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle lease süresi, yenileme veya lease sahiplik doğrusu ile ilgilidir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / renew_url_lease
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of renew_url_lease; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of renew_url_lease; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of renew_url_lease; this value is part of the visible DB-helper contract of this function
# EN: - worker_id => explicit frontier-gateway input parameter of renew_url_lease; this value is part of the visible DB-helper contract of this function
# EN: - extend_seconds => explicit frontier-gateway input parameter of renew_url_lease; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / renew_url_lease
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => renew_url_lease fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => renew_url_lease fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => renew_url_lease fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - worker_id => renew_url_lease fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - extend_seconds => renew_url_lease fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def renew_url_lease(
    conn: psycopg.Connection,
    url_id: int,
    lease_token: str,
    worker_id: str,
    extend_seconds: int,
) -> dict[str, Any] | None:
    # EN: We again use the existing connection because transaction ownership
    # EN: should stay under the caller/runtime layer.
    # TR: Yine mevcut bağlantıyı kullanıyoruz; çünkü transaction sahipliği
    # TR: çağıran taraf/runtime katmanı altında kalmalıdır.
    with conn.cursor() as cur:
        # EN: We call the canonical renewal function exactly as the docs require.
        # TR: Dokümanların gerektirdiği şekilde kanonik renewal fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM frontier.renew_url_lease(
                p_url_id => %(url_id)s,
                p_lease_token => %(lease_token)s::uuid,
                p_worker_id => %(worker_id)s,
                p_extend_by => make_interval(secs => %(extend_seconds)s)
            )
            """,
            {
                "url_id": url_id,
                "lease_token": lease_token,
                "worker_id": worker_id,
                "extend_seconds": extend_seconds,
            },
        )

        # EN: We fetch one row because a successful renewal should validate one
        # EN: currently-owned lease, not many.
        # TR: Tek satır çekiyoruz; çünkü başarılı bir renewal, birden fazla değil,
        # TR: mevcut sahip olunan tek bir lease'i doğrulamalıdır.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of crashing the worker-side lease path again.
    # TR: No-row yanıtı worker-tarafı lease yolunu yeniden çökertmek yerine
    # TR: operatörün görebileceği degrade payload'a dönmelidir.
    if row is None:
        return build_lease_no_row_payload(
            action="frontier_renew_url_lease",
            url_id=url_id,
            lease_token=lease_token,
            worker_id=worker_id,
            extend_seconds=extend_seconds,
            error_class="lease_renewal_no_row",
            error_message="frontier.renew_url_lease(...) returned no row",
        )

    # EN: We return the row directly for now because the renewal surface may grow
    # EN: before we lock its final Python representation.
    # TR: Şimdilik satırı doğrudan döndürüyoruz; çünkü renewal yüzeyi nihai Python
    # TR: temsili kilitlenmeden önce büyüyebilir.
    return row



# EN: This helper converts a frontier SQL wrapper no-row condition into an
# EN: operator-visible degraded payload so upper runtime layers can keep moving
# EN: with honest unresolved state instead of crashing again.
# TR: Bu yardımcı frontier SQL wrapper no-row durumunu operatörün görebileceği
# TR: degrade payload’a çevirir; böylece üst runtime katmanları yeniden çökmeden
# TR: dürüst çözülmemiş durumla ilerleyebilir.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / build_frontier_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'build_frontier_no_row_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: action, url_id, lease_token, http_status, content_type, body_bytes, etag, last_modified, error_class, error_message, retry_delay
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper exposes one named frontier-specific DB-truth boundary
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / build_frontier_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'build_frontier_no_row_payload' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: action, url_id, lease_token, http_status, content_type, body_bytes, etag, last_modified, error_class, error_message, retry_delay
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı frontier’e özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / build_frontier_no_row_payload
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - action => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - http_status => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - content_type => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - body_bytes => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - etag => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - last_modified => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - error_class => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - error_message => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# EN: - retry_delay => explicit frontier-gateway input parameter of build_frontier_no_row_payload; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_frontier_no_row_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - action => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - http_status => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - content_type => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - body_bytes => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - etag => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - last_modified => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_class => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_message => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - retry_delay => build_frontier_no_row_payload fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def build_frontier_no_row_payload(
    *,
    action: str,
    url_id: int,
    lease_token: str | None = None,
    http_status: int | None = None,
    content_type: str | None = None,
    body_bytes: int | None = None,
    etag: str | None = None,
    last_modified: str | None = None,
    error_class: str | None = None,
    error_message: str | None = None,
    retry_delay: str | None = None,
) -> dict[str, object]:
    # EN: We keep one normalized degraded payload shape across frontier wrappers.
    # TR: Frontier wrapper'ları arasında tek ve normalize bir degrade payload
    # TR: şekli tutuyoruz.
    return {
        "url_id": url_id,
        "lease_token": lease_token,
        "http_status": http_status,
        "content_type": content_type,
        "body_bytes": body_bytes,
        "etag": etag,
        "last_modified": last_modified,
        "error_class": error_class,
        "error_message": error_message,
        "retry_delay": retry_delay,
        "frontier_action": action,
        "frontier_degraded": True,
        "frontier_degraded_reason": f"{action}_returned_no_row",
        "frontier_completed": False,
    }


# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / finish_fetch_success
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'finish_fetch_success' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, lease_token, http_status, content_type, body_bytes, etag, last_modified
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper exposes one named frontier-specific DB-truth boundary
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / finish_fetch_success
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'finish_fetch_success' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, lease_token, http_status, content_type, body_bytes, etag, last_modified
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı frontier’e özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / finish_fetch_success
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - http_status => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - content_type => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - body_bytes => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - etag => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# EN: - last_modified => explicit frontier-gateway input parameter of finish_fetch_success; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / finish_fetch_success
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - http_status => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - content_type => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - body_bytes => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - etag => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - last_modified => finish_fetch_success fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def finish_fetch_success(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int,
    content_type: str | None,
    body_bytes: int,
    etag: str | None = None,
    last_modified: str | None = None,
) -> dict:
    # EN: We open a cursor because the finalize SQL function is executed as one
    # EN: explicit database statement inside the current transaction.
    # TR: Finalize SQL fonksiyonu mevcut transaction içinde tek bir açık veritabanı
    # TR: ifadesi olarak çalıştırıldığı için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core success finalize function and
        # EN: pass the leased URL identity plus visible fetch metadata.
        # TR: Kanonik crawler-core success finalize fonksiyonunu çağırıyor ve
        # TR: leased URL kimliğini görünür fetch metadata'sı ile birlikte iletiyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_success(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_content_type => %s,
                p_body_bytes => %s,
                p_etag => %s,
                p_last_modified => %s
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                content_type,
                body_bytes,
                etag,
                last_modified,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        return build_frontier_no_row_payload(
            action="frontier_finish_fetch_success",
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            content_type=content_type,
            body_bytes=body_bytes,
            etag=etag,
            last_modified=last_modified,
            error_class="success_finalize_no_row",
            error_message="frontier.finish_fetch_success(...) returned no row",
        )

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row



# EN: This helper finalizes a retryable fetch failure for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için retryable fetch hatasını finalize eder.

# EN: This helper calls frontier.release_parse_pending_to_queued(...) so Python can
# EN: move a success-finalized frontier row out of transient parse_pending and back
# EN: into the normal revisit queue without changing its already-computed next_fetch_at.
# TR: Bu yardımcı frontier.release_parse_pending_to_queued(...) çağrısını yapar;
# TR: böylece Python success-finalize edilmiş frontier satırını geçici parse_pending
# TR: durumundan, önceden hesaplanmış next_fetch_at değerini bozmadan normal revisit
# TR: kuyruğuna geri taşıyabilir.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / release_parse_pending_to_queued
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'release_parse_pending_to_queued' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper likely participates in releasing a claimed row or closing a claim corridor
# EN: - lease token and ownership truth may matter here
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / release_parse_pending_to_queued
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'release_parse_pending_to_queued' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle claim edilmiş satırı bırakma veya claim koridorunu kapatma işine katılır
# TR: - lease token ve sahiplik doğrusu burada önemli olabilir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / release_parse_pending_to_queued
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of release_parse_pending_to_queued; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of release_parse_pending_to_queued; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / release_parse_pending_to_queued
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => release_parse_pending_to_queued fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => release_parse_pending_to_queued fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def release_parse_pending_to_queued(
    conn: psycopg.Connection,
    *,
    url_id: int,
) -> dict[str, Any]:
    # EN: We open one isolated cursor because this helper performs one explicit
    # EN: crawler-core state transition call.
    # TR: Bu yardımcı tek bir açık crawler-core durum geçiş çağrısı yaptığı için
    # TR: izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core function instead of issuing an ad hoc
        # EN: update so Python stays aligned with the sealed SQL contract.
        # TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye özel bir
        # TR: update yazmak yerine kanonik crawler-core fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.release_parse_pending_to_queued(
                p_url_id => %(url_id)s
            )
            """,
            {
                "url_id": url_id,
            },
        )

        # EN: We fetch exactly one row because one call should release at most one
        # EN: frontier row.
        # TR: Tek çağrı en fazla bir frontier satırını serbest bırakması gerektiği
        # TR: için tam bir satır çekiyoruz.
        row = cur.fetchone()

    # EN: Missing output is a structural failure because the canonical crawler-core
    # EN: release function should always report the current persisted state.
    # TR: Çıktı yoksa bu yapısal hatadır; çünkü kanonik crawler-core release
    # TR: fonksiyonu mevcut persist edilmiş durumu her zaman raporlamalıdır.
    if row is None:
        return build_frontier_no_row_payload(
            action="frontier_release_parse_pending_to_queued",
            url_id=url_id,
            error_class="release_parse_pending_no_row",
            error_message="frontier.release_parse_pending_to_queued(...) returned no row",
        )

    # EN: We return the raw mapping because it is already beginner-readable.
    # TR: Ham mapping'i döndürüyoruz; çünkü zaten beginner-okunur yapıdadır.
    return row



# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / finish_fetch_retryable_error
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'finish_fetch_retryable_error' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, lease_token, http_status, error_class, error_message, retry_delay
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper exposes one named frontier-specific DB-truth boundary
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / finish_fetch_retryable_error
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'finish_fetch_retryable_error' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, lease_token, http_status, error_class, error_message, retry_delay
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı frontier’e özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / finish_fetch_retryable_error
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - http_status => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - error_class => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - error_message => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# EN: - retry_delay => explicit frontier-gateway input parameter of finish_fetch_retryable_error; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / finish_fetch_retryable_error
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - http_status => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_class => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_message => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - retry_delay => finish_fetch_retryable_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def finish_fetch_retryable_error(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int | None,
    error_class: str,
    error_message: str | None,
    retry_delay: str | None = None,
) -> dict:
    # EN: We open a cursor because the retryable finalize SQL function must run
    # EN: inside the current controlled transaction.
    # TR: Retryable finalize SQL fonksiyonu mevcut kontrollü transaction içinde
    # TR: çalışmak zorunda olduğu için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core retryable-error finalize function.
        # TR: Kanonik crawler-core retryable-error finalize fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_retryable_error(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_error_class => %s,
                p_error_message => %s,
                p_retry_delay => %s::interval
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                error_class,
                error_message,
                retry_delay,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        return build_frontier_no_row_payload(
            action="frontier_finish_fetch_retryable_error",
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=f"{error_class}_finalize_no_row",
            error_message="frontier.finish_fetch_retryable_error(...) returned no row",
            retry_delay=retry_delay,
        )

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row



# EN: This helper finalizes a permanent fetch failure for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için permanent fetch hatasını finalize eder.
# EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / finish_fetch_permanent_error
# EN:
# EN: Why this helper exists:
# EN: - because frontier-specific DB truth for 'finish_fetch_permanent_error' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable frontier helper name instead of repeating raw frontier SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, lease_token, http_status, error_class, error_message
# EN: - values should match the current Python signature and the live frontier SQL contract below
# EN:
# EN: Accepted output:
# EN: - a frontier-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a claimed work shape, or another explicit branch result
# EN:
# EN: Common frontier meaning hints:
# EN: - this helper exposes one named frontier-specific DB-truth boundary
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw SQL semantics instead of this helper contract
# TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / finish_fetch_permanent_error
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'finish_fetch_permanent_error' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham frontier SQL semantiğini tekrar etmek yerine okunabilir frontier yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, lease_token, http_status, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı frontier SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen frontier-odaklı sonuç şekli
# TR: - bu; yapılı payload, claim edilmiş iş şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak frontier anlam ipuçları:
# TR: - bu yardımcı frontier’e özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham SQL semantiğini anlamaya zorlamak

# EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / finish_fetch_permanent_error
# EN:
# EN: Why this function exists:
# EN: - because frontier gateway needs an explicit DB helper boundary instead of hidden SQL drift
# EN: - because the crawler must be able to audit exactly which frontier-side inputs shape each query/result branch
# EN:
# EN: Accepted role:
# EN: - named frontier-gateway helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# EN: - url_id => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# EN: - lease_token => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# EN: - http_status => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# EN: - error_class => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# EN: - error_message => explicit frontier-gateway input parameter of finish_fetch_permanent_error; this value is part of the visible DB-helper contract of this function
# TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / finish_fetch_permanent_error
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü frontier gateway gizli SQL dağılması yerine açık bir DB helper sınırına ihtiyaç duyar
# TR: - çünkü crawler her query/sonuç dalını hangi frontier-side girdilerin şekillendirdiğini açıkça denetleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli frontier-gateway helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - url_id => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - lease_token => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - http_status => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_class => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
# TR: - error_message => finish_fetch_permanent_error fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
def finish_fetch_permanent_error(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int | None,
    error_class: str,
    error_message: str | None,
) -> dict:
    # EN: We open a cursor because the permanent finalize SQL function must run
    # EN: inside the current controlled transaction.
    # TR: Permanent finalize SQL fonksiyonu mevcut kontrollü transaction içinde
    # TR: çalışmak zorunda olduğu için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core permanent-error finalize function.
        # TR: Kanonik crawler-core permanent-error finalize fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_permanent_error(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_error_class => %s,
                p_error_message => %s
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                error_class,
                error_message,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        return build_frontier_no_row_payload(
            action="frontier_finish_fetch_permanent_error",
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=f"{error_class}_finalize_no_row",
            error_message="frontier.finish_fetch_permanent_error(...) returned no row",
        )

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row
