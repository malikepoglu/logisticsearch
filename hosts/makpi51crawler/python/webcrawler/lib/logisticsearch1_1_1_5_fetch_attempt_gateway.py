# EN: This module is the fetch-attempt child of the state DB gateway family.
# EN: It owns only the terminal fetch-attempt logging wrapper.
# TR: Bu modül state DB gateway ailesinin fetch-attempt alt yüzeyidir.
# TR: Yalnızca terminal fetch-attempt logging wrapper'ını taşır.

from __future__ import annotations

# EN: We import typing helpers conservatively because some DB wrapper signatures
# EN: use structured Python types in annotations.
# TR: Bazı DB wrapper imzaları annotation içinde yapılı Python tipleri kullandığı
# TR: için typing yardımcılarını muhafazakâr biçimde içe aktarıyoruz.
from typing import Any

# EN: We import psycopg because this function is a thin wrapper around one SQL call.
# TR: Bu fonksiyon tek bir SQL çağrısının ince wrapper'ı olduğu için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row because the gateway returns dict-like row payloads.
# TR: Gateway dict-benzeri satır payload'ları döndürdüğü için dict_row içe aktarıyoruz.
from psycopg.rows import dict_row




# EN: This helper rolls back the current transaction.
# TR: Bu yardımcı, mevcut transaction'ı rollback eder.

# EN: This helper finalizes a successful fetch outcome for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için başarılı fetch sonucunu finalize eder.

# EN: This helper writes one terminal durable fetch_attempt row through the new
# EN: canonical SQL surface without mutating frontier state.
# TR: Bu yardımcı frontier durumunu değiştirmeden yeni kanonik SQL yüzeyi
# TR: üzerinden tek bir terminal kalıcı fetch_attempt satırı yazar.
def log_fetch_attempt_terminal(
    conn: psycopg.Connection,
    *,
    url_id: int | None,
    host_id: int,
    worker_id: str,
    request_url: str,
    outcome: str,
    fetch_kind: str = "page",
    lease_token: str | None = None,
    request_method: str = "GET",
    final_url: str | None = None,
    http_status: int | None = None,
    content_type: str | None = None,
    content_length: int | None = None,
    body_storage_path: str | None = None,
    body_sha256: str | None = None,
    body_bytes: int | None = None,
    etag: str | None = None,
    last_modified: str | None = None,
    error_class: str | None = None,
    error_message: str | None = None,
    fetch_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # EN: We open one isolated cursor because this helper performs exactly one
    # EN: explicit insert-through-function call.
    # TR: Bu yardımcı tam olarak tek bir açık fonksiyon-üzerinden-insert çağrısı
    # TR: yaptığı için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical terminal logging function instead of inserting
        # EN: into http_fetch.fetch_attempt directly so Python stays aligned with
        # EN: the sealed SQL contract.
        # TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye
        # TR: http_fetch.fetch_attempt tablosuna doğrudan insert atmak yerine
        # TR: kanonik terminal logging fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from http_fetch.log_fetch_attempt_terminal(
                p_url_id => %(url_id)s,
                p_host_id => %(host_id)s,
                p_worker_id => %(worker_id)s,
                p_request_url => %(request_url)s,
                p_outcome => %(outcome)s::http_fetch.fetch_outcome_enum,
                p_fetch_kind => %(fetch_kind)s::http_fetch.fetch_kind_enum,
                p_lease_token => %(lease_token)s::uuid,
                p_request_method => %(request_method)s,
                p_final_url => %(final_url)s,
                p_http_status => %(http_status)s,
                p_content_type => %(content_type)s,
                p_content_length => %(content_length)s,
                p_body_storage_path => %(body_storage_path)s,
                p_body_sha256 => %(body_sha256)s,
                p_body_bytes => %(body_bytes)s,
                p_etag => %(etag)s,
                p_last_modified => %(last_modified)s,
                p_error_class => %(error_class)s,
                p_error_message => %(error_message)s,
                p_fetch_metadata => %(fetch_metadata)s::jsonb
            )
            """,
            {
                "url_id": url_id,
                "host_id": host_id,
                "worker_id": worker_id,
                "request_url": request_url,
                "outcome": outcome,
                "fetch_kind": fetch_kind,
                "lease_token": lease_token,
                "request_method": request_method,
                "final_url": final_url,
                "http_status": http_status,
                "content_type": content_type,
                "content_length": content_length,
                "body_storage_path": body_storage_path,
                "body_sha256": body_sha256,
                "body_bytes": body_bytes,
                "etag": etag,
                "last_modified": last_modified,
                "error_class": error_class,
                "error_message": error_message,
                "fetch_metadata": psycopg.types.json.Jsonb(fetch_metadata or {}),
            },
        )

        # EN: We fetch the single inserted canonical log row.
        # TR: Tek eklenen kanonik log satırını çekiyoruz.
        row = cur.fetchone()

    # EN: Missing output would mean the terminal logging surface failed structurally.
    # TR: Çıktı yoksa terminal logging yüzeyi yapısal olarak başarısız olmuş demektir.
    if row is None:
        raise RuntimeError("http_fetch.log_fetch_attempt_terminal(...) returned no row")

    # EN: We return the structured inserted row so the caller can surface it in
    # EN: operator-visible result payloads when useful.
    # TR: Çağıran taraf gerekirse bunu operatörün göreceği sonuç payload'ına
    # TR: ekleyebilsin diye yapılı eklenen satırı döndürüyoruz.
    return row
