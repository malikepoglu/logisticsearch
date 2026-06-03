# LogisticSearch crawler_core worker/frontier visit-policy adapter.
#
# EN: WORKER_FRONTIER_POLICY_ADAPTER / topology
# EN:   Meaning: this module belongs to the 1_1_2 worker-orchestration family.
# EN:   Expected values: pure adapter functions that translate claimed frontier
# EN:   payloads into visit-policy receipts.
# EN:   Error values: direct network acquisition, direct database state writes,
# EN:   service control, or catalog JSON mutation.
# EN:   because PostgreSQL frontier tables remain the durable queue truth while
# EN:   Python owns only readable decision/orchestration boundaries.
# TR: WORKER_FRONTIER_POLICY_ADAPTER / topoloji
# TR:   Anlamı: bu modül 1_1_2 worker-orkestrasyon ailesine aittir.
# TR:   Beklenen doğru değerler: claimed frontier payloadlarını visit-policy
# TR:   receipt şekline çeviren saf adapter fonksiyonlarıdır.
# TR:   Hata değerleri: doğrudan network acquisition, doğrudan database state yazımı,
# TR:   service kontrolü veya catalog JSON mutasyonu.
# TR:   Çünkü PostgreSQL frontier tabloları kalıcı queue doğrusu olarak kalır;
# TR:   Python yalnızca okunabilir karar/orkestrasyon sınırlarını sahiplenir.
#
# EN: QUEUE_SYSTEM_DESIGN / lean queue contract
# EN:   Expected values: no new standalone Python queue engine.
# EN:   Expected values: capped root-domain decisions return skip receipts.
# EN:   Error values: sleeping inside this adapter or creating parallel in-memory
# EN:   queue truth.
# EN:   because the worker must be able to skip capped domains and ask frontier
# EN:   for another eligible row without duplicating durable queue state.
# TR: QUEUE_SYSTEM_DESIGN / yalın queue sözleşmesi
# TR:   Beklenen doğru değerler: yeni bağımsız Python queue motoru yok.
# TR:   Beklenen doğru değerler: capped root-domain kararları skip receipt döndürür.
# TR:   Hata değerleri: bu adapter içinde uyumak veya paralel memory queue doğrusu
# TR:   oluşturmak.
# TR:   Çünkü worker capped domainleri atlayıp durable queue state'i çoğaltmadan
# TR:   frontier'dan başka eligible satır isteyebilmelidir.

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from .logisticsearch1_1_0_3_visit_policy_runtime import (
    build_queue_scheduling_decision,
    derive_normalized_root_domain,
)


# EN: LOCAL VALUE EXPLANATION / CLAIM_URL_KEYS
# EN:   Meaning: accepted field names for URL text in loose claimed-row payloads.
# EN:   Expected values: canonical_url first, then url/seed/source/href fallbacks.
# EN:   Error values: silently accepting an empty URL as claimable work.
# EN:   because claim payload shapes may be dataclass-like or dict-like.
# TR: YEREL DEĞER AÇIKLAMASI / CLAIM_URL_KEYS
# TR:   Anlamı: gevşek claimed-row payloadları içinde URL metni için kabul edilen
# TR:   alan adlarıdır.
# TR:   Beklenen doğru değerler: önce canonical_url, sonra url/seed/source/href
# TR:   fallback alanları.
# TR:   Hata değerleri: boş URL'yi sessizce claim edilebilir iş saymak.
# TR:   Çünkü claim payload şekilleri dataclass benzeri veya dict benzeri olabilir.
CLAIM_URL_KEYS = (
    "canonical_url",
    "url",
    "seed_url",
    "source_url",
    "href",
)


# EN: LOCAL VALUE EXPLANATION / CLAIM_TIME_KEYS
# EN:   Meaning: runtime DB-derived time fields that may arrive with a claimed row.
# EN:   Expected values: datetime objects or ISO-style strings.
# EN:   Error values: writing these values back to JSON.
# EN:   because dynamic visit state belongs to DB/runtime state, not catalog JSON.
# TR: YEREL DEĞER AÇIKLAMASI / CLAIM_TIME_KEYS
# TR:   Anlamı: claimed row ile gelebilecek DB/runtime kaynaklı zaman alanlarıdır.
# TR:   Beklenen doğru değerler: datetime nesneleri veya ISO tarzı stringler.
# TR:   Hata değerleri: bu değerleri JSON'a geri yazmak.
# TR:   Çünkü dinamik ziyaret state catalog JSON'a değil DB/runtime state'e aittir.
CLAIM_TIME_KEYS = (
    "host_next_eligible_at",
    "next_eligible_at",
    "url_next_fetch_at",
    "next_fetch_at",
    "url_revisit_not_before",
    "revisit_not_before",
    "last_visit_at",
    "last_success_at",
)


# EN: LOCAL VALUE EXPLANATION / SKIP_CAPPED_DOMAIN_QUEUE_ACTION
# EN:   Meaning: explicit adapter-side receipt action for capped root-domain rows.
# EN:   Expected values: the helper action string skip_domain_select_next_eligible.
# EN:   Error values: sleeping in the adapter or silently continuing with a capped row.
# EN:   because worker orchestration must request another eligible frontier row instead of waiting.
# TR: YEREL DEĞER AÇIKLAMASI / SKIP_CAPPED_DOMAIN_QUEUE_ACTION
# TR:   Anlamı: capped root-domain satırları için açık adapter-side receipt aksiyonudur.
# TR:   Beklenen doğru değerler: helper aksiyon string'i skip_domain_select_next_eligible.
# TR:   Hata değerleri: adapter içinde uyumak veya capped satırla sessizce devam etmek.
# TR:   Çünkü worker orkestrasyonu beklemek yerine başka eligible frontier satırı istemelidir.
SKIP_CAPPED_DOMAIN_QUEUE_ACTION = "skip_domain_select_next_eligible"


def _mapping_get(payload: Any, key: str, default: Any = None) -> Any:
    if isinstance(payload, Mapping):
        return payload.get(key, default)

    return getattr(payload, key, default)


def first_present_value(payload: Any, keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = _mapping_get(payload, key)
        if value is not None and str(value).strip() != "":
            return value

    return None


def parse_runtime_datetime(value: Any) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    text = str(value).strip()
    if not text:
        return None

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed


def extract_claimed_url_text(claimed_payload: Any) -> str:
    value = first_present_value(claimed_payload, CLAIM_URL_KEYS)
    if value is None:
        return ""

    return str(value).strip()


def extract_policy_mapping(payload: Any, *keys: str) -> dict[str, Any]:
    for key in keys:
        value = _mapping_get(payload, key)
        if isinstance(value, Mapping):
            return dict(value)

    return {}


def build_policy_context_from_claimed_payload(claimed_payload: Any) -> dict[str, Any]:
    url = extract_claimed_url_text(claimed_payload)
    normalized_root_domain = derive_normalized_root_domain(url)

    host_next_eligible_at = parse_runtime_datetime(
        first_present_value(claimed_payload, ("host_next_eligible_at", "next_eligible_at"))
    )
    url_next_fetch_at = parse_runtime_datetime(
        first_present_value(claimed_payload, ("url_next_fetch_at", "next_fetch_at"))
    )
    url_revisit_not_before = parse_runtime_datetime(
        first_present_value(claimed_payload, ("url_revisit_not_before", "revisit_not_before"))
    )
    last_visit_at = parse_runtime_datetime(
        first_present_value(claimed_payload, ("last_visit_at", "last_success_at"))
    )

    return {
        "url": url,
        "normalized_root_domain": normalized_root_domain,
        "seed_policy": extract_policy_mapping(claimed_payload, "seed_policy", "seed_metadata"),
        "surface_policy": extract_policy_mapping(claimed_payload, "surface_policy", "surface_metadata"),
        "family_policy": extract_policy_mapping(claimed_payload, "family_policy", "family_metadata"),
        "host_next_eligible_at": host_next_eligible_at,
        "url_next_fetch_at": url_next_fetch_at,
        "url_revisit_not_before": url_revisit_not_before,
        "last_visit_at": last_visit_at,
    }


def build_worker_frontier_policy_receipt(
    *,
    now: datetime,
    claimed_payload: Any,
    retry_after_seconds: int | None = None,
    error_backoff_seconds: int | None = None,
    soft_limit_backoff_seconds: int | None = None,
) -> dict[str, Any]:
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    context = build_policy_context_from_claimed_payload(claimed_payload)
    url = context["url"]

    if not url:
        return {
            "worker_frontier_policy_adapter_version": "worker_frontier_policy_adapter.v1",
            "adapter_result": "reject_empty_url",
            "queue_should_claim_now": False,
            "queue_should_skip_domain": True,
            "queue_action": "reject_claim_without_url",
            "sleep_on_capped_domain": False,
        }

    decision = build_queue_scheduling_decision(
        now=now,
        url=url,
        seed_policy=context["seed_policy"],
        surface_policy=context["surface_policy"],
        family_policy=context["family_policy"],
        host_next_eligible_at=context["host_next_eligible_at"],
        url_next_fetch_at=context["url_next_fetch_at"],
        url_revisit_not_before=context["url_revisit_not_before"],
        last_visit_at=context["last_visit_at"],
        retry_after_seconds=retry_after_seconds,
        error_backoff_seconds=error_backoff_seconds,
        soft_limit_backoff_seconds=soft_limit_backoff_seconds,
    )

    if decision.get("queue_should_skip_domain") and not decision.get("queue_action"):
        decision = {
            **decision,
            "queue_action": SKIP_CAPPED_DOMAIN_QUEUE_ACTION,
        }

    return {
        **decision,
        "worker_frontier_policy_adapter_version": "worker_frontier_policy_adapter.v1",
        "adapter_result": "policy_decision_built",
        "adapter_reads_claim_payload": True,
        "adapter_writes_db": False,
        "adapter_fetches_public_url": False,
        "adapter_mutates_catalog_json": False,
    }


def should_worker_skip_claimed_payload(
    *,
    now: datetime,
    claimed_payload: Any,
) -> bool:
    receipt = build_worker_frontier_policy_receipt(
        now=now,
        claimed_payload=claimed_payload,
    )

    return bool(receipt.get("queue_should_skip_domain"))
