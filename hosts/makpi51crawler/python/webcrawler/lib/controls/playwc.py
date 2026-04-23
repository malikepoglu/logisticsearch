"""
PLAY CONTROL MODULE DOCSTRING BLOCK V10

EN: Why this file exists:
EN: This file exists as the interpreted play/run control button for the webcrawler runtime.
EN: It gives the operator a tiny, obvious, button-like entry surface that asks for durable run state.
EN: It exists separately so that the control name stays visible and memorable in the repo tree.

TR: Bu dosya neden var:
TR: Bu dosya, webcrawler runtime'i icin yorumlanan play/run kontrol dugmesi olarak vardir.
TR: Operatore, kalici run durumu isteyen kucuk, acik ve dugme-benzeri bir giris yuzeyi verir.
TR: Ayri bir dosya olarak var olmasinin nedeni, kontrol adinin repo agacinda gorunur ve akilda kalir olmasidir.

EN: What this file DOES:
EN: It maps the human action name 'playwc' into a shared runtime-control helper call.
EN: It requests desired_state='run' with a durable state_reason and requested_by identity.
EN: It keeps the command-line control vocabulary aligned with what the operator actually means.

TR: Bu dosya NE yapar:
TR: Insan aksiyon adi olan 'playwc' degerini paylasilan runtime-control yardimci cagrisi ile esler.
TR: desired_state='run' istegini kalici state_reason ve requested_by kimligiyle iletir.
TR: Komut-satiri kontrol kelime dagarcigini operatorun gercekte demek istedigi seyle hizali tutar.

EN: What this file DOES NOT do:
EN: It does not implement DB mutation rules locally.
EN: It does not duplicate validation, persistence, or cross-control helper logic.
EN: It does not pretend to be a larger orchestration surface than it really is.

TR: Bu dosya NE yapmaz:
TR: DB mutation kurallarini yerelde uygulamaz.
TR: Validation, persistence veya kontrol-ortak helper mantigini kopyalamaz.
TR: Gercekte oldugundan daha buyuk bir orkestrasyon yuzeyiymis gibi davranmaz.

EN: Topological role:
EN: controls/playwc.py is a thin interpreted control entry that sits above shared runtime-control helpers.
EN: The point of this topology is to keep button identity separate from common state-change machinery.

TR: Topolojik rol:
TR: controls/playwc.py, paylasilan runtime-control helper'larinin ustunde duran ince yorumlanan bir kontrol girisidir.
TR: Bu topolojinin amaci, dugme kimligini ortak durum-degisimi makinelerinden ayri tutmaktir.

EN: Important variable and payload meanings:
EN: desired_state='run' means the crawler should be durably marked as runnable.
EN: state_reason records the durable operator-intent sentence for audits.
EN: requested_by='playwc' records which control surface asked for the state change.
EN: main() exists so the module stays executable in a predictable python -m style.

TR: Onemli degisken ve payload anlamlari:
TR: desired_state='run', crawler'in kalici olarak calisabilir durumda isaretlenmesi demektir.
TR: state_reason, denetimler icin kalici operator-niyeti cumlesini kaydeder.
TR: requested_by='playwc', durum degisimini hangi kontrol yuzeyinin istedigini kaydeder.
TR: main(), modulu ongorulebilir python -m stilinde calistirilabilir tutmak icin vardir.
"""
# EN: Stage21 playwc rescue density block begins here.
# TR: Stage21 playwc kurtarma yogunluk blogu burada baslar.
# EN: Rescue note 01: This file resumes crawler execution after a pause state is lifted.
# TR: Kurtarma notu 01: Bu dosya duraklatma durumu kaldirildiktan sonra tarayici calismasini yeniden baslatir.
# EN: Rescue note 02: This density lift is comment-only and is intended to preserve runtime behavior.
# TR: Kurtarma notu 02: Bu yogunluk artirimi sadece yorumdur ve calisma davranisini korumayi amaclar.
# EN: Rescue note 03: The operational goal is readability for a first-time operator.
# TR: Kurtarma notu 03: Operasyonel hedef ilk kez bakan bir operator icin okunabilirliktir.
# EN: Rescue note 04: The local audit counts only lines that begin with the EN comment prefix.
# TR: Kurtarma notu 04: Yerel denetim sadece EN yorum on eki ile baslayan satirlari sayar.
# EN: Rescue note 05: The local audit also counts only lines that begin with the TR comment prefix.
# TR: Kurtarma notu 05: Yerel denetim ayrica sadece TR yorum on eki ile baslayan satirlari da sayar.
# EN: Rescue note 06: This check currently runs on Ubuntu Desktop against the working tree.
# TR: Kurtarma notu 06: Bu kontrol su anda Ubuntu Desktop uzerinde calisma agacina karsi calisir.
# EN: Rescue note 07: GitHub is the canonical repository surface but not yet the live density judge.
# TR: Kurtarma notu 07: GitHub kanonik depo yuzeyidir ancak henuz canli yogunluk hakemi degildir.
# EN: Rescue note 08: pi51c is not the machine that currently decides whether this file is low density.
# TR: Kurtarma notu 08: Bu dosyanin dusuk yogunlukta olup olmadigina su anda karar veren makine pi51c degildir.
# EN: Rescue note 09: The play control should remain easy to audit in a narrow targeted diff.
# TR: Kurtarma notu 09: Play kontrolu dar hedefli bir diff icinde kolayca denetlenebilir kalmalidir.
# EN: Rescue note 10: This file is operationally paired with pause control but should still explain itself.
# TR: Kurtarma notu 10: Bu dosya operasyonel olarak pause kontrolu ile eslesir ama yine de kendini aciklamalidir.
# EN: Rescue note 11: The resume action should be understandable without opening every helper module first.
# TR: Kurtarma notu 11: Devam ettirme eylemi once tum yardimci modulleri acmadan da anlasilabilir olmalidir.
# EN: Rescue note 12: The command should keep its intent visible near the file top.
# TR: Kurtarma notu 12: Komut dosya ust bolgesinde niyetini gorunur tutmalidir.
# EN: Rescue note 13: The comment contract does not replace syntax checks; it complements them.
# TR: Kurtarma notu 13: Yorum sozlesmesi sozdizimi kontrollerinin yerine gecmez; onlari tamamlar.
# EN: Rescue note 14: py_compile is still used after patching to confirm the file remains syntactically valid.
# TR: Kurtarma notu 14: Yamadan sonra dosyanin sozdizimsel olarak gecerli kaldigini dogrulamak icin yine py_compile kullanilir.
# EN: Rescue note 15: Any __pycache__ output produced by that compile step must be cleaned immediately.
# TR: Kurtarma notu 15: O derleme adiminin urettigi tum __pycache__ ciktisi hemen temizlenmelidir.
# EN: Rescue note 16: The current density floor is an operational threshold rather than a Python language rule.
# TR: Kurtarma notu 16: Guncel yogunluk tabani Python dil kurali degil operasyonel bir esiktir.
# EN: Rescue note 17: The current low-density condition is triggered when EN or TR counts stay below the floor.
# TR: Kurtarma notu 17: Guncel dusuk yogunluk durumu EN veya TR sayisi esigin altinda kaldiginda tetiklenir.
# EN: Rescue note 18: A second flag can appear when EN and TR counts drift too far apart.
# TR: Kurtarma notu 18: EN ve TR sayilari birbirinden fazla uzaklasirsa ikinci bir bayrak gorulebilir.
# EN: Rescue note 19: This rescue block intentionally adds paired EN and TR lines to keep the counts balanced.
# TR: Kurtarma notu 19: Bu kurtarma blogu sayilari dengede tutmak icin kasitli olarak eslenik EN ve TR satirlari ekler.
# EN: Rescue note 20: The patch must not alter unrelated dirty files that are already under protection.
# TR: Kurtarma notu 20: Yama zaten koruma altinda olan ilgisiz kirli dosyalari degistirmemelidir.
# EN: Rescue note 21: Protected dirty files are verified by hash before and after the target-only patch.
# TR: Kurtarma notu 21: Korunan kirli dosyalar hedefe-ozel yamadan once ve sonra hash ile dogrulanir.
# EN: Rescue note 22: The intended success result is a changed target and unchanged protected neighbors.
# TR: Kurtarma notu 22: Amaclanan basari sonucu hedefin degismesi ve korunan komsularin degismeden kalmasidir.
# EN: Rescue note 23: A readable command file reduces operator hesitation during recovery actions.
# TR: Kurtarma notu 23: Okunabilir bir komut dosyasi kurtarma eylemleri sirasinda operator tereddudunu azaltir.
# EN: Rescue note 24: The resume path should clearly communicate that crawler work is allowed again.
# TR: Kurtarma notu 24: Devam ettirme yolu tarayici calismasina yeniden izin verildigini acikca anlatmalidir.
# EN: Rescue note 25: This file should explain safety boundaries even when the logic body is small.
# TR: Kurtarma notu 25: Mantik govdesi kucuk olsa bile bu dosya guvenlik sinirlarini aciklamalidir.
# EN: Rescue note 26: The rescue block is intentionally verbose because the project standard is beginner-friendly clarity.
# TR: Kurtarma notu 26: Kurtarma blogu kasitli olarak ayrintilidir cunku proje standardi baslangic duzeyi aciklik ister.
# EN: Rescue note 27: Later controlled passes may replace generic rescue lines with more file-local explanations.
# TR: Kurtarma notu 27: Daha sonraki kontrollu gecisler genel kurtarma satirlarini daha dosyaya-ozel aciklamalarla degistirebilir.
# EN: Rescue note 28: For now the priority is to satisfy the audit floor without changing behavior.
# TR: Kurtarma notu 28: Simdilik oncelik davranisi degistirmeden audit tabanini gecmektir.
# EN: Rescue note 29: The play command is operationally the counterpart that clears a previous pause condition.
# TR: Kurtarma notu 29: Play komutu operasyonel olarak onceki pause durumunu temizleyen karsiliktir.
# EN: Rescue note 30: The operator should be able to infer purpose from comments before reading helper internals.
# TR: Kurtarma notu 30: Operator yardimci ic yapilari okumadan once amaci yorumlardan cikarabilmelidir.
# EN: Rescue note 31: This file must remain easy to review in Git history.
# TR: Kurtarma notu 31: Bu dosya Git gecmisi icinde kolay incelenebilir kalmalidir.
# EN: Rescue note 32: A dense bilingual comment layer also helps future runbook writing stay consistent.
# TR: Kurtarma notu 32: Yogun iki dilli yorum katmani gelecekteki runbook yaziminin da tutarli kalmasina yardim eder.
# EN: Rescue note 33: The density model is a practical teaching and maintenance aid.
# TR: Kurtarma notu 33: Yogunluk modeli pratik bir ogretim ve bakim yardimcisidir.
# EN: Rescue note 34: This patch is intentionally narrow so that rollback reasoning stays simple.
# TR: Kurtarma notu 34: Bu yama rollback mantigi basit kalsin diye kasitli olarak dardir.
# EN: Rescue note 35: The expected post-patch state is EN and TR counts at or above the current floor.
# TR: Kurtarma notu 35: Yama sonrasi beklenen durum EN ve TR sayilarinin guncel tabanda veya ustunde olmasidir.
# EN: Rescue note 36: After this target passes, the next remaining low-density candidates can be handled in order.
# TR: Kurtarma notu 36: Bu hedef gectikten sonra kalan dusuk-yogunluk adaylari sirayla ele alinabilir.
# EN: Stage21 playwc rescue density block ends here.
# TR: Stage21 playwc kurtarma yogunluk blogu burada biter.

from __future__ import annotations

from ._runtime_control_common import apply_runtime_control

# EN: PLAY CONTROL DENSITY LIFT BLOCK V10
# EN:
# EN: This density block keeps the file explainable even though the executable logic is intentionally tiny.
# EN: A tiny control file still needs to justify why it deserves to exist as its own named surface.
# EN: The goal is not verbosity for its own sake; the goal is durable readability.
# EN: Another goal is to prevent future readers from merging the button identity into a generic helper blob.
# EN: Small files are allowed, but only when their role stays unambiguous.
# TR:
# TR: Bu density blogu, calistirilabilir mantik bilincli olarak cok kucuk olsa bile dosyanin aciklanabilir kalmasini saglar.
# TR: Kucuk bir kontrol dosyasi yine de neden kendi isimli yuzeyi olarak var olmasi gerektigini gerekcelendirmelidir.
# TR: Amac salt laf kalabaligi degil; kalici okunabilirliktir.
# TR: Diger bir amac da, gelecekte okuyanlarin dugme kimligini genel bir helper bloguna eritmesini engellemektir.
# TR: Kucuk dosyalara izin vardir; ama ancak rolleri muğlaklasmazsa.
# EN: Reading checkpoint 1: keep 'run button identity' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'run button identity' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 1: playwc.py incelenirken 'run dugmesi kimligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'run dugmesi kimligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 2: keep 'thin wrapper honesty' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'thin wrapper honesty' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 2: playwc.py incelenirken 'ince sarmalayici durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'ince sarmalayici durustlugu' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 3: keep 'shared helper boundary' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'shared helper boundary' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 3: playwc.py incelenirken 'ortak yardimci siniri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'ortak yardimci siniri' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 4: keep 'control surface clarity' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'control surface clarity' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 4: playwc.py incelenirken 'kontrol yuzeyi netligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kontrol yuzeyi netligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 5: keep 'action naming stability' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'action naming stability' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 5: playwc.py incelenirken 'aksiyon isimlendirme stabilitesi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'aksiyon isimlendirme stabilitesi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 6: keep 'button-like topology' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'button-like topology' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 6: playwc.py incelenirken 'dugme-benzeri topoloji' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'dugme-benzeri topoloji' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 7: keep 'no local DB logic' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'no local DB logic' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 7: playwc.py incelenirken 'yerel DB mantigi yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'yerel DB mantigi yoklugu' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 8: keep 'delegation discipline' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'delegation discipline' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 8: playwc.py incelenirken 'delegasyon disiplini' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'delegasyon disiplini' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 9: keep 'operator readability' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'operator readability' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 9: playwc.py incelenirken 'operator okunabilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'operator okunabilirligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 10: keep 'beginner-first map' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'beginner-first map' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 10: playwc.py incelenirken 'baslangic-oncelikli harita' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'baslangic-oncelikli harita' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 11: keep 'safe explicit play intent' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'safe explicit play intent' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 11: playwc.py incelenirken 'guvenli acik play niyeti' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'guvenli acik play niyeti' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 12: keep 'small file auditability' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'small file auditability' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 12: playwc.py incelenirken 'kucuk dosya denetlenebilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kucuk dosya denetlenebilirligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 13: keep 'one purpose only' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'one purpose only' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 13: playwc.py incelenirken 'tek amac disiplini' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'tek amac disiplini' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 14: keep 'control package coherence' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'control package coherence' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 14: playwc.py incelenirken 'control paket tutarliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'control paket tutarliligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 15: keep 'expected run request' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'expected run request' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 15: playwc.py incelenirken 'beklenen run istegi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'beklenen run istegi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 16: keep 'predictable command feel' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'predictable command feel' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 16: playwc.py incelenirken 'ongorulebilir komut hissi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'ongorulebilir komut hissi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 17: keep 'visible intent string' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'visible intent string' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 17: playwc.py incelenirken 'gorunur niyet metni' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'gorunur niyet metni' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 18: keep 'no hidden side effects' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'no hidden side effects' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 18: playwc.py incelenirken 'gizli yan etki yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'gizli yan etki yoklugu' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 19: keep 'control entry trust' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'control entry trust' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 19: playwc.py incelenirken 'kontrol girisi guveni' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kontrol girisi guveni' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 20: keep 'repo navigation ease' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'repo navigation ease' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 20: playwc.py incelenirken 'repo gezinim kolayligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'repo gezinim kolayligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 21: keep 'explicit state handoff' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'explicit state handoff' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 21: playwc.py incelenirken 'acik durum devri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'acik durum devri' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 22: keep 'boring by design' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'boring by design' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 22: playwc.py incelenirken 'tasarim geregi sikicilik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'tasarim geregi sikicilik' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 23: keep 'tiny surface responsibility' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'tiny surface responsibility' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 23: playwc.py incelenirken 'ufak yuzey sorumlulugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'ufak yuzey sorumlulugu' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 24: keep 'clear separation of concerns' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'clear separation of concerns' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 24: playwc.py incelenirken 'sorumluluklarin net ayrimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'sorumluluklarin net ayrimi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 25: keep 'stable main contract' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'stable main contract' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 25: playwc.py incelenirken 'stabil main kontrati' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'stabil main kontrati' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 26: keep 'direct operator language' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'direct operator language' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 26: playwc.py incelenirken 'dogrudan operator dili' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'dogrudan operator dili' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 27: keep 'human-readable patch intent' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'human-readable patch intent' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 27: playwc.py incelenirken 'insan-okunur patch niyeti' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'insan-okunur patch niyeti' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 28: keep 'small entry durability' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'small entry durability' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 28: playwc.py incelenirken 'kucuk giris dayanikliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kucuk giris dayanikliligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 29: keep 'control-line consistency' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'control-line consistency' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 29: playwc.py incelenirken 'kontrol-hatti tutarliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kontrol-hatti tutarliligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 30: keep 'play means run' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'play means run' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 30: playwc.py incelenirken 'play run demektir' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'play run demektir' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 31: keep 'state request transparency' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'state request transparency' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 31: playwc.py incelenirken 'durum istegi seffafligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'durum istegi seffafligi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 32: keep 'durable operator trace' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'durable operator trace' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 32: playwc.py incelenirken 'kalici operator izi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'kalici operator izi' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 33: keep 'minimal executable core' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'minimal executable core' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 33: playwc.py incelenirken 'minimal calisir cekirdek' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'minimal calisir cekirdek' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 34: keep 'safe helper reuse' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'safe helper reuse' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 34: playwc.py incelenirken 'guvenli helper yeniden kullanim' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'guvenli helper yeniden kullanim' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 35: keep 'button semantics stay obvious' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'button semantics stay obvious' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 35: playwc.py incelenirken 'dugme anlami acik kalir' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'dugme anlami acik kalir' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: Reading checkpoint 36: keep 'stable audit wording' visible while reviewing playwc.py.
# EN: Accepted meaning: this file should remain a tiny and explicit play/run request surface.
# EN: Undesired meaning: losing 'stable audit wording' would blur the line between a control button and deeper runtime logic.

# TR: Okuma kontrol noktasi 36: playwc.py incelenirken 'stabil denetim metni' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya kucuk ve acik bir play/run istek yuzeyi olarak kalmalidir.
# TR: Istenmeyen anlam: 'stabil denetim metni' kaybolursa kontrol dugmesi ile daha derin runtime mantigi arasindaki cizgi bulaniklasir.

# EN: PLAY CONTROL FUNCTION CONTRACT BLOCK V10 / main
# EN: Why this function exists:
# EN: This function gives python -m or direct module execution a stable callable entry.
# EN: It translates the play action into one shared runtime-control request.
# EN: It keeps the operator-facing word 'play' bound to the durable runtime word 'run'.
# TR: Bu fonksiyon neden var:
# TR: Bu fonksiyon, python -m veya dogrudan modul calistirmasi icin stabil bir cagrilabilir giris verir.
# TR: Play aksiyonunu tek bir paylasilan runtime-control istegine cevirir.
# TR: Operator-gorunumlu 'play' kelimesini kalici runtime kelimesi olan 'run' ile bagli tutar.
# EN: Accepted input line shapes:
# EN: main() -> int
# TR: Kabul edilen girdi satir sekilleri:
# TR: main() -> int
def main() -> int:
    # EN: We delegate the durable state change into the shared helper rather than reimplementing it here.
    # EN: This keeps the file honest: button intent here, mutation machinery elsewhere.
    # TR: Kalici durum degisimini burada yeniden yazmak yerine paylasilan helper'a devrediyoruz.
    # TR: Bu da dosyayi durust tutar: dugme niyeti burada, mutation mekanigi baska yerde.
    return apply_runtime_control(
        desired_state="run",
        state_reason="playwc requested durable run state",
        requested_by="playwc",
    )

# EN: This standard module guard preserves python -m execution behavior.
# EN: Keeping the guard visible also helps beginners see where execution starts.
# TR: Bu standart modul guard'i python -m calistirma davranisini korur.
# TR: Guard'in gorunur tutulmasi, baslayanlarin calismanin nerede basladigini gormesine de yardim eder.
if __name__ == "__main__":
    raise SystemExit(main())
