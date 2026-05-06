# SECTION1_WEBCRAWLER_RUNTIME_TOPOLOGY_AND_NAMING_LOCK

## Purpose
## Amaç

This document freezes the corrected runtime topology and naming decision for the Pi51 webcrawler runtime tree.

Bu doküman, Pi51 webcrawler runtime ağacı için düzeltilmiş runtime topoloji ve isimlendirme kararını kilitler.

The previous draft mixed two different concepts:

Önceki taslak iki farklı kavramı birbirine karıştırıyordu:

1. hierarchical target numbering
2. temporary engineering/test order

1. hiyerarşik hedef numaralandırma
2. geçici mühendislik/test sırası

From this point onward, these two concepts must stay separate.

Bu noktadan sonra bu iki kavram birbirinden ayrı tutulmalıdır.

## Core rule
## Temel kural

We now separate three things very strictly:

Artık üç şeyi çok katı biçimde ayırıyoruz:

1. current physical file identity
2. future target rename topology
3. current controlled test order

1. mevcut fiziksel dosya kimliği
2. gelecekteki hedef rename topolojisi
3. mevcut kontrollü test sırası

## Important restriction
## Önemli kısıt

At the current crawler_core bring-up stage, we do **not** perform broad repo-wide rename work.

Mevcut crawler_core ayağa kaldırma aşamasında repo genelinde **toplu rename** yapmıyoruz.

However, this does **not** mean naming will stay this way forever.

Ancak bu, isimlendirmenin sonsuza kadar böyle kalacağı anlamına **gelmez**.

The correct model is:

Doğru model şudur:

- freeze the target topology now,
- keep current files operational for the moment,
- later apply controlled rename step by step,
- after each rename, re-test imports, contracts, and live runtime truth.

- hedef topolojiyi şimdi kilitle,
- mevcut dosyaları şimdilik çalışır halde tut,
- daha sonra controlled rename işlemini adım adım uygula,
- her rename sonrası import, sözleşme ve canlı runtime doğrularını yeniden test et.

## Stable top of tree
## Ağacın stabil üst kısmı

### Level 1
### Seviye 1

- `1` → `logisticsearch1_main_entry.py`
- thin root runtime entry surface

- `1` → `logisticsearch1_main_entry.py`
- ince kök runtime giriş yüzeyi

### Level 1.1
### Seviye 1.1

- `1.1` → `logisticsearch1_1_main_loop.py`
- loop / operator / CLI orchestration surface

- `1.1` → `logisticsearch1_1_main_loop.py`
- loop / operatör / CLI orchestration yüzeyi

### Level 1.1.1
### Seviye 1.1.1

- `1.1.1` → `logisticsearch1_1_1_state_db_gateway.py`
- thin DB gateway family hub / re-export surface

- `1.1.1` → `logisticsearch1_1_1_state_db_gateway.py`
- ince DB gateway family hub / re-export yüzeyi

#### Current stable 1.1.1 child topology
#### Mevcut stabil 1.1.1 alt topolojisi

- `1.1.1.1` → `logisticsearch1_1_1_1_gateway_support.py`
- `1.1.1.2` → `logisticsearch1_1_1_2_runtime_control_gateway.py`
- `1.1.1.3` → `logisticsearch1_1_1_3_frontier_gateway.py`
- `1.1.1.4` → `logisticsearch1_1_1_4_robots_gateway.py`
- `1.1.1.5` → `logisticsearch1_1_1_5_fetch_attempt_gateway.py`
- `1.1.1.6` → `logisticsearch1_1_1_6_preranking_gateway.py`
- `1.1.1.7` → `logisticsearch1_1_1_7_discovery_gateway.py`

## Corrected target topology for the 1.1.2 family
## 1.1.2 ailesi için düzeltilmiş hedef topoloji

### Stable parent
### Stabil ebeveyn

- `1.1.2` → `logisticsearch1_1_2_worker_runtime.py`
- worker runtime family hub

- `1.1.2` → `logisticsearch1_1_2_worker_runtime.py`
- worker runtime family hub yüzeyi

### Correct future target numbering
### Doğru gelecek hedef numaralandırma

This is the corrected **future target topology** for the worker family.

Bu, worker ailesi için düzeltilmiş **gelecek hedef topolojisidir**.

- `1.1.2.1` → `logisticsearch1_1_2_1_worker_runtime_support.py`
- `1.1.2.2` → `logisticsearch1_1_2_2_worker_lease_runtime.py`
- `1.1.2.3` → `logisticsearch1_1_2_3_worker_robots_runtime.py`
- `1.1.2.4` → `logisticsearch1_1_2_4_acquisition_runtime.py`
- `1.1.2.4.1` → `logisticsearch1_1_2_4_1_acquisition_support.py`
- `1.1.2.4.2` → `logisticsearch1_1_2_4_2_http_page_acquisition_runtime.py`
- `1.1.2.4.3` → `logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime.py`
- `1.1.2.4.4` → `logisticsearch1_1_2_4_4_browser_page_acquisition_runtime.py`
- `1.1.2.4.5` → `logisticsearch1_1_2_4_5_robots_txt_acquisition_runtime.py`
- `1.1.2.5` → `logisticsearch1_1_2_5_fetch_finalize_runtime.py`
- `1.1.2.6` → `logisticsearch1_1_2_6_parse_runtime.py`
- `1.1.2.6.1` → `logisticsearch1_1_2_6_1_taxonomy_runtime.py`
- `1.1.2.7` → `logisticsearch1_1_2_7_storage_routing.py`

### Why this corrected target topology is better
### Bu düzeltilmiş hedef topoloji neden daha iyi

The corrected target topology is better because:

Bu düzeltilmiş hedef topoloji daha iyidir; çünkü:

- the parent `1.1.2` stays above all children,
- child numbering is now left-to-right hierarchical,
- support / lease / robots appear before the broader acquisition family,
- acquisition keeps its own subtree,
- finalize stays after acquisition,
- parse stays after acquisition/finalize,
- storage routing stays late because it is an output-side policy surface.

- ebeveyn `1.1.2` tüm çocukların üstünde kalır,
- alt numaralandırma artık soldan sağa hiyerarşiktir,
- support / lease / robots, daha geniş acquisition ailesinden önce gelir,
- acquisition kendi alt ağacını korur,
- finalize acquisition’dan sonra kalır,
- parse acquisition/finalize sonrasında kalır,
- storage routing çıktı tarafı politika yüzeyi olduğu için sonda kalır.

## Current physical files versus future target names
## Mevcut fiziksel dosyalar ile gelecekteki hedef isimler

At this moment, current repository files still use historical names.

Bu anda repository içindeki dosyalar hâlâ tarihsel isimleri kullanmaktadır.

The planned controlled rename mapping is:

Planlanan controlled rename eşlemesi şudur:

- current `logisticsearch1_1_2_4_worker_runtime_support.py`
  → future `logisticsearch1_1_2_1_worker_runtime_support.py`

- current `logisticsearch1_1_2_7_worker_lease_runtime.py`
  → future `logisticsearch1_1_2_2_worker_lease_runtime.py`

- current `logisticsearch1_1_2_6_worker_robots_runtime.py`
  → future `logisticsearch1_1_2_3_worker_robots_runtime.py`

- current `logisticsearch1_1_2_2_acquisition_runtime.py`
  → future `logisticsearch1_1_2_4_acquisition_runtime.py`

- current `logisticsearch1_1_2_2_2_acquisition_support.py`
  → future `logisticsearch1_1_2_4_1_acquisition_support.py`

- current `logisticsearch1_1_2_2_3_http_page_acquisition_runtime.py`
  → future `logisticsearch1_1_2_4_2_http_page_acquisition_runtime.py`

- current `logisticsearch1_1_2_2_1_browser_dynamic_acquisition_runtime.py`
  → future `logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime.py`

- current `logisticsearch1_1_2_2_5_browser_page_acquisition_runtime.py`
  → future `logisticsearch1_1_2_4_4_browser_page_acquisition_runtime.py`

- current `logisticsearch1_1_2_2_4_robots_txt_acquisition_runtime.py`
  → future `logisticsearch1_1_2_4_5_robots_txt_acquisition_runtime.py`

- current `logisticsearch1_1_2_5_fetch_finalize_runtime.py`
  → future `logisticsearch1_1_2_5_fetch_finalize_runtime.py`

- current `logisticsearch1_1_2_3_parse_runtime.py`
  → future `logisticsearch1_1_2_6_parse_runtime.py`

- current `logisticsearch1_1_2_3_1_taxonomy_runtime.py`
  → future `logisticsearch1_1_2_6_1_taxonomy_runtime.py`

- current `logisticsearch1_1_2_1_storage_routing.py`
  → future `logisticsearch1_1_2_7_storage_routing.py`

## Current controlled test order
## Mevcut kontrollü test sırası

The current controlled test order is a temporary engineering order, not the canonical future numbering.

Mevcut kontrollü test sırası, kanonik gelecek numaralandırma değil; geçici mühendislik sırasıdır.

The current practical order is:

Mevcut pratik sıra şudur:

1. verify/support root surfaces
2. verify gateway family
3. verify worker family children one by one
4. verify worker parent again
5. verify main loop again
6. verify root entry again
7. only then consider controlled rename work

1. support/kök yüzeylerini doğrula
2. gateway ailesini doğrula
3. worker ailesi çocuklarını tek tek doğrula
4. sonra worker ebeveynini yeniden doğrula
5. sonra main loop’u yeniden doğrula
6. sonra root entry’yi yeniden doğrula
7. ancak ondan sonra controlled rename işini düşün

## Controlled rename discipline
## Controlled rename disiplini

When controlled rename begins later, the discipline must be:

Controlled rename daha sonra başladığında disiplin şu olmalıdır:

1. rename only one surface or one tightly related mini-family at a time
2. repair imports immediately
3. run syntax + import + isolated function tests immediately
4. commit and push immediately if the step is clean
5. fast-forward pi51 repo mirror
6. controlled sync repo → live runtime
7. live retest immediately

1. aynı anda yalnızca tek yüzeyi veya tek küçük ilişkili aileyi rename et
2. import bağlarını hemen onar
3. syntax + import + isolated function testlerini hemen çalıştır
4. adım temizse hemen commit ve push et
5. pi51 repo mirror’u fast-forward et
6. repo → live runtime kontrollü senkron yap
7. canlı tarafta hemen yeniden test et

## Runtime start truth
## Runtime başlangıç doğrusu

The canonical live runtime entry module is:

Kanonik canlı runtime giriş modülü şudur:

- `webcrawler.lib.logisticsearch1_main_entry`

This import string is not a permanent system setting by itself.

Bu import metni tek başına kalıcı bir sistem ayarı değildir.

The current permanent live-start truth is written in the live launcher file:

Mevcut kalıcı canlı başlatma doğrusu artık emekli edilmiş bir `bin/start_webcrawler_runtime.sh` launcher dosyası değildir.

Güncel runtime invocation doğrusu şu sözleşme ile okunmalıdır:

- `docs/TOPIC_CRAWLER_CORE_ENTRYPOINT_INVOCATION_CONTRACT_2026_05_05.md`

Güncel operational sınır:

- Canonical live runtime root: `/logisticsearch/makpi51crawler`
- Package-context entrypoint: `python_live_runtime.logisticsearch1_main_entry`
- Documentation, inventory, topology, and path-audit work must not start the crawler.
- Documentation, inventory, topology, and path-audit work must not execute control scripts.

## Current focus
## Mevcut odak

Current priority remains:

Mevcut öncelik hâlâ şudur:

- bring up `webcrawler`,
- bring up `crawler_core`,
- keep the runtime tree stable,
- test every surface with strict discipline,
- delay controlled rename until the runtime behavior is trustworthy enough.

- `webcrawler`’ı ayağa kaldırmak,
- `crawler_core`’u ayağa kaldırmak,
- runtime ağacını stabil tutmak,
- her yüzeyi çok katı disiplinle test etmek,
- runtime davranışı yeterince güvenilir hale gelene kadar controlled rename’i ertelemek.

