# EN: This module is the frontier child of the state DB gateway family.
# EN: It owns only frontier claim, lease, success, retryable, permanent, and
# EN: release DB wrappers.
# TR: Bu modül state DB gateway ailesinin frontier alt yüzeyidir.
# TR: Yalnızca frontier claim, lease, success, retryable, permanent ve release
# TR: DB wrapper'larını taşır.

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

# EN: We import the shared ClaimedUrl shape and row-mapping helper from the
# EN: gateway-support child so frontier wrappers keep one canonical row contract.
# TR: Frontier wrapper'ları tek bir kanonik satır sözleşmesi kullansın diye
# TR: paylaşılan ClaimedUrl şeklini ve satır-eşleme yardımcısını gateway-support
# TR: alt yüzeyinden içe aktarıyoruz.
from .logisticsearch1_1_1_1_gateway_support import ClaimedUrl, _row_to_claimed_url




# EN: This function calls the canonical crawler-core claim entry point.
# TR: Bu fonksiyon, kanonik crawler-core claim giriş noktasını çağırır.
def claim_next_url(
    conn: psycopg.Connection,
    worker_id: str,
    lease_seconds: int,
) -> ClaimedUrl | None:
    # EN: We open a cursor from the existing connection so we can execute SQL
    # EN: statements inside the caller-controlled transaction scope.
    # TR: SQL ifadelerini çağıran tarafın kontrol ettiği transaction kapsamı
    # TR: içinde çalıştırabilmek için mevcut bağlantıdan bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We execute the canonical function instead of re-implementing
        # EN: scheduling rules in Python because the repository docs say the DB
        # EN: is the durable truth of claimability.
        # TR: Repository dokümanları claim edilebilirlik doğrusunun veritabanında
        # TR: olduğunu söylediği için zamanlama kurallarını Python'da yeniden yazmak
        # TR: yerine kanonik fonksiyonu çalıştırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM frontier.claim_next_url(
                p_worker_id => %(worker_id)s,
                p_lease_duration => make_interval(secs => %(lease_seconds)s)
            )
            """,
            {
                "worker_id": worker_id,
                "lease_seconds": lease_seconds,
            },
        )

        # EN: We fetch at most one row because crawler-core claim_next_url(...)
        # EN: is already designed to claim exactly one eligible URL.
        # TR: En fazla bir satır çekiyoruz; çünkü crawler-core claim_next_url(...)
        # TR: zaten tam olarak bir uygun URL claim edecek şekilde tasarlanmıştır.
        row = cur.fetchone()

    # EN: If no row exists, the worker currently has no claimable work.
    # TR: Hiç satır yoksa worker'ın şu anda claim edebileceği iş yok demektir.
    if row is None:
        # EN: We return None to make the no-work state explicit in Python.
        # TR: Python tarafında iş-yok durumunu açık hale getirmek için None döndürüyoruz.
        return None

    # EN: If a row exists, we convert it into our strongly-shaped Python object.
    # TR: Satır varsa onu şekli net Python nesnemize dönüştürüyoruz.
    return _row_to_claimed_url(row)



# EN: This function tries to renew an already-owned lease.
# TR: Bu fonksiyon, halihazırda sahip olunan bir lease'i yenilemeyi dener.
def renew_url_lease(
    conn: psycopg.Connection,
    url_id: int,
    lease_token: str,
    worker_id: str,
    extend_seconds: int,
) -> dict[str, Any] | None:
    # EN: We again use the existing connection because transaction ownership
    # EN: should stay under the caller/runtime layer.
    # TR: Yine mevcut bağlantıyı kullanıyoruz; çünkü transaction sahipliği
    # TR: çağıran taraf/runtime katmanı altında kalmalıdır.
    with conn.cursor() as cur:
        # EN: We call the canonical renewal function exactly as the docs require.
        # TR: Dokümanların gerektirdiği şekilde kanonik renewal fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            SELECT *
            FROM frontier.renew_url_lease(
                p_url_id => %(url_id)s,
                p_lease_token => %(lease_token)s::uuid,
                p_worker_id => %(worker_id)s,
                p_extend_by => make_interval(secs => %(extend_seconds)s)
            )
            """,
            {
                "url_id": url_id,
                "lease_token": lease_token,
                "worker_id": worker_id,
                "extend_seconds": extend_seconds,
            },
        )

        # EN: We fetch one row because a successful renewal should validate one
        # EN: currently-owned lease, not many.
        # TR: Tek satır çekiyoruz; çünkü başarılı bir renewal, birden fazla değil,
        # TR: mevcut sahip olunan tek bir lease'i doğrulamalıdır.
        row = cur.fetchone()

    # EN: We return the row directly for now because the renewal surface may grow
    # EN: before we lock its final Python representation.
    # TR: Şimdilik satırı doğrudan döndürüyoruz; çünkü renewal yüzeyi nihai Python
    # TR: temsili kilitlenmeden önce büyüyebilir.
    return row



def finish_fetch_success(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int,
    content_type: str | None,
    body_bytes: int,
    etag: str | None = None,
    last_modified: str | None = None,
) -> dict:
    # EN: We open a cursor because the finalize SQL function is executed as one
    # EN: explicit database statement inside the current transaction.
    # TR: Finalize SQL fonksiyonu mevcut transaction içinde tek bir açık veritabanı
    # TR: ifadesi olarak çalıştırıldığı için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core success finalize function and
        # EN: pass the leased URL identity plus visible fetch metadata.
        # TR: Kanonik crawler-core success finalize fonksiyonunu çağırıyor ve
        # TR: leased URL kimliğini görünür fetch metadata'sı ile birlikte iletiyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_success(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_content_type => %s,
                p_body_bytes => %s,
                p_etag => %s,
                p_last_modified => %s
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                content_type,
                body_bytes,
                etag,
                last_modified,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        raise RuntimeError("frontier.finish_fetch_success(...) returned no row")

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row



# EN: This helper finalizes a retryable fetch failure for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için retryable fetch hatasını finalize eder.

# EN: This helper calls frontier.release_parse_pending_to_queued(...) so Python can
# EN: move a success-finalized frontier row out of transient parse_pending and back
# EN: into the normal revisit queue without changing its already-computed next_fetch_at.
# TR: Bu yardımcı frontier.release_parse_pending_to_queued(...) çağrısını yapar;
# TR: böylece Python success-finalize edilmiş frontier satırını geçici parse_pending
# TR: durumundan, önceden hesaplanmış next_fetch_at değerini bozmadan normal revisit
# TR: kuyruğuna geri taşıyabilir.
def release_parse_pending_to_queued(
    conn: psycopg.Connection,
    *,
    url_id: int,
) -> dict[str, Any]:
    # EN: We open one isolated cursor because this helper performs one explicit
    # EN: crawler-core state transition call.
    # TR: Bu yardımcı tek bir açık crawler-core durum geçiş çağrısı yaptığı için
    # TR: izole bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core function instead of issuing an ad hoc
        # EN: update so Python stays aligned with the sealed SQL contract.
        # TR: Python tarafı mühürlü SQL sözleşmesiyle hizalı kalsın diye özel bir
        # TR: update yazmak yerine kanonik crawler-core fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.release_parse_pending_to_queued(
                p_url_id => %(url_id)s
            )
            """,
            {
                "url_id": url_id,
            },
        )

        # EN: We fetch exactly one row because one call should release at most one
        # EN: frontier row.
        # TR: Tek çağrı en fazla bir frontier satırını serbest bırakması gerektiği
        # TR: için tam bir satır çekiyoruz.
        row = cur.fetchone()

    # EN: Missing output is a structural failure because the canonical crawler-core
    # EN: release function should always report the current persisted state.
    # TR: Çıktı yoksa bu yapısal hatadır; çünkü kanonik crawler-core release
    # TR: fonksiyonu mevcut persist edilmiş durumu her zaman raporlamalıdır.
    if row is None:
        raise RuntimeError("frontier.release_parse_pending_to_queued(...) returned no row")

    # EN: We return the raw mapping because it is already beginner-readable.
    # TR: Ham mapping'i döndürüyoruz; çünkü zaten beginner-okunur yapıdadır.
    return row



def finish_fetch_retryable_error(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int | None,
    error_class: str,
    error_message: str | None,
    retry_delay: str | None = None,
) -> dict:
    # EN: We open a cursor because the retryable finalize SQL function must run
    # EN: inside the current controlled transaction.
    # TR: Retryable finalize SQL fonksiyonu mevcut kontrollü transaction içinde
    # TR: çalışmak zorunda olduğu için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core retryable-error finalize function.
        # TR: Kanonik crawler-core retryable-error finalize fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_retryable_error(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_error_class => %s,
                p_error_message => %s,
                p_retry_delay => %s::interval
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                error_class,
                error_message,
                retry_delay,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        raise RuntimeError("frontier.finish_fetch_retryable_error(...) returned no row")

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row



# EN: This helper finalizes a permanent fetch failure for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için permanent fetch hatasını finalize eder.
def finish_fetch_permanent_error(
    conn: psycopg.Connection,
    *,
    url_id: int,
    lease_token: str,
    http_status: int | None,
    error_class: str,
    error_message: str | None,
) -> dict:
    # EN: We open a cursor because the permanent finalize SQL function must run
    # EN: inside the current controlled transaction.
    # TR: Permanent finalize SQL fonksiyonu mevcut kontrollü transaction içinde
    # TR: çalışmak zorunda olduğu için cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We call the canonical crawler-core permanent-error finalize function.
        # TR: Kanonik crawler-core permanent-error finalize fonksiyonunu çağırıyoruz.
        cur.execute(
            """
            select *
            from frontier.finish_fetch_permanent_error(
                p_url_id => %s,
                p_lease_token => %s::uuid,
                p_http_status => %s,
                p_error_class => %s,
                p_error_message => %s
            )
            """,
            (
                url_id,
                lease_token,
                http_status,
                error_class,
                error_message,
            ),
        )

        # EN: We fetch the single canonical finalize result row.
        # TR: Tek kanonik finalize sonuç satırını çekiyoruz.
        row = cur.fetchone()

    # EN: A missing row would mean the finalize path did not behave as expected.
    # TR: Eksik bir satır finalize yolunun beklendiği gibi davranmadığı anlamına gelir.
    if row is None:
        raise RuntimeError("frontier.finish_fetch_permanent_error(...) returned no row")

    # EN: We return the structured finalize result.
    # TR: Yapılı finalize sonucunu döndürüyoruz.
    return row
