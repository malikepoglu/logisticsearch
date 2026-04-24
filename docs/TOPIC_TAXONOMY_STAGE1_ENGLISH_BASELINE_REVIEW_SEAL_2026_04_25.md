# Stage1 English Baseline Taxonomy Review Seal — 2026-04-25

## EN

Final state: **PASS**.

This document seals the English baseline human-logic review that preceded the Turkish leasing patch chain.

Current English baseline decision:

- Language: `en`
- Total English taxonomy title/keyword rows reviewed: `335`
- English priority rows reviewed: `16`
- English service-side rows reviewed: `13`
- English title/keyword-difference rows reviewed: `3`
- English machine-phrase rows: `0`
- English patch required: **FALSE**
- English priority decision result: **KEEP all 16 priority rows**

The English baseline was intentionally treated as the first human-logic reference language before Turkish and German.

### Kept English title/keyword differences

The following title/keyword differences were intentionally kept:

1. `1.1`
   - Title: `Road Freight & Truck Transport`
   - Keyword: `Road Freight`
   - Reason: broader taxonomy display title; narrower search-intent keyword.

2. `1.2`
   - Title: `Sea Freight & Maritime Transport`
   - Keyword: `Sea Freight`
   - Reason: broader taxonomy display title; narrower search-intent keyword.

3. `5.1`
   - Title: `Logistics Software & Digital Systems`
   - Keyword: `Logistics Software`
   - Reason: broader taxonomy display title; narrower search-intent keyword.

### Kept English service-side rows

The English service-side rows under `10.2.*` and `10.3.*` were kept because their wording is understandable and did not create duplicate normalized primary keyword groups after the 007_R2B duplicate repair.

### Operational result

No English DB patch was created.

The later Turkish patch chain changed only:

- `tr / 10.3.2`
- `tr / 10.3.3`

It did not change English rows.

### Evidence location

The original ignored `_build` evidence was archived before `_build` cleanup under the local archive family:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2e_r6_and_build_cleanup_2026-04-25_00-24-15/`

Important archived file:

`logisticsearch__build_archive_before_cleanup_2026-04-25_00-24-15.tar.gz`

## TR

Son durum: **PASS**.

Bu belge, Turkish leasing patch zincirinden önce yapılan English baseline human-logic review kararını mühürler.

Mevcut English baseline kararı:

- Dil: `en`
- İncelenen toplam English taxonomy title/keyword satırı: `335`
- İncelenen English priority satırı: `16`
- İncelenen English service-side satırı: `13`
- İncelenen English title/keyword-difference satırı: `3`
- English machine-phrase satırı: `0`
- English patch gerekli mi: **FALSE**
- English priority karar sonucu: **16 priority satırın tamamı KEEP**

English baseline, Turkish ve German öncesindeki ilk insan-mantığı referans dili olarak bilinçli biçimde ele alındı.

### KEEP edilen English title/keyword farkları

Aşağıdaki title/keyword farkları bilinçli olarak korundu:

1. `1.1`
   - Title: `Road Freight & Truck Transport`
   - Keyword: `Road Freight`
   - Gerekçe: taxonomy gösterimi için daha geniş title; arama niyeti için daha dar keyword.

2. `1.2`
   - Title: `Sea Freight & Maritime Transport`
   - Keyword: `Sea Freight`
   - Gerekçe: taxonomy gösterimi için daha geniş title; arama niyeti için daha dar keyword.

3. `5.1`
   - Title: `Logistics Software & Digital Systems`
   - Keyword: `Logistics Software`
   - Gerekçe: taxonomy gösterimi için daha geniş title; arama niyeti için daha dar keyword.

### KEEP edilen English service-side satırları

`10.2.*` ve `10.3.*` altındaki English service-side satırları korundu; çünkü ifadeler anlaşılır ve 007_R2B duplicate repair sonrasında duplicate normalized primary keyword grubu üretmedi.

### Operasyon sonucu

English için DB patch oluşturulmadı.

Sonraki Turkish patch zinciri yalnızca şu satırları değiştirdi:

- `tr / 10.3.2`
- `tr / 10.3.3`

English satırlara dokunulmadı.

### Kanıt konumu

Orijinal ignored `_build` kanıtı, `_build` temizliği öncesinde şu local archive ailesi altında arşivlendi:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2e_r6_and_build_cleanup_2026-04-25_00-24-15/`

Önemli arşiv dosyası:

`logisticsearch__build_archive_before_cleanup_2026-04-25_00-24-15.tar.gz`
