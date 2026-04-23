"""
EN:
This file is the support layer of the state DB gateway family.

In very simple terms:
- If the gateway family were a small office, this file would hold the keys.
- It knows how to open the database door.
- It knows how to turn one raw database row into a clean Python object.
- It knows how to say "save", "cancel", and "close" at the transaction level.

What this file is mainly for:
- Opening a PostgreSQL connection.
- Defining the ClaimedUrl dataclass.
- Converting one dict-like DB row into ClaimedUrl.
- Providing very small transaction helpers: rollback, commit, close_db.

What this file is NOT for:
- It does not choose which URL should be claimed.
- It does not decide robots allow/block.
- It does not parse HTML.
- It does not classify taxonomy.
- It does not finalize fetch outcomes.

Why this separation matters:
- Beginners understand systems faster when one file has one clear job.
- This file is about shared DB support, not about crawler decisions.

Important beginner note:
- "Gateway" means a thin Python layer that talks to SQL.
- "Dataclass" means a named container with labeled fields.
- "ClaimedUrl" is the crawler's clean Python-shaped package for one claimed work item.
- "DSN" is the database connection string, basically the address card for PostgreSQL.

TR:
Bu dosya state DB gateway ailesinin support katmanıdır.

Çok basit anlatımla:
- Gateway ailesi küçük bir ofis olsaydı, bu dosya anahtarları tutan yer olurdu.
- Veritabanı kapısını nasıl açacağını bilir.
- Ham bir veritabanı satırını temiz bir Python nesnesine çevirmeyi bilir.
- Transaction seviyesinde "kaydet", "iptal et", "kapat" demeyi bilir.

Bu dosya esas olarak ne içindir:
- PostgreSQL bağlantısı açmak.
- ClaimedUrl dataclass yapısını tanımlamak.
- Tek bir dict-benzeri DB satırını ClaimedUrl nesnesine çevirmek.
- Çok küçük transaction yardımcıları sağlamak: rollback, commit, close_db.

Bu dosya ne için DEĞİLDİR:
- Hangi URL claim edilsin buna karar vermez.
- Robots allow/block kararı vermez.
- HTML parse etmez.
- Taxonomy sınıflandırması yapmaz.
- Fetch outcome sonlandırmaz.

Bu ayrım neden önemlidir:
- Yeni başlayanlar bir dosyanın tek ve net işi varsa sistemi daha hızlı anlar.
- Bu dosya crawler kararı değil, ortak DB destek işi içindir.

Önemli başlangıç notu:
- "Gateway" SQL ile konuşan ince Python katmanı demektir.
- "Dataclass" etiketli alanları olan isimli bir taşıma kabı demektir.
- "ClaimedUrl" claim edilmiş tek iş öğesinin temiz Python paketidir.
- "DSN" veritabanı bağlantı metnidir; yani PostgreSQL için adres kartı gibi düşünülür.
"""


# EN: GATEWAY SUPPORT IDENTITY MEMORY BLOCK V4
# EN:
# EN: Why this file exists:
# EN: - because the gateway family needs one child that owns the shared low-level DB support truth
# EN: - because connection opening, small transaction helpers, and row-shape conversion should not be duplicated everywhere
# EN: - because higher gateway children should focus on narrower crawler meanings, not on repeating support plumbing
# EN:
# EN: What this file DOES:
# EN: - define shared support-layer shapes
# EN: - open DB connections
# EN: - provide tiny transaction helpers
# EN: - convert one DB row payload into a clean ClaimedUrl object
# EN:
# EN: What this file DOES NOT do:
# EN: - it does not decide crawler policy
# EN: - it does not decide robots allow/block
# EN: - it does not parse HTML
# EN: - it does not rank or finalize work
# EN:
# EN: Topological role:
# EN: - parent gateway hub re-exports names from here
# EN: - narrower gateway children depend on these shared support primitives
# EN: - this file sits below policy meaning and above raw DB connection mechanics
# EN:
# EN: Important shared values and shapes:
# EN: - dsn => DB connection identity text
# EN: - conn => live psycopg connection object
# EN: - row => one DB row payload, commonly dict-like
# EN: - ClaimedUrl => clean Python package for one claimed work item
# EN:
# EN: Accepted architectural identity:
# EN: - shared support child
# EN: - DB helper layer
# EN: - row-shape conversion layer
# EN:
# EN: Undesired architectural identity:
# EN: - hidden crawler decision engine
# EN: - hidden robots policy engine
# EN: - hidden parse engine
# TR: GATEWAY SUPPORT KİMLİK HAFIZA BLOĞU V4
# TR:
# TR: Bu dosya neden var:
# TR: - çünkü gateway ailesi ortak düşük seviye DB destek doğrusuna sahip tek bir child yüzeye ihtiyaç duyar
# TR: - çünkü bağlantı açma, küçük transaction yardımcıları ve satır-şekli dönüşümü her yerde tekrar edilmemelidir
# TR: - çünkü daha dar gateway child'ları tekrar tekrar destek plumbing'i değil kendi crawler anlamlarını taşımalıdır
# TR:
# TR: Bu dosya NE yapar:
# TR: - ortak support katmanı şekillerini tanımlar
# TR: - DB bağlantısı açar
# TR: - küçük transaction yardımcıları sağlar
# TR: - tek bir DB row payload'ını temiz ClaimedUrl nesnesine dönüştürür
# TR:
# TR: Bu dosya NE yapmaz:
# TR: - crawler policy kararı vermez
# TR: - robots allow/block kararı vermez
# TR: - HTML parse etmez
# TR: - işi rank etmez veya finalize etmez
# TR:
# TR: Topolojik rol:
# TR: - parent gateway hub buradaki isimleri yeniden dışa açar
# TR: - daha dar gateway child'ları bu ortak support primitiflerine dayanır
# TR: - bu dosya policy anlamının altında, ham DB bağlantı mekaniğinin üstünde durur
# TR:
# TR: Önemli ortak değerler ve şekiller:
# TR: - dsn => DB bağlantı kimlik metni
# TR: - conn => canlı psycopg bağlantı nesnesi
# TR: - row => tek bir DB row payload'ı, çoğunlukla dict-benzeri
# TR: - ClaimedUrl => claim edilmiş tek iş öğesinin temiz Python paketi
# TR:
# TR: Kabul edilen mimari kimlik:
# TR: - ortak support child
# TR: - DB yardımcı katmanı
# TR: - satır-şekli dönüştürme katmanı
# TR:
# TR: İstenmeyen mimari kimlik:
# TR: - gizli crawler karar motoru
# TR: - gizli robots policy motoru
# TR: - gizli parse motoru

from __future__ import annotations

# EN: dataclass lets us define a small named data container.
# EN: This is easier for beginners to read than passing around a long tuple.
# TR: dataclass küçük ve isimli bir veri kabı tanımlamamızı sağlar.
# TR: Bu yaklaşım uzun bir tuple dolaştırmaktan daha okunurdur.
from dataclasses import dataclass

# EN: Any is used in a few places where the runtime contract is still intentionally
# EN: flexible at this layer.
# TR: Any bazı yerlerde kullanılır; çünkü bu katmanda runtime sözleşmesi bazı
# TR: alanlarda bilinçli olarak esnek bırakılmıştır.
from typing import Any

# EN: psycopg is the PostgreSQL client library used by this project.
# TR: psycopg bu projede kullanılan PostgreSQL istemci kütüphanesidir.
import psycopg

# EN: dict_row tells psycopg to return rows as dict-like objects.
# EN: That means we can write row["url_id"] instead of tuple position access.
# TR: dict_row psycopg'ye satırları dict-benzeri nesne olarak döndürmesini söyler.
# TR: Böylece tuple sıra numarası yerine row["url_id"] yazabiliriz.
from psycopg.rows import dict_row


@dataclass(slots=True)

# EN: CLAIMEDURL DATACLASS PURPOSE MEMORY BLOCK V4
# EN:
# EN: Why this dataclass exists:
# EN: - because one claimed work item should travel through Python as a named object, not as an anonymous row
# EN: - because a beginner should be able to inspect field names instead of memorizing tuple positions
# EN:
# EN: Accepted semantic role:
# EN: - clean Python-shaped representation of one claimed URL work item
# EN:
# EN: Undesired misunderstanding:
# EN: - assuming this object is the SQL row itself
# EN: It is not; it is the converted Python-side shape.
# TR: CLAIMEDURL DATACLASS AMAÇ HAFIZA BLOĞU V4
# TR:
# TR: Bu dataclass neden var:
# TR: - çünkü claim edilmiş tek iş öğesi Python içinde isimsiz satır olarak değil isimli nesne olarak taşınmalıdır
# TR: - çünkü yeni başlayan biri tuple pozisyonlarını ezberlemek yerine alan isimlerini okuyabilmelidir
# TR:
# TR: Kabul edilen semantik rol:
# TR: - claim edilmiş tek URL iş öğesinin temiz Python-şekilli temsili
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu nesnenin SQL satırının kendisi olduğunu sanmak
# TR: Değildir; Python tarafında dönüştürülmüş şekildir.

# EN: GATEWAY SUPPORT CLASS CONTRACT BLOCK / ClaimedUrl
# EN: Why this class exists:
# EN: - because ClaimedUrl gives one claimed work item a stable Python-side shape instead of leaving it as an anonymous DB-looking payload
# EN: - because beginners should be able to read one named container and understand what one claimed URL package contains
# EN: Accepted role:
# EN: - clean Python package for one claimed URL
# EN: - shared gateway-side data carrier
# TR: GATEWAY SUPPORT CLASS SÖZLEŞME BLOĞU / ClaimedUrl
# TR: Bu class neden var:
# TR: - çünkü ClaimedUrl tek bir claim edilmiş iş öğesine anonim DB-görünümlü payload yerine kararlı bir Python tarafı şekli verir
# TR: - çünkü yeni başlayan biri tek bir isimli taşıyıcıyı okuyup claim edilmiş URL paketinin ne içerdiğini anlayabilmelidir
# TR: Kabul edilen rol:
# TR: - tek claim edilmiş URL için temiz Python paketi
# TR: - ortak gateway tarafı veri taşıyıcısı
class ClaimedUrl:
    """
    EN:
    This dataclass is the clean Python package for one claimed URL.

    In very simple terms:
    - PostgreSQL gives us a row.
    - A raw row is useful but still a bit "database-shaped".
    - This dataclass turns that row into a named Python object.
    - Upper runtime layers can then say claimed_url.host or claimed_url.url_id
      instead of repeatedly digging through raw row keys.

    Why this object exists:
    - It makes field names explicit.
    - It reduces confusion.
    - It helps comments and contracts stay attached to each field.
    - It makes debugging easier because the payload shape is named and stable.

    Field contract summary:
    - url_id: required int identity of the frontier.url row.
    - host_id: required int identity of the frontier.host row.
    - canonical_url: required normalized URL text to fetch.
    - url_path: required path text such as "/" or "/about".
    - url_query: optional query-string text; may be None.
    - depth: int crawl depth.
    - priority: int scheduling priority.
    - score: flexible ranking-like value; exact type not sealed here.
    - lease_token: required text proving who currently owns the lease.
    - lease_expires_at: timestamp-like expiry payload.
    - scheme: usually "http" or "https".
    - host: host/domain text.
    - port: effective integer port.
    - authority_key: normalized host:port-like identity.
    - user_agent_token: required selected user-agent label.
    - robots_mode: required host-level robots mode text.

    TR:
    Bu dataclass claim edilmiş tek bir URL için temiz Python paketidir.

    Çok basit anlatımla:
    - PostgreSQL bize bir satır verir.
    - Ham satır faydalıdır ama hâlâ biraz "veritabanı şekilli"dir.
    - Bu dataclass o satırı isimli bir Python nesnesine çevirir.
    - Böylece üst runtime katmanları ham row anahtarlarıyla uğraşmak yerine
      claimed_url.host veya claimed_url.url_id diyebilir.

    Bu nesne neden var:
    - Alan isimlerini açık hale getirir.
    - Karışıklığı azaltır.
    - Yorumların ve sözleşmelerin her alana tutunmasını kolaylaştırır.
    - Payload şekli isimli ve stabil olduğu için debug etmeyi kolaylaştırır.

    Alan sözleşmesi özeti:
    - url_id: frontier.url satırının zorunlu int kimliği.
    - host_id: frontier.host satırının zorunlu int kimliği.
    - canonical_url: fetch edilecek zorunlu normalize URL metni.
    - url_path: "/" veya "/about" gibi zorunlu path metni.
    - url_query: opsiyonel query-string metni; None olabilir.
    - depth: int crawl derinliği.
    - priority: int zamanlama önceliği.
    - score: ranking-benzeri esnek değer; exact tipi burada mühürlü değildir.
    - lease_token: lease'in şu anda kimde olduğunu gösteren zorunlu metin.
    - lease_expires_at: zaman aşımı bitişini anlatan timestamp-benzeri payload.
    - scheme: genellikle "http" veya "https".
    - host: host/domain metni.
    - port: etkin int port.
    - authority_key: normalize host:port-benzeri kimlik.
    - user_agent_token: seçilmiş user-agent etiketi.
    - robots_mode: host seviyesi robots mod metni.
    """

    # EN: url_id is the main row id of frontier.url.
    # EN: It is an int and should not be None in a valid claimed payload.
    # TR: url_id frontier.url satırının ana kimliğidir.
    # TR: int tipindedir ve geçerli claimed payload içinde None olmamalıdır.
    url_id: int

    # EN: host_id is the linked host row id from frontier.host.
    # TR: host_id frontier.host tablosundaki bağlı host satır kimliğidir.
    host_id: int

    # EN: canonical_url is the exact normalized target URL text.
    # EN: Example values: "https://example.org/" or "https://example.org/about".
    # TR: canonical_url tam normalize hedef URL metnidir.
    # TR: Örnek değerler: "https://example.org/" veya "https://example.org/about".
    canonical_url: str

    # EN: url_path is only the path part, not the full URL.
    # EN: Example values: "/", "/team", "/products/item-1".
    # TR: url_path tam URL değil, yalnızca path bölümüdür.
    # TR: Örnek değerler: "/", "/team", "/products/item-1".
    url_path: str

    # EN: url_query is the query-string part without deciding higher-level meaning.
    # EN: It may be None when no query-string exists.
    # TR: url_query query-string bölümüdür; üst seviye anlamı burada çözülmez.
    # TR: Query-string yoksa None olabilir.
    url_query: str | None

    # EN: depth tells how far from the starting point this URL currently is.
    # TR: depth bu URL'nin başlangıç noktasından şu anda ne kadar uzakta olduğunu söyler.
    depth: int

    # EN: priority is the scheduling importance chosen by crawler-core.
    # TR: priority crawler-core tarafından verilmiş zamanlama önem derecesidir.
    priority: int

    # EN: score is intentionally flexible at this layer.
    # EN: It may later become more strictly typed when the contract is sealed harder.
    # TR: score bu katmanda bilinçli olarak esnektir.
    # TR: Sözleşme daha da mühürlenince ileride daha sıkı tipe indirgenebilir.
    score: Any

    # EN: lease_token is the proof string that this worker currently owns the lease.
    # EN: It is required because finalize and renew operations depend on it.
    # TR: lease_token bu worker'ın lease'i şu anda elinde tuttuğunu gösteren kanıt metnidir.
    # TR: Zorunludur; çünkü finalize ve renew işlemleri buna dayanır.
    lease_token: str

    # EN: lease_expires_at tells when the claimed lease should expire.
    # EN: Exact Python type may vary depending on psycopg / SQL return shape.
    # TR: lease_expires_at claim edilmiş lease'in ne zaman biteceğini söyler.
    # TR: Exact Python tipi psycopg / SQL dönüş şekline göre değişebilir.
    lease_expires_at: Any

    # EN: scheme is typically "http" or "https".
    # TR: scheme tipik olarak "http" veya "https" olur.
    scheme: str

    # EN: host is the domain or hostname text.
    # TR: host domain veya hostname metnidir.
    host: str

    # EN: port is the effective numeric port used for network access.
    # TR: port ağ erişiminde kullanılan etkin sayısal porttur.
    port: int

    # EN: authority_key is the normalized authority identity used by crawler-core logic.
    # TR: authority_key crawler-core mantığında kullanılan normalize authority kimliğidir.
    authority_key: str

    # EN: user_agent_token names which user-agent identity was selected.
    # TR: user_agent_token hangi user-agent kimliğinin seçildiğini adlandırır.
    user_agent_token: str

    # EN: robots_mode stores the host-level robots behavior mode text.
    # TR: robots_mode host-seviyesi robots davranış modu metnini taşır.
    robots_mode: str



# EN: CONNECTION HELPER PURPOSE MEMORY BLOCK V4 / connect_db
# EN:
# EN: Why this helper exists:
# EN: - because opening a psycopg connection is shared support work
# EN: - because DSN-to-connection conversion should live in one obvious place
# EN:
# EN: Accepted input:
# EN: - non-empty DSN string
# EN:
# EN: Accepted output:
# EN: - live psycopg connection object
# EN:
# EN: Undesired input:
# EN: - empty DSN
# EN: - whitespace-only DSN
# EN: - malformed unusable DSN text
# TR: BAĞLANTI YARDIMCISI AMAÇ HAFIZA BLOĞU V4 / connect_db
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü psycopg bağlantısı açmak ortak support işidir
# TR: - çünkü DSN'den bağlantı üretme işi tek ve açık yerde yaşamalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - boş olmayan DSN stringi
# TR:
# TR: Kabul edilen çıktı:
# TR: - canlı psycopg bağlantı nesnesi
# TR:
# TR: İstenmeyen girdi:
# TR: - boş DSN
# TR: - yalnızca boşluk içeren DSN
# TR: - bozuk ve kullanılamaz DSN metni

# EN: GATEWAY SUPPORT FUNCTION CONTRACT BLOCK / connect_db
# EN: Why this function exists:
# EN: - because the shared support layer needs one explicit place that opens a psycopg DB session
# EN: Parameter dsn:
# EN: - dsn is the PostgreSQL connection string used to open the live connection
# EN: Accepted output:
# EN: - live psycopg connection object
# TR: GATEWAY SUPPORT FONKSIYON SÖZLEŞME BLOĞU / connect_db
# TR: Bu fonksiyon neden var:
# TR: - çünkü ortak support katmanı psycopg DB oturumunu açan tek açık yere ihtiyaç duyar
# TR: dsn parametresi:
# TR: - dsn canlı bağlantıyı açmak için kullanılan PostgreSQL bağlantı metnidir
# TR: Kabul edilen çıktı:
# TR: - canlı psycopg bağlantı nesnesi
def connect_db(dsn: str) -> psycopg.Connection:
    """
    EN:
    Open a PostgreSQL connection using the given DSN string.

    In very simple terms:
    - The crawler cannot talk to PostgreSQL with only Python code.
    - It first needs a connection.
    - The DSN is the connection recipe.
    - This function uses that recipe and opens the door.

    Input contract:
    - dsn must be a non-empty PostgreSQL connection string.
    - Typical shape: "postgresql://user:pass@host:port/dbname"
    - This function does not repair an empty DSN for you.

    Return contract:
    - Returns a live psycopg.Connection object.
    - The connection uses dict_row, so SQL rows come back like dictionaries.
    - On success it never returns None.

    TR:
    Verilen DSN metniyle bir PostgreSQL bağlantısı açar.

    Çok basit anlatımla:
    - Crawler yalnızca Python kodu ile PostgreSQL ile konuşamaz.
    - Önce bir bağlantı gerekir.
    - DSN bağlantı tarifidir.
    - Bu fonksiyon o tarifle kapıyı açar.

    Girdi sözleşmesi:
    - dsn boş olmayan PostgreSQL bağlantı metni olmalıdır.
    - Tipik şekil: "postgresql://user:pass@host:port/dbname"
    - Bu fonksiyon boş DSN'yi senin yerine tamir etmez.

    Dönüş sözleşmesi:
    - Canlı bir psycopg.Connection nesnesi döndürür.
    - Bağlantı dict_row kullanır; böylece SQL satırları sözlük gibi gelir.
    - Başarıda asla None döndürmez.
    """

    # EN: conn is the live connection object returned by psycopg.
    # EN: Upper layers keep ownership of when to commit, rollback, and close it.
    # TR: conn psycopg tarafından dönen canlı bağlantı nesnesidir.
    # TR: Commit, rollback ve close zamanının sahipliği üst katmanlarda kalır.
    conn = psycopg.connect(dsn, row_factory=dict_row)
    return conn



# EN: ROW-CONVERSION PURPOSE MEMORY BLOCK V4 / _row_to_claimed_url
# EN:
# EN: Why this helper exists:
# EN: - because DB rows should be converted into one explicit Python-side shape
# EN: - because upper layers should read named fields, not raw row plumbing
# EN:
# EN: Accepted input:
# EN: - one dict-like row carrying the expected claimed-url columns
# EN:
# EN: Accepted output:
# EN: - ClaimedUrl object
# EN:
# EN: Undesired input:
# EN: - missing required columns
# EN: - malformed row payload
# EN: - non-row object
# TR: SATIR-DÖNÜŞÜM AMAÇ HAFIZA BLOĞU V4 / _row_to_claimed_url
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü DB satırları tek ve açık Python tarafı şekline dönüştürülmelidir
# TR: - çünkü üst katmanlar ham row plumbing yerine isimli alanları okumalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - beklenen claimed-url sütunlarını taşıyan dict-benzeri tek satır
# TR:
# TR: Kabul edilen çıktı:
# TR: - ClaimedUrl nesnesi
# TR:
# TR: İstenmeyen girdi:
# TR: - gerekli sütunların eksik olması
# TR: - bozuk row payload'ı
# TR: - row olmayan nesne

# EN: GATEWAY SUPPORT FUNCTION CONTRACT BLOCK / _row_to_claimed_url
# EN: Why this function exists:
# EN: - because one DB-shaped row should be converted into one stable ClaimedUrl object in exactly one shared place
# EN: Parameter row:
# EN: - row is the dict-like DB payload that already contains one claimed work item
# EN: Accepted output:
# EN: - ClaimedUrl object
# TR: GATEWAY SUPPORT FONKSIYON SÖZLEŞME BLOĞU / _row_to_claimed_url
# TR: Bu fonksiyon neden var:
# TR: - çünkü DB-şekilli tek bir row tam olarak tek bir ortak yerde kararlı ClaimedUrl nesnesine dönüştürülmelidir
# TR: row parametresi:
# TR: - row tek bir claim edilmiş iş öğesini zaten taşıyan dict-benzeri DB payload'ıdır
# TR: Kabul edilen çıktı:
# TR: - ClaimedUrl nesnesi
def _row_to_claimed_url(row: dict[str, Any]) -> ClaimedUrl:
    """
    EN:
    Convert one dict-like database row into a ClaimedUrl object.

    In very simple terms:
    - SQL gives us a row.
    - That row is still generic.
    - This function rebuilds it as a named Python object.
    - After that, upper layers work with claimed_url.field_name style access.

    Input contract:
    - row must contain all required claimed-url keys.
    - Missing keys raise KeyError naturally.
    - row["url_query"] may be None.
    - row["lease_token"] is forced into str so the lease token stays text-shaped.

    Return contract:
    - Returns ClaimedUrl.
    - Never returns dict.
    - Never returns None on success.

    TR:
    Tek bir dict-benzeri veritabanı satırını ClaimedUrl nesnesine çevirir.

    Çok basit anlatımla:
    - SQL bize bir satır verir.
    - O satır hâlâ geneldir.
    - Bu fonksiyon onu isimli bir Python nesnesi olarak yeniden kurar.
    - Böylece üst katmanlar claimed_url.field_name biçiminde erişir.

    Girdi sözleşmesi:
    - row tüm zorunlu claimed-url anahtarlarını içermelidir.
    - Eksik anahtarlar doğal olarak KeyError üretir.
    - row["url_query"] None olabilir.
    - row["lease_token"] metin şekli korunsun diye açıkça str yapılır.

    Dönüş sözleşmesi:
    - ClaimedUrl döndürür.
    - dict döndürmez.
    - Başarıda None döndürmez.
    """

    # EN: claimed_url is the rebuilt, named, clean Python payload.
    # TR: claimed_url yeniden kurulmuş, isimli ve temiz Python payload'ıdır.
    claimed_url = ClaimedUrl(
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
    return claimed_url



# EN: TRANSACTION HELPER PURPOSE MEMORY BLOCK V4 / rollback
# EN:
# EN: Why this helper exists:
# EN: - because caller code should be able to say "cancel current transaction work" with one clear support-layer function
# EN:
# EN: Accepted input:
# EN: - live connection object
# EN:
# EN: Accepted output:
# EN: - side-effect only helper, normally returning None
# EN:
# EN: Undesired input:
# EN: - closed/broken connection object
# TR: TRANSACTION YARDIMCISI AMAÇ HAFIZA BLOĞU V4 / rollback
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü çağıran kod "mevcut transaction işini iptal et" demeyi tek ve açık support katmanı fonksiyonuyla yapabilmelidir
# TR:
# TR: Kabul edilen girdi:
# TR: - canlı bağlantı nesnesi
# TR:
# TR: Kabul edilen çıktı:
# TR: - normalde None dönen yan-etki yardımcı fonksiyonu
# TR:
# TR: İstenmeyen girdi:
# TR: - kapalı/bozuk bağlantı nesnesi

# EN: GATEWAY SUPPORT FUNCTION CONTRACT BLOCK / rollback
# EN: Why this function exists:
# EN: - because gateway children need one tiny shared helper that cancels unfinished DB work cleanly
# EN: Parameter conn:
# EN: - conn is the live psycopg connection whose current uncommitted work will be rolled back
# EN: Accepted output:
# EN: - None side-effect helper
# TR: GATEWAY SUPPORT FONKSIYON SÖZLEŞME BLOĞU / rollback
# TR: Bu fonksiyon neden var:
# TR: - çünkü gateway child'ları yarım kalmış DB işini temiz biçimde iptal eden tek küçük ortak yardımcıya ihtiyaç duyar
# TR: conn parametresi:
# TR: - conn mevcut commit edilmemiş işi rollback edilecek canlı psycopg bağlantısıdır
# TR: Kabul edilen çıktı:
# TR: - None dönen yan-etki yardımcı fonksiyonu
def rollback(conn: psycopg.Connection) -> None:
    """
    EN:
    Cancel the current uncommitted transaction work on this connection.

    In very simple terms:
    - Think of rollback as "undo changes in the current unfinished DB step".
    - It is common in probe-only or failure corridors.

    Branch contract:
    - Returns None.
    - Main effect is on database transaction state, not on Python return payload.

    TR:
    Bu bağlantı üzerindeki henüz commit edilmemiş transaction işini geri alır.

    Çok basit anlatımla:
    - rollback'ı "tam bitmemiş mevcut DB adımındaki değişiklikleri geri al" gibi düşün.
    - Genellikle probe-only veya failure koridorlarında görülür.

    Dal sözleşmesi:
    - None döndürür.
    - Ana etkisi Python dönüş payload'ı değil, DB transaction durumu üzerindedir.
    """
    conn.rollback()



# EN: TRANSACTION HELPER PURPOSE MEMORY BLOCK V4 / commit
# EN:
# EN: Why this helper exists:
# EN: - because caller code should be able to finalize current transaction work through one shared support helper
# EN:
# EN: Accepted input:
# EN: - live connection object
# EN:
# EN: Accepted output:
# EN: - side-effect only helper, normally returning None
# EN:
# EN: Undesired input:
# EN: - closed/broken connection object
# TR: TRANSACTION YARDIMCISI AMAÇ HAFIZA BLOĞU V4 / commit
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü çağıran kod mevcut transaction işini tek ortak support yardımcısı ile sonlandırabilmelidir
# TR:
# TR: Kabul edilen girdi:
# TR: - canlı bağlantı nesnesi
# TR:
# TR: Kabul edilen çıktı:
# TR: - normalde None dönen yan-etki yardımcı fonksiyonu
# TR:
# TR: İstenmeyen girdi:
# TR: - kapalı/bozuk bağlantı nesnesi

# EN: GATEWAY SUPPORT FUNCTION CONTRACT BLOCK / commit
# EN: Why this function exists:
# EN: - because gateway children need one tiny shared helper that makes the current DB transaction durable
# EN: Parameter conn:
# EN: - conn is the live psycopg connection whose current transaction will be committed
# EN: Accepted output:
# EN: - None side-effect helper
# TR: GATEWAY SUPPORT FONKSIYON SÖZLEŞME BLOĞU / commit
# TR: Bu fonksiyon neden var:
# TR: - çünkü gateway child'ları mevcut DB transaction'ını kalıcı yapan tek küçük ortak yardımcıya ihtiyaç duyar
# TR: conn parametresi:
# TR: - conn mevcut transaction'ı commit edilecek canlı psycopg bağlantısıdır
# TR: Kabul edilen çıktı:
# TR: - None dönen yan-etki yardımcı fonksiyonu
def commit(conn: psycopg.Connection) -> None:
    """
    EN:
    Make the current transaction durable in the database.

    In very simple terms:
    - Think of commit as "save these DB changes for real".

    Branch contract:
    - Returns None.
    - Main effect is durable state change in PostgreSQL.

    TR:
    Mevcut transaction'ı veritabanında kalıcı hale getirir.

    Çok basit anlatımla:
    - commit'i "bu DB değişikliklerini gerçekten kaydet" gibi düşün.

    Dal sözleşmesi:
    - None döndürür.
    - Ana etkisi PostgreSQL içinde kalıcı durum değişimidir.
    """
    conn.commit()



# EN: TRANSACTION HELPER PURPOSE MEMORY BLOCK V4 / close_db
# EN:
# EN: Why this helper exists:
# EN: - because connection close should be expressed through one small shared helper
# EN:
# EN: Accepted input:
# EN: - live or closable connection object
# EN:
# EN: Accepted output:
# EN: - side-effect only helper, normally returning None
# EN:
# EN: Undesired input:
# EN: - already-invalid object that is not a connection-like surface
# TR: TRANSACTION YARDIMCISI AMAÇ HAFIZA BLOĞU V4 / close_db
# TR:
# TR: Bu yardımcı neden var:
# TR: - çünkü bağlantı kapatma işi tek küçük ortak yardımcıyla ifade edilmelidir
# TR:
# TR: Kabul edilen girdi:
# TR: - canlı veya kapatılabilir bağlantı nesnesi
# TR:
# TR: Kabul edilen çıktı:
# TR: - normalde None dönen yan-etki yardımcı fonksiyonu
# TR:
# TR: İstenmeyen girdi:
# TR: - bağlantı benzeri olmayan, zaten geçersiz nesne

# EN: GATEWAY SUPPORT FUNCTION CONTRACT BLOCK / close_db
# EN: Why this function exists:
# EN: - because gateway children need one tiny shared helper that closes the DB session cleanly at the end of work
# EN: Parameter conn:
# EN: - conn is the live psycopg connection that should now be closed
# EN: Accepted output:
# EN: - None side-effect helper
# TR: GATEWAY SUPPORT FONKSIYON SÖZLEŞME BLOĞU / close_db
# TR: Bu fonksiyon neden var:
# TR: - çünkü gateway child'ları iş bitiminde DB oturumunu temiz biçimde kapatan tek küçük ortak yardımcıya ihtiyaç duyar
# TR: conn parametresi:
# TR: - conn artık kapatılması gereken canlı psycopg bağlantısıdır
# TR: Kabul edilen çıktı:
# TR: - None dönen yan-etki yardımcı fonksiyonu
def close_db(conn: psycopg.Connection) -> None:
    """
    EN:
    Close the PostgreSQL connection.

    In very simple terms:
    - The work session with the database is over.
    - So we close the door cleanly.

    Branch contract:
    - Returns None.
    - Produces no runtime payload.

    TR:
    PostgreSQL bağlantısını kapatır.

    Çok basit anlatımla:
    - Veritabanı ile çalışma oturumu bitmiştir.
    - Bu yüzden kapıyı temiz biçimde kapatırız.

    Dal sözleşmesi:
    - None döndürür.
    - Runtime payload üretmez.
    """
    conn.close()
