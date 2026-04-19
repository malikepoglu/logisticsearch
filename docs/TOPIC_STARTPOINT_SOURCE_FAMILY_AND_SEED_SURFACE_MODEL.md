# Startpoint Source Family and Seed Surface Model
# Startpoint Source Family ve Seed Surface Modeli

## Purpose
## Amaç

This document defines the canonical modeling rule for LogisticSearch startpoints.

Bu doküman, LogisticSearch startpoint modellemesi için kanonik kuralı tanımlar.

The goal is to prevent source hierarchy drift, avoid fake top-level source inflation, and keep crawler pacing, cross-seed traversal, and cross-language traversal logically coherent.

Amaç; source hiyerarşisinin bozulmasını önlemek, sahte üst düzey source şişmesini engellemek ve crawler pacing, cross-seed traversal ile cross-language traversal mantığını tutarlı tutmaktır.

## Core Rule
## Temel Kural

A top-level source must represent the main source family, source root, or source ecosystem, not every path-level variation.

Bir üst düzey source, her path varyasyonunu değil, ana source family, source root veya source ecosystem düzeyini temsil etmelidir.

If the host, institution, and main ecosystem are the same, they must stay inside one source family.

Host, kurum ve ana ekosistem aynıysa bunlar tek bir source family içinde kalmalıdır.

Country, language, section, or path differences under the same ecosystem must be represented below that family, not as separate fake top-level sources.

Aynı ekosistem altındaki ülke, dil, bölüm veya path farkları, ayrı sahte üst düzey source olarak değil, o family’nin altında temsil edilmelidir.

## Practical Hierarchy
## Pratik Hiyerarşi

The canonical hierarchy is:

Kanonik hiyerarşi şöyledir:

1. Source family  
2. Surface  
3. Seed

1. Source family  
2. Surface  
3. Seed

## Source Family
## Source Family

A source family answers this question: which main source ecosystem is this?

Source family şu soruya cevap verir: bu hangi ana kaynak ekosistemidir?

Examples include:

Örnekler şunlardır:

- `fiata.org`
- `bifa.org`
- `wcaworld.com`
- `freightnet.com`
- `thomasnet.com`
- `kompass.com`
- `europages.co.uk`

This level stores the durable identity and default crawling policy of the source ecosystem.

Bu seviye, kaynak ekosisteminin kalıcı kimliğini ve varsayılan crawl politikasını taşır.

## Surface
## Surface

A surface answers this question: which discovery surface inside that source family are we entering?

Surface şu soruya cevap verir: bu source family içinde hangi keşif yüzeyine giriyoruz?

Examples include:

Örnekler şunlardır:

- directory
- member search
- country member directory
- category page
- ranking page
- marketplace query page
- network overview
- regional directory

This level exists to preserve site structure without flattening every path into a fake top-level source.

Bu seviye, site yapısını korumak ve her path’i sahte bir üst düzey source’a dönüştürmemek için vardır.

## Seed
## Seed

A seed answers this question: which exact URL will the crawler enter first?

Seed şu soruya cevap verir: crawler ilk olarak tam hangi URL’den içeri girecek?

Examples include:

Örnekler şunlardır:

- `https://fiata.org/directory/`
- `https://fiata.org/directory/de/`
- `https://fiata.org/directory/fr/`

A source family can have many seed surfaces.

Bir source family altında birden fazla seed surface olabilir.

## Important Modeling Correction
## Önemli Model Düzeltmesi

It is incorrect to treat these as separate top-level sources:

Şunları ayrı üst düzey source saymak yanlıştır:

- `https://fiata.org/directory/de/`
- `https://fiata.org/directory/fr/`
- `https://fiata.org/directory/gb/`

They are not different source families.

Bunlar farklı source family değildir.

They are different seed surfaces under the same source family rooted at `fiata.org`.

Bunlar, kökü `fiata.org` olan aynı source family altındaki farklı seed surface’lerdir.

## Why This Matters
## Bu Neden Önemli

This model gives the crawler a coherent source graph.

Bu model, crawler’a tutarlı bir source grafiği verir.

This keeps host-level pacing correct.

Bu, host-level pacing’in doğru kalmasını sağlar.

This allows many same-host seeds to share one crawl budget.

Bu, aynı host altındaki çoklu seed’in tek bir crawl budget paylaşmasını sağlar.

This makes cross-seed traversal inside the same ecosystem natural.

Bu, aynı ekosistem içindeki cross-seed traversal’ı doğal hale getirir.

This keeps cross-language traversal controlled without duplicating top-level source identity.

Bu, üst düzey source kimliğini çoğaltmadan cross-language traversal’ı kontrollü tutar.

## Capacity Model
## Kapasite Modeli

LogisticSearch must use a variable-capacity multilingual source catalog, not a fixed equal quota per language.

LogisticSearch, dil başına eşit sabit kota değil, değişken kapasiteli çok dilli source kataloğu kullanmalıdır.

This means English may have far more candidate seed surfaces than smaller languages.

Bu, İngilizcenin küçük dillere göre çok daha fazla aday seed surface içerebileceği anlamına gelir.

Some languages may have 50 plus worthwhile seed surfaces.

Bazı dillerde 50’den fazla değerli seed surface olabilir.

Some languages may have only 5 plus worthwhile seed surfaces.

Bazı dillerde sadece 5’ten fazla değerli seed surface olabilir.

Quality matters more than equal counts.

Önemli olan eşit sayı değil, kalite ve gerçek kaynak bulunabilirliğidir.

## Correct Planning Shape
## Doğru Planlama Şekli

The preferred planning shape is not fifty fake top-level sources.

Tercih edilen planlama şekli, elli sahte üst düzey source değildir.

The preferred planning shape is closer to twelve to twenty source families and thirty to sixty seed surfaces.

Tercih edilen planlama şekli, on iki ila yirmi source family ve otuz ila altmış seed surface yaklaşımına daha yakındır.

This keeps source-family-level pacing and seed-level entry diversity together.

Bu, source-family-level pacing ile seed-level entry diversity’yi birlikte korur.

## Quality Tiers
## Kalite Katmanları

Candidate source families and surfaces should be reviewed in tiers.

Aday source family ve surface’ler katmanlı biçimde incelenmelidir.

Tier A means official association, member, or network directories.

Tier A, resmi dernek, üye veya network dizinleri anlamına gelir.

Tier B means commercial directories, B2B supplier surfaces, or marketplace surfaces.

Tier B, ticari dizinler, B2B supplier yüzeyleri veya marketplace yüzeyleri anlamına gelir.

Tier C means discovery-only surfaces such as rankings or editorial lists.

Tier C, ranking veya editorial liste gibi discovery-only yüzeyler anlamına gelir.

## Operational Review Rule
## Operasyonel İnceleme Kuralı

Before inserting into live seed tables, each candidate seed surface must be reviewed individually.

Canlı seed tablolarına insert etmeden önce her aday seed surface tek tek incelenmelidir.

Review must stay lightweight first.

İnceleme önce hafif kalmalıdır.

Robots-first discipline must be respected.

Robots-first disiplini korunmalıdır.

Browser use must stay exceptional, not default.

Browser kullanımı varsayılan değil, istisnai kalmalıdır.

Same-host checks must be spaced out.

Aynı host üzerindeki kontroller zamana yayılmalıdır.

Cross-host round-robin should be preferred.

Cross-host round-robin tercih edilmelidir.

## Canonical Conclusion
## Kanonik Sonuç

Do not inflate source count artificially.

Source sayısını yapay olarak şişirme.

Treat the main site or ecosystem as the source family.

Ana siteyi veya ekosistemi source family olarak ele al.

Represent country, language, section, and path differences as seed surfaces and metadata beneath that family.

Ülke, dil, bölüm ve path farklarını o family altında seed surface ve metadata ile temsil et.

Let frontier and discovery handle cross-seed and cross-language traversal.

Cross-seed ve cross-language traversal işini frontier ve discovery katmanına bırak.

Keep host-level pacing attached to the source-family reality.

Host-level pacing’i source-family gerçeğine bağlı tut.
