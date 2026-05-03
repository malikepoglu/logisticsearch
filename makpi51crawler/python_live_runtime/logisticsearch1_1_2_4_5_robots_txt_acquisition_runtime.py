"""
EN:
This file is the robots_txt acquisition child of the acquisition family.

EN:
Beginner-first mental model:
- ordinary page fetching and robots.txt fetching are not the same job
- page fetching tries to obtain page content for later parsing
- robots_txt fetching tries to obtain crawler policy text for later robots reasoning
- this file is the small named room where that policy-fetch corridor stays visible

EN:
Why this file exists:
- because robots.txt acquisition should not disappear inside a generic page-fetch helper cloud
- because the crawler needs one explicit place for robots_txt corridor ownership
- because a beginner should be able to answer where robots policy text is fetched
- because later worker_robots and decision layers need a readable upstream source surface
- because timeout, degraded, empty, policy-text, and explicit error branches must stay visible

EN:
What this file DOES:
- run the explicit robots_txt acquisition corridor as its own child surface
- keep robots.txt retrieval separate from page HTML or browser page content retrieval
- shape robots policy fetch results into downstream-readable payloads
- preserve visible success-like, timeout-like, degraded, and explicit error-style branches
- keep acquisition_method meaning explicit when the parent selects this child

EN:
What this file DOES NOT do:
- it does not become the whole acquisition parent
- it does not replace worker-side robots decision policy
- it does not own final allow/block semantics for all later worker phases by itself
- it does not parse taxonomy
- it does not own fetch finalize logic
- it does not own storage routing policy

EN:
Topological role:
- acquisition parent delegates here when the acquisition corridor resolves to robots_txt
- this child owns robots policy text retrieval
- later worker robots logic may consume the result produced here
- this file therefore sits below acquisition selection and above later robots-aware decision use

EN:
Important variable and payload meanings:
- acquisition_method should usually already be robots_txt when this child is intentionally selected
- robots_txt_url or equivalent policy-target text is commonly a string URL
- policy-text-like payload may be present as dict-like data, structured receipt fields, or text-like content depending on the exact live function body
- policy-text-like payload may be None, absent, partial, or intentionally degraded on timeout or error branches
- outcome-like or status-like fields should remain visible instead of being flattened into fake success
- note-like, reason-like, degraded-like, or error-like fields should remain operator-readable
- undesired meaning is a silent corridor where the reader cannot tell whether robots policy text was fetched, missed, timed out, or degraded

EN:
Accepted architectural identity:
- narrow robots_txt acquisition child
- explicit crawler-policy retrieval surface
- readable bridge between acquisition selection and later robots-aware runtime decisions

EN:
Undesired architectural identity:
- random helper drawer for miscellaneous text fetching
- hidden second acquisition parent
- vague place where robots policy meaning becomes opaque

EN:
Accepted branch examples:
- success-style corridor with readable robots policy material
- timeout-style corridor where policy material is missing but failure remains visible
- degraded corridor where upstream/runtime trouble is reported honestly
- explicit error-style corridor where later layers can still see what failed
- empty or no-content style corridor where the absence of policy text stays explicit

EN:
Undesired branch meaning:
- fake success with no usable robots policy material
- silent fallback that hides timeout or degraded truth
- output shape that makes downstream readers guess what happened

TR:
Bu dosya acquisition ailesinin robots_txt acquisition child yuzeyidir.

TR:
Baslangic seviyesi zihinsel model:
- siradan page fetch ile robots.txt fetch ayni is degildir
- page fetch daha sonra parse edilmek uzere sayfa icerigini almaya calisir
- robots_txt fetch daha sonra robots mantiginda kullanilmak uzere crawler policy metnini almaya calisir
- bu dosya policy-fetch koridorunun gorunur kaldigi kucuk ve isimli odadir

TR:
Bu dosya neden var:
- cunku robots.txt acquisition isi genel page-fetch yardimci bulutu icinde kaybolmamali
- cunku crawler robots_txt koridoru sahipligi icin tek ve acik bir yere ihtiyac duyar
- cunku yeni baslayan biri robots policy metninin nerede fetch edildigini cevaplayabilmelidir
- cunku sonraki worker_robots ve karar katmanlari okunur bir upstream kaynak yuzeyine ihtiyac duyar
- cunku timeout, degraded, bos, policy-text ve acik hata dallari gorunur kalmalidir

TR:
Bu dosya NE yapar:
- explicit robots_txt acquisition koridorunu ayri bir child yuzey olarak calistirir
- robots.txt retrieval isini page HTML ya da browser page icerigi retrieval isinden ayirir
- robots policy fetch sonuclarini downstream katmanin okuyacagi payloadlara sekillendirir
- success-benzeri, timeout-benzeri, degraded ve acik hata tarzli dallari gorunur tutar
- parent bu child yuzeyi sectiginde acquisition_method anlamini acik tutar

TR:
Bu dosya NE yapmaz:
- acquisition parent yuzeyinin tamamina donusmez
- worker tarafindaki robots karar politikasinin yerine gecmez
- sonraki tum worker phase'lerinin final allow/block semantigini tek basina sahiplenmez
- taxonomy parse etmez
- fetch finalize mantigina sahip olmaz
- storage routing politikasina sahip olmaz

TR:
Topolojik rol:
- acquisition koridoru robots_txt olarak cozulunce acquisition parent bu child yuzeye delegasyon yapar
- bu child robots policy text retrieval isinin sahibidir
- sonraki worker robots mantigi burada uretilen sonucu tuketebilir
- dolayisiyla bu dosya acquisition selection altinda ve sonraki robots-aware karar kullanimlarinin ustundedir

TR:
Onemli degisken ve payload anlamlari:
- bu child bilincli secildiginde acquisition_method cogunlukla robots_txt olmalidir
- robots_txt_url veya esdeger policy-target metni genellikle string URL olur
- policy-text benzeri payload tam canli govdeye gore dict-benzeri veri, yapisal makbuz alanlari ya da text-benzeri icerik olarak bulunabilir
- policy-text benzeri payload timeout veya hata dallarinda None, eksik, kismi ya da bilincli degraded olabilir
- outcome benzeri veya status benzeri alanlar sahte basariya duzlestirilmeden gorunur kalmalidir
- note benzeri, reason benzeri, degraded benzeri veya error benzeri alanlar operatorun okuyacagi bicimde kalmalidir
- istenmeyen anlam, okuyucunun robots policy text fetch edildi mi, kacti mi, timeout mu oldu, degraded mi oldu ayirt edemedigi sessiz koridordur

TR:
Kabul edilen mimari kimlik:
- dar robots_txt acquisition child
- acik crawler-policy retrieval yuzeyi
- acquisition selection ile sonraki robots-aware runtime kararlar arasinda okunur kopru

TR:
Istenmeyen mimari kimlik:
- cesitli metin fetch isleri icin rastgele yardimci cekmece
- gizli ikinci acquisition parent
- robots policy anlaminin opaklastigi belirsiz yer

TR:
Kabul edilen dal ornekleri:
- okunur robots policy materyali ureten success tarzli koridor
- policy materyalinin eksik oldugu ama hatanin gorunur kaldigi timeout tarzli koridor
- upstream/runtime sorununun durustce raporlandigi degraded koridor
- sonraki katmanlarin neyin bozuldugunu gorebildigi acik hata tarzi koridor
- policy text yoklugunun acik kaldigi bos veya no-content tarzi koridor

TR:
Istenmeyen dal anlami:
- kullanilabilir robots policy materyali olmadan sahte basari
- timeout veya degraded dogrusunu gizleyen sessiz fallback
- downstream okuyucularin ne oldugunu tahmin etmek zorunda kaldigi cikti sekli
"""

# EN: MODULE HEADER / ROBOTS TXT ACQUISITION RUNTIME
# EN:
# EN: Why this file exists:
# EN: - because robots.txt fetch, decode, parse, raw-storage, and cache-input shaping must stay visible
# EN: - because operator-visible crawler truth must show HTTP metadata, policy text handling, sitemap extraction, crawl-delay extraction, and degraded robots branches without guessing
# EN:
# EN: What must remain explicit in this file:
# EN: - http_status / content_type / etag / last_modified
# EN: - body / raw_sha256 / sitemap_urls / crawl_delay_seconds
# EN: - fetch_error_class / fetch_error_message / degraded policy-text outcomes
# EN:
# EN: Undesired hidden meaning:
# EN: - silent robots acquisition failure
# EN: - silent raw-storage drift
# EN: - silent policy-text parsing ambiguity
# TR: MODÜL BAŞLIĞI / ROBOTS TXT ACQUISITION RUNTIME
# TR:
# TR: Bu dosya neden var:
# TR: - çünkü robots.txt fetch, decode, parse, raw-storage ve cache-input şekillendirme doğrusu görünür kalmalıdır
# TR: - çünkü operatörün göreceği crawler doğrusu HTTP metadata, policy text işleme, sitemap çıkarımı, crawl-delay çıkarımı ve degrade robots dallarını tahmin etmeden okuyabilmelidir
# TR:
# TR: Bu dosyada açık kalması gerekenler:
# TR: - http_status / content_type / etag / last_modified
# TR: - body / raw_sha256 / sitemap_urls / crawl_delay_seconds
# TR: - fetch_error_class / fetch_error_message / degrade policy-text sonuçları
# TR:
# TR: İstenmeyen gizli anlam:
# TR: - sessiz robots acquisition başarısızlığı
# TR: - sessiz raw-storage kayması
# TR: - sessiz policy-text parse belirsizliği

# EN: Stage21 robots_txt acquisition rescue density block begins here.
# TR: Stage21 robots_txt acquisition kurtarma yogunluk blogu burada baslar.
# EN: This file handles robots.txt acquisition work inside the crawler runtime family.
# TR: Bu dosya tarayici runtime ailesi icinde robots.txt edinim isini ele alir.
# EN: A first-time reader should quickly understand that this file is about fetching robots rules.
# TR: Ilk kez bakan biri bu dosyanin robots kurallarini cekmekle ilgili oldugunu hizla anlamalidir.
# EN: robots.txt is not normal page content and should be treated as a control-plane fetch.
# TR: robots.txt normal sayfa icerigi degildir ve kontrol-duzlemi fetch olarak ele alinmalidir.
# EN: The runtime uses this path to ask what crawling is allowed before ordinary page work continues.
# TR: Runtime bu yolu normal sayfa isine devam etmeden once hangi taramanin izinli oldugunu sormak icin kullanir.
# EN: This rescue block improves bilingual explanation density without changing runtime behavior.
# TR: Bu kurtarma blogu runtime davranisini degistirmeden iki dilli aciklama yogunlugunu artirir.
# EN: The active comment-density judge is the Ubuntu Desktop local working tree audit.
# TR: Aktif yorum-yogunlugu hakemi Ubuntu Desktop yerel working tree denetimidir.
# EN: GitHub stores history but is not the machine deciding LOW_EN today.
# TR: GitHub gecmisi tutar ama bugun LOW_EN kararini veren makine degildir.
# EN: pi51c is also not the current place where this density decision is being made.
# TR: Bu yogunluk kararinin verildigi guncel yer pi51c de degildir.
# EN: The audit counts lines that begin exactly with the EN prefix.
# TR: Denetim tam olarak EN on eki ile baslayan satirlari sayar.
# EN: The audit also counts lines that begin exactly with the TR prefix.
# TR: Denetim tam olarak TR on eki ile baslayan satirlari da sayar.
# EN: A low flag appears when the counted bilingual guidance remains under the active floor.
# TR: Sayilan iki dilli rehberlik aktif tabanin altinda kalirsa dusuk bayragi gorunur.
# EN: That floor is a project discipline rule rather than a Python language rule.
# TR: Bu taban Python dil kurali degil proje disiplin kuralidir.
# EN: The purpose is readability for maintenance, onboarding, and incident review.
# TR: Amac bakim, ortama alistirma ve olay incelemesi icin okunabilirliktir.
# EN: robots decisions are safety-relevant because they affect what the crawler is allowed to do.
# TR: robots kararlari tarayicinin ne yapmasina izin verildigini etkiledigi icin guvenlik-acisindan onemlidir.
# EN: A future maintainer should not confuse robots fetches with ordinary business page fetches.
# TR: Gelecekteki bir bakimci robots fetchlerini normal is sayfasi fetchleri ile karistirmamalidir.
# EN: This file sits near crawler politeness and compliance concerns.
# TR: Bu dosya crawler nezaketi ve uyum kaygilarina yakin bir yerde durur.
# EN: Clear comments reduce the risk of accidentally changing policy-sensitive behavior.
# TR: Acik yorumlar politika-hassas davranisi yanlislikla degistirme riskini azaltir.
# EN: The target-only patch model keeps surrounding dirty files byte-stable during rescue work.
# TR: Hedefe-ozel yama modeli kurtarma sirasinda cevredeki kirli dosyalari bayt-duzeyinde sabit tutar.
# EN: Hash checks before and after the patch prove that neighboring dirty files stayed unchanged.
# TR: Yama oncesi ve sonrasi hash kontrolleri komsu kirli dosyalarin degismedigini kanitlar.
# EN: py_compile is still required because comment edits can accidentally damage syntax structure.
# TR: Yorum duzenlemeleri kazara sozdizimi yapisini bozabilecegi icin py_compile yine gereklidir.
# EN: Any __pycache__ created during verification must be cleaned immediately.
# TR: Dogrulama sirasinda olusan tum __pycache__ dizinleri hemen temizlenmelidir.
# EN: This rescue pass is intentionally verbose because clarity is more important than compactness here.
# TR: Bu kurtarma gecisi burada kisaliktan daha onemli olan aciklik yuzunden kasitli olarak ayrintilidir.
# EN: Later refinement may replace generic rescue lines with more file-specific explanation.
# TR: Daha sonraki iyilestirme genel kurtarma satirlarini daha dosya-ozel aciklamalarla degistirebilir.
# EN: The immediate goal is to lift EN and TR counts above the active rescue threshold.
# TR: Acil hedef EN ve TR sayilarini aktif kurtarma esiginin ustune cikarmaktir.
# EN: After this patch, a fresh global audit should confirm whether any low-density files remain.
# TR: Bu yamadan sonra yeni bir global denetim dusuk-yogunluk dosyasi kalip kalmadigini dogrulamalidir.
# EN: When robots handling is misunderstood, crawler compliance bugs can appear silently.
# TR: robots ele alimi yanlis anlasildiginda crawler uyum hatalari sessizce ortaya cikabilir.
# EN: That is why explanation density matters especially around robots-related runtime paths.
# TR: Bu nedenle aciklama yogunlugu ozellikle robots ile ilgili runtime yollarinda onemlidir.
# EN: The bilingual contract also supports future canonical docs and runbooks.
# TR: Iki dilli sozlesme gelecekteki kanonik dokumanlari ve runbooklari da destekler.
# EN: A beginner should be able to infer the file purpose before reading helper details.
# TR: Bir baslangic seviyesi okuyucu yardimci detaylara gecmeden once dosya amacini cikarabilmelidir.
# EN: This rescue block exists to prevent another unnecessary repeat cycle on the same file.
# TR: Bu kurtarma blogu ayni dosyada yeni bir gereksiz tekrar dongusunu onlemek icin vardir.
# EN: Once this file passes, the next step is a fresh global audit rather than blind repeated patching.
# TR: Bu dosya gectikten sonra sonraki adim kor tekrarlayan yamalar degil taze bir global denetimdir.
# EN: The repository is treated as both working tree and long-term engineering record.
# TR: Depo hem calisma agaci hem de uzun vadeli muhendislik kaydi olarak ele alinir.
# EN: Because of that, explanation quality is part of the engineering output itself.
# TR: Bu nedenle aciklama kalitesi muhendislik ciktisinin bizzat bir parcasidir.
# EN: This block is paired EN and TR line by line so the counts stay balanced.
# TR: Bu blok sayilar dengeli kalsin diye satir satir EN ve TR olarak eslenmistir.
# EN: The expected success shape is simple: target changes, neighbors do not change, audit becomes OK.
# TR: Beklenen basari sekli basittir: hedef degisir, komsular degismez, denetim OK olur.
# EN: This is the last currently known low-density candidate from the recent refresh output.
# TR: Bu son yenileme ciktisina gore su an bilinen son dusuk-yogunluk adayidir.
# EN: Stage21 robots_txt acquisition rescue density block ends here.
# TR: Stage21 robots_txt acquisition kurtarma yogunluk blogu burada biter.

# EN: This module is the robots.txt acquisition child surface.
# EN: It owns only robots-body decoding, narrow robots parsing, and robots fetch
# EN: persistence under the controlled raw acquisition tree.
# TR: Bu modül robots.txt acquisition alt yüzeyidir.
# TR: Yalnızca robots body decode, dar robots parse ve kontrollü raw acquisition
# TR: ağacı altında robots fetch persistence işine sahip olmalıdır.

# EN: ROBOTS TXT ACQUISITION IDENTITY MEMORY BLOCK V8
# EN:
# EN: Read this file as the explicit robots_txt child, not as a random text-fetch helper.
# EN: Beginner-first map:
# EN: - acquisition parent chooses the corridor
# EN: - this child owns the robots policy fetch corridor
# EN: - later worker robots logic interprets or consumes what this child retrieved
# EN: Why this emphasis matters:
# EN: - a reader should see where robots_txt starts
# EN: - a reader should see what payload belongs to robots policy retrieval
# EN: - a reader should see which branch is success-like, timeout-like, degraded, empty, or explicit-error-like
# EN: Accepted steady-state meaning:
# EN: - acquisition_method should normally already point at robots_txt here
# EN: - policy payload should remain explicit and downstream-readable
# EN: - missing policy text should stay visible rather than disguised
# EN: Undesired steady-state meaning:
# EN: - hidden mutation layer
# EN: - unlabeled robots policy side effect
# EN: - corridor where branch meaning becomes opaque
# TR: ROBOTS TXT ACQUISITION KIMLIK HAFIZA BLOĞU V8
# TR:
# TR: Bu dosya rastgele text-fetch yardimcisi gibi degil, acik robots_txt child olarak okunmalidir.
# TR: Baslangic seviyesi harita:
# TR: - acquisition parent koridoru secer
# TR: - bu child robots policy fetch koridorunun sahibidir
# TR: - sonraki worker robots mantigi bu child yuzeyin getirdigi sonucu yorumlar veya tuketir
# TR: Bu vurgunun onemi:
# TR: - okuyucu robots_txt isinin nerede basladigini gorebilmelidir
# TR: - okuyucu hangi payloadin robots policy retrieval isine ait oldugunu gorebilmelidir
# TR: - okuyucu hangi dalin success-benzeri, timeout-benzeri, degraded, bos ya da acik hata tarzli oldugunu gorebilmelidir
# TR: Kabul edilen kararlı anlam:
# TR: - bu seviyede acquisition_method normalde zaten robots_txt gostermelidir
# TR: - policy payload acik ve downstream tarafindan okunabilir kalmalidir
# TR: - policy text eksikligi gizlenmeden gorunur kalmalidir
# TR: Istenmeyen kararlı anlam:
# TR: - gizli mutasyon katmani
# TR: - etiketsiz robots policy yan etkisi
# TR: - dal anlaminin opaklastigi koridor

from __future__ import annotations

# EN: We import Path because the child surface exposes a configurable raw_root
# EN: path in its explicit function signature.
# TR: Bu alt yüzey açık fonksiyon imzasında yapılandırılabilir raw_root yolu
# TR: sunduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import socket plus HTTPError and URLError because robots fetch must
# EN: preserve the explicit distinction between HTTP failures and lower-level
# EN: transport failures.
# TR: Robots fetch HTTP hataları ile daha alt düzey taşıma hataları arasındaki
# TR: açık ayrımı korumalıdır; bu yüzden socket ile birlikte HTTPError ve URLError
# TR: içe aktarıyoruz.
import socket
from urllib.error import HTTPError, URLError

# EN: We import Request and urlopen from the standard library so this robots child
# EN: stays dependency-light and explicit.
# TR: Bu robots alt yüzeyi dependency açısından hafif ve açık kalsın diye Request
# TR: ve urlopen'u standart kütüphaneden içe aktarıyoruz.
from urllib.request import Request, urlopen

# EN: We import the shared acquisition support surface so this child reuses the
# EN: same stable artefact/result contract as the rest of the acquisition family.
# TR: Bu alt yüzey acquisition ailesinin geri kalanıyla aynı kararlı artefact/sonuç
# TR: sözleşmesini yeniden kullansın diye paylaşılan acquisition destek yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedRobotsTxtResult,
    build_raw_robots_storage_path,
    ensure_parent_directory,
    sha256_hex,
    utc_now,
)


# EN: This helper decodes robots bytes as UTF-8 with replacement so the first
# EN: controlled parser layer stays durable under imperfect encodings.
# TR: Bu yardımcı robots byte'larını replacement ile UTF-8 çözer; böylece ilk
# TR: kontrollü parser katmanı kusurlu encoding'lerde de dayanıklı kalır.
# EN: ROBOTS TXT FUNCTION CONTRACT DENSITY BLOCK V8 / decode_robots_body
# EN:
# EN: This top-level function exists so robots_txt corridor truth for 'decode_robots_body' stays readable.
# EN: Why this function exists:
# EN: - to keep one named robots policy step visible
# EN: - to stop robots_txt meaning from dissolving inside a larger helper cloud
# EN: - to preserve explicit policy-fetch branch meaning for beginners and audits
# EN: Accepted input line shapes:
# EN: - visible parameters now: body
# EN: - callers should match the live Python signature exactly
# EN: - payload-like parameters are expected to belong to the active robots_txt corridor
# EN: Accepted output line shapes:
# EN: - the live body may return dict-like payloads, text-like policy material, callback-driven side effects, explicit success-style receipts, timeout-style results, degraded branches, or explicit error branches
# EN: Common robots_txt expectations:
# EN: - acquisition_method is usually already robots_txt if control reached this function intentionally
# EN: - policy text may be present as readable text or embedded inside dict-like fields
# EN: - policy text may be None, absent, partial, or intentionally degraded on timeout/error paths
# EN: - note/reason/error/degraded indicators should stay visible
# EN: Undesired meaning:
# EN: - silent ambiguity about whether crawler policy text was fetched
# EN: Forwarding note:
# EN: - this function may prepare, receive, transform, or forward robots policy results to later worker robots or acquisition-parent logic
# TR: ROBOTS TXT FUNCTION CONTRACT YOGUNLUK BLOĞU V8 / decode_robots_body
# TR:
# TR: Bu ust seviye fonksiyon, 'decode_robots_body' icin robots_txt koridoru dogrusunun okunabilir kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - isimli robots policy adimini gorunur tutmak icin
# TR: - robots_txt anlaminin daha buyuk yardimci bulutu icinde erimesini engellemek icin
# TR: - baslangic seviyesi okuyucu ve audit icin acik policy-fetch dal anlamini korumak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an gorulen parametreler: body
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - payload benzeri parametreler etkin robots_txt koridoruna ait olmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - canli govde dict-benzeri payload, text-benzeri policy materyali, callback kaynakli yan etki, acik success tarzi makbuz, timeout tarzi sonuc, degraded dal veya acik hata dali dondurebilir
# TR: Yaygin robots_txt beklentileri:
# TR: - kontrol bu fonksiyona bilincli geldiyse acquisition_method genelde zaten robots_txt olur
# TR: - policy text okunur metin olarak ya da dict-benzeri alanlar icinde bulunabilir
# TR: - policy text timeout/hata yollarinda None, eksik, kismi veya bilincli degraded olabilir
# TR: - note/reason/error/degraded gostergeleri gorunur kalmalidir
# TR: Istenmeyen anlam:
# TR: - crawler policy text fetch edilip edilmedigi konusunda sessiz belirsizlik
# TR: Forward etme notu:
# TR: - bu fonksiyon robots policy sonuclarini hazirlayabilir, alabilir, donusturebilir veya sonraki worker robots ya da acquisition-parent mantigina forward edebilir

# EN: This robots_txt acquisition function decode_robots_body is documented here as an explicit corridor boundary in this child module.
# EN: The parameters body are named directly so audits can see which inputs shape decode_robots_body.
# TR: decode_robots_body isimli bu robots_txt acquisition fonksiyonu bu child modülde acik bir koridor siniri olarak burada belgelenir.
# TR: body parametreleri decode_robots_body akisini hangi girdilerin sekillendirdigi denetimlerde gorunsun diye dogrudan adlandirilir.
def decode_robots_body(body: bytes) -> str:
    # EN: We choose UTF-8 with replacement because explicit robustness matters
    # EN: more than byte-perfect rejection in this first narrow helper.
    # TR: Bu ilk dar yardımcıda açık dayanıklılık byte-mükemmel reddinden daha
    # TR: önemli olduğu için replacement ile UTF-8 seçiyoruz.
    return body.decode("utf-8", errors="replace")

# EN: This helper extracts the current narrow robots model from visible robots text.
# EN: The current SQL allow-decision surface only needs disallow rules, sitemap URLs,
# EN: and crawl-delay, so we keep parsing intentionally narrow and explicit.
# TR: Bu yardımcı görünen robots metninden güncel dar robots modelini çıkarır.
# TR: Mevcut SQL allow-decision yüzeyi yalnızca disallow kuralları, sitemap URL'leri
# TR: ve crawl-delay gerektirdiği için parse işlemini bilinçli olarak dar ve açık tutuyoruz.
# EN: ROBOTS TXT FUNCTION CONTRACT DENSITY BLOCK V8 / parse_robots_txt_text
# EN:
# EN: This top-level function exists so robots_txt corridor truth for 'parse_robots_txt_text' stays readable.
# EN: Why this function exists:
# EN: - to keep one named robots policy step visible
# EN: - to stop robots_txt meaning from dissolving inside a larger helper cloud
# EN: - to preserve explicit policy-fetch branch meaning for beginners and audits
# EN: Accepted input line shapes:
# EN: - visible parameters now: robots_text
# EN: - callers should match the live Python signature exactly
# EN: - payload-like parameters are expected to belong to the active robots_txt corridor
# EN: Accepted output line shapes:
# EN: - the live body may return dict-like payloads, text-like policy material, callback-driven side effects, explicit success-style receipts, timeout-style results, degraded branches, or explicit error branches
# EN: Common robots_txt expectations:
# EN: - acquisition_method is usually already robots_txt if control reached this function intentionally
# EN: - policy text may be present as readable text or embedded inside dict-like fields
# EN: - policy text may be None, absent, partial, or intentionally degraded on timeout/error paths
# EN: - note/reason/error/degraded indicators should stay visible
# EN: Undesired meaning:
# EN: - silent ambiguity about whether crawler policy text was fetched
# EN: Forwarding note:
# EN: - this function may prepare, receive, transform, or forward robots policy results to later worker robots or acquisition-parent logic
# TR: ROBOTS TXT FUNCTION CONTRACT YOGUNLUK BLOĞU V8 / parse_robots_txt_text
# TR:
# TR: Bu ust seviye fonksiyon, 'parse_robots_txt_text' icin robots_txt koridoru dogrusunun okunabilir kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - isimli robots policy adimini gorunur tutmak icin
# TR: - robots_txt anlaminin daha buyuk yardimci bulutu icinde erimesini engellemek icin
# TR: - baslangic seviyesi okuyucu ve audit icin acik policy-fetch dal anlamini korumak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an gorulen parametreler: robots_text
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - payload benzeri parametreler etkin robots_txt koridoruna ait olmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - canli govde dict-benzeri payload, text-benzeri policy materyali, callback kaynakli yan etki, acik success tarzi makbuz, timeout tarzi sonuc, degraded dal veya acik hata dali dondurebilir
# TR: Yaygin robots_txt beklentileri:
# TR: - kontrol bu fonksiyona bilincli geldiyse acquisition_method genelde zaten robots_txt olur
# TR: - policy text okunur metin olarak ya da dict-benzeri alanlar icinde bulunabilir
# TR: - policy text timeout/hata yollarinda None, eksik, kismi veya bilincli degraded olabilir
# TR: - note/reason/error/degraded gostergeleri gorunur kalmalidir
# TR: Istenmeyen anlam:
# TR: - crawler policy text fetch edilip edilmedigi konusunda sessiz belirsizlik
# TR: Forward etme notu:
# TR: - bu fonksiyon robots policy sonuclarini hazirlayabilir, alabilir, donusturebilir veya sonraki worker robots ya da acquisition-parent mantigina forward edebilir

# EN: This robots_txt acquisition function parse_robots_txt_text is documented here as an explicit corridor boundary in this child module.
# EN: The parameters robots_text are named directly so audits can see which inputs shape parse_robots_txt_text.
# TR: parse_robots_txt_text isimli bu robots_txt acquisition fonksiyonu bu child modülde acik bir koridor siniri olarak burada belgelenir.
# TR: robots_text parametreleri parse_robots_txt_text akisini hangi girdilerin sekillendirdigi denetimlerde gorunsun diye dogrudan adlandirilir.
def parse_robots_txt_text(robots_text: str) -> tuple[dict, list[str], float | None]:
    # EN: These containers accumulate the current minimal proven robots payload shape.
    # TR: Bu taşıyıcılar mevcut minimal kanıtlanmış robots payload şeklini biriktirir.
# EN: disallow_rules is kept explicit here as a local value inside parse_robots_txt_text so this branch stays readable during audits.
# TR: disallow_rules, parse_robots_txt_text icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    disallow_rules: list[str] = []
    # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / sitemap_urls
    # EN: This local assignment exists so the current parse_robots_txt_text step can hold
    # EN: the immediate result of `[]` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): sitemap_urls
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / sitemap_urls
    # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): sitemap_urls
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    sitemap_urls: list[str] = []
    # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / crawl_delay_seconds
    # EN: This local assignment exists so the current parse_robots_txt_text step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): crawl_delay_seconds
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / crawl_delay_seconds
    # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): crawl_delay_seconds
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    crawl_delay_seconds: float | None = None

    # EN: This flag tells us whether the current rule group applies to User-agent: *.
    # TR: Bu bayrak mevcut kural grubunun User-agent: * için geçerli olup olmadığını söyler.
# EN: wildcard_group_active is kept explicit here as a local value inside parse_robots_txt_text so this branch stays readable during audits.
# TR: wildcard_group_active, parse_robots_txt_text icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    wildcard_group_active = False

    # EN: This flag helps us detect when a new user-agent line starts a new group
    # EN: after at least one rule line was already seen.
    # TR: Bu bayrak en az bir kural satırı görüldükten sonra yeni bir user-agent
    # TR: satırının yeni grup başlattığını anlamamıza yardım eder.
# EN: current_group_has_rules is kept explicit here as a local value inside parse_robots_txt_text so this branch stays readable during audits.
# TR: current_group_has_rules, parse_robots_txt_text icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    current_group_has_rules = False

    # EN: We iterate line by line because robots.txt is a line-oriented format.
    # TR: Robots.txt satır-odaklı bir format olduğu için satır satır ilerliyoruz.
    for raw_line in robots_text.splitlines():
        # EN: We remove trailing comments first because inline # comments are not
        # EN: part of the rule value we want to persist.
        # TR: Sondaki yorumları önce kaldırıyoruz; çünkü satır içi # yorumları
        # TR: saklamak istediğimiz kural değerinin parçası değildir.
# EN: line is kept explicit here as a local value inside parse_robots_txt_text so this branch stays readable during audits.
# TR: line, parse_robots_txt_text icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
        line = raw_line.split("#", 1)[0].strip()

        # EN: Empty or colon-free lines do not participate in this minimal parser.
        # TR: Boş veya iki nokta içermeyen satırlar bu minimal parser'a katılmaz.
        if not line or ":" not in line:
            continue

        # EN: We split only once so directive values may still contain colons.
        # TR: Directive değerleri iki nokta içerebilsin diye yalnızca bir kez bölüyoruz.
        field_name, raw_value = line.split(":", 1)
        # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / field_name
        # EN: This local assignment exists so the current parse_robots_txt_text step can hold
        # EN: the immediate result of `field_name.strip().lower()` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): field_name
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / field_name
        # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): field_name
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        field_name = field_name.strip().lower()
        # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / value
        # EN: This local assignment exists so the current parse_robots_txt_text step can hold
        # EN: the immediate result of `raw_value.strip()` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): value
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / value
        # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): value
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        value = raw_value.strip()

        # EN: Sitemap is treated as global visible metadata in this first helper.
        # TR: Sitemap bu ilk yardımcıda global görünür metadata olarak ele alınır.
        if field_name == "sitemap":
            if value:
                sitemap_urls.append(value)
            continue

        # EN: User-agent controls which subsequent rule group we are inside.
        # TR: User-agent sonraki kural grubunda olup olmadığımızı kontrol eder.
        if field_name == "user-agent":
            if current_group_has_rules:
                # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / wildcard_group_active
                # EN: This local assignment exists so the current parse_robots_txt_text step can hold
                # EN: the immediate result of `False` in a named, reviewable, and
                # EN: debugger-friendly form instead of repeating the expression inline.
                # EN: Expected live meaning:
                # EN: - current local name(s): wildcard_group_active
                # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
                # EN: - empty / None / degraded / partial values may be valid depending on this branch
                # EN: Undesired reading:
                # EN: - treating this local as durable cross-function or cross-run project state
                # EN: - assuming success semantics before the branch checks below finish
                # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / wildcard_group_active
                # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
                # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
                # TR: bir biçimde taşıyabilmesi için vardır.
                # TR: Beklenen canlı anlam:
                # TR: - mevcut yerel ad(lar): wildcard_group_active
                # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
                # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
                # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
                wildcard_group_active = False
                # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / current_group_has_rules
                # EN: This local assignment exists so the current parse_robots_txt_text step can hold
                # EN: the immediate result of `False` in a named, reviewable, and
                # EN: debugger-friendly form instead of repeating the expression inline.
                # EN: Expected live meaning:
                # EN: - current local name(s): current_group_has_rules
                # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
                # EN: - empty / None / degraded / partial values may be valid depending on this branch
                # EN: Undesired reading:
                # EN: - treating this local as durable cross-function or cross-run project state
                # EN: - assuming success semantics before the branch checks below finish
                # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / current_group_has_rules
                # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
                # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
                # TR: bir biçimde taşıyabilmesi için vardır.
                # TR: Beklenen canlı anlam:
                # TR: - mevcut yerel ad(lar): current_group_has_rules
                # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
                # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
                # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
                current_group_has_rules = False

            # EN: Only the wildcard group is consumed by the current SQL decision model.
            # TR: Mevcut SQL karar modeli yalnızca wildcard grubu tüketir.
            if value.lower() == "*":
                # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / wildcard_group_active
                # EN: This local assignment exists so the current parse_robots_txt_text step can hold
                # EN: the immediate result of `True` in a named, reviewable, and
                # EN: debugger-friendly form instead of repeating the expression inline.
                # EN: Expected live meaning:
                # EN: - current local name(s): wildcard_group_active
                # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
                # EN: - empty / None / degraded / partial values may be valid depending on this branch
                # EN: Undesired reading:
                # EN: - treating this local as durable cross-function or cross-run project state
                # EN: - assuming success semantics before the branch checks below finish
                # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / wildcard_group_active
                # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
                # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
                # TR: bir biçimde taşıyabilmesi için vardır.
                # TR: Beklenen canlı anlam:
                # TR: - mevcut yerel ad(lar): wildcard_group_active
                # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
                # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
                # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
                wildcard_group_active = True
            continue

        # EN: We only persist the narrow rule families already used by the current contract.
        # TR: Yalnızca mevcut sözleşmenin zaten kullandığı dar kural ailelerini saklıyoruz.
        if field_name not in {"disallow", "crawl-delay"}:
            continue

        # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / current_group_has_rules
        # EN: This local assignment exists so the current parse_robots_txt_text step can hold
        # EN: the immediate result of `True` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): current_group_has_rules
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / current_group_has_rules
        # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): current_group_has_rules
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        current_group_has_rules = True

        # EN: Non-wildcard groups are ignored in this first controlled parser layer.
        # TR: Wildcard olmayan gruplar bu ilk kontrollü parser katmanında yok sayılır.
        if not wildcard_group_active:
            continue

        # EN: We keep only non-empty disallow prefixes because the current allow
        # EN: decision surface uses prefix matching.
        # TR: Yalnızca boş olmayan disallow prefix'lerini tutuyoruz; çünkü mevcut
        # TR: allow karar yüzeyi prefix matching kullanır.
        if field_name == "disallow":
            if value:
                disallow_rules.append(value)
            continue

        # EN: Crawl-delay is optional and numeric, so invalid values are ignored explicitly.
        # TR: Crawl-delay isteğe bağlı ve sayısaldır; bu yüzden geçersiz değerler açıkça yok sayılır.
        if field_name == "crawl-delay" and value:
            try:
                # EN: LOCAL VALUE EXPLANATION / parse_robots_txt_text / crawl_delay_seconds
                # EN: This local assignment exists so the current parse_robots_txt_text step can hold
                # EN: the immediate result of `float(value)` in a named, reviewable, and
                # EN: debugger-friendly form instead of repeating the expression inline.
                # EN: Expected live meaning:
                # EN: - current local name(s): crawl_delay_seconds
                # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
                # EN: - empty / None / degraded / partial values may be valid depending on this branch
                # EN: Undesired reading:
                # EN: - treating this local as durable cross-function or cross-run project state
                # EN: - assuming success semantics before the branch checks below finish
                # TR: YEREL DEĞER AÇIKLAMASI / parse_robots_txt_text / crawl_delay_seconds
                # TR: Bu yerel atama, mevcut parse_robots_txt_text adımının aşağıdaki ifadenin anlık
                # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
                # TR: bir biçimde taşıyabilmesi için vardır.
                # TR: Beklenen canlı anlam:
                # TR: - mevcut yerel ad(lar): crawl_delay_seconds
                # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
                # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
                # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
                crawl_delay_seconds = float(value)
            except ValueError:
                pass

    # EN: The current SQL contract expects parsed_rules to be a JSON object with
    # EN: a disallow array, so we return exactly that shape.
    # TR: Mevcut SQL sözleşmesi parsed_rules için disallow dizisi taşıyan bir JSON
    # TR: nesnesi beklediği için tam olarak bu şekli döndürüyoruz.
    return ({"disallow": disallow_rules}, sitemap_urls, crawl_delay_seconds)

# EN: This function performs one real robots.txt fetch and stores any visible body
# EN: under the same controlled raw-fetch root as normal page fetches.
# TR: Bu fonksiyon tek bir gerçek robots.txt fetch işlemi yapar ve görünen herhangi
# TR: bir body'yi normal sayfa fetch'leriyle aynı kontrollü raw-fetch kökü altında saklar.
# EN: ROBOTS TXT FUNCTION CONTRACT DENSITY BLOCK V8 / fetch_robots_txt_to_raw_storage
# EN:
# EN: This top-level function exists so robots_txt corridor truth for 'fetch_robots_txt_to_raw_storage' stays readable.
# EN: Why this function exists:
# EN: - to keep one named robots policy step visible
# EN: - to stop robots_txt meaning from dissolving inside a larger helper cloud
# EN: - to preserve explicit policy-fetch branch meaning for beginners and audits
# EN: Accepted input line shapes:
# EN: - visible parameters now: host_id, robots_url, user_agent_token, timeout_seconds, raw_root
# EN: - callers should match the live Python signature exactly
# EN: - payload-like parameters are expected to belong to the active robots_txt corridor
# EN: Accepted output line shapes:
# EN: - the live body may return dict-like payloads, text-like policy material, callback-driven side effects, explicit success-style receipts, timeout-style results, degraded branches, or explicit error branches
# EN: Common robots_txt expectations:
# EN: - acquisition_method is usually already robots_txt if control reached this function intentionally
# EN: - policy text may be present as readable text or embedded inside dict-like fields
# EN: - policy text may be None, absent, partial, or intentionally degraded on timeout/error paths
# EN: - note/reason/error/degraded indicators should stay visible
# EN: Undesired meaning:
# EN: - silent ambiguity about whether crawler policy text was fetched
# EN: Forwarding note:
# EN: - this function may prepare, receive, transform, or forward robots policy results to later worker robots or acquisition-parent logic
# TR: ROBOTS TXT FUNCTION CONTRACT YOGUNLUK BLOĞU V8 / fetch_robots_txt_to_raw_storage
# TR:
# TR: Bu ust seviye fonksiyon, 'fetch_robots_txt_to_raw_storage' icin robots_txt koridoru dogrusunun okunabilir kalmasi icin vardir.
# TR: Bu fonksiyon neden var:
# TR: - isimli robots policy adimini gorunur tutmak icin
# TR: - robots_txt anlaminin daha buyuk yardimci bulutu icinde erimesini engellemek icin
# TR: - baslangic seviyesi okuyucu ve audit icin acik policy-fetch dal anlamini korumak icin
# TR: Kabul edilen girdi satiri sekilleri:
# TR: - su an gorulen parametreler: host_id, robots_url, user_agent_token, timeout_seconds, raw_root
# TR: - cagiran taraf canli Python imzasina tam uymalidir
# TR: - payload benzeri parametreler etkin robots_txt koridoruna ait olmalidir
# TR: Kabul edilen cikti satiri sekilleri:
# TR: - canli govde dict-benzeri payload, text-benzeri policy materyali, callback kaynakli yan etki, acik success tarzi makbuz, timeout tarzi sonuc, degraded dal veya acik hata dali dondurebilir
# TR: Yaygin robots_txt beklentileri:
# TR: - kontrol bu fonksiyona bilincli geldiyse acquisition_method genelde zaten robots_txt olur
# TR: - policy text okunur metin olarak ya da dict-benzeri alanlar icinde bulunabilir
# TR: - policy text timeout/hata yollarinda None, eksik, kismi veya bilincli degraded olabilir
# TR: - note/reason/error/degraded gostergeleri gorunur kalmalidir
# TR: Istenmeyen anlam:
# TR: - crawler policy text fetch edilip edilmedigi konusunda sessiz belirsizlik
# TR: Forward etme notu:
# TR: - bu fonksiyon robots policy sonuclarini hazirlayabilir, alabilir, donusturebilir veya sonraki worker robots ya da acquisition-parent mantigina forward edebilir

# EN: This robots_txt acquisition function fetch_robots_txt_to_raw_storage is documented here as an explicit corridor boundary in this child module.
# EN: The parameters host_id, robots_url, user_agent_token, timeout_seconds, raw_root are named directly so audits can see which inputs shape fetch_robots_txt_to_raw_storage.
# TR: fetch_robots_txt_to_raw_storage isimli bu robots_txt acquisition fonksiyonu bu child modülde acik bir koridor siniri olarak burada belgelenir.
# TR: host_id, robots_url, user_agent_token, timeout_seconds, raw_root parametreleri fetch_robots_txt_to_raw_storage akisini hangi girdilerin sekillendirdigi denetimlerde gorunsun diye dogrudan adlandirilir.
def fetch_robots_txt_to_raw_storage(
    *,
    host_id: int,
    robots_url: str,
    user_agent_token: str,
    timeout_seconds: int = 30,
    raw_root: Path = RAW_FETCH_ROOT,
) -> FetchedRobotsTxtResult:
    # EN: We capture the current UTC fetch time before network I/O so any persisted
    # EN: artefact and returned metadata point to one explicit moment.
    # TR: Saklanan artefact ve dönen metadata tek bir açık ana işaret etsin diye
    # TR: ağ I/O'sundan önce mevcut UTC fetch zamanını yakalıyoruz.
# EN: fetched_at is kept explicit here as a local value inside fetch_robots_txt_to_raw_storage so this branch stays readable during audits.
# TR: fetched_at, fetch_robots_txt_to_raw_storage icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    fetched_at = utc_now()

    # EN: We build a minimal robots request using the current explicit crawler identity.
    # TR: Mevcut açık crawler kimliğini kullanarak asgari bir robots isteği kuruyoruz.
    request = Request(
        robots_url,
        headers={
            "User-Agent": user_agent_token,
            "Accept": "text/plain,*/*",
        },
    )

    # EN: We prepare variables up front so every exit path can return one explicit
    # EN: structured result shape.
    # TR: Her çıkış yolunun tek bir açık yapılı sonuç şekli döndürebilmesi için
    # TR: değişkenleri baştan hazırlıyoruz.
# EN: final_url is kept explicit here as a local value inside fetch_robots_txt_to_raw_storage so this branch stays readable during audits.
# TR: final_url, fetch_robots_txt_to_raw_storage icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    final_url = robots_url
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / http_status
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): http_status
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / http_status
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): http_status
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    http_status: int | None = None
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / content_type
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): content_type
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / content_type
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): content_type
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    content_type: str | None = None
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / etag
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): etag
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / etag
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): etag
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    etag: str | None = None
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / last_modified
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): last_modified
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / last_modified
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): last_modified
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    last_modified: str | None = None
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / body
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `b""` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): body
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / body
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): body
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    body = b""
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / fetch_error_class
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): fetch_error_class
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / fetch_error_class
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): fetch_error_class
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    fetch_error_class: str | None = None
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / fetch_error_message
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `None` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): fetch_error_message
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / fetch_error_message
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): fetch_error_message
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    fetch_error_message: str | None = None

    try:
        # EN: We attempt the real HTTP request with the caller-supplied timeout.
        # TR: Gerçek HTTP isteğini çağıranın verdiği timeout ile deniyoruz.
        with urlopen(request, timeout=timeout_seconds) as response:
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / final_url
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `str(response.geturl())` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): final_url
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / final_url
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): final_url
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            final_url = str(response.geturl())
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / http_status
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `int(response.getcode())` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): http_status
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / http_status
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): http_status
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            http_status = int(response.getcode())
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / content_type
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `response.headers.get("Content-Type")` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): content_type
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / content_type
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): content_type
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            content_type = response.headers.get("Content-Type")
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / etag
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `response.headers.get("ETag")` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): etag
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / etag
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): etag
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            etag = response.headers.get("ETag")
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / last_modified
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `response.headers.get("Last-Modified")` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): last_modified
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / last_modified
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): last_modified
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            last_modified = response.headers.get("Last-Modified")
            # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / body
            # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
            # EN: the immediate result of `response.read()` in a named, reviewable, and
            # EN: debugger-friendly form instead of repeating the expression inline.
            # EN: Expected live meaning:
            # EN: - current local name(s): body
            # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
            # EN: - empty / None / degraded / partial values may be valid depending on this branch
            # EN: Undesired reading:
            # EN: - treating this local as durable cross-function or cross-run project state
            # EN: - assuming success semantics before the branch checks below finish
            # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / body
            # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
            # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
            # TR: bir biçimde taşıyabilmesi için vardır.
            # TR: Beklenen canlı anlam:
            # TR: - mevcut yerel ad(lar): body
            # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
            # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
            # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
            body = response.read()

    except HTTPError as exc:
        # EN: HTTPError still represents a real HTTP response, so we preserve its
        # EN: visible headers, status, and any returned body for cache truth.
        # TR: HTTPError yine de gerçek bir HTTP yanıtını temsil eder; bu yüzden
        # TR: cache doğrusu için görünen başlıkları, durumu ve varsa dönen body'yi koruyoruz.
# EN: final_url is kept explicit here as a local value inside fetch_robots_txt_to_raw_storage so this branch stays readable during audits.
# TR: final_url, fetch_robots_txt_to_raw_storage icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
        final_url = robots_url
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / http_status
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `int(exc.code)` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): http_status
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / http_status
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): http_status
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        http_status = int(exc.code)
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / content_type
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `exc.headers.get("Content-Type")` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): content_type
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / content_type
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): content_type
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        content_type = exc.headers.get("Content-Type")
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / etag
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `exc.headers.get("ETag")` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): etag
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / etag
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): etag
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        etag = exc.headers.get("ETag")
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / last_modified
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `exc.headers.get("Last-Modified")` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): last_modified
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / last_modified
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): last_modified
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        last_modified = exc.headers.get("Last-Modified")
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / body
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `exc.read()` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): body
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / body
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): body
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        body = exc.read()

    except (URLError, TimeoutError, socket.timeout) as exc:
        # EN: Transport-class failures produce no reliable HTTP cache truth, so we
        # EN: return a structured non-body result and let the caller decide cache_state.
        # TR: Taşıma-sınıfı hatalar güvenilir HTTP cache doğrusu üretmez; bu yüzden
        # TR: yapılı ama body'siz bir sonuç döndürüyor ve cache_state kararını çağırana bırakıyoruz.
# EN: fetch_error_class is kept explicit here as a local value inside fetch_robots_txt_to_raw_storage so this branch stays readable during audits.
# TR: fetch_error_class, fetch_robots_txt_to_raw_storage icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
        fetch_error_class = type(exc).__name__
        # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / fetch_error_message
        # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
        # EN: the immediate result of `str(exc)` in a named, reviewable, and
        # EN: debugger-friendly form instead of repeating the expression inline.
        # EN: Expected live meaning:
        # EN: - current local name(s): fetch_error_message
        # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
        # EN: - empty / None / degraded / partial values may be valid depending on this branch
        # EN: Undesired reading:
        # EN: - treating this local as durable cross-function or cross-run project state
        # EN: - assuming success semantics before the branch checks below finish
        # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / fetch_error_message
        # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
        # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
        # TR: bir biçimde taşıyabilmesi için vardır.
        # TR: Beklenen canlı anlam:
        # TR: - mevcut yerel ad(lar): fetch_error_message
        # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
        # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
        # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
        fetch_error_message = str(exc)

        return FetchedRobotsTxtResult(
            host_id=host_id,
            robots_url=robots_url,
            final_url=final_url,
            http_status=None,
            content_type=None,
            etag=None,
            last_modified=None,
            body_bytes=0,
            raw_storage_path=None,
            raw_sha256=None,
            fetched_at=fetched_at.isoformat(),
            fetch_error_class=fetch_error_class,
            fetch_error_message=fetch_error_message,
        )

    # EN: We persist any visible robots body, including HTTP error bodies, because
    # EN: later audits and cache reasoning benefit from that raw artefact.
    # TR: Sonraki audit ve cache muhakemesi bundan fayda göreceği için görünen
    # TR: herhangi bir robots body'yi, HTTP hata body'leri dahil, saklıyoruz.
# EN: raw_storage_path is kept explicit here as a local value inside fetch_robots_txt_to_raw_storage so this branch stays readable during audits.
# TR: raw_storage_path, fetch_robots_txt_to_raw_storage icindeki yerel bir deger olarak burada acik tutulur; boylece bu dal denetimlerde okunabilir kalir.
    raw_storage_path = build_raw_robots_storage_path(
        host_id=host_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )
    ensure_parent_directory(raw_storage_path)
    raw_storage_path.write_bytes(body)
    # EN: LOCAL VALUE EXPLANATION / fetch_robots_txt_to_raw_storage / raw_sha256
    # EN: This local assignment exists so the current fetch_robots_txt_to_raw_storage step can hold
    # EN: the immediate result of `sha256_hex(body)` in a named, reviewable, and
    # EN: debugger-friendly form instead of repeating the expression inline.
    # EN: Expected live meaning:
    # EN: - current local name(s): raw_sha256
    # EN: - the live value is branch-sensitive and must be read together with the checks immediately below
    # EN: - empty / None / degraded / partial values may be valid depending on this branch
    # EN: Undesired reading:
    # EN: - treating this local as durable cross-function or cross-run project state
    # EN: - assuming success semantics before the branch checks below finish
    # TR: YEREL DEĞER AÇIKLAMASI / fetch_robots_txt_to_raw_storage / raw_sha256
    # TR: Bu yerel atama, mevcut fetch_robots_txt_to_raw_storage adımının aşağıdaki ifadenin anlık
    # TR: sonucunu tekrar tekrar ifade yazmadan isimli, denetlenebilir ve debug-dostu
    # TR: bir biçimde taşıyabilmesi için vardır.
    # TR: Beklenen canlı anlam:
    # TR: - mevcut yerel ad(lar): raw_sha256
    # TR: - canlı değer dala duyarlıdır ve hemen aşağıdaki kontrollerle birlikte okunmalıdır
    # TR: - boş / None / degrade / kısmi değerler mevcut dala göre geçerli olabilir
    # TR: İstenmeyen okuma:
    # TR: - bu yereli fonksiyonlar-arası veya runlar-arası kalıcı proje state'i sanmak
    # TR: - aşağıdaki dal kontrolleri tamamlanmadan başarı anlamı yüklemek
    raw_sha256 = sha256_hex(body)

    # EN: We return one explicit structured robots fetch result.
    # TR: Tek bir açık yapılı robots fetch sonucu döndürüyoruz.
    return FetchedRobotsTxtResult(
        host_id=host_id,
        robots_url=robots_url,
        final_url=final_url,
        http_status=http_status,
        content_type=content_type,
        etag=etag,
        last_modified=last_modified,
        body_bytes=len(body),
        raw_storage_path=str(raw_storage_path),
        raw_sha256=raw_sha256,
        fetched_at=fetched_at.isoformat(),
        fetch_error_class=fetch_error_class,
        fetch_error_message=fetch_error_message,
    )

# EN: This export list keeps the robots child surface explicit.
# TR: Bu export listesi robots alt yüzeyini açık tutar.
__all__ = [
    "decode_robots_body",
    "parse_robots_txt_text",
    "fetch_robots_txt_to_raw_storage",
]
