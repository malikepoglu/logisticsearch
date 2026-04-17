# EN: This module is the discovery child of the state DB gateway family.
# EN: It owns only discovery-context read and discovered-URL enqueue DB wrappers.
# TR: Bu modül state DB gateway ailesinin discovery alt yüzeyidir.
# TR: Yalnızca discovery-context okuma ve discovered-URL enqueue DB wrapper'larını taşır.

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




# EN: This helper fetches the minimal parent-URL discovery context needed by the
# EN: HTML discovery bridge.
# TR: Bu yardımcı, HTML discovery köprüsünün ihtiyaç duyduğu minimal parent-URL
# TR: discovery bağlamını getirir.
def fetch_url_discovery_context(
    conn: psycopg.Connection,
    *,
    url_id: int,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is one explicit context query.
    # TR: Bu tek ve açık bağlam sorgusu olduğu için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We read the parent URL together with its host truth from the DB so
        # EN: Python does not invent crawl context on its own.
        # TR: Parent URL'yi host doğrusu ile birlikte DB'den okuyoruz; böylece
        # TR: Python kendi başına crawl context uydurmaz.
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
        row = cur.fetchone()

    # EN: We return the raw mapping so the caller can inspect the exact context.
    # TR: Çağıran taraf tam bağlamı inceleyebilsin diye ham mapping döndürüyoruz.
    return row



# EN: This helper asks the canonical discovery SQL surface to enqueue one
# EN: discovered URL.
# TR: Bu yardımcı, keşfedilmiş tek bir URL'yi enqueue etmesi için kanonik
# TR: discovery SQL yüzeyini çağırır.
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
    with conn.cursor() as cur:
        # EN: We call the canonical frontier function instead of duplicating upsert
        # EN: rules in Python.
        # TR: Upsert kurallarını Python'da kopyalamak yerine kanonik frontier
        # TR: fonksiyonunu çağırıyoruz.
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
        row = cur.fetchone()

    # EN: We return the raw mapping so the caller can inspect the exact enqueue result.
    # TR: Çağıran taraf tam enqueue sonucunu inceleyebilsin diye ham mapping döndürüyoruz.
    return row
