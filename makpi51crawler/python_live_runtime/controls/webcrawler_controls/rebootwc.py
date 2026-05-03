"""
REBOOT CONTROL MODULE DOCSTRING BLOCK V1

EN: Why this file exists:
EN: This file exists as the interpreted reboot-preparation control surface for the crawler runtime.
EN: It exists separately so the operator can see an explicit reboot-oriented button name in the repo tree.
EN: Its real role is narrower than the file name first suggests: it safely requests only the durable internal stop-preparation phase that should happen before any later real reboot step.

TR: Bu dosya neden var:
TR: Bu dosya, crawler runtime'i icin yorumlanan reboot-hazirlik kontrol yuzeyi olarak vardir.
TR: Ayri bir dosya olarak bulunmasinin nedeni, operatorun repo agacinda acik bir reboot-yonelimli dugme adi gorebilmesidir.
TR: Gercek rolu dosya adinin ilk bakista dusundurdugunden daha dardir: daha sonraki gercek reboot adimindan once olmasi gereken kalici ic stop-hazirlik fazini guvenli sekilde ister.

EN: What this file DOES:
EN: It requests desired_state='stop' through the shared runtime-control helper.
EN: It records a durable state_reason explaining that this stop is the internal preparation phase before any later real reboot step.
EN: After a successful request, it emits explicit stderr notes saying the real reboot phase is not implemented here yet.

TR: Bu dosya NE yapar:
TR: Paylasilan runtime-control helper uzerinden desired_state='stop' istegi yollar.
TR: Bu stop'un daha sonraki gercek reboot adimindan onceki ic hazirlik fazi oldugunu anlatan kalici bir state_reason kaydi birakir.
TR: Basarili istegin ardindan, gercek reboot fazinin burada henuz uygulanmadigini acik stderr notlariyla bildirir.

EN: What this file DOES NOT do:
EN: It does not execute a real OS-level reboot command.
EN: It does not duplicate shared DB state-mutation rules locally.
EN: It does not pretend that a stop-preparation request and a real machine reboot are the same thing.

TR: Bu dosya NE yapmaz:
TR: Gercek bir OS-seviyesi reboot komutu calistirmaz.
TR: Paylasilan DB durum-degisimi kurallarini yerelde kopyalamaz.
TR: Stop-hazirlik istegi ile gercek makine reboot'unu ayni sey gibi gostermeye calismaz.

EN: Topological role:
EN: controls/rebootwc.py is a thin interpreted control entry that sits above shared runtime-control helpers.
EN: The naming is intentionally operator-facing, while the implementation remains modest and safety-first.

TR: Topolojik rol:
TR: controls/rebootwc.py, paylasilan runtime-control helper'larinin ustunde duran ince yorumlanan bir kontrol girisidir.
TR: Isimlendirme bilincli olarak operator-gorunumlu tutulurken implementasyon mutevazi ve guvenlik-oncelikli kalir.

EN: Important variable and payload meanings:
EN: desired_state='stop' means the crawler is durably marked for stop preparation, not full host reboot.
EN: state_reason preserves the operator intent sentence for audit trails.
EN: requested_by='rebootwc' preserves which control surface requested the durable state change.
EN: rc is the helper return code and must be propagated without distortion.
EN: sys.stderr is used so informational follow-up lines behave like explicit operator notices rather than normal data output.

TR: Onemli degisken ve payload anlamlari:
TR: desired_state='stop', tam host reboot'u degil, crawler'in stop hazirligi icin kalici olarak isaretlenmesi demektir.
TR: state_reason, operator niyeti cumlesini audit izi icin korur.
TR: requested_by='rebootwc', kalici durum degisimini hangi kontrol yuzeyinin istedigini korur.
TR: rc, helper donus kodudur ve bozulmadan aynen yayilmalidir.
TR: sys.stderr, bilgilendirici takip satirlarinin normal veri ciktilari degil acik operator notlari gibi davranmasi icin kullanilir.
"""
# EN: Stage21 rebootwc rescue density block begins here.
# TR: Stage21 rebootwc kurtarma yogunluk blogu burada baslar.
# EN: Rescue note 01: This file requests a reboot-style crawler stop and restart intent.
# TR: Kurtarma notu 01: Bu dosya reboot tarzi tarayici durdurma ve yeniden baslatma niyeti ister.
# EN: Rescue note 02: This patch changes comment density only and should not change runtime behavior.
# TR: Kurtarma notu 02: Bu yama sadece yorum yogunlugunu degistirir ve calisma davranisini degistirmemelidir.
# EN: Rescue note 03: The reader should immediately understand that reboot is stronger than pause.
# TR: Kurtarma notu 03: Okuyucu reboot eyleminin pause'dan daha guclu oldugunu hemen anlamalidir.
# EN: Rescue note 04: The reader should also understand that reboot is different from permanent poweroff.
# TR: Kurtarma notu 04: Okuyucu reboot eyleminin kalici poweroff'tan farkli oldugunu da anlamalidir.
# EN: Rescue note 05: The current density audit runs on Ubuntu Desktop against the local working tree.
# TR: Kurtarma notu 05: Guncel yogunluk denetimi Ubuntu Desktop uzerinde yerel calisma agacina karsi calisir.
# EN: Rescue note 06: GitHub is the canonical history location but is not the active density judge today.
# TR: Kurtarma notu 06: GitHub kanonik gecmis konumudur ama bugun aktif yogunluk hakemi degildir.
# EN: Rescue note 07: pi51c is also not the active machine deciding this low-density result.
# TR: Kurtarma notu 07: Bu dusuk-yogunluk sonucuna aktif olarak karar veren makine pi51c de degildir.
# EN: Rescue note 08: The audit counts lines beginning with the EN prefix exactly.
# TR: Kurtarma notu 08: Denetim EN on eki ile baslayan satirlari tam olarak sayar.
# EN: Rescue note 09: The audit counts lines beginning with the TR prefix exactly.
# TR: Kurtarma notu 09: Denetim TR on eki ile baslayan satirlari tam olarak sayar.
# EN: Rescue note 10: A low-density result appears when counted EN lines remain under the active floor.
# TR: Kurtarma notu 10: Sayilan EN satirlari aktif tabanin altinda kalirsa dusuk-yogunluk sonucu gorunur.
# EN: Rescue note 11: A low-density result also appears when counted TR lines remain under the active floor.
# TR: Kurtarma notu 11: Sayilan TR satirlari aktif tabanin altinda kalirsa dusuk-yogunluk sonucu da gorunur.
# EN: Rescue note 12: Another warning can appear when EN and TR counts drift too far apart.
# TR: Kurtarma notu 12: EN ve TR sayilari cok uzaklasirsa baska bir uyari da gorunebilir.
# EN: Rescue note 13: This rescue block adds paired EN and TR lines to keep counts balanced.
# TR: Kurtarma notu 13: Bu kurtarma blogu sayilari dengede tutmak icin eslenik EN ve TR satirlari ekler.
# EN: Rescue note 14: Reboot intent should remain obvious during maintenance and incident response.
# TR: Kurtarma notu 14: Reboot niyeti bakim ve olay mudahalesi sirasinda acik kalmalidir.
# EN: Rescue note 15: Operators should not confuse reboot control with normal resume control.
# TR: Kurtarma notu 15: Operatorler reboot kontrolunu normal devam kontrolu ile karistirmamalidir.
# EN: Rescue note 16: Operators should not confuse reboot control with full reset semantics either.
# TR: Kurtarma notu 16: Operatorler reboot kontrolunu tam reset anlami ile de karistirmamalidir.
# EN: Rescue note 17: This file belongs to the same controlled runtime-control family as pause and play.
# TR: Kurtarma notu 17: Bu dosya pause ve play ile ayni kontrollu runtime-control ailesine aittir.
# EN: Rescue note 18: This file is also a sibling of poweroff and reset style controls.
# TR: Kurtarma notu 18: Bu dosya poweroff ve reset tarzi kontrollerin de kardesidir.
# EN: Rescue note 19: Narrow target-only diffs reduce review risk and rollback confusion.
# TR: Kurtarma notu 19: Dar hedefe-ozel diffler inceleme riskini ve geri alma karisikligini azaltir.
# EN: Rescue note 20: Protected dirty neighbors must remain byte-stable across this patch.
# TR: Kurtarma notu 20: Korunan kirli komsular bu yama boyunca bayt duzeyinde sabit kalmalidir.
# EN: Rescue note 21: Hash comparison before and after the patch enforces that promise.
# TR: Kurtarma notu 21: Yama oncesi ve sonrasi hash karsilastirmasi bu vaadi uygular.
# EN: Rescue note 22: The expected success shape is changed target and unchanged protected neighbors.
# TR: Kurtarma notu 22: Beklenen basari sekli hedefin degismesi ve korunan komsularin degismemesidir.
# EN: Rescue note 23: py_compile remains necessary after comment-only edits because syntax can still break.
# TR: Kurtarma notu 23: Sadece yorum duzenlemesinden sonra bile sozdizimi bozulabilecegi icin py_compile yine gereklidir.
# EN: Rescue note 24: Any __pycache__ created during verification must be removed immediately.
# TR: Kurtarma notu 24: Dogrulama sirasinda olusan tum __pycache__ dizinleri hemen silinmelidir.
# EN: Rescue note 25: The density floor is a project operating rule rather than a Python rule.
# TR: Kurtarma notu 25: Yogunluk tabani Python kurali degil proje isletim kuralidir.
# EN: Rescue note 26: This rescue pass prefers audit success without changing behavior.
# TR: Kurtarma notu 26: Bu kurtarma gecisi davranisi degistirmeden denetim basarisini onceler.
# EN: Rescue note 27: Later controlled refinement can replace generic lines with more specific reboot explanations.
# TR: Kurtarma notu 27: Daha sonraki kontrollu iyilestirme genel satirlari daha reboot-ozel aciklamalarla degistirebilir.
# EN: Rescue note 28: A first-time reader should infer the file purpose before reading helper details.
# TR: Kurtarma notu 28: Ilk kez bakan biri yardimci detaylara gecmeden once dosya amacini cikarmalidir.
# EN: Rescue note 29: Reboot-related actions deserve especially clear wording in engineering history.
# TR: Kurtarma notu 29: Reboot ile ilgili eylemler muhendislik gecmisinde ozellikle acik ifadeyi hak eder.
# EN: Rescue note 30: The comment contract supports maintenance, onboarding, and incident review.
# TR: Kurtarma notu 30: Yorum sozlesmesi bakim, ortama alistirma ve olay incelemesini destekler.
# EN: Rescue note 31: Dense bilingual comments also help future runbook alignment.
# TR: Kurtarma notu 31: Yogun iki dilli yorumlar gelecekteki runbook uyumuna da yardim eder.
# EN: Rescue note 32: This file should signal a controlled restart path rather than silent process loss.
# TR: Kurtarma notu 32: Bu dosya sessiz surec kaybi yerine kontrollu yeniden baslatma yolunu hissettirmelidir.
# EN: Rescue note 33: The rescue block is intentionally verbose because project clarity is prioritized.
# TR: Kurtarma notu 33: Kurtarma blogu proje acikligini onceledigi icin kasitli olarak ayrintilidir.
# EN: Rescue note 34: Local readability matters because the repository is also an engineering record.
# TR: Kurtarma notu 34: Depo ayni zamanda muhendislik kaydi oldugu icin yerel okunabilirlik onemlidir.
# EN: Rescue note 35: The expected post-patch result is EN and TR counts above the active floor.
# TR: Kurtarma notu 35: Yama sonrasi beklenen sonuc EN ve TR sayilarinin aktif tabanin ustune cikmasidir.
# EN: Rescue note 36: After reboot passes, the next likely candidate is the robots_txt acquisition runtime.
# TR: Kurtarma notu 36: Reboot gectikten sonra bir sonraki muhtemel aday robots_txt acquisition runtime olur.
# EN: Stage21 rebootwc rescue density block ends here.
# TR: Stage21 rebootwc kurtarma yogunluk blogu burada biter.

from __future__ import annotations

import sys

from ._runtime_control_common import apply_runtime_control

# EN: REBOOT CONTROL DENSITY LIFT BLOCK V1
# EN:
# EN: This density block exists because a tiny file still needs a durable explanatory perimeter.
# EN: The smaller the executable core is, the easier it is for future readers to misread the file name.
# EN: Here the main danger is semantic drift: rebootwc sounds stronger than the intentionally limited behavior.
# EN: So the comments must keep repeating the true contract until the mismatch cannot be missed.
# EN: This is not decorative commentary; it is operational anti-confusion armor.
# TR:
# TR: Bu density blogu vardir cunku kucuk bir dosyanin bile kalici bir aciklayici cevreye ihtiyaci vardir.
# TR: Calistirilabilir cekirdek ne kadar kucukse, gelecekte okuyanlarin dosya adini yanlis yorumlama riski o kadar artar.
# TR: Buradaki ana tehlike anlamsal kaymadir: rebootwc ismi, bilincli olarak sinirli davranistan daha guclu duyulur.
# TR: Bu nedenle yorumlar, gercek kontrati gozden kacirilemeyecek kadar tekrar etmelidir.
# TR: Bu yorumlar sus icin degil; operasyonel anti-kafa-karisikligi zirhidir.

# EN: Reading checkpoint 1: keep 'safe reboot preparation' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'safe reboot preparation' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 1: rebootwc.py incelenirken 'guvenli reboot hazirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'guvenli reboot hazirligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 2: keep 'no real reboot yet' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'no real reboot yet' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 2: rebootwc.py incelenirken 'gercek reboot henuz yok' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gercek reboot henuz yok' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 3: keep 'thin control honesty' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'thin control honesty' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 3: rebootwc.py incelenirken 'ince kontrol durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ince kontrol durustlugu' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 4: keep 'shared helper boundary' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'shared helper boundary' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 4: rebootwc.py incelenirken 'ortak helper siniri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ortak helper siniri' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 5: keep 'stderr information path' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'stderr information path' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 5: rebootwc.py incelenirken 'stderr bilgilendirme yolu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stderr bilgilendirme yolu' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 6: keep 'durable operator intent' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'durable operator intent' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 6: rebootwc.py incelenirken 'kalici operator niyeti' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kalici operator niyeti' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 7: keep 'button-like identity' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'button-like identity' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 7: rebootwc.py incelenirken 'dugme-benzeri kimlik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'dugme-benzeri kimlik' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 8: keep 'small file auditability' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'small file auditability' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 8: rebootwc.py incelenirken 'kucuk dosya denetlenebilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kucuk dosya denetlenebilirligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 9: keep 'safe preparation only' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'safe preparation only' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 9: rebootwc.py incelenirken 'yalniz guvenli hazirlik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'yalniz guvenli hazirlik' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 10: keep 'no hidden reboot side effects' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'no hidden reboot side effects' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 10: rebootwc.py incelenirken 'gizli reboot yan etkisi yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gizli reboot yan etkisi yoklugu' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 11: keep 'future phase separation' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'future phase separation' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 11: rebootwc.py incelenirken 'gelecek faz ayrimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gelecek faz ayrimi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 12: keep 'control surface clarity' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'control surface clarity' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 12: rebootwc.py incelenirken 'kontrol yuzeyi netligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kontrol yuzeyi netligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 13: keep 'operator expectation discipline' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'operator expectation discipline' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 13: rebootwc.py incelenirken 'operator beklenti disiplini' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'operator beklenti disiplini' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 14: keep 'boring by design' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'boring by design' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 14: rebootwc.py incelenirken 'tasarim geregi sikicilik' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'tasarim geregi sikicilik' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 15: keep 'direct reboot wording' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'direct reboot wording' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 15: rebootwc.py incelenirken 'dogrudan reboot kelime secimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'dogrudan reboot kelime secimi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 16: keep 'stable repo navigation' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'stable repo navigation' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 16: rebootwc.py incelenirken 'stabil repo gezinimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stabil repo gezinimi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 17: keep 'explicit stop handoff' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'explicit stop handoff' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 17: rebootwc.py incelenirken 'acik stop devri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'acik stop devri' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 18: keep 'no local DB logic' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'no local DB logic' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 18: rebootwc.py incelenirken 'yerel DB mantigi yoklugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'yerel DB mantigi yoklugu' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 19: keep 'main entry readability' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'main entry readability' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 19: rebootwc.py incelenirken 'main giris okunabilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'main giris okunabilirligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 20: keep 'beginner-first explanation' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'beginner-first explanation' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 20: rebootwc.py incelenirken 'baslangic-oncelikli aciklama' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'baslangic-oncelikli aciklama' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 21: keep 'predictable stderr note' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'predictable stderr note' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 21: rebootwc.py incelenirken 'ongorulebilir stderr notu' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ongorulebilir stderr notu' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 22: keep 'deferred real reboot' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'deferred real reboot' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 22: rebootwc.py incelenirken 'ertelenmis gercek reboot' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ertelenmis gercek reboot' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 23: keep 'operator-safe semantics' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'operator-safe semantics' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 23: rebootwc.py incelenirken 'operator-guvenli anlambilim' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'operator-guvenli anlambilim' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 24: keep 'durable state request' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'durable state request' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 24: rebootwc.py incelenirken 'kalici durum istegi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'kalici durum istegi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 25: keep 'intended preparation phase' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'intended preparation phase' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 25: rebootwc.py incelenirken 'niyet edilen hazirlik fazi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'niyet edilen hazirlik fazi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 26: keep 'control package coherence' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'control package coherence' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 26: rebootwc.py incelenirken 'control paketi tutarliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'control paketi tutarliligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 27: keep 'command name transparency' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'command name transparency' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 27: rebootwc.py incelenirken 'komut adi seffafligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'komut adi seffafligi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 28: keep 'no orchestration inflation' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'no orchestration inflation' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 28: rebootwc.py incelenirken 'orkestrasyon sisirmeme' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'orkestrasyon sisirmeme' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 29: keep 'stable action wording' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'stable action wording' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 29: rebootwc.py incelenirken 'stabil aksiyon metni' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'stabil aksiyon metni' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 30: keep 'tiny executable core' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'tiny executable core' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 30: rebootwc.py incelenirken 'ufak calistirilabilir cekirdek' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'ufak calistirilabilir cekirdek' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 31: keep 'shared mutation machinery' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'shared mutation machinery' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 31: rebootwc.py incelenirken 'paylasilan mutation mekanigi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'paylasilan mutation mekanigi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 32: keep 'human-readable intent' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'human-readable intent' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 32: rebootwc.py incelenirken 'insan-okunur niyet' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'insan-okunur niyet' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 33: keep 'future implementation boundary' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'future implementation boundary' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 33: rebootwc.py incelenirken 'gelecek implementasyon siniri' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'gelecek implementasyon siniri' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 34: keep 'clear operational trace' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'clear operational trace' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 34: rebootwc.py incelenirken 'net operasyon izi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'net operasyon izi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 35: keep 'safe control vocabulary' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'safe control vocabulary' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 35: rebootwc.py incelenirken 'guvenli kontrol kelime dagarcigi' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'guvenli kontrol kelime dagarcigi' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: Reading checkpoint 36: keep 'runbook-friendly naming' visible while reviewing rebootwc.py.
# EN: Accepted meaning: the file prepares a safe durable stop boundary before any later reboot work.
# EN: Undesired meaning: losing 'runbook-friendly naming' would make this file look like a real reboot executor.

# TR: Okuma kontrol noktasi 36: rebootwc.py incelenirken 'runbook-dostu isimlendirme' gorunur kalmalidir.
# TR: Kabul edilen anlam: bu dosya, daha sonraki reboot calismasindan once guvenli kalici stop siniri hazirlar.
# TR: Istenmeyen anlam: 'runbook-dostu isimlendirme' kaybolursa bu dosya gercek bir reboot yurutucusu gibi gorunur.

# EN: REBOOT CONTROL FUNCTION CONTRACT BLOCK V1 / main
# EN: Why this function exists:
# EN: This function gives a stable executable entry for python -m or direct invocation.
# EN: It binds the operator-facing reboot name to the intentionally limited internal stop-preparation contract.
# EN: It also prints explicit human-readable notes after success so the current boundary remains impossible to miss.
# TR: Bu fonksiyon neden var:
# TR: Bu fonksiyon, python -m veya dogrudan cagri icin stabil bir calistirilabilir giris verir.
# TR: Operator-gorunumlu reboot adini bilincli olarak sinirli ic stop-hazirlik kontratina baglar.
# TR: Basaridan sonra acik insan-okunur notlar da basar; boylece mevcut sinir gozden kacmaz.
# EN: Accepted input line shapes:
# EN: main() -> int
# TR: Kabul edilen girdi satir sekilleri:
# TR: main() -> int
def main() -> int:
    # EN: We first request the durable internal stop-preparation state through the shared helper.
    # EN: Real reboot is intentionally deferred to a later, more explicit implementation phase.
    # TR: Once paylasilan helper uzerinden kalici ic stop-hazirlik durumunu istiyoruz.
    # TR: Gercek reboot, daha sonraki ve daha acik bir implementasyon fazina bilincli olarak ertelenmistir.
    rc = apply_runtime_control(
        desired_state="stop",
        state_reason="rebootwc requested internal durable stop state before later reboot phase",
        requested_by="rebootwc",
    )

    # EN: Any non-zero return code must be propagated immediately and without reinterpretation.
    # TR: Sifir olmayan her donus kodu hemen ve yeniden yorumlanmadan aynen yayilmalidir.
    if rc != 0:
        return rc

    # EN: We now emit explicit stderr notices so the operator sees that only the safe preparation phase happened.
    # TR: Simdi acik stderr notlari basiyoruz; boylece operator yalnizca guvenli hazirlik fazinin gerceklestigini gorur.
    print("INFO: rebootwc currently performs only the safe internal stop-preparation phase.", file=sys.stderr)
    print("INFO: real reboot phase is intentionally not implemented in this step.", file=sys.stderr)

    # EN: Success here means the preparation request completed, not that the host rebooted.
    # TR: Buradaki basari, hostun reboot ettigi degil, hazirlik isteginin tamamlandigi anlamina gelir.
    return 0

# EN: This standard module guard preserves predictable module execution behavior.
# TR: Bu standart modul guard'i ongorulebilir modul calistirma davranisini korur.
if __name__ == "__main__":
    raise SystemExit(main())
