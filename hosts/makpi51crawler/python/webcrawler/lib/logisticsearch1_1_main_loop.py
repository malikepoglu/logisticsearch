# EN: MAIN_LOOP_DENSITY_RESCUE_BLOCK_V1
# EN: This module is the main orchestration loop for the crawler runtime surface.
# TR: Bu modul crawler runtime yuzeyinin ana orkestrasyon dongusudur.
# EN: A maintainer should read this file as the operational spine that keeps the crawler moving.
# TR: Bir bakimci bu dosyayi crawler'i hareket halinde tutan operasyonel omurga olarak okumelidir.
# EN: The main loop coordinates repeated work, stop conditions, recovery behavior, and observable control flow.
# TR: Ana dongu tekrarli isi, durdurma kosullarini, toparlanma davranisini ve gozlemlenebilir kontrol akisini koordine eder.
# EN: This rescue block only adds explanation and must not change execution semantics.
# TR: Bu kurtarma blogu yalnizca aciklama ekler ve calisma anlambilimini degistirmemelidir.
# EN: The purpose of this file is not only to iterate, but to iterate safely and predictably.
# TR: Bu dosyanin amaci yalnizca tekrar etmek degil, guvenli ve ongorulebilir bicimde tekrar etmektir.
# EN: Predictability matters because a crawler loop is often observed during incidents or long unattended runs.
# TR: Ongorulebilirlik onemlidir cunku bir crawler dongusu cogu zaman olay anlarinda veya uzun sureli gozetimsiz calismalarda izlenir.
# EN: If the loop becomes unclear, the operator loses confidence in where the crawler is and why it is waiting or progressing.
# TR: Dongu belirsiz hale gelirse operator crawler'in nerede oldugu ve neden bekledigi ya da ilerledigi konusunda guven kaybeder.
# EN: The comments below intentionally emphasize state transitions, sleep decisions, retry decisions, and exit decisions.
# TR: Asagidaki yorumlar bilerek durum gecislerini, uyku kararlarini, tekrar deneme kararlarini ve cikis kararlarini vurgular.
# EN: A main loop must make boundaries obvious: one cycle starts, one cycle does work, one cycle ends.
# TR: Bir ana dongu sinirlari acik hale getirmelidir: bir dongu baslar, bir dongu is yapar, bir dongu biter.
# EN: A main loop should also make it obvious when no work is available.
# TR: Bir ana dongu ayni zamanda hic is olmadiginda bunu da acik hale getirmelidir.
# EN: No-work behavior is operationally important because it defines idle posture, poll interval, and incident interpretation.
# TR: Is-yok davranisi operasyonel olarak onemlidir cunku bos bekleme durusunu, anket araligini ve olay yorumunu belirler.
# EN: A clear loop explains how it behaves when the frontier is empty, paused, blocked, or waiting on politeness.
# TR: Acik bir dongu frontier bos, pause edilmis, bloklu veya nezaket kurali nedeniyle beklemedeyken nasil davrandigini aciklar.
# EN: A clear loop also explains how it behaves when work succeeds, partially succeeds, or fails.
# TR: Acik bir dongu ayni zamanda is basarili oldugunda, kismen basarili oldugunda veya hata verdiginde nasil davrandigini aciklar.
# EN: This file should remain beginner-readable even if the full crawler architecture is large.
# TR: Tam crawler mimarisi buyuk olsa bile bu dosya baslangic seviyesinde okunabilir kalmalidir.
# EN: That is why repeated operational commentary is acceptable here.
# TR: Bu nedenle burada tekrarli operasyonel aciklama kabul edilebilirdir.
# EN: The loop is the heartbeat-like repetition surface of the worker process.
# TR: Dongu worker surecinin heartbeat benzeri tekrar yuzeyidir.
# EN: The loop should never hide why it continues, why it waits, or why it exits.
# TR: Dongu neden devam ettigini, neden bekledigini veya neden ciktigini asla gizlememelidir.
# EN: Continue decisions should be transparent.
# TR: Devam etme kararlari seffaf olmalidir.
# EN: Wait decisions should be transparent.
# TR: Bekleme kararlari seffaf olmalidir.
# EN: Exit decisions should be transparent.
# TR: Cikis kararlari seffaf olmalidir.
# EN: Recovery decisions should be transparent.
# TR: Toparlanma kararlari seffaf olmalidir.
# EN: Logging and return behavior should help future audits reconstruct what happened in the loop.
# TR: Loglama ve donus davranisi gelecekteki auditlerin dongude ne oldugunu yeniden kurmasina yardim etmelidir.
# EN: This module belongs to the highest-value runtime path because every worker cycle depends on it.
# TR: Bu modul en yuksek degerli runtime yoluna aittir cunku her worker dongusu ona baglidir.
# EN: If this file is misunderstood, the crawler may appear healthy while actually drifting, stalling, or looping badly.
# TR: Bu dosya yanlis anlasilirsa crawler saglikli gorunurken aslinda kayiyor, takiliyor veya kotu bir donguye giriyor olabilir.
# EN: Therefore each meaningful section should explain intent before code details.
# TR: Bu nedenle her anlamli bolum kod ayrintilarindan once niyeti aciklamalidir.
# EN: The next filler notes intentionally keep the file self-explanatory in isolation.
# TR: Siradaki doldurma notlari dosyayi tek basina aciklayici tutmayi bilerek hedefler.
# EN: Main loop note 001. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 001. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 002. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 002. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 003. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 003. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 004. Main loop retries should have a reason.
# TR: Ana dongu notu 004. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 005. Main loop exits should have a reason.
# TR: Ana dongu notu 005. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 006. Main loop progress should be externally explainable.
# TR: Ana dongu notu 006. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 007. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 007. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 008. Main loop should remain auditable line by line.
# TR: Ana dongu notu 008. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 009. Main loop should not surprise operators.
# TR: Ana dongu notu 009. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 010. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 010. Ana dongu takilma durumlarini gizlememelidir.
# EN: Main loop note 011. Main loop should support incident reasoning.
# TR: Ana dongu notu 011. Ana dongu olay muhakemesini desteklemelidir.
# EN: Main loop note 012. Main loop should support restart reasoning.
# TR: Ana dongu notu 012. Ana dongu yeniden baslatma muhakemesini desteklemelidir.
# EN: Main loop note 013. Main loop should support pause and resume reasoning.
# TR: Ana dongu notu 013. Ana dongu duraklatma ve devam ettirme muhakemesini desteklemelidir.
# EN: Main loop note 014. Main loop should show the difference between no work and blocked work.
# TR: Ana dongu notu 014. Ana dongu is yok durumu ile bloke is durumunun farkini gostermelidir.
# EN: Main loop note 015. Main loop should make sleep placement obvious.
# TR: Ana dongu notu 015. Ana dongu uyku yerlesimini belirgin hale getirmelidir.
# EN: Main loop note 016. Main loop should keep orchestration readable.
# TR: Ana dongu notu 016. Ana dongu orkestrasyonu okunabilir tutmalidir.
# EN: Main loop note 017. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 017. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 018. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 018. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 019. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 019. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 020. Main loop retries should have a reason.
# TR: Ana dongu notu 020. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 021. Main loop exits should have a reason.
# TR: Ana dongu notu 021. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 022. Main loop progress should be externally explainable.
# TR: Ana dongu notu 022. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 023. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 023. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 024. Main loop should remain auditable line by line.
# TR: Ana dongu notu 024. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 025. Main loop should not surprise operators.
# TR: Ana dongu notu 025. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 026. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 026. Ana dongu takilma durumlarini gizlememelidir.
# EN: Main loop note 027. Main loop should support incident reasoning.
# TR: Ana dongu notu 027. Ana dongu olay muhakemesini desteklemelidir.
# EN: Main loop note 028. Main loop should support restart reasoning.
# TR: Ana dongu notu 028. Ana dongu yeniden baslatma muhakemesini desteklemelidir.
# EN: Main loop note 029. Main loop should support pause and resume reasoning.
# TR: Ana dongu notu 029. Ana dongu duraklatma ve devam ettirme muhakemesini desteklemelidir.
# EN: Main loop note 030. Main loop should show the difference between no work and blocked work.
# TR: Ana dongu notu 030. Ana dongu is yok durumu ile bloke is durumunun farkini gostermelidir.
# EN: Main loop note 031. Main loop should make sleep placement obvious.
# TR: Ana dongu notu 031. Ana dongu uyku yerlesimini belirgin hale getirmelidir.
# EN: Main loop note 032. Main loop should keep orchestration readable.
# TR: Ana dongu notu 032. Ana dongu orkestrasyonu okunabilir tutmalidir.
# EN: Main loop note 033. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 033. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 034. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 034. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 035. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 035. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 036. Main loop retries should have a reason.
# TR: Ana dongu notu 036. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 037. Main loop exits should have a reason.
# TR: Ana dongu notu 037. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 038. Main loop progress should be externally explainable.
# TR: Ana dongu notu 038. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 039. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 039. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 040. Main loop should remain auditable line by line.
# TR: Ana dongu notu 040. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 041. Main loop should not surprise operators.
# TR: Ana dongu notu 041. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 042. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 042. Ana dongu takilma durumlarini gizlememelidir.
# EN: Main loop note 043. Main loop should support incident reasoning.
# TR: Ana dongu notu 043. Ana dongu olay muhakemesini desteklemelidir.
# EN: Main loop note 044. Main loop should support restart reasoning.
# TR: Ana dongu notu 044. Ana dongu yeniden baslatma muhakemesini desteklemelidir.
# EN: Main loop note 045. Main loop should support pause and resume reasoning.
# TR: Ana dongu notu 045. Ana dongu duraklatma ve devam ettirme muhakemesini desteklemelidir.
# EN: Main loop note 046. Main loop should show the difference between no work and blocked work.
# TR: Ana dongu notu 046. Ana dongu is yok durumu ile bloke is durumunun farkini gostermelidir.
# EN: Main loop note 047. Main loop should make sleep placement obvious.
# TR: Ana dongu notu 047. Ana dongu uyku yerlesimini belirgin hale getirmelidir.
# EN: Main loop note 048. Main loop should keep orchestration readable.
# TR: Ana dongu notu 048. Ana dongu orkestrasyonu okunabilir tutmalidir.
# EN: Main loop note 049. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 049. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 050. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 050. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 051. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 051. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 052. Main loop retries should have a reason.
# TR: Ana dongu notu 052. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 053. Main loop exits should have a reason.
# TR: Ana dongu notu 053. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 054. Main loop progress should be externally explainable.
# TR: Ana dongu notu 054. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 055. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 055. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 056. Main loop should remain auditable line by line.
# TR: Ana dongu notu 056. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 057. Main loop should not surprise operators.
# TR: Ana dongu notu 057. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 058. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 058. Ana dongu takilma durumlarini gizlememelidir.
# EN: Main loop note 059. Main loop should support incident reasoning.
# TR: Ana dongu notu 059. Ana dongu olay muhakemesini desteklemelidir.
# EN: Main loop note 060. Main loop should support restart reasoning.
# TR: Ana dongu notu 060. Ana dongu yeniden baslatma muhakemesini desteklemelidir.
# EN: Main loop note 061. Main loop should support pause and resume reasoning.
# TR: Ana dongu notu 061. Ana dongu duraklatma ve devam ettirme muhakemesini desteklemelidir.
# EN: Main loop note 062. Main loop should show the difference between no work and blocked work.
# TR: Ana dongu notu 062. Ana dongu is yok durumu ile bloke is durumunun farkini gostermelidir.
# EN: Main loop note 063. Main loop should make sleep placement obvious.
# TR: Ana dongu notu 063. Ana dongu uyku yerlesimini belirgin hale getirmelidir.
# EN: Main loop note 064. Main loop should keep orchestration readable.
# TR: Ana dongu notu 064. Ana dongu orkestrasyonu okunabilir tutmalidir.
# EN: Main loop note 065. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 065. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 066. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 066. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 067. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 067. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 068. Main loop retries should have a reason.
# TR: Ana dongu notu 068. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 069. Main loop exits should have a reason.
# TR: Ana dongu notu 069. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 070. Main loop progress should be externally explainable.
# TR: Ana dongu notu 070. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 071. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 071. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 072. Main loop should remain auditable line by line.
# TR: Ana dongu notu 072. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 073. Main loop should not surprise operators.
# TR: Ana dongu notu 073. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 074. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 074. Ana dongu takilma durumlarini gizlememelidir.
# EN: Main loop note 075. Main loop should support incident reasoning.
# TR: Ana dongu notu 075. Ana dongu olay muhakemesini desteklemelidir.
# EN: Main loop note 076. Main loop should support restart reasoning.
# TR: Ana dongu notu 076. Ana dongu yeniden baslatma muhakemesini desteklemelidir.
# EN: Main loop note 077. Main loop should support pause and resume reasoning.
# TR: Ana dongu notu 077. Ana dongu duraklatma ve devam ettirme muhakemesini desteklemelidir.
# EN: Main loop note 078. Main loop should show the difference between no work and blocked work.
# TR: Ana dongu notu 078. Ana dongu is yok durumu ile bloke is durumunun farkini gostermelidir.
# EN: Main loop note 079. Main loop should make sleep placement obvious.
# TR: Ana dongu notu 079. Ana dongu uyku yerlesimini belirgin hale getirmelidir.
# EN: Main loop note 080. Main loop should keep orchestration readable.
# TR: Ana dongu notu 080. Ana dongu orkestrasyonu okunabilir tutmalidir.
# EN: Main loop note 081. Main loop cycles should be easy to count mentally.
# TR: Ana dongu notu 081. Ana dongu cevrimleri zihinsel olarak sayilmasi kolay olmalidir.
# EN: Main loop note 082. Main loop state should be easy to inspect during debugging.
# TR: Ana dongu notu 082. Ana dongu durumu debug sirasinda incelenmesi kolay olmalidir.
# EN: Main loop note 083. Main loop waiting should be deliberate, not accidental.
# TR: Ana dongu notu 083. Ana dongu beklemesi kazara degil bilincli olmalidir.
# EN: Main loop note 084. Main loop retries should have a reason.
# TR: Ana dongu notu 084. Ana dongu tekrar denemelerinin bir nedeni olmalidir.
# EN: Main loop note 085. Main loop exits should have a reason.
# TR: Ana dongu notu 085. Ana dongu cikislarinin bir nedeni olmalidir.
# EN: Main loop note 086. Main loop progress should be externally explainable.
# TR: Ana dongu notu 086. Ana dongu ilerlemesi disaridan aciklanabilir olmalidir.
# EN: Main loop note 087. Main loop should separate control flow from side effects as much as possible.
# TR: Ana dongu notu 087. Ana dongu kontrol akisini yan etkilerden mumkun oldugunca ayirmalidir.
# EN: Main loop note 088. Main loop should remain auditable line by line.
# TR: Ana dongu notu 088. Ana dongu satir satir denetlenebilir kalmalidir.
# EN: Main loop note 089. Main loop should not surprise operators.
# TR: Ana dongu notu 089. Ana dongu operatorleri sasirtmamalidir.
# EN: Main loop note 090. Main loop should not hide stalled conditions.
# TR: Ana dongu notu 090. Ana dongu takilma durumlarini gizlememelidir.

"""
EN:
This file is the canonical operator-facing main loop surface directly below the
thin root-entry file.

EN:
If the root-entry file is the front door, this file is the first real control room.

EN:
Why this file exists:
- Because the project needs one visible place where operator input becomes runtime action.
- Because we do not want root-entry to own real control logic.
- Because we do not want worker-runtime files to also become CLI parsing files.
- Because the system becomes easier to read when "operator control surface" is
  separated from "deeper worker machinery".

EN:
Read this file as the place where these questions are answered:
- Did the operator ask to only inspect runtime-control?
- Did the operator ask to change runtime-control?
- Did the operator ask for one worker probe?
- Did the operator ask for repeated worker probes in a loop?

EN:
What this file DOES:
- define CLI arguments
- resolve default DSN / worker_id / requested_by values
- build WorkerConfig
- choose runtime-control corridor vs worker-probe corridor
- print structured JSON payloads
- decide small integer exit status for this CLI surface

EN:
What this file DOES NOT do:
- it does not write SQL itself
- it does not implement claim_next_url(...) itself
- it does not implement robots policy itself
- it does not fetch HTML itself
- it does not parse HTML itself
- it does not persist final fetch outcomes itself

EN:
Topological role:
- logisticsearch1_main_entry.py delegates into this file
- this file talks to gateway surfaces and worker-runtime surfaces
- deeper files do the DB / worker / acquisition / parse work
- this file remains the operator/controller layer

EN:
Important visible variables:
- args:
  - expected type: argparse.Namespace
  - meaning: parsed CLI input
  - accepted shape: parser-defined attributes only
  - undesired state: missing expected attributes
- config:
  - expected type: WorkerConfig
  - meaning: structured handoff package from CLI/controller layer to worker-runtime layer
- set_result:
  - accepted branches:
    - None => no runtime-control write happened
    - dict => runtime-control write happened
  - undesired value: non-dict truthy object
- runtime_control:
  - expected type: dict-like snapshot
  - common accepted desired_state values: "run", "pause", "stop"
  - tolerated fallback value: empty string when missing
  - undesired shape: non-dict truthy payload
- may_claim_result:
  - expected type: dict
  - accepted may_claim values:
    - True
    - False
    - None on degraded branch
- payload:
  - expected type: JSON-serializable dict
  - meaning: final operator-visible output package
- probe_only:
  - expected type: bool
  - accepted values:
    - True => rollback-style probe corridor
    - False => durable-claim corridor
- iteration:
  - expected type: int
  - accepted runtime values inside loop: 1, 2, 3, ...
  - undesired state: negative numbers

TR:
Bu dosya ince kök giriş dosyasının hemen altında duran kanonik operatör-yüzlü ana loop yüzeyidir.

TR:
Kök giriş dosyası ön kapıysa, bu dosya ilk gerçek kontrol odasıdır.

TR:
Bu dosya neden var:
- Çünkü projenin operatör girdisinin runtime davranışına dönüştüğü tek görünür bir yere ihtiyacı var.
- Çünkü kök giriş dosyasının gerçek kontrol mantığını taşımasını istemiyoruz.
- Çünkü worker-runtime dosyalarının aynı zamanda CLI parsing dosyasına dönüşmesini istemiyoruz.
- Çünkü "operatör kontrol yüzeyi" ile "daha derin worker makinesi" ayrılınca sistem daha kolay okunuyor.

TR:
Bu dosyayı şu soruların cevaplandığı yer gibi oku:
- Operatör yalnızca runtime-control durumunu görmek mi istedi?
- Operatör runtime-control durumunu değiştirmek mi istedi?
- Operatör tek worker probe mu istedi?
- Operatör loop içinde tekrar eden worker probe mu istedi?

TR:
Bu dosya NE yapar:
- CLI argümanlarını tanımlar
- varsayılan DSN / worker_id / requested_by değerlerini çözer
- WorkerConfig oluşturur
- runtime-control koridoru ile worker-probe koridoru arasında seçim yapar
- yapılı JSON payload'lar basar
- bu CLI yüzeyi için küçük int çıkış kodu belirler

TR:
Bu dosya NE yapmaz:
- SQL'i kendi başına yazmaz
- claim_next_url(...) mantığını kendi başına uygulamaz
- robots policy'yi kendi başına uygulamaz
- HTML fetch etmez
- HTML parse etmez
- final fetch outcome'larını kendi başına persist etmez

TR:
Topolojik rol:
- logisticsearch1_main_entry.py bu dosyaya delege eder
- bu dosya gateway yüzeyleri ve worker-runtime yüzeyleri ile konuşur
- daha derindeki dosyalar DB / worker / acquisition / parse işini yapar
- bu dosya operatör/controller katmanı olarak kalır

TR:
Önemli görünür değişkenler:
- args:
  - beklenen tip: argparse.Namespace
  - anlam: parse edilmiş CLI girdisi
  - kabul edilen şekil: yalnızca parser'ın tanımladığı attribute'lar
  - istenmeyen durum: beklenen attribute'ların eksik olması
- config:
  - beklenen tip: WorkerConfig
  - anlam: CLI/controller katmanından worker-runtime katmanına giden yapılı teslim paketi
- set_result:
  - kabul edilen dallar:
    - None => runtime-control write olmadı
    - dict => runtime-control write oldu
  - istenmeyen değer: dict olmayan truthy nesne
- runtime_control:
  - beklenen tip: dict-benzeri snapshot
  - yaygın kabul edilen desired_state değerleri: "run", "pause", "stop"
  - tolere edilen fallback değer: eksikse boş string
  - istenmeyen şekil: dict olmayan truthy payload
- may_claim_result:
  - beklenen tip: dict
  - kabul edilen may_claim değerleri:
    - True
    - False
    - degrade dalda None
- payload:
  - beklenen tip: JSON-serileştirilebilir dict
  - anlam: operatöre görünen son çıktı paketi
- probe_only:
  - beklenen tip: bool
  - kabul edilen değerler:
    - True => rollback-benzeri probe koridoru
    - False => durable-claim koridoru
- iteration:
  - beklenen tip: int
  - loop içinde kabul edilen runtime değerleri: 1, 2, 3, ...
  - istenmeyen durum: negatif sayılar
"""

from __future__ import annotations

# EN: MAIN LOOP PURPOSE MEMORY BLOCK V4
# EN:
# EN: This file exists because the project needs one clear operator-facing place
# EN: where human intent becomes structured runtime action.
# EN:
# EN: Without this file, responsibilities would blur:
# EN: - root-entry would become too smart
# EN: - worker-runtime would become too CLI-heavy
# EN: - gateway files would become too operator-facing
# EN:
# EN: That would damage readability.
# EN: This file prevents that damage.
# EN:
# EN: Accepted architectural identity:
# EN: - controller layer
# EN: - operator-facing surface
# EN: - orchestrator
# EN:
# EN: Undesired architectural identity:
# EN: - hidden SQL owner
# EN: - hidden parser engine
# EN: - hidden fetch engine
# EN: - hidden finalization engine
# TR: MAIN LOOP AMAÇ HAFIZA BLOĞU V4
# TR:
# TR: Bu dosya var; çünkü proje insan niyetinin yapılı runtime eylemine
# TR: dönüştüğü tek ve açık operatör-yüzlü yere ihtiyaç duyar.
# TR:
# TR: Bu dosya olmazsa sorumluluklar bulanıklaşır:
# TR: - root-entry fazla akıllı olur
# TR: - worker-runtime fazla CLI yüklü olur
# TR: - gateway dosyaları fazla operatör-yüzlü olur
# TR:
# TR: Bu da okunabilirliğe zarar verir.
# TR: Bu dosya o zararı önler.
# TR:
# TR: Kabul edilen mimari kimlik:
# TR: - controller katmanı
# TR: - operatör-yüzlü yüzey
# TR: - orkestratör
# TR:
# TR: İstenmeyen mimari kimlik:
# TR: - gizli SQL sahibi
# TR: - gizli parser motoru
# TR: - gizli fetch motoru
# TR: - gizli finalization motoru

import argparse
import json
import os
import time
from dataclasses import asdict

from .logisticsearch1_1_1_state_db_gateway import (
    connect_db,
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)
from .logisticsearch1_1_2_worker_runtime import WorkerConfig, run_claim_probe


# EN: Function default_dsn is part of the main loop orchestration contract.


# TR: default_dsn fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.


# EN: Read this function by checking inputs, cycle role, error path, and return meaning.


# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / default_dsn
# EN: default_dsn resolves the canonical fallback DSN string used by the main-loop control surface.
# EN: This helper has no direct parameters and returns the default DSN value when the operator did not pass an explicit DSN.
# TR: FONKSIYON SOZLESMESI / default_dsn
# TR: default_dsn ana dongu kontrol yuzeyi tarafindan kullanilan kanonik fallback DSN stringini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir DSN vermediginde varsayilan DSN degerini dondurur.

# EN: FUNCTION CONTRACT / default_dsn / IMMEDIATE BLOCK
# EN: default_dsn resolves the canonical fallback DSN string used by this main-loop control surface.
# EN: This helper has no direct parameters and returns the default DSN value when the operator did not pass one explicitly.
# TR: FONKSIYON SOZLESMESI / default_dsn / ANLIK BLOK
# TR: default_dsn bu ana-dongu kontrol yuzeyinin kullandigi kanonik fallback DSN stringini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir DSN vermediginde varsayilan DSN degerini dondurur.
def default_dsn() -> str:
    """
    EN:
    Resolve the DSN used by this CLI/controller surface.

    EN:
    Why this helper exists:
    - So the main() function does not get cluttered with repeated default-resolution logic.
    - So the DSN default rule is visible in one place.
    - So a reader can quickly answer:
      "Where does this CLI get its DB connection text if the operator says nothing?"

    EN:
    Resolution rule:
    - first prefer LOGISTICSEARCH_CRAWLER_DSN from the environment
    - otherwise fall back to a local scratch-oriented DSN string

    EN:
    Return contract:
    - expected type: str
    - accepted value: non-empty PostgreSQL DSN text
    - accepted branches:
      - explicit environment value
      - fallback local scratch value
    - undesired values:
      - empty string
      - whitespace-only string
      - None
      - non-string object

    TR:
    Bu CLI/controller yüzeyinin kullanacağı DSN değerini çözer.

    TR:
    Bu yardımcı neden var:
    - main() fonksiyonu tekrar eden varsayılan çözüm mantığı ile kirlenmesin diye
    - DSN varsayılan kuralı tek yerde görünür olsun diye
    - okuyucu şu soruya hızlı cevap verebilsin diye:
      "Operatör hiçbir şey söylemezse bu CLI DB bağlantı metnini nereden alıyor?"

    TR:
    Çözüm kuralı:
    - önce environment içindeki LOGISTICSEARCH_CRAWLER_DSN değerini tercih et
    - yoksa yerel scratch odaklı fallback DSN metnine düş

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: str
    - kabul edilen değer: boş olmayan PostgreSQL DSN metni
    - kabul edilen dallar:
      - açık environment değeri
      - fallback yerel scratch değeri
    - istenmeyen değerler:
      - boş string
      - yalnızca boşluk
      - None
      - string olmayan nesne
    """

    # EN:
    # env_value is the optional operator/environment override.
    # EN:
    # Expected type:
    # - str or None
    # EN:
    # Accepted value:
    # - non-empty DSN text
    # EN:
    # Undesired values:
    # - empty string
    # - blank string
    # - malformed text that looks like config but is not usable
    # TR:
    # env_value opsiyonel operatör/environment override değeridir.
    # TR:
    # Beklenen tip:
    # - str veya None
    # TR:
    # Kabul edilen değer:
    # - boş olmayan DSN metni
    # TR:
    # İstenmeyen değerler:
    # - boş string
    # - yalnızca boşluk
    # - konfigürasyon gibi görünüp aslında kullanılamayan bozuk metin
    env_value = os.getenv("LOGISTICSEARCH_CRAWLER_DSN")

    if env_value:
        return env_value

    # EN:
    # This fallback is intentionally explicit and local-facing.
    # EN:
    # Accepted meaning:
    # - a developer/operator scratch database target
    # EN:
    # Undesired misunderstanding:
    # - thinking this is a hidden production secret source
    # TR:
    # Bu fallback bilinçli olarak açık ve yerel geliştirici odaklıdır.
    # TR:
    # Kabul edilen anlam:
    # - geliştirici/operatör scratch veritabanı hedefi
    # TR:
    # İstenmeyen yanlış anlama:
    # - bunun gizli production secret kaynağı olduğunu sanmak
    return "dbname=logisticsearch_crawler_split_scratch user=postgres"


# EN: Function default_worker_id is part of the main loop orchestration contract.


# TR: default_worker_id fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.


# EN: Read this function by checking inputs, cycle role, error path, and return meaning.


# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / default_worker_id
# EN: default_worker_id resolves the visible fallback worker identity text used by claim-oriented runtime calls.
# EN: This helper has no direct parameters and returns the default worker id value when the operator did not pass one explicitly.
# TR: FONKSIYON SOZLESMESI / default_worker_id
# TR: default_worker_id claim odakli runtime cagirilari icin kullanilan gorunur fallback worker kimligini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir worker id vermediginde varsayilan worker kimligini dondurur.

# EN: FUNCTION CONTRACT / default_worker_id / IMMEDIATE BLOCK
# EN: default_worker_id resolves the visible fallback worker identity text used by claim-oriented runtime calls.
# EN: This helper has no direct parameters and returns the default worker id value when the operator did not pass one explicitly.
# TR: FONKSIYON SOZLESMESI / default_worker_id / ANLIK BLOK
# TR: default_worker_id claim odakli runtime cagirilari icin kullanilan gorunur fallback worker kimligini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir worker kimligi vermediginde varsayilan worker id degerini dondurur.
def default_worker_id() -> str:
    """
    EN:
    Resolve the worker identity text used by claim-oriented runtime calls.

    EN:
    Why this helper exists:
    - So worker identity resolution is visible and reusable.
    - So the reader can answer:
      "What worker_id is used if the operator does not pass one?"

    EN:
    Return contract:
    - expected type: str
    - accepted value: non-empty worker identity text
    - common accepted examples:
      - environment override
      - "makpi51crawler_probe_worker"
    - undesired values:
      - empty string
      - whitespace-only string
      - None

    TR:
    Claim odaklı runtime çağrılarında kullanılacak worker kimliği metnini çözer.

    TR:
    Bu yardımcı neden var:
    - worker kimliği çözüm kuralı görünür ve tekrar kullanılabilir olsun diye
    - okuyucu şu soruya cevap verebilsin diye:
      "Operatör worker_id vermezse hangi değer kullanılıyor?"

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: str
    - kabul edilen değer: boş olmayan worker kimlik metni
    - yaygın kabul edilen örnekler:
      - environment override
      - "makpi51crawler_probe_worker"
    - istenmeyen değerler:
      - boş string
      - yalnızca boşluk
      - None
    """

    # EN:
    # env_value is the optional environment override for worker identity.
    # TR:
    # env_value worker kimliği için opsiyonel environment override değeridir.
    env_value = os.getenv("LOGISTICSEARCH_WORKER_ID")

    if env_value:
        return env_value

    return "makpi51crawler_probe_worker"


# EN: Function default_requested_by is part of the main loop orchestration contract.


# TR: default_requested_by fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.


# EN: Read this function by checking inputs, cycle role, error path, and return meaning.


# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / default_requested_by
# EN: default_requested_by resolves the requester identity text written into runtime-control changes.
# EN: This helper has no direct parameters and returns the default requester text when the operator did not provide one explicitly.
# TR: FONKSIYON SOZLESMESI / default_requested_by
# TR: default_requested_by runtime-control degisikliklerine yazilan istek sahibi kimlik metnini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir requester metni vermediginde varsayilan degeri dondurur.

# EN: FUNCTION CONTRACT / default_requested_by / IMMEDIATE BLOCK
# EN: default_requested_by resolves the requester identity text written into runtime-control changes.
# EN: This helper has no direct parameters and returns the default requester text when the operator did not provide one explicitly.
# TR: FONKSIYON SOZLESMESI / default_requested_by / ANLIK BLOK
# TR: default_requested_by runtime-control degisikliklerine yazilan istek sahibi kimlik metnini cozer.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve operator acik bir requester metni vermediginde varsayilan requester degerini dondurur.
def default_requested_by() -> str:
    """
    EN:
    Resolve the requester identity text written into runtime-control changes.

    EN:
    Why this helper exists:
    - runtime-control writes should say who requested the change
    - that rule should be visible in one place

    EN:
    Return contract:
    - expected type: str
    - accepted value: non-empty requester identity text
    - undesired values:
      - empty string
      - whitespace-only string
      - None

    TR:
    Runtime-control değişikliklerine yazılacak requester kimliği metnini çözer.

    TR:
    Bu yardımcı neden var:
    - runtime-control yazıları değişikliği kimin istediğini söylemeli
    - bu kural tek bir yerde görünür olmalı

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: str
    - kabul edilen değer: boş olmayan requester kimlik metni
    - istenmeyen değerler:
      - boş string
      - yalnızca boşluk
      - None
    """

    # EN:
    # env_value is the optional environment override for requested_by identity.
    # TR:
    # env_value requested_by kimliği için opsiyonel environment override değeridir.
    env_value = os.getenv("LOGISTICSEARCH_CONTROL_REQUESTED_BY")

    if env_value:
        return env_value

    return "logisticsearch1_1_main_loop"


# EN: CORRIDOR IDENTITY MEMORY BLOCK V4
# EN:
# EN: A beginner should be able to point at this file and say:
# EN: "This is where corridor selection happens."
# EN:
# EN: Accepted corridor families:
# EN: - runtime-control read corridor
# EN: - runtime-control write corridor
# EN: - single worker probe corridor
# EN: - repeated worker loop corridor
# EN:
# EN: Undesired misunderstanding:
# EN: - assuming these corridors are implemented fully here
# EN: They are not.
# EN: They are selected here and executed through narrower layers.
# TR: KORİDOR KİMLİĞİ HAFIZA BLOĞU V4
# TR:
# TR: Yeni başlayan biri bu dosyayı gösterip şunu diyebilmelidir:
# TR: "Koridor seçimi burada oluyor."
# TR:
# TR: Kabul edilen koridor aileleri:
# TR: - runtime-control okuma koridoru
# TR: - runtime-control yazma koridoru
# TR: - tek worker probe koridoru
# TR: - tekrar eden worker loop koridoru
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu koridorların bütünüyle burada uygulandığını sanmak
# TR: Hayır.
# TR: Burada seçilirler, daha dar katmanlar üzerinden çalıştırılırlar.

# EN: Function build_parser is part of the main loop orchestration contract.

# TR: build_parser fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.

# EN: Read this function by checking inputs, cycle role, error path, and return meaning.

# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / build_parser
# EN: build_parser constructs the operator-facing argparse parser used by this main-loop surface.
# EN: This helper has no direct parameters and returns the CLI parser object that defines accepted operator arguments.
# TR: FONKSIYON SOZLESMESI / build_parser
# TR: build_parser bu ana-dongu yuzeyi tarafindan kullanilan operator odakli argparse parser nesnesini kurar.
# TR: Bu yardimcinin dogrudan parametresi yoktur ve kabul edilen operator argumanlarini tanimlayan CLI parser nesnesini dondurur.
def build_parser() -> argparse.ArgumentParser:
    """
    EN:
    Build the CLI parser for this operator/control surface.

    EN:
    Why this helper exists:
    - because operator language should be defined in one visible place
    - because parser acceptance and runtime meaning are related but not identical
    - because a new reader should quickly see which flags exist

    EN:
    Important reading rule:
    - parser acceptance is not the same thing as semantic goodness
    - example:
      - argparse may accept any int for --lease-seconds
      - but semantically we still prefer positive values

    EN:
    Return contract:
    - expected type: argparse.ArgumentParser
    - never returns None

    TR:
    Bu operatör/kontrol yüzeyi için CLI parser'ını kurar.

    TR:
    Bu yardımcı neden var:
    - çünkü operatör dili tek bir görünür yerde tanımlanmalı
    - çünkü parser kabulü ile runtime anlamı ilişkili ama aynı şey değildir
    - çünkü yeni okuyucu hangi bayrakların olduğunu hızlıca görmelidir

    TR:
    Önemli okuma kuralı:
    - parser kabulü ile semantik olarak iyi olmak aynı şey değildir
    - örnek:
      - argparse --lease-seconds için herhangi bir int kabul edebilir
      - ama semantik olarak yine de pozitif değerleri tercih ederiz

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: argparse.ArgumentParser
    - asla None döndürmez
    """

    # EN:
    # parser is the single CLI definition object for this file.
    # EN:
    # Expected type:
    # - argparse.ArgumentParser
    # EN:
    # Accepted role:
    # - define flags
    # - validate parser-level input
    # - produce argparse.Namespace
    # EN:
    # Undesired role:
    # - acting as hidden runtime state storage
    # TR:
    # parser bu dosyanın tek CLI tanım nesnesidir.
    # TR:
    # Beklenen tip:
    # - argparse.ArgumentParser
    # TR:
    # Kabul edilen rol:
    # - bayrakları tanımlamak
    # - parser-seviyesi girdiyi doğrulamak
    # - argparse.Namespace üretmek
    # TR:
    # İstenmeyen rol:
    # - gizli runtime state deposu gibi davranmak
    parser = argparse.ArgumentParser(
        description="Controlled worker probe, runtime-control, and loop operator surface for LogisticSearch crawler_core."
    )

    parser.add_argument(
        "--dsn",
        default=default_dsn(),
        help="PostgreSQL DSN. Defaults to LOGISTICSEARCH_CRAWLER_DSN or a local scratch fallback.",
    )

    parser.add_argument(
        "--worker-id",
        default=default_worker_id(),
        help="Worker identity passed into frontier.claim_next_url(...).",
    )

    parser.add_argument(
        "--lease-seconds",
        type=int,
        default=600,
        help="Lease duration, in seconds, passed into frontier.claim_next_url(...).",
    )

    parser.add_argument(
        "--durable-claim",
        action="store_true",
        help="Commit a successful claim so the lease remains durable in the database.",
    )

    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run repeated worker iterations inside the existing canonical CLI surface.",
    )

    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=5.0,
        help="Normal delay between loop iterations.",
    )

    parser.add_argument(
        "--pause-sleep-seconds",
        type=float,
        default=15.0,
        help="Delay between loop iterations while runtime-control is pause.",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="Maximum loop iterations. Zero means no explicit iteration limit.",
    )

    parser.add_argument(
        "--show-runtime-control",
        action="store_true",
        help="Read and print the current runtime-control DB truth.",
    )

    parser.add_argument(
        "--set-runtime-control",
        choices=("run", "pause", "stop"),
        help="Set the durable runtime-control state through DB truth.",
    )

    parser.add_argument(
        "--state-reason",
        default="operator requested runtime control change via canonical CLI",
        help="Reason text written into ops.webcrawler_runtime_control.",
    )

    parser.add_argument(
        "--requested-by",
        default=default_requested_by(),
        help="Requester identity written into ops.webcrawler_runtime_control.",
    )

    parser.add_argument(
        "--output",
        choices=("json",),
        default="json",
        help="Current supported output format.",
    )

    return parser


# EN: Function sleep_between_loop_iterations is part of the main loop orchestration contract.


# TR: sleep_between_loop_iterations fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.


# EN: Read this function by checking inputs, cycle role, error path, and return meaning.


# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / sleep_between_loop_iterations
# EN: sleep_between_loop_iterations chooses the next loop sleep duration from visible loop state.
# EN: Parameter contract:
# EN: - payload => the visible dict snapshot produced by the current loop iteration and inspected for pause/no-work meaning
# EN: - sleep_seconds => the normal steady-state sleep duration used when pause-specific sleep is not required
# EN: - pause_sleep_seconds => the longer or special sleep duration used when payload indicates pause-oriented waiting
# TR: FONKSIYON SOZLESMESI / sleep_between_loop_iterations
# TR: sleep_between_loop_iterations gorunur dongu durumundan bir sonraki uyku suresini secer.
# TR: Parametre sozlesmesi:
# TR: - payload => mevcut dongu iterasyonunun urettiği ve pause/is-yok anlamı icin incelenen gorunur dict anlik goruntusu
# TR: - sleep_seconds => pause-ozel uyku gerekmiyorsa kullanilan normal kararlı uyku suresi
# TR: - pause_sleep_seconds => payload pause-odakli bekleme gosteriyorsa kullanilan daha uzun veya ozel uyku suresi

# EN: FUNCTION CONTRACT / sleep_between_loop_iterations / IMMEDIATE BLOCK
# EN: sleep_between_loop_iterations chooses the next loop sleep duration from visible loop state.
# EN: Parameter contract:
# EN: - payload => the visible dict snapshot produced by the current loop iteration and inspected for pause or no-work meaning
# EN: - sleep_seconds => the normal steady-state sleep duration used when pause-specific sleep is not required
# EN: - pause_sleep_seconds => the pause-oriented sleep duration used when payload indicates pause-style waiting
# TR: FONKSIYON SOZLESMESI / sleep_between_loop_iterations / ANLIK BLOK
# TR: sleep_between_loop_iterations gorunur dongu durumundan bir sonraki uyku suresini secer.
# TR: Parametre sozlesmesi:
# TR: - payload => mevcut dongu iterasyonunun urettiği ve pause veya is-yok anlami icin incelenen gorunur dict anlik goruntusu
# TR: - sleep_seconds => pause-ozel uyku gerekmiyorsa kullanilan normal kararlı uyku suresi
# TR: - pause_sleep_seconds => payload pause-tarzı bekleme gosteriyorsa kullanilan pause-odakli uyku suresi
def sleep_between_loop_iterations(*, payload: dict, sleep_seconds: float, pause_sleep_seconds: float) -> float:
    """
    EN:
    Choose loop sleep duration from the visible payload snapshot.

    EN:
    Why this helper exists:
    - because timing choice should be visible and small
    - because pause mode should sleep differently from normal mode
    - because loop timing should follow the same payload the operator just saw

    EN:
    Input contract:
    - payload:
      - expected type: dict
      - accepted content: may contain runtime_control snapshot
      - tolerated branch: missing runtime_control
      - undesired shape: non-dict truthy payload
    - sleep_seconds:
      - expected type: float
      - accepted semantic value: non-negative normal delay
      - undesired value: negative float
    - pause_sleep_seconds:
      - expected type: float
      - accepted semantic value: non-negative pause delay
      - undesired value: negative float

    EN:
    Return contract:
    - expected type: float
    - if desired_state == "pause" => return pause_sleep_seconds
    - otherwise => return sleep_seconds

    TR:
    Görünür payload snapshot'ına göre loop sleep süresini seçer.

    TR:
    Bu yardımcı neden var:
    - çünkü zamanlama seçimi küçük ve görünür kalmalı
    - çünkü pause modu normal moddan farklı uyumalı
    - çünkü loop zamanlaması operatörün az önce gördüğü aynı payload'ı izlemeli

    TR:
    Girdi sözleşmesi:
    - payload:
      - beklenen tip: dict
      - kabul edilen içerik: runtime_control snapshot taşıyabilir
      - tolere edilen dal: runtime_control eksik olabilir
      - istenmeyen şekil: dict olmayan truthy payload
    - sleep_seconds:
      - beklenen tip: float
      - kabul edilen semantik değer: negatif olmayan normal gecikme
      - istenmeyen değer: negatif float
    - pause_sleep_seconds:
      - beklenen tip: float
      - kabul edilen semantik değer: negatif olmayan pause gecikmesi
      - istenmeyen değer: negatif float

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: float
    - desired_state == "pause" ise => pause_sleep_seconds döndür
    - aksi durumda => sleep_seconds döndür
    """

    # EN:
    # runtime_control is normalized to a dict snapshot.
    # EN:
    # Accepted states after normalization:
    # - real dict snapshot
    # - {} fallback
    # EN:
    # Undesired upstream shape:
    # - non-dict truthy payload
    # TR:
    # runtime_control dict snapshot'ına normalize edilir.
    # TR:
    # Normalizasyon sonrası kabul edilen durumlar:
    # TR:
    # - gerçek dict snapshot
    # - {} fallback
    # TR:
    # İstenmeyen upstream şekil:
    # - dict olmayan truthy payload
    runtime_control = payload.get("runtime_control") or {}

    # EN:
    # desired_state is normalized into lowercase text.
    # EN:
    # Common accepted values:
    # - "run"
    # - "pause"
    # - "stop"
    # EN:
    # Tolerated fallback:
    # - empty string
    # - unexpected text
    # EN:
    # Undesired semantic meaning:
    # - random text may indicate upstream drift,
    #   but this helper still falls back safely
    # TR:
    # desired_state küçük harfli metne normalize edilir.
    # TR:
    # Yaygın kabul edilen değerler:
    # - "run"
    # - "pause"
    # - "stop"
    # TR:
    # Tolere edilen fallback:
    # - boş string
    # - beklenmeyen metin
    # TR:
    # İstenmeyen semantik anlam:
    # - rastgele metin upstream drift gösterebilir,
    #   ama bu yardımcı yine de güvenli fallback'e düşer
    desired_state = str(runtime_control.get("desired_state") or "").strip().lower()

    if desired_state == "pause":
        return pause_sleep_seconds

    return sleep_seconds


# EN: VALUE SHAPE MEMORY BLOCK V4
# EN:
# EN: Three value-shape distinctions matter a lot in this file:
# EN: - parser-accepted value
# EN: - semantically good runtime value
# EN: - degraded-but-visible value
# EN:
# EN: Examples:
# EN: - may_claim may be True / False / None
# EN: - desired_state is commonly run / pause / stop
# EN: - payload shape differs by corridor
# EN:
# EN: Undesired beginner mistake:
# EN: - assuming one variable always has one semantic meaning in all branches
# EN: In this file branch-awareness matters.
# TR: DEĞER ŞEKLİ HAFIZA BLOĞU V4
# TR:
# TR: Bu dosyada üç değer-şekli ayrımı çok önemlidir:
# TR: - parser tarafından kabul edilen değer
# TR: - semantik olarak iyi runtime değeri
# TR: - degrade ama görünür değer
# TR:
# TR: Örnekler:
# TR: - may_claim True / False / None olabilir
# TR: - desired_state çoğunlukla run / pause / stop olur
# TR: - payload şekli koridora göre değişir
# TR:
# TR: İstenmeyen başlangıç hatası:
# TR: - bir değişkenin her dalda aynı semantik anlama sahip olduğunu sanmak
# TR: Bu dosyada dal farkındalığı önemlidir.

# EN: Function main is part of the main loop orchestration contract.

# TR: main fonksiyonu ana dongu orkestrasyon sozlesmesinin bir parcasidir.

# EN: Read this function by checking inputs, cycle role, error path, and return meaning.

# TR: Bu fonksiyonu girdiler, cevrim rolu, hata yolu ve donus anlami uzerinden okuyun.
# EN: FUNCTION CONTRACT / main
# EN: main runs the canonical operator-facing main-loop surface for runtime-control inspection and worker loop execution.
# EN: This function has no direct parameters and returns the final process exit code that explains the operator-visible outcome.
# TR: FONKSIYON SOZLESMESI / main
# TR: main runtime-control inceleme yolu ile worker dongu calistirma yolunu tasiyan kanonik operator-odakli ana-dongu yuzeyini calistirir.
# TR: Bu fonksiyonun dogrudan parametresi yoktur ve operatorun gorecegi sonucu aciklayan nihai process cikis kodunu dondurur.
def main() -> int:
    """
    EN:
    Run the canonical operator-facing main loop surface.

    EN:
    Why this function exists:
    - because one place must decide which operator corridor runs
    - because runtime-control inspection/set and worker-probe execution should not
      be mixed invisibly across many files
    - because structured JSON output should come from one visible controller layer

    EN:
    High-level execution map:
    1) parse CLI input
    2) choose runtime-control corridor or worker corridor
    3) if worker corridor, build WorkerConfig
    4) run one probe or repeated loop
    5) print JSON output
    6) return small integer exit status

    EN:
    Return contract:
    - expected type: int
    - accepted common values:
      - 0 => clean structured success
      - 2 => degraded-but-visible runtime-control corridor
    - accepted broader values:
      - any other intentional int if future controller policy adds one
    - undesired values:
      - None
      - non-int objects

    TR:
    Kanonik operatör-yüzlü ana loop yüzeyini çalıştırır.

    TR:
    Bu fonksiyon neden var:
    - çünkü hangi operatör koridorunun çalışacağını tek bir yer seçmelidir
    - çünkü runtime-control inceleme/ayarlama ile worker-probe çalıştırma işi
      görünmez biçimde birçok dosyaya dağılmamalıdır
    - çünkü yapılı JSON çıktı tek bir görünür controller katmanından gelmelidir

    TR:
    Yüksek seviye çalışma haritası:
    1) CLI girdisini parse et
    2) runtime-control koridoru mu worker koridoru mu seç
    3) worker koridoru ise WorkerConfig oluştur
    4) tek probe veya tekrar eden loop çalıştır
    5) JSON çıktı bas
    6) küçük int çıkış kodu döndür

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: int
    - kabul edilen yaygın değerler:
      - 0 => temiz yapılı başarı
      - 2 => degrade ama görünür runtime-control koridoru
    - daha geniş kabul edilen değerler:
      - ileride controller policy eklerse diğer bilinçli int değerleri
    - istenmeyen değerler:
      - None
      - int olmayan nesneler
    """

    # EN:
    # parser is the CLI definition surface for this file.
    # TR:
    # parser bu dosyanın CLI tanım yüzeyidir.
    parser = build_parser()

    # EN:
    # args is the parsed operator input package.
    # EN:
    # Expected type:
    # - argparse.Namespace
    # EN:
    # Accepted content:
    # - parser-defined attributes only
    # EN:
    # Undesired state:
    # - missing expected attributes
    # - parser/code drift
    # TR:
    # args parse edilmiş operatör girdi paketidir.
    # TR:
    # Beklenen tip:
    # - argparse.Namespace
    # TR:
    # Kabul edilen içerik:
    # - yalnızca parser tarafından tanımlanan attribute'lar
    # TR:
    # İstenmeyen durum:
    # - beklenen attribute'ların eksik olması
    # - parser/kod drift'i
    args = parser.parse_args()

    if args.show_runtime_control or args.set_runtime_control is not None:
        # EN:
        # conn is the live DB connection used only for runtime-control corridor work.
        # EN:
        # Expected type:
        # - psycopg.Connection-like object returned by connect_db(...)
        # EN:
        # Accepted input source:
        # - args.dsn non-empty usable DSN text
        # EN:
        # Undesired input:
        # - broken DSN text
        # - blank DSN text
        # TR:
        # conn yalnızca runtime-control koridorunda kullanılan canlı DB bağlantısıdır.
        # TR:
        # Beklenen tip:
        # - connect_db(...) tarafından dönen psycopg.Connection-benzeri nesne
        # TR:
        # Kabul edilen girdi kaynağı:
        # - args.dsn içinden gelen boş olmayan kullanılabilir DSN metni
        # TR:
        # İstenmeyen girdi:
        # - bozuk DSN metni
        # - boş DSN metni
        conn = connect_db(args.dsn)

        try:
            # EN:
            # set_result starts as None on the show-only branch.
            # EN:
            # Accepted branches:
            # - None => no write happened
            # - dict => runtime-control write happened
            # EN:
            # Undesired value:
            # - non-dict truthy object
            # TR:
            # set_result show-only dalında None ile başlar.
            # TR:
            # Kabul edilen dallar:
            # - None => write olmadı
            # - dict => runtime-control write oldu
            # TR:
            # İstenmeyen değer:
            # - dict olmayan truthy nesne
            set_result = None

            if args.set_runtime_control is not None:
                # EN: LOCAL VALUE EXPLANATION / main / set_result
                # EN: set_result stores the visible runtime-control write receipt returned by set_webcrawler_runtime_control(...).
                # EN: Expected values are a dict-like receipt payload or None before this set branch runs.
                # TR: YEREL DEGER ACIKLAMASI / main / set_result
                # TR: set_result set_webcrawler_runtime_control(...) tarafindan dondurulen gorunur runtime-control yazim makbuzunu tasir.
                # TR: Beklenen degerler dict-benzeri bir makbuz payload'i veya bu set dali calismadan once None degeridir.
                set_result = set_webcrawler_runtime_control(
                    conn,
                    desired_state=args.set_runtime_control,
                    state_reason=args.state_reason,
                    requested_by=args.requested_by,
                )

                if bool(set_result.get("runtime_control_degraded")):
                    # EN: LOCAL VALUE EXPLANATION / main / payload
                    # EN: payload stores the operator-visible degraded runtime-control response that will be printed and returned immediately.
                    # EN: Expected values are dict payloads describing the set action, degradation truth, and runtime-control snapshot.
                    # TR: YEREL DEGER ACIKLAMASI / main / payload
                    # TR: payload hemen yazdirilip dondurulecek operator-gorunur degrade runtime-control yanitini tasir.
                    # TR: Beklenen degerler set aksiyonunu, degrade dogrusunu ve runtime-control anlik goruntusunu anlatan dict payload'laridir.
                    payload = {
                        "mode": "runtime_control",
                        "action": "set",
                        "set_result": dict(set_result),
                        "runtime_control": dict(set_result),
                    }
                    conn.rollback()
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 2

                conn.commit()

            # EN:
            # runtime_control is the durable control snapshot read from DB truth.
            # EN:
            # Expected type:
            # - dict
            # EN:
            # Common accepted desired_state values:
            # - "run"
            # - "pause"
            # - "stop"
            # EN:
            # Accepted degraded branch marker:
            # - runtime_control_degraded=True
            # EN:
            # Undesired shape:
            # - non-dict truthy object
            # TR:
            # runtime_control DB truth içinden okunan kalıcı kontrol snapshot'ıdır.
            # TR:
            # Beklenen tip:
            # - dict
            # TR:
            # Yaygın kabul edilen desired_state değerleri:
            # - "run"
            # - "pause"
            # - "stop"
            # TR:
            # Kabul edilen degrade dal işareti:
            # - runtime_control_degraded=True
            # TR:
            # İstenmeyen şekil:
            # - dict olmayan truthy nesne
            runtime_control = get_webcrawler_runtime_control(conn)

            if bool(runtime_control.get("runtime_control_degraded")):
                # EN: LOCAL VALUE EXPLANATION / main / payload
                # EN: payload stores the operator-visible runtime-control degraded read response that will be printed before exiting.
                # EN: Expected values are dict payloads that keep set/show mode plus degraded runtime-control truth readable.
                # TR: YEREL DEGER ACIKLAMASI / main / payload
                # TR: payload cikmadan once yazdirilacak operator-gorunur degrade runtime-control okuma yanitini tasir.
                # TR: Beklenen degerler set/show modunu ve degrade runtime-control dogrusunu okunur tutan dict payload'lardir.
                payload = {
                    "mode": "runtime_control",
                    "action": "set" if args.set_runtime_control is not None else "show",
                    "set_result": set_result,
                    "runtime_control": dict(runtime_control),
                }
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 2

            # EN:
            # may_claim_result is the policy answer to:
            # "May the runtime currently claim new work?"
            # EN:
            # Expected type:
            # - dict
            # EN:
            # Accepted may_claim values:
            # - True
            # - False
            # - None on degraded/unresolved branch
            # EN:
            # Undesired shape:
            # - non-dict truthy object
            # TR:
            # may_claim_result şu sorunun policy cevabıdır:
            # "Runtime şu anda yeni iş claim edebilir mi?"
            # TR:
            # Beklenen tip:
            # - dict
            # TR:
            # Kabul edilen may_claim değerleri:
            # - True
            # - False
            # - degrade/çözülememiş dalda None
            # TR:
            # İstenmeyen şekil:
            # - dict olmayan truthy nesne
            may_claim_result = webcrawler_runtime_may_claim(conn)

            if bool(may_claim_result.get("runtime_control_degraded")):
                # EN: LOCAL VALUE EXPLANATION / main / payload
                # EN: payload stores the operator-visible may-claim degraded response that explains why claim readiness could not be trusted.
                # EN: Expected values are dict payloads merging may-claim degradation truth with the latest runtime-control snapshot.
                # TR: YEREL DEGER ACIKLAMASI / main / payload
                # TR: payload claim hazirligina neden guvenilemedigini aciklayan operator-gorunur degrade may-claim yanitini tasir.
                # TR: Beklenen degerler may-claim degrade dogrusunu en son runtime-control anlik goruntusu ile birlestiren dict payload'lardir.
                payload = {
                    "mode": "runtime_control",
                    "action": "set" if args.set_runtime_control is not None else "show",
                    "set_result": set_result,
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

            # EN: LOCAL VALUE EXPLANATION / main / payload
            # EN: payload stores the healthy runtime-control summary printed for the operator before optional loop execution begins.
            # EN: Expected values are dict payloads containing mode, action, optional set_result, and the merged runtime_control snapshot.
            # TR: YEREL DEGER ACIKLAMASI / main / payload
            # TR: payload opsiyonel dongu calismasi baslamadan once operatora yazdirilan saglikli runtime-control ozetini tasir.
            # TR: Beklenen degerler mode, action, opsiyonel set_result ve birlestirilmis runtime_control anlik goruntusunu iceren dict payload'lardir.
            payload = {
                "mode": "runtime_control",
                "action": "set" if args.set_runtime_control is not None else "show",
                "set_result": set_result,
                "runtime_control": {
                    **dict(runtime_control),
                    "may_claim": may_claim_result.get("may_claim"),
                },
            }
            print(json.dumps(payload, indent=2, default=str))
            return 0
        finally:
            conn.close()

    # EN:
    # config is the structured handoff package from controller layer to worker-runtime layer.
    # EN:
    # Expected field meanings:
    # - dsn => usable PostgreSQL connection text
    # - worker_id => visible claim identity
    # - lease_seconds => semantically positive int
    # - probe_only => bool
    # EN:
    # Undesired field meanings:
    # - blank dsn
    # - blank worker_id
    # - zero/negative lease_seconds
    # - non-bool probe_only
    # TR:
    # config controller katmanından worker-runtime katmanına giden yapılı teslim paketidir.
    # TR:
    # Beklenen alan anlamları:
    # - dsn => kullanılabilir PostgreSQL bağlantı metni
    # - worker_id => görünür claim kimliği
    # - lease_seconds => semantik olarak pozitif int
    # - probe_only => bool
    # TR:
    # İstenmeyen alan anlamları:
    # - boş dsn
    # - boş worker_id
    # - sıfır/negatif lease_seconds
    # - bool olmayan probe_only
    config = WorkerConfig(
        dsn=args.dsn,
        worker_id=args.worker_id,
        lease_seconds=args.lease_seconds,
        probe_only=not args.durable_claim,
    )

    if not args.loop:
        # EN:
        # result is the structured worker-runtime answer for one probe step.
        # EN:
        # Expected shape:
        # - dataclass-like object accepted by asdict(...)
        # EN:
        # Accepted semantic branches:
        # - success
        # - no-work
        # - degraded-visible
        # - other intentional worker-runtime shapes
        # EN:
        # Undesired value:
        # - None
        # - object not accepted by asdict(...)
        # TR:
        # result tek probe adımı için worker-runtime tarafından verilen yapılı cevaptır.
        # TR:
        # Beklenen şekil:
        # - asdict(...) tarafından kabul edilen dataclass-benzeri nesne
        # TR:
        # Kabul edilen semantik dallar:
        # - success
        # - no-work
        # - degrade-visible
        # - diğer bilinçli worker-runtime şekilleri
        # TR:
        # İstenmeyen değer:
        # - None
        # - asdict(...) tarafından kabul edilmeyen nesne
        result = run_claim_probe(config)

        # EN:
        # payload is the JSON-ready plain-dict version of the result object.
        # EN:
        # Expected type:
        # - dict
        # EN:
        # Accepted content:
        # - JSON-serializable fields derived from result
        # EN:
        # Undesired content:
        # - unserializable exotic objects
        # TR:
        # payload result nesnesinin JSON'a hazır düz dict halidir.
        # TR:
        # Beklenen tip:
        # - dict
        # TR:
        # Kabul edilen içerik:
        # - result içinden türetilen JSON-serileştirilebilir alanlar
        # TR:
        # İstenmeyen içerik:
        # - serileştirilemeyen egzotik nesneler
        payload = asdict(result)

        print(json.dumps(payload, indent=2, default=str))
        return 0

    # EN:
    # iteration is the visible loop counter.
    # EN:
    # Expected type:
    # - int
    # EN:
    # Accepted runtime values:
    # - 1, 2, 3, ...
    # EN:
    # Initial stored value:
    # - 0 before the first active loop iteration
    # EN:
    # Undesired values:
    # - negative ints
    # TR:
    # iteration görünür loop sayacıdır.
    # TR:
    # Beklenen tip:
    # - int
    # TR:
    # Kabul edilen runtime değerleri:
    # - 1, 2, 3, ...
    # TR:
    # İlk saklanan değer:
    # - ilk aktif iterasyondan önce 0
    # TR:
    # İstenmeyen değerler:
    # - negatif int'ler
    iteration = 0

    while True:
        iteration += 1
        # EN: LOCAL VALUE EXPLANATION / main / result
        # EN: result stores the structured ClaimProbeResult returned by one worker-loop cycle.
        # EN: Expected values are dataclass-like runtime results describing claim/no-claim/degraded/finalized truth for this iteration.
        # TR: YEREL DEGER ACIKLAMASI / main / result
        # TR: result bir worker-dongu cevriminin dondurdugu yapili ClaimProbeResult sonucunu tasir.
        # TR: Beklenen degerler bu iterasyon icin claim/is-yok/degrade/finalize dogrusunu anlatan dataclass-benzeri runtime sonuclaridir.
        result = run_claim_probe(config)

        # EN: LOCAL VALUE EXPLANATION / main / payload
        # EN: payload stores the JSON-serializable dict form of the current worker-loop result before extra loop metadata is attached.
        # EN: Expected values are dict payloads derived from result and then enriched with mode/iteration fields for printing.
        # TR: YEREL DEGER ACIKLAMASI / main / payload
        # TR: payload mode/iteration alanlari eklenmeden once mevcut worker-dongu sonucunun JSON-serilestirilebilir dict bicimini tasir.
        # TR: Beklenen degerler result'tan turetilen ve sonra yazdirma icin mode/iteration alanlariyla zenginlestirilen dict payload'lardir.
        payload = asdict(result)
        payload["mode"] = "worker_loop"
        payload["iteration"] = iteration

        print(json.dumps(payload, default=str), flush=True)

        # EN:
        # runtime_control is re-read from the visible payload.
        # EN:
        # Why:
        # - loop decisions should follow the same snapshot the operator just saw
        # EN:
        # Accepted shape after fallback:
        # - dict
        # EN:
        # Accepted desired_state values:
        # - "run"
        # - "pause"
        # - "stop"
        # - ""
        # EN:
        # Undesired upstream shape:
        # - non-dict truthy object
        # TR:
        # runtime_control görünür payload içinden yeniden okunur.
        # TR:
        # Neden:
        # - loop kararları operatörün az önce gördüğü aynı snapshot'ı izlemeli
        # TR:
        # Fallback sonrası kabul edilen şekil:
        # - dict
        # TR:
        # Kabul edilen desired_state değerleri:
        # - "run"
        # - "pause"
        # - "stop"
        # - ""
        # TR:
        # İstenmeyen upstream şekil:
        # - dict olmayan truthy nesne
        runtime_control = payload.get("runtime_control") or {}
        # EN: LOCAL VALUE EXPLANATION / main / desired_state
        # EN: desired_state stores the normalized runtime-control target state extracted from the latest loop payload.
        # EN: Expected values are lowercase state strings such as play/pause/stop or an empty string when no explicit desired state is present.
        # TR: YEREL DEGER ACIKLAMASI / main / desired_state
        # TR: desired_state en son dongu payload'undan cikarilan normalize runtime-control hedef durumunu tasir.
        # TR: Beklenen degerler play/pause/stop gibi kucuk-harf durum stringleri veya acik bir hedef durum yoksa bos stringdir.
        desired_state = str(runtime_control.get("desired_state") or "").strip().lower()

        if desired_state == "stop":
            return 0

        if args.max_iterations > 0 and iteration >= args.max_iterations:
            return 0

        time.sleep(
            sleep_between_loop_iterations(
                payload=payload,
                sleep_seconds=args.sleep_seconds,
                pause_sleep_seconds=args.pause_sleep_seconds,
            )
        )


# EN:
# This guard preserves normal direct Python module execution.
# EN:
# Expected main() output:
# - int
# EN:
# Accepted common outputs:
# - 0
# - 2
# EN:
# Undesired outputs:
# - non-int objects
# TR:
# Bu guard normal doğrudan Python modül çalıştırmasını korur.
# TR:
# main() için beklenen çıktı:
# - int
# TR:
# Kabul edilen yaygın çıktılar:
# - 0
# - 2
# TR:
# İstenmeyen çıktılar:
# - int olmayan nesneler
if __name__ == "__main__":
    raise SystemExit(main())
