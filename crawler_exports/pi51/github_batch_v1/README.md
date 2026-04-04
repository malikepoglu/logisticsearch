# github_batch_v1

## EN
Canonical live path pattern:

`crawler_exports/pi51/github_batch_v1/YYYY/MM/DD/<batch_key>/`

Each batch folder is expected to contain:
- `batch.json`
- `manifest.json`
- `SHA256SUMS.txt`
- `PUSH_RECEIPT.json`

Repository readability helpers generated on Ubuntu Desktop:
- `LATEST_BATCH.json`
- `BATCH_CATALOG.json`

Rules:
- The producer path must stay stable unless the Pi51 push worker contract is explicitly updated.
- Historical batch payload files are treated as append-only evidence.
- Catalog files may be regenerated as long as they reflect repository truth.

## TR
Canonical canlı path pattern:

`crawler_exports/pi51/github_batch_v1/YYYY/MM/DD/<batch_key>/`

Her batch klasöründe beklenen dosyalar:
- `batch.json`
- `manifest.json`
- `SHA256SUMS.txt`
- `PUSH_RECEIPT.json`

Ubuntu Desktop üzerinde üretilen repo okunabilirlik yardımcıları:
- `LATEST_BATCH.json`
- `BATCH_CATALOG.json`

Kurallar:
- Pi51 push worker kontratı açıkça güncellenmedikçe producer path sabit kalmalıdır.
- Geçmiş batch payload dosyaları append-only kanıt olarak ele alınır.
- Catalog dosyaları repo truth’u doğru yansıttığı sürece yeniden üretilebilir.
