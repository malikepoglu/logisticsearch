# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because small structured runtime result objects are
# EN: easier to inspect and reason about than loose tuples or unnamed dictionaries.
# TR: Küçük yapılı runtime sonuç nesneleri dağınık tuple veya isimsiz sözlüklere
# TR: göre incelemesi ve anlaması daha kolay olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone so fetch timestamps are explicit and UTC-based.
# TR: Fetch zaman damgaları açık ve UTC tabanlı olsun diye datetime ve timezone
# TR: içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import hashlib because raw response bytes should get a deterministic
# EN: SHA256 fingerprint before later pipeline layers trust that storage artefact.
# TR: Ham response byte'ları sonraki pipeline katmanları bu storage artefact'ına
# TR: güvenmeden önce deterministik bir SHA256 parmak izi almalıdır; bu yüzden
# TR: hashlib içe aktarıyoruz.
import hashlib

# EN: We import Path because filesystem path construction is clearer and safer
# EN: with pathlib objects than with raw string concatenation.
# TR: Filesystem path üretimi pathlib nesneleriyle ham metin birleştirmeye göre
# TR: daha açık ve daha güvenli olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import Request and urlopen from the standard library so the first real
# EN: fetch layer stays dependency-light and does not yet pull broader crawler packages.
# TR: İlk gerçek fetch katmanı dependency açısından hafif kalsın ve henüz daha
# TR: geniş crawler paketlerini çekmesin diye Request ve urlopen'u standart kütüphaneden içe aktarıyoruz.
import socket

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# EN: This constant defines the minimal controlled raw-fetch root under /srv.
# EN: Raw and working crawler accumulation must stay under /srv according to the
# EN: current simplified storage truth requested by the user.
# TR: Bu sabit /srv altındaki asgari kontrollü raw-fetch kökünü tanımlar.
# TR: Kullanıcının istediği güncel sade depolama doğrusuna göre ham ve çalışma
# TR: crawler birikimi /srv altında kalmalıdır.
RAW_FETCH_ROOT = Path("/srv/crawler/logisticsearch/raw_fetch")


# EN: This dataclass stores the minimal result of one real page fetch plus raw-body storage write.
# TR: Bu dataclass tek bir gerçek page fetch işleminin ve ham body storage yazımının
# TR: asgari sonucunu tutar.
@dataclass(slots=True)
class FetchedPageResult:
    # EN: url_id is the claimed frontier url id that produced this fetch result.
    # TR: url_id bu fetch sonucunu üreten claim edilmiş frontier url kimliğidir.
    url_id: int

    # EN: requested_url is the original canonical URL that the worker tried to fetch.
    # TR: requested_url worker'ın fetch etmeye çalıştığı özgün canonical URL'dir.
    requested_url: str

    # EN: final_url is the final URL reported by the HTTP client after redirects.
    # TR: final_url redirect'lerden sonra HTTP istemcisinin bildirdiği son URL'dir.
    final_url: str

    # EN: http_status is the numeric HTTP response status code.
    # TR: http_status sayısal HTTP yanıt durum kodudur.
    http_status: int

    # EN: content_type is the visible Content-Type response header when present.
    # TR: content_type varsa görünür Content-Type yanıt başlığıdır.
    content_type: str | None

    # EN: etag is the visible ETag response header when present.
    # TR: etag varsa görünür ETag yanıt başlığıdır.
    etag: str | None

    # EN: last_modified is the visible Last-Modified response header when present.
    # TR: last_modified varsa görünür Last-Modified yanıt başlığıdır.
    last_modified: str | None

    # EN: body_bytes is the exact number of raw response bytes that were written.
    # TR: body_bytes yazılmış ham yanıt byte'larının tam sayısıdır.
    body_bytes: int

    # EN: raw_storage_path is the full on-disk path of the raw body artefact.
    # TR: raw_storage_path ham body artefact'ının disk üzerindeki tam yoludur.
    raw_storage_path: str

    # EN: raw_sha256 is the SHA256 fingerprint of the raw body bytes.
    # TR: raw_sha256 ham body byte'larının SHA256 parmak izidir.
    raw_sha256: str

    # EN: fetched_at records when the fetch result was produced.
    # TR: fetched_at fetch sonucunun ne zaman üretildiğini kaydeder.
    fetched_at: str


# EN: This helper returns the current UTC time as a real datetime object.
# TR: Bu yardımcı mevcut UTC zamanını gerçek bir datetime nesnesi olarak döndürür.
def utc_now() -> datetime:
    # EN: We explicitly use timezone.utc so no local-machine timezone ambiguity leaks in.
    # TR: Yerel makine saat dilimi belirsizliği sızmasın diye açıkça timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc)


# EN: This helper formats a UTC timestamp as an ISO-8601 string.
# TR: Bu yardımcı UTC zaman damgasını ISO-8601 metni olarak biçimlendirir.
def utc_now_iso() -> str:
    # EN: We delegate to utc_now() so all current-time generation stays consistent.
    # TR: Tüm mevcut-zaman üretimi tutarlı kalsın diye utc_now() yardımcısını kullanıyoruz.
    return utc_now().isoformat()


# EN: This helper turns a datetime into a compact filesystem-safe UTC timestamp.
# TR: Bu yardımcı bir datetime değerini filesystem için güvenli, kompakt bir UTC
# TR: zaman damgasına dönüştürür.
def utc_path_stamp(moment: datetime) -> str:
    # EN: We use a compact YYYYMMDDTHHMMSSZ shape because it is easy to sort lexically.
    # TR: Leksik olarak kolay sıralandığı için kompakt YYYYMMDDTHHMMSSZ biçimini kullanıyoruz.
    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# EN: This helper reads one field from a claimed_url object in a tolerant way.
# EN: The current worker surfaces may hand us either an attribute-style object or a dict-like object.
# TR: Bu yardımcı claimed_url nesnesinden bir alanı toleranslı biçimde okur.
# TR: Güncel worker yüzeyleri bize attribute-stili bir nesne veya dict-benzeri bir nesne verebilir.
def get_claimed_url_value(claimed_url: object, field_name: str) -> object:
    # EN: If claimed_url is a dict, we read the key directly.
    # TR: claimed_url bir dict ise anahtarı doğrudan okuyoruz.
    if isinstance(claimed_url, dict):
        if field_name not in claimed_url:
            raise KeyError(f"claimed_url is missing key: {field_name}")
        return claimed_url[field_name]

    # EN: Otherwise we try attribute access because current DB helper surfaces may
    # EN: return row-like objects with named attributes.
    # TR: Aksi durumda attribute erişimini deniyoruz; çünkü güncel DB yardımcı
    # TR: yüzeyleri isimli alanları olan row-benzeri nesneler döndürebilir.
    if not hasattr(claimed_url, field_name):
        raise AttributeError(f"claimed_url is missing attribute: {field_name}")

    # EN: We return the discovered attribute value.
    # TR: Bulunan attribute değerini döndürüyoruz.
    return getattr(claimed_url, field_name)


# EN: This helper creates the raw fetch storage path for one fetched page body.
# TR: Bu yardımcı tek bir fetch edilmiş page body için raw fetch storage yolunu oluşturur.
def build_raw_fetch_storage_path(
    *,
    url_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: We create one deterministic filename that includes the frontier url id
    # EN: and the UTC fetch timestamp.
    # TR: Frontier url id'sini ve UTC fetch zaman damgasını içeren deterministik
    # TR: tek bir dosya adı oluşturuyoruz.
    filename = f"url_{url_id}_{utc_path_stamp(fetched_at)}.body.bin"

    # EN: We return the final full path object.
    # TR: Nihai tam path nesnesini döndürüyoruz.
    return day_root / filename


# EN: This helper ensures the parent directory of a target file exists.
# TR: Bu yardımcı hedef dosyanın parent dizininin var olduğundan emin olur.
def ensure_parent_directory(path: Path) -> None:
    # EN: parents=True lets deeper missing directories be created in one step.
    # TR: parents=True daha derindeki eksik dizinlerin tek adımda oluşturulmasını sağlar.
    path.parent.mkdir(parents=True, exist_ok=True)


# EN: This helper computes the SHA256 hex digest of raw bytes.
# TR: Bu yardımcı ham byte'ların SHA256 hex özetini hesaplar.
def sha256_hex(data: bytes) -> str:
    # EN: We use hashlib.sha256 because later pipeline layers need a stable body fingerprint.
    # TR: Sonraki pipeline katmanları kararlı bir body parmak izine ihtiyaç duyduğu için hashlib.sha256 kullanıyoruz.
    return hashlib.sha256(data).hexdigest()


# EN: This function performs one real HTTP fetch and writes the raw response body
# EN: under the controlled /srv raw-fetch subtree.
# TR: Bu fonksiyon tek bir gerçek HTTP fetch işlemi yapar ve ham yanıt body'sini
# TR: kontrollü /srv raw-fetch alt ağacına yazar.
def fetch_page_to_raw_storage(
    claimed_url: object,
    *,
    timeout_seconds: int = 30,
    raw_root: Path = RAW_FETCH_ROOT,
) -> FetchedPageResult:
    # EN: We read the claimed frontier url id because the raw artefact filename
    # EN: should stay directly traceable to the frontier work item.
    # TR: Ham artefact dosya adı frontier iş öğesine doğrudan izlenebilir kalsın
    # TR: diye claim edilmiş frontier url kimliğini okuyoruz.
    url_id = int(get_claimed_url_value(claimed_url, "url_id"))

    # EN: We read the requested canonical URL because it is the actual fetch target.
    # TR: Gerçek fetch hedefi olduğu için istenen canonical URL'yi okuyoruz.
    requested_url = str(get_claimed_url_value(claimed_url, "canonical_url"))

    # EN: We read the user-agent token because crawler politeness and identity
    # EN: should be visible in the outgoing HTTP request.
    # TR: Crawler politeness ve kimliği giden HTTP isteğinde görünür olmalı diye
    # TR: user-agent token'ını okuyoruz.
    user_agent_token = str(get_claimed_url_value(claimed_url, "user_agent_token"))

    # EN: We capture the current UTC fetch time before network I/O so storage path
    # EN: and result metadata stay tied to one explicit moment.
    # TR: Storage yolu ve sonuç metadata'sı tek bir açık ana bağlı kalsın diye
    # TR: ağ I/O'sundan önce mevcut UTC fetch zamanını yakalıyoruz.
    fetched_at = utc_now()

    # EN: We build a minimal HTTP request using only the current explicit crawler identity.
    # TR: Yalnızca mevcut açık crawler kimliğini kullanarak asgari bir HTTP isteği kuruyoruz.
    request = Request(
        requested_url,
        headers={
            "User-Agent": user_agent_token,
            "Accept": "*/*",
        },
    )

    # EN: We execute the real HTTP request with the caller-supplied timeout.
    # TR: Gerçek HTTP isteğini çağıran tarafından verilen timeout ile çalıştırıyoruz.
    with urlopen(request, timeout=timeout_seconds) as response:
        # EN: final_url captures the post-redirect visible final destination.
        # TR: final_url redirect sonrası görünen son hedefi yakalar.
        final_url = str(response.geturl())

        # EN: http_status captures the numeric response code.
        # TR: http_status sayısal yanıt kodunu yakalar.
        http_status = int(response.getcode())

        # EN: content_type captures the visible Content-Type header when present.
        # TR: content_type varsa görünür Content-Type başlığını yakalar.
        content_type = response.headers.get("Content-Type")

        # EN: etag captures the visible ETag header when present.
        # TR: etag varsa görünür ETag başlığını yakalar.
        etag = response.headers.get("ETag")

        # EN: last_modified captures the visible Last-Modified header when present.
        # TR: last_modified varsa görünür Last-Modified başlığını yakalar.
        last_modified = response.headers.get("Last-Modified")

        # EN: body stores the full raw response bytes exactly as returned by the server.
        # TR: body sunucunun döndürdüğü tam ham yanıt byte'larını olduğu gibi tutar.
        body = response.read()

    # EN: We compute the deterministic storage path only after fetch metadata is known.
    # TR: Deterministik storage yolunu ancak fetch metadata'sı bilindikten sonra hesaplıyoruz.
    raw_storage_path = build_raw_fetch_storage_path(
        url_id=url_id,
        fetched_at=fetched_at,
        raw_root=raw_root,
    )

    # EN: We ensure the target parent directory exists before writing bytes.
    # TR: Byte yazmadan önce hedef parent dizinin var olduğundan emin oluyoruz.
    ensure_parent_directory(raw_storage_path)

    # EN: We write the raw bytes in binary mode because HTTP bodies are not guaranteed
    # EN: to be valid text.
    # TR: HTTP body'lerinin geçerli metin olması garanti olmadığı için ham byte'ları
    # TR: binary modda yazıyoruz.
    raw_storage_path.write_bytes(body)

    # EN: We compute the body fingerprint after the body bytes are finalized.
    # TR: Body byte'ları kesinleştikten sonra body parmak izini hesaplıyoruz.
    raw_sha256 = sha256_hex(body)

    # EN: We return one explicit structured fetch result.
    # TR: Tek bir açık yapılı fetch sonucu döndürüyoruz.
    return FetchedPageResult(
        url_id=url_id,
        requested_url=requested_url,
        final_url=final_url,
        http_status=http_status,
        content_type=content_type,
        etag=etag,
        last_modified=last_modified,
        body_bytes=len(body),
        raw_storage_path=str(raw_storage_path),
        raw_sha256=raw_sha256,
        fetched_at=fetched_at.isoformat(),
    )


# EN: This dataclass stores the result of one robots.txt fetch plus optional
# EN: raw-body persistence under the controlled raw-fetch tree.
# TR: Bu dataclass tek bir robots.txt fetch sonucunu ve varsa kontrollü raw-fetch
# TR: ağacı altındaki ham body saklama sonucunu tutar.
@dataclass(slots=True)
class FetchedRobotsTxtResult:
    # EN: host_id is the frontier.host identity whose robots URL we fetched.
    # TR: host_id robots URL'sini fetch ettiğimiz frontier.host kimliğidir.
    host_id: int

    # EN: robots_url is the explicit robots.txt URL we attempted to fetch.
    # TR: robots_url fetch etmeyi denediğimiz açık robots.txt URL'sidir.
    robots_url: str

    # EN: final_url is the final visible URL after redirects, when available.
    # TR: final_url varsa redirect sonrası görünen son URL'dir.
    final_url: str

    # EN: http_status is the visible HTTP status code when an HTTP response existed.
    # TR: http_status bir HTTP yanıtı mevcutsa görünen HTTP durum kodudur.
    http_status: int | None

    # EN: content_type is the visible Content-Type header when present.
    # TR: content_type varsa görünen Content-Type başlığıdır.
    content_type: str | None

    # EN: etag is the visible ETag header when present.
    # TR: etag varsa görünen ETag başlığıdır.
    etag: str | None

    # EN: last_modified is the visible Last-Modified header when present.
    # TR: last_modified varsa görünen Last-Modified başlığıdır.
    last_modified: str | None

    # EN: body_bytes is the exact raw byte count that was persisted or observed.
    # TR: body_bytes saklanan veya gözlenen ham byte sayısının tam değeridir.
    body_bytes: int

    # EN: raw_storage_path is the persisted raw body path when a body was captured.
    # TR: raw_storage_path bir body yakalandıysa saklanan ham body yoludur.
    raw_storage_path: str | None

    # EN: raw_sha256 is the SHA256 fingerprint of the persisted raw body when present.
    # TR: raw_sha256 varsa saklanan ham body'nin SHA256 parmak izidir.
    raw_sha256: str | None

    # EN: fetched_at records the UTC timestamp of this robots fetch attempt.
    # TR: fetched_at bu robots fetch denemesinin UTC zaman damgasını kaydeder.
    fetched_at: str

    # EN: fetch_error_class stores a transport-class error name when no HTTP response existed.
    # TR: fetch_error_class HTTP yanıtı yoksa taşıma-sınıfı hata adını tutar.
    fetch_error_class: str | None

    # EN: fetch_error_message stores the visible transport error message when present.
    # TR: fetch_error_message varsa görünen taşıma hata mesajını tutar.
    fetch_error_message: str | None


# EN: This helper builds the deterministic raw-storage path for one robots.txt body.
# TR: Bu yardımcı tek bir robots.txt body için deterministik ham-saklama yolunu kurar.
def build_raw_robots_storage_path(
    *,
    host_id: int,
    fetched_at: datetime,
    raw_root: Path = RAW_FETCH_ROOT,
) -> Path:
    # EN: We split the raw root by UTC year/month/day so later inspection stays manageable.
    # TR: Daha sonra inceleme yönetilebilir kalsın diye raw kökü UTC year/month/day'e bölüyoruz.
    day_root = raw_root / fetched_at.strftime("%Y") / fetched_at.strftime("%m") / fetched_at.strftime("%d")

    # EN: The filename carries host identity plus UTC timestamp so later audits can
    # EN: connect the artefact back to the exact host-level robots refresh.
    # TR: Dosya adı host kimliğini ve UTC zaman damgasını taşır; böylece sonraki
    # TR: audit'ler artefact'ı tam host-seviyesi robots refresh işlemine bağlayabilir.
    filename = f"host_{host_id}_robots_{utc_path_stamp(fetched_at)}.body.bin"

    # EN: We return the final full path object.
    # TR: Nihai tam path nesnesini döndürüyoruz.
    return day_root / filename


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
