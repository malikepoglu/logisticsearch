# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because configuration and result objects become much
# EN: easier to inspect when every field is explicit and named.
# TR: Konfigürasyon ve sonuç nesneleri her alan açık ve isimli olduğunda çok
# TR: daha kolay incelendiği için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone so observed timestamps stay explicit and UTC-based.
# TR: Gözlenen zaman damgaları açık ve UTC tabanlı kalsın diye datetime ve timezone
# TR: içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import Path because the worker must read back persisted robots raw bodies
# EN: from disk during the first controlled cache-refresh integration step.
# TR: Worker ilk kontrollü cache-refresh entegrasyon adımında saklanan robots ham
# TR: body'lerini diskten geri okumak zorunda olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import socket because socket-level timeout and transport failures should
# EN: be classified explicitly in the minimal fetch runtime path.
# TR: Socket düzeyi timeout ve taşıma hataları minimal fetch runtime yolunda açıkça
# TR: sınıflandırılmalı diye socket içe aktarıyoruz.
import socket

# EN: We import uuid4 so every worker execution can get a unique run id.
# TR: Her worker çalıştırması benzersiz bir run id alabilsin diye uuid4 içe aktarıyoruz.
from uuid import uuid4

# EN: We import HTTPError and URLError because the minimal fetch flow must separate
# EN: HTTP status failures from lower-level transport failures.
# TR: Minimal fetch akışı HTTP durum hatalarını daha alt düzey taşıma hatalarından
# TR: ayırmak zorunda olduğu için HTTPError ve URLError içe aktarıyoruz.
from urllib.error import HTTPError, URLError

# EN: These DB helpers express the current canonical crawler-core interaction points.
# EN: We now import claim, robots decision/cache helpers, and finalize helpers together.
# TR: Bu DB yardımcıları mevcut kanonik crawler-core etkileşim noktalarını ifade eder.
# TR: Artık claim, robots karar/cache yardımcıları ve finalize yardımcılarını birlikte içe aktarıyoruz.
from .db import (
    claim_next_url,
    close_db,
    commit,
    compute_robots_allow_decision,
    compute_robots_refresh_decision,
    connect_db,
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    finish_fetch_success,
    rollback,
    upsert_robots_txt_cache,
)

# EN: We import the minimal processed-output storage planner because the worker
# EN: must refuse new work when storage policy says normal flow should pause.
# TR: Worker normal akış pause olmalıysa yeni iş almamalı; bu yüzden minimal
# TR: işlenmiş-çıktı storage planlayıcısını içe aktarıyoruz.
from .storage_routing import ProcessedOutputPlan, choose_processed_output_plan

# EN: We import the minimal real fetch helpers and their structured result objects
# EN: because durable worker mode now performs both normal page fetches and robots
# EN: refresh fetches during the first canonical cache-refresh integration step.
# TR: Durable worker modu artık hem normal sayfa fetch'lerini hem de ilk kanonik
# TR: cache-refresh entegrasyon adımındaki robots refresh fetch'lerini yaptığı için
# TR: minimal gerçek fetch yardımcılarını ve yapılı sonuç nesnelerini içe aktarıyoruz.
from .fetch_runtime import (
    FetchedPageResult,
    FetchedRobotsTxtResult,
    decode_robots_body,
    fetch_page_to_raw_storage,
    fetch_robots_txt_to_raw_storage,
    parse_robots_txt_text,
)


# EN: We import the canonical parse helpers here because worker_runtime must use
# EN: the repo-contained parse-apply path instead of ad hoc external snippets.
# TR: Worker runtime artık repository içindeki kanonik parse-apply yolunu
# TR: kullanmak zorunda olduğu için parse yardımcılarını burada içe aktarıyoruz.
from .parse_runtime import MinimalParseApplyResult, apply_minimal_parse_entry


# EN: This dataclass stores runtime configuration for the current worker surface.
# TR: Bu dataclass mevcut worker yüzeyi için runtime konfigürasyonunu tutar.
@dataclass(slots=True)
class WorkerConfig:
    # EN: dsn is the PostgreSQL connection string used by this worker runtime.
    # TR: dsn bu worker runtime tarafından kullanılan PostgreSQL bağlantı metnidir.
    dsn: str

    # EN: worker_id is the textual worker identity passed into frontier.claim_next_url(...).
    # TR: worker_id frontier.claim_next_url(...) içine verilen metinsel worker kimliğidir.
    worker_id: str

    # EN: lease_seconds says how long a claimed lease should stay valid before
    # EN: lease renewal would become necessary.
    # TR: lease_seconds claim edilmiş bir lease'in renewal gerekmeden önce ne kadar
    # TR: süre geçerli kalacağını söyler.
    lease_seconds: int = 600

    # EN: probe_only keeps the worker in non-durable verification mode when True.
    # EN: When False, the worker executes the minimal real fetch + finalize path.
    # TR: probe_only True olduğunda worker'ı kalıcı olmayan doğrulama modunda tutar.
    # TR: False olduğunda worker minimal gerçek fetch + finalize yolunu çalıştırır.
    probe_only: bool = True


# EN: This dataclass stores the result of one worker execution.
# TR: Bu dataclass tek bir worker çalıştırmasının sonucunu tutar.
@dataclass(slots=True)
class ClaimProbeResult:
    # EN: run_id is the unique id of this exact Python-side runtime execution.
    # TR: run_id bu tam Python-tarafı runtime çalıştırmasının benzersiz kimliğidir.
    run_id: str

    # EN: claimed tells whether a claimable row was actually returned.
    # TR: claimed gerçekten claim edilebilir bir satır dönüp dönmediğini söyler.
    claimed: bool

    # EN: claimed_url stores the claimed row object when a claim succeeded.
    # TR: claimed_url claim başarılıysa claim edilen satır nesnesini tutar.
    claimed_url: object | None

    # EN: robots_allow_decision stores the current visible robots allow/block
    # EN: decision for the claimed row when a claim succeeded.
    # TR: robots_allow_decision claim başarılıysa claim edilen satır için mevcut
    # TR: görünür robots allow/block kararını tutar.
    robots_allow_decision: dict | None

    # EN: storage_plan stores the current minimal processed-output storage decision.
    # TR: storage_plan mevcut minimal işlenmiş-çıktı storage kararını tutar.
    storage_plan: ProcessedOutputPlan

    # EN: fetched_page stores the structured raw fetch result when a real fetch ran.
    # TR: fetched_page gerçek bir fetch çalıştıysa yapılı ham fetch sonucunu tutar.
    fetched_page: FetchedPageResult | None

    # EN: finalize_result stores the canonical finalize SQL result when the worker
    # EN: reached a durable finalize decision.
    # TR: finalize_result worker kalıcı bir finalize kararına ulaştıysa kanonik
    # TR: finalize SQL sonucunu tutar.
    finalize_result: dict | None

    # EN: parse_apply_result stores the canonical minimal parse-apply DB results
    # EN: when the current runtime reaches that stage.
    # TR: parse_apply_result mevcut runtime bu aşamaya ulaştığında kanonik minimal
    # TR: parse-apply DB sonuçlarını tutar.
    parse_apply_result: MinimalParseApplyResult | None

    # EN: observed_at records when this result object was produced.
    # TR: observed_at bu sonuç nesnesinin ne zaman üretildiğini kaydeder.
    observed_at: str


# EN: This helper creates a unique runtime execution id.
# TR: Bu yardımcı benzersiz bir runtime çalıştırma kimliği üretir.
def new_run_id() -> str:
    # EN: We convert uuid4() to string because string ids are easier to print,
    # EN: inspect, and serialize in beginner-facing controlled surfaces.
    # TR: uuid4() sonucunu metne çeviriyoruz; çünkü metinsel kimlikler beginner
    # TR: odaklı kontrollü yüzeylerde yazdırmak, incelemek ve serileştirmek için daha kolaydır.
    return str(uuid4())


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı ISO-8601 biçiminde UTC timestamp metni döndürür.
def utc_now_iso() -> str:
    # EN: We use timezone.utc so output never depends on a machine-local timezone.
    # TR: Çıktı makineye özgü yerel saat dilimine bağlı kalmasın diye timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc).isoformat()


# EN: This helper reads a named field from either a dict-like claimed row or an
# EN: attribute-style claimed row object.
# TR: Bu yardımcı named bir alanı dict-benzeri claim satırından veya attribute-stili
# TR: claim satırı nesnesinden okur.
def claimed_url_value(claimed_url: object, field_name: str) -> object:
    # EN: If the claimed row is dict-like, we read the key directly.
    # TR: Claim satırı dict-benzeri ise anahtarı doğrudan okuyoruz.
    if isinstance(claimed_url, dict):
        if field_name not in claimed_url:
            raise KeyError(f"claimed_url is missing key: {field_name}")
        return claimed_url[field_name]

    # EN: Otherwise we fall back to attribute access.
    # TR: Aksi durumda attribute erişimine geri düşüyoruz.
    if not hasattr(claimed_url, field_name):
        raise AttributeError(f"claimed_url is missing attribute: {field_name}")

    # EN: We return the discovered attribute value.
    # TR: Bulunan attribute değerini döndürüyoruz.
    return getattr(claimed_url, field_name)


# EN: This helper decides whether the current robots verdict still allows the
# EN: minimal worker to perform a real page fetch.
# TR: Bu yardımcı mevcut robots verdict'inin minimal worker'ın gerçek page fetch
# TR: yapmasına hâlâ izin verip vermediğini belirler.
def robots_verdict_allows_fetch(verdict: str | None) -> bool:
    # EN: The current minimal worker treats these verdicts as fetch-allowed:
    # EN: explicit allow, allow with refresh recommendation, and ignore-mode allow.
    # TR: Güncel minimal worker şu verdict'leri fetch-allowed sayar:
    # TR: açık allow, refresh tavsiyesiyle allow ve ignore-mode allow.
    return verdict in {
        "allow",
        "allow_but_refresh_recommended",
        "allow_mode_ignore",
    }


# EN: This helper classifies HTTP status failures into minimal retryable vs permanent buckets.
# TR: Bu yardımcı HTTP durum hatalarını minimal retryable ve permanent kovalarına ayırır.
def classify_http_status_failure(http_status: int) -> tuple[str, bool]:
    # EN: These status codes are commonly retryable because they usually represent
    # EN: temporary overload, timeout, or transient upstream failure.
    # TR: Bu durum kodları genelde retryable kabul edilir; çünkü çoğu zaman geçici
    # TR: aşırı yük, timeout veya geçici upstream hatasını temsil eder.
    if http_status in {408, 425, 429, 500, 502, 503, 504}:
        return ("http_retryable_status", True)

    # EN: All remaining HTTP error statuses are treated as permanent for this minimal layer.
    # TR: Kalan tüm HTTP hata durumları bu minimal katmanda permanent kabul edilir.
    return ("http_permanent_status", False)


# EN: This helper finalizes a robots-blocked claim with a permanent outcome.
# EN: The project does not yet expose a dedicated robots-blocked finalize function,
# EN: so the minimal layer uses the permanent-error finalize path with an explicit class.
# TR: Bu yardımcı robots tarafından engellenmiş bir claim'i permanent sonuçla finalize eder.
# TR: Proje henüz dedicated bir robots-blocked finalize fonksiyonu göstermediği için
# TR: minimal katman açık bir hata sınıfıyla permanent-error finalize yolunu kullanır.
def finalize_robots_block(
    conn,
    *,
    claimed_url: object,
    robots_allow_decision: dict | None,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We read the visible verdict mainly so the stored error message remains explicit.
    # TR: Saklanan hata mesajı açık kalsın diye görünür verdict'i okuyoruz.
    verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

    # EN: We call the permanent finalize wrapper with an explicit robots_blocked class.
    # TR: Açık bir robots_blocked sınıfıyla permanent finalize wrapper'ını çağırıyoruz.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="robots_blocked",
        error_message=f"robots verdict forbids fetch: {verdict}",
    )


# EN: This helper finalizes an HTTP error according to the minimal retryable/permanent rule.
# TR: Bu yardımcı bir HTTP hatasını minimal retryable/permanent kuralına göre finalize eder.
def finalize_http_error(
    conn,
    *,
    claimed_url: object,
    http_status: int,
    error_message: str,
) -> dict:
    # EN: We classify the status code first so the finalize branch stays explicit.
    # TR: Finalize dalı açık kalsın diye önce durum kodunu sınıflandırıyoruz.
    error_class, is_retryable = classify_http_status_failure(http_status)

    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: Retryable statuses go through the retryable finalize wrapper.
    # TR: Retryable durumlar retryable finalize wrapper üzerinden gider.
    if is_retryable:
        return finish_fetch_retryable_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=error_class,
            error_message=error_message,
            retry_delay=None,
        )

    # EN: All other HTTP failure statuses go through the permanent finalize wrapper.
    # TR: Diğer tüm HTTP hata durumları permanent finalize wrapper üzerinden gider.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=http_status,
        error_class=error_class,
        error_message=error_message,
    )


# EN: This helper finalizes a lower-level transport failure as retryable.
# TR: Bu yardımcı daha alt düzey bir taşıma hatasını retryable olarak finalize eder.
def finalize_transport_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We use the retryable finalize wrapper because transport failures are
    # EN: typically transient in this minimal first implementation.
    # TR: Bu minimal ilk implementasyonda taşıma hataları tipik olarak geçici kabul
    # TR: edildiği için retryable finalize wrapper'ını kullanıyoruz.
    return finish_fetch_retryable_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="transport_retryable_error",
        error_message=error_message,
        retry_delay=None,
    )


# EN: This helper finalizes an unexpected runtime failure as permanent.
# TR: Bu yardımcı beklenmeyen bir runtime hatasını permanent olarak finalize eder.
def finalize_unexpected_runtime_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We use the permanent finalize wrapper because an unknown runtime error
    # EN: should not be silently retried by this minimal layer.
    # TR: Bilinmeyen bir runtime hatası bu minimal katman tarafından sessizce
    # TR: retry edilmemeli diye permanent finalize wrapper'ını kullanıyoruz.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="unexpected_fetch_runtime_error",
        error_message=error_message,
    )


# EN: This helper reads one persisted robots raw body back from disk and turns it
# EN: into the narrow parsed payload shape already expected by the DB cache-upsert surface.
# TR: Bu yardımcı saklanan tek bir robots ham body'sini diskten geri okur ve bunu
# TR: DB cache-upsert yüzeyinin zaten beklediği dar parse payload şekline dönüştürür.
# EN: This helper converts a persisted robots fetch result into the narrow parsed payload shape expected by the current DB cache contract.
# TR: Bu yardımcı, saklanmış robots fetch sonucunu mevcut DB cache sözleşmesinin beklediği dar parse payload şekline dönüştürür.
def parse_persisted_robots_payload(
    robots_fetch: FetchedRobotsTxtResult,
) -> tuple[dict, list[str], float | None]:
    # EN: The persisted raw path must exist here because this helper is only called
    # EN: for HTTP-result paths that actually wrote a visible raw body.
    # TR: Bu yardımcı yalnızca görünür ham body gerçekten yazılmış HTTP-sonuç yollarında
    # TR: çağrıldığı için burada saklanan ham yolun mevcut olması gerekir.
    raw_storage_path = robots_fetch.raw_storage_path
    if raw_storage_path is None:
        raise RuntimeError("robots fetch returned no raw_storage_path for payload parsing")

    # EN: We read the exact persisted bytes so worker-side parsing is derived from
    # EN: the same durable artefact later audits can inspect.
    # TR: Worker tarafı parse işlemi daha sonra audit'lerin inceleyebileceği aynı
    # TR: kalıcı artefact'tan türesin diye tam saklanan byte'ları okuyoruz.
    robots_body = Path(raw_storage_path).read_bytes()

    # EN: We decode through the sealed helper so encoding tolerance remains consistent.
    # TR: Encoding toleransı tutarlı kalsın diye mühürlü yardımcı üzerinden decode ediyoruz.
    robots_text = decode_robots_body(robots_body)

    # EN: We return the current narrow parsed payload shape expected by DB upsert.
    # TR: DB upsert'in beklediği güncel dar parse payload şeklini döndürüyoruz.
    return parse_robots_txt_text(robots_text)


# EN: This helper performs the first controlled worker-side robots cache refresh write.
# EN: It fetches robots.txt when refresh is needed, derives the narrow payload shape,
# EN: and persists the resulting cache truth through the canonical DB wrapper.
# TR: Bu yardımcı ilk kontrollü worker-tarafı robots cache refresh yazımını yapar.
# TR: Refresh gerektiğinde robots.txt dosyasını fetch eder, dar payload şeklini çıkarır
# TR: ve ortaya çıkan cache doğrusunu kanonik DB wrapper üzerinden yazar.
# EN: This helper performs one controlled robots refresh cycle and writes the resulting cache truth back through the canonical DB wrapper.
# TR: Bu yardımcı tek bir kontrollü robots refresh döngüsü çalıştırır ve ortaya çıkan cache doğrusunu kanonik DB wrapper üzerinden geri yazar.
def refresh_robots_cache_if_needed(
    conn,
    *,
    claimed_url: object,
    refresh_decision: dict,
) -> dict:
    # EN: We extract the host identity because refresh is a host-level operation.
    # TR: Refresh host-seviyesinde bir işlem olduğu için host kimliğini çıkarıyoruz.
    host_id = int(claimed_url_value(claimed_url, "host_id"))

    # EN: We read the robots URL from the DB refresh-decision row because the SQL
    # EN: contract is already the source of truth for that target.
    # TR: SQL sözleşmesi bu hedef için zaten doğruluk kaynağı olduğu için robots URL'yi
    # TR: DB refresh-decision satırından okuyoruz.
    robots_url = refresh_decision.get("robots_url")
    if robots_url is None or str(robots_url).strip() == "":
        raise RuntimeError("compute_robots_refresh_decision(...) returned empty robots_url")

    # EN: We reuse the claimed row's user-agent token so robots refresh uses the
    # EN: same explicit crawler identity as the page-fetch path.
    # TR: Robots refresh yolu sayfa-fetch yolu ile aynı açık crawler kimliğini
    # TR: kullansın diye claimed satırın user-agent token'ını yeniden kullanıyoruz.
    user_agent_token = str(claimed_url_value(claimed_url, "user_agent_token"))

    # EN: We perform the real robots fetch through the canonical fetch helper.
    # TR: Gerçek robots fetch işlemini kanonik fetch yardımcısı üzerinden yapıyoruz.
    robots_fetch = fetch_robots_txt_to_raw_storage(
        host_id=host_id,
        robots_url=str(robots_url),
        user_agent_token=user_agent_token,
    )

    # EN: We convert the returned ISO timestamp back to a datetime so psycopg can
    # EN: pass an explicit timestamptz-compatible value into the DB wrapper.
    # TR: psycopg açık timestamptz-uyumlu bir değer geçebilsin diye dönen ISO zamanını
    # TR: tekrar datetime nesnesine çeviriyoruz.
    fetched_at_value = datetime.fromisoformat(robots_fetch.fetched_at)

    # EN: We preserve a small visible metadata payload so later inspection can see
    # EN: where the robots fetch actually landed.
    # TR: Daha sonraki inceleme gerçek robots fetch'in nereye indiğini görebilsin
    # TR: diye küçük bir görünür metadata payload'ı koruyoruz.
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

    # EN: We start from an explicit empty parsed payload and then fill it only for
    # EN: genuinely cacheable success-class HTTP outcomes.
    # TR: Açık bir boş parse payload'ı ile başlıyor ve bunu yalnızca gerçekten
    # TR: cache'lenebilir başarı-sınıfı HTTP sonuçlarında dolduruyoruz.
    parsed_rules: dict = {}
    sitemap_urls: list = []
    crawl_delay_seconds = None
    cache_state = "fresh"
    error_class = None
    error_message = None

    # EN: HTTP 404 is treated as a missing robots file rather than a generic fetch error.
    # TR: HTTP 404 genel fetch hatası yerine eksik robots dosyası olarak ele alınır.
    if robots_fetch.http_status == 404:
        cache_state = "missing"

    # EN: Success-class HTTP outcomes are parsed into the narrow disallow/sitemap/crawl-delay model.
    # TR: Başarı-sınıfı HTTP sonuçları dar disallow/sitemap/crawl-delay modeline parse edilir.
    elif robots_fetch.http_status is not None and 200 <= robots_fetch.http_status < 400:
        parsed_rules, sitemap_urls, crawl_delay_seconds = parse_persisted_robots_payload(robots_fetch)
        cache_state = "fresh"

    # EN: All other HTTP outcomes are persisted as explicit robots HTTP errors.
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


# EN: This function performs one worker execution.
# EN: In probe mode it still rolls back safely.
# EN: In durable mode it now executes the minimal real fetch + finalize flow.
# TR: Bu fonksiyon tek bir worker çalıştırması yapar.
# TR: Probe modunda hâlâ güvenli rollback yapar.
# TR: Durable modda artık minimal gerçek fetch + finalize akışını çalıştırır.
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We create a unique run id first so the full execution can be traced.
    # TR: Tüm çalıştırma izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    run_id = new_run_id()

    # EN: We compute the current storage plan before touching the DB because the
    # EN: crawler must not claim new work when storage policy says it should pause.
    # TR: Crawler storage politikası pause diyorsa yeni iş claim etmemeli; bu yüzden
    # TR: DB'ye dokunmadan önce mevcut storage planı hesaplıyoruz.
    storage_plan = choose_processed_output_plan()


    # EN: We start with no parse-apply result because parse continuation should
    # EN: appear only after a successful fetch/finalize path reaches that stage.
    # TR: Parse continuation yalnızca başarılı fetch/finalize yolu o aşamaya
    # TR: ulaşınca ortaya çıkması gerektiği için başlangıçta parse-apply sonucu yoktur.
    parse_apply_result = None

    # EN: If storage says pause, we stop here deliberately and return a structured result.
    # TR: Storage pause diyorsa bilinçli olarak burada duruyor ve yapılı bir sonuç döndürüyoruz.
    if storage_plan.pause_crawler:
        return ClaimProbeResult(
            run_id=run_id,
            claimed=False,
            claimed_url=None,
            robots_allow_decision=None,
            storage_plan=storage_plan,
            fetched_page=None,
            finalize_result=None,
            parse_apply_result=parse_apply_result,
            observed_at=utc_now_iso(),
        )

    # EN: Only after storage allows normal flow do we open a DB connection.
    # TR: Ancak storage normal akışa izin verdikten sonra DB bağlantısı açıyoruz.
    conn = connect_db(config.dsn)

    try:
        # EN: We ask crawler-core for exactly one claimable row.
        # TR: crawler-core'dan tam olarak bir claim edilebilir satır istiyoruz.
        claimed_url = claim_next_url(
            conn=conn,
            worker_id=config.worker_id,
            lease_seconds=config.lease_seconds,
        )

        # EN: If nothing is currently claimable, we rollback and return a structured result.
        # TR: Şu anda claim edilebilir hiçbir şey yoksa rollback yapıyor ve yapılı sonuç döndürüyoruz.
        if claimed_url is None:
            rollback(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=None,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )

        # EN: We extract the host/path pair once because refresh-decision and
        # EN: allow-decision are both anchored to the same claimed target.
        # TR: Refresh-decision ve allow-decision aynı claimed hedefe bağlı olduğu için
        # TR: host/path çiftini bir kez çıkarıyoruz.
        claimed_host_id = int(claimed_url_value(claimed_url, "host_id"))
        claimed_url_path = str(claimed_url_value(claimed_url, "url_path"))

        # EN: We inspect the canonical DB-side refresh decision first because the
        # EN: worker contract says robots cache truth must be refreshed when needed.
        # TR: Worker sözleşmesi gerektiğinde robots cache doğrusunun yenilenmesini
        # TR: söylediği için önce kanonik DB-tarafı refresh kararını inceliyoruz.
        refresh_decision = compute_robots_refresh_decision(
            conn=conn,
            host_id=claimed_host_id,
        )

        # EN: A missing row would mean the sealed DB decision surface behaved unexpectedly.
        # TR: Satır dönmemesi mühürlü DB karar yüzeyinin beklenmedik davrandığı anlamına gelir.
        if refresh_decision is None:
            raise RuntimeError("compute_robots_refresh_decision(...) returned no row")

        # EN: Probe mode stays non-durable, so it may observe refresh need but must not
        # EN: write refreshed cache truth back into the database.
        # TR: Probe modu kalıcı olmayan mod olarak kalır; bu yüzden refresh ihtiyacını
        # TR: gözleyebilir ama yenilenmiş cache doğrusunu veritabanına yazmamalıdır.
        if (not config.probe_only) and refresh_decision.get("should_refresh"):
            refresh_robots_cache_if_needed(
                conn,
                claimed_url=claimed_url,
                refresh_decision=refresh_decision,
            )

        # EN: After any needed durable refresh write, we ask for the current visible
        # EN: robots allow/block decision for the claimed path.
        # TR: Gereken kalıcı refresh yazımı sonrası claimed path için mevcut görünür
        # TR: robots allow/block kararını soruyoruz.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_host_id,
            url_path=claimed_url_path,
        )

        # EN: Probe mode stays non-durable: claim + robots checks are observed and then rolled back.
        # TR: Probe modu kalıcı olmayan mod olarak kalır: claim + robots kontrolleri gözlenir ve sonra rollback edilir.
        if config.probe_only:
            rollback(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=None,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )

        # EN: In durable mode we inspect the robots verdict before any real page fetch is attempted.
        # TR: Durable modda gerçek sayfa fetch'i denenmeden önce robots verdict'ini inceliyoruz.
        robots_verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

        # EN: If robots forbids fetch, we finalize immediately through the minimal
        # EN: robots-block permanent path and commit that durable result.
        # TR: Robots fetch'i yasaklıyorsa minimal robots-block permanent yolu üzerinden
        # TR: hemen finalize ediyor ve bu kalıcı sonucu commit ediyoruz.
        if not robots_verdict_allows_fetch(robots_verdict):
            finalize_result = finalize_robots_block(
                conn,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )

        # EN: If robots allows fetch, we execute the minimal real HTTP fetch plus raw-body write.
        # TR: Robots fetch'e izin veriyorsa minimal gerçek HTTP fetch ve ham body yazımını çalıştırıyoruz.
        try:
            fetched_page = fetch_page_to_raw_storage(claimed_url)

            # EN: A successful fetch is finalized through the canonical success wrapper.
            # TR: Başarılı fetch kanonik success wrapper üzerinden finalize edilir.
            finalize_result = finish_fetch_success(
                conn,
                url_id=fetched_page.url_id,
                lease_token=str(claimed_url_value(claimed_url, "lease_token")),
                http_status=fetched_page.http_status,
                content_type=fetched_page.content_type,
                body_bytes=fetched_page.body_bytes,
                etag=fetched_page.etag,
                last_modified=fetched_page.last_modified,
            )


            # EN: We only run the minimal parse-apply helper for HTML-like successful
            # EN: fetches because the current narrow parse layer is intentionally HTML-first.
            # TR: Mevcut dar parse katmanı bilinçli olarak HTML-öncelikli olduğu için
            # TR: minimal parse-apply yardımcısını yalnızca HTML-benzeri başarılı fetch'lerde çalıştırıyoruz.
            should_run_minimal_parse = (
                fetched_page.content_type is None
                or "html" in fetched_page.content_type.lower()
            )

            # EN: When the fetched content is suitable, we continue through the
            # EN: canonical repo-contained parse helper instead of ad hoc external code.
            # TR: Fetch edilen içerik uygunsa, geçici dış kod yerine repository içindeki
            # TR: kanonik parse yardımcısı üzerinden devam ediyoruz.
            if should_run_minimal_parse:
                parse_apply_result = apply_minimal_parse_entry(
                    conn=conn,
                    url_id=claimed_url.url_id,
                    raw_storage_path=fetched_page.raw_storage_path,
                    source_run_id=run_id,
                    source_note="minimal parse continuation from worker runtime success path",
                )

                # EN: We commit so the claim, raw-fetch success finalize, and lease resolution
                # EN: become durable together.
                # TR: Claim, raw-fetch success finalize ve lease çözümü birlikte kalıcı olsun
                # TR: diye commit ediyoruz.
                commit(conn)

                return ClaimProbeResult(
                    run_id=run_id,
                    claimed=True,
                    claimed_url=claimed_url,
                    robots_allow_decision=robots_allow_decision,
                    storage_plan=storage_plan,
                    fetched_page=fetched_page,
                    finalize_result=finalize_result,
                    parse_apply_result=parse_apply_result,
                    observed_at=utc_now_iso(),
                )

        # EN: HTTPError means the server answered with an explicit HTTP failure status.
        # TR: HTTPError sunucunun açık bir HTTP hata durumu ile yanıt verdiği anlamına gelir.
        except HTTPError as exc:
            finalize_result = finalize_http_error(
                conn,
                claimed_url=claimed_url,
                http_status=int(exc.code),
                error_message=f"HTTPError {exc.code}: {exc.reason}",
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )

        # EN: URLError, socket timeout, and timeout-like transport failures are treated
        # EN: as retryable by the minimal first implementation.
        # TR: URLError, socket timeout ve timeout-benzeri taşıma hataları minimal ilk
        # TR: implementasyonda retryable kabul edilir.
        except (URLError, TimeoutError, socket.timeout) as exc:
            finalize_result = finalize_transport_error(
                conn,
                claimed_url=claimed_url,
                error_message=f"{type(exc).__name__}: {exc}",
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )

        # EN: Any other unexpected fetch/runtime failure is finalized as permanent
        # EN: so the minimal layer fails loudly instead of hiding unknown behavior.
        # TR: Diğer tüm beklenmeyen fetch/runtime hataları minimal katman bilinmeyen
        # TR: davranışı gizlemesin diye permanent olarak finalize edilir.
        except Exception as exc:
            finalize_result = finalize_unexpected_runtime_error(
                conn,
                claimed_url=claimed_url,
                error_message=f"{type(exc).__name__}: {exc}",
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
            )
    finally:
        # EN: We always close the connection even if an error occurs.
        # TR: Hata oluşsa bile bağlantıyı her durumda kapatıyoruz.
        close_db(conn)
