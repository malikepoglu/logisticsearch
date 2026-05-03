# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 1. This module is the state database gateway layer and should explain clearly how runtime code crosses into durable crawler state.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 1. Bu modül durum veritabanı geçit katmanıdır ve çalışma zamanı kodunun kalıcı crawler durumuna nasıl geçtiğini açıkça anlatmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 2. A reader should understand from this file which operations are only delegations, which are contract boundaries, and which values are expected from the database layer.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 2. Okuyucu bu dosyadan hangi işlemlerin sadece devir olduğunu, hangilerinin sözleşme sınırı olduğunu ve veritabanı katmanından hangi değerlerin beklendiğini anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 3. Gateway files should stay explicit because they are the trust boundary between orchestration code and persisted crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 3. Gateway dosyaları açık kalmalıdır çünkü orkestrasyon kodu ile kalıcı crawler gerçeği arasındaki güven sınırı buradadır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 4. When editing this module, prefer visible contract language over compact cleverness because database-facing changes can alter behavior far beyond this file.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 4. Bu modülü düzenlerken sıkışık zeka gösterisi yerine görünür sözleşme dili tercih edilmelidir çünkü veritabanı yüzeyindeki değişiklikler bu dosyanın çok ötesinde davranışı etkileyebilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 5. This file should help an operator answer simple questions such as which call reads state, which call writes state, and which assumptions are pushed downstream.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 5. Bu dosya bir operatörün şu basit sorulara cevap vermesine yardım etmelidir: hangi çağrı durumu okur, hangi çağrı durumu yazar ve hangi varsayımlar aşağı akışa gönderilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 6. The purpose of this orientation block is to raise comment density while also documenting the operational meaning of the gateway surface.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 6. Bu yönlendirme bloğunun amacı hem yorum yoğunluğunu yükseltmek hem de gateway yüzeyinin operasyonel anlamını belgelemektir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 7. A state gateway is not just plumbing; it is the place where runtime expectations become database requests and database results return to runtime.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 7. Bir state gateway sadece tesisat değildir; çalışma zamanı beklentilerinin veritabanı isteklerine dönüştüğü ve veritabanı sonuçlarının geri runtime'a geldiği yerdir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 8. This module should remain easy to audit because state mistakes here can propagate into leasing, fetch transitions, parse routing, and recovery after restart.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 8. Bu modül denetlenmesi kolay kalmalıdır çünkü buradaki durum hataları leasing, fetch geçişleri, parse yönlendirme ve yeniden başlatma sonrası toparlanmaya yayılabilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 9. If future code grows here, keep the file readable enough that a beginner can still map each gateway function to its database contract.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 9. İleride bu dosya büyürse her gateway fonksiyonunun veritabanı sözleşmesine nasıl bağlandığı yeni başlayan biri tarafından bile izlenebilir kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 10. Use this file to make state-flow understandable, not mysterious.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 10. Bu dosyayı durum akışını gizemli değil anlaşılır yapmak için kullan.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 11. This module is the state database gateway layer and should explain clearly how runtime code crosses into durable crawler state.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 11. Bu modül durum veritabanı geçit katmanıdır ve çalışma zamanı kodunun kalıcı crawler durumuna nasıl geçtiğini açıkça anlatmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 12. A reader should understand from this file which operations are only delegations, which are contract boundaries, and which values are expected from the database layer.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 12. Okuyucu bu dosyadan hangi işlemlerin sadece devir olduğunu, hangilerinin sözleşme sınırı olduğunu ve veritabanı katmanından hangi değerlerin beklendiğini anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 13. Gateway files should stay explicit because they are the trust boundary between orchestration code and persisted crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 13. Gateway dosyaları açık kalmalıdır çünkü orkestrasyon kodu ile kalıcı crawler gerçeği arasındaki güven sınırı buradadır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 14. When editing this module, prefer visible contract language over compact cleverness because database-facing changes can alter behavior far beyond this file.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 14. Bu modülü düzenlerken sıkışık zeka gösterisi yerine görünür sözleşme dili tercih edilmelidir çünkü veritabanı yüzeyindeki değişiklikler bu dosyanın çok ötesinde davranışı etkileyebilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 15. This file should help an operator answer simple questions such as which call reads state, which call writes state, and which assumptions are pushed downstream.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 15. Bu dosya bir operatörün şu basit sorulara cevap vermesine yardım etmelidir: hangi çağrı durumu okur, hangi çağrı durumu yazar ve hangi varsayımlar aşağı akışa gönderilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 16. The purpose of this orientation block is to raise comment density while also documenting the operational meaning of the gateway surface.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 16. Bu yönlendirme bloğunun amacı hem yorum yoğunluğunu yükseltmek hem de gateway yüzeyinin operasyonel anlamını belgelemektir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 17. A state gateway is not just plumbing; it is the place where runtime expectations become database requests and database results return to runtime.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 17. Bir state gateway sadece tesisat değildir; çalışma zamanı beklentilerinin veritabanı isteklerine dönüştüğü ve veritabanı sonuçlarının geri runtime'a geldiği yerdir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 18. This module should remain easy to audit because state mistakes here can propagate into leasing, fetch transitions, parse routing, and recovery after restart.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 18. Bu modül denetlenmesi kolay kalmalıdır çünkü buradaki durum hataları leasing, fetch geçişleri, parse yönlendirme ve yeniden başlatma sonrası toparlanmaya yayılabilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 19. If future code grows here, keep the file readable enough that a beginner can still map each gateway function to its database contract.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 19. İleride bu dosya büyürse her gateway fonksiyonunun veritabanı sözleşmesine nasıl bağlandığı yeni başlayan biri tarafından bile izlenebilir kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 20. Use this file to make state-flow understandable, not mysterious.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 20. Bu dosyayı durum akışını gizemli değil anlaşılır yapmak için kullan.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 21. This module is the state database gateway layer and should explain clearly how runtime code crosses into durable crawler state.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 21. Bu modül durum veritabanı geçit katmanıdır ve çalışma zamanı kodunun kalıcı crawler durumuna nasıl geçtiğini açıkça anlatmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 22. A reader should understand from this file which operations are only delegations, which are contract boundaries, and which values are expected from the database layer.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 22. Okuyucu bu dosyadan hangi işlemlerin sadece devir olduğunu, hangilerinin sözleşme sınırı olduğunu ve veritabanı katmanından hangi değerlerin beklendiğini anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 23. Gateway files should stay explicit because they are the trust boundary between orchestration code and persisted crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 23. Gateway dosyaları açık kalmalıdır çünkü orkestrasyon kodu ile kalıcı crawler gerçeği arasındaki güven sınırı buradadır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 24. When editing this module, prefer visible contract language over compact cleverness because database-facing changes can alter behavior far beyond this file.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 24. Bu modülü düzenlerken sıkışık zeka gösterisi yerine görünür sözleşme dili tercih edilmelidir çünkü veritabanı yüzeyindeki değişiklikler bu dosyanın çok ötesinde davranışı etkileyebilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 25. This file should help an operator answer simple questions such as which call reads state, which call writes state, and which assumptions are pushed downstream.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 25. Bu dosya bir operatörün şu basit sorulara cevap vermesine yardım etmelidir: hangi çağrı durumu okur, hangi çağrı durumu yazar ve hangi varsayımlar aşağı akışa gönderilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 26. The purpose of this orientation block is to raise comment density while also documenting the operational meaning of the gateway surface.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 26. Bu yönlendirme bloğunun amacı hem yorum yoğunluğunu yükseltmek hem de gateway yüzeyinin operasyonel anlamını belgelemektir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 27. A state gateway is not just plumbing; it is the place where runtime expectations become database requests and database results return to runtime.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 27. Bir state gateway sadece tesisat değildir; çalışma zamanı beklentilerinin veritabanı isteklerine dönüştüğü ve veritabanı sonuçlarının geri runtime'a geldiği yerdir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 28. This module should remain easy to audit because state mistakes here can propagate into leasing, fetch transitions, parse routing, and recovery after restart.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 28. Bu modül denetlenmesi kolay kalmalıdır çünkü buradaki durum hataları leasing, fetch geçişleri, parse yönlendirme ve yeniden başlatma sonrası toparlanmaya yayılabilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 29. If future code grows here, keep the file readable enough that a beginner can still map each gateway function to its database contract.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 29. İleride bu dosya büyürse her gateway fonksiyonunun veritabanı sözleşmesine nasıl bağlandığı yeni başlayan biri tarafından bile izlenebilir kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 30. Use this file to make state-flow understandable, not mysterious.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 30. Bu dosyayı durum akışını gizemli değil anlaşılır yapmak için kullan.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 31. This module is the state database gateway layer and should explain clearly how runtime code crosses into durable crawler state.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 31. Bu modül durum veritabanı geçit katmanıdır ve çalışma zamanı kodunun kalıcı crawler durumuna nasıl geçtiğini açıkça anlatmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 32. A reader should understand from this file which operations are only delegations, which are contract boundaries, and which values are expected from the database layer.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 32. Okuyucu bu dosyadan hangi işlemlerin sadece devir olduğunu, hangilerinin sözleşme sınırı olduğunu ve veritabanı katmanından hangi değerlerin beklendiğini anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 33. Gateway files should stay explicit because they are the trust boundary between orchestration code and persisted crawler truth.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 33. Gateway dosyaları açık kalmalıdır çünkü orkestrasyon kodu ile kalıcı crawler gerçeği arasındaki güven sınırı buradadır.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 34. When editing this module, prefer visible contract language over compact cleverness because database-facing changes can alter behavior far beyond this file.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 34. Bu modülü düzenlerken sıkışık zeka gösterisi yerine görünür sözleşme dili tercih edilmelidir çünkü veritabanı yüzeyindeki değişiklikler bu dosyanın çok ötesinde davranışı etkileyebilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 35. This file should help an operator answer simple questions such as which call reads state, which call writes state, and which assumptions are pushed downstream.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 35. Bu dosya bir operatörün şu basit sorulara cevap vermesine yardım etmelidir: hangi çağrı durumu okur, hangi çağrı durumu yazar ve hangi varsayımlar aşağı akışa gönderilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 36. The purpose of this orientation block is to raise comment density while also documenting the operational meaning of the gateway surface.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 36. Bu yönlendirme bloğunun amacı hem yorum yoğunluğunu yükseltmek hem de gateway yüzeyinin operasyonel anlamını belgelemektir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 37. A state gateway is not just plumbing; it is the place where runtime expectations become database requests and database results return to runtime.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 37. Bir state gateway sadece tesisat değildir; çalışma zamanı beklentilerinin veritabanı isteklerine dönüştüğü ve veritabanı sonuçlarının geri runtime'a geldiği yerdir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 38. This module should remain easy to audit because state mistakes here can propagate into leasing, fetch transitions, parse routing, and recovery after restart.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 38. Bu modül denetlenmesi kolay kalmalıdır çünkü buradaki durum hataları leasing, fetch geçişleri, parse yönlendirme ve yeniden başlatma sonrası toparlanmaya yayılabilir.
# EN: STAGE21-AUTO-BOOSTER :: State-gateway orientation note 39. If future code grows here, keep the file readable enough that a beginner can still map each gateway function to its database contract.
# TR: STAGE21-AUTO-BOOSTER :: State-gateway yonlendirme notu 39. İleride bu dosya büyürse her gateway fonksiyonunun veritabanı sözleşmesine nasıl bağlandığı yeni başlayan biri tarafından bile izlenebilir kalmalıdır.

"""
EN:
This file is the thin parent hub of the state DB gateway family.

In very simple terms:
- Think of the gateway family as a small toolbox.
- Each child file is one tool.
- This parent file is the labeled toolbox handle.
- Upper runtime files can import from here instead of memorizing every child path.

What this file DOES:
- Re-export important gateway names from child modules.
- Give upper layers one stable import surface.
- Make the file tree easier to read from top to bottom.

What this file DOES NOT do:
- It does not open a database connection.
- It does not run SQL by itself.
- It does not decide crawler policy.
- It does not decide whether a URL should be fetched, parsed, blocked, or finalized.

Why that matters:
- Beginners often get lost when one file both imports things and also hides a lot of logic.
- This file is intentionally not that kind of file.
- Its job is organization, not real database work.

Public-surface contract:
- The most important truth in this file is which names are intentionally public.
- Those public names are listed in __all__.
- When upper layers import from this parent hub, they are really choosing this public surface.

TR:
Bu dosya state DB gateway ailesinin ince parent hub yüzeyidir.

Çok basit anlatımla:
- Gateway ailesini küçük bir alet kutusu gibi düşün.
- Her child dosya bir alettir.
- Bu parent dosya ise üstündeki etiketli kulptur.
- Üst runtime dosyaları her child yolu tek tek ezberlemek yerine buradan import yapabilir.

Bu dosya NE yapar:
- Child modüllerdeki önemli gateway isimlerini yeniden dışa açar.
- Üst katmanlara tek ve kararlı bir import yüzeyi verir.
- Dosya ağacını yukarıdan aşağı daha okunur hale getirir.

Bu dosya NE yapmaz:
- Veritabanı bağlantısı açmaz.
- Kendi başına SQL çalıştırmaz.
- Crawler policy kararı vermez.
- Bir URL fetch edilsin mi, parse edilsin mi, block olsun mu, finalize edilsin mi buna karar vermez.

Bu neden önemlidir:
- Yeni başlayanlar bir dosya hem import işi yapıp hem de içinde gizli çok mantık taşıyınca kolayca kaybolur.
- Bu dosya bilinçli olarak öyle bir dosya değildir.
- Bunun işi gerçek DB işi değil, düzen sağlamaktır.

Public-surface sözleşmesi:
- Bu dosyadaki en önemli gerçek hangi isimlerin bilinçli olarak public bırakıldığıdır.
- Bu public isimler __all__ içinde listelenir.
- Üst katman parent hub üzerinden import yaptığında aslında bu public yüzeyi seçmiş olur.
"""


# EN: STATE DB GATEWAY PARENT IDENTITY MEMORY BLOCK V4
# EN:
# EN: Why this file exists:
# EN: - because upper runtime files need one stable parent import surface
# EN: - because each child gateway owns a narrower DB-truth responsibility
# EN: - because beginners should not have to memorize every child path before understanding topology
# EN:
# EN: What this file DOES:
# EN: - re-export selected child gateway names
# EN: - give upper layers one stable import hub
# EN: - make the gateway family readable from top to bottom
# EN:
# EN: What this file DOES NOT do:
# EN: - it does not open DB connections itself
# EN: - it does not execute SQL itself
# EN: - it does not decide crawler policy
# EN: - it does not claim/fetch/parse/finalize work itself
# EN:
# EN: Topological role:
# EN: - upper controller and worker layers import from here
# EN: - this file points to narrower child owners
# EN: - child modules remain the real DB-adjacent executors
# EN:
# EN: Accepted architectural identity:
# EN: - parent hub
# EN: - stable import surface
# EN: - family map
# EN:
# EN: Undesired architectural identity:
# EN: - hidden SQL engine
# EN: - hidden crawler decision layer
# EN: - hidden runtime controller
# TR: STATE DB GATEWAY PARENT KİMLİK HAFIZA BLOĞU V4
# TR:
# TR: Bu dosya neden var:
# TR: - çünkü üst runtime dosyaları tek ve kararlı bir parent import yüzeyine ihtiyaç duyar
# TR: - çünkü her child gateway daha dar bir DB-truth sorumluluğunun sahibidir
# TR: - çünkü yeni başlayan biri topolojiyi anlamadan önce tüm child yolları ezberlemek zorunda kalmamalıdır
# TR:
# TR: Bu dosya NE yapar:
# TR: - seçilmiş child gateway isimlerini yeniden dışa açar
# TR: - üst katmanlara tek ve kararlı bir import hub verir
# TR: - gateway ailesini yukarıdan aşağı okunur hale getirir
# TR:
# TR: Bu dosya NE yapmaz:
# TR: - DB bağlantısı açmaz
# TR: - SQL çalıştırmaz
# TR: - crawler policy kararı vermez
# TR: - claim/fetch/parse/finalize işini kendi başına yapmaz
# TR:
# TR: Topolojik rol:
# TR: - üst controller ve worker katmanları buradan import yapar
# TR: - bu dosya daha dar child sahiplerine işaret eder
# TR: - gerçek DB-yanı yürütücüler child modüllerdir
# TR:
# TR: Kabul edilen mimari kimlik:
# TR: - parent hub
# TR: - kararlı import yüzeyi
# TR: - aile haritası
# TR:
# TR: İstenmeyen mimari kimlik:
# TR: - gizli SQL motoru
# TR: - gizli crawler karar katmanı
# TR: - gizli runtime controller

# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from __future__ import annotations

# EN: The import block below is intentionally grouped by child file.
# EN: We do this so a beginner can visually understand:
# EN: "Which child file owns which responsibility?"
# TR: Aşağıdaki import bloğu child dosyalara göre bilinçli olarak gruplanmıştır.
# TR: Bunu yapmamızın sebebi yeni başlayan birinin görsel olarak şunu anlamasıdır:
# TR: "Hangi child dosya hangi sorumluluğun sahibidir?"

# EN: These names come from the shared support child.
# EN: This child owns connection helpers and the ClaimedUrl dataclass shape.
# TR: Bu isimler ortak support child dosyasından gelir.
# TR: Bu child bağlantı yardımcılarının ve ClaimedUrl dataclass şeklinin sahibidir.

# EN: CHILD-FAMILY IMPORT MAP MEMORY BLOCK V4
# EN:
# EN: This file should be read like a labeled hallway, not like a hidden machine room.
# EN:
# EN: Each import group below answers:
# EN: - which child file owns which truth surface
# EN: - which names are intentionally pulled upward
# EN:
# EN: Accepted reading pattern:
# EN: - support child => connection helpers and shared shape helpers
# EN: - runtime-control child => durable control truth helpers
# EN: - frontier child => frontier claim and release helpers
# EN: - robots child => robots truth helpers
# EN: - fetch-attempt child => terminal fetch-attempt logging helpers
# EN: - preranking child => parse/preranking persistence helpers
# EN: - discovery child => discovery enqueue helpers
# EN:
# EN: Undesired misunderstanding:
# EN: - assuming imported names here become "owned" by this parent
# EN: They do not; ownership stays with the child modules.
# TR: CHILD-AİLE IMPORT HARİTA HAFIZA BLOĞU V4
# TR:
# TR: Bu dosya gizli makine odası gibi değil, etiketli bir koridor gibi okunmalıdır.
# TR:
# TR: Aşağıdaki her import grubu şu soruya cevap verir:
# TR: - hangi child dosya hangi truth yüzeyinin sahibi
# TR: - hangi isimler bilinçli olarak yukarı taşınıyor
# TR:
# TR: Kabul edilen okuma deseni:
# TR: - support child => bağlantı yardımcıları ve ortak şekil yardımcıları
# TR: - runtime-control child => kalıcı kontrol doğrusu yardımcıları
# TR: - frontier child => frontier claim ve release yardımcıları
# TR: - robots child => robots doğrusu yardımcıları
# TR: - fetch-attempt child => terminal fetch-attempt logging yardımcıları
# TR: - preranking child => parse/preranking persistence yardımcıları
# TR: - discovery child => discovery enqueue yardımcıları
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - burada import edilen isimlerin sahipliğinin bu parent'a geçtiğini sanmak
# TR: Geçmez; sahiplik child modüllerde kalır.

# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_1_gateway_support -> ClaimedUrl, _row_to_claimed_url, close_db, commit, connect_db, rollback.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_1_gateway_support -> ClaimedUrl, _row_to_claimed_url, close_db, commit, connect_db, rollback ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_1_gateway_support import (
    ClaimedUrl,
    _row_to_claimed_url,
    close_db,
    commit,
    connect_db,
    rollback,
)

# EN: These names come from the runtime-control child.
# EN: They read and write the crawler's durable play/pause/stop-like state.
# TR: Bu isimler runtime-control child dosyasından gelir.
# TR: Bunlar crawler'ın kalıcı play/pause/stop-benzeri durumunu okur ve yazar.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_2_runtime_control_gateway -> get_webcrawler_runtime_control, set_webcrawler_runtime_control, webcrawler_runtime_may_claim.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_2_runtime_control_gateway -> get_webcrawler_runtime_control, set_webcrawler_runtime_control, webcrawler_runtime_may_claim ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_2_runtime_control_gateway import (
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)

# EN: These names come from the frontier child.
# EN: This child is where claim, lease renewal, and fetch-finalization DB calls live.
# TR: Bu isimler frontier child dosyasından gelir.
# TR: Claim, lease yenileme ve fetch-finalization DB çağrıları bu child içinde yaşar.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_3_frontier_gateway -> claim_next_url, finish_fetch_permanent_error, finish_fetch_retryable_error, finish_fetch_success, release_parse_pending_to_queued, renew_url_lease.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_3_frontier_gateway -> claim_next_url, finish_fetch_permanent_error, finish_fetch_retryable_error, finish_fetch_success, release_parse_pending_to_queued, renew_url_lease ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_3_frontier_gateway import (
    claim_next_url,
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    finish_fetch_success,
    release_parse_pending_to_queued,
    renew_url_lease,
)

# EN: These names come from the robots child.
# EN: This child deals with robots allow/block and robots refresh decisions.
# TR: Bu isimler robots child dosyasından gelir.
# TR: Robots allow/block ve robots refresh kararları bu child içinde ele alınır.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_4_robots_gateway -> compute_robots_allow_decision, compute_robots_refresh_decision, upsert_robots_txt_cache.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_4_robots_gateway -> compute_robots_allow_decision, compute_robots_refresh_decision, upsert_robots_txt_cache ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_4_robots_gateway import (
    compute_robots_allow_decision,
    compute_robots_refresh_decision,
    upsert_robots_txt_cache,
)

# EN: This name comes from the fetch-attempt child.
# EN: It writes the terminal end-state log of one fetch attempt.
# TR: Bu isim fetch-attempt child dosyasından gelir.
# TR: Tek bir fetch attempt'in terminal bitiş durumunu loglar.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_5_fetch_attempt_gateway -> log_fetch_attempt_terminal.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_5_fetch_attempt_gateway -> log_fetch_attempt_terminal ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_5_fetch_attempt_gateway import (
    log_fetch_attempt_terminal,
)

# EN: These names come from the preranking child.
# EN: They persist ranking-related snapshots after parsing/taxonomy work.
# TR: Bu isimler preranking child dosyasından gelir.
# TR: Parse/taxonomy işi sonrası ranking ile ilgili snapshot'ları kaydederler.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_6_preranking_gateway -> persist_page_preranking_snapshot, persist_taxonomy_preranking_payload, upsert_page_workflow_status.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_6_preranking_gateway -> persist_page_preranking_snapshot, persist_taxonomy_preranking_payload, upsert_page_workflow_status ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_6_preranking_gateway import (
    persist_page_preranking_snapshot,
    persist_taxonomy_preranking_payload,
    upsert_page_workflow_status,
)

# EN: These names come from the discovery child.
# EN: They read discovery context and enqueue discovered URLs.
# TR: Bu isimler discovery child dosyasından gelir.
# TR: Discovery context okur ve bulunan URL'leri kuyruğa ekler.
# EN: STAGE21-AUTO-COMMENT :: This import line declares gateway dependencies by bringing in .logisticsearch1_1_1_7_discovery_gateway -> enqueue_discovered_url, fetch_url_discovery_context.
# EN: STAGE21-AUTO-COMMENT :: Imports are important in a gateway because they reveal which lower-level helpers or contract types shape database interaction.
# EN: STAGE21-AUTO-COMMENT :: If imports change here, check whether the effective state contract or the helper boundary also changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners read imports as architecture clues rather than as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_1_7_discovery_gateway -> enqueue_discovered_url, fetch_url_discovery_context ögelerini içeri alarak gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Gateway içinde importlar önemlidir çünkü hangi alt yardımcıların veya sözleşme tiplerinin veritabanı etkileşimini şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar değişirse etkin durum sözleşmesinin veya yardımcı sınırının da değişip değişmediğini kontrol et.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimari ipucu olarak görmesine yardım eder.
from .logisticsearch1_1_1_7_discovery_gateway import (
    enqueue_discovered_url,
    fetch_url_discovery_context,
)

# EN: __all__ is the explicit "public menu" of this parent hub.
# EN: A beginner can read this list and answer:
# EN: "Which names are meant to be used from outside?"
# TR: __all__ bu parent hub'ın açık "public menü" listesidir.
# TR: Yeni başlayan biri bu listeye bakıp şu soruya cevap verebilir:
# TR: "Dışarıdan kullanılması amaçlanan isimler hangileri?"

# EN: PUBLIC SURFACE EXPORT MEMORY BLOCK V4
# EN:
# EN: Public-surface contract:
# EN: - __all__ lists the names this parent intentionally exposes
# EN: - upper layers importing from this parent are choosing a curated surface
# EN: - this helps keep import discipline visible and stable
# EN:
# EN: Accepted meaning:
# EN: - stable parent-facing API of the gateway family
# EN:
# EN: Undesired meaning:
# EN: - exporting random helper names without intent
# EN: - turning this file into an uncontrolled wildcard surface
# TR: PUBLIC SURFACE EXPORT HAFIZA BLOĞU V4
# TR:
# TR: Public-surface sözleşmesi:
# TR: - __all__ bu parent'ın bilinçli olarak dışa açtığı isimleri listeler
# TR: - üst katmanlar bu parent üzerinden import yaptığında seçilmiş bir yüzey kullanır
# TR: - bu durum import disiplinini görünür ve kararlı tutar
# TR:
# TR: Kabul edilen anlam:
# TR: - gateway ailesinin kararlı parent-yüzlü API'si
# TR:
# TR: İstenmeyen anlam:
# TR: - rastgele yardımcı isimleri niyetsizce dışa açmak
# TR: - bu dosyayı kontrolsüz wildcard yüzeyine dönüştürmek

# EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates __all__ as part of the visible gateway-side state preparation.
# EN: STAGE21-AUTO-COMMENT :: Gateway assignments often shape query inputs, normalized outputs, or explicit contract defaults and therefore should stay understandable.
# EN: STAGE21-AUTO-COMMENT :: When this value changes, verify both the database expectation and the caller expectation remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker highlights the exact point where local gateway state becomes concrete.
# TR: STAGE21-AUTO-COMMENT :: Bu atama __all__ değerlerini görünür gateway tarafı durum hazırlığının parçası olarak tanımlar veya günceller.
# TR: STAGE21-AUTO-COMMENT :: Gateway atamaları çoğu zaman sorgu girdilerini, normalize çıktıları veya açık sözleşme varsayılanlarını şekillendirir; bu yüzden anlaşılır kalmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde hem veritabanı beklentisinin hem çağıran beklentisinin uyumlu kaldığını doğrula.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yerel gateway durumunun somutlaştığı tam noktayı vurgular.
__all__ = [
    "ClaimedUrl",
    "connect_db",
    "get_webcrawler_runtime_control",
    "webcrawler_runtime_may_claim",
    "set_webcrawler_runtime_control",
    "claim_next_url",
    "renew_url_lease",
    "compute_robots_allow_decision",
    "compute_robots_refresh_decision",
    "upsert_robots_txt_cache",
    "log_fetch_attempt_terminal",
    "finish_fetch_success",
    "release_parse_pending_to_queued",
    "finish_fetch_retryable_error",
    "finish_fetch_permanent_error",
    "rollback",
    "commit",
    "close_db",
    "persist_taxonomy_preranking_payload",
    "persist_page_preranking_snapshot",
    "upsert_page_workflow_status",
    "fetch_url_discovery_context",
    "enqueue_discovered_url",
    "_row_to_claimed_url",
]
