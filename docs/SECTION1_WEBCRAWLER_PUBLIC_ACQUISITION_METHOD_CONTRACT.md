# Webcrawler Public Acquisition Method Contract
# Webcrawler Kamuya Açık Edinim Yöntemi Sözleşmesi

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Purpose
## Amaç

This document freezes the current canonical design direction for how the LogisticSearch webcrawler must acquire publicly accessible content.

It exists because the current crawler core already proves several important direct-HTTP foundation paths, but that is still not enough to declare crawler-core closure.

The user goal is stricter:

- the crawler must visibly browse
- it must collect public content
- it must use different acquisition methods when necessary
- crawler_core must remain open until those broader public-acquisition capabilities are real, visible, and tested

Bu belge, LogisticSearch webcrawler’ın kamuya açık erişilebilir içeriği nasıl edinmesi gerektiğine dair mevcut kanonik tasarım yönünü sabitler.

Bu belgeye ihtiyaç vardır; çünkü mevcut crawler core birkaç önemli direct-HTTP foundation yolunu zaten kanıtlamıştır, ancak bu hâlâ crawler_core kapanışı ilan etmek için yeterli değildir.

Kullanıcı hedefi daha katıdır:

- crawler görünür biçimde gezinmelidir
- public içeriği toplamalıdır
- gerektiğinde farklı acquisition yöntemleri kullanmalıdır
- bu daha geniş public-acquisition kabiliyetleri gerçek, görünür ve test edilmiş hale gelene kadar crawler_core açık kalmalıdır

## Current truth boundary
## Güncel gerçeklik sınırı

At the time of writing, the repository visibly contains a real direct-HTTP acquisition surface.

Visible current truth includes:

- direct HTTP request/response acquisition through the current Python worker runtime
- raw HTTP body persistence under `/srv/crawler/logisticsearch/raw_fetch`
- robots refresh and robots allow/block decisions
- durable success / retryable / permanent / unexpected-runtime finalize paths
- storage fallback decision logic for processed output

But the repository does **not** yet visibly contain a canonical browser-render acquisition runtime.

That means crawler_core is still **OPEN**.

Bu belge yazıldığı anda repository içinde görünür bir gerçek direct-HTTP acquisition yüzeyi vardır.

Görünür güncel doğrular şunları içerir:

- mevcut Python worker runtime üzerinden direct HTTP request/response acquisition
- ham HTTP body kalıcılığı: `/srv/crawler/logisticsearch/raw_fetch`
- robots refresh ve robots allow/block kararları
- durable success / retryable / permanent / unexpected-runtime finalize yolları
- işlenmiş çıktı için storage fallback karar mantığı

Ancak repository görünür biçimde henüz kanonik bir browser-render acquisition runtime içermemektedir.

Bu da crawler_core’un hâlâ **AÇIK** olduğu anlamına gelir.

## Canonical acquisition method families
## Kanonik edinim yöntemi aileleri

The crawler must be designed around the following acquisition method families.

### 1. Direct HTTP acquisition
### 1. Direct HTTP edinimi

Use the current lightweight direct request/response path when the target content is already visible in the original HTTP response body.

This remains the simplest and cheapest acquisition path.

Hedef içerik zaten ilk HTTP response body içinde görünüyorsa mevcut hafif direct request/response yolu kullanılmalıdır.

Bu, en basit ve en ucuz acquisition yoludur.

### 2. Browser-render acquisition
### 2. Browser-render edinimi

Use a controlled browser runtime when the public page requires client-side rendering before meaningful content becomes visible.

This is required for JS-rendered or hydration-dependent public pages.

Anlamlı içerik görünür hale gelmeden önce istemci tarafı render gerektiren public sayfalarda kontrollü browser runtime kullanılmalıdır.

Bu yol, JS-rendered veya hydration-dependent public sayfalar için gereklidir.

### 3. Post-render DOM snapshot capture
### 3. Post-render DOM snapshot yakalama

When browser rendering is used, the crawler must be able to capture the rendered DOM snapshot as evidence.

This is different from the original raw HTTP body.

Browser rendering kullanıldığında crawler rendered DOM snapshot’ını kanıt olarak yakalayabilmelidir.

Bu, ilk ham HTTP body’den farklı bir şeydir.

### 4. Public network capture
### 4. Public network capture

When public content becomes visible through XHR/fetch/API calls made by the browser, the crawler must be able to capture that public network evidence.

This means the crawler should not be limited to only the first HTML response.

Public içerik tarayıcının yaptığı XHR/fetch/API çağrıları üzerinden görünür hale geliyorsa crawler bu public network evidence’ını da yakalayabilmelidir.

Yani crawler yalnızca ilk HTML response ile sınırlı kalmamalıdır.

### 5. Controlled interaction acquisition
### 5. Kontrollü etkileşim edinimi

When public content requires actions such as scrolling, expanding, paginating, or pressing a public “load more” style control, the crawler must support controlled interaction.

This must remain disciplined and bounded.

Public içeriğe ulaşmak için scroll, expand, pagination veya kamuya açık “load more” benzeri kontroller gerekiyorsa crawler kontrollü etkileşimi desteklemelidir.

Bu destek disiplinli ve sınırlı kalmalıdır.

## Method selection contract
## Yöntem seçimi sözleşmesi

The crawler must not jump blindly into browser usage.

The canonical selection order must remain:

1. try direct HTTP first when the target is likely visible without rendering
2. escalate to browser-render acquisition only when direct HTTP is insufficient
3. capture rendered DOM and public network evidence when browser mode is used
4. use controlled interaction only when simpler browser render is still insufficient
5. store enough evidence to explain why the chosen method was necessary

Crawler kör biçimde hemen browser kullanımına atlamamalıdır.

Kanonik seçim sırası şöyle kalmalıdır:

1. hedef render olmadan görünür olma ihtimali taşıyorsa önce direct HTTP dene
2. direct HTTP yetersiz kaldığında browser-render acquisition’a yüksel
3. browser modu kullanılıyorsa rendered DOM ve public network evidence yakala
4. daha basit browser render yine yetersizse kontrollü etkileşim kullan
5. seçilen yöntemin neden gerekli olduğunu açıklayacak kadar evidence sakla

## Evidence storage direction
## Kanıt depolama yönü

Current visible raw HTTP body evidence already belongs under:

- `/srv/crawler/logisticsearch/raw_fetch`

The next canonical evidence families that must be introduced for broader public acquisition are:

- rendered HTML / post-render DOM evidence
- public network capture evidence
- browser-session level acquisition evidence

This document freezes those evidence families as required design scope, even if the exact child paths are implemented in the next steps.

Mevcut görünür ham HTTP body evidence’ı zaten şu yol altına aittir:

- `/srv/crawler/logisticsearch/raw_fetch`

Daha geniş public acquisition için sıradaki kanonik evidence aileleri şunlar olmalıdır:

- rendered HTML / post-render DOM evidence
- public network capture evidence
- browser-session seviyesinde acquisition evidence

Bu belge, kesin çocuk path’ler bir sonraki adımlarda implemente edilecek olsa bile, bu evidence ailelerini zorunlu tasarım kapsamı olarak sabitler.

## Closure rule
## Kapanış kuralı

Crawler core must **not** be treated as closed merely because direct-HTTP paths are working.

Crawler core may be considered closure-ready only after all of the following become true:

- direct HTTP acquisition is proven
- browser-render acquisition is real
- rendered DOM capture is real
- public network capture is real
- at least one real browser-driven public collection path is seen and tested
- method-selection behavior is explicitly documented and validated

Crawler core, yalnızca direct-HTTP yolları çalışıyor diye **kapalı** kabul edilmemelidir.

Crawler core ancak şu koşulların tamamı sağlandığında closure-ready olarak düşünülebilir:

- direct HTTP acquisition kanıtlandı
- browser-render acquisition gerçek oldu
- rendered DOM capture gerçek oldu
- public network capture gerçek oldu
- en az bir gerçek browser-driven public collection yolu görüldü ve test edildi
- method-selection davranışı açıkça dokümante edilip doğrulandı

## Required next implementation sequence
## Gerekli sonraki implementation sırası

The next implementation sequence should remain strict:

1. bootstrap a canonical browser acquisition runtime surface in the repository
2. install the necessary automation dependency in the crawler runtime environment
3. run a first real browser-render smoke against a public target
4. persist rendered DOM evidence
5. persist public network capture evidence
6. define controlled interaction boundaries
7. integrate method-selection logic into the crawler worker flow
8. only then revisit crawler-core closure language

Sonraki implementation sırası katı kalmalıdır:

1. repository içinde kanonik bir browser acquisition runtime yüzeyi bootstrap et
2. crawler runtime ortamına gerekli automation dependency’yi kur
3. public bir hedefe karşı ilk gerçek browser-render smoke’u çalıştır
4. rendered DOM evidence kalıcılığını ekle
5. public network capture evidence kalıcılığını ekle
6. kontrollü etkileşim sınırlarını tanımla
7. method-selection mantığını crawler worker akışına entegre et
8. ancak ondan sonra crawler-core closure diline geri dön

## Relation to parse_core
## parse_core ile ilişki

This document does not move the project into parse_core.

It keeps the project inside crawler_core by defining the acquisition expansion required before crawler_core can honestly be considered complete enough.

Bu belge projeyi parse_core aşamasına taşımaz.

Tam tersine, crawler_core’un dürüst biçimde yeterince tamamlanmış sayılabilmesi için gereken acquisition genişlemesini tanımlayarak projeyi crawler_core içinde tutar.
