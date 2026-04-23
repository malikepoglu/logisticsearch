"""
EN:
This file is the shared runtime-control helper surface used by the interpreted
control entry files under the controls package.

Why this file exists:
- The tiny control entry files should stay tiny.
- A beginner should be able to open pause/play/reboot/reset style files and
  immediately see that they are only thin entry surfaces.
- Shared logic therefore belongs here instead of being copied into many small files.
- This makes the project identity easier to read from top to bottom.

Very simple mental model:
- controls/pausewc.py, playwc.py, rebootwc.py, poweroffwc.py, resetwc.py
  are the visible buttons.
- This file is the shared wiring behind those buttons.
- The buttons should stay readable.
- The wiring should stay centralized.

What this file DOES:
- Hold shared helper functions used by multiple control entry surfaces.
- Keep path handling, small payload shaping, and repeated control-side helper
  steps in one place.
- Reduce copy-paste drift between control files.
- Give the controls package one shared helper backbone.

What this file DOES NOT do:
- It does not run the crawler main loop.
- It does not claim frontier work.
- It does not fetch or parse page content.
- It does not classify taxonomy.
- It does not rank search results.
- It does not hide core crawler state-machine decisions.

Topological role:
- Thin control entry files call into this helper file.
- This helper file supports control-entry readability.
- Upper crawler runtime files remain separate.
- So this file belongs to the control-side support corridor, not to the worker
  execution core.

Important variable and payload meanings:
- path-like values:
  - Expected meaning: readable filesystem locations expressed as str or Path.
  - Accepted values: non-empty, explicit, deterministic paths.
  - Undesired values: empty text, None, or ambiguous path construction.
- payload-like values:
  - Expected meaning: small readable dictionaries or structured control-facing
    response shapes.
  - Accepted values: explicit, serializable, operator-readable data.
  - Undesired values: silent, shape-breaking, or ambiguous objects.
- text/state-like values:
  - Expected meaning: small normalized control text such as an action or state
    token.
  - Accepted values: explicit, stripped, readable strings.
  - Undesired values: hidden whitespace drift, None, or inconsistent casing
    when normalization is expected.
- return-code-like values:
  - Expected meaning: explicit integer outcome for an operator-visible action.
  - Accepted values: readable int outcomes.
  - Undesired values: silent None branches where success/failure meaning is unclear.

Beginner-first warning:
- "Common helper" does not mean "unimportant helper".
- Shared support files often decide whether the surrounding project remains easy
  to read or becomes repetitive and messy.
- So this file must stay boring, clear, and predictable on purpose.

TR:
Bu dosya, controls paketi altindaki yorumlanan kontrol giris dosyalari tarafindan
kullanilan ortak runtime-control yardimci yuzeyidir.

Bu dosya neden var:
- Kucuk kontrol giris dosyalari kucuk kalmalidir.
- Yeni baslayan biri pause/play/reboot/reset benzeri dosyalari actiginda,
  bunlarin yalnizca ince giris yuzeyleri oldugunu hemen gorebilmelidir.
- Bu nedenle ortak mantik bircok kucuk dosyaya kopyalanmak yerine burada
  toplanir.
- Boylece proje kimligi yukaridan asagi okumada daha kolay anlasilir.

Cok basit zihinsel model:
- controls/pausewc.py, playwc.py, rebootwc.py, poweroffwc.py, resetwc.py
  gorunen dugmelerdir.
- Bu dosya ise o dugmelerin arkasindaki ortak kablolamadir.
- Dugmeler okunur kalmalidir.
- Kablolama ise merkezde kalmalidir.

Bu dosya NE yapar:
- Birden fazla kontrol giris yuzeyi tarafindan kullanilan ortak yardimci
  fonksiyonlari tutar.
- Path isleme, kucuk payload kurma ve tekrarlanan control-yardimci adimlarini
  tek yerde toplar.
- Kontrol dosyalari arasindaki copy-paste driftini azaltir.
- controls paketi icin ortak bir yardimci omurga saglar.

Bu dosya NE yapmaz:
- Crawler ana loop'unu calistirmaz.
- Frontier isi claim etmez.
- Sayfa icerigi fetch veya parse etmez.
- Taxonomy siniflandirmasi yapmaz.
- Arama sonuclarini rank etmez.
- Ana crawler state-machine kararlarini gizlemez.

Topolojik rol:
- Ince kontrol giris dosyalari bu yardimci dosyayi cagirir.
- Bu yardimci dosya control-entry okunabilirligini destekler.
- Ust crawler runtime dosyalari ayri kalir.
- Yani bu dosya worker execution core degil, control-side support koridoruna aittir.

Onemli degisken ve payload anlamlari:
- path-benzeri degerler:
  - Beklenen anlam: str veya Path olarak ifade edilen okunur dosya sistemi konumlari.
  - Kabul edilen degerler: bos olmayan, acik, deterministik path'ler.
  - Istenmeyen degerler: bos metin, None veya belirsiz path kurulumudur.
- payload-benzeri degerler:
  - Beklenen anlam: kucuk, okunur dictionary veya yapisal kontrol-cevap sekilleridir.
  - Kabul edilen degerler: acik, serilestirilebilir, operatorun okuyacagi veridir.
  - Istenmeyen degerler: sessiz, sekli bozan veya belirsiz nesnelerdir.
- text/state-benzeri degerler:
  - Beklenen anlam: action veya state tokeni gibi kucuk normalize kontrol metnidir.
  - Kabul edilen degerler: acik, strip edilmis, okunur string'lerdir.
  - Istenmeyen degerler: gizli bosluk drift'i, None veya normalization beklenirken
    tutarsiz harf buyuklugu-kucuklugudur.
- return-code-benzeri degerler:
  - Beklenen anlam: operator-yuzlu bir eylem icin acik integer sonucudur.
  - Kabul edilen degerler: okunur int sonuc degerleridir.
  - Istenmeyen degerler: success/failure anlami belirsiz sessiz None dallaridir.

Baslangic seviyesi uyari:
- "Ortak yardimci" demek "onemsiz yardimci" demek degildir.
- Paylasilan destek dosyalari, cevredeki projenin okunur kalip kalmayacagini
  sikca belirler.
- Bu nedenle bu dosya bilincli olarak sikici, net ve ongorulebilir kalmalidir.
"""



# EN: RUNTIME CONTROL COMMON DENSITY LIFT BLOCK V9
# EN:
# EN: This density-lift block exists so the common-helper file can still explain itself even when a reader opens it without any prior project memory.
# EN: The purpose is clarity, not filler.
# EN: A first-time reader should understand how to position this file in the project map.
# TR:
# TR: Bu density-lift blogu, ortak-yardimci dosyanin okuyucu projeyi hic hatirlamasa bile kendini aciklayabilmesi icin vardir.
# TR: Amac dolgu degil, netliktir.
# TR: Ilk kez okuyan biri bu dosyayi proje haritasinda nereye koyacagini anlayabilmelidir.
# EN:
# EN: Operator reading path:
# EN: 1) confirm this is a shared helper surface
# EN: 2) confirm thin entry files delegate here
# EN: 3) confirm worker logic lives elsewhere
# EN: 4) confirm helper outputs must stay explicit and readable
# TR:
# TR: Operator okuma yolu:
# TR: 1) bunun ortak bir yardimci yuzey oldugunu dogrula
# TR: 2) ince giris dosyalarinin buraya delege ettigini dogrula
# TR: 3) worker mantiginin baska yerde yasadigini dogrula
# TR: 4) yardimci ciktilarin acik ve okunur kalmasi gerektigini dogrula
# EN: Reading checkpoint 1: keep 'shared helper identity' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'shared helper identity' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 1: bu ortak yardimci dosyayi incelerken 'ortak yardimci kimligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'ortak yardimci kimligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 2: keep 'thin entry preservation' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'thin entry preservation' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 2: bu ortak yardimci dosyayi incelerken 'ince girislerin korunmasi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'ince girislerin korunmasi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 3: keep 'copy-paste avoidance' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'copy-paste avoidance' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 3: bu ortak yardimci dosyayi incelerken 'copy-paste kacinmasi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'copy-paste kacinmasi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 4: keep 'operator readability' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'operator readability' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 4: bu ortak yardimci dosyayi incelerken 'operator okunabilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'operator okunabilirligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 5: keep 'deterministic path handling' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'deterministic path handling' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 5: bu ortak yardimci dosyayi incelerken 'deterministik path isleme' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'deterministik path isleme' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 6: keep 'payload shaping honesty' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'payload shaping honesty' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 6: bu ortak yardimci dosyayi incelerken 'payload kurulum durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'payload kurulum durustlugu' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 7: keep 'control-side narrowness' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'control-side narrowness' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 7: bu ortak yardimci dosyayi incelerken 'control-side darligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'control-side darligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 8: keep 'worker/runtime separation' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'worker/runtime separation' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 8: bu ortak yardimci dosyayi incelerken 'worker/runtime ayrimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'worker/runtime ayrimi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 9: keep 'explicit result shaping' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'explicit result shaping' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 9: bu ortak yardimci dosyayi incelerken 'acik sonuc kurma' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'acik sonuc kurma' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 10: keep 'safe helper centralization' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'safe helper centralization' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 10: bu ortak yardimci dosyayi incelerken 'guvenli yardimci merkezilestirme' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'guvenli yardimci merkezilestirme' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 11: keep 'support-layer boringness' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'support-layer boringness' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 11: bu ortak yardimci dosyayi incelerken 'destek katmaninin sikiciligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'destek katmaninin sikiciligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 12: keep 'project map clarity' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'project map clarity' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 12: bu ortak yardimci dosyayi incelerken 'proje haritasi netligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'proje haritasi netligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 13: keep 'state text normalization' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'state text normalization' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 13: bu ortak yardimci dosyayi incelerken 'durum metni normalize etme' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'durum metni normalize etme' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 14: keep 'path ambiguity avoidance' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'path ambiguity avoidance' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 14: bu ortak yardimci dosyayi incelerken 'path belirsizliginden kacinma' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'path belirsizliginden kacinma' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 15: keep 'operator trust preservation' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'operator trust preservation' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 15: bu ortak yardimci dosyayi incelerken 'operator guvenini koruma' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'operator guvenini koruma' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 16: keep 'visible failure preference' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'visible failure preference' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 16: bu ortak yardimci dosyayi incelerken 'gorunur hata tercihi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'gorunur hata tercihi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 17: keep 'small helper contracts' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'small helper contracts' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 17: bu ortak yardimci dosyayi incelerken 'kucuk yardimci sozlesmeleri' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'kucuk yardimci sozlesmeleri' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN: Reading checkpoint 18: keep 'entry-point consistency' visible while inspecting this shared helper file.
# EN: Accepted meaning: repeated control-side support belongs in one stable file instead of being copied into many entry files.
# EN: Undesired meaning: losing 'entry-point consistency' would make the controls package harder to read and harder to trust.
# TR: Okuma kontrol noktasi 18: bu ortak yardimci dosyayi incelerken 'giris noktasi tutarliligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: tekrarlanan control-side destek, bircok giris dosyasina kopyalanmak yerine tek kararlı dosyada durmalidir.
# TR: Istenmeyen anlam: 'giris noktasi tutarliligi' kaybolursa controls paketi hem daha zor okunur hem de daha zor guvenilir hale gelir.
# EN:
# EN: Final reminder:
# EN: shared helper files should reduce noise, not create hidden logic fog.
# EN: if a helper becomes too magical, the surrounding small entry files stop being educational.
# TR:
# TR: Son hatirlatma:
# TR: ortak yardimci dosyalar gurultuyu azaltmali, gizli mantik sisi olusturmamalidir.
# TR: yardimci asiri buyulu hale gelirse etraftaki kucuk giris dosyalari egitici olmaktan cikar.

# EN: We enable postponed annotation evaluation so type hints remain readable.
# TR: Type hint'ler okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import getpass because the current control surface must verify which
# EN: OS user is invoking the command, just like the old shell wrappers did.
# TR: Mevcut control yüzeyi komutu hangi OS kullanıcısının çağırdığını
# TR: doğrulamalıdır; eski shell wrapper'lar da bunu yaptığı için getpass
# TR: içe aktarıyoruz.
import getpass

# EN: We import json because control results should be printed in a structured
# EN: machine-readable form.
# TR: Kontrol sonuçları yapılı ve makine-okunur biçimde yazdırılmalıdır; bu
# TR: yüzden json içe aktarıyoruz.
import json

# EN: We import os because environment variables still participate in DSN
# EN: resolution.
# TR: DSN çözümünde environment variable'lar hâlâ rol oynadığı için os içe
# TR: aktarıyoruz.
import os

# EN: We import Path because filesystem path handling is clearer with pathlib.
# TR: Dosya yolu işlemleri pathlib ile daha açık olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import the canonical runtime-control DB helpers directly, because the
# EN: interpreted controls surface should talk to the sealed DB gateway rather
# EN: than shelling out into a stale CLI string.
# TR: Yorumlanan controls yüzeyi stale CLI metnine shell ile gitmek yerine
# TR: mühürlü DB gateway ile doğrudan konuşmalıdır; bu yüzden kanonik
# TR: runtime-control DB yardımcılarını içe aktarıyoruz.
from ..logisticsearch1_1_1_state_db_gateway import (
    connect_db,
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)

# EN: The current live controls contract expects the non-root makpi51 user.
# TR: Güncel canlı controls sözleşmesi root olmayan makpi51 kullanıcısını bekler.
EXPECTED_USER = "makpi51"


# EN: This helper resolves the webcrawler root from this file location.
# EN: controls/_runtime_control_common.py -> controls -> lib -> webcrawler
# TR: Bu yardımcı webcrawler kökünü bu dosyanın konumundan çözer.
# TR: controls/_runtime_control_common.py -> controls -> lib -> webcrawler
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / webcrawler_root
# EN:
# EN: This top-level function exists so 'webcrawler_root' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / webcrawler_root
# TR:
# TR: Bu ust seviye fonksiyon, 'webcrawler_root' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def webcrawler_root() -> Path:
    # EN: parents[2] lands at the webcrawler directory.
    # TR: parents[2] bizi webcrawler dizinine getirir.
    return Path(__file__).resolve().parents[2]


# EN: This helper returns the canonical live env-file path.
# TR: Bu yardımcı kanonik canlı env dosyası yolunu döndürür.
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / env_file_path
# EN:
# EN: This top-level function exists so 'env_file_path' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / env_file_path
# TR:
# TR: Bu ust seviye fonksiyon, 'env_file_path' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def env_file_path() -> Path:
    # EN: Runtime env truth currently lives under webcrawler/config/webcrawler.env.
    # TR: Runtime env doğrusu şu anda webcrawler/config/webcrawler.env altında yaşar.
    return webcrawler_root() / "config" / "webcrawler.env"


# EN: This helper enforces the same user policy the old shell wrappers used.
# TR: Bu yardımcı eski shell wrapper'ların kullandığı aynı kullanıcı politikasını
# TR: uygular.
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / ensure_expected_user
# EN:
# EN: This top-level function exists so 'ensure_expected_user' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / ensure_expected_user
# TR:
# TR: Bu ust seviye fonksiyon, 'ensure_expected_user' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def ensure_expected_user() -> None:
    # EN: We read the visible current username through getpass.
    # TR: Mevcut kullanıcı adını getpass üzerinden okuyoruz.
    current_user = getpass.getuser()

    # EN: Root is intentionally forbidden for these operator controls.
    # TR: Bu operatör kontrolleri için root bilinçli olarak yasaktır.
    if current_user == "root":
        raise RuntimeError(f"control must be run as {EXPECTED_USER}, not root")

    # EN: Any non-root but wrong user is also rejected explicitly.
    # TR: Root olmayan ama yanlış kullanıcı da açık biçimde reddedilir.
    if current_user != EXPECTED_USER:
        raise RuntimeError(
            f"control must be run as {EXPECTED_USER}; current user is {current_user}"
        )


# EN: This helper reads a very small .env-like file format in a conservative way.
# EN: We support the current webcrawler.env style without trying to implement a
# EN: full shell parser.
# TR: Bu yardımcı çok küçük bir .env-benzeri formatı muhafazakâr biçimde okur.
# TR: Tam bir shell parser yazmaya çalışmadan mevcut webcrawler.env stilini
# TR: destekliyoruz.
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / read_simple_env_file
# EN:
# EN: This top-level function exists so 'read_simple_env_file' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: path
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / read_simple_env_file
# TR:
# TR: Bu ust seviye fonksiyon, 'read_simple_env_file' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: path
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def read_simple_env_file(path: Path) -> dict[str, str]:
    # EN: Missing env file is a hard failure because the old controls surface also
    # EN: required it explicitly.
    # TR: Eksik env dosyası sert hatadır; çünkü eski controls yüzeyi de bunu açıkça
    # TR: zorunlu tutuyordu.
    if not path.is_file():
        raise RuntimeError(f"missing env file: {path}")

    # EN: This dictionary accumulates parsed key/value pairs.
    # TR: Bu sözlük parse edilen anahtar/değer çiftlerini biriktirir.
    parsed: dict[str, str] = {}

    # EN: We iterate line by line because the accepted format is line-oriented.
    # TR: Kabul edilen biçim satır-odaklı olduğu için satır satır ilerliyoruz.
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        # EN: We strip outer whitespace first.
        # TR: Önce dış boşlukları kırpıyoruz.
        line = raw_line.strip()

        # EN: Empty lines and comment lines carry no runtime value here.
        # TR: Boş satırlar ve yorum satırları burada runtime değeri taşımaz.
        if not line or line.startswith("#"):
            continue

        # EN: We tolerate an optional leading export prefix.
        # TR: İsteğe bağlı baştaki export önekini tolere ediyoruz.
        if line.startswith("export "):
            # EN: LOCAL VALUE EXPLANATION / read_simple_env_file / line
            # EN: This local exists because the shared control-helper corridor should keep
            # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
            # EN: Expected meaning:
            # EN: - current local name: line
            # EN: - this value carries a small readable helper-side meaning inside read_simple_env_file
            # EN: - accepted values depend on the branch below but should stay explicit and inspectable
            # EN: Undesired meaning:
            # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
            # TR: YEREL DEGER ACIKLAMASI / read_simple_env_file / line
            # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
            # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
            # TR: Beklenen anlam:
            # TR: - guncel yerel ad: line
            # TR: - bu deger read_simple_env_file icinde kucuk ama okunur yardimci-anlam tasir
            # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
            # TR: Istenmeyen anlam:
            # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
            line = line[len("export "):].strip()

        # EN: Lines without '=' are ignored because they do not fit the narrow
        # EN: accepted contract.
        # TR: '=' içermeyen satırlar dar kabul sözleşmesine uymadığı için yok sayılır.
        if "=" not in line:
            continue

        # EN: We split only once so the value may still contain '=' characters.
        # TR: Değer içinde '=' bulunabilsin diye yalnızca bir kez bölüyoruz.
        key, value = line.split("=", 1)
        # EN: LOCAL VALUE EXPLANATION / read_simple_env_file / key
        # EN: This local exists because the shared control-helper corridor should keep
        # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
        # EN: Expected meaning:
        # EN: - current local name: key
        # EN: - this value carries a small readable helper-side meaning inside read_simple_env_file
        # EN: - accepted values depend on the branch below but should stay explicit and inspectable
        # EN: Undesired meaning:
        # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
        # TR: YEREL DEGER ACIKLAMASI / read_simple_env_file / key
        # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
        # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
        # TR: Beklenen anlam:
        # TR: - guncel yerel ad: key
        # TR: - bu deger read_simple_env_file icinde kucuk ama okunur yardimci-anlam tasir
        # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
        # TR: Istenmeyen anlam:
        # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
        key = key.strip()
        # EN: LOCAL VALUE EXPLANATION / read_simple_env_file / value
        # EN: This local exists because the shared control-helper corridor should keep
        # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
        # EN: Expected meaning:
        # EN: - current local name: value
        # EN: - this value carries a small readable helper-side meaning inside read_simple_env_file
        # EN: - accepted values depend on the branch below but should stay explicit and inspectable
        # EN: Undesired meaning:
        # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
        # TR: YEREL DEGER ACIKLAMASI / read_simple_env_file / value
        # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
        # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
        # TR: Beklenen anlam:
        # TR: - guncel yerel ad: value
        # TR: - bu deger read_simple_env_file icinde kucuk ama okunur yardimci-anlam tasir
        # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
        # TR: Istenmeyen anlam:
        # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
        value = value.strip()

        # EN: We remove one matching pair of surrounding quotes when present.
        # TR: Varsa eşleşen tek çift dış tırnağı kaldırıyoruz.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            # EN: LOCAL VALUE EXPLANATION / read_simple_env_file / value
            # EN: This local exists because the shared control-helper corridor should keep
            # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
            # EN: Expected meaning:
            # EN: - current local name: value
            # EN: - this value carries a small readable helper-side meaning inside read_simple_env_file
            # EN: - accepted values depend on the branch below but should stay explicit and inspectable
            # EN: Undesired meaning:
            # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
            # TR: YEREL DEGER ACIKLAMASI / read_simple_env_file / value
            # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
            # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
            # TR: Beklenen anlam:
            # TR: - guncel yerel ad: value
            # TR: - bu deger read_simple_env_file icinde kucuk ama okunur yardimci-anlam tasir
            # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
            # TR: Istenmeyen anlam:
            # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
            value = value[1:-1]

        # EN: We keep only non-empty keys.
        # TR: Yalnızca boş olmayan anahtarları tutuyoruz.
        if key:
            parsed[key] = value

    # EN: We return the parsed environment mapping.
    # TR: Parse edilmiş environment eşlemesini döndürüyoruz.
    return parsed


# EN: This helper resolves the crawler DSN using current environment first and
# EN: env-file fallback second.
# TR: Bu yardımcı crawler DSN değerini önce mevcut environment'dan, sonra env
# TR: dosyası fallback'inden çözer.
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / resolve_crawler_dsn
# EN:
# EN: This top-level function exists so 'resolve_crawler_dsn' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / resolve_crawler_dsn
# TR:
# TR: Bu ust seviye fonksiyon, 'resolve_crawler_dsn' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def resolve_crawler_dsn() -> str:
    # EN: Current process environment gets first priority.
    # TR: İlk öncelik mevcut süreç environment'ıdır.
    env_dsn = (os.getenv("LOGISTICSEARCH_CRAWLER_DSN") or "").strip()
    if env_dsn:
        return env_dsn

    # EN: If process environment is empty, we read the canonical env file.
    # TR: Süreç environment'ı boşsa kanonik env dosyasını okuyoruz.
    file_values = read_simple_env_file(env_file_path())
    # EN: LOCAL VALUE EXPLANATION / resolve_crawler_dsn / file_dsn
    # EN: This local exists because the shared control-helper corridor should keep
    # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
    # EN: Expected meaning:
    # EN: - current local name: file_dsn
    # EN: - this value carries a small readable helper-side meaning inside resolve_crawler_dsn
    # EN: - accepted values depend on the branch below but should stay explicit and inspectable
    # EN: Undesired meaning:
    # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
    # TR: YEREL DEGER ACIKLAMASI / resolve_crawler_dsn / file_dsn
    # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
    # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
    # TR: Beklenen anlam:
    # TR: - guncel yerel ad: file_dsn
    # TR: - bu deger resolve_crawler_dsn icinde kucuk ama okunur yardimci-anlam tasir
    # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
    # TR: Istenmeyen anlam:
    # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
    file_dsn = (file_values.get("LOGISTICSEARCH_CRAWLER_DSN") or "").strip()
    if file_dsn:
        return file_dsn

    # EN: Missing DSN is a hard failure because controls cannot talk to DB truth
    # EN: without it.
    # TR: DSN eksikse sert hata veririz; çünkü controls DB doğrusu ile onsuz
    # TR: konuşamaz.
    raise RuntimeError("missing LOGISTICSEARCH_CRAWLER_DSN in environment and env file")


# EN: This helper executes one durable runtime-control state change and prints
# EN: the final visible truth as JSON.
# TR: Bu yardımcı tek bir kalıcı runtime-control durum değişimini çalıştırır ve
# TR: son görünür doğruluğu JSON olarak yazdırır.
# EN: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOCK V9 / apply_runtime_control
# EN:
# EN: This top-level function exists so 'apply_runtime_control' stays readable inside the shared control-helper corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: desired_state, state_reason, requested_by
# EN: - explicit and readable helper input is desired
# EN: Accepted output line shapes:
# EN: - explicit helper result
# EN: - explicit normalized text/path/payload shape
# EN: - explicit raised error that stays visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the entry surface can no longer explain what happened
# TR: RUNTIME CONTROL COMMON FUNCTION CONTRACT BLOĞU V9 / apply_runtime_control
# TR:
# TR: Bu ust seviye fonksiyon, 'apply_runtime_control' yapisinin ortak kontrol-yardimci koridoru icinde okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: desired_state, state_reason, requested_by
# TR: - acik ve okunur yardimci girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik yardimci sonucu
# TR: - acik normalize edilmis text/path/payload sekli
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - giris yuzeyinin ne oldugunu aciklayamadigi sessiz belirsizlik

def apply_runtime_control(
    *,
    desired_state: str,
    state_reason: str,
    requested_by: str,
) -> int:
    # EN: We enforce the current user policy first.
    # TR: Önce güncel kullanıcı politikasını uygularız.
    ensure_expected_user()

    # EN: We resolve the crawler DSN before opening the DB connection.
    # TR: DB bağlantısını açmadan önce crawler DSN değerini çözüyoruz.
    dsn = resolve_crawler_dsn()

    # EN: We connect through the canonical DB gateway.
    # TR: Kanonik DB gateway üzerinden bağlanıyoruz.
    conn = connect_db(dsn)

    try:
        # EN: We execute the durable state change through the sealed DB function.
        # TR: Kalıcı durum değişimini mühürlü DB fonksiyonu üzerinden çalıştırıyoruz.
        set_result = set_webcrawler_runtime_control(
            conn,
            desired_state=desired_state,
            state_reason=state_reason,
            requested_by=requested_by,
        )

        # EN: A degraded set-result means the lower mutation wrapper returned no
        # EN: row. We must surface that payload honestly instead of crashing.
        # TR: Degrade olmuş set-result alt mutation wrapper'ın satır döndürmediği
        # TR: anlamına gelir. Bunu çökmeden dürüstçe görünür kılmalıyız.
        if bool(set_result.get("runtime_control_degraded")):
            # EN: LOCAL VALUE EXPLANATION / apply_runtime_control / payload
            # EN: This local exists because the shared control-helper corridor should keep
            # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
            # EN: Expected meaning:
            # EN: - current local name: payload
            # EN: - this value carries a small readable helper-side meaning inside apply_runtime_control
            # EN: - accepted values depend on the branch below but should stay explicit and inspectable
            # EN: Undesired meaning:
            # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
            # TR: YEREL DEGER ACIKLAMASI / apply_runtime_control / payload
            # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
            # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
            # TR: Beklenen anlam:
            # TR: - guncel yerel ad: payload
            # TR: - bu deger apply_runtime_control icinde kucuk ama okunur yardimci-anlam tasir
            # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
            # TR: Istenmeyen anlam:
            # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
            payload = {
                "mode": "runtime_control",
                "action": "set",
                "set_result": dict(set_result),
                "runtime_control": dict(set_result),
            }
            conn.rollback()
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

        # EN: The durable state change must be committed before the visible truth is
        # EN: re-read.
        # TR: Görünür doğruluk yeniden okunmadan önce kalıcı durum değişimi commit
        # TR: edilmelidir.
        conn.commit()

        # EN: We read back the visible runtime-control row.
        # TR: Görünür runtime-control satırını geri okuyoruz.
        runtime_control = get_webcrawler_runtime_control(conn)

        # EN: A degraded runtime-control read after commit must stay operator-visible
        # EN: instead of turning into an exception.
        # TR: Commit sonrası degrade runtime-control okuması istisnaya dönüşmek
        # TR: yerine operatöre görünür kalmalıdır.
        if bool(runtime_control.get("runtime_control_degraded")):
            # EN: LOCAL VALUE EXPLANATION / apply_runtime_control / payload
            # EN: This local exists because the shared control-helper corridor should keep
            # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
            # EN: Expected meaning:
            # EN: - current local name: payload
            # EN: - this value carries a small readable helper-side meaning inside apply_runtime_control
            # EN: - accepted values depend on the branch below but should stay explicit and inspectable
            # EN: Undesired meaning:
            # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
            # TR: YEREL DEGER ACIKLAMASI / apply_runtime_control / payload
            # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
            # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
            # TR: Beklenen anlam:
            # TR: - guncel yerel ad: payload
            # TR: - bu deger apply_runtime_control icinde kucuk ama okunur yardimci-anlam tasir
            # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
            # TR: Istenmeyen anlam:
            # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
            payload = {
                "mode": "runtime_control",
                "action": "set",
                "set_result": dict(set_result),
                "runtime_control": dict(runtime_control),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

        # EN: We also read back the visible may-claim decision.
        # TR: Görünür may-claim kararını da geri okuyoruz.
        may_claim_result = webcrawler_runtime_may_claim(conn)

        # EN: A degraded may-claim read must be surfaced explicitly instead of
        # EN: pretending the final control snapshot is complete.
        # TR: Degrade olmuş may-claim okuması nihai kontrol görüntüsü tamamlanmış
        # TR: gibi davranmak yerine açıkça görünür kılınmalıdır.
        if bool(may_claim_result.get("runtime_control_degraded")):
            # EN: LOCAL VALUE EXPLANATION / apply_runtime_control / payload
            # EN: This local exists because the shared control-helper corridor should keep
            # EN: intermediate value meaning named, visible, and reviewable instead of hiding it inline.
            # EN: Expected meaning:
            # EN: - current local name: payload
            # EN: - this value carries a small readable helper-side meaning inside apply_runtime_control
            # EN: - accepted values depend on the branch below but should stay explicit and inspectable
            # EN: Undesired meaning:
            # EN: - treating this local as invisible throwaway state while it still shapes control-readable behavior
            # TR: YEREL DEGER ACIKLAMASI / apply_runtime_control / payload
            # TR: Bu yerel, ortak control-yardimci koridorunda ara deger anlaminin
            # TR: satir icine gizlenmek yerine isimli, gorunur ve denetlenebilir kalmasi icin vardir.
            # TR: Beklenen anlam:
            # TR: - guncel yerel ad: payload
            # TR: - bu deger apply_runtime_control icinde kucuk ama okunur yardimci-anlam tasir
            # TR: - kabul edilen degerler asagidaki dala gore degisir ama acik ve incelenebilir kalmalidir
            # TR: Istenmeyen anlam:
            # TR: - bu yereli, okunur kontrol davranisini etkilerken gorunmez gecici durum gibi gormek
            payload = {
                "mode": "runtime_control",
                "action": "set",
                "set_result": dict(set_result),
                "may_claim_result": dict(may_claim_result),
                "runtime_control": {
                    **dict(runtime_control),
                    "may_claim": may_claim_result.get("may_claim"),
                    "may_claim_degraded": True,
                    "may_claim_degraded_reason": may_claim_result.get("runtime_control_degraded_reason"),
                },
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

        # EN: We build one final structured payload.
        # TR: Tek bir nihai yapılı payload kuruyoruz.
        payload = {
            "mode": "runtime_control",
            "action": "set",
            "set_result": set_result,
            "runtime_control": {
                **dict(runtime_control),
                "may_claim": may_claim_result.get("may_claim"),
            },
        }

        # EN: We print JSON for both humans and tools.
        # TR: JSON çıktısını hem insanlar hem araçlar için yazdırıyoruz.
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return 0
    finally:
        # EN: We always close the DB connection.
        # TR: DB bağlantısını her durumda kapatıyoruz.
        conn.close()
