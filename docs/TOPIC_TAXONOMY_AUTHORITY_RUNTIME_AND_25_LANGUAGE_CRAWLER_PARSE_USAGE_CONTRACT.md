# Topic: Taxonomy Authority, Runtime, and 25-Language Crawler/Parse Usage Contract

## Canonical 25-language exact order

## Kanonik 25 dil için exact sıra

EN: The canonical exact order is:
TR: Kanonik exact sıra şudur:

"ar" "bg" "cs" "de" "el" "en" "es" "fr" "hu" "it" "ja" "ko" "nl" "pt" "ro" "ru" "tr" "zh" "hi" "bn" "ur" "uk" "id" "vi" "he"

# Konu: Taksonomi Otoritesi, Runtime ve 25 Dilli Crawler/Parse Kullanım Sözleşmesi

## Purpose
## Amaç

This document freezes the current canonical design rule for how taxonomy must be owned, replicated, and used across Ubuntu Desktop and `makpi51crawler`.

Bu belge, taksonominin Ubuntu Desktop ve `makpi51crawler` arasında nasıl sahiplenileceği, çoğaltılacağı ve kullanılacağı konusundaki güncel kanonik tasarım kuralını dondurur.

It exists to prevent drift between:

- authority taxonomy design
- crawler runtime lookup behavior
- parse classification behavior
- GitHub-tracked repository truth
- Pi51 live runtime truth

Şu katmanlar arasında drift oluşmasını engellemek için vardır:

- authority taxonomy tasarımı
- crawler runtime lookup davranışı
- parse sınıflandırma davranışı
- GitHub’da izlenen repository doğrusu
- Pi51 canlı runtime doğrusu

## Canonical role split
## Kanonik rol ayrımı

### Ubuntu Desktop = taxonomy authority
### Ubuntu Desktop = taxonomy otoritesi

Ubuntu Desktop is the canonical authority for taxonomy design.

Ubuntu Desktop, taxonomy tasarımının kanonik otoritesidir.

Authority responsibilities include:

- defining the normalized `logistics` taxonomy structure
- enforcing constraints and indexes
- maintaining closure truth
- preparing translations and keywords
- maintaining overlay truth
- versioning the taxonomy package
- deciding what Pi51 runtime should consume

Authority sorumlulukları şunları içerir:

- normalize `logistics` taxonomy yapısını tanımlamak
- constraint ve index kurallarını uygulamak
- closure doğrusunu korumak
- translation ve keyword katmanlarını hazırlamak
- overlay doğrusunu korumak
- taxonomy paketini versiyonlamak
- Pi51 runtime’ın neyi tüketeceğine karar vermek

### Pi51crawler = taxonomy runtime consumer
### Pi51crawler = taxonomy runtime tüketicisi

`makpi51crawler` is not the taxonomy authority.

`makpi51crawler`, taxonomy otoritesi değildir.

It is the runtime consumer that must hold a fast, queryable, local taxonomy copy suitable for crawler and parse operations.

Crawler ve parse işlemlerine uygun, hızlı, sorgulanabilir, yerel bir taxonomy kopyasını taşıyan runtime tüketicisidir.

Pi51 responsibilities include:

- keeping a runtime-ready taxonomy surface
- serving crawler_core lookups
- serving parse_core lookups
- staying aligned with the authority package
- never silently inventing taxonomy truth that is not sealed upstream

Pi51 sorumlulukları şunları içerir:

- runtime-hazır taxonomy yüzeyini tutmak
- crawler_core lookup’larını beslemek
- parse_core lookup’larını beslemek
- authority paketi ile hizalı kalmak
- upstream’de mühürlenmemiş taxonomy doğrusunu sessizce uydurmamak

## Hard rule: crawler_core also uses the 25-language layer
## Sert kural: crawler_core da 25 dilli katmanı kullanır

The 25-language translation and keyword layer is **not** parse-only.

25 dilli translation ve keyword katmanı **yalnızca parse katmanına ait değildir**.

`crawler_core` must also use that layer.

`crawler_core` da bu katmanı kullanmak zorundadır.

This is a hard design rule from this repository point onward.

Bu, bu repository noktasından itibaren sert bir tasarım kuralıdır.

## Why crawler_core must use the taxonomy layer
## crawler_core neden taxonomy katmanını kullanmak zorundadır

Crawler behavior must not be blind.

Crawler davranışı kör olmamalıdır.

A serious logistics crawler must use multilingual taxonomy signals early, before full final classification.

Ciddi bir lojistik crawler, nihai sınıflandırmadan önce çok dilli taxonomy sinyallerini erken aşamada kullanmalıdır.

That early usage exists to improve:

- link selection
- frontier scoring
- crawl depth decisions
- revisit priority
- static-vs-browser acquisition choice
- early rejection of clearly irrelevant paths
- early strengthening of high-value logistics surfaces

Bu erken kullanım şu alanları iyileştirmek içindir:

- link seçimi
- frontier skorlaması
- crawl derinliği kararları
- revisit önceliği
- static-vs-browser acquisition seçimi
- açıkça alakasız yolların erken zayıflatılması
- yüksek değerli lojistik yüzeylerin erken güçlendirilmesi

## crawler_core taxonomy usage scope
## crawler_core taxonomy kullanım kapsamı

`crawler_core` must use multilingual taxonomy lookup against signals such as:

- hostname
- subdomain
- URL path segments
- query-string fragments
- anchor text
- nearby link context
- menu/navigation labels
- title
- h1
- short visible text
- HTML `lang`
- browser-rendered DOM text when needed

`crawler_core`, aşağıdaki sinyaller üzerinde çok dilli taxonomy lookup kullanmalıdır:

- hostname
- subdomain
- URL path segmentleri
- query-string parçaları
- anchor text
- link çevresi bağlamı
- menü/navigasyon etiketleri
- title
- h1
- kısa görünür metin
- HTML `lang`
- gerektiğinde browser-render sonrası DOM metni

This usage is for **crawl intelligence**, not final classification truth.

Bu kullanım **crawl intelligence** içindir; nihai sınıflandırma doğrusu için değildir.

## parse_core taxonomy usage scope
## parse_core taxonomy kullanım kapsamı

`parse_core` uses the same multilingual taxonomy foundation more deeply.

`parse_core`, aynı çok dilli taxonomy temelini daha derin kullanır.

Its responsibility includes:

- candidate extraction
- negative keyword suppression
- ancestor rollup through closure
- preranking snapshot production
- workflow state progression
- later packaging/export readiness

Sorumlulukları şunları içerir:

- candidate extraction
- negative keyword baskılama
- closure üzerinden ata düğüm rollup’ı
- preranking snapshot üretimi
- workflow state ilerletme
- sonraki paketleme/export hazırlığı

## Practical split in one sentence
## Tek cümlede pratik ayrım

- `crawler_core` = taxonomy-assisted exploration
- `parse_core` = taxonomy-backed classification and preranking

- `crawler_core` = taxonomy destekli keşif
- `parse_core` = taxonomy destekli sınıflandırma ve preranking

## Runtime alignment rule
## Runtime hizalama kuralı

Pi51 runtime taxonomy should converge toward the authority structure.

Pi51 runtime taxonomy, authority yapısına doğru yakınsamalıdır.

At minimum, Pi51 runtime must expose a normalized queryable taxonomy surface compatible with multilingual lookup.

En azından Pi51 runtime, çok dilli lookup ile uyumlu, normalize ve sorgulanabilir bir taxonomy yüzeyi göstermelidir.

The current raw staging-only state is not sufficient as the final runtime state.

Mevcut yalnızca ham staging durumu, nihai runtime durumu için yeterli değildir.

## Current proven facts
## Güncel kanıtlanmış gerçekler

At the current known point:

- Ubuntu Desktop authority has 25-language normalized taxonomy tables, indexes, constraints, and closure truth.
- Pi51 currently has raw staging tables for taxonomy input.
- Pi51 crawler runtime already proved a narrow host-scoped durable run on `https://example.com/`.
- The upstream truth for `https://example.com/robots.txt` is a 404 that returns HTML identical to the example page body.
- Canonical worker CLI package import repair has been committed and pushed.

Bilinen güncel noktada:

- Ubuntu Desktop authority tarafında 25 dilli, normalize taxonomy tabloları, index’ler, constraint’ler ve closure doğrusu vardır.
- Pi51 tarafında taxonomy girdisi için şu anda ham staging tabloları vardır.
- Pi51 crawler runtime, `https://example.com/` üzerinde dar ama gerçek bir host-scoped durable run kanıtlamıştır.
- `https://example.com/robots.txt` için upstream doğrusu, example page body’si ile aynı HTML döndüren bir 404’tür.
- Kanonik worker CLI package import düzeltmesi commit edilip pushlanmıştır.

## Immediate implementation order
## Acil uygulama sırası

1. Freeze this contract in the repository.
2. Build a normalized runtime taxonomy surface on Pi51 from staging data.
3. Add crawler_core multilingual taxonomy lookup helpers.
4. Apply taxonomy-assisted frontier/discovery scoring in crawler_core.
5. Seal crawler_core only after dynamic/browser discovery and cross-page traversal are also proven.
6. Then move to parse_core.

1. Bu sözleşmeyi repository içinde dondur.
2. Pi51 üzerinde staging verisinden normalize runtime taxonomy yüzeyi kur.
3. crawler_core için çok dilli taxonomy lookup yardımcılarını ekle.
4. crawler_core içinde taxonomy destekli frontier/discovery skorlamasını uygula.
5. dynamic/browser discovery ve sayfalar arası traversal da kanıtlanmadan crawler_core’u mühürleme.
6. Sonra parse_core’a geç.

## Non-goal
## Amaç dışı konu

This document does not claim that crawler_core already satisfies the full public-content reading target.

Bu belge, crawler_core’un tüm public içerik okuma hedefini şimdiden sağladığını iddia etmez.

That closure requires:

- static public fetch
- browser-backed public fetch
- cross-page traversal
- multilingual taxonomy-assisted crawl intelligence
- sealed runtime truth

Bu kapanış için şunlar gerekir:

- statik public fetch
- browser-backed public fetch
- sayfalar arası traversal
- çok dilli taxonomy destekli crawl intelligence
- mühürlü runtime doğrusu
