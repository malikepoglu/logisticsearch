"""
EN:
This file is the preranking child of the state DB gateway family.

EN:
Why this file exists:
- because preranking-specific DB truth should live behind one explicit named gateway child
- because upper layers should use readable Python helpers instead of repeating raw SQL semantics for preranking persistence
- because preranking visibility is a separate concern from frontier claim truth, runtime control truth, robots truth, and terminal fetch-attempt logging

EN:
What this file DOES:
- expose preranking-oriented DB helper boundaries
- expose named helpers for reading or persisting preranking-related truth
- preserve visible branch boundaries for upper runtime layers

EN:
What this file DOES NOT do:
- it does not own shared DB connection helpers
- it does not own runtime-control truth
- it does not own frontier claim truth
- it does not parse HTML by itself
- it does not act as an operator CLI surface

EN:
Topological role:
- gateway_support sits below this file for shared DB support
- this file sits in the middle for preranking-specific DB truth
- parse/runtime layers above call these helpers instead of embedding raw preranking SQL ideas

EN:
Important visible values and shapes:
- conn => live DB connection object
- page or candidate identifiers => the records whose preranking truth is being read or written
- score / signals / features / evidence payloads => structured preranking-related meaning
- no-row / degraded visibility => non-happy branches that should remain explicit

EN:
Accepted architectural identity:
- preranking truth gateway
- scoring-or-persistence DB-adjacent helper layer
- readable preranking contract boundary

EN:
Undesired architectural identity:
- hidden crawler controller
- hidden parse executor
- hidden ranking engine beyond its DB-boundary role
- hidden operator CLI surface

TR:
Bu dosya state DB gateway ailesinin preranking child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü prerankinge özgü DB doğrusu tek ve açık isimli gateway child yüzeyi arkasında yaşamalıdır
- çünkü üst katmanlar ham SQL semantiğini tekrar etmek yerine preranking kalıcılığı için okunabilir Python yardımcıları kullanmalıdır
- çünkü preranking görünürlüğü frontier claim doğrusu, runtime control doğrusu, robots doğrusu ve terminal fetch-attempt loggingten ayrı bir konudur

TR:
Bu dosya NE yapar:
- preranking odaklı DB yardımcı sınırlarını açığa çıkarır
- preranking ile ilgili doğruları okumak veya kalıcılaştırmak için isimli yardımcılar sunar
- üst runtime katmanları için görünür dal sınırlarını korur

TR:
Bu dosya NE yapmaz:
- ortak DB bağlantı yardımcılarının sahibi değildir
- runtime-control doğrusunun sahibi değildir
- frontier claim doğrusunun sahibi değildir
- HTMLi kendi başına parse etmez
- operatör CLI yüzeyi gibi davranmaz

TR:
Topolojik rol:
- ortak DB desteği için gateway_support bu dosyanın altındadır
- prerankinge özgü DB doğrusu için bu dosya ortadadır
- üstteki parse/runtime katmanları ham preranking SQL fikrini gömmek yerine bu yardımcıları çağırır

TR:
Önemli görünür değerler ve şekiller:
- conn => canlı DB bağlantı nesnesi
- page veya candidate kimlikleri => preranking doğrusu okunan veya yazılan kayıtlar
- score / signals / features / evidence payloadları => yapılı preranking anlamı
- no-row / degraded görünürlüğü => açık kalması gereken mutlu-yol-dışı dallar

TR:
Kabul edilen mimari kimlik:
- preranking truth gateway
- scoring-or-persistence DB-yanı yardımcı katmanı
- okunabilir preranking sözleşme sınırı

TR:
İstenmeyen mimari kimlik:
- gizli crawler controller
- gizli parse yürütücüsü
- DB-sınırı rolünün ötesine geçen gizli ranking motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module is the preranking child of the state DB gateway family.
# EN: It owns only taxonomy/preranking/workflow DB wrappers.
# TR: Bu modül state DB gateway ailesinin preranking alt yüzeyidir.
# TR: Yalnızca taxonomy/preranking/workflow DB wrapper'larını taşır.

# EN: PRERANKING GATEWAY IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the DB-boundary layer where preranking truth becomes durable and inspectable.
# EN: Beginner mental model:
# EN: - earlier layers discover signals or candidate meaning
# EN: - this gateway child helps persist or read preranking-side truth
# EN: - upper layers should not hand-write DB logic every time they need preranking visibility
# EN:
# EN: Accepted architectural meaning:
# EN: - named preranking DB-truth boundary
# EN: - score/signal persistence helper surface
# EN:
# EN: Undesired architectural meaning:
# EN: - hidden parse executor
# EN: - hidden final-ranking engine
# EN: - hidden operator surface
# EN:
# EN: Important value-shape reminders:
# EN: - signal or scoring payloads may be structured dict-like shapes
# EN: - page/candidate identity should remain explicit
# EN: - missing-row or degraded branches should stay visible
# TR: PRERANKING GATEWAY KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya preranking doğrusunun kalıcı ve denetlenebilir hale geldiği DB-sınırı katmanı gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - önceki katmanlar sinyal veya aday anlamını keşfeder
# TR: - bu gateway child preranking tarafı doğrusunu okumaya veya kalıcılaştırmaya yardım eder
# TR: - üst katmanlar her preranking görünürlüğünde DB mantığını elle yazmamalıdır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli preranking DB-truth sınırı
# TR: - score/signal persistence yardımcı yüzeyi
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - gizli parse yürütücüsü
# TR: - gizli final-ranking motoru
# TR: - gizli operatör yüzeyi
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - signal veya scoring payloadları yapılı dict-benzeri şekiller olabilir
# TR: - page/candidate kimliği açık kalmalıdır
# TR: - missing-row veya degraded dalları görünür kalmalıdır

from __future__ import annotations

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
from typing import Any

# EN: We import psycopg because these functions are thin wrappers around SQL calls.
# TR: Bu fonksiyonlar SQL çağrılarının ince wrapper'ları olduğu için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
from psycopg.rows import dict_row



# EN: This helper converts a preranking/workflow SQL wrapper no-row condition into
# EN: an operator-visible degraded payload so upper parse runtime layers can keep
# EN: moving with honest unresolved state instead of crashing again.
# TR: Bu yardımcı preranking/workflow SQL wrapper no-row durumunu operatörün
# TR: görebileceği degrade payload'a çevirir; böylece üst parse runtime katmanları
# TR: yeniden çökmeden dürüst çözülmemiş durumla ilerleyebilir.
# EN: PRERANKING HELPER PURPOSE MEMORY BLOCK V6 / build_preranking_no_row_payload
# EN:
# EN: Why this helper exists:
# EN: - because preranking-specific DB truth for 'build_preranking_no_row_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable preranking helper name instead of repeating raw SQL semantics
# EN: - because preranking persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: action, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, linked_snapshot_id, workflow_state, state_reason, persisted_candidate_count, error_class, error_message
# EN: - values should match the current Python signature and the live preranking SQL contract below
# EN:
# EN: Accepted output:
# EN: - a preranking-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a score/signal write result, a lookup result, or another explicit branch result
# EN:
# EN: Common preranking meaning hints:
# EN: - this helper likely exposes score, prerank, or candidate-ordering-related DB truth
# EN: - score payloads, evidence fields, or degraded write visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the source of truth about full ranking policy by itself
# EN: - it is the named boundary where preranking-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw preranking SQL semantics instead of this helper contract
# TR: PRERANKING YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / build_preranking_no_row_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'build_preranking_no_row_payload' için prerankinge özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham preranking SQL semantiğini tekrar etmek yerine okunabilir preranking yardımcı adı çağırmalıdır
# TR: - çünkü preranking kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: action, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, linked_snapshot_id, workflow_state, state_reason, persisted_candidate_count, error_class, error_message
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı preranking SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen preranking-odaklı sonuç şekli
# TR: - bu; yapılı payload, score/signal write sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak preranking anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle score, prerank veya aday-sıralama ile ilgili DB doğrusunu açığa çıkarır
# TR: - score payloadları, evidence alanları veya degrade yazma görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı tek başına tam ranking politikasının kaynağı değildir
# TR: - bu, preranking tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham preranking SQL semantiğini anlamaya zorlamak

# EN: REAL-RULE AST REPAIR / DEF build_preranking_no_row_payload
# EN: build_preranking_no_row_payload is an explicit preranking-gateway helper/runtime contract.
# EN: Parameters kept explicit here: action, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, linked_snapshot_id, workflow_state, state_reason, persisted_candidate_count, error_class, error_message.
# TR: REAL-RULE AST REPAIR / FONKSIYON build_preranking_no_row_payload
# TR: build_preranking_no_row_payload acik bir preranking-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: action, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, linked_snapshot_id, workflow_state, state_reason, persisted_candidate_count, error_class, error_message.
def build_preranking_no_row_payload(
    *,
    action: str,
    url_id: int | None = None,
    input_lang_code: str | None = None,
    taxonomy_package_version: str | None = None,
    top_candidate_count: int | None = None,
    top_score: Any = None,
    linked_snapshot_id: int | None = None,
    workflow_state: str | None = None,
    state_reason: str | None = None,
    persisted_candidate_count: int | None = None,
    error_class: str,
    error_message: str,
) -> dict[str, Any]:
    # EN: We keep one normalized degraded payload shape across preranking/workflow
    # EN: wrappers so caller-visible results stay explicit and consistent.
    # TR: Preranking/workflow wrapper'ları arasında tek ve normalize bir degrade
    # TR: payload şekli tutuyoruz; böylece çağıranın gördüğü sonuç açık ve tutarlı kalır.
    return {
        "snapshot_id": None,
        "workflow_status_id": None,
        "url_id": url_id,
        "input_lang_code": input_lang_code,
        "taxonomy_package_version": taxonomy_package_version,
        "top_candidate_count": top_candidate_count,
        "top_score": top_score,
        "linked_snapshot_id": linked_snapshot_id,
        "workflow_state": workflow_state,
        "state_reason": state_reason,
        "persisted_candidate_count": persisted_candidate_count,
        "preranking_action": action,
        "preranking_degraded": True,
        "preranking_degraded_reason": f"{action}_returned_no_row",
        "preranking_completed": False,
        "error_class": error_class,
        "error_message": error_message,
    }



# EN: This helper calls parse.persist_taxonomy_preranking_payload(...) so Python
# EN: can persist one minimal parse payload into the parse schema.
# TR: Bu yardımcı parse.persist_taxonomy_preranking_payload(...) çağrısını yapar;
# TR: böylece Python tek bir minimal parse payload'ını parse şemasına yazabilir.
# EN: PRERANKING HELPER PURPOSE MEMORY BLOCK V6 / persist_taxonomy_preranking_payload
# EN:
# EN: Why this helper exists:
# EN: - because preranking-specific DB truth for 'persist_taxonomy_preranking_payload' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable preranking helper name instead of repeating raw SQL semantics
# EN: - because preranking persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, payload
# EN: - values should match the current Python signature and the live preranking SQL contract below
# EN:
# EN: Accepted output:
# EN: - a preranking-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a score/signal write result, a lookup result, or another explicit branch result
# EN:
# EN: Common preranking meaning hints:
# EN: - this helper likely exposes score, prerank, or candidate-ordering-related DB truth
# EN: - score payloads, evidence fields, or degraded write visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the source of truth about full ranking policy by itself
# EN: - it is the named boundary where preranking-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw preranking SQL semantics instead of this helper contract
# TR: PRERANKING YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / persist_taxonomy_preranking_payload
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'persist_taxonomy_preranking_payload' için prerankinge özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham preranking SQL semantiğini tekrar etmek yerine okunabilir preranking yardımcı adı çağırmalıdır
# TR: - çünkü preranking kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, payload
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı preranking SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen preranking-odaklı sonuç şekli
# TR: - bu; yapılı payload, score/signal write sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak preranking anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle score, prerank veya aday-sıralama ile ilgili DB doğrusunu açığa çıkarır
# TR: - score payloadları, evidence alanları veya degrade yazma görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı tek başına tam ranking politikasının kaynağı değildir
# TR: - bu, preranking tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham preranking SQL semantiğini anlamaya zorlamak

# EN: REAL-RULE AST REPAIR / DEF persist_taxonomy_preranking_payload
# EN: persist_taxonomy_preranking_payload is an explicit preranking-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, payload.
# TR: REAL-RULE AST REPAIR / FONKSIYON persist_taxonomy_preranking_payload
# TR: persist_taxonomy_preranking_payload acik bir preranking-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, payload.
def persist_taxonomy_preranking_payload(
    conn: psycopg.Connection,
    payload: dict,
) -> dict:
    # EN: We import json locally because this helper converts a Python dict into
    # EN: a JSON text value for the SQL payload entry function.
    # TR: Bu yardımcı Python dict değerini SQL payload giriş fonksiyonu için JSON
    # TR: metnine çevirdiği için json modülünü yerel olarak içe aktarıyoruz.
    import json

    # EN: We defensively validate the candidate list before the SQL call so an
    # EN: invalid Python payload cannot poison the current transaction.
    # TR: SQL çağrısından önce candidate listesini savunmacı biçimde doğruluyoruz;
    # TR: böylece geçersiz Python payload'ı mevcut transaction'ı zehirleyemez.
    # EN: REAL-RULE AST REPAIR / LOCAL persist_taxonomy_preranking_payload / candidates
    # EN: candidates are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL persist_taxonomy_preranking_payload / candidates
    # TR: candidates burada acik ara dal degerleri olarak atanir.
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        raise RuntimeError("payload['candidates'] must be a list")

    # EN: REAL-RULE AST REPAIR / LOCAL persist_taxonomy_preranking_payload / invalid_candidate_indexes
    # EN: invalid_candidate_indexes are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL persist_taxonomy_preranking_payload / invalid_candidate_indexes
    # TR: invalid_candidate_indexes burada acik ara dal degerleri olarak atanir.
    invalid_candidate_indexes: list[int] = []

    # EN: The currently proven hard requirement is taxonomy_package_id.
    # TR: Şu anda kanıtlanmış sert gereklilik taxonomy_package_id alanıdır.
    for idx, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            invalid_candidate_indexes.append(idx)
            continue
        if candidate.get("taxonomy_package_id") in (None, ""):
            invalid_candidate_indexes.append(idx)

    # EN: We fail fast here with one explicit message instead of letting SQL abort
    # EN: the whole transaction at a deeper layer.
    # TR: Burada tek ve açık bir mesajla erken hata veriyoruz; böylece SQL daha
    # TR: derinde tüm transaction'ı abort etmez.
    if invalid_candidate_indexes:
        raise RuntimeError(
            "parse taxonomy payload contains invalid candidate(s) without "
            f"taxonomy_package_id at indexes {invalid_candidate_indexes}"
        )

    # EN: We open a cursor from the already-open connection.
    # TR: Zaten açık bağlantı üzerinden bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We send the payload as JSON text and cast it to jsonb inside SQL.
        # TR: Payload'ı JSON metni olarak gönderiyor ve SQL içinde jsonb'ye cast ediyoruz.
        cur.execute(
            """
            select *
            from parse.persist_taxonomy_preranking_payload(%s::jsonb)
            """,
            [json.dumps(payload)],
        )

        # EN: We fetch exactly one returned row from the wrapper function.
        # TR: Wrapper fonksiyondan dönen tam bir satırı çekiyoruz.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of aborting the parent parse runtime again.
    # TR: No-row yanıtı parent parse runtime'ı yeniden abort etmek yerine
    # TR: operatörün görebileceği degrade payload'a dönmelidir.
    if row is None:
        return build_preranking_no_row_payload(
            action="parse_persist_taxonomy_preranking_payload",
            url_id=payload.get("url_id"),
            input_lang_code=payload.get("input_lang_code"),
            taxonomy_package_version=(payload.get("metadata") or {}).get("taxonomy_package_version"),
            persisted_candidate_count=0,
            error_class="persist_taxonomy_preranking_no_row",
            error_message="parse.persist_taxonomy_preranking_payload(...) returned no row",
        )

    # EN: We return the structured row to the caller.
    # TR: Yapılı satırı çağırana döndürüyoruz.
    return row



# EN: This helper calls parse.persist_page_preranking_snapshot(...) so Python can
# EN: materialize the durable preranking snapshot row after evidence/candidate persistence.
# TR: Bu yardımcı parse.persist_page_preranking_snapshot(...) çağrısını yapar;
# TR: böylece evidence/candidate persistence sonrasında kalıcı preranking snapshot
# TR: satırı Python tarafından üretilebilir.
# EN: PRERANKING HELPER PURPOSE MEMORY BLOCK V6 / persist_page_preranking_snapshot
# EN:
# EN: Why this helper exists:
# EN: - because preranking-specific DB truth for 'persist_page_preranking_snapshot' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable preranking helper name instead of repeating raw SQL semantics
# EN: - because preranking persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, candidate_summary, snapshot_metadata, source_run_id, source_note, review_status
# EN: - values should match the current Python signature and the live preranking SQL contract below
# EN:
# EN: Accepted output:
# EN: - a preranking-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a score/signal write result, a lookup result, or another explicit branch result
# EN:
# EN: Common preranking meaning hints:
# EN: - this helper likely exposes score, prerank, or candidate-ordering-related DB truth
# EN: - score payloads, evidence fields, or degraded write visibility may matter here
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the source of truth about full ranking policy by itself
# EN: - it is the named boundary where preranking-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw preranking SQL semantics instead of this helper contract
# TR: PRERANKING YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / persist_page_preranking_snapshot
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'persist_page_preranking_snapshot' için prerankinge özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham preranking SQL semantiğini tekrar etmek yerine okunabilir preranking yardımcı adı çağırmalıdır
# TR: - çünkü preranking kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, candidate_summary, snapshot_metadata, source_run_id, source_note, review_status
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı preranking SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen preranking-odaklı sonuç şekli
# TR: - bu; yapılı payload, score/signal write sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak preranking anlam ipuçları:
# TR: - bu yardımcı büyük ihtimalle score, prerank veya aday-sıralama ile ilgili DB doğrusunu açığa çıkarır
# TR: - score payloadları, evidence alanları veya degrade yazma görünürlüğü burada önemli olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı tek başına tam ranking politikasının kaynağı değildir
# TR: - bu, preranking tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham preranking SQL semantiğini anlamaya zorlamak

# EN: REAL-RULE AST REPAIR / DEF persist_page_preranking_snapshot
# EN: persist_page_preranking_snapshot is an explicit preranking-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, candidate_summary, snapshot_metadata, source_run_id, source_note, review_status.
# TR: REAL-RULE AST REPAIR / FONKSIYON persist_page_preranking_snapshot
# TR: persist_page_preranking_snapshot acik bir preranking-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, url_id, input_lang_code, taxonomy_package_version, top_candidate_count, top_score, candidate_summary, snapshot_metadata, source_run_id, source_note, review_status.
def persist_page_preranking_snapshot(
    conn: psycopg.Connection,
    *,
    url_id: int,
    input_lang_code: str,
    taxonomy_package_version: str,
    top_candidate_count: int = 0,
    top_score: Any = None,
    candidate_summary: list[dict[str, Any]] | None = None,
    snapshot_metadata: dict[str, Any] | None = None,
    source_run_id: str | None = None,
    source_note: str | None = None,
    review_status: str = "pre_ranked",
) -> dict[str, Any]:
    # EN: We import json locally because only this helper needs jsonb-safe serialization.
    # TR: Yalnızca bu yardımcı jsonb-uyumlu serileştirme kullandığı için json'u yerel içe aktarıyoruz.
    import json

    # EN: We serialize optional JSON-shaped inputs only when needed.
    # TR: Opsiyonel JSON-biçimli girdileri yalnızca gerektiğinde serileştiriyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL persist_page_preranking_snapshot / candidate_summary_json
    # EN: candidate_summary_json are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL persist_page_preranking_snapshot / candidate_summary_json
    # TR: candidate_summary_json burada acik ara dal degerleri olarak atanir.
    candidate_summary_json = json.dumps(candidate_summary or [])
    # EN: REAL-RULE AST REPAIR / LOCAL persist_page_preranking_snapshot / snapshot_metadata_json
    # EN: snapshot_metadata_json are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL persist_page_preranking_snapshot / snapshot_metadata_json
    # TR: snapshot_metadata_json burada acik ara dal degerleri olarak atanir.
    snapshot_metadata_json = json.dumps(snapshot_metadata or {})

    # EN: We execute the canonical SQL function inside the caller-owned transaction.
    # TR: Kanonik SQL fonksiyonunu çağıranın sahip olduğu transaction içinde çalıştırıyoruz.
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT *
            FROM parse.persist_page_preranking_snapshot(
                p_url_id => %(url_id)s,
                p_input_lang_code => %(input_lang_code)s,
                p_taxonomy_package_version => %(taxonomy_package_version)s,
                p_top_candidate_count => %(top_candidate_count)s,
                p_top_score => %(top_score)s,
                p_candidate_summary => %(candidate_summary)s::jsonb,
                p_snapshot_metadata => %(snapshot_metadata)s::jsonb,
                p_source_run_id => %(source_run_id)s,
                p_source_note => %(source_note)s,
                p_review_status => %(review_status)s
            )
            """,
            {
                "url_id": url_id,
                "input_lang_code": input_lang_code,
                "taxonomy_package_version": taxonomy_package_version,
                "top_candidate_count": top_candidate_count,
                "top_score": top_score,
                "candidate_summary": candidate_summary_json,
                "snapshot_metadata": snapshot_metadata_json,
                "source_run_id": source_run_id,
                "source_note": source_note,
                "review_status": review_status,
            },
        )

        # EN: We fetch exactly one row because one call produces one durable snapshot row.
        # TR: Tek çağrı tek bir kalıcı snapshot satırı ürettiği için tam bir satır çekiyoruz.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of aborting the parent parse runtime again.
    # TR: No-row yanıtı parent parse runtime'ı yeniden abort etmek yerine
    # TR: operatörün görebileceği degrade payload'a dönmelidir.
    if row is None:
        return build_preranking_no_row_payload(
            action="parse_persist_page_preranking_snapshot",
            url_id=url_id,
            input_lang_code=input_lang_code,
            taxonomy_package_version=taxonomy_package_version,
            top_candidate_count=top_candidate_count,
            top_score=top_score,
            error_class="preranking_snapshot_no_row",
            error_message="parse.persist_page_preranking_snapshot(...) returned no row",
        )

    # EN: We return the raw mapping because it is already beginner-readable.
    # TR: Ham mapping'i döndürüyoruz; çünkü zaten beginner-okunur yapıdadır.
    return row



# EN: This helper calls parse.upsert_page_workflow_status(...) so Python can mark
# EN: the current parse workflow state of one URL explicitly.
# TR: Bu yardımcı parse.upsert_page_workflow_status(...) çağrısını yapar; böylece
# TR: Python tek bir URL'nin mevcut parse workflow durumunu açık biçimde işaretleyebilir.
# EN: PRERANKING HELPER PURPOSE MEMORY BLOCK V6 / upsert_page_workflow_status
# EN:
# EN: Why this helper exists:
# EN: - because preranking-specific DB truth for 'upsert_page_workflow_status' should be exposed through one named helper boundary
# EN: - because upper layers should call a readable preranking helper name instead of repeating raw SQL semantics
# EN: - because preranking persistence or lookup should remain inspectable at the Python boundary
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this helper are: conn, url_id, workflow_state, state_reason, linked_snapshot_id, source_run_id, source_note, status_metadata
# EN: - values should match the current Python signature and the live preranking SQL contract below
# EN:
# EN: Accepted output:
# EN: - a preranking-oriented result shape defined by the current function body and DB truth
# EN: - this may be a structured payload, a score/signal write result, a lookup result, or another explicit branch result
# EN:
# EN: Common preranking meaning hints:
# EN: - this helper exposes one named preranking-specific DB-truth boundary
# EN:
# EN: Important beginner reminder:
# EN: - this helper is not the source of truth about full ranking policy by itself
# EN: - it is the named boundary where preranking-side truth becomes durable or readable
# EN:
# EN: Undesired behavior:
# EN: - silent hidden mutation without a named helper boundary
# EN: - forcing upper layers to understand raw preranking SQL semantics instead of this helper contract
# TR: PRERANKING YARDIMCISI AMAÇ HAFIZA BLOĞU V6 / upsert_page_workflow_status
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü 'upsert_page_workflow_status' için prerankinge özgü DB doğrusu tek ve isimli bir yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ham preranking SQL semantiğini tekrar etmek yerine okunabilir preranking yardımcı adı çağırmalıdır
# TR: - çünkü preranking kalıcılığı veya okuması Python sınırında denetlenebilir kalmalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu yardımcının açık parametreleri şunlardır: conn, url_id, workflow_state, state_reason, linked_snapshot_id, source_run_id, source_note, status_metadata
# TR: - değerler aşağıdaki mevcut Python imzası ve canlı preranking SQL sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi ve DB doğrusu tarafından belirlenen preranking-odaklı sonuç şekli
# TR: - bu; yapılı payload, score/signal write sonucu, lookup sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak preranking anlam ipuçları:
# TR: - bu yardımcı prerankinge özgü isimli bir DB-truth sınırını açığa çıkarır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu yardımcı tek başına tam ranking politikasının kaynağı değildir
# TR: - bu, preranking tarafı doğrusunun kalıcı veya okunabilir hale geldiği isimli sınırdır
# TR:
# TR: İstenmeyen davranış:
# TR: - isimli yardımcı sınırı olmadan sessiz gizli değişim
# TR: - üst katmanları bu yardımcı sözleşmesi yerine ham preranking SQL semantiğini anlamaya zorlamak

# EN: REAL-RULE AST REPAIR / DEF upsert_page_workflow_status
# EN: upsert_page_workflow_status is an explicit preranking-gateway helper/runtime contract.
# EN: Parameters kept explicit here: conn, url_id, workflow_state, state_reason, linked_snapshot_id, source_run_id, source_note, status_metadata.
# TR: REAL-RULE AST REPAIR / FONKSIYON upsert_page_workflow_status
# TR: upsert_page_workflow_status acik bir preranking-gateway helper/runtime sozlesmesidir.
# TR: Burada acik tutulan parametreler: conn, url_id, workflow_state, state_reason, linked_snapshot_id, source_run_id, source_note, status_metadata.
def upsert_page_workflow_status(
    conn: psycopg.Connection,
    *,
    url_id: int,
    workflow_state: str,
    state_reason: str | None = None,
    linked_snapshot_id: int | None = None,
    source_run_id: str | None = None,
    source_note: str | None = None,
    status_metadata: dict | None = None,
) -> dict:
    # EN: We default metadata to an empty dict so the SQL layer always receives
    # EN: a valid JSON object shape.
    # TR: SQL katmanı her zaman geçerli bir JSON nesne şekli alsın diye metadata'yı
    # TR: varsayılan olarak boş sözlüğe indiriyoruz.
    # EN: REAL-RULE AST REPAIR / LOCAL upsert_page_workflow_status / effective_status_metadata
    # EN: effective_status_metadata are assigned here as explicit intermediate branch values.
    # TR: REAL-RULE AST REPAIR / YEREL upsert_page_workflow_status / effective_status_metadata
    # TR: effective_status_metadata burada acik ara dal degerleri olarak atanir.
    effective_status_metadata = {} if status_metadata is None else status_metadata

    # EN: We import json locally because this helper converts Python metadata into
    # EN: JSON text for SQL.
    # TR: Bu yardımcı Python metadata'sını SQL için JSON metnine çevirdiği için
    # TR: json modülünü yerel olarak içe aktarıyoruz.
    import json

    # EN: We open a cursor from the active connection.
    # TR: Aktif bağlantıdan bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical parse workflow upsert function.
        # TR: Kanonik parse workflow upsert fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from parse.upsert_page_workflow_status(
                p_url_id := %s,
                p_workflow_state := %s::parse.workflow_state_enum,
                p_state_reason := %s,
                p_linked_snapshot_id := %s,
                p_source_run_id := %s,
                p_source_note := %s,
                p_status_metadata := %s::jsonb
            )
            """,
            [
                url_id,
                workflow_state,
                state_reason,
                linked_snapshot_id,
                source_run_id,
                source_note,
                json.dumps(effective_status_metadata),
            ],
        )

        # EN: We fetch exactly one returned row.
        # TR: Dönen tam bir satırı çekiyoruz.
        row = cur.fetchone()

    # EN: A no-row response must degrade into an operator-visible payload instead
    # EN: of aborting the parent parse runtime again.
    # TR: No-row yanıtı parent parse runtime'ı yeniden abort etmek yerine
    # TR: operatörün görebileceği degrade payload'a dönmelidir.
    if row is None:
        return build_preranking_no_row_payload(
            action="parse_upsert_page_workflow_status",
            url_id=url_id,
            linked_snapshot_id=linked_snapshot_id,
            workflow_state=workflow_state,
            state_reason=state_reason,
            error_class="workflow_status_no_row",
            error_message="parse.upsert_page_workflow_status(...) returned no row",
        )

    # EN: We return the structured row to the caller.
    # TR: Yapılı satırı çağırana döndürüyoruz.
    return row
