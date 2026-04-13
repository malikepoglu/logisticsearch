# Webcrawler Runtime Layout and Naming Standard

Documentation hub:

- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:

- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Purpose

This document freezes the canonical layout, naming, role separation, and version-metadata rule for the LogisticSearch Python webcrawler runtime surfaces.

The crawler runtime is expected to remain lean, explicit, maintainable, and structurally readable as it evolves.

## Amaç

Bu belge, LogisticSearch Python webcrawler runtime yüzeyleri için kanonik yerleşim, adlandırma, rol ayrımı ve version-metadata kuralını dondurur.

Crawler runtime, gelişmeye devam ederken yalın, açık, sürdürülebilir ve yapısal olarak okunabilir kalmalıdır.

## Canonical layout rule

All live Python runtime surfaces of the webcrawler should live under:

- `python/webcrawler/lib/`

This includes the thin worker/operator CLI surface and the repo-local smoke tools.

The parent directory `python/webcrawler/` should remain the broader surface root, but the active Python runtime family itself should be grouped inside `lib/` so the numbered hierarchy can be seen in one place.

## Kanonik yerleşim kuralı

Webcrawler'ın tüm canlı Python runtime yüzeyleri şu klasör altında yaşamalıdır:

- `python/webcrawler/lib/`

Buna ince worker/operator CLI yüzeyi ve repo-local smoke araçları da dahildir.

Üst klasör olan `python/webcrawler/` geniş yüzey kökü olarak kalmalıdır; ancak aktif Python runtime ailesinin kendisi, numaralı hiyerarşi tek yerde görülebilsin diye `lib/` içinde gruplanmalıdır.

## Canonical target filename family

The corrected target family is:

- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

The numbering is structural, not decorative.

## Kanonik hedef dosya ailesi

Düzeltilmiş hedef aile şudur:

- `logisticsearch1_main_worker_runtime.py`
- `logisticsearch1_1_fetch_runtime.py`
- `logisticsearch1_2_browser_acquisition_runtime.py`
- `logisticsearch1_2_1_browser_acquisition_smoke.py`
- `logisticsearch1_3_parse_runtime.py`
- `logisticsearch1_4_db.py`
- `logisticsearch1_5_storage_routing.py`
- `logisticsearch2_worker_claim_loop.py`

Numaralandırma kozmetik değil, yapısaldır.

## Detailed role map

### `logisticsearch1_main_worker_runtime.py`

Main continuous runtime core.

It should orchestrate the canonical sequence:

claim -> robots -> acquisition -> parse continuation -> finalize

### `logisticsearch1_1_fetch_runtime.py`

Acquisition home.

Direct HTTP and robots fetch live here.
Browser-backed acquisition should gradually fold into this home too.

### `logisticsearch1_2_browser_acquisition_runtime.py`

Narrow transitional browser seam.

It exists while browser-backed acquisition is still being integrated into the canonical fetch layer.

### `logisticsearch1_2_1_browser_acquisition_smoke.py`

Repo-local browser smoke tool.

It proves browser launch, navigation, rendered DOM capture, screenshot evidence, and machine-readable JSON evidence.

### `logisticsearch1_3_parse_runtime.py`

Parse / filtering / evidence extraction layer.

### `logisticsearch1_4_db.py`

Database and state-transition helper layer.

### `logisticsearch1_5_storage_routing.py`

Storage decision layer for:

- `/srv/crawler/logisticsearch/`
- `/srv/data/`
- `/srv/buffer/`

### `logisticsearch2_worker_claim_loop.py`

Thin operator/CLI entry.

It is related to the main worker runtime but is not hierarchically a child implementation layer under the same top-level runtime family.

## Ayrıntılı rol haritası

### `logisticsearch1_main_worker_runtime.py`

Ana sürekli çalışan runtime çekirdeği.

Kanonik sırayı orkestre etmelidir:

claim -> robots -> acquisition -> parse continuation -> finalize

### `logisticsearch1_1_fetch_runtime.py`

Acquisition evidir.

Direct HTTP ve robots fetch burada yaşar.
Browser destekli acquisition da zamanla bu eve katlanmalıdır.

### `logisticsearch1_2_browser_acquisition_runtime.py`

Dar geçiş browser seam'idir.

Browser destekli acquisition, kanonik fetch katmanına tam entegre edilene kadar burada durur.

### `logisticsearch1_2_1_browser_acquisition_smoke.py`

Repo-local browser smoke aracıdır.

Browser launch, navigation, rendered DOM capture, screenshot kanıtı ve machine-readable JSON kanıtı üretimini kanıtlar.

### `logisticsearch1_3_parse_runtime.py`

Parse / süzme / evidence extraction katmanıdır.

### `logisticsearch1_4_db.py`

Veritabanı ve state-transition yardımcı katmanıdır.

### `logisticsearch1_5_storage_routing.py`

Şu yollar için storage karar katmanıdır:

- `/srv/crawler/logisticsearch/`
- `/srv/data/`
- `/srv/buffer/`

### `logisticsearch2_worker_claim_loop.py`

İnce operatör/CLI girişidir.

Ana worker runtime ile ilişkilidir; ancak aynı üst runtime ailesi altında hiyerarşik alt implementasyon katmanı değildir.

## Canonical version metadata rule

Live filenames should stay stable.

Version truth should live inside source metadata.

Canonical example:

- `SURFACE_VERSION = "V1-13.04.2026-15.41.13"`

## Kanonik version metadata kuralı

Canlı dosya adları stabil kalmalıdır.

Version doğrusu source metadata içinde yaşamalıdır.

Kanonik örnek:

- `SURFACE_VERSION = "V1-13.04.2026-15.41.13"`

## Immediate next order

1. Freeze this standard in docs and README surfaces.
2. Rename the Python files in one controlled patch.
3. Repair imports and smoke references.
4. Re-prove syntax and smoke behavior.
5. Then continue browser-backed acquisition integration.

## Hemen sonraki sıra

1. Bu standardı docs ve README yüzeylerinde dondur.
2. Python dosyalarını tek bir kontrollü patch ile yeniden adlandır.
3. Import ve smoke referanslarını onar.
4. Sözdizimi ve smoke davranışını yeniden kanıtla.
5. Ondan sonra browser destekli acquisition entegrasyonuna devam et.
