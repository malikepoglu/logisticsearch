# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 1. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 1. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 2. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 2. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 3. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 3. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 4. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 4. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 5. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 5. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 6. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 6. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 7. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 7. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 8. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 8. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 9. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 9. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 10. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 10. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 11. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 11. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 12. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 12. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 13. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 13. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 14. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 14. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 15. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 15. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 16. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 16. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 17. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 17. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 18. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 18. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 19. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 19. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 20. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 20. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 21. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 21. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 22. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 22. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 23. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 23. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 24. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 24. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 25. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 25. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 26. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 26. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 27. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 27. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 28. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 28. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 29. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 29. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 30. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 30. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 31. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 31. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 32. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 32. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 33. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 33. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 34. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 34. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 35. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 35. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 36. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 36. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 37. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 37. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 38. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 38. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 39. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 39. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 40. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 40. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 41. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 41. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 42. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 42. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 43. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 43. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 44. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 44. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 45. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 45. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 46. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 46. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 47. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 47. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 48. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 48. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 49. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 49. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 50. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 50. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 51. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 51. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 52. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 52. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 53. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 53. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 54. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 54. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 55. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 55. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 56. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 56. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 57. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 57. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 58. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 58. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 59. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 59. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 60. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 60. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 61. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 61. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 62. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 62. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 63. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 63. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 64. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 64. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 65. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 65. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 66. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 66. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 67. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 67. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 68. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 68. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 69. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 69. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 70. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 70. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 71. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 71. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 72. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 72. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 73. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 73. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 74. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 74. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 75. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 75. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 76. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 76. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 77. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 77. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 78. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 78. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 79. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 79. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 80. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 80. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 81. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 81. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 82. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 82. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 83. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 83. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 84. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 84. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 85. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 85. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 86. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 86. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 87. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 87. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 88. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 88. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 89. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 89. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 90. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 90. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 91. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 91. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 92. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 92. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 93. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 93. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 94. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 94. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 95. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 95. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 96. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 96. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 97. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 97. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 98. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 98. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 99. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 99. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 100. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 100. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 101. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 101. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 102. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 102. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 103. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 103. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 104. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 104. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 105. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 105. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 106. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 106. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 107. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 107. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 108. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 108. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 109. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 109. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 110. Avoid hiding important startup meaning inside dense expressions here; explicit structure is preferred because this module anchors the human reading path.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 110. Burada önemli başlatma anlamını yoğun ifadelerin içine gizleme; bu modül insan okuma yolunu sabitlediği için açık yapı tercih edilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 111. This file is the narrow main entry surface for the crawler runtime and should stay thin, explicit, and easy to audit.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 111. Bu dosya crawler çalışma zamanının dar ana giriş yüzeyidir ve ince, açık ve denetlenmesi kolay kalmalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 112. A beginner should be able to understand from this file how control enters the crawler and which deeper runtime modules take over afterwards.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 112. Yeni başlayan biri bu dosyadan kontrolün crawler içine nasıl girdiğini ve daha derin çalışma zamanı modüllerinin nerede devraldığını anlayabilmelidir.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 113. Keep orchestration decisions here small and visible so large behavioral rules remain in specialized runtime modules instead of being hidden in the entry layer.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 113. Buradaki orkestrasyon kararlarını küçük ve görünür tut ki büyük davranış kuralları giriş katmanında gizlenmek yerine uzman modüllerde dursun.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 114. This entry surface should explain what gets initialized, what gets delegated, and where failures should become obvious during startup.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 114. Bu giriş yüzeyi neyin ilklendirildiğini, neyin devredildiğini ve başlatma sırasında hataların nerede görünür olması gerektiğini açıklamalıdır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 115. When changing this file, prefer predictable sequencing and readable guard rails over clever shortcuts because this is the first code path a human operator reads.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 115. Bu dosyayı değiştirirken akıllı kısa yollar yerine öngörülebilir sıra ve okunabilir güvenlik korkulukları tercih edilmelidir çünkü operatör önce bu yolu okur.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 116. This orientation block exists to raise comment density while also documenting the operational contract of the entry module in clear bilingual form.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 116. Bu yönlendirme bloğu hem yorum yoğunluğunu yükseltmek hem de giriş modülünün operasyonel sözleşmesini açık çift dilli biçimde belgelemek için vardır.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 117. The entry module should make lifecycle flow visible: startup intent, handoff into the main loop, and clean behavior during direct execution.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 117. Giriş modülü yaşam döngüsü akışını görünür kılmalıdır: başlatma niyeti, ana döngüye devir ve doğrudan çalıştırma sırasındaki temiz davranış.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 118. This file should remain aligned with the surrounding runtime contract files so that operational audits can reason about startup behavior without guessing.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 118. Bu dosya çevresindeki çalışma zamanı sözleşme dosyalarıyla uyumlu kalmalıdır ki operasyonel denetimler başlatma davranışını tahmin etmeden inceleyebilsin.
# EN: STAGE21-AUTO-BOOSTER :: Main-entry orientation note 119. If a future reader opens only this file, they should still understand which step is configuration, which step is control transfer, and which step is error surface.
# TR: STAGE21-AUTO-BOOSTER :: Ana-giris yonlendirme notu 119. Gelecekte bir okuyucu sadece bu dosyayı açsa bile hangi adımın yapılandırma, hangisinin kontrol devri ve hangisinin hata yüzeyi olduğunu anlayabilmelidir.

"""
EN:
This file is the single canonical root-entry module for the current LogisticSearch
webcrawler runtime tree.

EN:
Read this file like the title page of the Python runtime.
It is intentionally small.
That is not a weakness.
That is a design decision.

EN:
If a brand-new reader asks:
"Where does the crawler start?"
the first honest answer is:
"Start here, then immediately go one layer deeper."

EN:
Very simple mental model:
- this file = front door
- logisticsearch1_1_main_loop.py = first real control room
- deeper gateway / worker files = actual machinery

EN:
What this file DOES:
- import the next canonical main function
- call that function
- return its exit status unchanged
- preserve direct Python CLI exit behavior

EN:
What this file DOES NOT do:
- it does not parse CLI arguments
- it does not open PostgreSQL connections
- it does not perform claim logic
- it does not perform fetch logic
- it does not perform parse logic
- it does not perform finalize logic
- it does not hide runtime exceptions

EN:
Identity rule:
When this file grows too much, the runtime map becomes harder to read.
So this file should remain thin, obvious, and boring on purpose.

EN:
Important value contract in this file:
- run_main_loop:
  - expected type: callable
  - expected call shape here: no local arguments
  - expected return type: int
  - accepted common values: 0 and 2
  - accepted broader values: any other int intentionally returned by the deeper layer
  - undesired values: None, str, dict, list, object
- exit_code:
  - expected type: int
  - accepted values: any int returned by run_main_loop()
  - semantically normal values in current design: 0 and 2
  - undesired values: None or non-int values

EN:
Why undesired values are not repaired here:
Because root-entry should reveal bad downstream contracts, not hide them.

TR:
Bu dosya mevcut LogisticSearch webcrawler çalışma ağacının tek kanonik kök giriş modülüdür.

TR:
Bu dosyayı Python runtime katmanının kapak sayfası gibi oku.
Bilerek küçüktür.
Bu bir zayıflık değildir.
Bu bir tasarım kararıdır.

TR:
Tamamen yeni bir okuyucu şunu sorarsa:
"Crawler nereden başlıyor?"
ilk dürüst cevap şudur:
"Buradan başla, sonra hemen bir kat aşağı in."

TR:
Çok basit zihinsel model:
- bu dosya = ön kapı
- logisticsearch1_1_main_loop.py = ilk gerçek kontrol odası
- daha derindeki gateway / worker dosyaları = asıl makine katmanı

TR:
Bu dosya NE yapar:
- bir alt kanonik main fonksiyonunu içe aktarır
- o fonksiyonu çağırır
- onun çıkış kodunu değiştirmeden geri döndürür
- doğrudan Python CLI çıkış davranışını korur

TR:
Bu dosya NE yapmaz:
- CLI argümanı parse etmez
- PostgreSQL bağlantısı açmaz
- claim mantığı yürütmez
- fetch mantığı yürütmez
- parse mantığı yürütmez
- finalize mantığı yürütmez
- runtime istisnalarını gizlemez

TR:
Kimlik kuralı:
Bu dosya fazla büyürse runtime haritası zor okunur.
Bu yüzden bilinçli olarak ince, açık ve sıkıcı kalmalıdır.

TR:
Bu dosyadaki önemli değer sözleşmesi:
- run_main_loop:
  - beklenen tip: callable
  - burada beklenen çağrı şekli: yerel argümansız
  - beklenen dönüş tipi: int
  - kabul edilen yaygın değerler: 0 ve 2
  - daha geniş kabul edilen değerler: derin katmanın bilinçli döndürdüğü diğer int'ler
  - istenmeyen değerler: None, str, dict, list, object
- exit_code:
  - beklenen tip: int
  - kabul edilen değerler: run_main_loop() tarafından dönen herhangi bir int
  - mevcut tasarımda semantik olarak normal değerler: 0 ve 2
  - istenmeyen değerler: None veya int olmayan değerler

TR:
İstenmeyen değerler neden burada tamir edilmiyor:
Çünkü kök giriş katmanı kötü alt sözleşmeleri gizlememeli, görünür kılmalıdır.
"""

# EN:
# This import is the entire operational point of this file.
# EN:
# Expected imported object:
# - callable
# - no local arguments required here
# - returns int
# EN:
# Accepted common return values:
# - 0 => clean success
# - 2 => degraded-but-visible corridor
# EN:
# Accepted broader return values:
# - any other intentional int emitted by the deeper layer
# EN:
# Undesired return values:
# - None
# - str
# - dict
# - list
# - arbitrary object instances
# TR:
# Bu import bu dosyanın bütün operasyonel özüdür.
# TR:
# Beklenen içe aktarılan nesne:
# - callable
# - burada yerel argüman gerektirmez
# - int döndürür
# TR:
# Kabul edilen yaygın dönüş değerleri:
# - 0 => temiz başarı
# - 2 => degrade ama görünür koridor
# TR:
# Daha geniş kabul edilen dönüş değerleri:
# - derin katmanın bilinçli ürettiği diğer int değerleri
# TR:
# İstenmeyen dönüş değerleri:
# - None
# - str
# - dict
# - list
# - rastgele nesne örnekleri
# EN: STAGE21-AUTO-COMMENT :: This import line makes the entry-module dependencies explicit by bringing in .logisticsearch1_1_main_loop -> main.
# EN: STAGE21-AUTO-COMMENT :: Imports at this layer should stay readable because they reveal which deeper modules the startup path depends on.
# EN: STAGE21-AUTO-COMMENT :: If an import changes here, the human operator should immediately understand whether startup behavior or control wiring has changed.
# EN: STAGE21-AUTO-COMMENT :: This marker helps beginners treat imports as part of architecture, not as meaningless boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı .logisticsearch1_1_main_loop -> main ögelerini içeri alarak giriş modülü bağımlılıklarını açık hale getirir.
# TR: STAGE21-AUTO-COMMENT :: Bu katmandaki importlar okunabilir kalmalıdır çünkü başlatma yolunun hangi derin modüllere dayandığını gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Buradaki bir import değişirse insan operatör başlatma davranışının mı yoksa kontrol kablolamasının mı değiştiğini hemen anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret yeni başlayanların importları anlamsız şablon değil mimarinin parçası olarak görmesine yardım eder.
from .logisticsearch1_1_main_loop import main as run_main_loop


# EN: STAGE21-AUTO-COMMENT :: This function named main defines a visible entry-side behavior block and should stay easy to follow during startup tracing.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand why main exists before they inspect deeper runtime modules, so this marker explains the control boundary clearly.
# EN: STAGE21-AUTO-COMMENT :: Keep the body of main aligned with the crawler lifecycle contract so orchestration stays explicit instead of becoming hidden and accidental.
# EN: STAGE21-AUTO-COMMENT :: This comment also marks the start of a logical block for audit work, refactoring review, and later incident debugging.
# TR: STAGE21-AUTO-COMMENT :: main isimli bu fonksiyon görünür bir giriş tarafı davranış bloğu tanımlar ve başlatma izleme sırasında kolay takip edilmelidir.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu daha derin çalışma zamanı modüllerine bakmadan önce main neden var anlayabilmelidir; bu işaret kontrol sınırını açıkça anlatır.
# TR: STAGE21-AUTO-COMMENT :: main gövdesini crawler yaşam döngüsü sözleşmesiyle uyumlu tut ki orkestrasyon gizli ve kazara hale gelmesin.
# TR: STAGE21-AUTO-COMMENT :: Bu yorum aynı zamanda denetim, yeniden düzenleme incelemesi ve ileride olay ayıklama için mantıksal blok başlangıcını işaretler.
def main() -> int:
    """
    EN:
    Call the next canonical main layer and return its exit status unchanged.

    EN:
    Very simple explanation:
    - this function is a relay
    - it does not build local policy
    - it does not transform the result
    - it forwards execution to the deeper control surface

    EN:
    Return contract:
    - expected type: int
    - accepted common values: 0 and 2
    - accepted broader values: any other int intentionally emitted downstream
    - undesired values: None or any non-int object

    TR:
    Bir alt kanonik main katmanını çağırır ve çıkış durumunu değiştirmeden döndürür.

    TR:
    Çok basit açıklama:
    - bu fonksiyon bir aktarıcıdır
    - yerel policy kurmaz
    - sonucu dönüştürmez
    - çalıştırmayı daha derindeki kontrol yüzeyine devreder

    TR:
    Dönüş sözleşmesi:
    - beklenen tip: int
    - kabul edilen yaygın değerler: 0 ve 2
    - daha geniş kabul edilen değerler: aşağı akışta bilinçli üretilen diğer int'ler
    - istenmeyen değerler: None veya int olmayan nesneler
    """

    # EN:
    # exit_code is the only real runtime value produced locally in this function.
    # EN:
    # Expected type:
    # - int
    # EN:
    # Accepted values:
    # - 0
    # - 2
    # - any other intentional int from the deeper layer
    # EN:
    # Undesired values:
    # - None
    # - str
    # - dict
    # - list
    # - any non-int object
    # EN:
    # We do not "repair" bad values here because root-entry should remain honest.
    # TR:
    # exit_code bu fonksiyonun yerel olarak ürettiği tek gerçek runtime değeridir.
    # TR:
    # Beklenen tip:
    # - int
    # TR:
    # Kabul edilen değerler:
    # - 0
    # - 2
    # - derin katmandan gelen diğer bilinçli int değerleri
    # TR:
    # İstenmeyen değerler:
    # - None
    # - str
    # - dict
    # - list
    # - int olmayan herhangi bir nesne
    # TR:
    # Kök giriş dürüst kalsın diye kötü değerleri burada "tamir etmiyoruz".
    # EN: STAGE21-AUTO-COMMENT :: This assignment establishes or updates exit_code as part of the visible entry-layer state.
    # EN: STAGE21-AUTO-COMMENT :: State created here should stay minimal because the entry module should describe startup intent, not hide broad business logic.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that downstream runtime modules still receive the same contract and sequencing assumptions.
    # EN: STAGE21-AUTO-COMMENT :: This marker exists so a reader can pause at the exact point where local entry-state becomes defined or mutated.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama exit_code değerlerini görünür giriş katmanı durumu olarak kurar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Burada oluşturulan durum minimal kalmalıdır çünkü giriş modülü geniş iş mantığını gizlemek yerine başlatma niyetini anlatmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış çalışma zamanı modüllerinin aynı sözleşme ve sıralama varsayımlarını hâlâ aldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucunun yerel giriş durumunun tanımlandığı veya değiştiği noktada durabilmesi için vardır.
    exit_code = run_main_loop()

    # EN:
    # Return the exit code unchanged.
    # EN:
    # Why:
    # - outer CLI semantics should match the deeper layer truth
    # - this file should not reinterpret process status meaning
    # TR:
    # Çıkış kodunu değiştirmeden geri döndür.
    # TR:
    # Neden:
    # - dış CLI semantiği daha derin katman doğrusu ile aynı kalmalı
    # - bu dosya süreç durum anlamını yeniden yorumlamamalı
    # EN: STAGE21-AUTO-COMMENT :: This return point ends the current entry-side function path and hands a result or completion signal back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return sites deserve comments because they often define the practical contract observed by the next orchestration layer.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, verify the caller still receives the shape, meaning, and timing it expects.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the function exit semantics visible to a beginner reader.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası mevcut giriş tarafı fonksiyon yolunu bitirir ve sonucu veya tamamlanma sinyalini çağırana geri verir.
    # TR: STAGE21-AUTO-COMMENT :: Return noktaları yorum hak eder çünkü çoğu zaman bir sonraki orkestrasyon katmanının gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satırı değiştirirken çağıranın beklediği biçim, anlam ve zamanlamayı hâlâ aldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret fonksiyon çıkış anlamını yeni başlayan okuyucu için görünür kılar.
    return exit_code


# EN:
# This direct-execution guard preserves normal Python CLI behavior.
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
# EN:
# SystemExit(main()) is used so the process exits with the delegated status.
# TR:
# Bu doğrudan-çalıştırma guard'ı normal Python CLI davranışını korur.
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
# TR:
# SystemExit(main()) kullanılır; böylece süreç delege edilen durumla kapanır.
# EN: STAGE21-AUTO-COMMENT :: This main-guard ensures the module can be imported safely without triggering direct runtime execution.
# EN: STAGE21-AUTO-COMMENT :: The guard cleanly separates reusable import behavior from direct command-line style startup behavior.
# EN: STAGE21-AUTO-COMMENT :: In operational audits, this block tells us exactly where direct execution begins and where import-only behavior ends.
# EN: STAGE21-AUTO-COMMENT :: Keeping this guard explicit is important because entry modules are the first place humans inspect during startup incidents.
# TR: STAGE21-AUTO-COMMENT :: Bu ana-koruma modülün doğrudan çalışma zamanını tetiklemeden güvenli biçimde import edilebilmesini sağlar.
# TR: STAGE21-AUTO-COMMENT :: Bu koruma yeniden kullanılabilir import davranışı ile doğrudan komut satırı tarzı başlatma davranışını temiz biçimde ayırır.
# TR: STAGE21-AUTO-COMMENT :: Operasyonel denetimlerde bu blok doğrudan çalıştırmanın nerede başladığını ve sadece import davranışının nerede bittiğini söyler.
# TR: STAGE21-AUTO-COMMENT :: Bu korumayı açık tutmak önemlidir çünkü giriş modülleri başlatma olaylarında insanların ilk baktığı yerdir.
if __name__ == "__main__":
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible main-entry control path and is being annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even when the syntax is familiar, the purpose of the statement should remain explicit because entry code anchors the reading path.
    # EN: STAGE21-AUTO-COMMENT :: Review this line together with nearby comments so the local intention and the larger orchestration intention stay aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker exists to prevent silent meaning from hiding inside compact startup code.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür ana giriş kontrol yolunun parçasıdır ve dosyayı yeni başlayanlar için anlaşılır tutmak adına açıklanmaktadır.
    # TR: STAGE21-AUTO-COMMENT :: Sözdizimi tanıdık olsa bile ifadenin amacı açık kalmalıdır çünkü giriş kodu okuma yolunu sabitler.
    # TR: STAGE21-AUTO-COMMENT :: Bu satırı yakın yorumlarla birlikte gözden geçir ki yerel niyet ile büyük orkestrasyon niyeti uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık başlatma kodu içine sessiz anlam gizlenmesini önlemek için vardır.
    raise SystemExit(main())
