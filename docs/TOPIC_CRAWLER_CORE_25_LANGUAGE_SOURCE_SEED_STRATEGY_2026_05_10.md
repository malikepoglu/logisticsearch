# Crawler Core 25 Language Source/Seed Strategy
# Crawler Core 25 Dil Source/Seed Stratejisi

## English

### Purpose

This document defines the controlled source/startpoint strategy for crawler_core across all 25 LogisticSearch taxonomy languages.

The goal is to prepare high-quality language-specific source family and seed catalogs without touching the active pi51c crawler runtime while the 24-hour crawler_core test is running.

This document is a planning and governance surface only. It does not activate any seed, does not insert frontier rows, does not change scheduler behavior, does not connect to PostgreSQL, and does not sync anything to pi51c.

### Strict boundary

This work line is limited to Ubuntu Desktop and GitHub.

Forbidden in this line:

- no pi51c repo sync
- no pi51c live runtime copy
- no crawler start or stop
- no systemd start, stop, restart, enable, or disable
- no PostgreSQL mutation
- no frontier insert
- no scheduler runtime patch
- no raw body deletion
- no sidecar deletion
- no chmod, chown, mount, rm, rsync, or scp
- no secret, DSN, token, password, user-agent secret, or process command line printing

The running pi51c R96 24-hour test must remain untouched.

### Canonical topology decision

The existing repository already has a source/startpoint design surface:

- `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`

The repository does not currently have:

- `makpi51crawler/source_seed/`
- `makpi51crawler/source_seed/crawler_core/`
- `makpi51crawler/source_seed/crawler_core/languages/`

Therefore, the canonical decision for this work line is:

- extend the existing `makpi51crawler/catalog/startpoints/<lang>/` pattern
- do not introduce a new `makpi51crawler/source_seed/` tree unless a later explicit architecture decision changes the contract
- keep source/startpoint manifests tracked in GitHub first
- sync to pi51c only through a later separate explicit gate

English remains the existing exception because it already has:

- `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`

New language catalog target pattern:

- `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/de/german_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v1.json`
- and the same pattern for the remaining languages

### 25 language catalog plan

The full target language set is exactly 25 languages:

1. `en` English
2. `tr` Turkish
3. `de` German
4. `ar` Arabic
5. `zh` Chinese
6. `es` Spanish
7. `fr` French
8. `it` Italian
9. `pt` Portuguese
10. `nl` Dutch
11. `ru` Russian
12. `uk` Ukrainian
13. `bg` Bulgarian
14. `cs` Czech
15. `hu` Hungarian
16. `ro` Romanian
17. `el` Greek
18. `he` Hebrew
19. `ja` Japanese
20. `ko` Korean
21. `hi` Hindi
22. `bn` Bengali
23. `ur` Urdu
24. `id` Indonesian
25. `vi` Vietnamese

The first implementation target is all 25 languages as a complete design surface, not only 5 languages.

The practical construction order may still be staged to reduce risk:

1. audit English baseline
2. create strict 25-language manifest standard
3. create missing language directories and catalogs in controlled gates
4. validate JSON structure
5. validate URL format
6. validate duplicate domains and duplicate seed URLs
7. validate source type coverage
8. validate language relevance
9. validate logistics relevance
10. validate GitHub tracked manifest inventory
11. commit and push to GitHub
12. later, after R96 is complete and explicitly gated, sync to pi51c

### Source family quality model

A source family is the durable parent object for one trusted source.

A source family should represent a source such as:

- official logistics association
- freight forwarder association
- customs broker association
- chamber or business registry
- port authority
- airport cargo authority
- rail freight authority or directory
- road freight directory
- sea freight directory
- air cargo directory
- courier or parcel directory
- 3PL / 4PL directory
- project cargo network
- cold chain logistics source
- dangerous goods logistics source
- trade fair or exhibitor directory
- industry portal
- company directory

Each source family must preserve scheduler and safety signals.

Required source family fields:

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
- `family_metadata`
- `family_review_state`
- `host_budget_group`
- `cross_seed_traversal_allowed`
- `cross_language_traversal_allowed`
- `seed_surfaces`

Required family metadata signals:

- `trust_tier`
- `source_quality_tier`
- `discovery_value`
- `noise_risk`
- `quality_model_version`
- `runtime_activation_policy`
- `human_review_required_before_frontier`
- `live_check_required`

The English catalog is useful but must not be copied blindly. R3B found structural gaps in the existing English catalog, including missing `host_budget_group`, missing `family_review_state`, missing traversal flags, missing seed review states, duplicate surface code patterns, and host mismatch rows.

New catalogs must use the improved stricter model.

### Seed surface quality model

A seed surface is a crawlable or reviewable entry surface under a source family.

Required seed surface fields:

- `surface_code`
- `surface_type`
- `surface_name`
- `surface_scope`
- `surface_metadata`
- `seed_urls`

A seed surface may represent:

- member directory
- directory search page
- country directory
- regional directory
- category page
- association member search
- listing index
- trade fair exhibitor index
- public registry search page

The `surface_code` must be unique within the language catalog unless a documented exception exists. Reused generic names such as `directory_root`, `member_directory`, or `members_directory` should be avoided unless namespaced by source family.

### Seed URL quality model

A seed URL is the actual planned startpoint URL.

Required seed URL fields:

- `seed_type`
- `submitted_url`
- `canonical_url`
- `is_enabled`
- `priority`
- `max_depth`
- `recrawl_interval`
- `seed_metadata`
- `review_state`

Required seed metadata signals:

- language relevance
- logistics relevance
- expected entity type
- expected content type
- expected discovery value
- risk notes
- robots review requirement
- source authority reason
- category coverage reason

Seed URLs must not be activated directly from planning files. They require later review and explicit runtime insertion gate.

### Scheduler diversity design notes

The current crawler_core duration test showed a domain diversity risk: the crawler can spend long periods inside one domain.

This strategy prepares data for a later domain-aware scheduler, but it does not patch scheduler runtime now.

Future scheduler direction:

- if domain A is in cooldown, select eligible domain B
- rotate across languages
- rotate across source categories
- rotate across host budget groups
- avoid same-host back-to-back claims when alternatives exist
- preserve robots and politeness per host
- apply diversity penalty to over-dominant domains
- produce duration-test domain diversity metrics

This must not become aggressive crawling. Same-domain politeness remains strict. The gain comes from choosing a different eligible domain, source, or language instead of sleeping globally when safe alternatives exist.

### Crawler_core boundary

Source/seed quality is not content filtering.

crawler_core remains a raw evidence collector. It should collect raw evidence and preserve crawl facts.

The following belong later to parse_core or desktop_import:

- semantic filtering
- entity extraction
- taxonomy mapping
- quality scoring
- duplicate company resolution
- language-specific entity confidence
- ranking and enrichment

Source/startpoint catalogs only improve where crawler_core begins and how future scheduling can maintain diversity.

### Audit gates before runtime

No language catalog may be used by runtime before these audits pass:

1. JSON parse audit
2. required top-level field audit
3. required source family field audit
4. required seed surface field audit
5. required seed URL field audit
6. duplicate `source_family_code` audit
7. duplicate `surface_code` audit
8. duplicate `canonical_url` audit
9. HTTPS-only audit
10. valid domain audit
11. host mismatch audit
12. language relevance audit
13. logistics relevance audit
14. authority/trust audit
15. source category coverage audit
16. domain diversity audit
17. robots/politeness review note audit
18. GitHub tracked manifest audit
19. no runtime activation audit
20. pi51c sync gate audit

### Do-not-touch-pi51c rule

During the R96 24-hour crawler_core test, this line must not touch pi51c.

Allowed:

- Ubuntu Desktop repo read-only audit
- Ubuntu Desktop doc and catalog file preparation
- GitHub commit/push through explicit gate

Forbidden:

- pi51c SSH command
- pi51c repo fetch/reset/pull
- pi51c live runtime copy
- pi51c service changes
- pi51c crawler start/stop
- pi51c DB mutation
- pi51c raw evidence cleanup

pi51c sync comes later as a separate explicit gate.

### Next implementation order

The next safe order is:

1. create and seal this strategy document
2. add docs README link
3. run post-mutation audit
4. commit and push doc-only change
5. create strict JSON schema or manifest standard for 25 language catalogs
6. create missing language catalog directories and placeholder-safe manifest files in controlled gates
7. fill all 25 languages with high-quality source families and seed surfaces
8. audit all 25 catalogs
9. commit/push
10. only after R96 is complete, decide pi51c sync gate

## Türkçe

### Amaç

Bu doküman crawler_core için LogisticSearch taxonomy kapsamındaki 25 dilde kontrollü source/startpoint stratejisini tanımlar.

Amaç, pi51c üzerinde çalışan 24 saatlik crawler_core testini bozmadan, yüksek kaliteli dil bazlı source family ve seed katalogları hazırlamaktır.

Bu doküman sadece planlama ve yönetişim yüzeyidir. Hiçbir seed'i aktif etmez, frontier satırı eklemez, scheduler davranışını değiştirmez, PostgreSQL'e bağlanmaz ve pi51c'ye senkron yapmaz.

### Sert sınır

Bu çalışma hattı sadece Ubuntu Desktop ve GitHub ile sınırlıdır.

Bu hatta yasak olanlar:

- pi51c repo sync yok
- pi51c live runtime kopyalama yok
- crawler start veya stop yok
- systemd start, stop, restart, enable veya disable yok
- PostgreSQL mutation yok
- frontier insert yok
- scheduler runtime patch yok
- raw body silme yok
- sidecar silme yok
- chmod, chown, mount, rm, rsync veya scp yok
- secret, DSN, token, parola, user-agent secret veya process command line basma yok

Çalışan pi51c R96 24 saatlik testi kesinlikle dokunulmadan kalmalıdır.

### Kanonik topoloji kararı

Repo içinde zaten source/startpoint tasarım yüzeyi vardır:

- `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`

Repo içinde şu anda yoktur:

- `makpi51crawler/source_seed/`
- `makpi51crawler/source_seed/crawler_core/`
- `makpi51crawler/source_seed/crawler_core/languages/`

Bu yüzden bu çalışma hattındaki kanonik karar:

- mevcut `makpi51crawler/catalog/startpoints/<lang>/` modeli genişletilecek
- ayrı bir mimari karar olmadan yeni `makpi51crawler/source_seed/` ağacı açılmayacak
- source/startpoint manifestleri önce GitHub'da tracked dosya olarak hazırlanacak
- pi51c senkronu sadece daha sonra ayrı açık gate ile yapılacak

İngilizce mevcut istisnadır, çünkü zaten şu dosya vardır:

- `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`

Yeni dil katalog hedef deseni:

- `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/de/german_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v1.json`
- `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v1.json`
- kalan tüm diller için aynı desen

### 25 dil katalog planı

Tam hedef dil seti kesin olarak 25 dildir:

1. `en` English
2. `tr` Turkish
3. `de` German
4. `ar` Arabic
5. `zh` Chinese
6. `es` Spanish
7. `fr` French
8. `it` Italian
9. `pt` Portuguese
10. `nl` Dutch
11. `ru` Russian
12. `uk` Ukrainian
13. `bg` Bulgarian
14. `cs` Czech
15. `hu` Hungarian
16. `ro` Romanian
17. `el` Greek
18. `he` Hebrew
19. `ja` Japanese
20. `ko` Korean
21. `hi` Hindi
22. `bn` Bengali
23. `ur` Urdu
24. `id` Indonesian
25. `vi` Vietnamese

İlk uygulama hedefi sadece 5 dil değil, 25 dilin tamamı için eksiksiz tasarım yüzeyidir.

Pratik üretim sırası yine risk azaltmak için kademeli olabilir:

1. English baseline audit
2. katı 25 dil manifest standardı
3. eksik dil dizinleri ve kataloglarının kontrollü gate ile oluşturulması
4. JSON structure validation
5. URL format validation
6. duplicate domain ve duplicate seed URL validation
7. source type coverage validation
8. language relevance validation
9. logistics relevance validation
10. GitHub tracked manifest inventory validation
11. commit ve push
12. R96 bittikten sonra ayrı gate ile pi51c sync

### Source family kalite modeli

Source family, güvenilir bir kaynağın kalıcı üst nesnesidir.

Source family şu kaynak tiplerini temsil edebilir:

- resmi lojistik derneği
- freight forwarder association
- customs broker association
- chamber veya business registry
- port authority
- airport cargo authority
- rail freight authority veya directory
- road freight directory
- sea freight directory
- air cargo directory
- courier veya parcel directory
- 3PL / 4PL directory
- project cargo network
- cold chain logistics source
- dangerous goods logistics source
- trade fair veya exhibitor directory
- industry portal
- company directory

Her source family scheduler ve güvenlik sinyallerini korumalıdır.

Zorunlu source family alanları:

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
- `family_metadata`
- `family_review_state`
- `host_budget_group`
- `cross_seed_traversal_allowed`
- `cross_language_traversal_allowed`
- `seed_surfaces`

Zorunlu family metadata sinyalleri:

- `trust_tier`
- `source_quality_tier`
- `discovery_value`
- `noise_risk`
- `quality_model_version`
- `runtime_activation_policy`
- `human_review_required_before_frontier`
- `live_check_required`

English katalog faydalı bir başlangıçtır ama kör kopyalanmamalıdır. R3B, mevcut English katalogda `host_budget_group`, `family_review_state`, traversal flag'leri, seed review state alanları, duplicate surface code kalıpları ve host mismatch satırları gibi eksikler buldu.

Yeni kataloglar daha katı modelle hazırlanmalıdır.

### Seed surface kalite modeli

Seed surface, source family altındaki crawlable veya reviewable giriş yüzeyidir.

Zorunlu seed surface alanları:

- `surface_code`
- `surface_type`
- `surface_name`
- `surface_scope`
- `surface_metadata`
- `seed_urls`

Seed surface şunları temsil edebilir:

- member directory
- directory search page
- country directory
- regional directory
- category page
- association member search
- listing index
- trade fair exhibitor index
- public registry search page

`surface_code`, dil kataloğu içinde tekil olmalıdır. `directory_root`, `member_directory`, `members_directory` gibi genel isimler source family ile namespaced hale getirilmeden tekrar kullanılmamalıdır.

### Seed URL kalite modeli

Seed URL gerçek planlanan başlangıç URL'idir.

Zorunlu seed URL alanları:

- `seed_type`
- `submitted_url`
- `canonical_url`
- `is_enabled`
- `priority`
- `max_depth`
- `recrawl_interval`
- `seed_metadata`
- `review_state`

Zorunlu seed metadata sinyalleri:

- language relevance
- logistics relevance
- expected entity type
- expected content type
- expected discovery value
- risk notes
- robots review requirement
- source authority reason
- category coverage reason

Seed URL'ler planlama dosyasından doğrudan aktif edilmemelidir. Daha sonra review ve explicit runtime insertion gate gerekir.

### Scheduler çeşitlilik tasarım notları

Mevcut crawler_core duration testi bir domain diversity riski gösterdi: crawler uzun süre tek domain içinde kalabiliyor.

Bu strateji ileride domain-aware scheduler için veri hazırlar, fakat şu anda scheduler runtime patch yapmaz.

Gelecekte scheduler yönü:

- domain A cooldown içindeyse uygun domain B seç
- diller arasında rotasyon yap
- source category arasında rotasyon yap
- host budget group arasında rotasyon yap
- alternatif varsa aynı host'u arka arkaya seçmekten kaçın
- robots ve politeness kuralını host bazında koru
- aşırı baskın domainlere diversity penalty uygula
- duration testlerde domain diversity metriği üret

Bu agresif crawling anlamına gelmez. Same-domain politeness katı biçimde kalır. Kazanç, global sleep sırasında güvenli alternatif domain, source veya language seçebilmekten gelir.

### crawler_core sınırı

Source/seed kalitesi içerik filtreleme değildir.

crawler_core ham kanıt toplayıcı olarak kalır. Ham kanıtı toplar ve crawl gerçeklerini saklar.

Şunlar daha sonra parse_core veya desktop_import tarafına aittir:

- semantic filtering
- entity extraction
- taxonomy mapping
- quality scoring
- duplicate company resolution
- language-specific entity confidence
- ranking and enrichment

Source/startpoint katalogları sadece crawler_core'un nereden başlayacağını ve ileride scheduling çeşitliliğini iyileştirir.

### Runtime öncesi audit gate'leri

Hiçbir dil kataloğu şu auditler geçmeden runtime tarafından kullanılamaz:

1. JSON parse audit
2. required top-level field audit
3. required source family field audit
4. required seed surface field audit
5. required seed URL field audit
6. duplicate `source_family_code` audit
7. duplicate `surface_code` audit
8. duplicate `canonical_url` audit
9. HTTPS-only audit
10. valid domain audit
11. host mismatch audit
12. language relevance audit
13. logistics relevance audit
14. authority/trust audit
15. source category coverage audit
16. domain diversity audit
17. robots/politeness review note audit
18. GitHub tracked manifest audit
19. no runtime activation audit
20. pi51c sync gate audit

### pi51c'ye dokunmama kuralı

R96 24 saatlik crawler_core testi boyunca bu çalışma hattı pi51c'ye dokunmaz.

İzinli olanlar:

- Ubuntu Desktop repo read-only audit
- Ubuntu Desktop doküman ve katalog hazırlığı
- açık gate ile GitHub commit/push

Yasak olanlar:

- pi51c SSH komutu
- pi51c repo fetch/reset/pull
- pi51c live runtime copy
- pi51c service değişikliği
- pi51c crawler start/stop
- pi51c DB mutation
- pi51c raw evidence cleanup

pi51c sync daha sonra ayrı explicit gate ile yapılır.

### Sonraki uygulama sırası

Güvenli sonraki sıra:

1. bu strateji dokümanını oluştur ve mühürle
2. docs README linkini ekle
3. post-mutation audit çalıştır
4. doc-only değişikliği commit ve push yap
5. 25 dil katalogları için katı JSON schema veya manifest standardı oluştur
6. eksik dil katalog dizinlerini ve placeholder-safe manifest dosyalarını kontrollü gate ile oluştur
7. 25 dilin tamamını yüksek kaliteli source family ve seed surface ile doldur
8. 25 kataloğun tamamını audit et
9. commit/push yap
10. sadece R96 tamamlandıktan sonra pi51c sync gate kararını ver
<!-- SOURCE_SEED_R5B_CONTROLLED_REPAIR_START -->

## Controlled R5B repair addendum

### English

This addendum seals the missing documentation details found by `SOURCE_SEED_R4B_DIRTY_DOC_SCOPE_CLASSIFICATION_READONLY`.

Durable data/configuration rule: source/startpoint manifests remain source-controlled JSON files and future runtime persistence must preserve the project-wide PostgreSQL + JSONB model. JSONB is the intended database-side representation for durable crawler/source/seed metadata when a later explicit DB gate exists. This strategy document does not execute that DB gate.

Planned 25 language catalog files:

- `en` / English: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- `tr` / Turkish: `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json`
- `de` / German: `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json`
- `ar` / Arabic: `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json`
- `zh` / Chinese: `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json`
- `es` / Spanish: `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json`
- `fr` / French: `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json`
- `it` / Italian: `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json`
- `pt` / Portuguese: `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json`
- `nl` / Dutch: `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json`
- `ru` / Russian: `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json`
- `uk` / Ukrainian: `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json`
- `bg` / Bulgarian: `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json`
- `cs` / Czech: `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json`
- `hu` / Hungarian: `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json`
- `ro` / Romanian: `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json`
- `el` / Greek: `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json`
- `he` / Hebrew: `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json`
- `ja` / Japanese: `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json`
- `ko` / Korean: `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json`
- `hi` / Hindi: `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json`
- `bn` / Bengali: `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json`
- `ur` / Urdu: `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json`
- `id` / Indonesian: `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json`
- `vi` / Vietnamese: `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json`

### Türkçe

Bu ek bölüm, `SOURCE_SEED_R4B_DIRTY_DOC_SCOPE_CLASSIFICATION_READONLY` tarafından bulunan eksik dokümantasyon noktalarını mühürler.

Kalıcı veri/konfigürasyon kuralı: source/startpoint manifestleri source-control altındaki JSON dosyaları olarak kalır ve ileride runtime kalıcılığına geçilecekse proje genelindeki PostgreSQL + JSONB modeli korunmalıdır. JSONB, daha sonra açık bir DB gate geldiğinde crawler/source/seed metadata için veritabanı tarafındaki hedef temsildir. Bu strateji dokümanı o DB gate'ini çalıştırmaz.

Planlanan 25 dil katalog dosyaları:

- `en` / English: `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
- `tr` / Turkish: `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json`
- `de` / German: `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json`
- `ar` / Arabic: `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json`
- `zh` / Chinese: `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json`
- `es` / Spanish: `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json`
- `fr` / French: `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json`
- `it` / Italian: `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json`
- `pt` / Portuguese: `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json`
- `nl` / Dutch: `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json`
- `ru` / Russian: `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json`
- `uk` / Ukrainian: `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json`
- `bg` / Bulgarian: `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json`
- `cs` / Czech: `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json`
- `hu` / Hungarian: `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json`
- `ro` / Romanian: `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json`
- `el` / Greek: `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json`
- `he` / Hebrew: `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json`
- `ja` / Japanese: `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json`
- `ko` / Korean: `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json`
- `hi` / Hindi: `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json`
- `bn` / Bengali: `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json`
- `ur` / Urdu: `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json`
- `id` / Indonesian: `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json`
- `vi` / Vietnamese: `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json`

<!-- SOURCE_SEED_R5B_CONTROLLED_REPAIR_END -->
<!-- SOURCE_SEED_R6A_EXACT_NEEDLE_REPAIR_START -->

## R6A exact audit phrase repair

### English

The source/seed strategy is limited to Ubuntu Desktop + GitHub until a later explicit sync gate exists. There is no runtime scheduler patch in this documentation step, and there is no DB mutation in this documentation step.

### Türkçe

Source/seed stratejisi, daha sonra açık bir sync gate gelene kadar Ubuntu Desktop + GitHub ile sınırlıdır. Bu dokümantasyon adımında no runtime scheduler patch kuralı geçerlidir ve bu dokümantasyon adımında no DB mutation kuralı geçerlidir.

<!-- SOURCE_SEED_R6A_EXACT_NEEDLE_REPAIR_END -->
