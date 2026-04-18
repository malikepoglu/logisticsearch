# EN: This module is the robots.txt acquisition child surface.
# EN: It owns only robots-body decoding, narrow robots parsing, and robots fetch
# EN: persistence under the controlled raw acquisition tree.
# TR: Bu modül robots.txt acquisition alt yüzeyidir.
# TR: Yalnızca robots body decode, dar robots parse ve kontrollü raw acquisition
# TR: ağacı altında robots fetch persistence işine sahip olmalıdır.

from __future__ import annotations

# EN: We import Path because the child surface exposes a configurable raw_root
# EN: path in its explicit function signature.
# TR: Bu alt yüzey açık fonksiyon imzasında yapılandırılabilir raw_root yolu
# TR: sunduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import socket plus HTTPError and URLError because robots fetch must
# EN: preserve the explicit distinction between HTTP failures and lower-level
# EN: transport failures.
# TR: Robots fetch HTTP hataları ile daha alt düzey taşıma hataları arasındaki
# TR: açık ayrımı korumalıdır; bu yüzden socket ile birlikte HTTPError ve URLError
# TR: içe aktarıyoruz.
import socket
from urllib.error import HTTPError, URLError

# EN: We import Request and urlopen from the standard library so this robots child
# EN: stays dependency-light and explicit.
# TR: Bu robots alt yüzeyi dependency açısından hafif ve açık kalsın diye Request
# TR: ve urlopen'u standart kütüphaneden içe aktarıyoruz.
from urllib.request import Request, urlopen

# EN: We import the shared acquisition support surface so this child reuses the
# EN: same stable artefact/result contract as the rest of the acquisition family.
# TR: Bu alt yüzey acquisition ailesinin geri kalanıyla aynı kararlı artefact/sonuç
# TR: sözleşmesini yeniden kullansın diye paylaşılan acquisition destek yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedRobotsTxtResult,
    build_raw_robots_storage_path,
    ensure_parent_directory,
    sha256_hex,
    utc_now,
)


# EN: This helper decodes robots bytes as UTF-8 with replacement so the first
# EN: controlled parser layer stays durable under imperfect encodings.
# TR: Bu yardımcı robots byte'larını replacement ile UTF-8 çözer; böylece ilk
# TR: kontrollü parser katmanı kusurlu encoding'lerde de dayanıklı kalır.
def decode_robots_body(body: bytes) -> str:
    # EN: We choose UTF-8 with replacement because explicit robustness matters
    # EN: more than byte-perfect rejection in this first narrow helper.
    # TR: Bu ilk dar yardımcıda açık dayanıklılık byte-mükemmel reddinden daha
    # TR: önemli olduğu için replacement ile UTF-8 seçiyoruz.
    return body.decode("utf-8", errors="replace")

# EN: This helper extracts the current narrow robots model from visible robots text.
# EN: The current SQL allow-decision surface only needs disallow rules, sitemap URLs,
# EN: and crawl-delay, so we keep parsing intentionally narrow and explicit.
# TR: Bu yardımcı görünen robots metninden güncel dar robots modelini çıkarır.
# TR: Mevcut SQL allow-decision yüzeyi yalnızca disallow kuralları, sitemap URL'leri
# TR: ve crawl-delay gerektirdiği için parse işlemini bilinçli olarak dar ve açık tutuyoruz.
def parse_robots_txt_text(robots_text: str) -> tuple[dict, list[str], float | None]:
    # EN: These containers accumulate the current minimal proven robots payload shape.
    # TR: Bu taşıyıcılar mevcut minimal kanıtlanmış robots payload şeklini biriktirir.
    disallow_rules: list[str] = []
    sitemap_urls: list[str] = []
    crawl_delay_seconds: float | None = None

    # EN: This flag tells us whether the current rule group applies to User-agent: *.
    # TR: Bu bayrak mevcut kural grubunun User-agent: * için geçerli olup olmadığını söyler.
    wildcard_group_active = False

    # EN: This flag helps us detect when a new user-agent line starts a new group
    # EN: after at least one rule line was already seen.
    # TR: Bu bayrak en az bir kural satırı görüldükten sonra yeni bir user-agent
    # TR: satırının yeni grup başlattığını anlamamıza yardım eder.
    current_group_has_rules = False

    # EN: We iterate line by line because robots.txt is a line-oriented format.
    # TR: Robots.txt satır-odaklı bir format olduğu için satır satır ilerliyoruz.
    for raw_line in robots_text.splitlines():
        # EN: We remove trailing comments first because inline # comments are not
        # EN: part of the rule value we want to persist.
        # TR: Sondaki yorumları önce kaldırıyoruz; çünkü satır içi # yorumları
        # TR: saklamak istediğimiz kural değerinin parçası değildir.
        line = raw_line.split("#", 1)[0].strip()

        # EN: Empty or colon-free lines do not participate in this minimal parser.
        # TR: Boş veya iki nokta içermeyen satırlar bu minimal parser'a katılmaz.
        if not line or ":" not in line:
            continue

        # EN: We split only once so directive values may still contain colons.
        # TR: Directive değerleri iki nokta içerebilsin diye yalnızca bir kez bölüyoruz.
        field_name, raw_value = line.split(":", 1)
        field_name = field_name.strip().lower()
        value = raw_value.strip()

        # EN: Sitemap is treated as global visible metadata in this first helper.
        # TR: Sitemap bu ilk yardımcıda global görünür metadata olarak ele alınır.
        if field_name == "sitemap":
            if value:
                sitemap_urls.append(value)
            continue

        # EN: User-agent controls which subsequent rule group we are inside.
        # TR: User-agent sonraki kural grubunda olup olmadığımızı kontrol eder.
        if field_name == "user-agent":
            if current_group_has_rules:
                wildcard_group_active = False
                current_group_has_rules = False

            # EN: Only the wildcard group is consumed by the current SQL decision model.
            # TR: Mevcut SQL karar modeli yalnızca wildcard grubu tüketir.
            if value.lower() == "*":
                wildcard_group_active = True
            continue

        # EN: We only persist the narrow rule families already used by the current contract.
        # TR: Yalnızca mevcut sözleşmenin zaten kullandığı dar kural ailelerini saklıyoruz.
        if field_name not in {"disallow", "crawl-delay"}:
            continue

        current_group_has_rules = True

        # EN: Non-wildcard groups are ignored in this first controlled parser layer.
        # TR: Wildcard olmayan gruplar bu ilk kontrollü parser katmanında yok sayılır.
        if not wildcard_group_active:
            continue

        # EN: We keep only non-empty disallow prefixes because the current allow
        # EN: decision surface uses prefix matching.
        # TR: Yalnızca boş olmayan disallow prefix'lerini tutuyoruz; çünkü mevcut
        # TR: allow karar yüzeyi prefix matching kullanır.
        if field_name == "disallow":
            if value:
                disallow_rules.append(value)
            continue

        # EN: Crawl-delay is optional and numeric, so invalid values are ignored explicitly.
        # TR: Crawl-delay isteğe bağlı ve sayısaldır; bu yüzden geçersiz değerler açıkça yok sayılır.
        if field_name == "crawl-delay" and value:
            try:
                crawl_delay_seconds = float(value)
            except ValueError:
                pass

    # EN: The current SQL contract expects parsed_rules to be a JSON object with
    # EN: a disallow array, so we return exactly that shape.
    # TR: Mevcut SQL sözleşmesi parsed_rules için disallow dizisi taşıyan bir JSON
    # TR: nesnesi beklediği için tam olarak bu şekli döndürüyoruz.
    return ({"disallow": disallow_rules}, sitemap_urls, crawl_delay_seconds)

# EN: This function performs one real robots.txt fetch and stores any visible body
# EN: under the same controlled raw-fetch root as normal page fetches.
# TR: Bu fonksiyon tek bir gerçek robots.txt fetch işlemi yapar ve görünen herhangi
# TR: bir body'yi normal sayfa fetch'leriyle aynı kontrollü raw-fetch kökü altında saklar.
def fetch_robots_txt_to_raw_storage(
    *,
    host_id: int,
    robots_url: str,
    user_agent_token: str,
    timeout_seconds: int = 30,
    raw_root: Path = RAW_FETCH_ROOT,
) -> FetchedRobotsTxtResult:
    # EN: We capture the current UTC fetch time before network I/O so any persisted
    # EN: artefact and returned metadata point to one explicit moment.
    # TR: Saklanan artefact ve dönen metadata tek bir açık ana işaret etsin diye
    # TR: ağ I/O'sundan önce mevcut UTC fetch zamanını yakalıyoruz.
    fetched_at = utc_now()

    # EN: We build a minimal robots request using the current explicit crawler identity.
    # TR: Mevcut açık crawler kimliğini kullanarak asgari bir robots isteği kuruyoruz.
    request = Request(
        robots_url,
        headers={
            "User-Agent": user_agent_token,
            "Accept": "text/plain,*/*",
        },
    )

    # EN: We prepare variables up front so every exit path can return one explicit
    # EN: structured result shape.
    # TR: Her çıkış yolunun tek bir açık yapılı sonuç şekli döndürebilmesi için
    # TR: değişkenleri baştan hazırlıyoruz.
    final_url = robots_url
    http_status: int | None = None
    content_type: str | None = None
    etag: str | None = None
    last_modified: str | None = None
    body = b""
    fetch_error_class: str | None = None
    fetch_error_message: str | None = None

    try:
        # EN: We attempt the real HTTP request with the caller-supplied timeout.
        # TR: Gerçek HTTP isteğini çağıranın verdiği timeout ile deniyoruz.
        with urlopen(request, timeout=timeout_seconds) as response:
            final_url = str(response.geturl())
            http_status = int(response.getcode())
            content_type = response.headers.get("Content-Type")
            etag = response.headers.get("ETag")
            last_modified = response.headers.get("Last-Modified")
            body = response.read()

    except HTTPError as exc:
        # EN: HTTPError still represents a real HTTP response, so we preserve its
        # EN: visible headers, status, and any returned body for cache truth.
        # TR: HTTPError yine de gerçek bir HTTP yanıtını temsil eder; bu yüzden
        # TR: cache doğrusu için görünen başlıkları, durumu ve varsa dönen body'yi koruyoruz.
        final_url = robots_url
        http_status = int(exc.code)
        content_type = exc.headers.get("Content-Type")
        etag = exc.headers.get("ETag")
        last_modified = exc.headers.get("Last-Modified")
        body = exc.read()

    except (URLError, TimeoutError, socket.timeout) as exc:
        # EN: Transport-class failures produce no reliable HTTP cache truth, so we
        # EN: return a structured non-body result and let the caller decide cache_state.
        # TR: Taşıma-sınıfı hatalar güvenilir HTTP cache doğrusu üretmez; bu yüzden
        # TR: yapılı ama body'siz bir sonuç döndürüyor ve cache_state kararını çağırana bırakıyoruz.
        fetch_error_class = type(exc).__name__
        fetch_error_message = str(exc)

        return FetchedRobotsTxtResult(
            host_id=host_id,
            robots_url=robots_url,
            final_url=final_url,
            http_status=None,
            content_type=None,
            etag=None,
            last_modified=None,
            body_bytes=0,
            raw_storage_path=None,
            raw_sha256=None,
            fetched_at=fetched_at.isoformat(),
            fetch_error_class=fetch_error_class,
            fetch_error_message=fetch_error_message,
        )

    # EN: We persist any visible robots body, including HTTP error bodies, because
    # EN: later audits and cache reasoning benefit from that raw artefact.
    # TR: Sonraki audit ve cache muhakemesi bundan fayda göreceği için görünen
    # TR: herhangi bir robots body'yi, HTTP hata body'leri dahil, saklıyoruz.
    raw_storage_path = build_raw_robots_storage_path(
        host_id=host_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )
    ensure_parent_directory(raw_storage_path)
    raw_storage_path.write_bytes(body)
    raw_sha256 = sha256_hex(body)

    # EN: We return one explicit structured robots fetch result.
    # TR: Tek bir açık yapılı robots fetch sonucu döndürüyoruz.
    return FetchedRobotsTxtResult(
        host_id=host_id,
        robots_url=robots_url,
        final_url=final_url,
        http_status=http_status,
        content_type=content_type,
        etag=etag,
        last_modified=last_modified,
        body_bytes=len(body),
        raw_storage_path=str(raw_storage_path),
        raw_sha256=raw_sha256,
        fetched_at=fetched_at.isoformat(),
        fetch_error_class=fetch_error_class,
        fetch_error_message=fetch_error_message,
    )

# EN: This export list keeps the robots child surface explicit.
# TR: Bu export listesi robots alt yüzeyini açık tutar.
__all__ = [
    "decode_robots_body",
    "parse_robots_txt_text",
    "fetch_robots_txt_to_raw_storage",
]
