# EN: This module is the repo-tracked bridge between the reviewed seed surfaces
# EN: stored in seed.seed_url and the real frontier.host / frontier.url runtime
# EN: surfaces that the worker can actually claim from.
# TR: Bu modül seed.seed_url içinde tutulan gözden geçirilmiş seed yüzeyleri ile
# TR: worker’ın gerçekten claim edebildiği frontier.host / frontier.url runtime
# TR: yüzeyleri arasındaki repo-tracked köprüdür.

from __future__ import annotations

# EN: We import argparse because this module must also be runnable as a small
# EN: operational CLI surface on pi51c.
# TR: Bu modül pi51c üzerinde küçük bir operasyonel CLI yüzeyi olarak da
# TR: çalıştırılabilsin diye argparse içe aktarılıyor.
import argparse

# EN: We import ast because the env-file reader must safely unwrap quoted values
# EN: without executing shell code.
# TR: Env-dosyası okuyucusu shell kodu çalıştırmadan quoted değerleri güvenli
# TR: biçimde açabilsin diye ast içe aktarılıyor.
import ast

# EN: We import hashlib because frontier.url may expose canonical_url_sha256 and
# EN: we must be able to derive it even if the source row does not carry it.
# TR: Frontier.url canonical_url_sha256 alanını gösterebilir ve kaynak satır bu
# TR: değeri taşımıyorsa bile türetebilmemiz gerektiği için hashlib içe aktarılıyor.
import hashlib

# EN: We import ipaddress because registrable-domain fallback logic should not
# EN: accidentally treat literal IP addresses as normal DNS hostnames.
# TR: Registrable-domain fallback mantığı literal IP adreslerini yanlışlıkla
# TR: normal DNS hostname’leri gibi ele almasın diye ipaddress içe aktarılıyor.
import ipaddress

# EN: We import json because the CLI prints a structured JSON receipt that later
# EN: audit steps can store and inspect.
# TR: CLI daha sonraki audit adımlarının saklayıp inceleyebileceği yapılı bir
# TR: JSON makbuzu bassın diye json içe aktarılıyor.
import json

# EN: We import dataclass because parsed URL bundles and final bridge results
# EN: should stay explicit, named, and beginner-readable.
# TR: Ayrıştırılmış URL paketleri ve nihai bridge sonuçları açık, isimli ve
# TR: beginner-okunur kalsın diye dataclass içe aktarılıyor.
from dataclasses import asdict, dataclass

# EN: We import datetime/timezone because seed rows marked as enqueued should
# EN: carry explicit UTC evidence strings in receipts.
# TR: Enqueued olarak işaretlenen seed satırları makbuzlarda açık UTC kanıt
# TR: metinleri taşısın diye datetime/timezone içe aktarılıyor.
from datetime import datetime, timezone

# EN: We import Path because env files and local JSON receipts are explicit file
# EN: surfaces in this crawler design.
# TR: Env dosyaları ve yerel JSON makbuzları bu crawler tasarımında açık dosya
# TR: yüzeyleri olduğu için Path içe aktarılıyor.
from pathlib import Path

# EN: We import urlsplit because seed canonical URLs must be decomposed into the
# EN: exact frontier host/url fields.
# TR: Seed canonical URL’leri exact frontier host/url alanlarına ayrıştırılmak
# TR: zorunda olduğu için urlsplit içe aktarılıyor.
from urllib.parse import urlsplit

# EN: We import psycopg because this bridge writes live PostgreSQL rows into the
# EN: crawler_core frontier surfaces.
# TR: Bu bridge live PostgreSQL satırlarını crawler_core frontier yüzeylerine
# TR: yazdığı için psycopg içe aktarılıyor.
import psycopg

# EN: We import SQL helpers because frontier inserts are built dynamically from
# EN: the exact live column set instead of assuming one frozen table shape.
# TR: Frontier insert’leri tek bir donmuş tablo şekli varsaymak yerine exact canlı
# TR: sütun kümesinden dinamik kurulsun diye SQL yardımcıları içe aktarılıyor.
from psycopg import sql

# EN: We import dict_row so every query result can be addressed by column name
# EN: and remain easy to audit.
# TR: Her sorgu sonucu sütun adıyla adreslenebilsin ve denetlemesi kolay kalsın
# TR: diye dict_row içe aktarılıyor.
from psycopg.rows import dict_row


# EN: This default path matches the current live runtime env surface on pi51c.
# TR: Bu varsayılan yol, pi51c üzerindeki mevcut live runtime env yüzeyi ile eşleşir.
DEFAULT_ENV_FILE = Path("/logisticsearch/webcrawler/config/webcrawler.env")


# EN: This dataclass holds the exact frontier-ready decomposition of one
# EN: canonical URL.
# TR: Bu dataclass tek bir canonical URL’nin exact frontier-ready ayrıştırmasını tutar.
@dataclass(slots=True)
class ParsedCanonicalUrl:
    # EN: canonical_url is the original normalized target URL.
    # TR: canonical_url özgün normalize hedef URL’dir.
    canonical_url: str

    # EN: canonical_url_sha256 is the deterministic SHA256 fingerprint of the URL.
    # TR: canonical_url_sha256 URL’nin deterministik SHA256 parmak izidir.
    canonical_url_sha256: str

    # EN: scheme is the public URL scheme such as https or http.
    # TR: scheme https veya http gibi public URL şemasıdır.
    scheme: str

    # EN: host is the lowercase network hostname.
    # TR: host küçük harfli ağ hostname değeridir.
    host: str

    # EN: port is the effective numeric network port.
    # TR: port etkin sayısal ağ portudur.
    port: int

    # EN: authority_key is the stable host identity used by frontier.host lookup.
    # TR: authority_key frontier.host lookup’unda kullanılan stabil host kimliğidir.
    authority_key: str

    # EN: registrable_domain is the coarse registrable-domain approximation used
    # EN: by current frontier surfaces.
    # TR: registrable_domain mevcut frontier yüzeylerinde kullanılan kaba
    # TR: registrable-domain yaklaşımıdır.
    registrable_domain: str

    # EN: url_path is the normalized URL path, never empty.
    # TR: url_path normalize URL path’idir ve asla boş kalmaz.
    url_path: str

    # EN: url_query is the raw query string without the leading question mark.
    # TR: url_query baştaki soru işareti olmadan ham query metnidir.
    url_query: str


# EN: This dataclass stores one row-level bridge outcome.
# TR: Bu dataclass tek bir satır düzeyi bridge sonucunu tutar.
@dataclass(slots=True)
class SeedFrontierBridgeRowResult:
    # EN: source_code identifies the seed.source family row.
    # TR: source_code seed.source aile satırını tanımlar.
    source_code: str

    # EN: seed_id is the seed.seed_url primary key rendered as text.
    # TR: seed_id metne çevrilmiş seed.seed_url primary key değeridir.
    seed_id: str

    # EN: canonical_url is the bridged public URL.
    # TR: canonical_url köprülenen public URL’dir.
    canonical_url: str

    # EN: host_id is the frontier.host row id used by the url row.
    # TR: host_id url satırının kullandığı frontier.host satır kimliğidir.
    host_id: int

    # EN: url_id is the frontier.url row id that resulted from the bridge step.
    # TR: url_id bridge adımından çıkan frontier.url satır kimliğidir.
    url_id: int

    # EN: host_created says whether a new frontier.host row had to be inserted.
    # TR: host_created yeni frontier.host satırı eklemek gerekip gerekmediğini söyler.
    host_created: bool

    # EN: url_created says whether a new frontier.url row had to be inserted.
    # TR: url_created yeni frontier.url satırı eklemek gerekip gerekmediğini söyler.
    url_created: bool

    # EN: seed_marked_enqueued says whether seed.seed_url was marked as enqueued.
    # TR: seed_marked_enqueued seed.seed_url satırının enqueued olarak işaretlenip
    # TR: işaretlenmediğini söyler.
    seed_marked_enqueued: bool

    # EN: note is a small explicit operator-readable explanation.
    # TR: note küçük ve açık operatör-okunur açıklamadır.
    note: str


# EN: This dataclass stores the full bridge run result.
# TR: Bu dataclass tam bridge çalıştırmasının sonucunu tutar.
@dataclass(slots=True)
class SeedFrontierBridgeResult:
    # EN: env_file records which env file provided the live DSN.
    # TR: env_file canlı DSN’i hangi env dosyasının sağladığını kaydeder.
    env_file: str

    # EN: scanned_seed_count is the number of ready seed rows considered.
    # TR: scanned_seed_count düşünülen hazır seed satırı sayısıdır.
    scanned_seed_count: int

    # EN: frontier_host_created_count is the number of newly inserted frontier hosts.
    # TR: frontier_host_created_count yeni eklenen frontier host sayısıdır.
    frontier_host_created_count: int

    # EN: frontier_url_created_count is the number of newly inserted frontier urls.
    # TR: frontier_url_created_count yeni eklenen frontier url sayısıdır.
    frontier_url_created_count: int

    # EN: frontier_url_existing_count is the number of already-present frontier urls.
    # TR: frontier_url_existing_count zaten mevcut olan frontier url sayısıdır.
    frontier_url_existing_count: int

    # EN: seed_rows_marked_enqueued_count is the number of seed rows whose
    # EN: last_enqueued_at / last_result were updated.
    # TR: seed_rows_marked_enqueued_count last_enqueued_at / last_result alanları
    # TR: güncellenen seed satırı sayısıdır.
    seed_rows_marked_enqueued_count: int

    # EN: row_results stores the per-seed bridge outcomes.
    # TR: row_results seed-başı bridge sonuçlarını taşır.
    row_results: list[dict[str, object]]

    # EN: committed records whether this run was committed or intentionally rolled back.
    # TR: committed bu çalıştırmanın commit edilip edilmediğini veya bilinçli olarak
    # TR: geri alınıp alınmadığını kaydeder.
    committed: bool


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı ISO-8601 UTC zaman damgası metni döndürür.
def utc_now_iso() -> str:
    # EN: Explicit UTC avoids machine-local timezone ambiguity in receipts.
    # TR: Açık UTC, makineye özgü saat dilimi belirsizliğini makbuzlardan uzak tutar.
    return datetime.now(timezone.utc).isoformat()


# EN: This helper reads a small KEY=VALUE env file without executing shell code.
# TR: Bu yardımcı küçük KEY=VALUE env dosyasını shell kodu çalıştırmadan okur.
def parse_simple_env_file(path: Path) -> dict[str, str]:
    # EN: data collects the parsed key/value pairs.
    # TR: data ayrıştırılmış anahtar/değer çiftlerini toplar.
    data: dict[str, str] = {}

    # EN: We iterate over every raw line because comments and blank lines should
    # EN: be ignored explicitly.
    # TR: Yorum ve boş satırlar açık biçimde yok sayılsın diye her ham satır
    # TR: üzerinde tek tek dönüyoruz.
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        # EN: line is the trimmed line used for the lightweight parser.
        # TR: line hafif parser’ın kullandığı kırpılmış satırdır.
        line = raw_line.strip()

        # EN: Empty lines and comment lines carry no config payload.
        # TR: Boş satırlar ve yorum satırları konfigürasyon payload’ı taşımaz.
        if not line or line.startswith("#"):
            continue

        # EN: Only KEY=VALUE lines participate in this narrow parser.
        # TR: Bu dar parser’da yalnızca KEY=VALUE satırları yer alır.
        if "=" not in line:
            continue

        # EN: key/value split happens only on the first equals sign.
        # TR: key/value ayrımı yalnızca ilk eşittir işaretinde yapılır.
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # EN: Empty keys are ignored defensively.
        # TR: Boş anahtarlar savunmacı biçimde yok sayılır.
        if not key:
            continue

        # EN: Quoted values are unwrapped safely with literal_eval when possible.
        # TR: Quoted değerler mümkünse literal_eval ile güvenli biçimde açılır.
        if value and value[0] in {"'", '"'}:
            try:
                value = ast.literal_eval(value)
            except Exception:
                value = value.strip("'").strip('"')

        # EN: Parsed value is stored under the normalized key.
        # TR: Ayrıştırılan değer normalize anahtar altında saklanır.
        data[key] = value

    return data


# EN: This helper extracts the crawler DSN from the runtime env file.
# TR: Bu yardımcı crawler DSN’ini runtime env dosyasından çıkarır.
def crawler_dsn_from_env_file(env_file: Path) -> str:
    # EN: env_map stores the parsed env file contents.
    # TR: env_map ayrıştırılmış env dosyası içeriğini tutar.
    env_map = parse_simple_env_file(env_file)

    # EN: dsn is the crawler PostgreSQL DSN used by the bridge.
    # TR: dsn bridge’in kullandığı crawler PostgreSQL DSN değeridir.
    dsn = env_map.get("LOGISTICSEARCH_CRAWLER_DSN")
    if dsn is None or str(dsn).strip() == "":
        raise RuntimeError(f"LOGISTICSEARCH_CRAWLER_DSN missing in env file: {env_file}")
    return str(dsn)


# EN: This helper derives a stable authority_key from scheme/host/port.
# TR: Bu yardımcı scheme/host/port üçlüsünden stabil authority_key türetir.
def build_authority_key(scheme: str, host: str, port: int) -> str:
    # EN: default_port stores the protocol-default port if one exists.
    # TR: default_port varsa protokolün varsayılan portunu tutar.
    default_port = 443 if scheme == "https" else 80 if scheme == "http" else None

    # EN: Default ports are omitted from authority_key so host identity stays stable.
    # TR: Varsayılan portlar authority_key’den çıkarılır; böylece host kimliği stabil kalır.
    if default_port is not None and port == default_port:
        return host

    # EN: Non-default ports stay visible in the key because they define a distinct host surface.
    # TR: Varsayılan olmayan portlar görünür kalır; çünkü ayrı bir host yüzeyi tanımlarlar.
    return f"{host}:{port}"


# EN: This helper builds a pragmatic registrable-domain approximation suitable
# EN: for current crawler runtime needs.
# TR: Bu yardımcı mevcut crawler runtime ihtiyaçlarına uygun pratik bir
# TR: registrable-domain yaklaşımı üretir.
def build_registrable_domain(host: str) -> str:
    # EN: normalized_host is the stripped lowercase hostname candidate.
    # TR: normalized_host kırpılmış küçük harfli hostname adayını tutar.
    normalized_host = host.lower().strip(".")

    # EN: Empty hostnames are invalid input for this helper.
    # TR: Boş hostname değerleri bu yardımcı için geçersiz girdidir.
    if not normalized_host:
        raise ValueError("empty host")

    # EN: Literal IP addresses are returned unchanged because they are already exact.
    # TR: Literal IP adresleri zaten exact olduğu için değiştirilmeden döndürülür.
    try:
        ipaddress.ip_address(normalized_host)
        return normalized_host
    except ValueError:
        pass

    # EN: labels stores the DNS labels from left to right.
    # TR: labels DNS etiketlerini soldan sağa tutar.
    labels = [label for label in normalized_host.split(".") if label]

    # EN: Very short hostnames already are their own registrable-domain approximation.
    # TR: Çok kısa hostname’ler zaten kendi registrable-domain yaklaşımıdır.
    if len(labels) <= 2:
        return normalized_host

    # EN: This small set handles a few common second-level public suffix shapes
    # EN: without pulling an external dependency into the runtime.
    # TR: Bu küçük küme, dış bağımlılık çekmeden bazı yaygın ikinci seviye public
    # TR: suffix şekillerini ele alır.
    second_level_suffixes = {
        "co.uk", "org.uk", "gov.uk", "ac.uk",
        "com.au", "net.au", "org.au",
        "co.jp", "ne.jp", "or.jp",
        "com.sg", "com.tr", "com.br",
        "co.nz", "co.za",
    }

    # EN: tail2 and tail3 are the compact suffix windows used by the approximation.
    # TR: tail2 ve tail3 yaklaşımın kullandığı kompakt suffix pencereleridir.
    tail2 = ".".join(labels[-2:])
    tail3 = ".".join(labels[-3:])

    # EN: Known second-level suffix patterns keep one additional label.
    # TR: Bilinen ikinci seviye suffix desenleri bir ek etiketi daha korur.
    if tail2 in second_level_suffixes and len(labels) >= 3:
        return tail3

    # EN: Otherwise the last two labels are used.
    # TR: Aksi halde son iki etiket kullanılır.
    return tail2


# EN: This helper parses one canonical URL into frontier-ready fields.
# TR: Bu yardımcı tek bir canonical URL’yi frontier-ready alanlara ayrıştırır.
def parse_canonical_url_text(canonical_url: str) -> ParsedCanonicalUrl:
    # EN: parts stores the structured URL decomposition.
    # TR: parts yapılandırılmış URL ayrıştırmasını tutar.
    parts = urlsplit(canonical_url)

    # EN: scheme must be explicit and supported by the first crawler bridge.
    # TR: scheme ilk crawler bridge tarafından açık ve desteklenir olmalıdır.
    scheme = (parts.scheme or "").lower()
    if scheme not in {"http", "https"}:
        raise ValueError(f"unsupported scheme for frontier bridge: {canonical_url}")

    # EN: host is the lowercase hostname seen by frontier.host.
    # TR: host frontier.host tarafından görülen küçük harfli hostname değeridir.
    host = (parts.hostname or "").lower()
    if host == "":
        raise ValueError(f"canonical_url has no hostname: {canonical_url}")

    # EN: port is the effective network port. Default ports stay explicit here and
    # EN: authority_key decides whether they should collapse.
    # TR: port etkin ağ portudur. Varsayılan portlar burada açık kalır; bunların
    # TR: authority_key içinde daralıp daralmayacağına authority_key karar verir.
    port = parts.port if parts.port is not None else (443 if scheme == "https" else 80)

    # EN: authority_key is the stable host identity for frontier.host lookup/upsert.
    # TR: authority_key frontier.host lookup/upsert için stabil host kimliğidir.
    authority_key = build_authority_key(scheme, host, port)

    # EN: registrable_domain is the pragmatic host grouping token.
    # TR: registrable_domain pratik host gruplama belirtecidir.
    registrable_domain = build_registrable_domain(host)

    # EN: url_path never stays empty because frontier.url expects a real path.
    # TR: url_path asla boş bırakılmaz; çünkü frontier.url gerçek bir path bekler.
    url_path = parts.path or "/"

    # EN: url_query keeps the raw query string without the leading question mark.
    # TR: url_query baştaki soru işareti olmadan ham query metnini tutar.
    url_query = parts.query or ""

    # EN: canonical_url_sha256 is computed directly from the canonical URL text.
    # TR: canonical_url_sha256 doğrudan canonical URL metninden hesaplanır.
    canonical_url_sha256 = hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()

    return ParsedCanonicalUrl(
        canonical_url=canonical_url,
        canonical_url_sha256=canonical_url_sha256,
        scheme=scheme,
        host=host,
        port=port,
        authority_key=authority_key,
        registrable_domain=registrable_domain,
        url_path=url_path,
        url_query=url_query,
    )


# EN: This helper reads the exact current frontier column set for one table.
# TR: Bu yardımcı tek bir tablo için exact güncel frontier sütun kümesini okur.
def load_frontier_column_names(cur: psycopg.Cursor, table_name: str) -> set[str]:
    # EN: We ask information_schema instead of hard-coding one table shape.
    # TR: Tek bir tablo şekli hard-code edilmesin diye information_schema’ya soruyoruz.
    cur.execute(
        """
        select column_name
        from information_schema.columns
        where table_schema = 'frontier'
          and table_name = %s
        order by ordinal_position
        """,
        (table_name,),
    )
    return {str(row["column_name"]) for row in cur.fetchall()}


# EN: This helper selects ready seed rows that have not yet been marked as enqueued.
# TR: Bu yardımcı henüz enqueued olarak işaretlenmemiş hazır seed satırlarını seçer.
def select_ready_seed_rows(
    cur: psycopg.Cursor,
    *,
    limit: int | None = None,
) -> list[dict[str, object]]:
    # EN: base_query keeps the ready-seed contract explicit and narrow.
    # TR: base_query hazır-seed sözleşmesini açık ve dar tutar.
    base_query = sql.SQL(
        """
        select
            s.source_id,
            s.source_code,
            s.source_name,
            s.homepage_url,
            s.source_category,
            s.default_priority,
            s.default_max_depth,
            u.seed_id,
            u.seed_type,
            u.submitted_url,
            u.canonical_url,
            u.canonical_url_sha256,
            u.priority,
            u.max_depth,
            u.recrawl_interval::text as recrawl_interval,
            u.next_discover_at,
            u.last_enqueued_at,
            u.last_result,
            u.seed_metadata
        from seed.seed_url u
        join seed.source s on s.source_id = u.source_id
        where u.is_enabled = true
          and s.source_status = 'active'
          and u.last_enqueued_at is null
        order by u.priority desc, u.next_discover_at asc, u.canonical_url asc
        """
    )

    # EN: limit_clause is appended only when the caller requested a finite slice.
    # TR: limit_clause yalnızca çağıran sonlu bir dilim istediğinde eklenir.
    limit_clause = sql.SQL("")
    params: list[object] = []

    if limit is not None:
        limit_clause = sql.SQL(" limit %s")
        params.append(int(limit))

    # EN: Final query is executed with explicit ordering and optional limit.
    # TR: Nihai sorgu açık sıralama ve opsiyonel limit ile çalıştırılır.
    cur.execute(base_query + limit_clause, params)
    return list(cur.fetchall())


# EN: This helper looks up or creates one frontier.host row for a parsed URL.
# TR: Bu yardımcı ayrıştırılmış URL için bir frontier.host satırını bulur veya oluşturur.
def ensure_frontier_host_for_parsed_url(
    cur: psycopg.Cursor,
    frontier_host_columns: set[str],
    parsed_url: ParsedCanonicalUrl,
) -> tuple[int, bool]:
    # EN: Existing host lookup prefers authority_key because stage17c showed that
    # EN: frontier.host is currently keyed that way in live audit usage.
    # TR: Mevcut host lookup authority_key’yi tercih eder; çünkü stage17c canlı
    # TR: audit kullanımında frontier.host’un şu anda bu şekilde anahtarlandığını gösterdi.
    if "authority_key" in frontier_host_columns:
        cur.execute(
            """
            select host_id
            from frontier.host
            where authority_key = %s
            """,
            (parsed_url.authority_key,),
        )
    else:
        cur.execute(
            """
            select host_id
            from frontier.host
            where scheme = %s
              and host = %s
              and port = %s
            """,
            (parsed_url.scheme, parsed_url.host, parsed_url.port),
        )

    # EN: If a host row already exists, we reuse it.
    # TR: Host satırı zaten varsa onu yeniden kullanırız.
    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["host_id"]), False

    # EN: insert_values is built dynamically so the bridge stays aligned with the
    # EN: exact live frontier.host contract.
    # TR: insert_values dinamik kurulur; böylece bridge exact canlı frontier.host
    # TR: sözleşmesiyle hizalı kalır.
    insert_values: dict[str, object] = {}

    # EN: These three fields were confirmed by stage17c as required-without-default.
    # TR: Bu üç alan stage17c tarafından required-without-default olarak doğrulandı.
    if "scheme" in frontier_host_columns:
        insert_values["scheme"] = parsed_url.scheme
    if "host" in frontier_host_columns:
        insert_values["host"] = parsed_url.host
    if "port" in frontier_host_columns:
        insert_values["port"] = parsed_url.port

    # EN: We also provide stable host identity helpers when the live table exposes them.
    # TR: Canlı tablo bunları gösteriyorsa stabil host kimliği yardımcılarını da sağlıyoruz.
    if "authority_key" in frontier_host_columns:
        insert_values["authority_key"] = parsed_url.authority_key
    if "registrable_domain" in frontier_host_columns:
        insert_values["registrable_domain"] = parsed_url.registrable_domain

    # EN: cols and vals become the final dynamic INSERT column/value lists.
    # TR: cols ve vals nihai dinamik INSERT sütun/değer listelerine dönüşür.
    cols = list(insert_values.keys())
    vals = [insert_values[col] for col in cols]

    # EN: Dynamic INSERT is generated only from columns we intentionally supply.
    # TR: Dinamik INSERT yalnızca bilinçli olarak sağladığımız sütunlardan üretilir.
    cur.execute(
        sql.SQL("insert into frontier.host ({cols}) values ({vals}) returning host_id").format(
            cols=sql.SQL(", ").join(sql.Identifier(col) for col in cols),
            vals=sql.SQL(", ").join(sql.Placeholder() for _ in cols),
        ),
        vals,
    )

    # EN: Newly inserted host_id is returned to the caller.
    # TR: Yeni eklenen host_id çağırana döndürülür.
    inserted_row = cur.fetchone()
    return int(inserted_row["host_id"]), True


# EN: This helper looks up or creates one frontier.url row for a seed row.
# TR: Bu yardımcı bir seed satırı için frontier.url satırını bulur veya oluşturur.
def ensure_frontier_url_for_seed_row(
    cur: psycopg.Cursor,
    frontier_url_columns: set[str],
    seed_row: dict[str, object],
    parsed_url: ParsedCanonicalUrl,
    host_id: int,
) -> tuple[int, bool]:
    # EN: Existing URL lookup uses canonical_url because stage17 showed that exact
    # EN: field is present and was the live audit needle.
    # TR: Mevcut URL lookup canonical_url kullanır; çünkü stage17 exact bu alanın
    # TR: mevcut olduğunu ve canlı audit needle’ı olduğunu gösterdi.
    cur.execute(
        """
        select url_id
        from frontier.url
        where canonical_url = %s
        """,
        (parsed_url.canonical_url,),
    )

    # EN: Already-present frontier.url rows are reused instead of duplicated.
    # TR: Zaten mevcut frontier.url satırları çoğaltılmak yerine yeniden kullanılır.
    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["url_id"]), False

    # EN: insert_values is built dynamically against the exact live frontier.url columns.
    # TR: insert_values exact canlı frontier.url sütunlarına karşı dinamik biçimde kurulur.
    insert_values: dict[str, object] = {}

    # EN: These three fields were confirmed by stage17c as required-without-default.
    # TR: Bu üç alan stage17c tarafından required-without-default olarak doğrulandı.
    if "host_id" in frontier_url_columns:
        insert_values["host_id"] = host_id
    if "canonical_url" in frontier_url_columns:
        insert_values["canonical_url"] = parsed_url.canonical_url
    if "url_path" in frontier_url_columns:
        insert_values["url_path"] = parsed_url.url_path

    # EN: The remaining fields are supplied opportunistically when the live table
    # EN: exposes them, so the inserted rows stay rich without assuming too much.
    # TR: Kalan alanlar canlı tablo bunları gösterdiğinde fırsatçı biçimde sağlanır;
    # TR: böylece eklenen satırlar gereğinden fazla varsayım yapmadan zengin kalır.
    if "canonical_url_sha256" in frontier_url_columns:
        insert_values["canonical_url_sha256"] = (
            seed_row.get("canonical_url_sha256") or parsed_url.canonical_url_sha256
        )
    if "scheme" in frontier_url_columns:
        insert_values["scheme"] = parsed_url.scheme
    if "host" in frontier_url_columns:
        insert_values["host"] = parsed_url.host
    if "port" in frontier_url_columns:
        insert_values["port"] = parsed_url.port
    if "authority_key" in frontier_url_columns:
        insert_values["authority_key"] = parsed_url.authority_key
    if "registrable_domain" in frontier_url_columns:
        insert_values["registrable_domain"] = parsed_url.registrable_domain
    if "url_query" in frontier_url_columns:
        insert_values["url_query"] = parsed_url.url_query
    if "priority" in frontier_url_columns:
        insert_values["priority"] = int(seed_row["priority"])
    if "depth" in frontier_url_columns:
        # EN: Seed entrypoints start at frontier depth 0 because they are root crawl entries.
        # TR: Seed entrypoint’ler root crawl girişi olduğu için frontier depth 0’dan başlar.
        insert_values["depth"] = 0
    if "max_depth" in frontier_url_columns:
        insert_values["max_depth"] = int(seed_row["max_depth"])
    if "discovery_type" in frontier_url_columns:
        insert_values["discovery_type"] = "seed"
    if "state" in frontier_url_columns:
        insert_values["state"] = "queued"
    if "seed_id" in frontier_url_columns:
        insert_values["seed_id"] = seed_row["seed_id"]
    if "source_id" in frontier_url_columns:
        insert_values["source_id"] = seed_row["source_id"]

    # EN: cols and vals become the final dynamic INSERT column/value lists.
    # TR: cols ve vals nihai dinamik INSERT sütun/değer listelerine dönüşür.
    cols = list(insert_values.keys())
    vals = [insert_values[col] for col in cols]

    # EN: Dynamic INSERT is generated only from columns we intentionally provide.
    # TR: Dinamik INSERT yalnızca bilinçli olarak sağladığımız sütunlardan üretilir.
    cur.execute(
        sql.SQL("insert into frontier.url ({cols}) values ({vals}) returning url_id").format(
            cols=sql.SQL(", ").join(sql.Identifier(col) for col in cols),
            vals=sql.SQL(", ").join(sql.Placeholder() for _ in cols),
        ),
        vals,
    )

    # EN: Newly inserted url_id is returned to the caller.
    # TR: Yeni eklenen url_id çağırana döndürülür.
    inserted_row = cur.fetchone()
    return int(inserted_row["url_id"]), True


# EN: This helper marks one seed.seed_url row as enqueued.
# TR: Bu yardımcı tek bir seed.seed_url satırını enqueued olarak işaretler.
def mark_seed_row_enqueued(
    cur: psycopg.Cursor,
    *,
    seed_id: object,
    note: str,
) -> bool:
    # EN: We update last_enqueued_at and last_result in one small explicit statement.
    # TR: last_enqueued_at ve last_result alanlarını tek küçük ve açık ifade ile güncelliyoruz.
    cur.execute(
        """
        update seed.seed_url
        set
            last_enqueued_at = now(),
            last_result = %s,
            updated_at = now()
        where seed_id = %s
        """,
        (note, seed_id),
    )
    return cur.rowcount == 1


# EN: This is the main repo-tracked bridge function. It selects ready seed rows,
# EN: ensures frontier.host rows, ensures frontier.url rows, and then marks the
# EN: seed rows as enqueued.
# TR: Bu ana repo-tracked bridge fonksiyonudur. Hazır seed satırlarını seçer,
# TR: frontier.host satırlarını garanti eder, frontier.url satırlarını garanti eder
# TR: ve ardından seed satırlarını enqueued olarak işaretler.
def bridge_ready_seed_rows_to_frontier(
    conn: psycopg.Connection,
    *,
    limit: int | None = None,
) -> SeedFrontierBridgeResult:
    # EN: result_rows accumulates per-seed outcomes in operator-readable form.
    # TR: result_rows seed-başı sonuçları operatör-okunur biçimde biriktirir.
    result_rows: list[dict[str, object]] = []

    # EN: These counters keep the top-level receipt compact and auditable.
    # TR: Bu sayaçlar üst-seviye makbuzu kompakt ve denetlenebilir tutar.
    frontier_host_created_count = 0
    frontier_url_created_count = 0
    frontier_url_existing_count = 0
    seed_rows_marked_enqueued_count = 0

    with conn.cursor(row_factory=dict_row) as cur:
        # EN: We read the exact live frontier column sets before doing any bridge work.
        # TR: Herhangi bir bridge işi yapmadan önce exact canlı frontier sütun
        # TR: kümelerini okuyoruz.
        frontier_host_columns = load_frontier_column_names(cur, "host")
        frontier_url_columns = load_frontier_column_names(cur, "url")

        # EN: ready_seed_rows is the ordered queue of still-unenqueued seed rows.
        # TR: ready_seed_rows hâlâ unenqueued durumda olan seed satırlarının sıralı kuyruğudur.
        ready_seed_rows = select_ready_seed_rows(cur, limit=limit)

        # EN: Each seed row is bridged one by one so failures remain narrow and obvious.
        # TR: Hatalar dar ve açık kalsın diye her seed satırı tek tek bridge edilir.
        for seed_row in ready_seed_rows:
            # EN: parsed_url is the frontier-ready URL decomposition for this seed.
            # TR: parsed_url bu seed için frontier-ready URL ayrıştırmasıdır.
            parsed_url = parse_canonical_url_text(str(seed_row["canonical_url"]))

            # EN: host row is ensured first because frontier.url depends on host_id.
            # TR: frontier.url host_id’ye bağlı olduğu için önce host satırı garanti edilir.
            host_id, host_created = ensure_frontier_host_for_parsed_url(
                cur,
                frontier_host_columns,
                parsed_url,
            )

            # EN: url row is then ensured against the exact frontier.url contract.
            # TR: Ardından exact frontier.url sözleşmesine karşı url satırı garanti edilir.
            url_id, url_created = ensure_frontier_url_for_seed_row(
                cur,
                frontier_url_columns,
                seed_row,
                parsed_url,
                host_id,
            )

            # EN: We build one explicit result note before marking the seed row.
            # TR: Seed satırını işaretlemeden önce tek bir açık sonuç notu kuruyoruz.
            if url_created:
                note = "seed_bridged_to_frontier_url_created_v1"
            else:
                note = "seed_bridged_to_frontier_url_already_present_v1"

            # EN: Seed row is marked as enqueued so it will not be bridged again blindly.
            # TR: Seed satırı körlemesine tekrar bridge edilmesin diye enqueued olarak işaretlenir.
            seed_marked_enqueued = mark_seed_row_enqueued(
                cur,
                seed_id=seed_row["seed_id"],
                note=note,
            )

            # EN: We update the compact counters from the row outcome.
            # TR: Kompakt sayaçları satır sonucundan güncelliyoruz.
            if host_created:
                frontier_host_created_count += 1
            if url_created:
                frontier_url_created_count += 1
            else:
                frontier_url_existing_count += 1
            if seed_marked_enqueued:
                seed_rows_marked_enqueued_count += 1

            # EN: Row-level result is appended in text-safe form for JSON printing later.
            # TR: Satır-düzeyi sonuç daha sonra JSON basımı için metin-güvenli biçimde eklenir.
            row_result = SeedFrontierBridgeRowResult(
                source_code=str(seed_row["source_code"]),
                seed_id=str(seed_row["seed_id"]),
                canonical_url=str(seed_row["canonical_url"]),
                host_id=host_id,
                url_id=url_id,
                host_created=host_created,
                url_created=url_created,
                seed_marked_enqueued=seed_marked_enqueued,
                note=note,
            )
            result_rows.append(asdict(row_result))

    return SeedFrontierBridgeResult(
        env_file="db_connection_supplied_by_caller",
        scanned_seed_count=len(result_rows),
        frontier_host_created_count=frontier_host_created_count,
        frontier_url_created_count=frontier_url_created_count,
        frontier_url_existing_count=frontier_url_existing_count,
        seed_rows_marked_enqueued_count=seed_rows_marked_enqueued_count,
        row_results=result_rows,
        committed=False,
    )


# EN: This helper turns the dataclass result into a JSON-ready dict.
# TR: Bu yardımcı dataclass sonucunu JSON-ready dict’e dönüştürür.
def bridge_result_to_dict(result: SeedFrontierBridgeResult) -> dict[str, object]:
    return asdict(result)


# EN: This CLI entry point opens the live crawler DSN from the env file, runs the
# EN: bridge, and either commits or rolls back.
# TR: Bu CLI giriş noktası canlı crawler DSN’ini env dosyasından açar, bridge’i
# TR: çalıştırır ve ardından commit veya rollback yapar.
def main() -> int:
    # EN: Argument parser defines the narrow operator-visible surface.
    # TR: Argument parser dar operatör-görünür yüzeyi tanımlar.
    parser = argparse.ArgumentParser(
        description="Bridge ready seed.seed_url rows into frontier.host/frontier.url.",
    )
    parser.add_argument(
        "--env-file",
        default=str(DEFAULT_ENV_FILE),
        help="Path to the live webcrawler env file that contains LOGISTICSEARCH_CRAWLER_DSN.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of ready seed rows to bridge in one run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the bridge and then roll back instead of committing.",
    )
    args = parser.parse_args()

    # EN: env_file is the explicit runtime env surface chosen by the operator.
    # TR: env_file operatör tarafından seçilen açık runtime env yüzeyidir.
    env_file = Path(args.env_file)

    # EN: dsn is resolved from the env file so the CLI stays aligned with live runtime config.
    # TR: CLI canlı runtime konfigürasyonu ile hizalı kalsın diye dsn env dosyasından çözülür.
    dsn = crawler_dsn_from_env_file(env_file)

    # EN: We open one explicit psycopg connection with dict_row results for readability.
    # TR: Okunabilirlik için dict_row sonuçlarıyla tek bir açık psycopg bağlantısı açıyoruz.
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        # EN: We run the core bridge function inside the transaction owned by this connection.
        # TR: Çekirdek bridge fonksiyonunu bu bağlantının sahip olduğu transaction içinde çalıştırıyoruz.
        result = bridge_ready_seed_rows_to_frontier(
            conn,
            limit=args.limit,
        )

        # EN: Receipt dict is materialized before final transaction decision.
        # TR: Makbuz dict’i nihai transaction kararından önce somutlaştırılır.
        payload = bridge_result_to_dict(result)
        payload["env_file"] = str(env_file)
        payload["observed_at"] = utc_now_iso()

        # EN: Dry-run intentionally rolls back so operators can inspect the outcome safely.
        # TR: Dry-run, operatörler sonucu güvenli biçimde inceleyebilsin diye bilinçli
        # TR: olarak rollback yapar.
        if args.dry_run:
            conn.rollback()
            payload["committed"] = False
        else:
            conn.commit()
            payload["committed"] = True

    # EN: Final JSON receipt is printed to stdout for outer audit wrappers.
    # TR: Nihai JSON makbuzu dış audit wrapper’ları için stdout’a basılır.
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


# EN: This export list keeps the public module surface explicit.
# TR: Bu export listesi modülün public yüzeyini açık tutar.
__all__ = [
    "ParsedCanonicalUrl",
    "SeedFrontierBridgeRowResult",
    "SeedFrontierBridgeResult",
    "DEFAULT_ENV_FILE",
    "utc_now_iso",
    "parse_simple_env_file",
    "crawler_dsn_from_env_file",
    "build_authority_key",
    "build_registrable_domain",
    "parse_canonical_url_text",
    "load_frontier_column_names",
    "select_ready_seed_rows",
    "ensure_frontier_host_for_parsed_url",
    "ensure_frontier_url_for_seed_row",
    "mark_seed_row_enqueued",
    "bridge_ready_seed_rows_to_frontier",
    "bridge_result_to_dict",
    "main",
]


# EN: Standard script entry point.
# TR: Standart betik giriş noktası.
if __name__ == "__main__":
    raise SystemExit(main())
