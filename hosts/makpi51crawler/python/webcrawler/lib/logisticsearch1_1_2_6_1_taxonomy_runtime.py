# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: and forward references do not need eager runtime resolution.
# TR: Type hint'ler okunabilir kalsın ve forward reference'lar anında çözülmek
# TR: zorunda olmasın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because taxonomy match rows should travel through the
# EN: runtime as explicit, named, beginner-readable structured objects.
# TR: Taxonomy eşleşme satırları runtime içinde açık, isimli ve beginner-okunur
# TR: yapılı nesneler olarak taşınsın diye dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import Any because some PostgreSQL-returned numeric/text fields may stay
# EN: lightly flexible until the scoring surface is sealed more tightly.
# TR: Bazı PostgreSQL dönen sayısal/metinsel alanlar skor yüzeyi daha sıkı
# TR: mühürlenene kadar hafif esnek kalabileceği için Any içe aktarıyoruz.
from typing import Any

# EN: We import os because the taxonomy DSN should be overridable explicitly from
# EN: the environment rather than hidden in code only.
# TR: Taxonomy DSN değeri yalnızca kod içinde gizli kalmasın, environment'dan da
# TR: açıkça override edilebilsin diye os içe aktarıyoruz.
import os

# EN: We import psycopg because taxonomy runtime reads are performed directly from
# EN: PostgreSQL through a second controlled read-only connection.
# TR: Taxonomy runtime okumaları ikinci kontrollü read-only bağlantı üzerinden
# TR: doğrudan PostgreSQL'den yapılacağı için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row so query results arrive as dictionary-like mappings with
# EN: explicit column names instead of positional tuples.
# TR: Sorgu sonuçları pozisyonel tuple yerine açık sütun adlarıyla dict-benzeri
# TR: mapping olarak gelsin diye dict_row içe aktarıyoruz.
from psycopg.rows import dict_row

# EN: This tuple is the explicit canonical 25-language order consumed by the
# EN: crawler/taxonomy runtime contract. It must stay byte-for-byte aligned with
# EN: the SQL taxonomy authority surface.
# TR: Bu tuple crawler/taxonomy runtime sözleşmesinin kullandığı açık kanonik
# TR: 25 dil sırasıdır. SQL taxonomy otorite yüzeyi ile byte-for-byte hizalı
# TR: kalmalıdır.
CANONICAL_LANGUAGE_ORDER: tuple[str, ...] = (
    "ar", "bg", "cs", "de", "el", "en", "es", "fr", "hu", "it",
    "ja", "ko", "nl", "pt", "ro", "ru", "tr", "zh", "hi", "bn",
    "ur", "uk", "id", "vi", "he",
)


# EN: This dataclass represents one runtime taxonomy match returned by the narrow
# EN: read-only lookup seam.
# TR: Bu dataclass dar read-only lookup seam'i tarafından döndürülen tek bir
# TR: runtime taxonomy eşleşmesini temsil eder.
@dataclass(slots=True)
class TaxonomyRuntimeMatch:
    # EN: node_id is the durable numeric identity of the matched taxonomy node.
    # TR: node_id eşleşen taxonomy düğümünün kalıcı sayısal kimliğidir.
    node_id: int

    # EN: node_code is the human-inspectable stable taxonomy code.
    # TR: node_code insan tarafından incelenebilir stabil taxonomy kodudur.
    node_code: str

    # EN: domain_type stores the major domain family of the matched node.
    # TR: domain_type eşleşen düğümün büyük alan ailesini tutar.
    domain_type: str

    # EN: node_kind stores the narrower runtime kind of the matched node.
    # TR: node_kind eşleşen düğümün daha dar runtime türünü tutar.
    node_kind: str

    # EN: lang_code stores which language row actually matched.
    # TR: lang_code gerçekte hangi dil satırının eşleştiğini tutar.
    lang_code: str

    # EN: matched_surface tells whether the hit came from translations or keywords.
    # TR: matched_surface vuruşun translations mı keywords mü yüzeyinden geldiğini söyler.
    matched_surface: str

    # EN: matched_text stores the exact runtime text that matched.
    # TR: matched_text eşleşen tam runtime metnini tutar.
    matched_text: str

    # EN: match_score is the current narrow numeric score used only for ordering.
    # TR: match_score şu an yalnızca sıralama için kullanılan dar sayısal skordur.
    match_score: Any

    # EN: lang_priority stores the explicit language-priority bucket used by the query.
    # TR: lang_priority sorgu tarafından kullanılan açık dil-öncelik kovasını tutar.
    lang_priority: int


# EN: This helper returns the default taxonomy DSN. The runtime should prefer an
# EN: explicit environment value and only then fall back to the controlled local default.
# TR: Bu yardımcı varsayılan taxonomy DSN değerini döndürür. Runtime önce açık
# TR: environment değerini tercih etmeli, ancak sonra kontrollü yerel varsayılana düşmelidir.
def taxonomy_default_dsn() -> str:
    # EN: We first check the dedicated taxonomy DSN variable because a second DB
    # EN: connection should be explicit at operator level.
    # TR: Önce ayrılmış taxonomy DSN değişkenini kontrol ediyoruz; çünkü ikinci DB
    # TR: bağlantısı operatör seviyesinde açık olmalıdır.
    env_value = os.getenv("LOGISTICSEARCH_TAXONOMY_DSN")

    # EN: If the operator provided a non-empty DSN, we trust and return it.
    # TR: Operatör boş olmayan bir DSN verdiyse ona güvenip geri döndürüyoruz.
    if env_value:
        return env_value

    # EN: Otherwise we use the current controlled live-runtime default.
    # TR: Aksi durumda mevcut kontrollü canlı-runtime varsayımını kullanıyoruz.
    return "dbname=logisticsearch_taxonomy user=makpi51"


# EN: This helper opens one read-only-style taxonomy connection using psycopg.
# EN: We keep autocommit disabled and transaction control explicit for auditability.
# TR: Bu yardımcı psycopg ile tek bir read-only-tarzı taxonomy bağlantısı açar.
# TR: Denetlenebilirlik için autocommit kapalı ve transaction kontrolü açık kalır.
def connect_taxonomy_db(dsn: str) -> psycopg.Connection:
    # EN: We connect with dict_row so callers can read by column name.
    # TR: Çağıranlar sütun adına göre okuyabilsin diye dict_row ile bağlanıyoruz.
    conn = psycopg.connect(dsn, row_factory=dict_row)

    # EN: We return the open connection to the caller.
    # TR: Açık bağlantıyı çağırana döndürüyoruz.
    return conn


# EN: This helper normalizes incoming query text before it is compared against the
# EN: normalized runtime translation/keyword surfaces.
# TR: Bu yardımcı gelen sorgu metnini normalize eder; sonra bu metin normalize edilmiş
# TR: runtime translation/keyword yüzeylerine karşı karşılaştırılır.
def normalize_taxonomy_query_text(query_text: str) -> str:
    # EN: We strip outer whitespace first because surrounding spaces carry no meaning.
    # TR: Dış boşluklar anlam taşımadığı için önce onları kırpıyoruz.
    normalized_text = query_text.strip()

    # EN: We lower-case the text because current runtime normalized columns are
    # EN: designed for case-insensitive comparison.
    # TR: Mevcut runtime normalize sütunları büyük/küçük harf duyarsız karşılaştırma
    # TR: için tasarlandığı için metni küçük harfe indiriyoruz.
    normalized_text = normalized_text.lower()

    # EN: We collapse repeated whitespace so the query shape becomes more stable.
    # TR: Tekrarlayan boşlukları indiriyoruz; böylece sorgu şekli daha stabil oluyor.
    normalized_text = " ".join(normalized_text.split())

    # EN: We return the final normalized form.
    # TR: Son normalize edilmiş biçimi döndürüyoruz.
    return normalized_text


# EN: This helper fetches one compact identity/count snapshot from the runtime
# EN: taxonomy database so callers can prove they connected to the expected surface.
# TR: Bu yardımcı runtime taxonomy veritabanından tek bir kompakt kimlik/sayım
# TR: özeti çeker; böylece çağıranlar beklenen yüzeye bağlandığını kanıtlayabilir.
def fetch_taxonomy_runtime_identity_counts(conn: psycopg.Connection) -> dict[str, Any]:
    # EN: We open one cursor for the compact read-only snapshot query.
    # TR: Kompakt read-only özet sorgusu için tek bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We select the current DB identity and the main runtime counts together
        # EN: so the proof stays compact and explicit.
        # TR: Kanıt kompakt ve açık kalsın diye mevcut DB kimliğini ve ana runtime
        # TR: sayımlarını birlikte seçiyoruz.
        cur.execute(
            """
            SELECT
              current_database() AS db_name,
              current_user AS db_user,
              (SELECT count(*)::bigint FROM logistics.supported_languages)        AS supported_languages,
              (SELECT count(*)::bigint FROM logistics.taxonomy_nodes)             AS taxonomy_nodes,
              (SELECT count(*)::bigint FROM logistics.taxonomy_node_translations) AS taxonomy_node_translations,
              (SELECT count(*)::bigint FROM logistics.taxonomy_keywords)          AS taxonomy_keywords,
              (SELECT count(*)::bigint FROM logistics.taxonomy_closure)           AS taxonomy_closure
            """
        )

        # EN: We fetch exactly one row because this proof query returns one compact snapshot.
        # TR: Bu kanıt sorgusu tek bir kompakt özet döndürdüğü için tam bir satır çekiyoruz.
        row = cur.fetchone()

    # EN: We return the raw mapping directly because its shape is already explicit.
    # TR: Şekli zaten açık olduğu için ham mapping'i doğrudan döndürüyoruz.
    return row


# EN: This helper performs one deliberately narrow runtime lookup against the 25-language
# EN: taxonomy surfaces. It is not final ranking logic. It is only the first controlled seam.
# TR: Bu yardımcı 25 dilli taxonomy yüzeylerine karşı bilinçli olarak dar bir runtime
# TR: lookup yapar. Bu nihai ranking mantığı değildir. Yalnızca ilk kontrollü seam'dir.
def search_runtime_taxonomy(
    conn: psycopg.Connection,
    *,
    query_text: str,
    input_lang_code: str | None = None,
    limit: int = 20,
) -> list[TaxonomyRuntimeMatch]:
    # EN: We normalize the external query first so runtime matching stays stable.
    # TR: Runtime eşleşmesi stabil kalsın diye dış sorguyu önce normalize ediyoruz.
    normalized_query_text = normalize_taxonomy_query_text(query_text)

    # EN: Empty normalized text must not hit the DB because that would be noisy and misleading.
    # TR: Boş normalize metin DB'ye gitmemelidir; aksi gürültülü ve yanıltıcı olur.
    if normalized_query_text == "":
        return []

    # EN: We clamp the limit into a safe narrow range so callers cannot accidentally
    # EN: request a huge uncontrolled result set.
    # TR: Çağıranlar kazara devasa ve kontrolsüz sonuç kümesi istemesin diye limit
    # TR: değerini güvenli ve dar aralığa sıkıştırıyoruz.
    safe_limit = max(1, min(limit, 100))

    # EN: We build one contains-pattern once because both translation and keyword
    # EN: surfaces use the same normalized contains check.
    # TR: Hem translation hem keyword yüzeyi aynı normalize contains kontrolünü
    # TR: kullandığı için contains-pattern değerini bir kez kuruyoruz.
    contains_pattern = f"%{normalized_query_text}%"

    # EN: We open a cursor for the single narrow search query.
    # TR: Tek dar arama sorgusu için bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We query translations and keywords together, but still keep the SQL
        # EN: intentionally simple and inspectable.
        # TR: Translation ve keyword yüzeylerini birlikte sorguluyoruz; ama SQL'i
        # TR: yine de bilinçli olarak sade ve incelenebilir tutuyoruz.
        cur.execute(
            """
            WITH language_priority AS (
                SELECT %(input_lang_code)s::text AS lang_code, 0 AS lang_priority
                WHERE %(input_lang_code)s::text IS NOT NULL
                  AND btrim(%(input_lang_code)s::text) <> ''

                UNION ALL
                SELECT 'en'::text, 1
                UNION ALL
                SELECT 'tr'::text, 2
                UNION ALL
                SELECT 'de'::text, 3
            ),
            translation_hits AS (
                SELECT
                    n.id AS node_id,
                    n.node_code,
                    n.domain_type,
                    n.node_kind,
                    t.lang_code,
                    'translation'::text AS matched_surface,
                    t.title AS matched_text,
                    CASE
                        WHEN t.title_normalized = %(normalized_query_text)s THEN 100.0::numeric
                        WHEN t.title_normalized LIKE %(contains_pattern)s THEN 80.0::numeric
                        ELSE round((similarity(t.title_normalized, %(normalized_query_text)s) * 100.0)::numeric, 4)
                    END AS match_score,
                    COALESCE(lp.lang_priority, 50) AS lang_priority
                FROM logistics.taxonomy_nodes AS n
                JOIN logistics.taxonomy_node_translations AS t
                  ON t.node_id = n.id
                LEFT JOIN language_priority AS lp
                  ON lp.lang_code = t.lang_code
                WHERE n.is_active = true
                  AND (
                        t.title_normalized = %(normalized_query_text)s
                     OR t.title_normalized LIKE %(contains_pattern)s
                     OR similarity(t.title_normalized, %(normalized_query_text)s) >= 0.35
                  )
            ),
            keyword_hits AS (
                SELECT
                    n.id AS node_id,
                    n.node_code,
                    n.domain_type,
                    n.node_kind,
                    k.lang_code,
                    'keyword'::text AS matched_surface,
                    k.keyword AS matched_text,
                    CASE
                        WHEN k.keyword_normalized = %(normalized_query_text)s THEN 100.0::numeric
                        WHEN k.keyword_normalized LIKE %(contains_pattern)s THEN 80.0::numeric
                        ELSE round((similarity(k.keyword_normalized, %(normalized_query_text)s) * 100.0)::numeric, 4)
                    END AS match_score,
                    COALESCE(lp.lang_priority, 50) AS lang_priority
                FROM logistics.taxonomy_nodes AS n
                JOIN logistics.taxonomy_keywords AS k
                  ON k.node_id = n.id
                LEFT JOIN language_priority AS lp
                  ON lp.lang_code = k.lang_code
                WHERE n.is_active = true
                  AND (
                        k.keyword_normalized = %(normalized_query_text)s
                     OR k.keyword_normalized LIKE %(contains_pattern)s
                     OR similarity(k.keyword_normalized, %(normalized_query_text)s) >= 0.35
                  )
            ),
            combined_hits AS (
                SELECT * FROM translation_hits
                UNION ALL
                SELECT * FROM keyword_hits
            ),
            ranked_hits AS (
                SELECT
                    node_id,
                    node_code,
                    domain_type,
                    node_kind,
                    lang_code,
                    matched_surface,
                    matched_text,
                    match_score,
                    lang_priority,
                    row_number() OVER (
                        PARTITION BY node_id, lang_code, matched_surface, matched_text
                        ORDER BY match_score DESC, lang_priority ASC, node_id ASC
                    ) AS dedupe_rank
                FROM combined_hits
            )
            SELECT
                node_id,
                node_code,
                domain_type,
                node_kind,
                lang_code,
                matched_surface,
                matched_text,
                match_score,
                lang_priority
            FROM ranked_hits
            WHERE dedupe_rank = 1
            ORDER BY
                match_score DESC,
                lang_priority ASC,
                node_id ASC,
                matched_surface ASC,
                lang_code ASC
            LIMIT %(safe_limit)s
            """,
            {
                "input_lang_code": input_lang_code,
                "normalized_query_text": normalized_query_text,
                "contains_pattern": contains_pattern,
                "safe_limit": safe_limit,
            },
        )

        # EN: We fetch all rows because the limit is already clamped and explicit.
        # TR: Limit zaten sıkıştırılmış ve açık olduğu için tüm satırları çekiyoruz.
        rows = cur.fetchall()

    # EN: We convert every row into the shaped dataclass so later runtime layers do
    # EN: not depend on loose dict shapes.
    # TR: Sonraki runtime katmanları gevşek dict şekillerine bağlı kalmasın diye her
    # TR: satırı şekilli dataclass nesnesine dönüştürüyoruz.
    return [
        TaxonomyRuntimeMatch(
            node_id=row["node_id"],
            node_code=row["node_code"],
            domain_type=row["domain_type"],
            node_kind=row["node_kind"],
            lang_code=row["lang_code"],
            matched_surface=row["matched_surface"],
            matched_text=row["matched_text"],
            match_score=row["match_score"],
            lang_priority=row["lang_priority"],
        )
        for row in rows
    ]
