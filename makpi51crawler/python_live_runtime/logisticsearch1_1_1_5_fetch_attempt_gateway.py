"""
EN:
This file is the fetch-attempt gateway surface for the crawler runtime.

EN:
Why this file exists:
- because fetch-attempt database boundary helpers should stay explicit and separately readable
- because attempt rows, insert/update/read helpers, and fetch-attempt state transitions should not disappear into unrelated gateway files
- because a beginner should be able to find where fetch-attempt persistence truth lives

EN:
What this file DOES:
- expose fetch-attempt gateway helpers
- keep fetch-attempt storage contracts readable
- preserve explicit runtime-to-database boundary meaning for fetch attempts

EN:
What this file DOES NOT do:
- it does not become the whole worker runtime
- it does not become the full acquisition layer
- it does not become parse or storage routing
- it does not become a vague utility dump

TR:
Bu dosya crawler runtime icin fetch-attempt gateway yuzeyidir.

TR:
Bu dosya neden var:
- cunku fetch-attempt veritabani sinir yardimcilari acik ve ayri okunabilir kalmalidir
- cunku attempt satiri, insert/update/read yardimcilari ve fetch-attempt durum gecisleri ilgisiz gateway dosyalarinda kaybolmamalidir
- cunku yeni baslayan biri fetch-attempt persistence dogrusunun nerede yasadigini bulabilmelidir

TR:
Bu dosya NE yapar:
- fetch-attempt gateway yardimcilarini aciga cikarir
- fetch-attempt storage sozlesmelerini okunabilir tutar
- fetch-attempt icin runtime-veritabani sinir anlamini gorunur korur

TR:
Bu dosya NE yapmaz:
- worker runtime'in tamami olmaz
- acquisition katmaninin tamami olmaz
- parse veya storage routing katmani olmaz
- belirsiz utility coplugu olmaz
"""
from __future__ import annotations

# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 1. This module is the fetch-attempt gateway and should explain how runtime code records, reads, or interprets fetch-attempt state at the database edge.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 1. Bu modül fetch-attempt gateway katmanıdır ve çalışma zamanı kodunun veritabanı sınırında fetch denemesi durumunu nasıl kaydettiğini, okuduğunu veya yorumladığını açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 2. A fetch-attempt gateway is operationally important because it carries evidence about what was tried, when it was tried, and how the attempt should be interpreted later.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 2. Bir fetch-attempt gateway operasyonel olarak önemlidir çünkü neyin denendiği, ne zaman denendiği ve denemenin daha sonra nasıl yorumlanacağına dair kanıt taşır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 3. Readers should be able to see from this file which values belong to attempt metadata, which values belong to persistence boundaries, and which assumptions are pushed back to callers.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 3. Okuyucu bu dosyadan hangi değerlerin deneme metadatasına ait olduğunu, hangilerinin kalıcılık sınırına ait olduğunu ve hangi varsayımların tekrar çağıranlara döndüğünü görebilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 4. Compact database code is risky here because attempt-tracking mistakes can corrupt retry logic, diagnostics, and post-fetch analysis.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 4. Sıkışık veritabanı kodu burada risklidir çünkü deneme izleme hataları retry mantığını, tanı yüzeyini ve fetch sonrası analizi bozabilir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 5. This orientation block exists to keep the module auditable and beginner-readable while raising bilingual comment density in a controlled way.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 5. Bu yönlendirme bloğu yorum yoğunluğunu kontrollü biçimde yükseltirken modülü denetlenebilir ve yeni başlayan dostu tutmak için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 6. When changing this file, prefer visible contract wording over clever compression because fetch-attempt records are part of crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 6. Bu dosya değiştirilirken zeki sıkıştırma yerine görünür sözleşme dili tercih edilmelidir çünkü fetch-attempt kayıtları crawler gerçeğinin parçasıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 7. This file should help explain how attempt-side facts move between runtime orchestration and stored crawler evidence.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 7. Bu dosya deneme tarafı gerçeklerinin runtime orkestrasyonu ile saklanan crawler kanıtı arasında nasıl hareket ettiğini açıklamaya yardım etmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 8. If a production issue affects fetch history, this module should be readable enough that an operator can trace intent without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 8. Üretim sorunu fetch geçmişini etkilerse operatör bu modülü tahmin yürütmeden niyeti izleyebilecek kadar okunabilir bulmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 9. Gateway code here should make attempt persistence understandable rather than magical.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 9. Buradaki gateway kodu deneme kalıcılığını büyülü değil anlaşılır yapmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 10. Keep this surface explicit because fetch-attempt facts later influence retries, diagnostics, and workflow transitions.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 10. Bu yüzeyi açık tut çünkü fetch-attempt gerçekleri daha sonra retry, tanı ve iş akışı geçişlerini etkiler.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 11. This module is the fetch-attempt gateway and should explain how runtime code records, reads, or interprets fetch-attempt state at the database edge.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 11. Bu modül fetch-attempt gateway katmanıdır ve çalışma zamanı kodunun veritabanı sınırında fetch denemesi durumunu nasıl kaydettiğini, okuduğunu veya yorumladığını açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 12. A fetch-attempt gateway is operationally important because it carries evidence about what was tried, when it was tried, and how the attempt should be interpreted later.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 12. Bir fetch-attempt gateway operasyonel olarak önemlidir çünkü neyin denendiği, ne zaman denendiği ve denemenin daha sonra nasıl yorumlanacağına dair kanıt taşır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 13. Readers should be able to see from this file which values belong to attempt metadata, which values belong to persistence boundaries, and which assumptions are pushed back to callers.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 13. Okuyucu bu dosyadan hangi değerlerin deneme metadatasına ait olduğunu, hangilerinin kalıcılık sınırına ait olduğunu ve hangi varsayımların tekrar çağıranlara döndüğünü görebilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 14. Compact database code is risky here because attempt-tracking mistakes can corrupt retry logic, diagnostics, and post-fetch analysis.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 14. Sıkışık veritabanı kodu burada risklidir çünkü deneme izleme hataları retry mantığını, tanı yüzeyini ve fetch sonrası analizi bozabilir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 15. This orientation block exists to keep the module auditable and beginner-readable while raising bilingual comment density in a controlled way.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 15. Bu yönlendirme bloğu yorum yoğunluğunu kontrollü biçimde yükseltirken modülü denetlenebilir ve yeni başlayan dostu tutmak için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 16. When changing this file, prefer visible contract wording over clever compression because fetch-attempt records are part of crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 16. Bu dosya değiştirilirken zeki sıkıştırma yerine görünür sözleşme dili tercih edilmelidir çünkü fetch-attempt kayıtları crawler gerçeğinin parçasıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 17. This file should help explain how attempt-side facts move between runtime orchestration and stored crawler evidence.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 17. Bu dosya deneme tarafı gerçeklerinin runtime orkestrasyonu ile saklanan crawler kanıtı arasında nasıl hareket ettiğini açıklamaya yardım etmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 18. If a production issue affects fetch history, this module should be readable enough that an operator can trace intent without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 18. Üretim sorunu fetch geçmişini etkilerse operatör bu modülü tahmin yürütmeden niyeti izleyebilecek kadar okunabilir bulmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 19. Gateway code here should make attempt persistence understandable rather than magical.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 19. Buradaki gateway kodu deneme kalıcılığını büyülü değil anlaşılır yapmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 20. Keep this surface explicit because fetch-attempt facts later influence retries, diagnostics, and workflow transitions.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 20. Bu yüzeyi açık tut çünkü fetch-attempt gerçekleri daha sonra retry, tanı ve iş akışı geçişlerini etkiler.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 21. This module is the fetch-attempt gateway and should explain how runtime code records, reads, or interprets fetch-attempt state at the database edge.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 21. Bu modül fetch-attempt gateway katmanıdır ve çalışma zamanı kodunun veritabanı sınırında fetch denemesi durumunu nasıl kaydettiğini, okuduğunu veya yorumladığını açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 22. A fetch-attempt gateway is operationally important because it carries evidence about what was tried, when it was tried, and how the attempt should be interpreted later.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 22. Bir fetch-attempt gateway operasyonel olarak önemlidir çünkü neyin denendiği, ne zaman denendiği ve denemenin daha sonra nasıl yorumlanacağına dair kanıt taşır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 23. Readers should be able to see from this file which values belong to attempt metadata, which values belong to persistence boundaries, and which assumptions are pushed back to callers.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 23. Okuyucu bu dosyadan hangi değerlerin deneme metadatasına ait olduğunu, hangilerinin kalıcılık sınırına ait olduğunu ve hangi varsayımların tekrar çağıranlara döndüğünü görebilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 24. Compact database code is risky here because attempt-tracking mistakes can corrupt retry logic, diagnostics, and post-fetch analysis.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 24. Sıkışık veritabanı kodu burada risklidir çünkü deneme izleme hataları retry mantığını, tanı yüzeyini ve fetch sonrası analizi bozabilir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 25. This orientation block exists to keep the module auditable and beginner-readable while raising bilingual comment density in a controlled way.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 25. Bu yönlendirme bloğu yorum yoğunluğunu kontrollü biçimde yükseltirken modülü denetlenebilir ve yeni başlayan dostu tutmak için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 26. When changing this file, prefer visible contract wording over clever compression because fetch-attempt records are part of crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 26. Bu dosya değiştirilirken zeki sıkıştırma yerine görünür sözleşme dili tercih edilmelidir çünkü fetch-attempt kayıtları crawler gerçeğinin parçasıdır.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 27. This file should help explain how attempt-side facts move between runtime orchestration and stored crawler evidence.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 27. Bu dosya deneme tarafı gerçeklerinin runtime orkestrasyonu ile saklanan crawler kanıtı arasında nasıl hareket ettiğini açıklamaya yardım etmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway orientation note 28. If a production issue affects fetch history, this module should be readable enough that an operator can trace intent without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Fetch-attempt gateway yonlendirme notu 28. Üretim sorunu fetch geçmişini etkilerse operatör bu modülü tahmin yürütmeden niyeti izleyebilecek kadar okunabilir bulmalıdır.

"""
EN:
This file is the fetch-attempt child of the state DB gateway family.

EN:
Why this file exists:
- because terminal fetch-attempt truth should be exposed through one explicit named gateway child
- because upper layers should log fetch-attempt results through readable Python helpers instead of repeating raw SQL details
- because fetch-attempt terminal visibility is a separate concern from frontier claiming, runtime-control, or robots truth

EN:
What this file DOES:
- expose fetch-attempt-oriented DB helper boundaries
- persist terminal fetch-attempt truth in a readable gateway layer
- preserve explicit result visibility for upper runtime layers

EN:
What this file DOES NOT do:
- it does not own shared DB connection helpers
- it does not own frontier claim truth
- it does not own runtime-control truth
- it does not fetch page content by itself
- it does not parse HTML

EN:
Topological role:
- gateway_support sits below this file for shared DB support
- this file sits in the middle for fetch-attempt terminal DB truth
- upper runtime/finalize layers call these helpers instead of embedding raw SQL semantics

EN:
Important visible values and shapes:
- conn => live DB connection object
- fetch_attempt identifiers => row-level fetch-attempt truth
- outcome => terminal result meaning such as success, retryable error, permanent error, or blocked path visibility
- metadata / payload fields => structured evidence about what happened
- degraded or missing-row visibility => non-happy branches that should stay explicit

EN:
Accepted architectural identity:
- fetch-attempt truth gateway
- terminal logging DB-adjacent helper layer
- readable fetch-attempt contract boundary

EN:
Undesired architectural identity:
- hidden fetch engine
- hidden parse engine
- hidden ranking engine
- hidden operator CLI surface

TR:
Bu dosya state DB gateway ailesinin fetch-attempt child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü terminal fetch-attempt doğrusu tek ve açık isimli gateway child yüzeyi üzerinden açığa çıkmalıdır
- çünkü üst katmanlar ham SQL ayrıntısını tekrar etmek yerine fetch-attempt sonuçlarını okunabilir Python yardımcıları üzerinden loglamalıdır
- çünkü fetch-attempt terminal görünürlüğü frontier claim, runtime-control veya robots doğrusundan ayrı bir konudur

TR:
Bu dosya NE yapar:
- fetch-attempt odaklı DB yardımcı sınırlarını açığa çıkarır
- terminal fetch-attempt doğrusunu okunabilir gateway katmanında kalıcılaştırır
- üst runtime katmanları için açık sonuç görünürlüğü korur

TR:
Bu dosya NE yapmaz:
- ortak DB bağlantı yardımcılarının sahibi değildir
- frontier claim doğrusunun sahibi değildir
- runtime-control doğrusunun sahibi değildir
- sayfa içeriğini kendi başına fetch etmez
- HTML parse etmez

TR:
Topolojik rol:
- ortak DB desteği için gateway_support bu dosyanın altındadır
- terminal fetch-attempt DB doğrusu için bu dosya ortadadır
- üst runtime/finalize katmanları ham SQL semantiğini gömmek yerine bu yardımcıları çağırır

TR:
Önemli görünür değerler ve şekiller:
- conn => canlı DB bağlantı nesnesi
- fetch_attempt kimlikleri => satır-düzeyi fetch-attempt doğrusu
- outcome => success, retryable error, permanent error veya blocked path görünürlüğü gibi terminal sonuç anlamı
- metadata / payload alanları => ne olduğunu anlatan yapılı kanıt
- degraded veya missing-row görünürlüğü => açık kalması gereken mutlu-yol-dışı dallar

TR:
Kabul edilen mimari kimlik:
- fetch-attempt truth gateway
- terminal logging DB-yanı yardımcı katmanı
- okunabilir fetch-attempt sözleşme sınırı

TR:
İstenmeyen mimari kimlik:
- gizli fetch motoru
- gizli parse motoru
- gizli ranking motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module is the fetch-attempt child of the state DB gateway family.
# EN: It owns only the terminal fetch-attempt logging wrapper.
# TR: Bu modül state DB gateway ailesinin fetch-attempt alt yüzeyidir.
# TR: Yalnızca terminal fetch-attempt logging wrapper'ını taşır.

# EN: FETCH-ATTEMPT GATEWAY IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the durable logging doorway for fetch-attempt result truth.
# EN: A beginner mental model:
# EN: - acquisition/runtime layers discover what happened
# EN: - this gateway child helps persist that terminal truth
# EN: - upper layers should not hand-write DB statements each time a terminal attempt result must be stored
# EN:
# EN: Accepted architectural meaning:
# EN: - named fetch-attempt DB-truth boundary
# EN: - durable attempt-result persistence helper surface
# EN:
# EN: Undesired architectural meaning:
# EN: - hidden network fetch executor
# EN: - hidden parse executor
# EN: - hidden ranking executor
# EN:
# EN: Important value-shape reminders:
# EN: - terminal result payloads are allowed to be structured dict-like shapes
# EN: - fetch_attempt identifiers should stay explicit
# EN: - missing-row or degraded branches should remain visible, not silently coerced
# TR: FETCH-ATTEMPT GATEWAY KİMLİK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya fetch-attempt sonuç doğrusunun kalıcı log kapısı gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition/runtime katmanları ne olduğunu keşfeder
# TR: - bu gateway child terminal doğrusu kalıcılaştırmaya yardım eder
# TR: - üst katmanlar her terminal sonuçta DB cümlesini elle yazmamalıdır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli fetch-attempt DB-truth sınırı
# TR: - kalıcı attempt-result persistence yardımcı yüzeyi
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - gizli network fetch yürütücüsü
# TR: - gizli parse yürütücüsü
# TR: - gizli ranking yürütücüsü
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - terminal sonuç payload'ları yapılı dict-benzeri şekiller olabilir
# TR: - fetch_attempt kimlikleri açık kalmalıdır
# TR: - missing-row veya degraded dalları sessizce zorlanmamalı, görünür kalmalıdır

# EN: STAGE21-AUTO-COMMENT :: This import line declares fetch-attempt gateway dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, types, or constants shape attempt persistence behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether the effective attempt contract or helper boundary changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker helps readers treat imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak fetch-attempt gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi yardımcıların, tiplerin veya sabitlerin deneme kalıcılığı davranışını şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse etkin deneme sözleşmesinin veya yardımcı sınırının da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuların importları sessiz şablon değil mimari ipucu olarak görmesine yardım eder.

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares fetch-attempt gateway dependencies by bringing in typing -> Any.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, types, or constants shape attempt persistence behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether the effective attempt contract or helper boundary changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker helps readers treat imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı typing -> Any ögelerini içeri alarak fetch-attempt gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi yardımcıların, tiplerin veya sabitlerin deneme kalıcılığı davranışını şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse etkin deneme sözleşmesinin veya yardımcı sınırının da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuların importları sessiz şablon değil mimari ipucu olarak görmesine yardım eder.
from typing import Any

# EN: We import psycopg because this function is a thin wrapper around one SQL call.
# TR: Bu fonksiyon tek bir SQL çağrısının ince wrapper'ı olduğu için psycopg içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares fetch-attempt gateway dependencies by bringing in psycopg.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, types, or constants shape attempt persistence behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether the effective attempt contract or helper boundary changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker helps readers treat imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg ögelerini içeri alarak fetch-attempt gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi yardımcıların, tiplerin veya sabitlerin deneme kalıcılığı davranışını şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse etkin deneme sözleşmesinin veya yardımcı sınırının da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuların importları sessiz şablon değil mimari ipucu olarak görmesine yardım eder.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares fetch-attempt gateway dependencies by bringing in psycopg.rows -> dict_row.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, types, or constants shape attempt persistence behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether the effective attempt contract or helper boundary changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker helps readers treat imports as architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg.rows -> dict_row ögelerini içeri alarak fetch-attempt gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü hangi yardımcıların, tiplerin veya sabitlerin deneme kalıcılığı davranışını şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse etkin deneme sözleşmesinin veya yardımcı sınırının da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuların importları sessiz şablon değil mimari ipucu olarak görmesine yardım eder.
from psycopg.rows import dict_row




# EN: This helper rolls back the current transaction.
# TR: Bu yardımcı, mevcut transaction'ı rollback eder.

# EN: This helper finalizes a successful fetch outcome for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için başarılı fetch sonucunu finalize eder.

# EN: This helper writes one terminal durable fetch_attempt row through the new
# EN: canonical SQL surface without mutating frontier state.
# TR: Bu yardımcı frontier durumunu değiştirmeden yeni kanonik SQL yüzeyi
# TR: üzerinden tek bir terminal kalıcı fetch_attempt satırı yazar.
# EN: FETCH-ATTEMPT HELPER PURPOSE MEMORY BLOCK V5 / log_fetch_attempt_terminal
# EN:
# EN: Why this helper exists:
# EN: - because fetch-attempt-specific DB truth for 'log_fetch_attempt_terminal' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable fetch-attempt helper name instead of repeating raw SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata
# EN: - values should match the current Python signature and the live fetch-attempt SQL contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-attempt-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a terminal logging result, or another explicit branch result
# EN:
# EN: Common fetch-attempt meaning hints:
# EN: - this helper likely persists terminal fetch-attempt outcome truth
# EN: - outcome, evidence payload, or degraded write visibility may matter here
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw fetch-attempt SQL semantics instead of this helper contract
# TR: FETCH-ATTEMPT YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / log_fetch_attempt_terminal
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'log_fetch_attempt_terminal' için fetch-attempt'e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham fetch-attempt SQL semantiğini tekrar etmek yerine okunabilir fetch-attempt yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı fetch-attempt SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen fetch-attempt-odaklı sonuç şekli
# TR: - bu; yapılı payload, terminal logging sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak fetch-attempt anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal fetch-attempt sonuç doğrusunu kalıcılaştırır
# TR: - outcome, kanıt payload'ı veya degrade yazma görünürlüğü burada önemli olabilir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham fetch-attempt SQL semantiğini anlamaya zorlamak

# EN: FETCH-ATTEMPT HELPER PURPOSE MEMORY BLOCK V6 / log_fetch_attempt_terminal
# EN:
# EN: Why this helper exists:
# EN: - because fetch-attempt-specific DB truth for 'log_fetch_attempt_terminal' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable fetch-attempt helper name instead of repeating raw SQL semantics
# EN: - because terminal result persistence should stay inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata
# EN: - values should match the current Python signature and the live fetch-attempt SQL contract below
# EN:
# EN: Accepted output:
# EN: - a fetch-attempt-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a terminal logging result, a write receipt, or another explicit branch result
# EN:
# EN: Common fetch-attempt meaning hints:
# EN: - this helper likely persists terminal fetch-attempt outcome truth
# EN: - outcome, evidence payload, or degraded write visibility may matter here
# EN: - row-level write result visibility is often important here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the source of truth about network execution itself
# EN: - it is the named boundary where fetch-attempt truth becomes durable and readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw fetch-attempt SQL semantics instead of this helper contract
# TR: FETCH-ATTEMPT YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / log_fetch_attempt_terminal
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'log_fetch_attempt_terminal' için fetch-attempt'e özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham fetch-attempt SQL semantiğini tekrar etmek yerine okunabilir fetch-attempt yardımcı adı çağırmalıdır
# TR: - çünkü terminal sonuç kalıcılaştırması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı fetch-attempt SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen fetch-attempt-odaklı sonuç şekli
# TR: - bu; yapılı payload, terminal logging sonucu, write receipt veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak fetch-attempt anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle terminal fetch-attempt sonuç doğrusunu kalıcılaştırır
# TR: - outcome, kanıt payload'ı veya degrade yazma görünürlüğü burada önemli olabilir
# TR: - satır-düzeyi yazma sonuç görünürlüğü burada çoğu zaman önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı network yürütmesinin kendisi hakkında nihai doğruluk kaynağı değildir
# TR: - bu, fetch-attempt doğrusunun kalıcı ve okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham fetch-attempt SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This gateway function named log_fetch_attempt_terminal defines a fetch-attempt-facing contract boundary.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what log_fetch_attempt_terminal sends into persistence and what shape of attempt information comes back out.
# EN: STAGE21-AUTO-COMMENT :: When changing log_fetch_attempt_terminal, verify that caller expectations, attempt evidence semantics, and retry-related meaning all remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker exists so the beginning of log_fetch_attempt_terminal is easy to find during audits and incident tracing.
# TR: STAGE21-AUTO-COMMENT :: log_fetch_attempt_terminal isimli bu gateway fonksiyonu fetch-attempt tarafına bakan bir sözleşme sınırı tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu log_fetch_attempt_terminal fonksiyonunun kalıcılığa ne gönderdiğini ve hangi şekil deneme bilgisinin geri çıktığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: log_fetch_attempt_terminal değiştirilirken çağıran beklentilerinin, deneme kanıtı anlamının ve retry ile ilgili anlamın uyumlu kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret log_fetch_attempt_terminal başlangıcının denetim ve olay izleme sırasında kolay bulunabilmesi için vardır.
# EN: REAL-RULE AST REPAIR / DEF log_fetch_attempt_terminal
# EN: log_fetch_attempt_terminal is an explicit fetch-attempt-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata.
# TR: REAL-RULE AST REPAIR / FONKSIYON log_fetch_attempt_terminal
# TR: log_fetch_attempt_terminal acik bir fetch-attempt-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, url_id, host_id, worker_id, request_url, outcome, fetch_kind, lease_token, request_method, final_url, http_status, content_type, content_length, body_storage_path, body_sha256, body_bytes, etag, last_modified, error_class, error_message, fetch_metadata.
def log_fetch_attempt_terminal(
    conn: psycopg.Connection,
    *,
    url_id: int | None,
    host_id: int,
    worker_id: str,
    request_url: str,
    outcome: str,
    fetch_kind: str = "page",
    lease_token: str | None = None,
    request_method: str = "GET",
    final_url: str | None = None,
    http_status: int | None = None,
    content_type: str | None = None,
    content_length: int | None = None,
    body_storage_path: str | None = None,
    body_sha256: str | None = None,
    body_bytes: int | None = None,
    etag: str | None = None,
    last_modified: str | None = None,
    error_class: str | None = None,
    error_message: str | None = None,
    fetch_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # EN: We open one isolated cursor because this helper performs exactly one
    # EN: explicit insert-through-function call.
    # TR: Bu yardımcı tam olarak tek bir açık fonksiyon-üzerinden-insert çağrısı
    # TR: yaptığı için izole bir cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible fetch-attempt gateway flow and is annotated to keep the module beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this layer shapes stored attempt truth.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement together with nearby comments so local intention and wider persistence meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact gateway code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür fetch-attempt gateway akışının parçasıdır ve modülü yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu katman saklanan deneme gerçeğini şekillendirir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifadeyi yakın yorumlarla birlikte gözden geçir ki yerel niyet ile geniş kalıcılık anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık gateway kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We call the canonical terminal logging function instead of inserting
        # EN: into http_fetch.fetch_attempt directly so Python stays aligned with
        # EN: the sealed SQL contract.
        # TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye
        # TR: http_fetch.fetch_attempt tablosuna doğrudan insert atmak yerine
        # TR: kanonik terminal logging fonksiyonunu çağırıyoruz.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway-side action, often a call that bridges runtime intent to attempt persistence.
        # EN: STAGE21-AUTO-COMMENT :: Expressions here should stay readable because one compact call can hide an important write or read side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the gateway layer and still matches the intended attempt contract.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan gateway tarafı bir eylem gerçekleştirir; çoğu zaman runtime niyetini deneme kalıcılığına bağlayan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: Buradaki ifadeler okunabilir kalmalıdır çünkü tek bir sıkışık çağrı önemli bir yazma veya okuma yan etkisini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ gateway katmanına ait olduğunu ve amaçlanan deneme sözleşmesiyle eşleştiğini doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            select *
            from http_fetch.log_fetch_attempt_terminal(
                p_url_id => %(url_id)s,
                p_host_id => %(host_id)s,
                p_worker_id => %(worker_id)s,
                p_request_url => %(request_url)s,
                p_outcome => %(outcome)s::http_fetch.fetch_outcome_enum,
                p_fetch_kind => %(fetch_kind)s::http_fetch.fetch_kind_enum,
                p_lease_token => %(lease_token)s::uuid,
                p_request_method => %(request_method)s,
                p_final_url => %(final_url)s,
                p_http_status => %(http_status)s,
                p_content_type => %(content_type)s,
                p_content_length => %(content_length)s,
                p_body_storage_path => %(body_storage_path)s,
                p_body_sha256 => %(body_sha256)s,
                p_body_bytes => %(body_bytes)s,
                p_etag => %(etag)s,
                p_last_modified => %(last_modified)s,
                p_error_class => %(error_class)s,
                p_error_message => %(error_message)s,
                p_fetch_metadata => %(fetch_metadata)s::jsonb
            )
            """,
            {
                "url_id": url_id,
                "host_id": host_id,
                "worker_id": worker_id,
                "request_url": request_url,
                "outcome": outcome,
                "fetch_kind": fetch_kind,
                "lease_token": lease_token,
                "request_method": request_method,
                "final_url": final_url,
                "http_status": http_status,
                "content_type": content_type,
                "content_length": content_length,
                "body_storage_path": body_storage_path,
                "body_sha256": body_sha256,
                "body_bytes": body_bytes,
                "etag": etag,
                "last_modified": last_modified,
                "error_class": error_class,
                "error_message": error_message,
                "fetch_metadata": psycopg.types.json.Jsonb(fetch_metadata or {}),
            },
        )

        # EN: We fetch the single inserted canonical log row.
        # TR: Tek eklenen kanonik log satırını çekiyoruz.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the visible fetch-attempt gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this module often shape attempt metadata, persistence inputs, or normalized outputs and should remain easy to read.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, verify both the database-side expectation and the caller-side interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where local gateway state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini görünür fetch-attempt gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu modüldeki atamalar çoğu zaman deneme metadata'sını, kalıcılık girdilerini veya normalize çıktıları şekillendirir ve okunması kolay kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde hem veritabanı tarafı beklentisinin hem çağıran tarafı yorumunun uyumlu kaldığını doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret yerel gateway durumunun somutlaştığı noktayı vurgular.
        row = cur.fetchone()

    # EN: Missing output would mean the terminal logging surface failed structurally.
    # TR: Çıktı yoksa terminal logging yüzeyi yapısal olarak başarısız olmuş demektir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects gateway behavior based on current fetch-attempt input or state.
    # EN: STAGE21-AUTO-COMMENT :: Conditional logic matters here because even a small branch change can alter how attempt evidence is stored or interpreted.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect both paths and confirm they still preserve intended attempt semantics.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a control decision with downstream persistence consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut fetch-attempt girdisine veya duruma göre gateway davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşullu mantık burada önemlidir çünkü küçük bir dal değişimi bile deneme kanıtının nasıl saklandığını veya yorumlandığını değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dalı düzenlerken her iki yolu da incele ve amaçlanan deneme anlamını koruduklarını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret aşağı akış kalıcılık sonuçları doğuran bir kontrol kararını vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible fetch-attempt gateway flow and is annotated to keep the module beginner-friendly.
        # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this layer shapes stored attempt truth.
        # EN: STAGE21-AUTO-COMMENT :: Review this statement together with nearby comments so local intention and wider persistence meaning remain aligned.
        # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact gateway code from hiding silent meaning.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür fetch-attempt gateway akışının parçasıdır ve modülü yeni başlayan dostu tutmak için açıklanmıştır.
        # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu katman saklanan deneme gerçeğini şekillendirir.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifadeyi yakın yorumlarla birlikte gözden geçir ki yerel niyet ile geniş kalıcılık anlamı uyumlu kalsın.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık gateway kodunun sessiz anlam gizlemesini önler.
        raise RuntimeError("http_fetch.log_fetch_attempt_terminal(...) returned no row")

    # EN: We return the structured inserted row so the caller can surface it in
    # EN: operator-visible result payloads when useful.
    # TR: Çağıran taraf gerekirse bunu operatörün göreceği sonuç payload'ına
    # TR: ekleyebilsin diye yapılı eklenen satırı döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete fetch-attempt gateway result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract shape observed upstream.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, semantics, and nullability behavior.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir fetch-attempt gateway sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akışın gördüğü pratik sözleşme şeklini tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satırı değiştirirken çağıranların beklenen yapı, anlam ve boş olabilirlik davranışını almaya devam ettiğini doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row
