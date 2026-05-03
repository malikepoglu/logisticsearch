"""
EN:
This file is the discovery child of the state DB gateway family.

EN:
Why this file exists:
- because discovery-specific DB truth should live behind one explicit named gateway child
- because upper layers should use readable Python helpers instead of repeating raw discovery SQL semantics
- because discovered URL persistence and enqueue visibility are separate concerns from frontier claim truth, runtime control truth, robots truth, and terminal fetch-attempt logging

EN:
What this file DOES:
- expose discovery-oriented DB helper boundaries
- expose named helpers for reading or persisting discovery-related truth
- preserve visible branch boundaries for upper runtime layers

EN:
What this file DOES NOT do:
- it does not own shared DB connection helpers
- it does not own runtime-control truth
- it does not own frontier claim truth
- it does not fetch HTML by itself
- it does not act as an operator CLI surface

EN:
Topological role:
- gateway_support sits below this file for shared DB support
- this file sits in the middle for discovery-specific DB truth
- parse/runtime layers above call these helpers instead of embedding raw discovery SQL ideas

EN:
Important visible values and shapes:
- conn => live DB connection object
- source or parent identifiers => the records from which discovery truth is derived
- discovered_url or enqueue payload => structured discovery meaning
- insert, reuse, skip, or degraded visibility => explicit branch outcomes that should remain visible

EN:
Accepted architectural identity:
- discovery truth gateway
- enqueue-or-persistence DB-adjacent helper layer
- readable discovery contract boundary

EN:
Undesired architectural identity:
- hidden crawler controller
- hidden network fetch executor
- hidden parse executor
- hidden operator CLI surface

TR:
Bu dosya state DB gateway ailesinin discovery child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü discoveryye özgü DB doğrusu tek ve açık isimli gateway child yüzeyi arkasında yaşamalıdır
- çünkü üst katmanlar ham discovery SQL semantiğini tekrar etmek yerine okunabilir Python yardımcıları kullanmalıdır
- çünkü discovered URL kalıcılığı ve enqueue görünürlüğü frontier claim doğrusu, runtime control doğrusu, robots doğrusu ve terminal fetch-attempt loggingten ayrı bir konudur

TR:
Bu dosya NE yapar:
- discovery odaklı DB yardımcı sınırlarını açığa çıkarır
- discovery ile ilgili doğruları okumak veya kalıcılaştırmak için isimli yardımcılar sunar
- üst runtime katmanları için görünür dal sınırlarını korur

TR:
Bu dosya NE yapmaz:
- ortak DB bağlantı yardımcılarının sahibi değildir
- runtime-control doğrusunun sahibi değildir
- frontier claim doğrusunun sahibi değildir
- HTMLi kendi başına fetch etmez
- operatör CLI yüzeyi gibi davranmaz

TR:
Topolojik rol:
- ortak DB desteği için gateway_support bu dosyanın altındadır
- discoveryye özgü DB doğrusu için bu dosya ortadadır
- üstteki parse/runtime katmanları ham discovery SQL fikrini gömmek yerine bu yardımcıları çağırır

TR:
Önemli görünür değerler ve şekiller:
- conn => canlı DB bağlantı nesnesi
- source veya parent kimlikleri => discovery doğrusunun türetildiği kayıtlar
- discovered_url veya enqueue payload => yapılı discovery anlamı
- insert, reuse, skip veya degraded görünürlüğü => açık kalması gereken dal sonuçları

TR:
Kabul edilen mimari kimlik:
- discovery truth gateway
- enqueue-or-persistence DB-yanı yardımcı katmanı
- okunabilir discovery sözleşme sınırı

TR:
İstenmeyen mimari kimlik:
- gizli crawler controller
- gizli network fetch yürütücüsü
- gizli parse yürütücüsü
- gizli operatör CLI yüzeyi
"""

# EN: This module is the discovery child of the state DB gateway family.
# EN: It owns only discovery-context read and discovered-URL enqueue DB wrappers.
# TR: Bu modül state DB gateway ailesinin discovery alt yüzeyidir.
# TR: Yalnızca discovery-context okuma ve discovered-URL enqueue DB wrapper'larını taşır.

# EN: DISCOVERY GATEWAY IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the DB-boundary layer where discovery truth becomes durable and inspectable.
# EN: Beginner mental model:
# EN: - earlier layers encounter candidate outbound URLs or discovered entities
# EN: - this gateway child helps persist that discovery-side truth
# EN: - upper layers should not hand-write DB logic each time discovery visibility is needed
# EN:
# EN: Accepted architectural meaning:
# EN: - named discovery DB-truth boundary
# EN: - discovered-url enqueue/persistence helper surface
# EN:
# EN: Undesired architectural meaning:
# EN: - hidden parse executor
# EN: - hidden queue controller
# EN: - hidden operator surface
# EN:
# EN: Important value-shape reminders:
# EN: - discovered-url payloads may be structured dict-like shapes
# EN: - source and parent identity should remain explicit
# EN: - missing-row, reuse, skip, or degraded branches should stay visible
# TR: DISCOVERY GATEWAY KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya discovery doğrusunun kalıcı ve denetlenebilir hale geldiği DB-sınırı katmanı gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - önceki katmanlar aday outbound URLleri veya discovered varlıkları görür
# TR: - bu gateway child discovery tarafı doğrusunu kalıcılaştırmaya yardım eder
# TR: - üst katmanlar discovery görünürlüğü gerektiğinde DB mantığını elle yazmamalıdır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli discovery DB-truth sınırı
# TR: - discovered-url enqueue/persistence yardımcı yüzeyi
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - gizli parse yürütücüsü
# TR: - gizli queue controller
# TR: - gizli operatör yüzeyi
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - discovered-url payloadları yapılı dict-benzeri şekiller olabilir
# TR: - source ve parent kimliği açık kalmalıdır
# TR: - missing-row, reuse, skip veya degraded dalları görünür kalmalıdır

# EN: STAGE21-AUTO-COMMENT :: This import line declares discovery gateway dependencies by bringing in __future__ -> annotations.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or URL-shaping rules affect crawler expansion.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether discovery semantics, validation behavior, or provenance handling changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı __future__ -> annotations ögelerini içeri alarak discovery gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü crawler genişlemesini hangi yardımcıların, sözleşmelerin veya URL şekillendirme kurallarının etkilediğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse discovery anlamının, doğrulama davranışının veya köken bilgisinin de değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from __future__ import annotations

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares discovery gateway dependencies by bringing in typing -> Any.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or URL-shaping rules affect crawler expansion.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether discovery semantics, validation behavior, or provenance handling changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı typing -> Any ögelerini içeri alarak discovery gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü crawler genişlemesini hangi yardımcıların, sözleşmelerin veya URL şekillendirme kurallarının etkilediğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse discovery anlamının, doğrulama davranışının veya köken bilgisinin de değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from typing import Any

# EN: We import psycopg because these functions are thin wrappers around SQL calls.
# TR: Bu fonksiyonlar SQL çağrılarının ince wrapper'ları olduğu için psycopg içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares discovery gateway dependencies by bringing in psycopg.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or URL-shaping rules affect crawler expansion.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether discovery semantics, validation behavior, or provenance handling changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg ögelerini içeri alarak discovery gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü crawler genişlemesini hangi yardımcıların, sözleşmelerin veya URL şekillendirme kurallarının etkilediğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse discovery anlamının, doğrulama davranışının veya köken bilgisinin de değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
# EN: STAGE21-AUTO-COMMENT :: This import line declares discovery gateway dependencies by bringing in psycopg.rows -> dict_row.
# EN: STAGE21-AUTO-COMMENT :: Imports matter here because they reveal which helpers, contracts, or URL-shaping rules affect crawler expansion.
# EN: STAGE21-AUTO-COMMENT :: If imports change, inspect whether discovery semantics, validation behavior, or provenance handling changed too.
# EN: STAGE21-AUTO-COMMENT :: This marker treats imports as visible architecture clues rather than silent boilerplate.
# TR: STAGE21-AUTO-COMMENT :: Bu import satırı psycopg.rows -> dict_row ögelerini içeri alarak discovery gateway bağımlılıklarını bildirir.
# TR: STAGE21-AUTO-COMMENT :: Importlar burada önemlidir çünkü crawler genişlemesini hangi yardımcıların, sözleşmelerin veya URL şekillendirme kurallarının etkilediğini gösterirler.
# TR: STAGE21-AUTO-COMMENT :: Importlar değişirse discovery anlamının, doğrulama davranışının veya köken bilgisinin de değişip değişmediğini incele.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret importları sessiz şablon değil görünür mimari ipucu olarak ele alır.
from psycopg.rows import dict_row




# EN: This helper converts a discovery SQL wrapper no-row condition into an
# EN: operator-visible degraded payload so parse runtime can continue with honest
# EN: unresolved discovery state instead of crashing again.
# TR: Bu yardımcı discovery SQL wrapper no-row durumunu operatörün görebileceği
# TR: degrade payload'a çevirir; böylece parse runtime yeniden çökmeden dürüst
# TR: çözülmemiş discovery durumu ile devam edebilir.
# EN: DISCOVERY HELPER PURPOSE MEMORY BLOCK V6 / build_discovery_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because discovery-specific DB truth for 'build_discovery_no_row_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable discovery helper name instead of repeating raw SQL semantics
# EN: - because discovery persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: action, parent_url_id, canonical_url, depth, priority, scheme, host, port, authority_key, registrable_domain, error_class, error_message
# EN: - values should match the current Python signature and the live discovery SQL contract below
# EN:
# EN: Accepted output:
# EN: - a discovery-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an enqueue result, a lookup result, or another explicit branch result
# EN:
# EN: Common discovery meaning hints:
# EN: - this helper likely exposes one named discovery-specific DB-truth boundary
# EN: - source identity, candidate payload, or skip/degraded visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the whole crawler discovery policy by itself
# EN: - it is the named boundary where discovery-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw discovery SQL semantics instead of this helper contract
# TR: DISCOVERY YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / build_discovery_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'build_discovery_no_row_payload' için discoveryye özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham discovery SQL semantiğini tekrar etmek yerine okunabilir discovery yardımcı adı çağırmalıdır
# TR: - çünkü discovery kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: action, parent_url_id, canonical_url, depth, priority, scheme, host, port, authority_key, registrable_domain, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı discovery SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen discovery-odaklı sonuç şekli
# TR: - bu; yapılı payload, enqueue sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak discovery anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle discoveryye özgü isimli bir DB-truth sınırını açığa çıkarır
# TR: - source kimliği, candidate payloadı veya skip/degraded görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı discovery politikasının tamamı değildir
# TR: - bu, discovery tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham discovery SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This discovery gateway function named build_discovery_no_row_payload defines an entry, normalization, or forwarding point for discovered candidates.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what build_discovery_no_row_payload receives, how it shapes discovery metadata, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing build_discovery_no_row_payload, confirm that provenance, deduplication intent, and discovery scope remain consistent with crawler policy.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of build_discovery_no_row_payload obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: build_discovery_no_row_payload isimli bu discovery gateway fonksiyonu keşfedilen adaylar için bir giriş, normalizasyon veya ileri taşıma noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu build_discovery_no_row_payload fonksiyonunun ne aldığını, discovery metadatasını nasıl şekillendirdiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: build_discovery_no_row_payload değiştirilirken köken bilgisi, tekilleştirme niyeti ve discovery kapsamının crawler politikasıyla tutarlı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret build_discovery_no_row_payload başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: REAL-RULE AST REPAIR / DEF build_discovery_no_row_payload
# EN: build_discovery_no_row_payload is an explicit discovery-gateway helper/runtime contract.
# EN: Parameters kept explicit here: action, parent_url_id, canonical_url, depth, priority, scheme, host, port, authority_key, registrable_domain, error_class, error_message.
# TR: REAL-RULE AST REPAIR / FONKSIYON build_discovery_no_row_payload
# TR: build_discovery_no_row_payload acik bir discovery-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: action, parent_url_id, canonical_url, depth, priority, scheme, host, port, authority_key, registrable_domain, error_class, error_message.
def build_discovery_no_row_payload(
    *,
    action: str,
    parent_url_id: int | None = None,
    canonical_url: str | None = None,
    depth: int | None = None,
    priority: int | None = None,
    scheme: str | None = None,
    host: str | None = None,
    port: int | None = None,
    authority_key: str | None = None,
    registrable_domain: str | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, Any]:
    # EN: We keep one normalized degraded payload shape across discovery wrappers
    # EN: so caller-visible results stay explicit and consistent.
    # TR: Discovery wrapper'ları arasında tek ve normalize bir degrade payload
    # TR: şekli tutuyoruz; böylece çağıranın gördüğü sonuç açık ve tutarlı kalır.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete discovery result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream code sees when handling discovered candidates.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, provenance, and policy meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir discovery sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü keşfedilen adaylar işlenirken yukarı akış kodun gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı, köken bilgisi ve politika anlamını almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return {
        "parent_url_id": parent_url_id,
        "canonical_url": canonical_url,
        "depth": depth,
        "priority": priority,
        "scheme": scheme,
        "host": host,
        "port": port,
        "authority_key": authority_key,
        "registrable_domain": registrable_domain,
        "discovery_action": action,
        "discovery_degraded": True,
        "discovery_degraded_reason": f"{action}_returned_no_row",
        "discovery_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }



# EN: This helper fetches the minimal parent-URL discovery context needed by the
# EN: HTML discovery bridge.
# TR: Bu yardımcı, HTML discovery köprüsünün ihtiyaç duyduğu minimal parent-URL
# TR: discovery bağlamını getirir.
# EN: DISCOVERY HELPER PURPOSE MEMORY BLOCK V6 / fetch_url_discovery_context
# EN:
# EN: Why this helper exists:
# EN: - because discovery-specific DB truth for 'fetch_url_discovery_context' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable discovery helper name instead of repeating raw SQL semantics
# EN: - because discovery persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id
# EN: - values should match the current Python signature and the live discovery SQL contract below
# EN:
# EN: Accepted output:
# EN: - a discovery-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an enqueue result, a lookup result, or another explicit branch result
# EN:
# EN: Common discovery meaning hints:
# EN: - this helper likely exposes one named discovery-specific DB-truth boundary
# EN: - source identity, candidate payload, or skip/degraded visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the whole crawler discovery policy by itself
# EN: - it is the named boundary where discovery-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw discovery SQL semantics instead of this helper contract
# TR: DISCOVERY YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / fetch_url_discovery_context
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'fetch_url_discovery_context' için discoveryye özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham discovery SQL semantiğini tekrar etmek yerine okunabilir discovery yardımcı adı çağırmalıdır
# TR: - çünkü discovery kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı discovery SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen discovery-odaklı sonuç şekli
# TR: - bu; yapılı payload, enqueue sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak discovery anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle discoveryye özgü isimli bir DB-truth sınırını açığa çıkarır
# TR: - source kimliği, candidate payloadı veya skip/degraded görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı discovery politikasının tamamı değildir
# TR: - bu, discovery tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham discovery SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This discovery gateway function named fetch_url_discovery_context defines an entry, normalization, or forwarding point for discovered candidates.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what fetch_url_discovery_context receives, how it shapes discovery metadata, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing fetch_url_discovery_context, confirm that provenance, deduplication intent, and discovery scope remain consistent with crawler policy.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of fetch_url_discovery_context obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: fetch_url_discovery_context isimli bu discovery gateway fonksiyonu keşfedilen adaylar için bir giriş, normalizasyon veya ileri taşıma noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu fetch_url_discovery_context fonksiyonunun ne aldığını, discovery metadatasını nasıl şekillendirdiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: fetch_url_discovery_context değiştirilirken köken bilgisi, tekilleştirme niyeti ve discovery kapsamının crawler politikasıyla tutarlı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret fetch_url_discovery_context başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: REAL-RULE AST REPAIR / DEF fetch_url_discovery_context
# EN: fetch_url_discovery_context is an explicit discovery-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, url_id.
# TR: REAL-RULE AST REPAIR / FONKSIYON fetch_url_discovery_context
# TR: fetch_url_discovery_context acik bir discovery-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, url_id.
def fetch_url_discovery_context(
    conn: psycopg.Connection,
    *,
    url_id: int,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is one explicit context query.
    # TR: Bu tek ve açık bağlam sorgusu olduğu için izole bir cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible discovery gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface can influence how fast and how far the crawler expands.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intention and wider discovery meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact discovery code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür discovery gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey crawler'ın ne kadar hızlı ve ne kadar uzağa genişleyeceğini etkileyebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş discovery anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık discovery kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We read the parent URL together with its host truth from the DB so
        # EN: Python does not invent crawl context on its own.
        # TR: Parent URL'yi host doğrusu ile birlikte DB'den okuyoruz; böylece
        # TR: Python kendi başına crawl context uydurmaz.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct discovery-side action, often a call that moves candidate data toward downstream storage or runtime logic.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because a compact call can hide an important expansion side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the discovery gateway layer and still matches crawl policy.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational discovery effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan discovery tarafı bir eylem gerçekleştirir; çoğu zaman aday veriyi aşağı akış storage veya runtime mantığına taşıyan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık bir çağrı önemli bir genişleme yan etkisini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ discovery gateway katmanına ait olduğu ve crawl politikasıyla eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel discovery etkisinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT
                u.url_id,
                u.canonical_url,
                u.depth,
                u.priority,
                h.scheme,
                h.host,
                h.port,
                h.authority_key,
                h.registrable_domain
            FROM frontier.url AS u
            JOIN frontier.host AS h
              ON h.host_id = u.host_id
            WHERE u.url_id = %(url_id)s
            """,
            {
                "url_id": url_id,
            },
        )
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the discovery gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw discovered signals into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that origin meaning, validation meaning, and downstream interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where discovery state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini discovery gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham keşif sinyallerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde köken anlamının, doğrulama anlamının ve aşağı akış yorumunun uyumlu kaldığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret discovery durumunun somutlaştığı yeri vurgular.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of crashing the parent parse runtime.
    # TR: No-row yanıtı parent parse runtime'ı çökertmek yerine operatörün
    # TR: görebileceği degrade payload'a dönmelidir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects discovery behavior based on current input, state, or validation outcome.
    # EN: STAGE21-AUTO-COMMENT :: Conditional differences matter here because a small branch change can alter crawler expansion scope or allow unintended candidates.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect every path and confirm discovery policy still matches runtime expectations.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision with direct crawl-growth consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut girdi, durum veya doğrulama sonucuna göre discovery davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşul farkları burada önemlidir çünkü küçük bir dal değişikliği crawler genişleme kapsamını değiştirebilir veya istenmeyen adaylara izin verebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dal düzenlenirken her yol incelenmeli ve discovery politikasının runtime beklentileriyle hâlâ eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret crawl büyümesine doğrudan etkisi olan bir kararı vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete discovery result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream code sees when handling discovered candidates.
        # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, provenance, and policy meaning.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir discovery sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü keşfedilen adaylar işlenirken yukarı akış kodun gördüğü pratik sözleşmeyi tanımlarlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı, köken bilgisi ve politika anlamını almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_discovery_no_row_payload(
            action="fetch_url_discovery_context",
            parent_url_id=url_id,
            error_class="discovery_context_no_row",
            error_message="fetch_url_discovery_context(...) returned no row",
        )

    # EN: We return the raw mapping so the caller can inspect the exact context.
    # TR: Çağıran taraf tam bağlamı inceleyebilsin diye ham mapping döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete discovery result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream code sees when handling discovered candidates.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, provenance, and policy meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir discovery sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü keşfedilen adaylar işlenirken yukarı akış kodun gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı, köken bilgisi ve politika anlamını almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row



# EN: This helper asks the canonical discovery SQL surface to enqueue one
# EN: discovered URL.
# TR: Bu yardımcı, keşfedilmiş tek bir URL'yi enqueue etmesi için kanonik
# TR: discovery SQL yüzeyini çağırır.
# EN: DISCOVERY HELPER PURPOSE MEMORY BLOCK V6 / enqueue_discovered_url
# EN:
# EN: Why this helper exists:
# EN: - because discovery-specific DB truth for 'enqueue_discovered_url' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable discovery helper name instead of repeating raw SQL semantics
# EN: - because discovery persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, parent_url_id, canonical_url, canonical_url_sha256, port, scheme, host, authority_key, registrable_domain, url_path, url_query, discovery_type, depth, priority, enqueue_reason
# EN: - values should match the current Python signature and the live discovery SQL contract below
# EN:
# EN: Accepted output:
# EN: - a discovery-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, an enqueue result, a lookup result, or another explicit branch result
# EN:
# EN: Common discovery meaning hints:
# EN: - this helper likely persists or enqueues discovery-side truth
# EN: - discovered URL payload, parent identity, or reuse-vs-insert visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the whole crawler discovery policy by itself
# EN: - it is the named boundary where discovery-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw discovery SQL semantics instead of this helper contract
# TR: DISCOVERY YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / enqueue_discovered_url
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'enqueue_discovered_url' için discoveryye özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham discovery SQL semantiğini tekrar etmek yerine okunabilir discovery yardımcı adı çağırmalıdır
# TR: - çünkü discovery kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, parent_url_id, canonical_url, canonical_url_sha256, port, scheme, host, authority_key, registrable_domain, url_path, url_query, discovery_type, depth, priority, enqueue_reason
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı discovery SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen discovery-odaklı sonuç şekli
# TR: - bu; yapılı payload, enqueue sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak discovery anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle discovery tarafı doğrusunu kalıcılaştırır veya enqueue eder
# TR: - discovered URL payloadı, parent kimliği veya reuse-vs-insert görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı discovery politikasının tamamı değildir
# TR: - bu, discovery tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham discovery SQL semantiğini anlamaya zorlamak

# EN: STAGE21-AUTO-COMMENT :: This discovery gateway function named enqueue_discovered_url defines an entry, normalization, or forwarding point for discovered candidates.
# EN: STAGE21-AUTO-COMMENT :: A reader should understand what enqueue_discovered_url receives, how it shapes discovery metadata, and which downstream boundary it calls.
# EN: STAGE21-AUTO-COMMENT :: When changing enqueue_discovered_url, confirm that provenance, deduplication intent, and discovery scope remain consistent with crawler policy.
# EN: STAGE21-AUTO-COMMENT :: This marker keeps the beginning of enqueue_discovered_url obvious during audits and incident review.
# TR: STAGE21-AUTO-COMMENT :: enqueue_discovered_url isimli bu discovery gateway fonksiyonu keşfedilen adaylar için bir giriş, normalizasyon veya ileri taşıma noktası tanımlar.
# TR: STAGE21-AUTO-COMMENT :: Okuyucu enqueue_discovered_url fonksiyonunun ne aldığını, discovery metadatasını nasıl şekillendirdiğini ve hangi aşağı akış sınırı çağırdığını anlayabilmelidir.
# TR: STAGE21-AUTO-COMMENT :: enqueue_discovered_url değiştirilirken köken bilgisi, tekilleştirme niyeti ve discovery kapsamının crawler politikasıyla tutarlı kaldığı doğrulanmalıdır.
# TR: STAGE21-AUTO-COMMENT :: Bu işaret enqueue_discovered_url başlangıcını denetim ve olay incelemesi sırasında belirgin tutar.
# EN: REAL-RULE AST REPAIR / DEF enqueue_discovered_url
# EN: enqueue_discovered_url is an explicit discovery-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, parent_url_id, canonical_url, canonical_url_sha256, port, scheme, host, authority_key, registrable_domain, url_path, url_query, discovery_type, depth, priority, enqueue_reason.
# TR: REAL-RULE AST REPAIR / FONKSIYON enqueue_discovered_url
# TR: enqueue_discovered_url acik bir discovery-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, parent_url_id, canonical_url, canonical_url_sha256, port, scheme, host, authority_key, registrable_domain, url_path, url_query, discovery_type, depth, priority, enqueue_reason.
def enqueue_discovered_url(
    conn: psycopg.Connection,
    *,
    parent_url_id: int,
    canonical_url: str,
    canonical_url_sha256: str,
    port: int,
    scheme: str,
    host: str,
    authority_key: str,
    registrable_domain: str,
    url_path: str,
    url_query: str | None,
    discovery_type: str,
    depth: int,
    priority: int,
    enqueue_reason: str,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this helper performs one explicit
    # EN: discovery-enqueue call.
    # TR: Bu yardımcı tek bir açık discovery-enqueue çağrısı yaptığı için izole
    # TR: bir cursor açıyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This statement is part of the visible discovery gateway flow and is annotated to keep the file beginner-friendly.
    # EN: STAGE21-AUTO-COMMENT :: Even familiar syntax should remain purpose-driven here because this surface can influence how fast and how far the crawler expands.
    # EN: STAGE21-AUTO-COMMENT :: Review this statement with nearby comments so local intention and wider discovery meaning remain aligned.
    # EN: STAGE21-AUTO-COMMENT :: This marker prevents compact discovery code from hiding silent meaning.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade görünür discovery gateway akışının parçasıdır ve dosyayı yeni başlayan dostu tutmak için açıklanmıştır.
    # TR: STAGE21-AUTO-COMMENT :: Tanıdık sözdizimi bile burada amaca bağlı kalmalıdır çünkü bu yüzey crawler'ın ne kadar hızlı ve ne kadar uzağa genişleyeceğini etkileyebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu ifade yakın yorumlarla birlikte gözden geçirilmelidir ki yerel niyet ile geniş discovery anlamı uyumlu kalsın.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret sıkışık discovery kodunun sessiz anlam gizlemesini önler.
    with conn.cursor() as cur:
        # EN: We call the canonical frontier function instead of duplicating upsert
        # EN: rules in Python.
        # TR: Upsert kurallarını Python'da kopyalamak yerine kanonik frontier
        # TR: fonksiyonunu çağırıyoruz.
        # EN: STAGE21-AUTO-COMMENT :: This expression performs a direct discovery-side action, often a call that moves candidate data toward downstream storage or runtime logic.
        # EN: STAGE21-AUTO-COMMENT :: Expressions should stay readable here because a compact call can hide an important expansion side effect.
        # EN: STAGE21-AUTO-COMMENT :: If this line changes, verify that the effect still belongs in the discovery gateway layer and still matches crawl policy.
        # EN: STAGE21-AUTO-COMMENT :: This marker warns the reader that an operational discovery effect happens at this statement.
        # TR: STAGE21-AUTO-COMMENT :: Bu ifade doğrudan discovery tarafı bir eylem gerçekleştirir; çoğu zaman aday veriyi aşağı akış storage veya runtime mantığına taşıyan bir çağrıdır.
        # TR: STAGE21-AUTO-COMMENT :: İfadeler burada okunabilir kalmalıdır çünkü sıkışık bir çağrı önemli bir genişleme yan etkisini gizleyebilir.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değişirse etkinin hâlâ discovery gateway katmanına ait olduğu ve crawl politikasıyla eşleştiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret okuyucuya bu ifadede operasyonel discovery etkisinin gerçekleştiğini söyler.
        cur.execute(
            """
            SELECT *
            FROM frontier.enqueue_discovered_url(
                p_parent_url_id => %(parent_url_id)s,
                p_canonical_url => %(canonical_url)s,
                p_canonical_url_sha256 => %(canonical_url_sha256)s,
                p_port => %(port)s,
                p_scheme => %(scheme)s,
                p_host => %(host)s,
                p_authority_key => %(authority_key)s,
                p_registrable_domain => %(registrable_domain)s,
                p_url_path => %(url_path)s,
                p_url_query => %(url_query)s,
                p_discovery_type => %(discovery_type)s::frontier.discovery_type_enum,
                p_depth => %(depth)s,
                p_priority => %(priority)s,
                p_enqueue_reason => %(enqueue_reason)s
            )
            """,
            {
                "parent_url_id": parent_url_id,
                "canonical_url": canonical_url,
                "canonical_url_sha256": canonical_url_sha256,
                "port": port,
                "scheme": scheme,
                "host": host,
                "authority_key": authority_key,
                "registrable_domain": registrable_domain,
                "url_path": url_path,
                "url_query": url_query,
                "discovery_type": discovery_type,
                "depth": depth,
                "priority": priority,
                "enqueue_reason": enqueue_reason,
            },
        )
        # EN: STAGE21-AUTO-COMMENT :: This assignment defines or updates row as part of the discovery gateway flow.
        # EN: STAGE21-AUTO-COMMENT :: Assignments in this file often convert raw discovered signals into normalized gateway state and should stay explicit.
        # EN: STAGE21-AUTO-COMMENT :: When this value changes, confirm that origin meaning, validation meaning, and downstream interpretation remain compatible.
        # EN: STAGE21-AUTO-COMMENT :: This marker highlights where discovery state becomes concrete.
        # TR: STAGE21-AUTO-COMMENT :: Bu atama row değerlerini discovery gateway akışının parçası olarak tanımlar veya günceller.
        # TR: STAGE21-AUTO-COMMENT :: Bu dosyadaki atamalar çoğu zaman ham keşif sinyallerini normalize gateway durumuna dönüştürür ve açık kalmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu değer değiştiğinde köken anlamının, doğrulama anlamının ve aşağı akış yorumunun uyumlu kaldığı doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret discovery durumunun somutlaştığı yeri vurgular.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of becoming a silent enqueue loss.
    # TR: No-row yanıtı sessiz bir enqueue kaybına dönüşmek yerine operatörün
    # TR: görebileceği degrade payload'a dönmelidir.
    # EN: STAGE21-AUTO-COMMENT :: This conditional branch selects discovery behavior based on current input, state, or validation outcome.
    # EN: STAGE21-AUTO-COMMENT :: Conditional differences matter here because a small branch change can alter crawler expansion scope or allow unintended candidates.
    # EN: STAGE21-AUTO-COMMENT :: When editing this branch, inspect every path and confirm discovery policy still matches runtime expectations.
    # EN: STAGE21-AUTO-COMMENT :: This marker highlights a decision with direct crawl-growth consequences.
    # TR: STAGE21-AUTO-COMMENT :: Bu koşullu dal mevcut girdi, durum veya doğrulama sonucuna göre discovery davranışını seçer.
    # TR: STAGE21-AUTO-COMMENT :: Koşul farkları burada önemlidir çünkü küçük bir dal değişikliği crawler genişleme kapsamını değiştirebilir veya istenmeyen adaylara izin verebilir.
    # TR: STAGE21-AUTO-COMMENT :: Bu dal düzenlenirken her yol incelenmeli ve discovery politikasının runtime beklentileriyle hâlâ eşleştiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret crawl büyümesine doğrudan etkisi olan bir kararı vurgular.
    if row is None:
        # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete discovery result back to the caller.
        # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream code sees when handling discovered candidates.
        # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, provenance, and policy meaning.
        # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
        # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir discovery sonucu geri gönderir.
        # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü keşfedilen adaylar işlenirken yukarı akış kodun gördüğü pratik sözleşmeyi tanımlarlar.
        # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı, köken bilgisi ve politika anlamını almaya devam ettiği doğrulanmalıdır.
        # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
        return build_discovery_no_row_payload(
            action="enqueue_discovered_url",
            parent_url_id=parent_url_id,
            canonical_url=canonical_url,
            depth=depth,
            priority=priority,
            scheme=scheme,
            host=host,
            port=port,
            authority_key=authority_key,
            registrable_domain=registrable_domain,
            error_class="discovery_enqueue_no_row",
            error_message="frontier.enqueue_discovered_url(...) returned no row",
        )

    # EN: We return the raw mapping so the caller can inspect the exact enqueue result.
    # TR: Çağıran taraf tam enqueue sonucunu inceleyebilsin diye ham mapping döndürüyoruz.
    # EN: STAGE21-AUTO-COMMENT :: This return point sends a concrete discovery result back to the caller.
    # EN: STAGE21-AUTO-COMMENT :: Return lines matter because they define the practical contract that upstream code sees when handling discovered candidates.
    # EN: STAGE21-AUTO-COMMENT :: When changing this line, confirm callers still receive the expected structure, provenance, and policy meaning.
    # EN: STAGE21-AUTO-COMMENT :: This marker makes the exit contract explicit.
    # TR: STAGE21-AUTO-COMMENT :: Bu return noktası çağırana somut bir discovery sonucu geri gönderir.
    # TR: STAGE21-AUTO-COMMENT :: Return satırları önemlidir çünkü keşfedilen adaylar işlenirken yukarı akış kodun gördüğü pratik sözleşmeyi tanımlarlar.
    # TR: STAGE21-AUTO-COMMENT :: Bu satır değiştiğinde çağıranların beklenen yapı, köken bilgisi ve politika anlamını almaya devam ettiği doğrulanmalıdır.
    # TR: STAGE21-AUTO-COMMENT :: Bu işaret çıkış sözleşmesini açık hale getirir.
    return row
