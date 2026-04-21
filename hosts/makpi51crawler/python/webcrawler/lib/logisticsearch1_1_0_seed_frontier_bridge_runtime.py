"""\
EN:
This file is the repo-tracked bridge between reviewed seed rows and the live
frontier surfaces that workers can actually claim from.

Topological role:
- Input truth begins in seed.seed_url.
- Output truth is materialized into frontier.host and frontier.url.
- This file does not perform crawling; it prepares crawlable frontier rows.
- The bridge is intentionally DB-contract-aware and column-aware so it can adapt
  to the exact live frontier schema exposed by the database.

Important runtime values in this file:
- DEFAULT_ENV_FILE: explicit env file path used by the CLI corridor.
- ParsedCanonicalUrl: normalized URL payload used by frontier upsert helpers.
- ready_seed_rows: list[dict] of seed rows still eligible for bridging.
- result_rows: per-row operator-readable receipts.
- host_id/url_id: integer identifiers of the live frontier rows.
- committed: bool set only by the outer CLI transaction branch.

TR:
Bu dosya gözden geçirilmiş seed satırları ile worker'ların gerçekten claim
edebildiği canlı frontier yüzeyleri arasındaki repo-tracked köprüdür.

Topolojik rol:
- Girdi doğrusu seed.seed_url içinde başlar.
- Çıktı doğrusu frontier.host ve frontier.url içine somutlaştırılır.
- Bu dosya crawl yapmaz; crawl edilebilir frontier satırlarını hazırlar.
- Köprü bilinçli olarak DB-sözleşmesi ve sütun sözleşmesi farkında yazılmıştır;
  böylece veritabanının açığa çıkardığı exact canlı frontier şemasına uyum sağlar.

Bu dosyadaki önemli runtime değerleri:
- DEFAULT_ENV_FILE: CLI koridorunda kullanılan açık env dosya yolu.
- ParsedCanonicalUrl: frontier upsert yardımcılarının kullandığı normalize URL payload'ı.
- ready_seed_rows: hâlâ köprülenmeye uygun seed satırlarından oluşan list[dict].
- result_rows: satır başına operatör-okunur makbuzlar.
- host_id/url_id: canlı frontier satırlarının tamsayı kimlikleri.
- committed: yalnızca dış CLI transaction dalında ayarlanan bool.
"""

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

# EN: We try to import psycopg because live DB work needs it, but inspection-only
# EN: contexts should not crash at module import time if psycopg is absent.
# TR: Canlı DB işleri psycopg ister; fakat yalnızca denetim yapılan bağlamlar
# TR: psycopg yok diye modül import anında çökmemelidir.
try:
    # EN: Live runtime path: psycopg is present and DB helpers stay fully active.
    # TR: Canlı runtime yolu: psycopg mevcuttur ve DB yardımcıları tam aktif kalır.
    import psycopg

    # EN: SQL helper import stays available on the normal runtime path.
    # TR: SQL yardımcı import’u normal runtime yolunda kullanılabilir kalır.
    from psycopg import sql

    # EN: dict_row keeps row access explicit by column name.
    # TR: dict_row satır erişimini sütun adıyla açık tutar.
    from psycopg.rows import dict_row

    # EN: None means the runtime dependency is available.
    # TR: None değeri runtime bağımlılığının mevcut olduğunu gösterir.
    PSYCOPG_IMPORT_ERROR: ModuleNotFoundError | None = None

except ModuleNotFoundError as exc:
    # EN: Inspection-only path: we keep the module importable and delay the hard
    # EN: failure until actual DB work is requested.
    # TR: Yalnızca denetim yolu: modülü import edilebilir tutuyoruz ve sert hatayı
    # TR: gerçek DB işi istenene kadar erteliyoruz.
    psycopg = None
    sql = None
    dict_row = None
    PSYCOPG_IMPORT_ERROR = exc


# EN: This helper turns a missing psycopg dependency into one clean runtime error
# EN: instead of a module-import crash.
# TR: Bu yardımcı eksik psycopg bağımlılığını modül-import çökmesi yerine temiz
# TR: tek bir runtime hatasına dönüştürür.
def require_psycopg_runtime() -> None:
    # EN: When psycopg is absent we raise one explicit operator-readable error.
    # TR: psycopg yoksa tek ve açık operatör-okunur hata yükseltiyoruz.
    if PSYCOPG_IMPORT_ERROR is not None:
        raise RuntimeError(
            "psycopg runtime dependency missing; use the webcrawler venv/python "
            "for DB-backed execution paths"
        ) from PSYCOPG_IMPORT_ERROR


# EN: This default path matches the current live runtime env surface on pi51c.
# TR: Bu varsayılan yol, pi51c üzerindeki mevcut live runtime env yüzeyi ile eşleşir.
# EN: DEFAULT_ENV_FILE is the canonical live-runtime env file path used by the
# EN: CLI when the operator does not override --env-file. It is always a Path
# EN: object at import time, not a string.
# TR: DEFAULT_ENV_FILE operatör --env-file ile override etmediğinde CLI'nin
# TR: kullandığı kanonik canlı-runtime env dosya yoludur. Import anında her zaman
# TR: string değil Path nesnesidir.
DEFAULT_ENV_FILE = Path("/logisticsearch/webcrawler/config/webcrawler.env")


# EN: This dataclass holds the exact frontier-ready decomposition of one
# EN: canonical URL.
# TR: Bu dataclass tek bir canonical URL’nin exact frontier-ready ayrıştırmasını tutar.
@dataclass(slots=True)
class ParsedCanonicalUrl:
    """\
    EN:
    Normalized frontier-ready decomposition of a single canonical URL.

    Field contract summary:
    - canonical_url: original normalized URL text.
    - canonical_url_sha256: deterministic hash text of canonical_url.
    - scheme: currently expected to be "http" or "https".
    - host: lowercase hostname text, never empty.
    - port: effective integer port.
    - authority_key: stable host identity used by frontier.host logic.
    - registrable_domain: coarse registrable-domain approximation.
    - url_path: normalized path text; never empty because "/" is used as fallback.
    - url_query: raw query text without leading "?"; may be empty string.

    TR:
    Tek bir canonical URL'nin normalize edilmiş frontier-ready ayrıştırmasıdır.

    Alan sözleşmesi özeti:
    - canonical_url: özgün normalize URL metni.
    - canonical_url_sha256: canonical_url'nin deterministik hash metni.
    - scheme: şu an için beklenen değerler "http" veya "https".
    - host: küçük harfli hostname metni; asla boş değildir.
    - port: etkin tamsayı port.
    - authority_key: frontier.host mantığında kullanılan stabil host kimliği.
    - registrable_domain: kaba registrable-domain yaklaşımı.
    - url_path: normalize path metni; fallback olarak "/" kullanıldığı için boş kalmaz.
    - url_query: baştaki "?" olmadan ham query metni; boş metin olabilir.
    """
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
    """\
    EN:
    Row-level bridge receipt for one seed row.

    Branch-sensitive fields:
    - host_id/url_id are positive integers on success-style branches.
    - host_id/url_id fall back to 0 on exception/error receipt branches.
    - note is a short text token explaining whether the URL was created,
      already present, or failed with an explicit error note.

    TR:
    Tek bir seed satırı için satır düzeyi bridge makbuzudur.

    Dala duyarlı alanlar:
    - host_id/url_id başarı tarzı dallarda pozitif tamsayılardır.
    - host_id/url_id istisna/hata makbuzu dallarında 0'a düşer.
    - note alanı URL'nin oluşturulduğunu, zaten mevcut olduğunu veya açık bir
      hata notuyla başarısız olduğunu anlatan kısa metin tokenıdır.
    """
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
    """\
    EN:
    Full run receipt returned by the bridge corridor.

    Important branches:
    - committed is not decided by the core bridge function; it is finalized by
      the outer CLI branch after commit/rollback selection.
    - row_results is always a list payload, even when it is empty.

    TR:
    Bridge koridoru tarafından dönen tam çalıştırma makbuzudur.

    Önemli dallar:
    - committed değeri çekirdek bridge fonksiyonu tarafından belirlenmez; commit/
      rollback seçiminin ardından dış CLI dalı tarafından sonlandırılır.
    - row_results boş olsa bile her zaman list payload olarak kalır.
    """
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
    """\
    EN:
    Parse a narrow KEY=VALUE env file into a plain dict[str, str].

    Return branches:
    - dict[str, str] containing parsed keys.
    - Empty dict when the file exists but contributes no usable KEY=VALUE rows.
    - Raises FileNotFoundError or decoding/runtime errors when the file cannot be
      read normally.

    TR:
    Dar bir KEY=VALUE env dosyasını düz dict[str, str] yapısına parse eder.

    Dönüş dalları:
    - Parse edilen anahtarları taşıyan dict[str, str].
    - Dosya mevcut olsa bile kullanılabilir KEY=VALUE satırı üretmiyorsa boş dict.
    - Dosya normal biçimde okunamazsa FileNotFoundError veya çözümleme/runtime
      hataları yükseltir.
    """
    # EN: data collects the parsed key/value pairs.
    # TR: data ayrıştırılmış anahtar/değer çiftlerini toplar.
    # EN: data is the accumulating plain string dictionary produced by this narrow
    # EN: env parser. Every accepted key and value is normalized to stripped text.
    # TR: data bu dar env parser'ının ürettiği biriken düz metin sözlüğüdür.
    # TR: Kabul edilen her anahtar ve değer kırpılmış metne normalize edilir.
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
    """\
    EN:
    Resolve LOGISTICSEARCH_CRAWLER_DSN from an explicit env file.

    Return contract:
    - Returns non-empty DSN text.
    - Raises RuntimeError when the expected key is absent or empty.
    - Never returns None.

    TR:
    LOGISTICSEARCH_CRAWLER_DSN değerini açık bir env dosyasından çözer.

    Dönüş sözleşmesi:
    - Boş olmayan DSN metni döndürür.
    - Beklenen anahtar yoksa veya boşsa RuntimeError yükseltir.
    - Asla None döndürmez.
    """
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
# EN: This helper derives a stable authority_key from scheme/host/port.
# TR: Bu yardımcı scheme/host/port üçlüsünden stabil authority_key türetir.
def build_authority_key(scheme: str, host: str, port: int) -> str:
    # EN: The live pi51c frontier.host audit showed that the generated authority_key
    # EN: unique surface currently behaves as host:port, including default ports.
    # TR: Canlı pi51c frontier.host denetimi generated authority_key benzersiz
    # TR: yüzeyinin şu anda varsayılan portlar dahil host:port gibi davrandığını gösterdi.
    _ = scheme

    # EN: We therefore keep the operator-facing authority_key derivation aligned
    # EN: with the current live database contract instead of collapsing default ports.
    # TR: Bu yüzden operatör-görünür authority_key türetimini varsayılan portları
    # TR: daraltmak yerine mevcut canlı veritabanı sözleşmesiyle hizalı tutuyoruz.
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
    """\
    EN:
    Parse one canonical URL string into the exact payload required by the bridge.

    Input contract:
    - canonical_url must be a public URL string.
    - Supported schemes in the current bridge corridor are http and https only.

    Return branches:
    - ParsedCanonicalUrl on success.
    - Raises ValueError when scheme/host requirements are not met.

    TR:
    Tek bir canonical URL metnini köprünün ihtiyaç duyduğu exact payload'a çevirir.

    Girdi sözleşmesi:
    - canonical_url public URL metni olmalıdır.
    - Mevcut bridge koridorunda desteklenen şemalar yalnızca http ve https'tir.

    Dönüş dalları:
    - Başarıda ParsedCanonicalUrl.
    - Scheme/host gereksinimleri sağlanmazsa ValueError yükseltir.
    """
    # EN: parts stores the structured URL decomposition.
    # TR: parts yapılandırılmış URL ayrıştırmasını tutar.
    # EN: parts is the standard-library URL decomposition object. It is not yet the
    # EN: final bridge payload; it is only the raw parsed source used to derive it.
    # TR: parts standart kütüphane URL ayrıştırma nesnesidir. Henüz nihai bridge
    # TR: payload'ı değildir; onu türetmek için kullanılan ham ayrıştırma kaynağıdır.
    parts = urlsplit(canonical_url)

    # EN: scheme must be explicit and supported by the first crawler bridge.
    # TR: scheme ilk crawler bridge tarafından açık ve desteklenir olmalıdır.
    # EN: scheme is normalized lowercase text. Allowed values in this corridor are
    # EN: only "http" and "https"; any other value raises ValueError.
    # TR: scheme normalize edilmiş küçük harfli metindir. Bu koridorda izin verilen
    # TR: değerler yalnızca "http" ve "https"tir; diğer değerler ValueError üretir.
    scheme = (parts.scheme or "").lower()
    if scheme not in {"http", "https"}:
        raise ValueError(f"unsupported scheme for frontier bridge: {canonical_url}")

    # EN: host is the lowercase hostname seen by frontier.host.
    # TR: host frontier.host tarafından görülen küçük harfli hostname değeridir.
    # EN: host is the lowercase hostname text used by frontier.host/frontier.url.
    # EN: Empty host is invalid and becomes a ValueError branch.
    # TR: host frontier.host/frontier.url tarafından kullanılan küçük harfli
    # TR: hostname metnidir. Boş host geçersizdir ve ValueError dalına gider.
    host = (parts.hostname or "").lower()
    if host == "":
        raise ValueError(f"canonical_url has no hostname: {canonical_url}")

    # EN: port is the effective network port. Default ports stay explicit here and
    # EN: authority_key decides whether they should collapse.
    # TR: port etkin ağ portudur. Varsayılan portlar burada açık kalır; bunların
    # TR: authority_key içinde daralıp daralmayacağına authority_key karar verir.
    # EN: port is always normalized to an integer effective port. It never remains
    # EN: None after this line.
    # TR: port her zaman etkin tamsayı porta normalize edilir. Bu satırdan sonra
    # TR: None olarak kalmaz.
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
    # EN: We first look up by the exact insert-driving natural key: scheme + host + port.
    # EN: This avoids depending on generated-column semantics during the primary lookup.
    # TR: Önce tam insert-sürücü doğal anahtar olan scheme + host + port ile lookup
    # TR: yapıyoruz. Böylece birincil lookup aşamasında generated kolon semantiğine
    # TR: bağımlı kalmıyoruz.
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
    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["host_id"]), False

    # EN: As a secondary compatibility lookup, we also try authority_key if the
    # EN: live table exposes that column.
    # TR: İkincil uyumluluk lookup’ı olarak canlı tablo authority_key kolonunu
    # TR: gösteriyorsa authority_key ile de deniyoruz.
    if "authority_key" in frontier_host_columns:
        cur.execute(
            """
            select host_id
            from frontier.host
            where authority_key = %s
            """,
            (parsed_url.authority_key,),
        )
        existing_row = cur.fetchone()
        if existing_row is not None:
            return int(existing_row["host_id"]), False

    # EN: insert_values only contains truly insertable fields. Generated authority_key
    # EN: must never be written explicitly.
    # TR: insert_values yalnızca gerçekten insert edilebilir alanları içerir.
    # TR: Generated authority_key asla açıkça yazılmamalıdır.
    insert_values: dict[str, object] = {}

    if "scheme" in frontier_host_columns:
        insert_values["scheme"] = parsed_url.scheme
    if "host" in frontier_host_columns:
        insert_values["host"] = parsed_url.host
    if "port" in frontier_host_columns:
        insert_values["port"] = parsed_url.port
    if "registrable_domain" in frontier_host_columns:
        insert_values["registrable_domain"] = parsed_url.registrable_domain

    cols = list(insert_values.keys())
    vals = [insert_values[col] for col in cols]

    # EN: We insert conflict-safely against the live unique authority_key surface.
    # EN: If another row already exists, RETURNING may yield no row and we fall back
    # EN: to a deterministic re-select.
    # TR: Canlı benzersiz authority_key yüzeyine karşı conflict-güvenli insert
    # TR: yapıyoruz. Başka bir satır zaten varsa RETURNING satır döndürmeyebilir;
    # TR: bu durumda deterministik yeniden-select fallback kullanıyoruz.
    cur.execute(
        sql.SQL(
            "insert into frontier.host ({cols}) values ({vals}) "
            "on conflict on constraint host_authority_key_key do nothing "
            "returning host_id"
        ).format(
            cols=sql.SQL(", ").join(sql.Identifier(col) for col in cols),
            vals=sql.SQL(", ").join(sql.Placeholder() for _ in cols),
        ),
        vals,
    )

    inserted_row = cur.fetchone()
    if inserted_row is not None:
        return int(inserted_row["host_id"]), True

    # EN: Conflict or race path: re-select by exact natural key first.
    # TR: Conflict veya yarış durumu yolunda önce exact doğal anahtar ile yeniden seçiyoruz.
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
    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["host_id"]), False

    # EN: Final compatibility fallback by authority_key if exposed.
    # TR: authority_key görünüyorsa son uyumluluk fallback’i budur.
    if "authority_key" in frontier_host_columns:
        cur.execute(
            """
            select host_id
            from frontier.host
            where authority_key = %s
            """,
            (parsed_url.authority_key,),
        )
        existing_row = cur.fetchone()
        if existing_row is not None:
            return int(existing_row["host_id"]), False

    # EN: Reaching this point means the live uniqueness path behaved unexpectedly.
    # TR: Buraya gelmek canlı benzersizlik yolunun beklenmedik davrandığı anlamına gelir.
    raise RuntimeError(
        "frontier.host insert/select reconciliation failed for "
        f"{parsed_url.scheme}://{parsed_url.host}:{parsed_url.port}"
    )


# EN: This helper looks up or creates one frontier.url row for a seed row.
# TR: Bu yardımcı bir seed satırı için frontier.url satırını bulur veya oluşturur.
def ensure_frontier_url_for_seed_row(
    cur: psycopg.Cursor,
    frontier_url_columns: set[str],
    seed_row: dict[str, object],
    parsed_url: ParsedCanonicalUrl,
    host_id: int,
) -> tuple[int, bool]:
    # EN: Existing URL lookup uses canonical_url because that is the clearest
    # EN: operator-visible identity for the bridge layer.
    # TR: Mevcut URL lookup canonical_url kullanır; çünkü bridge katmanı için
    # TR: operatör-görünür en açık kimlik budur.
    cur.execute(
        """
        select url_id
        from frontier.url
        where canonical_url = %s
        """,
        (parsed_url.canonical_url,),
    )

    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["url_id"]), False

    # EN: insert_values is built dynamically against the exact live frontier.url columns.
    # TR: insert_values exact canlı frontier.url sütunlarına karşı dinamik biçimde kurulur.
    insert_values: dict[str, object] = {}

    # EN: These three fields were confirmed as required-without-default for live insertability.
    # TR: Bu üç alan canlı insert edilebilirlik için required-without-default olarak doğrulandı.
    if "host_id" in frontier_url_columns:
        insert_values["host_id"] = host_id
    if "canonical_url" in frontier_url_columns:
        insert_values["canonical_url"] = parsed_url.canonical_url
    if "url_path" in frontier_url_columns:
        insert_values["url_path"] = parsed_url.url_path

    # EN: The remaining fields are supplied opportunistically when the live table
    # EN: exposes them, so inserted rows stay rich without assuming too much.
    # TR: Kalan alanlar canlı tablo bunları gösterdiğinde fırsatçı biçimde sağlanır;
    # TR: böylece eklenen satırlar gereğinden fazla varsayım yapmadan zengin kalır.
    if "scheme" in frontier_url_columns:
        insert_values["scheme"] = parsed_url.scheme
    if "host" in frontier_url_columns:
        insert_values["host"] = parsed_url.host
    if "port" in frontier_url_columns:
        insert_values["port"] = parsed_url.port
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

    cols = list(insert_values.keys())
    vals = [insert_values[col] for col in cols]

    # EN: URL insert is also conflict-safe, because another worker/process may insert
    # EN: the same canonical URL between our pre-lookup and INSERT.
    # TR: URL insert de conflict-güvenlidir; çünkü başka bir worker/process bizim
    # TR: pre-lookup ile INSERT aramızda aynı canonical URL’yi ekleyebilir.
    cur.execute(
        sql.SQL(
            "insert into frontier.url ({cols}) values ({vals}) "
            "on conflict on constraint url_canonical_url_sha256_key do nothing "
            "returning url_id"
        ).format(
            cols=sql.SQL(", ").join(sql.Identifier(col) for col in cols),
            vals=sql.SQL(", ").join(sql.Placeholder() for _ in cols),
        ),
        vals,
    )

    inserted_row = cur.fetchone()
    if inserted_row is not None:
        return int(inserted_row["url_id"]), True

    # EN: Conflict or race path falls back to a deterministic re-select.
    # TR: Conflict veya yarış durumu yolu deterministik yeniden-select fallback’ine düşer.
    cur.execute(
        """
        select url_id
        from frontier.url
        where canonical_url = %s
        """,
        (parsed_url.canonical_url,),
    )
    existing_row = cur.fetchone()
    if existing_row is not None:
        return int(existing_row["url_id"]), False

    raise RuntimeError(
        "frontier.url insert/select reconciliation failed for "
        f"{parsed_url.canonical_url}"
    )


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
    """\
    EN:
    Materialize ready seed rows into frontier.host/frontier.url rows.

    Input contract:
    - conn: live psycopg connection already chosen by the caller.
    - limit: optional positive int-like cap or None for all currently ready rows.

    Return contract:
    - SeedFrontierBridgeResult with row_results list payload.
    - committed stays False here because transaction finalization belongs to the
      outer caller/CLI corridor.

    Important variable branches:
    - ready_seed_rows: list[dict[str, object]], possibly empty.
    - parsed_url: ParsedCanonicalUrl on success branch per row.
    - host_id/url_id: int ids on successful row reconciliation.
    - note: success token or explicit error token.

    TR:
    Hazır seed satırlarını frontier.host/frontier.url satırlarına somutlaştırır.

    Girdi sözleşmesi:
    - conn: çağıran tarafından seçilmiş canlı psycopg bağlantısı.
    - limit: opsiyonel pozitif int-benzeri sınır veya tüm hazır satırlar için None.

    Dönüş sözleşmesi:
    - row_results list payload'ı taşıyan SeedFrontierBridgeResult.
    - committed burada False kalır; transaction sonlandırması dış çağıran/CLI
      koridorunun işidir.

    Önemli değişken dalları:
    - ready_seed_rows: list[dict[str, object]], boş olabilir.
    - parsed_url: satır başına başarı dalında ParsedCanonicalUrl.
    - host_id/url_id: başarılı satır uzlaştırmasında int kimlikler.
    - note: başarı tokenı veya açık hata tokenı.
    """
    # EN: result_rows accumulates per-seed outcomes in operator-readable form.
    # TR: result_rows seed-başı sonuçları operatör-okunur biçimde biriktirir.
    result_rows: list[dict[str, object]] = []

    # EN: These counters keep the top-level receipt compact and auditable.
    # TR: Bu sayaçlar üst-seviye makbuzu kompakt ve denetlenebilir tutar.
    frontier_host_created_count = 0
    frontier_url_created_count = 0
    frontier_url_existing_count = 0
    seed_rows_marked_enqueued_count = 0

    # EN: DB-backed bridge execution requires a real psycopg runtime.
    # TR: DB-destekli bridge çalışması gerçek bir psycopg runtime ister.
    require_psycopg_runtime()

    with conn.cursor(row_factory=dict_row) as cur:
        # EN: We read the exact live frontier column sets before doing any bridge work.
        # TR: Herhangi bir bridge işi yapmadan önce exact canlı frontier sütun
        # TR: kümelerini okuyoruz.
        # EN: frontier_host_columns is the exact live set[str] of insertable/visible
        # EN: frontier.host columns. This keeps the bridge contract aligned to the
        # EN: actual database instead of assumptions.
        # TR: frontier_host_columns canlı frontier.host sütunlarının exact set[str]
        # TR: kümesidir. Böylece köprü varsayımlara değil gerçek veritabanına hizalanır.
        frontier_host_columns = load_frontier_column_names(cur, "host")
        # EN: frontier_url_columns is the exact live set[str] of frontier.url column
        # EN: names used to build a safe dynamic insert payload.
        # TR: frontier_url_columns güvenli dinamik insert payload'ı kurmak için
        # TR: kullanılan frontier.url sütun adlarının exact canlı set[str] kümesidir.
        frontier_url_columns = load_frontier_column_names(cur, "url")

        # EN: ready_seed_rows is the ordered queue of still-unenqueued seed rows.
        # TR: ready_seed_rows hâlâ unenqueued durumda olan seed satırlarının sıralı kuyruğudur.
        # EN: ready_seed_rows is a list of dict rows representing seed entries that
        # EN: are still eligible for bridging. It may be empty; an empty list is a
        # EN: normal no-work branch, not an error.
        # TR: ready_seed_rows köprülenmeye hâlâ uygun seed girdilerini temsil eden
        # TR: dict satırlarından oluşan listedir. Boş olabilir; boş liste hata değil,
        # TR: normal bir no-work dalıdır.
        ready_seed_rows = select_ready_seed_rows(cur, limit=limit)

        # EN: Each seed row gets its own SAVEPOINT. This means one bad seed row does
        # EN: not abort the entire bridge run.
        # TR: Her seed satırı kendi SAVEPOINT’ini alır. Böylece tek bir problemli
        # TR: seed satırı tüm bridge çalışmasını iptal etmez.
        for seed_row in ready_seed_rows:
            cur.execute("savepoint seed_bridge_row_sp")
            try:
                # EN: parsed_url is the frontier-ready URL decomposition for this seed.
                # TR: parsed_url bu seed için frontier-ready URL ayrıştırmasıdır.
                # EN: parsed_url is the required ParsedCanonicalUrl payload derived from
                # EN: the seed row's canonical_url text. If parsing fails, control jumps
                # EN: to the row-local error branch below.
                # TR: parsed_url seed satırının canonical_url metninden türetilen zorunlu
                # TR: ParsedCanonicalUrl payload'ıdır. Parse başarısız olursa akış aşağıdaki
                # TR: satır-yerel hata dalına gider.
                parsed_url = parse_canonical_url_text(str(seed_row["canonical_url"]))

                # EN: host row is ensured first because frontier.url depends on host_id.
                # TR: frontier.url host_id’ye bağlı olduğu için önce host satırı garanti edilir.
                # EN: host_id is the integer frontier.host identifier used by the URL row.
                # EN: host_created is a bool that tells whether this bridge run inserted a
                # EN: new host row or reused an existing one.
                # TR: host_id URL satırının kullandığı frontier.host tamsayı kimliğidir.
                # TR: host_created bu bridge çalışmasının yeni host satırı ekleyip eklemediğini
                # TR: veya mevcut satırı yeniden kullanıp kullanmadığını söyleyen bool değerdir.
                host_id, host_created = ensure_frontier_host_for_parsed_url(
                    cur,
                    frontier_host_columns,
                    parsed_url,
                )

                # EN: url row is then ensured against the exact frontier.url contract.
                # TR: Ardından exact frontier.url sözleşmesine karşı url satırı garanti edilir.
                # EN: url_id is the integer frontier.url identifier produced by the bridge.
                # EN: url_created is True only when a new URL row had to be inserted.
                # TR: url_id köprü tarafından üretilen frontier.url tamsayı kimliğidir.
                # TR: url_created yalnızca yeni bir URL satırı eklemek gerektiğinde True olur.
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
                    # EN: note is a short operator-readable success token. In this branch
                    # EN: it explicitly records that a new frontier.url row was created.
                    # TR: note kısa operatör-okunur başarı tokenıdır. Bu dalda yeni bir
                    # TR: frontier.url satırının oluşturulduğunu açıkça kaydeder.
                    note = "seed_bridged_to_frontier_url_created_v1"
                else:
                    # EN: This branch records that the canonical URL was already present
                    # EN: in frontier.url and therefore no new URL row was inserted.
                    # TR: Bu dal canonical URL'nin frontier.url içinde zaten mevcut
                    # TR: olduğunu ve bu nedenle yeni URL satırı eklenmediğini kaydeder.
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

                # EN: Success path releases the row-local savepoint cleanly.
                # TR: Başarı yolu satır-yerel savepoint’i temiz biçimde serbest bırakır.
                cur.execute("release savepoint seed_bridge_row_sp")

            except Exception as exc:
                # EN: Failure path rolls back only the current row’s work, not the full run.
                # TR: Hata yolu yalnızca mevcut satırın işini geri alır; tüm çalışmayı değil.
                cur.execute("rollback to savepoint seed_bridge_row_sp")
                cur.execute("release savepoint seed_bridge_row_sp")

                error_note = (
                    "seed_bridge_error_v1:"
                    f"{exc.__class__.__name__}:"
                    f"{str(exc)}"
                )

                row_result = SeedFrontierBridgeRowResult(
                    source_code=str(seed_row.get("source_code", "")),
                    seed_id=str(seed_row.get("seed_id", "")),
                    canonical_url=str(seed_row.get("canonical_url", "")),
                    host_id=0,
                    url_id=0,
                    host_created=False,
                    url_created=False,
                    seed_marked_enqueued=False,
                    note=error_note,
                )
                result_rows.append(asdict(row_result))
                continue

    return SeedFrontierBridgeResult(
        env_file="db_connection_supplied_by_caller",
        scanned_seed_count=len(ready_seed_rows),
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
    """\
    EN:
    CLI entry for the seed->frontier bridge corridor.

    Broad steps:
    1) resolve env file,
    2) resolve DSN,
    3) run bridge,
    4) commit or roll back,
    5) print structured JSON receipt.

    Return contract:
    - 0 when execution reaches a structured JSON receipt successfully.
    - 1 when an exception is caught and converted into an error JSON payload.

    TR:
    Seed->frontier bridge koridorunun CLI girişidir.

    Geniş adımlar:
    1) env file çöz,
    2) DSN çöz,
    3) bridge çalıştır,
    4) commit veya rollback yap,
    5) yapılı JSON makbuz bas.

    Dönüş sözleşmesi:
    - Yapılı JSON makbuzuna başarıyla ulaşıldığında 0.
    - İstisna yakalanıp hata JSON payload'ına çevrildiğinde 1.
    """
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
    # EN: env_file is the explicit Path chosen for DSN resolution. It is always a
    # EN: Path object here even if the CLI argument originally arrived as text.
    # TR: env_file DSN çözümü için seçilen açık Path değeridir. CLI argümanı önce
    # TR: metin olarak gelmiş olsa bile burada her zaman Path nesnesidir.
    env_file = Path(args.env_file)

    try:
        # EN: We require psycopg before any DB-backed execution path begins, so even
        # EN: dependency failures become structured JSON receipts.
        # TR: Herhangi bir DB-destekli çalışma yolu başlamadan önce psycopg isteriz;
        # TR: böylece bağımlılık hataları bile yapılı JSON makbuzuna dönüşür.
        require_psycopg_runtime()

        # EN: dsn is resolved from the env file so the CLI stays aligned with live runtime config.
        # TR: CLI canlı runtime konfigürasyonu ile hizalı kalsın diye dsn env dosyasından çözülür.
        # EN: dsn is the non-empty PostgreSQL connection text resolved from env_file.
        # EN: It is required for all DB-backed bridge work and never intentionally None.
        # TR: dsn env_file içinden çözülen boş olmayan PostgreSQL bağlantı metnidir.
        # TR: Tüm DB-destekli bridge işleri için zorunludur ve bilinçli olarak asla None değildir.
        dsn = crawler_dsn_from_env_file(env_file)

        # EN: We open one explicit psycopg connection with dict_row results for readability.
        # TR: Okunabilirlik için dict_row sonuçlarıyla tek bir açık psycopg bağlantısı açıyoruz.
        with psycopg.connect(dsn, row_factory=dict_row) as conn:
            result = bridge_ready_seed_rows_to_frontier(
                conn,
                limit=args.limit,
            )

            # EN: payload is the JSON-ready dict receipt derived from the result dataclass.
            # EN: It becomes the single structured stdout surface for outer audits.
            # TR: payload result dataclass'ından türetilen JSON-ready dict makbuzudur.
            # TR: Dış auditler için tek yapılı stdout yüzeyine dönüşür.
            payload = bridge_result_to_dict(result)
            payload["env_file"] = str(env_file)
            payload["observed_at"] = utc_now_iso()

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

    except Exception as exc:
        # EN: Even unexpected failures are rendered as JSON receipts instead of raw traceback-only crashes.
        # TR: Beklenmedik hatalar bile ham traceback yerine JSON makbuzu olarak basılır.
        error_payload = {
            "env_file": str(env_file),
            "observed_at": utc_now_iso(),
            "committed": False,
            "scanned_seed_count": 0,
            "frontier_host_created_count": 0,
            "frontier_url_created_count": 0,
            "frontier_url_existing_count": 0,
            "seed_rows_marked_enqueued_count": 0,
            "row_results": [],
            "error_class": exc.__class__.__name__,
            "error_message": str(exc),
            "dry_run": bool(args.dry_run),
            "limit": args.limit,
        }
        print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        return 1


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
    "require_psycopg_runtime",
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
