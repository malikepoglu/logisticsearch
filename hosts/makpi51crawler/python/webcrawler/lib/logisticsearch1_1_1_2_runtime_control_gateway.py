# EN: This module is the runtime-control child of the state DB gateway family.
# EN: It owns only the narrow DB wrappers that read or mutate durable crawler
# EN: runtime-control truth.
# TR: Bu modül state DB gateway ailesinin runtime-control alt yüzeyidir.
# TR: Yalnızca kalıcı crawler runtime-control doğrusunu okuyan veya değiştiren
# TR: dar DB wrapper'larını taşır.

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



# EN: This helper reads the single durable webcrawler runtime-control row from
# EN: the database truth surface.
# TR: Bu yardımcı, veritabanındaki tekil ve kalıcı webcrawler runtime-control
# TR: satırını doğruluk yüzeyinden okur.
def get_webcrawler_runtime_control(
    conn: psycopg.Connection,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is a single read operation.
    # TR: Bu tek bir okuma işlemi olduğu için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical DB function instead of reading the table
        # EN: directly so Python stays aligned with the sealed SQL contract.
        # TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye tabloyu
        # TR: doğrudan okumak yerine kanonik DB fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM ops.get_webcrawler_runtime_control()
            """
        )

        # EN: We fetch one row because the control model is intentionally single-row.
        # TR: Kontrol modeli bilinçli olarak tek satırlı olduğu için tek satır çekiyoruz.
        row = cur.fetchone()

    # EN: We return the raw mapping for now because the current control surface is
    # EN: still small and explicit.
    # TR: Güncel kontrol yüzeyi hâlâ küçük ve açık olduğu için şimdilik ham
    # TR: mapping döndürüyoruz.
    return row



# EN: This helper asks the database whether the crawler is currently allowed to
# EN: claim new work.
# TR: Bu yardımcı, crawler'ın şu anda yeni iş claim etmeye izinli olup olmadığını
# TR: veritabanına sorar.
def webcrawler_runtime_may_claim(
    conn: psycopg.Connection,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this is a single decision query.
    # TR: Bu tek bir karar sorgusu olduğu için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical DB truth function instead of duplicating state
        # EN: interpretation rules inside Python.
        # TR: Durum yorumlama kurallarını Python içinde kopyalamak yerine kanonik
        # TR: DB doğruluk fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM ops.webcrawler_runtime_may_claim()
            """
        )

        # EN: We fetch one row because the current runtime-control model is single-row.
        # TR: Güncel runtime-control modeli tek satırlı olduğu için tek satır çekiyoruz.
        row = cur.fetchone()

    # EN: We return the raw mapping so the caller can inspect both may_claim and
    # EN: the surrounding state details.
    # TR: Çağıran taraf hem may_claim sonucunu hem de etrafındaki durum ayrıntılarını
    # TR: inceleyebilsin diye ham mapping döndürüyoruz.
    return row



# EN: This helper asks the database to change the durable crawler runtime-control
# EN: state through the canonical SQL truth surface.
# TR: Bu yardımcı, kalıcı crawler runtime-control durumunu kanonik SQL doğruluk
# TR: yüzeyi üzerinden değiştirmesi için veritabanına çağrı yapar.
def set_webcrawler_runtime_control(
    conn: psycopg.Connection,
    *,
    desired_state: str,
    state_reason: str,
    requested_by: str,
) -> dict[str, Any] | None:
    # EN: We open one isolated cursor because this helper performs one explicit
    # EN: state-change call inside the caller-owned transaction.
    # TR: Bu yardımcı çağıranın sahip olduğu transaction içinde tek bir açık
    # TR: durum-değiştirme çağrısı yaptığı için izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical SQL function instead of writing directly into
        # EN: the table so Python stays aligned with the sealed DB contract.
        # TR: Python tarafı mühürlü DB sözleşmesiyle hizalı kalsın diye tabloya
        # TR: doğrudan yazmak yerine kanonik SQL fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM ops.set_webcrawler_runtime_control(
                p_desired_state => %(desired_state)s,
                p_state_reason => %(state_reason)s,
                p_requested_by => %(requested_by)s
            )
            """,
            {
                "desired_state": desired_state,
                "state_reason": state_reason,
                "requested_by": requested_by,
            },
        )

        # EN: We fetch one row because the control model is intentionally single-row.
        # TR: Kontrol modeli bilinçli olarak tek satırlı olduğu için tek satır çekiyoruz.
        row = cur.fetchone()

    # EN: We return the raw mapping so the caller can inspect the exact durable
    # EN: state transition result.
    # TR: Çağıran taraf tam kalıcı durum geçişi sonucunu inceleyebilsin diye ham
    # TR: mapping döndürüyoruz.
    return row
