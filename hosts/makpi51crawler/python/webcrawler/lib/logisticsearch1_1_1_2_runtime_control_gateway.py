# EN: We enable postponed evaluation of annotations so type hints stay cleaner
# EN: and forward-friendly across this small gateway surface.
# TR: Type hint'ler daha temiz ve ileriye uyumlu kalsın diye annotation
# TR: çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import Any because each gateway function returns a small dict-shaped row
# EN: payload whose exact SQL-return shape can vary by gateway function.
# TR: Her gateway fonksiyonu küçük sözlük-biçimli bir satır payload'ı döndürür ve
# TR: tam SQL dönüş şekli fonksiyona göre değişebilir; bu yüzden Any kullanıyoruz.
from typing import Any

# EN: We import psycopg because this file is a real PostgreSQL gateway surface.
# TR: Bu dosya gerçek bir PostgreSQL gateway yüzeyi olduğu için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row so each fetched SQL row is exposed as a dict-like object
# EN: with explicit column names instead of tuple-position guessing.
# TR: Her SQL satırı tuple sıra tahmini yerine açık sütun adlarıyla dict-benzeri
# TR: nesne olarak gelsin diye dict_row içe aktarıyoruz.
from psycopg.rows import dict_row


# EN: This function reads the current durable runtime-control row from the DB.
# EN: It must stay a thin SQL wrapper and must hard-fail if the sealed SQL surface
# EN: unexpectedly returns no row.
# TR: Bu fonksiyon DB'den mevcut kalıcı runtime-control satırını okur.
# TR: İnce bir SQL wrapper olarak kalmalı ve mühürlü SQL yüzeyi beklenmedik biçimde
# TR: satır döndürmezse sert hata vermelidir.
def get_webcrawler_runtime_control(conn: psycopg.Connection) -> dict[str, Any]:
    # EN: We open a dict-row cursor so downstream Python code can read stable keys.
    # TR: Aşağı katman Python kodu kararlı anahtarları okuyabilsin diye dict-row
    # TR: cursor açıyoruz.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: We call the sealed SQL function exactly as the runtime-control contract defines it.
        # TR: Mühürlü SQL fonksiyonunu runtime-control sözleşmesinin tanımladığı
        # TR: tam şekliyle çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM ops.get_webcrawler_runtime_control()
            """
        )

        # EN: We fetch the single expected row.
        # TR: Beklenen tek satırı alıyoruz.
        row = cur.fetchone()

    # EN: No row here would mean the lower SQL contract broke its explicit shape.
    # TR: Burada satır çıkmaması alt SQL sözleşmesinin açık şekli bozduğu anlamına gelir.
    if row is None:
        raise RuntimeError("ops.get_webcrawler_runtime_control() returned no row")

    # EN: We normalize the dict-row into a plain dict so upper layers stay simple.
    # TR: Üst katmanlar sade kalsın diye dict-row sonucunu düz dict'e normalize ediyoruz.
    return dict(row)


# EN: This function asks the DB whether crawler runtime currently may claim work.
# EN: It must remain a thin gateway and must hard-fail if no row comes back.
# TR: Bu fonksiyon crawler runtime'ın şu anda iş claim edip edemeyeceğini DB'ye sorar.
# TR: İnce gateway olarak kalmalı ve geri hiç satır gelmezse sert hata vermelidir.
def webcrawler_runtime_may_claim(conn: psycopg.Connection) -> dict[str, Any]:
    # EN: We open a dict-row cursor so the returned policy row stays key-addressable.
    # TR: Dönen politika satırı anahtarlarla erişilebilir kalsın diye dict-row
    # TR: cursor açıyoruz.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: We call the sealed SQL policy function exactly once.
        # TR: Mühürlü SQL politika fonksiyonunu tam bir kez çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM ops.webcrawler_runtime_may_claim()
            """
        )

        # EN: We fetch the single expected row.
        # TR: Beklenen tek satırı alıyoruz.
        row = cur.fetchone()

    # EN: Missing row means the lower SQL contract violated the gateway expectation.
    # TR: Satırın eksik gelmesi alt SQL sözleşmesinin gateway beklentisini ihlal
    # TR: ettiği anlamına gelir.
    if row is None:
        raise RuntimeError("ops.webcrawler_runtime_may_claim() returned no row")

    # EN: We normalize the dict-row into a plain dict.
    # TR: Dict-row sonucunu düz dict'e normalize ediyoruz.
    return dict(row)


# EN: This function writes a durable runtime-control change request into the DB
# EN: through the sealed SQL surface and returns the resulting visible row.
# EN: It must hard-fail if the SQL layer returns no row.
# TR: Bu fonksiyon mühürlü SQL yüzeyi üzerinden DB'ye kalıcı runtime-control
# TR: değişiklik isteği yazar ve ortaya çıkan görünür satırı döndürür.
# TR: SQL katmanı satır döndürmezse sert hata vermelidir.
def set_webcrawler_runtime_control(
    conn: psycopg.Connection,
    *,
    desired_state: str,
    state_reason: str,
    requested_by: str,
) -> dict[str, Any]:
    # EN: We open a dict-row cursor so the returned control row stays explicit.
    # TR: Dönen kontrol satırı açık ve okunur kalsın diye dict-row cursor açıyoruz.
    with conn.cursor(row_factory=dict_row) as cur:
        # EN: We call the sealed SQL mutation function with named parameters so
        # EN: argument meaning stays explicit and audit-friendly.
        # TR: Argüman anlamı açık ve audit-dostu kalsın diye mühürlü SQL mutation
        # TR: fonksiyonunu isimli parametrelerle çağırıyoruz.
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

        # EN: We fetch the single expected row.
        # TR: Beklenen tek satırı alıyoruz.
        row = cur.fetchone()

    # EN: No row would mean the lower mutation contract behaved unexpectedly.
    # TR: Satır dönmemesi alt mutation sözleşmesinin beklenmedik davrandığı
    # TR: anlamına gelir.
    if row is None:
        raise RuntimeError("ops.set_webcrawler_runtime_control() returned no row")

    # EN: We normalize the dict-row into a plain dict.
    # TR: Dict-row sonucunu düz dict'e normalize ediyoruz.
    return dict(row)
