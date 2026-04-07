# Repository Artifact Numbering Standard

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document defines the canonical numbering standard for ordered repository artifacts in LogisticSearch.

The goal is to make numbered files readable, predictable, scalable, and structurally consistent across SQL, Python, JavaScript, shell helpers, data-flow helpers, and future execution surfaces.

A numbered prefix must never be treated as cosmetic. It carries structural meaning.

## Genel Bakış

Bu belge, LogisticSearch içindeki sıralı repository artefact'ları için kanonik numaralandırma standardını tanımlar.

Amaç; numaralı dosyaları SQL, Python, JavaScript, shell yardımcıları, veri akışı yardımcıları ve gelecekteki execution yüzeyleri boyunca okunabilir, öngörülebilir, ölçeklenebilir ve yapısal olarak tutarlı hale getirmektir.

Numaralı bir önek asla kozmetik kabul edilmemelidir. Yapısal anlam taşır.

## Core rule

A numbered artifact expresses two things at once:

1. **band meaning** — what class of artifact this is
2. **ordinal meaning** — where this artifact sits inside that class

Therefore:

- the **range** carries the artifact-family meaning
- the **exact number** carries the ordered position inside that family

Example:

- `004_frontier_politeness_and_freshness.sql`

does **not** mean that number `004` universally means politeness.  
It means:

- this file belongs to an early ordered working-artifact band
- it is the 4th ordered artifact in that surface

## Temel kural

Numaralı bir artefact aynı anda iki şeyi ifade eder:

1. **bant anlamı** — bunun hangi artefact sınıfına ait olduğu
2. **sıra anlamı** — bu artefact'ın o sınıf içindeki yeri

Dolayısıyla:

- **aralık**, artefact ailesinin anlamını taşır
- **tam sayı**, o aile içindeki sıralı konumu taşır

Örnek:

- `004_frontier_politeness_and_freshness.sql`

şu anlama **gelmez**: `004` sayısı evrensel olarak politeness demektir.  
Şu anlama gelir:

- bu dosya erken sıralı çalışma-artefact bandına aittir
- bu yüzeydeki 4. sıralı artefact'tır

## Canonical 3-digit bands

### `001–099` — early ordered working surface

Use this band for the earliest and most foundational ordered artifacts inside a surface.

Typical meanings:

- imported baseline truth files
- foundational split working files
- first chronology-aligned packages
- first dependency-ordered executable artifacts

Interpretation rule:

- `001` = first foundational artifact in that surface
- `002` = second foundational artifact
- `003` = third foundational artifact
- etc.

This band is where the most important early structural files normally live.

### `100–699` — extended ordered working surface

Use this band when the surface grows beyond its earliest foundational files.

Typical meanings:

- additional split packages
- later chronology-aligned modules
- growing contract families
- structured domain expansion packs

Interpretation rule:

- lower number = earlier dependency / earlier chronology / earlier structural priority
- higher number = later addition inside the same working family

### `700–799` — reference / comparison support band

Use this band only when a surface needs numbered reference companions beyond the earliest baseline set.

Typical meanings:

- imported comparison bundles
- secondary comparison surfaces
- generated reference packs that remain version-worthy

This band should be used sparingly.

### `800–899` — transition / compatibility / support reserve

Reserved for advanced support cases such as:

- compatibility layers
- temporary transition packs
- structured support helpers
- late support artifacts that should remain distinct from the main working series

This band should not become a dump zone.

## Kanonik 3 haneli bantlar

### `001–099` — erken sıralı çalışma yüzeyi

Bu bant, bir yüzey içindeki en erken ve en temel sıralı artefact'lar için kullanılır.

Tipik anlamlar:

- ithal edilmiş baseline truth dosyaları
- temel split çalışma dosyaları
- ilk chronology uyumlu paketler
- ilk dependency sıralı çalıştırılabilir artefact'lar

Yorum kuralı:

- `001` = o yüzeydeki ilk temel artefact
- `002` = ikinci temel artefact
- `003` = üçüncü temel artefact
- vb.

En önemli erken yapısal dosyalar normalde bu bantta yaşar.

### `100–699` — genişleyen sıralı çalışma yüzeyi

Yüzey ilk temel dosyalarının ötesine büyüdüğünde bu bant kullanılır.

Tipik anlamlar:

- ek split paketler
- daha geç chronology uyumlu modüller
- büyüyen contract aileleri
- yapısal domain genişleme paketleri

Yorum kuralı:

- düşük sayı = daha erken bağımlılık / daha erken chronology / daha yüksek yapısal öncelik
- yüksek sayı = aynı çalışma ailesi içinde daha geç ekleme

### `700–799` — referans / karşılaştırma destek bandı

Bir yüzeyin, ilk baseline setinin ötesinde numaralı referans eşlikçilere ihtiyacı olduğunda kullanılır.

Tipik anlamlar:

- imported comparison bundle'ları
- ikincil comparison yüzeyleri
- versiyonlanmaya değer üretilmiş referans paketleri

Bu bant seyrek kullanılmalıdır.

### `800–899` — geçiş / uyumluluk / destek rezervi

Aşağıdaki gelişmiş destek durumları için ayrılmıştır:

- uyumluluk katmanları
- geçici geçiş paketleri
- yapısal destek yardımcıları
- ana çalışma serisinden ayrı tutulması gereken geç destek artefact'ları

Bu bant bir döküm alanına dönüşmemelidir.

## Canonical execution and validation family

### `900–909` — execution entry points

This family is reserved for canonical execution-control artifacts.

Recommended meanings:

- `900` = canonical apply / execution bundle
- `901` = canonical preflight
- `902` = canonical presence audit
- `903` = canonical equivalence / shape audit
- `904` = canonical smoke / integration check
- `905` = canonical rollback / undo helper
- `906` = canonical repair / rebuild helper
- `907` = canonical replay / backfill helper
- `908` = canonical release / packaging helper
- `909` = reserved

Not every surface must use every number.  
But if a number is used, its role should remain consistent.

### `910–919` — reusable validation runners

This family is reserved for reusable validation wrappers.

Recommended meanings:

- `910` = canonical one-command validation runner
- `911` = scratch reset + validate runner
- `912` = integration validation runner
- `913` = performance / load validation runner
- `914` = dependency validation runner
- `915` = portability / environment validation runner
- `916–919` = reserved

### `920–999` — advanced audit / repair / seal reserve

Reserved for later advanced control artifacts such as:

- specialized audits
- state-repair helpers
- seal builders
- freeze helpers
- transition retirement helpers
- emergency structured support tools

Use only with discipline.

## Kanonik execution ve validation ailesi

### `900–909` — execution giriş noktaları

Bu aile, kanonik execution-control artefact'ları için ayrılmıştır.

Önerilen anlamlar:

- `900` = kanonik apply / execution bundle
- `901` = kanonik preflight
- `902` = kanonik presence audit
- `903` = kanonik equivalence / shape audit
- `904` = kanonik smoke / integration check
- `905` = kanonik rollback / undo helper
- `906` = kanonik repair / rebuild helper
- `907` = kanonik replay / backfill helper
- `908` = kanonik release / packaging helper
- `909` = rezerv

Her yüzeyin her numarayı kullanması gerekmez.  
Ama bir numara kullanılıyorsa, rolü tutarlı kalmalıdır.

### `910–919` — reusable validation runner'lar

Bu aile, reusable validation sarmalayıcıları için ayrılmıştır.

Önerilen anlamlar:

- `910` = kanonik tek-komut validation runner
- `911` = scratch reset + validate runner
- `912` = integration validation runner
- `913` = performance / load validation runner
- `914` = dependency validation runner
- `915` = portability / environment validation runner
- `916–919` = rezerv

### `920–999` — ileri audit / repair / seal rezervi

Aşağıdaki gibi ileri kontrol artefact'ları için ayrılmıştır:

- özelleşmiş audit'ler
- state-repair yardımcıları
- seal builder'lar
- freeze yardımcıları
- transition retirement yardımcıları
- acil durum yapısal destek araçları

Yalnızca disiplinli şekilde kullanılmalıdır.

## 4-digit extension model

The project may later use 4-digit prefixes if a surface grows significantly.

### `0001–0899`

Extended ordered working-artifact space.

Use this if 3-digit space becomes too cramped or if a surface becomes large enough to justify a wider ordered series.

### `0900–0999`

Extended execution / validation family with the same role logic as `900–999`.

Examples:

- `0900` apply
- `0901` preflight
- `0902` presence audit
- `0910` validation runner

### `1000–7999`

Large-scale extended ordered artifact space.

Reserved for very large surfaces that outgrow the shorter form.

### `8000–8999`

Large-scale support / compatibility / transition reserve.

### `9000–9999`

Large-scale execution / validation / audit / repair reserve.

The project should **not** jump to 4-digit numbering without need.  
Use it only when scale genuinely requires it.

## 4 haneli genişleme modeli

Yüzey ciddi biçimde büyürse proje daha sonra 4 haneli önekler kullanabilir.

### `0001–0899`

Genişletilmiş sıralı çalışma-artefact alanı.

3 haneli alan dar gelmeye başlarsa veya yüzey daha geniş bir sıralı seri gerektirecek kadar büyürse kullanılır.

### `0900–0999`

`900–999` ile aynı rol mantığını koruyan genişletilmiş execution / validation ailesi.

Örnekler:

- `0900` apply
- `0901` preflight
- `0902` presence audit
- `0910` validation runner

### `1000–7999`

Çok büyük yüzeyler için geniş ölçekli sıralı artefact alanı.

### `8000–8999`

Geniş ölçekli support / compatibility / transition rezervi.

### `9000–9999`

Geniş ölçekli execution / validation / audit / repair rezervi.

Proje ihtiyaç yokken 4 haneli numaralandırmaya **atlamamalıdır**.  
Sadece ölçek gerçekten gerektirirse kullanılmalıdır.

## Current concrete examples in LogisticSearch

Examples already visible in the repository:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`
- `900_apply_crawler_core_split_surface.psql.sql`
- `901_preflight_crawler_core_split_surface.psql.sql`
- `902_presence_audit_crawler_core_split_surface.psql.sql`
- `910_validate_crawler_core_split_surface.sh`

Meaning:

- `001–005` are early ordered working artifacts in the crawler-core surface
- `900` is the canonical apply bundle
- `901` is the canonical preflight
- `902` is the canonical presence audit
- `910` is the canonical one-command validation runner

## LogisticSearch içindeki güncel somut örnekler

Repository içinde şimdiden görülen örnekler:

- `001_seed_frontier_http_fetch_base.sql`
- `002_frontier_claim_and_lease.sql`
- `003_frontier_finish_transitions.sql`
- `004_frontier_politeness_and_freshness.sql`
- `005_http_fetch_robots_cache_and_enforcement.sql`
- `900_apply_crawler_core_split_surface.psql.sql`
- `901_preflight_crawler_core_split_surface.psql.sql`
- `902_presence_audit_crawler_core_split_surface.psql.sql`
- `910_validate_crawler_core_split_surface.sh`

Anlamı şudur:

- `001–005`, crawler-core yüzeyi içindeki erken sıralı çalışma artefact'larıdır
- `900`, kanonik apply bundle'dır
- `901`, kanonik preflight'tır
- `902`, kanonik presence audit'tir
- `910`, kanonik tek-komut validation runner'dır

## Rules for future use

1. Do not invent ad-hoc meanings per file.
2. Keep range semantics stable across the repository.
3. Let README / file map explain the role of concrete files within a surface.
4. Let the number express order, not marketing.
5. Do not renumber casually once a surface is sealed.
6. Prefer consistency over cleverness.
7. If a new number family is introduced, document it first.

## Gelecekte kullanım kuralları

1. Dosya bazında keyfi anlam uydurma.
2. Aralık semantiklerini repository boyunca sabit tut.
3. Yüzey içindeki somut dosya rolünü README / file map ile açıkla.
4. Numara pazarlama değil, sıra anlamı taşısın.
5. Bir yüzey mühürlendikten sonra gelişigüzel renumber yapma.
6. Zekice numara oyunları yerine tutarlılığı tercih et.
7. Yeni bir numara ailesi getirilecekse önce dokümante et.

## Explicit non-goals

This standard does **not** mean:

- every directory must use every number
- every file must be numbered
- every `004` across the repository means the same business concept
- documentation files must always be numbered

Human guidance documents such as `README.md`, `NEXT_STEP.md`, and `PRIMARY_WORKING_SURFACE_SEAL.md` may remain unnumbered when that is clearer.

## Açık non-goal'ler

Bu standart şu anlama **gelmez**:

- her dizin her numarayı kullanmak zorundadır
- her dosya numaralı olmak zorundadır
- repository içindeki her `004`, aynı iş kavramını ifade eder
- dokümantasyon dosyaları mutlaka numaralı olmak zorundadır

`README.md`, `NEXT_STEP.md` ve `PRIMARY_WORKING_SURFACE_SEAL.md` gibi insan-yönelimli rehber dokümanlar daha netse numarasız kalabilir.

## Immediate consequence for crawler work

For upcoming crawler-core work, the practical reading is:

- `001–005` are the current ordered crawler-core working SQL files
- `004_frontier_politeness_and_freshness.sql` is important now because it is the 4th ordered crawler-core artifact and currently carries the politeness / backoff / revisit timing logic
- that importance comes from its **content**, not from the mystical meaning of number 4

## Yaklaşan crawler işi için anlık sonuç

Yaklaşan crawler-core işi açısından pratik okuma şudur:

- `001–005`, mevcut sıralı crawler-core çalışma SQL dosyalarıdır
- `004_frontier_politeness_and_freshness.sql`, şu anda 4. sıralı crawler-core artefact olduğu ve politeness / backoff / revisit timing mantığını taşıdığı için önemlidir
- bu önem, 4 sayısının mistik anlamından değil, dosyanın **içeriğinden** gelir
