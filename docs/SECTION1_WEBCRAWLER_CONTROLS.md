# Section1: Webcrawler Controls

## EN

### Purpose

This document defines the canonical public control surface and the canonical internal runtime-control truth for the Pi51crawler webcrawler system.

This document is a control-surface contract. It defines which public operator commands must exist, which public operator commands must not exist, and how those public commands relate to the smaller and clearer operational model.

This document is not a migration runbook. It does not authorize blind deletion, blind rename, or blind replacement of live runtime surfaces.

### Canonical Public Operator Control Surface

The canonical public operator control surface must be limited to exactly these wrappers:

- `/logisticsearch/makpi51crawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/rebootwc.py`

No additional public wrapper should be treated as canonical unless a later controlled documentation decision explicitly changes this contract.

### Public Command Meanings

#### `playwc`

`playwc` is the canonical public command that puts the crawler into active running mode.

`playwc` is used both for:

- first start
- resume-after-pause

Because of this dual role, `playwc` replaces the need for a separate public `resumewc` wrapper.

#### `pausewc`

`pausewc` is the canonical public command that pauses active crawling while preserving durable crawler position and progress truth.

`pausewc` is non-destructive with respect to crawler progress. It must not mean “forget position and restart from scratch.”

#### `resetwc`

`resetwc` is the canonical public controlled reset surface.

`resetwc` is not the same thing as pause. Its role is stronger and more deliberate. A controlled reset may internally use stop truth before reset logic is executed.

#### `poweroffwc`

`poweroffwc` is the canonical public crawler-aware poweroff surface.

It exists so crawler shutdown semantics can be kept explicit and controlled before system poweroff behavior is performed.

#### `rebootwc`

`rebootwc` is the canonical public crawler-aware reboot surface.

It exists so crawler shutdown semantics can be kept explicit and controlled before system reboot behavior is performed.

### Public Wrapper Names That Must Not Exist

The following names must not exist as canonical public operator wrappers:

- `stopwc`
- `resumewc`

#### Why `stopwc` must not exist as a public wrapper

`stopwc` must not exist as a public operator wrapper.

The reason is semantic clarity. The public operator need here is not a destructive stop that sounds like “terminate and forget.” The public operator need is a pause-and-preserve behavior, and that behavior must be named `pausewc`.

Internal runtime truth may still use `stop` for stricter machine-oriented service and state handling, but that does not justify exposing `stopwc` as part of the canonical public wrapper surface.

#### Why `resumewc` must not exist as a public wrapper

`resumewc` must not exist as a public operator wrapper.

The reason is surface minimization. `playwc` already covers both first start and resume-after-pause behavior. A second public wrapper for the same visible operator intention would enlarge the surface without improving clarity.

### Canonical Internal Runtime-Control Truth

The canonical internal runtime-control truth may still use these internal states:

- `run`
- `pause`
- `stop`

This is acceptable because internal machine-oriented truth and public operator surface do not need to be identical.

The canonical design rule is:

- internal truth may be slightly richer
- public operator surface must remain smaller and clearer

### Binding Rule Between Public Commands and Internal Truth

The intended public-to-internal binding is:

- `playwc` -> internal durable state `run`
- `pausewc` -> internal durable state `pause`
- `resetwc` -> controlled reset path, which may first force internal durable state `stop`
- `poweroffwc` -> controlled shutdown path, which may first force internal durable state `stop`
- `rebootwc` -> controlled reboot path, which may first force internal durable state `stop`

### Simplicity Rule

The control model must remain intentionally small.

The canonical public operator surface must stay focused on these five commands:

- `playwc`
- `pausewc`
- `resetwc`
- `poweroffwc`
- `rebootwc`

This smaller surface is preferred because it improves operator clarity and long-term manageability.

---

## TR

### Amaç

Bu doküman, Pi51crawler webcrawler sistemi için kanonik açık kontrol yüzeyini ve kanonik iç runtime-control doğrusunu tanımlar.

Bu doküman bir kontrol-yüzeyi sözleşmesidir. Hangi açık operatör komutlarının var olması gerektiğini, hangi açık operatör komutlarının var olmaması gerektiğini ve bu açık komutların daha küçük ve daha anlaşılır operasyon modeline nasıl bağlandığını tanımlar.

Bu doküman bir geçiş runbook'u değildir. Canlı runtime yüzeylerinde kör silme, kör yeniden adlandırma veya kör değiştirme yetkisi vermez.

### Kanonik Açık Operatör Kontrol Yüzeyi

Kanonik açık operatör kontrol yüzeyi tam olarak şu sarmalayıcılarla sınırlı kalmalıdır:

- `/logisticsearch/makpi51crawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/rebootwc.py`

Daha sonra kontrollü bir dokümantasyon kararı bu sözleşmeyi açıkça değiştirmedikçe, başka hiçbir açık sarmalayıcı kanonik kabul edilmemelidir.

### Açık Komut Anlamları

#### `playwc`

`playwc`, crawler'ı aktif çalışma moduna alan kanonik açık komuttur.

`playwc` şu iki görünür operatör ihtiyacı için birlikte kullanılır:

- ilk başlatma
- pause sonrasında devam etme

Bu çift rol nedeniyle `playwc`, ayrı bir açık `resumewc` sarmalayıcısına duyulan ihtiyacın yerine geçer.

#### `pausewc`

`pausewc`, aktif crawl işlemini duraksatan ama kalıcı crawler konumunu ve ilerleme doğrusunu koruyan kanonik açık komuttur.

`pausewc`, crawler ilerlemesi açısından yıkıcı değildir. “Konumu unut ve baştan başla” anlamına gelmemelidir.

#### `resetwc`

`resetwc`, kanonik açık kontrollü reset yüzeyidir.

`resetwc`, pause ile aynı şey değildir. Rolü daha güçlü ve daha bilinçlidir. Kontrollü bir reset yolu, gerçek reset mantığı çalıştırılmadan önce içte stop doğrusunu kullanabilir.

#### `poweroffwc`

`poweroffwc`, kanonik açık crawler-farkındalıklı poweroff yüzeyidir.

Sistem poweroff davranışı uygulanmadan önce crawler kapatma semantiği açık ve kontrollü tutulabilsin diye vardır.

#### `rebootwc`

`rebootwc`, kanonik açık crawler-farkındalıklı reboot yüzeyidir.

Sistem reboot davranışı uygulanmadan önce crawler kapatma semantiği açık ve kontrollü tutulabilsin diye vardır.

### Var Olmaması Gereken Açık Wrapper İsimleri

Aşağıdaki isimler kanonik açık operatör sarmalayıcısı olarak var olmamalıdır:

- `stopwc`
- `resumewc`

#### `stopwc` neden açık wrapper olarak var olmamalıdır

`stopwc` açık operatör sarmalayıcısı olarak bulunmamalıdır.

Sebep anlamsal açıklıktır. Buradaki açık operatör ihtiyacı, “durdur ve unut” gibi duyulan yıkıcı bir stop değildir. Açık operatör ihtiyacı, duraksat-ve-koru davranışıdır ve bu davranışın adı `pausewc` olmalıdır.

İç runtime doğrusu daha katı makine odaklı servis ve durum yönetimi için yine `stop` kullanabilir; ancak bu, `stopwc` adının kanonik açık wrapper yüzeyine taşınmasını haklı kılmaz.

#### `resumewc` neden açık wrapper olarak var olmamalıdır

`resumewc` açık operatör sarmalayıcısı olarak bulunmamalıdır.

Sebep yüzey küçültmedir. `playwc`, hem ilk başlatma hem de pause sonrası devam davranışını zaten kapsar. Aynı görünür operatör niyeti için ikinci bir açık wrapper, açıklığı artırmadan yüzeyi büyütür.

### Kanonik İç Runtime-Control Doğrusu

Kanonik iç runtime-control doğrusu yine şu iç durumları kullanabilir:

- `run`
- `pause`
- `stop`

Bu kabul edilebilir; çünkü iç makine odaklı doğruluk ile açık operatör yüzeyi bire bir aynı olmak zorunda değildir.

Kanonik tasarım kuralı şudur:

- iç doğruluk biraz daha zengin olabilir
- açık operatör yüzeyi daha küçük ve daha açık kalmalıdır

### Açık Komutlar ile İç Doğruluk Arasındaki Bağlama Kuralı

Hedeflenen açık-yüzeyden iç-doğruluğa bağlama şu şekildedir:

- `playwc` -> iç kalıcı durum `run`
- `pausewc` -> iç kalıcı durum `pause`
- `resetwc` -> kontrollü reset yolu; önce iç kalıcı durumu `stop` yapabilir
- `poweroffwc` -> kontrollü kapanış yolu; önce iç kalıcı durumu `stop` yapabilir
- `rebootwc` -> kontrollü yeniden başlatma yolu; önce iç kalıcı durumu `stop` yapabilir

### Yalınlık Kuralı

Kontrol modeli bilinçli olarak küçük kalmalıdır.

Kanonik açık operatör yüzeyi şu beş komuta odaklı kalmalıdır:

- `playwc`
- `pausewc`
- `resetwc`
- `poweroffwc`
- `rebootwc`

Bu daha küçük yüzey tercih edilir; çünkü operatör açıklığını ve uzun vadeli yönetilebilirliği artırır.

## Runtime-tree control reading path

### EN

Before any future change to the public crawler-control surface, the runtime tree must be read first.

This document defines the public operator control surface. It does not, by itself, prove which Python file owns startup, loop execution, worker orchestration, durable state, database truth, acquisition, parsing, taxonomy lookup, or shutdown behavior.

The mandatory companion document for that ownership map is:

- `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`

Use the runtime-tree map to identify the current owner of each runtime responsibility:

- root entry and package-context invocation,
- main loop and loop boundary behavior,
- worker orchestration and phase ordering,
- durable crawler-control state,
- database gateway and durable DB truth,
- static/public HTTP acquisition,
- dynamic browser acquisition,
- raw-fetch to parse boundary,
- taxonomy lookup and taxonomy authority boundary,
- crawler output and processed-data routing boundaries.

The safe reading order is:

1. Read this controls document to understand the allowed public operator commands.
2. Read the runtime-tree and data-flow map to understand which runtime file owns each execution role.
3. Read the controls run-policy classification document before running, testing, or changing any control script.
4. Only after those checks should a patch touch control wrappers, runtime entrypoints, worker loop behavior, or systemd-facing launch behavior.

The important boundary is simple:

- control wrappers express operator intent;
- runtime-tree files own execution behavior;
- database/runtime state stores durable truth;
- documentation or inventory audits must not execute control scripts
For the operator-run safety classification of each control script, read `docs/TOPIC_CONTROLS_RUN_POLICY_AND_SAFETY_CLASSIFICATION_2026_05_06.md` together with this document. That policy document is the canonical source for A0/B1/C2/D3/E4/F5 run classes and for the `NO_CONTROL_SCRIPT_EXECUTION` audit rule.
.

Do not infer runtime ownership from wrapper names alone. A wrapper name may be public and operator-friendly, while the real state transition, loop behavior, lease handling, or shutdown behavior is owned by another runtime module.

### TR

Açık crawler kontrol yüzeyinde gelecekte yapılacak her değişiklikten önce runtime ağacı okunmalıdır.

Bu doküman açık operatör kontrol yüzeyini tanımlar. Tek başına hangi Python dosyasının başlangıç, döngü çalışması, worker orkestrasyonu, kalıcı durum, veritabanı doğrusu, acquisition, parse, taxonomy lookup veya kapanış davranışını sahiplendiğini kanıtlamaz.

Bu sahiplik haritası için zorunlu yardımcı doküman şudur:

- `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`

Runtime-tree haritası şu runtime sorumluluklarının güncel sahibini bulmak için okunmalıdır:

- root entry ve package-context invocation,
- main loop ve döngü sınırı davranışı,
- worker orkestrasyonu ve phase sırası,
- kalıcı crawler-control state,
- database gateway ve kalıcı DB doğrusu,
- statik/açık HTTP acquisition,
- dinamik browser acquisition,
- raw-fetch ile parse arasındaki sınır,
- taxonomy lookup ve taxonomy authority sınırı,
- crawler çıktısı ve processed-data routing sınırları.

Güvenli okuma sırası şudur:

1. İzin verilen açık operatör komutlarını anlamak için önce bu controls dokümanını oku.
2. Her runtime rolünün hangi dosyaya ait olduğunu anlamak için runtime-tree ve data-flow map dokümanını oku.
3. Herhangi bir control script çalıştırmadan, test etmeden veya değiştirmeden önce controls run-policy classification dokümanını oku.
4. Ancak bu kontrollerden sonra control wrapper, runtime entrypoint, worker loop davranışı veya systemd-facing launch davranışı patch kapsamına alınabilir.

Önemli sınır yalındır:

- control wrapper'lar operatör niyetini ifade eder;
- runtime-tree dosyaları execution davranışını sahiplenir;
- database/runtime state kalıcı doğruyu tutar;
- dokümantasyon veya envanter audit adımları control script çalıştırmamalıdır
Her control script için operatör çalıştırma güvenlik sınıfını anlamak gerektiğinde, bu doküman `docs/TOPIC_CONTROLS_RUN_POLICY_AND_SAFETY_CLASSIFICATION_2026_05_06.md` ile birlikte okunmalıdır. O policy dokümanı A0/B1/C2/D3/E4/F5 run sınıfları ve `NO_CONTROL_SCRIPT_EXECUTION` audit kuralı için kanonik kaynaktır.
.

Runtime sahipliği yalnızca wrapper isimlerinden çıkarılmamalıdır. Bir wrapper adı açık ve operatör-dostu olabilir; fakat gerçek state transition, loop davranışı, lease handling veya shutdown davranışı başka bir runtime modülüne ait olabilir.
