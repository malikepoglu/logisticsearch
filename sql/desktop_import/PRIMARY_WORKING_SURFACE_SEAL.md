# Desktop Import Primary Working Surface Seal

## Overview

This document records the decision about which file should now be treated as the primary working surface for `sql/desktop_import`.

This decision is made only after:

- live snapshot capture
- inventory and hash capture
- README / chronology / role interpretation
- structural equivalence audit between live schema and repository contract

## Genel Bakış

Bu belge, `sql/desktop_import` için artık hangi dosyanın ana çalışma yüzeyi olarak ele alınacağına dair kararı kayda geçirir.

Bu karar ancak şu adımlardan sonra verilmektedir:

- canlı snapshot yakalama
- inventory ve hash yakalama
- README / kronoloji / rol yorumu
- canlı şema ile repository contract arasındaki yapısal eşdeğerlik denetimi

## Sealed decision

At the current sealed point, the primary working surface is:

- `001_pi51_batch_intake_contract.sql`

## Mühürlü karar

Mevcut mühürlü noktada ana çalışma yüzeyi şudur:

- `001_pi51_batch_intake_contract.sql`

## Why this file is the primary working surface

This file is selected as the primary working surface because:

1. it is executable
2. it is repository-side
3. it is human-maintained and evolution-friendly
4. it has been structurally verified against the live observed `desktop_import` schema
5. it is the correct place to begin controlled future SQL evolution

## Bu dosyanın neden ana çalışma yüzeyi olduğu

Bu dosya ana çalışma yüzeyi olarak seçilmiştir; çünkü:

1. çalıştırılabilirdir
2. repository-side'dır
3. insan tarafından sürdürülebilir ve evrime uygundur
4. canlı gözlenen `desktop_import` şemasına karşı yapısal olarak doğrulanmıştır
5. kontrollü gelecekteki SQL evriminin doğru başlangıç noktasıdır

## Role of the live snapshot after this seal

After this seal, the live snapshot trio still remains important, but its role is now clearly secondary:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Their role is:

- evidence
- comparison baseline
- live-state reference

They are not the primary editing surface.

## Bu mühürden sonra canlı snapshot'ın rolü

Bu mühürden sonra canlı snapshot üçlüsü önemini korur, ancak rolü artık açık biçimde ikincildir:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Bunların rolü şudur:

- kanıt
- karşılaştırma tabanı
- canlı durum referansı

Bunlar ana düzenleme yüzeyi değildir.

## Working rule from this point

From this point onward:

1. preserve the live snapshot trio as evidence
2. treat `001_pi51_batch_intake_contract.sql` as the primary working SQL surface
3. make future structural changes there first
4. re-audit against live or scratch when changes become meaningful
5. document the evolution in the same disciplined repository style

## Bu noktadan sonraki çalışma kuralı

Bu noktadan sonra:

1. canlı snapshot üçlüsünü kanıt olarak koru
2. `001_pi51_batch_intake_contract.sql` dosyasını ana çalışma SQL yüzeyi olarak ele al
3. gelecekteki yapısal değişiklikleri önce burada yap
4. değişiklikler anlamlı hale geldiğinde canlı veya scratch karşısında yeniden denetle
5. evrimi aynı disiplinli repository stiliyle belgeye işle

## Practical meaning

This seal changes the status of `sql/desktop_import`.

Previously, the surface was in a pre-decision interpretation phase.

Now it has a confirmed primary working surface.

That means future work should no longer hesitate about where controlled SQL evolution belongs.

## Pratik anlamı

Bu mühür, `sql/desktop_import` yüzeyinin statüsünü değiştirir.

Önceden bu yüzey karar öncesi yorum fazındaydı.

Şimdi ise doğrulanmış bir ana çalışma yüzeyine sahiptir.

Bu da gelecekteki işin kontrollü SQL evriminin nereye ait olduğu konusunda artık tereddüt etmemesi gerektiği anlamına gelir.

## Next continuation point

After this seal, the next normal work should be one of these:

- add execution entry points around the primary working surface
- add preflight / presence audit surfaces
- add scratch validation runner
- standardize the package toward the same maturity model used in other SQL surfaces

## Sonraki devam noktası

Bu mühürden sonra sıradaki normal iş şu alanlardan biri olmalıdır:

- ana çalışma yüzeyi etrafına execution giriş noktaları eklemek
- preflight / presence audit yüzeyleri eklemek
- scratch validation runner eklemek
- paketi diğer SQL yüzeylerinde kullanılan olgunluk modeline doğru standartlaştırmak
