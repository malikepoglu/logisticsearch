# EN: This module is the robots child of the state DB gateway family.
# EN: It owns only robots allow/refresh/cache DB wrappers.
# TR: Bu modül state DB gateway ailesinin robots alt yüzeyidir.
# TR: Yalnızca robots allow/refresh/cache DB wrapper'larını taşır.

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




# EN: This helper asks the DB whether the current path appears allowed/blocked
# EN: according to the visible robots decision surface.
# TR: Bu yardımcı, görünür robots karar yüzeyine göre mevcut path'in allowed/blocked
# TR: görünüp görünmediğini veritabanına sorar.
def compute_robots_allow_decision(
    conn: psycopg.Connection,
    host_id: int,
    url_path: str,
) -> dict[str, Any] | None:
    # EN: We open a cursor for one isolated decision query.
    # TR: Tek bir izole karar sorgusu için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the visible allow-decision function because the worker
        # EN: contract explicitly says robots must not be silently ignored.
        # TR: Worker sözleşmesi robots'ın sessizce yok sayılamayacağını açıkça
        # TR: söylediği için görünür allow-decision fonksiyonunu çağırıyoruz.
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
        row = cur.fetchone()

    # EN: We return the raw mapping for now to avoid pretending the final
    # EN: dedicated Python-side robots model is already sealed.
    # TR: Ayrı ve nihai Python-tarafı robots modelinin şimdiden mühürlü olduğunu
    # TR: varsaymamak için şimdilik ham mapping döndürüyoruz.
    return row



# EN: This helper asks the DB whether the current robots cache truth for one host
# EN: should be refreshed right now according to the sealed SQL contract.
# TR: Bu yardımcı, mühürlü SQL sözleşmesine göre tek bir host için mevcut robots
# TR: cache doğrusunun şu anda yenilenmesi gerekip gerekmediğini veritabanına sorar.
def compute_robots_refresh_decision(
    conn: psycopg.Connection,
    host_id: int,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is a single read-only decision query.
    # TR: Bu tek ve salt-okunur karar sorgusu olduğu için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the exact sealed SQL function instead of inventing Python-side
        # EN: refresh logic, because the DB contract already defines the truth.
        # TR: Python tarafında yeni refresh mantığı uydurmak yerine mühürlü SQL
        # TR: fonksiyonunu doğrudan çağırıyoruz; çünkü doğruluk zaten DB sözleşmesinde tanımlı.
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
        row = cur.fetchone()

    # EN: We return the raw mapping for now so Python does not pretend that a
    # EN: stricter dedicated model is already sealed.
    # TR: Python tarafı henüz daha katı özel bir model mühürlenmiş gibi davranmasın
    # TR: diye şimdilik ham mapping'i döndürüyoruz.
    return row



# EN: This helper writes one robots cache truth row through the canonical SQL
# EN: upsert function and returns the structured DB result row.
# TR: Bu yardımcı tek bir robots cache doğrusu satırını kanonik SQL upsert
# TR: fonksiyonu üzerinden yazar ve yapılı DB sonuç satırını döndürür.
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
    import json

    # EN: We serialize JSON-shaped inputs only when they are provided.
    # EN: None stays None so the SQL function can apply its own defaults honestly.
    # TR: JSON-biçimli girdileri yalnızca gerçekten verilmişlerse serileştiriyoruz.
    # TR: None değeri None kalır; böylece SQL fonksiyonu kendi default'larını dürüstçe uygulayabilir.
    parsed_rules_json = None if parsed_rules is None else json.dumps(parsed_rules)
    sitemap_urls_json = None if sitemap_urls is None else json.dumps(sitemap_urls)
    robots_metadata_json = None if robots_metadata is None else json.dumps(robots_metadata)

    # EN: We open a cursor because this helper executes one explicit canonical SQL
    # EN: statement inside the caller's current transaction.
    # TR: Bu yardımcı çağıranın mevcut transaction'ı içinde tek bir açık kanonik SQL
    # TR: ifadesi çalıştırdığı için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the sealed upsert function exactly, including its enum/jsonb
        # EN: parameter casts, so Python stays aligned with the SQL contract.
        # TR: Python tarafı SQL sözleşmesiyle hizalı kalsın diye mühürlü upsert
        # TR: fonksiyonunu enum/jsonb cast'leriyle birlikte tam olarak çağırıyoruz.
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
        row = cur.fetchone()

    # EN: Returning no row would mean the canonical wrapper contract was broken.
    # TR: Hiç satır dönmemesi, kanonik wrapper sözleşmesinin bozulduğu anlamına gelir.
    if row is None:
        raise RuntimeError("http_fetch.upsert_robots_txt_cache(...) returned no row")

    # EN: We return the structured DB row to the caller.
    # TR: Yapılı DB satırını çağırana döndürüyoruz.
    return row
