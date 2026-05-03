"""
EN:
This file is the small worker-runtime support child directly beneath the main worker runtime hub.

EN:
Why this file exists:
- because tiny worker-side support contracts should live in one readable child instead of being mixed into the main worker hub
- because upper worker orchestration should stay focused while small shaping helpers stay isolated and named
- because a beginner should be able to see which helper logic is support-only and which logic is full worker orchestration

EN:
What this file DOES:
- expose small worker-runtime support helpers
- hold readable helper boundaries for payload shaping, phase labeling, or other support-only runtime semantics
- keep support logic separate from heavier worker orchestration logic

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not own all acquisition logic
- it does not own all parse logic
- it does not own all SQL details

EN:
Topological role:
- the main worker runtime hub sits above this file
- narrower lease/robots/acquisition/parse/finalize layers sit beside or below the main hub
- this file exists to keep small support semantics named and readable

EN:
Important visible values and shapes:
- support payloads => small structured values used by the worker corridor
- phase labels => readable text markers for where the worker currently is
- claimed_url or related phase data => handoff-friendly support meaning
- degraded or branch-helper outputs => explicit support-side visibility that should not be hidden

EN:
Accepted architectural identity:
- worker support child
- small helper contract layer
- readability-preserving support boundary

EN:
Undesired architectural identity:
- second hidden worker hub
- random utility dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya ana worker runtime hubının hemen altındaki küçük worker-runtime support child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü küçük worker-side support sözleşmeleri ana worker hubının içine karışmak yerine tek okunabilir child yüzeyde yaşamalıdır
- çünkü üst worker orkestrasyonu odaklı kalırken küçük şekillendirme yardımcıları izole ve isimli kalmalıdır
- çünkü yeni başlayan biri hangi yardımcının support-only, hangisinin tam worker orkestrasyonu olduğunu görebilmelidir

TR:
Bu dosya NE yapar:
- küçük worker-runtime support yardımcılarını açığa çıkarır
- payload shaping, phase labeling veya benzeri support-only runtime semantiklerini okunabilir yardımcı sınırları halinde tutar
- support mantığını daha ağır worker orkestrasyon mantığından ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tüm acquisition mantığının sahibi değildir
- tüm parse mantığının sahibi değildir
- tüm SQL ayrıntılarının sahibi değildir

TR:
Topolojik rol:
- ana worker runtime hubı bu dosyanın üstündedir
- daha dar lease/robots/acquisition/parse/finalize katmanları ana hubın yanında veya altındadır
- bu dosya küçük support semantiklerini isimli ve okunabilir tutmak için vardır

TR:
Önemli görünür değerler ve şekiller:
- support payloadları => worker koridorunda kullanılan küçük yapılı değerler
- phase labeları => workerın şu anda nerede olduğunu anlatan okunabilir metin işaretleri
- claimed_url veya ilgili faz verisi => devre uygun support anlamı
- degraded veya branch-helper çıktıları => gizlenmemesi gereken support tarafı görünürlüğü

TR:
Kabul edilen mimari kimlik:
- worker support child
- küçük yardımcı sözleşme katmanı
- okunabilirliği koruyan support sınırı

TR:
İstenmeyen mimari kimlik:
- ikinci gizli worker hubı
- rastgele utility çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module is the small worker-runtime support child created by the
# EN: controlled split. It keeps tiny generic helpers out of the parent
# EN: orchestrator so the parent can focus on branch flow only.
# TR: Bu modül kontrollü split ile oluşturulan küçük worker-runtime destek
# TR: alt yüzeyidir. Küçük genel yardımcıları parent orchestrator dışına taşır;
# TR: böylece parent yalnızca branch akışına odaklanabilir.

# EN: WORKER RUNTIME SUPPORT IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the small side table of the worker corridor, not the whole corridor itself.
# EN: Beginner mental model:
# EN: - the main worker runtime file is the main room
# EN: - this file keeps smaller support semantics from cluttering that main room
# EN: - readable support helpers make the whole system easier to map from scratch
# EN:
# EN: Accepted architectural meaning:
# EN: - named support boundary under the worker runtime family
# EN: - small payload/phase helper surface
# EN:
# EN: Undesired architectural meaning:
# EN: - random helper trash pile
# EN: - secret second orchestrator
# EN: - place where branch meaning becomes vague
# EN:
# EN: Important value-shape reminders:
# EN: - support outputs should remain explicit and named
# EN: - phase markers should stay readable
# EN: - no-work/degraded helper meaning should remain visible when produced here
# TR: WORKER RUNTIME SUPPORT KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun tamamı değil, küçük yan masası gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - ana worker runtime dosyası ana odadır
# TR: - bu dosya küçük support semantiklerini o ana odayı kalabalıklaştırmadan tutar
# TR: - okunabilir support yardımcıları tüm sistemi sıfırdan haritalamayı kolaylaştırır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - worker runtime ailesi altındaki isimli support sınırı
# TR: - küçük payload/faz yardımcısı yüzeyi
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele yardımcı çöplüğü
# TR: - gizli ikinci orchestrator
# TR: - dal anlamının belirsizleştiği yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - support çıktıları açık ve isimli kalmalıdır
# TR: - faz işaretleri okunabilir kalmalıdır
# TR: - burada üretilen no-work/degraded helper anlamı görünür kalmalıdır

from __future__ import annotations

# EN: We import datetime and timezone so the support child can produce explicit
# EN: UTC timestamps without depending on parent-level helpers.
# TR: Destek alt yüzeyi parent-seviyesi yardımcılara bağlı kalmadan açık UTC
# TR: zaman damgaları üretebilsin diye datetime ve timezone içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import uuid4 so each worker execution can still receive a unique run id.
# TR: Her worker çalıştırması benzersiz bir run id alabilsin diye uuid4 içe
# TR: aktarıyoruz.
from uuid import uuid4

# EN: We import the canonical claimed-url field reader directly from the
# EN: acquisition-support child instead of the acquisition hub. This avoids a
# EN: circular import while still unifying field access in one canonical place.
# TR: Kanonik claimed-url alan okuyucusunu acquisition hub yerine doğrudan
# TR: acquisition-support alt yüzeyinden içe aktarıyoruz. Bu yaklaşım circular
# TR: import riskini önlerken alan erişimini yine tek kanonik yerde birleştirir.
from .logisticsearch1_1_2_4_1_acquisition_support import get_claimed_url_value


# EN: This helper creates a unique runtime execution id.
# TR: Bu yardımcı benzersiz bir runtime çalıştırma kimliği üretir.
# EN: WORKER SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / new_run_id
# EN:
# EN: Why this function exists:
# EN: - because worker-support truth for 'new_run_id' should be exposed through one named top-level helper boundary
# EN: - because small support semantics should remain readable instead of being buried inside bigger orchestrator code
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the support contract below
# EN:
# EN: Accepted output:
# EN: - a worker-support-oriented result shape defined by the current function body
# EN: - this may be a small structured payload, a readable phase marker, or another explicit support branch result
# EN:
# EN: Common support meaning hints:
# EN: - this helper exposes one named worker-support contract boundary
# EN:
# EN: Important beginner reminder:
# EN: - this function is support logic, not the whole worker corridor
# EN: - support outputs should stay explicit so the bigger corridor remains easy to inspect
# EN:
# EN: Undesired behavior:
# EN: - silent helper behavior with no readable boundary
# EN: - vague support outputs that hide branch meaning
# TR: WORKER SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / new_run_id
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'new_run_id' için worker-support doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü küçük support semantiği büyük orchestrator kodu içine gömülmek yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-support odaklı sonuç şekli
# TR: - bu; küçük yapılı payload, okunabilir faz işareti veya başka açık support dal sonucu olabilir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı isimli bir worker-support sözleşme sınırını açığa çıkarır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon support mantığıdır, worker koridorunun tamamı değildir
# TR: - support çıktıları açık kalmalıdır ki büyük koridor kolay denetlenebilir olsun
# TR:
# TR: İstenmeyen davranış:
# TR: - okunabilir sınır olmadan sessiz helper davranışı
# TR: - dal anlamını gizleyen belirsiz support çıktıları

# EN: WORKER RUNTIME SUPPORT DENSITY LIFT MEMORY BLOCK V7
# EN:
# EN: Why one more block is useful here:
# EN: - because this file is intentionally small, so each support helper must carry unusually explicit explanation density
# EN: - because a beginner reading only this file should still understand why support helpers are separated from the main worker hub
# EN: - because support boundaries are easy to underestimate when the code itself looks compact
# EN:
# EN: For-dummies framing:
# EN: - the main worker file is the manager room
# EN: - this support file is the labeled drawer for smaller but still important helper pieces
# EN: - if these small pieces are unnamed or underexplained, the whole crawler map becomes harder to rebuild from scratch
# EN:
# EN: Accepted reading model:
# EN: - read this file as support-only helper ground
# EN: - expect smaller payload shaping or phase naming helpers here
# EN: - expect outputs to stay explicit and beginner-readable
# EN:
# EN: Undesired reading model:
# EN: - assuming this file is unimportant because it is smaller
# EN: - assuming support code needs fewer contracts than heavier runtime files
# EN:
# TR: WORKER RUNTIME SUPPORT YOĞUNLUK TAKVİYE HAFIZA BLOĞU V7
# TR:
# TR: Burada bir ek blok neden faydalıdır:
# TR: - çünkü bu dosya bilinçli olarak küçük tutulur, bu yüzden her support yardımcısı alışılmadık derecede açık açıklama yoğunluğu taşımalıdır
# TR: - çünkü yalnızca bu dosyayı okuyan yeni başlayan biri bile support yardımcılarının neden ana worker hubından ayrıldığını anlamalıdır
# TR: - çünkü support sınırları kod görünüşte kompakt olduğunda kolayca küçümsenir
# TR:
# TR: For-dummies çerçevesi:
# TR: - ana worker dosyası yönetici odasıdır
# TR: - bu support dosyası küçük ama önemli yardımcı parçaların etiketli çekmecesidir
# TR: - bu küçük parçalar isimsiz veya yetersiz açıklanmış olursa tüm crawler haritasını sıfırdan kurmak zorlaşır
# TR:
# TR: Kabul edilen okuma modeli:
# TR: - bu dosyayı support-only yardımcı zemini gibi oku
# TR: - burada daha küçük payload shaping veya phase naming yardımcıları bekle
# TR: - çıktıların açık ve başlangıç seviyesine uygun kalmasını bekle
# TR:
# TR: İstenmeyen okuma modeli:
# TR: - bu dosyanın küçük olduğu için önemsiz olduğunu sanmak
# TR: - support kodunun ağır runtime dosyalarından daha az sözleşme gerektirdiğini sanmak

# EN: WORKER SUPPORT FUNCTION REINFORCEMENT BLOCK V7 / new_run_id
# EN:
# EN: Extra clarity layer:
# EN: - small support helpers are exactly the places where hidden assumptions tend to accumulate
# EN: - therefore this function gets an extra contract reminder layer
# EN:
# EN: Input reminder:
# EN: - current explicit parameters: (no explicit parameters)
# EN: - callers should pass values that keep branch meaning explicit
# EN:
# EN: Output reminder:
# EN: - the result should stay small but still contract-visible
# EN: - helper results should not erase degraded or branch-specific meaning
# EN:
# EN: Common support meaning hints:
# EN: - this helper exposes one named worker-support contract boundary
# EN: - even small support helpers should remain contract-visible
# EN:
# EN: Beginner warning:
# EN: - when a helper looks tiny, it becomes tempting to stop documenting it
# EN: - that temptation is exactly what this block resists
# TR: WORKER SUPPORT FUNCTION PEKİŞTİRME BLOĞU V7 / new_run_id
# TR:
# TR: Ek açıklık katmanı:
# TR: - küçük support yardımcıları gizli varsayımların birikmeye en açık yerlerdir
# TR: - bu yüzden bu fonksiyon ek sözleşme hatırlatma katmanı alır
# TR:
# TR: Girdi hatırlatması:
# TR: - mevcut açık parametreler: (açık parametre yok)
# TR: - çağıranlar dal anlamını açık tutan değerler geçmelidir
# TR:
# TR: Çıktı hatırlatması:
# TR: - sonuç küçük kalsa bile sözleşme açısından görünür kalmalıdır
# TR: - yardımcı sonuçları degraded veya dala özgü anlamı silmemelidir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı isimli bir worker-support sözleşme sınırını açığa çıkarır
# TR: - küçük support yardımcıları bile sözleşme açısından görünür kalmalıdır
# TR:
# TR: Başlangıç seviyesi uyarı:
# TR: - bir yardımcı küçük göründüğünde onu belgeleme isteği azalır
# TR: - bu blok tam olarak o hatalı eğilime karşı konur

# EN: This worker-support helper creates a fresh run identifier for one worker-side execution span.
# EN: Why this function exists:
# EN: - because run_id should be produced in one tiny named support helper instead of being improvised in many branches
# EN: - because a readable run identifier helps correlate worker events, degraded paths, and downstream receipts
# TR: Bu worker-support yardımcısı tek bir worker-side yürütme aralığı için yeni bir run kimliği üretir.
# TR: Bu fonksiyon neden var:
# TR: - çünkü run_id değeri birçok dalda gelişigüzel üretilmek yerine tek küçük isimli support yardımcısında üretilmelidir
# TR: - çünkü okunabilir bir run kimliği worker olaylarını, degraded yolları ve aşağı akış makbuzlarını ilişkilendirmeyi kolaylaştırır
def new_run_id() -> str:
    # EN: We convert uuid4() to text because text ids are easy to print, audit,
    # EN: serialize, and carry through structured result payloads.
    # TR: uuid4() sonucunu metne çeviriyoruz; çünkü metinsel kimlikler yapılı
    # TR: sonuç payload’larında yazdırmak, denetlemek, serileştirmek ve taşımak
    # TR: için kolaydır.
    return str(uuid4())


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı ISO-8601 biçiminde UTC zaman damgası metni döndürür.
# EN: WORKER SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / utc_now_iso
# EN:
# EN: Why this function exists:
# EN: - because worker-support truth for 'utc_now_iso' should be exposed through one named top-level helper boundary
# EN: - because small support semantics should remain readable instead of being buried inside bigger orchestrator code
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the support contract below
# EN:
# EN: Accepted output:
# EN: - a worker-support-oriented result shape defined by the current function body
# EN: - this may be a small structured payload, a readable phase marker, or another explicit support branch result
# EN:
# EN: Common support meaning hints:
# EN: - this helper exposes one named worker-support contract boundary
# EN:
# EN: Important beginner reminder:
# EN: - this function is support logic, not the whole worker corridor
# EN: - support outputs should stay explicit so the bigger corridor remains easy to inspect
# EN:
# EN: Undesired behavior:
# EN: - silent helper behavior with no readable boundary
# EN: - vague support outputs that hide branch meaning
# TR: WORKER SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / utc_now_iso
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'utc_now_iso' için worker-support doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü küçük support semantiği büyük orchestrator kodu içine gömülmek yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-support odaklı sonuç şekli
# TR: - bu; küçük yapılı payload, okunabilir faz işareti veya başka açık support dal sonucu olabilir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı isimli bir worker-support sözleşme sınırını açığa çıkarır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon support mantığıdır, worker koridorunun tamamı değildir
# TR: - support çıktıları açık kalmalıdır ki büyük koridor kolay denetlenebilir olsun
# TR:
# TR: İstenmeyen davranış:
# TR: - okunabilir sınır olmadan sessiz helper davranışı
# TR: - dal anlamını gizleyen belirsiz support çıktıları

# EN: WORKER SUPPORT FUNCTION REINFORCEMENT BLOCK V7 / utc_now_iso
# EN:
# EN: Extra clarity layer:
# EN: - small support helpers are exactly the places where hidden assumptions tend to accumulate
# EN: - therefore this function gets an extra contract reminder layer
# EN:
# EN: Input reminder:
# EN: - current explicit parameters: (no explicit parameters)
# EN: - callers should pass values that keep branch meaning explicit
# EN:
# EN: Output reminder:
# EN: - the result should stay small but still contract-visible
# EN: - helper results should not erase degraded or branch-specific meaning
# EN:
# EN: Common support meaning hints:
# EN: - this helper exposes one named worker-support contract boundary
# EN: - even small support helpers should remain contract-visible
# EN:
# EN: Beginner warning:
# EN: - when a helper looks tiny, it becomes tempting to stop documenting it
# EN: - that temptation is exactly what this block resists
# TR: WORKER SUPPORT FUNCTION PEKİŞTİRME BLOĞU V7 / utc_now_iso
# TR:
# TR: Ek açıklık katmanı:
# TR: - küçük support yardımcıları gizli varsayımların birikmeye en açık yerlerdir
# TR: - bu yüzden bu fonksiyon ek sözleşme hatırlatma katmanı alır
# TR:
# TR: Girdi hatırlatması:
# TR: - mevcut açık parametreler: (açık parametre yok)
# TR: - çağıranlar dal anlamını açık tutan değerler geçmelidir
# TR:
# TR: Çıktı hatırlatması:
# TR: - sonuç küçük kalsa bile sözleşme açısından görünür kalmalıdır
# TR: - yardımcı sonuçları degraded veya dala özgü anlamı silmemelidir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı isimli bir worker-support sözleşme sınırını açığa çıkarır
# TR: - küçük support yardımcıları bile sözleşme açısından görünür kalmalıdır
# TR:
# TR: Başlangıç seviyesi uyarı:
# TR: - bir yardımcı küçük göründüğünde onu belgeleme isteği azalır
# TR: - bu blok tam olarak o hatalı eğilime karşı konur

# EN: This worker-support helper returns the current UTC timestamp in ISO text form.
# EN: Why this function exists:
# EN: - because worker-side timestamps should be shaped consistently in one helper
# EN: - because later receipts and diagnostics should not drift between multiple ad-hoc timestamp formats
# TR: Bu worker-support yardımcısı mevcut UTC zaman damgasını ISO metin biçiminde döndürür.
# TR: Bu fonksiyon neden var:
# TR: - çünkü worker tarafı zaman damgaları tek bir yardımcıda tutarlı biçimde şekillendirilmelidir
# TR: - çünkü sonraki makbuzlar ve tanı çıktıları birden çok gelişigüzel zaman biçimi arasında drift yaşamamalıdır
def utc_now_iso() -> str:
    # EN: We explicitly use timezone.utc so no machine-local timezone ambiguity
    # EN: can leak into worker-runtime evidence.
    # TR: Worker-runtime kanıtına makineye özgü saat dilimi belirsizliği sızmasın
    # TR: diye açıkça timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc).isoformat()


# EN: This helper builds a small explicit terminal fetch-attempt metadata payload.
# EN: The goal is to keep durable per-attempt evidence easy to interpret later.
# TR: Bu yardımcı küçük ve açık bir terminal fetch-attempt metadata payload’ı
# TR: kurar. Amaç kalıcı deneme-bazlı kanıtın daha sonra kolay yorumlanmasıdır.
# EN: WORKER SUPPORT FUNCTION PURPOSE MEMORY BLOCK V6 / build_terminal_fetch_attempt_metadata
# EN:
# EN: Why this function exists:
# EN: - because worker-support truth for 'build_terminal_fetch_attempt_metadata' should be exposed through one named top-level helper boundary
# EN: - because small support semantics should remain readable instead of being buried inside bigger orchestrator code
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: claimed_url, acquisition_method, note
# EN: - values should match the current Python signature and the support contract below
# EN:
# EN: Accepted output:
# EN: - a worker-support-oriented result shape defined by the current function body
# EN: - this may be a small structured payload, a readable phase marker, or another explicit support branch result
# EN:
# EN: Common support meaning hints:
# EN: - this helper likely shapes a small worker payload or claim-related support structure
# EN: - explicit field names and branch visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this function is support logic, not the whole worker corridor
# EN: - support outputs should stay explicit so the bigger corridor remains easy to inspect
# EN:
# EN: Undesired behavior:
# EN: - silent helper behavior with no readable boundary
# EN: - vague support outputs that hide branch meaning
# TR: WORKER SUPPORT FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_terminal_fetch_attempt_metadata
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_terminal_fetch_attempt_metadata' için worker-support doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü küçük support semantiği büyük orchestrator kodu içine gömülmek yerine okunabilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: claimed_url, acquisition_method, note
# TR: - değerler aşağıdaki mevcut Python imzası ve support sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-support odaklı sonuç şekli
# TR: - bu; küçük yapılı payload, okunabilir faz işareti veya başka açık support dal sonucu olabilir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle küçük worker payloadı veya claim ile ilgili support yapısı şekillendirir
# TR: - açık alan isimleri ve dal görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon support mantığıdır, worker koridorunun tamamı değildir
# TR: - support çıktıları açık kalmalıdır ki büyük koridor kolay denetlenebilir olsun
# TR:
# TR: İstenmeyen davranış:
# TR: - okunabilir sınır olmadan sessiz helper davranışı
# TR: - dal anlamını gizleyen belirsiz support çıktıları

# EN: WORKER SUPPORT FUNCTION REINFORCEMENT BLOCK V7 / build_terminal_fetch_attempt_metadata
# EN:
# EN: Extra clarity layer:
# EN: - small support helpers are exactly the places where hidden assumptions tend to accumulate
# EN: - therefore this function gets an extra contract reminder layer
# EN:
# EN: Input reminder:
# EN: - current explicit parameters: claimed_url, acquisition_method, note
# EN: - callers should pass values that keep branch meaning explicit
# EN:
# EN: Output reminder:
# EN: - the result should stay small but still contract-visible
# EN: - helper results should not erase degraded or branch-specific meaning
# EN:
# EN: Common support meaning hints:
# EN: - this helper likely shapes a small worker payload or claim-related support structure
# EN: - explicit field names and branch visibility may matter here
# EN: - this kind of helper often exists to stop anonymous dict drift
# EN:
# EN: Beginner warning:
# EN: - when a helper looks tiny, it becomes tempting to stop documenting it
# EN: - that temptation is exactly what this block resists
# TR: WORKER SUPPORT FUNCTION PEKİŞTİRME BLOĞU V7 / build_terminal_fetch_attempt_metadata
# TR:
# TR: Ek açıklık katmanı:
# TR: - küçük support yardımcıları gizli varsayımların birikmeye en açık yerlerdir
# TR: - bu yüzden bu fonksiyon ek sözleşme hatırlatma katmanı alır
# TR:
# TR: Girdi hatırlatması:
# TR: - mevcut açık parametreler: claimed_url, acquisition_method, note
# TR: - çağıranlar dal anlamını açık tutan değerler geçmelidir
# TR:
# TR: Çıktı hatırlatması:
# TR: - sonuç küçük kalsa bile sözleşme açısından görünür kalmalıdır
# TR: - yardımcı sonuçları degraded veya dala özgü anlamı silmemelidir
# TR:
# TR: Ortak support anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle küçük worker payloadı veya claim ile ilgili support yapısı şekillendirir
# TR: - açık alan isimleri ve dal görünürlüğü burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman isimsiz dict driftini durdurmak için vardır
# TR:
# TR: Başlangıç seviyesi uyarı:
# TR: - bir yardımcı küçük göründüğünde onu belgeleme isteği azalır
# TR: - bu blok tam olarak o hatalı eğilime karşı konur

# EN: This worker-support helper builds the terminal fetch-attempt metadata payload used at the end of one worker-side branch.
# EN: Parameter meanings:
# EN: - claimed_url => the claimed work item whose visible fields are copied into the terminal metadata payload
# EN: - acquisition_method => the explicit acquisition corridor label such as http_page or browser_page that ended this attempt
# EN: - note => an extra operator-readable explanation attached to the terminal metadata payload when needed
# TR: Bu worker-support yardımcısı bir worker-side dalının sonunda kullanılan terminal fetch-attempt metadata payload'ını kurar.
# TR: Parametre anlamları:
# TR: - claimed_url => görünür alanları terminal metadata payload'ına kopyalanan claim edilmiş iş öğesi
# TR: - acquisition_method => bu denemeyi bitiren http_page veya browser_page gibi açık acquisition corridor etiketi
# TR: - note => gerektiğinde terminal metadata payload'ına eklenen ek operatör-okunur açıklama
def build_terminal_fetch_attempt_metadata(
    *,
    claimed_url: object,
    acquisition_method: str | None,
    note: str,
) -> dict[str, object]:
    # EN: We keep the metadata shape narrow and explicit so later audits can see
    # EN: exactly which runtime path created the durable row.
    # TR: Daha sonraki audit’ler kalıcı satırı hangi runtime yolunun ürettiğini
    # TR: açıkça görebilsin diye metadata şeklini dar ve açık tutuyoruz.
    return {
        "runtime_surface": "worker_runtime",
        "note": note,
        "acquisition_method": acquisition_method,
        "canonical_url": str(get_claimed_url_value(claimed_url, "canonical_url")),
        "authority_key": str(get_claimed_url_value(claimed_url, "authority_key")),
        "scheme": str(get_claimed_url_value(claimed_url, "scheme")),
        "host": str(get_claimed_url_value(claimed_url, "host")),
    }


# EN: This explicit export list keeps the public surface of the support child
# EN: stable and readable.
# TR: Bu açık export listesi destek alt yüzeyinin public yüzeyini stabil ve
# TR: okunabilir tutar.
__all__ = [
    "new_run_id",
    "utc_now_iso",
    "build_terminal_fetch_attempt_metadata",
]
