# Crawler Core Error Class Quality Report / Policy Breakdown

- Gate: `FULL_R4_P2C60_ERROR_CLASS_QUALITY_REPORT_DOC_LOCAL_ONLY_R1`
- Image item: `3_OF_5_ERROR_CLASS_QUALITY_REPORT_POLICY_BREAKDOWN`
- Generated UTC: `2026-05-30T12:31:10.311943+00:00`
- Canonical head: `5543d26d9b383b2988793a196bf553c36b6658a1`
- Service state: `inactive` / enabled `disabled`
- Process counts: crawler `0`, browser `0`
- Raw evidence: `6070` files / `808308265` bytes

## Safety Invariants

| Check | Value |
| --- | --- |
| Runtime control | `pause` / state_version `75` |
| Rows with error class | `522` |
| Distinct error classes | `23` |
| Retry-wait lease metadata | `0` |
| Non-retry-wait lease metadata | `0` |

## Global Error Class Breakdown

| last_error_class | total_rows | retry_wait_rows | dead_rows | due_now_rows | future_rows | min_fetch_attempt_count | max_fetch_attempt_count | min_http_status | max_http_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| http_404 | 151 | 0 | 151 | 151 | 0 | 1 | 2 | 404 | 404 |
| browser_navigation_timeout | 98 | 98 | 0 | 97 | 1 | 1 | 3 | 307 | 307 |
| browser_dns_name_not_resolved | 43 | 43 | 0 | 6 | 37 | 1 | 1 |  |  |
| http_3xx_redirect_target_enqueued | 42 | 0 | 42 | 42 | 0 | 1 | 1 | 301 | 308 |
| robots_blocked | 32 | 0 | 32 | 32 | 0 | 1 | 1 |  |  |
| http_403_forbidden | 26 | 0 | 26 | 26 | 0 | 1 | 1 | 403 | 403 |
| browser_navigation_error | 24 | 24 | 0 | 24 | 0 | 2 | 3 | 302 | 503 |
| http_405_client_error | 24 | 0 | 24 | 24 | 0 | 1 | 1 | 405 | 405 |
| browser_cert_common_name_invalid | 18 | 18 | 0 | 0 | 18 | 1 | 1 |  |  |
| browser_http2_protocol_error | 18 | 18 | 0 | 18 | 0 | 1 | 1 |  |  |
| browser_connection_refused | 9 | 9 | 0 | 9 | 0 | 2 | 2 |  |  |
| browser_cert_date_invalid | 8 | 8 | 0 | 0 | 8 | 1 | 1 |  |  |
| http_500_server_error | 7 | 7 | 0 | 7 | 0 | 2 | 3 | 500 | 500 |
| browser_connection_reset | 4 | 4 | 0 | 4 | 0 | 2 | 2 |  |  |
| http_3xx_unresolved_redirect | 4 | 4 | 0 | 4 | 0 | 2 | 2 | 302 | 307 |
| browser_ssl_protocol_error | 2 | 2 | 0 | 0 | 2 | 1 | 1 |  |  |
| browser_ssl_version_or_cipher_mismatch | 2 | 2 | 0 | 0 | 2 | 1 | 1 |  |  |
| http_3xx_no_resolvable_redirect_target | 2 | 0 | 2 | 2 | 0 | 3 | 3 | 302 | 307 |
| http_401_access_denied | 2 | 0 | 2 | 2 | 0 | 1 | 1 | 401 | 401 |
| http_418_client_error | 2 | 0 | 2 | 2 | 0 | 1 | 1 | 418 | 418 |
| runtime_transport_retryable_error | 2 | 2 | 0 | 2 | 0 | 3 | 3 |  |  |
| browser_too_many_redirects | 1 | 1 | 0 | 1 | 0 | 2 | 2 |  |  |
| http_503_server_error | 1 | 1 | 0 | 1 | 0 | 2 | 2 | 503 | 503 |

## Policy Bucket Breakdown

| policy_bucket | row_count | retry_wait_rows | dead_rows | due_now_rows | future_rows | min_fetch_attempt_count | max_fetch_attempt_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BROWSER_RUNTIME_BACKOFF_REVIEW | 227 | 227 | 0 | 159 | 68 | 1 | 3 |
| SOURCE_QUALITY_404_REVIEW | 151 | 0 | 151 | 151 | 0 | 1 | 2 |
| REDIRECT_POLICY_REVIEW | 48 | 4 | 44 | 48 | 0 | 1 | 3 |
| ROBOTS_POLICY_REVIEW | 32 | 0 | 32 | 32 | 0 | 1 | 1 |
| SOURCE_ACCESS_OR_METHOD_REVIEW | 30 | 0 | 30 | 30 | 0 | 1 | 1 |
| OTHER_ERROR_POLICY_REVIEW | 24 | 0 | 24 | 24 | 0 | 1 | 1 |
| SERVER_5XX_BACKOFF_REVIEW | 8 | 8 | 0 | 8 | 0 | 2 | 3 |
| TRANSPORT_RETRYABLE_BACKOFF_REVIEW | 2 | 2 | 0 | 2 | 0 | 3 | 3 |

## Policy Notes

- `BROWSER_RUNTIME_BACKOFF_REVIEW`: `227` rows. Retry/backoff ve browser runtime sınıflandırması izlenmeli; otomatik silme yok.
- `SOURCE_QUALITY_404_REVIEW`: `151` rows. Kaynak/seed kalite borcu; katalog kaynakları tek tek doğrulanmadan toplu silme yok.
- `REDIRECT_POLICY_REVIEW`: `48` rows. 4/5 aşamasında öncelikli hedef; unresolved 3xx ve no-target 3xx ayrımı korunmalı.
- `ROBOTS_POLICY_REVIEW`: `32` rows. Robots kararına saygı; crawl zorlaması yok, sadece kaynak kalite/alternatif kaynak kararı.
- `SOURCE_ACCESS_OR_METHOD_REVIEW`: `30` rows. 403/405/401/418 erişim veya metod uyumsuzluğu; otomatik retry değil kaynak/policy kararı.
- `SERVER_5XX_BACKOFF_REVIEW`: `8` rows. Sunucu kaynaklı geçici hata; backoff korunmalı, kısa aralıkta agresif retry yok.
- `TRANSPORT_RETRYABLE_BACKOFF_REVIEW`: `2` rows. Transport timeout/retryable; kontrollü backoff ve küçük örneklem testi.
- `OTHER_ERROR_POLICY_REVIEW`: `24` rows. Sınıf eşlemesi genişletilecek; önce statik sınıflandırma raporu.

## HTTP Fetch Attempt Error Breakdown

| error_class | row_count | non_success_outcome_rows | success_outcome_rows | min_http_status | max_http_status | min_fetch_attempt_id | max_fetch_attempt_id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| http_404 | 152 | 152 | 0 | 404 | 404 | 1 | 1904 |
| http_3xx_unresolved_redirect | 65 | 65 | 0 | 301 | 308 | 130 | 1915 |
| robots_blocked | 32 | 32 | 0 |  |  | 161 | 1826 |
| http_403_forbidden | 26 | 26 | 0 | 403 | 403 | 192 | 1840 |
| http_405_client_error | 24 | 24 | 0 | 405 | 405 | 328 | 1447 |
| http_500_server_error | 16 | 16 | 0 | 500 | 500 | 70 | 1912 |
| http_503_server_error | 7 | 7 | 0 | 503 | 503 | 436 | 1906 |
| runtime_transport_retryable_error | 6 | 6 | 0 |  |  | 74 | 1913 |
| http_401_access_denied | 2 | 2 | 0 | 401 | 401 | 965 | 968 |
| http_418_client_error | 2 | 2 | 0 | 418 | 418 | 833 | 836 |
| http_3xx_no_resolvable_redirect_target | 1 | 1 | 0 | 302 | 302 | 1916 | 1916 |

## Representative Samples

### `browser_cert_common_name_invalid`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 227 | retry_wait | False |  | 1 | 1 | 0 | https://eski.und.org.tr/tr/26/uyelerimiz | Error: Page.goto: net::ERR_CERT_COMMON_NAME_INVALID at https://eski.und.org.tr/tr/26/uyelerimiz Call log:   - navigating to "https://eski.und.org.tr/tr/26/uyelerimiz", waiting unti |
| 2 | 445 | retry_wait | False |  | 1 | 1 | 0 | https://loglink.com/ | Error: Page.goto: net::ERR_CERT_COMMON_NAME_INVALID at https://loglink.com/ Call log:   - navigating to "https://loglink.com/", waiting until "networkidle"  \| frontier_runtime_exce |
| 3 | 446 | retry_wait | False |  | 1 | 1 | 0 | https://loglink.com/search.asp?m=all&query=Israel&sm=cou&ss=ns | Error: Page.goto: net::ERR_CERT_COMMON_NAME_INVALID at https://loglink.com/search.asp?m=all&query=Israel&sm=cou&ss=ns Call log:   - navigating to "https://loglink.com/search.asp?m= |

### `browser_cert_date_invalid`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 202 | retry_wait | False |  | 1 | 1 | 0 | https://en-shftz.pudong.gov.cn/investment/services/17.shtml | Error: Page.goto: net::ERR_CERT_DATE_INVALID at https://en-shftz.pudong.gov.cn/investment/services/17.shtml Call log:   - navigating to "https://en-shftz.pudong.gov.cn/investment/s |
| 2 | 437 | retry_wait | False |  | 1 | 1 | 0 | https://logiship.vn/ | Error: Page.goto: net::ERR_CERT_DATE_INVALID at https://logiship.vn/ Call log:   - navigating to "https://logiship.vn/", waiting until "networkidle"  \| frontier_runtime_exception_r |
| 3 | 887 | retry_wait | False |  | 1 | 1 | 0 | https://www.bollore-logistics.com/en/country/netherlands/ | Error: Page.goto: net::ERR_CERT_DATE_INVALID at https://www.bollore-logistics.com/en/country/netherlands/ Call log:   - navigating to "https://www.bollore-logistics.com/en/country/ |

### `browser_connection_refused`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1005 | retry_wait | True |  | 2 | 2 | 0 | https://www.cifa.org.cn/ | Error: Page.goto: net::ERR_CONNECTION_REFUSED at https://www.cifa.org.cn/ Call log:   - navigating to "https://www.cifa.org.cn/", waiting until "networkidle"  \| frontier_runtime_ex |
| 2 | 1198 | retry_wait | True |  | 2 | 2 | 0 | https://www.fois.indianrail.gov.in/FOISWebPortal/index.jsp | Error: Page.goto: net::ERR_CONNECTION_REFUSED at https://www.fois.indianrail.gov.in/FOISWebPortal/index.jsp Call log:   - navigating to "https://www.fois.indianrail.gov.in/FOISWebP |
| 3 | 1199 | retry_wait | True |  | 2 | 2 | 0 | https://www.fois.indianrail.gov.in/RailSAHAY/index.jsp | Error: Page.goto: net::ERR_CONNECTION_REFUSED at https://www.fois.indianrail.gov.in/RailSAHAY/index.jsp Call log:   - navigating to "https://www.fois.indianrail.gov.in/RailSAHAY/in |

### `browser_connection_reset`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 124 | retry_wait | True |  | 2 | 2 | 0 | https://catlaiport.com.vn/en | Error: Page.goto: net::ERR_CONNECTION_RESET at https://catlaiport.com.vn/en Call log:   - navigating to "https://catlaiport.com.vn/en", waiting until "networkidle"  \| frontier_runt |
| 2 | 1519 | retry_wait | True |  | 2 | 2 | 0 | https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx | Error: Page.goto: net::ERR_CONNECTION_RESET at https://www.indiapost.gov.in/_layouts/15/dop.portal.tracking/trackconsignment.aspx Call log:   - navigating to "https://www.indiapost |
| 3 | 1917 | retry_wait | True |  | 2 | 2 | 0 | https://www.snowman.in/ | Error: Page.goto: net::ERR_CONNECTION_RESET at https://www.snowman.in/ Call log:   - navigating to "https://www.snowman.in/", waiting until "networkidle"  \| frontier_runtime_except |

### `browser_dns_name_not_resolved`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 26 | retry_wait | True |  | 1 | 1 | 0 | https://allportcargoservices.com/ | Error: Page.goto: net::ERR_NAME_NOT_RESOLVED at https://allportcargoservices.com/ Call log:   - navigating to "https://allportcargoservices.com/", waiting until "networkidle"  \| fr |
| 2 | 27 | retry_wait | True |  | 1 | 1 | 0 | https://alsc.com.vn/ | Error: Page.goto: net::ERR_NAME_NOT_RESOLVED at https://alsc.com.vn/ Call log:   - navigating to "https://alsc.com.vn/", waiting until "networkidle"  \| frontier_runtime_exception_r |
| 3 | 99 | retry_wait | True |  | 1 | 1 | 0 | https://barcelona-air-cargo.com/ | Error: Page.goto: net::ERR_NAME_NOT_RESOLVED at https://barcelona-air-cargo.com/ Call log:   - navigating to "https://barcelona-air-cargo.com/", waiting until "networkidle"  \| fron |

### `browser_http2_protocol_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1100 | retry_wait | True |  | 1 | 1 | 0 | https://www.dhl.com/bd-en/home.html | Error: Page.goto: net::ERR_HTTP2_PROTOCOL_ERROR at https://www.dhl.com/bd-en/home.html Call log:   - navigating to "https://www.dhl.com/bd-en/home.html", waiting until "networkidle |
| 2 | 1101 | retry_wait | True |  | 1 | 1 | 0 | https://www.dhl.com/bd-en/home/our-divisions/global-forwarding.html | Error: Page.goto: net::ERR_HTTP2_PROTOCOL_ERROR at https://www.dhl.com/bd-en/home/our-divisions/global-forwarding.html Call log:   - navigating to "https://www.dhl.com/bd-en/home/o |
| 3 | 1102 | retry_wait | True |  | 1 | 1 | 0 | https://www.dhl.com/hu-en/home/our-divisions/global-forwarding.html | Error: Page.goto: net::ERR_HTTP2_PROTOCOL_ERROR at https://www.dhl.com/hu-en/home/our-divisions/global-forwarding.html Call log:   - navigating to "https://www.dhl.com/hu-en/home/o |

### `browser_navigation_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 129 | retry_wait | True |  | 2 | 2 | 0 | https://clutch.co/gr/logistics/freight-forwarders | Error: It looks like you are using Playwright Sync API inside the asyncio loop. Please use the Async API instead. \| frontier_runtime_exception_retry_wait_r1=exception_module=playwr |
| 2 | 130 | retry_wait | True |  | 2 | 2 | 0 | https://clutch.co/gr/logistics/supply-chain-management | Error: It looks like you are using Playwright Sync API inside the asyncio loop. Please use the Async API instead. \| frontier_runtime_exception_retry_wait_r1=exception_module=playwr |
| 3 | 133 | retry_wait | True |  | 2 | 2 | 0 | https://clutch.co/jp/logistics/3pls | Error: It looks like you are using Playwright Sync API inside the asyncio loop. Please use the Async API instead. \| frontier_runtime_exception_retry_wait_r1=exception_module=playwr |

### `browser_navigation_timeout`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 127 | retry_wait | True |  | 2 | 2 | 0 | https://clutch.co/cz/logistics/freight-forwarders | TimeoutError: Page.goto: Timeout 30000ms exceeded. Call log:   - navigating to "https://clutch.co/cz/logistics/freight-forwarders", waiting until "networkidle"  \| frontier_runtime_ |
| 2 | 131 | retry_wait | True |  | 2 | 2 | 0 | https://clutch.co/in/logistics/air-freight-companies | TimeoutError: Page.goto: Timeout 30000ms exceeded. Call log:   - navigating to "https://clutch.co/in/logistics/air-freight-companies", waiting until "networkidle"  \| frontier_runti |
| 3 | 136 | retry_wait | True |  | 1 | 1 | 0 | https://clutch.co/jp/logistics/distribution-companies | TimeoutError: Page.goto: Timeout 30000ms exceeded. Call log:   - navigating to "https://clutch.co/jp/logistics/distribution-companies", waiting until "networkidle"  \| frontier_runt |

### `browser_ssl_protocol_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 106 | retry_wait | False |  | 1 | 1 | 0 | https://biek.de/ | Error: Page.goto: net::ERR_SSL_PROTOCOL_ERROR at https://biek.de/ Call log:   - navigating to "https://biek.de/", waiting until "networkidle"  \| frontier_runtime_exception_retry_wa |
| 2 | 107 | retry_wait | False |  | 1 | 1 | 0 | https://biek.de/mitglieder.html | Error: Page.goto: net::ERR_SSL_PROTOCOL_ERROR at https://biek.de/mitglieder.html Call log:   - navigating to "https://biek.de/mitglieder.html", waiting until "networkidle"  \| front |

### `browser_ssl_version_or_cipher_mismatch`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1598 | retry_wait | False |  | 1 | 1 | 0 | https://www.lfs-lb.org/ | Error: Page.goto: net::ERR_SSL_VERSION_OR_CIPHER_MISMATCH at https://www.lfs-lb.org/ Call log:   - navigating to "https://www.lfs-lb.org/", waiting until "networkidle"  \| frontier_ |
| 2 | 1599 | retry_wait | False |  | 1 | 1 | 0 | https://www.lfs-lb.org/directory-f/ | Error: Page.goto: net::ERR_SSL_VERSION_OR_CIPHER_MISMATCH at https://www.lfs-lb.org/directory-f/ Call log:   - navigating to "https://www.lfs-lb.org/directory-f/", waiting until "n |

### `browser_too_many_redirects`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1809 | retry_wait | True |  | 2 | 2 | 0 | https://www.pqa.gov.pk/en/port-operations | Error: Page.goto: net::ERR_TOO_MANY_REDIRECTS at https://www.pqa.gov.pk/en/port-operations Call log:   - navigating to "https://www.pqa.gov.pk/en/port-operations", waiting until "n |

### `http_3xx_no_resolvable_redirect_target`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1003 | dead | True | 307 | 3 | 2 | 1 | https://www.chamber.org.il/en/ | HTTP status 307 is not a parseable success \| p2c34_http_3xx_redirect_policy: 3xx response has no actionable redirect target; redirect_location empty or unavailable and final_url di |
| 2 | 1732 | dead | True | 302 | 3 | 2 | 1 | https://www.paginasamarillas.es/ | HTTP status 302 is not a parseable success \| p2c44_fetch_attempt_3xx_class_alignment: redirect_location empty or unavailable and final_url did not change |

### `http_3xx_redirect_target_enqueued`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 162 | dead | True | 308 | 1 | 0 | 1 | https://corcel.com.ua/en/our-services/logistics-services/ | HTTP status 308 is not a parseable success \| p1k_http_3xx_redirect_target_policy_v1: redirect target queued/reused |
| 2 | 168 | dead | True | 302 | 1 | 0 | 1 | https://customs.gov.bd/portal/services | HTTP status 302 is not a parseable success \| p1k_http_3xx_redirect_target_policy_v1: redirect target queued/reused |
| 3 | 372 | dead | True | 301 | 1 | 0 | 1 | https://home.kuehne-nagel.com/en/-/locations/bangladesh | HTTP status 301 is not a parseable success \| p1k_http_3xx_redirect_target_policy_v1: redirect target queued/reused |

### `http_3xx_unresolved_redirect`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1733 | retry_wait | True | 302 | 2 | 2 | 0 | https://www.paginasamarillas.es/search/agencias-de-transporte/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1 | HTTP status 302 is not a parseable success |
| 2 | 1734 | retry_wait | True | 302 | 2 | 2 | 0 | https://www.paginasamarillas.es/search/transporte-logistica/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1 | HTTP status 302 is not a parseable success |
| 3 | 1774 | retry_wait | True | 307 | 2 | 2 | 0 | https://www.portialtotirreno.it/ | HTTP status 307 is not a parseable success |

### `http_401_access_denied`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1082 | dead | True | 401 | 1 | 0 | 1 | https://www.dellin.ru/cities/ | HTTP status 401 is not a parseable success |
| 2 | 1083 | dead | True | 401 | 1 | 0 | 1 | https://www.dellin.ru/contacts/ | HTTP status 401 is not a parseable success |

### `http_403_forbidden`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 228 | dead | True | 403 | 1 | 0 | 1 | https://exhibitors.transportlogistic.de/ | HTTP status 403 is not a parseable success |
| 2 | 229 | dead | True | 403 | 1 | 0 | 1 | https://exhibitors.transportlogistic.de/en/ | HTTP status 403 is not a parseable success |
| 3 | 230 | dead | True | 403 | 1 | 0 | 1 | https://exhibitors.transportlogistic.de/en/exhibitors-and-directories/exhibitors-brand-names | HTTP status 403 is not a parseable success |

### `http_404`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | dead | True | 404 | 1 | 0 | 1 | https://aeroceanetwork.net/members-directory/ | HTTP status 404 is not a parseable success |
| 2 | 11 | dead | True | 404 | 1 | 0 | 1 | https://aeroceanetwork.net/members/ | HTTP status 404 is not a parseable success |
| 3 | 25 | dead | True | 404 | 1 | 0 | 1 | https://alhagroup.com/en/services/ | HTTP status 404 is not a parseable success |

### `http_405_client_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 374 | dead | True | 405 | 1 | 0 | 1 | https://hu.kompass.com/c/airmax-cargo-budapest-zrt/hu1167024/ | HTTP status 405 is not a parseable success |
| 2 | 375 | dead | True | 405 | 1 | 0 | 1 | https://hu.kompass.com/c/botlik-trans-kft/hu0767072/ | HTTP status 405 is not a parseable success |
| 3 | 376 | dead | True | 405 | 1 | 0 | 1 | https://hu.kompass.com/c/ekol-logistics-kft/hu1219171/ | HTTP status 405 is not a parseable success |

### `http_418_client_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 996 | dead | True | 418 | 1 | 0 | 1 | https://www.cdek.ru/ru/contacts/ | HTTP status 418 is not a parseable success |
| 2 | 997 | dead | True | 418 | 1 | 0 | 1 | https://www.cdek.ru/ru/offices/ | HTTP status 418 is not a parseable success |

### `http_500_server_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 117 | retry_wait | True | 500 | 3 | 3 | 0 | https://caapakistan.com.pk/ | HTTP status 500 is not a parseable success |
| 2 | 118 | retry_wait | True | 500 | 3 | 3 | 0 | https://caapakistan.com.pk/airports.aspx | HTTP status 500 is not a parseable success |
| 3 | 1494 | retry_wait | True | 500 | 2 | 2 | 0 | https://www.icpa.or.kr/eng/content/view.do?menuKey=412 | HTTP status 500 is not a parseable success |

### `http_503_server_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1994 | retry_wait | True | 503 | 2 | 2 | 0 | https://www.uspa.gov.ua/en/homepage-en | HTTP status 503 is not a parseable success |

### `robots_blocked`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 191 | dead | True |  | 1 | 0 | 1 | https://dubaisouth.my.salesforce-sites.com/CompanyDirectory | robots verdict forbids fetch: block |
| 2 | 392 | dead | True |  | 1 | 0 | 1 | https://id.linkedin.com/company/samudera-indonesia | robots verdict forbids fetch: block |
| 3 | 421 | dead | True |  | 1 | 0 | 1 | https://koto.org.tr/ | robots verdict forbids fetch: block |

### `runtime_transport_retryable_error`

| rn | url_id | state | due_now | last_http_status | fetch_attempt_count | retryable_error_count | permanent_error_count | canonical_url | last_error_message_prefix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 121 | retry_wait | True |  | 3 | 3 | 0 | https://cargo.rzd.ru/en/ | URLError: <urlopen error timed out> |
| 2 | 214 | retry_wait | True |  | 3 | 3 | 0 | https://eng.rzd.ru/en/ | URLError: <urlopen error timed out> |

## Item 3 Decision

- Item 3 is a reporting and policy-breakdown item; no DB/runtime cleanup is allowed in this step.
- The next safest technical target is Item 4/5: `REDIRECT_POLICY_REVIEW`, because it is small, bounded, and already separated into `http_3xx_redirect_target_enqueued`, `http_3xx_unresolved_redirect`, and `http_3xx_no_resolvable_redirect_target`.
- Source-quality-heavy groups such as 404, robots, 403/405 and access-denied should not be bulk removal without reviewd; they require later source/seed review, preferably after round-robin startpoint testing.
- Browser runtime failures should remain retry-wait/backoff controlled; they are not deletion candidates.

## Next Gate

`FULL_R4_P2C61_ERROR_CLASS_QUALITY_REPORT_DOC_AUDIT_READONLY_R1`
