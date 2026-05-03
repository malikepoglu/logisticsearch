"""
EN:
This file is the robots child of the state DB gateway family.

EN:
Why this file exists:
- because robots-specific DB truth should live behind one explicit named gateway child
- because upper layers should ask named Python helpers about robots truth instead of repeating raw SQL semantics
- because allow/block/cache/refresh style robots visibility is a separate concern from runtime-control and frontier claim logic

EN:
What this file DOES:
- expose robots-oriented DB helper boundaries
- expose named helpers for reading or updating robots-related truth
- preserve visible allow/block/degraded branch boundaries for upper runtime layers

EN:
What this file DOES NOT do:
- it does not own shared DB connection helpers
- it does not own runtime-control truth
- it does not own frontier claim/release truth
- it does not fetch HTML pages for general content parsing
- it does not act as an operator CLI surface

EN:
Topological role:
- gateway_support sits below this file for shared DB support
- this file sits in the middle for robots-specific DB truth
- worker/controller layers above call these helpers instead of embedding raw robots SQL ideas

EN:
Important visible values and shapes:
- conn => live DB connection object
- user_agent or agent identity text => robots policy evaluation identity
- robots_txt_url or robots target identity => the robots resource being reasoned about
- allow/block verdict visibility => structured robots decision meaning
- cache / refresh / stale visibility => whether existing robots truth is reused or should be refreshed
- degraded / no-row style payloads => visible non-happy branches that should not be hidden

EN:
Accepted architectural identity:
- robots truth gateway
- allow/block/cache DB-adjacent helper layer
- readable robots contract boundary

EN:
Undesired architectural identity:
- hidden crawler controller
- hidden page parser
- hidden ranking engine
- hidden operator surface

TR:
Bu dosya state DB gateway ailesinin robots child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü robots’a özgü DB doğrusu tek ve açık isimli gateway child yüzeyi arkasında yaşamalıdır
- çünkü üst katmanlar ham SQL semantiğini tekrar etmek yerine robots doğrusunu isimli Python yardımcıları üzerinden sormalıdır
- çünkü allow/block/cache/refresh tarzı robots görünürlüğü runtime-control ve frontier claim mantığından ayrı bir konudur

TR:
Bu dosya NE yapar:
- robots odaklı DB yardımcı sınırlarını açığa çıkarır
- robots ile ilgili doğruları okumak veya güncellemek için isimli yardımcılar sunar
- üst runtime katmanları için görünür allow/block/degraded dal sınırlarını korur

TR:
Bu dosya NE yapmaz:
- ortak DB bağlantı yardımcılarının sahibi değildir
- runtime-control doğrusunun sahibi değildir
- frontier claim/release doğrusunun sahibi değildir
- genel içerik parse etmek için HTML sayfa fetch etmez
- operatör CLI yüzeyi gibi davranmaz

TR:
Topolojik rol:
- ortak DB desteği için gateway_support bu dosyanın altındadır
- robots’a özgü DB doğrusu için bu dosya ortadadır
- üstteki worker/controller katmanları ham robots SQL fikrini gömmek yerine bu yardımcıları çağırır

TR:
Önemli görünür değerler ve şekiller:
- conn => canlı DB bağlantı nesnesi
- user_agent veya agent kimlik metni => robots policy değerlendirme kimliği
- robots_txt_url veya robots hedef kimliği => hakkında düşünülen robots kaynağı
- allow/block verdict görünürlüğü => yapılı robots karar anlamı
- cache / refresh / stale görünürlüğü => mevcut robots doğrusunun yeniden kullanılıp kullanılmadığı veya yenilenmesi gerekip gerekmediği
- degraded / no-row tarzı payload’lar => gizlenmemesi gereken mutlu-yol-dışı dallar

TR:
Kabul edilen mimari kimlik:
- robots truth gateway
- allow/block/cache DB-yanı yardımcı katmanı
- okunabilir robots sözleşme sınırı

TR:
İstenmeyen mimari kimlik:
- gizli crawler controller
- gizli sayfa parser’ı
- gizli ranking motoru
- gizli operatör yüzeyi
"""

# EN: This module is the robots child of the state DB gateway family.
# EN: It owns only robots allow/refresh/cache DB wrappers.
# TR: Bu modül state DB gateway ailesinin robots alt yüzeyidir.
# TR: Yalnızca robots allow/refresh/cache DB wrapper'larını taşır.

# EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether policy meaning or gateway responsibility changed as well.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as design evidence rather than boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse politika anlamının veya gateway sorumluluğunun da değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları şablon değil tasarım kanıtı olarak ele alır.
from __future__ import annotations

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in typing -> Any.
# EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether policy meaning or gateway responsibility changed as well.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as design evidence rather than boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı typing -> Any ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse politika anlamının veya gateway sorumluluğunun da değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları şablon değil tasarım kanıtı olarak ele alır.
from typing import Any

# EN: We import psycopg because these functions are thin wrappers around SQL calls.
# TR: Bu fonksiyonlar SQL çağrılarının ince wrapper'ları olduğu için psycopg içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in psycopg.
# EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether policy meaning or gateway responsibility changed as well.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as design evidence rather than boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse politika anlamının veya gateway sorumluluğunun da değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları şablon değil tasarım kanıtı olarak ele alır.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in psycopg.rows -> dict_row.
# EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether policy meaning or gateway responsibility changed as well.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as design evidence rather than boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg.rows -> dict_row ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse politika anlamının veya gateway sorumluluğunun da değişip değişmediği incelenmelidir.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları şablon değil tasarım kanıtı olarak ele alır.
from psycopg.rows import dict_row




# EN: This helper converts a robots SQL wrapper no-row condition into an
# EN: operator-visible degraded payload so upper runtime layers can keep moving
# EN: with honest unresolved robots state instead of crashing or silently drifting.
# TR: Bu yardımcı robots SQL wrapper no-row durumunu operatörün görebileceği
# TR: degrade payload'a çevirir; böylece üst runtime katmanları çökmeden ya da
# TR: sessiz mantık kaymasına düşmeden dürüst çözülmemiş robots durumu ile ilerler.
# EN: ROBOTS HELPER PURPOSE MEMORY BLOCK V5 / build_robots_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because robots-specific DB truth for 'build_robots_no_row_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable robots helper name instead of repeating raw robots SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message
# EN: - values should match the current Python signature and the live robots SQL contract below
# EN:
# EN: Accepted output:
# EN: - a robots-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an allow/block decision shape, a cache/refresh shape, or another explicit branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely exposes one named robots-specific DB-truth boundary
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw robots SQL semantics instead of this helper contract
# TR: ROBOTS YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / build_robots_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'build_robots_no_row_payload' için robots’a özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham robots SQL semantiğini tekrar etmek yerine okunabilir robots yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı robots SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen robots-odaklı sonuç şekli
# TR: - bu; yapılı payload, allow/block karar şekli, cache/refresh şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle robots’a özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham robots SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This robots gateway function named build_robots_no_row_payload defines a visible contract point for policy lookup or policy shaping.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand which host or URL policy build_robots_no_row_payload reads, how it interprets it, and what safe result it returns.
# EN: STAGE21-AUTO-COMMENT :: When editing build_robots_no_row_payload, verify that caller expectations, database truth, and worker semantics remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the entry point easy to find during robots-policy audits.
# TR: STAGE21-AUTO-COMMENT :: build_robots_no_row_payload isimli bu robots gateway fonksiyonu politika okuma veya politika biçimlendirme için görünür bir sözleşme noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu build_robots_no_row_payload fonksiyonunun hangi host veya URL politikasını okuduğunu, bunu nasıl yorumladığını ve hangi güvenli sonucu döndürdüğünü anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: build_robots_no_row_payload düzenlenirken çağıran beklentilerinin, veritabanı gerçeğinin ve worker anlamının hizalı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret giriş noktasını robots politika denetimlerinde kolay bulunur halde tutar.
# EN: REAL-RULE AST REPAIR / DEF build_robots_no_row_payload
# EN: build_robots_no_row_payload is an explicit robots-gateway helper/runtime contract.
# EN: Parameters kept explicit here: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message.
# TR: REAL-RULE AST REPAIR / FONKSIYON build_robots_no_row_payload
# TR: build_robots_no_row_payload acik bir robots-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: action, host_id, url_path, robots_url, cache_state, http_status, error_class, error_message.
def build_robots_no_row_payload(
    *,
    action: str,
    host_id: int,
    url_path: str | None = None,
    robots_url: str | None = None,
    cache_state: str | None = None,
    http_status: int | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, Any]:
    # EN: We keep one normalized degraded payload shape across robots wrappers so
    # EN: caller-visible results stay explicit and consistent.
    # TR: Robots wrapper'ları arasında tek ve normalize bir degrade payload şekli
    # TR: tutuyoruz; böylece çağıranın gördüğü sonuç açık ve tutarlı kalır.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
    # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return {
        "host_id": host_id,
        "url_path": url_path,
        "robots_url": robots_url,
        "cache_state": cache_state,
        "http_status": http_status,
        "robots_action": action,
        "robots_degraded": True,
        "robots_degraded_reason": f"{action}_returned_no_row",
        "robots_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }


# EN: This helper asks the DB whether the current path appears allowed/blocked
# EN: according to the visible robots decision surface.
# TR: Bu yardımcı, görünür robots karar yüzeyine göre mevcut path'in allowed/blocked
# TR: görünüp görünmediğini veritabanına sorar.
# EN: ROBOTS HELPER PURPOSE MEMORY BLOCK V5 / compute_robots_allow_decision
# EN:
# EN: Why this helper exists:
# EN: - because robots-specific DB truth for 'compute_robots_allow_decision' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable robots helper name instead of repeating raw robots SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, host_id, url_path
# EN: - values should match the current Python signature and the live robots SQL contract below
# EN:
# EN: Accepted output:
# EN: - a robots-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an allow/block decision shape, a cache/refresh shape, or another explicit branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely exposes allow/block verdict truth or robots decision visibility
# EN: - agent identity, path identity, or cached robots truth may matter here
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw robots SQL semantics instead of this helper contract
# TR: ROBOTS YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / compute_robots_allow_decision
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'compute_robots_allow_decision' için robots’a özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham robots SQL semantiğini tekrar etmek yerine okunabilir robots yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, host_id, url_path
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı robots SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen robots-odaklı sonuç şekli
# TR: - bu; yapılı payload, allow/block karar şekli, cache/refresh şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle allow/block verdict doğrusunu veya robots karar görünürlüğünü açığa çıkarır
# TR: - agent kimliği, path kimliği veya cache’lenmiş robots doğrusu burada önemli olabilir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham robots SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This robots gateway function named compute_robots_allow_decision defines a visible contract point for policy lookup or policy shaping.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand which host or URL policy compute_robots_allow_decision reads, how it interprets it, and what safe result it returns.
# EN: STAGE21-AUTO-COMMENT :: When editing compute_robots_allow_decision, verify that caller expectations, database truth, and worker semantics remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the entry point easy to find during robots-policy audits.
# TR: STAGE21-AUTO-COMMENT :: compute_robots_allow_decision isimli bu robots gateway fonksiyonu politika okuma veya politika biçimlendirme için görünür bir sözleşme noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu compute_robots_allow_decision fonksiyonunun hangi host veya URL politikasını okuduğunu, bunu nasıl yorumladığını ve hangi güvenli sonucu döndürdüğünü anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: compute_robots_allow_decision düzenlenirken çağıran beklentilerinin, veritabanı gerçeğinin ve worker anlamının hizalı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret giriş noktasını robots politika denetimlerinde kolay bulunur halde tutar.
# EN: REAL-RULE AST REPAIR / DEF compute_robots_allow_decision
# EN: compute_robots_allow_decision is an explicit robots-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, host_id, url_path.
# TR: REAL-RULE AST REPAIR / FONKSIYON compute_robots_allow_decision
# TR: compute_robots_allow_decision acik bir robots-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, host_id, url_path.
def compute_robots_allow_decision(
    conn: psycopg.Connection,
    host_id: int,
    url_path: str,
) -> dict[str, Any] | None:
    # EN: We open a cursor for one isolated decision query.
    # TR: Tek bir izole karar sorgusu için cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement belongs to the visible robots gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface affects crawl safety.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intent and wider policy meaning stay aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact gateway code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür robots gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey crawl güvenliğini etkiler.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş politika anlamı hizalı kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık gateway kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We call the visible allow-decision function because the worker
        # EN: contract explicitly says robots must not be silently ignored.
        # TR: Worker sözleşmesi robots'ın sessizce yok sayılamayacağını açıkça
        # TR: söylediği için görünür allow-decision fonksiyonunu çağırıyoruz.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway action, often a call that advances robots lookup or policy shaping.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because compact calls can hide important policy effects.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the action still belongs in the gateway layer and still matches robots intent.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that a meaningful operational effect happens here.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan bir gateway eylemi gerçekleştirir; çoğu zaman robots okumasını veya politika biçimlendirmeyi ilerleten bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık çağrılar önemli politika etkilerini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse eylemin hâlâ gateway katmanına ait olduğu ve robots niyetiyle eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya burada anlamlı bir operasyonel etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT *
            FROM http_fetch.compute_robots_allow_decision(
                p_host_id => %(host_id)s,
                p_url_path => %(url_path)s
            )
            """,
            {
                "host_id": host_id,
                "url_path": url_path,
            },
        )

        # EN: We fetch one decision row because this function describes the
        # EN: current decision for one host/path pair.
        # TR: Tek karar satırı çekiyoruz; çünkü bu fonksiyon bir host/path çifti
        # TR: için mevcut kararı tanımlar.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the robots-policy gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of silently becoming an implicit block/allow drift.
    # TR: No-row yanıtı sessizce örtük block/allow drift'ine dönüşmek yerine
    # TR: operatörün görebileceği degrade payload'a dönmelidir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects robots behavior based on current policy truth, cache state, or fallback conditions.
    # EN: STAGE21-AUTO-COMMENT :: Small branch changes here can alter whether the crawler waits, allows, denies, or refreshes policy.
    # EN: STAGE21-AUTO-COMMENT :: Review every path carefully when changing this condition because robots logic is safety-critical.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision point with direct politeness impact.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut politika gerçeğine, cache durumuna veya geri dönüş koşullarına göre robots davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Buradaki küçük dal değişiklikleri crawler'ın bekleyip beklemeyeceğini, izin verip vermeyeceğini, engelleyip engellemeyeceğini veya politikayı yenileyip yenilemeyeceğini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşul değiştirilirken her yol dikkatle incelenmelidir çünkü robots mantığı güvenlik açısından kritiktir.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret nezaket davranışına doğrudan etkisi olan bir karar noktasını vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
        # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_robots_no_row_payload(
            action="compute_robots_allow_decision",
            host_id=host_id,
            url_path=url_path,
            error_class="robots_allow_decision_no_row",
            error_message="http_fetch.compute_robots_allow_decision(...) returned no row",
        )

    # EN: We return the raw mapping for now to avoid pretending the final
    # EN: dedicated Python-side robots model is already sealed.
    # TR: Ayrı ve nihai Python-tarafı robots modelinin şimdiden mühürlü olduğunu
    # TR: varsaymamak için şimdilik ham mapping döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
    # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row



# EN: This helper asks the DB whether the current robots cache truth for one host
# EN: should be refreshed right now according to the sealed SQL contract.
# TR: Bu yardımcı, mühürlü SQL sözleşmesine göre tek bir host için mevcut robots
# TR: cache doğrusunun şu anda yenilenmesi gerekip gerekmediğini veritabanına sorar.
# EN: ROBOTS HELPER PURPOSE MEMORY BLOCK V5 / compute_robots_refresh_decision
# EN:
# EN: Why this helper exists:
# EN: - because robots-specific DB truth for 'compute_robots_refresh_decision' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable robots helper name instead of repeating raw robots SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, host_id
# EN: - values should match the current Python signature and the live robots SQL contract below
# EN:
# EN: Accepted output:
# EN: - a robots-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an allow/block decision shape, a cache/refresh shape, or another explicit branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely deals with cached robots truth, refresh need, or staleness visibility
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw robots SQL semantics instead of this helper contract
# TR: ROBOTS YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / compute_robots_refresh_decision
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'compute_robots_refresh_decision' için robots’a özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham robots SQL semantiğini tekrar etmek yerine okunabilir robots yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, host_id
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı robots SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen robots-odaklı sonuç şekli
# TR: - bu; yapılı payload, allow/block karar şekli, cache/refresh şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle cache’lenmiş robots doğrusu, refresh ihtiyacı veya stale görünürlüğü ile ilgilidir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham robots SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This robots gateway function named compute_robots_refresh_decision defines a visible contract point for policy lookup or policy shaping.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand which host or URL policy compute_robots_refresh_decision reads, how it interprets it, and what safe result it returns.
# EN: STAGE21-AUTO-COMMENT :: When editing compute_robots_refresh_decision, verify that caller expectations, database truth, and worker semantics remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the entry point easy to find during robots-policy audits.
# TR: STAGE21-AUTO-COMMENT :: compute_robots_refresh_decision isimli bu robots gateway fonksiyonu politika okuma veya politika biçimlendirme için görünür bir sözleşme noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu compute_robots_refresh_decision fonksiyonunun hangi host veya URL politikasını okuduğunu, bunu nasıl yorumladığını ve hangi güvenli sonucu döndürdüğünü anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: compute_robots_refresh_decision düzenlenirken çağıran beklentilerinin, veritabanı gerçeğinin ve worker anlamının hizalı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret giriş noktasını robots politika denetimlerinde kolay bulunur halde tutar.
# EN: REAL-RULE AST REPAIR / DEF compute_robots_refresh_decision
# EN: compute_robots_refresh_decision is an explicit robots-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, host_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON compute_robots_refresh_decision
# TR: compute_robots_refresh_decision acik bir robots-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, host_id.
def compute_robots_refresh_decision(
    conn: psycopg.Connection,
    host_id: int,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is a single read-only decision query.
    # TR: Bu tek ve salt-okunur karar sorgusu olduğu için izole bir cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement belongs to the visible robots gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface affects crawl safety.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intent and wider policy meaning stay aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact gateway code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür robots gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey crawl güvenliğini etkiler.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş politika anlamı hizalı kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık gateway kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We call the exact sealed SQL function instead of inventing Python-side
        # EN: refresh logic, because the DB contract already defines the truth.
        # TR: Python tarafında yeni refresh mantığı uydurmak yerine mühürlü SQL
        # TR: fonksiyonunu doğrudan çağırıyoruz; çünkü doğruluk zaten DB sözleşmesinde tanımlı.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway action, often a call that advances robots lookup or policy shaping.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because compact calls can hide important policy effects.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the action still belongs in the gateway layer and still matches robots intent.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that a meaningful operational effect happens here.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan bir gateway eylemi gerçekleştirir; çoğu zaman robots okumasını veya politika biçimlendirmeyi ilerleten bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık çağrılar önemli politika etkilerini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse eylemin hâlâ gateway katmanına ait olduğu ve robots niyetiyle eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya burada anlamlı bir operasyonel etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT *
            FROM http_fetch.compute_robots_refresh_decision(
                p_host_id => %(host_id)s
            )
            """,
            {
                "host_id": host_id,
            },
        )

        # EN: We fetch one row because this function returns the current refresh
        # EN: decision for exactly one host.
        # TR: Tek satır çekiyoruz; çünkü bu fonksiyon tam olarak tek bir host için
        # TR: mevcut refresh kararını döndürür.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the robots-policy gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of crashing the parent worker path.
    # TR: No-row yanıtı parent worker yolunu çökertmek yerine operatörün
    # TR: görebileceği degrade payload'a dönmelidir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects robots behavior based on current policy truth, cache state, or fallback conditions.
    # EN: STAGE21-AUTO-COMMENT :: Small branch changes here can alter whether the crawler waits, allows, denies, or refreshes policy.
    # EN: STAGE21-AUTO-COMMENT :: Review every path carefully when changing this condition because robots logic is safety-critical.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision point with direct politeness impact.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut politika gerçeğine, cache durumuna veya geri dönüş koşullarına göre robots davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Buradaki küçük dal değişiklikleri crawler'ın bekleyip beklemeyeceğini, izin verip vermeyeceğini, engelleyip engellemeyeceğini veya politikayı yenileyip yenilemeyeceğini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşul değiştirilirken her yol dikkatle incelenmelidir çünkü robots mantığı güvenlik açısından kritiktir.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret nezaket davranışına doğrudan etkisi olan bir karar noktasını vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
        # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_robots_no_row_payload(
            action="compute_robots_refresh_decision",
            host_id=host_id,
            error_class="robots_refresh_decision_no_row",
            error_message="http_fetch.compute_robots_refresh_decision(...) returned no row",
        )

    # EN: We return the raw mapping for now so Python does not pretend that a
    # EN: stricter dedicated model is already sealed.
    # TR: Python tarafı henüz daha katı özel bir model mühürlenmiş gibi davranmasın
    # TR: diye şimdilik ham mapping'i döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
    # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row



# EN: This helper writes one robots cache truth row through the canonical SQL
# EN: upsert function and returns the structured DB result row.
# TR: Bu yardımcı tek bir robots cache doğrusu satırını kanonik SQL upsert
# TR: fonksiyonu üzerinden yazar ve yapılı DB sonuç satırını döndürür.
# EN: ROBOTS HELPER PURPOSE MEMORY BLOCK V5 / upsert_robots_txt_cache
# EN:
# EN: Why this helper exists:
# EN: - because robots-specific DB truth for 'upsert_robots_txt_cache' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable robots helper name instead of repeating raw robots SQL semantics
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, host_id, robots_url, cache_state, http_status, fetched_at, expires_at, etag, last_modified, raw_storage_path, raw_sha256, raw_bytes, parsed_rules, sitemap_urls, crawl_delay_seconds, error_class, error_message, robots_metadata
# EN: - values should match the current Python signature and the live robots SQL contract below
# EN:
# EN: Accepted output:
# EN: - a robots-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an allow/block decision shape, a cache/refresh shape, or another explicit branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely deals with cached robots truth, refresh need, or staleness visibility
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw robots SQL semantics instead of this helper contract
# TR: ROBOTS YARDIMCISI AMAÇ HAFIZA BLOĞU V5 / upsert_robots_txt_cache
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'upsert_robots_txt_cache' için robots’a özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham robots SQL semantiğini tekrar etmek yerine okunabilir robots yardımcı adı çağırmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, host_id, robots_url, cache_state, http_status, fetched_at, expires_at, etag, last_modified, raw_storage_path, raw_sha256, raw_bytes, parsed_rules, sitemap_urls, crawl_delay_seconds, error_class, error_message, robots_metadata
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı robots SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen robots-odaklı sonuç şekli
# TR: - bu; yapılı payload, allow/block karar şekli, cache/refresh şekli veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle cache’lenmiş robots doğrusu, refresh ihtiyacı veya stale görünürlüğü ile ilgilidir
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham robots SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This robots gateway function named upsert_robots_txt_cache defines a visible contract point for policy lookup or policy shaping.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand which host or URL policy upsert_robots_txt_cache reads, how it interprets it, and what safe result it returns.
# EN: STAGE21-AUTO-COMMENT :: When editing upsert_robots_txt_cache, verify that caller expectations, database truth, and worker semantics remain aligned.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the entry point easy to find during robots-policy audits.
# TR: STAGE21-AUTO-COMMENT :: upsert_robots_txt_cache isimli bu robots gateway fonksiyonu politika okuma veya politika biçimlendirme için görünür bir sözleşme noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu upsert_robots_txt_cache fonksiyonunun hangi host veya URL politikasını okuduğunu, bunu nasıl yorumladığını ve hangi güvenli sonucu döndürdüğünü anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: upsert_robots_txt_cache düzenlenirken çağıran beklentilerinin, veritabanı gerçeğinin ve worker anlamının hizalı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret giriş noktasını robots politika denetimlerinde kolay bulunur halde tutar.
# EN: REAL-RULE AST REPAIR / DEF upsert_robots_txt_cache
# EN: upsert_robots_txt_cache is an explicit robots-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, host_id, robots_url, cache_state, http_status, fetched_at, expires_at, etag, last_modified, raw_storage_path, raw_sha256, raw_bytes, parsed_rules, sitemap_urls, crawl_delay_seconds, error_class, error_message, robots_metadata.
# TR: REAL-RULE AST REPAIR / FONKSIYON upsert_robots_txt_cache
# TR: upsert_robots_txt_cache acik bir robots-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, host_id, robots_url, cache_state, http_status, fetched_at, expires_at, etag, last_modified, raw_storage_path, raw_sha256, raw_bytes, parsed_rules, sitemap_urls, crawl_delay_seconds, error_class, error_message, robots_metadata.
def upsert_robots_txt_cache(
    conn: psycopg.Connection,
    *,
    host_id: int,
    robots_url: str,
    cache_state: str,
    http_status: int | None = None,
    fetched_at: Any = None,
    expires_at: Any = None,
    etag: str | None = None,
    last_modified: str | None = None,
    raw_storage_path: str | None = None,
    raw_sha256: str | None = None,
    raw_bytes: int | None = None,
    parsed_rules: dict[str, Any] | None = None,
    sitemap_urls: list[Any] | None = None,
    crawl_delay_seconds: Any = None,
    error_class: str | None = None,
    error_message: str | None = None,
    robots_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # EN: We import json locally because only this helper needs to serialize
    # EN: Python dict/list values into jsonb-safe text parameters.
    # TR: json modülünü yerel olarak içe aktarıyoruz; çünkü yalnızca bu yardımcı
    # TR: Python dict/list değerlerini jsonb-uyumlu metin parametrelerine serileştirir.
    # EN: STAGE21-AUTO-COMMENT :: This import line declares robots gateway dependencies by bringing in json.
    # EN: STAGE21-AUTO-COMMENT :: Imports here reveal which contracts, helpers, or database tools shape robots decisions before the worker sees them.
    # EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether policy meaning or gateway responsibility changed as well.
    # EN: STAGE21-AUTO-COMMENT :: This marker treats imports as design evidence rather than boilerplate.
    # TR: STAGE21-AUTO-COMMENT :: Bu import satırı json ögelerini içeri alarak robots gateway bağımlılıklarını bildirir.
    # TR: STAGE21-AUTO-COMMENT :: Buradaki importlar worker görmeden önce robots kararlarını hangi sözleşmelerin, yardımcıların veya veritabanı araçlarının şekillendirdiğini gösterir.
    # TR: STAGE21-AUTO-COMMENT :: Importlar değişirse politika anlamının veya gateway sorumluluğunun da değişip değişmediği incelenmelidir.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret importları şablon değil tasarım kanıtı olarak ele alır.
    import json

    # EN: We serialize JSON-shaped inputs only when they are provided.
    # EN: None stays None so the SQL function can apply its own defaults honestly.
    # TR: JSON-biçimli girdileri yalnızca gerçekten verilmişlerse serileştiriyoruz.
    # TR: None değeri None kalır; böylece SQL fonksiyonu kendi default'larını dürüstçe uygulayabilir.
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates parsed_rules_json as part of the robots-policy gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama parsed_rules_json değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
    parsed_rules_json = None if parsed_rules is None else json.dumps(parsed_rules)
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates sitemap_urls_json as part of the robots-policy gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama sitemap_urls_json değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
    sitemap_urls_json = None if sitemap_urls is None else json.dumps(sitemap_urls)
    # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates robots_metadata_json as part of the robots-policy gateway flow.
    # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
    # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
    # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
    # TR: STAGE21-AUTO-COMMENT :: Bu atama robots_metadata_json değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
    # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
    robots_metadata_json = None if robots_metadata is None else json.dumps(robots_metadata)

    # EN: We open a cursor because this helper executes one explicit canonical SQL
    # EN: statement inside the caller's current transaction.
    # TR: Bu yardımcı çağıranın mevcut transaction'ı içinde tek bir açık kanonik SQL
    # TR: ifadesi çalıştırdığı için cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement belongs to the visible robots gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface affects crawl safety.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intent and wider policy meaning stay aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact gateway code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür robots gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey crawl güvenliğini etkiler.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş politika anlamı hizalı kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık gateway kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We call the sealed upsert function exactly, including its enum/jsonb
        # EN: parameter casts, so Python stays aligned with the SQL contract.
        # TR: Python tarafı SQL sözleşmesiyle hizalı kalsın diye mühürlü upsert
        # TR: fonksiyonunu enum/jsonb cast'leriyle birlikte tam olarak çağırıyoruz.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct gateway action, often a call that advances robots lookup or policy shaping.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because compact calls can hide important policy effects.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the action still belongs in the gateway layer and still matches robots intent.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that a meaningful operational effect happens here.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan bir gateway eylemi gerçekleştirir; çoğu zaman robots okumasını veya politika biçimlendirmeyi ilerleten bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık çağrılar önemli politika etkilerini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse eylemin hâlâ gateway katmanına ait olduğu ve robots niyetiyle eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya burada anlamlı bir operasyonel etkinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT *
            FROM http_fetch.upsert_robots_txt_cache(
                p_host_id => %(host_id)s,
                p_robots_url => %(robots_url)s,
                p_cache_state => %(cache_state)s::http_fetch.robots_cache_state_enum,
                p_http_status => %(http_status)s,
                p_fetched_at => %(fetched_at)s,
                p_expires_at => %(expires_at)s,
                p_etag => %(etag)s,
                p_last_modified => %(last_modified)s,
                p_raw_storage_path => %(raw_storage_path)s,
                p_raw_sha256 => %(raw_sha256)s,
                p_raw_bytes => %(raw_bytes)s,
                p_parsed_rules => %(parsed_rules)s::jsonb,
                p_sitemap_urls => %(sitemap_urls)s::jsonb,
                p_crawl_delay_seconds => %(crawl_delay_seconds)s,
                p_error_class => %(error_class)s,
                p_error_message => %(error_message)s,
                p_robots_metadata => %(robots_metadata)s::jsonb
            )
            """,
            {
                "host_id": host_id,
                "robots_url": robots_url,
                "cache_state": cache_state,
                "http_status": http_status,
                "fetched_at": fetched_at,
                "expires_at": expires_at,
                "etag": etag,
                "last_modified": last_modified,
                "raw_storage_path": raw_storage_path,
                "raw_sha256": raw_sha256,
                "raw_bytes": raw_bytes,
                "parsed_rules": parsed_rules_json,
                "sitemap_urls": sitemap_urls_json,
                "crawl_delay_seconds": crawl_delay_seconds,
                "error_class": error_class,
                "error_message": error_message,
                "robots_metadata": robots_metadata_json,
            },
        )

        # EN: We fetch one row because the canonical upsert function returns one
        # EN: structured cache result row for one host.
        # TR: Tek satır çekiyoruz; çünkü kanonik upsert fonksiyonu tek bir host için
        # TR: tek yapılı cache sonuç satırı döndürür.
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the robots-policy gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often turn stored policy truth into worker-usable runtime values and should remain explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm downstream code still interprets allow, deny, freshness, and fallback behavior correctly.
        # EN: STAGE21-AUTO-COMMENT :: This marker shows where robots meaning becomes concrete runtime state.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini robots politika gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman kayıtlı politika gerçeğini worker'ın kullanabileceği runtime değerlerine dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde aşağı akış kodunun izin, engel, tazelik ve geri dönüş davranışını hâlâ doğru yorumladığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret robots anlamının somut runtime durumuna dönüştüğü yeri gösterir.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of crashing the worker-side robots refresh path again.
    # TR: No-row yanıtı worker-tarafı robots refresh yolunu yeniden çökertmek
    # TR: yerine operatörün görebileceği degrade payload'a dönmelidir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects robots behavior based on current policy truth, cache state, or fallback conditions.
    # EN: STAGE21-AUTO-COMMENT :: Small branch changes here can alter whether the crawler waits, allows, denies, or refreshes policy.
    # EN: STAGE21-AUTO-COMMENT :: Review every path carefully when changing this condition because robots logic is safety-critical.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision point with direct politeness impact.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut politika gerçeğine, cache durumuna veya geri dönüş koşullarına göre robots davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Buradaki küçük dal değişiklikleri crawler'ın bekleyip beklemeyeceğini, izin verip vermeyeceğini, engelleyip engellemeyeceğini veya politikayı yenileyip yenilemeyeceğini değiştirebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşul değiştirilirken her yol dikkatle incelenmelidir çünkü robots mantığı güvenlik açısından kritiktir.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret nezaket davranışına doğrudan etkisi olan bir karar noktasını vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
        # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_robots_no_row_payload(
            action="upsert_robots_txt_cache",
            host_id=host_id,
            robots_url=robots_url,
            cache_state=cache_state,
            http_status=http_status,
            error_class="robots_cache_upsert_no_row",
            error_message="http_fetch.upsert_robots_txt_cache(...) returned no row",
        )

    # EN: We return the structured DB row to the caller.
    # TR: Yapılı DB satırını çağırana döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete robots-policy result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines define the practical gateway contract that the runtime uses when deciding what can be fetched.
    # EN: STAGE21-AUTO-COMMENT :: When editing this line, verify that callers still receive the expected shape, safety meaning, and fallback semantics.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir robots politika sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları runtime'ın neyin çekilebileceğine karar verirken kullandığı pratik gateway sözleşmesini tanımlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen biçimi, güvenlik anlamını ve geri dönüş semantiğini almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row
