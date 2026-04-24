# Stage3 German baseline taxonomy review seal / Stage3 German baseline taksonomi inceleme mührü

## EN

Final state: **PASS**.

This document seals the German baseline human-logic taxonomy review chain after the Turkish leasing taxonomy patch/sync/live-swap was completed.

### Scope

- Language: `de`
- Language name: German
- Source DB: Ubuntu Desktop canonical taxonomy DB
- Runtime sync status before this stage: Desktop canonical DB and pi51c live taxonomy DB already matched after Stage2H.
- DB mutation in Stage3A/Stage3B: **FALSE**
- pi51c access in Stage3A/Stage3B: **FALSE**

### Stage3A baseline package

Stage3A regenerated the German baseline package from the Desktop canonical taxonomy DB because `_build` had previously been cleaned.

Verified German package counts:

| Metric | Value |
|---|---:|
| German all rows | `335` |
| German all non-low-risk priority rows | `218` |
| German manual-actionable priority rows | `14` |
| German P2 language-quality rows | `0` |
| German machine-phrase rows | `0` |
| German node-code-controlled service rows | `13` |
| German wide `service_side_row` diagnostic rows | `217` |
| German title/keyword-difference rows | `1` |

Important classification rule:

- The wide German `service_side_row` flag is diagnostic only.
- The manual-actionable service set is controlled by exact node codes:
  - `10.2.1`-`10.2.9`
  - `10.3.1`-`10.3.4`

### Stage3B human decision seal

Stage3B sealed the 14 German manual-actionable rows:

| Decision area | Result |
|---|---:|
| German manual-actionable decisions | `14` |
| German KEEP decisions | `14` |
| German patch-required rows | `0` |
| German service rows kept | `13` |
| German title/keyword-difference rows kept | `1` |

German patch required: **FALSE**.

The single title/keyword difference is intentionally kept:

- Node: `1.1`
- Title: `Straßengütertransport`
- Keyword: `Lkw-Transport`
- Reason: the title is broader for taxonomy display, while the keyword is narrower for search intent matching.

### Guard result

The taxonomy guard surface remained healthy:

- supported languages: `25`
- taxonomy nodes: `335`
- translations: `8375`
- keywords: `8375`
- search documents: `8375`
- duplicate primary keyword groups: `0`
- target-related duplicate groups: `0`
- blank/orphan/marker guards: `0`
- required function floor: **PASS**

### Final decision

German baseline review is accepted as-is.

No German DB patch is required.

Next step: continue the full 8375 title/keyword human-logic review with the next language baseline review.

## TR

Son durum: **PASS**.

Bu belge, Turkish leasing taxonomy patch/sync/live-swap tamamlandıktan sonra yapılan German baseline human-logic taxonomy review zincirini mühürler.

### Kapsam

- Dil: `de`
- Dil adı: German
- Kaynak DB: Ubuntu Desktop canonical taxonomy DB
- Bu aşamadan önce runtime sync durumu: Desktop canonical DB ve pi51c live taxonomy DB Stage2H sonrası eşleşmişti.
- Stage3A/Stage3B içinde DB mutation: **FALSE**
- Stage3A/Stage3B içinde pi51c erişimi: **FALSE**

### Stage3A baseline paketi

Stage3A, `_build` daha önce temizlendiği için German baseline paketini Desktop canonical taxonomy DB'den yeniden üretti.

Doğrulanan German paket sayıları:

| Metrik | Değer |
|---|---:|
| German tüm satırlar | `335` |
| German tüm non-low-risk priority satırlar | `218` |
| German manual-actionable priority satırlar | `14` |
| German P2 language-quality satırlar | `0` |
| German machine-phrase satırlar | `0` |
| German node-code-controlled service satırlar | `13` |
| German geniş `service_side_row` diagnostic satırlar | `217` |
| German title/keyword-difference satırlar | `1` |

Önemli sınıflandırma kuralı:

- Geniş German `service_side_row` flag'i yalnızca diagnostic olarak kullanılır.
- Manual-actionable service seti tam node code listesiyle kontrol edilir:
  - `10.2.1`-`10.2.9`
  - `10.3.1`-`10.3.4`

### Stage3B human decision seal

Stage3B, 14 German manual-actionable satırı mühürledi:

| Karar alanı | Sonuç |
|---|---:|
| German manual-actionable kararları | `14` |
| German KEEP kararları | `14` |
| German patch-required satırlar | `0` |
| KEEP edilen German service satırları | `13` |
| KEEP edilen German title/keyword-difference satırları | `1` |

German patch gerekli mi: **FALSE**.

Tek title/keyword farkı bilinçli olarak korundu:

- Node: `1.1`
- Title: `Straßengütertransport`
- Keyword: `Lkw-Transport`
- Gerekçe: title taxonomy gösterimi için daha geniş, keyword ise arama niyeti eşleşmesi için daha dar tutulur.

### Guard sonucu

Taksonomi guard yüzeyi sağlıklı kaldı:

- supported languages: `25`
- taxonomy nodes: `335`
- translations: `8375`
- keywords: `8375`
- search documents: `8375`
- duplicate primary keyword groups: `0`
- target-related duplicate groups: `0`
- blank/orphan/marker guard değerleri: `0`
- required function floor: **PASS**

### Nihai karar

German baseline review mevcut haliyle kabul edildi.

German için DB patch gerekmiyor.

Sonraki adım: 8375 title/keyword human-logic review hattında sıradaki dil baseline review ile devam etmek.
