# EN: This module is the preranking child of the state DB gateway family.
# EN: It owns only taxonomy/preranking/workflow DB wrappers.
# TR: Bu modül state DB gateway ailesinin preranking alt yüzeyidir.
# TR: Yalnızca taxonomy/preranking/workflow DB wrapper'larını taşır.

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



# EN: This helper calls parse.persist_taxonomy_preranking_payload(...) so Python
# EN: can persist one minimal parse payload into the parse schema.
# TR: Bu yardımcı parse.persist_taxonomy_preranking_payload(...) çağrısını yapar;
# TR: böylece Python tek bir minimal parse payload'ını parse şemasına yazabilir.
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
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        raise RuntimeError("payload['candidates'] must be a list")

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

    # EN: Returning no row is a structural failure because persistence should
    # EN: always report what it wrote.
    # TR: Hiç satır dönmemesi yapısal hatadır; çünkü persistence ne yazdığını
    # TR: her zaman raporlamalıdır.
    if row is None:
        raise RuntimeError("parse.persist_taxonomy_preranking_payload(...) returned no row")

    # EN: We return the structured row to the caller.
    # TR: Yapılı satırı çağırana döndürüyoruz.
    return row



# EN: This helper calls parse.persist_page_preranking_snapshot(...) so Python can
# EN: materialize the durable preranking snapshot row after evidence/candidate persistence.
# TR: Bu yardımcı parse.persist_page_preranking_snapshot(...) çağrısını yapar;
# TR: böylece evidence/candidate persistence sonrasında kalıcı preranking snapshot
# TR: satırı Python tarafından üretilebilir.
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
    candidate_summary_json = json.dumps(candidate_summary or [])
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

    # EN: Missing output means the canonical SQL function behaved unexpectedly.
    # TR: Çıktı yoksa kanonik SQL fonksiyonu beklenmedik davranmıştır.
    if row is None:
        raise RuntimeError("parse.persist_page_preranking_snapshot(...) returned no row")

    # EN: We return the raw mapping because it is already beginner-readable.
    # TR: Ham mapping'i döndürüyoruz; çünkü zaten beginner-okunur yapıdadır.
    return row



# EN: This helper calls parse.upsert_page_workflow_status(...) so Python can mark
# EN: the current parse workflow state of one URL explicitly.
# TR: Bu yardımcı parse.upsert_page_workflow_status(...) çağrısını yapar; böylece
# TR: Python tek bir URL'nin mevcut parse workflow durumunu açık biçimde işaretleyebilir.
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

    # EN: Returning no row is a structural failure because workflow upsert should
    # EN: always report the current persisted state.
    # TR: Hiç satır dönmemesi yapısal hatadır; çünkü workflow upsert mevcut
    # TR: persist edilmiş durumu her zaman raporlamalıdır.
    if row is None:
        raise RuntimeError("parse.upsert_page_workflow_status(...) returned no row")

    # EN: We return the structured row to the caller.
    # TR: Yapılı satırı çağırana döndürüyoruz.
    return row
