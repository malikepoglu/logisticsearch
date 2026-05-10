# TOPIC: Crawler Core Raw Fetch JSON Zstandard Envelope / Crawler Core Ham Fetch JSON Zstandard Zarfı

## EN — Purpose

This document seals the first raw-fetch JSON envelope design for crawler_core duration tests.

Crawler_core already stores raw body evidence under `/srv/webcrawler/raw_fetch/`. The new rule keeps that existing evidence unchanged and creates a compressed sidecar JSON envelope beside each fetched page body. The sidecar uses Zstandard compression through the system `zstd` CLI and uses the extension `.fetch.json.zst`.

The goal is operational inspection during 15-minute, 1-hour, overnight, and later 24-hour tests without printing full HTML to the terminal and without changing the canonical raw JSONL runtime log.

## TR — Amaç

Bu belge crawler_core süre testleri için ilk ham-fetch JSON zarf tasarımını mühürler.

Crawler_core zaten ham body kanıtlarını `/srv/webcrawler/raw_fetch/` altında saklıyor. Yeni kural mevcut kanıtı değiştirmeden her fetch edilen sayfa body dosyasının yanına sıkıştırılmış bir JSON zarf sidecar dosyası üretir. Sidecar Zstandard sıkıştırmasını sistemdeki `zstd` CLI ile yapar ve `.fetch.json.zst` uzantısını kullanır.

Amaç, 15 dakika, 1 saat, overnight ve daha sonra 24 saatlik testlerde içerik ve disk kullanımını inceleyebilmek; bunu yaparken terminale tam HTML basmamak ve canonical raw JSONL runtime log sözleşmesini değiştirmemektir.

## EN — Storage contract

Crawler-core raw fetch evidence:

- Required root: `/srv/webcrawler/raw_fetch/`
- Existing body evidence remains unchanged: `.body.bin` and `.rendered.html`
- New sidecar evidence: `.fetch.json.zst`
- The sidecar contains JSON before compression.
- The JSON contains decoded HTML text including tags when decoding is possible.
- Raw JSONL stdout/stderr logging remains canonical and unchanged.

Pause rule:

- Pause if `/srv/webcrawler/raw_fetch` is unusable or effectively full.
- Pause if both parse-core downstream paths are unusable or effectively full:
  - primary: `/srv/data`
  - fallback: `/srv/buffer`

## TR — Storage sözleşmesi

Crawler-core ham fetch kanıtı:

- Zorunlu kök: `/srv/webcrawler/raw_fetch/`
- Mevcut body kanıtı değişmeden kalır: `.body.bin` ve `.rendered.html`
- Yeni sidecar kanıtı: `.fetch.json.zst`
- Sidecar sıkıştırma öncesinde JSON içerir.
- JSON, decode edilebildiği durumda HTML taglerini koruyan metin içerir.
- Raw JSONL stdout/stderr log sözleşmesi kanonik kalır ve değişmez.

Pause kuralı:

- `/srv/webcrawler/raw_fetch` kullanılamazsa veya fiilen doluysa pause.
- Parse-core downstream yollarının ikisi de kullanılamazsa veya fiilen doluysa pause:
  - primary: `/srv/data`
  - fallback: `/srv/buffer`

## EN — Exact schema identity

The exact schema_version value is `logisticsearch.raw_fetch.envelope.v1`.

## TR — Exact schema kimliği

Exact schema_version değeri `logisticsearch.raw_fetch.envelope.v1` olmalıdır.

## EN — JSON envelope v1

Required top-level fields:

- `schema_version`
- `compression`
- `url_id`
- `host_id`
- `requested_url`
- `final_url`
- `http_status`
- `content_type`
- `content_encoding`
- `body_bytes`
- `body_sha256`
- `raw_body_path`
- `raw_json_uncompressed_bytes`
- `fetched_at`
- `html`
- `html_decode_strategy`
- `storage_policy`
- `crawler_metadata`

The envelope must not store DSN, passwords, lease tokens, or user-agent tokens.

## TR — JSON zarf v1

Zorunlu üst alanlar:

- `schema_version`
- `compression`
- `url_id`
- `host_id`
- `requested_url`
- `final_url`
- `http_status`
- `content_type`
- `content_encoding`
- `body_bytes`
- `body_sha256`
- `raw_body_path`
- `raw_json_uncompressed_bytes`
- `fetched_at`
- `html`
- `html_decode_strategy`
- `storage_policy`
- `crawler_metadata`

Zarf DSN, parola, lease token veya user-agent token saklamamalıdır.

## EN — First implementation rule

The first implementation deliberately creates a sidecar file and does not widen `FetchedPageResult`. This preserves the existing DB/log contract while allowing runtime tests to inspect compressed JSON content.

The sidecar is critical evidence for the JSON+Zstd test phase. If sidecar creation fails during the patch-test phase, the test must fail visibly instead of silently pretending that JSON evidence exists.

## TR — İlk uygulama kuralı

İlk uygulama bilinçli olarak sidecar dosya üretir ve `FetchedPageResult` sözleşmesini genişletmez. Böylece mevcut DB/log sözleşmesi korunurken runtime testlerinde sıkıştırılmış JSON içerik incelenebilir.

Sidecar, JSON+Zstd test fazı için kritik kanıttır. Patch-test fazında sidecar üretimi başarısız olursa test sessizce JSON kanıtı varmış gibi davranmamalı; görünür biçimde fail etmelidir.

## EN — Next validation gates

1. Static audit: AST, import, helper, sidecar call, and doc checks.
2. Commit/push/sync only after static audit passes.
3. Small runtime smoke to verify `.fetch.json.zst` generation.
4. 15-minute foreground duration test with bounded live activity.
5. Read-only post-seal with decompression, JSON validation, HTML tag evidence, and compression ratio.
6. 24-hour test remains blocked until the 15-minute JSON+Zstd post-seal passes.

## TR — Sonraki doğrulama kapıları

1. Static audit: AST, import, helper, sidecar çağrısı ve doküman kontrolleri.
2. Static audit PASS olmadan commit/push/sync yok.
3. `.fetch.json.zst` üretimini doğrulayan küçük runtime smoke.
4. Bounded live activity ile 15 dakikalık foreground süre testi.
5. Decompression, JSON doğrulama, HTML tag kanıtı ve sıkıştırma oranı içeren read-only post-seal.
6. 15 dakikalık JSON+Zstd post-seal PASS olmadan 24 saatlik test blokludur.

## EN — 15-minute comparison mode and 24-hour zstd-only mode

For the 15-minute validation test, crawler_core writes both sibling files:

- `.fetch.json`
- `.fetch.json.zst`

This is temporary and exists only to compare readable JSON content, compressed size, disk usage, and HTML tag preservation.

For the later 24-hour system-limit test, crawler_core must keep only `.fetch.json.zst` raw evidence by running with:

`LOGISTICSEARCH_RAW_FETCH_PLAIN_JSON_COMPARE_MODE=0`

The 24-hour test does not need terminal live activity lines because pi51c must be able to continue independently if Ubuntu Desktop is shut down.

## TR — 15 dakikalık karşılaştırma modu ve 24 saatlik yalnız zstd modu

15 dakikalık doğrulama testinde crawler_core iki kardeş dosyayı birlikte yazar:

- `.fetch.json`
- `.fetch.json.zst`

Bu geçicidir; okunabilir JSON içeriğini, sıkıştırılmış boyutu, disk kullanımını ve HTML tag korunmasını karşılaştırmak içindir.

Sonraki 24 saatlik sistem-limit testinde crawler_core yalnız `.fetch.json.zst` ham kanıtını tutmalıdır. Bunun için çalışma şu env ile yapılır:

`LOGISTICSEARCH_RAW_FETCH_PLAIN_JSON_COMPARE_MODE=0`

24 saatlik testte terminal live activity satırları gerekli değildir; çünkü pi51c, Ubuntu Desktop kapatılsa bile bağımsız devam edebilmelidir.

## Terminal HTML safety rule

Do not print HTML to terminal. Terminal output must remain bounded live summary text only; full fetched HTML belongs inside the raw fetch JSON/Zstandard evidence artifact.

## Crawler core raw-evidence responsibility

crawler_core is a raw evidence collector, not a filtering stage. Its job in this validation line is to absorb available page content like a sponge and preserve HTML tags inside the raw fetch JSON/Zstandard evidence.

Filtering, sieving, semantic selection, enrichment, normalization, and search-ready shaping belong to later phases such as parse_core and desktop_import, not to crawler_core.

For the 15-minute validation test only, crawler_core keeps both `.fetch.json` and `.fetch.json.zst` so compression ratio, content shape, and disk usage can be compared, and the terminal may show bounded live activity summaries.

For the 24-hour/system-limit test, crawler_core should write only `.fetch.json.zst` raw evidence and does not need terminal live activity lines, because pi51c must continue independently after Ubuntu Desktop may be shut down.

## Exact 24h raw-evidence file rule / Kesin 24h ham-kanıt dosya kuralı

- EN: For 24h/system-limit tests, write only .fetch.json.zst files; do not write .fetch.json comparison files.
- TR: 24 saatlik/sistem-limit testlerinde yalnızca .fetch.json.zst dosyaları yazılır; .fetch.json karşılaştırma dosyaları yazılmaz.
- EN: 15-minute validation is the temporary exception: it writes both .fetch.json and .fetch.json.zst so compression ratio and content can be compared.
- TR: 15 dakikalık doğrulama geçici istisnadır: sıkıştırma oranı ve içerik kıyaslanabilsin diye hem .fetch.json hem .fetch.json.zst yazar.

