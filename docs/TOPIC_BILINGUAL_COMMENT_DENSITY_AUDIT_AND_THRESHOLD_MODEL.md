# TOPIC_BILINGUAL_COMMENT_DENSITY_AUDIT_AND_THRESHOLD_MODEL

## EN

### Why this document exists

This document defines the canonical explanation rule for LogisticSearch repository surfaces.

The rule is intentionally larger than a narrow comment-count rule.

A file may have many English and Turkish comment lines and still fail the real project standard if:
- the file identity is unclear,
- the code-near explanation is missing,
- variables, fields, parameters, branches, commands, or DB effects are not explained,
- expected and undesired values are not made visible,
- the repository cannot be used to recover project position after memory loss.

So the real rule is:

**comment density is only a floor; recoverability, code-near explanation, and bilingual semantic clarity are the real acceptance standard.**

---

### Universal scope

This standard applies to all tracked technical surfaces, not only Python.

Included surface families:
- Python
- SQL
- PostgreSQL-oriented SQL and DB scripts
- Markdown
- runbooks
- topic docs
- status docs
- to-do docs
- shell scripts
- future C++
- future Assembly
- future other technical source files

Different file types may use different comment syntax.
The explanation duty does not disappear.

---

### Project-level recovery requirement

The repository must be readable strongly enough that if both:
- assistant memory is lost, and
- operator memory is lost,

the project and the current position can still be reconstructed by carefully reading GitHub.

That means the repository must explain:
- what the project is,
- what each important surface is,
- what has already been done,
- where the project currently stands,
- what the current blocker is,
- what the next exact steps are,
- and what order those steps belong in.

The repository is not only a code tree.
It is also a continuity and recovery surface.

---

### Immediate-above explanation rule

The preferred placement rule is strict.

The explanation should appear immediately above the thing it explains.

Examples:
- file/module identity block above the module body
- class explanation above the class line
- function explanation above the def line
- important variable explanation above the variable or the smallest relevant block
- SQL block explanation above the SQL block
- shell command explanation above the command block
- Markdown section framing above the relevant section

What is not enough by itself:
- only a distant top docstring,
- only a function docstring below the signature,
- only a remote explanation many lines away,
- only English nearby,
- only Turkish nearby.

---

### Universal explanation coverage rule

Every important file should explain, in English and Turkish:
- why this file exists,
- what it does,
- what it does not do,
- where it sits topologically,
- what upstream/downstream surfaces it touches.

Every important code/document surface should explain, in English and Turkish:
- class
- function
- important variable
- important field
- important parameter
- important branch
- important command
- important DB call
- important filesystem effect
- important runtime effect
- important status section
- important to-do queue section

---

### Expected / undesired value rule

Where relevant, the explanation must say:
- accepted values,
- expected values,
- undesired values,
- invalid values,
- degraded values,
- success/failure branch meanings.

This especially matters for:
- runtime payload fields,
- DB result fields,
- taxonomy/language values,
- state labels,
- verdict strings,
- booleans that change flow,
- method selectors,
- path selectors,
- fetch/parse/finalize outcomes,
- queue/status fields.

---

### Small-file clarification

No tracked technical file is exempt merely because it is small.

This includes:
- `__init__.py`
- wrappers
- small helpers
- tiny control entry files
- small docs
- short scripts

A small file may naturally need fewer lines than a large file.
But it still must make its role understandable.

So:
- “small” does not mean “skip explanation”
- “small” only means the explanation may be shorter if the real surface is truly smaller

---

### Why raw count is not enough

A count-only audit can tell us:
- EN line count,
- TR line count,
- AST validity,
- compile validity.

But a count-only audit cannot guarantee:
- the right thing is explained,
- the explanation is above the right code,
- the explanation is specific,
- the explanation covers variables/fields/branches,
- the explanation is continuity-strong enough for GitHub-only recovery.

Therefore raw counts are only weak indicators, not the final judge.

---

### Layered audit model

A proper audit must be layered.

#### Layer 1 — Structural validity
- parser/AST passes where applicable
- compile passes where applicable

#### Layer 2 — Presence coverage
- module/file identity header exists
- class/function explanation exists
- variable/field/parameter/branch explanation exists where needed

#### Layer 3 — Placement quality
- explanation is immediately above the relevant surface
- explanation is not incorrectly drifting into unrelated context

#### Layer 4 — Semantic quality
- explanation is file-specific and code-specific
- explanation explains why, not only what
- explanation states accepted/undesired values where relevant
- explanation preserves visible branch meaning

#### Layer 5 — Continuity quality
- repository contains status truth
- repository contains next-step truth
- repository contains timestamped execution truth
- GitHub alone can recover the project state

---

### Living status / to-do rule

Repository continuity is incomplete if code comments exist but current project position is invisible.

So the repository must also maintain living canonical documents for:
- current status,
- current blockers,
- current next actions,
- timestamped execution queue.

Those documents must be updated continuously after meaningful work.
They are not decorative.
They are part of the technical continuity contract.

---

### Current strategic context that this rule must support

The current project line includes:
- webcrawler / crawler_core bring-up
- strict runtime-control auditing
- multilingual direction with 25-language compatibility
- current active working language line starting from English
- GitHub-controlled canon first
- later controlled sync to pi51c repo
- later controlled sync to live runtime
- then strict runtime validation continuation

This standard exists partly to stop repeated work and position loss while moving through those lines.

---

### Canonical acceptance rule

A tracked technical file or continuity document should be considered truly acceptable only when:
1. it is structurally valid,
2. its role is understandable,
3. the important surfaces are explained immediately above the relevant code/section,
4. variables/fields/parameters/branches/commands are explained where relevant,
5. expected and undesired values are visible where relevant,
6. both English and Turkish carry real meaning,
7. the file contributes to long-term GitHub-only recovery.

---

## TR

### Bu belge neden var

Bu belge, LogisticSearch repository yüzeyleri için kanonik açıklama kuralını tanımlar.

Bu kural, dar bir yorum-sayısı kuralından bilinçli olarak daha büyüktür.

Bir dosya İngilizce ve Türkçe yorum satırı olarak yüksek görünebilir ama yine de gerçek proje standardını geçemeyebilir. Örneğin:
- dosya kimliği açık değildir,
- koda yakın açıklama eksiktir,
- değişkenler, alanlar, parametreler, branch’ler, komutlar veya DB etkileri açıklanmamıştır,
- beklenen ve istenmeyen değerler görünür değildir,
- repository, hafıza kaybı sonrası proje konumunu yeniden kuracak kadar açıklayıcı değildir.

Bu yüzden gerçek kural şudur:

**yorum yoğunluğu sadece tabandır; geri-kurulabilirlik, koda yakın açıklama ve çift dilli semantik açıklık asıl kabul standardıdır.**

---

### Evrensel kapsam

Bu standart sadece Python için değil, izlenen tüm teknik yüzeyler için geçerlidir.

Dahil olan yüzey aileleri:
- Python
- SQL
- PostgreSQL odaklı SQL ve DB scriptleri
- Markdown
- runbook’lar
- topic dokümanları
- status dokümanları
- to-do dokümanları
- shell scriptleri
- gelecekte C++
- gelecekte Assembly
- gelecekte diğer teknik kaynak dosyaları

Farklı dosya tipleri farklı yorum sözdizimi kullanabilir.
Açıklama yükümlülüğü ortadan kalkmaz.

---

### Proje-seviyesi kurtarma gereksinimi

Repository, hem:
- asistan hafızası silinse, hem de
- operatör hafızası silinse,

yalnız GitHub dikkatle okunarak proje ve mevcut konum yeniden kurulabilecek kadar açıklayıcı olmalıdır.

Bu şu anlama gelir:
repository şunları açıklamalıdır:
- proje nedir,
- her önemli yüzey nedir,
- neler yapılmıştır,
- şu an neredeyiz,
- mevcut blocker nedir,
- sıradaki net adımlar nelerdir,
- bu adımlar hangi sıraya aittir.

Repository yalnızca bir kod ağacı değildir.
Aynı zamanda süreklilik ve kurtarma yüzeyidir.

---

### Hemen-üstünde açıklama kuralı

Tercih edilen yerleşim kuralı sıkıdır.

Açıklama, açıkladığı şeyin hemen üstünde görünmelidir.

Örnekler:
- file/module kimlik bloğu modül gövdesinin üstünde
- class açıklaması class satırının üstünde
- function açıklaması def satırının üstünde
- önemli variable açıklaması variable satırının veya en küçük ilgili bloğun üstünde
- SQL blok açıklaması SQL bloğunun üstünde
- shell komut açıklaması komut bloğunun üstünde
- Markdown bölüm çerçevesi ilgili bölümün üstünde

Tek başına yeterli olmayan şeyler:
- sadece uzaktaki top docstring,
- sadece imza altındaki function docstring,
- sadece çok uzaktaki açıklama,
- sadece yakın İngilizce,
- sadece yakın Türkçe.

---

### Evrensel açıklama kapsama kuralı

Her önemli dosya İngilizce ve Türkçe olarak şunları açıklamalıdır:
- bu dosya neden var,
- ne yapar,
- ne yapmaz,
- topolojik olarak nereye oturur,
- hangi üst/alt yüzeylerle temas eder.

Her önemli kod/doküman yüzeyi İngilizce ve Türkçe olarak şunları açıklamalıdır:
- class
- function
- önemli variable
- önemli field
- önemli parameter
- önemli branch
- önemli command
- önemli DB call
- önemli filesystem etkisi
- önemli runtime etkisi
- önemli status bölümü
- önemli to-do queue bölümü

---

### Beklenen / istenmeyen değer kuralı

Gerekli yerlerde açıklama şunları söylemelidir:
- kabul edilen değerler,
- beklenen değerler,
- istenmeyen değerler,
- geçersiz değerler,
- degraded değerler,
- success/failure branch anlamları.

Bu özellikle şu alanlarda önemlidir:
- runtime payload field’ları,
- DB sonuç field’ları,
- taxonomy/dil değerleri,
- state label’lar,
- verdict string’leri,
- akışı değiştiren boolean’lar,
- method seçicileri,
- path seçicileri,
- fetch/parse/finalize outcome’ları,
- queue/status alanları.

---

### Küçük dosya açıklaması

İzlenen hiçbir teknik dosya, küçük diye kapsam dışı sayılamaz.

Buna şunlar da dahildir:
- `__init__.py`
- wrapper dosyaları
- küçük helper dosyaları
- küçük control entry dosyaları
- küçük dokümanlar
- kısa scriptler

Küçük dosya doğal olarak büyük dosya kadar satır istemeyebilir.
Ama yine de rolünü anlaşılır kılmalıdır.

Yani:
- “küçük” olmak “açıklamayı atla” anlamına gelmez
- sadece gerçek yüzey küçükse açıklama daha kısa olabilir

---

### Ham sayı neden yetmez

Sadece sayıya bakan audit bize şunu söyleyebilir:
- EN satır sayısı,
- TR satır sayısı,
- AST geçerliliği,
- compile geçerliliği.

Ama bu, şunu garanti etmez:
- doğru şey açıklanmıştır,
- açıklama doğru kodun üstündedir,
- açıklama özeldir,
- variable/field/branch kapsaması vardır,
- açıklama GitHub-only recovery için yeterince güçlüdür.

Bu yüzden ham sayılar son hakem değildir; sadece zayıf göstergelerdir.

---

### Katmanlı audit modeli

Doğru audit çok katmanlı olmalıdır.

#### Katman 1 — Yapısal geçerlilik
- uygun yerde parser/AST geçer
- uygun yerde compile geçer

#### Katman 2 — Varlık kapsaması
- module/file kimlik header’ı vardır
- class/function açıklaması vardır
- gerekli yerlerde variable/field/parameter/branch açıklaması vardır

#### Katman 3 — Yerleşim kalitesi
- açıklama ilgili yüzeyin hemen üstündedir
- açıklama yanlış bağlama kaymamıştır

#### Katman 4 — Semantik kalite
- açıklama dosyaya ve koda özgüdür
- sadece ne yaptığını değil neden var olduğunu açıklar
- gerekli yerlerde kabul edilen/istenmeyen değerleri söyler
- görünür branch anlamını korur

#### Katman 5 — Süreklilik kalitesi
- repository status doğrusu taşır
- repository next-step doğrusu taşır
- repository timestamp’li execution doğrusu taşır
- yalnız GitHub okunarak proje durumu yeniden kurulabilir

---

### Yaşayan status / to-do kuralı

Kod yorumları olsa bile mevcut proje konumu görünmüyorsa repository sürekliliği eksiktir.

Bu yüzden repository ayrıca yaşayan kanonik dokümanlar da taşımalıdır:
- current status,
- current blockers,
- current next actions,
- timestamped execution queue.

Bu dokümanlar anlamlı her işten sonra güncellenmelidir.
Dekoratif değildirler.
Teknik süreklilik sözleşmesinin parçasıdırlar.

---

### Bu kuralın desteklemesi gereken güncel stratejik bağlam

Mevcut proje hattında şunlar vardır:
- webcrawler / crawler_core ayağa kaldırma
- sert runtime-control audit hattı
- 25 dil uyumlu çok dilli yön
- şu an İngilizce ile başlayan aktif çalışma hattı
- önce GitHub-kontrollü kanon
- sonra kontrollü pi51c repo sync
- sonra kontrollü live runtime sync
- ardından sert runtime validation devamı

Bu standart, tam da bu hatlarda tekrar işi ve konum kaybını azaltmak için vardır.

---

### Kanonik kabul kuralı

İzlenen bir teknik dosya veya süreklilik dokümanı ancak şu durumda gerçekten kabul edilebilir sayılmalıdır:
1. yapısal olarak geçerliyse,
2. rolü anlaşılırsa,
3. önemli yüzeyleri ilgili kodun/bölümün hemen üstünde açıklanmışsa,
4. gerekli yerlerde variable/field/parameter/branch/command açıklaması varsa,
5. gerekli yerlerde beklenen ve istenmeyen değerler görünürse,
6. İngilizce ve Türkçe ikisi de gerçek anlam taşıyorsa,
7. dosya uzun vadeli GitHub-only recovery’ye hizmet ediyorsa.
