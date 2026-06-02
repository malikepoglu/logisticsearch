# Service Pipeline and ZSTD Topology Decision / Service Pipeline ve ZSTD Topoloji Kararı

Marker: `KOD_BLOGU_091B_SERVICE_PIPELINE_ZSTD_TOPOLOGY_REPAIRED_TRUTH`

Date: 2026-06-02  
Scope: LogisticSearch crawler runtime topology, raw evidence path truth, `.body.bin`, `.fetch.json.zst`, robots raw body, ZSTD separation, and future C++ compression helper naming.

---

## 1. English summary

The active crawler raw evidence root is:

- `/srv/webcrawler/raw_fetch`

The legacy path below is not the current active raw evidence root and must not be used for new code or new documentation:

- `/srv/crawler/logisticsearch/raw_fetch`

The current crawler raw body artefact is:

- `.body.bin`

The current crawler fetch envelope sidecar artefact is:

- `.fetch.json.zst`

Strict rule:

- `.body.bin = gerçek ham içerik dosyası`
- `.fetch.json.zst = ham içerik hakkında sıkıştırılmış JSON makbuz/envelope`

In English:

- `.body.bin` is the package itself.
- `.fetch.json.zst` is the compressed receipt/envelope for that package.
- `.fetch.json.zst is not the raw response body.`
- `.fetch.json.zst` must not contain a full embedded copy of the `.body.bin` payload.
- `.fetch.json.zst` may reference the `.body.bin` file by path, byte count, checksum, content type, and fetch metadata.

Target architecture:

- crawler_core remains the fetch/raw-evidence collector
- compression moves into a separate worker/service pipeline
- future ZSTD helper work prefers C++
- unused empty worker directories are forbidden
- `makpi51crawler/python_live_runtime/controls/` remains untouched

---

## 2. Türkçe özet

Aktif crawler ham kanıt kökü şudur:

- `/srv/webcrawler/raw_fetch`

Aşağıdaki legacy path güncel aktif ham kanıt kökü değildir ve yeni kod veya yeni dokümantasyon için kullanılmayacaktır:

- `/srv/crawler/logisticsearch/raw_fetch`

Güncel crawler ham body artefact dosyası şudur:

- `.body.bin`

Güncel crawler fetch envelope sidecar artefact dosyası şudur:

- `.fetch.json.zst`

Katı kural:

- `.body.bin = gerçek ham içerik dosyası`
- `.fetch.json.zst = ham içerik hakkında sıkıştırılmış JSON makbuz/envelope`

Türkçe net anlam:

- `.body.bin` paketin kendisidir.
- `.fetch.json.zst` o paketin sıkıştırılmış teslim fişi/envelope dosyasıdır.
- `.fetch.json.zst, ham response body değildir.`
- `.fetch.json.zst`, `.body.bin` payload’unun tamamını içine gömmemelidir.
- `.fetch.json.zst`, `.body.bin` dosyasını path, byte sayısı, checksum, content type ve fetch metadata ile referanslayabilir.

Hedef mimari:

- crawler_core fetch/raw-evidence collector olarak kalır
- compression ayrı worker/service pipeline katmanına taşınır
- gelecekteki ZSTD helper işleri için tercih edilen yüzey C++ olur
- kullanılmayan boş worker dizinleri yasaktır
- `makpi51crawler/python_live_runtime/controls/` olduğu yerde kalır

---

## 3. `.body.bin` contract / `.body.bin` sözleşmesi

### English

`.body.bin` is the raw HTTP response body file.

It is written by crawler_core after an HTTP or browser fetch returns response body bytes.

It is intentionally generic because the crawler does not decide the semantic file type at raw-evidence time.

The inside of `.body.bin` may be:

- HTML text
- JSON API response text
- JavaScript text
- CSS text
- plain text
- XML
- CSV
- PDF bytes
- image bytes
- another raw server response body

The filename says:

- this is a body artefact
- the payload is stored as raw bytes
- the payload has not yet been normalized into parse/ranking/import JSON

Current URL body path pattern:

- `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`

Current robots body path pattern:

- `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`

### Türkçe

`.body.bin`, ham HTTP response body dosyasıdır.

HTTP veya browser fetch response body byte'ları döndürdükten sonra crawler_core tarafından yazılır.

Bu dosya bilerek genel tutulur; çünkü crawler raw-evidence aşamasında semantik dosya tipi kararı vermez.

`.body.bin` içinde şunlar olabilir:

- HTML text
- JSON API response text
- JavaScript text
- CSS text
- plain text
- XML
- CSV
- PDF bytes
- image bytes
- sunucudan gelen başka bir ham response body

Dosya adı şunu söyler:

- bu bir body artefact dosyasıdır
- payload ham byte olarak saklanmıştır
- payload henüz parse/ranking/import JSON formatına normalize edilmemiştir

Güncel URL body path formatı:

- `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`

Güncel robots body path formatı:

- `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`

---

## 4. `.fetch.json.zst` contract / `.fetch.json.zst` sözleşmesi

### English

`.fetch.json.zst` is a compressed JSON fetch envelope.

It is not the raw body.

It is not package plus receipt.

It is only the compressed receipt/envelope.

It should describe or reference:

- URL id
- host id when relevant
- fetch attempt id when available
- requested URL
- final URL
- HTTP status
- content type
- content length when available
- raw body storage path
- raw body byte count
- raw body SHA/checksum
- fetch policy result
- redirect result
- timeout/error class when applicable
- schema/version of the envelope

`.fetch.json.zst` must not embed the full `.body.bin` bytes.

Correct mental model:

- `.body.bin` = package
- `.fetch.json.zst` = compressed receipt
- DB row = operational state and queryable receipt fields

### Türkçe

`.fetch.json.zst`, sıkıştırılmış JSON fetch envelope dosyasıdır.

Ham body değildir.

Paket + teslim fişi değildir.

Sadece sıkıştırılmış teslim fişi/envelope dosyasıdır.

Şunları açıklamalı veya referanslamalıdır:

- URL id
- gerekiyorsa host id
- varsa fetch attempt id
- istenen URL
- final URL
- HTTP status
- content type
- varsa content length
- raw body storage path
- raw body byte sayısı
- raw body SHA/checksum
- fetch policy sonucu
- redirect sonucu
- varsa timeout/error class
- envelope schema/version bilgisi

`.fetch.json.zst`, `.body.bin` byte'larının tamamını içine gömmemelidir.

Doğru zihinsel model:

- `.body.bin` = paket
- `.fetch.json.zst` = sıkıştırılmış makbuz
- DB row = operasyonel state ve sorgulanabilir makbuz alanları

---

## 5. URL body vs robots body / URL body ile robots body farkı

### English table

| Field | URL raw body | Robots raw body |
|---|---|---|
| Filename pattern | `url_<url_id>_<timestamp>.body.bin` | `host_<host_id>_robots_<timestamp>.body.bin` |
| Path pattern | `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin` | `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin` |
| Main id | `url_id` | `host_id` |
| Scope | one URL | one host/domain authority |
| Content | page, PDF, JSON API response, HTML, CSS, JS, text, binary response | robots.txt policy response |
| Used for | later parse, classification, ranking, import | crawl permission and host policy |
| Typical content type | many possible types | usually text/plain |
| Is raw evidence? | yes | yes |
| Is structured JSON? | no | no |

### Türkçe tablo

| Alan | URL raw body | Robots raw body |
|---|---|---|
| Dosya adı formatı | `url_<url_id>_<timestamp>.body.bin` | `host_<host_id>_robots_<timestamp>.body.bin` |
| Path formatı | `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin` | `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin` |
| Ana id | `url_id` | `host_id` |
| Kapsam | tek URL | tek host/domain authority |
| İçerik | sayfa, PDF, JSON API response, HTML, CSS, JS, text, binary response | robots.txt policy response |
| Kullanım | sonra parse, classification, ranking, import | crawl izni ve host policy |
| Tipik content type | birçok farklı tip olabilir | genelde text/plain |
| Raw evidence mı? | evet | evet |
| Structured JSON mı? | hayır | hayır |

---

## 6. Why robots body is separate / Robots body neden ayrı?

### English

Robots data is not normal page content.

Robots data controls whether the crawler is allowed to fetch specific paths on a host.

It is host-scoped, not URL-scoped.

That is why robots body uses:

- `host_<host_id>_robots_<timestamp>.body.bin`

instead of:

- `url_<url_id>_<timestamp>.body.bin`

Robots body is still raw evidence because the fetched robots.txt response must be auditable.

### Türkçe

Robots verisi normal sayfa içeriği değildir.

Robots verisi, crawler'ın bir host üzerindeki belirli path'leri çekip çekemeyeceğini belirler.

Host kapsamlıdır, tek URL kapsamlı değildir.

Bu yüzden robots body şu formatı kullanır:

- `host_<host_id>_robots_<timestamp>.body.bin`

şu formatı değil:

- `url_<url_id>_<timestamp>.body.bin`

Robots body yine raw evidence kabul edilir; çünkü çekilen robots.txt response denetlenebilir olmalıdır.

---

## 7. Current active artefact flow / Güncel aktif artefact akışı

### English

1. crawler_core claims or receives a URL/host task.
2. crawler_core checks robots policy when required.
3. robots fetch may write:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`
4. URL fetch writes:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`
5. Current crawler_core may also create:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.fetch.json.zst`
6. `.fetch.json.zst` is a compressed JSON envelope about the fetch.
7. Current active audit did not prove active `.body.bin.zst` output.
8. Current active audit did not prove active `.raw_response_body.bin.zst` output.

### Türkçe

1. crawler_core URL/host görevi claim eder veya alır.
2. gerekiyorsa robots policy kontrolü yapar.
3. robots fetch şunu yazabilir:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`
4. URL fetch şunu yazar:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`
5. mevcut crawler_core ayrıca şunu üretebilir:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.fetch.json.zst`
6. `.fetch.json.zst`, fetch hakkında sıkıştırılmış JSON envelope dosyasıdır.
7. güncel aktif audit aktif `.body.bin.zst` output kanıtlamadı.
8. güncel aktif audit aktif `.raw_response_body.bin.zst` output kanıtlamadı.

---

## 8. Target compression separation / Hedef compression ayrımı

### English

Compression must move out of crawler_core.

Future compression ownership:

- compression worker/service pipeline
- C++ helper code for deterministic ZSTD work
- no unused Python compression worker directory
- no unused C compression worker directory
- no unused worker directory without immediate code/use

Preferred future C++ helper directories:

- `makpi51crawler/cpp_live_runtime/compression_worker/raw_response_body_bin_zstd/`
- `makpi51crawler/cpp_live_runtime/compression_worker/structured_json_zstd/`

Meaning:

- `raw_response_body_bin_zstd/` handles raw `.body.bin` body artefacts and may produce `.body.bin.zst`
- `structured_json_zstd/` handles structured JSON artefacts and may produce `.json.zst`

### Türkçe

Compression crawler_core dışına taşınmalıdır.

Gelecekte compression sahipliği:

- compression worker/service pipeline
- deterministik ZSTD işleri için C++ helper kodu
- kullanılmayan Python compression worker dizini yok
- kullanılmayan C compression worker dizini yok
- hemen kod/kullanım yoksa boş worker dizini yok

Tercih edilen gelecek C++ helper dizinleri:

- `makpi51crawler/cpp_live_runtime/compression_worker/raw_response_body_bin_zstd/`
- `makpi51crawler/cpp_live_runtime/compression_worker/structured_json_zstd/`

Anlam:

- `raw_response_body_bin_zstd/`, ham `.body.bin` body artefact dosyalarını işler ve `.body.bin.zst` üretebilir
- `structured_json_zstd/`, structured JSON artefact dosyalarını işler ve `.json.zst` üretebilir

---

## 9. Legacy path policy / Legacy path politikası

The following path is deprecated for new truth:

- `/srv/crawler/logisticsearch/raw_fetch`

The current active raw evidence root is:

- `/srv/webcrawler/raw_fetch`

Legacy references must be cleaned only by a later exact-scope documentation cleanup gate.

No broad uncontrolled replacement is allowed.

---

## 10. Immediate next safe sequence / Sıradaki güvenli sıra

1. Audit this repaired local-only document.
2. Commit and push the document if audit passes.
3. Sync pi51c repo.
4. Post-seal read-only.
5. Run exact legacy documentation path audit for `/srv/crawler/logisticsearch/raw_fetch`.
6. Plan extraction of `.fetch.json.zst` creation from crawler_core.
7. Implement C++ helper directories only when actual code is added.
8. Keep `makpi51crawler/python_live_runtime/controls/` untouched.

No code mutation, raw mutation, DB mutation, systemd mutation, live copy, package install, directory creation, or crawler start is allowed in this documentation repair gate.

---

## 11. Final decision / Nihai karar

The canonical active raw evidence root is `/srv/webcrawler/raw_fetch`.

The current raw body artefact is `.body.bin`.

The current fetch envelope sidecar is `.fetch.json.zst`.

`.fetch.json.zst` is not the raw body and must not embed the complete `.body.bin` payload.

URL body and robots body are both raw evidence, but they have different scope:

- URL body is URL-scoped and uses `url_<url_id>_<timestamp>.body.bin`
- robots body is host-scoped and uses `host_<host_id>_robots_<timestamp>.body.bin`

The future C++ helper name for raw body compression is `raw_response_body_bin_zstd`.

The existing `makpi51crawler/python_live_runtime/controls/` directory is preserved untouched.

---

## 12. Same URL compressed artefact rule / Aynı URL için sıkıştırılmış artefact kuralı

### English

For one successful URL fetch, the target design may have separate artefacts for the same fetch:

- `url_<url_id>_<timestamp>.body.bin`
- `url_<url_id>_<timestamp>.body.bin.zst`
- `url_<url_id>_<timestamp>.fetch.json.zst`

Meaning:

- `.body.bin` is the original raw response body payload.
- `.body.bin.zst` is the ZSTD-compressed copy of the original raw response body payload.
- `.fetch.json.zst` is the ZSTD-compressed fetch receipt/envelope.

Strict rule:

- `.fetch.json.zst must not embed the full .body.bin payload.`
- `.fetch.json.zst must not contain a full embedded copy of the .body.bin payload.`
- `.body.bin.zst must be verified by decompression and checksum comparison before any cleanup decision can mark .body.bin as removable.`

Storage policy:

- `.body.bin` is the large original evidence file.
- `.body.bin.zst` is the large compressed evidence file.
- `.fetch.json.zst` is the small compressed receipt file.
- `.body.bin` is not deleted merely because `.body.bin.zst` exists.
- `.body.bin` becomes cleanup-eligible only after `.body.bin.zst` passes decompression verification and checksum verification.

### Türkçe

Başarılı tek bir URL fetch için hedef tasarımda aynı fetch’e ait ayrı artefact dosyaları olabilir:

- `url_<url_id>_<timestamp>.body.bin`
- `url_<url_id>_<timestamp>.body.bin.zst`
- `url_<url_id>_<timestamp>.fetch.json.zst`

Anlam:

- `.body.bin` orijinal ham response body payload dosyasıdır.
- `.body.bin.zst` orijinal ham response body payload dosyasının ZSTD ile sıkıştırılmış kopyasıdır.
- `.fetch.json.zst` ZSTD ile sıkıştırılmış fetch makbuzu/envelope dosyasıdır.

Katı kural:

- `.fetch.json.zst, ham response body değildir.`
- `.fetch.json.zst, .body.bin payload'unun tamamını içine gömmemelidir.`
- `.body.bin.zst doğrulanmadan .body.bin silinmez.`
- `.body.bin.zst`, cleanup kararından önce decompress verification ve checksum verification ile doğrulanmalıdır.

Storage politikası:

- `.body.bin` büyük orijinal evidence dosyasıdır.
- `.body.bin.zst` büyük sıkıştırılmış evidence dosyasıdır.
- `.fetch.json.zst` küçük sıkıştırılmış makbuz dosyasıdır.
- `.body.bin`, sadece `.body.bin.zst` var diye silinmez.
- `.body.bin`, sadece `.body.bin.zst` decompress verification ve checksum verification geçtikten sonra cleanup-eligible olabilir.

## 13. Controls preservation exact statement

The existing makpi51crawler/python_live_runtime/controls/ directory is preserved untouched.

---

## 14. Hot path compression timing decision / Sıcak hat sıkıştırma zamanlama kararı

Marker: `KOD_BLOGU_091D_HOT_PATH_AND_DESKTOP_IMPORT_COMPRESSION_TRUTH`

### English

This section supersedes any interpretation that would make parse_core repeatedly open `.body.bin.zst` on the normal hot path.

Final hot-path decision:

- crawler_core writes `.body.bin`.
- `.body.bin` remains the canonical hot payload until parse_core finishes.
- parse_core reads `.body.bin` on the normal hot path.
- parse_core must not read `.body.bin.zst` on the normal hot path.
- parse_core must not work with `.zst` artefacts on the normal hot path.
- `.body.bin.zst` is not a parse hot-path input.
- `.body.bin.zst` is an archive/storage artefact.
- `.fetch.json.zst` is a compressed fetch receipt/envelope, not the parse payload.
- no double compression is allowed.
- no decompress-for-parse loop is allowed.
- no compress, decompress, parse, recompress cycle is allowed.

Desktop import handoff decision:

- compression is triggered after parse_core has completed the hot parse step.
- desktop_import_worker prepares the data handoff toward compression_worker.
- desktop_import_worker prepares FIFO queue handoff for compression_worker.
- compression_worker receives explicit work from the desktop_import boundary.
- compression_worker compresses the raw body artefact and fetch envelope separately.
- `.body.bin` and the fetch envelope are compressed separately once.
- `.body.bin.zst` is created only as a cold/archive/storage artefact.
- `.body.bin` is not cleanup-eligible merely because `.body.bin.zst` exists.
- `.body.bin` cleanup eligibility requires verified compression, decompression verification, checksum verification, and a later explicit cleanup policy gate.

Immediate implementation priority:

- current crawler_core Python `.fetch.json.zst` production is legacy behavior for the target design.
- current crawler_core Python `.fetch.json.zst` production must be disabled in the next code-change gate before the next crawler test.
- the next crawler test must measure behavior without crawler_core-owned Python ZSTD sidecar production.
- old crawl outputs, old JSON/ZSTD evidence, DB rows, counters, and raw artefacts must be audited before cleanup.
- cleanup of old crawl data must happen only after a dedicated reset/cleanup gate.

### Türkçe

Bu bölüm, parse_core katmanının normal sıcak hatta tekrar tekrar `.body.bin.zst` açacağı yönündeki her yorumu geçersiz kılar.

Nihai sıcak hat kararı:

- crawler_core `.body.bin` yazar.
- `.body.bin`, parse_core işi bitene kadar canonical hot payload olarak kalır.
- parse_core normal sıcak hatta `.body.bin` okur.
- parse_core normal sıcak hatta `.body.bin.zst` okumaz.
- parse_core normal sıcak hatta `.zst` artefact ile çalışmaz.
- `.body.bin.zst` parse hot-path input değildir.
- `.body.bin.zst` arşiv/storage artefact dosyasıdır.
- `.fetch.json.zst` sıkıştırılmış fetch makbuzu/envelope dosyasıdır, parse payload değildir.
- iki kere sıkıştırma yasaktır.
- parse için decompress döngüsü yasaktır.
- compress, decompress, parse, recompress döngüsü yasaktır.

Desktop import handoff kararı:

- compression, parse_core sıcak parse adımını tamamladıktan sonra tetiklenir.
- desktop_import_worker veriyi compression_worker katmanına doğru handoff için hazırlar.
- desktop_import_worker compression_worker için FIFO queue handoff hazırlar.
- compression_worker açık işi desktop_import sınırından alır.
- compression_worker raw body artefact ve fetch envelope dosyasını ayrı ayrı sıkıştırır.
- `.body.bin` ve fetch envelope ayrı ayrı sadece bir kere sıkıştırılır.
- `.body.bin.zst` yalnızca cold/archive/storage artefact olarak oluşturulur.
- `.body.bin`, sadece `.body.bin.zst` var diye cleanup-eligible olmaz.
- `.body.bin` cleanup eligibility için verified compression, decompression verification, checksum verification ve daha sonra ayrı explicit cleanup policy gate gerekir.

Acil implementasyon önceliği:

- mevcut crawler_core Python `.fetch.json.zst` üretimi hedef tasarım açısından legacy davranıştır.
- mevcut crawler_core Python `.fetch.json.zst` üretimi bir sonraki code-change gate içinde, yeni crawler testi öncesinde disable edilmelidir.
- bir sonraki crawler testi crawler_core-owned Python ZSTD sidecar üretimi olmadan ölçülmelidir.
- eski crawl çıktıları, eski JSON/ZSTD evidence, DB satırları, sayaçlar ve raw artefact dosyaları cleanup öncesinde audit edilmelidir.
- eski crawl verisi cleanup işlemi yalnızca ayrı reset/cleanup gate sonrası yapılmalıdır.

---

## 15. Crawler core body-bin-only hot path clarification / Crawler core body-bin-only sıcak hat netleştirmesi

Marker: `KOD_BLOGU_096_BODY_BIN_ONLY_CRAWLER_CORE_PATCH_TRUTH`

### English

This section clarifies the exact file artefacts expected from crawler_core after the crawler-core ZSTD hot-path disable patch.

Crawler_core hot path output:

- HTTP URL fetch writes only the raw body artefact:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`
- robots fetch writes only the raw robots body artefact:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`
- browser-rendered fetch, when used, may write the rendered HTML artefact:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.rendered.html`

Crawler_core hot path must not create:

- `.fetch.json`
- `.fetch.json.zst`
- `.body.bin.zst`
- `.raw_response_body.bin.zst`

The existing Python ZSTD helper infrastructure is retained but disabled from crawler_core hot-path callers.

Desktop import / compression handoff:

- desktop_import_worker will later prepare a FIFO handoff toward compression_worker.
- compression_worker will later create `.body.bin.zst`.
- compression_worker will later create `.fetch.json.zst`.
- those compressed artefacts are cold/archive/packaging artefacts, not crawler_core hot-path artefacts.

### Türkçe

Bu bölüm, crawler-core ZSTD hot-path disable patch sonrasında crawler_core katmanından beklenen exact dosya artefact davranışını netleştirir.

Crawler_core sıcak hat output:

- HTTP URL fetch yalnızca ham body artefact dosyasını yazar:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`
- robots fetch yalnızca ham robots body artefact dosyasını yazar:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`
- browser-rendered fetch kullanılırsa rendered HTML artefact yazabilir:
  - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.rendered.html`

Crawler_core sıcak hat şunları oluşturmayacaktır:

- `.fetch.json`
- `.fetch.json.zst`
- `.body.bin.zst`
- `.raw_response_body.bin.zst`

Mevcut Python ZSTD helper altyapısı korunur fakat crawler_core hot-path caller'larından deaktif edilir.

Desktop import / compression handoff:

- desktop_import_worker daha sonra compression_worker için FIFO handoff hazırlar.
- compression_worker daha sonra `.body.bin.zst` üretir.
- compression_worker daha sonra `.fetch.json.zst` üretir.
- bu compressed artefact dosyaları cold/archive/packaging artefact dosyalarıdır; crawler_core sıcak hat artefact dosyaları değildir.

---

## 16. Crawler core raw-body-family output clarification / Crawler core raw-body-family output netleştirmesi

Marker: `KOD_BLOGU_096B_RAW_BODY_FAMILY_AND_ZSTD_INFRA_DEACTIVATED_TRUTH`

### English

The phrase `BODY_BIN_ONLY` must not be interpreted as “crawler_core creates only one single file”.

Correct interpretation:

- crawler_core creates only raw body family artefacts on the hot path.
- crawler_core does not create JSON or ZSTD sidecar artefacts on the hot path.
- crawler_core does not create compressed raw body artefacts on the hot path.

Current crawler_core hot-path raw body family outputs:

1. URL raw body artefact:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`

2. Robots raw body artefact:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`

3. Browser rendered artefact, only when browser-rendered acquisition is used:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.rendered.html`

Forbidden crawler_core hot-path outputs:

- `.fetch.json`
- `.fetch.json.zst`
- `.body.bin.zst`
- `.raw_response_body.bin.zst`

ZSTD infrastructure status:

- The Python ZSTD envelope constants are preserved.
- The Python ZSTD envelope builder is preserved.
- The Python ZSTD compressed writer is preserved.
- The Python ZSTD compare/decompress helpers are preserved.
- The HTTP and browser page caller argument mappings are preserved inside a disabled flag gate.
- The feature is deactivated because crawler_core hot path does not use it now.
- The feature is not deleted because future desktop_import → compression_worker handoff may reuse the preserved infrastructure.

### Türkçe

`BODY_BIN_ONLY` ifadesi “crawler_core yalnızca tek bir dosya oluşturur” şeklinde yorumlanmamalıdır.

Doğru yorum:

- crawler_core sıcak hatta yalnızca raw body ailesi artefact dosyaları oluşturur.
- crawler_core sıcak hatta JSON veya ZSTD sidecar artefact oluşturmaz.
- crawler_core sıcak hatta sıkıştırılmış raw body artefact oluşturmaz.

Güncel crawler_core hot-path raw body ailesi output dosyaları:

1. URL raw body artefact:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.body.bin`

2. Robots raw body artefact:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/host_<host_id>_robots_<timestamp>.body.bin`

3. Browser-rendered acquisition kullanılırsa browser rendered artefact:
   - `/srv/webcrawler/raw_fetch/YYYY/MM/DD/url_<url_id>_<timestamp>.rendered.html`

Crawler_core sıcak hatta yasak output dosyaları:

- `.fetch.json`
- `.fetch.json.zst`
- `.body.bin.zst`
- `.raw_response_body.bin.zst`

ZSTD altyapı durumu:

- Python ZSTD envelope constant değerleri korunmuştur.
- Python ZSTD envelope builder korunmuştur.
- Python ZSTD compressed writer korunmuştur.
- Python ZSTD compare/decompress helper fonksiyonları korunmuştur.
- HTTP ve browser page caller argument mapping yapısı disabled flag gate içinde korunmuştur.
- Bu özellik şu anda crawler_core sıcak hatta kullanılmadığı için deaktif edilmiştir.
- Bu özellik silinmemiştir; çünkü ileride desktop_import → compression_worker handoff bu korunmuş altyapıyı yeniden kullanabilir.

