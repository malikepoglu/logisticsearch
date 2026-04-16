# Webcrawler Python Runtime Library Surface

Documentation hub:

* `hosts/makpi51crawler/python/webcrawler/README.md` — webcrawler runtime surface
* `hosts/makpi51crawler/python/README.md` — host-scoped Python hub
* `hosts/makpi51crawler/README.md` — host root for makpi51crawler
* `hosts/README.md` — host family root
* `README.md` — repository root surface
* `docs/README.md` — documentation hub

Dokümantasyon merkezi:

* `hosts/makpi51crawler/python/webcrawler/README.md` — webcrawler runtime yüzeyi
* `hosts/makpi51crawler/python/README.md` — host-kapsamlı Python merkezi
* `hosts/makpi51crawler/README.md` — makpi51crawler host kökü
* `hosts/README.md` — host aile kökü
* `README.md` — repository kök yüzeyi
* `docs/README.md` — dokümantasyon merkezi

Parent surface:

- `hosts/makpi51crawler/python/webcrawler/README.md` — use this as the broader crawler Python surface map.
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md` — use this as the canonical runtime naming and role standard.

Üst yüzey:

- `hosts/makpi51crawler/python/webcrawler/README.md` — geniş crawler Python yüzey haritası olarak bunu kullan.
- `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md` — kanonik runtime adlandırma ve rol standardı olarak bunu kullan.

## Purpose

This folder should hold the live numbered Python runtime family of the LogisticSearch webcrawler.

The goal is to make the active runtime tree visible in one place.

## Amaç

Bu klasör, LogisticSearch webcrawler'ın canlı numaralı Python runtime ailesini tek yerde tutmalıdır.

Amaç, aktif runtime ağacını tek bakışta görünür hale getirmektir.

## Current visible files
At the current repository point, this folder visibly contains the active numbered runtime family itself:

- `__init__.py`
- `logisticsearch1_1_2_worker_runtime.py`
- `logisticsearch1_1_2_2_acquisition_runtime.py`
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
- `logisticsearch2_diag_browser_acquisition_smoke.py`
- `logisticsearch1_1_2_3_parse_runtime.py`
- `logisticsearch1_1_1_state_db_gateway.py`
- `logisticsearch1_1_2_1_storage_routing.py`
- `logisticsearch1_1_main_loop.py`

This means the live numbered runtime family is already visible here together in one place.

So this folder is no longer a partial transitional runtime surface.

## Güncel görünen dosyalar
Mevcut repository noktasında bu klasör, aktif numaralı runtime ailesinin kendisini görünür olarak içerir:

- `__init__.py`
- `logisticsearch1_1_2_worker_runtime.py`
- `logisticsearch1_1_2_2_acquisition_runtime.py`
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
- `logisticsearch2_diag_browser_acquisition_smoke.py`
- `logisticsearch1_1_2_3_parse_runtime.py`
- `logisticsearch1_1_1_state_db_gateway.py`
- `logisticsearch1_1_2_1_storage_routing.py`
- `logisticsearch1_1_main_loop.py`

Bu da canlı numaralı runtime ailesinin artık burada tek yerde birlikte görünür olduğu anlamına gelir.

Dolayısıyla bu klasör artık kısmi geçiş runtime yüzeyi değildir.

## Target canonical family for this folder

The intended stable family for this folder is:

- `logisticsearch1_1_2_worker_runtime.py`
- `logisticsearch1_1_2_2_acquisition_runtime.py`
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
- `logisticsearch2_diag_browser_acquisition_smoke.py`
- `logisticsearch1_1_2_3_parse_runtime.py`
- `logisticsearch1_1_1_state_db_gateway.py`
- `logisticsearch1_1_2_1_storage_routing.py`
- `logisticsearch1_1_main_loop.py`

## Bu klasör için hedef kanonik aile

Bu klasör için hedef stabil aile şudur:

- `logisticsearch1_1_2_worker_runtime.py`
- `logisticsearch1_1_2_2_acquisition_runtime.py`
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
- `logisticsearch2_diag_browser_acquisition_smoke.py`
- `logisticsearch1_1_2_3_parse_runtime.py`
- `logisticsearch1_1_1_state_db_gateway.py`
- `logisticsearch1_1_2_1_storage_routing.py`
- `logisticsearch1_1_main_loop.py`

## Current live-family truth
## Güncel canlı-aile doğrusu

This means the active numbered runtime family is now visible here together, including the thin worker CLI and the browser smoke entry.

So this folder can now be read as the live runtime family home rather than as a partial transitional runtime surface.

Use the following boundary topic as the canonical boundary truth for raw fetch, parse, taxonomy, selection order, and non-logistics handling:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`

Bu da aktif numaralı runtime ailesinin artık ince worker CLI ve browser smoke girişi dahil olmak üzere burada birlikte görünür olduğu anlamına gelir.

Dolayısıyla bu klasör artık kısmi geçiş runtime yüzeyi olarak değil, canlı runtime ailesinin evi olarak okunmalıdır.

Raw fetch, parse, taxonomy, seçim sırası ve lojistik dışı sayfaların ele alınışı için aşağıdaki boundary topic'i kanonik sınır doğrusu olarak kullan:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
## Current root-surface and host-boundary truth
## Güncel kök-yüzey ve host-sınırı doğrusu

At the current repository point, this runtime-family surface now lives at `hosts/makpi51crawler/python/webcrawler/lib/`.

It is intentionally located under the active crawler-host Python surface.

The `hosts/` family documents host-specific operational truth, and this `lib/` folder is now the live runtime-family surface for `makpi51crawler` inside the repository.

For host-side boundary reading, also see:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`

Mevcut repository noktasında bu runtime-aile yüzeyi artık `hosts/makpi51crawler/python/webcrawler/lib/` yolunda yaşamaktadır.

Bu yüzey aktif crawler-host Python yüzeyi altında bilinçli olarak konumlandırılmıştır.

`hosts/` ailesi host-özel operasyon doğrusunu belgeler; bu `lib/` klasörü ise artık repository içinde `makpi51crawler` için canlı runtime-aile yüzeyidir.

Host-tarafı sınır okuması için ayrıca şunlara bak:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`

## Root entry and main loop topology note
## Kök giriş ve ana loop topoloji notu

- `logisticsearch1_main_entry.py` is the single thin root-entry surface at the top of the runtime tree.
- `logisticsearch1_main_entry.py`, runtime ağacının tepesindeki tek ince kök-giriş yüzeyidir.

- `logisticsearch1_1_main_loop.py` is the main continuous loop directly under that root entry.
- `logisticsearch1_1_main_loop.py`, bu kök girişin hemen altındaki ana sürekli loop yüzeyidir.

- `logisticsearch1_1_2_worker_runtime.py` is not the root and not the outer loop; it is the main per-iteration worker orchestration layer called by the main loop.
- `logisticsearch1_1_2_worker_runtime.py` kök değildir ve dış loop da değildir; ana loop tarafından çağrılan iterasyon başına ana worker orkestrasyon katmanıdır.

## Runtime tree and data-flow reading path
## Runtime ağacı ve veri akışı okuma yolu

For the exact active runtime tree, the role of each Python file, and the real relationship between `/srv/webcrawler/raw_fetch`, `/srv/data`, `/srv/buffer`, and `/srv/webcrawler/exports`, read `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`.

Aktif runtime ağacının tam şekli, her Python dosyasının rolü ve `/srv/webcrawler/raw_fetch`, `/srv/data`, `/srv/buffer` ile `/srv/webcrawler/exports` arasındaki gerçek ilişki için `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md` dokümanını oku.
