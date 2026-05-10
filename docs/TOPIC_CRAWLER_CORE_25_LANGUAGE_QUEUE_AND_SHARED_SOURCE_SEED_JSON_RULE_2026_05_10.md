# Crawler Core 25 Language Queue and Shared Source/Seed JSON Rule

# Crawler Core 25 Dil Queue ve Ortak Source/Seed JSON Kuralı

## English

### Purpose

This document seals the source/seed queue and shared JSON catalog rule for crawler_core. It is a documentation-only rule. It does not patch runtime scheduler code, it does not create catalog JSON files, it does not touch PostgreSQL, it does not touch pi51c, and it does not start crawler_core.

### Canonical rule

- The 25-language source/seed program must use the same standard and format for every language.
- Improvements discovered while working on one language, such as `source_category` arrays and `seed_surfaces` arrays, must be applied back to English/default and then reused for all 25 languages.
- crawler_core must be planned as 25 language-aware queue streams, one logical queue per language.
- The durable source/seed catalog should be represented as a shared JSON structure with explicit `lang_code` fields instead of unrelated one-off formats.
- English/default may contain global/default source families, but language-specific catalogs must not blindly copy the same global source family as if it belonged to each language.
- A source family owns many seed surfaces. `source_category` and `seed_surfaces` must be arrays.
- `seed_urls` must be derived later from reviewed seed surfaces, not guessed blindly.

### Required shared JSON shape

Each source family record should follow this shape before any live use:

```json
{
  "lang_code": "tr",
  "source_family_code": "example_source_family",
  "source_language_scope": ["tr"],
  "source_country_scope": ["TR"],
  "source_quality_tier": "A",
  "source_category": ["official_association_directory"],
  "decision_status": "ACCEPT",
  "runtime_activation_policy": "pi51c_live_probe_required_before_db_or_frontier_insert",
  "human_review_required_before_frontier": true,
  "live_check_required": true,
  "robots_review_required": true,
  "seed_surfaces": [
    {
      "seed_surface_code": "member_directory",
      "seed_surface_category": ["official_association_directory"],
      "seed_surface_type": "directory",
      "seed_decision_status": "ACCEPT",
      "seed_urls": []
    }
  ]
}
```

### Queue model

- crawler_core should plan one logical queue per language: 25 language queues total.
- The scheduler should read the 25 language queues in a fair rotation.
- If the next eligible work item belongs to the same domain/source host as the previous request, the same-host politeness delay remains 5 seconds unless a stricter robots/live policy requires more.
- If another language/source/domain is eligible and not inside its host cooldown, crawler_core may rotate to that different source without waiting for the previous host's cooldown.
- The rule is domain-aware politeness, not a blind global sleep.
- Same-host pressure must be avoided; different-host diversity should increase throughput safely.

### Source and seed standard

- `source_category` must be an array.
- `seed_surfaces` must be an array.
- `seed_urls` must be an array inside each reviewed seed surface.
- A large company/operator can be a source, but it must be classified as operator/entity/reference if it does not discover multiple external entities.
- Public authority, chamber, association, port, airport, customs, rail, road, courier, cold-chain, warehousing, trade-fair, and commercial directory categories must remain distinguishable.
- Commercial directories can be accepted as `B`, `B_PLUS`, or `B_MINUS`, but they must not be promoted to `A` without official authority evidence.

### Quality model

- `A_PLUS`: canonical public registry, government system, global/default authority, or strongest official source.
- `A`: strong official association, chamber, authority, or institutional source.
- `A_MINUS`: official/institutional but narrower, regional, operator, or context-heavy source.
- `B_PLUS`: useful sector directory, trade fair, newer association, or serious commercial discovery source.
- `B`: commercial or medium-trust source; useful but live proof and manual review are mandatory.
- `B_MINUS`: high-noise or weak discovery source; hold or low-priority only.

### Language list

| Order | lang_code | Language |
|---:|---|---|
| 1 | `en` | English |
| 2 | `tr` | Turkish |
| 3 | `de` | German |
| 4 | `ar` | Arabic |
| 5 | `zh` | Chinese |
| 6 | `es` | Spanish |
| 7 | `fr` | French |
| 8 | `it` | Italian |
| 9 | `pt` | Portuguese |
| 10 | `nl` | Dutch |
| 11 | `ru` | Russian |
| 12 | `uk` | Ukrainian |
| 13 | `bg` | Bulgarian |
| 14 | `cs` | Czech |
| 15 | `hu` | Hungarian |
| 16 | `ro` | Romanian |
| 17 | `el` | Greek |
| 18 | `he` | Hebrew |
| 19 | `ja` | Japanese |
| 20 | `ko` | Korean |
| 21 | `hi` | Hindi |
| 22 | `bn` | Bengali |
| 23 | `ur` | Urdu |
| 24 | `id` | Indonesian |
| 25 | `vi` | Vietnamese |

### Runtime boundary

This document does not implement scheduler runtime behavior. Runtime implementation must be a later explicitly gated patch. Until that separate gate exists, no systemd, no DB mutation, no crawler start, no pi51c sync, and no live frontier insert is allowed from this document.

## Türkçe

### Amaç

Bu doküman crawler_core için 25 dil queue ve ortak source/seed JSON catalog kuralını mühürler. Bu yalnızca dokümantasyon kuralıdır. Runtime scheduler kodu patch etmez, katalog JSON dosyası oluşturmaz, PostgreSQL'e dokunmaz, pi51c'ye dokunmaz ve crawler_core başlatmaz.

### Kanonik kural

- 25 dil source/seed programı her dil için aynı standart ve formatı kullanmalıdır.
- Bir dil üzerinde çalışırken bulunan iyileştirmeler, örneğin `source_category` array ve `seed_surfaces` array, English/default tarafına da geri uygulanmalı ve sonra 25 dilin tamamında kullanılmalıdır.
- crawler_core, 25 language-aware queue stream olarak planlanmalıdır: her dil için bir mantıksal queue.
- Kalıcı source/seed catalog, ayrı ayrı kopuk formatlar yerine açık `lang_code` alanı taşıyan ortak JSON yapısı ile temsil edilmelidir.
- English/default global/default source family taşıyabilir; fakat dil catalog'ları aynı global source family'yi kör şekilde kendi source'u gibi kopyalamamalıdır.
- Bir source family çok sayıda seed surface sahibi olabilir. `source_category` ve `seed_surfaces` array olmalıdır.
- `seed_urls` daha sonra reviewed seed surface üzerinden çıkarılmalıdır; kör tahmin yapılmamalıdır.

### Zorunlu ortak JSON şekli

Her source family kaydı canlı kullanımdan önce şu şekle yaklaşmalıdır:

```json
{
  "lang_code": "tr",
  "source_family_code": "example_source_family",
  "source_language_scope": ["tr"],
  "source_country_scope": ["TR"],
  "source_quality_tier": "A",
  "source_category": ["official_association_directory"],
  "decision_status": "ACCEPT",
  "runtime_activation_policy": "pi51c_live_probe_required_before_db_or_frontier_insert",
  "human_review_required_before_frontier": true,
  "live_check_required": true,
  "robots_review_required": true,
  "seed_surfaces": [
    {
      "seed_surface_code": "member_directory",
      "seed_surface_category": ["official_association_directory"],
      "seed_surface_type": "directory",
      "seed_decision_status": "ACCEPT",
      "seed_urls": []
    }
  ]
}
```

### Queue modeli

- crawler_core her dil için bir mantıksal queue planlamalıdır: toplam 25 language queue.
- Scheduler 25 language queue'yu adil rotasyonla okumalıdır.
- Sıradaki uygun iş önceki istekle aynı domain/source host üzerindeyse aynı-host politeness beklemesi 5 saniye kalır; robots/live policy daha sıkıysa daha uzun beklenir.
- Başka bir dil/source/domain uygunsa ve kendi host cooldown içinde değilse crawler_core önceki host cooldown'ını beklemeden o farklı source'a dönebilir.
- Kural kör global sleep değil, domain-aware politeness olmalıdır.
- Aynı-host baskısı önlenmeli; farklı-host çeşitliliği güvenli şekilde throughput artırmalıdır.

### Source ve seed standardı

- `source_category` array olmalıdır.
- `seed_surfaces` array olmalıdır.
- `seed_urls` her reviewed seed surface içinde array olmalıdır.
- Büyük bir şirket/operator source olabilir; fakat çoklu dış entity keşfetmiyorsa operator/entity/reference olarak sınıflandırılmalıdır.
- Kamu otoritesi, oda, dernek, liman, havalimanı, gümrük, demiryolu, karayolu, kargo/kurye, soğuk zincir, depolama, fuar ve ticari directory kategorileri ayrı tutulmalıdır.
- Ticari directory'ler `B`, `B_PLUS` veya `B_MINUS` olabilir; resmi otorite kanıtı olmadan `A` seviyesine çıkarılmamalıdır.

### Kalite modeli

- `A_PLUS`: kanonik kamu registry, devlet sistemi, global/default otorite veya en güçlü resmi kaynak.
- `A`: güçlü resmi dernek, oda, otorite veya kurumsal kaynak.
- `A_MINUS`: resmi/kurumsal fakat daha dar, bölgesel, operator veya context ağırlıklı kaynak.
- `B_PLUS`: yararlı sektör directory, fuar, yeni dernek veya ciddi ticari discovery kaynağı.
- `B`: ticari veya orta güven source; yararlı ama live proof ve manual review zorunlu.
- `B_MINUS`: noise riski yüksek veya zayıf discovery source; hold veya düşük öncelik.

### Dil listesi

| Sıra | lang_code | Dil |
|---:|---|---|
| 1 | `en` | English |
| 2 | `tr` | Turkish |
| 3 | `de` | German |
| 4 | `ar` | Arabic |
| 5 | `zh` | Chinese |
| 6 | `es` | Spanish |
| 7 | `fr` | French |
| 8 | `it` | Italian |
| 9 | `pt` | Portuguese |
| 10 | `nl` | Dutch |
| 11 | `ru` | Russian |
| 12 | `uk` | Ukrainian |
| 13 | `bg` | Bulgarian |
| 14 | `cs` | Czech |
| 15 | `hu` | Hungarian |
| 16 | `ro` | Romanian |
| 17 | `el` | Greek |
| 18 | `he` | Hebrew |
| 19 | `ja` | Japanese |
| 20 | `ko` | Korean |
| 21 | `hi` | Hindi |
| 22 | `bn` | Bengali |
| 23 | `ur` | Urdu |
| 24 | `id` | Indonesian |
| 25 | `vi` | Vietnamese |

### Runtime sınırı

Bu doküman scheduler runtime davranışını uygulamaz. Runtime uygulaması daha sonra ayrı ve açık gate ile yapılmalıdır. O ayrı gate gelene kadar bu dokümandan dolayı systemd yok, DB mutation yok, crawler start yok, pi51c sync yok ve live frontier insert yoktur.
