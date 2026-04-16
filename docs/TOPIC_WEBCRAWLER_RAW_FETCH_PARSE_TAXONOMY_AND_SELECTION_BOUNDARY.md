# Webcrawler Raw Fetch, Parse, Taxonomy, and Selection Boundary
# Webcrawler Raw Fetch, Parse, Taxonomy ve Seçim Sınırı

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Purpose
## Amaç

This document freezes the canonical boundary between the following layers of the LogisticSearch webcrawler system:

- raw fetch
- acquisition
- parse
- taxonomy/classification
- later ranking/export decisions

It exists because these boundaries must remain explicit, beginner-readable, and operationally stable while crawler_core keeps evolving.

Bu belge, LogisticSearch webcrawler sistemindeki şu katmanlar arasındaki kanonik sınırı sabitler:

- raw fetch
- acquisition
- parse
- taxonomy/classification
- sonraki ranking/export kararları

Bu belgeye ihtiyaç vardır; çünkü crawler_core gelişmeye devam ederken bu sınırlar açık, beginner-okunur ve operasyonel olarak stabil kalmalıdır.

## Very short mental model
## Çok kısa zihinsel model

If you are doing this for the first time, read the system like this:

1. choose a public candidate URL
2. fetch what the crawler can visibly obtain
3. save that first evidence safely
4. parse the saved evidence
5. classify the parsed result with taxonomy
6. keep useful logistics-facing results
7. discard or down-rank irrelevant material later

İlk kez yapıyorsan sistemi şu şekilde oku:

1. kamuya açık aday URL seç
2. crawler'ın görünür biçimde alabildiğini fetch et
3. bu ilk kanıtı güvenli biçimde sakla
4. saklanan kanıtı parse et
5. parse sonucunu taxonomy ile sınıflandır
6. işe yarayan lojistik odaklı sonuçları koru
7. alakasız materyali daha sonra ele veya düşür

## What `raw_fetch` really means
## `raw_fetch` gerçekte ne demektir

`raw_fetch` is the first raw evidence layer of the crawler.

It is **not** the final structured business dataset.

It is **not** the final logistics entity dataset.

It is **not** the final ranking or search-ready payload.

It is the place where the crawler stores the first captured evidence of what it saw at a public URL before deeper interpretation begins.

`raw_fetch`, crawler'ın ilk ham kanıt katmanıdır.

Bu katman **nihai yapılı iş verisi** değildir.

Bu katman **nihai lojistik entity veri seti** değildir.

Bu katman **nihai ranking veya search-ready payload** değildir.

Bu katman, daha derin yorumlama başlamadan önce crawler'ın kamuya açık bir URL'de ne gördüğüne dair ilk yakalanmış kanıtı sakladığı yerdir.

## What can belong to `raw_fetch`
## `raw_fetch` içine neler girebilir

Typical raw-fetch artefacts include:

- original HTTP response body
- rendered HTML produced through browser acquisition
- screenshot evidence
- robots.txt body
- basic fetch metadata such as final URL, status, content type, hashes, and timestamps

These are still first-layer evidence artefacts.

They have not yet been interpreted into domain meaning.

Tipik raw-fetch artefact'ları şunları içerebilir:

- ilk HTTP response body
- browser acquisition ile üretilen rendered HTML
- screenshot kanıtı
- robots.txt body
- final URL, status, content type, hash ve timestamp gibi temel fetch metadata'sı

Bunların hepsi hâlâ ilk katman kanıt artefact'larıdır.

Henüz alan-anlamı üretilmiş veri değildir.

## What `raw_fetch` does **not** mean
## `raw_fetch` **ne anlama gelmez**

`raw_fetch` does **not** mean:

- the crawler mirrors the whole internet
- every fetched page becomes a useful kept record
- every fetched page is already classified as logistics-related
- the taxonomy decision is already made
- the parse/extraction phase is already complete

`raw_fetch` şu anlama **gelmez**:

- crawler bütün interneti aynalıyor
- fetch edilen her sayfa faydalı kalıcı kayıt oluyor
- fetch edilen her sayfa zaten lojistikle ilgili diye sınıflandırıldı
- taxonomy kararı çoktan verildi
- parse/extraction aşaması çoktan tamamlandı

## What `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_2_2_acquisition_runtime.py` is responsible for
## `hosts/makpi51crawler/python/webcrawler/lib/logisticsearch1_1_2_2_acquisition_runtime.py` tam olarak neden sorumludur

This file is the acquisition home.

Its job is to produce first-layer acquisition evidence for a claimed candidate URL.

Its scope is intentionally narrower than later parse and classification work.

Bu dosya acquisition evidir.

Görevi, claim edilmiş aday bir URL için ilk katman acquisition evidence üretmektir.

Kapsamı, daha sonraki parse ve classification işinden bilinçli olarak daha dardır.

### What this file should collect
### Bu dosya ne toplamalıdır

This file should collect:

- direct-HTTP page bodies when the content is already visible without rendering
- robots.txt bodies and related fetch evidence
- browser-backed rendered HTML when direct HTTP is insufficient
- screenshot evidence when browser-backed acquisition is used
- narrow fetch metadata needed to prove what was acquired

Bu dosya şunları toplamalıdır:

- içerik render gerektirmeden görünüyorsa direct HTTP page body
- robots.txt body ve ilgili fetch kanıtı
- direct HTTP yetersiz kaldığında browser-backed rendered HTML
- browser-backed acquisition kullanıldığında screenshot kanıtı
- neyin alındığını ispatlamak için gereken dar fetch metadata'sı

### What this file should **not** decide
### Bu dosya neyi **kararlaştırmamalıdır**

This file should **not** decide:

- whether the page is definitely a logistics company page
- whether the page should become a final entity
- which taxonomy node is the final match
- whether the page deserves downstream ranking
- whether the page is a high-value export candidate

Those are later-layer responsibilities.

Bu dosya şunları **kararlaştırmamalıdır**:

- sayfanın kesin olarak lojistik firma sayfası olup olmadığı
- sayfanın nihai entity'ye dönüşüp dönüşmeyeceği
- hangi taxonomy node'unun nihai eşleşme olduğu
- sayfanın downstream ranking'i hak edip etmediği
- sayfanın yüksek değerli export adayı olup olmadığı

Bunlar daha sonraki katmanların sorumluluğudur.

## What parse is supposed to do later
## Parse daha sonra ne yapmalıdır

Parse is the first layer that starts reading meaning from raw evidence.

It should work on the evidence already captured by acquisition.

Typical parse work includes:

- title/body/link extraction
- simple structured field discovery
- snapshot-safe evidence extraction
- first content suitability checks
- first candidate signal extraction for later classification

Parse, ham kanıttan anlam okumaya başlayan ilk katmandır.

Acquisition tarafından zaten yakalanmış kanıt üzerinde çalışmalıdır.

Tipik parse işleri şunları içerir:

- title/body/link extraction
- basit yapılı alan keşfi
- snapshot-safe evidence extraction
- ilk içerik uygunluk kontrolleri
- daha sonraki classification için ilk aday sinyal çıkarımı

## What taxonomy is supposed to do later
## Taxonomy daha sonra ne yapmalıdır

Taxonomy is not the same thing as acquisition.

Taxonomy is the domain interpretation and classification backbone.

Its job is to help answer questions such as:

- what kind of logistics-facing signal is present here
- which service/category/node does this page most likely belong to
- is this probably relevant, weakly relevant, or irrelevant
- which downstream paths deserve further processing

Taxonomy, acquisition ile aynı şey değildir.

Taxonomy, alan yorumu ve classification omurgasıdır.

Görevi şu tür sorulara yardım etmektir:

- burada hangi tür lojistik odaklı sinyal var
- bu sayfa en olası olarak hangi service/category/node'a ait
- bu içerik muhtemelen ilgili mi, zayıf ilgili mi, yoksa alakasız mı
- hangi downstream yollar daha ileri işlemeyi hak ediyor

## Will the crawler visit non-logistics pages too
## Crawler lojistik dışı sayfaları da ziyaret edecek mi

Yes, sometimes it must.

A crawler often cannot know the full domain meaning of a page before it first acquires the visible evidence.

That is especially true for:

- weakly described landing pages
- JS-rendered pages
- navigation-heavy sites
- pages where the useful signal appears only after rendering or later extraction

So the correct rule is:

- acquisition may visit broader candidate public pages
- parse and taxonomy later decide whether the material is useful
- irrelevant material should not automatically become a kept high-value result

Evet, bazen etmek zorundadır.

Crawler çoğu zaman bir sayfanın tam alan-anlamını ilk görünür evidence'i almadan önce bilemez.

Bu özellikle şu durumlarda daha da doğrudur:

- zayıf açıklanmış landing page'ler
- JS-rendered sayfalar
- navigasyonu ağır siteler
- faydalı sinyalin ancak render veya sonraki extraction sonrası göründüğü sayfalar

Bu yüzden doğru kural şudur:

- acquisition daha geniş aday public sayfaları ziyaret edebilir
- parse ve taxonomy daha sonra materyalin faydalı olup olmadığını kararlaştırır
- alakasız materyal otomatik olarak kalıcı yüksek değerli sonuç haline gelmemelidir

## Method selection rule
## Yöntem seçimi kuralı

The canonical order should remain:

1. try direct HTTP first when rendering is probably unnecessary
2. escalate to browser-backed acquisition only when direct HTTP is insufficient
3. capture rendered DOM and screenshot evidence when browser mode is used
4. later add public network evidence and controlled interaction where required
5. keep the system bounded and explicit

Kanonik sıra şu şekilde kalmalıdır:

1. render büyük ihtimalle gereksizse önce direct HTTP dene
2. direct HTTP yetersizse browser-backed acquisition'a yüksel
3. browser modu kullanıldığında rendered DOM ve screenshot kanıtını yakala
4. gerektiğinde daha sonra public network evidence ve kontrollü etkileşimi ekle
5. sistemi sınırlı ve açık tut

## Where the main paths belong
## Ana yolların sistemdeki yeri

### `/srv/crawler/logisticsearch/`
### `/srv/crawler/logisticsearch/`

This is the crawler-side operational root.

It is where crawler-local operational surfaces live.

This includes the raw-fetch evidence tree.

Burası crawler tarafı operasyon köküdür.

Crawler'a ait yerel operasyon yüzeyleri burada yaşar.

Buna raw-fetch evidence ağacı da dahildir.

### `/srv/crawler/logisticsearch/raw_fetch`
### `/srv/crawler/logisticsearch/raw_fetch`

This is the raw evidence root for first captured fetch artefacts.

Burası ilk yakalanmış fetch artefact'ları için ham kanıt köküdür.

### `/srv/data/`
### `/srv/data/`

This is not the same thing as raw_fetch.

This path belongs to the processed-output side of the system.

It should hold more valuable, later-stage, operator-meaningful output rather than first raw evidence.

Burası raw_fetch ile aynı şey değildir.

Bu yol sistemin işlenmiş çıktı tarafına aittir.

İlk ham kanıttan çok, daha değerli, daha sonraki aşama, operatör-anlamlı çıktıları tutmalıdır.

### `/srv/buffer/`
### `/srv/buffer/`

This is the controlled fallback/buffer area.

It exists so the system can remain operational when the primary processed-output path is temporarily unsuitable.

Burası kontrollü fallback/buffer alanıdır.

Birincil işlenmiş çıktı yolu geçici olarak uygun değilken sistemin çalışmaya devam edebilmesi için vardır.

## Current design reading
## Güncel tasarım okuması

Read the current design like this:

- acquisition first captures evidence
- parse then reads structure and initial meaning
- taxonomy/classification then decides domain relevance and category interpretation
- later ranking/export should operate on already-filtered meaning, not on blind raw evidence

Güncel tasarımı şöyle oku:

- acquisition önce kanıtı yakalar
- parse sonra yapıyı ve ilk anlamı okur
- taxonomy/classification sonra alan ilgisini ve kategori yorumunu kararlaştırır
- daha sonraki ranking/export, kör ham kanıt üzerinde değil, zaten filtrelenmiş anlam üzerinde çalışmalıdır

## What is already true today
## Bugün zaten doğru olan nedir

At the current controlled stage, the system already proves:

- direct HTTP acquisition exists
- robots fetch exists
- narrow browser acquisition exists
- browser smoke evidence exists
- active runtime family lives under `hosts/makpi51crawler/python/webcrawler/lib/`

This is still not the same thing as full crawler-core closure.

Güncel kontrollü aşamada sistem şunları zaten kanıtlamaktadır:

- direct HTTP acquisition vardır
- robots fetch vardır
- dar browser acquisition vardır
- browser smoke kanıtı vardır
- aktif runtime ailesi `hosts/makpi51crawler/python/webcrawler/lib/` altında yaşamaktadır

Bu hâlâ tam crawler-core closure ile aynı şey değildir.

## Immediate next reading
## Hemen sonraki okuma

The next implementation work should keep the system lean:

- keep the main runtime stable
- keep the thin worker CLI thin
- let acquisition evolve inside the acquisition home
- let parse and taxonomy remain later-layer responsibilities
- do not blur fetch with classification

Sıradaki implementation işi sistemi yalın tutmalıdır:

- ana runtime'ı stabil tut
- ince worker CLI'yi ince tut
- acquisition'ın acquisition evi içinde gelişmesine izin ver
- parse ve taxonomy'yi sonraki katman sorumlulukları olarak koru
- fetch ile classification'ı birbirine karıştırma

## Tiny glossary
## Mini sözlük

### raw evidence
### ham kanıt

The first captured artefact before deeper interpretation.

Daha derin yorumlamadan önceki ilk yakalanmış artefact.

### acquisition
### edinim / acquisition

The act of obtaining visible public content and writing first evidence.

Görünür public içeriği alıp ilk kanıtı yazma işi.

### parse
### parse

Reading structure and extracting first usable signals from saved evidence.

Saklanan kanıttan yapı okuyup ilk kullanılabilir sinyalleri çıkarma işi.

### taxonomy
### taxonomy

The domain vocabulary and classification backbone.

Alan sözlüğü ve classification omurgası.

### seam
### seam

A narrow transition point between two layers while integration is still being completed.

Entegrasyon henüz tamamlanmamışken iki katman arasındaki dar geçiş noktası.

## Runtime tree cross-reference
## Runtime ağacı çapraz başvurusu

Use `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md` when you need the exact active file tree that sits above acquisition, parse, and taxonomy boundaries.

Acquisition, parse ve taxonomy sınırlarının üzerinde duran tam aktif dosya ağacına ihtiyaç duyduğunda `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md` dokümanını kullan.

## Canonical active path truth
## Kanonik aktif yol doğrusu

The current active raw evidence root is `/srv/webcrawler/raw_fetch`.

Mevcut aktif ham kanıt kökü `/srv/webcrawler/raw_fetch` dizinidir.

This path is distinct from processed-output routing under `/srv/data` and `/srv/buffer`, and it is also distinct from the later controlled export boundary at `/srv/webcrawler/exports`.

Bu yol, `/srv/data` ve `/srv/buffer` altındaki işlenmiş-çıktı yönlendirmesinden ayrıdır; ayrıca daha sonraki kontrollü export sınırı olan `/srv/webcrawler/exports` yolundan da ayrıdır.
