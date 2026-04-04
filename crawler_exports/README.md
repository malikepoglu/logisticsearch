# crawler_exports

## EN
This tree stores exported crawler payload batches that are produced outside the main application runtime and then published into the repository in a deterministic structure.

Current producer family:
- `pi51`

Current live export channel family:
- `github_batch_v1`

Rules:
- Historical batch payload folders are immutable once pushed.
- Do not manually edit `batch.json`, `manifest.json`, `SHA256SUMS.txt`, or `PUSH_RECEIPT.json` inside historical batch folders.
- Readability and catalog files may be regenerated on Ubuntu Desktop without changing payload meaning.

## TR
Bu ağaç, ana uygulama runtime’ının dışında üretilen ve daha sonra deterministic bir yapıyla repoya yayınlanan crawler payload batch’lerini tutar.

Mevcut üretici ailesi:
- `pi51`

Mevcut canlı export kanal ailesi:
- `github_batch_v1`

Kurallar:
- Geçmiş batch payload klasörleri push edildikten sonra değiştirilemez kabul edilir.
- Tarihsel batch klasörleri içindeki `batch.json`, `manifest.json`, `SHA256SUMS.txt` ve `PUSH_RECEIPT.json` dosyalarını elle düzenleme.
- Okunabilirlik ve katalog dosyaları Ubuntu Desktop üzerinde, payload anlamını değiştirmeden yeniden üretilebilir.
