# Crawler Core 25 Language Source Research Standard

# Crawler Core 25 Dil Source Araştırma Standardı

## English

### Purpose

This document defines the controlled source research standard for all 25 LogisticSearch crawler_core languages. It is a documentation-only planning surface. It does not create new catalog files, it does not add new source families, it does not insert seeds into PostgreSQL or JSONB runtime storage, and it does not touch pi51c while the R96 24-hour crawler_core test may still be active.

The current English catalog is the metadata-harmonized reference template:

- English catalog: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- English catalog SHA256: `9053c367e96ac737b38b3da4db381431422f8e4b00c45c24f9c33c152eb16e5b`
- English template counts: 27 source families, 43 seed surfaces, 43 seed URLs.
- Required family, surface, and seed metadata presence is sealed as complete.

### Strict boundary

- no live frontier insert
- no DB insert/update/delete
- no crawler run
- no pi51c sync while R96 24h test is active
- no runtime scheduler patch
- no blind domain expansion
- no scraping before robots/live review
- no equal quota forcing across languages
- no source_seed directory creation unless contract changes

### Variable-capacity language plan

Equal quotas are forbidden. Each language uses a variable-capacity research model based on available high-quality logistics sources. English can be expanded aggressively, while smaller language markets may have fewer but higher-trust source families.

| Lang | Language | Capacity class | Initial research candidates | Minimum pre-manifest candidates | Target manifest families after review | Planned catalog path |
|---|---|---:|---:|---:|---:|---|
| `en` | English | `high_capacity_global` | 40-60 | 30 | 20-40 | `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json` |
| `tr` | Turkish | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json` |
| `de` | German | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json` |
| `ar` | Arabic | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json` |
| `zh` | Chinese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json` |
| `es` | Spanish | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json` |
| `fr` | French | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json` |
| `it` | Italian | `regional_medium_high` | 16-30 | 12 | 10-22 | `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json` |
| `pt` | Portuguese | `multi_region_medium_high` | 18-34 | 14 | 10-24 | `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json` |
| `nl` | Dutch | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json` |
| `ru` | Russian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json` |
| `uk` | Ukrainian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json` |
| `bg` | Bulgarian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json` |
| `cs` | Czech | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json` |
| `hu` | Hungarian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json` |
| `ro` | Romanian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json` |
| `el` | Greek | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json` |
| `he` | Hebrew | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json` |
| `ja` | Japanese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json` |
| `ko` | Korean | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json` |
| `hi` | Hindi | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json` |
| `bn` | Bengali | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json` |
| `ur` | Urdu | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json` |
| `id` | Indonesian | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json` |
| `vi` | Vietnamese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json` |

Total minimum pre-manifest candidates across all 25 languages: **332**.

### Source category standard

| Category slug | Trust tier | Description |
|---|---:|---|
| `official_association_directory` | Tier A | Freight forwarder/logistics/customs/transport association member directory. |
| `public_registry_or_chamber` | Tier A | Official chamber, government registry, customs broker registry or business registry. |
| `port_authority_or_port_directory` | Tier A | Port authority, terminal/operator directory, port community logistics directory. |
| `airport_cargo_authority_or_directory` | Tier A | Airport cargo authority, cargo terminal, airport freight/cargo directory. |
| `customs_broker_directory` | Tier A | Licensed customs broker or customs intermediary directory. |
| `trade_fair_exhibitor_directory` | Tier B+ | Logistics, transport, supply chain fair exhibitor directory. |
| `rail_freight_directory` | Tier B+ | Rail freight, intermodal or rail logistics directory. |
| `sea_freight_directory` | Tier B+ | Shipping, maritime freight, NVOCC, ocean freight directory. |
| `road_freight_directory` | Tier B+ | Road haulage, trucking, transport company directory. |
| `air_cargo_directory` | Tier B+ | Air cargo agent, GSA/GSSA, cargo airline or air freight directory. |
| `warehousing_directory` | Tier B | Warehouse, fulfillment, distribution center directory. |
| `cold_chain_directory` | Tier B | Cold chain, pharma logistics, reefer logistics directory. |
| `dangerous_goods_logistics_directory` | Tier B | Dangerous goods, hazmat logistics, ADR/IMDG/IATA-DGR related directory. |
| `courier_express_parcel_directory` | Tier B | Courier, express, parcel, last-mile logistics directory. |
| `third_party_logistics_3pl_directory` | Tier B | 3PL provider directory. |
| `fourth_party_logistics_4pl_directory` | Tier B | 4PL/lead logistics provider directory. |
| `project_cargo_directory` | Tier B | Project cargo, heavy lift, breakbulk logistics directory. |
| `commercial_logistics_directory` | Tier B- | Commercial directory with logistics category pages. |
| `network_directory` | Tier B- | Private freight/logistics network member directory. |
| `discovery_only_surface` | Tier C | Search/discovery surface that may reveal useful logistics entities but must not dominate. |

### Required JSON field standard

Family records must contain:

- `source_family_code`
- `source_family_name`
- `source_status`
- `source_root_url`
- `source_category`
- `source_host`
- `source_country_scope`
- `source_language`
- `source_selection_reason`
- `allowed_schemes`
- `default_priority`
- `default_recrawl_interval`
- `default_max_depth`
- `source_quality_tier`
- `family_metadata`
- `seed_surfaces`

Family metadata must contain:

- `family_metadata.lang_code`
- `family_metadata.quality_model_version`
- `family_metadata.trust_tier`
- `family_metadata.discovery_value`
- `family_metadata.noise_risk`
- `family_metadata.manual_review_priority`
- `family_metadata.host_budget_group`
- `family_metadata.cross_seed_traversal_allowed`
- `family_metadata.cross_language_traversal_allowed`
- `family_metadata.runtime_activation_policy`
- `family_metadata.human_review_required_before_frontier`
- `family_metadata.live_check_required`
- `family_metadata.family_review_state`

Surface metadata must contain:

- `surface_metadata.surface_scope`
- `surface_metadata.runtime_activation_policy`
- `surface_metadata.human_review_required_before_frontier`
- `surface_metadata.live_check_required`
- `surface_metadata.quality_model_version`

Seed metadata must contain:

- `seed_metadata.lang_code`
- `seed_metadata.review_state`
- `seed_metadata.runtime_activation_policy`
- `seed_metadata.human_review_required_before_frontier`
- `seed_metadata.live_check_required`
- `seed_metadata.quality_model_version`

### Research gates before any manifest patch

- `candidate_url_format_audit`
- `candidate_domain_duplicate_audit`
- `language_relevance_audit`
- `logistics_relevance_audit`
- `authority_trust_tier_audit`
- `robots_politeness_risk_note`
- `category_coverage_audit`
- `country_region_diversity_audit`
- `single_domain_dominance_audit`
- `scheduler_diversity_signal_audit`
- `manual_review_before_frontier_assertion`
- `github_tracked_manifest_audit`

### Runtime boundary

Source research and source/seed selection are not filtering decisions for crawler_core. crawler_core remains a raw evidence collector. Content evaluation, entity extraction, logistics relevance scoring, taxonomy mapping, ranking, and downstream quality scoring belong to parse_core and desktop_import. Future persistence must preserve the project-wide PostgreSQL + JSONB model, but this document performs no DB mutation.

### Scheduler diversity design support

The research standard must support future domain-aware scheduler design without changing runtime now. Candidate manifests must carry enough language, source family, host budget group, cross-seed, cross-language, trust tier, noise risk, live-check, and manual-review metadata to allow future fair rotation across language/source/domain pools.

## Türkçe

### Amaç

Bu doküman LogisticSearch crawler_core için 25 dilde kontrollü source araştırma standardını tanımlar. Bu yalnızca dokümantasyon planlama yüzeyidir. Yeni katalog dosyası oluşturmaz, yeni source family eklemez, PostgreSQL veya JSONB runtime storage içine seed yazmaz ve R96 24 saatlik crawler_core testi hâlâ aktif olabilirken pi51c'ye dokunmaz.

Mevcut İngilizce katalog metadata-harmonized referans şablondur:

- İngilizce katalog: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- İngilizce katalog SHA256: `9053c367e96ac737b38b3da4db381431422f8e4b00c45c24f9c33c152eb16e5b`
- İngilizce şablon sayıları: 27 source family, 43 seed surface, 43 seed URL.
- Zorunlu family, surface ve seed metadata varlığı eksiksiz olarak mühürlenmiştir.

### Sert sınır

- no live frontier insert
- no DB insert/update/delete
- no crawler run
- no pi51c sync while R96 24h test is active
- no runtime scheduler patch
- no blind domain expansion
- no scraping before robots/live review
- no equal quota forcing across languages
- no source_seed directory creation unless contract changes

### Değişken kapasiteli dil planı

Eşit kota yasaktır. Her dil, ulaşılabilir yüksek kaliteli lojistik kaynak sayısına göre değişken kapasiteli araştırma modeli kullanır. İngilizce agresif genişletilebilir; daha küçük dil pazarlarında daha az ama daha güvenilir source family kabul edilir.

| Dil | Language | Kapasite sınıfı | İlk araştırma adayı | Minimum pre-manifest aday | Review sonrası hedef manifest family | Planlanan katalog yolu |
|---|---|---:|---:|---:|---:|---|
| `en` | English | `high_capacity_global` | 40-60 | 30 | 20-40 | `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json` |
| `tr` | Turkish | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json` |
| `de` | German | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json` |
| `ar` | Arabic | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json` |
| `zh` | Chinese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json` |
| `es` | Spanish | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json` |
| `fr` | French | `multi_region_high` | 25-45 | 20 | 15-30 | `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json` |
| `it` | Italian | `regional_medium_high` | 16-30 | 12 | 10-22 | `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json` |
| `pt` | Portuguese | `multi_region_medium_high` | 18-34 | 14 | 10-24 | `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json` |
| `nl` | Dutch | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json` |
| `ru` | Russian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json` |
| `uk` | Ukrainian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json` |
| `bg` | Bulgarian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json` |
| `cs` | Czech | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json` |
| `hu` | Hungarian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json` |
| `ro` | Romanian | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json` |
| `el` | Greek | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json` |
| `he` | Hebrew | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json` |
| `ja` | Japanese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json` |
| `ko` | Korean | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json` |
| `hi` | Hindi | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json` |
| `bn` | Bengali | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json` |
| `ur` | Urdu | `regional_medium` | 10-24 | 8 | 6-18 | `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json` |
| `id` | Indonesian | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json` |
| `vi` | Vietnamese | `regional_high` | 20-35 | 16 | 12-25 | `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json` |

25 dil toplam minimum pre-manifest aday sayısı: **332**.

### Source kategori standardı

| Kategori slug | Güven katmanı | Açıklama |
|---|---:|---|
| `official_association_directory` | Tier A | Freight forwarder/logistics/customs/transport association member directory. |
| `public_registry_or_chamber` | Tier A | Official chamber, government registry, customs broker registry or business registry. |
| `port_authority_or_port_directory` | Tier A | Port authority, terminal/operator directory, port community logistics directory. |
| `airport_cargo_authority_or_directory` | Tier A | Airport cargo authority, cargo terminal, airport freight/cargo directory. |
| `customs_broker_directory` | Tier A | Licensed customs broker or customs intermediary directory. |
| `trade_fair_exhibitor_directory` | Tier B+ | Logistics, transport, supply chain fair exhibitor directory. |
| `rail_freight_directory` | Tier B+ | Rail freight, intermodal or rail logistics directory. |
| `sea_freight_directory` | Tier B+ | Shipping, maritime freight, NVOCC, ocean freight directory. |
| `road_freight_directory` | Tier B+ | Road haulage, trucking, transport company directory. |
| `air_cargo_directory` | Tier B+ | Air cargo agent, GSA/GSSA, cargo airline or air freight directory. |
| `warehousing_directory` | Tier B | Warehouse, fulfillment, distribution center directory. |
| `cold_chain_directory` | Tier B | Cold chain, pharma logistics, reefer logistics directory. |
| `dangerous_goods_logistics_directory` | Tier B | Dangerous goods, hazmat logistics, ADR/IMDG/IATA-DGR related directory. |
| `courier_express_parcel_directory` | Tier B | Courier, express, parcel, last-mile logistics directory. |
| `third_party_logistics_3pl_directory` | Tier B | 3PL provider directory. |
| `fourth_party_logistics_4pl_directory` | Tier B | 4PL/lead logistics provider directory. |
| `project_cargo_directory` | Tier B | Project cargo, heavy lift, breakbulk logistics directory. |
| `commercial_logistics_directory` | Tier B- | Commercial directory with logistics category pages. |
| `network_directory` | Tier B- | Private freight/logistics network member directory. |
| `discovery_only_surface` | Tier C | Search/discovery surface that may reveal useful logistics entities but must not dominate. |

### Zorunlu JSON alan standardı

Family kayıtları şunları içermelidir:

- `source_family_code`
- `source_family_name`
- `source_status`
- `source_root_url`
- `source_category`
- `source_host`
- `source_country_scope`
- `source_language`
- `source_selection_reason`
- `allowed_schemes`
- `default_priority`
- `default_recrawl_interval`
- `default_max_depth`
- `source_quality_tier`
- `family_metadata`
- `seed_surfaces`

Family metadata şunları içermelidir:

- `family_metadata.lang_code`
- `family_metadata.quality_model_version`
- `family_metadata.trust_tier`
- `family_metadata.discovery_value`
- `family_metadata.noise_risk`
- `family_metadata.manual_review_priority`
- `family_metadata.host_budget_group`
- `family_metadata.cross_seed_traversal_allowed`
- `family_metadata.cross_language_traversal_allowed`
- `family_metadata.runtime_activation_policy`
- `family_metadata.human_review_required_before_frontier`
- `family_metadata.live_check_required`
- `family_metadata.family_review_state`

Surface metadata şunları içermelidir:

- `surface_metadata.surface_scope`
- `surface_metadata.runtime_activation_policy`
- `surface_metadata.human_review_required_before_frontier`
- `surface_metadata.live_check_required`
- `surface_metadata.quality_model_version`

Seed metadata şunları içermelidir:

- `seed_metadata.lang_code`
- `seed_metadata.review_state`
- `seed_metadata.runtime_activation_policy`
- `seed_metadata.human_review_required_before_frontier`
- `seed_metadata.live_check_required`
- `seed_metadata.quality_model_version`

### Manifest patch öncesi araştırma gate'leri

- `candidate_url_format_audit`
- `candidate_domain_duplicate_audit`
- `language_relevance_audit`
- `logistics_relevance_audit`
- `authority_trust_tier_audit`
- `robots_politeness_risk_note`
- `category_coverage_audit`
- `country_region_diversity_audit`
- `single_domain_dominance_audit`
- `scheduler_diversity_signal_audit`
- `manual_review_before_frontier_assertion`
- `github_tracked_manifest_audit`

### Runtime sınırı

Source araştırması ve source/seed seçimi crawler_core için filtreleme kararı değildir. crawler_core ham kanıt toplayıcı olarak kalır. İçerik değerlendirme, entity extraction, lojistik uygunluk puanı, taxonomy mapping, ranking ve downstream kalite puanı parse_core ve desktop_import alanına aittir. İleride kalıcılık gerekiyorsa PostgreSQL + JSONB modeli korunacaktır; bu doküman DB mutation yapmaz.

### Scheduler çeşitlilik tasarım desteği

Bu araştırma standardı runtime'ı şimdi değiştirmeden gelecekteki domain-aware scheduler tasarımını desteklemelidir. Aday manifestler ileride language/source/domain havuzları arasında adil rotasyon sağlayabilmek için language, source family, host budget group, cross-seed, cross-language, trust tier, noise risk, live-check ve manual-review metadata taşımalıdır.
