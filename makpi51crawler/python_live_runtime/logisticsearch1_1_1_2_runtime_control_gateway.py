"""
EN:
This file is the runtime-control gateway child of the state DB gateway family.

In very simple terms:
- The crawler has a durable control state in PostgreSQL.
- That state can say things like "play", "pause", or "stop".
- This file is the Python messenger that asks the database:
  "What is the current control state?" or
  "Please change the control state."

What this file mainly does:
- Read current runtime-control state.
- Ask whether runtime may currently claim new work.
- Write a new desired control state.
- Build a safe degraded payload when SQL returns no row.

What this file does NOT do:
- It does not open the DB connection.
- It does not close the DB connection.
- It does not commit or rollback.
- It does not itself decide policy.
- It only exposes the database truth or exposes that the truth could not be read cleanly.

Important beginner meaning:
- "runtime_control" = the crawler's durable control panel state.
- "may_claim" = whether the crawler is allowed to take a new URL right now.
- "degraded" = we could not get the normal expected DB answer, so we return an
  honest warning-shaped payload instead of pretending everything is fine.
- "no row" = SQL returned nothing when one row was expected.

TR:
Bu dosya state DB gateway ailesinin runtime-control gateway child yüzeyidir.

Çok basit anlatımla:
- Crawler'ın PostgreSQL içinde kalıcı bir kontrol durumu vardır.
- Bu durum "play", "pause" veya "stop" gibi şeyler söyleyebilir.
- Bu dosya veritabanına şunu soran Python habercisidir:
  "Şu anki kontrol durumu nedir?" veya
  "Lütfen kontrol durumunu değiştir."

Bu dosya esas olarak ne yapar:
- Mevcut runtime-control durumunu okur.
- Runtime'ın şu anda yeni iş claim edip edemeyeceğini sorar.
- Yeni desired control state yazar.
- SQL satır döndürmezse güvenli degrade payload kurar.

Bu dosya ne yapmaz:
- DB bağlantısı açmaz.
- DB bağlantısı kapatmaz.
- Commit veya rollback yapmaz.
- Policy'yi kendi başına belirlemez.
- Yalnızca veritabanı truth'ünü veya truth'ün temiz okunamadığını açığa çıkarır.

Önemli başlangıç anlamları:
- "runtime_control" = crawler'ın kalıcı kontrol paneli durumu.
- "may_claim" = crawler'ın şu anda yeni bir URL almasına izin var mı.
- "degraded" = veritabanından beklenen normal cevabı alamadık; her şey yolunda gibi
  davranmak yerine dürüst bir uyarı payload'ı döndürüyoruz.
- "no row" = SQL bir satır beklenirken hiçbir şey döndürmedi.
"""


# EN: RUNTIME CONTROL GATEWAY IDENTITY MEMORY BLOCK V4
# EN:
# EN: Why this file exists:
# EN: - because durable runtime-control truth lives in PostgreSQL and needs one explicit Python messenger layer
# EN: - because upper layers should ask for control truth through named helpers instead of embedding SQL details everywhere
# EN: - because degraded/no-row branches must stay visible and structured, not hidden
# EN:
# EN: What this file DOES:
# EN: - read current runtime-control truth
# EN: - answer whether runtime may currently claim new work
# EN: - write a new desired runtime-control state
# EN: - build honest degraded payloads when expected DB truth is missing
# EN:
# EN: What this file DOES NOT do:
# EN: - it does not open DB connections
# EN: - it does not close DB connections
# EN: - it does not own transaction commit/rollback policy
# EN: - it does not decide crawler business policy by itself
# EN:
# EN: Topological role:
# EN: - controller and worker layers call into this gateway child
# EN: - this child exposes durable control truth from SQL-facing functions
# EN: - gateway_support owns the lower shared connection/row plumbing
# EN:
# EN: Important beginner meanings:
# EN: - runtime_control => durable crawler control panel snapshot
# EN: - desired_state => commonly run / pause / stop
# EN: - may_claim => whether runtime should currently take new work
# EN: - degraded => normal expected DB truth could not be read cleanly
# EN: - no row => SQL returned nothing where one row was expected
# EN:
# EN: Accepted architectural identity:
# EN: - runtime-control truth gateway
# EN: - durable control-state messenger
# EN:
# EN: Undesired architectural identity:
# EN: - DB connection owner
# EN: - hidden worker loop
# EN: - hidden fetch engine
# TR: RUNTIME CONTROL GATEWAY KİMLİK HAFIZA BLOĞU V4
# TR:
# TR: Bu dosya neden var:
# TR: - çünkü kalıcı runtime-control doğrusu PostgreSQL içinde yaşar ve bunun için açık bir Python haberci katmanı gerekir
# TR: - çünkü üst katmanlar SQL ayrıntısını her yere gömmek yerine kontrol doğrusunu isimli yardımcılar üzerinden sormalıdır
# TR: - çünkü degrade/no-row dalları gizlenmeden, yapılı biçimde görünür kalmalıdır
# TR:
# TR: Bu dosya NE yapar:
# TR: - mevcut runtime-control doğrusunu okur
# TR: - runtime'ın şu anda yeni iş claim edip edemeyeceğine cevap verir
# TR: - yeni bir desired runtime-control state yazar
# TR: - beklenen DB doğrusu yoksa dürüst degrade payload'lar kurar
# TR:
# TR: Bu dosya NE yapmaz:
# TR: - DB bağlantısı açmaz
# TR: - DB bağlantısı kapatmaz
# TR: - transaction commit/rollback policy'sinin sahibi değildir
# TR: - crawler iş politikasını kendi başına belirlemez
# TR:
# TR: Topolojik rol:
# TR: - controller ve worker katmanları bu gateway child'ını çağırır
# TR: - bu child SQL-yüzlü fonksiyonlardan gelen kalıcı kontrol doğrusunu açığa çıkarır
# TR: - daha aşağıdaki ortak bağlantı/satır plumbing'inin sahibi gateway_support'tur
# TR:
# TR: Önemli başlangıç anlamları:
# TR: - runtime_control => kalıcı crawler kontrol paneli snapshot'ı
# TR: - desired_state => çoğunlukla run / pause / stop
# TR: - may_claim => runtime'ın şu anda yeni iş alıp almaması gerektiği
# TR: - degraded => beklenen normal DB doğrusu temiz biçimde okunamadı
# TR: - no row => SQL bir satır beklenirken hiçbir şey döndürmedi
# TR:
# TR: Kabul edilen mimari kimlik:
# TR: - runtime-control truth gateway
# TR: - kalıcı kontrol-durumu habercisi
# TR:
# TR: İstenmeyen mimari kimlik:
# TR: - DB bağlantı sahibi
# TR: - gizli worker loop
# TR: - gizli fetch motoru

# EN: STAGE21-AUTO-COMMENT :: This import line declares runtime-control gateway dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or command surfaces shape live control behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether gateway routing or operational semantics changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak runtime-control gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü canlı kontrol davranışını hangi yardımcıların, sözleşmelerin veya komut yüzeylerinin şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse gateway yönlendirmesinin veya operasyonel anlamın da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from __future__ import annotations

# EN: Any is used because these payload dictionaries intentionally remain flexible
# EN: and easy to print, inspect, and audit.
# TR: Any kullanılır; çünkü bu payload sözlükleri bilinçli olarak esnek, yazdırması
# TR: kolay ve denetlenebilir bırakılır.
# EN: STAGE21-AUTO-COMMENT :: This import line declares runtime-control gateway dependencies by bringing in typing -> Any.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or command surfaces shape live control behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether gateway routing or operational semantics changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı typing -> Any ögelerini içeri alarak runtime-control gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü canlı kontrol davranışını hangi yardımcıların, sözleşmelerin veya komut yüzeylerinin şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse gateway yönlendirmesinin veya operasyonel anlamın da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from typing import Any

# EN: psycopg provides the live PostgreSQL connection type used by these functions.
# TR: psycopg bu fonksiyonların kullandığı canlı PostgreSQL bağlantı tipini sağlar.
# EN: STAGE21-AUTO-COMMENT :: This import line declares runtime-control gateway dependencies by bringing in psycopg.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or command surfaces shape live control behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether gateway routing or operational semantics changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg ögelerini içeri alarak runtime-control gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü canlı kontrol davranışını hangi yardımcıların, sözleşmelerin veya komut yüzeylerinin şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse gateway yönlendirmesinin veya operasyonel anlamın da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
import psycopg

# EN: dict_row lets fetched SQL rows behave like dictionaries.
# TR: dict_row okunan SQL satırlarının sözlük gibi davranmasını sağlar.
# EN: STAGE21-AUTO-COMMENT :: This import line declares runtime-control gateway dependencies by bringing in psycopg.rows -> dict_row.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or command surfaces shape live control behavior.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether gateway routing or operational semantics changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg.rows -> dict_row ögelerini içeri alarak runtime-control gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü canlı kontrol davranışını hangi yardımcıların, sözleşmelerin veya komut yüzeylerinin şekillendirdiğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse gateway yönlendirmesinin veya operasyonel anlamın da değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from psycopg.rows import dict_row



# EN: NO-ROW PAYLOAD PURPOSE MEMORY BLOCK V4 / build_runtime_control_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because a missing control row should become an explicit degraded payload, not a silent crash or fake success
# EN:
# EN: Accepted input meaning:
# EN: - context explaining which control read/write corridor failed to receive a row
# EN:
# EN: Accepted output meaning:
# EN: - dict payload with runtime_control_degraded visibility
# EN:
# EN: Accepted shape examples:
# EN: - desired_state may be None when unresolved
# EN: - may_claim may be None when unresolved
# EN:
# EN: Undesired behavior:
# EN: - pretending no-row means normal healthy truth
# TR: NO-ROW PAYLOAD AMAÇ HAFIZA BLOĞU V4 / build_runtime_control_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü eksik kontrol satırı sessiz crash veya sahte başarı yerine açık degrade payload'a dönüşmelidir
# TR:
# TR: Kabul edilen girdi anlamı:
# TR: - hangi kontrol okuma/yazma koridorunun satır alamadığını anlatan bağlam
# TR:
# TR: Kabul edilen çıktı anlamı:
# TR: - runtime_control_degraded görünürlüğü taşıyan dict payload
# TR:
# TR: Kabul edilen şekil örnekleri:
# TR: - desired_state çözülemediyse None olabilir
# TR: - may_claim çözülemediyse None olabilir
# TR:
# TR: İstenmeyen davranış:
# TR: - no-row durumunu normal sağlıklı truth gibi göstermek

# EN: STAGE21-AUTO-COMMENT :: This gateway function named build_runtime_control_no_row_payload defines a runtime-control entry or transformation point.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what build_runtime_control_no_row_payload receives, how it normalizes control intent, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing build_runtime_control_no_row_payload, verify that operator-visible semantics and runtime-side semantics still match exactly.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of build_runtime_control_no_row_payload obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: build_runtime_control_no_row_payload isimli bu gateway fonksiyonu bir runtime-control giriş veya dönüşüm noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu build_runtime_control_no_row_payload fonksiyonunun ne aldığını, kontrol niyetini nasıl normalize ettiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: build_runtime_control_no_row_payload değiştirilirken operatörün gördüğü anlam ile runtime tarafı anlamın tam olarak eşleşmeye devam ettiği doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret build_runtime_control_no_row_payload başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: Parameter action is the operator-visible control action label that says which runtime-control no-row corridor is being reported.
# TR: `action` parametresi hangi runtime-control no-row koridorunun raporlandığını söyleyen operatör-görünür kontrol eylem etiketidir.
# EN: Parameter desired_state is the optional requested durable state such as run, pause, or stop when that intent exists.
# TR: `desired_state` parametresi böyle bir niyet varsa run, pause veya stop gibi opsiyonel istenen kalıcı durumdur.
# EN: Parameter state_reason is the optional human-readable explanation for why the control state was requested or inspected.
# TR: `state_reason` parametresi kontrol durumunun neden istendiğini veya incelendiğini açıklayan opsiyonel insan-okunur gerekçedir.
# EN: Parameter requested_by is the optional actor identity that says who requested or triggered the control-side action.
# TR: `requested_by` parametresi kontrol tarafı eylemini kimin istediğini veya tetiklediğini söyleyen opsiyonel aktör kimliğidir.
# EN: Parameter error_class is the required error type label that makes the degraded no-row payload auditable.
# TR: `error_class` parametresi degrade no-row payloadını denetlenebilir yapan zorunlu hata türü etiketidir.
# EN: Parameter error_message is the required concrete failure text that explains why expected DB truth was missing.
# TR: `error_message` parametresi beklenen DB doğrusunun neden eksik kaldığını açıklayan zorunlu somut hata metnidir.
def build_runtime_control_no_row_payload(
    *,
    action: str,
    desired_state: str | None = None,
    state_reason: str | None = None,
    requested_by: str | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, Any]:
    """
    EN:
    Build the standard degraded payload for a runtime-control no-row problem.

    In very simple terms:
    - Normal branch: SQL should give us one row.
    - Broken branch: SQL gives us no row.
    - In that broken branch, we do not fake a success result.
    - We build one honest warning-shaped dictionary instead.

    Input contract:
    - action: required text telling which SQL path failed.
    - desired_state/state_reason/requested_by: optional echoed input values.
    - error_class/error_message: required explanatory text.

    Return contract:
    - Returns dict[str, Any].
    - runtime_control_degraded is always True.
    - may_claim is always None here.
    - runtime_control_completed is always False here.
    - Never returns None.

    Why may_claim is None here:
    - None means "unknown / unresolved".
    - False would wrongly mean "known and explicitly denied".
    - That distinction matters.

    TR:
    Runtime-control no-row problemi için standart degrade payload'ı kurar.

    Çok basit anlatımla:
    - Normal dal: SQL bize bir satır vermelidir.
    - Bozuk dal: SQL hiç satır vermez.
    - Böyle bir durumda sahte başarı sonucu üretmeyiz.
    - Onun yerine dürüst bir uyarı sözlüğü kurarız.

    Girdi sözleşmesi:
    - action: hangi SQL yolunun bozulduğunu anlatan zorunlu metin.
    - desired_state/state_reason/requested_by: opsiyonel yankılanan giriş değerleri.
    - error_class/error_message: zorunlu açıklama metinleri.

    Dönüş sözleşmesi:
    - dict[str, Any] döndürür.
    - runtime_control_degraded burada her zaman True'dur.
    - may_claim burada her zaman None'dır.
    - runtime_control_completed burada her zaman False'dur.
    - Asla None döndürmez.

    Burada may_claim neden None'dır:
    - None "bilmiyoruz / çözülemedi" demektir.
    - False ise "biliyoruz ve açıkça izin yok" anlamına gelirdi.
    - Bu ayrım önemlidir.
    """

    # EN: degraded_payload is the shared warning-shaped dictionary for all
    # EN: runtime-control no-row branches in this file.
    # TR: degraded_payload bu dosyadaki tüm runtime-control no-row dallarının
    # TR: paylaştığı ortak uyarı-şekilli sözlüktür.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates degraded_payload as part of the runtime-control gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama degraded_payload değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
    degraded_payload = {
        "desired_state": desired_state,
        "state_reason": state_reason,
        "requested_by": requested_by,
        "may_claim": None,
        "runtime_control_action": action,
        "runtime_control_degraded": True,
        "runtime_control_degraded_reason": f"{action}_returned_no_row",
        "runtime_control_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return degraded_payload



# EN: READ-TRUTH PURPOSE MEMORY BLOCK V4 / get_webcrawler_runtime_control
# EN:
# EN: Why this helper exists:
# EN: - because upper layers need one small named function that reads the durable control snapshot
# EN:
# EN: Accepted input:
# EN: - live DB connection
# EN:
# EN: Accepted output:
# EN: - dict payload representing current control truth
# EN: - degraded dict payload on no-row branch
# EN:
# EN: Common accepted desired_state values:
# EN: - run
# EN: - pause
# EN: - stop
# EN:
# EN: Undesired output:
# EN: - silent None instead of structured payload
# TR: READ-TRUTH AMAÇ HAFIZA BLOĞU V4 / get_webcrawler_runtime_control
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü üst katmanların kalıcı kontrol snapshot'ını okuyan küçük ve isimli bir fonksiyona ihtiyacı vardır
# TR:
# TR: Kabul edilen girdi:
# TR: - canlı DB bağlantısı
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut kontrol doğrusunu temsil eden dict payload
# TR: - no-row dalında degrade dict payload
# TR:
# TR: Yaygın kabul edilen desired_state değerleri:
# TR: - run
# TR: - pause
# TR: - stop
# TR:
# TR: İstenmeyen çıktı:
# TR: - yapılı payload yerine sessiz None

# EN: STAGE21-AUTO-COMMENT :: This gateway function named get_webcrawler_runtime_control defines a runtime-control entry or transformation point.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what get_webcrawler_runtime_control receives, how it normalizes control intent, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing get_webcrawler_runtime_control, verify that operator-visible semantics and runtime-side semantics still match exactly.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of get_webcrawler_runtime_control obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: get_webcrawler_runtime_control isimli bu gateway fonksiyonu bir runtime-control giriş veya dönüşüm noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu get_webcrawler_runtime_control fonksiyonunun ne aldığını, kontrol niyetini nasıl normalize ettiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: get_webcrawler_runtime_control değiştirilirken operatörün gördüğü anlam ile runtime tarafı anlamın tam olarak eşleşmeye devam ettiği doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret get_webcrawler_runtime_control başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: Parameter conn is the live psycopg connection that this gateway uses to read the durable runtime-control row from PostgreSQL.
# TR: `conn` parametresi bu gateway'in PostgreSQL içindeki kalıcı runtime-control satırını okumak için kullandığı canlı psycopg bağlantısıdır.
def get_webcrawler_runtime_control(conn: psycopg.Connection) -> dict[str, Any]:
    """
    EN:
    Read the current durable runtime-control state from PostgreSQL.

    In very simple terms:
    - This asks the DB control panel: "What state are we in right now?"
    - A healthy answer is one row.
    - That row is returned as a plain dictionary.
    - If no row comes back, we return a degraded warning dictionary.

    Input contract:
    - conn must be an already-open psycopg.Connection.
    - This function does not own commit/rollback/close.

    Return branches:
    - dict(row) on the normal branch.
    - degraded dict on the no-row branch.
    - Unexpected DB exceptions are not swallowed.

    TR:
    PostgreSQL'den mevcut kalıcı runtime-control durumunu okur.

    Çok basit anlatımla:
    - Bu fonksiyon DB kontrol paneline "Şu an hangi durumdayız?" diye sorar.
    - Sağlıklı cevap tek bir satırdır.
    - O satır düz bir sözlük olarak döndürülür.
    - Hiç satır gelmezse degrade uyarı sözlüğü döndürülür.

    Girdi sözleşmesi:
    - conn önceden açılmış psycopg.Connection olmalıdır.
    - Commit/rollback/close sahipliği bu fonksiyonda değildir.

    Dönüş dalları:
    - Normal dalda dict(row).
    - No-row dalında degrade dict.
    - Beklenmeyen DB istisnaları yutulmaz.
    """

    # EN: cur is a cursor configured so fetchone() returns dict-like rows.
    # TR: cur fetchone() sonucunun dict-benzeri satır dönmesi için ayarlanmış cursor'dır.
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible runtime-control gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface can change live crawler behavior.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intention and wider control meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact control code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür runtime-control gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey canlı crawler davranışını değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş kontrol anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık kontrol kodunun sessiz anlam gizlemesini önler.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: This SQL function is the durable DB surface for reading runtime control.
        # TR: Bu SQL fonksiyonu runtime control okumak için kalıcı DB yüzeyidir.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway-side action, often a call that moves control intent into the runtime layer.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because a compact call can hide an important operational side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the gateway layer and still matches control semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan gateway tarafı bir eylem gerçekleştirir; çoğu zaman kontrol niyetini runtime katmanına taşıyan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık bir çağrı önemli bir operasyonel yan etkiyi gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ gateway katmanına ait olduğu ve kontrol anlamıyla eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT * FROM ops.get_webcrawler_runtime_control()
            """
        )

        # EN: row should normally be one dict-like result row.
        # EN: None means the SQL surface did not return the expected row.
        # TR: row normalde tek bir dict-benzeri sonuç satırı olmalıdır.
        # TR: None olması SQL yüzeyinin beklenen satırı döndürmediği anlamına gelir.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the runtime-control gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
        row = cur.fetchone()

    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects runtime-control behavior based on current input, state, or validation outcome.
    # EN: STAGE21-AUTO-COMMENT :: Conditional differences matter here because a small branch change can alter whether a live control request is accepted, rejected, or redirected.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect every path and confirm the visible operator contract still matches runtime behavior.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision with direct operational consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut girdi, durum veya doğrulama sonucuna göre runtime-control davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşul farkları burada önemlidir çünkü küçük bir dal değişikliği canlı kontrol isteğinin kabul edilmesini, reddedilmesini veya başka yöne gitmesini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dal düzenlenirken her yol incelenmeli ve görünür operatör sözleşmesinin runtime davranışıyla hâlâ eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret doğrudan operasyonel sonucu olan bir kararı vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
        # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_runtime_control_no_row_payload(
            action="ops_get_webcrawler_runtime_control",
            error_class="runtime_control_get_no_row",
            error_message="ops.get_webcrawler_runtime_control() returned no row",
        )

    # EN: payload is the plain dictionary snapshot seen by upper layers.
    # TR: payload üst katmanların gördüğü düz sözlük anlık görüntüsüdür.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates payload as part of the runtime-control gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama payload değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
    payload = dict(row)
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return payload



# EN: MAY-CLAIM PURPOSE MEMORY BLOCK V4 / webcrawler_runtime_may_claim
# EN:
# EN: Why this helper exists:
# EN: - because upper layers often need the narrow answer "may runtime claim now?"
# EN: - because this should stay separate from raw control-row reading semantics
# EN:
# EN: Accepted input:
# EN: - live DB connection
# EN:
# EN: Accepted output:
# EN: - dict payload with may_claim True / False
# EN: - degraded dict payload with may_claim None when unresolved
# EN:
# EN: Undesired output:
# EN: - plain bool with no context
# EN: - silent failure
# TR: MAY-CLAIM AMAÇ HAFIZA BLOĞU V4 / webcrawler_runtime_may_claim
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü üst katmanlar çoğu zaman dar şu cevaba ihtiyaç duyar: "runtime şu anda claim edebilir mi?"
# TR: - çünkü bu anlam ham control-row okuma semantiğinden ayrı kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - canlı DB bağlantısı
# TR:
# TR: Kabul edilen çıktı:
# TR: - may_claim True / False taşıyan dict payload
# TR: - çözülemeyen durumda may_claim None taşıyan degrade dict payload
# TR:
# TR: İstenmeyen çıktı:
# TR: - bağlamsız düz bool
# TR: - sessiz hata

# EN: STAGE21-AUTO-COMMENT :: This gateway function named webcrawler_runtime_may_claim defines a runtime-control entry or transformation point.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what webcrawler_runtime_may_claim receives, how it normalizes control intent, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing webcrawler_runtime_may_claim, verify that operator-visible semantics and runtime-side semantics still match exactly.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of webcrawler_runtime_may_claim obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: webcrawler_runtime_may_claim isimli bu gateway fonksiyonu bir runtime-control giriş veya dönüşüm noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu webcrawler_runtime_may_claim fonksiyonunun ne aldığını, kontrol niyetini nasıl normalize ettiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: webcrawler_runtime_may_claim değiştirilirken operatörün gördüğü anlam ile runtime tarafı anlamın tam olarak eşleşmeye devam ettiği doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret webcrawler_runtime_may_claim başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: Parameter conn is the live psycopg connection that this gateway uses to ask whether runtime may currently claim new work.
# TR: `conn` parametresi bu gateway'in runtime'ın şu anda yeni iş claim edip edemeyeceğini sormak için kullandığı canlı psycopg bağlantısıdır.
def webcrawler_runtime_may_claim(conn: psycopg.Connection) -> dict[str, Any]:
    """
    EN:
    Ask the database whether runtime is currently allowed to claim new work.

    In very simple terms:
    - The crawler does not just grab work blindly.
    - It first asks the DB policy surface: "May I claim now?"
    - Normal answer: one row with may_claim-style information.
    - Broken answer: no row, which becomes a degraded dictionary.

    Input contract:
    - conn must be an already-open psycopg.Connection.

    Return branches:
    - dict(row) on the normal branch.
    - degraded dict on the no-row branch.
    - Unexpected DB exceptions are not swallowed.

    Important detail:
    - In the degraded branch, may_claim is None.
    - That means unknown.
    - It does NOT mean False.

    TR:
    Runtime'ın şu anda yeni iş claim etmesine izin verilip verilmediğini DB'ye sorar.

    Çok basit anlatımla:
    - Crawler işi körlemesine almaz.
    - Önce DB policy yüzeyine "Şu an claim edebilir miyim?" diye sorar.
    - Normal cevap: may_claim benzeri bilgi taşıyan tek satır.
    - Bozuk cevap: hiç satır yok; bu da degrade sözlüğe çevrilir.

    Girdi sözleşmesi:
    - conn önceden açılmış psycopg.Connection olmalıdır.

    Dönüş dalları:
    - Normal dalda dict(row).
    - No-row dalında degrade dict.
    - Beklenmeyen DB istisnaları yutulmaz.

    Önemli ayrıntı:
    - Degrade dalında may_claim None olur.
    - Bu "bilmiyoruz" demektir.
    - False demek değildir.
    """

    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible runtime-control gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface can change live crawler behavior.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intention and wider control meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact control code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür runtime-control gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey canlı crawler davranışını değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş kontrol anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık kontrol kodunun sessiz anlam gizlemesini önler.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: This SQL function is the DB truth surface for "may claim?" policy.
        # TR: Bu SQL fonksiyonu "claim edebilir miyim?" policy sorusunun DB truth yüzeyidir.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway-side action, often a call that moves control intent into the runtime layer.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because a compact call can hide an important operational side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the gateway layer and still matches control semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan gateway tarafı bir eylem gerçekleştirir; çoğu zaman kontrol niyetini runtime katmanına taşıyan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık bir çağrı önemli bir operasyonel yan etkiyi gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ gateway katmanına ait olduğu ve kontrol anlamıyla eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT * FROM ops.webcrawler_runtime_may_claim()
            """
        )

        # EN: row is expected to be the single policy answer row.
        # TR: row tek policy cevap satırı olarak beklenir.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the runtime-control gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
        row = cur.fetchone()

    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects runtime-control behavior based on current input, state, or validation outcome.
    # EN: STAGE21-AUTO-COMMENT :: Conditional differences matter here because a small branch change can alter whether a live control request is accepted, rejected, or redirected.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect every path and confirm the visible operator contract still matches runtime behavior.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision with direct operational consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut girdi, durum veya doğrulama sonucuna göre runtime-control davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşul farkları burada önemlidir çünkü küçük bir dal değişikliği canlı kontrol isteğinin kabul edilmesini, reddedilmesini veya başka yöne gitmesini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dal düzenlenirken her yol incelenmeli ve görünür operatör sözleşmesinin runtime davranışıyla hâlâ eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret doğrudan operasyonel sonucu olan bir kararı vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
        # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_runtime_control_no_row_payload(
            action="ops_webcrawler_runtime_may_claim",
            error_class="runtime_control_may_claim_no_row",
            error_message="ops.webcrawler_runtime_may_claim() returned no row",
        )

    # EN: payload is the plain visible result dictionary.
    # TR: payload düz ve görünür sonuç sözlüğüdür.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates payload as part of the runtime-control gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama payload değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
    payload = dict(row)
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return payload



# EN: WRITE-TRUTH PURPOSE MEMORY BLOCK V4 / set_webcrawler_runtime_control
# EN:
# EN: Why this helper exists:
# EN: - because changing durable control state should happen through one explicit gateway function
# EN: - because desired_state writes need structured payload visibility
# EN:
# EN: Accepted input values:
# EN: - desired_state commonly run / pause / stop
# EN: - state_reason text
# EN: - requested_by text
# EN:
# EN: Accepted output:
# EN: - dict payload describing written or degraded control truth
# EN:
# EN: Undesired input:
# EN: - blank/uninformative state_reason when caller should provide meaning
# EN: - empty requested_by identity
# EN: - unsupported desired_state text
# TR: WRITE-TRUTH AMAÇ HAFIZA BLOĞU V4 / set_webcrawler_runtime_control
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü kalıcı kontrol durumunu değiştirme işi tek ve açık gateway fonksiyonu üzerinden yapılmalıdır
# TR: - çünkü desired_state yazıları yapılı payload görünürlüğü taşımalıdır
# TR:
# TR: Kabul edilen girdi değerleri:
# TR: - desired_state çoğunlukla run / pause / stop
# TR: - state_reason metni
# TR: - requested_by metni
# TR:
# TR: Kabul edilen çıktı:
# TR: - yazılmış veya degrade kontrol doğrusunu anlatan dict payload
# TR:
# TR: İstenmeyen girdi:
# TR: - çağıranın anlam vermesi gerekirken boş/anlamsız state_reason
# TR: - boş requested_by kimliği
# TR: - desteklenmeyen desired_state metni

# EN: STAGE21-AUTO-COMMENT :: This gateway function named set_webcrawler_runtime_control defines a runtime-control entry or transformation point.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what set_webcrawler_runtime_control receives, how it normalizes control intent, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing set_webcrawler_runtime_control, verify that operator-visible semantics and runtime-side semantics still match exactly.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of set_webcrawler_runtime_control obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: set_webcrawler_runtime_control isimli bu gateway fonksiyonu bir runtime-control giriş veya dönüşüm noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu set_webcrawler_runtime_control fonksiyonunun ne aldığını, kontrol niyetini nasıl normalize ettiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: set_webcrawler_runtime_control değiştirilirken operatörün gördüğü anlam ile runtime tarafı anlamın tam olarak eşleşmeye devam ettiği doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret set_webcrawler_runtime_control başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: Parameter conn is the live psycopg connection that this gateway uses to write the durable runtime-control update.
# TR: `conn` parametresi bu gateway'in kalıcı runtime-control güncellemesini yazmak için kullandığı canlı psycopg bağlantısıdır.
# EN: Parameter desired_state is the required next durable control state that should be stored, commonly run, pause, or stop.
# TR: `desired_state` parametresi depolanması gereken zorunlu sonraki kalıcı kontrol durumudur; çoğunlukla run, pause veya stop olur.
# EN: Parameter state_reason is the required operator-readable reason that explains why the new durable state is being written.
# TR: `state_reason` parametresi yeni kalıcı durumun neden yazıldığını açıklayan zorunlu operatör-okunur gerekçedir.
# EN: Parameter requested_by is the required actor identity that records who requested the durable runtime-control change.
# TR: `requested_by` parametresi kalıcı runtime-control değişimini kimin istediğini kaydeden zorunlu aktör kimliğidir.
def set_webcrawler_runtime_control(
    conn: psycopg.Connection,
    *,
    desired_state: str,
    state_reason: str,
    requested_by: str,
) -> dict[str, Any]:
    """
    EN:
    Write a new durable runtime-control request into PostgreSQL.

    In very simple terms:
    - This is the "change the control panel state" function.
    - Example idea: switch from play to pause.
    - The database should return one result row describing the write outcome.
    - If no row comes back, we return a degraded warning dictionary.

    Input contract:
    - conn: already-open psycopg.Connection.
    - desired_state: required text such as "play", "pause", or "stop".
    - state_reason: required explanatory text.
    - requested_by: required requester/operator identity text.

    Return branches:
    - dict(row) on the normal write-result branch.
    - degraded dict on the no-row branch.
    - Unexpected DB exceptions are not swallowed.

    TR:
    PostgreSQL içine yeni bir kalıcı runtime-control isteği yazar.

    Çok basit anlatımla:
    - Bu fonksiyon "kontrol paneli durumunu değiştir" fonksiyonudur.
    - Örnek fikir: play durumundan pause durumuna geçmek.
    - Veritabanı normalde yazım sonucunu anlatan tek satır döndürmelidir.
    - Hiç satır gelmezse degrade uyarı sözlüğü döndürürüz.

    Girdi sözleşmesi:
    - conn: önceden açılmış psycopg.Connection.
    - desired_state: "play", "pause" veya "stop" gibi zorunlu metin.
    - state_reason: zorunlu açıklama metni.
    - requested_by: zorunlu istekçi/operatör kimliği.

    Dönüş dalları:
    - Normal yazım sonucu dalında dict(row).
    - No-row dalında degrade dict.
    - Beklenmeyen DB istisnaları yutulmaz.
    """

    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible runtime-control gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface can change live crawler behavior.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intention and wider control meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact control code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür runtime-control gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey canlı crawler davranışını değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş kontrol anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık kontrol kodunun sessiz anlam gizlemesini önler.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: params is the named argument package sent into the SQL function.
        # EN: Keeping it as a dict makes each argument easier to read and audit.
        # TR: params SQL fonksiyonuna gönderilen isimli argüman paketidir.
        # TR: Bunu dict tutmak her argümanı okumayı ve denetlemeyi kolaylaştırır.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates params as part of the runtime-control gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama params değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
        params = {
            "desired_state": desired_state,
            "state_reason": state_reason,
            "requested_by": requested_by,
        }

        # EN: This SQL call writes the desired runtime-control change request.
        # TR: Bu SQL çağrısı istenen runtime-control değişiklik isteğini yazar.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway-side action, often a call that moves control intent into the runtime layer.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because a compact call can hide an important operational side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the gateway layer and still matches control semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan gateway tarafı bir eylem gerçekleştirir; çoğu zaman kontrol niyetini runtime katmanına taşıyan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık bir çağrı önemli bir operasyonel yan etkiyi gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ gateway katmanına ait olduğu ve kontrol anlamıyla eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel bir etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT * FROM ops.set_webcrawler_runtime_control(
                p_desired_state => %(desired_state)s,
                p_state_reason => %(state_reason)s,
                p_requested_by => %(requested_by)s
            )
            """,
            params,
        )

        # EN: row should normally contain one write-result row.
        # TR: row normalde tek bir yazım-sonucu satırı içermelidir.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the runtime-control gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
        row = cur.fetchone()

    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects runtime-control behavior based on current input, state, or validation outcome.
    # EN: STAGE21-AUTO-COMMENT :: Conditional differences matter here because a small branch change can alter whether a live control request is accepted, rejected, or redirected.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect every path and confirm the visible operator contract still matches runtime behavior.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision with direct operational consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut girdi, durum veya doğrulama sonucuna göre runtime-control davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşul farkları burada önemlidir çünkü küçük bir dal değişikliği canlı kontrol isteğinin kabul edilmesini, reddedilmesini veya başka yöne gitmesini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dal düzenlenirken her yol incelenmeli ve görünür operatör sözleşmesinin runtime davranışıyla hâlâ eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret doğrudan operasyonel sonucu olan bir kararı vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
        # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_runtime_control_no_row_payload(
            action="ops_set_webcrawler_runtime_control",
            desired_state=desired_state,
            state_reason=state_reason,
            requested_by=requested_by,
            error_class="runtime_control_set_no_row",
            error_message="ops.set_webcrawler_runtime_control() returned no row",
        )

    # EN: payload is the final plain dictionary returned to upper layers.
    # TR: payload üst katmanlara dönen son düz sözlüktür.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates payload as part of the runtime-control gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw command values into normalized gateway state and should stay explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that caller expectation and downstream runtime interpretation remain compatible.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights where gateway state becomes concrete.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama payload değerlerini runtime-control gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham komut değerlerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde çağıran beklentisinin ve aşağı akış runtime yorumunun uyumlu kaldığını doğrula.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret gateway durumunun somutlaştığı yeri vurgular.
    payload = dict(row)
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete runtime-control result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream command surfaces observe.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure and meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir runtime-control sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü yukarı akış komut yüzeylerinin gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı ve anlamı almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return payload
