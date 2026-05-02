# Source Seed PostgreSQL JSONB + Geo Runtime Contract

## English

### Purpose

This document records the canonical LogisticSearch decision for storing and later operating `source_seed_` records.

The decision is strict:

- PostgreSQL is the durable/runtime store.
- Source and seed details are stored as JSONB metadata.
- Canonical catalog authoring remains repo JSON.
- One approved source seed must never become an uncontrolled crawl.
- Pi51c, runtime, systemd, and live frontier surfaces stay forbidden until separate controlled approval.

This document was created after the NCBFAA single-seed R4B read-only proof.

### Current sealed NCBFAA source_seed

| Field | Value |
|---|---|
| source_seed_code | `source_seed_en_ncbfaa_org_membership_search_001` |
| source_family_code | `ncbfaa_org` |
| source_family_name | `NCBFAA` |
| source_host | `www.ncbfaa.org` |
| lang_code | `en` |
| trust_tier | `A_MINUS` |
| seed_url | `https://www.ncbfaa.org/search-our-membership` |
| canonical_url_sha256 | `f0b372af72c1668db70da294d62ff1aebfc01ab174cb727f7f75493e44cfe203` |
| scope | exactly one source, exactly one seed |

### PostgreSQL storage decision

The durable runtime target is PostgreSQL.

The selected read-only scratch reference in R4B was:

`logisticsearch_crawler_split_scratch`

The target table candidate is:

`seed.seed_url`

The important columns observed in R4B are:

| Column | Type | Meaning |
|---|---|---|
| `source_id` | `uuid NOT NULL` | Foreign key to `seed.source`; must be resolved before any insert. |
| `seed_type` | `seed.seed_type_enum` | Current default is `entrypoint`. |
| `submitted_url` | `text NOT NULL` | Human/catalog submitted seed URL. |
| `canonical_url` | `text NOT NULL` | Canonicalized URL. |
| `canonical_url_sha256` | `text` | SHA256 hex string; do not use `decode(..., 'hex')` for this schema. |
| `priority` | `integer NOT NULL` | Scheduling priority. |
| `max_depth` | `integer NOT NULL` | Crawl depth guard. |
| `recrawl_interval` | `interval NOT NULL` | Recrawl/discovery interval. |
| `seed_metadata` | `jsonb NOT NULL` | Source/seed metadata payload. |

### JSONB metadata decision

The `seed.seed_url.seed_metadata` JSONB payload is the place for structured source/seed information.

The JSONB payload should include:

- `source_seed_code`
- source family identity
- host and language
- trust tier
- surface identity
- canonical URL
- URL SHA256
- runtime policy
- future geo/map contract metadata

This keeps runtime PostgreSQL strict while keeping management and future API output JSON-friendly.

### Source ID decision

R4B intentionally did not insert anything.

The blocker is:

`UNRESOLVED_SOURCE_ID_NEEDS_R5_DECISION`

Before any scratch insert, R5 must decide one of these strategies:

1. reuse an existing valid `seed.source` row,
2. create exactly one scratch-only `seed.source` row,
3. or define a controlled source identity migration path.

No `seed.seed_url` insert is allowed until `source_id` is resolved.

### Geo / OSM / map runtime decision

The future company and branch map architecture is:

`PostgreSQL/PostGIS -> API -> GeoJSON -> MapLibre GL JS`

The future live tracking architecture is:

`Socket.IO + MapLibre GL JS`

The future technical analysis map architecture is:

`API/GeoJSON + OpenLayers`

The rule is:

- PostgreSQL stores durable structured data.
- PostGIS stores spatial data when coordinates/geometry are verified.
- API serves GeoJSON for map clients.
- MapLibre GL JS handles normal company/branch map rendering and live map rendering.
- Socket.IO handles live vehicle or fleet position updates.
- OpenLayers may be used for technical analysis screens.
- No coordinates may be invented.
- No geocoding result becomes trusted without evidence.

### NCBFAA R4B schema fixes

R4B fixed two important read-only planning details:

1. PostgreSQL `pg_constraint.contype` must be cast as `con.contype::text` before text concatenation.
2. `seed.seed_url.canonical_url_sha256` is `text`, so the SQL preview must store the SHA256 hex string directly.

### SQL execution rule

The R4B SQL preview is not executable by default.

Any SQL preview must contain:

- `DO_NOT_EXECUTE` naming,
- explicit transaction wrapper,
- explicit rollback,
- unresolved `source_id` placeholder until R5,
- no live DB target,
- no Pi51c target,
- no fetch/crawl side effect.

### Hard safety rules

- Do not bulk insert English sources.
- Do not insert NCBFAA into live DB.
- Do not touch Pi51c before Desktop scratch proof.
- Do not start worker.
- Do not write frontier rows from the planner.
- Do not fetch/crawl from a catalog patch step.
- Do not convert one source seed into uncontrolled discovery fanout.
- Do not bypass source_id strategy.
- Do not bypass robots/politeness proof.
- Do not bypass runbook discipline.

### Next step

Next canonical step:

`SOURCE_SEED_NCBFAA_CRAWLER_CORE_R5_SOURCE_ID_STRATEGY_READONLY`

R5 must stay read-only unless a separate explicit scratch-only mutation approval is given.

## Türkçe

### Amaç

Bu doküman, LogisticSearch içinde `source_seed_` kayıtlarının nasıl saklanacağı ve daha sonra nasıl çalıştırılacağı konusunda canonical kararı kaydeder.

Karar nettir:

- PostgreSQL durable/runtime saklama katmanıdır.
- Source ve seed detayları JSONB metadata olarak saklanır.
- Canonical catalog yazım yüzeyi repo JSON olarak kalır.
- Onaylanmış tek bir source seed asla kontrolsüz crawl’a dönüşmemelidir.
- Pi51c, runtime, systemd ve live frontier yüzeyleri ayrı kontrollü onay olmadan yasaktır.

Bu doküman, NCBFAA single-seed R4B read-only kanıtından sonra oluşturulmuştur.

### Mevcut mühürlü NCBFAA source_seed

| Alan | Değer |
|---|---|
| source_seed_code | `source_seed_en_ncbfaa_org_membership_search_001` |
| source_family_code | `ncbfaa_org` |
| source_family_name | `NCBFAA` |
| source_host | `www.ncbfaa.org` |
| lang_code | `en` |
| trust_tier | `A_MINUS` |
| seed_url | `https://www.ncbfaa.org/search-our-membership` |
| canonical_url_sha256 | `f0b372af72c1668db70da294d62ff1aebfc01ab174cb727f7f75493e44cfe203` |
| kapsam | tam olarak bir source, tam olarak bir seed |

### PostgreSQL saklama kararı

Durable runtime hedefi PostgreSQL’dir.

R4B sırasında read-only scratch referans olarak seçilen DB:

`logisticsearch_crawler_split_scratch`

Hedef tablo adayı:

`seed.seed_url`

R4B’de gözlenen önemli kolonlar:

| Kolon | Tip | Anlam |
|---|---|---|
| `source_id` | `uuid NOT NULL` | `seed.source` foreign key; insert öncesi çözülmelidir. |
| `seed_type` | `seed.seed_type_enum` | Mevcut default `entrypoint`. |
| `submitted_url` | `text NOT NULL` | İnsan/catalog tarafından verilen seed URL. |
| `canonical_url` | `text NOT NULL` | Canonical URL. |
| `canonical_url_sha256` | `text` | SHA256 hex string; bu schema için `decode(..., 'hex')` kullanılmaz. |
| `priority` | `integer NOT NULL` | Scheduling priority. |
| `max_depth` | `integer NOT NULL` | Crawl depth sınırı. |
| `recrawl_interval` | `interval NOT NULL` | Recrawl/discovery aralığı. |
| `seed_metadata` | `jsonb NOT NULL` | Source/seed metadata payload. |

### JSONB metadata kararı

`seed.seed_url.seed_metadata` JSONB payload structured source/seed bilgileri için kullanılacaktır.

JSONB payload şunları içermelidir:

- `source_seed_code`
- source family kimliği
- host ve dil
- trust tier
- surface kimliği
- canonical URL
- URL SHA256
- runtime policy
- gelecekteki geo/map contract metadata

Bu model PostgreSQL runtime tarafını sıkı tutarken yönetim ve gelecekteki API çıktısını JSON dostu tutar.

### Source ID kararı

R4B bilinçli olarak hiçbir insert yapmadı.

Bloker:

`UNRESOLVED_SOURCE_ID_NEEDS_R5_DECISION`

Herhangi bir scratch insert öncesinde R5 şu stratejilerden birini seçmelidir:

1. mevcut geçerli bir `seed.source` row kullanmak,
2. tam olarak bir scratch-only `seed.source` row oluşturmak,
3. veya kontrollü source identity migration yolu tanımlamak.

`source_id` çözülmeden `seed.seed_url` insert yasaktır.

### Geo / OSM / harita runtime kararı

Gelecekteki firma ve şube haritası mimarisi:

`PostgreSQL/PostGIS -> API -> GeoJSON -> MapLibre GL JS`

Gelecekteki canlı izleme mimarisi:

`Socket.IO + MapLibre GL JS`

Gelecekteki teknik analiz haritası mimarisi:

`API/GeoJSON + OpenLayers`

Kural:

- PostgreSQL durable structured data saklar.
- Koordinat/geometri doğrulanınca PostGIS spatial data saklar.
- API map client’lara GeoJSON sunar.
- MapLibre GL JS normal firma/şube haritaları ve canlı haritaları render eder.
- Socket.IO canlı araç veya filo konum güncellemelerini taşır.
- OpenLayers teknik analiz ekranlarında kullanılabilir.
- Koordinat uydurulamaz.
- Geocoding sonucu kanıtsız trusted kabul edilemez.

### NCBFAA R4B schema düzeltmeleri

R4B iki önemli read-only planlama detayını düzeltti:

1. PostgreSQL `pg_constraint.contype`, text concat öncesi `con.contype::text` olarak cast edilmelidir.
2. `seed.seed_url.canonical_url_sha256` tipi `text` olduğu için SQL preview SHA256 hex string’i doğrudan saklamalıdır.

### SQL çalıştırma kuralı

R4B SQL preview varsayılan olarak çalıştırılabilir değildir.

Her SQL preview şunları içermelidir:

- `DO_NOT_EXECUTE` isimlendirmesi,
- açık transaction wrapper,
- açık rollback,
- R5’e kadar unresolved `source_id` placeholder,
- live DB hedefi yok,
- Pi51c hedefi yok,
- fetch/crawl yan etkisi yok.

### Sert güvenlik kuralları

- English source bulk insert yapma.
- NCBFAA’yı live DB’ye insert etme.
- Desktop scratch proof olmadan Pi51c’ye dokunma.
- Worker başlatma.
- Planner’dan frontier row yazma.
- Catalog patch adımında fetch/crawl yapma.
- Tek source seed’i kontrolsüz discovery fanout’a çevirme.
- source_id stratejisini atlama.
- robots/politeness proof’u atlama.
- runbook disiplinini atlama.

### Sonraki adım

Sonraki canonical adım:

`SOURCE_SEED_NCBFAA_CRAWLER_CORE_R5_SOURCE_ID_STRATEGY_READONLY`

R5, ayrı açık scratch-only mutation onayı verilmedikçe read-only kalmalıdır.
