# EN: This module is the gateway-support child of the state DB gateway family.
# EN: It owns the shared DB connection helpers, the ClaimedUrl row shape,
# EN: and the small transaction-boundary helpers used by the narrower child gateways.
# TR: Bu modül state DB gateway ailesinin gateway-support alt yüzeyidir.
# TR: Paylaşılan DB bağlantı yardımcılarını, ClaimedUrl satır şeklini ve daha dar
# TR: alt gateway'lerin kullandığı küçük transaction-boundary yardımcılarını taşır.

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
