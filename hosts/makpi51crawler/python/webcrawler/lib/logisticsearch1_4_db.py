# EN: We enable postponed evaluation of type hints so that type annotations can
# EN: refer to classes and types that may be defined later in the file without
# EN: forcing Python to resolve them immediately at import time.
# TR: Type hint çözümlemesini ertelemeyi açıyoruz. Böylece type annotation'lar
# TR: dosyanın ilerleyen kısmında tanımlanacak sınıflara veya tiplere hemen
# TR: import anında çözülmek zorunda kalmadan referans verebilir.
from __future__ import annotations

# EN: We import dataclass because we want a small, explicit, strongly-shaped
# EN: container for the claimed crawler work row coming from PostgreSQL.
# TR: dataclass içe aktarıyoruz; çünkü PostgreSQL'den gelen claim edilmiş
# TR: crawler iş satırı için küçük, açık ve şekli net bir veri taşıyıcısı istiyoruz.
from dataclasses import dataclass

# EN: We import Any because some DB-returned fields may temporarily remain
# EN: flexible until later runtime layers become stricter and more sealed.
# TR: Any içe aktarıyoruz; çünkü veritabanından dönen bazı alanlar daha sonraki
# TR: runtime katmanları daha katı biçimde mühürlenene kadar geçici olarak esnek kalabilir.
from typing import Any

# EN: We import psycopg, the PostgreSQL client library expected for modern
# EN: Python-side PostgreSQL work in this project surface.
# TR: psycopg içe aktarıyoruz; bu proje yüzeyinde modern Python-tarafı PostgreSQL
# TR: çalışmaları için beklenen istemci kütüphanesidir.
import psycopg

# EN: We import dict_row so that database query results can come back as
# EN: dictionary-like mappings with column names, which is much easier to read
# EN: and audit than positional tuple indexing for a beginner-friendly surface.
# TR: dict_row içe aktarıyoruz; böylece veritabanı sorgu sonuçları sütun adlarıyla
# TR: sözlük-benzeri yapılar olarak dönebilir. Bu, beginner-friendly bir yüzey için
# TR: pozisyonel tuple index kullanımından çok daha okunabilir ve denetlenebilirdir.
from psycopg.rows import dict_row


# EN: This dataclass represents exactly one claimed work item returned by the
# EN: canonical crawler-core function frontier.claim_next_url(...).
# TR: Bu dataclass, kanonik crawler-core fonksiyonu frontier.claim_next_url(...)
# TR: tarafından döndürülen tam bir claim edilmiş iş öğesini temsil eder.
@dataclass(slots=True)
class ClaimedUrl:
    # EN: url_id is the durable numeric identity of the frontier.url row.
    # TR: url_id, frontier.url satırının kalıcı sayısal kimliğidir.
    url_id: int

    # EN: host_id is the durable numeric identity of the related frontier.host row.
    # TR: host_id, ilgili frontier.host satırının kalıcı sayısal kimliğidir.
    host_id: int

    # EN: canonical_url is the normalized URL string that the crawler should
    # EN: treat as the canonical work target.
    # TR: canonical_url, crawler'ın kanonik iş hedefi olarak görmesi gereken
    # TR: normalize edilmiş URL metnidir.
    canonical_url: str

    # EN: url_path is the path portion of the URL and is especially important
    # EN: for robots allow/block decisions.
    # TR: url_path, URL'nin path bölümüdür ve özellikle robots allow/block
    # TR: kararları için önemlidir.
    url_path: str

    # EN: url_query stores the query-string part when it exists.
    # TR: url_query, varsa query-string bölümünü tutar.
    url_query: str | None

    # EN: depth is the crawl depth currently associated with this URL.
    # TR: depth, bu URL ile ilişkili mevcut crawl derinliğidir.
    depth: int

    # EN: priority is the current scheduling priority selected by crawler-core.
    # TR: priority, crawler-core tarafından seçilmiş mevcut zamanlama önceliğidir.
    priority: int

    # EN: score is a numeric ranking-like field already present in crawler-core.
    # TR: score, crawler-core içinde halihazırda bulunan sayısal skor alanıdır.
    score: Any

    # EN: lease_token is the durable lease ownership token returned by the DB.
    # TR: lease_token, veritabanının döndürdüğü kalıcı lease sahiplik token'ıdır.
    lease_token: str

    # EN: lease_expires_at is the timestamp that marks when current ownership
    # EN: should be treated as expired unless renewed earlier.
    # TR: lease_expires_at, mevcut sahipliğin daha önce yenilenmedikçe ne zaman
    # TR: süresi dolmuş sayılması gerektiğini gösteren timestamp değeridir.
    lease_expires_at: Any

    # EN: scheme stores http/https information.
    # TR: scheme, http/https bilgisini tutar.
    scheme: str

    # EN: host stores the host/domain name.
    # TR: host, host/domain adını tutar.
    host: str

    # EN: port stores the resolved port value used by crawler-core.
    # TR: port, crawler-core tarafından kullanılan çözülmüş port değerini tutar.
    port: int

    # EN: authority_key is the normalized host:port identity.
    # TR: authority_key, normalize edilmiş host:port kimliğidir.
    authority_key: str

    # EN: user_agent_token is the user-agent identity selected at host level.
    # TR: user_agent_token, host seviyesinde seçilen user-agent kimliğidir.
    user_agent_token: str

    # EN: robots_mode tells the worker whether this host should respect or
    # EN: ignore robots rules according to current DB truth.
    # TR: robots_mode, worker'a bu host için robots kurallarına mevcut DB doğrusuna
    # TR: göre saygı gösterilip gösterilmeyeceğini söyler.
    robots_mode: str


# EN: This helper opens a PostgreSQL connection using a DSN string and
# EN: configures row_factory=dict_row so that results stay beginner-readable.
# TR: Bu yardımcı, bir DSN metni kullanarak PostgreSQL bağlantısı açar ve
# TR: row_factory=dict_row ayarını yapar; böylece sonuçlar beginner seviyesinde okunabilir kalır.
def connect_db(dsn: str) -> psycopg.Connection:
    # EN: We call psycopg.connect with autocommit disabled on purpose because
    # EN: explicit transaction control is safer and more auditable for crawler work.
    # TR: psycopg.connect çağrısını autocommit kapalı şekilde bilinçli yapıyoruz;
    # TR: çünkü açık transaction kontrolü crawler işi için daha güvenli ve denetlenebilirdir.
    conn = psycopg.connect(dsn, row_factory=dict_row)

    # EN: We return the connection object so the caller can decide transaction
    # EN: boundaries explicitly.
    # TR: Çağıran taraf transaction sınırlarını açıkça belirleyebilsin diye
    # TR: bağlantı nesnesini geri döndürüyoruz.
    return conn

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



# EN: This helper converts a dict-like database row into a strongly-shaped
# EN: ClaimedUrl dataclass instance.
# TR: Bu yardımcı, sözlük-benzeri bir veritabanı satırını şekli net bir
# TR: ClaimedUrl dataclass örneğine dönüştürür.
def _row_to_claimed_url(row: dict[str, Any]) -> ClaimedUrl:
    # EN: We map each expected column name explicitly instead of relying on
    # EN: magical unpacking so that the shape stays easy to audit.
    # TR: Şekil kolay denetlenebilir kalsın diye her beklenen sütun adını,
    # TR: sihirli unpack yöntemine güvenmeden açıkça eşliyoruz.
    return ClaimedUrl(
        url_id=row["url_id"],
        host_id=row["host_id"],
        canonical_url=row["canonical_url"],
        url_path=row["url_path"],
        url_query=row["url_query"],
        depth=row["depth"],
        priority=row["priority"],
        score=row["score"],
        lease_token=str(row["lease_token"]),
        lease_expires_at=row["lease_expires_at"],
        scheme=row["scheme"],
        host=row["host"],
        port=row["port"],
        authority_key=row["authority_key"],
        user_agent_token=row["user_agent_token"],
        robots_mode=row["robots_mode"],
    )


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


# EN: This helper rolls back the current transaction.
# TR: Bu yardımcı, mevcut transaction'ı rollback eder.

# EN: This helper finalizes a successful fetch outcome for one leased frontier URL.
# TR: Bu yardımcı leased durumdaki tek bir frontier URL için başarılı fetch sonucunu finalize eder.
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


def rollback(conn: psycopg.Connection) -> None:
    # EN: A rollback is especially useful for safe probe-style worker steps that
    # EN: must prove claimability without leaving durable leased residue.
    # TR: Rollback özellikle claim edilebilirliği kanıtlarken kalıcı leased izi
    # TR: bırakmaması gereken güvenli probe-tarzı worker adımları için faydalıdır.
    conn.rollback()


# EN: This helper commits the current transaction.
# TR: Bu yardımcı, mevcut transaction'ı commit eder.
def commit(conn: psycopg.Connection) -> None:
    # EN: We keep commit explicit because durable state change must never happen
    # EN: by accident in crawler work.
    # TR: Commit'i açık tutuyoruz; çünkü crawler işinde kalıcı durum değişikliği
    # TR: asla kazara olmamalıdır.
    conn.commit()


# EN: This helper closes the DB connection cleanly.
# TR: Bu yardımcı, veritabanı bağlantısını temiz şekilde kapatır.
def close_db(conn: psycopg.Connection) -> None:
    # EN: Closing explicitly is simpler and safer for a beginner-auditable tool.
    # TR: Açık kapatma, beginner seviyesinde denetlenebilir bir araç için daha basit ve güvenlidir.
    conn.close()

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

