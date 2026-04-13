# Webcrawler Python Runtime Library Surface

Parent surface:

- `python/webcrawler/README.md` — use this as the broader crawler Python surface map.
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md` — use this as the canonical runtime naming and role standard.

Üst yüzey:

- `python/webcrawler/README.md` — geniş crawler Python yüzey haritası olarak bunu kullan.
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md` — kanonik runtime adlandırma ve rol standardı olarak bunu kullan.

## Purpose

This folder should hold the live numbered Python runtime family of the LogisticSearch webcrawler.

The goal is to make the active runtime tree visible in one place.

## Amaç

Bu klasör, LogisticSearch webcrawler'ın canlı numaralı Python runtime ailesini tek yerde tutmalıdır.

Amaç, aktif runtime ağacını tek bakışta görünür hale getirmektir.

## Current visible files

At the current repository point, this folder visibly contains:

- `__init__.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch1_main_worker_runtime.py`

This means the browser seam and the main runtime helpers are already here, but the thin worker CLI and the browser smoke tool still sit one level above and should later be folded into this folder during the controlled rename/layout patch.

## Güncel görünen dosyalar

Mevcut repository noktasında bu klasör görünür olarak şunları içerir:

- `__init__.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch1_main_worker_runtime.py`

Bu da browser seam'i ile ana runtime yardımcılarının zaten burada olduğu, ancak ince worker CLI ile browser smoke aracının hâlâ bir seviye yukarıda durduğu ve kontrollü rename/layout patch'i sırasında daha sonra bu klasöre katlanması gerektiği anlamına gelir.

## Target canonical family for this folder

The intended stable family for this folder is:

- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

## Bu klasör için hedef kanonik aile

Bu klasör için hedef stabil aile şudur:

- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

## Current live-family truth
## Güncel canlı-aile doğrusu

This means the active numbered runtime family is now visible here together, including the thin worker CLI and the browser smoke entry.

So this folder can now be read as the live runtime family home rather than as a partial pre-move surface.

Use the following boundary topic as the canonical boundary truth for raw fetch, parse, taxonomy, selection order, and non-logistics handling:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`

Bu da aktif numaralı runtime ailesinin artık ince worker CLI ve browser smoke girişi dahil olmak üzere burada birlikte görünür olduğu anlamına gelir.

Dolayısıyla bu klasör artık kısmi pre-move yüzey olarak değil, canlı runtime ailesinin evi olarak okunmalıdır.

Raw fetch, parse, taxonomy, seçim sırası ve lojistik dışı sayfaların ele alınışı için aşağıdaki boundary topic'i kanonik sınır doğrusu olarak kullan:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
