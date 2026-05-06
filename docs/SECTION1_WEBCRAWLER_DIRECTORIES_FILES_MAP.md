# Section1: Webcrawler Directories Files Map

## EN

### Purpose

This document defines the canonical directories-and-files map for the Pi51crawler webcrawler surface.

This document is a layout and boundary contract. It defines where data lives, where runtime code lives, where controls live, where configuration lives, and where the tracked repository lives.

This document is not a runbook. It does not authorize blind moves, deletes, or symlink shortcuts. Any migration from old paths to these canonical paths must be performed in controlled steps with explicit verification.

### Hard Rules

1. Public crawler data must live under `/srv/`.
2. Canonical runtime code must live under `/logisticsearch/makpi51crawler/`.
3. Canonical tracked repository must live under `/logisticsearch/repo/`.
4. Public operator control wrappers must be limited to the small fixed surface defined in this document.
5. `stopwc` must not exist as a public operator wrapper.
6. `resumewc` must not exist as a public operator wrapper.
7. `playwc` is the public command for both first start and resume-after-pause behavior.
8. `pausewc` must preserve durable crawler position and progress truth rather than forgetting where the crawler was.
9. Internal runtime-control truth may still use `run`, `pause`, and `stop` inside the database and service logic, but the public operator surface must remain smaller and clearer.
10. Old long paths and mixed surfaces must be retired only through controlled migration steps. They must not be treated as the long-term canonical layout.

### Canonical Data Surface

All crawler data paths must live under `/srv/`.

The canonical data paths are:

- `/srv/webcrawler/raw_fetch/`
- `/srv/data/`
- `/srv/buffer/`
- `/srv/webcrawler/exports/`

The meaning of these paths is fixed:

- `/srv/webcrawler/raw_fetch/` stores raw fetched body artefacts.
- `/srv/data/` stores processed output chosen for the durable processed-data surface.
- `/srv/buffer/` stores temporary processed-output buffering when routing policy requires it.
- `/srv/webcrawler/exports/` stores crawler export artefacts.

No runtime code should be treated as canonical under `/srv/`. `/srv/` is the canonical data surface, not the canonical runtime-code surface.

### Canonical Runtime Code Surface

Canonical runtime code must live under:

- `/logisticsearch/makpi51crawler/`
- `/logisticsearch/makpi51crawler/python_live_runtime/`
- `/logisticsearch/makpi51crawler/.venv/`

The meaning of these paths is fixed:

- `/logisticsearch/makpi51crawler/` is the canonical runtime root.
- `/logisticsearch/makpi51crawler/python_live_runtime/` stores the runtime Python module surface used by the live crawler runtime.
- `/logisticsearch/makpi51crawler/.venv/` stores the canonical Python virtual environment for this runtime surface.

The `.venv` directory is the isolated Python package environment for the canonical webcrawler runtime. It is part of the runtime execution surface, not the tracked repository source surface.

### Canonical Config Surface

Canonical runtime configuration must live under:

- `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`

This file is the canonical runtime environment file for the live webcrawler surface.

Secret-bearing values must still be handled carefully and intentionally. This document only defines the canonical location.

### Canonical Controls Surface

Public operator control wrappers must live under:

- `/logisticsearch/makpi51crawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/rebootwc.py`

The public meanings are:

- `playwc` sets the crawler into active running mode and is also the public resume command after pause.
- `pausewc` pauses active crawling while preserving durable crawler position and progress truth.
- `resetwc` is the explicit controlled reset surface. It is not the same thing as pause.
- `poweroffwc` is the controlled crawler-aware poweroff surface.
- `rebootwc` is the controlled crawler-aware reboot surface.

The public control surface must not expose `stopwc` as a public wrapper name because that name suggests a stronger and more destructive semantics than the intended pause-and-preserve behavior.

The public control surface must not expose `resumewc` as a separate wrapper because `playwc` already covers both first start and resume-after-pause behavior.

### Canonical Repository Surface

The canonical tracked repository path on Pi51crawler must be:

- `/logisticsearch/repo/`

This is the canonical short-path tracked repository surface.

Tracked host-scoped crawler code remains under the repository tree, for example:

- `/logisticsearch/repo/makpi51crawler/`

The repository is the tracked source-of-truth surface. The live runtime surface under `/logisticsearch/makpi51crawler/` is the canonical execution surface populated from controlled tracked code.

### Legacy Path Rule

The following old long-path family is a legacy transition surface and must not be treated as the long-term canonical layout:

- `/srv/webcrawler/...`

If old surfaces still exist during migration, they must be treated as controlled transition surfaces only.

### Current Direction Rule

The current direction is:

1. keep tracked repository truth under `/logisticsearch/repo/`
2. keep live runtime code under `/logisticsearch/makpi51crawler/`
3. keep crawler data under `/srv/...`
4. keep the public operator surface small and explicit
5. continue controlled migration away from old mixed long-path layout

---

## TR

### Amaç

Bu doküman, Pi51crawler webcrawler yüzeyi için kanonik dizin-ve-dosya haritasını tanımlar.

Bu doküman bir yerleşim ve sınır sözleşmesidir. Verinin nerede duracağını, runtime kodunun nerede duracağını, kontrol sarmalayıcılarının nerede duracağını, konfigürasyonun nerede duracağını ve izlenen repository'nin nerede duracağını tanımlar.

Bu doküman bir runbook değildir. Kör taşıma, silme veya symlink kısayolu yetkisi vermez. Eski yollardan bu kanonik yollara geçiş yalnızca kontrollü adımlarla ve açık doğrulamalarla yapılmalıdır.

### Kesin Kurallar

1. Açık crawler veri yüzeyi `/srv/` altında yaşamalıdır.
2. Kanonik runtime kodu `/logisticsearch/makpi51crawler/` altında yaşamalıdır.
3. Kanonik izlenen repository `/logisticsearch/repo/` altında yaşamalıdır.
4. Açık operatör kontrol sarmalayıcıları bu dokümanda tanımlanan küçük ve sabit yüzeyle sınırlı kalmalıdır.
5. `stopwc` açık operatör sarmalayıcısı olarak bulunmamalıdır.
6. `resumewc` açık operatör sarmalayıcısı olarak bulunmamalıdır.
7. `playwc`, hem ilk başlatma hem de pause sonrasında devam etme davranışı için açık komuttur.
8. `pausewc`, crawler'ın bulunduğu yeri unutmadan kalıcı crawler konumu ve ilerleme doğrusunu korumalıdır.
9. İç runtime-control doğrusu veritabanı ve servis mantığında yine `run`, `pause` ve `stop` kullanabilir; ancak açık operatör yüzeyi daha küçük ve daha anlaşılır kalmalıdır.
10. Eski uzun yollar ve birbirine karışmış yüzeyler yalnızca kontrollü geçiş adımlarıyla emekliye ayrılmalıdır. Uzun vadeli kanonik yerleşim olarak kabul edilmemelidir.

### Kanonik Veri Yüzeyi

Tüm crawler veri yolları `/srv/` altında yaşamalıdır.

Kanonik veri yolları şunlardır:

- `/srv/webcrawler/raw_fetch/`
- `/srv/data/`
- `/srv/buffer/`
- `/srv/webcrawler/exports/`

Bu yolların anlamı sabittir:

- `/srv/webcrawler/raw_fetch/` ham fetch body artefact'larını tutar.
- `/srv/data/` kalıcı processed-data yüzeyi için seçilen işlenmiş çıktıyı tutar.
- `/srv/buffer/` yönlendirme politikası gerektirdiğinde geçici işlenmiş çıktı tamponlamasını tutar.
- `/srv/webcrawler/exports/` crawler export artefact'larını tutar.

`/srv/` altında hiçbir runtime kod yüzeyi kanonik kabul edilmemelidir. `/srv/` kanonik veri yüzeyidir; kanonik runtime-kod yüzeyi değildir.

### Kanonik Runtime Kod Yüzeyi

Kanonik runtime kodu şu yollar altında yaşamalıdır:

- `/logisticsearch/makpi51crawler/`
- `/logisticsearch/makpi51crawler/python_live_runtime/`
- `/logisticsearch/makpi51crawler/.venv/`

Bu yolların anlamı sabittir:

- `/logisticsearch/makpi51crawler/` kanonik runtime köküdür.
- `/logisticsearch/makpi51crawler/python_live_runtime/` canlı crawler runtime'ının kullandığı Python modül yüzeyini tutar.
- `/logisticsearch/makpi51crawler/.venv/` bu runtime yüzeyi için kanonik Python virtual environment'ı tutar.

`.venv` dizini, kanonik webcrawler runtime'ının izole Python paket ortamıdır. İzlenen repository kaynak yüzeyinin değil, runtime çalışma yüzeyinin parçasıdır.

### Kanonik Konfigürasyon Yüzeyi

Kanonik runtime konfigürasyonu şu dosyada yaşamalıdır:

- `/home/makpi51/.config/logisticsearch/secrets/webcrawler.env`

Bu dosya, canlı webcrawler yüzeyi için kanonik runtime environment dosyasıdır.

Secret taşıyan değerler yine dikkatli ve bilinçli biçimde ele alınmalıdır. Bu doküman yalnızca kanonik konumu tanımlar.

### Kanonik Kontrol Yüzeyi

Açık operatör kontrol sarmalayıcıları şu yollar altında yaşamalıdır:

- `/logisticsearch/makpi51crawler/python_live_runtime/controls/playwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/pausewc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/resetwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/poweroffwc.py`
- `/logisticsearch/makpi51crawler/python_live_runtime/controls/rebootwc.py`

Açık anlamlar şunlardır:

- `playwc`, crawler'ı aktif çalışma moduna alır ve pause sonrasında devam etmek için de kullanılan açık komuttur.
- `pausewc`, aktif crawl işlemini duraksatır ama kalıcı crawler konumu ve ilerleme doğrusunu korur.
- `resetwc`, açık ve kontrollü reset yüzeyidir. Pause ile aynı şey değildir.
- `poweroffwc`, crawler-farkındalıklı kontrollü poweroff yüzeyidir.
- `rebootwc`, crawler-farkındalıklı kontrollü reboot yüzeyidir.

Açık kontrol yüzeyi `stopwc` adını bir açık sarmalayıcı olarak sunmamalıdır; çünkü bu ad, hedeflenen pause-et-ve-koru davranışından daha güçlü ve daha yıkıcı bir anlam çağrıştırır.

Açık kontrol yüzeyi `resumewc` adını ayrı bir sarmalayıcı olarak da sunmamalıdır; çünkü `playwc` hem ilk başlatma hem de pause sonrası devam davranışını zaten kapsar.

### Kanonik Repository Yüzeyi

Pi51crawler üzerindeki kanonik izlenen repository yolu şu olmalıdır:

- `/logisticsearch/repo/`

Bu yol, kanonik kısa-yol izlenen repository yüzeyidir.

İzlenen host-scoped crawler kodu repository ağacı altında kalmaya devam eder; örneğin:

- `/logisticsearch/repo/makpi51crawler/`

Repository, izlenen source-of-truth yüzeyidir. `/logisticsearch/makpi51crawler/` altındaki canlı runtime yüzeyi ise kontrollü izlenen koddan doldurulan kanonik execution yüzeyidir.

### Eski Yol Kuralı

Aşağıdaki eski uzun-yol ailesi bir geçiş yüzeyidir ve uzun vadeli kanonik yerleşim olarak görülmemelidir:

- `/srv/webcrawler/...`

Geçiş sırasında eski yüzeyler hâlâ bulunuyorsa, bunlar yalnızca kontrollü geçiş yüzeyleri olarak ele alınmalıdır.

### Güncel Yön Kuralı

Güncel yön şudur:

1. izlenen repository doğrusu `/logisticsearch/repo/` altında kalsın
2. canlı runtime kodu `/logisticsearch/makpi51crawler/` altında kalsın
3. crawler verisi `/srv/...` altında kalsın
4. açık operatör yüzeyi küçük ve açık kalsın
5. eski karışık uzun-yol yerleşiminden kontrollü biçimde çıkılsın

## Runtime tree and data-flow map

### EN

The directory map and the runtime-tree map answer different questions and must be read together.

This document answers the layout question:

- where crawler data lives,
- where live runtime code lives,
- where controls live,
- where runtime configuration lives,
- where the tracked repository lives,
- which old path families are legacy or transition-only surfaces.

The runtime-tree document answers the execution question:

- which Python file owns root entry,
- which file owns the main loop,
- which file owns worker orchestration,
- which file owns database access,
- which file owns static/public acquisition,
- which file owns dynamic browser acquisition,
- which file owns parse behavior,
- which file owns taxonomy lookup,
- which boundary separates raw evidence, processed output, and export handoff.

The mandatory companion document is:

- `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`

Use this file first when checking filesystem placement. Use the runtime-tree map immediately after it when checking behavior ownership.

A path being canonical does not automatically mean that every file under that path is allowed to run during an audit.

Execution-safety policy is not owned by this directory map. For the control-class and no-execution rule, read `docs/TOPIC_CONTROLS_RUN_POLICY_AND_SAFETY_CLASSIFICATION_2026_05_06.md`.

During documentation, inventory, or path-audit work, this means `NO_CONTROL_SCRIPT_EXECUTION` remains mandatory even when a path is canonical.. Runtime location, execution permission, operator control policy, and crawler start permission are separate safety gates.

For documentation and inventory work, the safe rule is:

- read files;
- compare paths;
- compare hashes;
- compare line counts;
- parse Python syntax when explicitly allowed;
- do not execute crawler controls;
- do not start the crawler;
- do not mutate DB, systemd, live runtime, or pi51c unless a later step explicitly authorizes that mutation.

### TR

Dizin haritası ile runtime-tree haritası farklı sorulara cevap verir ve birlikte okunmalıdır.

Bu doküman yerleşim sorusuna cevap verir:

- crawler verisinin nerede durduğu,
- canlı runtime kodunun nerede durduğu,
- control yüzeyinin nerede durduğu,
- runtime konfigürasyonunun nerede durduğu,
- izlenen repository'nin nerede durduğu,
- hangi eski yol ailelerinin legacy veya yalnızca geçiş yüzeyi olduğu.

Runtime-tree dokümanı execution sorusuna cevap verir:

- hangi Python dosyasının root entry sahibi olduğu,
- hangi dosyanın main loop sahibi olduğu,
- hangi dosyanın worker orchestration sahibi olduğu,
- hangi dosyanın database access sahibi olduğu,
- hangi dosyanın static/public acquisition sahibi olduğu,
- hangi dosyanın dynamic browser acquisition sahibi olduğu,
- hangi dosyanın parse davranışı sahibi olduğu,
- hangi dosyanın taxonomy lookup sahibi olduğu,
- raw evidence, processed output ve export handoff sınırının nerede olduğu.

Zorunlu yardımcı doküman şudur:

- `docs/SECTION1_WEBCRAWLER_RUNTIME_TREE_AND_DATA_FLOW_MAP.md`

Filesystem yerleşimini kontrol ederken önce bu dosyayı oku. Davranış sahipliğini kontrol ederken hemen ardından runtime-tree haritasını oku.

Bir yolun kanonik olması, o yol altındaki her dosyanın audit sırasında çalıştırılabileceği anlamına gelmez.

Execution-güvenliği politikası bu dizin haritasının sahibi olduğu konu değildir. Control-class ve çalıştırmama kuralı için `docs/TOPIC_CONTROLS_RUN_POLICY_AND_SAFETY_CLASSIFICATION_2026_05_06.md` okunmalıdır.

Dokümantasyon, envanter veya path-audit işlerinde bu, yol kanonik olsa bile `NO_CONTROL_SCRIPT_EXECUTION` kuralının zorunlu kaldığı anlamına gelir.. Runtime konumu, execution permission, operator control policy ve crawler start izni ayrı güvenlik kapılarıdır.

Dokümantasyon ve envanter çalışmaları için güvenli kural şudur:

- dosyaları oku;
- path karşılaştır;
- hash karşılaştır;
- satır sayısı karşılaştır;
- açıkça izin verildiyse Python syntax parse et;
- crawler control scriptleri çalıştırma;
- crawler başlatma;
- sonraki bir adım açıkça yetki vermedikçe DB, systemd, live runtime veya pi51c üzerinde mutasyon yapma.
