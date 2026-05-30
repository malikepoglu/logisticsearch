# Crawler Core Request Identity and User-Agent Token Map

Gate: `FULL_R4_P2C76L_REQUEST_IDENTITY_AND_USER_AGENT_TOKEN_MAP_DOC_LOCAL_ONLY_R1`
Image item: `4_OF_5_HTTP_3XX_REDIRECT_HANDLING_REMAINING_DEBT`
Created at: `2026-05-30T19:29:13+02:00`
Canonical head: `de786956657992f50b3bac31dd1df93a529e3488`
Canonical subject: `fix(crawler-core): cast targeted claim worker metadata`

## 1. Purpose

This document records where crawler_core request identity information lives, which layer is responsible for carrying it, and how the current `LogisticSearchBot` identity should be renamed to `LS` without misrepresenting crawler_core as Chrome, Googlebot, Bingbot, or any third-party crawler.

## 2. Current verified live state

| Check | Value |
|---|---|
| pi51c head | `de786956657992f50b3bac31dd1df93a529e3488` |
| pi51c subject | `fix(crawler-core): cast targeted claim worker metadata` |
| service state | `inactive` / enabled `disabled` |
| crawler/browser process count | `0` / `0` |
| raw evidence | `6084` files / `812212036` bytes |
| control state/version | `pause` / `81` |
| max fetch_attempt_id | `1920` |
| new attempts after 1918 | `2` |

## 3. DB source of truth

The request identity token currently comes from the PostgreSQL runtime DB, not from a hard-coded Python default.

### 3.1 Token distribution

```json
[
  {
    "host_count": 722,
    "user_agent_token": "LogisticSearchBot"
  }
]
```

Interpretation: all currently audited live host rows use `LogisticSearchBot` as `frontier.host.user_agent_token`. The intended replacement token is `LS`.

### 3.2 Token-bearing schema columns

```json
[
  {
    "column_name": "user_agent_token",
    "data_type": "text",
    "table_name": "host",
    "table_schema": "frontier"
  }
]
```

Interpretation: the only token-bearing DB column found by this audit is `frontier.host.user_agent_token`.

### 3.3 Robots cache token schema

```json
{
  "robots_cache_regclass": "http_fetch.robots_txt_cache",
  "robots_token_columns": []
}
```

Interpretation: `http_fetch.robots_txt_cache` exists but has no user-agent token column in this audit. Robots behavior may still depend on runtime request headers, but the token is not stored in robots cache as a separate token field.

## 4. File and layer map

| Layer | File / surface | Identity information in that layer | Mutation policy |
|---|---|---|---|
| DB source | `frontier.host.user_agent_token` | Stores the active crawler token per host. Current value: `LogisticSearchBot`; desired value: `LS`. | Change by controlled DB migration only. |
| Claim gateway | `makpi51crawler/python_live_runtime/logisticsearch1_1_1_3_frontier_gateway.py` | Carries host identity from DB into the claimed URL payload: `user_agent_token`, `robots_mode`, `authority_key`, scheme/host/port. | Python change only if claim payload contract changes. |
| Worker runtime | `makpi51crawler/python_live_runtime/logisticsearch1_1_2_worker_runtime.py` | Receives claimed URL payload and routes work through static/browser acquisition. | Python change only if payload handoff or acquisition branching changes. |
| Static HTTP acquisition | `makpi51crawler/python_live_runtime/logisticsearch1_1_2_4_acquisition_runtime.py` | The first place to inspect for actual static HTTP headers and `User-Agent` construction. | Python change only if header construction policy changes. |
| Browser acquisition | `makpi51crawler/python_live_runtime/logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime.py` | The first place to inspect for Playwright/Chromium/browser context identity, extra headers, navigation behavior, and browser-like signals. | Python change only if browser identity policy changes. |
| Robots gateway | `makpi51crawler/python_live_runtime/logisticsearch1_1_1_4_robots_gateway.py` | The first place to inspect robots policy and robots-fetch identity behavior. | Python change only if robots request identity changes. |
| Fetch finalize | `makpi51crawler/python_live_runtime/logisticsearch1_1_2_5_fetch_finalize_runtime.py` | Does not decide identity; records terminal fetch outcomes. Relevant for proving what happened after identity was used. | Do not change for token rename. |

## 5. File evidence snippets

### 5.x frontier claim gateway: `makpi51crawler/python_live_runtime/logisticsearch1_1_1_3_frontier_gateway.py`

- SHA256: `88eed768687025d86275fbb37e8e46d891fb478790cdde95d077b6d5432481be`
- Lines: `1719`

```text
146: # EN: FRONTIER HELPER PURPOSE MEMORY BLOCK V5 / claim_next_url
149: # EN: - because frontier-specific DB truth for 'claim_next_url' should be exposed through one named helper boundary
167: # TR: FRONTIER YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / claim_next_url
170: # TR: - çünkü 'claim_next_url' için frontier’e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
189: # EN: FRONTIER GATEWAY FUNCTION PURPOSE MEMORY BLOCK V7 / claim_next_url
199: # EN: - conn => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
200: # EN: - worker_id => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
201: # EN: - lease_seconds => explicit frontier-gateway input parameter of claim_next_url; this value is part of the visible DB-helper contract of this function
202: # TR: FRONTIER GATEWAY FUNCTION AMAÇ HAFIZA BLOĞU V7 / claim_next_url
212: # TR: - conn => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
213: # TR: - worker_id => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
214: # TR: - lease_seconds => claim_next_url fonksiyonunun açık frontier-gateway girdi parametresidir; bu değer fonksiyonun görünür DB-helper sözleşmesinin parçasıdır
270:         "authority_key",
271:         "robots_mode",
272:         "user_agent_token",
341:     target_url_ids unset so frontier.claim_next_url(...) remains the canonical
346:     target_url_ids değerini boş bırakır; frontier.claim_next_url(...) kanonik
384: def claim_next_url(
407:                 FROM frontier.claim_next_url(
452:                         h.authority_key,
453:                         h.user_agent_token,
454:                         h.robots_mode,
538:                     c.authority_key,
539:                     c.user_agent_token,
540:                     c.robots_mode
```

### 5.x worker runtime: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_worker_runtime.py`

- SHA256: `071e925e0abdd3d044d6e3a0ce789838f92d1e367e91e332aa0746405470bd6f`
- Lines: `2332`

```text
15: - coordinate visible phase boundaries such as runtime control, claim, robots, fetch, parse, finalize, and release style outcomes
27: - narrower worker submodules below provide lease, robots, acquisition, parse, finalize, and storage details
36: - phase-boundary payloads => visible handoff meaning between robots, fetch, parse, finalize, and release steps
65: - runtime control, claim, robots, fetch, parse, finalize ve release tarzı sonuçlar arasındaki görünür faz sınırlarını koordine eder
77: - alttaki daha dar worker altmodülleri lease, robots, acquisition, parse, finalize ve storage ayrıntılarını sağlar
86: - phase-boundary payloadları => robots, fetch, parse, finalize ve release adımları arasındaki görünür devir anlamı
105: # EN: flow, while lower children own support/finalize/robots/lease logic.
108: # TR: tutar; daha alt çocuklar ise support/finalize/robots/lease mantığını sahiplenir.
196:     claim_next_url,
199:     compute_robots_allow_decision,
200:     compute_robots_refresh_decision,
219: # EN: chooses HTTP/browser child fetch paths inline. Instead it asks the canonical
223: # TR: veya browser çocuk fetch yollarını inline seçmez. Bunun yerine doğru fetch
262:     finalize_robots_block,
268: # EN: We import the robots child because robots decision helpers no longer belong
270: # TR: Robots karar yardımcıları artık parent orchestration modülü içinde inline
271: # TR: durmaması gerektiği için robots alt yüzeyini içe aktarıyoruz.
272: from .logisticsearch1_1_2_3_worker_robots_runtime import (
273:     refresh_robots_cache_if_needed,
274:     robots_verdict_allows_fetch,
343:     # EN: worker_id is the textual worker identity passed into frontier.claim_next_url(...).
344:     # TR: worker_id frontier.claim_next_url(...) içine verilen metinsel worker kimliğidir.
372: # EN: - visible field set currently detected here: run_id, claimed, claimed_url, robots_allow_decision, storage_plan, fetched_page, finalize_result, parse_apply_result, observed_at, runtime_control
389: # TR: - burada şu an tespit edilen görünür alan kümesi: run_id, claimed, claimed_url, robots_allow_decision, storage_plan, fetched_page, finalize_result, parse_apply_result, observed_at, runtime_control
416:     # EN: robots_allow_decision stores the visible robots allow/block decision
418:     # TR: robots_allow_decision claim başarılıysa görünür robots allow/block
420:     robots_allow_decision: dict | None
455: # EN: storage gate -> runtime control gate -> claim -> robots gate/refresh ->
459: # TR: storage kapısı -> runtime control kapısı -> claim -> robots kapısı/refresh ->
582: # PLAYWRIGHT_BROWSER_ERROR_CLASSIFICATION_R2_BEGIN
583: def _logisticsearch_classify_browser_runtime_error(
590:     EN: Browser/navigation failures are ordinary web-crawl facts, not unknown
593:     TR: Browser/navigation hataları sıradan web-crawl gerçekleridir, bilinmeyen
602:     browser_patterns: tuple[tuple[str, str, bool], ...] = (
603:         ("err_ssl_version_or_cipher_mismatch", "browser_ssl_version_or_cipher_mismatch", True),
604:         ("err_ssl_protocol_error", "browser_ssl_protocol_error", True),
605:         ("err_cert_common_name_invalid", "browser_cert_common_name_invalid", True),
606:         ("err_cert_date_invalid", "browser_cert_date_invalid", True),
607:         ("err_name_not_resolved", "browser_dns_name_not_resolved", True),
608:         ("err_http2_protocol_error", "browser_http2_protocol_error", True),
609:         ("timeout 30000ms exceeded", "browser_navigation_timeout", True),
610:         ("page.goto: timeout", "browser_navigation_timeout", True),
611:         ("net::err_connection_reset", "browser_connection_reset", True),
612:         ("net::err_connection_closed", "browser_connection_closed", True),
613:         ("net::err_connection_refused", "browser_connection_refused", True),
614:         ("net::err_timed_out", "browser_network_timeout", True),
615:         ("net::err_too_many_redirects", "browser_too_many_redirects", True),
618:     for raw_pattern, error_class, retryable in browser_patterns:
622:     if "playwright" in evidence or "page.goto" in evidence:
623:         return "browser_navigation_error", True
649:     """Return conservative retry_wait backoff for browser/runtime acquisition errors.
651:     EN: DNS, SSL, certificate and browser protocol failures are usually not
653:     TR: DNS, SSL, sertifika ve browser protokol hataları çoğu zaman birkaç
658:         "browser_dns_name_not_resolved": 86400,
659:         "browser_ssl_version_or_cipher_mismatch": 604800,
660:         "browser_ssl_protocol_error": 604800,
661:         "browser_cert_common_name_invalid": 604800,
662:         "browser_cert_date_invalid": 604800,
663:         "browser_http2_protocol_error": 21600,
664:         "browser_navigation_timeout": 21600,
670: # PLAYWRIGHT_BROWSER_ERROR_CLASSIFICATION_R2_END
680:     EN: Playwright navigation timeouts, SSL/cipher negotiation failures, network
681:     transient browser acquisition errors and Python timeout/socket/URL errors are
685:     TR: Playwright navigation timeout, SSL/cipher negotiation hataları, geçici
686:     browser/network acquisition hataları ve Python timeout/socket/URL hataları
691:     _error_class, retryable = _logisticsearch_classify_browser_runtime_error(
734:     error_class = _logisticsearch_classify_browser_runtime_error(
740:     # EN: This branch handles recoverable browser/runtime acquisition exceptions.
742:     # TR: Bu dal toparlanabilir browser/runtime acquisition exception durumlarını işler.
762:     # EN: Runtime/browser acquisition exceptions must create durable
766:     # TR: Runtime/browser acquisition exception durumları frontier.retry_wait
933:             robots_allow_decision=None,
977:                 robots_allow_decision=None,
1013:             # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
1024:             # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
1040:                 robots_allow_decision=None,
1075:                 robots_allow_decision=None,
1097:         claimed_url = claim_next_url(
1115:                 robots_allow_decision=None,
1126:         # EN: It runs after frontier.claim_next_url(...) returned a row and before robots
```

### 5.x static acquisition runtime: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_4_acquisition_runtime.py`

- SHA256: `ceeeaccd8a98342984e338a3b26d92825cf73171be593299d43495a84b8f38f5`
- Lines: `1232`

```text
8: - because acquisition_method selection, acquisition_execution meaning, static vs dynamic path choice, browser vs http branching, and fetched-page production boundaries must remain readable
15: - keep acquisition semantics separate from broader worker orchestration, lease handling, robots policy, parse logic, and storage logic
20: - it does not become the entire browser implementation by itself
32: - acquisition_method => values such as http_page, browser_page, or None when no real acquisition method is chosen
47: - vague browser/http helper dump
57: - çünkü acquisition_method seçimi, acquisition_execution anlamı, static vs dynamic yol tercihi, browser vs http dal seçimi ve fetched-page üretim sınırları okunabilir kalmalıdır
64: - acquisition semantiklerini daha geniş worker orkestrasyonundan, lease yönetiminden, robots policy mantığından, parse mantığından ve storage mantığından ayrı tutar
69: - browser implementasyonunun tamamı tek başına olmaz
81: - acquisition_method => http_page, browser_page veya gerçek acquisition method seçilmediğinde None gibi değerler
96: - belirsiz browser/http helper çöplüğü
124: # EN: - random browser/http helper pile
146: # TR: - rastgele browser/http helper yığını
184:     FetchedRobotsTxtResult,
185:     build_browser_rendered_storage_path,
186:     build_browser_screenshot_storage_path,
188:     build_raw_robots_storage_path,
205: # EN: We re-export the robots acquisition child because the acquisition family
206: # EN: still includes robots work in the same stable public surface.
207: # TR: Acquisition ailesi aynı kararlı public yüzey içinde robots işini de
208: # TR: taşımaya devam ettiği için robots acquisition alt yüzeyini yeniden dışa
210: from .logisticsearch1_1_2_4_5_robots_txt_acquisition_runtime import (
211:     decode_robots_body,
212:     fetch_robots_txt_to_raw_storage,
213:     parse_robots_txt_text,
216: # EN: We re-export the browser-backed page-acquisition child because some callers
217: # EN: still need the direct browser adapter explicitly.
218: # TR: Bazı çağıranlar doğrudan browser adapter'ına açık biçimde ihtiyaç duymaya
219: # TR: devam ettiği için browser-backed page-acquisition alt yüzeyini yeniden dışa
221: from .logisticsearch1_1_2_4_4_browser_page_acquisition_runtime import (
222:     fetch_page_with_browser_to_raw_storage,
223:     infer_browser_document_status,
227: # EN: or direct-fetch surfaces instead of browser-first HTML pages.
228: # TR: Bu sonekler, URL hedeflerinin browser-first HTML sayfaları yerine doğrudan
262: # EN: - visible field set currently detected here: target_url, strategy, url_kind, reason, browser_fallback_allowed, browser_required
265: # EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
268: # EN: - visible http vs browser vs no-method distinction is especially important here
281: # TR: - burada şu an tespit edilen görünür alan kümesi: target_url, strategy, url_kind, reason, browser_fallback_allowed, browser_required
284: # TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
287: # TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
310:     # EN: browser_fallback_allowed tells the executor whether an HTTP exception
311:     # EN: may escalate into a browser-backed retry.
312:     # TR: browser_fallback_allowed, yürütücünün bir HTTP istisnasını browser-backed
314:     browser_fallback_allowed: bool
316:     # EN: browser_required records whether the plan intentionally starts with browser.
317:     # TR: browser_required planın bilinçli olarak browser ile başlayıp başlamadığını kaydeder.
318:     browser_required: bool
339: # EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
342: # EN: - visible http vs browser vs no-method distinction is especially important here
358: # TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
361: # TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
566:     return normalized_text in {"1", "true", "yes", "y", "on", "browser", "required"}
646:     # EN: Fragment-driven targets are browser-oriented because the visible document
648:     # TR: Fragment-tabanlı hedefler browser odaklıdır; çünkü görünür belge çoğu zaman
651:         return "browser_oriented_html"
660: # EN: 1) explicit browser flags win,
662: # EN: 3) normal page-like URLs start with HTTP and may fall back to browser on transport failure.
665: # TR: 1) açık browser bayrakları kazanır,
667: # TR: 3) normal sayfa-benzeri URL'ler HTTP ile başlar ve taşıma hatasında browser'a düşebilir.
683: # EN: - this surface likely deals with acquisition method choice, fetch execution, or browser/http route meaning
686: # EN: - visible http vs browser vs no-method distinction is especially important here
710: # TR: - bu yüzey büyük ihtimalle acquisition method seçimi, fetch execution veya browser/http yol anlamı ile ilgilenir
713: # TR: - görünür http vs browser vs no-method ayrımı burada özellikle önemlidir
730:     # EN: target_url is the canonical fetch target used by both HTTP and browser paths.
731:     # TR: target_url hem HTTP hem browser yollarının kullandığı kanonik fetch hedefidir.
734:     # EN: force_browser records the strongest explicit browser request.
735:     # TR: force_browser en güçlü açık browser isteğini kaydeder.
736:     force_browser = _read_optional_bool_flag(
739:             "force_browser",
740:             "browser_required",
741:             "requires_browser",
742:             "use_browser",
746:     # EN: prefer_browser records a softer browser preference that still deserves
747:     # EN: browser-first execution in this early implementation.
748:     # TR: prefer_browser daha yumuşak bir browser tercihidir; ancak bu erken
749:     # TR: implementasyonda yine de browser-first yürütmeyi hak eder.
750:     prefer_browser = _read_optional_bool_flag(
753:             "prefer_browser",
754:             "browser_preferred",
775:     # EN: Explicit browser demand wins unless the caller also explicitly demanded
777:     # TR: Açık browser talebi, çağıran aynı anda açıkça HTTP-only de istemediyse
```

### 5.x browser dynamic acquisition runtime: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime.py`

- SHA256: `dfb8a0188b8f8f71deb648597b3a9c187e8a362311632a3e5f264de19d2ae552`
- Lines: `1013`

```text
3: This file is the dynamic-browser acquisition child inside the broader acquisition family.
7: - because some pages cannot be understood by plain HTTP alone and need a browser-driven dynamic corridor
8: - because browser startup, navigation, rendering, dynamic DOM state, browser-side timeout handling, and rendered-page shaping must remain readable in one narrow child
9: - because a beginner should be able to answer where the crawler handles JavaScript-rendered or browser-required acquisition work
13: - expose the browser-dynamic acquisition boundaries
14: - keep browser-driven request/navigation/render semantics readable
16: - keep degraded dynamic-browser outcomes visible instead of hiding them
23: - it does not turn browser failure into fake success
27: - acquisition parent can delegate here when dynamic browser execution is required
28: - this child owns browser-driven render/navigation style work that is narrower than the full parent but broader than plain support utilities
33: - browser-execution helper values => visible indicators that a browser-style corridor ran
34: - rendered page or browser result payloads => dynamic acquisition outputs prepared for later validation or parse use
35: - timeout/error/degraded branches => explicit non-happy browser outcomes that must remain readable
36: - acquisition_method-related meaning => browser-oriented selection signals, often feeding later browser-page style downstream logic
40: - dynamic-browser acquisition child
42: - readable browser-required acquisition boundary
46: - vague browser utility dump
52: Bu dosya daha geniş acquisition ailesinin içindeki dynamic-browser acquisition child yüzeyidir.
56: - çünkü bazı sayfalar yalnızca plain HTTP ile anlaşılamaz ve browser güdümlü dynamic koridora ihtiyaç duyar
57: - çünkü browser başlatma, navigation, rendering, dynamic DOM durumu, browser tarafı timeout işleme ve render edilmiş sayfa şekillendirme tek bir dar child yüzeyde okunabilir kalmalıdır
58: - çünkü yeni başlayan biri crawlerın JavaScript-rendered veya browser-gerekli acquisition işini tam olarak nerede yaptığını anlayabilmelidir
62: - browser-dynamic acquisition sınırlarını açığa çıkarır
63: - browser güdümlü request/navigation/render semantiklerini okunabilir tutar
65: - degraded dynamic-browser sonuçlarını gizlemek yerine görünür tutar
72: - browser başarısızlığını sahte başarıya çevirmez
76: - dynamic browser çalıştırması gerektiğinde acquisition parent bu child yüzeye delegasyon yapabilir
77: - bu child parent yüzeyden daha dar, plain support utility yüzeylerinden daha geniş browser güdümlü render/navigation işini taşır
82: - browser-execution yardımcı değerleri => browser tarzı koridorun çalıştığını gösteren görünür işaretler
83: - render edilmiş sayfa veya browser sonuç payloadları => sonraki validation veya parse kullanımına hazırlanan dynamic acquisition çıktıları
84: - timeout/error/degraded dallar => okunabilir kalması gereken mutlu-yol-dışı browser sonuçları
85: - acquisition_method ile ilgili anlam => sonraki browser-page tarzı downstream mantığına besleme yapan browser-yönelimli seçim işaretleri
89: - dynamic-browser acquisition child
91: - okunabilir browser-gerekli acquisition sınırı
95: - belirsiz browser utility çöplüğü
101: # EN: BROWSER DYNAMIC ACQUISITION IDENTITY MEMORY BLOCK V6
103: # EN: This file should be read as the browser-required dynamic child inside the acquisition family.
106: # EN: - this child runs browser-driven dynamic work
107: # EN: - it exists so the crawler can later answer which rendered-page corridor ran, what browser-driven result came back, and how that result was shaped
110: # EN: - named dynamic-browser acquisition child
111: # EN: - focused rendered-page and browser-execution surface
115: # EN: - random browser helper pile
117: # EN: - place where dynamic browser failures become invisible
120: # EN: - browser-driven outputs should stay explicit
122: # EN: - degraded browser branches must remain visible
123: # TR: BROWSER DYNAMIC ACQUISITION KIMLIK HAFIZA BLOĞU V6
125: # TR: Bu dosya acquisition ailesinin içindeki browser-gerekli dynamic child gibi okunmalıdır.
128: # TR: - bu child browser güdümlü dynamic işi çalıştırır
129: # TR: - crawlerın daha sonra hangi render edilmiş sayfa koridorunun çalıştığını, hangi browser sonucunun geldiğini ve bu sonucun nasıl şekillendiğini cevaplayabilmesi için vardır
132: # TR: - isimli dynamic-browser acquisition child
133: # TR: - odaklı render edilmiş sayfa ve browser-execution yüzeyi
137: # TR: - rastgele browser helper yığını
139: # TR: - dynamic browser hatalarının görünmez olduğu yer
142: # TR: - browser güdümlü çıktılar açık kalmalıdır
144: # TR: - degraded browser dalları görünür kalmalıdır
148: # EN: We import dataclass helpers because this first canonical browser-acquisition
151: # TR: İlk kanonik browser-acquisition yüzeyi gevşek ve dağınık sözlükler yerine
166: # EN: This first real browser-acquisition surface uses Playwright's sync API
169: # TR: Bu ilk gerçek browser-acquisition yüzeyi Playwright'ın sync API'sini
173: from playwright.sync_api import Page, Response, sync_playwright
178: # EN: During systemd stop, Playwright's subprocess transport may otherwise be
180: # EN: context, browser, and the sync_playwright manager explicitly and suppress
182: # TR: systemd stop sırasında Playwright subprocess transport, Python event loop
184: # TR: üretebilir. Bu yüzden page, context, browser ve sync_playwright manager
187: def _logisticsearch_is_known_playwright_shutdown_close_noise(exc: BaseException) -> bool:
195:         "browser has been closed",
196:         "browser closed",
201:         "playwright connection closed",
206: def _logisticsearch_close_playwright_resource_quietly(resource: object, label: str) -> None:
219:         if _logisticsearch_is_known_playwright_shutdown_close_noise(exc):
224: def _logisticsearch_stop_sync_playwright_manager_quietly(manager: object) -> None:
237:         if _logisticsearch_is_known_playwright_shutdown_close_noise(exc):
243: # EN: This dataclass stores one observed public browser-network response in a
245: # TR: Bu dataclass gözlenen bir public browser-network response'unu dar ve
247: # EN: REAL-RULE AST REPAIR / CLASS BrowserNetworkRecord
248: # EN: BrowserNetworkRecord is an explicit browser-dynamic acquisition runtime data shape.
249: # TR: REAL-RULE AST REPAIR / SINIF BrowserNetworkRecord
250: # TR: BrowserNetworkRecord acik bir browser-dynamic acquisition runtime veri seklidir.
252: # EN: BROWSER DYNAMIC CLASS PURPOSE MEMORY BLOCK V6 / BrowserNetworkRecord
255: # EN: - because browser-dynamic acquisition truth for 'BrowserNetworkRecord' should be carried by a named structure instead of anonymous loose payload passing
256: # EN: - because beginners should inspect field names and understand rendered/browser-side role meaning directly
```

### 5.x robots gateway: `makpi51crawler/python_live_runtime/logisticsearch1_1_1_4_robots_gateway.py`

- SHA256: `3aac486a49a510a2e1232edc9d30baaaedc98b15e4b1f84d794f633f007d167a`
- Lines: `828`

```text
3: This file is the robots child of the state DB gateway family.
7: - because robots-specific DB truth should live behind one explicit named gateway child
8: - because upper layers should ask named Python helpers about robots truth instead of repeating raw SQL semantics
9: - because allow/block/cache/refresh style robots visibility is a separate concern from runtime-control and frontier claim logic
13: - expose robots-oriented DB helper boundaries
14: - expose named helpers for reading or updating robots-related truth
28: - this file sits in the middle for robots-specific DB truth
29: - worker/controller layers above call these helpers instead of embedding raw robots SQL ideas
34: - user_agent or agent identity text => robots policy evaluation identity
35: - robots_txt_url or robots target identity => the robots resource being reasoned about
36: - allow/block verdict visibility => structured robots decision meaning
37: - cache / refresh / stale visibility => whether existing robots truth is reused or should be refreshed
42: - robots truth gateway
44: - readable robots contract boundary
54: Bu dosya state DB gateway ailesinin robots child yüzeyidir.
58: - çünkü robots’a özgü DB doğrusu tek ve açık isimli gateway child yüzeyi arkasında yaşamalıdır
59: - çünkü üst katmanlar ham SQL semantiğini tekrar etmek yerine robots doğrusunu isimli Python yardımcıları üzerinden sormalıdır
60: - çünkü allow/block/cache/refresh tarzı robots görünürlüğü runtime-control ve frontier claim mantığından ayrı bir konudur
64: - robots odaklı DB yardımcı sınırlarını açığa çıkarır
65: - robots ile ilgili doğruları okumak veya güncellemek için isimli yardımcılar sunar
79: - robots’a özgü DB doğrusu için bu dosya ortadadır
80: - üstteki worker/controller katmanları ham robots SQL fikrini gömmek yerine bu yardımcıları çağırır
85: - user_agent veya agent kimlik metni => robots policy değerlendirme kimliği
86: - robots_txt_url veya robots hedef kimliği => hakkında düşünülen robots kaynağı
87: - allow/block verdict görünürlüğü => yapılı robots karar anlamı
88: - cache / refresh / stale görünürlüğü => mevcut robots doğrusunun yeniden kullanılıp kullanılmadığı veya yenilenmesi gerekip gerekmediği
93: - robots truth gateway
95: - okunabilir robots sözleşme sınırı
105: # EN: This module is the robots child of the state DB gateway family.
106: # EN: It owns only robots allow/refresh/cache DB wrappers.
107: # TR: Bu modül state DB gateway ailesinin robots alt yüzeyidir.
108: # TR: Yalnızca robots allow/refresh/cache DB wrapper'larını taşır.
110: # EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in __future__ -> annotations.
111: # EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
114: # TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
115: # TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
124: # EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in typing -> Any.
125: # EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
128: # TR: STAGE21-AUTO-COMMENT :: Bu import satırı typing -> Any ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
129: # TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
136: # EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in psycopg.
137: # EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
140: # TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
141: # TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
148: # EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in psycopg.rows -> dict_row.
149: # EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
152: # TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg.rows -> dict_row ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
153: # TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
161: # EN: This helper converts a robots SQL wrapper no-row condition into an
163: # EN: with honest unresolved robots state instead of crashing or silently drifting.
164: # TR: Bu yardımcı robots SQL wrapper no-row durumunu operatörün görebileceği
166: # TR: sessiz mantık kaymasına düşmeden dürüst çözülmemiş robots durumu ile ilerler.
167: # EN: ROBOTS HELPER PURPOSE MEMORY BLOCK V5 / build_robots_no_row_payload
170: # EN: - because robots-specific DB truth for 'build_robots_no_row_payload' should be exposed through one named helper boundary
171: # EN: - because upper layers should call a readable robots helper name instead of repeating raw robots SQL semantics
174: # EN: - the explicit parameters of this helper are: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message
175: # EN: - values should match the current Python signature and the live robots SQL contract below
178: # EN: - a robots-oriented result shape defined by the current function body and DB truth
181: # EN: Common robots meaning hints:
182: # EN: - this helper likely exposes one named robots-specific DB-truth boundary
186: # EN: - forcing upper layers to understand raw robots SQL semantics instead of this helper contract
187: # TR: ROBOTS YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / build_robots_no_row_payload
190: # TR: - çünkü 'build_robots_no_row_payload' için robots’a özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
191: # TR: - çünkü üst katmanlar ham robots SQL semantiğini tekrar etmek yerine okunabilir robots yardımcı adı çağırmalıdır
194: # TR: - bu yardımcının açık parametreleri şunlardır: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message
195: # TR: - değerler aşağıdaki mevcut Python imzası ve canlı robots SQL sözleşmesi ile uyumlu olmalıdır
198: # TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen robots-odaklı sonuç şekli
201: # TR: Ortak robots anlam ipuçları:
202: # TR: - bu yardımcı büyük ihtimalle robots’a özgü isimli bir DB-truth sınırını açığa çıkarır
206: # TR: - üst katmanları bu yardımcı sözleşmesi yerine ham robots SQL semantiğini anlamaya zorlamak
208: # EN: STAGE21-AUTO-COMMENT :: This robots gateway function named build_robots_no_row_payload defines a visible contract point for policy lookup or policy shaping.
209: # EN: STAGE21-AUTO-COMMENT :: A reader should understand which host or URL policy build_robots_no_row_payload reads, how it interprets it, and what safe result it returns.
210: # EN: STAGE21-AUTO-COMMENT :: When editing build_robots_no_row_payload, verify that caller expectations, database truth, and worker semantics remain aligned.
211: # EN: STAGE21-AUTO-COMMENT :: This marker keeps the entry point easy to find during robots-policy audits.
212: # TR: STAGE21-AUTO-COMMENT :: build_robots_no_row_payload isimli bu robots gateway fonksiyonu politika okuma veya politika biçimlendirme için görünür bir sözleşme noktası tanımlar.
213: # TR: STAGE21-AUTO-COMMENT :: Okuyucu build_robots_no_row_payload fonksiyonunun hangi host veya URL politikasını okuduğunu, bunu nasıl yorumladığını ve hangi güvenli sonucu döndürdüğünü anlayabilmelidir.
214: # TR: STAGE21-AUTO-COMMENT :: build_robots_no_row_payload düzenlenirken çağıran beklentilerinin, veritabanı gerçeğinin ve worker anlamının hizalı kaldığı doğrulanmalıdır.
215: # TR: STAGE21-AUTO-COMMENT :: Bu işaret giriş noktasını robots politika denetimlerinde kolay bulunur halde tutar.
216: # EN: REAL-RULE AST REPAIR / DEF build_robots_no_row_payload
217: # EN: build_robots_no_row_payload is an explicit robots-gateway helper/runtime contract.
```

### 5.x fetch finalize runtime: `makpi51crawler/python_live_runtime/logisticsearch1_1_2_5_fetch_finalize_runtime.py`

- SHA256: `ab3102e6d269012d0bb0ff22ff6ff468444d996054d8f25e34d1e3135e0bb99f`
- Lines: `2290`

```text
8: - because success, blocked_robots, retryable_error, permanent_error, timeout, and network_error branches must remain readable and auditable
9: - because a beginner should be able to find where a fetch attempt becomes durably finalized without digging through unrelated lease, robots, acquisition, or parse phases
32: - outcome => values such as success, blocked_robots, retryable_error, permanent_error, timeout, or network_error
57: - çünkü success, blocked_robots, retryable_error, permanent_error, timeout ve network_error dalları okunabilir ve denetlenebilir kalmalıdır
58: - çünkü yeni başlayan biri bir fetch attemptin nerede kalıcı olarak finalize edildiğini ilgisiz lease, robots, acquisition veya parse fazları arasında kaybolmadan bulabilmelidir
81: - outcome => success, blocked_robots, retryable_error, permanent_error, timeout veya network_error gibi değerler
387:         "redirect_target_authority_key": f"{host}:{port}",
490:     target_authority_key = str(redirect_policy.get("redirect_target_authority_key") or f"{target_host}:{target_port}").strip()
516:                   p_authority_key := %s,
533:                     target_authority_key,
1129: # EN: This helper finalizes a robots-blocked claim as a permanent outcome.
1130: # TR: Bu yardımcı robots tarafından engellenen bir claim’i permanent sonuç olarak
1132: # EN: FETCH FINALIZE FUNCTION PURPOSE MEMORY BLOCK V6 / finalize_robots_block
1135: # EN: - because fetch-finalize truth for 'finalize_robots_block' should be exposed through one named top-level helper boundary
1139: # EN: - the explicit parameters of this function are: conn, claimed_url, robots_allow_decision, worker_id
1159: # TR: FETCH FINALIZE FUNCTION AMAÇ HAFIZA BLOĞU V6 / finalize_robots_block
1162: # TR: - çünkü 'finalize_robots_block' için fetch-finalize doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
1166: # TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, robots_allow_decision, worker_id
1187: # EN: REAL-RULE AST REPAIR / DEF finalize_robots_block
1188: # EN: finalize_robots_block is an explicit fetch-finalize runtime/helper contract.
1189: # EN: Parameters kept explicit here: conn, claimed_url, robots_allow_decision, worker_id.
1190: # TR: REAL-RULE AST REPAIR / FONKSIYON finalize_robots_block
1191: # TR: finalize_robots_block acik bir fetch-finalize runtime/helper sozlesmesidir.
1192: # TR: Burada acik tutulan parametreler: conn, claimed_url, robots_allow_decision, worker_id.
1193: def finalize_robots_block(
1197:     robots_allow_decision: dict | None,
1202:     # EN: REAL-RULE AST REPAIR / LOCAL finalize_robots_block / url_id
1204:     # TR: REAL-RULE AST REPAIR / YEREL finalize_robots_block / url_id
1207:     # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / lease_token
1217:     # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / lease_token
1231:     verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")
1232:     # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / error_message
1234:     # EN: and reviewable intermediate value instead of hiding `f"robots verdict forbids fetch: {verdict}"` inline.
1242:     # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / error_message
1252:     error_message = f"robots verdict forbids fetch: {verdict}"
1257:     # EN: REAL-RULE AST REPAIR / LOCAL finalize_robots_block / fetch_attempt_log
1259:     # TR: REAL-RULE AST REPAIR / YEREL finalize_robots_block / fetch_attempt_log
1265:         outcome="blocked_robots",
1266:         note="worker runtime robots-blocked finalize path",
1269:         error_class="robots_blocked",
1279:         # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result
1281:         # EN: and reviewable intermediate value instead of hiding `finish_fetch_permanent_error( conn, url_id=url_id, lease_token=lease_token, http_status=None, error_class="robots_blocked", error_message=er` inline.
1289:         # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result
1304:             error_class="robots_blocked",
1307:         # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result_payload
1317:         # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result_payload
1332:         # EN: LOCAL VALUE EXPLANATION / finalize_robots_block / finalize_result_payload
1334:         # EN: and reviewable intermediate value instead of hiding `build_finalize_no_row_payload( url_id=url_id, lease_token=lease_token, http_status=None, error_class="robots_blocked_finalize_no_row", error` inline.
1342:         # TR: YEREL DEĞER AÇIKLAMASI / finalize_robots_block / finalize_result_payload
1356:             error_class="robots_blocked_finalize_no_row",
2286:     "finalize_robots_block",
```

## 6. Rename decision

The safe rename is a DB-token rename, not a browser impersonation. The system should identify itself as `LS`, keep robots respect behavior intact, and avoid misrepresenting crawler_core as Googlebot, Bingbot, Chrome, or a human browser.

Required controlled rename sequence:

1. Read-only preflight: verify repo/live clean, service inactive/disabled, crawler/browser process zero, and `frontier.host.user_agent_token = 'LogisticSearchBot'` count matches expected host count.
2. DB mutation gate: update only `frontier.host.user_agent_token` from `LogisticSearchBot` to `LS`; no raw delete, no DB reset, no crawler start.
3. Post-mutation seal: verify old token count zero, new token count equals prior old-token count, service/process/raw stillness unchanged.
4. Optional smoke: run a tiny controlled fetch later and confirm claim payload shows `user_agent_token: LS`.

## 7. Hard safety rules

- Do not disguise crawler_core as Chrome, Googlebot, Bingbot, or another third-party bot.
- Do not change robots policy as part of this token rename.
- Do not reset crawler DB or delete raw evidence for this rename.
- Do not start systemd service for the rename.
- Do not alter 26 catalog JSON files for this rename.
- Treat static HTTP identity and browser identity as separate surfaces; document both before optimizing fingerprint behavior.

