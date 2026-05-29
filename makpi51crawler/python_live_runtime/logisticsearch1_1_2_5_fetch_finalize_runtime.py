"""
EN:
This file is the fetch-finalize child of the worker-runtime family.

EN:
Why this file exists:
- because terminal fetch outcome handling should live in one explicit child instead of being hidden inside the main worker hub
- because success, blocked_robots, retryable_error, permanent_error, timeout, and network_error branches must remain readable and auditable
- because a beginner should be able to find where a fetch attempt becomes durably finalized without digging through unrelated lease, robots, acquisition, or parse phases

EN:
What this file DOES:
- expose worker-side fetch-finalize helper boundaries
- preserve visible logging, finalization, success-path, retry-path, and degraded branch meaning
- keep terminal fetch semantics separate from broader worker orchestration

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not own all acquisition logic
- it does not own all parse logic
- it does not own all storage-routing logic

EN:
Topological role:
- the main worker runtime hub sits above this file
- acquisition or page-fetch phases produce inputs that flow into this file
- parse/storage layers sit after this file or consume its visible finalized outcome meaning

EN:
Important visible values and shapes:
- outcome => values such as success, blocked_robots, retryable_error, permanent_error, timeout, or network_error
- fetch_attempt_log => structured terminal logging payload for the current attempt
- success_finalize_result or finalize_result => explicit durable finalization meaning
- release_result => whether lease release or cleanup side effect became visible
- degraded branch payloads => explicit non-happy finalize outcomes that must remain readable

EN:
Accepted architectural identity:
- worker fetch-finalize runtime child
- narrow terminal-outcome contract layer
- readable finalization boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague outcome utility dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya worker-runtime ailesinin fetch-finalize child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü terminal fetch outcome işleme ana worker hubının içinde gizlenmek yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü success, blocked_robots, retryable_error, permanent_error, timeout ve network_error dalları okunabilir ve denetlenebilir kalmalıdır
- çünkü yeni başlayan biri bir fetch attemptin nerede kalıcı olarak finalize edildiğini ilgisiz lease, robots, acquisition veya parse fazları arasında kaybolmadan bulabilmelidir

TR:
Bu dosya NE yapar:
- worker-side fetch-finalize yardımcı sınırlarını açığa çıkarır
- logging, finalization, success-path, retry-path ve degraded dal anlamını görünür tutar
- terminal fetch semantiklerini daha geniş worker orkestrasyonundan ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tüm acquisition mantığının sahibi değildir
- tüm parse mantığının sahibi değildir
- tüm storage-routing mantığının sahibi değildir

TR:
Topolojik rol:
- ana worker runtime hubı bu dosyanın üstündedir
- acquisition veya page-fetch fazları bu dosyaya akan girdileri üretir
- parse/storage katmanları bu dosyadan sonra gelir veya bu dosyanın görünür finalized outcome anlamını tüketir

TR:
Önemli görünür değerler ve şekiller:
- outcome => success, blocked_robots, retryable_error, permanent_error, timeout veya network_error gibi değerler
- fetch_attempt_log => mevcut attempt için yapılı terminal logging payloadı
- success_finalize_result veya finalize_result => açık kalıcı finalization anlamı
- release_result => lease release veya cleanup yan etkisinin görünür olup olmadığı
- degraded dal payloadları => okunabilir kalması gereken mutlu-yol-dışı finalize sonuçları

TR:
Kabul edilen mimari kimlik:
- worker fetch-finalize runtime child
- dar terminal-outcome sözleşme katmanı
- okunabilir finalization sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz outcome utility çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module owns worker-side terminal fetch-attempt logging plus durable
# EN: error finalization helpers after the controlled worker-runtime split.
# TR: Bu modül kontrollü worker-runtime split’inden sonra worker-tarafı terminal
# TR: fetch-attempt loglamasını ve kalıcı hata finalization yardımcılarını sahiplenir.

# EN: FETCH FINALIZE RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow terminal-outcome corner of the worker corridor.
# EN: Beginner mental model:
# EN: - the worker first obtains and processes a work item
# EN: - this file is where that attempt becomes explicitly concluded
# EN: - it exists so the crawler can later answer: what happened, was it logged, was it finalized, was it released
# EN:
# EN: Accepted architectural meaning:
# EN: - named fetch-finalize child
# EN: - focused terminal outcome and finalization helper surface
# EN: - readable boundary for success vs retry vs permanent failure style outcomes
# EN:
# EN: Undesired architectural meaning:
# EN: - random outcome helper pile
# EN: - hidden second orchestrator
# EN: - place where finalization failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - outcome values should stay explicit
# EN: - logging and finalization payloads should stay structured and readable
# EN: - degraded finalize branches must remain visible
# TR: FETCH FINALIZE RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar terminal-outcome köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - worker önce bir iş öğesi alır ve işler
# TR: - bu dosya o attemptin açık biçimde sonuçlandığı yerdir
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: ne oldu, loglandı mı, finalize edildi mi, release edildi mi
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli fetch-finalize child
# TR: - odaklı terminal outcome ve finalization yardımcı yüzeyi
# TR: - success vs retry vs permanent failure tarzı sonuçlar için okunabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele outcome helper yığını
# TR: - gizli ikinci orchestrator
# TR: - finalization hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - outcome değerleri açık kalmalıdır
# TR: - logging ve finalization payloadları yapılı ve okunabilir kalmalıdır
# TR: - degraded finalize dalları görünür kalmalıdır

from __future__ import annotations

import hashlib
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

# EN: We import the stable acquisition-family public surface because finalize
# EN: helpers need claimed-url field access plus the fetched-page contract shape.
# TR: Finalize yardımcıları claimed-url alan erişimine ve fetched-page sözleşme
# TR: şekline ihtiyaç duyduğu için kararlı acquisition-aile public yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    FetchedPageResult,
    get_claimed_url_value,
)

# EN: We import the worker support helper that builds explicit metadata for
# EN: durable per-attempt logging.
# TR: Kalıcı deneme-bazlı loglama için açık metadata üreten worker destek
# TR: yardımcısını içe aktarıyoruz.
from .logisticsearch1_1_2_1_worker_runtime_support import (
    build_terminal_fetch_attempt_metadata,
)

# EN: We import the canonical DB gateway finalize/log wrappers because Python
# EN: must stay aligned with the sealed SQL contract.
# TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye kanonik DB
# TR: gateway finalize/log wrapper’larını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    log_fetch_attempt_terminal,
)


# EN: This helper writes one terminal fetch-attempt row using only the fields the
# EN: current worker surface honestly knows at log time.
# TR: Bu yardımcı log anında worker yüzeyinin dürüstçe bildiği alanları kullanarak
# TR: tek bir terminal fetch-attempt satırı yazar.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / log_fetch_attempt_terminal_from_worker
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'log_fetch_attempt_terminal_from_worker' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, worker_id, outcome, note, acquisition_method, fetched_page, error_class, error_message
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely shapes terminal logging payloads or fetch-attempt evidence visibility
# EN: - explicit payload structure is often important for audits
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / log_fetch_attempt_terminal_from_worker
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'log_fetch_attempt_terminal_from_worker' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, worker_id, outcome, note, acquisition_method, fetched_page, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal logging payloadlarını veya fetch-attempt evidence görünürlüğünü şekillendirir
# TR: - açık payload yapısı denetimler için çoğu zaman önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF log_fetch_attempt_terminal_from_worker
# EN: log_fetch_attempt_terminal_from_worker is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: conn, claimed_url, worker_id, outcome, note, acquisition_method, fetched_page, error_class, error_message.
# TR: REAL-RULE AST REPAIR / FONKSIYON log_fetch_attempt_terminal_from_worker
# TR: log_fetch_attempt_terminal_from_worker acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, claimed_url, worker_id, outcome, note, acquisition_method, fetched_page, error_class, error_message.
# P1F_TIMEOUT_POLICY_FETCH_METADATA_PERSISTENCE_R1_BEGIN
def _logisticsearch_build_p1f_timeout_policy_fetch_metadata_patch(
    fetched_page: FetchedPageResult | None,
) -> dict[str, object]:
    """Return behavior-neutral timeout-policy metadata for terminal fetch-attempt logging.

    EN: This does not change acquisition, timeout, retry/dead, raw storage, or DB schema behavior.
    TR: Bu; acquisition, timeout, retry/dead, raw storage veya DB schema davranışını değiştirmez.
    """

    if fetched_page is None:
        return {}

    timeout_policy = getattr(fetched_page, "timeout_policy", None)
    if not isinstance(timeout_policy, dict) or not timeout_policy:
        return {}

    return {
        "timeout_policy": dict(timeout_policy),
        "timeout_policy_persistence": {
            "schema": "p1f_timeout_policy_fetch_metadata_persistence_v1",
            "source": "FetchedPageResult.timeout_policy",
            "destination": "http_fetch.fetch_attempt.fetch_metadata.timeout_policy",
            "behavior_change": False,
        },
    }
# P1F_TIMEOUT_POLICY_FETCH_METADATA_PERSISTENCE_R1_END


# P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_R1_BEGIN
P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA = "p1k_http_3xx_redirect_target_policy_v1"

def _logisticsearch_p1k_normalize_absolute_url(url_value: str) -> str:
    """Normalize one absolute URL for P1K equality and frontier identity checks."""
    raw_url = str(url_value or "").strip()
    if not raw_url:
        return ""
    try:
        without_fragment, _fragment = urldefrag(raw_url)
        parsed = urlparse(without_fragment)
        scheme = str(parsed.scheme or "").lower()
        host = str(parsed.hostname or "").lower()
        if scheme not in {"http", "https"} or not host:
            return raw_url
        try:
            parsed_port = parsed.port
        except ValueError:
            return raw_url
        if parsed_port is None:
            netloc = host
        elif (scheme == "https" and parsed_port == 443) or (scheme == "http" and parsed_port == 80):
            netloc = host
        else:
            netloc = f"{host}:{int(parsed_port)}"
        path = parsed.path or "/"
        return urlunparse((scheme, netloc, path, "", parsed.query or "", ""))
    except Exception:
        return raw_url


def _logisticsearch_p1k_normalize_http_3xx_redirect_target(
    *,
    request_url: str,
    redirect_target_url: str,
) -> dict[str, object]:
    """Normalize one HTTP 3xx redirect target without network I/O."""
    raw_request_url = str(request_url or "").strip()
    raw_redirect_target_url = str(redirect_target_url or "").strip()

    if not raw_request_url or not raw_redirect_target_url:
        return {
            "redirect_target_available": False,
            "redirect_target_skip_reason": "missing_request_or_redirect_target",
        }

    try:
        absolute_url = urljoin(raw_request_url, raw_redirect_target_url)
        absolute_url, _fragment = urldefrag(absolute_url)
        parsed = urlparse(absolute_url)
    except Exception as exc:
        return {
            "redirect_target_available": False,
            "redirect_target_skip_reason": "url_parse_error",
            "redirect_target_error": f"{type(exc).__name__}: {exc}",
        }

    scheme = str(parsed.scheme or "").lower()
    host = str(parsed.hostname or "").lower()

    if scheme not in {"http", "https"} or not host:
        return {
            "redirect_target_available": False,
            "redirect_target_skip_reason": "unsupported_scheme_or_missing_host",
            "redirect_target_scheme": scheme,
            "redirect_target_host": host,
        }

    try:
        parsed_port = parsed.port
    except ValueError:
        return {
            "redirect_target_available": False,
            "redirect_target_skip_reason": "invalid_port",
            "redirect_target_raw": raw_redirect_target_url,
        }

    if parsed_port is None:
        port = 443 if scheme == "https" else 80
        netloc = host
    else:
        port = int(parsed_port)
        if (scheme == "https" and port == 443) or (scheme == "http" and port == 80):
            netloc = host
        else:
            netloc = f"{host}:{port}"

    path = parsed.path or "/"
    query = parsed.query or ""
    normalized_url = urlunparse((scheme, netloc, path, "", query, ""))
    request_normalized = _logisticsearch_p1k_normalize_absolute_url(raw_request_url)

    if normalized_url == request_normalized:
        return {
            "redirect_target_available": False,
            "redirect_target_skip_reason": "target_equals_request_after_normalization",
            "redirect_target_url": normalized_url,
            "request_url_normalized": request_normalized,
        }

    target_has_404_hint = any(
        token in normalized_url.lower()
        for token in ["/404", "404.aspx", "customerrorpages/404", "not-found", "notfound"]
    )

    return {
        "redirect_target_available": True,
        "redirect_target_url": normalized_url,
        "request_url_normalized": request_normalized,
        "redirect_target_scheme": scheme,
        "redirect_target_host": host,
        "redirect_target_port": port,
        "redirect_target_authority_key": f"{host}:{port}",
        "redirect_target_path": path,
        "redirect_target_query": query,
        "redirect_target_has_404_hint": target_has_404_hint,
        "redirect_target_policy_schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
    }


def _logisticsearch_p1k_build_http_3xx_redirect_target_policy(
    *,
    request_url: str,
    http_status: int | None,
    fetched_page: FetchedPageResult | None,
) -> dict[str, object]:
    """Build P1K metadata when a 3xx final_url points to a different target."""
    if http_status is None or not (300 <= int(http_status) <= 399):
        return {}

    if fetched_page is None:
        return {
            "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
            "source": "fetch_finalize_runtime.finalize_http_error",
            "destination": "http_fetch.fetch_attempt.fetch_metadata",
            "behavior_change": True,
            "redirect_target_available": False,
            "redirect_target_skip_reason": "fetched_page_missing",
            "http_status": int(http_status),
        }

    final_url = str(getattr(fetched_page, "final_url", "") or "").strip()
    normalized = _logisticsearch_p1k_normalize_http_3xx_redirect_target(
        request_url=str(request_url or ""),
        redirect_target_url=final_url,
    )

    return {
        "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
        "source": "fetch_finalize_runtime.finalize_http_error",
        "destination": "http_fetch.fetch_attempt.fetch_metadata_and_frontier.enqueue_discovered_url",
        "behavior_change": True,
        "http_status": int(http_status),
        "request_url": str(request_url or ""),
        "fetched_page_final_url": final_url,
        **normalized,
    }


def _logisticsearch_p1k_build_http_3xx_redirect_target_policy_fetch_metadata_patch(
    *,
    request_url: str,
    http_status: int | None,
    fetched_page: FetchedPageResult | None,
) -> dict[str, object]:
    """Return fetch_metadata patch for P1K redirect target evidence."""
    policy = _logisticsearch_p1k_build_http_3xx_redirect_target_policy(
        request_url=request_url,
        http_status=http_status,
        fetched_page=fetched_page,
    )
    if not policy:
        return {}
    return {
        "p1k_http_3xx_redirect_target_policy": policy,
    }


def _logisticsearch_p1k_policy_has_redirect_target(policy: dict[str, object]) -> bool:
    return bool(policy.get("redirect_target_available")) and bool(
        str(policy.get("redirect_target_url") or "").strip()
    )


def _logisticsearch_p1k_int_claimed_url_value(
    claimed_url: object,
    key: str,
    default: int,
) -> int:
    try:
        return int(get_claimed_url_value(claimed_url, key))
    except Exception:
        return int(default)


def _logisticsearch_p1k_enqueue_http_3xx_redirect_target(
    conn,
    *,
    claimed_url: object,
    redirect_policy: dict[str, object],
) -> dict[str, object]:
    """Enqueue or reuse normalized redirect target through the existing frontier function."""
    if not _logisticsearch_p1k_policy_has_redirect_target(redirect_policy):
        return {
            "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
            "redirect_target_enqueue_attempted": False,
            "redirect_target_enqueue_reason": "no_redirect_target",
        }

    target_url = str(redirect_policy.get("redirect_target_url") or "").strip()
    target_scheme = str(redirect_policy.get("redirect_target_scheme") or "").strip()
    target_host = str(redirect_policy.get("redirect_target_host") or "").strip()
    target_path = str(redirect_policy.get("redirect_target_path") or "/").strip() or "/"
    target_query = str(redirect_policy.get("redirect_target_query") or "").strip()
    target_port = int(redirect_policy.get("redirect_target_port") or (443 if target_scheme == "https" else 80))
    target_authority_key = str(redirect_policy.get("redirect_target_authority_key") or f"{target_host}:{target_port}").strip()

    parent_url_id = _logisticsearch_p1k_int_claimed_url_value(claimed_url, "url_id", 0)
    parent_depth = _logisticsearch_p1k_int_claimed_url_value(claimed_url, "depth", 0)
    parent_priority = _logisticsearch_p1k_int_claimed_url_value(claimed_url, "priority", 100)
    canonical_url_sha256 = hashlib.sha256(target_url.encode("utf-8")).hexdigest()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                  url_id,
                  host_id,
                  canonical_url,
                  state::text,
                  discovery_type::text,
                  depth,
                  priority
                FROM frontier.enqueue_discovered_url(
                  p_parent_url_id := %s,
                  p_canonical_url := %s,
                  p_canonical_url_sha256 := %s,
                  p_port := %s,
                  p_scheme := %s,
                  p_host := %s,
                  p_authority_key := %s,
                  p_registrable_domain := %s,
                  p_url_path := %s,
                  p_url_query := %s,
                  p_discovery_type := 'redirect'::frontier.discovery_type_enum,
                  p_depth := %s,
                  p_priority := %s,
                  p_enqueue_reason := %s
                )
                """,
                (
                    parent_url_id,
                    target_url,
                    canonical_url_sha256,
                    target_port,
                    target_scheme,
                    target_host,
                    target_authority_key,
                    target_host,
                    target_path,
                    target_query,
                    parent_depth + 1,
                    parent_priority,
                    f"{P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA}: normalized HTTP 3xx final_url target",
                ),
            )
            row = cursor.fetchone()
    except Exception as exc:
        return {
            "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
            "redirect_target_enqueue_attempted": True,
            "redirect_target_enqueue_persisted": False,
            "redirect_target_enqueue_error": f"{type(exc).__name__}: {exc}",
            "redirect_target_url": target_url,
        }

    if row is None:
        return {
            "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
            "redirect_target_enqueue_attempted": True,
            "redirect_target_enqueue_persisted": False,
            "redirect_target_enqueue_error": "frontier.enqueue_discovered_url_returned_no_row",
            "redirect_target_url": target_url,
        }

    def row_value(index: int, key: str) -> object:
        if hasattr(row, "keys") and key in row:
            return row[key]
        return row[index]

    return {
        "schema": P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA,
        "redirect_target_enqueue_attempted": True,
        "redirect_target_enqueue_persisted": True,
        "redirect_target_url_id": row_value(0, "url_id"),
        "redirect_target_host_id": row_value(1, "host_id"),
        "redirect_target_url": row_value(2, "canonical_url"),
        "redirect_target_state": row_value(3, "state"),
        "redirect_target_discovery_type": row_value(4, "discovery_type"),
        "redirect_target_depth": row_value(5, "depth"),
        "redirect_target_priority": row_value(6, "priority"),
    }
# P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_R1_END


def log_fetch_attempt_terminal_from_worker(
    conn,
    *,
    claimed_url: object,
    worker_id: str,
    outcome: str,
    note: str,
    acquisition_method: str | None,
    fetched_page: FetchedPageResult | None = None,
    error_class: str | None = None,
    error_message: str | None = None,
) -> dict[str, object]:
    # EN: We extract the exact frontier identities so the durable log row stays
    # EN: anchored to the same leased work item.
    # TR: Kalıcı log satırı aynı leased iş öğesine bağlı kalsın diye tam frontier
    # TR: kimliklerini çıkarıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL log_fetch_attempt_terminal_from_worker / url_id
    # EN: url_id are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL log_fetch_attempt_terminal_from_worker / url_id
    # TR: url_id burada acik ara dal degerleri olarak atanir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / host_id
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `int(get_claimed_url_value(claimed_url, "host_id"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): host_id
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / host_id
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): host_id
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    host_id = int(get_claimed_url_value(claimed_url, "host_id"))
    # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / lease_token
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "lease_token"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): lease_token
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / lease_token
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): lease_token
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))
    # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / request_url
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "canonical_url"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): request_url
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / request_url
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): request_url
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    request_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We start with the minimum field set always visible in the worker.
    # TR: Worker’da her zaman görünür olan asgari alan kümesiyle başlıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL log_fetch_attempt_terminal_from_worker / payload
    # EN: payload are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL log_fetch_attempt_terminal_from_worker / payload
    # TR: payload burada acik ara dal degerleri olarak atanir.
    payload = {
        "url_id": url_id,
        "host_id": host_id,
        "worker_id": worker_id,
        "request_url": request_url,
        "outcome": outcome,
        "fetch_kind": "page",
        "lease_token": lease_token,
        "request_method": "GET",
        "final_url": request_url,
        "http_status": None,
        "content_type": None,
        "content_length": None,
        "body_storage_path": None,
        "body_sha256": None,
        "body_bytes": None,
        "etag": None,
        "last_modified": None,
        "error_class": error_class,
        "error_message": error_message,
        "fetch_metadata": build_terminal_fetch_attempt_metadata(
            claimed_url=claimed_url,
            acquisition_method=acquisition_method,
            note=note,
        ),
    }

    # EN: When a real fetched-page artefact exists, we enrich the payload with
    # EN: honest response/storage fields.
    # TR: Gerçek bir fetched-page artefact’ı varsa payload’ı dürüst response ve
    # TR: storage alanlarıyla zenginleştiriyoruz.
    if fetched_page is not None:
        payload.update(
            {
                "final_url": fetched_page.final_url,
                "http_status": fetched_page.http_status,
                "content_type": fetched_page.content_type,
                "content_length": fetched_page.body_bytes,
                "body_storage_path": fetched_page.raw_storage_path,
                "body_sha256": fetched_page.raw_sha256,
                "body_bytes": fetched_page.body_bytes,
                "etag": fetched_page.etag,
                "last_modified": fetched_page.last_modified,
            }
        )

    timeout_policy_metadata = _logisticsearch_build_p1f_timeout_policy_fetch_metadata_patch(
        fetched_page
    )
    if timeout_policy_metadata:
        fetch_metadata_value = payload.get("fetch_metadata")
        if isinstance(fetch_metadata_value, dict):
            payload["fetch_metadata"] = {
                **fetch_metadata_value,
                **timeout_policy_metadata,
            }


    p1k_redirect_policy_metadata = _logisticsearch_p1k_build_http_3xx_redirect_target_policy_fetch_metadata_patch(
        request_url=request_url,
        http_status=payload.get("http_status"),
        fetched_page=fetched_page,
    )
    if p1k_redirect_policy_metadata:
        fetch_metadata_value = payload.get("fetch_metadata")
        if isinstance(fetch_metadata_value, dict):
            payload["fetch_metadata"] = {
                **fetch_metadata_value,
                **p1k_redirect_policy_metadata,
            }


    # EN: The canonical fetch-attempt logging surface may still return no row on
    # EN: some drift paths. That must degrade cleanly instead of crashing the worker.
    # TR: Kanonik fetch-attempt logging yüzeyi bazı drift yollarında hâlâ satır
    # TR: döndürmeyebilir. Bu durum worker’ı çökertmek yerine temizce degrade edilmelidir.
    try:
        return log_fetch_attempt_terminal(
            conn,
            **payload,
        )
    except RuntimeError as exc:
        if "http_fetch.log_fetch_attempt_terminal(...) returned no row" not in str(exc):
            raise

        # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / degraded_error_message
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `payload.get("error_message")` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): degraded_error_message
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / degraded_error_message
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): degraded_error_message
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        degraded_error_message = payload.get("error_message")
        if degraded_error_message is None:
            # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / degraded_error_message
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `f"fetch_attempt_no_row: {exc}"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): degraded_error_message
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / degraded_error_message
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): degraded_error_message
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            degraded_error_message = f"fetch_attempt_no_row: {exc}"
        else:
            # EN: LOCAL VALUE EXPLANATION / log_fetch_attempt_terminal_from_worker / degraded_error_message
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `f"{degraded_error_message} | fetch_attempt_no_row: {exc}"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): degraded_error_message
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / log_fetch_attempt_terminal_from_worker / degraded_error_message
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): degraded_error_message
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            degraded_error_message = f"{degraded_error_message} | fetch_attempt_no_row: {exc}"

        return build_fetch_attempt_no_row_payload(
            url_id=payload["url_id"],
            host_id=payload["host_id"],
            worker_id=payload["worker_id"],
            request_url=payload["request_url"],
            outcome=payload["outcome"],
            error_class=payload.get("error_class"),
            error_message=degraded_error_message,
        )


# EN: This helper classifies HTTP status failures into the minimal retryable vs
# EN: permanent buckets currently used by the worker.
# TR: Bu yardımcı HTTP durum hatalarını worker’ın şu anda kullandığı minimal
# TR: retryable ve permanent kovalarına ayırır.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / classify_http_status_failure
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'classify_http_status_failure' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: http_status
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper exposes one named worker fetch-finalize contract boundary
# EN: - explicit outcome and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / classify_http_status_failure
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'classify_http_status_failure' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: http_status
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı isimli bir worker fetch-finalize sözleşme sınırını açığa çıkarır
# TR: - açık outcome ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF classify_http_status_failure
# EN: classify_http_status_failure is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: http_status.
# TR: REAL-RULE AST REPAIR / FONKSIYON classify_http_status_failure
# TR: classify_http_status_failure acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: http_status.
def classify_http_status_failure(http_status: int) -> tuple[str, bool]:
    # EN: Only HTTP 2xx belongs to the success corridor. This helper classifies
    # EN: all non-2xx statuses before the worker can enter parse/discovery.
    # TR: Yalnızca HTTP 2xx başarı koridoruna aittir. Bu yardımcı, worker
    # TR: parse/discovery aşamasına girmeden önce tüm 2xx dışı durumları sınıflandırır.
    if 200 <= http_status <= 299:
        return ("http_success_status_unexpected_error_path", False)

    # EN: Redirects should normally be resolved by the HTTP client. If a final
    # EN: unresolved 3xx reaches this layer, do not parse it; retry/inspect later.
    # TR: Redirect normalde HTTP client tarafından çözülmelidir. Final çözülmemiş
    # TR: 3xx bu katmana ulaşırsa parse edilmez; retry/inceleme yoluna gider.
    if 300 <= http_status <= 399:
        return ("http_3xx_unresolved_redirect", True)

    # EN: 304 needs a future conditional-fetch/not-modified path; current worker
    # EN: must not treat it as a normal parseable success page.
    # TR: 304 için ileride conditional-fetch/not-modified yolu gerekir; mevcut
    # TR: worker bunu normal parse edilebilir başarı saymamalıdır.
    if http_status == 304:
        return ("http_304_not_modified_unhandled", True)

    permanent_client_statuses = {
        400: "http_400_bad_request",
        401: "http_401_access_denied",
        403: "http_403_forbidden",
        404: "http_404",
        410: "http_410_gone",
        451: "http_451_legal_block",
    }
    if http_status in permanent_client_statuses:
        return (permanent_client_statuses[http_status], False)

    retryable_client_statuses = {
        408: "http_408_timeout",
        425: "http_425_too_early",
        429: "http_429_rate_limited",
    }
    if http_status in retryable_client_statuses:
        return (retryable_client_statuses[http_status], True)

    if 400 <= http_status <= 499:
        return (f"http_{http_status}_client_error", False)

    if 500 <= http_status <= 599:
        return (f"http_{http_status}_server_error", True)

    return ("http_invalid_or_unknown_status", True)


# EN: This helper converts a frontier finalize no-row failure into an operator-visible
# EN: degraded payload so the worker can keep already-written fetch-attempt evidence
# EN: and return an honest unresolved state instead of crashing again.
# TR: Bu yardımcı frontier finalize no-row hatasını operatörün görebileceği
# TR: degrade payload'a çevirir; böylece worker zaten yazılmış fetch-attempt
# TR: kanıtını korur ve yeniden çökmeden dürüst bir çözülmemiş durum döndürür.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / build_finalize_no_row_payload
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'build_finalize_no_row_payload' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, lease_token, http_status, error_class, error_message, degraded_reason
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely deals with terminal outcome logging, durable finalization, or release visibility
# EN: - explicit outcome values and degraded finalize behavior may matter here
# EN: - these helpers often decide whether success, retry, or permanent-failure meaning becomes durable
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_finalize_no_row_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_finalize_no_row_payload' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, lease_token, http_status, error_class, error_message, degraded_reason
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal outcome logging, kalıcı finalization veya release görünürlüğü ile ilgilenir
# TR: - açık outcome değerleri ve degraded finalize davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman success, retry veya permanent-failure anlamının kalıcı olup olmayacağını belirler
# TR: - görünür success vs failure ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF build_finalize_no_row_payload
# EN: build_finalize_no_row_payload is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: url_id, lease_token, http_status, error_class, error_message, degraded_reason.
# TR: REAL-RULE AST REPAIR / FONKSIYON build_finalize_no_row_payload
# TR: build_finalize_no_row_payload acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: url_id, lease_token, http_status, error_class, error_message, degraded_reason.
def build_finalize_no_row_payload(
    *,
    url_id: int,
    lease_token: str,
    http_status: int | None,
    error_class: str,
    error_message: str,
    degraded_reason: str,
) -> dict[str, object]:
    # EN: We return one normalized degraded payload shape shared by sibling finalize
    # EN: paths so operator-facing results stay consistent.
    # TR: Kardeş finalize yolları arasında ortak, normalize bir degrade payload
    # TR: şekli döndürüyoruz; böylece operatörün gördüğü sonuçlar tutarlı kalır.
    return {
        "url_id": url_id,
        "lease_token": lease_token,
        "http_status": http_status,
        "error_class": error_class,
        "error_message": error_message,
        "finalize_degraded": True,
        "finalize_degraded_reason": degraded_reason,
        "finalize_completed": False,
    }


# EN: This helper converts a fetch-attempt no-row failure into an operator-visible
# EN: degraded payload so runtime call sites can keep moving with honest unresolved
# EN: state instead of crashing again.
# TR: Bu yardımcı fetch-attempt no-row hatasını operatörün görebileceği degrade
# TR: payload’a çevirir; böylece runtime çağrı noktaları yeniden çökmeden dürüst
# TR: çözülmemiş durumla ilerleyebilir.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / build_fetch_attempt_no_row_payload
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'build_fetch_attempt_no_row_payload' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, host_id, worker_id, request_url, outcome, error_class, error_message
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely shapes terminal logging payloads or fetch-attempt evidence visibility
# EN: - explicit payload structure is often important for audits
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_fetch_attempt_no_row_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_fetch_attempt_no_row_payload' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, host_id, worker_id, request_url, outcome, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal logging payloadlarını veya fetch-attempt evidence görünürlüğünü şekillendirir
# TR: - açık payload yapısı denetimler için çoğu zaman önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF build_fetch_attempt_no_row_payload
# EN: build_fetch_attempt_no_row_payload is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: url_id, host_id, worker_id, request_url, outcome, error_class, error_message.
# TR: REAL-RULE AST REPAIR / FONKSIYON build_fetch_attempt_no_row_payload
# TR: build_fetch_attempt_no_row_payload acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: url_id, host_id, worker_id, request_url, outcome, error_class, error_message.
def build_fetch_attempt_no_row_payload(
    *,
    url_id: int | None,
    host_id: int,
    worker_id: str,
    request_url: str,
    outcome: str,
    error_class: str | None,
    error_message: str | None,
) -> dict[str, object]:
    # EN: We return one normalized degraded payload shape for fetch-attempt logging
    # EN: drift so caller-visible results stay explicit and consistent.
    # TR: Fetch-attempt logging drift’i için normalize tek bir degrade payload
    # TR: şekli döndürüyoruz; böylece çağıranın gördüğü sonuç açık ve tutarlı kalır.
    return {
        "attempt_id": None,
        "url_id": url_id,
        "host_id": host_id,
        "worker_id": worker_id,
        "request_url": request_url,
        "outcome": outcome,
        "error_class": error_class,
        "error_message": error_message,
        "fetch_attempt_degraded": True,
        "fetch_attempt_degraded_reason": "http_fetch_log_fetch_attempt_terminal_returned_no_row",
        "fetch_attempt_persisted": False,
    }


# EN: This helper finalizes a robots-blocked claim as a permanent outcome.
# TR: Bu yardımcı robots tarafından engellenen bir claim’i permanent sonuç olarak
# TR: finalize eder.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / finalize_robots_block
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'finalize_robots_block' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, robots_allow_decision, worker_id
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely deals with terminal outcome logging, durable finalization, or release visibility
# EN: - explicit outcome values and degraded finalize behavior may matter here
# EN: - these helpers often decide whether success, retry, or permanent-failure meaning becomes durable
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / finalize_robots_block
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'finalize_robots_block' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, robots_allow_decision, worker_id
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal outcome logging, kalıcı finalization veya release görünürlüğü ile ilgilenir
# TR: - açık outcome değerleri ve degraded finalize davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman success, retry veya permanent-failure anlamının kalıcı olup olmayacağını belirler
# TR: - görünür success vs failure ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF finalize_robots_block
# EN: finalize_robots_block is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: conn, claimed_url, robots_allow_decision, worker_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON finalize_robots_block
# TR: finalize_robots_block acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, claimed_url, robots_allow_decision, worker_id.
def finalize_robots_block(
    conn,
    *,
    claimed_url: object,
    robots_allow_decision: dict | None,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_robots_block / url_id
    # EN: url_id are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_robots_block / url_id
    # TR: url_id burada acik ara dal degerleri olarak atanir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / lease_token
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "lease_token"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): lease_token
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / lease_token
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): lease_token
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We read the visible verdict so the stored error stays explicit.
    # TR: Saklanan hata açık kalsın diye görünür verdict’i okuyoruz.
    verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")
    # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / error_message
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `f"robots verdict forbids fetch: {verdict}"` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): error_message
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / error_message
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): error_message
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    error_message = f"robots verdict forbids fetch: {verdict}"

    # EN: We first persist one terminal per-attempt row for audit visibility.
    # TR: Audit görünürlüğü oluşsun diye önce tek bir terminal deneme satırı
    # TR: yazıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_robots_block / fetch_attempt_log
    # EN: fetch_attempt_log are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_robots_block / fetch_attempt_log
    # TR: fetch_attempt_log burada acik ara dal degerleri olarak atanir.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="blocked_robots",
        note="worker runtime robots-blocked finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="robots_blocked",
        error_message=error_message,
    )

    # EN: The frontier permanent finalize call may still return no row on some drift
    # EN: paths. That must degrade cleanly instead of crashing the worker again.
    # TR: Frontier permanent finalize çağrısı bazı drift yollarında hâlâ satır
    # TR: döndürmeyebilir. Bu durum worker’ı yeniden çökertmek yerine temizce
    # TR: degrade edilmelidir.
    try:
        # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `finish_fetch_permanent_error( conn, url_id=url_id, lease_token=lease_token, http_status=None, error_class="robots_blocked", error_message=er` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result = finish_fetch_permanent_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="robots_blocked",
            error_message=error_message,
        )
        # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `dict(finalize_result)` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = dict(finalize_result)
    except RuntimeError as exc:
        if "frontier.finish_fetch_permanent_error(...) returned no row" not in str(exc):
            raise

        # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `build_finalize_no_row_payload( url_id=url_id, lease_token=lease_token, http_status=None, error_class="robots_blocked_finalize_no_row", error` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = build_finalize_no_row_payload(
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="robots_blocked_finalize_no_row",
            error_message=f"{error_message} | finalize_no_row: {exc}",
            degraded_reason="frontier_finish_fetch_permanent_error_returned_no_row",
        )

    # EN: We merge durable fetch-attempt evidence into the returned payload.
    # TR: Kalıcı fetch-attempt kanıtını dönen payload’a birleştiriyoruz.
    return {
        **finalize_result_payload,
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This helper finalizes an HTTP error according to the current minimal
# EN: retryable/permanent rule.
# TR: Bu yardımcı bir HTTP hatasını mevcut minimal retryable/permanent kuralına
# TR: göre finalize eder.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / finalize_http_error
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'finalize_http_error' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, http_status, error_message, worker_id
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely deals with terminal outcome logging, durable finalization, or release visibility
# EN: - explicit outcome values and degraded finalize behavior may matter here
# EN: - these helpers often decide whether success, retry, or permanent-failure meaning becomes durable
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / finalize_http_error
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'finalize_http_error' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, http_status, error_message, worker_id
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal outcome logging, kalıcı finalization veya release görünürlüğü ile ilgilenir
# TR: - açık outcome değerleri ve degraded finalize davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman success, retry veya permanent-failure anlamının kalıcı olup olmayacağını belirler
# TR: - görünür success vs failure ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF finalize_http_error
# EN: finalize_http_error is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: conn, claimed_url, http_status, error_message, worker_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON finalize_http_error
# TR: finalize_http_error acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, claimed_url, http_status, error_message, worker_id.
def finalize_http_error(
    conn,
    *,
    claimed_url: object,
    http_status: int,
    error_message: str,
    worker_id: str,
    fetched_page: FetchedPageResult | None = None,
) -> dict[str, object]:
    # EN: We classify the HTTP status first so the branch stays explicit.
    # TR: Branch açık kalsın diye önce HTTP durumunu sınıflandırıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_http_error / error_class, is_retryable
    # EN: error_class, is_retryable are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_http_error / error_class, is_retryable
    # TR: error_class, is_retryable burada acik ara dal degerleri olarak atanir.
    error_class, is_retryable = classify_http_status_failure(http_status)

    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_http_error / url_id
    # EN: url_id are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_http_error / url_id
    # TR: url_id burada acik ara dal degerleri olarak atanir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    # EN: LOCAL VALUE EXPLANATION / finalize_http_error / lease_token
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "lease_token"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): lease_token
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / lease_token
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): lease_token
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We persist one terminal fetch-attempt row before frontier finalization.
    # TR: Frontier finalization’dan önce tek bir terminal fetch-attempt satırı
    # TR: yazıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_http_error / fetch_attempt_log
    # EN: fetch_attempt_log are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_http_error / fetch_attempt_log
    # TR: fetch_attempt_log burada acik ara dal degerleri olarak atanir.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="retryable_error" if is_retryable else "permanent_error",
        note="worker runtime HTTP status error finalize path",
        acquisition_method=None,
        fetched_page=fetched_page,
        error_class=error_class,
        error_message=error_message,
    )

    request_url = str(get_claimed_url_value(claimed_url, "canonical_url"))
    p1k_redirect_policy = _logisticsearch_p1k_build_http_3xx_redirect_target_policy(
        request_url=request_url,
        http_status=http_status,
        fetched_page=fetched_page,
    )
    p1k_redirect_enqueue_result: dict[str, object] | None = None
    p1k_finish_mode = "retryable" if is_retryable else "permanent"

    # P2C34_HTTP_3XX_NO_RESOLVABLE_REDIRECT_TARGET_R1_BEGIN
    # EN: If a final HTTP 3xx reaches finalize without a normalized redirect
    # EN: target, retrying the same URL only churns retry_wait. Keep the good
    # EN: path above/below for changed final_url targets, but make no-target
    # EN: redirects terminal and explicit.
    # TR: Finalize katmanına normalize edilebilir redirect hedefi olmadan gelen
    # TR: HTTP 3xx aynı URL'yi tekrar retry_wait'e sokar. final_url değişmişse
    # TR: hedef enqueue davranışı korunur; hedef yoksa açık terminal sınıfa alınır.
    if (
        error_class == "http_3xx_unresolved_redirect"
        and not _logisticsearch_p1k_policy_has_redirect_target(p1k_redirect_policy)
    ):
        is_retryable = False
        p1k_finish_mode = "permanent"
        error_class = "http_3xx_no_resolvable_redirect_target"
        base_error_message = str(error_message or "").strip()
        p2c34_note = (
            "p2c34_http_3xx_redirect_policy: "
            "3xx response has no actionable redirect target; "
            "redirect_location empty or unavailable and final_url did not change"
        )
        error_message = f"{base_error_message} | {p2c34_note}" if base_error_message else p2c34_note
    # P2C34_HTTP_3XX_NO_RESOLVABLE_REDIRECT_TARGET_R1_END

    # EN: The retryable/permanent frontier finalize call may still return no row on
    # EN: some drift paths. That must degrade cleanly instead of crashing the worker.
    # TR: Retryable/permanent frontier finalize çağrısı bazı drift yollarında hâlâ
    # TR: satır döndürmeyebilir. Bu durum worker’ı çökertmek yerine temizce
    # TR: degrade edilmelidir.
    try:
        if _logisticsearch_p1k_policy_has_redirect_target(p1k_redirect_policy):
            p1k_redirect_enqueue_result = _logisticsearch_p1k_enqueue_http_3xx_redirect_target(
                conn,
                claimed_url=claimed_url,
                redirect_policy=p1k_redirect_policy,
            )
            if bool(p1k_redirect_enqueue_result.get("redirect_target_enqueue_persisted")):
                p1k_finish_mode = "permanent"
                finalize_result = finish_fetch_permanent_error(
                    conn,
                    url_id=url_id,
                    lease_token=lease_token,
                    http_status=http_status,
                    error_class="http_3xx_redirect_target_enqueued",
                    error_message=f"{error_message} | {P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA}: redirect target queued/reused",
                )
            else:
                p1k_finish_mode = "retryable"
                finalize_result = finish_fetch_retryable_error(
                    conn,
                    url_id=url_id,
                    lease_token=lease_token,
                    http_status=http_status,
                    error_class=error_class,
                    error_message=f"{error_message} | {P1K_HTTP_3XX_REDIRECT_TARGET_POLICY_SCHEMA}: redirect target enqueue failed",
                    retry_delay=None,
                )
        elif is_retryable:
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / finalize_result
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `finish_fetch_retryable_error( conn, url_id=url_id, lease_token=lease_token, http_status=http_status, error_class=error_class, error_message=` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / finalize_result
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            finalize_result = finish_fetch_retryable_error(
                conn,
                url_id=url_id,
                lease_token=lease_token,
                http_status=http_status,
                error_class=error_class,
                error_message=error_message,
                retry_delay=None,
            )
        else:
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / finalize_result
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `finish_fetch_permanent_error( conn, url_id=url_id, lease_token=lease_token, http_status=http_status, error_class=error_class, error_message=` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / finalize_result
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            finalize_result = finish_fetch_permanent_error(
                conn,
                url_id=url_id,
                lease_token=lease_token,
                http_status=http_status,
                error_class=error_class,
                error_message=error_message,
            )

        # EN: LOCAL VALUE EXPLANATION / finalize_http_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `dict(finalize_result)` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = dict(finalize_result)
    except RuntimeError as exc:
        if p1k_finish_mode == "retryable":
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / expected_message
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `"frontier.finish_fetch_retryable_error(...) returned no row"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): expected_message
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / expected_message
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): expected_message
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            expected_message = "frontier.finish_fetch_retryable_error(...) returned no row"
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / degraded_reason
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `"frontier_finish_fetch_retryable_error_returned_no_row"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): degraded_reason
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / degraded_reason
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): degraded_reason
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            degraded_reason = "frontier_finish_fetch_retryable_error_returned_no_row"
        else:
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / expected_message
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `"frontier.finish_fetch_permanent_error(...) returned no row"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): expected_message
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / expected_message
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): expected_message
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            expected_message = "frontier.finish_fetch_permanent_error(...) returned no row"
            # EN: LOCAL VALUE EXPLANATION / finalize_http_error / degraded_reason
            # EN: This local exists because the current finalize-phase branch needs a named
            # EN: and reviewable intermediate value instead of hiding `"frontier_finish_fetch_permanent_error_returned_no_row"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): degraded_reason
            # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as global durable project state
            # EN: - assuming this local guarantees success before the branch logic below finishes
            # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / degraded_reason
            # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
            # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): degraded_reason
            # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli global ve kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
            degraded_reason = "frontier_finish_fetch_permanent_error_returned_no_row"

        if expected_message not in str(exc):
            raise

        # EN: LOCAL VALUE EXPLANATION / finalize_http_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `build_finalize_no_row_payload( url_id=url_id, lease_token=lease_token, http_status=http_status, error_class=f"{error_class}_finalize_no_row"` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_http_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = build_finalize_no_row_payload(
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=f"{error_class}_finalize_no_row",
            error_message=f"{error_message} | finalize_no_row: {exc}",
            degraded_reason=degraded_reason,
        )

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **finalize_result_payload,
        "fetch_attempt_log": dict(fetch_attempt_log),
        "p1k_redirect_target_policy": dict(p1k_redirect_policy) if p1k_redirect_policy else None,
        "p1k_redirect_enqueue_result": dict(p1k_redirect_enqueue_result) if p1k_redirect_enqueue_result else None,
    }


# EN: This helper finalizes a transport-layer failure as retryable.
# TR: Bu yardımcı bir taşıma-katmanı hatasını retryable olarak finalize eder.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / finalize_transport_error
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'finalize_transport_error' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, error_message, worker_id
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely deals with terminal outcome logging, durable finalization, or release visibility
# EN: - explicit outcome values and degraded finalize behavior may matter here
# EN: - these helpers often decide whether success, retry, or permanent-failure meaning becomes durable
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / finalize_transport_error
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'finalize_transport_error' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, error_message, worker_id
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal outcome logging, kalıcı finalization veya release görünürlüğü ile ilgilenir
# TR: - açık outcome değerleri ve degraded finalize davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman success, retry veya permanent-failure anlamının kalıcı olup olmayacağını belirler
# TR: - görünür success vs failure ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF finalize_transport_error
# EN: finalize_transport_error is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: conn, claimed_url, error_message, worker_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON finalize_transport_error
# TR: finalize_transport_error acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, claimed_url, error_message, worker_id.
# TRANSPORT_NAMING_DRIFT_RUNTIME_TRANSPORT_R3_BEGIN
# EN: finalize_transport_error must use the same canonical transport class
# EN: as the worker retry/backoff classifier: runtime_transport_retryable_error.
# EN: The separate transport_retryable_error_finalize_no_row diagnostic label
# EN: intentionally remains distinct for degraded no-row evidence.
# TR: finalize_transport_error, worker retry/backoff sınıflandırmasıyla aynı
# TR: canonical transport sınıfını kullanmalıdır: runtime_transport_retryable_error.
# TR: Ayrı transport_retryable_error_finalize_no_row diagnostic etiketi,
# TR: degraded no-row kanıtı için bilinçli olarak ayrı bırakılır.
# TRANSPORT_NAMING_DRIFT_RUNTIME_TRANSPORT_R3_END
def finalize_transport_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_transport_error / url_id
    # EN: url_id are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_transport_error / url_id
    # TR: url_id burada acik ara dal degerleri olarak atanir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    # EN: LOCAL VALUE EXPLANATION / finalize_transport_error / lease_token
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "lease_token"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): lease_token
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_transport_error / lease_token
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): lease_token
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We separate timeout-like text from broader network failure text so the
    # EN: durable fetch-attempt row stays more informative.
    # TR: Kalıcı fetch-attempt satırı daha bilgilendirici kalsın diye timeout-benzeri
    # TR: metni daha genel ağ hatasından ayırıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_transport_error / normalized_error_message
    # EN: normalized_error_message are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_transport_error / normalized_error_message
    # TR: normalized_error_message burada acik ara dal degerleri olarak atanir.
    normalized_error_message = error_message.lower()
    # EN: LOCAL VALUE EXPLANATION / finalize_transport_error / transport_outcome
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `"timeout" if "timeout" in normalized_error_message else "network_error"` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): transport_outcome
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_transport_error / transport_outcome
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): transport_outcome
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    transport_outcome = "timeout" if "timeout" in normalized_error_message else "network_error"

    # EN: We persist one terminal per-attempt row before frontier finalization.
    # TR: Frontier finalization’dan önce tek bir terminal deneme satırı yazıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_transport_error / fetch_attempt_log
    # EN: fetch_attempt_log are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_transport_error / fetch_attempt_log
    # TR: fetch_attempt_log burada acik ara dal degerleri olarak atanir.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome=transport_outcome,
        note="worker runtime transport-error finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="runtime_transport_retryable_error",
        error_message=error_message,
    )

    # EN: The retryable frontier finalize call may still return no row on some drift
    # EN: paths. That must degrade cleanly instead of crashing the worker again.
    # TR: Retryable frontier finalize çağrısı bazı drift yollarında hâlâ satır
    # TR: döndürmeyebilir. Bu durum worker’ı yeniden çökertmek yerine temizce
    # TR: degrade edilmelidir.
    try:
        # EN: LOCAL VALUE EXPLANATION / finalize_transport_error / finalize_result
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `finish_fetch_retryable_error( conn, url_id=url_id, lease_token=lease_token, http_status=None, error_class="runtime_transport_retryable_error", error` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_transport_error / finalize_result
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result = finish_fetch_retryable_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="runtime_transport_retryable_error",
            error_message=error_message,
            retry_delay=None,
        )
        # EN: LOCAL VALUE EXPLANATION / finalize_transport_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `dict(finalize_result)` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_transport_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = dict(finalize_result)
    except RuntimeError as exc:
        if "frontier.finish_fetch_retryable_error(...) returned no row" not in str(exc):
            raise

        # EN: LOCAL VALUE EXPLANATION / finalize_transport_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `build_finalize_no_row_payload( url_id=url_id, lease_token=lease_token, http_status=None, error_class="transport_retryable_error_finalize_no_` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_transport_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = build_finalize_no_row_payload(
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="transport_retryable_error_finalize_no_row",
            error_message=f"{error_message} | finalize_no_row: {exc}",
            degraded_reason="frontier_finish_fetch_retryable_error_returned_no_row",
        )

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **finalize_result_payload,
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This helper finalizes an unexpected runtime failure as permanent.
# TR: Bu yardımcı beklenmeyen bir runtime hatasını permanent olarak finalize eder.
# EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / finalize_unexpected_runtime_error
# EN:
# EN: Why this function exists:
# EN: - because fetch-finalize truth for 'finalize_unexpected_runtime_error' should be exposed through one named top-level helper boundary
# EN: - because terminal outcome semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, error_message, worker_id
# EN: - values should match the current Python signature and the finalize contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-finalize-oriented result shape defined by the current function body
# EN: - this may be a structured finalization payload, a release result, a logging result, or another explicit terminal-outcome branch result
# EN:
# EN: Common fetch-finalize meaning hints:
# EN: - this helper likely deals with terminal outcome logging, durable finalization, or release visibility
# EN: - explicit outcome values and degraded finalize behavior may matter here
# EN: - these helpers often decide whether success, retry, or permanent-failure meaning becomes durable
# EN: - visible success vs failure distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is terminal-outcome helper logic, not the whole worker corridor
# EN: - finalize results must stay explicit so audits can understand success, degradation, retry, and failure meaning
# EN:
# EN: Undesired behavior:
# EN: - silent outcome mutation
# EN: - vague finalize results that hide branch meaning
# TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / finalize_unexpected_runtime_error
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'finalize_unexpected_runtime_error' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü terminal outcome semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, error_message, worker_id
# TR: - değerler aşağıdaki mevcut Python imzası ve finalize sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen fetch-finalize odaklı sonuç şekli
# TR: - bu; yapılı finalization payloadı, release sonucu, logging sonucu veya başka açık terminal-outcome dal sonucu olabilir
# TR:
# TR: Ortak fetch-finalize anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal outcome logging, kalıcı finalization veya release görünürlüğü ile ilgilenir
# TR: - açık outcome değerleri ve degraded finalize davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman success, retry veya permanent-failure anlamının kalıcı olup olmayacağını belirler
# TR: - görünür success vs failure ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon terminal-outcome yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - finalize sonuçları açık kalmalıdır ki denetimler success, degraded, retry ve failure anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz outcome değişimi
# TR: - dal anlamını gizleyen belirsiz finalize sonuçları

# EN: REAL-RULE AST REPAIR / DEF finalize_unexpected_runtime_error
# EN: finalize_unexpected_runtime_error is an explicit fetch-finalize runtime/helper contract.
# EN: Parameters kept explicit here: conn, claimed_url, error_message, worker_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON finalize_unexpected_runtime_error
# TR: finalize_unexpected_runtime_error acik bir fetch-finalize runtime/helper sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, claimed_url, error_message, worker_id.
def finalize_unexpected_runtime_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
    worker_id: str,
) -> dict[str, object]:
    # EN: We target the exact leased URL identity.
    # TR: Tam leased URL kimliğini hedefliyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_unexpected_runtime_error / url_id
    # EN: url_id are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_unexpected_runtime_error / url_id
    # TR: url_id burada acik ara dal degerleri olarak atanir.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))
    # EN: LOCAL VALUE EXPLANATION / finalize_unexpected_runtime_error / lease_token
    # EN: This local exists because the current finalize-phase branch needs a named
    # EN: and reviewable intermediate value instead of hiding `str(get_claimed_url_value(claimed_url, "lease_token"))` inline.
    # EN: Expected meaning:
    # EN: - current local name(s): lease_token
    # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
    # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
    # EN: Undesired reading:
    # EN: - treating this local as global durable project state
    # EN: - assuming this local guarantees success before the branch logic below finishes
    # TR: YEREL DEĞER AÇIKLAMASI / finalize_unexpected_runtime_error / lease_token
    # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
    # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
    # TR: Beklenen anlam:
    # TR: - mevcut yerel ad(lar): lease_token
    # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli global ve kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
    lease_token = str(get_claimed_url_value(claimed_url, "lease_token"))

    # EN: We first persist one terminal fetch-attempt row.
    # TR: Önce tek bir terminal fetch-attempt satırı yazıyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL finalize_unexpected_runtime_error / fetch_attempt_log
    # EN: fetch_attempt_log are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL finalize_unexpected_runtime_error / fetch_attempt_log
    # TR: fetch_attempt_log burada acik ara dal degerleri olarak atanir.
    fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
        conn,
        claimed_url=claimed_url,
        worker_id=worker_id,
        outcome="permanent_error",
        note="worker runtime unexpected-error finalize path",
        acquisition_method=None,
        fetched_page=None,
        error_class="unexpected_fetch_runtime_error",
        error_message=error_message,
    )

    # EN: Unknown runtime failures are treated as permanent so the minimal layer
    # EN: fails loudly instead of hiding drift.
    # TR: Minimal katman drift’i gizlemek yerine yüksek sesle hata versin diye
    # TR: bilinmeyen runtime hataları permanent kabul edilir.
    try:
        # EN: LOCAL VALUE EXPLANATION / finalize_unexpected_runtime_error / finalize_result
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `finish_fetch_permanent_error( conn, url_id=url_id, lease_token=lease_token, http_status=None, error_class="unexpected_fetch_runtime_error", ` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_unexpected_runtime_error / finalize_result
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result = finish_fetch_permanent_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=None,
            error_class="unexpected_fetch_runtime_error",
            error_message=error_message,
        )
        # EN: LOCAL VALUE EXPLANATION / finalize_unexpected_runtime_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `dict(finalize_result)` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_unexpected_runtime_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = dict(finalize_result)

    # EN: A no-row finalize result must not crash the worker again. We degrade the
    # EN: payload into an operator-visible unresolved state and keep the fetch-attempt
    # EN: evidence that was already written in this transaction.
    # TR: Finalize fonksiyonunun satır döndürmemesi worker’ı yeniden çökertmemelidir.
    # TR: Payload’ı operatör-görünür çözülmemiş duruma düşürüyor ve bu transaction içinde
    # TR: zaten yazılmış fetch-attempt kanıtını koruyoruz.
    except RuntimeError as exc:
        if "frontier.finish_fetch_permanent_error(...) returned no row" not in str(exc):
            raise

        # EN: LOCAL VALUE EXPLANATION / finalize_unexpected_runtime_error / finalize_result_payload
        # EN: This local exists because the current finalize-phase branch needs a named
        # EN: and reviewable intermediate value instead of hiding `{ "url_id": url_id, "lease_token": lease_token, "http_status": None, "error_class": "unexpected_fetch_runtime_error_finalize_no_row", "error` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): finalize_result_payload
        # EN: - this value helps keep success / retryable / permanent / degraded outcome meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as global durable project state
        # EN: - assuming this local guarantees success before the branch logic below finishes
        # TR: YEREL DEĞER AÇIKLAMASI / finalize_unexpected_runtime_error / finalize_result_payload
        # TR: Bu yerel değer vardır; çünkü mevcut finalize-fazı dalı, aşağıdaki
        # TR: ifadeyi satır içine gizlemek yerine isimli ve denetlenebilir ara değerle taşımalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): finalize_result_payload
        # TR: - bu değer success / retryable / permanent / degrade outcome anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli global ve kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal mantığı tamamlanmadan bu yerelin başarıyı garanti ettiğini düşünmek
        finalize_result_payload = {
            "url_id": url_id,
            "lease_token": lease_token,
            "http_status": None,
            "error_class": "unexpected_fetch_runtime_error_finalize_no_row",
            "error_message": f"{error_message} | finalize_no_row: {exc}",
            "finalize_degraded": True,
            "finalize_degraded_reason": "frontier_finish_fetch_permanent_error_returned_no_row",
            "finalize_completed": False,
        }

    # EN: We merge terminal per-attempt evidence into the returned payload.
    # TR: Terminal deneme-bazlı kanıtı dönen payload’a birleştiriyoruz.
    return {
        **finalize_result_payload,
        "fetch_attempt_log": dict(fetch_attempt_log),
    }


# EN: This explicit export list documents the public finalize child surface.
# TR: Bu açık export listesi public finalize alt yüzeyini belgelendirir.
__all__ = [
    "log_fetch_attempt_terminal_from_worker",
    "classify_http_status_failure",
    "finalize_robots_block",
    "finalize_http_error",
    "finalize_transport_error",
    "finalize_unexpected_runtime_error",
]
