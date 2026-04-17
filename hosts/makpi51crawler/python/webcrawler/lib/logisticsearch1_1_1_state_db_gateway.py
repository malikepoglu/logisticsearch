# EN: This module is now the thin parent hub of the state DB gateway family.
# EN: Its job is to preserve the stable import surface used by upper crawler
# EN: layers while delegating real DB wrapper bodies into narrower child modules.
# TR: Bu modül artık state DB gateway ailesinin ince parent hub yüzeyidir.
# TR: Görevi, üst crawler katmanlarının kullandığı kararlı import yüzeyini
# TR: korurken gerçek DB wrapper gövdelerini daha dar alt modüllere devretmektir.

from __future__ import annotations

# EN: We re-export the gateway-support child so callers can keep using the same
# EN: connection helpers and ClaimedUrl row shape through the stable parent hub.
# TR: Çağıranlar aynı bağlantı yardımcılarını ve ClaimedUrl satır şeklini kararlı
# TR: parent hub üzerinden kullanmaya devam edebilsin diye gateway-support alt
# TR: yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_1_gateway_support import (
    ClaimedUrl,
    _row_to_claimed_url,
    close_db,
    commit,
    connect_db,
    rollback,
)

# EN: We re-export the runtime-control child.
# TR: Runtime-control alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_2_runtime_control_gateway import (
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)

# EN: We re-export the frontier child.
# TR: Frontier alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_3_frontier_gateway import (
    claim_next_url,
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    finish_fetch_success,
    release_parse_pending_to_queued,
    renew_url_lease,
)

# EN: We re-export the robots child.
# TR: Robots alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_4_robots_gateway import (
    compute_robots_allow_decision,
    compute_robots_refresh_decision,
    upsert_robots_txt_cache,
)

# EN: We re-export the fetch-attempt child.
# TR: Fetch-attempt alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_5_fetch_attempt_gateway import (
    log_fetch_attempt_terminal,
)

# EN: We re-export the preranking child.
# TR: Preranking alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_6_preranking_gateway import (
    persist_page_preranking_snapshot,
    persist_taxonomy_preranking_payload,
    upsert_page_workflow_status,
)

# EN: We re-export the discovery child.
# TR: Discovery alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_1_7_discovery_gateway import (
    enqueue_discovered_url,
    fetch_url_discovery_context,
)

# EN: This export list keeps the stable public parent-gateway surface explicit.
# TR: Bu export listesi kararlı public parent-gateway yüzeyini açık tutar.
__all__ = [
    "ClaimedUrl",
    "connect_db",
    "get_webcrawler_runtime_control",
    "webcrawler_runtime_may_claim",
    "set_webcrawler_runtime_control",
    "claim_next_url",
    "renew_url_lease",
    "compute_robots_allow_decision",
    "compute_robots_refresh_decision",
    "upsert_robots_txt_cache",
    "log_fetch_attempt_terminal",
    "finish_fetch_success",
    "release_parse_pending_to_queued",
    "finish_fetch_retryable_error",
    "finish_fetch_permanent_error",
    "rollback",
    "commit",
    "close_db",
    "persist_taxonomy_preranking_payload",
    "persist_page_preranking_snapshot",
    "upsert_page_workflow_status",
    "fetch_url_discovery_context",
    "enqueue_discovered_url",
]
