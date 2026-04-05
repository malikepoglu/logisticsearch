# Outbox Core Live Operational Reality Audit - 2026-04-05

## Overview

This document records the observed live operational state of the `outbox` schema on Pi51 as audited on 2026-04-05.

This is not a structural import/split document.  
It is a live-state observation document that captures how the outbox layer is currently behaving in production reality.

## Genel Bakış

Bu belge, 2026-04-05 tarihinde Pi51 üzerinde denetlenen `outbox` şemasının gözlenen canlı operasyonel durumunu kayda geçirir.

Bu belge yapısal import/split belgesi değildir.  
Bu, outbox katmanının şu anda üretim gerçeğinde nasıl davrandığını kaydeden canlı durum gözlem belgesidir.

## Audit source context

Audit path:
- Ubuntu Desktop
- SSH to `pi51-eth`
- database: `logisticsearch_crawler`

Audit type:
- read-only
- no mutation
- live operational observation

## Denetim kaynak bağlamı

Denetim yolu:
- Ubuntu Desktop
- `pi51-eth` üzerinden SSH
- veritabanı: `logisticsearch_crawler`

Denetim tipi:
- salt-okunur
- mutasyon yok
- canlı operasyonel gözlem

## Observed row counts

Observed table row counts at audit time:

- `outbox.export_batch`: 4
- `outbox.export_batch_item`: 0
- `outbox.page_export_item`: 0

## Gözlenen satır sayıları

Denetim anında gözlenen tablo satır sayıları:

- `outbox.export_batch`: 4
- `outbox.export_batch_item`: 0
- `outbox.page_export_item`: 0

## Observed state distributions

### export_batch state distribution

For `github_batch_v1`:

- `pushed`: 2
- `failed`: 2

### page_export_item state distribution

No live rows were present at audit time.

## Gözlenen durum dağılımları

### export_batch durum dağılımı

`github_batch_v1` için:

- `pushed`: 2
- `failed`: 2

### page_export_item durum dağılımı

Denetim anında canlı satır bulunmamıştır.

## Latest observed batch headers

Latest observed batch headers were:

1. `github_batch_v1_20260404T212728Z_6_1` → `pushed`
2. `github_batch_v1_20260404T211857Z_5_1` → `failed`
3. `github_batch_v1_20260404T205424Z_4_1` → `pushed`
4. `github_batch_v1_20260404T203838Z_3_1` → `failed`

Each recorded `item_count = 1`.

## Gözlenen son batch header kayıtları

Gözlenen son batch header kayıtları şunlardır:

1. `github_batch_v1_20260404T212728Z_6_1` → `pushed`
2. `github_batch_v1_20260404T211857Z_5_1` → `failed`
3. `github_batch_v1_20260404T205424Z_4_1` → `pushed`
4. `github_batch_v1_20260404T203838Z_3_1` → `failed`

Her kayıtta `item_count = 1` görülmüştür.

## Observed storage_relpath convention

Observed batch storage path pattern:

- `github_batch_v1/batches/<batch_key>`

Observed examples:

- `github_batch_v1/batches/github_batch_v1_20260404T212728Z_6_1`
- `github_batch_v1/batches/github_batch_v1_20260404T211857Z_5_1`
- `github_batch_v1/batches/github_batch_v1_20260404T205424Z_4_1`
- `github_batch_v1/batches/github_batch_v1_20260404T203838Z_3_1`

## Gözlenen storage_relpath kuralı

Gözlenen batch storage path kalıbı:

- `github_batch_v1/batches/<batch_key>`

Gözlenen örnekler:

- `github_batch_v1/batches/github_batch_v1_20260404T212728Z_6_1`
- `github_batch_v1/batches/github_batch_v1_20260404T211857Z_5_1`
- `github_batch_v1/batches/github_batch_v1_20260404T205424Z_4_1`
- `github_batch_v1/batches/github_batch_v1_20260404T203838Z_3_1`

## Consistency checks

Observed consistency checks:

- `batch_items_without_batch = 0`
- `batch_items_without_export_item = 0`
- `export_items_without_batch_link = 0`

## Tutarlılık kontrolleri

Gözlenen tutarlılık kontrolleri:

- `batch_items_without_batch = 0`
- `batch_items_without_export_item = 0`
- `export_items_without_batch_link = 0`

## Operational interpretation

The live outbox layer is currently not empty, but it is also not holding active item-level export queue rows at audit time.

Observed practical reality:

1. batch header history exists
2. failed/pushed batch states exist
3. no current `page_export_item` rows are present
4. no current `export_batch_item` rows are present
5. no structural consistency issue was observed in the checked relations

This means the current live system appears to retain batch-level history while not currently retaining active item/link rows.

This is an observation, not a speculative redesign claim.

## Operasyonel yorum

Canlı outbox katmanı şu anda tamamen boş değildir, ancak denetim anında aktif item-level export kuyruk satırları da tutmamaktadır.

Gözlenen pratik gerçek şudur:

1. batch header geçmişi vardır
2. failed/pushed batch durumları vardır
3. şu anda `page_export_item` satırı yoktur
4. şu anda `export_batch_item` satırı yoktur
5. kontrol edilen ilişkilerde yapısal bir tutarlılık sorunu gözlenmemiştir

Bu, mevcut canlı sistemin batch-level geçmişi koruyor göründüğünü; buna karşılık aktif item/link satırlarını şu anda tutmadığını gösterir.

Bu bir gözlemdir; spekülatif bir yeniden tasarım iddiası değildir.

## Why this matters

This matters because structural correctness alone is not enough.

For reliable future evolution, the project must preserve both:

1. repository-side structural truth
2. live operational truth

This audit belongs to the second category.

## Bu neden önemlidir

Bu önemlidir; çünkü yalnızca yapısal doğruluk yeterli değildir.

Güvenilir gelecekteki evrim için proje şu iki doğruluk katmanını birlikte korumalıdır:

1. repository-side yapısal doğruluk
2. canlı operasyonel doğruluk

Bu denetim ikinci kategoriye aittir.

## Immediate follow-up relevance

This live-state observation should inform future work in areas such as:

- export lifecycle semantics
- retention vs cleanup policy for item/link rows
- batch-history expectations
- operational monitoring and reporting

## Anlık devam ilişkisi

Bu canlı durum gözlemi, gelecekte şu alanlardaki işi beslemelidir:

- export lifecycle semantiği
- item/link satırları için retention vs cleanup politikası
- batch-history beklentileri
- operasyonel izleme ve raporlama
