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

# EN: We import json because frontier.url.url_metadata is updated through explicit JSONB patches.
# TR: frontier.url.url_metadata açık JSONB patch'leriyle güncellendiği için json içe aktarıyoruz.
import json

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
# EN: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_BEGIN
# EN: The SQL claim function returns lease/scheduling fields. Raw evidence also
# EN: needs source_id, seed_id, discovery_type and url_metadata. This helper
# EN: enriches the transient Python payload from frontier.url by url_id inside
# EN: the existing transaction. It performs SELECT only.
# TR: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_BEGIN
# TR: SQL claim fonksiyonu lease/scheduling alanlarını döndürür. Raw kanıt ayrıca
# TR: source_id, seed_id, discovery_type ve url_metadata ister. Bu yardımcı mevcut
# TR: transaction içinde url_id ile frontier.url üzerinden geçici Python payload'ını
# TR: zenginleştirir. Sadece SELECT yapar.
def _frontier_claim_payload_get_optional(row: object, key: str) -> object | None:
    if row is None:
        return None
    if isinstance(row, dict):
        return row.get(key)

    getter = getattr(row, "get", None)
    if callable(getter):
        try:
            return getter(key)
        except Exception:
            pass

    try:
        return row[key]  # type: ignore[index]
    except Exception:
        pass

    return getattr(row, key, None)


def _frontier_claim_payload_as_dict(row: object) -> dict[str, object]:
    if isinstance(row, dict):
        return dict(row)

    keys_callable = getattr(row, "keys", None)
    if callable(keys_callable):
        try:
            return {
                str(key): _frontier_claim_payload_get_optional(row, str(key))
                for key in keys_callable()
            }
        except Exception:
            pass

    payload: dict[str, object] = {}
    for key in (
        "url_id",
        "canonical_url",
        "scheme",
        "host",
        "port",
        "url_path",
        "url_query",
        "host_id",
        "authority_key",
        "robots_mode",
        "user_agent_token",
        "score",
        "depth",
        "priority",
        "lease_token",
        "lease_expires_at",
    ):
        value = _frontier_claim_payload_get_optional(row, key)
        if value is not None:
            payload[key] = value
    return payload


def _frontier_enrich_claimed_row_with_provenance(
    conn: psycopg.Connection,
    row: object,
) -> dict[str, object]:
    payload = _frontier_claim_payload_as_dict(row)
    url_id = payload.get("url_id")
    if url_id is None:
        return payload

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT
              source_id,
              seed_id,
              parent_url_id,
              discovery_type::text AS discovery_type,
              url_metadata,
              url_metadata AS metadata
            FROM frontier.url
            WHERE url_id = %(url_id)s
            """,
            {"url_id": url_id},
        )
        provenance_row = cur.fetchone()

    if provenance_row is None:
        return payload

    payload["source_id"] = (
        None if provenance_row.get("source_id") is None else str(provenance_row.get("source_id"))
    )
    payload["seed_id"] = (
        None if provenance_row.get("seed_id") is None else str(provenance_row.get("seed_id"))
    )
    payload["parent_url_id"] = provenance_row.get("parent_url_id")
    payload["discovery_type"] = provenance_row.get("discovery_type")
    payload["url_metadata"] = provenance_row.get("url_metadata")
    payload["metadata"] = provenance_row.get("metadata")

    return payload


# EN: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_END
# TR: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_END



# P2C69_TARGETED_CLAIM_SCOPE_R1_BEGIN
def _logisticsearch_p2c69_normalize_target_url_ids(
    target_url_ids: object | None,
) -> list[int] | None:
    """Normalize optional controlled target claim scope.

    EN: This helper is only for controlled crawler-core smoke tests where a
    small set of url_id values must be isolated. Normal crawling leaves
    target_url_ids unset so frontier.claim_next_url(...) remains the canonical
    database scheduling authority.

    TR: Bu yardımcı yalnızca küçük bir url_id kümesinin izole edilmesi gereken
    kontrollü crawler-core smoke testleri içindir. Normal crawl akışı
    target_url_ids değerini boş bırakır; frontier.claim_next_url(...) kanonik
    database scheduling otoritesi olarak kalır.
    """

    if target_url_ids is None:
        return None

    normalized: list[int] = []
    seen: set[int] = set()

    if isinstance(target_url_ids, str):
        raw_values = target_url_ids.replace(";", ",").replace(" ", ",").split(",")
    else:
        try:
            raw_values = list(target_url_ids)  # type: ignore[arg-type]
        except TypeError as exc:
            raise ValueError("target_url_ids must be None, string, or iterable") from exc

    for raw_value in raw_values:
        value_text = str(raw_value).strip()
        if not value_text:
            continue

        value = int(value_text)
        if value <= 0:
            raise ValueError(f"target_url_ids contains non-positive url_id: {value}")

        if value not in seen:
            normalized.append(value)
            seen.add(value)

    if not normalized:
        return None

    return normalized
# P2C69_TARGETED_CLAIM_SCOPE_R1_END


def claim_next_url(
    conn: psycopg.Connection,
    worker_id: str,
    lease_seconds: int,
    target_url_ids: object | None = None,
) -> ClaimedUrl | None:
    # EN: P2C69 adds an optional explicit url_id scope for controlled tests.
    # EN: When target_url_ids is unset, the original DB function path is used.
    # TR: P2C69 kontrollü testler için opsiyonel açık url_id kapsamı ekler.
    # TR: target_url_ids boşsa özgün DB function yolu kullanılır.
    normalized_target_url_ids = _logisticsearch_p2c69_normalize_target_url_ids(
        target_url_ids
    )

    with conn.cursor() as cur:
        if normalized_target_url_ids is None:
            # EN: Normal/default path: keep the canonical database function as
            # EN: the scheduling authority.
            # TR: Normal/default yol: kanonik database function scheduling
            # TR: otoritesi olarak kalır.
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
        else:

            cur.execute(
                """
                WITH runtime_params AS (
                    SELECT
                        now() AS p_now,
                        (%(lease_seconds)s::integer * interval '1 second') AS p_lease_duration
                ),
                active_leases AS (
                    SELECT
                        u.host_id,
                        count(*)::integer AS active_lease_count
                    FROM frontier.url u
                    CROSS JOIN runtime_params rp
                    WHERE u.state = 'leased'
                      AND (
                            u.lease_expires_at IS NULL
                         OR u.lease_expires_at >= rp.p_now
                      )
                    GROUP BY u.host_id
                ),
                candidate AS (
                    SELECT
                        u.url_id,
                        u.host_id,
                        u.canonical_url,
                        u.url_path,
                        u.url_query,
                        u.depth,
                        u.priority,
                        u.score,
                        h.scheme,
                        h.host,
                        h.port,
                        h.authority_key,
                        h.user_agent_token,
                        h.robots_mode,
                        h.min_delay_ms,
                        rp.p_now,
                        rp.p_lease_duration
                    FROM frontier.url u
                    JOIN frontier.host h
                      ON h.host_id = u.host_id
                    CROSS JOIN runtime_params rp
                    LEFT JOIN active_leases al
                      ON al.host_id = h.host_id
                    WHERE u.url_id = ANY(%(target_url_ids)s::bigint[])
                      AND u.state IN ('queued', 'retry_wait')
                      AND u.next_fetch_at <= rp.p_now
                      AND (u.revisit_not_before IS NULL OR u.revisit_not_before <= rp.p_now)
                      AND h.host_status = 'active'
                      AND (h.pause_until IS NULL OR h.pause_until <= rp.p_now)
                      AND (h.backoff_until IS NULL OR h.backoff_until <= rp.p_now)
                      AND h.next_eligible_at <= rp.p_now
                      AND COALESCE(al.active_lease_count, 0) < h.max_concurrency
                    ORDER BY
                        u.priority DESC,
                        u.score DESC,
                        u.next_fetch_at ASC,
                        u.url_id ASC
                    LIMIT 1
                    FOR UPDATE OF u, h SKIP LOCKED
                ),
                updated_url AS (
                    UPDATE frontier.url AS u
                       SET state = 'leased'::frontier.url_state_enum,
                           lease_token = gen_random_uuid(),
                           lease_owner = %(worker_id)s,
                           lease_acquired_at = c.p_now,
                           lease_expires_at = c.p_now + c.p_lease_duration,
                           fetch_attempt_count = COALESCE(u.fetch_attempt_count, 0) + 1,
                           last_fetch_started_at = c.p_now,
                           updated_at = c.p_now,
                           url_metadata = COALESCE(u.url_metadata, '{}'::jsonb)
                             || jsonb_build_object(
                                  'p2c69_targeted_claim_scope_enabled', true,
                                  'p2c69_targeted_claim_allowed_url_ids', to_jsonb(%(target_url_ids)s::bigint[]),
                                  'p2c69_targeted_claim_worker_id', %(worker_id)s,
                                  'p2c69_targeted_claim_policy', 'exclusive_url_id_scope_for_controlled_smoke_tests',
                                  'p2c69_targeted_claim_normal_crawler_behavior_changed', false,
                                  'p2c70e_canonical_parity_repaired', true,
                                  'p2c70e_host_eligibility_preserved', true
                                )
                    FROM candidate AS c
                    WHERE u.url_id = c.url_id
                    RETURNING
                        u.url_id,
                        u.host_id,
                        u.canonical_url,
                        u.url_path,
                        u.url_query,
                        u.depth,
                        u.priority,
                        u.score,
                        u.lease_token,
                        u.lease_expires_at
                ),
                updated_host AS (
                    UPDATE frontier.host AS h
                       SET last_fetch_started_at = c.p_now,
                           next_eligible_at = c.p_now + make_interval(secs => c.min_delay_ms / 1000.0),
                           updated_at = c.p_now
                    FROM candidate AS c
                    WHERE h.host_id = c.host_id
                    RETURNING h.host_id
                )
                SELECT
                    uu.url_id,
                    uu.host_id,
                    uu.canonical_url,
                    uu.url_path,
                    uu.url_query,
                    uu.depth,
                    uu.priority,
                    uu.score,
                    uu.lease_token,
                    uu.lease_expires_at,
                    c.scheme,
                    c.host,
                    c.port,
                    c.authority_key,
                    c.user_agent_token,
                    c.robots_mode
                FROM updated_url uu
                JOIN candidate c
                  ON c.url_id = uu.url_id
                JOIN updated_host uh
                  ON uh.host_id = uu.host_id
                """,
                {
                    "worker_id": worker_id,
                    "lease_seconds": lease_seconds,
                    "target_url_ids": normalized_target_url_ids,
                },
            )

        row = cur.fetchone()

    if row is None:
        return None

    enriched_row = _frontier_enrich_claimed_row_with_provenance(conn, row)
    return _row_to_claimed_url(enriched_row)
    # EN: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_END
    # TR: FRONTIER_CLAIM_PAYLOAD_PROVENANCE_GATEWAY_R3_END



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

# EN: Approved lightweight metadata schema for frontier.url.url_metadata.
# EN: PostgreSQL durable columns remain authoritative; this JSONB only carries crawl-map context.
# TR: frontier.url.url_metadata için onaylı hafif metadata şeması.
# TR: PostgreSQL kalıcı kolonları otorite kalır; bu JSONB yalnızca crawl-map bağlamı taşır.
CRAWLER_URL_METADATA_SCHEMA_VERSION = "crawler_url_metadata.v1"
CRAWLER_URL_METADATA_CRAWL_MAP_KEY = "crawl_map"


def _clean_url_metadata_text(value: object) -> str | None:
    """Return a stripped text value for JSONB metadata, or None for empty values."""
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    return text


def build_crawler_url_metadata_v1_crawl_map(
    *,
    root_url_id: int | None,
    branch_role: str | None,
    branch_label: str | None,
    crawl_path_hint: str | None,
) -> dict[str, Any]:
    """
    EN:
    Build the approved crawler_url_metadata.v1 crawl_map patch.

    This helper intentionally does not duplicate durable PostgreSQL truth columns
    such as canonical_url, state, success_count, last_success_at, next_fetch_at,
    lease fields, or HTTP status.

    TR:
    Onaylı crawler_url_metadata.v1 crawl_map patch'ini üretir.

    Bu yardımcı canonical_url, state, success_count, last_success_at,
    next_fetch_at, lease alanları veya HTTP status gibi kalıcı PostgreSQL
    gerçeklik kolonlarını özellikle kopyalamaz.
    """
    crawl_map: dict[str, Any] = {}

    if root_url_id is not None:
        crawl_map["root_url_id"] = int(root_url_id)

    clean_branch_role = _clean_url_metadata_text(branch_role)
    if clean_branch_role is not None:
        crawl_map["branch_role"] = clean_branch_role

    clean_branch_label = _clean_url_metadata_text(branch_label)
    if clean_branch_label is not None:
        crawl_map["branch_label"] = clean_branch_label

    clean_crawl_path_hint = _clean_url_metadata_text(crawl_path_hint)
    if clean_crawl_path_hint is not None:
        crawl_map["crawl_path_hint"] = clean_crawl_path_hint

    return {
        "schema_version": CRAWLER_URL_METADATA_SCHEMA_VERSION,
        CRAWLER_URL_METADATA_CRAWL_MAP_KEY: crawl_map,
    }


def update_url_crawl_map_metadata(
    conn: psycopg.Connection[Any],
    *,
    url_id: int,
    root_url_id: int | None,
    branch_role: str | None,
    branch_label: str | None,
    crawl_path_hint: str | None,
) -> dict[str, Any]:
    """
    EN:
    Update only frontier.url.url_metadata with the approved crawler_url_metadata.v1
    crawl_map context.

    Existing unrelated metadata keys are preserved. Managed `schema_version` and
    `crawl_map` keys are refreshed. Durable PostgreSQL truth columns are not
    duplicated into JSONB.

    Parent-conflict guard failures are classified as safe metadata skips, not as
    hard degraded helper failures. This keeps rediscovered pre-existing rows from
    receiving misleading crawl_map context.

    TR:
    Yalnızca frontier.url.url_metadata alanını onaylı crawler_url_metadata.v1
    crawl_map bağlamıyla günceller.

    İlgisiz mevcut metadata anahtarları korunur. Yönetilen `schema_version` ve
    `crawl_map` anahtarları yenilenir. Kalıcı PostgreSQL gerçeklik kolonları
    JSONB içine kopyalanmaz.

    Parent-conflict guard başarısızlıkları sert degraded helper hatası değil,
    güvenli metadata skip olarak sınıflandırılır. Böylece yeniden keşfedilmiş
    mevcut satırlara yanıltıcı crawl_map bağlamı yazılmaz.
    """
    metadata_patch = build_crawler_url_metadata_v1_crawl_map(
        root_url_id=root_url_id,
        branch_role=branch_role,
        branch_label=branch_label,
        crawl_path_hint=crawl_path_hint,
    )

    crawl_map = metadata_patch.get(CRAWLER_URL_METADATA_CRAWL_MAP_KEY)
    if not isinstance(crawl_map, dict) or not crawl_map:
        return {
            "action": "update_url_crawl_map_metadata",
            "url_id": int(url_id),
            "metadata_updated": False,
            "metadata_degraded": True,
            "metadata_skipped": False,
            "error_class": "empty_crawl_map_patch",
            "error_message": "crawler_url_metadata.v1 crawl_map patch was empty",
        }

    metadata_patch_json = json.dumps(
        metadata_patch,
        sort_keys=True,
        separators=(",", ":"),
    )
    target_url_id = int(url_id)
    root_url_id_int = int(root_url_id) if root_url_id is not None else None

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT
                u.url_id,
                u.parent_url_id
            FROM frontier.url AS u
            WHERE u.url_id = %(url_id)s
            """,
            {
                "url_id": target_url_id,
            },
        )
        guard_row = cur.fetchone()

    if guard_row is None:
        return {
            "action": "update_url_crawl_map_metadata",
            "url_id": target_url_id,
            "metadata_updated": False,
            "metadata_degraded": True,
            "metadata_skipped": False,
            "error_class": "url_metadata_target_missing",
            "error_message": "frontier.url target row was not found for metadata update",
        }

    target_parent_url_id = guard_row.get("parent_url_id")
    parent_guard_allows_update = (
        root_url_id_int is None
        or target_url_id == root_url_id_int
        or (
            target_parent_url_id is not None
            and int(target_parent_url_id) == root_url_id_int
        )
    )

    if not parent_guard_allows_update:
        return {
            "action": "update_url_crawl_map_metadata",
            "url_id": target_url_id,
            "parent_url_id": (
                int(target_parent_url_id) if target_parent_url_id is not None else None
            ),
            "root_url_id": root_url_id_int,
            "metadata_updated": False,
            "metadata_degraded": False,
            "metadata_skipped": True,
            "skip_class": "parent_conflict_guard_skipped",
            "skip_message": "frontier.url metadata update skipped because target row parent does not match requested root_url_id",
        }

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            WITH metadata_patch AS (
                SELECT %(metadata_patch)s::jsonb AS patch
            )
            UPDATE frontier.url AS u
               SET url_metadata =
                   (
                       (COALESCE(u.url_metadata, '{}'::jsonb) - 'schema_version' - 'crawl_map')
                       || jsonb_build_object('schema_version', 'crawler_url_metadata.v1')
                       || jsonb_build_object(
                            'crawl_map',
                            COALESCE(u.url_metadata -> 'crawl_map', '{}'::jsonb)
                            || COALESCE(
                                (SELECT patch -> 'crawl_map' FROM metadata_patch),
                                '{}'::jsonb
                            )
                          )
                   )
             WHERE u.url_id = %(url_id)s
               AND (
                   %(root_url_id)s IS NULL
                   OR u.url_id = %(root_url_id)s
                   OR u.parent_url_id = %(root_url_id)s
               )
             RETURNING
                   u.url_id,
                   u.parent_url_id,
                   u.url_metadata
            """,
            {
                "url_id": target_url_id,
                "root_url_id": root_url_id_int,
                "metadata_patch": metadata_patch_json,
            },
        )
        row = cur.fetchone()

    if row is None:
        return {
            "action": "update_url_crawl_map_metadata",
            "url_id": target_url_id,
            "parent_url_id": (
                int(target_parent_url_id) if target_parent_url_id is not None else None
            ),
            "root_url_id": root_url_id_int,
            "metadata_updated": False,
            "metadata_degraded": True,
            "metadata_skipped": False,
            "error_class": "url_metadata_update_no_row_after_guard_pass",
            "error_message": "frontier.url metadata update returned no row after parent guard precheck passed",
        }

    payload = dict(row)
    payload["action"] = "update_url_crawl_map_metadata"
    payload["metadata_updated"] = True
    payload["metadata_degraded"] = False
    payload["metadata_skipped"] = False
    return payload
