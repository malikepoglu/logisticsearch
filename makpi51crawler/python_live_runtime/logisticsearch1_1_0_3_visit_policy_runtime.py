# LogisticSearch crawler_core visit policy runtime helpers.
#
# Topology:
# - 1_1_0_1: startpoint catalog runtime
# - 1_1_0_2: multilingual startpoint seed planner
# - 1_1_0_3: visit policy and queue scheduling decision helper
#
# This module is intentionally pure-Python and side-effect free.
# It does not fetch URLs.
# It does not write DB state.
# It does not mutate catalog JSON.
# It separates static JSON policy from dynamic runtime DB state.

# VISIT_POLICY_RUNTIME_STYLE_ALIGNMENT_R1_BEGIN
# EN: MODULE TOPOLOGY / logisticsearch1_1_0_3_visit_policy_runtime
# EN:   Meaning: this helper is the third child in the 1_1_0 startpoint / seed-policy family.
# EN:   Expected values: pure decision helpers only; no crawler start, no DB write, no URL fetch.
# EN:   Error values: embedding PostgreSQL mutations, network acquisition, or service control in this layer.
# EN:   because queue truth belongs to PostgreSQL frontier tables and this Python file only computes decisions.
# TR: MODÜL TOPOLOJİSİ / logisticsearch1_1_0_3_visit_policy_runtime
# TR:   Anlamı: bu yardımcı 1_1_0 startpoint / seed-policy ailesinin üçüncü çocuğudur.
# TR:   Beklenen doğru değerler: yalnızca saf karar yardımcıları; crawler başlatma, DB yazma, URL fetch yok.
# TR:   Hata değerleri: PostgreSQL mutasyonunu, network acquisition'ı veya service control'ü bu katmana gömmek.
# TR:   Çünkü queue doğrusu PostgreSQL frontier tablolarındadır ve bu Python dosyası sadece karar hesaplar.
#
# EN: QUEUE_SYSTEM_DESIGN / DESIGN BOUNDARY / queue system
# EN:   Meaning: the queue system is not a new standalone Python queue engine.
# EN:   Expected values: frontier.host and frontier.url remain durable queue truth.
# EN:   Expected values: Python reads JSON policy and DB state, then returns claim/skip decisions.
# EN:   Error values: sleeping on a capped domain, mutating JSON state, or creating a parallel in-memory queue truth.
# EN:   because a lean crawler must avoid duplicated queue state and must keep recovery durable.
# TR: TASARIM SINIRI / queue sistemi
# TR:   Anlamı: queue sistemi yeni ve bağımsız bir Python queue motoru değildir.
# TR:   Beklenen doğru değerler: frontier.host ve frontier.url kalıcı queue doğrusu olarak kalır.
# TR:   Beklenen doğru değerler: Python JSON policy ve DB state okur, sonra claim/skip kararı döndürür.
# TR:   Hata değerleri: capped domain üzerinde uyumak, JSON state değiştirmek veya paralel memory queue doğrusu kurmak.
# TR:   Çünkü yalın crawler çift queue state üretmemeli ve recovery kalıcı DB doğrusu üzerinden yapılmalıdır.
#
# EN: LOCAL VALUE EXPLANATION / DEFAULT_MIN_VISIT_INTERVAL_SECONDS
# EN:   Meaning: experimental default minimum interval per normalized_root_domain.
# EN:   Expected values: positive integer seconds; current activation experiment value is 60.
# EN:   Error values: zero, negative, boolean, or production-hardcoded value without a gate.
# EN:   because this default controls queue claim pressure across all 26 catalog JSON files.
# TR: YEREL DEĞER AÇIKLAMASI / DEFAULT_MIN_VISIT_INTERVAL_SECONDS
# TR:   Anlamı: normalized_root_domain başına deneysel default minimum aralıktır.
# TR:   Beklenen doğru değerler: pozitif integer saniye; güncel aktivasyon deney değeri 60'tır.
# TR:   Hata değerleri: sıfır, negatif, boolean veya gate olmadan production-hardcoded değer.
# TR:   Çünkü bu default 26 catalog JSON dosyasındaki queue claim baskısını kontrol eder.
#
# EN: LOCAL VALUE EXPLANATION / FIATA_INITIAL_MIN_VISIT_INTERVAL_SECONDS
# EN:   Meaning: first explicit fast-domain override for fiata.org.
# EN:   Expected values: positive integer seconds; current initial value is 30.
# EN:   Error values: treating this as permission to ignore robots, retry-after, or soft-limit warnings.
# EN:   because large repeated source domains still need robots/retry/error backoff to win over JSON policy.
# TR: YEREL DEĞER AÇIKLAMASI / FIATA_INITIAL_MIN_VISIT_INTERVAL_SECONDS
# TR:   Anlamı: fiata.org için ilk açık hızlı-domain override değeridir.
# TR:   Beklenen doğru değerler: pozitif integer saniye; güncel ilk değer 30'dur.
# TR:   Hata değerleri: bunu robots, retry-after veya soft-limit uyarılarını yok sayma izni saymak.
# TR:   Çünkü büyük tekrar eden kaynak domainlerde robots/retry/error backoff JSON policy'den üstün kalmalıdır.
#
# EN: LOCAL VALUE EXPLANATION / normalized_root_domain
# EN:   Meaning: global queue budget key derived from each seed URL host.
# EN:   Expected values: fiata.org, freightnet.com, cargoyellowpages.com style root-domain strings.
# EN:   Error values: catalog_code, source_family_code, seed_surface_code, or raw hostname as the budget key.
# EN:   because the same domain appears across many language catalogs and must share one budget.
# TR: YEREL DEĞER AÇIKLAMASI / normalized_root_domain
# TR:   Anlamı: her seed URL host değerinden türetilen global queue budget anahtarıdır.
# TR:   Beklenen doğru değerler: fiata.org, freightnet.com, cargoyellowpages.com tarzı root-domain stringleri.
# TR:   Hata değerleri: budget key olarak catalog_code, source_family_code, seed_surface_code veya raw hostname kullanmak.
# TR:   Çünkü aynı domain birçok dil katalogunda tekrar eder ve tek budget paylaşmalıdır.
#
# EN: LOCAL VALUE EXPLANATION / SOFT_LIMIT_SIGNAL_FAMILIES
# EN:   Meaning: text/header signals for sites that return HTTP 200 but warn about usage limits.
# EN:   Expected values: quota warning, temporary block, automation warning, challenge/captcha, login/access wall.
# EN:   Error values: relying only on HTTP 429/403/503 and missing warning pages that still return 200.
# EN:   because some sources warn about limit pressure without emitting a hard HTTP error.
# TR: YEREL DEĞER AÇIKLAMASI / SOFT_LIMIT_SIGNAL_FAMILIES
# TR:   Anlamı: HTTP 200 döndürüp kullanım limiti uyarısı veren siteler için text/header sinyalleridir.
# TR:   Beklenen doğru değerler: quota warning, temporary block, automation warning, challenge/captcha, login/access wall.
# TR:   Hata değerleri: yalnızca HTTP 429/403/503'e güvenip 200 dönen uyarı sayfalarını kaçırmak.
# TR:   Çünkü bazı kaynaklar hard HTTP hata kodu vermeden limit baskısını bildirir.
#
# EN: LOCAL VALUE EXPLANATION / build_queue_scheduling_decision
# EN:   Meaning: single pure function that merges JSON policy, DB runtime gates, and soft-limit backoff.
# EN:   Expected values: visible receipt with queue_should_claim_now or queue_should_skip_domain.
# EN:   Error values: sleeping inside this helper, fetching a URL, or changing DB/JSON state.
# EN:   because the worker layer must orchestrate side effects while this helper remains testable and deterministic.
# TR: YEREL DEĞER AÇIKLAMASI / build_queue_scheduling_decision
# TR:   Anlamı: JSON policy, DB runtime gate'leri ve soft-limit backoff bilgisini birleştiren saf fonksiyondur.
# TR:   Beklenen doğru değerler: queue_should_claim_now veya queue_should_skip_domain içeren görünür receipt.
# TR:   Hata değerleri: bu helper içinde uyumak, URL fetch yapmak veya DB/JSON state değiştirmek.
# TR:   Çünkü side effect orkestrasyonu worker katmanında kalmalı, bu helper test edilebilir ve deterministik olmalıdır.
#
# EN: LOCAL VALUE EXPLANATION / detect_soft_limit_warning
# EN:   Meaning: conservative signal classifier for soft usage-limit pages and headers.
# EN:   Expected values: no full body logging, only limited classification fields and matched signal families.
# EN:   Error values: dumping full HTML, storing sensitive page bodies, or converting every warning into permanent block.
# EN:   because the crawler needs safety receipts without polluting logs or overreacting to recoverable warnings.
# TR: YEREL DEĞER AÇIKLAMASI / detect_soft_limit_warning
# TR:   Anlamı: soft kullanım limiti sayfaları ve header'ları için muhafazakar sinyal sınıflandırıcıdır.
# TR:   Beklenen doğru değerler: full body log yok; sadece sınırlı sınıflandırma alanları ve matched signal families.
# TR:   Hata değerleri: full HTML dökmek, hassas page body saklamak veya her uyarıyı permanent block'a çevirmek.
# TR:   Çünkü crawler güvenli receipt üretmeli, logları kirletmemeli ve toparlanabilir uyarılara aşırı tepki vermemelidir.
#
# EN: RUNTIME SAFETY CONTRACT
# EN:   Expected values: no network-client import, no Python URL-opener import, no database-client mutation, no SQL write statements.
# EN:   Expected values: static JSON policy is read-only; dynamic visit state comes from DB.
# EN:   because activation testing must stay reversible until explicit worker/frontier gates permit mutation.
# TR: RUNTIME GÜVENLİK SÖZLEŞMESİ
# TR:   Beklenen doğru değerler: network-client import yok, Python URL-opener import yok, database-client mutasyonu yok, SQL write statement yok.
# TR:   Beklenen doğru değerler: statik JSON policy read-only; dinamik ziyaret state DB'den gelir.
# TR:   Çünkü aktivasyon testi açık worker/frontier gate'leri izin verene kadar geri alınabilir kalmalıdır.
# VISIT_POLICY_RUNTIME_STYLE_ALIGNMENT_R1_END

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from urllib.parse import urlparse


DEFAULT_MIN_VISIT_INTERVAL_SECONDS = 60
FIATA_INITIAL_MIN_VISIT_INTERVAL_SECONDS = 30

STATIC_POLICY_KEYS = frozenset(
    {
        "host_budget_group",
        "recrawl_interval",
        "default_recrawl_interval",
        "crawl_depth_policy",
        "crawl_priority",
        "daily_family_budget_required",
        "source_family_visit_policy",
        "min_visit_interval_seconds",
        "crawl_delay_seconds",
        "visit_interval_seconds",
        "rate_limit_per_hour",
    }
)

FORBIDDEN_DYNAMIC_JSON_KEYS = frozenset(
    {
        "last_visit_at",
        "last_fetch_at",
        "last_success_at",
        "next_fetch_at",
        "retry_after_until",
        "last_http_status",
    }
)

DEFAULT_ROOT_DOMAIN_MIN_INTERVAL_OVERRIDES = {
    "fiata.org": FIATA_INITIAL_MIN_VISIT_INTERVAL_SECONDS,
}

SOFT_LIMIT_SIGNAL_FAMILIES = {
    "quota_warning": (
        "usage limit",
        "daily limit",
        "monthly limit",
        "quota exceeded",
        "rate limit exceeded",
        "request limit",
        "search limit",
        "query limit",
    ),
    "temporary_block": (
        "temporarily blocked",
        "temporary block",
        "try again later",
        "please wait",
        "too many requests",
        "slow down",
    ),
    "automation_warning": (
        "automated access",
        "unusual traffic",
        "suspicious traffic",
        "bot detection",
        "robot detection",
    ),
    "challenge_or_captcha": (
        "captcha",
        "recaptcha",
        "cloudflare",
        "verify you are human",
        "security check",
    ),
    "login_or_access_wall": (
        "sign in to continue",
        "login to continue",
        "access denied",
        "permission required",
    ),
}

_COMMON_SECOND_LEVEL_SUFFIXES = frozenset(
    {
        "ac.uk",
        "co.uk",
        "gov.uk",
        "ltd.uk",
        "me.uk",
        "net.uk",
        "org.uk",
        "plc.uk",
        "com.au",
        "net.au",
        "org.au",
        "com.br",
        "com.tr",
        "com.cn",
        "com.hk",
        "com.sg",
        "co.jp",
        "co.kr",
        "co.in",
        "com.mx",
        "com.ar",
        "com.co",
        "co.za",
    }
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def extract_hostname(url_or_host: Any) -> str:
    value = _clean_text(url_or_host)
    if not value:
        return ""

    if "://" not in value:
        value = "https://" + value

    try:
        parsed = urlparse(value)
    except Exception:
        return ""

    host = (parsed.hostname or "").lower().strip(".")
    if host.startswith("www."):
        host = host[4:]

    return host


def derive_normalized_root_domain(url_or_host: Any) -> str:
    host = extract_hostname(url_or_host)
    if not host:
        return ""

    labels = [part for part in host.split(".") if part]
    if len(labels) <= 2:
        return host

    suffix2 = ".".join(labels[-2:])
    suffix3 = ".".join(labels[-3:])

    if suffix2 in _COMMON_SECOND_LEVEL_SUFFIXES and len(labels) >= 3:
        return suffix3

    if suffix3 in _COMMON_SECOND_LEVEL_SUFFIXES and len(labels) >= 4:
        return ".".join(labels[-4:])

    return ".".join(labels[-2:])


def coerce_positive_int(value: Any) -> int | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value if value > 0 else None

    if isinstance(value, float):
        if value.is_integer() and value > 0:
            return int(value)
        return None

    text = _clean_text(value)
    if not text:
        return None

    if text.isdigit():
        parsed = int(text)
        return parsed if parsed > 0 else None

    return None


def _walk_mapping_values(value: Any) -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []

    def rec(obj: Any, prefix: str) -> None:
        if isinstance(obj, Mapping):
            for key, child in obj.items():
                path = f"{prefix}.{key}" if prefix else str(key)
                out.append((path, child))
                rec(child, path)
        elif isinstance(obj, list):
            for index, child in enumerate(obj):
                path = f"{prefix}[{index}]"
                rec(child, path)

    rec(value, "")
    return out


def find_first_positive_int_by_key(policy: Mapping[str, Any] | None, keys: tuple[str, ...]) -> int | None:
    if not isinstance(policy, Mapping):
        return None

    wanted = set(keys)

    for path, value in _walk_mapping_values(policy):
        key = path.rsplit(".", 1)[-1]
        if key in wanted:
            parsed = coerce_positive_int(value)
            if parsed is not None:
                return parsed

    return None


def detect_forbidden_dynamic_json_keys(policy: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(policy, Mapping):
        return []

    found: list[str] = []
    for path, _value in _walk_mapping_values(policy):
        key = path.rsplit(".", 1)[-1]
        if key in FORBIDDEN_DYNAMIC_JSON_KEYS:
            found.append(path)

    return sorted(found)


def resolve_json_policy_min_visit_interval_seconds(
    *,
    root_domain: str,
    seed_policy: Mapping[str, Any] | None = None,
    surface_policy: Mapping[str, Any] | None = None,
    family_policy: Mapping[str, Any] | None = None,
    root_domain_overrides: Mapping[str, int] | None = None,
    default_seconds: int = DEFAULT_MIN_VISIT_INTERVAL_SECONDS,
) -> int:
    parsed_default = coerce_positive_int(default_seconds) or DEFAULT_MIN_VISIT_INTERVAL_SECONDS

    for policy in (seed_policy, surface_policy, family_policy):
        parsed = find_first_positive_int_by_key(
            policy,
            (
                "min_visit_interval_seconds",
                "crawl_delay_seconds",
                "visit_interval_seconds",
                "min_fetch_interval_seconds",
                "min_crawl_interval_seconds",
            ),
        )
        if parsed is not None:
            return parsed

    normalized = derive_normalized_root_domain(root_domain)
    overrides = dict(DEFAULT_ROOT_DOMAIN_MIN_INTERVAL_OVERRIDES)

    if root_domain_overrides:
        for key, value in root_domain_overrides.items():
            parsed = coerce_positive_int(value)
            if parsed is not None:
                overrides[derive_normalized_root_domain(key)] = parsed

    if normalized in overrides:
        return overrides[normalized]

    return parsed_default


def compute_effective_min_visit_interval_seconds(
    *,
    json_policy_min_visit_interval_seconds: int,
    robots_crawl_delay_seconds: int | None = None,
    retry_after_seconds: int | None = None,
    error_backoff_seconds: int | None = None,
    soft_limit_backoff_seconds: int | None = None,
    global_safety_floor_seconds: int = 1,
) -> int:
    values = [
        coerce_positive_int(json_policy_min_visit_interval_seconds),
        coerce_positive_int(robots_crawl_delay_seconds),
        coerce_positive_int(retry_after_seconds),
        coerce_positive_int(error_backoff_seconds),
        coerce_positive_int(soft_limit_backoff_seconds),
        coerce_positive_int(global_safety_floor_seconds),
    ]

    clean_values = [value for value in values if value is not None]
    if not clean_values:
        return DEFAULT_MIN_VISIT_INTERVAL_SECONDS

    return max(clean_values)


def compute_next_allowed_fetch_at(
    *,
    reference_time: datetime,
    effective_min_visit_interval_seconds: int,
) -> datetime:
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)

    seconds = coerce_positive_int(effective_min_visit_interval_seconds)
    if seconds is None:
        seconds = DEFAULT_MIN_VISIT_INTERVAL_SECONDS

    return reference_time + timedelta(seconds=seconds)


def should_skip_capped_domain(
    *,
    now: datetime,
    next_allowed_at: datetime | None,
) -> bool:
    if next_allowed_at is None:
        return False

    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    if next_allowed_at.tzinfo is None:
        next_allowed_at = next_allowed_at.replace(tzinfo=timezone.utc)

    return now < next_allowed_at


def capped_domain_decision(
    *,
    now: datetime,
    next_allowed_at: datetime | None,
) -> dict[str, Any]:
    skip = should_skip_capped_domain(now=now, next_allowed_at=next_allowed_at)

    if skip:
        return {
            "domain_capped": True,
            "action": "skip_domain_select_next_eligible",
            "sleep_on_capped_domain": False,
        }

    return {
        "domain_capped": False,
        "action": "domain_eligible",
        "sleep_on_capped_domain": False,
    }


def detect_soft_limit_warning(
    *,
    http_status: int | None,
    response_headers: Mapping[str, Any] | None = None,
    text_sample: str | None = None,
) -> dict[str, Any]:
    headers = response_headers if isinstance(response_headers, Mapping) else {}
    sample = (text_sample or "").lower()
    header_blob = " ".join(f"{key}: {value}" for key, value in headers.items()).lower()
    combined = (header_blob + " " + sample).strip()

    matched_families: list[str] = []
    matched_terms: list[str] = []

    if http_status in (429, 403, 503):
        matched_families.append("hard_http_limit")
        matched_terms.append(str(http_status))

    if "retry-after" in header_blob:
        matched_families.append("retry_after_header")
        matched_terms.append("retry-after")

    for family, terms in SOFT_LIMIT_SIGNAL_FAMILIES.items():
        for term in terms:
            if term in combined:
                matched_families.append(family)
                matched_terms.append(term)

    unique_families = sorted(set(matched_families))
    unique_terms = sorted(set(matched_terms))

    soft_limit_detected = any(
        family in unique_families
        for family in (
            "quota_warning",
            "temporary_block",
            "automation_warning",
            "challenge_or_captcha",
            "login_or_access_wall",
        )
    )

    hard_limit_detected = any(
        family in unique_families
        for family in ("hard_http_limit", "retry_after_header")
    )

    return {
        "limit_signal_detected": bool(unique_families),
        "soft_limit_detected": soft_limit_detected,
        "hard_limit_detected": hard_limit_detected,
        "matched_signal_families": unique_families,
        "matched_signal_terms": unique_terms,
        "http_status": http_status,
    }


def latest_runtime_gate_at(*values: datetime | None) -> datetime | None:
    clean_values: list[datetime] = []

    for value in values:
        if value is None:
            continue

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        clean_values.append(value)

    if not clean_values:
        return None

    return max(clean_values)


def build_visit_policy_receipt(
    *,
    url: str,
    seed_policy: Mapping[str, Any] | None = None,
    surface_policy: Mapping[str, Any] | None = None,
    family_policy: Mapping[str, Any] | None = None,
    robots_crawl_delay_seconds: int | None = None,
    retry_after_seconds: int | None = None,
    error_backoff_seconds: int | None = None,
    soft_limit_backoff_seconds: int | None = None,
) -> dict[str, Any]:
    root_domain = derive_normalized_root_domain(url)
    json_interval = resolve_json_policy_min_visit_interval_seconds(
        root_domain=root_domain,
        seed_policy=seed_policy,
        surface_policy=surface_policy,
        family_policy=family_policy,
    )
    effective_interval = compute_effective_min_visit_interval_seconds(
        json_policy_min_visit_interval_seconds=json_interval,
        robots_crawl_delay_seconds=robots_crawl_delay_seconds,
        retry_after_seconds=retry_after_seconds,
        error_backoff_seconds=error_backoff_seconds,
        soft_limit_backoff_seconds=soft_limit_backoff_seconds,
    )

    forbidden_paths: list[str] = []
    for policy in (seed_policy, surface_policy, family_policy):
        forbidden_paths.extend(detect_forbidden_dynamic_json_keys(policy))

    return {
        "url": url,
        "normalized_root_domain": root_domain,
        "json_policy_min_visit_interval_seconds": json_interval,
        "effective_min_visit_interval_seconds": effective_interval,
        "forbidden_dynamic_json_key_paths": sorted(set(forbidden_paths)),
        "budget_key": "normalized_root_domain",
        "runtime_state_must_come_from_db": True,
        "catalog_json_runtime_state_mutation_allowed": False,
    }


def build_queue_scheduling_decision(
    *,
    now: datetime,
    url: str,
    seed_policy: Mapping[str, Any] | None = None,
    surface_policy: Mapping[str, Any] | None = None,
    family_policy: Mapping[str, Any] | None = None,
    host_next_eligible_at: datetime | None = None,
    url_next_fetch_at: datetime | None = None,
    url_revisit_not_before: datetime | None = None,
    last_visit_at: datetime | None = None,
    robots_crawl_delay_seconds: int | None = None,
    retry_after_seconds: int | None = None,
    error_backoff_seconds: int | None = None,
    soft_limit_backoff_seconds: int | None = None,
) -> dict[str, Any]:
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    receipt = build_visit_policy_receipt(
        url=url,
        seed_policy=seed_policy,
        surface_policy=surface_policy,
        family_policy=family_policy,
        robots_crawl_delay_seconds=robots_crawl_delay_seconds,
        retry_after_seconds=retry_after_seconds,
        error_backoff_seconds=error_backoff_seconds,
        soft_limit_backoff_seconds=soft_limit_backoff_seconds,
    )

    effective_interval = int(receipt["effective_min_visit_interval_seconds"])

    interval_gate_at = None
    if last_visit_at is not None:
        interval_gate_at = compute_next_allowed_fetch_at(
            reference_time=last_visit_at,
            effective_min_visit_interval_seconds=effective_interval,
        )

    retry_gate_at = None
    parsed_retry_after = coerce_positive_int(retry_after_seconds)
    if parsed_retry_after is not None:
        retry_gate_at = now + timedelta(seconds=parsed_retry_after)

    soft_limit_gate_at = None
    parsed_soft_limit_backoff = coerce_positive_int(soft_limit_backoff_seconds)
    if parsed_soft_limit_backoff is not None:
        soft_limit_gate_at = now + timedelta(seconds=parsed_soft_limit_backoff)

    next_allowed_at = latest_runtime_gate_at(
        host_next_eligible_at,
        url_next_fetch_at,
        url_revisit_not_before,
        interval_gate_at,
        retry_gate_at,
        soft_limit_gate_at,
    )

    domain_decision = capped_domain_decision(
        now=now,
        next_allowed_at=next_allowed_at,
    )

    queue_should_skip_domain = bool(domain_decision["domain_capped"])
    queue_should_claim_now = not queue_should_skip_domain

    return {
        **receipt,
        "queue_policy_version": "queue_visit_policy.v1",
        "queue_should_claim_now": queue_should_claim_now,
        "queue_should_skip_domain": queue_should_skip_domain,
        "queue_action": domain_decision["action"],
        "sleep_on_capped_domain": False,
        "next_allowed_at": next_allowed_at,
        "host_next_eligible_at": host_next_eligible_at,
        "url_next_fetch_at": url_next_fetch_at,
        "url_revisit_not_before": url_revisit_not_before,
        "last_visit_at": last_visit_at,
        "soft_limit_backoff_seconds": soft_limit_backoff_seconds,
        "queue_uses_min_visit_interval_seconds": True,
        "queue_uses_normalized_root_domain_budget": True,
    }
