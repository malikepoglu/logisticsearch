# Section1: Webcrawler Controls

## EN

### Purpose

This document defines the canonical public control surface and the canonical internal runtime-control truth for the Pi51crawler webcrawler system.

This document is a control-surface contract. It defines which public operator commands must exist, which public operator commands must not exist, and how those public commands relate to the smaller and clearer operational model.

This document is not a migration runbook. It does not authorize blind deletion, blind rename, or blind replacement of live runtime surfaces.

### Canonical Public Operator Control Surface

The canonical public operator control surface must be limited to exactly these wrappers:

- `/logisticsearch/webcrawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/rebootwc.py`

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

- `/logisticsearch/webcrawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/webcrawler/python_live_runtime/controls/rebootwc.py`

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
## Runtime-ağacı kontrol okuma yolu

When you need to understand which file owns root entry, main loop, worker orchestration, DB truth, acquisition, dynamic browser acquisition, parse, and taxonomy roles, read `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md` before making control-surface changes.

Hangi dosyanın root entry, main loop, worker orchestration, DB doğrusu, acquisition, dinamik browser acquisition, parse ve taxonomy rollerine sahip olduğunu anlaman gerektiğinde, control-surface değişikliği yapmadan önce `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md` dokümanını oku.
