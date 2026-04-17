# EN: This module is the direct HTTP page-acquisition child surface.
# EN: It should do only one thing: fetch one page through direct HTTP and persist
# EN: the raw body under the controlled raw acquisition tree.
# TR: Bu modül doğrudan HTTP page-acquisition alt yüzeyidir.
# TR: Yalnızca tek iş yapmalıdır: bir sayfayı doğrudan HTTP üzerinden fetch etmek
# TR: ve ham body'yi kontrollü raw acquisition ağacı altına yazmak.

from __future__ import annotations

# EN: We import Path because the child surface exposes a configurable raw_root
# EN: path in its explicit function signature.
# TR: Bu alt yüzey açık fonksiyon imzasında yapılandırılabilir raw_root yolu
# TR: sunduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import Request and urlopen from the standard library so this direct HTTP
# EN: child stays dependency-light and fully explicit.
# TR: Bu doğrudan HTTP alt yüzeyi dependency açısından hafif ve tamamen açık
# TR: kalsın diye Request ve urlopen'u standart kütüphaneden içe aktarıyoruz.
from urllib.request import Request, urlopen

# EN: We import the shared acquisition support surface so this child reuses the
# EN: same stable artefact/result contract as the rest of the acquisition family.
# TR: Bu alt yüzey acquisition ailesinin geri kalanıyla aynı kararlı artefact/sonuç
# TR: sözleşmesini yeniden kullansın diye paylaşılan acquisition destek yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_2_2_acquisition_support import (
    RAW_FETCH_ROOT,
    FetchedPageResult,
    build_raw_fetch_storage_path,
    ensure_parent_directory,
    get_claimed_url_value,
    sha256_hex,
    utc_now,
)


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

# EN: This export list keeps the direct HTTP child surface explicit.
# TR: Bu export listesi doğrudan HTTP alt yüzeyini açık tutar.
__all__ = [
    "fetch_page_to_raw_storage",
]
