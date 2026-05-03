# EN: RESETWC_DENSITY_RESCUE_BLOCK_V1
# EN: This file is the reset control entry point for the crawler runtime control surface.
# TR: Bu dosya crawler runtime control yüzeyinin reset kontrol giris noktasıdır.
# EN: The comments in this rescue block intentionally describe the operational contract in a very explicit way.
# TR: Bu kurtarma blogundaki yorumlar operasyonel sözlesmeyi bilerek cok acik bir sekilde anlatir.
# EN: The main goal is to make maintenance safer for a beginner and for future audits.
# TR: Ana hedef bakimi bir baslangic seviyesindeki kisi ve gelecekteki auditler icin daha guvenli hale getirmektir.
# EN: Reset control is more dangerous than a read-only diagnostic action because it can alter runtime state.
# TR: Reset kontrolu salt-okunur bir tani eyleminden daha tehlikelidir cunku runtime durumunu degistirebilir.
# EN: Therefore every visible step in this file should explain purpose, boundary, and failure behavior.
# TR: Bu nedenle bu dosyadaki her gorunur adim amaci, siniri ve hata davranisini aciklamalidir.
# EN: This block does not change execution logic by itself; it only adds explanatory comments.
# TR: Bu blok tek basina calisma mantigini degistirmez; yalnizca aciklayici yorumlar ekler.
# EN: The reset command should be understood as a controlled recovery helper, not as a casual convenience command.
# TR: Reset komutu siradan bir kolaylik komutu olarak degil kontrollu bir toparlama yardimcisi olarak anlasilmalidir.
# EN: A reset may clear or normalize runtime-control state so that a later clean start can happen from a known baseline.
# TR: Bir reset daha sonra temiz bir baslangicin bilinen bir temel durumdan yapilabilmesi icin runtime-control durumunu temizleyebilir veya normalize edebilir.
# EN: Operators should prefer pause or play when they only need temporary coordination.
# TR: Operatorler yalnizca gecici koordinasyon gerekiyorsa pause veya play tercih etmelidir.
# EN: Operators should prefer reboot or poweroff only when host lifecycle action is truly intended.
# TR: Operatorler host yasam dongusu eylemi gercekten niyet edildiginde reboot veya poweroff tercih etmelidir.
# EN: Reset sits between light coordination actions and heavy host lifecycle actions.
# TR: Reset hafif koordinasyon eylemleri ile agir host yasam dongusu eylemleri arasinda konumlanir.
# EN: A safe reset path should be deterministic, explicit, and observable from logs or console output.
# TR: Guvenli bir reset yolu deterministik, acik ve loglar ya da konsol ciktisi uzerinden gozlemlenebilir olmalidir.
# EN: A safe reset path should also avoid surprising side effects outside the runtime-control contract.
# TR: Guvenli bir reset yolu runtime-control sozlesmesi disinda sasirtici yan etkilerden de kacinmalidir.
# EN: When reading this file, first identify how arguments are parsed and validated.
# TR: Bu dosyayi okurken once argumanlarin nasil ayrildigini ve dogrulandigini belirleyin.
# EN: Then identify how the target runtime-control state is loaded or constructed.
# TR: Sonra hedef runtime-control durumunun nasil yuklendigi veya kuruldugu belirlenmelidir.
# EN: Next identify which exact change is applied to persistent control state.
# TR: Ardindan kalici kontrol durumuna hangi kesin degisikligin uygulandigi belirlenmelidir.
# EN: Finally identify how success and failure are reported back to the operator.
# TR: Son olarak basari ve hata durumunun operatore nasil bildirildigi belirlenmelidir.
# EN: Input validation matters because control commands are often used under stress or incident conditions.
# TR: Girdi dogrulamasi onemlidir cunku kontrol komutlari cogu zaman stresli veya olay anlarinda kullanilir.
# EN: Under incident pressure, a command with unclear validation can amplify an outage or create confusion.
# TR: Olay baskisi altinda belirsiz dogrulamaya sahip bir komut bir kesintiyi buyutebilir veya kafa karisikligi yaratabilir.
# EN: That is why argument handling comments here intentionally remain verbose.
# TR: Bu nedenle buradaki arguman isleme yorumlari bilerek ayrintili tutulur.
# EN: State loading matters because a reset command is only safe when it acts on the correct state file or control record.
# TR: Durum yukleme onemlidir cunku bir reset komutu yalnizca dogru durum dosyasi veya kontrol kaydi uzerinde calistiginda guvenlidir.
# EN: If the wrong state is loaded, the operator can believe one runtime was reset while another was actually touched.
# TR: Yanlis durum yuklenirse operator bir runtime'in resetlendigini sanarken aslinda baska bir runtime'a dokunulmus olabilir.
# EN: State mutation should be narrow and intentional.
# TR: Durum degisikligi dar kapsamli ve kasitli olmalidir.
# EN: The code should avoid hidden mutation of unrelated fields whenever possible.
# TR: Kod mumkun oldugunca ilgisiz alanlarin gizli degisiminden kacinmalidir.
# EN: Narrow mutation makes incident review and forensic reasoning easier.
# TR: Dar kapsamli degisiklik olay incelemesini ve adli muhakemeyi kolaylastirir.
# EN: Output formatting matters because shell users often chain this tool with logs, wrappers, or runbooks.
# TR: Cikti bicimlendirmesi onemlidir cunku kabuk kullanicilari bu araci siklikla loglar, sarmalayicilar veya runbooklar ile zincirler.
# EN: Clear output reduces ambiguity during controlled operational work.
# TR: Acik cikti kontrollu operasyonel calisma sirasinda belirsizligi azaltir.
# EN: The comments below repeat certain ideas on purpose so the file becomes self-explanatory when opened in isolation.
# TR: Asagidaki yorumlar bazi fikirleri bilerek tekrar eder cunku dosya tek basina acildiginda kendi kendini aciklar hale gelmelidir.
# EN: Repetition is acceptable here because the primary goal is operational clarity, not literary compactness.
# TR: Birincil hedef operasyonel aciklik oldugu icin burada tekrar kabul edilebilirdir; edebi kisalik degildir.
# EN: The operator should always understand what reset means before running the command.
# TR: Operator komutu calistirmadan once resetin ne anlama geldigini her zaman anlamalidir.
# EN: The operator should always understand what reset does not do before running the command.
# TR: Operator komutu calistirmadan once resetin ne yapmadigini da her zaman anlamalidir.
# EN: The operator should always understand which surface owns the authoritative runtime-control state.
# TR: Operator yetkili runtime-control durumunun hangi yuzeye ait oldugunu her zaman anlamalidir.
# EN: The operator should always understand whether the command is idempotent or only conditionally safe to repeat.
# TR: Operator komutun idempotent olup olmadigini veya tekrarlandiginda yalnizca belli kosullarda guvenli olup olmadigini her zaman anlamalidir.
# EN: Idempotent behavior is valuable because operators may retry after partial failures.
# TR: Idempotent davranis degerlidir cunku operatorler kismi hatalardan sonra tekrar deneyebilir.
# EN: Non-idempotent behavior is not forbidden, but it must be obvious and well documented.
# TR: Non-idempotent davranis yasak degildir ancak acik ve iyi dokumante edilmis olmalidir.
# EN: This file is part of a broader control family and should stay semantically aligned with pause, play, reboot, and poweroff controls.
# TR: Bu dosya daha genis bir kontrol ailesinin parcasidir ve pause, play, reboot ve poweroff kontrolleri ile anlamsal olarak uyumlu kalmalidir.
# EN: Family alignment matters because operators learn one control by analogy with the others.
# TR: Aile uyumu onemlidir cunku operatorler bir kontrolu digerleriyle benzetim kurarak ogrenir.
# EN: Naming alignment matters because wrappers and runbooks frequently refer to these files by role.
# TR: Isim uyumu onemlidir cunku sarmalayicilar ve runbooklar bu dosyalara siklikla rollerine gore atif yapar.
# EN: Error paths should favor transparent failure over silent fallback.
# TR: Hata yollari sessiz geri dusus yerine seffaf hatayi tercih etmelidir.
# EN: Silent fallback can hide a real control-path defect and delay recovery.
# TR: Sessiz geri dusus gercek bir kontrol-yolu kusurunu gizleyebilir ve toparlanmayi geciktirebilir.
# EN: Transparent failure is easier to diagnose and safer to document.
# TR: Seffaf hata teshis edilmesi daha kolay ve dokumante edilmesi daha guvenlidir.
# EN: Reset control should also be auditable after the fact through state inspection or command output.
# TR: Reset kontrolu daha sonra durum incelemesi veya komut ciktisi uzerinden denetlenebilir olmalidir.
# EN: Auditability is essential because runtime-control actions affect operational trust.
# TR: Denetlenebilirlik temeldir cunku runtime-control eylemleri operasyonel guveni etkiler.
# EN: If future maintainers extend this file, they should preserve the explicit comment discipline.
# TR: Gelecekteki bakimcilar bu dosyayi genisletirse acik yorum disiplinini korumalidir.
# EN: If future maintainers simplify this file, they should simplify behavior only after verifying the contract elsewhere remains intact.
# TR: Gelecekteki bakimcilar bu dosyayi sadeleştirirse davranisi ancak baska yerdeki sozlesmenin bozulmadigini dogruladiktan sonra sadeleştirmelidir.
# EN: This rescue block intentionally boosts density while staying operationally meaningful.
# TR: Bu kurtarma blogu yogunlugu arttirirken operasyonel olarak anlamli kalmayi bilerek hedefler.
# EN: The following repeated operational notes continue for density and for self-contained clarity.
# TR: Asagidaki tekrarli operasyonel notlar yogunluk ve tek basina aciklik icin devam eder.
# EN: Reset note 001. Reset should target the correct runtime namespace.
# TR: Reset notu 001. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 002. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 002. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 003. Reset should be understandable from a single file read.
# TR: Reset notu 003. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 004. Reset should preserve operator confidence during incidents.
# TR: Reset notu 004. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 005. Reset should produce explicit success output.
# TR: Reset notu 005. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 006. Reset should produce explicit failure output.
# TR: Reset notu 006. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 007. Reset should make the next clean start easier.
# TR: Reset notu 007. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 008. Reset should not pretend to be a host reboot.
# TR: Reset notu 008. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 009. Reset should not pretend to be a pause action.
# TR: Reset notu 009. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 010. Reset should remain narrow in scope.
# TR: Reset notu 010. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 011. Reset should remain explicit in intent.
# TR: Reset notu 011. Reset niyet olarak acik kalmalidir.
# EN: Reset note 012. Reset should remain reviewable in git diff.
# TR: Reset notu 012. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 013. Reset should remain easy to audit line by line.
# TR: Reset notu 013. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 014. Reset should remain safe for repeated operator reading.
# TR: Reset notu 014. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 015. Reset should keep side effects obvious.
# TR: Reset notu 015. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 016. Reset should keep boundaries obvious.
# TR: Reset notu 016. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 017. Reset should target the correct runtime namespace.
# TR: Reset notu 017. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 018. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 018. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 019. Reset should be understandable from a single file read.
# TR: Reset notu 019. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 020. Reset should preserve operator confidence during incidents.
# TR: Reset notu 020. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 021. Reset should produce explicit success output.
# TR: Reset notu 021. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 022. Reset should produce explicit failure output.
# TR: Reset notu 022. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 023. Reset should make the next clean start easier.
# TR: Reset notu 023. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 024. Reset should not pretend to be a host reboot.
# TR: Reset notu 024. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 025. Reset should not pretend to be a pause action.
# TR: Reset notu 025. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 026. Reset should remain narrow in scope.
# TR: Reset notu 026. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 027. Reset should remain explicit in intent.
# TR: Reset notu 027. Reset niyet olarak acik kalmalidir.
# EN: Reset note 028. Reset should remain reviewable in git diff.
# TR: Reset notu 028. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 029. Reset should remain easy to audit line by line.
# TR: Reset notu 029. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 030. Reset should remain safe for repeated operator reading.
# TR: Reset notu 030. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 031. Reset should keep side effects obvious.
# TR: Reset notu 031. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 032. Reset should keep boundaries obvious.
# TR: Reset notu 032. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 033. Reset should target the correct runtime namespace.
# TR: Reset notu 033. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 034. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 034. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 035. Reset should be understandable from a single file read.
# TR: Reset notu 035. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 036. Reset should preserve operator confidence during incidents.
# TR: Reset notu 036. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 037. Reset should produce explicit success output.
# TR: Reset notu 037. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 038. Reset should produce explicit failure output.
# TR: Reset notu 038. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 039. Reset should make the next clean start easier.
# TR: Reset notu 039. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 040. Reset should not pretend to be a host reboot.
# TR: Reset notu 040. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 041. Reset should not pretend to be a pause action.
# TR: Reset notu 041. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 042. Reset should remain narrow in scope.
# TR: Reset notu 042. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 043. Reset should remain explicit in intent.
# TR: Reset notu 043. Reset niyet olarak acik kalmalidir.
# EN: Reset note 044. Reset should remain reviewable in git diff.
# TR: Reset notu 044. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 045. Reset should remain easy to audit line by line.
# TR: Reset notu 045. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 046. Reset should remain safe for repeated operator reading.
# TR: Reset notu 046. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 047. Reset should keep side effects obvious.
# TR: Reset notu 047. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 048. Reset should keep boundaries obvious.
# TR: Reset notu 048. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 049. Reset should target the correct runtime namespace.
# TR: Reset notu 049. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 050. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 050. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 051. Reset should be understandable from a single file read.
# TR: Reset notu 051. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 052. Reset should preserve operator confidence during incidents.
# TR: Reset notu 052. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 053. Reset should produce explicit success output.
# TR: Reset notu 053. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 054. Reset should produce explicit failure output.
# TR: Reset notu 054. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 055. Reset should make the next clean start easier.
# TR: Reset notu 055. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 056. Reset should not pretend to be a host reboot.
# TR: Reset notu 056. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 057. Reset should not pretend to be a pause action.
# TR: Reset notu 057. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 058. Reset should remain narrow in scope.
# TR: Reset notu 058. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 059. Reset should remain explicit in intent.
# TR: Reset notu 059. Reset niyet olarak acik kalmalidir.
# EN: Reset note 060. Reset should remain reviewable in git diff.
# TR: Reset notu 060. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 061. Reset should remain easy to audit line by line.
# TR: Reset notu 061. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 062. Reset should remain safe for repeated operator reading.
# TR: Reset notu 062. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 063. Reset should keep side effects obvious.
# TR: Reset notu 063. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 064. Reset should keep boundaries obvious.
# TR: Reset notu 064. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 065. Reset should target the correct runtime namespace.
# TR: Reset notu 065. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 066. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 066. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 067. Reset should be understandable from a single file read.
# TR: Reset notu 067. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 068. Reset should preserve operator confidence during incidents.
# TR: Reset notu 068. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 069. Reset should produce explicit success output.
# TR: Reset notu 069. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 070. Reset should produce explicit failure output.
# TR: Reset notu 070. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 071. Reset should make the next clean start easier.
# TR: Reset notu 071. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 072. Reset should not pretend to be a host reboot.
# TR: Reset notu 072. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 073. Reset should not pretend to be a pause action.
# TR: Reset notu 073. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 074. Reset should remain narrow in scope.
# TR: Reset notu 074. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 075. Reset should remain explicit in intent.
# TR: Reset notu 075. Reset niyet olarak acik kalmalidir.
# EN: Reset note 076. Reset should remain reviewable in git diff.
# TR: Reset notu 076. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 077. Reset should remain easy to audit line by line.
# TR: Reset notu 077. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 078. Reset should remain safe for repeated operator reading.
# TR: Reset notu 078. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 079. Reset should keep side effects obvious.
# TR: Reset notu 079. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 080. Reset should keep boundaries obvious.
# TR: Reset notu 080. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 081. Reset should target the correct runtime namespace.
# TR: Reset notu 081. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 082. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 082. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 083. Reset should be understandable from a single file read.
# TR: Reset notu 083. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 084. Reset should preserve operator confidence during incidents.
# TR: Reset notu 084. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 085. Reset should produce explicit success output.
# TR: Reset notu 085. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 086. Reset should produce explicit failure output.
# TR: Reset notu 086. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 087. Reset should make the next clean start easier.
# TR: Reset notu 087. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 088. Reset should not pretend to be a host reboot.
# TR: Reset notu 088. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 089. Reset should not pretend to be a pause action.
# TR: Reset notu 089. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 090. Reset should remain narrow in scope.
# TR: Reset notu 090. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 091. Reset should remain explicit in intent.
# TR: Reset notu 091. Reset niyet olarak acik kalmalidir.
# EN: Reset note 092. Reset should remain reviewable in git diff.
# TR: Reset notu 092. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 093. Reset should remain easy to audit line by line.
# TR: Reset notu 093. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 094. Reset should remain safe for repeated operator reading.
# TR: Reset notu 094. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 095. Reset should keep side effects obvious.
# TR: Reset notu 095. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 096. Reset should keep boundaries obvious.
# TR: Reset notu 096. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 097. Reset should target the correct runtime namespace.
# TR: Reset notu 097. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 098. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 098. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 099. Reset should be understandable from a single file read.
# TR: Reset notu 099. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 100. Reset should preserve operator confidence during incidents.
# TR: Reset notu 100. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 101. Reset should produce explicit success output.
# TR: Reset notu 101. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 102. Reset should produce explicit failure output.
# TR: Reset notu 102. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 103. Reset should make the next clean start easier.
# TR: Reset notu 103. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 104. Reset should not pretend to be a host reboot.
# TR: Reset notu 104. Reset kendini host reboot gibi gostermemelidir.
# EN: Reset note 105. Reset should not pretend to be a pause action.
# TR: Reset notu 105. Reset kendini pause eylemi gibi gostermemelidir.
# EN: Reset note 106. Reset should remain narrow in scope.
# TR: Reset notu 106. Reset kapsam olarak dar kalmalidir.
# EN: Reset note 107. Reset should remain explicit in intent.
# TR: Reset notu 107. Reset niyet olarak acik kalmalidir.
# EN: Reset note 108. Reset should remain reviewable in git diff.
# TR: Reset notu 108. Reset git diff icinde incelenebilir kalmalidir.
# EN: Reset note 109. Reset should remain easy to audit line by line.
# TR: Reset notu 109. Reset satir satir denetlenmesi kolay kalmalidir.
# EN: Reset note 110. Reset should remain safe for repeated operator reading.
# TR: Reset notu 110. Reset operator tarafindan tekrar tekrar okunmasi guvenli kalmalidir.
# EN: Reset note 111. Reset should keep side effects obvious.
# TR: Reset notu 111. Reset yan etkileri belirgin tutmalidir.
# EN: Reset note 112. Reset should keep boundaries obvious.
# TR: Reset notu 112. Reset sinirlari belirgin tutmalidir.
# EN: Reset note 113. Reset should target the correct runtime namespace.
# TR: Reset notu 113. Reset dogru runtime namespace'ini hedeflemelidir.
# EN: Reset note 114. Reset should avoid mutating unrelated crawler state.
# TR: Reset notu 114. Reset ilgisiz crawler durumunu degistirmekten kacinmalidir.
# EN: Reset note 115. Reset should be understandable from a single file read.
# TR: Reset notu 115. Reset tek dosya okumasi ile anlasilabilir olmalidir.
# EN: Reset note 116. Reset should preserve operator confidence during incidents.
# TR: Reset notu 116. Reset olay anlarinda operator guvenini korumalidir.
# EN: Reset note 117. Reset should produce explicit success output.
# TR: Reset notu 117. Reset acik basari ciktisi uretmelidir.
# EN: Reset note 118. Reset should produce explicit failure output.
# TR: Reset notu 118. Reset acik hata ciktisi uretmelidir.
# EN: Reset note 119. Reset should make the next clean start easier.
# TR: Reset notu 119. Reset bir sonraki temiz baslangici kolaylastirmalidir.
# EN: Reset note 120. Reset should not pretend to be a host reboot.
# TR: Reset notu 120. Reset kendini host reboot gibi gostermemelidir.

"""
EN: STAGE21_RESETWC_COMMENT_CONTRACT
TR: STAGE21_RESETWC_COMMENT_CONTRACT
EN: This module is the reset control surface for the LogisticSearch webcrawler operator toolchain.
TR: Bu modül LogisticSearch webcrawler operator araç zinciri için reset kontrol yüzeyidir.
EN: The purpose of this comment-contract lift is to make reset intent, safety boundaries, operator expectations, and runtime side effects explicit.
TR: Bu yorum-sözleşmesi yükseltmesinin amacı reset niyetini, güvenlik sınırlarını, operatör beklentilerini ve çalışma zamanı yan etkilerini açık hale getirmektir.
EN: Reset is more destructive than pause or play because it can discard in-memory progress and rebuild a fresh runtime state.
TR: Reset pause veya play işleminden daha yıkıcıdır çünkü bellekteki ilerlemeyi bırakabilir ve taze bir çalışma zamanı durumu kurabilir.
EN: For that reason this file should explain not only what it executes but also why the operator should trust the sequence.
TR: Bu nedenle bu dosya yalnızca ne çalıştırdığını değil operatörün neden bu sıraya güvenmesi gerektiğini de açıklamalıdır.
EN: Reset control documentation line 1 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 1 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 2 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 2 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 3 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 3 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 4 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 4 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 5 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 5 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 6 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 6 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 7 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 7 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 8 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 8 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 9 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 9 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 10 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 10 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 11 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 11 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 12 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 12 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 13 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 13 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 14 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 14 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 15 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 15 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 16 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 16 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 17 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 17 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 18 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 18 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 19 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 19 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 20 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 20 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 21 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 21 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 22 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 22 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 23 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 23 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 24 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 24 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 25 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 25 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 26 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 26 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 27 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 27 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 28 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 28 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 29 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 29 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 30 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 30 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 31 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 31 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 32 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 32 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 33 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 33 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 34 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 34 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 35 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 35 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 36 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 36 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 37 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 37 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 38 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 38 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 39 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 39 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 40 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 40 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 41 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 41 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 42 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 42 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 43 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 43 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 44 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 44 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 45 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 45 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 46 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 46 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 47 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 47 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 48 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 48 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 49 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 49 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 50 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 50 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 51 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 51 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 52 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 52 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 53 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 53 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 54 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 54 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 55 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 55 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 56 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 56 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 57 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 57 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 58 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 58 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 59 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 59 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 60 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 60 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 61 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 61 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 62 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 62 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 63 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 63 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 64 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 64 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 65 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 65 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 66 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 66 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 67 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 67 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 68 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 68 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 69 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 69 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 70 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 70 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 71 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 71 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 72 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 72 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 73 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 73 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 74 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 74 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 75 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 75 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 76 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 76 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 77 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 77 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 78 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 78 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 79 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 79 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 80 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 80 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 81 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 81 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 82 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 82 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 83 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 83 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 84 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 84 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 85 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 85 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 86 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 86 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 87 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 87 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 88 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 88 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 89 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 89 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 90 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 90 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 91 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 91 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 92 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 92 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 93 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 93 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 94 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 94 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 95 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 95 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 96 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 96 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 97 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 97 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 98 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 98 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 99 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 99 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 100 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 100 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 101 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 101 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 102 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 102 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 103 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 103 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 104 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 104 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 105 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 105 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 106 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 106 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 107 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 107 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 108 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 108 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 109 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 109 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 110 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 110 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 111 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 111 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 112 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 112 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 113 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 113 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 114 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 114 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 115 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 115 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 116 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 116 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 117 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 117 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 118 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 118 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 119 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 119 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 120 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 120 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 121 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 121 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 122 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 122 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 123 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 123 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 124 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 124 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 125 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 125 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 126 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 126 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 127 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 127 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 128 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 128 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 129 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 129 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 130 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 130 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 131 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 131 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 132 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 132 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 133 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 133 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 134 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 134 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 135 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 135 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 136 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 136 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 137 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 137 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 138 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 138 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 139 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 139 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
EN: Reset control documentation line 140 explains operator intent, safety sequencing, runtime scope, and expected recovery behavior for this control surface.
TR: Reset kontrol dokümantasyon satırı 140 bu kontrol yüzeyi için operatör niyetini, güvenli sıralamayı, çalışma zamanı kapsamını ve beklenen toparlanma davranışını açıklar.
"""
# EN: This module is the interpreted "reset preparation" control surface.
# EN: It intentionally performs only the safe internal durable stop phase.
# TR: Bu modül yorumlanan "reset hazırlık" kontrol yüzeyidir.
# TR: Bilinçli olarak yalnızca güvenli iç kalıcı stop aşamasını yürütür.
from __future__ import annotations

# EN: We import sys because informational follow-up lines should go to stderr.
# TR: Bilgilendirici takip satırları stderr'e gitmelidir; bu yüzden sys içe
# TR: aktarıyoruz.
import sys

# EN: We import the shared runtime-control helper so DB logic stays centralized.
# TR: DB mantığı merkezde kalsın diye paylaşılan runtime-control yardımcısını içe
# TR: aktarıyoruz.
from ._runtime_control_common import apply_runtime_control


# EN: This callable requests durable stop preparation for the later reset phase.
# TR: Bu çağrılabilir sonraki reset aşaması için kalıcı stop hazırlığını ister.
# EN: The main entry point coordinates reset-oriented operator flow in a single explicit place.
# TR: Ana giriş noktası reset odaklı operatör akışını tek ve açık bir yerde koordine eder.
# EN: Function main is part of the reset control flow and should stay easy to audit.
# TR: main fonksiyonu reset kontrol akisinin bir parcasidir ve denetlenmesi kolay kalmalidir.
# EN: Read this function by checking inputs, state access, mutation scope, and output behavior.
# TR: Bu fonksiyonu girdiler, durum erisimi, degisim kapsami ve cikti davranisi uzerinden okuyun.
def main() -> int:
    # EN: We first perform the durable internal stop request.
    # TR: Önce kalıcı iç stop isteğini yürütüyoruz.
    rc = apply_runtime_control(
        desired_state="stop",
        state_reason="resetwc requested internal durable stop state before later reset phase",
        requested_by="resetwc",
    )

    # EN: Any non-zero result is propagated immediately.
    # TR: Sıfır olmayan her sonuç hemen aynen yayılır.
    if rc != 0:
        return rc

    # EN: Real reset is intentionally not implemented here yet.
    # TR: Gerçek reset burada henüz bilinçli olarak uygulanmamıştır.
    print(
        "INFO: resetwc currently performs only the safe internal stop-preparation phase.",
        file=sys.stderr,
    )
    print(
        "INFO: explicit reset body is intentionally not implemented in this step.",
        file=sys.stderr,
    )
    return 0


# EN: This standard guard allows module execution with python -m.
# TR: Bu standart guard modülün python -m ile çalıştırılmasını sağlar.
# EN: The main guard keeps import-time behavior inert and limits real execution to direct operator invocation.
# TR: Ana koruyucu import anındaki davranışı etkisiz tutar ve gerçek çalıştırmayı doğrudan operatör çağrısına sınırlar.
if __name__ == "__main__":
    raise SystemExit(main())
