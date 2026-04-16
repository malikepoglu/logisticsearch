# SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP
# SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP

## Purpose
## Amaç

This document freezes the current beginner-first explanation for the active Pi51 webcrawler runtime tree, the role of each Python file, and the real data-flow boundaries between raw evidence, processed output, and later export handoff.

Bu doküman, aktif Pi51 webcrawler runtime ağacının güncel beginner-first açıklamasını, her Python dosyasının rolünü ve ham kanıt, işlenmiş çıktı ve sonraki export handoff sınırları arasındaki gerçek veri akışını mühürler.

This document exists because the crawler no longer uses the older flat naming model. The runtime now follows a tree-logic topology: one thin root entry, one main loop directly under that entry, a state gateway branch, a worker branch, and then deeper acquisition / parse / taxonomy leaves.

Bu doküman gereklidir; çünkü crawler artık eski düz adlandırma modelini kullanmıyor. Runtime artık tree-logic topolojisini izliyor: tek ince kök giriş, onun hemen altında tek ana loop, bir state gateway dalı, bir worker dalı ve onun altında daha derin acquisition / parse / taxonomy yaprakları.

## Current runtime tree
## Güncel runtime ağacı

`logisticsearch1_main_entry.py`  
└── `logisticsearch1_1_main_loop.py`  
&nbsp;&nbsp;&nbsp;&nbsp;├── `logisticsearch1_1_1_state_db_gateway.py`  
&nbsp;&nbsp;&nbsp;&nbsp;└── `logisticsearch1_1_2_worker_runtime.py`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `logisticsearch1_1_2_1_storage_routing.py`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── `logisticsearch1_1_2_2_acquisition_runtime.py`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   └── `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `logisticsearch1_1_2_3_parse_runtime.py`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── `logisticsearch1_1_2_3_1_taxonomy_runtime.py`  

`logisticsearch2_diag_browser_acquisition_smoke.py`

## Why this tree is correct
## Bu ağaç neden doğrudur

There must be only one thin root entry at the top. That root must not contain the real crawler business logic. Its job is only to provide the outermost module entry surface.

En üstte yalnızca tek bir ince kök giriş olmalıdır. Bu kök, gerçek crawler iş mantığını taşımamalıdır. Görevi yalnızca en dış modül giriş yüzeyini sağlamaktır.

Directly under that root there must be one main continuous loop. That loop owns CLI entry, repeated iteration rhythm, runtime-control operator surface, and the act of calling the per-iteration worker layer.

Bu kökün hemen altında tek bir ana sürekli loop bulunmalıdır. Bu loop; CLI girişini, tekrar eden iterasyon ritmini, runtime-control operatör yüzeyini ve iterasyon başına worker katmanını çağırma işini sahiplenir.

The per-iteration worker layer is not the root and not the outer loop. It is the orchestration layer that coordinates one worker pass: storage decision, DB truth read, URL claim, robots refresh, fetch selection, parse, and finish transitions.

İterasyon başına çalışan worker katmanı ne köktür ne de dış loop’tur. Bu katman; tek bir worker geçişinin orkestrasyon katmanıdır: storage kararı, DB doğrusu okuma, URL claim, robots refresh, fetch seçimi, parse ve finish transition işlemleri burada koordine edilir.

## File-by-file role map
## Dosya bazında rol haritası

### `logisticsearch1_main_entry.py`
### `logisticsearch1_main_entry.py`

This is the single thin root-entry surface. It exists so systemd and module execution can point to one unambiguous top-level runtime module.

Bu dosya tek ince kök-giriş yüzeyidir. systemd ve modül çalıştırma katmanı, tek ve belirsiz olmayan üst seviye runtime modülüne işaret edebilsin diye vardır.

It should stay small. It should import the main loop and delegate to it. It should not silently absorb worker logic, DB logic, or parse logic.

Küçük kalmalıdır. Ana loop’u import edip ona devretmelidir. Worker mantığını, DB mantığını veya parse mantığını sessizce içine çekmemelidir.

### `logisticsearch1_1_main_loop.py`
### `logisticsearch1_1_main_loop.py`

This is the main continuous loop directly under the root entry.

Bu dosya, kök girişin hemen altındaki ana sürekli loop’tur.

Its responsibilities are:
- parsing CLI arguments
- exposing runtime-control operator actions
- deciding whether to run one iteration or repeated iterations
- sleeping between loop iterations
- calling the per-iteration worker runtime

Sorumlulukları şunlardır:
- CLI argümanlarını parse etmek
- runtime-control operatör aksiyonlarını göstermek
- tek iterasyon mu yoksa tekrar eden iterasyon mu çalışacağını belirlemek
- loop iterasyonları arasında beklemek
- iterasyon başına worker runtime’ı çağırmak

It must remain thin. It is a control-loop surface, not the deeper worker logic owner.

İnce kalmalıdır. Bu dosya bir control-loop yüzeyidir; derin worker mantığının sahibi değildir.

### `logisticsearch1_1_1_state_db_gateway.py`
### `logisticsearch1_1_1_state_db_gateway.py`

This file is the state and DB gateway branch.

Bu dosya state ve DB gateway dalıdır.

It is the Python side that talks to the crawler database truth. It provides helpers for:
- opening and closing DB connections
- runtime-control read/write truth
- URL claim and lease operations
- robots decision helpers
- fetch finish transitions
- discovery enqueue helpers
- parse/preranking persistence helpers

Crawler veritabanı doğrusu ile konuşan Python tarafı budur. Şunlar için yardımcılar sağlar:
- DB bağlantısı açma ve kapama
- runtime-control okuma/yazma doğrusu
- URL claim ve lease işlemleri
- robots karar yardımcıları
- fetch finish transition işlemleri
- discovery enqueue yardımcıları
- parse/preranking persistence yardımcıları

The reason this sits beside the worker branch is simple: the worker and the loop both need durable DB truth, but DB truth itself should not be scattered across all runtime leaves.

Bu dalın worker dalının yanında durma nedeni basittir: hem worker hem de loop kalıcı DB doğrusuna ihtiyaç duyar, ama DB doğrusu tüm runtime yapraklarına dağılmamalıdır.

### `logisticsearch1_1_2_worker_runtime.py`
### `logisticsearch1_1_2_worker_runtime.py`

This is the main per-iteration worker orchestration layer.

Bu dosya iterasyon başına ana worker orkestrasyon katmanıdır.

One call into this file should represent one controlled worker pass. In that pass, the runtime:
- decides the processed-output routing state
- reads runtime-control truth
- decides whether claiming may continue
- claims one URL when allowed
- refreshes robots state when needed
- selects acquisition method
- fetches or blocks
- parses fetched evidence
- persists outcomes
- returns one structured payload

Bu dosyaya yapılan tek bir çağrı, kontrollü tek bir worker geçişini temsil etmelidir. Bu geçişte runtime:
- işlenmiş çıktı yönlendirme durumunu belirler
- runtime-control doğrusunu okur
- claim işlemine devam edilip edilemeyeceğine karar verir
- izin varsa bir URL claim eder
- gerekirse robots durumunu yeniler
- acquisition yöntemini seçer
- fetch yapar veya bloklar
- fetch edilmiş kanıtı parse eder
- sonuçları persist eder
- tek bir yapılandırılmış payload döndürür

### `logisticsearch1_1_2_1_storage_routing.py`
### `logisticsearch1_1_2_1_storage_routing.py`

This file does not own the whole crawler storage universe. Its job is narrower and more important: it decides the live processed-output destination policy.

Bu dosya crawler’ın tüm storage evreninin sahibi değildir. Görevi daha dar ama daha önemlidir: canlı işlenmiş-çıktı hedef politikasını belirler.

It answers questions such as:
- is `/srv/data` currently usable?
- if not, is `/srv/buffer` currently usable?
- if `/srv/data` became usable again but buffer backlog still exists, should crawler pause first?
- should ordinary processed writes go to data, buffer, or pause?

Şu sorulara cevap verir:
- `/srv/data` şu anda kullanılabilir mi?
- değilse `/srv/buffer` şu anda kullanılabilir mi?
- `/srv/data` yeniden kullanılabilir hale geldiyse ama buffer backlog hâlâ varsa crawler önce pause olmalı mı?
- normal işlenmiş yazımlar data’ya mı, buffer’a mı gitmeli, yoksa pause mu olunmalı?

Important boundary: raw evidence is not the same thing as processed-output routing. Raw fetch evidence belongs under `/srv/webcrawler/raw_fetch`. Processed output belongs under `/srv/data` or `/srv/buffer` depending on policy.

Önemli sınır: ham kanıt, işlenmiş-çıktı yönlendirmesi ile aynı şey değildir. Ham fetch kanıtı `/srv/webcrawler/raw_fetch` altında bulunur. İşlenmiş çıktı ise politikaya göre `/srv/data` veya `/srv/buffer` altında bulunur.

### `logisticsearch1_1_2_2_acquisition_runtime.py`
### `logisticsearch1_1_2_2_acquisition_runtime.py`

This is the acquisition layer.

Bu dosya acquisition katmanıdır.

Its job is to obtain page or robots material and write first-capture evidence.

Görevi, sayfa veya robots materyalini elde etmek ve ilk-yakalama kanıtını yazmaktır.

In the normal direct path it writes raw fetch or raw robots artefacts into the canonical raw evidence root:
- `/srv/webcrawler/raw_fetch`

Normal direct path içinde ham fetch veya ham robots artefact’larını kanonik ham kanıt köküne yazar:
- `/srv/webcrawler/raw_fetch`

This is the first concrete capture layer. It is not the later export layer.

Bu katman ilk somut yakalama katmanıdır. Daha sonraki export katmanı değildir.

### `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
### `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`

This is the dynamic/browser-backed acquisition leaf.

Bu dosya dinamik/browser destekli acquisition yaprağıdır.

It exists for cases where direct HTTP acquisition is not enough and browser rendering is required to observe useful public content.

Direct HTTP acquisition yeterli olmadığında ve faydalı public içeriği gözlemek için browser rendering gerektiğinde vardır.

This leaf must stay below the general acquisition layer. The general acquisition layer owns the overall fetch decision. The browser dynamic leaf only provides the narrower dynamic-rendered capture path.

Bu yaprak, genel acquisition katmanının altında kalmalıdır. Genel acquisition katmanı, genel fetch kararının sahibidir. Browser dynamic yaprağı ise yalnızca daha dar dinamik-rendered capture yolunu sağlar.

### `logisticsearch1_1_2_3_parse_runtime.py`
### `logisticsearch1_1_2_3_parse_runtime.py`

This is the parse layer.

Bu dosya parse katmanıdır.

It reads the already-captured raw evidence and starts extracting meaning:
- title
- visible text
- discovered links
- minimal parse payload
- taxonomy candidate inputs
- preranking snapshots

Önceden yakalanmış ham kanıtı okur ve anlam çıkarmaya başlar:
- başlık
- görünür metin
- keşfedilen linkler
- minimal parse payload
- taxonomy candidate girdileri
- preranking snapshot’ları

This is the first layer that starts turning raw evidence into structured meaning.

Ham kanıtı yapılandırılmış anlama çevirmeye başlayan ilk katman budur.

### `logisticsearch1_1_2_3_1_taxonomy_runtime.py`
### `logisticsearch1_1_2_3_1_taxonomy_runtime.py`

This is the taxonomy runtime leaf used by parse.

Bu dosya parse tarafından kullanılan taxonomy runtime yaprağıdır.

It does not do final search ranking. It performs the narrow runtime taxonomy lookup used during parse/preranking preparation.

Nihai arama sıralamasını yapmaz. Parse/preranking hazırlığı sırasında kullanılan dar runtime taxonomy lookup işini yapar.

It sits under parse because taxonomy interpretation here is part of later meaning extraction, not the first raw capture.

Parse katmanının altında bulunur; çünkü buradaki taxonomy yorumu, ilk ham yakalamanın değil, sonraki anlam çıkarımının parçasıdır.

### `logisticsearch2_diag_browser_acquisition_smoke.py`
### `logisticsearch2_diag_browser_acquisition_smoke.py`

This is not part of the main runtime trunk.

Bu dosya ana runtime gövdesinin parçası değildir.

It is a diagnostic surface for controlled browser-acquisition smoke checks.

Bu dosya kontrollü browser-acquisition smoke kontrolleri için tanısal bir yüzeydir.

The `2` prefix is intentional here because this is a diagnostic/operator side surface, not the main runtime tree.

Buradaki `2` öneki bilinçlidir; çünkü bu dosya ana runtime ağacının değil, tanısal/operatör tarafı yüzeyinin parçasıdır.

## Real data flow, step by step
## Gerçek veri akışı, adım adım

### Step 1
### Adım 1

`systemd` starts the crawler service by pointing Python module execution at:

`systemd`, crawler servisini Python modül çalıştırmasını şu hedefe yönlendirerek başlatır:

- `lib.logisticsearch1_main_entry`

### Step 2
### Adım 2

`logisticsearch1_main_entry.py` immediately delegates into `logisticsearch1_1_main_loop.py`.

`logisticsearch1_main_entry.py`, işi hemen `logisticsearch1_1_main_loop.py` dosyasına devreder.

### Step 3
### Adım 3

`logisticsearch1_1_main_loop.py` handles loop rhythm and operator/runtime-control concerns. When one worker pass is needed, it calls `logisticsearch1_1_2_worker_runtime.py`.

`logisticsearch1_1_main_loop.py`, loop ritmini ve operatör/runtime-control konularını yönetir. Tek worker geçişi gerektiğinde `logisticsearch1_1_2_worker_runtime.py` dosyasını çağırır.

### Step 4
### Adım 4

`logisticsearch1_1_2_worker_runtime.py` begins one worker pass. Early in that pass it asks:
- what is the current processed-output routing truth?
- may the crawler currently claim work?
- can a URL be claimed?
- does robots need refresh?
- which acquisition method should be used?

`logisticsearch1_1_2_worker_runtime.py`, tek worker geçişini başlatır. Bu geçişin başında şunları sorar:
- güncel işlenmiş-çıktı yönlendirme doğrusu nedir?
- crawler şu anda iş claim edebilir mi?
- bir URL claim edilebilir mi?
- robots yenilenmeli mi?
- hangi acquisition yöntemi kullanılmalı?

It gets durable DB truth through `logisticsearch1_1_1_state_db_gateway.py`.

Kalıcı DB doğrusunu `logisticsearch1_1_1_state_db_gateway.py` üzerinden alır.

### Step 5
### Adım 5

When fetch is actually allowed, the worker calls `logisticsearch1_1_2_2_acquisition_runtime.py`.

Fetch’e gerçekten izin verildiğinde worker, `logisticsearch1_1_2_2_acquisition_runtime.py` dosyasını çağırır.

If a dynamic-rendered path is required, that acquisition layer calls:
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`

Dinamik-rendered yol gerekiyorsa acquisition katmanı şunu çağırır:
- `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`

### Step 6
### Adım 6

The acquisition layer writes first-capture evidence under:
- `/srv/webcrawler/raw_fetch`

Acquisition katmanı ilk-yakalama kanıtını şuraya yazar:
- `/srv/webcrawler/raw_fetch`

This is where raw HTML body, robots capture, rendered HTML, screenshots, and similar first evidence belong.

Ham HTML body, robots yakalaması, rendered HTML, screenshot ve benzeri ilk kanıtlar burada bulunur.

### Step 7
### Adım 7

After fetch evidence exists, `logisticsearch1_1_2_3_parse_runtime.py` reads that raw evidence and extracts structured meaning.

Fetch kanıtı oluştuktan sonra `logisticsearch1_1_2_3_parse_runtime.py` bu ham kanıtı okur ve yapılandırılmış anlam çıkarır.

This includes:
- text extraction
- title extraction
- discovered-link extraction
- minimal parse payload
- taxonomy candidate preparation

Buna şunlar dahildir:
- metin çıkarımı
- başlık çıkarımı
- keşfedilen link çıkarımı
- minimal parse payload
- taxonomy candidate hazırlığı

### Step 8
### Adım 8

For taxonomy-assisted interpretation, parse calls:
- `logisticsearch1_1_2_3_1_taxonomy_runtime.py`

Taxonomy destekli yorum için parse şu dosyayı çağırır:
- `logisticsearch1_1_2_3_1_taxonomy_runtime.py`

This returns runtime taxonomy matches used for later parse/preranking persistence.

Bu dosya, sonraki parse/preranking persistence işlemlerinde kullanılacak runtime taxonomy eşleşmelerini döndürür.

### Step 9
### Adım 9

Parse and worker then persist outcomes through `logisticsearch1_1_1_state_db_gateway.py`.

Parse ve worker daha sonra sonuçları `logisticsearch1_1_1_state_db_gateway.py` üzerinden persist eder.

This includes:
- workflow status updates
- discovery enqueue actions
- fetch finish transitions
- taxonomy preranking persistence
- page preranking snapshots

Buna şunlar dahildir:
- workflow status güncellemeleri
- discovery enqueue işlemleri
- fetch finish transition’ları
- taxonomy preranking persistence
- page preranking snapshot’ları

### Step 10
### Adım 10

Processed output routing is a separate decision from raw evidence capture.

İşlenmiş-çıktı yönlendirmesi, ham kanıt yakalamadan ayrı bir karardır.

The processed-output target is:
- `/srv/data` when primary processed storage is usable
- `/srv/buffer` when primary processed storage is not usable but fallback is usable

İşlenmiş-çıktı hedefi şudur:
- birincil işlenmiş depolama kullanılabiliyorsa `/srv/data`
- birincil işlenmiş depolama kullanılamıyorsa ama fallback kullanılabiliyorsa `/srv/buffer`

If `/srv/data` becomes usable again while buffered backlog still exists, crawler should pause until the backlog is drained.

`/srv/data` yeniden kullanılabilir hale geldiğinde ama buffered backlog hâlâ varsa, crawler backlog boşaltılana kadar pause olmalıdır.

### Step 11
### Adım 11

`/srv/webcrawler/exports` is not the first destination of every fetch.

`/srv/webcrawler/exports`, her fetch’in ilk hedefi değildir.

It is the later controlled export / handoff boundary used for material that is ready to be packaged or handed off in a controlled way.

Bu dizin, kontrollü şekilde paketlenmeye veya devredilmeye hazır materyal için kullanılan daha sonraki kontrollü export / handoff sınırıdır.

## The most important correction
## En önemli düzeltme

The live crawler is **not** a simple linear pipe of:

Canlı crawler **şu şekilde basit doğrusal bir boru hattı değildir**:

`raw_fetch -> exports -> data/buffer`

The correct mental model is:

Doğru zihinsel model şudur:

1. control and claim truth come from DB  
2. acquisition writes first raw evidence into `/srv/webcrawler/raw_fetch`  
3. parse reads raw evidence and produces structured meaning  
4. processed output routing decides `/srv/data` versus `/srv/buffer`  
5. later selected material may cross the controlled export boundary at `/srv/webcrawler/exports`

1. kontrol ve claim doğrusu DB’den gelir  
2. acquisition, ilk ham kanıtı `/srv/webcrawler/raw_fetch` içine yazar  
3. parse, ham kanıtı okuyup yapılandırılmış anlam üretir  
4. işlenmiş çıktı yönlendirmesi `/srv/data` ile `/srv/buffer` arasında karar verir  
5. daha sonra seçilmiş materyal kontrollü export sınırı olan `/srv/webcrawler/exports` dizinine geçebilir

## Directory boundary truth
## Dizin sınırı doğrusu

### `/srv/webcrawler/raw_fetch/`
### `/srv/webcrawler/raw_fetch/`

This is the canonical raw evidence root.

Burası kanonik ham kanıt köküdür.

### `/srv/data/`
### `/srv/data/`

This is the preferred durable processed-output root.

Burası tercih edilen kalıcı işlenmiş-çıktı köküdür.

### `/srv/buffer/`
### `/srv/buffer/`

This is the fallback processed-output root used only when policy requires fallback or controlled draining.

Burası yalnızca politika fallback gerektirdiğinde veya kontrollü drain gerektiğinde kullanılan fallback işlenmiş-çıktı köküdür.

### `/srv/webcrawler/exports/`
### `/srv/webcrawler/exports/`

This is the controlled export / handoff boundary.

Burası kontrollü export / handoff sınırıdır.

It should hold later-stage, already-selected, operator-meaningful material rather than blind first raw evidence.

İlk kör ham kanıt yerine, daha sonraki aşamaya ait, zaten seçilmiş, operatör açısından anlamlı materyali taşımalıdır.

## Dynamic internet content
## Dinamik internet içeriği

Dynamic public content belongs to the acquisition branch, but specifically to the browser dynamic leaf below the general acquisition layer.

Dinamik public içerik acquisition dalına aittir; ama daha özel olarak, genel acquisition katmanının altındaki browser dynamic yaprağına aittir.

That means:
- dynamic content is still part of acquisition
- it is not a separate second trunk
- it is not parse
- it is not export
- it is not final ranking

Bu şu anlama gelir:
- dinamik içerik hâlâ acquisition’ın parçasıdır
- ayrı ikinci bir gövde değildir
- parse değildir
- export değildir
- nihai ranking değildir

## Mandatory code comment discipline
## Zorunlu kod yorum disiplini

For crawler/webcrawler Python and SQL surfaces, the mandatory rule is:

Crawler/webcrawler Python ve SQL yüzeyleri için zorunlu kural şudur:

Every relevant line, variable, parameter, function, library usage, and important block must be explained immediately above the code with very detailed bilingual comments in English and Turkish, written for a first-time learner.

İlgili her satır, değişken, parametre, fonksiyon, kütüphane kullanımı ve önemli blok; kodun hemen üstünde, ilk kez öğrenen birine göre yazılmış çok detaylı İngilizce ve Türkçe açıklama yorumlarıyla anlatılmalıdır.

This rule is not optional for future crawler/webcrawler code hardening.

Bu kural, gelecekteki crawler/webcrawler code hardening çalışmaları için isteğe bağlı değildir.

## Operational reading order
## Operasyonel okuma sırası

Read in this order:

Şu sırayla oku:

1. `docs/TOPIC_WEBCRAWLER_RUNTIME_LAYOUT_AND_NAMING_STANDARD.md`
2. `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`
3. `docs/TOPIC_WEBCRAWLER_RAW_FETCH_PARSE_TAXONOMY_AND_SELECTION_BOUNDARY.md`
4. `docs/SECTION1_WEBCRAWLER_DIRECTORIES_FILES_MAP.md`
5. `hosts/makpi51crawler/python/webcrawler/README.md`
6. `hosts/makpi51crawler/python/webcrawler/lib/README.md`

