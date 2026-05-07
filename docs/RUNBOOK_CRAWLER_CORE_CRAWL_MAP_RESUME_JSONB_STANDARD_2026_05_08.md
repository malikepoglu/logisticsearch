# RUNBOOK — Crawler Core Crawl Map / Resume JSONB Standard — 2026-05-08

## 1. EN: Purpose / TR: Amaç

EN: This runbook defines how crawler_core should use `frontier.url.url_metadata` as a lightweight JSONB context layer without duplicating PostgreSQL runtime truth.

TR: Bu runbook, crawler_core’un `frontier.url.url_metadata` alanını PostgreSQL runtime gerçeğini kopyalamadan hafif bir JSONB bağlam katmanı olarak nasıl kullanacağını tanımlar.

## 2. EN: Authority boundary / TR: Otorite sınırı

EN: PostgreSQL columns remain the durable truth for scheduling, graph topology, leases, success state, retries, and resume safety.

TR: Zamanlama, graph topolojisi, lease, başarı durumu, retry ve güvenli resume için dayanıklı gerçek PostgreSQL kolonlarıdır.

EN: JSONB stores only why/how/context hints: crawl-map labels, discovery surface, checkpoint phase, and policy hints.

TR: JSONB yalnızca neden/nasıl/bağlam ipuçlarını taşır: crawl-map etiketleri, discovery yüzeyi, checkpoint fazı ve policy ipuçları.

## 3. EN: Required schema marker / TR: Zorunlu şema işareti

EN: Every managed metadata object should use `schema_version: crawler_url_metadata.v1`.

TR: Yönetilen her metadata nesnesi `schema_version: crawler_url_metadata.v1` kullanmalıdır.

## 4. EN: Allowed sections / TR: İzin verilen bölümler

EN: `crawl_map` may contain `root_url_id`, `branch_role`, `branch_label`, and `crawl_path_hint`.

TR: `crawl_map`, `root_url_id`, `branch_role`, `branch_label` ve `crawl_path_hint` içerebilir.

EN: `discovered_from` may contain `surface`, `source_url_id`, `link_text_normalized`, `selector_hint`, and `source_content_type`.

TR: `discovered_from`, `surface`, `source_url_id`, `link_text_normalized`, `selector_hint` ve `source_content_type` içerebilir.

EN: `resume` may contain `last_checkpoint_phase`, `last_checkpoint_at`, `last_worker_id`, and `last_safe_resume_action`.

TR: `resume`, `last_checkpoint_phase`, `last_checkpoint_at`, `last_worker_id` ve `last_safe_resume_action` içerebilir.

EN: `policy` may contain `crawl_reason`, `robots_allowed`, `nofollow_seen`, `noindex_seen`, and `politeness_bucket`.

TR: `policy`, `crawl_reason`, `robots_allowed`, `nofollow_seen`, `noindex_seen` ve `politeness_bucket` içerebilir.

## 5. EN: State interpretation / TR: Durum yorumu

EN: `queued` means the URL is durably waiting. It may be claimed only when `next_fetch_at` is due.

TR: `queued`, URL’nin dayanıklı şekilde beklediğini gösterir. Yalnızca `next_fetch_at` zamanı geldiyse claim edilebilir.

EN: `leased` means work is in flight. A valid lease must not be duplicated.

TR: `leased`, işin devam ettiğini gösterir. Geçerli lease duplicate edilmemelidir.

EN: `parse_pending` means fetch completed and parse_core should process the raw capture or release it through a controlled transition.

TR: `parse_pending`, fetch’in tamamlandığını ve parse_core’un raw capture verisini işlemesi ya da kontrollü geçişle serbest bırakması gerektiğini gösterir.

EN: `retry_wait` means backoff is active. The crawler must preserve `next_fetch_at` until the retry time is due.

TR: `retry_wait`, backoff’un aktif olduğunu gösterir. Crawler retry zamanı gelene kadar `next_fetch_at` değerini korumalıdır.

## 6. EN: Non-goals / TR: Kapsam dışı

EN: This runbook does not create SQL files, database patches, DB mutations, service changes, or crawler starts.

TR: Bu runbook SQL dosyası, database patch’i, DB mutation, servis değişikliği veya crawler start oluşturmaz.

EN: Do not create or resurrect `sql/`, `makpi51crawler/sql/`, `patch_manifests/`, or `runtime_changes/`.

TR: `sql/`, `makpi51crawler/sql/`, `patch_manifests/` veya `runtime_changes/` oluşturulmaz ve geri getirilmez.

## 7. EN: Naming distinction / TR: İsim ayrımı

EN: `logisticsearch_crawler` is the live PostgreSQL logical database name.

TR: `logisticsearch_crawler`, canlı PostgreSQL mantıksal veritabanı adıdır.

EN: `crawler_core` is the repository topology key for the crawler PostgreSQL manifest surface.

TR: `crawler_core`, crawler PostgreSQL manifest yüzeyi için repo topoloji anahtarıdır.

EN: `http_raw_capture.v1.json` and `frontier_queue.v1.json` are manifests, not databases and not raw body stores.

TR: `http_raw_capture.v1.json` ve `frontier_queue.v1.json` manifesttir; veritabanı veya raw body deposu değildir.

## 8. EN: Safety checklist / TR: Güvenlik kontrol listesi

EN: Before any future runtime mutation, verify HEAD/origin alignment, exact dirty scope, zero tracked `.sql` files, forbidden paths absent, service inactive/disabled, and crawler process count zero.

TR: Gelecekteki her runtime mutation öncesinde HEAD/origin hizası, tam dirty scope, sıfır tracked `.sql` dosyası, yasak path yokluğu, servisin inactive/disabled olması ve crawler process count sıfır doğrulanmalıdır.


## 9. EN: R115 enqueue conflict preservation decision / TR: R115 enqueue conflict koruma kararı

EN: R115_R5C selected `frontier.enqueue_discovered_url` as the first patch target for URL queue correctness.

TR: R115_R5C, URL kuyruğu doğruluğu için ilk patch hedefi olarak `frontier.enqueue_discovered_url` fonksiyonunu seçti.

EN: The current conflict branch can rewrite `next_fetch_at` to `now()` for rediscovered successful queued URLs. This can make already-successful URLs immediately due again.

TR: Mevcut conflict branch, yeniden keşfedilen başarılı queued URL’lerde `next_fetch_at` değerini `now()` yapabilir. Bu, daha önce başarıyla fetch edilmiş URL’leri hemen tekrar due hale getirebilir.

EN: Required patch invariants: keep `leased` and `parse_pending` protected, preserve `retry_wait` backoff, preserve future schedules for successful queued URLs, and keep new URL inserts immediately crawlable.

TR: Zorunlu patch invariantları: `leased` ve `parse_pending` korunsun, `retry_wait` backoff korunsun, başarılı queued URL’lerin gelecek schedule’ı korunsun ve yeni URL insert’leri hemen crawl edilebilir kalsın.

EN: This runbook entry is not a live DB patch. The live PostgreSQL apply step requires a separate explicit DB mutation gate.

TR: Bu runbook kaydı canlı DB patch’i değildir. Canlı PostgreSQL apply adımı ayrı ve açık bir DB mutation gate gerektirir.


EN: Exact R115 patch invariant wording: Do not overwrite future next_fetch_at for successful queued rows. New URL inserts must remain immediately crawlable.

TR: R115 exact patch invariant ifadesi: başarılı queued URL satırlarında gelecekteki `next_fetch_at` ezilmez. Yeni URL insert’leri hemen crawl edilebilir kalır.
