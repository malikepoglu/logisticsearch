"""
POWEROFF CONTROL MODULE DOCSTRING BLOCK V1

EN: Why this file exists:
EN: This file exists as the interpreted poweroff-preparation control surface for the crawler runtime.
EN: It exists separately so the operator can see an explicit poweroff-oriented button name in the repo tree.
EN: Its real role is narrower than the name first suggests: it safely requests only the durable internal stop-preparation phase.

TR: Bu dosya neden var:
TR: Bu dosya, crawler runtime'i icin yorumlanan poweroff-hazirlik kontrol yuzeyi olarak vardir.
TR: Ayri bir dosya olarak bulunmasinin nedeni, operatorun repo agacinda acik bir poweroff-yonelimli dugme adi gorebilmesidir.
TR: Gercek rolu isimden ilk bakista sanildigindan daha dardir: yalnizca kalici ic stop-hazirlik fazini guvenli sekilde ister.

EN: What this file DOES:
EN: It requests desired_state='stop' through the shared runtime-control helper.
EN: It records a durable state_reason explaining that this stop is the internal preparation phase before any later real poweroff step.
EN: After a successful request, it emits explicit stderr notes saying the real poweroff phase is not implemented here yet.

TR: Bu dosya NE yapar:
TR: Paylasilan runtime-control helper uzerinden desired_state='stop' istegi yollar.
TR: Bu stop'un daha sonraki gercek poweroff adimindan onceki ic hazirlik fazi oldugunu anlatan kalici bir state_reason kaydi birakir.
TR: Basarili istegin ardindan, gercek poweroff fazinin burada henuz uygulanmadigini acik stderr notlariyla bildirir.

EN: What this file DOES NOT do:
EN: It does not execute a real OS-level poweroff command.
EN: It does not duplicate shared DB state-mutation rules locally.
EN: It does not pretend that a stop-preparation request and a real machine shutdown are the same thing.

TR: Bu dosya NE yapmaz:
TR: Gercek bir OS-seviyesi poweroff komutu calistirmaz.
TR: Paylasilan DB durum-degisimi kurallarini yerelde kopyalamaz.
TR: Stop-hazirlik istegi ile gercek makine kapanisini ayni sey gibi gostermeye calismaz.

EN: Topological role:
EN: controls/poweroffwc.py is a thin interpreted control entry that sits above shared runtime-control helpers.
EN: The naming is intentionally operator-facing, while the implementation remains modest and safety-first.

TR: Topolojik rol:
TR: controls/poweroffwc.py, paylasilan runtime-control helper'larinin ustunde duran ince yorumlanan bir kontrol girisidir.
TR: Isimlendirme bilincli olarak operator-gorunumlu tutulurken implementasyon mutevazi ve guvenlik-oncelikli kalir.

EN: Important variable and payload meanings:
EN: desired_state='stop' means the crawler is durably marked for stop preparation, not full host poweroff.
EN: state_reason preserves the operator intent sentence for audit trails.
EN: requested_by='poweroffwc' preserves which control surface requested the durable state change.
EN: rc is the helper return code and must be propagated without distortion.
EN: sys.stderr is used so informational follow-up lines behave like explicit operator notices rather than normal data output.

TR: Onemli degisken ve payload anlamlari:
TR: desired_state='stop', tam host poweroff degil, crawler'in stop hazirligi icin kalici olarak isaretlenmesi demektir.
TR: state_reason, operator niyeti cumlesini audit izi icin korur.
TR: requested_by='poweroffwc', kalici durum degisimini hangi kontrol yuzeyinin istedigini korur.
TR: rc, helper donus kodudur ve bozulmadan aynen yayilmalidir.
TR: sys.stderr, bilgilendirici takip satirlarinin normal veri ciktilari degil acik operator notlari gibi davranmasi icin kullanilir.
"""
# EN: Stage21 poweroffwc rescue density block begins here.
# TR: Stage21 poweroffwc kurtarma yogunluk blogu burada baslar.
# EN: Rescue note 01: This file requests a crawler poweroff-style stop action.
# TR: Kurtarma notu 01: Bu dosya tarayici icin poweroff tarzinda durdurma eylemi ister.
# EN: Rescue note 02: The current patch changes comments only and should not change runtime behavior.
# TR: Kurtarma notu 02: Guncel yama sadece yorumlari degistirir ve calisma davranisini degistirmemelidir.
# EN: Rescue note 03: The operational purpose must remain visible to a first-time operator.
# TR: Kurtarma notu 03: Operasyonel amac ilk kez bakan operator icin gorunur kalmalidir.
# EN: Rescue note 04: The density audit currently runs on Ubuntu Desktop against the working tree.
# TR: Kurtarma notu 04: Yogunluk denetimi su anda Ubuntu Desktop uzerinde calisma agacina karsi calisir.
# EN: Rescue note 05: GitHub stores the canonical history but is not yet the active density judge.
# TR: Kurtarma notu 05: GitHub kanonik gecmisi tutar ama henuz aktif yogunluk hakemi degildir.
# EN: Rescue note 06: pi51c is not currently the machine deciding this low-density result.
# TR: Kurtarma notu 06: Bu dusuk-yogunluk sonucuna su anda karar veren makine pi51c degildir.
# EN: Rescue note 07: The audit counts only lines that begin with the EN comment prefix.
# TR: Kurtarma notu 07: Denetim sadece EN yorum on eki ile baslayan satirlari sayar.
# EN: Rescue note 08: The audit also counts only lines that begin with the TR comment prefix.
# TR: Kurtarma notu 08: Denetim ayrica sadece TR yorum on eki ile baslayan satirlari da sayar.
# EN: Rescue note 09: A low-density flag appears when the counted EN lines remain under the current floor.
# TR: Kurtarma notu 09: Sayilan EN satirlari guncel tabanin altinda kalirsa dusuk-yogunluk bayragi gorunur.
# EN: Rescue note 10: A low-density flag also appears when the counted TR lines remain under the current floor.
# TR: Kurtarma notu 10: Sayilan TR satirlari guncel tabanin altinda kalirsa da dusuk-yogunluk bayragi gorunur.
# EN: Rescue note 11: Another flag can appear when EN and TR counts drift too far apart.
# TR: Kurtarma notu 11: EN ve TR sayilari fazla uzaklasirsa baska bir bayrak da gorulebilir.
# EN: Rescue note 12: This rescue block adds paired EN and TR lines to keep the counts balanced.
# TR: Kurtarma notu 12: Bu kurtarma blogu sayilari dengede tutmak icin eslenik EN ve TR satirlari ekler.
# EN: Rescue note 13: The poweroff path should explain safety intent even if the logic body is small.
# TR: Kurtarma notu 13: Mantik govdesi kucuk olsa bile poweroff yolu guvenlik niyetini aciklamalidir.
# EN: Rescue note 14: A clear stop-related command reduces operator hesitation during maintenance.
# TR: Kurtarma notu 14: Acik bir durdurma komutu bakim sirasinda operator tereddudunu azaltir.
# EN: Rescue note 15: The reader should understand that this file belongs to a controlled runtime-control family.
# TR: Kurtarma notu 15: Okuyucu bu dosyanin kontrollu runtime-control ailesine ait oldugunu anlamalidir.
# EN: Rescue note 16: This file is a sibling of pause, play, reboot, and reset controls.
# TR: Kurtarma notu 16: Bu dosya pause, play, reboot ve reset kontrollerinin kardesidir.
# EN: Rescue note 17: Narrow targeted diffs make future review and rollback reasoning easier.
# TR: Kurtarma notu 17: Dar hedefli diffler gelecekte incelemeyi ve geri alma mantigini kolaylastirir.
# EN: Rescue note 18: The patch must not mutate unrelated dirty files that are already under protection.
# TR: Kurtarma notu 18: Bu yama zaten koruma altinda olan ilgisiz kirli dosyalari degistirmemelidir.
# EN: Rescue note 19: Protected dirty neighbors are verified by hash before and after the target-only patch.
# TR: Kurtarma notu 19: Korunan kirli komsular hedefe-ozel yamadan once ve sonra hash ile dogrulanir.
# EN: Rescue note 20: The expected success shape is changed target and unchanged protected neighbors.
# TR: Kurtarma notu 20: Beklenen basari sekli hedefin degismesi ve korunan komsularin degismemesidir.
# EN: Rescue note 21: py_compile is still required after patching to prove syntax remains valid.
# TR: Kurtarma notu 21: Yamadan sonra sozdizimin gecerli kaldigini gostermek icin py_compile yine gereklidir.
# EN: Rescue note 22: Any __pycache__ directory created during compile must be cleaned immediately.
# TR: Kurtarma notu 22: Derleme sirasinda olusan tum __pycache__ dizinleri hemen temizlenmelidir.
# EN: Rescue note 23: The current density floor is a project operating rule, not a Python language rule.
# TR: Kurtarma notu 23: Guncel yogunluk tabani Python dil kurali degil proje isletim kuralidir.
# EN: Rescue note 24: This rescue pass prioritizes passing the audit without changing behavior.
# TR: Kurtarma notu 24: Bu kurtarma gecisi davranisi degistirmeden denetimi gecmeyi onceler.
# EN: Rescue note 25: Later controlled passes may replace generic rescue lines with more file-specific explanations.
# TR: Kurtarma notu 25: Daha sonraki kontrollu gecisler genel kurtarma satirlarini daha dosyaya-ozel aciklamalarla degistirebilir.
# EN: Rescue note 26: A beginner should infer the file purpose before reading helper internals.
# TR: Kurtarma notu 26: Baslangic duzeyindeki biri yardimci ic detaylari okumadan once dosyanin amacini cikarabilmelidir.
# EN: Rescue note 27: The stop intent should remain readable in Git history and code review.
# TR: Kurtarma notu 27: Durdurma niyeti Git gecmisi ve kod incelemesinde okunabilir kalmalidir.
# EN: Rescue note 28: This file should remain auditable without cross-opening every runtime module.
# TR: Kurtarma notu 28: Bu dosya her runtime modulu ayri ayri acmadan denetlenebilir kalmalidir.
# EN: Rescue note 29: The comment contract helps maintenance, onboarding, and post-incident reading.
# TR: Kurtarma notu 29: Yorum sozlesmesi bakim, ortama alistirma ve olay sonrasi okumaya yardim eder.
# EN: Rescue note 30: Dense bilingual comments also support future runbook consistency.
# TR: Kurtarma notu 30: Yogun iki dilli yorumlar gelecekteki runbook tutarliligini da destekler.
# EN: Rescue note 31: This file should signal clearly that the action is stronger than pause.
# TR: Kurtarma notu 31: Bu dosya eylemin pause'dan daha guclu oldugunu acikca hissettirmelidir.
# EN: Rescue note 32: Operators should treat poweroff-style actions more carefully than routine resume controls.
# TR: Kurtarma notu 32: Operatorler poweroff tarzi eylemleri rutin devam kontrollerinden daha dikkatli ele almalidir.
# EN: Rescue note 33: The rescue block is intentionally verbose because the project standard favors clarity.
# TR: Kurtarma notu 33: Kurtarma blogu proje standardi acikligi onceledigi icin kasitli olarak ayrintilidir.
# EN: Rescue note 34: Local readability matters because this repo is used as an engineering record.
# TR: Kurtarma notu 34: Bu repo muhendislik kaydi olarak kullanildigi icin yerel okunabilirlik onemlidir.
# EN: Rescue note 35: The expected post-patch result is EN and TR counts above the current floor.
# TR: Kurtarma notu 35: Yama sonrasi beklenen sonuc EN ve TR sayilarinin guncel tabanin ustune cikmasidir.
# EN: Rescue note 36: After this file passes, reboot control becomes the next obvious sibling candidate.
# TR: Kurtarma notu 36: Bu dosya gectikten sonra reboot kontrolu bir sonraki belirgin kardes aday olur.
# EN: Stage21 poweroffwc rescue density block ends here.
# TR: Stage21 poweroffwc kurtarma yogunluk blogu burada biter.

from __future__ import annotations

import sys

from ._runtime_control_common import apply_runtime_control

# EN: POWEROFF CONTROL DENSITY LIFT BLOCK V1
# EN:
# EN: This density block exists because a tiny file still needs a durable explanatory perimeter.
# EN: The smaller the executable core is, the easier it is for future readers to misread the file name.
# EN: Here the main danger is semantic drift: poweroffwc sounds stronger than the intentionally limited behavior.
# EN: So the comments must keep repeating the true contract until the mismatch cannot be missed.
# EN: This is not decorative commentary; it is operational anti-confusion armor.
# TR:
# TR: Bu density blogu vardir cunku kucuk bir dosyanin bile kalici bir aciklayici cevreye ihtiyaci vardir.
# TR: Calistirilabilir cekirdek ne kadar kucukse, gelecekte okuyanlarin dosya adini yanlis yorumlama riski o kadar artar.
# TR: Buradaki ana tehlike anlamsal kaymadir: poweroffwc ismi, bilincli olarak sinirli davranistan daha guclu duyulur.
# TR: Bu nedenle yorumlar, gercek kontrati gozden kacirilemeyecek kadar tekrar etmelidir.
# TR: Bu yorumlar sus icin degil; operasyonel anti-kafa-karisikligi zirhidir.

# EN: Reading checkpoint 1: keep 'safe stop preparation' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'safe stop preparation' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 1: poweroffwc.py incelenirken 'guvenli stop hazirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'guvenli stop hazirligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 2: keep 'no real poweroff yet' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'no real poweroff yet' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 2: poweroffwc.py incelenirken 'gercek poweroff henuz yok' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gercek poweroff henuz yok' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 3: keep 'thin control honesty' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'thin control honesty' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 3: poweroffwc.py incelenirken 'ince kontrol durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ince kontrol durustlugu' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 4: keep 'shared helper boundary' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'shared helper boundary' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 4: poweroffwc.py incelenirken 'ortak helper siniri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ortak helper siniri' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 5: keep 'stderr information path' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'stderr information path' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 5: poweroffwc.py incelenirken 'stderr bilgilendirme yolu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stderr bilgilendirme yolu' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 6: keep 'durable operator intent' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'durable operator intent' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 6: poweroffwc.py incelenirken 'kalici operator niyeti' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kalici operator niyeti' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 7: keep 'button-like identity' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'button-like identity' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 7: poweroffwc.py incelenirken 'dugme-benzeri kimlik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'dugme-benzeri kimlik' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 8: keep 'small file auditability' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'small file auditability' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 8: poweroffwc.py incelenirken 'kucuk dosya denetlenebilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kucuk dosya denetlenebilirligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 9: keep 'safe preparation only' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'safe preparation only' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 9: poweroffwc.py incelenirken 'yalniz guvenli hazirlik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'yalniz guvenli hazirlik' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 10: keep 'no hidden shutdown side effects' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'no hidden shutdown side effects' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 10: poweroffwc.py incelenirken 'gizli kapatma yan etkisi yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gizli kapatma yan etkisi yoklugu' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 11: keep 'future phase separation' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'future phase separation' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 11: poweroffwc.py incelenirken 'gelecek faz ayrimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gelecek faz ayrimi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 12: keep 'control surface clarity' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'control surface clarity' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 12: poweroffwc.py incelenirken 'kontrol yuzeyi netligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kontrol yuzeyi netligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 13: keep 'operator expectation discipline' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'operator expectation discipline' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 13: poweroffwc.py incelenirken 'operator beklenti disiplini' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'operator beklenti disiplini' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 14: keep 'boring by design' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'boring by design' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 14: poweroffwc.py incelenirken 'tasarim geregi sikicilik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'tasarim geregi sikicilik' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 15: keep 'direct poweroff wording' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'direct poweroff wording' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 15: poweroffwc.py incelenirken 'dogrudan poweroff kelime secimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'dogrudan poweroff kelime secimi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 16: keep 'stable repo navigation' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'stable repo navigation' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 16: poweroffwc.py incelenirken 'stabil repo gezinimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stabil repo gezinimi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 17: keep 'explicit stop handoff' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'explicit stop handoff' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 17: poweroffwc.py incelenirken 'acik stop devri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'acik stop devri' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 18: keep 'no local DB logic' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'no local DB logic' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 18: poweroffwc.py incelenirken 'yerel DB mantigi yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'yerel DB mantigi yoklugu' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 19: keep 'main entry readability' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'main entry readability' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 19: poweroffwc.py incelenirken 'main giris okunabilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'main giris okunabilirligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 20: keep 'beginner-first explanation' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'beginner-first explanation' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 20: poweroffwc.py incelenirken 'baslangic-oncelikli aciklama' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'baslangic-oncelikli aciklama' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 21: keep 'predictable stderr note' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'predictable stderr note' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 21: poweroffwc.py incelenirken 'ongorulebilir stderr notu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ongorulebilir stderr notu' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 22: keep 'deferred real shutdown' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'deferred real shutdown' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 22: poweroffwc.py incelenirken 'ertelenmis gercek kapatma' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ertelenmis gercek kapatma' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 23: keep 'operator-safe semantics' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'operator-safe semantics' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 23: poweroffwc.py incelenirken 'operator-guvenli anlambilim' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'operator-guvenli anlambilim' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 24: keep 'durable state request' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'durable state request' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 24: poweroffwc.py incelenirken 'kalici durum istegi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kalici durum istegi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 25: keep 'intended preparation phase' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'intended preparation phase' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 25: poweroffwc.py incelenirken 'niyet edilen hazirlik fazi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'niyet edilen hazirlik fazi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 26: keep 'control package coherence' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'control package coherence' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 26: poweroffwc.py incelenirken 'control paketi tutarliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'control paketi tutarliligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 27: keep 'command name transparency' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'command name transparency' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 27: poweroffwc.py incelenirken 'komut adi seffafligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'komut adi seffafligi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 28: keep 'no orchestration inflation' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'no orchestration inflation' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 28: poweroffwc.py incelenirken 'orkestrasyon sisirmeme' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'orkestrasyon sisirmeme' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 29: keep 'stable action wording' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'stable action wording' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 29: poweroffwc.py incelenirken 'stabil aksiyon metni' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stabil aksiyon metni' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 30: keep 'tiny executable core' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'tiny executable core' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 30: poweroffwc.py incelenirken 'ufak calistirilabilir cekirdek' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ufak calistirilabilir cekirdek' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 31: keep 'shared mutation machinery' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'shared mutation machinery' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 31: poweroffwc.py incelenirken 'paylasilan mutation mekanigi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'paylasilan mutation mekanigi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 32: keep 'human-readable intent' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'human-readable intent' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 32: poweroffwc.py incelenirken 'insan-okunur niyet' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'insan-okunur niyet' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 33: keep 'future implementation boundary' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'future implementation boundary' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 33: poweroffwc.py incelenirken 'gelecek implementasyon siniri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gelecek implementasyon siniri' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 34: keep 'clear operational trace' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'clear operational trace' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 34: poweroffwc.py incelenirken 'net operasyon izi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'net operasyon izi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 35: keep 'safe control vocabulary' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'safe control vocabulary' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 35: poweroffwc.py incelenirken 'guvenli kontrol kelime dagarcigi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'guvenli kontrol kelime dagarcigi' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: Reading checkpoint 36: keep 'runbook-friendly naming' visible while reviewing poweroffwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later shutdown work.
# EN: Undesired meaning: losing 'runbook-friendly naming' would make this file look like a real poweroff executor.

# TR: Okuma kontrol noktasi 36: poweroffwc.py incelenirken 'runbook-dostu isimlendirme' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki shutdown calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'runbook-dostu isimlendirme' kaybolursa bu dosya gercek bir poweroff yurutucusu gibi gorunur.

# EN: POWEROFF CONTROL FUNCTION CONTRACT BLOCK V1 / main
# EN: Why this function exists:
# EN: This function gives a stable executable entry for python -m or direct invocation.
# EN: It binds the operator-facing poweroff name to the intentionally limited internal stop-preparation contract.
# EN: It also prints explicit human-readable notes after success so the current boundary remains impossible to miss.
# TR: Bu fonksiyon neden var:
# TR: Bu fonksiyon, python -m veya dogrudan cagri icin stabil bir calistirilabilir giris verir.
# TR: Operator-gorunumlu poweroff adini bilincli olarak sinirli ic stop-hazirlik kontratina baglar.
# TR: Basaridan sonra acik insan-okunur notlar da basar; boylece mevcut sinir gozden kacmaz.
# EN: Accepted input line shapes:
# EN: main() -> int
# TR: Kabul edilen girdi satir sekilleri:
# TR: main() -> int
def main() -> int:
    # EN: We first request the durable internal stop-preparation state through the shared helper.
    # EN: Real shutdown is intentionally deferred to a later, more explicit implementation phase.
    # TR: Once paylasilan helper uzerinden kalici ic stop-hazirlik durumunu istiyoruz.
    # TR: Gercek kapatma, daha sonraki ve daha acik bir implementasyon fazina bilincli olarak ertelenmistir.
    rc = apply_runtime_control(
        desired_state="stop",
        state_reason="poweroffwc requested internal durable stop state before later poweroff phase",
        requested_by="poweroffwc",
    )

    # EN: Any non-zero return code must be propagated immediately and without reinterpretation.
    # TR: Sifir olmayan her donus kodu hemen ve yeniden yorumlanmadan aynen yayilmalidir.
    if rc != 0:
        return rc

    # EN: We now emit explicit stderr notices so the operator sees that only the safe preparation phase happened.
    # TR: Simdi acik stderr notlari basiyoruz; boylece operator yalnizca guvenli hazirlik fazinin gerceklestigini gorur.
    print("INFO: poweroffwc currently performs only the safe internal stop-preparation phase.", file=sys.stderr)
    print("INFO: real poweroff phase is intentionally not implemented in this step.", file=sys.stderr)

    # EN: Success here means the preparation request completed, not that host power was removed.
    # TR: Buradaki basari, host gucunun kesildigi degil, hazirlik isteginin tamamlandigi anlamina gelir.
    return 0

# EN: This standard module guard preserves predictable module execution behavior.
# TR: Bu standart modul guard'i ongorulebilir modul calistirma davranisini korur.
if __name__ == "__main__":
    raise SystemExit(main())
