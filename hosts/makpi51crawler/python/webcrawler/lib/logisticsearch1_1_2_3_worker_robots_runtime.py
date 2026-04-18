# EN: This module owns worker-side robots decision helpers that are more than
# EN: pure orchestration but narrower than the parent worker runtime.
# TR: Bu modül worker-tarafı robots karar yardımcılarını sahiplenir; bunlar saf
# TR: orchestration’dan fazladır ama parent worker runtime’dan daha dardır.

from __future__ import annotations

# EN: We import datetime because robots fetch timestamps come back as ISO text and
# EN: must be converted into explicit datetime objects for psycopg.
# TR: Robots fetch zamanları ISO metni olarak döndüğü ve psycopg için açık
# TR: datetime nesnelerine çevrilmesi gerektiği için datetime içe aktarıyoruz.
from datetime import datetime

# EN: We import Path because persisted robots artefacts must be read back from
# EN: disk during worker-side payload derivation.
# TR: Saklanan robots artefact’larının worker-tarafı payload türetimi sırasında
# TR: diskten geri okunması gerektiği için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import the stable acquisition-family public surface because this child
# EN: needs robots fetch/parse helpers plus canonical claimed-url field access.
# TR: Bu alt yüzey robots fetch/parse yardımcılarına ve kanonik claimed-url alan
# TR: erişimine ihtiyaç duyduğu için kararlı acquisition-aile public yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    FetchedRobotsTxtResult,
    decode_robots_body,
    fetch_robots_txt_to_raw_storage,
    get_claimed_url_value,
    parse_robots_txt_text,
)

# EN: We import the canonical robots cache upsert gateway because durable cache
# EN: truth must still be written through the sealed SQL surface.
# TR: Kalıcı robots cache doğrusu yine mühürlü SQL yüzeyi üzerinden yazılmalı
# TR: olduğu için kanonik robots cache upsert gateway’ini içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    upsert_robots_txt_cache,
)


# EN: This helper decides whether the current robots verdict still allows a real
# EN: page fetch in the minimal worker.
# TR: Bu yardımcı mevcut robots verdict’inin minimal worker’da gerçek page fetch’e
# TR: hâlâ izin verip vermediğini belirler.
def robots_verdict_allows_fetch(verdict: str | None) -> bool:
    # EN: These verdicts are currently treated as fetch-allowed by the minimal
    # EN: worker contract.
    # TR: Bu verdict’ler mevcut minimal worker sözleşmesi tarafından fetch-allowed
    # TR: kabul edilir.
    return verdict in {
        "allow",
        "allow_but_refresh_recommended",
        "allow_mode_ignore",
    }


# EN: This helper converts a persisted robots fetch artefact into the narrow
# EN: parsed payload shape expected by the DB cache contract.
# TR: Bu yardımcı saklanan robots fetch artefact’ını DB cache sözleşmesinin
# TR: beklediği dar parse payload şekline dönüştürür.
def parse_persisted_robots_payload(
    robots_fetch: FetchedRobotsTxtResult,
) -> tuple[dict, list[str], float | None]:
    # EN: The persisted raw path must exist on this code path because this helper
    # EN: is only used for body-present robots results.
    # TR: Bu kod yolunda saklanan ham yol mevcut olmalıdır; çünkü bu yardımcı
    # TR: yalnızca body mevcut olan robots sonuçlarında kullanılır.
    raw_storage_path = robots_fetch.raw_storage_path
    if raw_storage_path is None:
        raise RuntimeError("robots fetch returned no raw_storage_path for payload parsing")

    # EN: We read the exact persisted bytes so later audits can inspect the same
    # EN: durable artefact the parser used.
    # TR: Daha sonraki audit’ler parser’ın kullandığı aynı kalıcı artefact’ı
    # TR: inceleyebilsin diye tam saklanan byte’ları okuyoruz.
    robots_body = Path(raw_storage_path).read_bytes()

    # EN: We decode through the sealed helper so encoding tolerance stays
    # EN: consistent with the acquisition family.
    # TR: Encoding toleransı acquisition ailesiyle tutarlı kalsın diye decode
    # TR: işlemini mühürlü yardımcı üzerinden yapıyoruz.
    robots_text = decode_robots_body(robots_body)

    # EN: We return the exact narrow parsed shape expected by the current DB
    # EN: cache-upsert contract.
    # TR: Mevcut DB cache-upsert sözleşmesinin beklediği tam dar parse şeklini
    # TR: döndürüyoruz.
    return parse_robots_txt_text(robots_text)


# EN: This helper performs one controlled robots refresh cycle and writes the
# EN: resulting cache truth through the canonical DB wrapper.
# TR: Bu yardımcı tek bir kontrollü robots refresh döngüsü çalıştırır ve ortaya
# TR: çıkan cache doğrusunu kanonik DB wrapper üzerinden yazar.
def refresh_robots_cache_if_needed(
    conn,
    *,
    claimed_url: object,
    refresh_decision: dict,
) -> dict[str, object]:
    # EN: We extract the host identity because robots refresh is a host-level
    # EN: operation.
    # TR: Robots refresh host-seviyesinde bir işlem olduğu için host kimliğini
    # TR: çıkarıyoruz.
    host_id = int(get_claimed_url_value(claimed_url, "host_id"))

    # EN: We read the robots URL from the DB decision row because SQL is already
    # EN: the source of truth for that target.
    # TR: Bu hedef için doğruluk kaynağı zaten SQL olduğu için robots URL’yi DB
    # TR: karar satırından okuyoruz.
    robots_url = refresh_decision.get("robots_url")
    if robots_url is None or str(robots_url).strip() == "":
        raise RuntimeError("compute_robots_refresh_decision(...) returned empty robots_url")

    # EN: We reuse the host-level user-agent token from the claimed row so robots
    # EN: refresh uses the same explicit crawler identity.
    # TR: Robots refresh aynı açık crawler kimliğini kullansın diye claimed
    # TR: satırdaki host-seviyesi user-agent token’ını yeniden kullanıyoruz.
    user_agent_token = str(get_claimed_url_value(claimed_url, "user_agent_token"))

    # EN: We perform the real robots fetch through the canonical acquisition helper.
    # TR: Gerçek robots fetch işlemini kanonik acquisition yardımcısı üzerinden
    # TR: yapıyoruz.
    robots_fetch = fetch_robots_txt_to_raw_storage(
        host_id=host_id,
        robots_url=str(robots_url),
        user_agent_token=user_agent_token,
    )

    # EN: We convert fetched_at ISO text back into datetime so psycopg receives an
    # EN: explicit timestamptz-compatible value.
    # TR: psycopg açık timestamptz-uyumlu bir değer alsın diye fetched_at ISO
    # TR: metnini tekrar datetime nesnesine çeviriyoruz.
    fetched_at_value = datetime.fromisoformat(robots_fetch.fetched_at)

    # EN: We preserve a small visible metadata payload so later inspection can see
    # EN: where the fetch actually landed.
    # TR: Daha sonraki inceleme fetch’in gerçekte nereye indiğini görebilsin diye
    # TR: küçük bir görünür metadata payload’ı koruyoruz.
    robots_metadata = {
        "final_url": robots_fetch.final_url,
        "content_type": robots_fetch.content_type,
    }

    # EN: Transport-class failure means no reliable HTTP cache truth existed, so
    # EN: we persist an explicit error-state cache row.
    # TR: Taşıma-sınıfı hata güvenilir HTTP cache doğrusu oluşmadığı anlamına gelir;
    # TR: bu yüzden açık bir error-state cache satırı yazıyoruz.
    if robots_fetch.fetch_error_class is not None:
        return upsert_robots_txt_cache(
            conn,
            host_id=host_id,
            robots_url=str(robots_url),
            cache_state="error",
            http_status=None,
            fetched_at=fetched_at_value,
            expires_at=None,
            etag=None,
            last_modified=None,
            raw_storage_path=None,
            raw_sha256=None,
            raw_bytes=0,
            parsed_rules={},
            sitemap_urls=[],
            crawl_delay_seconds=None,
            error_class=robots_fetch.fetch_error_class,
            error_message=robots_fetch.fetch_error_message,
            robots_metadata=robots_metadata,
        )

    # EN: We start from an explicit empty parsed payload and only fill it for
    # EN: cacheable success-class outcomes.
    # TR: Açık boş bir parse payload ile başlıyor ve bunu yalnızca cache’lenebilir
    # TR: başarı-sınıfı sonuçlarda dolduruyoruz.
    parsed_rules: dict = {}
    sitemap_urls: list[str] = []
    crawl_delay_seconds = None
    cache_state = "fresh"
    error_class = None
    error_message = None

    # EN: HTTP 404 is treated as a missing robots file.
    # TR: HTTP 404 eksik robots dosyası olarak ele alınır.
    if robots_fetch.http_status == 404:
        cache_state = "missing"

    # EN: Success-class HTTP results are parsed into the narrow rules model.
    # TR: Başarı-sınıfı HTTP sonuçları dar kural modeline parse edilir.
    elif robots_fetch.http_status is not None and 200 <= robots_fetch.http_status < 400:
        parsed_rules, sitemap_urls, crawl_delay_seconds = parse_persisted_robots_payload(robots_fetch)
        cache_state = "fresh"

    # EN: All other HTTP results are persisted as explicit robots HTTP errors.
    # TR: Diğer tüm HTTP sonuçları açık robots HTTP hataları olarak yazılır.
    else:
        cache_state = "error"
        error_class = "robots_http_error"
        error_message = f"robots fetch returned HTTP status {robots_fetch.http_status}"

    # EN: We persist the observed robots cache truth through the canonical DB wrapper.
    # TR: Gözlenen robots cache doğrusunu kanonik DB wrapper üzerinden yazıyoruz.
    return upsert_robots_txt_cache(
        conn,
        host_id=host_id,
        robots_url=str(robots_url),
        cache_state=cache_state,
        http_status=robots_fetch.http_status,
        fetched_at=fetched_at_value,
        expires_at=None,
        etag=robots_fetch.etag,
        last_modified=robots_fetch.last_modified,
        raw_storage_path=robots_fetch.raw_storage_path,
        raw_sha256=robots_fetch.raw_sha256,
        raw_bytes=robots_fetch.body_bytes,
        parsed_rules=parsed_rules,
        sitemap_urls=sitemap_urls,
        crawl_delay_seconds=crawl_delay_seconds,
        error_class=error_class,
        error_message=error_message,
        robots_metadata=robots_metadata,
    )


# EN: This explicit export list documents the public robots child surface.
# TR: Bu açık export listesi public robots alt yüzeyini belgelendirir.
__all__ = [
    "robots_verdict_allows_fetch",
    "parse_persisted_robots_payload",
    "refresh_robots_cache_if_needed",
]
