# pi51 crawler exports

## EN
This subtree contains crawler export batches produced by Pi51 and published into GitHub for Ubuntu Desktop intake.

Producer role:
- Pi51 crawler node

Consumer role:
- Ubuntu Desktop intake / downstream ranking and application-side processing

Contract:
- Producer writes deterministic batch folders under the active channel path.
- Ubuntu Desktop pulls from GitHub, copies into `_imports/...`, and loads into local intake tables.

## TR
Bu alt ağaç, Pi51 tarafından üretilip Ubuntu Desktop intake için GitHub’a yayınlanan crawler export batch’lerini içerir.

Üretici rolü:
- Pi51 crawler node

Tüketici rolü:
- Ubuntu Desktop intake / sonraki ranking ve uygulama tarafı işleme

Kontrat:
- Producer, aktif kanal yolu altında deterministic batch klasörleri üretir.
- Ubuntu Desktop, GitHub’dan çeker, `_imports/...` altına kopyalar ve yerel intake tablolarına yükler.
