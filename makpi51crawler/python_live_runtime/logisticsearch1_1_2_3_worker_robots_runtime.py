"""
EN:
This file is the worker-robots child of the worker-runtime family.

EN:
Why this file exists:
- because robots-specific runtime truth should live in one explicit child instead of being hidden inside the main worker hub
- because robots allow/block meaning directly changes whether the worker may continue to page fetch or must stop early
- because a beginner should be able to find robots decision logic without digging through unrelated lease, fetch, parse, or finalize phases

EN:
What this file DOES:
- expose worker-robots-oriented runtime helper boundaries
- preserve visible robots_refresh, allow, block, cache, and degraded branch meaning
- keep robots-specific semantics separate from broader worker orchestration

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not own all lease logic
- it does not own all acquisition logic
- it does not own all parse/finalize logic

EN:
Topological role:
- the main worker runtime hub sits above this file
- this file owns narrow robots-side runtime semantics
- sibling worker submodules own other focused contracts such as lease, acquisition, parse, finalize, and storage

EN:
Important visible values and shapes:
- robots_refresh_decision => whether robots data should be refreshed now
- robots_allow_decision or robots_verdict => readable allow/block truth for the claimed work item
- phase_label => values such as robots_refresh or page_fetch that explain where the worker is
- degraded branch payloads => explicit non-happy robots-side outcomes that must remain visible

EN:
Accepted architectural identity:
- worker robots runtime child
- narrow robots contract layer
- readable robots allow/block boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague policy utility dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya worker-runtime ailesinin worker-robots child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü robotse özgü runtime doğrusu ana worker hubının içinde gizlenmek yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü robots allow/block anlamı workerın page fetch fazına devam edip edemeyeceğini veya erken durması gerekip gerekmediğini doğrudan değiştirir
- çünkü yeni başlayan biri robots karar mantığını ilgisiz lease, fetch, parse veya finalize fazları arasında kaybolmadan bulabilmelidir

TR:
Bu dosya NE yapar:
- worker-robots odaklı runtime yardımcı sınırlarını açığa çıkarır
- robots_refresh, allow, block, cache ve degraded dal anlamını görünür tutar
- robotse özgü semantiklerini daha geniş worker orkestrasyonundan ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tüm lease mantığının sahibi değildir
- tüm acquisition mantığının sahibi değildir
- tüm parse/finalize mantığının sahibi değildir

TR:
Topolojik rol:
- ana worker runtime hubı bu dosyanın üstündedir
- bu dosya dar robots tarafı runtime semantiklerini taşır
- kardeş worker altmodülleri lease, acquisition, parse, finalize ve storage gibi diğer odaklı sözleşmeleri taşır

TR:
Önemli görünür değerler ve şekiller:
- robots_refresh_decision => robots verisinin şimdi yenilenip yenilenmeyeceği
- robots_allow_decision veya robots_verdict => claim edilmiş iş öğesi için okunabilir allow/block doğrusu
- phase_label => workerın nerede olduğunu anlatan robots_refresh veya page_fetch gibi değerler
- degraded dal payloadları => görünür kalması gereken mutlu-yol-dışı robots tarafı sonuçlar

TR:
Kabul edilen mimari kimlik:
- worker robots runtime child
- dar robots sözleşme katmanı
- okunabilir robots allow/block sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz policy utility çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module owns worker-side robots decision helpers that are more than
# EN: pure orchestration but narrower than the parent worker runtime.
# TR: Bu modül worker-tarafı robots karar yardımcılarını sahiplenir; bunlar saf
# TR: orchestration’dan fazladır ama parent worker runtime’dan daha dardır.

# EN: WORKER ROBOTS RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow robots corner of the worker corridor.
# EN: Beginner mental model:
# EN: - the main worker runtime file is the main room
# EN: - this file is the labeled robots desk inside that larger runtime building
# EN: - it exists so allow/block meaning does not become vague or silently disappear
# EN:
# EN: Accepted architectural meaning:
# EN: - named robots-runtime child
# EN: - focused allow/block and refresh helper surface
# EN: - readable branch boundary for robots-side outcomes
# EN:
# EN: Undesired architectural meaning:
# EN: - random policy helper pile
# EN: - hidden second orchestrator
# EN: - place where robots failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - robots verdicts should stay explicit
# EN: - allow/block decisions should stay structured and readable
# EN: - degraded robots branches must remain visible
# TR: WORKER ROBOTS RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar robots köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - ana worker runtime dosyası ana odadır
# TR: - bu dosya o daha büyük runtime binası içindeki etiketli robots masasıdır
# TR: - allow/block anlamı belirsizleşmesin veya sessizce kaybolmasın diye vardır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli robots-runtime child
# TR: - odaklı allow/block ve refresh yardımcı yüzeyi
# TR: - robots tarafı sonuçlar için okunabilir dal sınırı
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele policy helper yığını
# TR: - gizli ikinci orchestrator
# TR: - robots hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - robots verdictleri açık kalmalıdır
# TR: - allow/block kararları yapılı ve okunabilir kalmalıdır
# TR: - degraded robots dalları görünür kalmalıdır

from __future__ import annotations

# EN: We import datetime because robots fetch timestamps come back as ISO text and
# EN: must be converted into explicit datetime objects for psycopg.
# TR: Robots fetch zamanları ISO metni olarak döndüğü ve psycopg için açık
# TR: datetime nesnelerine çevrilmesi gerektiği için datetime içe aktarıyoruz.
from datetime import datetime

# EN: We import Path because persisted robots artefacts must be read back from
# EN: disk during worker-side payload derivation.
# TR: Saklanan robots artefact’larının worker-tarafı payload türetimi sırasında
# TR: diskten geri okunması gerektiği için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import the stable acquisition-family public surface because this child
# EN: needs robots fetch/parse helpers plus canonical claimed-url field access.
# TR: Bu alt yüzey robots fetch/parse yardımcılarına ve kanonik claimed-url alan
# TR: erişimine ihtiyaç duyduğu için kararlı acquisition-aile public yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    FetchedRobotsTxtResult,
    decode_robots_body,
    fetch_robots_txt_to_raw_storage,
    get_claimed_url_value,
    parse_robots_txt_text,
)

# EN: We import the canonical robots cache upsert gateway because durable cache
# EN: truth must still be written through the sealed SQL surface.
# TR: Kalıcı robots cache doğrusu yine mühürlü SQL yüzeyi üzerinden yazılmalı
# TR: olduğu için kanonik robots cache upsert gateway’ini içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    upsert_robots_txt_cache,
)

# EN: We import the strict fetched-robots contract validator so worker-side cache
# EN: refresh cannot trust corrupted artefact metadata blindly.
# TR: Worker-tarafı cache refresh bozuk artefact metadata'sına körü körüne
# TR: güvenmesin diye sıkı fetched-robots contract validator'ını içe aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    validate_fetched_robots_result_contract,
)


# EN: This helper decides whether the current robots verdict still allows a real
# EN: page fetch in the minimal worker.
# TR: Bu yardımcı mevcut robots verdict’inin minimal worker’da gerçek page fetch’e
# TR: hâlâ izin verip vermediğini belirler.
# EN: WORKER ROBOTS FUNCTION PURPOSE MEMORY BLOCK V6 / robots_verdict_allows_fetch
# EN:
# EN: Why this function exists:
# EN: - because worker-robots truth for 'robots_verdict_allows_fetch' should be exposed through one named top-level helper boundary
# EN: - because robots-side runtime semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: verdict
# EN: - values should match the current Python signature and the robots contract below
# EN:
# EN: Accepted output:
# EN: - a worker-robots-oriented result shape defined by the current function body
# EN: - this may be a structured robots payload, a verdict shape, a refresh result, or another explicit robots-side branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely deals with robots refresh, robots verdict, or allow/block visibility
# EN: - explicit allow vs block meaning and degraded robots behavior may matter here
# EN: - these helpers often protect crawl politeness and compliance
# EN: - visible success vs deny distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is robots-side helper logic, not the whole worker corridor
# EN: - robots results must stay explicit so compliance, denial, degradation, and recovery meaning are easy to understand
# EN:
# EN: Undesired behavior:
# EN: - silent allow/block mutation
# EN: - vague robots results that hide branch meaning
# TR: WORKER ROBOTS FUNCTION AMAÇ HAFIZA BLOĞU V6 / robots_verdict_allows_fetch
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'robots_verdict_allows_fetch' için worker-robots doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü robots tarafı runtime semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: verdict
# TR: - değerler aşağıdaki mevcut Python imzası ve robots sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-robots odaklı sonuç şekli
# TR: - bu; yapılı robots payloadı, verdict şekli, refresh sonucu veya başka açık robots tarafı dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle robots refresh, robots verdict veya allow/block görünürlüğü ile ilgilenir
# TR: - açık allow vs block anlamı ve degraded robots davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman crawl politeness ve uyumluluğu korur
# TR: - görünür success vs deny ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon robots tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - robots sonuçları açık kalmalıdır ki uyumluluk, engel, degraded durum ve recovery anlamı kolay anlaşılsın
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz allow/block değişimi
# TR: - dal anlamını gizleyen belirsiz robots sonuçları

# EN: Function contract for robots_verdict_allows_fetch.
# EN: This helper turns one robots-side verdict into a narrow yes/no fetch continuation answer.
# EN: - verdict => robots verdict text/object whose allow/block meaning is normalized here.
# TR: robots_verdict_allows_fetch için fonksiyon sözleşmesi.
# TR: Bu yardımcı tek bir robots tarafı verdict değerini dar bir fetch-devam evet/hayır cevabına dönüştürür.
# TR: - verdict => allow/block anlamı burada normalize edilen robots verdict metni/nesnesi.
def robots_verdict_allows_fetch(verdict: str | None) -> bool:
    # EN: These verdicts are currently treated as fetch-allowed by the minimal
    # EN: worker contract.
    # TR: Bu verdict’ler mevcut minimal worker sözleşmesi tarafından fetch-allowed
    # TR: kabul edilir.
    return verdict in {
        "allow",
        "allow_but_refresh_recommended",
        "allow_mode_ignore",
    }


# EN: This helper converts a persisted robots fetch artefact into the narrow
# EN: parsed payload shape expected by the DB cache contract.
# TR: Bu yardımcı saklanan robots fetch artefact’ını DB cache sözleşmesinin
# TR: beklediği dar parse payload şekline dönüştürür.
# EN: WORKER ROBOTS FUNCTION PURPOSE MEMORY BLOCK V6 / parse_persisted_robots_payload
# EN:
# EN: Why this function exists:
# EN: - because worker-robots truth for 'parse_persisted_robots_payload' should be exposed through one named top-level helper boundary
# EN: - because robots-side runtime semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: robots_fetch
# EN: - values should match the current Python signature and the robots contract below
# EN:
# EN: Accepted output:
# EN: - a worker-robots-oriented result shape defined by the current function body
# EN: - this may be a structured robots payload, a verdict shape, a refresh result, or another explicit robots-side branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely deals with robots refresh, robots verdict, or allow/block visibility
# EN: - explicit allow vs block meaning and degraded robots behavior may matter here
# EN: - these helpers often protect crawl politeness and compliance
# EN: - visible success vs deny distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is robots-side helper logic, not the whole worker corridor
# EN: - robots results must stay explicit so compliance, denial, degradation, and recovery meaning are easy to understand
# EN:
# EN: Undesired behavior:
# EN: - silent allow/block mutation
# EN: - vague robots results that hide branch meaning
# TR: WORKER ROBOTS FUNCTION AMAÇ HAFIZA BLOĞU V6 / parse_persisted_robots_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'parse_persisted_robots_payload' için worker-robots doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü robots tarafı runtime semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: robots_fetch
# TR: - değerler aşağıdaki mevcut Python imzası ve robots sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-robots odaklı sonuç şekli
# TR: - bu; yapılı robots payloadı, verdict şekli, refresh sonucu veya başka açık robots tarafı dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle robots refresh, robots verdict veya allow/block görünürlüğü ile ilgilenir
# TR: - açık allow vs block anlamı ve degraded robots davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman crawl politeness ve uyumluluğu korur
# TR: - görünür success vs deny ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon robots tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - robots sonuçları açık kalmalıdır ki uyumluluk, engel, degraded durum ve recovery anlamı kolay anlaşılsın
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz allow/block değişimi
# TR: - dal anlamını gizleyen belirsiz robots sonuçları

# EN: Function contract for parse_persisted_robots_payload.
# EN: This helper reshapes one persisted robots fetch payload into readable runtime-side robots text/metadata meaning.
# EN: - robots_fetch => persisted robots fetch payload/contract that may contain raw storage path, bytes, and metadata.
# TR: parse_persisted_robots_payload için fonksiyon sözleşmesi.
# TR: Bu yardımcı kalıcı robots fetch payloadını okunabilir runtime tarafı robots metni/metadata anlamına dönüştürür.
# TR: - robots_fetch => ham saklama yolu, byte içeriği ve metadata taşıyabilen kalıcı robots fetch payloadı/sözleşmesi.
def parse_persisted_robots_payload(
    robots_fetch: FetchedRobotsTxtResult,
) -> tuple[dict, list[str], float | None]:
    # EN: The persisted raw path must exist on this code path because this helper
    # EN: is only used for body-present robots results.
    # TR: Bu kod yolunda saklanan ham yol mevcut olmalıdır; çünkü bu yardımcı
    # TR: yalnızca body mevcut olan robots sonuçlarında kullanılır.
# EN: raw_storage_path keeps the persisted raw robots artifact path when the fetch payload exposes one.
# TR: raw_storage_path fetch payloadı sunuyorsa kalıcı ham robots artefact yolunu tutar.
    raw_storage_path = robots_fetch.raw_storage_path
    if raw_storage_path is None:
        raise RuntimeError("robots fetch returned no raw_storage_path for payload parsing")

    # EN: We read the exact persisted bytes so later audits can inspect the same
    # EN: durable artefact the parser used.
    # TR: Daha sonraki audit’ler parser’ın kullandığı aynı kalıcı artefact’ı
    # TR: inceleyebilsin diye tam saklanan byte’ları okuyoruz.
# EN: robots_body keeps the raw robots body bytes/content loaded from the persisted source.
# TR: robots_body kalıcı kaynaktan yüklenen ham robots gövde byte/içeriğini tutar.
    robots_body = Path(raw_storage_path).read_bytes()

    # EN: We decode through the sealed helper so encoding tolerance stays
    # EN: consistent with the acquisition family.
    # TR: Encoding toleransı acquisition ailesiyle tutarlı kalsın diye decode
    # TR: işlemini mühürlü yardımcı üzerinden yapıyoruz.
# EN: robots_text keeps the decoded text form used by downstream robots parsing logic.
# TR: robots_text aşağı akış robots parse mantığında kullanılan decode edilmiş metin biçimini tutar.
    robots_text = decode_robots_body(robots_body)

    # EN: We return the exact narrow parsed shape expected by the current DB
    # EN: cache-upsert contract.
    # TR: Mevcut DB cache-upsert sözleşmesinin beklediği tam dar parse şeklini
    # TR: döndürüyoruz.
    return parse_robots_txt_text(robots_text)


# EN: This helper performs one controlled robots refresh cycle and writes the
# EN: resulting cache truth through the canonical DB wrapper.
# TR: Bu yardımcı tek bir kontrollü robots refresh döngüsü çalıştırır ve ortaya
# TR: çıkan cache doğrusunu kanonik DB wrapper üzerinden yazar.
# EN: WORKER ROBOTS FUNCTION PURPOSE MEMORY BLOCK V6 / refresh_robots_cache_if_needed
# EN:
# EN: Why this function exists:
# EN: - because worker-robots truth for 'refresh_robots_cache_if_needed' should be exposed through one named top-level helper boundary
# EN: - because robots-side runtime semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, claimed_url, refresh_decision
# EN: - values should match the current Python signature and the robots contract below
# EN:
# EN: Accepted output:
# EN: - a worker-robots-oriented result shape defined by the current function body
# EN: - this may be a structured robots payload, a verdict shape, a refresh result, or another explicit robots-side branch result
# EN:
# EN: Common robots meaning hints:
# EN: - this helper likely deals with robots refresh, robots verdict, or allow/block visibility
# EN: - explicit allow vs block meaning and degraded robots behavior may matter here
# EN: - these helpers often protect crawl politeness and compliance
# EN: - visible success vs deny distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is robots-side helper logic, not the whole worker corridor
# EN: - robots results must stay explicit so compliance, denial, degradation, and recovery meaning are easy to understand
# EN:
# EN: Undesired behavior:
# EN: - silent allow/block mutation
# EN: - vague robots results that hide branch meaning
# TR: WORKER ROBOTS FUNCTION AMAÇ HAFIZA BLOĞU V6 / refresh_robots_cache_if_needed
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'refresh_robots_cache_if_needed' için worker-robots doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü robots tarafı runtime semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, claimed_url, refresh_decision
# TR: - değerler aşağıdaki mevcut Python imzası ve robots sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-robots odaklı sonuç şekli
# TR: - bu; yapılı robots payloadı, verdict şekli, refresh sonucu veya başka açık robots tarafı dal sonucu olabilir
# TR:
# TR: Ortak robots anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle robots refresh, robots verdict veya allow/block görünürlüğü ile ilgilenir
# TR: - açık allow vs block anlamı ve degraded robots davranışı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman crawl politeness ve uyumluluğu korur
# TR: - görünür success vs deny ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon robots tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - robots sonuçları açık kalmalıdır ki uyumluluk, engel, degraded durum ve recovery anlamı kolay anlaşılsın
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz allow/block değişimi
# TR: - dal anlamını gizleyen belirsiz robots sonuçları

# EN: Function contract for refresh_robots_cache_if_needed.
# EN: This helper decides and executes the narrow worker-side robots refresh corridor when refresh is actually required.
# EN: - conn => live database connection used for host lookup and cache write/update work.
# EN: - claimed_url => claimed work item whose host/context drives robots refresh behavior.
# EN: - refresh_decision => structured robots refresh decision that says whether refresh should happen now and why.
# TR: refresh_robots_cache_if_needed için fonksiyon sözleşmesi.
# TR: Bu yardımcı yalnızca gerçekten gerektiğinde dar worker-tarafı robots yenileme koridorunu çalıştırır.
# TR: - conn => host lookup ve cache yazma/güncelleme işi için kullanılan canlı veritabanı bağlantısı.
# TR: - claimed_url => robots yenileme davranışını belirleyen host/bağlamı taşıyan claim edilmiş iş öğesi.
# TR: - refresh_decision => robots yenilemenin şimdi gerekip gerekmediğini ve nedenini söyleyen yapılı karar payloadı.
def refresh_robots_cache_if_needed(
    conn,
    *,
    claimed_url: object,
    refresh_decision: dict,
) -> dict[str, object]:
    # EN: We extract the host identity because robots refresh is a host-level
    # EN: operation.
    # TR: Robots refresh host-seviyesinde bir işlem olduğu için host kimliğini
    # TR: çıkarıyoruz.
# EN: host_id stores the frontier/http-fetch host identity used by the robots cache corridor.
# TR: host_id robots cache koridorunun kullandığı frontier/http-fetch host kimliğini tutar.
    host_id = int(get_claimed_url_value(claimed_url, "host_id"))

    # EN: We read the robots URL from the DB decision row because SQL is already
    # EN: the source of truth for that target.
    # TR: Bu hedef için doğruluk kaynağı zaten SQL olduğu için robots URL’yi DB
    # TR: karar satırından okuyoruz.
# EN: robots_url stores the exact robots.txt URL derived for this host refresh attempt.
# TR: robots_url bu host yenileme denemesi için türetilen tam robots.txt URL değerini tutar.
    robots_url = refresh_decision.get("robots_url")
    if robots_url is None or str(robots_url).strip() == "":
        raise RuntimeError("compute_robots_refresh_decision(...) returned empty robots_url")

    # EN: We reuse the host-level user-agent token from the claimed row so robots
    # EN: refresh uses the same explicit crawler identity.
    # TR: Robots refresh aynı açık crawler kimliğini kullansın diye claimed
    # TR: satırdaki host-seviyesi user-agent token’ını yeniden kullanıyoruz.
# EN: user_agent_token stores the crawler user-agent token sent into robots acquisition logic.
# TR: user_agent_token robots acquisition mantığına verilen crawler user-agent token değerini tutar.
    user_agent_token = str(get_claimed_url_value(claimed_url, "user_agent_token"))

    # EN: We perform the real robots fetch through the canonical acquisition helper.
    # TR: Gerçek robots fetch işlemini kanonik acquisition yardımcısı üzerinden
    # TR: yapıyoruz.
# EN: robots_fetch stores the direct robots acquisition result returned by the acquisition corridor.
# TR: robots_fetch acquisition koridorundan dönen doğrudan robots edinim sonucunu tutar.
    robots_fetch = fetch_robots_txt_to_raw_storage(
        host_id=host_id,
        robots_url=str(robots_url),
        user_agent_token=user_agent_token,
    )

    # EN: We validate the fetched-robots contract immediately so corrupted raw
    # EN: artefacts cannot silently flow into parse/cache persistence.
    # TR: Bozuk ham artefact'lar sessizce parse/cache persistence yoluna akmasın
    # TR: diye fetched-robots contract'ını hemen doğruluyoruz.
# EN: robots_fetch_contract stores the normalized dict-like view of the robots fetch result.
# TR: robots_fetch_contract robots fetch sonucunun normalize edilmiş dict-benzeri görünümünü tutar.
    robots_fetch_contract = validate_fetched_robots_result_contract(robots_fetch)
    if robots_fetch_contract is not None:
        return {
            "host_id": host_id,
            "robots_url": str(robots_url),
            "robots_degraded": True,
            "robots_degraded_reason": "validate_fetched_robots_result_contract_failed",
            "robots_completed": False,
            "error_class": str(robots_fetch_contract["error_class"]),
            "error_message": str(robots_fetch_contract["error_message"]),
            "acquisition_contract": dict(robots_fetch_contract),
        }

    # EN: We convert fetched_at ISO text back into datetime so psycopg receives an
    # EN: explicit timestamptz-compatible value.
    # TR: psycopg açık timestamptz-uyumlu bir değer alsın diye fetched_at ISO
    # TR: metnini tekrar datetime nesnesine çeviriyoruz.
# EN: fetched_at_value stores the timestamp value associated with this robots fetch result.
# TR: fetched_at_value bu robots fetch sonucuna bağlı zaman damgası değerini tutar.
    fetched_at_value = datetime.fromisoformat(robots_fetch.fetched_at)

    # EN: We preserve a small visible metadata payload so later inspection can see
    # EN: where the fetch actually landed.
    # TR: Daha sonraki inceleme fetch’in gerçekte nereye indiğini görebilsin diye
    # TR: küçük bir görünür metadata payload’ı koruyoruz.
# EN: robots_metadata stores parsed metadata/details extracted from the robots fetch contract.
# TR: robots_metadata robots fetch sözleşmesinden çıkarılan parse edilmiş metadata/ayrıntıları tutar.
    robots_metadata = {
        "final_url": robots_fetch.final_url,
        "content_type": robots_fetch.content_type,
    }

    # EN: Transport-class failure means no reliable HTTP cache truth existed, so
    # EN: we persist an explicit error-state cache row.
    # TR: Taşıma-sınıfı hata güvenilir HTTP cache doğrusu oluşmadığı anlamına gelir;
    # TR: bu yüzden açık bir error-state cache satırı yazıyoruz.
    if robots_fetch.fetch_error_class is not None:
        return upsert_robots_txt_cache(
            conn,
            host_id=host_id,
            robots_url=str(robots_url),
            cache_state="error",
            http_status=None,
            fetched_at=fetched_at_value,
            expires_at=None,
            etag=None,
            last_modified=None,
            raw_storage_path=None,
            raw_sha256=None,
            raw_bytes=0,
            parsed_rules={},
            sitemap_urls=[],
            crawl_delay_seconds=None,
            error_class=robots_fetch.fetch_error_class,
            error_message=robots_fetch.fetch_error_message,
            robots_metadata=robots_metadata,
        )

    # EN: We start from an explicit empty parsed payload and only fill it for
    # EN: cacheable success-class outcomes.
    # TR: Açık boş bir parse payload ile başlıyor ve bunu yalnızca cache’lenebilir
    # TR: başarı-sınıfı sonuçlarda dolduruyoruz.
# EN: parsed_rules stores the normalized parsed robots rules structure extracted from the fetched robots material.
# TR: parsed_rules fetch edilen robots materyalinden çıkarılan normalize edilmiş parsed robots rules yapısını tutar.
    parsed_rules: dict = {}
# EN: sitemap_urls stores the sitemap URL list extracted from the parsed robots payload when present.
# TR: sitemap_urls varsa parse edilmiş robots payloadından çıkarılan sitemap URL listesini tutar.
    sitemap_urls: list[str] = []
# EN: crawl_delay_seconds stores the parsed crawl-delay value when robots rules expose one.
# TR: crawl_delay_seconds robots kuralları sunuyorsa parse edilmiş crawl-delay değerini tutar.
# EN: crawl_delay_seconds stores the numeric crawl-delay value extracted from the parsed robots metadata when present.
# TR: crawl_delay_seconds varsa parse edilmis robots metadata icinden cikarilan sayisal crawl-delay degerini tutar.
# EN: crawl_delay_seconds is the exact local variable that stores the normalized numeric crawl-delay value derived for robots cache persistence.
# TR: crawl_delay_seconds robots cache persistence icin turetilen normalize sayisal crawl-delay degerini tutan exact local degiskendir.
    crawl_delay_seconds = None
# EN: cache_state stores the explicit robots cache state selected for this branch/result.
# TR: cache_state bu dal/sonuç için seçilen açık robots cache durumunu tutar.
    cache_state = "fresh"
# EN: error_class stores the visible error class label when the robots refresh branch degrades or fails.
# TR: error_class robots yenileme dalı degrade olduğunda veya başarısız olduğunda görünür hata sınıfı etiketini tutar.
    error_class = None
# EN: error_message stores the visible human-readable failure/degraded detail for this robots branch.
# TR: error_message bu robots dalı için görünür insan-okur hata/degrade ayrıntısını tutar.
    error_message = None

    # EN: HTTP 404 is treated as a missing robots file.
    # TR: HTTP 404 eksik robots dosyası olarak ele alınır.
    if robots_fetch.http_status == 404:
# EN: cache_state stores the explicit robots cache state selected for this branch/result.
# TR: cache_state bu dal/sonuç için seçilen açık robots cache durumunu tutar.
        cache_state = "missing"

    # EN: Success-class HTTP results are parsed into the narrow rules model.
    # TR: Başarı-sınıfı HTTP sonuçları dar kural modeline parse edilir.
    elif robots_fetch.http_status is not None and 200 <= robots_fetch.http_status < 400:
# EN: sitemap_urls stores the sitemap URL list extracted from the parsed robots payload when present.
# TR: sitemap_urls varsa parse edilmiş robots payloadından çıkarılan sitemap URL listesini tutar.
# EN: parsed_rules stores the normalized parsed robots rules structure extracted from the fetched robots material.
# TR: parsed_rules fetch edilen robots materyalinden çıkarılan normalize edilmiş parsed robots rules yapısını tutar.
# EN: crawl_delay_seconds is the exact local variable that stores the normalized robots crawl-delay value derived from the refreshed robots metadata for cache persistence.
# TR: crawl_delay_seconds yenilenen robots metadata'sindan cache persistence icin turetilen normalize robots crawl-delay degerini tutan exact local degiskendir.
        parsed_rules, sitemap_urls, crawl_delay_seconds = parse_persisted_robots_payload(robots_fetch)
# EN: cache_state stores the explicit robots cache state selected for this branch/result.
# TR: cache_state bu dal/sonuç için seçilen açık robots cache durumunu tutar.
        cache_state = "fresh"

    # EN: All other HTTP results are persisted as explicit robots HTTP errors.
    # TR: Diğer tüm HTTP sonuçları açık robots HTTP hataları olarak yazılır.
    else:
# EN: cache_state stores the explicit robots cache state selected for this branch/result.
# TR: cache_state bu dal/sonuç için seçilen açık robots cache durumunu tutar.
        cache_state = "error"
# EN: error_class stores the visible error class label when the robots refresh branch degrades or fails.
# TR: error_class robots yenileme dalı degrade olduğunda veya başarısız olduğunda görünür hata sınıfı etiketini tutar.
        error_class = "robots_http_error"
# EN: error_message stores the visible human-readable failure/degraded detail for this robots branch.
# TR: error_message bu robots dalı için görünür insan-okur hata/degrade ayrıntısını tutar.
        error_message = f"robots fetch returned HTTP status {robots_fetch.http_status}"

    # EN: We persist the observed robots cache truth through the canonical DB wrapper.
    # TR: Gözlenen robots cache doğrusunu kanonik DB wrapper üzerinden yazıyoruz.
    return upsert_robots_txt_cache(
        conn,
        host_id=host_id,
        robots_url=str(robots_url),
        cache_state=cache_state,
        http_status=robots_fetch.http_status,
        fetched_at=fetched_at_value,
        expires_at=None,
        etag=robots_fetch.etag,
        last_modified=robots_fetch.last_modified,
        raw_storage_path=robots_fetch.raw_storage_path,
        raw_sha256=robots_fetch.raw_sha256,
        raw_bytes=robots_fetch.body_bytes,
        parsed_rules=parsed_rules,
        sitemap_urls=sitemap_urls,
        crawl_delay_seconds=crawl_delay_seconds,
        error_class=error_class,
        error_message=error_message,
        robots_metadata=robots_metadata,
    )


# EN: This explicit export list documents the public robots child surface.
# TR: Bu açık export listesi public robots alt yüzeyini belgelendirir.
__all__ = [
    "robots_verdict_allows_fetch",
    "parse_persisted_robots_payload",
    "refresh_robots_cache_if_needed",
]
