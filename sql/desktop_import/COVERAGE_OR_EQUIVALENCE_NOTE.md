# Desktop Import Coverage / Equivalence Note

## Overview

This document records the current equivalence judgement between the live observed `desktop_import` schema and the repository-side executable contract.

It exists to answer a previously open question:

Does `001_pi51_batch_intake_contract.sql` actually match the currently observed live `desktop_import` structure on Ubuntu Desktop?

## Genel Bakış

Bu belge, canlı gözlenen `desktop_import` şeması ile repository-side çalıştırılabilir contract arasındaki mevcut eşdeğerlik hükmünü kayda geçirir.

Bu belge daha önce açık kalan şu soruya cevap vermek için vardır:

`001_pi51_batch_intake_contract.sql`, Ubuntu Desktop üzerindeki şu anda gözlenen canlı `desktop_import` yapısıyla gerçekten eşleşiyor mu?

## Audit basis

The judgement in this note is based on the structural equivalence audit performed on 2026-04-06.

Audit method summary:

1. recreate scratch database
2. apply `001_pi51_batch_intake_contract.sql` into scratch
3. compare live `logisticsearch.desktop_import` vs scratch structure
4. compare these object families:
   - tables
   - sequences
   - columns
   - constraints
   - indexes

## Denetim temeli

Bu belgedeki hüküm, 2026-04-06 tarihinde yapılan yapısal eşdeğerlik denetimine dayanır.

Denetim yöntemi özeti:

1. scratch veritabanını yeniden oluştur
2. `001_pi51_batch_intake_contract.sql` dosyasını scratch'e uygula
3. canlı `logisticsearch.desktop_import` yapısını scratch ile karşılaştır
4. şu nesne ailelerini karşılaştır:
   - tablolar
   - sequence'ler
   - kolonlar
   - constraint'ler
   - index'ler

## Audited result

At the audited layer, no structural difference was observed between live and scratch.

Observed result:

- table diff: none
- sequence diff: none
- column diff: none
- constraint diff: none
- index diff: none

Observed audited counts:

- tables: 2
- sequences: 1
- columns: 29
- constraints: 23
- indexes: 6

## Denetlenen sonuç

Denetlenen katmanda canlı yapı ile scratch yapı arasında yapısal fark gözlenmemiştir.

Gözlenen sonuç:

- tablo farkı: yok
- sequence farkı: yok
- kolon farkı: yok
- constraint farkı: yok
- index farkı: yok

Gözlenen denetim sayıları:

- tablo: 2
- sequence: 1
- kolon: 29
- constraint: 23
- index: 6

## Practical judgement

The practical judgement is:

`001_pi51_batch_intake_contract.sql` is structurally equivalent to the currently observed live `desktop_import` schema at the audited layer.

This means the repository-side executable contract is not merely approximate.

At the audited structural layer, it accurately reproduces the live schema shape.

## Pratik hüküm

Pratik hüküm şudur:

`001_pi51_batch_intake_contract.sql`, denetlenen katmanda şu anda gözlenen canlı `desktop_import` şemasıyla yapısal olarak eşdeğerdir.

Bu, repository-side çalıştırılabilir contract'ın yalnızca yaklaşık bir taslak olmadığını gösterir.

Denetlenen yapısal katmanda canlı şema biçimini doğru şekilde yeniden üretmektedir.

## Important scope boundary

This equivalence note is strong, but still scope-bounded.

It records audited structural equivalence for:

- tables
- sequences
- columns
- constraints
- indexes

It does not try to claim broader semantic workflow equivalence beyond that scope.

## Önemli kapsam sınırı

Bu eşdeğerlik notu güçlüdür, ancak yine de kapsamla sınırlıdır.

Şu alanlarda denetlenmiş yapısal eşdeğerliği kayda geçirir:

- tablolar
- sequence'ler
- kolonlar
- constraint'ler
- index'ler

Bunun ötesinde daha geniş semantik workflow eşdeğerliği iddiasında bulunmaz.

## Consequence for surface roles

Because of this result, the role model becomes clearer:

- live snapshot files remain evidence
- the executable contract file is confirmed as structurally aligned executable truth

This result also supports the later primary-working-surface decision.

## Yüzey rolleri açısından sonucu

Bu sonuç sayesinde rol modeli daha net hale gelir:

- canlı snapshot dosyaları kanıt olarak kalır
- çalıştırılabilir contract dosyası yapısal olarak hizalı yürütülebilir doğruluk olarak doğrulanır

Bu sonuç, daha sonra verilen ana çalışma yüzeyi kararını da destekler.

## Decision consequence

After this equivalence result, the project sealed the next decision:

- `001_pi51_batch_intake_contract.sql` is now the primary working surface

That decision is recorded in:

- `PRIMARY_WORKING_SURFACE_SEAL.md`

## Karar sonucu

Bu eşdeğerlik sonucundan sonra proje şu kararı mühürlemiştir:

- `001_pi51_batch_intake_contract.sql` artık ana çalışma yüzeyidir

Bu karar şu belgede kaydedilmiştir:

- `PRIMARY_WORKING_SURFACE_SEAL.md`

## Current rule after equivalence audit

For the current state:

1. preserve the snapshot trio as evidence
2. preserve the contract file as executable truth
3. treat structural equivalence as verified
4. treat the primary working surface decision as already sealed

## Eşdeğerlik denetimi sonrası güncel kural

Mevcut durumda:

1. snapshot üçlüsünü kanıt olarak koru
2. contract dosyasını yürütülebilir doğruluk olarak koru
3. yapısal eşdeğerliği doğrulanmış kabul et
4. ana çalışma yüzeyi kararını zaten mühürlenmiş kabul et
