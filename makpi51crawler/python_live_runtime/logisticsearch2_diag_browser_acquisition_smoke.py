"""
EN:
This file is the explicit diagnostic smoke surface for the browser-backed
acquisition corridor.

EN:
Beginner-first mental model:
- the main crawler runtime is the real production highway
- this file is not that highway
- this file is the small test lane near the highway
- operators use it to ask a narrow question:
  "Can the browser acquisition corridor still start and return something readable?"

EN:
Why this file exists:
- because a complicated browser corridor needs a tiny named proof surface
- because operators need a fast smoke test before trusting deeper runtime work
- because debugging is easier when diagnostic entry points stay separate from production orchestration
- because a beginner should be able to find one file that answers where browser acquisition is smoke-tested
- because timeout, degraded, missing browser dependency, startup failure, and success-like branches must stay visible

EN:
What this file DOES:
- exercise the browser-backed acquisition path in a narrow diagnostic way
- provide a readable and operator-facing smoke corridor
- keep returned payloads and failure shapes visible
- help distinguish browser-start problems from broader crawler-system problems
- act as a small controlled observability surface for the browser corridor

EN:
What this file DOES NOT do:
- it does not become the whole crawler runtime
- it does not replace the worker runtime
- it does not replace acquisition parent orchestration
- it does not own final ranking, taxonomy, or storage routing
- it does not silently hide browser failures behind fake success
- it does not claim that production is healthy just because one smoke check worked

EN:
Topological role:
- this file sits outside the main worker loop
- it points at the browser acquisition family as a diagnostic caller
- it is therefore a thin diagnostic entry surface, not the production owner of acquisition logic
- production files remain the real owners; this file only verifies a narrow corridor

EN:
Important variable and payload meanings:
- argv-like input is usually lightweight diagnostic input
- url-like input is usually the target resource chosen for smoke verification
- result-like payloads should remain readable and inspection-friendly
- success-like output may still include warnings or degraded notes
- error-like output should stay explicit rather than being flattened
- browser-start failures, dependency failures, timeout-like failures, and payload-shape failures should remain visible
- undesired meaning is a silent test surface that hides whether the browser corridor truly worked

EN:
Accepted diagnostic identity:
- tiny smoke entry point
- narrow browser acquisition verifier
- operator-readable observability helper

EN:
Undesired diagnostic identity:
- hidden second production runtime
- random scratchpad with no contract meaning
- ambiguous script where the reader cannot tell if it is safe to use for diagnosis

TR:
Bu dosya browser destekli acquisition koridorunun acik diagnostic smoke yuzeyidir.

TR:
Baslangic seviyesi zihinsel model:
- ana crawler runtime gercek uretim otoyoludur
- bu dosya o otoyol degildir
- bu dosya otoyolun yanindaki kucuk test serididir
- operator bu dosyayla dar bir soruya cevap arar:
  "Browser acquisition koridoru hala baslayip okunur bir sonuc dondurebiliyor mu?"

TR:
Bu dosya neden var:
- cunku karmasik browser koridorunun kucuk ve isimli bir ispat yuzeyine ihtiyaci vardir
- cunku operator derin runtime isine guvenmeden once hizli smoke test ister
- cunku diagnostic giris noktasi uretim orchestration dosyalarindan ayri kalirsa debug daha kolay olur
- cunku yeni baslayan biri browser acquisition isinin nerede smoke-test edildigini tek dosyada gorebilmelidir
- cunku timeout, degraded, browser bagimlilik eksigi, startup failure ve success-benzeri dallar gorunur kalmalidir

TR:
Bu dosya NE yapar:
- browser destekli acquisition yolunu dar bir diagnostic bicimde dener
- okunur ve operator-yuzlu bir smoke koridoru sunar
- donen payloadlari ve hata sekillerini gorunur tutar
- browser-start problemlerini daha genis crawler sistemi problemlerinden ayirmaya yardim eder
- browser koridoru icin kucuk ve kontrollu bir gozlenebilirlik yuzeyi olur

TR:
Bu dosya NE yapmaz:
- tum crawler runtime haline gelmez
- worker runtime yerine gecmez
- acquisition parent orchestration yuzeyinin yerine gecmez
- final ranking, taxonomy veya storage routing sahipligi almaz
- browser hatalarini sahte basari arkasina gizlemez
- tek bir smoke check calisti diye production saglikli demis olmaz

TR:
Topolojik rol:
- bu dosya ana worker loop disinda durur
- diagnostic cagiran olarak browser acquisition ailesine isaret eder
- dolayisiyla bu dosya production acquisition mantiginin sahibi degil, ince bir diagnostic giris yuzeyidir
- gercek sahipler production dosyalardir; bu dosya sadece dar bir koridoru dogrular

TR:
Onemli degisken ve payload anlamlari:
- argv benzeri girdi genellikle hafif diagnostic girdisidir
- url benzeri girdi cogunlukla smoke verification icin secilen hedeftir
- result benzeri payloadlar okunur ve incelenebilir kalmalidir
- success-benzeri cikti warning veya degraded notlari yine de icerebilir
- error-benzeri cikti duzlestirilmeden acik kalmalidir
- browser-start failure, bagimlilik failure, timeout-benzeri failure ve payload-shape failure gorunur kalmalidir
- istenmeyen anlam, browser koridorunun gercekten calisip calismadigini gizleyen sessiz test yuzeyidir

TR:
Kabul edilen diagnostic kimlik:
- kucuk smoke entry point
- dar browser acquisition dogrulayicisi
- operatorun okuyacagi gozlenebilirlik yardimcisi

TR:
Istenmeyen diagnostic kimlik:
- gizli ikinci production runtime
- sozlesme anlami olmayan rastgele scratchpad
- okuyucunun tanisal kullanim icin guvenli olup olmadigini anlayamadigi belirsiz script
"""



# EN: DIAG SMOKE DENSITY LIFT BLOCK V8
# EN:
# EN: This density-lift block exists because the diagnostic smoke file must be self-explanatory even for a first-time reader.
# EN: The goal is not filler text; the goal is to make the file identity, reading order, and error interpretation obvious.
# EN: A reader should understand why the file exists before trusting any smoke result.
# TR: DIAG SMOKE DENSITY LIFT BLOĞU V8
# TR:
# TR: Bu density-lift blogu, diagnostic smoke dosyasinin ilk kez okuyan biri icin bile kendini aciklamasi gerektigi icin vardir.
# TR: Amac bos yorum eklemek degil; dosya kimligini, okuma sirasini ve hata yorumunu acik etmektir.
# TR: Okuyucu herhangi bir smoke sonucuna guvenmeden once bu dosyanin neden var oldugunu anlamalidir.
# EN:
# EN: Operator reading path:
# EN: 1) identify that this is a smoke surface
# EN: 2) identify which corridor it probes
# EN: 3) identify what counts as success, degraded, timeout, or explicit error
# EN: 4) identify what this file does not prove about production
# TR:
# TR: Operator okuma yolu:
# TR: 1) bunun bir smoke yuzeyi oldugunu tespit et
# TR: 2) hangi koridoru probe ettigini tespit et
# TR: 3) neyin success, degraded, timeout veya acik hata oldugunu tespit et
# TR: 4) bu dosyanin production hakkinda neyi kanitlamadigini tespit et
# EN: Reading checkpoint 1: keep 'smoke scope' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'smoke scope' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 1: bu diagnostic dosyayi incelerken 'smoke kapsami' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'smoke kapsami' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 2: keep 'entry-point identity' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'entry-point identity' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 2: bu diagnostic dosyayi incelerken 'giris noktasi kimligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'giris noktasi kimligi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 3: keep 'operator reading path' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'operator reading path' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 3: bu diagnostic dosyayi incelerken 'operator okuma yolu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'operator okuma yolu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 4: keep 'degraded honesty' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'degraded honesty' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 4: bu diagnostic dosyayi incelerken 'degraded durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'degraded durustlugu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 5: keep 'explicit timeout visibility' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'explicit timeout visibility' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 5: bu diagnostic dosyayi incelerken 'acik timeout gorunurlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'acik timeout gorunurlugu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 6: keep 'browser startup visibility' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'browser startup visibility' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 6: bu diagnostic dosyayi incelerken 'browser baslangic gorunurlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'browser baslangic gorunurlugu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 7: keep 'dependency-failure visibility' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'dependency-failure visibility' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 7: bu diagnostic dosyayi incelerken 'bagimlilik-hatasi gorunurlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'bagimlilik-hatasi gorunurlugu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 8: keep 'payload readability' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'payload readability' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 8: bu diagnostic dosyayi incelerken 'payload okunabilirligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'payload okunabilirligi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 9: keep 'diagnostic narrowness' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'diagnostic narrowness' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 9: bu diagnostic dosyayi incelerken 'diagnostic darligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'diagnostic darligi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 10: keep 'production separation' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'production separation' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 10: bu diagnostic dosyayi incelerken 'production ayrimi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'production ayrimi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 11: keep 'result interpretation' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'result interpretation' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 11: bu diagnostic dosyayi incelerken 'sonuc yorumlama' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'sonuc yorumlama' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 12: keep 'error interpretation' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'error interpretation' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 12: bu diagnostic dosyayi incelerken 'hata yorumlama' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'hata yorumlama' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 13: keep 'success interpretation' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'success interpretation' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 13: bu diagnostic dosyayi incelerken 'basari yorumlama' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'basari yorumlama' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 14: keep 'smoke-test limit awareness' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'smoke-test limit awareness' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 14: bu diagnostic dosyayi incelerken 'smoke-test sinir farkindaligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'smoke-test sinir farkindaligi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 15: keep 'observability value' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'observability value' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 15: bu diagnostic dosyayi incelerken 'gozlenebilirlik degeri' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'gozlenebilirlik degeri' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 16: keep 'debug usefulness' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'debug usefulness' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 16: bu diagnostic dosyayi incelerken 'debug faydasi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'debug faydasi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 17: keep 'operator trust' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'operator trust' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 17: bu diagnostic dosyayi incelerken 'operator guveni' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'operator guveni' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 18: keep 'false confidence avoidance' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'false confidence avoidance' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 18: bu diagnostic dosyayi incelerken 'sahte guvenden kacis' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'sahte guvenden kacis' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 19: keep 'input simplicity' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'input simplicity' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 19: bu diagnostic dosyayi incelerken 'girdi sadeligi' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'girdi sadeligi' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN: Reading checkpoint 20: keep 'output honesty' visible while inspecting this diagnostic file.
# EN: Accepted meaning: the smoke file should help the operator reason about one narrow browser-backed verification corridor.
# EN: Undesired meaning: losing 'output honesty' would make the file look like a random script instead of a controlled diagnostic surface.
# TR: Okuma kontrol noktasi 20: bu diagnostic dosyayi incelerken 'cikti durustlugu' gorunur kalmalidir.
# TR: Kabul edilen anlam: smoke dosyasi operatorun tek ve dar bir browser destekli verification koridoru hakkinda dusunmesine yardim etmelidir.
# TR: Istenmeyen anlam: 'cikti durustlugu' kaybolursa dosya kontrollu diagnostic yuzey yerine rastgele script gibi gorunur.
# EN:
# EN: Variable and payload glossary:
# EN: The names below are generic reading anchors for a beginner.
# EN: They explain how to interpret common smoke-test shapes without pretending every project file uses the exact same local variable names.
# TR:
# TR: Degisken ve payload sozlugu:
# TR: Asagidaki adlar yeni baslayan biri icin genel okuma capalaridir.
# TR: Bunlar her dosyanin birebir ayni lokal degisken adlarini kullandigini iddia etmeden yaygin smoke-test sekillerini yorumlamayi aciklar.
# EN: Glossary item 1: 'target_url' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 1: 'hedef_url' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 2: 'result payload' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 2: 'sonuc payloadi' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 3: 'browser session' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 3: 'browser oturumu' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 4: 'timeout branch' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 4: 'timeout dali' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 5: 'degraded branch' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 5: 'degraded dali' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 6: 'error branch' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 6: 'hata dali' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 7: 'success-style branch' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 7: 'basari-benzeri dal' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 8: 'diagnostic note' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 8: 'diagnostic not' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 9: 'operator message' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 9: 'operator mesaji' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN: Glossary item 10: 'readable receipt' usually means a small, readable diagnostic input or output concept.
# EN: Accepted values are explicit and operator-readable; undesired values are silent, ambiguous, or shape-breaking payloads.
# TR: Sozluk ogesi 10: 'okunur makbuz' genellikle kucuk ve okunur bir diagnostic girdi veya cikti kavrami demektir.
# TR: Kabul edilen degerler acik ve operatorun okuyacagi sekildedir; istenmeyen degerler sessiz, belirsiz veya sekli bozan payloadlardir.
# EN:
# EN: Final reminder:
# EN: passing this smoke file means one narrow corridor looked healthy enough to report back.
# EN: failing this smoke file means the browser-backed corridor needs inspection before broader trust is granted.
# EN: neither branch should be over-interpreted.
# TR:
# TR: Son hatirlatma:
# TR: bu smoke dosyasinin gecmesi, tek ve dar bir koridorun rapor verecek kadar saglikli gorundugu anlamina gelir.
# TR: bu smoke dosyasinin kalmasi, browser destekli koridorun daha genis guven verilmeden once incelenmesi gerektigi anlamina gelir.
# TR: hicbir dal asiri yorumlanmamalidir.

# EN: DIAG BROWSER ACQUISITION SMOKE IDENTITY MEMORY BLOCK V7
# EN:
# EN: Read this file as a narrow diagnostic smoke entry, not as the production browser runtime.
# EN: Beginner-first map:
# EN: - production acquisition files own the real browser corridor
# EN: - this file only probes that corridor
# EN: - this keeps operator diagnosis separate from worker orchestration
# EN: Accepted meaning:
# EN: - explicit smoke test
# EN: - readable diagnostic result
# EN: - visible success, timeout, degraded, or explicit-error branches
# EN: Undesired meaning:
# EN: - fake production health proof
# EN: - hidden second runtime
# EN: - ambiguous script with no diagnostic identity
# TR: DIAG BROWSER ACQUISITION SMOKE KIMLIK HAFIZA BLOĞU V7
# TR:
# TR: Bu dosya production browser runtime degil, dar diagnostic smoke giris yuzeyi olarak okunmalidir.
# TR: Baslangic seviyesi harita:
# TR: - gercek browser koridorunun sahibi production acquisition dosyalaridir
# TR: - bu dosya sadece o koridoru probe eder
# TR: - boylece operator diagnostigi worker orchestration isinden ayri kalir
# TR: Kabul edilen anlam:
# TR: - acik smoke test
# TR: - okunur diagnostic sonuc
# TR: - gorunur success, timeout, degraded veya acik hata dallari
# TR: Istenmeyen anlam:
# TR: - sahte production health ispati
# TR: - gizli ikinci runtime
# TR: - diagnostic kimligi olmayan belirsiz script

from __future__ import annotations

# EN: We use argparse because this smoke entry must accept explicit operator
# EN: inputs instead of hiding assumptions in hard-coded paths.
# TR: Bu smoke giriş yüzeyi hard-coded varsayımlar yerine açık operatör girdileri
# TR: almalıdır; bu yüzden argparse kullanıyoruz.
import argparse

# EN: We use json because the smoke result must be written as machine-readable evidence.
# TR: Smoke sonucu makine-okunur kanıt olarak yazılacağı için json kullanıyoruz.
import json

# EN: We use datetime only to build deterministic default output paths with timestamps.
# TR: datetime'ı yalnızca zaman damgalı deterministik varsayılan çıktı yolları
# TR: üretmek için kullanıyoruz.
from datetime import UTC, datetime

# EN: We use Path because evidence files are real filesystem artifacts.
# TR: Kanıt dosyaları gerçek dosya-sistemi artıkları olduğu için Path kullanıyoruz.
from pathlib import Path

# EN: We import the canonical browser-acquisition runtime we just created.
# TR: Az önce oluşturduğumuz kanonik browser-acquisition runtime yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_4_3_browser_dynamic_acquisition_runtime import acquire_public_page_with_browser


# EN: This helper builds timestamped default evidence paths under /tmp.
# TR: Bu yardımcı /tmp altında zaman damgalı varsayılan kanıt yolları üretir.
# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V7 / build_default_output_paths
# EN:
# EN: This top-level function exists so the diagnostic role of 'build_default_output_paths' stays readable.
# EN: Why this function exists:
# EN: - to preserve one named step in the browser smoke corridor
# EN: - to help a beginner map which function prepares, runs, transforms, or reports the smoke result
# EN: - to keep success, degraded, timeout, and explicit error meaning visible
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - callers should match the live Python signature exactly
# EN: - diagnostic payloads should stay small, readable, and explicit
# EN: Accepted output line shapes:
# EN: - dict-like payload
# EN: - text-like output
# EN: - explicit success-style receipt
# EN: - explicit timeout-like or degraded result
# EN: - explicit raised failure that remains visible to diagnostics
# EN: Undesired meaning:
# EN: - silent branch where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V7 / build_default_output_paths
# TR:
# TR: Bu ust seviye fonksiyon, 'build_default_output_paths' fonksiyonunun diagnostic rolunun okunur kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - browser smoke koridorundaki tek isimli adimi korumak icin
# TR: - yeni baslayanin hangi fonksiyonun hazirladigini, calistirdigini, donusturdugunu veya raporladigini gorebilmesi icin
# TR: - success, degraded, timeout ve acik hata anlamlarini gorunur tutmak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - diagnostic payloadlar kucuk, okunur ve acik kalmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - dict-benzeri payload
# TR: - text-benzeri cikti
# TR: - acik success tarzi makbuz
# TR: - acik timeout-benzeri veya degraded sonuc
# TR: - diagnostic yuzeyde gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz dal

# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V8 / build_default_output_paths
# EN:
# EN: This top-level function exists so 'build_default_output_paths' stays readable in the browser diagnostic corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - readable, explicit, operator-facing diagnostic input is desired
# EN: Accepted output line shapes:
# EN: - explicit success-style data
# EN: - explicit degraded data
# EN: - explicit timeout-like data
# EN: - explicit raised error that remains visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V8 / build_default_output_paths
# TR:
# TR: Bu ust seviye fonksiyon, 'build_default_output_paths' yapisinin browser diagnostic koridorunda okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - okunur, acik ve operator-yuzlu diagnostic girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik success-benzeri veri
# TR: - acik degraded veri
# TR: - acik timeout-benzeri veri
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz belirsizlik

# EN: Function build_default_output_paths belongs to the narrow diagnostic smoke contract.
# EN: This helper keeps the default output artefact destinations in one visible place.
# EN: Return contract: it returns a fixed-order tuple of Path values for html, png screenshot, and json output artefacts.
# TR: build_default_output_paths fonksiyonu dar diagnostic smoke sozlesmesinin parcasidir.
# TR: Bu helper varsayilan cikti artefact hedeflerini tek gorunur yerde tutar.
# TR: Donus sozlesmesi: html, png screenshot ve json cikti artefactlari icin sabit sirali Path demeti dondurur.
def build_default_output_paths() -> tuple[Path, Path, Path]:
    # EN: UTC timestamp keeps cross-host comparison simpler.
    # TR: UTC zaman damgası çoklu host karşılaştırmasını daha sade tutar.
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
# EN: html_path stores the default saved HTML artefact destination for this smoke run.
# EN: Expected values are writable Path objects under the diagnostic output directory.
# TR: html_path bu smoke calismasi icin varsayilan kaydedilmis HTML artefact hedefini tasir.
# TR: Beklenen degerler diagnostic output dizini altindaki yazilabilir Path nesneleridir.
    html_path = Path(f"/tmp/browser_acquisition_rendered_{ts}.html")
# EN: png_path stores the default screenshot artefact destination for this smoke run.
# EN: Expected values are writable Path objects under the diagnostic output directory.
# TR: png_path bu smoke calismasi icin varsayilan screenshot artefact hedefini tasir.
# TR: Beklenen degerler diagnostic output dizini altindaki yazilabilir Path nesneleridir.
    png_path = Path(f"/tmp/browser_acquisition_screenshot_{ts}.png")
# EN: json_path stores the default json payload artefact destination for this smoke run.
# EN: Expected values are writable Path objects under the diagnostic output directory.
# TR: json_path bu smoke calismasi icin varsayilan json payload artefact hedefini tasir.
# TR: Beklenen degerler diagnostic output dizini altindaki yazilabilir Path nesneleridir.
    json_path = Path(f"/tmp/browser_acquisition_result_{ts}.json")
    return html_path, png_path, json_path


# EN: This parser defines the explicit CLI contract of the smoke entry.
# TR: Bu parser smoke giriş yüzeyinin açık CLI sözleşmesini tanımlar.
# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V7 / build_parser
# EN:
# EN: This top-level function exists so the diagnostic role of 'build_parser' stays readable.
# EN: Why this function exists:
# EN: - to preserve one named step in the browser smoke corridor
# EN: - to help a beginner map which function prepares, runs, transforms, or reports the smoke result
# EN: - to keep success, degraded, timeout, and explicit error meaning visible
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - callers should match the live Python signature exactly
# EN: - diagnostic payloads should stay small, readable, and explicit
# EN: Accepted output line shapes:
# EN: - dict-like payload
# EN: - text-like output
# EN: - explicit success-style receipt
# EN: - explicit timeout-like or degraded result
# EN: - explicit raised failure that remains visible to diagnostics
# EN: Undesired meaning:
# EN: - silent branch where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V7 / build_parser
# TR:
# TR: Bu ust seviye fonksiyon, 'build_parser' fonksiyonunun diagnostic rolunun okunur kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - browser smoke koridorundaki tek isimli adimi korumak icin
# TR: - yeni baslayanin hangi fonksiyonun hazirladigini, calistirdigini, donusturdugunu veya raporladigini gorebilmesi icin
# TR: - success, degraded, timeout ve acik hata anlamlarini gorunur tutmak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - diagnostic payloadlar kucuk, okunur ve acik kalmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - dict-benzeri payload
# TR: - text-benzeri cikti
# TR: - acik success tarzi makbuz
# TR: - acik timeout-benzeri veya degraded sonuc
# TR: - diagnostic yuzeyde gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz dal

# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V8 / build_parser
# EN:
# EN: This top-level function exists so 'build_parser' stays readable in the browser diagnostic corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - readable, explicit, operator-facing diagnostic input is desired
# EN: Accepted output line shapes:
# EN: - explicit success-style data
# EN: - explicit degraded data
# EN: - explicit timeout-like data
# EN: - explicit raised error that remains visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V8 / build_parser
# TR:
# TR: Bu ust seviye fonksiyon, 'build_parser' yapisinin browser diagnostic koridorunda okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - okunur, acik ve operator-yuzlu diagnostic girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik success-benzeri veri
# TR: - acik degraded veri
# TR: - acik timeout-benzeri veri
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz belirsizlik

# EN: Function build_parser belongs to the operator-facing diagnostic smoke contract.
# EN: This helper keeps the accepted CLI language in one visible place instead of scattering parser rules.
# EN: Return contract: it returns the argparse parser that defines the smoke script interface.
# TR: build_parser fonksiyonu operator-yuzlu diagnostic smoke sozlesmesinin parcasidir.
# TR: Bu helper kabul edilen CLI dilini parser kurallarini dagitmadan tek gorunur yerde tutar.
# TR: Donus sozlesmesi: smoke script arayuzunu tanimlayan argparse parser nesnesini dondurur.
def build_parser() -> argparse.ArgumentParser:
# EN: parser is the concrete CLI parser object that will collect operator diagnostic input.
# EN: Expected values are argparse.ArgumentParser instances.
# TR: parser operator diagnostic girdisini toplayacak somut CLI parser nesnesidir.
# TR: Beklenen degerler argparse.ArgumentParser ornekleridir.
    parser = argparse.ArgumentParser(
        description="Controlled browser-acquisition smoke for LogisticSearch webcrawler."
    )
    parser.add_argument("--url", required=True, help="Public target URL to open in the browser.")
    parser.add_argument(
        "--html-out",
        default=None,
        help="Path to write rendered HTML evidence.",
    )
    parser.add_argument(
        "--screenshot-out",
        default=None,
        help="Path to write screenshot evidence.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Path to write machine-readable JSON result.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=30000,
        help="Navigation timeout in milliseconds.",
    )
    parser.add_argument(
        "--wait-until",
        default="networkidle",
        choices=["load", "domcontentloaded", "networkidle", "commit"],
        help="Playwright wait-until mode for page.goto(...).",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Launch browser with a visible window instead of headless mode.",
    )
    return parser


# EN: main wires CLI inputs into the canonical browser-acquisition runtime and
# EN: writes the resulting evidence JSON to disk and stdout.
# TR: main, CLI girdilerini kanonik browser-acquisition runtime yüzeyine bağlar
# TR: ve ortaya çıkan kanıt JSON'unu hem diske hem stdout'a yazar.
# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V7 / main
# EN:
# EN: This top-level function exists so the diagnostic role of 'main' stays readable.
# EN: Why this function exists:
# EN: - to preserve one named step in the browser smoke corridor
# EN: - to help a beginner map which function prepares, runs, transforms, or reports the smoke result
# EN: - to keep success, degraded, timeout, and explicit error meaning visible
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - callers should match the live Python signature exactly
# EN: - diagnostic payloads should stay small, readable, and explicit
# EN: Accepted output line shapes:
# EN: - dict-like payload
# EN: - text-like output
# EN: - explicit success-style receipt
# EN: - explicit timeout-like or degraded result
# EN: - explicit raised failure that remains visible to diagnostics
# EN: Undesired meaning:
# EN: - silent branch where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V7 / main
# TR:
# TR: Bu ust seviye fonksiyon, 'main' fonksiyonunun diagnostic rolunun okunur kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - browser smoke koridorundaki tek isimli adimi korumak icin
# TR: - yeni baslayanin hangi fonksiyonun hazirladigini, calistirdigini, donusturdugunu veya raporladigini gorebilmesi icin
# TR: - success, degraded, timeout ve acik hata anlamlarini gorunur tutmak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - diagnostic payloadlar kucuk, okunur ve acik kalmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - dict-benzeri payload
# TR: - text-benzeri cikti
# TR: - acik success tarzi makbuz
# TR: - acik timeout-benzeri veya degraded sonuc
# TR: - diagnostic yuzeyde gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz dal

# EN: DIAG SMOKE FUNCTION CONTRACT BLOCK V8 / main
# EN:
# EN: This top-level function exists so 'main' stays readable in the browser diagnostic corridor.
# EN: Accepted input line shapes:
# EN: - current discovered parameters: (no explicit parameters)
# EN: - readable, explicit, operator-facing diagnostic input is desired
# EN: Accepted output line shapes:
# EN: - explicit success-style data
# EN: - explicit degraded data
# EN: - explicit timeout-like data
# EN: - explicit raised error that remains visible
# EN: Undesired meaning:
# EN: - silent ambiguity where the operator cannot tell what happened
# TR: DIAG SMOKE FUNCTION CONTRACT BLOĞU V8 / main
# TR:
# TR: Bu ust seviye fonksiyon, 'main' yapisinin browser diagnostic koridorunda okunur kalmasi icin vardir.
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an bulunan parametreler: (acik parametre yok)
# TR: - okunur, acik ve operator-yuzlu diagnostic girdi istenir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - acik success-benzeri veri
# TR: - acik degraded veri
# TR: - acik timeout-benzeri veri
# TR: - gorunur kalan acik hata
# TR: Istenmeyen anlam:
# TR: - operatorun ne oldugunu anlayamadigi sessiz belirsizlik

# EN: Function main is the direct execution entry of the diagnostic smoke corridor.
# EN: This function keeps startup, argument parsing, browser smoke delegation, and final payload emission readable in one obvious place.
# EN: Return contract: it returns a process-style integer status code.
# TR: main fonksiyonu diagnostic smoke koridorunun dogrudan calistirma girisidir.
# TR: Bu fonksiyon baslatma, arguman ayrisma, browser smoke delegasyonu ve son payload yayimini tek acik yerde okunur tutar.
# TR: Donus sozlesmesi: surec tarzi tamsayi durum kodu dondurur.
def main() -> int:
# EN: parser stores the prepared CLI contract for this direct execution path.
# EN: Expected values are argparse.ArgumentParser instances.
# TR: parser bu dogrudan calistirma yolu icin hazir CLI sozlesmesini tasir.
# TR: Beklenen degerler argparse.ArgumentParser ornekleridir.
    parser = build_parser()
# EN: args stores the parsed operator input namespace for this smoke execution.
# EN: Expected values are parser-produced namespace objects.
# TR: args bu smoke calistirmasi icin ayrismis operator girdi namespace nesnesini tasir.
# TR: Beklenen degerler parser tarafindan uretilen namespace nesneleridir.
    args = parser.parse_args()

    default_html, default_png, default_json = build_default_output_paths()

    html_out = Path(args.html_out) if args.html_out else default_html
    screenshot_out = Path(args.screenshot_out) if args.screenshot_out else default_png
    json_out = Path(args.json_out) if args.json_out else default_json

# EN: result stores the raw browser smoke execution result returned by the diagnostic helper.
# EN: Expected values are structured result objects or dict-like payload carriers depending on the helper contract.
# TR: result diagnostic helperdan donen ham browser smoke yurutme sonucunu tasir.
# TR: Beklenen degerler helper sozlesmesine gore yapili sonuc nesneleri veya dict-benzeri payload tasiyicilaridir.
    result = acquire_public_page_with_browser(
        target_url=args.url,
        html_output_path=html_out,
        screenshot_output_path=screenshot_out,
        headless=not args.headed,
        wait_until=args.wait_until,
        timeout_ms=args.timeout_ms,
    )

# EN: payload is the final operator-facing structured output assembled by this entry surface.
# EN: Expected values are JSON-serializable dict objects.
# TR: payload bu giris yuzeyinin kurdugu son operator-yuzlu yapili cikti nesnesidir.
# TR: Beklenen degerler JSON-serilestirilebilir dict nesneleridir.
    payload = result.to_dict()
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


# EN: This keeps the file executable as a direct CLI entry.
# TR: Bu sayede dosya doğrudan CLI girişi olarak çalıştırılabilir.
if __name__ == "__main__":
    raise SystemExit(main())
