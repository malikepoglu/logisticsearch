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
At the current repository point, this folder visibly contains the active numbered runtime family itself:

- `__init__.py`
- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

This means the live numbered runtime family is already visible here together in one place.

So this folder is no longer a partial pre-move surface.

## Güncel görünen dosyalar
Mevcut repository noktasında bu klasör, aktif numaralı runtime ailesinin kendisini görünür olarak içerir:

- `__init__.py`
- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

Bu da canlı numaralı runtime ailesinin artık burada tek yerde birlikte görünür olduğu anlamına gelir.

Dolayısıyla bu klasör artık kısmi pre-move yüzey değildir.

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

So this folder can now be read as the live runtime family home rather than as a partial transitional runtime surface.

Use the following boundary topic as the canonical boundary truth for raw fetch, parse, taxonomy, selection order, and non-logistics handling:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`

Bu da aktif numaralı runtime ailesinin artık ince worker CLI ve browser smoke girişi dahil olmak üzere burada birlikte görünür olduğu anlamına gelir.

Dolayısıyla bu klasör artık kısmi pre-move yüzey olarak değil, canlı runtime ailesinin evi olarak okunmalıdır.

Raw fetch, parse, taxonomy, seçim sırası ve lojistik dışı sayfaların ele alınışı için aşağıdaki boundary topic'i kanonik sınır doğrusu olarak kullan:

* `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
## Current root-surface and host-boundary truth
## Güncel kök-yüzey ve host-sınırı doğrusu

At the current repository point, `python/webcrawler/lib/` remains part of the shared root `python/` project surface.

It is not being physically relocated under `hosts/makpi51crawler/`.

The `hosts/` family documents host-specific operational truth, while this `lib/` folder remains the shared live runtime-family surface inside the root Python tree.

For host-side boundary reading, also see:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`

Mevcut repository noktasında `python/webcrawler/lib/`, ortak kök `python/` proje yüzeyinin parçası olarak kalır.

Bu yüzey fiziksel olarak `hosts/makpi51crawler/` altına taşınmamaktadır.

`hosts/` ailesi host-özel operasyon doğrusunu belgelerken, bu `lib/` klasörü kök Python ağacı içindeki ortak canlı runtime-aile yüzeyi olarak kalır.

Host-tarafı sınır okuması için ayrıca şunlara bak:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`
