# Outbox Core Commit Chronology Note - 2026-04-05

## Overview

This note records an observed commit-history clarity issue encountered during the repository-side maturation of the outbox-core surface on 2026-04-05.

The issue was not a structural SQL problem.  
It was a commit-history interpretation problem.

## Genel Bakış

Bu not, 2026-04-05 tarihinde outbox-core yüzeyinin repository-side olgunlaştırılması sırasında gözlenen bir commit-geçmişi açıklığı sorununu kayda geçirir.

Sorun yapısal bir SQL sorunu değildi.  
Bu, commit geçmişinin yorumlanmasıyla ilgili bir sorundu.

## Observed chronology fact

Two different commits used the same title:

- `7c7877d` → `docs(outbox-core): record live operational reality audit`
- `44e08e0` → `docs(outbox-core): record live operational reality audit`

However, the actual changed surfaces were different:

- `7c7877d` introduced `LIVE_OPERATIONAL_REALITY_AUDIT_2026-04-05.md`
- `44e08e0` updated `README.md` to link and reflect that newly added live-operational audit layer

## Gözlenen kronoloji gerçeği

Aynı başlığı kullanan iki farklı commit gözlendi:

- `7c7877d` → `docs(outbox-core): record live operational reality audit`
- `44e08e0` → `docs(outbox-core): record live operational reality audit`

Ancak gerçekte değişen yüzeyler farklıydı:

- `7c7877d`, `LIVE_OPERATIONAL_REALITY_AUDIT_2026-04-05.md` dosyasını ekledi
- `44e08e0`, bu yeni canlı-operasyonel audit katmanını bağlamak ve yansıtmak için `README.md` dosyasını güncelledi

## Why this mattered

The repository state itself remained technically correct.

But the repeated title made later audit reading less clear than desired.

The problem was therefore:

- not technical correctness
- but chronology readability and semantic precision in commit history

## Bu neden önemliydi

Repository durumu teknik olarak doğru kalmaya devam etti.

Ancak aynı başlığın tekrarı, sonraki audit okumalarını istenenden daha az net hale getirdi.

Dolayısıyla sorun şuydu:

- teknik doğruluk sorunu değil
- commit geçmişinde kronoloji okunabilirliği ve semantik hassasiyet sorunu

## Resulting standardization decision

Because of this observed case, commit naming discipline was explicitly added to:

- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`

The practical rule derived from this case is:

1. different semantic actions should use different commit titles
2. README alignment should not share the same title as first-time content creation
3. commit titles should describe the real changed surface, not only the broad topic

## Bu gözlemden çıkan standardizasyon kararı

Bu gözlenen vaka nedeniyle commit adlandırma disiplini açıkça şu belgeye işlendi:

- `WORKING_STYLE_AND_VALIDATION_DISCIPLINE.md`

Bu vakadan türetilen pratik kural şudur:

1. farklı semantik işlemler farklı commit başlıkları kullanmalıdır
2. README hizalaması, ilk kez içerik ekleme ile aynı başlığı paylaşmamalıdır
3. commit başlıkları yalnızca geniş konuyu değil, gerçek değişim yüzeyini tarif etmelidir

## Sealed interpretation

This note exists so that future audits can understand:

- why commit naming discipline was strengthened
- which concrete outbox-core commits motivated that rule
- that the rule was derived from an observed real chronology case, not from abstract preference alone

## Mühürlü yorum

Bu not, gelecekteki audit'lerin şunları anlayabilmesi için vardır:

- commit adlandırma disiplininin neden güçlendirildiği
- bu kuralı hangi somut outbox-core commit'lerinin tetiklediği
- kuralın yalnızca soyut tercihten değil, gözlenen gerçek bir kronoloji vakasından türetildiği
