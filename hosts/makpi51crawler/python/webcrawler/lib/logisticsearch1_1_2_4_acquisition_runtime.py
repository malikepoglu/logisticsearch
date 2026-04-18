# EN: This module is now the thin acquisition-family hub.
# EN: Its job is to preserve the stable import surface expected by worker_runtime
# EN: while delegating real work into narrower child modules below.
# TR: Bu modül artık ince acquisition-aile hub yüzeyidir.
# TR: Görevi, worker_runtime'ın beklediği kararlı import yüzeyini korurken gerçek
# TR: işi aşağıdaki daha dar alt modüllere devretmektir.

from __future__ import annotations

# EN: We re-export the shared support surface so upstream callers can keep using
# EN: the stable acquisition-family contract without knowing the new split layout.
# TR: Yukarı akış çağıranlar yeni split yerleşimini bilmeden acquisition-aile
# TR: sözleşmesini kullanmaya devam edebilsin diye paylaşılan destek yüzeyini
# TR: yeniden dışa aktarıyoruz.
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

# EN: We re-export the direct HTTP page-acquisition child.
# TR: Doğrudan HTTP page-acquisition alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_2_4_2_http_page_acquisition_runtime import (
    fetch_page_to_raw_storage,
)

# EN: We re-export the robots acquisition child.
# TR: Robots acquisition alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_2_2_4_robots_txt_acquisition_runtime import (
    decode_robots_body,
    fetch_robots_txt_to_raw_storage,
    parse_robots_txt_text,
)

# EN: We re-export the browser-backed page-acquisition child.
# TR: Browser-backed page-acquisition alt yüzeyini yeniden dışa aktarıyoruz.
from .logisticsearch1_1_2_2_5_browser_page_acquisition_runtime import (
    fetch_page_with_browser_to_raw_storage,
    infer_browser_document_status,
)

# EN: This export list keeps the stable public acquisition-family surface explicit.
# TR: Bu export listesi kararlı public acquisition-aile yüzeyini açık tutar.
__all__ = [
    "RAW_FETCH_ROOT",
    "FetchedPageResult",
    "FetchedRobotsTxtResult",
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
    "fetch_page_to_raw_storage",
    "decode_robots_body",
    "fetch_robots_txt_to_raw_storage",
    "parse_robots_txt_text",
    "fetch_page_with_browser_to_raw_storage",
    "infer_browser_document_status",
]
